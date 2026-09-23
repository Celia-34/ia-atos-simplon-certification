"""Réentraîne un modèle **candidat** à partir des feedbacks métier — brique C.

Enchaîne : lecture des feedbacks non consommés → garde-seuil → entraînement du
candidat → évaluation candidat *et* production sur le même jeu de référence figé
→ `decide_promotion` → journalisation. Le candidat est écrit séparément :
``emploi_retour_s1_1.joblib`` (v1.1.0) n'existe **que** s'il est promu.

Usage::

    python scripts/retrain.py --min-feedback 100
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feedback_store import load_labeled_feedback, mark_used_for_training  # noqa: E402
from preprocess import (  # noqa: E402
    DATA,
    FEATURES,
    ROOT,
    TARGET_COLUMN,
    TEXT_COLUMN,
    build_features,
    build_pipeline,
    build_served_features,
    evaluate,
    load_dataset,
    load_prepared_csv,
    split_train_holdout,
)
from promotion import PromotionDecision, decide_promotion  # noqa: E402

MODELS = ROOT / "services" / "model" / "models"
PROD_SCORED_PATH = DATA / "prod_scored.csv"
REFERENCE_PATH = DATA / "reference_set.csv"
FEEDBACK_DB = Path(os.environ.get("FEEDBACK_DB", DATA / "feedbacks.db"))

PRODUCTION_PATH = MODELS / "emploi_retour_s1.joblib"
PRODUCTION_META_PATH = MODELS / "emploi_retour_s1.json"
CANDIDATE_PATH = MODELS / "emploi_retour_candidate.joblib"
PROMOTED_PATH = MODELS / "emploi_retour_s1_1.joblib"
PROMOTED_META_PATH = MODELS / "emploi_retour_s1_1.json"
DECISION_LOG = ROOT / "decisions_log.jsonl"

PROMOTED_VERSION = "v1.1.0"
DEFAULT_MIN_FEEDBACK = 100


def load_new_feedbacks() -> pd.DataFrame:
    """Feedbacks non encore consommés, enrichis des features du dossier scoré."""
    if not FEEDBACK_DB.exists():
        raise FileNotFoundError(f"Base de feedbacks introuvable : {FEEDBACK_DB}")
    return load_labeled_feedback(FEEDBACK_DB, PROD_SCORED_PATH, only_new=True)


def build_training_data(feedbacks: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Jeu d'entraînement d'origine (§4.1) + dossiers de production annotés."""
    dataset = load_dataset()
    train, _ = split_train_holdout(dataset)
    X_train = build_features(train)
    y_train = train[TARGET_COLUMN].astype(int)

    if not feedbacks.empty:
        # `build_features` sélectionne les colonnes du scénario s1 : les dossiers
        # scorés portent déjà `departement` et `famille_thematique` (le journal
        # les écrit explicitement), donc rien n'est redérivé ici.
        X_feedback = build_features(feedbacks)
        X_train = pd.concat([X_train, X_feedback], ignore_index=True)
        y_train = pd.concat(
            [y_train, feedbacks["true_label"].astype(int)], ignore_index=True
        )
    return X_train, y_train


def train_candidate(X_train: pd.DataFrame, y_train: pd.Series):
    """Entraîne et persiste le candidat, sans jamais toucher au modèle servi."""
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    MODELS.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, CANDIDATE_PATH)
    return pipeline


def validate_candidate(model) -> None:
    """Garde-fou technique avant toute comparaison de métriques.

    Le candidat doit accepter les features **telles que le service les
    présente** (nationalité neutralisée) : un candidat qui ne passerait que sur
    les features brutes serait impromouvable.
    """
    reference = load_prepared_csv(REFERENCE_PATH)
    probabilities = model.predict_proba(build_served_features(reference))
    if not ((probabilities >= 0).all() and (probabilities <= 1).all()):
        raise ValueError("Probabilités du candidat hors de [0, 1]")
    if set(model.classes_) != {0, 1, 2}:
        raise ValueError(f"Classes inattendues pour le candidat : {model.classes_}")


def evaluate_on_reference(model) -> dict[str, float]:
    return evaluate(model, load_prepared_csv(REFERENCE_PATH))


def dataset_hash(X_train: pd.DataFrame, y_train: pd.Series) -> str:
    """Empreinte du jeu d'entraînement : rend la version promue auditable."""
    payload = pd.concat([X_train, y_train.rename(TARGET_COLUMN)], axis=1)
    return hashlib.sha256(payload.to_csv(index=False).encode("utf-8")).hexdigest()


def write_decision(
    decision: PromotionDecision,
    candidate_metrics: dict[str, float],
    production_metrics: dict[str, float],
    feedback_count: int,
) -> None:
    """Journalise la décision — promotion **comme** rejet."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "feedback_count": feedback_count,
        "candidate_metrics": candidate_metrics,
        "production_metrics": production_metrics,
        "promote": decision.promote,
        "reason": decision.reason,
    }
    with DECISION_LOG.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_promoted_metadata(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    candidate_metrics: dict[str, float],
) -> None:
    metadata = json.loads(PRODUCTION_META_PATH.read_text(encoding="utf-8"))
    metadata["model_version"] = PROMOTED_VERSION
    metadata["created_at"] = datetime.now(timezone.utc).isoformat()
    metadata["dataset_sha256"] = dataset_hash(X_train, y_train)
    metadata["metrics_reference"] = candidate_metrics
    PROMOTED_META_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-feedback", type=int, default=DEFAULT_MIN_FEEDBACK)
    args = parser.parse_args()

    feedbacks = load_new_feedbacks()
    unused_count = len(feedbacks)
    if unused_count < args.min_feedback:
        print(
            f"Skip : {unused_count} feedback(s) non consommé(s), "
            f"seuil à {args.min_feedback}"
        )
        return 0

    X_train, y_train = build_training_data(feedbacks)
    candidate = train_candidate(X_train, y_train)
    validate_candidate(candidate)

    candidate_metrics = evaluate_on_reference(candidate)
    production_metrics = evaluate_on_reference(joblib.load(PRODUCTION_PATH))
    decision = decide_promotion(candidate_metrics, production_metrics)
    write_decision(decision, candidate_metrics, production_metrics, unused_count)

    if not decision.promote:
        print(json.dumps({"promote": False, "reason": decision.reason}, ensure_ascii=False))
        return 0

    joblib.dump(candidate, PROMOTED_PATH)
    write_promoted_metadata(X_train, y_train, candidate_metrics)
    mark_used_for_training(FEEDBACK_DB, feedbacks["request_id"].tolist())
    print(json.dumps({"promote": True, "reason": decision.reason}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
