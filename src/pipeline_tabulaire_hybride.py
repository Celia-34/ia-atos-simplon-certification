"""Hybrid scenarios: TF-IDF text (S3) combined with any tabular scenario from pipeline_tabulaire.

Reuses pipeline_tabulaire.build_tabular_preprocessor for the tabular part and
pipeline_texte's TF-IDF settings for the text part, so this module only assembles
the two together without duplicating preprocessing logic.

Correction (cf. §5.6/§6/§7 du notebook) : le scénario S1, décrit dans scenarii.md comme
« approche multimodale complète » (tabulaire + synthèse d'entretien), était jusqu'ici
implémenté en tabulaire seul (pipeline_tabulaire.build_tabular_preprocessor("s1")) — un
écart entre le plan documenté et le code. Ce module généralise l'assemblage hybride,
initialement codé en dur pour "s4-age-dip", à n'importe quel scénario tabulaire (dont "s1")
afin que le code corresponde réellement au plan. La variante purement tabulaire de S1
(sans texte) est conservée sous le nom "s4-all" dans pipeline_tabulaire.SCENARIO_FEATURES,
pour continuer à mesurer l'apport du texte par comparaison.
"""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from src import metrics as metrics_module
from src import pipeline_tabulaire
from src import pipeline_texte

# Conservé pour compatibilité avec le sous-scénario hybride S3+S4-age-dip déjà utilisé en §5.2.2.
SCENARIO_HYBRIDE = "s3+s4-age-dip"
TABULAR_SCENARIO = "s4-age-dip"
TEXT_COLUMN = "synthese_entretien_prepare"
HYBRID_COLUMNS = (*pipeline_tabulaire.get_scenario_features(TABULAR_SCENARIO), TEXT_COLUMN)


def get_hybrid_columns(tabular_scenario: str = TABULAR_SCENARIO) -> tuple[str, ...]:
    """Return the tabular features + text column needed for a given hybrid scenario."""
    return (*pipeline_tabulaire.get_scenario_features(tabular_scenario), TEXT_COLUMN)


def build_hybrid_preprocessor(tabular_scenario: str = TABULAR_SCENARIO) -> ColumnTransformer:
    """Combine a tabular scenario's preprocessor with the S3 TF-IDF vectorizer.

    ``tabular_scenario`` accepte n'importe quel scénario défini dans
    ``pipeline_tabulaire.SCENARIO_FEATURES`` (ex. "s1" pour le scénario multimodal complet,
    "s4-age-dip" pour le sous-scénario hybride historique).
    """
    tabular_features = list(pipeline_tabulaire.get_scenario_features(tabular_scenario))
    return ColumnTransformer(
        transformers=[
            ("tabulaire", pipeline_tabulaire.build_tabular_preprocessor(tabular_scenario), tabular_features),
            ("text", pipeline_texte.build_tfidf_vectorizer(), TEXT_COLUMN),
        ]
    )


def build_hybrid_pipeline(model, densify: bool = False, tabular_scenario: str = TABULAR_SCENARIO) -> Pipeline:
    """Assemble the leakage-safe Pipeline(preprocessing[, densify], model) for a hybrid scenario."""
    etapes = [("preprocessing", build_hybrid_preprocessor(tabular_scenario))]
    if densify:
        etapes.append(("densify", FunctionTransformer(pipeline_texte._to_dense)))
    etapes.append(("model", model))
    return Pipeline(steps=etapes)


def evaluer_scenario_hybride_cv(
    model,
    besoin_dense: bool,
    X_train,
    y_train,
    cross_validation_folds,
    tabular_scenario: str = TABULAR_SCENARIO,
) -> dict:
    """Prédictions hors-échantillon (5-fold CV, train uniquement) pour un scénario hybride.

    Le Pipeline (preprocessing refit à chaque fold, sans fuite) est assemblé par
    build_hybrid_pipeline. X_train/y_train/cross_validation_folds sont passés explicitement
    par l'appelant (notebook) : ce module n'entraîne jamais rien lui-même et ne doit pas
    dépendre de variables globales du notebook.

    ``prepare_tabular_features`` dérive ``departement`` depuis ``code_insee_commune`` si besoin
    (cf. pipeline_tabulaire), avant de rattacher la colonne de texte brute.
    """
    pipeline_scenario = build_hybrid_pipeline(model, densify=besoin_dense, tabular_scenario=tabular_scenario)
    features_tabulaires = pipeline_tabulaire.prepare_tabular_features(X_train, tabular_scenario)
    features_hybrides = features_tabulaires.assign(**{TEXT_COLUMN: X_train[TEXT_COLUMN]})
    y_pred_oof = cross_val_predict(
        pipeline_scenario, features_hybrides, y_train, cv=cross_validation_folds, n_jobs=-1
    )
    return metrics_module.compute_classification_metrics(y_train, y_pred_oof)
