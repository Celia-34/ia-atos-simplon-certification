"""Pydantic schemas for the Emploi-Retour API (scénario s1) — backend.

Dupliqué à l'identique du schéma du service `model` : le backend valide
l'entrée **avant** d'appeler le service model upstream (fail fast, pas
d'appel réseau inutile sur une saisie invalide).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


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
