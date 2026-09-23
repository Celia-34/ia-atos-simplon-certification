"""Contrat du référentiel figé des 9 familles thématiques (§4.2.2).

Vérifie sur le **dataset réel** que le zero-shot n'est plus nécessaire : la table
statique couvre exactement les templates observés, et l'assignation est totale.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.preprocess import load_dataset  # noqa: E402
from src import pipeline_texte  # noqa: E402


@pytest.fixture(scope="module")
def referentiel() -> pd.DataFrame:
    return pipeline_texte.charger_referentiel_familles()


@pytest.fixture(scope="module")
def dataset() -> pd.DataFrame:
    return load_dataset()


def test_referentiel_contient_neuf_lignes_et_neuf_familles(referentiel):
    assert len(referentiel) == 9
    assert referentiel["famille_thematique"].nunique() == 9
    assert referentiel["synthese_entretien_prepare"].is_unique
    assert (referentiel["modele"] == "cmarkea/distilcamembert-base-nli").all()
    assert (referentiel["score_confiance"] >= 0.5).all()


def test_referentiel_couvre_exactement_les_templates_du_dataset(referentiel, dataset):
    textes = dataset[pipeline_texte.TEXT_COLUMN].fillna("").astype(str)
    observes = set(textes[textes.str.strip() != ""].unique())
    assert set(referentiel["synthese_entretien_prepare"]) == observes


def test_assigner_famille_mappe_tous_les_textes_non_vides(dataset):
    resultat = pipeline_texte.assigner_famille(dataset)
    textes = resultat[pipeline_texte.TEXT_COLUMN].fillna("").astype(str)
    mask_vide = textes.str.strip() == ""

    familles = resultat[pipeline_texte.FAMILLE_COLUMN]
    assert familles.notna().all()
    assert (familles[mask_vide] == pipeline_texte.FAMILLE_TEXTE_MANQUANT).all()
    assert (familles[~mask_vide] != pipeline_texte.FAMILLE_TEXTE_MANQUANT).all()
    assert familles[~mask_vide].nunique() == 9
    assert mask_vide.sum() > 0  # le dataset contient bien des synthèses manquantes


def test_assigner_famille_leve_une_erreur_sur_texte_inconnu(dataset):
    df = dataset.head(1).copy()
    df[pipeline_texte.TEXT_COLUMN] = "Texte totalement inconnu du référentiel."
    with pytest.raises(ValueError, match="référentiel"):
        pipeline_texte.assigner_famille(df)
