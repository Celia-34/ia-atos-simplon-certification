"""Brique C : construction du jeu d'entraînement, empreinte et journalisation.

Aucun entraînement réel n'est déclenché ici (l'entraînement complet est coûteux) :
`train_candidate` est couvert par l'exécution manuelle de `retrain.py`, tandis
que ces tests verrouillent la plomberie qui rend la décision auditable.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd
import pytest

import retrain
from promotion import PromotionDecision

PRODUCTION_METRICS = {
    "accuracy": 0.7029,
    "f1_macro": 0.6894,
    "f1_classe_2": 0.6250,
    "recall_classe_2": 0.6349,
    "taux_erreur_grave_2_vers_0": 0.0794,
}


@pytest.fixture
def feedbacks(feedback_db: Path, prod_scored_path: Path) -> pd.DataFrame:
    with sqlite3.connect(feedback_db) as con:
        con.executemany(
            "INSERT INTO feedbacks (request_id, true_label, comments, created_at) "
            "VALUES (?, ?, ?, ?)",
            [
                ("REQ-00000", 2, None, "2026-09-01T08:00:00+00:00"),
                ("REQ-00001", 0, None, "2026-09-01T09:00:00+00:00"),
            ],
        )
    return retrain.load_labeled_feedback(feedback_db, prod_scored_path)


def test_le_jeu_d_entrainement_integre_les_feedbacks(feedbacks):
    X_sans, y_sans = retrain.build_training_data(pd.DataFrame())
    X_avec, y_avec = retrain.build_training_data(feedbacks)

    assert len(X_avec) == len(X_sans) + len(feedbacks)
    assert list(X_avec.columns) == retrain.FEATURES
    assert list(y_avec.tail(2)) == [2, 0]


def test_empreinte_du_dataset_est_deterministe_et_sensible(feedbacks):
    X_train, y_train = retrain.build_training_data(feedbacks)

    assert retrain.dataset_hash(X_train, y_train) == retrain.dataset_hash(X_train, y_train)
    assert retrain.dataset_hash(X_train, y_train) != retrain.dataset_hash(
        X_train.head(10), y_train.head(10)
    )


def test_le_rejet_est_journalise_comme_la_promotion(tmp_path, monkeypatch):
    monkeypatch.setattr(retrain, "DECISION_LOG", tmp_path / "decisions_log.jsonl")
    candidate_metrics = {**PRODUCTION_METRICS, "recall_classe_2": 0.55}

    retrain.write_decision(
        PromotionDecision(False, "Régression critique"), candidate_metrics, PRODUCTION_METRICS, 100
    )

    record = json.loads(retrain.DECISION_LOG.read_text(encoding="utf-8").strip())
    assert record["promote"] is False
    assert record["reason"] == "Régression critique"
    assert record["feedback_count"] == 100
    assert record["candidate_metrics"] == candidate_metrics


def test_les_metadonnees_promues_portent_la_nouvelle_version(tmp_path, monkeypatch, feedbacks):
    monkeypatch.setattr(retrain, "PROMOTED_META_PATH", tmp_path / "emploi_retour_s1_1.json")
    X_train, y_train = retrain.build_training_data(feedbacks)

    retrain.write_promoted_metadata(X_train, y_train, PRODUCTION_METRICS)

    metadata = json.loads(retrain.PROMOTED_META_PATH.read_text(encoding="utf-8"))
    assert metadata["model_version"] == retrain.PROMOTED_VERSION
    assert metadata["dataset_sha256"] == retrain.dataset_hash(X_train, y_train)
    assert metadata["metrics_reference"] == PRODUCTION_METRICS
