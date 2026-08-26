"""Zero-shot classification pipeline for the free-text comments (synthese_entretien).

The comments are cleaned/anonymized upstream (§3.3.2.1, notebook). This module only
covers step 2 of §4.2.2: submitting the (few, deduplicated) comment templates to a
zero-shot classifier and reporting the result back onto every row.
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

from src.metrics import evaluate_model

DEFAULT_MODEL = "cmarkea/distilcamembert-base-nli"  # modèle français, exécutable localement
DEFAULT_HYPOTHESIS_TEMPLATE = "Ce commentaire concerne {}."
FALLBACK_LABEL = "a_valider"


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


def evaluate_text_scenario(model, X_train_prepared, X_test_prepared, y_train, y_test) -> dict:
    """Fit ``model`` on scenario S3's TF-IDF features and return its §1.4 metrics.

    No model is chosen by this module: ``model`` is an unfitted estimator supplied
    by the caller (§5 picks the model family; §4 only benchmarks scenarios).
    """
    model.fit(X_train_prepared, y_train)
    return evaluate_model(model, X_test_prepared, y_test)
