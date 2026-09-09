"""Zero-shot classification pipeline for the free-text comments (synthese_entretien).

The comments are cleaned/anonymized upstream (§3.3.2.1, notebook). This module only
covers step 2 of §4.2.2: submitting the (few, deduplicated) comment templates to a
zero-shot classifier and reporting the result back onto every row.
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from src.metrics import evaluate_model
from src import metrics as metrics_module


DEFAULT_MODEL = "cmarkea/distilcamembert-base-nli"  # modèle français, exécutable localement
DEFAULT_HYPOTHESIS_TEMPLATE = "Ce commentaire concerne {}."
FALLBACK_LABEL = "a_valider"
DEFAULT_MAX_FEATURES = 300  # taille du vocabulaire TF-IDF pour le scénario S3
DEFAULT_MIN_DF = 2  # ignore les termes présents dans moins de 2 documents


def build_zero_shot_classifier(
    model_name: str = DEFAULT_MODEL,
    hypothesis_template: str = DEFAULT_HYPOTHESIS_TEMPLATE,
):
    """Instantiate the local zero-shot classification pipeline (requires torch)."""
    from transformers import pipeline

    return pipeline(
        task="zero-shot-classification",
        model=model_name,
        hypothesis_template=hypothesis_template,
    )


def classify_comments(
    classifier,
    comments: Sequence[str],
    candidate_labels: Sequence[str],
    confidence_threshold: float,
) -> pd.DataFrame:
    """Classify unique comments and flag low-confidence ones for manual review.

    Below ``confidence_threshold``, the family is not assigned automatically:
    the comment is marked ``FALLBACK_LABEL`` and routed to human validation (§7.2).
    """
    resultats_zero_shot = classifier(list(comments), candidate_labels=list(candidate_labels))

    familles_par_commentaire = pd.DataFrame(
        {
            "synthese_entretien_prepare": comments,
            "famille_thematique": [resultat["labels"][0] for resultat in resultats_zero_shot],
            "score_confiance": [resultat["scores"][0] for resultat in resultats_zero_shot],
        }
    )

    familles_par_commentaire["a_valider_manuellement"] = (
        familles_par_commentaire["score_confiance"] < confidence_threshold
    )
    familles_par_commentaire.loc[
        familles_par_commentaire["a_valider_manuellement"], "famille_thematique"
    ] = FALLBACK_LABEL

    return familles_par_commentaire


def merge_familles_thematiques(
    df: pd.DataFrame,
    familles_par_commentaire: pd.DataFrame,
    mask_non_vide: pd.Series,
    text_column: str = "synthese_entretien_prepare",
) -> pd.DataFrame:
    """Merge the per-template classification back onto every row of ``df``.

    Rejouable : les colonnes issues d'un précédent merge sont supprimées avant
    de refaire la jointure, pour éviter les suffixes `_x`/`_y` en cas de re-run.
    """
    colonnes_zero_shot = ["famille_thematique", "score_confiance", "a_valider_manuellement"]
    df = df.drop(columns=[colonne for colonne in colonnes_zero_shot if colonne in df.columns])

    df = df.merge(familles_par_commentaire, on=text_column, how="left")
    df.loc[~mask_non_vide, colonnes_zero_shot] = pd.NA

    return df


def _to_dense(X):
    """Convert a sparse matrix to a dense array; pass dense input through unchanged."""
    return X.toarray() if hasattr(X, "toarray") else X


def build_text_pipeline(
    model,
    densify: bool = False,
    max_features: int = DEFAULT_MAX_FEATURES,
    min_df: int = DEFAULT_MIN_DF,
) -> Pipeline:
    """Assemble the leakage-safe Pipeline(tfidf[, densify], model) for scenario S3.

    Centralizes the TF-IDF vectorizer settings so they stay consistent between
    §4.2.2 (S3 preparation) and §5 (CV benchmark, hyperparameter search).
    """
    etapes = [("tfidf", TfidfVectorizer(max_features=max_features, min_df=min_df))]
    if densify:
        etapes.append(("densify", FunctionTransformer(_to_dense)))
    etapes.append(("model", model))
    return Pipeline(steps=etapes)


def fit_and_evaluate_text_scenario(model, X_train_prepared, X_test_prepared, y_train, y_test) -> dict:
    """Fit ``model`` on scenario S3's TF-IDF features and return its §1.4 metrics.

    No model is chosen by this module: ``model`` is an unfitted estimator supplied
    by the caller (§5 picks the model family; §4 only benchmarks scenarios).
    """
    model.fit(X_train_prepared, y_train)
    return evaluate_model(model, X_test_prepared, y_test)

def evaluer_scenario_texte_cv(model, besoin_dense: bool, X_train, y_train, cv) -> dict:
    """Prédictions hors-échantillon (5-fold CV, train uniquement) pour le scénario texte S3.

    Le Pipeline (TF-IDF refit à chaque fold) est assemblé par pipeline_texte.build_text_pipeline.
    X_train/y_train/cv sont passés explicitement par l'appelant (notebook), ce module n'entraîne
    jamais rien lui-même et ne doit pas dépendre de variables globales du notebook.
    """
    pipeline_s3 = build_text_pipeline(model, densify=besoin_dense)
    y_pred_oof = cross_val_predict(pipeline_s3, X_train["synthese_entretien_prepare"], y_train, cv=cv, n_jobs=-1)
    return metrics_module.compute_classification_metrics(y_train, y_pred_oof)

