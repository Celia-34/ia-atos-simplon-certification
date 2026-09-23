"""Construit `data/prod_scored.csv` : le journal des dossiers scorés en production.

C'est la table à laquelle `POST /feedback` se rattache par ``request_id`` : un
feedback dont le ``request_id`` est absent d'ici est une jointure cassée, et le
service répond 404. Chaque ligne porte donc à la fois les **features** du
dossier (rejouées à l'identique par le retrain) et la **prédiction** servie.

Le trafic provient de la part du holdout non réservée au jeu de référence
(cf. `preprocess.split_holdout`) : 150 dossiers jamais vus à l'entraînement et
disjoints du jeu qui arbitre la promotion.

`data/feedbacks_simules.csv` accompagne le journal : 100 annotations prêtes à
être rejouées vers `POST /feedback` pour dérouler la boucle sans attendre de
vrais conseillers. La « vérité terrain » y est la classe réelle du dossier,
conservée dans `prod_scored.csv` — en production elle viendrait d'un conseiller.

Usage::

    python scripts/build_prod_scored.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import joblib
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preprocess import (  # noqa: E402
    DATA,
    FEATURES,
    TARGET_COLUMN,
    build_features,
    load_dataset,
    split_holdout,
    split_train_holdout,
)

PROD_SCORED_PATH = DATA / "prod_scored.csv"
SIMULATED_FEEDBACK_PATH = DATA / "feedbacks_simules.csv"
PRODUCTION_PATH = (
    Path(__file__).resolve().parent.parent
    / "services"
    / "model"
    / "models"
    / "emploi_retour_s1.joblib"
)
PRODUCTION_META_PATH = PRODUCTION_PATH.with_suffix(".json")

N_SIMULATED_FEEDBACK = 100
FIRST_TIMESTAMP = datetime(2026, 9, 1, 8, 0, tzinfo=timezone.utc)
TIMESTAMP_STEP = timedelta(hours=1)


def main() -> int:
    if not PRODUCTION_PATH.exists():
        raise SystemExit(f"{PRODUCTION_PATH} est absent : impossible de scorer le trafic.")

    dataset = load_dataset()
    _, holdout = split_train_holdout(dataset)
    _, production_slice = split_holdout(holdout)
    production_slice = production_slice.reset_index(drop=True)

    model = joblib.load(PRODUCTION_PATH)
    metadata = json.loads(PRODUCTION_META_PATH.read_text(encoding="utf-8"))
    features = build_features(production_slice)
    # Scoré dans les conditions de service : depuis l'alignement `v3.0.0` le
    # service reçoit `nationalite_hors_ue` de l'appelant et ne la réécrit pas.
    # Le journal porte donc exactement les features vues par l'API.
    predictions = model.predict(features)
    probabilities = model.predict_proba(features)

    # `departement` (dérivé de `code_insee_commune`) et `famille_thematique` (dérivée du
    # texte via le référentiel figé) n'existent que dans les features : le journal doit
    # les porter pour que le retrain rejoue les mêmes colonnes que celles servies.
    scored = production_slice.assign(
        departement=features["departement"],
        famille_thematique=features["famille_thematique"],
        request_id=[f"REQ-{index:05d}" for index in range(len(production_slice))],
        prediction=predictions.astype(int),
        probability=[
            round(float(row[prediction]), 4)
            for row, prediction in zip(probabilities, predictions)
        ],
        model_version=metadata["model_version"],
        timestamp=[
            (FIRST_TIMESTAMP + index * TIMESTAMP_STEP).isoformat()
            for index in range(len(production_slice))
        ],
    )
    columns = [
        "request_id",
        *FEATURES,
        TARGET_COLUMN,
        "prediction",
        "probability",
        "model_version",
        "timestamp",
    ]
    scored[columns].to_csv(PROD_SCORED_PATH, index=False)

    simulated = pd.DataFrame(
        {
            "request_id": scored["request_id"].head(N_SIMULATED_FEEDBACK),
            "true_label": scored[TARGET_COLUMN].head(N_SIMULATED_FEEDBACK).astype(int),
            "comments": "annotation simulée (conseiller)",
        }
    )
    simulated.to_csv(SIMULATED_FEEDBACK_PATH, index=False)

    print(f"{len(scored)} dossiers scorés écrits dans {PROD_SCORED_PATH}")
    print(scored["prediction"].value_counts().sort_index().to_string())
    print(f"\n{len(simulated)} annotations simulées écrites dans {SIMULATED_FEEDBACK_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
