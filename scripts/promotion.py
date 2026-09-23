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
# PAS les planchers de promotion. Le modèle v3.0.0 en production ne les atteint
# pas encore (recall classe 2 = 0.651 pour une cible de 0.80) ; les utiliser
# comme planchers rejetterait tout candidat, y compris ceux qui rapprochent le
# modèle de la cible. Cet écart est un choix à défendre, pas un oubli.
CIBLES_METIER: dict[str, float] = {
    "accuracy": 0.70,
    "f1_macro": 0.65,
    "f1_classe_2": 0.60,
    "recall_classe_2": 0.80,
    "taux_erreur_grave_2_vers_0": 0.05,
}

# Planchers de non-régression, dérivés du golden run **v3.0.0** mesuré sur
# data/reference_set.csv (accuracy 0.7171, f1_macro 0.6990, f1_classe_2 0.6029,
# recall_classe_2 0.6508, erreur 2→0 0.0794).
#
# Règle de calibration, explicite et rejouable à chaque changement de modèle
# servi : plancher = performance du golden run − 5 points, tronquée à deux
# décimales. Cinq points, c'est cinq fois TOLERANCE (le bruit d'échantillonnage
# sur 350 lignes) : assez haut pour écarter un candidat réellement dégradé,
# assez bas pour ne pas rejeter le modèle de production lui-même.
#
#   accuracy         0.7171 − 0.05 → 0.66
#   f1_macro         0.6990 − 0.05 → 0.64
#   f1_classe_2      0.6029 − 0.05 → 0.55
#   recall_classe_2  0.6508 − 0.05 → 0.60
#
# `f1_macro` passe ainsi de 0.65 à 0.64, soit un point sous la cible §1.4. C'est
# assumé : un plancher n'est pas une cible, et f1_macro n'est pas une métrique
# critique (cf. CRITICAL_METRICS) — la protection de la classe 2 est portée par
# `recall_classe_2` et `taux_erreur_grave_2_vers_0`, tous deux resserrés.
#
# `taux_erreur_grave_2_vers_0` fait exception : la règle donnerait 0.11, mais le
# plancher est ramené au **garde-fou métier §1.4 de 10 %**, que le modèle aligné
# franchit désormais (0.0794 sur le jeu de référence, 0.100 sur le test set).
# C'est la résorption durable du point #6 : la neutralisation de la phase 4
# portait ce taux à 12,2 %, ce qui avait contraint à desserrer le plancher à
# 0.12 — un garde-fou qu'aucun modèle ne pouvait plus déclencher.
#
# Historique : les planchers de la phase 4 (f1_classe_2 0.55, recall_classe_2
# 0.53, erreur 2→0 0.12) avaient été abaissés parce que le modèle à nationalité
# neutralisée ne franchissait plus ses propres seuils. Le modèle v3.0.0 étant
# meilleur sur les cinq métriques, ces valeurs n'écartaient plus rien.
THRESHOLDS: dict[str, float] = {
    "accuracy": 0.66,
    "f1_macro": 0.64,
    "f1_classe_2": 0.55,
    "recall_classe_2": 0.60,
    "taux_erreur_grave_2_vers_0": 0.10,
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
