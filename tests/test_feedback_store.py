"""Brique B : jointure feedback ⋈ prod_scored, marquage et injection simulée."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from feedback_store import (
    inject_mock_feedback,
    load_labeled_feedback,
    mark_used_for_training,
)


def _insert(db: Path, request_id: str, true_label: int, used: int = 0) -> None:
    with sqlite3.connect(db) as con:
        con.execute(
            "INSERT INTO feedbacks (request_id, true_label, comments, created_at, "
            "used_for_training) VALUES (?, ?, ?, ?, ?)",
            (request_id, true_label, None, "2026-09-01T08:00:00+00:00", used),
        )


def test_join_enrichit_le_feedback_avec_les_features(feedback_db, prod_scored_path):
    _insert(feedback_db, "REQ-00000", 2)

    joined = load_labeled_feedback(feedback_db, prod_scored_path)

    assert list(joined["request_id"]) == ["REQ-00000"]
    assert joined.loc[0, "true_label"] == 2
    # `famille_thematique` et non `synthese_entretien_prepare` : depuis la
    # phase 2, le journal de production porte la modalité catégorielle, pas le
    # texte — c'est exactement ce que le retrain doit rejouer.
    assert {"age", "code_rome_vise", "famille_thematique"} <= set(joined.columns)


def test_only_new_exclut_les_feedbacks_consommes(feedback_db, prod_scored_path):
    _insert(feedback_db, "REQ-00000", 0, used=1)
    _insert(feedback_db, "REQ-00001", 1, used=0)

    assert list(load_labeled_feedback(feedback_db, prod_scored_path)["request_id"]) == [
        "REQ-00001"
    ]
    assert len(load_labeled_feedback(feedback_db, prod_scored_path, only_new=False)) == 2


def test_base_vide_renvoie_un_dataframe_vide(feedback_db, prod_scored_path):
    assert load_labeled_feedback(feedback_db, prod_scored_path).empty


def test_jointure_cassee_leve_une_erreur(feedback_db, prod_scored_path):
    _insert(feedback_db, "REQ-99999", 1)

    with pytest.raises(ValueError, match="jointure cassée"):
        load_labeled_feedback(feedback_db, prod_scored_path)


def test_mark_used_for_training_retire_du_lot_suivant(feedback_db, prod_scored_path):
    _insert(feedback_db, "REQ-00000", 0)
    _insert(feedback_db, "REQ-00001", 1)

    mark_used_for_training(feedback_db, ["REQ-00000"])

    assert list(load_labeled_feedback(feedback_db, prod_scored_path)["request_id"]) == [
        "REQ-00001"
    ]


def test_injection_mock_est_incrementale(feedback_db, prod_scored_path):
    premiers = inject_mock_feedback(feedback_db, prod_scored_path, 10)
    suivants = inject_mock_feedback(feedback_db, prod_scored_path, 5)

    assert premiers == [f"REQ-{index:05d}" for index in range(10)]
    assert suivants == [f"REQ-{index:05d}" for index in range(10, 15)]


def test_injection_mock_reprend_le_vrai_label(feedback_db, prod_scored_path):
    inject_mock_feedback(feedback_db, prod_scored_path, 3)

    prod = pd.read_csv(prod_scored_path).head(3)
    stored = load_labeled_feedback(feedback_db, prod_scored_path)
    assert list(stored["true_label"]) == list(prod["classe_retour_emploi"])


def test_injection_mock_refuse_de_depasser_le_trafic(feedback_db, prod_scored_path):
    total = len(pd.read_csv(prod_scored_path))

    with pytest.raises(ValueError, match="ligne"):
        inject_mock_feedback(feedback_db, prod_scored_path, total + 1)


def test_injection_mock_refuse_un_count_non_positif(feedback_db, prod_scored_path):
    with pytest.raises(ValueError, match="positif"):
        inject_mock_feedback(feedback_db, prod_scored_path, 0)
