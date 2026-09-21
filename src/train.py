#
# Pour chaque couple (scénario, modèle) évalué ci-dessous — scénario tabulaire S4-all ET scénario S1 hybride,
# tous les modèles/hyperparamètres —, on mesure aussi les caractéristiques d'industrialisation (§8/§9.1) :
# sauvegarde du pipeline complet, taille sérialisée sur disque, temps de fit, et latence d'inférence unitaire
# p50/p95 sur N_APPELS_LATENCE appels predict.
import time
import os
import re
from pathlib import Path

import joblib
import numpy as np

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