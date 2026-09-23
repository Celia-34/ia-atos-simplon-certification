"""Tests API + contract test du modèle — service model."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

MODELS_DIR = Path(__file__).parent.parent / "models"
REPO_ROOT = Path(__file__).resolve().parents[3]
REFERENTIEL_PATH = REPO_ROOT / "data" / "referentiel_familles.csv"


def _metadata() -> dict:
    return json.loads((MODELS_DIR / "emploi_retour_s1.json").read_text(encoding="utf-8"))


# --- Tests API --------------------------------------------------------------

def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_info_exposes_holdout_metrics(client):
    """L'/info doit refléter le fichier de métadonnées, pas une valeur figée
    dans le test : sinon le test devient faux dès la release suivante."""
    meta = _metadata()
    resp = client.get("/info")
    assert resp.status_code == 200
    body = resp.json()
    assert body["model_name"] == "emploi_retour_s1"
    assert body["model_version"] == meta["model_version"]
    assert body["metrics_holdout"] == meta["metrics_holdout"]
    assert body["sklearn_version"] == meta["sklearn_version"]


def test_info_expose_le_scenario_et_les_features(client):
    """Le scénario servi doit être auditable depuis l'API : c'est ce qui
    permet de constater qu'on sert bien S1 (avec `famille_thematique`) et non
    une variante purement tabulaire."""
    body = client.get("/info").json()
    assert body["scenario"] == "s1"
    assert "famille_thematique" in body["feature_columns_categorical"]
    # Écart assumé schéma ↔ modèle : la nationalité est injectée, pas demandée.
    assert body["feature_columns_forced"] == {"nationalite_hors_ue": 0}


def test_predict_valid_returns_class_and_proba(client, valid_payload):
    resp = client.post("/predict", json=valid_payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["prediction"] in (0, 1, 2)
    assert 0.0 <= body["probability"] <= 1.0
    assert body["model_version"] == _metadata()["model_version"]


def test_predict_invalid_returns_422(client, valid_payload):
    bad = dict(valid_payload)
    bad["departement"] = "999"  # hors format (2 caractères attendus)
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422


def test_predict_famille_thematique_inconnue_returns_422(client, valid_payload):
    """Le OneHotEncoder est en handle_unknown='ignore' : une modalité hors
    référentiel ne lèverait PAS d'erreur, elle produirait un vecteur nul et donc
    une prédiction silencieusement fausse. Le Literal du schéma est le garde-fou."""
    bad = dict(valid_payload)
    bad["famille_thematique"] = "profil en or massif"
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422


def test_predict_famille_thematique_est_obligatoire(client, valid_payload):
    incomplet = {k: v for k, v in valid_payload.items() if k != "famille_thematique"}
    assert client.post("/predict", json=incomplet).status_code == 422


def test_predict_ne_demande_pas_la_nationalite(client, valid_payload):
    """`nationalite_hors_ue` ne doit pas pouvoir influencer le scoring : elle
    n'est pas un champ du schéma, donc une valeur envoyée par un appelant est
    ignorée et la prédiction reste identique."""
    reference = client.post("/predict", json=valid_payload).json()
    injecte = client.post(
        "/predict", json={**valid_payload, "nationalite_hors_ue": 1}
    ).json()
    assert injecte["prediction"] == reference["prediction"]
    assert injecte["probability"] == reference["probability"]


def test_metrics_endpoint_exposes_prometheus(client, valid_payload):
    client.post("/predict", json=valid_payload)  # génère au moins 1 observation
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "emploi_retour_predictions_total" in resp.text
    # Drift des features en entrée (§9) : la famille thématique est la seule
    # feature de cardinalité assez faible pour être suivie en label Prometheus.
    assert "emploi_retour_feature_famille_thematique_total" in resp.text


# --- Contract test du modèle (bloque la release en CI) ----------------------

def test_model_contract_features_and_output():
    """Le modèle chargé accepte EXACTEMENT les features attendues et sort
    une prédiction dans {0, 1, 2} — garde-fou anti-régression schéma."""
    model = joblib.load(MODELS_DIR / "emploi_retour_s1.joblib")
    meta = _metadata()

    cols = meta["feature_columns_numeric"] + meta["feature_columns_categorical"]
    row = {
        "age": 35, "anciennete_poste_ans": 3.5, "niveau_diplome": "Bac+2",
        "code_rome_vise": "M1607", "est_allocataire": 1, "departement": "75",
        "famille_thematique": "reconversion et besoin de formation",
        **meta["feature_columns_forced"],
    }
    X = pd.DataFrame([row])[cols]
    pred = int(model.predict(X)[0])
    assert pred in (0, 1, 2)


def test_metadata_declare_bien_le_scenario_s1_complet():
    """L'écart corrigé en phase 4 : les métadonnées déclaraient un modèle
    purement tabulaire alors que le scénario retenu est multimodal."""
    meta = _metadata()
    assert meta["scenario"] == "s1"
    assert "famille_thematique" in meta["feature_columns_categorical"]
    assert meta["feature_columns_numeric"] == ["age", "anciennete_poste_ans"]


def test_le_schema_couvre_toutes_les_familles_du_referentiel():
    """Le Literal du schéma et le référentiel figé ne doivent jamais diverger :
    une famille ajoutée au CSV sans être ajoutée au schéma rendrait des dossiers
    non scorables (422)."""
    import typing

    from app.schemas import UsagerFeatures

    referentiel = pd.read_csv(REFERENTIEL_PATH, encoding="utf-8")
    attendues = set(referentiel["famille_thematique"]) | {"texte_manquant"}
    declarees = set(typing.get_args(typing.get_type_hints(UsagerFeatures)["famille_thematique"]))
    assert declarees == attendues


def test_les_modalites_du_schema_sont_connues_de_l_encodeur():
    """handle_unknown='ignore' masque les modalités inconnues : on vérifie donc
    explicitement que chaque valeur acceptée par l'API a bien été apprise."""
    import typing

    from app.schemas import UsagerFeatures

    pre = joblib.load(MODELS_DIR / "emploi_retour_s1.joblib").named_steps["preprocessing"]
    apprises = None
    for _, trans, cols in pre.transformers_:
        steps = trans.named_steps.values() if hasattr(trans, "named_steps") else [trans]
        for step in steps:
            if hasattr(step, "categories_") and "famille_thematique" in cols:
                apprises = set(
                    dict(zip(cols, step.categories_))["famille_thematique"]
                )
    assert apprises is not None, "famille_thematique absente de l'encodeur catégoriel"
    declarees = set(typing.get_args(typing.get_type_hints(UsagerFeatures)["famille_thematique"]))
    assert declarees <= apprises
