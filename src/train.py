#
# Pour chaque couple (scénario, modèle) évalué ci-dessous — scénario tabulaire S4-all ET scénario S1 hybride,
# tous les modèles/hyperparamètres —, on mesure aussi les caractéristiques d'industrialisation (§8/§9.1) :
# sauvegarde du pipeline complet, taille sérialisée sur disque, temps de fit, et latence d'inférence unitaire
# p50/p95 sur N_APPELS_LATENCE appels predict.
import json
import sys
import time
import os
import re
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

try:  # Import tolérant : `src.train` est chargé aussi bien comme module du
    # package `src` (scripts) que par chemin depuis le notebook.
    from src import tracking
except ImportError:  # pragma: no cover - dépend du sys.path de l'appelant
    import tracking

MODELS_DIR = Path("..") / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
N_APPELS_LATENCE = 1000


def chemin_pipeline(nom_scenario: str, nom_modele: str) -> Path:
    # Nom de fichier assaini : les descriptions d'hyperparamètres contiennent des caractères interdits sous Windows.
    nom_fichier = re.sub(r"[^0-9A-Za-z._-]", "_", f"modele_{nom_scenario}_{nom_modele}")
    return MODELS_DIR / f"{nom_fichier}.joblib"


def train(pipeline_perf, X_fit, y_fit) -> float:
    """Fit chronométré du pipeline complet ; renvoie le temps de fit en secondes."""
    debut_fit = time.perf_counter()
    pipeline_perf.fit(X_fit, y_fit)
    return time.perf_counter() - debut_fit


def save(pipeline_perf, nom_scenario, nom_modele) -> tuple[float, Path]:
    """Sérialise le pipeline sur disque et renvoie (taille en Mo, chemin)."""
    chemin_modele = chemin_pipeline(nom_scenario, nom_modele)
    joblib.dump(pipeline_perf, chemin_modele)
    taille_mo = os.path.getsize(chemin_modele) / (1024 * 1024)
    return taille_mo, chemin_modele


def _json_safe(valeur):
    """Convertit récursivement les types numpy/pandas/Path en équivalents sérialisables en JSON."""
    if isinstance(valeur, np.ndarray):
        return valeur.tolist()
    if isinstance(valeur, (np.integer, np.floating, np.bool_)):
        return valeur.item()
    if isinstance(valeur, Path):
        return str(valeur)
    if isinstance(valeur, dict):
        return {str(cle): _json_safe(sous_valeur) for cle, sous_valeur in valeur.items()}
    if isinstance(valeur, (list, tuple, set)):
        return [_json_safe(sous_valeur) for sous_valeur in valeur]
    return valeur


def save_metadata(chemin_modele, metadata: dict) -> Path:
    """Écrit les métadonnées du modèle en JSON à côté du .joblib (traçabilité §0.5/§8.1).

    Les informations d'environnement (date, versions, taille du fichier) sont ajoutées
    automatiquement ; ``metadata`` porte le contexte métier fourni par l'appelant
    (scénario, hyperparamètres, features, métriques, seuils, commit Git...).

    Le même contenu est poussé vers MLflow **si et seulement si**
    ``MLFLOW_TRACKING_URI`` est définie (cf. ``src/tracking.py``). Le fichier
    JSON reste écrit dans tous les cas : c'est lui qui fait foi, MLflow n'est
    qu'une vue comparative par-dessus. Ce branchement ici, plutôt qu'à l'appel,
    évite de modifier le notebook — clos depuis la phase 3.
    """
    chemin_modele = Path(chemin_modele)
    chemin_metadata = chemin_modele.with_suffix(".metadata.json")
    charge_utile = {
        "date_persistance": datetime.now().isoformat(timespec="seconds"),
        "chemin_modele": chemin_modele.name,
        "taille_mo": round(os.path.getsize(chemin_modele) / (1024 * 1024), 3),
        "versions": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit-learn": sklearn.__version__,
            "joblib": joblib.__version__,
        },
        **_json_safe(metadata),
    }
    chemin_metadata.write_text(
        json.dumps(charge_utile, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    tracking.log_run(
        nom=f"{charge_utile.get('scenario', 'run')}-{charge_utile.get('modele', chemin_modele.stem)}",
        metadata=charge_utile,
        artefacts=[chemin_metadata],
        tags={"etape": "entrainement", "source": "notebook"},
    )
    return chemin_metadata


def latence_performance(pipeline_perf, echantillon_unitaire) -> np.ndarray:
    """Latences (ms) de N_APPELS_LATENCE appels predict unitaires."""
    latences_ms = np.empty(N_APPELS_LATENCE)
    for i in range(N_APPELS_LATENCE):
        debut_predict = time.perf_counter()
        pipeline_perf.predict(echantillon_unitaire)
        latences_ms[i] = (time.perf_counter() - debut_predict) * 1000
    return latences_ms


def mesurer_industrialisation(pipeline_perf, X_fit, y_fit, echantillon_unitaire, nom_scenario, nom_modele) -> dict:
    """Fit chronométré + sauvegarde + taille disque + latence predict p50/p95 pour un pipeline complet.

    Le pipeline est fit sur ``X_fit``/``y_fit`` (appelant : train set uniquement), sérialisé, puis
    chronométré en inférence sur ``echantillon_unitaire``. À l'issue, ``pipeline_perf`` est entraîné
    et peut être réutilisé tel quel pour l'évaluation finale sur le test set.
    """
    temps_fit_s = train(pipeline_perf, X_fit, y_fit)
    taille_mo, chemin_modele = save(pipeline_perf, nom_scenario, nom_modele)
    latences_ms = latence_performance(pipeline_perf, echantillon_unitaire)
    return {
        "scenario": nom_scenario,
        "modele": nom_modele,
        "taille_mo": round(taille_mo, 3),
        "temps_fit_s": round(temps_fit_s, 3),
        "latence_p50_ms": round(float(np.percentile(latences_ms, 50)), 3),
        "latence_p95_ms": round(float(np.percentile(latences_ms, 95)), 3),
        "chemin_modele": str(chemin_modele),
    }