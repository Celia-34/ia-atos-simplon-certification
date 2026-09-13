"""Tests API + contract test du modèle — service model."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

MODELS_DIR = Path(__file__).parent.parent / "models"


# --- Tests API --------------------------------------------------------------

def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_info_exposes_holdout_metrics(client):
    resp = client.get("/info")
    assert resp.status_code == 200
    body = resp.json()
    assert body["model_name"] == "emploi_retour_s1"
    assert body["metrics_holdout"]["accuracy"] == 0.652


def test_predict_valid_returns_class_and_proba(client, valid_payload):
    resp = client.post("/predict", json=valid_payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["prediction"] in (0, 1, 2)
    assert 0.0 <= body["probability"] <= 1.0
    assert body["model_version"] == "v1.0.0"


def test_predict_invalid_returns_422(client, valid_payload):
    bad = dict(valid_payload)
    bad["departement"] = "999"  # hors format (2 caractères attendus)
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422


def test_metrics_endpoint_exposes_prometheus(client, valid_payload):
    client.post("/predict", json=valid_payload)  # génère au moins 1 observation
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "emploi_retour_predictions_total" in resp.text


# --- Contract test du modèle (bloque la release en CI) ----------------------

def test_model_contract_features_and_output():
    """Le modèle chargé accepte EXACTEMENT les features attendues et sort
    une prédiction dans {0, 1, 2} — garde-fou anti-régression schéma."""
    model = joblib.load(MODELS_DIR / "emploi_retour_s1.joblib")
    meta = json.loads((MODELS_DIR / "emploi_retour_s1.json").read_text())

    cols = meta["feature_columns_numeric"] + meta["feature_columns_categorical"]
    row = {
        "age": 35, "anciennete_poste_ans": 3.5, "niveau_diplome": "Bac+2",
        "code_rome_vise": "M1607", "est_allocataire": 1, "departement": "75",
    }
    X = pd.DataFrame([row])[cols]
    pred = int(model.predict(X)[0])
    assert pred in (0, 1, 2)
