"""Politique de promotion du modèle Emploi-Retour — brique D.

Répond à *« pourquoi déployer ? »*, question distincte du trigger de
réentraînement (*« pourquoi réentraîner ? »*). Rejeter un candidat est une
issue normale : elle est tracée dans `decisions_log.jsonl` et défendable.

Module volontairement sans dépendance : la décision est une **fonction pure**
sur des dictionnaires de métriques, testable sans entraîner quoi que ce soit.
"""

from __future__ import annotations

from dataclasses import dataclass

# Sens de la performance : la classe 2 (risque de non-retour > 12 mois) est la
# classe minoritaire et coûteuse ; son taux d'erreur grave 2→0 (un dossier à
# risque classé « retour rapide », donc privé d'accompagnement) se minimise.
HIGHER_IS_BETTER: dict[str, bool] = {
    "accuracy": True,
    "f1_macro": True,
    "f1_classe_2": True,
    "recall_classe_2": True,
    "taux_erreur_grave_2_vers_0": False,
}

# Cibles métier §1.4 (criteria.md), rappelées ici pour mémoire : elles ne sont
# PAS les planchers de promotion. Le modèle v2.0.0 en production ne les atteint
# pas encore (recall classe 2 = 0.571 pour une cible de 0.80) ; les utiliser
# comme planchers rejetterait tout candidat, y compris ceux qui rapprochent le
# modèle de la cible. Cet écart est un choix à défendre, pas un oubli.
CIBLES_METIER: dict[str, float] = {
    "accuracy": 0.70,
    "f1_macro": 0.65,
    "f1_classe_2": 0.60,
    "recall_classe_2": 0.80,
    "taux_erreur_grave_2_vers_0": 0.05,
}

# Planchers de non-régression, calibrés sous la performance du golden run
# v2.0.0 mesuré sur data/reference_set.csv (accuracy 0.706, f1_macro 0.684,
# f1_classe_2 0.585, recall_classe_2 0.571, erreur 2→0 0.095). Un candidat qui
# passe sous ces valeurs n'est plus un modèle acceptable, quel que soit son
# gain ailleurs.
#
# Recalibrés en phase 4 : les planchers précédents (recall 0.58, erreur 2→0
# 0.10) avaient été calés sur le golden run v1.0.0. Le modèle v2.0.0 — S1 avec
# `famille_thematique` en one-hot et nationalité neutralisée — est plus précis
# globalement mais moins sensible sur la classe 2 ; conservés tels quels, ces
# planchers auraient rejeté le modèle **de production lui-même**, rendant toute
# promotion impossible. Un plancher qu'aucun modèle servi ne franchit n'est pas
# un garde-fou, c'est un blocage.
THRESHOLDS: dict[str, float] = {
    "accuracy": 0.65,
    "f1_macro": 0.65,
    "f1_classe_2": 0.55,
    "recall_classe_2": 0.53,
    "taux_erreur_grave_2_vers_0": 0.12,
}

# Métriques protégées contre toute régression : détecter les dossiers à risque
# (recall classe 2) et ne pas les renvoyer vers « retour rapide » (erreur 2→0)
# sont les deux engagements métier du modèle. L'accuracy globale, elle, peut
# reculer légèrement si la classe 2 progresse.
CRITICAL_METRICS: tuple[str, ...] = ("recall_classe_2", "taux_erreur_grave_2_vers_0")

# Bruit d'échantillonnage sur 350 lignes de référence : en deçà, un écart n'est
# pas un signal.
TOLERANCE = 0.01
MIN_GAIN = 0.01


@dataclass(frozen=True)
class PromotionDecision:
    """Résultat de l'arbitrage candidat vs production."""

    promote: bool
    reason: str


def _missing_metrics(metrics: dict[str, float]) -> list[str]:
    return [name for name in THRESHOLDS if name not in metrics]


def _gain(metric: str, candidate: dict[str, float], production: dict[str, float]) -> float:
    """Progrès signé du candidat : toujours positif quand le candidat est meilleur."""
    delta = candidate[metric] - production[metric]
    return delta if HIGHER_IS_BETTER[metric] else -delta


def _violates_threshold(metric: str, value: float) -> bool:
    threshold = THRESHOLDS[metric]
    return value < threshold if HIGHER_IS_BETTER[metric] else value > threshold


def decide_promotion(
    candidate: dict[str, float],
    production: dict[str, float],
) -> PromotionDecision:
    """Applique la politique de promotion à deux jeux de métriques.

    Candidat et production doivent avoir été évalués sur le **même** jeu de
    référence figé. Le candidat est promu s'il respecte tous les planchers, ne
    régresse sur aucune métrique critique au-delà de ``TOLERANCE``, et progresse
    d'au moins ``MIN_GAIN`` sur au moins une métrique suivie.
    """
    missing = sorted(set(_missing_metrics(candidate) + _missing_metrics(production)))
    if missing:
        return PromotionDecision(
            False,
            "Métriques manquantes pour comparer les modèles : " + ", ".join(missing),
        )

    floor_violations = [
        f"{metric}={candidate[metric]:.4f} hors du plancher {THRESHOLDS[metric]:.2f}"
        for metric in THRESHOLDS
        if _violates_threshold(metric, candidate[metric])
    ]
    if floor_violations:
        return PromotionDecision(
            False, "Plancher de qualité non respecté : " + " ; ".join(floor_violations)
        )

    critical_regressions = [
        f"{metric} recule de {abs(_gain(metric, candidate, production)):.4f} "
        f"(tolérance {TOLERANCE:.2f})"
        for metric in CRITICAL_METRICS
        if _gain(metric, candidate, production) < -TOLERANCE
    ]
    if critical_regressions:
        return PromotionDecision(
            False, "Régression critique : " + " ; ".join(critical_regressions)
        )

    gains = {metric: _gain(metric, candidate, production) for metric in THRESHOLDS}
    best_metric, best_gain = max(gains.items(), key=lambda item: item[1])
    if best_gain < MIN_GAIN:
        return PromotionDecision(
            False,
            f"Aucun gain d'au moins {MIN_GAIN:.2f} ; "
            f"meilleur gain : {best_metric} ({best_gain:+.4f})",
        )

    return PromotionDecision(
        True,
        f"Promotion acceptée : {best_metric} progresse de {best_gain:+.4f} ; "
        "planchers respectés et métriques critiques protégées.",
    )
