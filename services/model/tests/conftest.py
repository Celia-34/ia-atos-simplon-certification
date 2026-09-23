"""Fixtures pytest — service model.

Ajoute la racine du service au sys.path pour que `from app.main import app`
fonctionne quand pytest est lancé depuis la racine du repo
(`pytest services/model/tests`).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SERVICE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SERVICE_ROOT))


@pytest.fixture
def client():
    """TestClient FastAPI (déclenche le lifespan → charge le modèle).

    L'isolation du package `app` entre les services est assurée par le
    `conftest.py` racine (hooks `pytest_collectstart` / `pytest_runtest_setup`).
    """
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def valid_payload() -> dict:
    """Un usager valide aligné sur UsagerFeatures (scénario s1).

    `famille_thematique` est une modalité du référentiel figé (§4.2.2) :
    depuis la phase 2 la synthèse d'entretien est catégorielle, pas du texte.
    Les 8 champs du payload sont exactement les 8 features du scénario s1 —
    `nationalite_hors_ue` comprise, depuis l'alignement `v3.0.0`.
    """
    return {
        "age": 35,
        "anciennete_poste_ans": 3.5,
        "niveau_diplome": "Bac+2",
        "code_rome_vise": "M1607",
        "est_allocataire": 1,
        "departement": "75",
        "famille_thematique": "reconversion et besoin de formation",
        "nationalite_hors_ue": 0,
    }
