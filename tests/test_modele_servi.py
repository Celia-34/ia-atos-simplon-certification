"""Garde-fous sur le modèle servi : configuration et métriques.

Ces tests ne valident pas une performance, ils valident une **concordance**.
Ils existent parce que deux régressions silencieuses se sont déjà produites :

* A1.3 / #13 — ``class_weight="balanced"`` avait disparu de ``build_pipeline``,
  parce que le descripteur textuel du notebook (``"n_estimators=300"``) n'en
  faisait pas mention. Le retrain produisait alors des candidats d'une
  configuration différente du modèle servi : la boucle de promotion comparait
  deux réglages et non deux jeux de données.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pytest

ROOT = Path(__file__).resolve().parent.parent
SERVED_MODEL_PATH = ROOT / "services" / "model" / "models" / "emploi_retour_s1.joblib"

# Paramètres qui définissent la configuration du classifieur retenu en §6.1.
# `class_weight` est le paramètre historiquement perdu (#13).
PARAMETRES_SUIVIS = ("n_estimators", "class_weight", "random_state")


def _classifieur(pipeline):
    return pipeline.named_steps["model"]


@pytest.fixture(scope="module")
def modele_servi():
    if not SERVED_MODEL_PATH.exists():
        pytest.skip(f"{SERVED_MODEL_PATH} absent : lancez scripts/export_model_prod.py")
    return joblib.load(SERVED_MODEL_PATH)


def test_le_pipeline_de_retrain_a_la_configuration_du_modele_servi(modele_servi):
    """A1.3 — garde-fou permanent contre la réapparition de #13.

    Le candidat du retrain doit différer du modèle de production **par les
    données uniquement**. Toute divergence d'hyperparamètre fausse
    silencieusement la décision de promotion.
    """
    from preprocess import build_pipeline

    candidat = _classifieur(build_pipeline()).get_params()
    servi = _classifieur(modele_servi).get_params()

    ecarts = {
        nom: (candidat.get(nom), servi.get(nom))
        for nom in PARAMETRES_SUIVIS
        if candidat.get(nom) != servi.get(nom)
    }
    assert not ecarts, (
        "build_pipeline() ne reproduit pas la configuration du modèle servi "
        f"(candidat, servi) : {ecarts}"
    )


def test_le_modele_servi_est_bien_un_random_forest_pondere(modele_servi):
    """Le descripteur `algorithm` des métadonnées doit dire vrai (#13)."""
    metadata = json.loads(
        SERVED_MODEL_PATH.with_suffix(".json").read_text(encoding="utf-8")
    )
    params = _classifieur(modele_servi).get_params()

    assert type(_classifieur(modele_servi)).__name__ in metadata["algorithm"]
    for nom in PARAMETRES_SUIVIS:
        assert repr(params[nom]) in metadata["algorithm"], (
            f"{nom}={params[nom]!r} absent du descripteur "
            f"« {metadata['algorithm']} »"
        )
