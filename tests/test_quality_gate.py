"""Tests de la quality gate — elle doit surtout savoir **bloquer**.

Une gate qui passe est une information faible : elle passe aussi quand elle ne
contrôle rien. Ces tests vérifient donc en priorité les cas d'échec, et en
particulier celui qu'aucune autre suite du dépôt ne couvre : une
``reference_baseline.json`` désynchronisée de l'artefact réellement servi.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import quality_gate
from promotion import THRESHOLDS

ROOT = Path(__file__).resolve().parent.parent


# --- Contrat servi (G1) ------------------------------------------------------


def _meta_valide() -> dict:
    return {
        "model_version": "v3.0.0",
        "feature_columns_numeric": ["age", "anciennete_poste_ans"],
        "feature_columns_categorical": [
            "nationalite_hors_ue",
            "niveau_diplome",
            "code_rome_vise",
            "est_allocataire",
            "departement",
            "famille_thematique",
        ],
        "metrics_holdout": {},
    }


def _codes_en_echec(rapport: quality_gate.Rapport) -> list[str]:
    return [controle["code"] for controle in rapport.echecs]


def test_le_contrat_servi_valide_passe():
    rapport = quality_gate.Rapport()
    quality_gate.controler_contrat_servi(
        rapport, _meta_valide(), {"model_version": "v3.0.0"}
    )
    assert rapport.ok, rapport.echecs


@pytest.mark.parametrize(
    "cle", ["feature_columns_forced", "metrics_holdout_notebook", "metrics_note"]
)
def test_une_cle_de_neutralisation_bloque_la_gate(cle):
    """#7 / #14 — ces clés signent une prod qui a divergé du notebook."""
    meta = {**_meta_valide(), cle: {"nationalite_hors_ue": 0}}
    rapport = quality_gate.Rapport()
    quality_gate.controler_contrat_servi(rapport, meta, {"model_version": "v3.0.0"})
    assert "G1.1" in _codes_en_echec(rapport)


def test_une_version_desalignee_du_golden_run_bloque_la_gate():
    """Servir un v3.1.0 arbitré sur la baseline d'un v3.0.0 n'a aucun sens."""
    rapport = quality_gate.Rapport()
    quality_gate.controler_contrat_servi(
        rapport, {**_meta_valide(), "model_version": "v3.1.0"}, {"model_version": "v3.0.0"}
    )
    assert "G1.2" in _codes_en_echec(rapport)


def test_un_champ_manquant_au_contrat_d_entree_bloque_la_gate():
    """Le retrait silencieux d'une feature est la régression #7 revisitée."""
    meta = _meta_valide()
    meta["feature_columns_categorical"].remove("nationalite_hors_ue")
    rapport = quality_gate.Rapport()
    quality_gate.controler_contrat_servi(rapport, meta, {"model_version": "v3.0.0"})
    assert "G1.3" in _codes_en_echec(rapport)


# --- Concordance documentaire (G3) -------------------------------------------


def test_une_metrique_servie_divergente_bloque_la_gate():
    source = json.loads(quality_gate.SOURCE_META_PATH.read_text(encoding="utf-8"))
    faussees = {
        nom: round(float(valeur), 4)
        for nom, valeur in source["metriques_test"].items()
    }
    faussees["accuracy"] = round(faussees["accuracy"] + 0.05, 4)

    rapport = quality_gate.Rapport()
    quality_gate.controler_concordance(rapport, {"metrics_holdout": faussees})
    assert "G3.1" in _codes_en_echec(rapport)


# --- Golden run rejoué (G4) --------------------------------------------------


@pytest.fixture(scope="module")
def modele_servi():
    joblib = pytest.importorskip("joblib")
    if not quality_gate.SERVED_MODEL_PATH.exists():
        pytest.skip("artefact servi absent : lancez scripts/export_model_prod.py")
    return joblib.load(quality_gate.SERVED_MODEL_PATH)


@pytest.fixture(scope="module")
def baseline() -> dict:
    return json.loads(quality_gate.BASELINE_PATH.read_text(encoding="utf-8"))


def test_l_artefact_servi_reproduit_le_golden_run_publie(modele_servi, baseline):
    """Le contrôle central : métriques **calculées**, pas relues d'un fichier."""
    rapport = quality_gate.Rapport()
    mesurees = quality_gate.controler_golden_run(rapport, modele_servi, baseline)

    assert rapport.ok, rapport.echecs
    assert set(THRESHOLDS).issubset(mesurees)


def test_une_baseline_perimee_bloque_la_gate(modele_servi, baseline):
    """LE cas que personne d'autre ne couvre.

    ``tests/test_boucle.py`` compare ``reference_baseline.json`` à des
    constantes et à ``THRESHOLDS`` : il reste vert si le fichier **et** les
    constantes dérivent ensemble, ou si l'artefact est remplacé sans que la
    baseline soit régénérée. Seul ce contrôle confronte le fichier à une
    prédiction réelle.
    """
    perimee = {
        **baseline,
        "metrics": {**baseline["metrics"], "recall_classe_2": 0.95},
    }
    rapport = quality_gate.Rapport()
    quality_gate.controler_golden_run(rapport, modele_servi, perimee)
    assert "G4.1" in _codes_en_echec(rapport)


def test_un_modele_sous_ses_planchers_bloque_la_gate(monkeypatch, modele_servi, baseline):
    """Un artefact dégradé ne doit pas partir en image, même concordant.

    On dégrade les planchers plutôt que le modèle : la gate doit réagir à la
    règle autant qu'à la mesure.
    """
    exigeants = {**THRESHOLDS, "recall_classe_2": 0.99}
    monkeypatch.setattr(quality_gate, "THRESHOLDS", exigeants)

    rapport = quality_gate.Rapport()
    quality_gate.controler_golden_run(rapport, modele_servi, baseline)
    assert "G4.2" in _codes_en_echec(rapport)


# --- Restitution -------------------------------------------------------------


def test_le_rapport_markdown_affiche_le_verdict_et_chaque_controle():
    rapport = quality_gate.Rapport()
    rapport.verdict("G9.9", "Contrôle factice", False, "raison lisible")
    rendu = quality_gate.rendre_markdown(rapport, {})

    assert "BLOQUE" in rendu
    assert "G9.9" in rendu
    assert "raison lisible" in rendu
    assert "❌" in rendu
