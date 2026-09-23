"""Exporte le modèle retenu en §6.1 vers l'artefact servi par le service `model`.

Rejoue **hors notebook** (Phase 3 close, le notebook n'est pas modifié) la
dernière étape d'industrialisation : copier le pipeline final vers
``services/model/models/emploi_retour_s1.joblib`` et écrire à côté le
``emploi_retour_s1.json`` que ``app.model_loader`` lit au démarrage.

Deux points méritent d'être explicités, parce qu'ils sont la raison d'être de ce
script plutôt que d'un simple ``copy`` :

1. **``famille_thematique`` est désormais une colonne catégorielle** (§4.2.2) et
   non plus du texte libre : elle figure donc dans
   ``feature_columns_categorical`` et devient un champ d'entrée de l'API.
2. **``nationalite_hors_ue`` est neutralisée en production.** Le pipeline retenu
   la consomme (cf. ``SCENARIO_FEATURES["s1"]``), mais l'API ne la demande pas :
   le service injecte une valeur constante (``NATIONALITE_HORS_UE_NEUTRE``) avant
   l'inférence, si bien qu'aucun usager n'est traité différemment selon sa
   nationalité. Les métriques écrites dans ``metrics_holdout`` sont recalculées
   **avec ce forçage**, pour décrire le modèle réellement servi et non celui du
   notebook. Les métriques du notebook sont conservées sous
   ``metrics_holdout_notebook`` pour rendre l'écart mesurable.

Usage::

    python scripts/export_model_prod.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import sklearn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preprocess import (  # noqa: E402
    NATIONALITE_COLUMN,
    NATIONALITE_HORS_UE_NEUTRE,
    ROOT,
    TARGET_COLUMN,
    build_features,
    build_served_features,
    load_dataset,
    split_train_holdout,
)
from src import metrics as metrics_module  # noqa: E402
from src import pipeline_tabulaire  # noqa: E402

# Modèle retenu en §5.6/§6.1 et évalué une seule fois sur le test set
# (cf. evaluation_finale.md) : S1 / RandomForestClassifier(n_estimators=300).
SOURCE_MODEL_PATH = (
    ROOT / "models" / "modele_final_s1_RandomForestClassifier__n_estimators_300_.joblib"
)
SOURCE_META_PATH = SOURCE_MODEL_PATH.with_suffix(".metadata.json")

SERVED_DIR = ROOT / "services" / "model" / "models"
SERVED_MODEL_PATH = SERVED_DIR / "emploi_retour_s1.joblib"
SERVED_META_PATH = SERVED_DIR / "emploi_retour_s1.json"

MODEL_NAME = "emploi_retour_s1"
MODEL_VERSION = "v2.0.0"  # majeure : le contrat d'entrée de /predict change.

CLASSES = {
    "0": "retour_rapide",
    "1": "retour_standard",
    "2": "a_risque",
}

REPORTED_METRICS = (
    "accuracy",
    "f1_macro",
    "recall_classe_2",
    "f1_classe_2",
    "taux_erreur_grave_2_vers_0",
    "taux_erreur_0_vers_2",
)


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):  # pragma: no cover - hors CI
        return None


def holdout_metrics(model, holdout, *, neutraliser_nationalite: bool) -> dict[str, float]:
    """Métriques §1.4 sur le holdout §4.1 (500 lignes jamais vues à l'entraînement).

    ``neutraliser_nationalite`` reproduit le comportement du service : la colonne
    est écrasée par ``NATIONALITE_HORS_UE_NEUTRE`` avant l'appel à ``predict``.
    """
    prepare = build_served_features if neutraliser_nationalite else build_features
    computed = metrics_module.compute_classification_metrics(
        holdout[TARGET_COLUMN].astype(int), model.predict(prepare(holdout))
    )
    return {name: round(float(computed[name]), 4) for name in REPORTED_METRICS}


def main() -> int:
    if not SOURCE_MODEL_PATH.exists():
        raise SystemExit(
            f"{SOURCE_MODEL_PATH} est absent : rejouez §6.1 du notebook avant cet export."
        )

    source_meta = json.loads(SOURCE_META_PATH.read_text(encoding="utf-8"))
    model = joblib.load(SOURCE_MODEL_PATH)

    _, holdout = split_train_holdout(load_dataset())
    metrics_servies = holdout_metrics(model, holdout, neutraliser_nationalite=True)
    metrics_notebook = holdout_metrics(model, holdout, neutraliser_nationalite=False)

    features = list(pipeline_tabulaire.get_scenario_features("s1"))
    numeriques = [f for f in features if f in pipeline_tabulaire.NUMERIC_FEATURES]
    categorielles = [f for f in features if f not in numeriques]

    metadata = {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "scenario": "s1",
        "algorithm": source_meta["modele"],
        "feature_columns_numeric": numeriques,
        "feature_columns_categorical": categorielles,
        # Colonnes attendues par le pipeline mais NON demandées à l'appelant :
        # le service les injecte lui-même (cf. app.schemas / app.main).
        "feature_columns_forced": {NATIONALITE_COLUMN: NATIONALITE_HORS_UE_NEUTRE},
        "classes": CLASSES,
        "metrics_holdout": metrics_servies,
        "metrics_holdout_notebook": metrics_notebook,
        "metrics_note": (
            "metrics_holdout mesure le modèle tel qu'il est servi, "
            f"{NATIONALITE_COLUMN} forcée à {NATIONALITE_HORS_UE_NEUTRE} ; "
            "metrics_holdout_notebook conserve la mesure §6.1 avec la nationalité réelle."
        ),
        "regles_validation_manuelle": source_meta["regles_validation_manuelle"],
        "source_model": SOURCE_MODEL_PATH.name,
        "trained_at": source_meta["date_persistance"],
        "sklearn_version": sklearn.__version__,
        "git_commit": git_commit(),
        "dataset_sha256": None,
    }

    SERVED_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_MODEL_PATH, SERVED_MODEL_PATH)
    SERVED_META_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"{SOURCE_MODEL_PATH.name} → {SERVED_MODEL_PATH}")
    print(f"Métadonnées → {SERVED_META_PATH}")
    print(f"\nMétriques holdout (servies, {NATIONALITE_COLUMN}={NATIONALITE_HORS_UE_NEUTRE}) :")
    for name, value in metrics_servies.items():
        ecart = value - metrics_notebook[name]
        print(f"  {name:28s} = {value:.4f}   (notebook {metrics_notebook[name]:.4f}, Δ {ecart:+.4f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
