"""Pydantic schemas for the Emploi-Retour API (scénario s1).

Alignés sur les features du pipeline `models/emploi_retour_s1.joblib`
(cf. `src/pipeline_tabulaire.py::SCENARIO_FEATURES["s1"]`).

Un seul écart subsiste entre les features du pipeline et les champs de l'API :

- ``famille_thematique`` **est** un champ d'entrée : depuis la phase 2, la
  synthèse d'entretien ne se présente plus comme du texte libre mais comme une
  variable catégorielle à 9 modalités (+ ``texte_manquant``), figée dans
  ``data/referentiel_familles.csv``. Un ``Literal`` fermé est donc possible —
  et souhaitable : l'encodeur du pipeline est en ``handle_unknown="ignore"``,
  une modalité inconnue passerait silencieusement en vecteur nul.

``nationalite_hors_ue`` est, depuis ``v3.0.0``, une **feature d'entrée à part
entière** : le service la reçoit de l'appelant et ne la réécrit plus. Les 8
champs du schéma sont donc exactement les 8 features du scénario s1, et les
métriques annoncées par ``/info`` sont celles du modèle réellement servi.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# Les 9 familles thématiques du référentiel figé (§4.2.2), plus la modalité
# ``texte_manquant`` utilisée lorsqu'aucune synthèse n'a été saisie. Cette liste
# DOIT rester synchronisée avec `data/referentiel_familles.csv` : le test
# `tests/test_referentiel_familles.py` et le contract test du service en sont
# les garde-fous.
FamilleThematique = Literal[
    "compétences techniques à jour et reprise rapide",
    "dynamisme et clarté du projet professionnel",
    "freins périphériques et illettrisme numérique",
    "garde d'enfants et absence de moyen de transport",
    "mobilité géographique et zone mal desservie",
    "perte de confiance et barrière de la langue",
    "profil autonome sans aucun frein",
    "reconversion et besoin de formation",
    "réactualisation des compétences sur les outils numériques",
    "texte_manquant",
]

# Statut réglementaire de `nationalite_hors_ue`, exposé tel quel dans l'OpenAPI
# du service : tout intégrateur qui lit le contrat lit aussi les limites de
# l'usage autorisé. C'est le seul endroit du code où cette donnée est décrite,
# et il est volontairement explicite.
NATIONALITE_DESCRIPTION = (
    "Nationalité hors Union européenne : 1 (hors UE), 0 (UE). "
    "DONNÉE SENSIBLE — collectée au titre de l'arbitrage métier et juridique "
    "J0, sur la base légale de l'art. 6.1.e RGPD (mission d'intérêt public). "
    "Finalité strictement limitée à la priorisation vers un accompagnement "
    "renforcé : tout usage de contrôle, de sanction, de radiation ou de refus "
    "est exclu. Cette variable est conservée parce qu'elle AMÉLIORE la "
    "détection du public le plus exposé (recall classe 2 : 0.800 hors UE contre "
    "0.529 UE, §7.2) et parce qu'elle est l'axe obligatoire de l'audit "
    "d'équité. Elle ne doit être ni journalisée, ni exposée en supervision, ni "
    "réutilisée hors de ce traitement."
)


class UsagerFeatures(BaseModel):
    """Input schema for /predict.

    Bornes informées par l'EDA du dataset `dataset_trajectoire_emploi.csv` :
    - age : 18-70 ans (dataset observé : 18-63)
    - anciennete_poste_ans : 0-40 ans
    - code_rome_vise : code ROME à 5 caractères (1 lettre + 4 chiffres)
    - departement : code département français à 2 caractères (dont 2A/2B)
    - famille_thematique : synthèse d'entretien réduite à ses 9 familles
    - nationalite_hors_ue : donnée sensible, cf. la description du champ
    """

    age: int = Field(..., ge=18, le=70, description="Âge de l'usager en années")
    anciennete_poste_ans: float = Field(
        ..., ge=0, le=40, description="Ancienneté dans le dernier poste occupé (années)"
    )
    niveau_diplome: Literal["Sans diplôme", "Bac", "Bac+2", "Bac+5"] = Field(
        ..., description="Plus haut niveau de diplôme obtenu"
    )
    code_rome_vise: str = Field(
        ...,
        min_length=5,
        max_length=5,
        pattern=r"^[A-Z]\d{4}$",
        description="Code ROME à 5 caractères du métier visé",
    )
    est_allocataire: int = Field(
        ..., ge=0, le=1, description="Statut d'indemnisation : 1 (Oui), 0 (Non)"
    )
    departement: str = Field(
        ...,
        pattern=r"^(\d{2}|2A|2B)$",
        description="Code département de résidence (2 caractères, ex. '75', '2A')",
    )
    famille_thematique: FamilleThematique = Field(
        ...,
        description=(
            "Famille thématique de la synthèse d'entretien : le frein ou l'atout "
            "principal identifié par le conseiller. 'texte_manquant' si aucune "
            "synthèse n'a été saisie."
        ),
    )
    nationalite_hors_ue: int = Field(
        ...,
        ge=0,
        le=1,
        description=NATIONALITE_DESCRIPTION,
    )


class Prediction(BaseModel):
    """Output schema for /predict."""

    prediction: int = Field(
        ..., description="Classe prédite : 0 = retour rapide, 1 = retour standard, 2 = à risque"
    )
    probability: float = Field(..., ge=0.0, le=1.0, description="Probabilité de la classe prédite")
    model_version: str
    request_id: str


class HealthResponse(BaseModel):
    """Output schema for /health."""

    status: str


class InfoResponse(BaseModel):
    """Output schema for /info."""

    api_version: str
    model_name: str
    model_version: str
    model_created_at: str
    scenario: str | None = None
    feature_columns_numeric: list[str] = []
    feature_columns_categorical: list[str] = []
    metrics_holdout: dict | None = None
    sklearn_version: str | None = None
    dataset_sha256: str | None = None
