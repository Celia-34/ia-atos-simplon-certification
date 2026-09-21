"""Shared benchmark metrics for the S1/S2/S3/S4 scenarios (cf. §1.4 critères de succès).

This module is model-agnostic and never fits anything itself: at this stage of
the notebook (§4, data preparation) no model has been chosen yet (that happens
in §5). Callers fit whichever estimator they want to benchmark and pass the
already-fitted model in to get its §1.4 metrics.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score

CLASSE_RETOUR_RAPIDE = 0
CLASSE_A_RISQUE = 2

METRIC_LABELS = {
    "accuracy": "Accuracy globale",
    "f1_macro": "F1-score macro",
    "recall_classe_2": "Recall classe 2",
    "f1_classe_2": "F1-score classe 2 (minoritaire)",
    "taux_erreur_grave_2_vers_0": "Matr. confusion : Taux erreur grave (2→0)",
    "taux_erreur_0_vers_2": "Matr. confusion : Taux erreur (0→2)",
}

# Clés optionnelles ajoutées par compute_cost_metrics (§5.2.3) : absentes tant que couts/seuils
# ne sont pas fournis à compute_classification_metrics, donc jamais requises par METRIC_LABELS.
COST_METRIC_LABELS = {
    "part_alerte": "Part dossiers en alerte (validation manuelle)",
    "cout_erreurs": "Coût erreurs résiduelles (€)",
    "cout_revues": "Coût revues manuelles (€)",
    "cout_total": "Coût métier total (€)",
}

# Clés optionnelles d'industrialisation (§8/§9.1) : taille disque, temps de fit et latence predict
# p50/p95, ajoutées par l'appelant (cf. §5.6.2) ; absentes des benchmarks purement métriques.
PERF_METRIC_LABELS = {
    "taille_mo": "Taille modèle (Mo)",
    "temps_fit_s": "Temps de fit (s)",
    "latence_p50_ms": "Latence predict p50 (ms)",
    "latence_p95_ms": "Latence predict p95 (ms)",
}


def cout_total(y_true, y_pred, couts: pd.DataFrame) -> int:
    """Coût métier total en € : matrice de confusion (labels 0/1/2) × matrice de coûts (§5.2.1) fournie par l'appelant."""
    conf = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    return int((conf * couts.to_numpy()).sum())


def appliquer_regles_validation_manuelle(
    y_pred,
    probas,
    seuil_a: float,
    seuil_b: float,
    classe_risque: int = CLASSE_A_RISQUE,
    classe_rapide: int = CLASSE_RETOUR_RAPIDE,
):
    """Masque booléen 'à valider manuellement' (règles §5.2.3) : P(classe à risque) >= seuil_a,
    ou (prédiction = classe rapide et P(classe à risque) >= seuil_b).
    """
    proba_classe_risque = probas[:, classe_risque]
    regle_a = proba_classe_risque >= seuil_a
    regle_b = (y_pred == classe_rapide) & (proba_classe_risque >= seuil_b)
    return regle_a | regle_b


def compute_cost_metrics(y_true, y_pred, probas, couts: pd.DataFrame, seuil_a: float, seuil_b: float, cout_revue: float) -> dict:
    """Coût métier (erreurs résiduelles + revues) une fois les règles de validation manuelle (§5.2.3) appliquées.

    Les dossiers signalés (`a_valider`) sont supposés corrigés sans erreur par un conseiller,
    au prix de ``cout_revue`` € chacun ; les autres gardent le risque d'erreur du modèle brut.
    """
    a_valider = appliquer_regles_validation_manuelle(y_pred, probas, seuil_a, seuil_b)
    predictions_corrigees = np.where(a_valider, y_true, y_pred)
    cout_erreurs = cout_total(y_true, predictions_corrigees, couts)
    cout_revues = int(a_valider.sum()) * cout_revue
    return {
        "part_alerte": round(float(a_valider.mean()), 3),
        "cout_erreurs": cout_erreurs,
        "cout_revues": cout_revues,
        "cout_total": cout_erreurs + cout_revues,
    }


def compute_classification_metrics(
    y_true,
    y_pred,
    probas=None,
    couts: pd.DataFrame | None = None,
    seuil_a: float | None = None,
    seuil_b: float | None = None,
    cout_revue: float | None = None,
) -> dict:
    """Compute the §1.4 model metrics for one scenario's test predictions.

    When ``probas``/``couts``/``seuil_a``/``seuil_b``/``cout_revue`` are all provided, the §5.2.3
    business-cost metrics (``compute_cost_metrics``) are merged in as an additional decision
    criterion alongside F1 macro / recall — used by the §5.2.1 benchmark loop.
    """
    matrice_confusion = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])

    effectif_classe_2 = matrice_confusion[CLASSE_A_RISQUE].sum()
    erreurs_2_vers_0 = matrice_confusion[CLASSE_A_RISQUE, CLASSE_RETOUR_RAPIDE]
    taux_erreur_grave = erreurs_2_vers_0 / effectif_classe_2 if effectif_classe_2 else float("nan")

    effectif_classe_0 = matrice_confusion[CLASSE_RETOUR_RAPIDE].sum()
    erreurs_0_vers_2 = matrice_confusion[CLASSE_RETOUR_RAPIDE, CLASSE_A_RISQUE]
    taux_erreur_0_vers_2 = erreurs_0_vers_2 / effectif_classe_0 if effectif_classe_0 else float("nan")

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "recall_classe_2": recall_score(y_true, y_pred, labels=[CLASSE_A_RISQUE], average="macro"),
        "f1_classe_2": f1_score(y_true, y_pred, labels=[CLASSE_A_RISQUE], average="macro"),
        "taux_erreur_grave_2_vers_0": taux_erreur_grave,
        "taux_erreur_0_vers_2": taux_erreur_0_vers_2,
        "matrice_confusion": matrice_confusion,
    }

    if probas is not None and couts is not None and seuil_a is not None and seuil_b is not None and cout_revue is not None:
        metrics.update(compute_cost_metrics(y_true, y_pred, probas, couts, seuil_a, seuil_b, cout_revue))

    return metrics


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
    """Flatten one (scénario, modèle) pair's metrics (minus the fitted model/matrix) into a benchmark row.

    Any of the optional §5.2.3 cost keys (``COST_METRIC_LABELS``) or §8/§9.1 industrialisation keys
    (``PERF_METRIC_LABELS``) present in ``metrics`` are carried over too, so callers that add them get
    them in the row automatically ; callers that don't are unaffected (no extra columns added).
    """
    row = {"scenario": scenario, **{key: metrics[key] for key in METRIC_LABELS}}
    for extra_labels in (COST_METRIC_LABELS, PERF_METRIC_LABELS):
        for extra_key in extra_labels:
            if extra_key in metrics:
                row[extra_key] = metrics[extra_key]
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
    # Colonnes de coût §5.2.3, présentes uniquement quand compute_classification_metrics reçoit
    # couts/seuil_a/seuil_b/cout_revue : plus petit est toujours meilleur.
    "cout_erreurs": False,
    "cout_revues": False,
    "cout_total": False,
    # Colonnes d'industrialisation §8/§9.1 (taille, temps de fit, latence) : plus petit est meilleur.
    "taille_mo": False,
    "temps_fit_s": False,
    "latence_p50_ms": False,
    "latence_p95_ms": False,
}
BEST_ICON = "🟢"
WORST_ICON = "🔴"
GLOBAL_BEST_ICON = "⭐"


def write_benchmark_markdown(rows: list[dict], path: str | Path, model_label: str = "modèle fourni par l'appelant") -> pd.DataFrame:
    """Consolidate per-(scénario, modèle) metrics rows into ``benchmark.md``, one table per scénario.

    Rows missing a ``modele`` key (legacy single-model calls) default to ``model_label``.
    Best/worst values are flagged with 🟢/🔴 **par scénario** (comparaison entre modèles sur un
    même jeu de features), pas sur l'ensemble scénarios × modèles, pour éviter qu'un scénario
    globalement plus facile n'écrase les écarts entre modèles des autres scénarios.
    """
    rows = [row if "modele" in row else {"modele": model_label, **row} for row in rows]
    # Indexé (scenario, modele) pour que le DataFrame affiché/retourné regroupe par scénario
    # d'abord — les modèles sont comparés à features constantes, ce qui est l'axe le plus utile.
    benchmark_df = pd.DataFrame(rows).set_index(["scenario", "modele"]).sort_index()

    # Meilleure valeur de chaque colonne tous scénarios × modèles confondus (une seule fois par colonne),
    # en plus du meilleur/pire par scénario ci-dessous.
    global_best_masks = {}
    for column, higher_is_better in HIGHER_IS_BETTER.items():
        if column not in benchmark_df.columns:
            continue
        values = benchmark_df[column]
        best_value = values.max() if higher_is_better else values.min()
        global_best_masks[column] = values == best_value

    lines = [
        "# Benchmark des scénarios × modèles — métriques §1.4",
        "",
        "Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). "
        "Chaque scénario est rejoué sur chacun des modèles candidats "
        "(métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). "
        "Un tableau par scénario, pour comparer les modèles entre eux à features constantes.",
        "",
        f"Légende : {BEST_ICON} meilleure valeur de la colonne · {WORST_ICON} pire valeur de la colonne "
        "(comparaison entre modèles, pour ce scénario uniquement) · "
        f"{GLOBAL_BEST_ICON} meilleure valeur de la colonne tous scénarios × modèles confondus.",
    ]

    for scenario in benchmark_df.index.get_level_values("scenario").unique():
        scenario_df = benchmark_df.xs(scenario, level="scenario")

        # Repère les valeurs extrêmes (best/worst) par colonne présente pour ce scénario ; les
        # colonnes de coût (§5.2.3) sont absentes tant qu'aucun appel n'a fourni couts/seuils.
        best_masks, worst_masks = {}, {}
        for column, higher_is_better in HIGHER_IS_BETTER.items():
            if column not in scenario_df.columns:
                continue
            values = scenario_df[column]
            best_value = values.max() if higher_is_better else values.min()
            worst_value = values.min() if higher_is_better else values.max()
            best_masks[column] = values == best_value
            # Si toutes les valeurs sont égales, il n'y a pas de "pire" à distinguer du "meilleur".
            worst_masks[column] = (values == worst_value) if worst_value != best_value else pd.Series(False, index=values.index)

        display_df = scenario_df.copy()
        for column in ["taux_erreur_grave_2_vers_0", "taux_erreur_0_vers_2"]:
            display_df[column] = (display_df[column] * 100).round(1).map(lambda v: f"{v} %")
        for column in ["accuracy", "f1_macro", "recall_classe_2", "f1_classe_2"]:
            display_df[column] = display_df[column].round(3)
        if "part_alerte" in display_df.columns:
            display_df["part_alerte"] = (display_df["part_alerte"] * 100).round(1).map(lambda v: f"{v} %")
        for column in ["cout_erreurs", "cout_revues", "cout_total"]:
            if column in display_df.columns:
                display_df[column] = display_df[column].map(lambda v: f"{v:,.0f} €".replace(",", " "))
        for column in ["taille_mo", "temps_fit_s", "latence_p50_ms", "latence_p95_ms"]:
            if column in display_df.columns:
                display_df[column] = display_df[column].round(3)

        for column in best_masks:
            is_global_best = global_best_masks[column].xs(scenario, level="scenario")
            display_df[column] = [
                f"{GLOBAL_BEST_ICON}{BEST_ICON} {value}" if is_star
                else (f"{BEST_ICON} {value}" if is_best else (f"{WORST_ICON} {value}" if is_worst else str(value)))
                for value, is_best, is_worst, is_star in zip(
                    display_df[column], best_masks[column], worst_masks[column], is_global_best
                )
            ]

        all_labels = {**METRIC_LABELS, **COST_METRIC_LABELS, **PERF_METRIC_LABELS}
        headers = ["Modèle"] + [all_labels[column] for column in display_df.columns]
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = "|" + "|".join(["---"] * len(headers)) + "|"
        data_rows = [
            "| " + " | ".join([modele] + [str(value) for value in row]) + " |"
            for modele, row in zip(display_df.index, display_df.itertuples(index=False))
        ]

        lines += [
            "",
            f"## Scénario `{scenario}`",
            "",
            header_row,
            separator_row,
            *data_rows,
        ]

    lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    return benchmark_df
