"""Service `backend` — orchestrateur.

Exposé au navigateur (via le frontend nginx) : valide l'entrée avec le
**même schéma Pydantic** que le modèle, appelle le service `model` en
interne (`http://model:8000/predict`), et expose `/health`, `/score`,
`/metrics`.
"""
from __future__ import annotations

import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, disable_created_metrics
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import ValidationError

from app.middleware import LoggingMiddleware
from app.schemas import HealthResponse, InferenceRecord, Prediction, UsagerFeatures

# URL du service model — configurable par variable d'env (dev/staging/prod)
MODEL_URL = os.environ.get("MODEL_URL", "http://model:8000")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:8088").split(",")
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
INFERENCE_DB = Path(os.environ.get("INFERENCE_DB", DATA_DIR / "inferences.db"))


def _init_inference_db() -> None:
    INFERENCE_DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(INFERENCE_DB) as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS inferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT NOT NULL,
                prediction INTEGER NOT NULL,
                probability REAL NOT NULL,
                model_version TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    _init_inference_db()
    yield


app = FastAPI(
    title="Emploi-Retour Backend Orchestrator", version="1.0.0", lifespan=lifespan
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Request-ID"],
)

# Expose http_requests_total / http_request_duration_seconds (mêmes métriques que le model)
Instrumentator(should_group_status_codes=False).instrument(app).expose(
    app, endpoint="/metrics", include_in_schema=False
)

# Expose les erreurs cumulées lors de l'appel au model upstream, sur le même /metrics
disable_created_metrics()
backend_upstream_errors_total = Counter(
    "backend_upstream_errors_total",
    "Nombre d'erreurs rencontrées lors de l'appel au service model upstream depuis le backend.",
    labelnames=("kind",),
)
backend_upstream_errors_total.labels(kind="unavailable")
backend_upstream_errors_total.labels(kind="bad_response")
backend_score_calls_total = Counter(
    "backend_score_calls_total",
    "Nombre total d'appels au endpoint /score.",
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness du backend (ne dépend PAS du model)."""
    return HealthResponse(status="ok")


@app.get("/history", response_model=list[InferenceRecord])
async def history(limit: int = 20) -> list[InferenceRecord]:
    """Retourne les inférences récentes sans exposer les données du profil."""
    if not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="limit doit être compris entre 1 et 100")

    with sqlite3.connect(INFERENCE_DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT request_id, prediction, probability, model_version, created_at "
            "FROM inferences ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [InferenceRecord.model_validate(dict(row)) for row in rows]


@app.post("/score", response_model=Prediction)
async def score(usager: UsagerFeatures, request: Request) -> Prediction:
    """Appelle le service model et comptabilise ses erreurs upstream."""
    backend_score_calls_total.inc()
    request_id = getattr(request.state, "request_id", "n/a")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MODEL_URL}/predict",
                json=usager.model_dump(),
                headers={"X-Request-ID": request_id},
                timeout=5.0,
            )
    except httpx.RequestError as exc:
        backend_upstream_errors_total.labels(kind="unavailable").inc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model service unavailable",
        ) from exc

    if response.is_error:
        backend_upstream_errors_total.labels(kind="bad_response").inc()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Model service returned an error",
        )

    try:
        prediction = Prediction.model_validate(response.json())
    except (ValueError, ValidationError) as exc:
        backend_upstream_errors_total.labels(kind="bad_response").inc()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid response from model service",
        ) from exc

    with sqlite3.connect(INFERENCE_DB) as con:
        con.execute(
            "INSERT INTO inferences "
            "(request_id, prediction, probability, model_version, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                prediction.request_id,
                prediction.prediction,
                prediction.probability,
                prediction.model_version,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
    return prediction
