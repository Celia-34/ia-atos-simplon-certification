"""Shared benchmark metrics for the S1/S2/S3/S4 scenarios (cf. §1.4 critères de succès).

This module is model-agnostic and never fits anything itself: at this stage of
the notebook (§4, data preparation) no model has been chosen yet (that happens
in §5). Callers fit whichever estimator they want to benchmark and pass the
already-fitted model in to get its §1.4 metrics.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score

CLASSE_RETOUR_RAPIDE = 0
CLASSE_A_RISQUE = 2

METRIC_LABELS = {
    "accuracy": "Accuracy",
    "f1_macro": "F1 macro",
    "recall_classe_2": "Recall classe 2",
    "f1_classe_2": "F1 classe 2",
    "taux_erreur_grave_2_vers_0": "Taux erreur grave (2→0)",
    "taux_erreur_0_vers_2": "Taux erreur (0→2)",
}


def compute_classification_metrics(y_true, y_pred) -> dict:
    """Compute the §1.4 model metrics for one scenario's test predictions."""
    matrice_confusion = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])

    effectif_classe_2 = matrice_confusion[CLASSE_A_RISQUE].sum()
    erreurs_2_vers_0 = matrice_confusion[CLASSE_A_RISQUE, CLASSE_RETOUR_RAPIDE]
    taux_erreur_grave = erreurs_2_vers_0 / effectif_classe_2 if effectif_classe_2 else float("nan")

    effectif_classe_0 = matrice_confusion[CLASSE_RETOUR_RAPIDE].sum()
    erreurs_0_vers_2 = matrice_confusion[CLASSE_RETOUR_RAPIDE, CLASSE_A_RISQUE]
    taux_erreur_0_vers_2 = erreurs_0_vers_2 / effectif_classe_0 if effectif_classe_0 else float("nan")

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "recall_classe_2": recall_score(y_true, y_pred, labels=[CLASSE_A_RISQUE], average="macro"),
        "f1_classe_2": f1_score(y_true, y_pred, labels=[CLASSE_A_RISQUE], average="macro"),
        "taux_erreur_grave_2_vers_0": taux_erreur_grave,
        "taux_erreur_0_vers_2": taux_erreur_0_vers_2,
        "matrice_confusion": matrice_confusion,
    }


def evaluate_model(model, X_test, y_test) -> dict:
    """Compute the §1.4 metrics for an already-fitted ``model`` on the test set.

    ``model`` must already be fitted by the caller; this function only calls
    ``model.predict`` and never trains anything (cf. module docstring).
    """
    y_pred = model.predict(X_test)

    metrics = compute_classification_metrics(y_test, y_pred)
    metrics["model"] = model
    return metrics


def metrics_to_row(scenario: str, metrics: dict, modele: str | None = None) -> dict:
    """Flatten one (scénario, modèle) pair's metrics (minus the fitted model/matrix) into a benchmark row."""
    row = {"scenario": scenario, **{key: metrics[key] for key in METRIC_LABELS}}
    if modele is not None:
        row["modele"] = modele
    return row


# Sens de la performance par métrique : True = plus grand est meilleur, False = plus petit est meilleur
HIGHER_IS_BETTER = {
    "accuracy": True,
    "f1_macro": True,
    "recall_classe_2": True,
    "f1_classe_2": True,
    "taux_erreur_grave_2_vers_0": False,
    "taux_erreur_0_vers_2": False,
}
BEST_ICON = "🟢"
WORST_ICON = "🔴"


def write_benchmark_markdown(rows: list[dict], path: str | Path, model_label: str = "modèle fourni par l'appelant") -> pd.DataFrame:
    """Consolidate per-(scénario, modèle) metrics rows into ``benchmark.md`` as a comparison table.

    Rows missing a ``modele`` key (legacy single-model calls) default to ``model_label``.
    Best/worst values in each metric column (across all scenarios × modèles) are flagged
    with 🟢/🔴 so the reader spots the extremes at a glance, without relying on colored
    markdown (unsupported by plain `.md` rendering).
    """
    rows = [row if "modele" in row else {"modele": model_label, **row} for row in rows]
    benchmark_df = pd.DataFrame(rows).set_index(["modele", "scenario"]).sort_index()

    # Repère les valeurs extrêmes (best/worst) par colonne, sur les données brutes (avant arrondi/formatage).
    best_masks, worst_masks = {}, {}
    for column, higher_is_better in HIGHER_IS_BETTER.items():
        values = benchmark_df[column]
        best_value = values.max() if higher_is_better else values.min()
        worst_value = values.min() if higher_is_better else values.max()
        best_masks[column] = values == best_value
        # Si toutes les valeurs sont égales, il n'y a pas de "pire" à distinguer du "meilleur".
        worst_masks[column] = (values == worst_value) if worst_value != best_value else pd.Series(False, index=values.index)

    display_df = benchmark_df.copy()
    for column in ["taux_erreur_grave_2_vers_0", "taux_erreur_0_vers_2"]:
        display_df[column] = (display_df[column] * 100).round(1).map(lambda v: f"{v} %")
    for column in ["accuracy", "f1_macro", "recall_classe_2", "f1_classe_2"]:
        display_df[column] = display_df[column].round(3)

    for column in HIGHER_IS_BETTER:
        display_df[column] = [
            f"{BEST_ICON} {value}" if is_best else (f"{WORST_ICON} {value}" if is_worst else str(value))
            for value, is_best, is_worst in zip(display_df[column], best_masks[column], worst_masks[column])
        ]

    headers = ["Modèle", "Scénario"] + [METRIC_LABELS[column] for column in display_df.columns]
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "|" + "|".join(["---"] * len(headers)) + "|"
    data_rows = [
        "| " + " | ".join([modele, scenario] + [str(value) for value in row]) + " |"
        for (modele, scenario), row in zip(display_df.index, display_df.itertuples(index=False))
    ]

    lines = [
        "# Benchmark des scénarios × modèles — métriques §1.4",
        "",
        "Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). "
        "Chaque scénario est rejoué sur chacun des modèles candidats "
        "(métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même).",
        "",
        f"Légende : {BEST_ICON} meilleure valeur de la colonne · {WORST_ICON} pire valeur de la colonne "
        "(sur l'ensemble scénarios × modèles).",
        "",
        header_row,
        separator_row,
        *data_rows,
        "",
    ]
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    return benchmark_df
