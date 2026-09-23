"""Accès en lecture au stockage des feedbacks — brique B (stockage + jointure).

Le service `feedback` (brique A) écrit dans la table SQLite ``feedbacks``. Ce
module fournit la **jointure** ``feedbacks ⋈ prod_scored`` sur ``request_id``,
qui donne à `retrain.py` (brique C) des lignes labellisées enrichies des
features du dossier, ainsi que le marquage ``used_for_training`` après une
promotion réussie. Il fournit aussi `inject_mock_feedback`, utilisée par
l'endpoint de démo ``GET /mock-feedback``.

Volontairement limité à pandas + sqlite3 : le service `feedback` reste léger,
sans dépendance scikit-learn.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

TARGET_COLUMN = "classe_retour_emploi"


def load_labeled_feedback(
    feedback_db: Path, prod_scored_path: Path, *, only_new: bool = True
) -> pd.DataFrame:
    """Jointure ``feedbacks ⋈ prod_scored`` sur ``request_id``.

    Renvoie les features du dossier scoré + le ``true_label`` annoté, pour les
    dossiers déjà annotés (et non encore consommés si ``only_new``). Un
    ``request_id`` annoté mais absent de `prod_scored` est une jointure cassée :
    on lève une erreur explicite plutôt que de perdre des lignes en silence.
    """
    query = "SELECT request_id, true_label FROM feedbacks"
    if only_new:
        query += " WHERE used_for_training = 0"
    with sqlite3.connect(feedback_db) as con:
        feedback = pd.read_sql_query(query, con)

    if feedback.empty:
        return feedback

    prod = pd.read_csv(prod_scored_path, dtype={"departement": "string"})
    joined = feedback.merge(prod, on="request_id", how="inner", validate="one_to_one")
    missing = set(feedback["request_id"]) - set(joined["request_id"])
    if missing:
        raise ValueError(
            "request_id annotés absents de prod_scored (jointure cassée) : "
            f"{sorted(missing)}"
        )
    return joined


def mark_used_for_training(feedback_db: Path, request_ids: list[str]) -> None:
    """Marque des feedbacks comme consommés, après une **promotion** réussie.

    À n'appeler que si le candidat est promu : un rejet laisse les feedbacks
    non consommés, pour qu'ils soient repris au prochain réentraînement avec
    les nouvelles annotations.
    """
    if not request_ids:
        return
    with sqlite3.connect(feedback_db) as con:
        con.executemany(
            "UPDATE feedbacks SET used_for_training = 1 WHERE request_id = ?",
            [(request_id,) for request_id in request_ids],
        )


def inject_mock_feedback(
    feedback_db: Path, prod_scored_path: Path, count: int
) -> list[str]:
    """Simule l'arrivée de ``count`` feedbacks, pour tester le trigger/cron.

    Incrémental : reprend après le dernier ``request_id`` de `prod_scored` déjà
    injecté (un premier appel avec 10 insère REQ-00000..REQ-00009, l'appel
    suivant repart à REQ-00010). Le ``true_label`` est la classe réelle déjà
    connue dans `prod_scored` — c'est un mock : en production cette vérité
    terrain viendrait d'un conseiller via ``POST /feedback``.
    """
    if count <= 0:
        raise ValueError(f"count doit être positif, reçu : {count}")

    prod = pd.read_csv(prod_scored_path)
    total = len(prod)

    with sqlite3.connect(feedback_db) as con:
        existing_ids = {row[0] for row in con.execute("SELECT request_id FROM feedbacks")}

    already_injected = prod.index[prod["request_id"].isin(existing_ids)]
    start = int(already_injected.max()) + 1 if len(already_injected) else 0
    end = start + count
    if end > total:
        remaining = total - start
        raise ValueError(
            f"{count} feedbacks demandés à partir de l'index {start}, mais "
            f"prod_scored ne contient que {remaining} ligne(s) restante(s) "
            f"(sur {total} au total)."
        )

    batch = prod.iloc[start:end]
    now = datetime.now(timezone.utc).isoformat()
    inserted: list[str] = []
    with sqlite3.connect(feedback_db) as con:
        for _, row in batch.iterrows():
            con.execute(
                "INSERT INTO feedbacks (request_id, true_label, comments, created_at) "
                "VALUES (?, ?, ?, ?)",
                (
                    row["request_id"],
                    int(row[TARGET_COLUMN]),
                    "mock (cron simulé)",
                    now,
                ),
            )
            inserted.append(row["request_id"])
    return inserted
