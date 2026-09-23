"""Boucle complète : endpoint de feedback (brique A) et politique de promotion (brique D).

``FEEDBACK_DB`` est positionnée avant l'import du service : celui-ci résout le
chemin de sa base au chargement du module, pas à chaque requête.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
os.environ["FEEDBACK_DB"] = str(Path(tempfile.mkdtemp()) / "feedbacks.db")
sys.path.insert(0, str(ROOT / "services" / "feedback"))

from app.main import DB_PATH, app  # noqa: E402
from promotion import MIN_GAIN, THRESHOLDS, decide_promotion  # noqa: E402

# Golden run v2.0.0 mesuré sur data/reference_set.csv (data/reference_baseline.json).
PRODUCTION_METRICS = {
    "accuracy": 0.7057,
    "f1_macro": 0.6839,
    "f1_classe_2": 0.5854,
    "recall_classe_2": 0.5714,
    "taux_erreur_grave_2_vers_0": 0.0952,
}


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        with sqlite3.connect(DB_PATH) as con:
            con.execute("DELETE FROM feedbacks")
        yield test_client


# --- Brique A : endpoint de feedback ----------------------------------------


def test_health_ok(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_feedback_valide_est_stocke(client):
    response = client.post("/feedback", json={"request_id": "REQ-00000", "true_label": 2})

    assert response.status_code == 201
    assert client.get("/feedback/count").json() == {"count": 1, "new": 1}


def test_request_id_inconnu_renvoie_404(client):
    response = client.post("/feedback", json={"request_id": "REQ-99999", "true_label": 1})

    assert response.status_code == 404


def test_label_hors_domaine_renvoie_422(client):
    response = client.post("/feedback", json={"request_id": "REQ-00000", "true_label": 3})

    assert response.status_code == 422


def test_rejeu_a_l_identique_est_idempotent(client):
    payload = {"request_id": "REQ-00000", "true_label": 1}
    client.post("/feedback", json=payload)

    assert client.post("/feedback", json=payload).status_code == 201
    assert client.get("/feedback/count").json()["count"] == 1


def test_feedback_contradictoire_renvoie_409(client):
    client.post("/feedback", json={"request_id": "REQ-00000", "true_label": 1})

    response = client.post("/feedback", json={"request_id": "REQ-00000", "true_label": 2})

    assert response.status_code == 409


def test_mock_feedback_alimente_le_compteur(client):
    response = client.get("/mock-feedback", params={"feedNumber": 12})

    assert response.json()["inserted"] == 12
    assert client.get("/feedback/count").json()["new"] == 12


def test_mock_feedback_refuse_un_nombre_non_positif(client):
    assert client.get("/mock-feedback", params={"feedNumber": 0}).status_code == 422


# --- Brique D : politique de promotion --------------------------------------


def test_candidat_qui_progresse_est_promu():
    candidate = {**PRODUCTION_METRICS, "recall_classe_2": 0.70}

    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert decision.promote
    assert "recall_classe_2" in decision.reason


def test_regression_critique_sur_le_recall_est_rejetee():
    candidate = {**PRODUCTION_METRICS, "accuracy": 0.75, "recall_classe_2": 0.55}

    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert not decision.promote
    assert "Plancher" in decision.reason or "Régression critique" in decision.reason


def test_hausse_de_l_erreur_grave_est_une_regression_critique():
    candidate = {
        **PRODUCTION_METRICS,
        "f1_macro": 0.75,
        "taux_erreur_grave_2_vers_0": 0.11,
    }

    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert not decision.promote
    assert "taux_erreur_grave_2_vers_0" in decision.reason


def test_plancher_de_qualite_non_respecte_est_rejete():
    candidate = {**PRODUCTION_METRICS, "f1_classe_2": 0.40, "recall_classe_2": 0.40}

    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert not decision.promote
    assert "Plancher de qualité" in decision.reason


def test_candidat_sans_gain_suffisant_est_rejete():
    candidate = {**PRODUCTION_METRICS, "accuracy": PRODUCTION_METRICS["accuracy"] + MIN_GAIN / 2}

    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert not decision.promote
    assert "Aucun gain" in decision.reason


def test_metriques_manquantes_bloquent_la_decision():
    decision = decide_promotion({"accuracy": 0.80}, PRODUCTION_METRICS)

    assert not decision.promote
    assert "Métriques manquantes" in decision.reason


def test_le_modele_de_production_respecte_ses_propres_planchers():
    """Un plancher que le modèle servi ne franchit pas rend toute promotion
    impossible : le rejet tomberait sur « Plancher de qualité » avant même de
    comparer candidat et production. Les seuils doivent donc être recalibrés à
    chaque changement de modèle servi — c'est ce qui a été manqué en v1→v2."""
    import json

    baseline = json.loads(
        (ROOT / "data" / "reference_baseline.json").read_text(encoding="utf-8")
    )
    for metric, floor in THRESHOLDS.items():
        value = baseline["metrics"][metric]
        if metric == "taux_erreur_grave_2_vers_0":
            assert value <= floor, f"{metric}={value:.4f} > plancher {floor}"
        else:
            assert value >= floor, f"{metric}={value:.4f} < plancher {floor}"
