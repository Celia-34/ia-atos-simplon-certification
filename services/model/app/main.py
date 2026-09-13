"""Service `model` — API de scoring du risque de retour à l'emploi (scénario s1).

Charge le pipeline scikit-learn entraîné (`ColumnTransformer` + `RandomForestClassifier`)
et l'expose via `/health`, `/info`, `/predict`, `/metrics` (Prometheus). Service
**interne** : il est appelé par le `backend`, jamais directement par le
navigateur — donc pas de CORS ici.
"""
from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Request, status
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from app.metrics import observe_prediction
from app.middleware import LoggingMiddleware
from app.model_loader import load_model_and_metadata
from app.schemas import HealthResponse, InfoResponse, Prediction, UsagerFeatures

# --- Loguru -----------------------------------------------------------------

LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stderr, level="INFO", colorize=True)
logger.add(
    LOGS_DIR / "api.log",
    rotation="10 MB",
    retention="7 days",
    serialize=True,
    enqueue=True,
    level="INFO",
)

# --- Lifespan ---------------------------------------------------------------

MODELS_DIR = Path(__file__).parent.parent / "models"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modèle + métadonnées au démarrage, libère à l'arrêt."""
    app.state.model, app.state.metadata = load_model_and_metadata(MODELS_DIR)
    logger.info(
        "Model loaded: {name} {version}",
        name=app.state.metadata["model_name"],
        version=app.state.metadata["model_version"],
    )
    yield
    app.state.model = None
    logger.info("Model released")


app = FastAPI(
    title="Emploi-Retour Model Service",
    version="1.0.0",
    description="Service interne de prédiction du risque de non-retour à l'emploi (scénario s1).",
    lifespan=lifespan,
)
app.add_middleware(LoggingMiddleware)

# Expose /metrics (latence, RPS, codes retour). should_group_status_codes=False
# pour distinguer 422 (validation) de 500 (erreur modèle) dans Grafana.
Instrumentator(should_group_status_codes=False).instrument(app).expose(
    app, endpoint="/metrics", include_in_schema=False
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness : 503 si le modèle n'est pas chargé."""
    if not hasattr(app.state, "model") or app.state.model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded"
        )
    return HealthResponse(status="ok")


@app.get("/info", response_model=InfoResponse)
async def info() -> InfoResponse:
    """Métadonnées du modèle chargé."""
    meta = app.state.metadata
    return InfoResponse(
        api_version=app.version,
        model_name=meta["model_name"],
        model_version=meta["model_version"],
        model_created_at=meta["created_at"],
        metrics_holdout=meta["metrics_holdout"],
        sklearn_version=meta.get("sklearn_version"),
        dataset_sha256=meta.get("dataset_sha256"),
    )


@app.post("/predict", response_model=Prediction, status_code=status.HTTP_200_OK)
async def predict(usager: UsagerFeatures, request: Request) -> Prediction:
    """Prédit la classe de retour à l'emploi (0 = rapide, 1 = standard, 2 = à risque)."""
    request_id = getattr(request.state, "request_id", "n/a")
    try:
        X = pd.DataFrame([usager.model_dump()])
        pred = int(app.state.model.predict(X)[0])
        proba = float(app.state.model.predict_proba(X)[0, pred])
    except Exception as exc:  # noqa: BLE001 — garde large en production
        logger.bind(request_id=request_id).exception("Prediction failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {exc.__class__.__name__}",
        ) from exc

    observe_prediction(predicted_class=pred, probability=proba)
    return Prediction(
        prediction=pred,
        probability=round(proba, 4),
        model_version=app.state.metadata["model_version"],
        request_id=request_id,
    )
