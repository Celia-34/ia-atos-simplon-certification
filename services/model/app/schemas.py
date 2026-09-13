"""Pydantic schemas for the Emploi-Retour API (scénario s1).

Alignés sur les features du pipeline `models/emploi_retour_s1.joblib`
(cf. `src/pipeline_tabulaire.py::SCENARIO_FEATURES["s1"]`).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class UsagerFeatures(BaseModel):
    """Input schema for /predict.

    Bornes informées par l'EDA du dataset `dataset_trajectoire_emploi.csv` :
    - age : 18-70 ans (dataset observé : 18-63)
    - anciennete_poste_ans : 0-40 ans
    - code_rome_vise : code ROME à 5 caractères (1 lettre + 4 chiffres)
    - departement : code département français à 2 caractères (dont 2A/2B)
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
    metrics_holdout: dict | None = None
    sklearn_version: str | None = None
    dataset_sha256: str | None = None
