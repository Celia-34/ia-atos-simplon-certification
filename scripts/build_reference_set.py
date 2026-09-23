"""Fige `data/reference_set.csv` et son golden run `data/reference_baseline.json`.

Le jeu de référence est le **seul** juge de la promotion : candidat et modèle de
production y sont évalués sur exactement les mêmes lignes. Il est extrait du
holdout §4.1 (jamais vu à l'entraînement), stratifié sur ``classe_retour_emploi``
pour conserver la part de la classe 2 (~18 %), et disjoint du trafic de
production (cf. `preprocess.split_holdout`).

⚠️ Ne pas relancer ce script une fois le modèle en v1.0.0 : un jeu de référence
qui change rend les métriques incomparables d'une release à l'autre — et donc la
décision de promotion indéfendable.

Usage::

    python scripts/build_reference_set.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preprocess import (  # noqa: E402
    DATA,
    TARGET_COLUMN,
    evaluate,
    load_dataset,
    split_holdout,
    split_train_holdout,
)

REFERENCE_PATH = DATA / "reference_set.csv"
BASELINE_PATH = DATA / "reference_baseline.json"
PRODUCTION_PATH = (
    Path(__file__).resolve().parent.parent
    / "services"
    / "model"
    / "models"
    / "emploi_retour_s1.joblib"
)
PRODUCTION_META_PATH = PRODUCTION_PATH.with_suffix(".json")


def main() -> int:
    if not PRODUCTION_PATH.exists():
        raise SystemExit(
            f"{PRODUCTION_PATH} est absent : le golden run ne peut pas être mesuré.\n"
            "Exportez d'abord le modèle retenu en §6.1 sous ce nom."
        )

    dataset = load_dataset()
    _, holdout = split_train_holdout(dataset)
    reference, _ = split_holdout(holdout)
    reference.to_csv(REFERENCE_PATH, index=False)

    production = joblib.load(PRODUCTION_PATH)
    metadata = json.loads(PRODUCTION_META_PATH.read_text(encoding="utf-8"))
    baseline = {
        "model_version": metadata["model_version"],
        "reference_set": str(REFERENCE_PATH.relative_to(REFERENCE_PATH.parent.parent)),
        "n_reference": int(len(reference)),
        "metrics": evaluate(production, reference),
    }
    BASELINE_PATH.write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"{len(reference)} lignes écrites dans {REFERENCE_PATH}")
    print(reference[TARGET_COLUMN].value_counts(normalize=True).sort_index())
    print(f"\nGolden run {baseline['model_version']} → {BASELINE_PATH}")
    for name, value in baseline["metrics"].items():
        print(f"  {name:28s} = {value:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
