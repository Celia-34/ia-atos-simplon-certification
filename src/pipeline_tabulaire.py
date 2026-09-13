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
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, OrdinalEncoder, StandardScaler
from transformers import data

from src import metrics as metrics_module
from src.metrics import evaluate_model



NUMERIC_FEATURES = ("age", "anciennete_poste_ans")
# Ordre croissant du niveau d'études (§2.3), encodé par OrdinalEncoder plutôt que OneHotEncoder
# pour préserver cette relation d'ordre.
NIVEAU_DIPLOME_ORDER = ["Sans diplôme", "Bac", "Bac+2", "Bac+5"]
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
	# Sous-scénarios S4 nommés d'après les features tabulaires conservées (§3.7/§4.4) :
	# ablation d'un proxy à la fois pour attribuer précisément son apport.
	"s4-age-dip-anc-dep": ("age", "anciennete_poste_ans", "niveau_diplome", "departement"),
	"s4-dip-anc-dep": ("anciennete_poste_ans", "niveau_diplome", "departement"),
	"s4-age-anc-dep": ("age", "anciennete_poste_ans", "departement"),
	"s4-age-dip-anc": ("age", "anciennete_poste_ans", "niveau_diplome"),
	"s4-anc": ("anciennete_poste_ans",),
	"s4-age-dip": ("age", "niveau_diplome"),
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
	ordinal_features = [feature for feature in features if feature == "niveau_diplome"]
	categorical_features = [
		feature for feature in features if feature not in NUMERIC_FEATURES and feature not in ordinal_features
	]

	transformers = []
	if numeric_features:
		numeric_pipeline = Pipeline(
			steps=[
				("imputer", SimpleImputer(strategy="median")),
				("scaler", StandardScaler()),
			]
		)
		transformers.append(("numeric", numeric_pipeline, numeric_features))

	if ordinal_features:
		ordinal_pipeline = Pipeline(
			steps=[
				("imputer", SimpleImputer(strategy="most_frequent")),
				("encoder", OrdinalEncoder(categories=[NIVEAU_DIPLOME_ORDER], handle_unknown="use_encoded_value", unknown_value=-1)),
			]
		)
		transformers.append(("ordinal", ordinal_pipeline, ordinal_features))

	if categorical_features:
		categorical_pipeline = Pipeline(
			steps=[
				("imputer", SimpleImputer(strategy="most_frequent")),
				("encoder", OneHotEncoder(handle_unknown="ignore")),
			]
		)
		transformers.append(("categorical", categorical_pipeline, categorical_features))

	return ColumnTransformer(transformers=transformers)


def _to_dense(X):
	"""Convert a sparse matrix to a dense array; pass dense input through unchanged."""
	return X.toarray() if hasattr(X, "toarray") else X


def build_scenario_pipeline(scenario: str, model, densify: bool = False) -> Pipeline:
	"""Assemble the leakage-safe Pipeline(preprocessing[, densify], model) for one scenario.

	Centralizes what §5 callers (CV benchmark, hyperparameter search) need to build a
	ready-to-fit pipeline without knowing how the ColumnTransformer is assembled or
	whether ``model`` requires dense input (ex. HistGradientBoostingClassifier).
	"""
	etapes = [("preprocessing", build_tabular_preprocessor(scenario))]
	if densify:
		etapes.append(("densify", FunctionTransformer(_to_dense)))
	etapes.append(("model", model))
	return Pipeline(steps=etapes)


def fit_and_evaluate_tabular_scenario(model, X_train_prepared, X_test_prepared, y_train, y_test) -> dict:
	"""Fit ``model`` on a tabular scenario's prepared features and return its §1.4 metrics.

	No model is chosen by this module: ``model`` is an unfitted estimator supplied
	by the caller (§5 picks the model family; §4 only benchmarks scenarios).
	"""
	model.fit(X_train_prepared, y_train)
	return evaluate_model(model, X_test_prepared, y_test)

def evaluer_scenario_tabulaire_cv(nom_scenario: str, model, besoin_dense: bool, X_train, y_train, cross_validation_folds) -> dict:
    """Prédictions hors-échantillon (5-fold CV, train uniquement) pour un scénario tabulaire.

    Le Pipeline (preprocessing refit à chaque fold, sans fuite) est assemblé par
    pipeline_tabulaire.build_scenario_pipeline, pas construit ici. X_train/y_train/cv sont
    passés explicitement par l'appelant (notebook) : ce module n'entraîne jamais rien lui-même
    et ne doit pas dépendre de variables globales du notebook.
    """
    
    features_train = prepare_tabular_features(X_train, nom_scenario)
    pipeline_scenario = build_scenario_pipeline(nom_scenario, model, densify=besoin_dense)
	# Effectue les prédictions hors-échantillon pour chaque fold de la CV.
    y_pred_oof = cross_val_predict(pipeline_scenario, features_train, y_train, cv=cross_validation_folds, n_jobs=-1)
    return metrics_module.compute_classification_metrics(y_train, y_pred_oof)

