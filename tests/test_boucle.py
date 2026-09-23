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

# Golden run v3.0.0 mesuré sur data/reference_set.csv (data/reference_baseline.json).
PRODUCTION_METRICS = {
    "accuracy": 0.7171,
    "f1_macro": 0.6990,
    "f1_classe_2": 0.6029,
    "recall_classe_2": 0.6508,
    "taux_erreur_grave_2_vers_0": 0.0794,
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
    """Un recul du recall classe 2 n'est pas rachetable par un gain d'accuracy.

    La valeur choisie reste **au-dessus du plancher** (0.60) : sans cela le rejet
    tomberait sur « Plancher de qualité » et ce test ne vérifierait plus la règle
    de non-régression critique qu'il prétend couvrir.
    """
    candidate = {**PRODUCTION_METRICS, "accuracy": 0.78, "recall_classe_2": 0.62}

    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert not decision.promote
    assert "Régression critique" in decision.reason
    assert "recall_classe_2" in decision.reason


def test_hausse_de_l_erreur_grave_est_une_regression_critique():
    """Renvoyer un dossier à risque vers « retour rapide » est l'erreur la plus
    coûteuse : elle prive l'usager de tout accompagnement.

    0.095 reste **sous le plancher** de 0.10 mais au-dessus du golden run
    (0.0794) de plus d'une tolérance : le rejet doit donc venir de la règle de
    non-régression, pas du plancher.
    """
    candidate = {
        **PRODUCTION_METRICS,
        "f1_macro": 0.78,
        "taux_erreur_grave_2_vers_0": 0.095,
    }

    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert not decision.promote
    assert "Régression critique" in decision.reason
    assert "taux_erreur_grave_2_vers_0" in decision.reason


def test_le_plancher_d_erreur_grave_est_le_garde_fou_metier_de_10_pourcent():
    """Résorption durable de #6.

    La neutralisation de la phase 4 portait l'erreur grave à 12,2 %, ce qui
    avait contraint à desserrer le plancher à 0.12 — un garde-fou qu'aucun
    modèle ne pouvait plus déclencher. Le modèle aligné repasse sous les 10 %
    du §1.4 : le plancher y revient et doit y rester.
    """
    assert THRESHOLDS["taux_erreur_grave_2_vers_0"] == 0.10

    candidate = {**PRODUCTION_METRICS, "taux_erreur_grave_2_vers_0": 0.101}
    decision = decide_promotion(candidate, PRODUCTION_METRICS)

    assert not decision.promote
    assert "Plancher de qualité" in decision.reason


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


def test_les_metriques_de_reference_du_test_suivent_le_golden_run():
    """A3.3 — `PRODUCTION_METRICS` est une copie du golden run.

    Une copie qui dérive rend tous les cas limites ci-dessus faux sans qu'aucun
    d'eux n'échoue : ils continueraient de tester une frontière de décision qui
    n'existe plus. Ce test est le lien qui les rattache au fichier de vérité.
    """
    import json

    baseline = json.loads(
        (ROOT / "data" / "reference_baseline.json").read_text(encoding="utf-8")
    )
    assert baseline["model_version"] == "v3.0.0"
    for metric, value in PRODUCTION_METRICS.items():
        assert value == pytest.approx(baseline["metrics"][metric], abs=5e-5), metric
