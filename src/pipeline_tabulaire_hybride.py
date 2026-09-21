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
from xmlrpc.client import boolean

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
    tabular_scenario: boolean = TABULAR_SCENARIO,
    couts=None,
    seuil_a: float | None = None,
    seuil_b: float | None = None,
    cout_revue: float | None = None,
) -> dict:
    """Prédictions hors-échantillon (5-fold CV, train uniquement) pour un scénario hybride.

    Le Pipeline (preprocessing refit à chaque fold, sans fuite) est assemblé par
    build_hybrid_pipeline. X_train/y_train/cross_validation_folds sont passés explicitement
    par l'appelant (notebook) : ce module n'entraîne jamais rien lui-même et ne doit pas
    dépendre de variables globales du notebook.

    ``prepare_tabular_features`` dérive ``departement`` depuis ``code_insee_commune`` si besoin
    (cf. pipeline_tabulaire), avant de rattacher la colonne de texte brute.

    Les probabilités hors-échantillon sont toujours calculées (``method="predict_proba"``) : les
    prédictions dures en sont dérivées (argmax), et si ``couts``/``seuil_a``/``seuil_b``/``cout_revue``
    sont fournis, le coût métier §5.2.3 (règles de validation manuelle) est ajouté aux métriques.
    """
    pipeline_scenario = build_hybrid_pipeline(model, densify=besoin_dense, tabular_scenario=tabular_scenario)
    features_tabulaires = pipeline_tabulaire.prepare_tabular_features(X_train, tabular_scenario)
    features_hybrides = features_tabulaires.assign(**{TEXT_COLUMN: X_train[TEXT_COLUMN]})
    probas_oof = cross_val_predict(
        pipeline_scenario, features_hybrides, y_train, cv=cross_validation_folds, method="predict_proba", n_jobs=-1
    )
    y_pred_oof = probas_oof.argmax(axis=1)  # classes 0/1/2 triées : index de colonne = classe
    return metrics_module.compute_classification_metrics(
        y_train, y_pred_oof, probas=probas_oof, couts=couts, seuil_a=seuil_a, seuil_b=seuil_b, cout_revue=cout_revue
    )


def evaluer_scenario_cv(
    model,
    besoin_dense: bool,
    X_train,
    y_train,
    cross_validation_folds,
    tabular_scenario: str = TABULAR_SCENARIO,
    with_text: bool = True,
    couts=None,
    seuil_a: float | None = None,
    seuil_b: float | None = None,
    cout_revue: float | None = None,
) -> dict:
    """Évalue un scénario en CV, avec ou sans la feature texte selon ``with_text``.

    ``with_text=True``  -> pipeline hybride (tabulaire + TF-IDF du texte), ex. S1.
    ``with_text=False`` -> pipeline purement tabulaire (sans texte), ex. S4.
    """
    if with_text:
        return evaluer_scenario_hybride_cv(
            model, besoin_dense, X_train, y_train, cross_validation_folds,
            tabular_scenario=tabular_scenario,
            couts=couts, seuil_a=seuil_a, seuil_b=seuil_b, cout_revue=cout_revue,
        )
    return pipeline_tabulaire.evaluer_scenario_tabulaire_cv(
        tabular_scenario, model, besoin_dense, X_train, y_train, cross_validation_folds,
        couts=couts, seuil_a=seuil_a, seuil_b=seuil_b, cout_revue=cout_revue,
    )
