"""Contrat de l'ablation J0 : S1 sans nationalité, et rien d'autre."""

from __future__ import annotations

import pandas as pd

from src.pipeline_tabulaire import (
    get_scenario_features,
    prepare_tabular_features,
)


def test_s1_sans_nationalite_ne_retire_aucune_autre_feature():
    features_s1 = get_scenario_features("s1")
    features_ablation = get_scenario_features("s1-sans-nationalite")

    assert "nationalite_hors_ue" in features_s1
    assert "nationalite_hors_ue" not in features_ablation
    assert tuple(feature for feature in features_s1 if feature != "nationalite_hors_ue") == features_ablation
    assert "age" in features_ablation
    assert "niveau_diplome" in features_ablation
    assert "famille_thematique" in features_ablation


def test_preparer_features_ablation_ne_transmet_pas_la_nationalite():
    data = pd.DataFrame(
        {
            "nationalite_hors_ue": [1],
            "age": [35],
            "anciennete_poste_ans": [4.0],
            "niveau_diplome": ["Bac+2"],
            "code_rome_vise": ["A1203"],
            "est_allocataire": [1],
            "departement": ["75"],
            "famille_thematique": ["mobilite_geographique"],
        }
    )

    features = prepare_tabular_features(data, "s1-sans-nationalite")

    assert "nationalite_hors_ue" not in features.columns
    assert set(features.columns) == set(get_scenario_features("s1-sans-nationalite"))
