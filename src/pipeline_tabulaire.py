"""Reusable tabular preprocessing for the employment-return scenarios.

The text-only scenario S3 deliberately lives outside this module. Scenarios S1
and S2 use the returned pipeline for their tabular component before it is
combined with a separate NLP representation.
"""

from __future__ import annotations

from collections.abc import Mapping

from PIL.features import features
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from transformers import data


NUMERIC_FEATURES = ("age", "anciennete_poste_ans")
SCENARIO_FEATURES: Mapping[str, tuple[str, ...]] = {
	"s1": (
		"age",
		"anciennete_poste_ans",
		"niveau_diplome",
		"code_rome_vise",
		"est_allocataire",
		"departement",
	),
	"s2": ("anciennete_poste_ans", "code_rome_vise", "est_allocataire"),
	"s4a": ("age", "anciennete_poste_ans", "niveau_diplome", "departement"),
	"s4b": ("anciennete_poste_ans", "niveau_diplome", "departement"),
	"s4c": ("age", "anciennete_poste_ans", "departement"),
	"s4d": ("age", "anciennete_poste_ans", "niveau_diplome"),
	"s4e": ("anciennete_poste_ans",),
}


def get_scenario_features(scenario: str) -> tuple[str, ...]:
	"""Return the tabular features selected for a documented scenario.

	Scenario names are case-insensitive. S3 is intentionally unsupported here
	because it uses only ``synthese_entretien`` and belongs to the NLP pipeline.
	"""
	normalized_scenario = scenario.lower()
	try:
		return SCENARIO_FEATURES[normalized_scenario]
	except KeyError as error:
		supported_scenarios = ", ".join(SCENARIO_FEATURES)
		raise ValueError(
			f"Scenario '{scenario}' is not supported by the tabular pipeline. "
			f"Use one of: {supported_scenarios}."
		) from error


def prepare_tabular_features(data: pd.DataFrame, scenario: str) -> pd.DataFrame:
    """Select a scenario's features and derive ``departement`` when required."""
    features = get_scenario_features(scenario)
    numeric_features = [feature for feature in features if feature in NUMERIC_FEATURES]
    categorical_features = [feature for feature in features if feature not in NUMERIC_FEATURES]
    excluded_features = [feature for feature in data.columns if feature not in features]
    print(f"Features numériques : {numeric_features}")
    print(f"Features catégorielles : {categorical_features}")
    print(f"Features exclues : {excluded_features}")
    prepared_data = data.copy()

    if "departement" in features and "departement" not in prepared_data:
        if "code_insee_commune" not in prepared_data:
            raise ValueError(
                "The 'departement' feature requires either a 'departement' or "
                "a 'code_insee_commune' column."
            )
        commune_codes = prepared_data["code_insee_commune"].astype("string")
        prepared_data["departement"] = commune_codes.str.zfill(5).str[:2]

    missing_features = sorted(set(features) - set(prepared_data.columns))
    if missing_features:
        missing_feature_names = ", ".join(missing_features)
        raise ValueError(f"Missing features for scenario '{scenario}': {missing_feature_names}.")

    return prepared_data.loc[:, features].copy()


def build_tabular_preprocessor(scenario: str) -> ColumnTransformer:
	"""Build the leakage-safe scikit-learn preprocessor for one scenario.

	Call ``fit`` only on training data, then use ``transform`` on validation or
	test data. ``nationalite_hors_ue`` and the raw municipality code are never
	selected by this module.
	"""
	features = get_scenario_features(scenario)
	numeric_features = [feature for feature in features if feature in NUMERIC_FEATURES]
	categorical_features = [feature for feature in features if feature not in NUMERIC_FEATURES]

	transformers = []
	if numeric_features:
		numeric_pipeline = Pipeline(
			steps=[
				("imputer", SimpleImputer(strategy="median")),
				("scaler", StandardScaler()),
			]
		)
		transformers.append(("numeric", numeric_pipeline, numeric_features))

	if categorical_features:
		categorical_pipeline = Pipeline(
			steps=[
				("imputer", SimpleImputer(strategy="most_frequent")),
				("encoder", OneHotEncoder(handle_unknown="ignore")),
			]
		)
		transformers.append(("categorical", categorical_pipeline, categorical_features))

	return ColumnTransformer(transformers=transformers)
