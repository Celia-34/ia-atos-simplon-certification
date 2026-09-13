"""Single source of truth for loading the Emploi-Retour model (scénario s1).

Used by:
- ``app.main.lifespan`` — boot the API (long-running uvicorn process)
- ``tests.test_api`` — CI-time contract test (pytest process)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib

MODEL_FILENAME = "emploi_retour_s1.joblib"
METADATA_FILENAME = "emploi_retour_s1.json"


def load_model_and_metadata(models_dir: Path) -> tuple[Any, dict]:
    """Load the Emploi-Retour model and its metadata from a models directory.

    Args:
        models_dir: Directory containing ``emploi_retour_s1.joblib`` and
            ``emploi_retour_s1.json``.

    Returns:
        A ``(model, metadata)`` tuple where ``model`` is a fitted
        scikit-learn Pipeline and ``metadata`` is the parsed JSON.

    Raises:
        FileNotFoundError: If either the model or the metadata file is
            missing from ``models_dir``.
    """
    model_path = models_dir / MODEL_FILENAME
    meta_path = models_dir / METADATA_FILENAME

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    if not meta_path.exists():
        raise FileNotFoundError(f"Metadata file not found at {meta_path}")

    model = joblib.load(model_path)
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    return model, metadata
