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
    # Plus aucun écart schéma ↔ modèle : les features annoncées sont celles
    # demandées à l'appelant, et rien n'est injecté côté serveur.
    assert "feature_columns_forced" not in body


def test_info_ne_declare_plus_de_colonne_forcee():
    """Garde-fou anti-retour en arrière : la neutralisation serveur de
    `nationalite_hors_ue` rendait l'audit d'équité §7.2 irréalisable sur
    données de production (#3) et faisait diverger les métriques annoncées de
    celles du notebook (#14). Le fichier de métadonnées ne doit plus porter
    aucune trace de ce mécanisme."""
    meta = _metadata()
    assert "feature_columns_forced" not in meta
    assert "metrics_holdout_notebook" not in meta
    assert "metrics_note" not in meta


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


def test_predict_exige_la_nationalite(client, valid_payload):
    """Critère de sortie n° 2 de l'alignement : un payload à 7 champs — le
    contrat `v2.0.0` — doit désormais être rejeté. La rupture est explicite,
    elle est la raison du passage en version majeure `v3.0.0`."""
    incomplet = {k: v for k, v in valid_payload.items() if k != "nationalite_hors_ue"}

    assert len(incomplet) == 7
    assert client.post("/predict", json=incomplet).status_code == 422


def test_predict_refuse_une_nationalite_hors_domaine(client, valid_payload):
    """La variable est binaire : toute autre valeur trahit un appelant qui a
    mal compris le contrat, et ne doit pas atteindre le pipeline."""
    for valeur in (2, -1):
        resp = client.post("/predict", json={**valid_payload, "nationalite_hors_ue": valeur})
        assert resp.status_code == 422, f"nationalite_hors_ue={valeur} accepté"


def test_la_nationalite_est_bien_consommee_par_le_modele(client, valid_payload):
    """Contrepartie du test supprimé en A2.4.

    L'arbitrage `J0` assume que la variable **influence** la prédiction : c'est
    la condition pour que le recall classe 2 des usagers hors UE (0.800) reste
    supérieur à celui des usagers UE (0.529). Un service qui la recevrait sans
    la transmettre au pipeline rejouerait silencieusement la neutralisation de
    la phase 4 — ce test l'interdit.

    On balaie plusieurs profils : sur un profil donné la frontière de décision
    peut être insensible à la variable, mais elle ne peut pas l'être partout.
    """
    profils = [
        {**valid_payload, "age": age, "niveau_diplome": diplome}
        for age in (25, 35, 45, 55)
        for diplome in ("Sans diplôme", "Bac", "Bac+2")
    ]
    ecarts = 0
    for profil in profils:
        ue = client.post("/predict", json={**profil, "nationalite_hors_ue": 0}).json()
        hors_ue = client.post("/predict", json={**profil, "nationalite_hors_ue": 1}).json()
        if (ue["prediction"], ue["probability"]) != (
            hors_ue["prediction"],
            hors_ue["probability"],
        ):
            ecarts += 1

    assert ecarts > 0, (
        "La nationalité n'a modifié aucune sortie sur 12 profils : le service "
        "la neutralise probablement avant l'inférence."
    )


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
        "nationalite_hors_ue": 0,
    }
    # Les colonnes déclarées et les champs du schéma d'entrée doivent coïncider
    # exactement : plus aucune colonne n'est injectée par le service.
    assert set(cols) == set(row)
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
