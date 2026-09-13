"""Métriques métier Prometheus — service model.

En plus des métriques HTTP standard exposées par
``prometheus-fastapi-instrumentator`` (latence, RPS, codes retour), on
expose 2 métriques **métier** :

- ``emploi_retour_predictions_total`` : compteur des prédictions, labellé
  par classe prédite (0 = retour rapide, 1 = retour standard, 2 = à
  risque). La dérive de la répartition dans le temps est un signal
  d'alerte (data drift / concept drift).
- ``emploi_retour_prediction_proba`` : histogramme des probabilités de la
  classe prédite renvoyées par le modèle.
"""
from __future__ import annotations

from prometheus_client import Counter, Histogram

PREDICTIONS_TOTAL = Counter(
    "emploi_retour_predictions_total",
    "Nombre de prédictions servies, par classe prédite.",
    labelnames=("predicted_class",),
)

PREDICTION_PROBA = Histogram(
    "emploi_retour_prediction_proba",
    "Distribution des probabilités de la classe prédite.",
    buckets=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
)


def observe_prediction(predicted_class: int, probability: float) -> None:
    """Enregistre une prédiction dans les métriques métier.

    Args:
        predicted_class: Classe prédite (0, 1 ou 2).
        probability: Probabilité de la classe prédite renvoyée par le modèle.
    """
    PREDICTIONS_TOTAL.labels(predicted_class=str(predicted_class)).inc()
    PREDICTION_PROBA.observe(probability)
