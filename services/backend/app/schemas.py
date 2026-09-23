"""Pydantic schemas for the Emploi-Retour API (scénario s1) — backend.

Dupliqué à l'identique du schéma du service `model` : le backend valide
l'entrée **avant** d'appeler le service model upstream (fail fast, pas
d'appel réseau inutile sur une saisie invalide).

La duplication est assumée : le backend est bâti depuis `services/backend/`
seul, sans accès à `src/` ni au package `app` du service model. Toute
modification ici doit être répercutée dans
`services/model/app/schemas.py` — `services/frontend/tests/test_frontend.py`
vérifie que le formulaire reste aligné sur ce fichier.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# 9 familles thématiques du référentiel figé (`data/referentiel_familles.csv`,
# §4.2.2) + `texte_manquant`. Depuis la phase 2, la synthèse d'entretien est une
# variable catégorielle et non du texte libre : un Literal fermé est donc le bon
# contrat d'entrée.
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


class UsagerFeatures(BaseModel):
    """Input schema for /score."""

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


class Prediction(BaseModel):
    """Output schema for /score."""

    prediction: int = Field(
        ..., description="Classe prédite : 0 = retour rapide, 1 = retour standard, 2 = à risque"
    )
    probability: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    request_id: str


class HealthResponse(BaseModel):
    """Output schema for /health."""

    status: str
