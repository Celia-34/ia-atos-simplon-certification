"""Reusable tabular preprocessing for the employment-return scenarios.

Depuis la phase 2, la synthèse d'entretien n'a plus de pipeline dédié : elle est
résumée par ``famille_thematique`` (9 modalités + ``texte_manquant``, cf.
``src.pipeline_texte.assigner_famille``) et traitée ici comme une variable
catégorielle ordinaire (OneHot). Tous les scénarios — y compris S3 (texte seul) et
S1 (multimodal complet) — passent donc par ce module.
"""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, OrdinalEncoder, StandardScaler

from src import metrics as metrics_module
from src import pipeline_texte
from src.metrics import evaluate_model



NUMERIC_FEATURES = ("age", "anciennete_poste_ans")
# Ordre croissant du niveau d'études (§2.3), encodé par OrdinalEncoder plutôt que OneHotEncoder
# pour préserver cette relation d'ordre.
NIVEAU_DIPLOME_ORDER = ["Sans diplôme", "Bac", "Bac+2", "Bac+5"]
# Représentation catégorielle de la synthèse d'entretien (§4.2.2), encodée en OneHot avec
# handle_unknown="ignore" comme les autres catégorielles.
FAMILLE_FEATURE = "famille_thematique"
SCENARIO_FEATURES: Mapping[str, tuple[str, ...]] = {
	# S1 (§4.2/§6.1) : approche multimodale complète = variables tabulaires + la synthèse
	# d'entretien sous sa forme catégorielle (famille_thematique).
	"s1": (
		"nationalite_hors_ue",
		"age",
		"anciennete_poste_ans",
		"niveau_diplome",
		"code_rome_vise",
		"est_allocataire",
		"departement",
		FAMILLE_FEATURE,
	),
	# Ablation dédiée à J0 : seule la nationalité est retirée de S1.
	"s1-sans-nationalite": (
		"age",
		"anciennete_poste_ans",
		"niveau_diplome",
		"code_rome_vise",
		"est_allocataire",
		"departement",
		FAMILLE_FEATURE,
	),
	# S4-all : mêmes variables tabulaires que "s1", MAIS sans le texte — sert de référence pure
	# tabulaire pour mesurer l'apport réel du texte dans le scénario S1 (cf. §6.1).
	# Anciennement appelé (à tort) "s1" avant correction : cf. décision consignée en §5.6/§6.
	"s4-all": (
		"nationalite_hors_ue",
		"age",
		"anciennete_poste_ans",
		"niveau_diplome",
		"code_rome_vise",
		"est_allocataire",
		"departement",
	),
	"s2": ("anciennete_poste_ans", "code_rome_vise", "est_allocataire", FAMILLE_FEATURE),
	# S3 : texte seul. Plus de pipeline NLP séparé — une unique colonne catégorielle.
	"s3": (FAMILLE_FEATURE,),
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
	"""Return the features selected for a documented scenario.

	Scenario names are case-insensitive. S3 est désormais supporté : la synthèse
	d'entretien s'y réduit à la seule colonne catégorielle ``famille_thematique``.
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
    """Select a scenario's features, deriving ``departement`` and ``famille_thematique``.

    Les deux colonnes dérivées le sont uniquement si elles manquent : ``departement``
    depuis ``code_insee_commune``, ``famille_thematique`` depuis la synthèse d'entretien
    préparée via le référentiel figé (§4.2.2).
    """
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

    if FAMILLE_FEATURE in features and FAMILLE_FEATURE not in prepared_data:
        if pipeline_texte.TEXT_COLUMN not in prepared_data:
            raise ValueError(
                f"The '{FAMILLE_FEATURE}' feature requires either a '{FAMILLE_FEATURE}' "
                f"or a '{pipeline_texte.TEXT_COLUMN}' column."
            )
        prepared_data = pipeline_texte.assigner_famille(prepared_data)

    missing_features = sorted(set(features) - set(prepared_data.columns))
    if missing_features:
        missing_feature_names = ", ".join(missing_features)
        raise ValueError(f"Missing features for scenario '{scenario}': {missing_feature_names}.")

    return prepared_data.loc[:, features].copy()


def build_tabular_preprocessor(scenario: str) -> ColumnTransformer:
	"""Build the leakage-safe scikit-learn preprocessor for one scenario.

	Call ``fit`` only on training data, then use ``transform`` on validation or
	test data. The raw municipality code is never selected; nationality is used
	only in scenarios that explicitly include it.
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


def fit_tabular_scenario(model, X_train_prepared, y_train):
	"""Fit ``model`` on a tabular scenario's prepared training features.

	No model is chosen by this module: ``model`` is an unfitted estimator supplied
	by the caller (§5 picks the model family; §4 only benchmarks scenarios).
	"""
	model.fit(X_train_prepared, y_train)
	return model


def evaluate_tabular_scenario(model, X_test_prepared, y_test) -> dict:
	"""Evaluate an already-fitted ``model`` on a tabular scenario's prepared test features and return its §1.4 metrics."""
	return evaluate_model(model, X_test_prepared, y_test)

def evaluer_scenario_tabulaire_cv(
    nom_scenario: str,
    model,
    besoin_dense: bool,
    X_train,
    y_train,
    cross_validation_folds,
    couts=None,
    seuil_a: float | None = None,
    seuil_b: float | None = None,
    cout_revue: float | None = None,
) -> dict:
    """Prédictions hors-échantillon (5-fold CV, train uniquement) pour un scénario tabulaire.

    Le Pipeline (preprocessing refit à chaque fold, sans fuite) est assemblé par
    pipeline_tabulaire.build_scenario_pipeline, pas construit ici. X_train/y_train/cv sont
    passés explicitement par l'appelant (notebook) : ce module n'entraîne jamais rien lui-même
    et ne doit pas dépendre de variables globales du notebook.

    Les probabilités hors-échantillon sont toujours calculées (``method="predict_proba"``) : les
    prédictions dures en sont dérivées (argmax), et si ``couts``/``seuil_a``/``seuil_b``/``cout_revue``
    sont fournis, le coût métier §5.2.3 (règles de validation manuelle) est ajouté aux métriques.
    """

    features_train = prepare_tabular_features(X_train, nom_scenario)
    pipeline_scenario = build_scenario_pipeline(nom_scenario, model, densify=besoin_dense)
	# Effectue les prédictions hors-échantillon (probabilités) pour chaque fold de la CV.
    probas_oof = cross_val_predict(
        pipeline_scenario, features_train, y_train, cv=cross_validation_folds, method="predict_proba", n_jobs=-1
    )
    y_pred_oof = probas_oof.argmax(axis=1)  # classes 0/1/2 triées : index de colonne = classe
    return metrics_module.compute_classification_metrics(
        y_train, y_pred_oof, probas=probas_oof, couts=couts, seuil_a=seuil_a, seuil_b=seuil_b, cout_revue=cout_revue
    )


