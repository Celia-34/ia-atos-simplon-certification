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
2. **``nationalite_hors_ue`` est une feature d'entrée à part entière.**
   L'arbitrage métier et juridique ``J0`` a validé son usage : le service la
   reçoit de l'appelant et ne la réécrit plus. Il n'existe donc qu'**un seul
   jeu de métriques**, celui du notebook (§5.6.2 / §6.1 / §7.1 / §7.2), et
   ``metrics_holdout`` doit être strictement égal à ``evaluation_finale.md``
   et à ``models/modele_final_s1_*.metadata.json::metriques_test``.

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
    ROOT,
    TARGET_COLUMN,
    build_features,
    load_dataset,
    split_train_holdout,
)
from src import metrics as metrics_module  # noqa: E402
from src import pipeline_tabulaire  # noqa: E402

# Modèle retenu en §5.6/§6.1 et évalué une seule fois sur le test set
# (cf. evaluation_finale.md) : S1 / RandomForestClassifier(n_estimators=300,
# class_weight="balanced", random_state=42).
SOURCE_MODEL_PATH = (
    ROOT / "models" / "modele_final_s1_RandomForestClassifier__n_estimators_300_.joblib"
)
SOURCE_META_PATH = SOURCE_MODEL_PATH.with_suffix(".metadata.json")

SERVED_DIR = ROOT / "services" / "model" / "models"
SERVED_MODEL_PATH = SERVED_DIR / "emploi_retour_s1.joblib"
SERVED_META_PATH = SERVED_DIR / "emploi_retour_s1.json"

MODEL_NAME = "emploi_retour_s1"
# Majeure : `nationalite_hors_ue` redevient un champ requis de /predict — le
# contrat d'entrée passe de 7 à 8 champs, un client v2.0.0 reçoit désormais 422.
MODEL_VERSION = "v3.0.0"

# Paramètres du classifieur dont le descripteur textuel doit rendre compte.
# `class_weight="balanced"` était porté par la lambda de `MODELES_FINALISTES`
# mais absent du descripteur `"n_estimators=300"` propagé dans les livrables
# (#13) : on le relit sur l'estimateur réellement entraîné plutôt que de le
# recopier, pour que le fichier servi ne puisse plus mentir sur sa propre
# configuration.
ALGORITHM_PARAMS = ("n_estimators", "class_weight", "random_state")

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


def describe_algorithm(model) -> str:
    """Descripteur exact du classifieur final, relu sur l'estimateur entraîné."""
    estimator = model.named_steps["model"] if hasattr(model, "named_steps") else model
    params = estimator.get_params()
    rendered = ", ".join(
        f"{name}={params[name]!r}" for name in ALGORITHM_PARAMS if name in params
    )
    return f"{type(estimator).__name__}({rendered})"


def holdout_metrics(model, holdout) -> dict[str, float]:
    """Métriques §1.4 sur le holdout §4.1 (500 lignes jamais vues à l'entraînement).

    Calculées sur ``build_features``, donc avec la nationalité réelle : le
    service n'applique plus aucune transformation entre le payload et le
    pipeline, ces chiffres sont ceux du modèle servi **et** ceux du notebook.
    """
    computed = metrics_module.compute_classification_metrics(
        holdout[TARGET_COLUMN].astype(int), model.predict(build_features(holdout))
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
    metrics_holdout = holdout_metrics(model, holdout)

    features = list(pipeline_tabulaire.get_scenario_features("s1"))
    numeriques = [f for f in features if f in pipeline_tabulaire.NUMERIC_FEATURES]
    categorielles = [f for f in features if f not in numeriques]

    metadata = {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "scenario": "s1",
        "algorithm": describe_algorithm(model),
        "feature_columns_numeric": numeriques,
        "feature_columns_categorical": categorielles,
        "classes": CLASSES,
        "metrics_holdout": metrics_holdout,
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
    print(f"Algorithme  : {metadata['algorithm']}")
    print(f"Version     : {MODEL_VERSION}")

    # Concordance avec la source de vérité (#14) : l'export échoue plutôt que de
    # produire un troisième jeu de chiffres sur « le modèle final ».
    reference = source_meta["metriques_test"]
    ecarts = {
        name: (value, round(float(reference[name]), 4))
        for name, value in metrics_holdout.items()
        if name in reference and value != round(float(reference[name]), 4)
    }
    print("\nMétriques holdout (nationalité réelle) :")
    for name, value in metrics_holdout.items():
        print(f"  {name:28s} = {value:.4f}")
    if ecarts:
        raise SystemExit(
            "Divergence avec "
            f"{SOURCE_META_PATH.name}::metriques_test : {ecarts}"
        )
    print(f"\nConcordance vérifiée avec {SOURCE_META_PATH.name}::metriques_test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
