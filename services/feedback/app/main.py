"""Service `feedback` — collecte des annotations métier (briques A et B).

``POST /feedback`` : un conseiller renvoie la **vraie** classe de retour à
l'emploi d'un dossier déjà scoré (``request_id``). On vérifie que le
``request_id`` existe (jointure avec `prod_scored.csv`), puis on stocke dans
SQLite. Quand assez de **nouveaux** feedbacks se sont accumulés, `retrain.py`
réentraîne un candidat.

Un feedback devient une **donnée d'entraînement** : une annotation fausse, mal
rattachée ou écrasée en silence dégrade le prochain modèle. D'où les quatre cas
traités explicitement :

    request_id inconnu               → 404
    label hors {0, 1, 2}             → 422 (Pydantic)
    même request_id, même label      → 201, sans doublon (rejeu réseau)
    même request_id, label différent → 409 (arbitrage humain requis)
"""

from __future__ import annotations

import os
import sqlite3
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA = Path(os.environ.get("DATA_DIR", ROOT / "data"))
DB_PATH = Path(os.environ.get("FEEDBACK_DB", DATA / "feedbacks.db"))
PROD_SCORED_PATH = DATA / "prod_scored.csv"

sys.path.insert(0, str(Path(os.environ.get("SCRIPTS_DIR", ROOT / "scripts"))))
from feedback_store import inject_mock_feedback  # noqa: E402


class Feedback(BaseModel):
    """Annotation métier sur un dossier déjà scoré."""

    request_id: str = Field(..., examples=["REQ-00042"])
    true_label: int = Field(
        ...,
        ge=0,
        le=2,
        description="0 = retour rapide, 1 = retour standard, 2 = à risque",
    )
    comments: str | None = None


def _init_db() -> None:
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS feedbacks (
                request_id TEXT PRIMARY KEY,
                true_label INTEGER NOT NULL,
                comments   TEXT,
                created_at TEXT NOT NULL,
                used_for_training INTEGER NOT NULL DEFAULT 0
            )"""
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise la base et charge les ``request_id`` valides au démarrage."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    _init_db()
    app.state.valid_ids = set(pd.read_csv(PROD_SCORED_PATH)["request_id"])
    yield


app = FastAPI(
    title="Emploi-Retour Feedback Service",
    version="1.0.0",
    description="Collecte des annotations métier alimentant la boucle de rétroaction.",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/feedback/count")
async def count() -> dict[str, int]:
    """Volume de feedbacks : total et non encore consommés par un réentraînement."""
    with sqlite3.connect(DB_PATH) as con:
        total = con.execute("SELECT COUNT(*) FROM feedbacks").fetchone()[0]
        new = con.execute(
            "SELECT COUNT(*) FROM feedbacks WHERE used_for_training = 0"
        ).fetchone()[0]
    return {"count": int(total), "new": int(new)}


@app.get("/mock-feedback")
async def mock_feedback(feedNumber: int) -> dict[str, object]:
    """Démo : simule l'arrivée de ``feedNumber`` annotations, incrémentalement."""
    if feedNumber <= 0:
        raise HTTPException(422, "feedNumber doit être un entier positif")
    try:
        inserted = inject_mock_feedback(DB_PATH, PROD_SCORED_PATH, feedNumber)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"inserted": len(inserted), "request_ids": inserted}


@app.post("/feedback", status_code=status.HTTP_201_CREATED)
async def post_feedback(fb: Feedback) -> dict[str, str]:
    """Enregistre une annotation métier."""
    if fb.request_id not in app.state.valid_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"request_id inconnu : {fb.request_id}",
        )

    with sqlite3.connect(DB_PATH) as con:
        existing = con.execute(
            "SELECT true_label FROM feedbacks WHERE request_id = ?",
            (fb.request_id,),
        ).fetchone()
        if existing is not None:
            if existing[0] != fb.true_label:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"request_id déjà annoté avec le label {existing[0]} "
                        f"(nouveau label : {fb.true_label})"
                    ),
                )
            return {"status": "stored", "request_id": fb.request_id}

        con.execute(
            "INSERT INTO feedbacks (request_id, true_label, comments, created_at) "
            "VALUES (?, ?, ?, ?)",
            (
                fb.request_id,
                fb.true_label,
                fb.comments,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
    return {"status": "stored", "request_id": fb.request_id}
