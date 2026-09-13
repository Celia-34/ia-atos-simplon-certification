"""Hybrid scenario S3+S4-age-dip: TF-IDF text (S3) combined with age + niveau_diplome (S4-age-dip).

Reuses pipeline_tabulaire.build_tabular_preprocessor for the tabular part (scenario
"s4-age-dip") and pipeline_texte's TF-IDF settings for the text part, so this module
only assembles the two together without duplicating preprocessing logic.
"""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from src import metrics as metrics_module
from src import pipeline_tabulaire
from src import pipeline_texte

SCENARIO_HYBRIDE = "s3+s4-age-dip"
TABULAR_SCENARIO = "s4-age-dip"
TEXT_COLUMN = "synthese_entretien_prepare"
HYBRID_COLUMNS = (*pipeline_tabulaire.get_scenario_features(TABULAR_SCENARIO), TEXT_COLUMN)


def build_hybrid_preprocessor() -> ColumnTransformer:
    """Combine the S4-age-dip tabular preprocessor with the S3 TF-IDF vectorizer."""
    tabular_features = list(pipeline_tabulaire.get_scenario_features(TABULAR_SCENARIO))
    return ColumnTransformer(
        transformers=[
            ("tabulaire", pipeline_tabulaire.build_tabular_preprocessor(TABULAR_SCENARIO), tabular_features),
            ("text", pipeline_texte.build_tfidf_vectorizer(), TEXT_COLUMN),
        ]
    )


def build_hybrid_pipeline(model, densify: bool = False) -> Pipeline:
    """Assemble the leakage-safe Pipeline(preprocessing[, densify], model) for the hybrid scenario."""
    etapes = [("preprocessing", build_hybrid_preprocessor())]
    if densify:
        etapes.append(("densify", FunctionTransformer(pipeline_texte._to_dense)))
    etapes.append(("model", model))
    return Pipeline(steps=etapes)


def evaluer_scenario_hybride_cv(model, besoin_dense: bool, X_train, y_train, cross_validation_folds) -> dict:
    """Prédictions hors-échantillon (5-fold CV, train uniquement) pour le scénario hybride S3+S4-age-dip.

    Le Pipeline (preprocessing refit à chaque fold, sans fuite) est assemblé par
    build_hybrid_pipeline. X_train/y_train/cross_validation_folds sont passés explicitement
    par l'appelant (notebook) : ce module n'entraîne jamais rien lui-même et ne doit pas
    dépendre de variables globales du notebook.
    """
    pipeline_scenario = build_hybrid_pipeline(model, densify=besoin_dense)
    y_pred_oof = cross_val_predict(
        pipeline_scenario, X_train[list(HYBRID_COLUMNS)], y_train, cv=cross_validation_folds, n_jobs=-1
    )
    return metrics_module.compute_classification_metrics(y_train, y_pred_oof)
