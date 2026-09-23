"""Fixtures partagées : chaque test travaille sur une base de feedbacks isolée.

``FEEDBACK_DB`` doit être positionnée **avant** l'import du service, qui résout
le chemin de la base au chargement du module.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

PROD_SCORED_PATH = ROOT / "data" / "prod_scored.csv"
SCHEMA = """CREATE TABLE IF NOT EXISTS feedbacks (
    request_id TEXT PRIMARY KEY,
    true_label INTEGER NOT NULL,
    comments   TEXT,
    created_at TEXT NOT NULL,
    used_for_training INTEGER NOT NULL DEFAULT 0
)"""


@pytest.fixture
def feedback_db(tmp_path: Path) -> Path:
    """Base SQLite vide, au schéma du service."""
    db_path = tmp_path / "feedbacks.db"
    with sqlite3.connect(db_path) as con:
        con.execute(SCHEMA)
    return db_path


@pytest.fixture
def prod_scored_path() -> Path:
    return PROD_SCORED_PATH
