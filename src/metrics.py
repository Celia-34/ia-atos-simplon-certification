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


def metrics_to_row(scenario: str, metrics: dict) -> dict:
    """Flatten one scenario's metrics (minus the fitted model/matrix) into a benchmark row."""
    return {"scenario": scenario, **{key: metrics[key] for key in METRIC_LABELS}}


def write_benchmark_markdown(rows: list[dict], path: str | Path, model_label: str = "modèle fourni par l'appelant") -> pd.DataFrame:
    """Consolidate per-scenario metrics rows into ``benchmark.md`` as a comparison table."""
    benchmark_df = pd.DataFrame(rows).set_index("scenario").sort_index()

    display_df = benchmark_df.copy()
    for column in ["taux_erreur_grave_2_vers_0", "taux_erreur_0_vers_2"]:
        display_df[column] = (display_df[column] * 100).round(1).map(lambda v: f"{v} %")
    for column in ["accuracy", "f1_macro", "recall_classe_2", "f1_classe_2"]:
        display_df[column] = display_df[column].round(3)

    headers = ["Scénario"] + [METRIC_LABELS[column] for column in display_df.columns]
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "|" + "|".join(["---"] * len(headers)) + "|"
    data_rows = [
        "| " + " | ".join([scenario] + [str(value) for value in row]) + " |"
        for scenario, row in zip(display_df.index, display_df.itertuples(index=False))
    ]

    lines = [
        "# Benchmark des scénarios — métriques §1.4",
        "",
        "Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§4.2). "
        f"Modèle utilisé : {model_label} (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même).",
        "",
        header_row,
        separator_row,
        *data_rows,
        "",
    ]
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    return benchmark_df
