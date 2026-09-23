"""Métriques métier Prometheus — service model.

En plus des métriques HTTP standard exposées par
``prometheus-fastapi-instrumentator`` (latence, RPS, codes retour), on
expose 3 métriques **métier** :

- ``emploi_retour_predictions_total`` : compteur des prédictions, labellé
  par classe prédite (0 = retour rapide, 1 = retour standard, 2 = à
  risque). La dérive de la répartition dans le temps est un signal
  d'alerte (data drift / concept drift).
- ``emploi_retour_prediction_proba`` : histogramme des probabilités de la
  classe prédite renvoyées par le modèle.
- ``emploi_retour_feature_famille_thematique_total`` : compteur des entrées
  par famille thématique. C'est la seule feature du scénario s1 dont la
  cardinalité est assez faible (10 modalités) pour être suivie en labels
  Prometheus sans explosion cardinale — et c'est aussi celle qui porte la
  synthèse d'entretien, donc la plus exposée à un changement de pratique des
  conseillers. Surveiller sa distribution, c'est surveiller le **data drift
  en entrée**, complément indispensable du drift observé en sortie.

Volontairement **non** instrumentées en labels : ``code_rome_vise`` (≈50
modalités) et ``departement`` (≈96) feraient exploser le nombre de séries ;
``age``/``anciennete_poste_ans`` relèvent d'un histogramme dédié si le besoin
se confirme.

``nationalite_hors_ue`` est un cas à part, et son exclusion relève d'une
décision et non d'une contrainte technique. Elle est redevenue une entrée de
l'API en ``v3.0.0``, et sa cardinalité (2 modalités) la rendrait triviale à
instrumenter. C'est précisément pour cela que l'interdiction doit être écrite :
labelliser une métrique Prometheus par un critère de discrimination prohibé
reviendrait à constituer un **journal permanent, non expurgeable et largement
accessible** de cette donnée — disproportionné au regard de la finalité, et
incompatible avec les droits d'effacement et de rectification. C'est la
condition **C2** de l'arbitrage `J0`.

L'audit d'équité par nationalité se fait donc **hors ligne**
(``scripts/audit_equite.py``), sur le périmètre restreint et tracé du jeu
annoté, et jamais en temps réel sur ``/metrics``.
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

FEATURE_FAMILLE_TOTAL = Counter(
    "emploi_retour_feature_famille_thematique_total",
    "Nombre de dossiers scorés, par famille thématique de la synthèse d'entretien.",
    labelnames=("famille_thematique",),
)


def observe_prediction(
    predicted_class: int, probability: float, famille_thematique: str | None = None
) -> None:
    """Enregistre une prédiction dans les métriques métier.

    Args:
        predicted_class: Classe prédite (0, 1 ou 2).
        probability: Probabilité de la classe prédite renvoyée par le modèle.
        famille_thematique: Modalité reçue en entrée, suivie pour le drift des
            features. ``None`` n'incrémente rien (aucune série parasite).
    """
    PREDICTIONS_TOTAL.labels(predicted_class=str(predicted_class)).inc()
    PREDICTION_PROBA.observe(probability)
    if famille_thematique is not None:
        FEATURE_FAMILLE_TOTAL.labels(famille_thematique=famille_thematique).inc()
