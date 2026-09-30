"""Tracking d'expériences MLflow — **strictement optionnel**.

Ce module est une façade. Il existe pour que l'ajout d'un serveur de tracking
ne puisse jamais casser ce qui marchait sans lui :

* si ``mlflow`` n'est pas installé, ou si ``MLFLOW_TRACKING_URI`` n'est pas
  définie, toutes les fonctions deviennent des no-op et renvoient ``None`` ;
* aucune exception de tracking ne remonte à l'appelant. Perdre la trace d'un
  run est ennuyeux ; perdre un entraînement de 40 minutes parce qu'un serveur
  de métadonnées était injoignable est inacceptable.

**Ce que MLflow apporte, et que les livrables markdown n'apportaient pas.**
Le projet trace déjà ses expériences par ``benchmark.md`` / ``baseline.md`` /
``comparaison_finalistes.md`` (générés par le notebook via
``src/metrics.py::write_benchmark_markdown``) et par ``decisions_log.jsonl``
(promotions et rejets). C'est reproductible, diffable en revue et lisible par
un jury — ces fichiers restent la source de vérité des livrables. Il leur
manque trois choses, et trois seulement :

1. le **rattachement artefact ↔ run** autrement que par un champ ``git_commit``
   recopié à la main ;
2. la **comparaison multi-runs** sans régénérer un markdown ;
3. un **cycle de vie de modèle** (``Staging`` → ``Production``) sur lequel
   brancher ``scripts/promotion.py``.

MLflow est retenu plutôt que W&B parce qu'il est auto-hébergeable : un
traitement fondé sur l'art. 6.1.e RGPD portant sur des demandeurs d'emploi
n'envoie pas ses métadonnées chez un tiers. Plutôt que DVC, parce que DVC
versionne bien les données mais suit mal les métriques de modèle.

Usage::

    export MLFLOW_TRACKING_URI=http://localhost:5000   # ou file:./mlruns
    python scripts/retrain.py
"""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

LOGGER = logging.getLogger(__name__)

EXPERIMENT_DEFAUT = "emploi-retour"
VARIABLE_URI = "MLFLOW_TRACKING_URI"

# Clés de métadonnées qui sont des **métriques** et non des paramètres : elles
# sont numériques et comparables entre runs. Tout le reste part en `params`.
BLOCS_DE_METRIQUES = ("metriques_test", "metrics_holdout", "metrics_reference")

_avertissement_emis = False


def _avertir_une_fois(message: str) -> None:
    """Un entraînement de benchmark produit des dizaines de runs : sans ce
    garde, l'absence de serveur noierait la sortie sous le même avertissement."""
    global _avertissement_emis
    if not _avertissement_emis:
        LOGGER.warning("Tracking MLflow désactivé : %s", message)
        _avertissement_emis = True


def uri_configuree() -> str | None:
    return os.environ.get(VARIABLE_URI) or None


def _mlflow():
    """Importe MLflow à la demande, ou renvoie ``None``.

    L'import est différé : ``import mlflow`` coûte plusieurs secondes et tire
    un arbre de dépendances important. Le payer au chargement de ``src``
    ralentirait chaque cellule du notebook, y compris celles qui ne tracent
    rien.
    """
    if not uri_configuree():
        _avertir_une_fois(f"{VARIABLE_URI} non définie")
        return None
    try:
        import mlflow  # noqa: PLC0415
    except ImportError:
        _avertir_une_fois("le paquet `mlflow` n'est pas installé")
        return None
    return mlflow


def _aplatir(prefixe: str, valeur: Any, sortie: dict[str, Any]) -> None:
    """Aplatit les métadonnées imbriquées en clés ``a.b.c``.

    MLflow n'accepte que des paires plates ; ``dataset.version`` est plus
    parlant qu'un dictionnaire sérialisé en chaîne.
    """
    if isinstance(valeur, dict):
        for cle, sous_valeur in valeur.items():
            _aplatir(f"{prefixe}.{cle}" if prefixe else str(cle), sous_valeur, sortie)
    elif isinstance(valeur, (list, tuple)):
        sortie[prefixe] = ", ".join(str(element) for element in valeur)
    elif valeur is not None:
        sortie[prefixe] = valeur


def separer_params_et_metriques(
    metadata: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, float]]:
    """Répartit les métadonnées entre `params` (figés) et `metrics` (comparables).

    La distinction n'est pas cosmétique : MLflow ne trace de courbes et ne
    classe des runs que sur les `metrics`. Ranger une métrique en `param` la
    rend invisible aux comparaisons, ce qui est précisément l'usage recherché.
    """
    params: dict[str, Any] = {}
    metriques: dict[str, float] = {}

    for cle, valeur in metadata.items():
        if cle in BLOCS_DE_METRIQUES and isinstance(valeur, dict):
            for nom, mesure in valeur.items():
                try:
                    metriques[nom] = float(mesure)
                except (TypeError, ValueError):
                    continue
        else:
            _aplatir(cle, valeur, params)

    # La matrice de confusion n'est ni un paramètre ni une métrique scalaire :
    # elle part en artefact (cf. `log_run`), pas en `params` illisible.
    params.pop("matrice_confusion_test", None)
    return params, metriques


@contextmanager
def run(nom: str, experiment: str = EXPERIMENT_DEFAUT) -> Iterator[Any]:
    """Contexte de run MLflow, transparent quand le tracking est désactivé.

    Cède ``None`` si MLflow est indisponible, pour que l'appelant puisse écrire
    le même code dans les deux cas.
    """
    mlflow = _mlflow()
    if mlflow is None:
        yield None
        return
    try:
        mlflow.set_experiment(experiment)
        with mlflow.start_run(run_name=nom) as run_actif:
            yield run_actif
    except Exception as erreur:  # noqa: BLE001 - le tracking ne doit rien casser
        _avertir_une_fois(f"serveur injoignable ({erreur})")
        yield None


def log_run(
    nom: str,
    metadata: dict[str, Any],
    artefacts: list[Path] | None = None,
    tags: dict[str, str] | None = None,
    experiment: str = EXPERIMENT_DEFAUT,
    modele: Any | None = None,
    nom_modele_registre: str | None = None,
) -> str | None:
    """Enregistre un run complet à partir d'un dictionnaire de métadonnées.

    Conçu pour consommer **telles quelles** les métadonnées déjà produites par
    ``src/train.py::save_metadata`` et ``scripts/export_model_prod.py`` : le
    tracking ne crée pas un second vocabulaire concurrent de celui des
    fichiers ``.metadata.json``. Renvoie l'identifiant du run, ou ``None``.
    """
    mlflow = _mlflow()
    if mlflow is None:
        return None

    params, metriques = separer_params_et_metriques(metadata)
    try:
        with run(nom, experiment) as run_actif:
            if run_actif is None:
                return None
            if params:
                mlflow.log_params(params)
            if metriques:
                mlflow.log_metrics(metriques)
            if tags:
                mlflow.set_tags(tags)
            for artefact in artefacts or []:
                chemin = Path(artefact)
                if chemin.exists():
                    mlflow.log_artifact(str(chemin))
            if modele is not None:
                mlflow.sklearn.log_model(
                    sk_model=modele,
                    artifact_path="model",
                    registered_model_name=nom_modele_registre,
                )
            return run_actif.info.run_id
    except Exception as erreur:  # noqa: BLE001
        _avertir_une_fois(f"échec de journalisation ({erreur})")
        return None


def log_decision_promotion(
    candidate_metrics: dict[str, float],
    production_metrics: dict[str, float],
    promote: bool,
    reason: str,
    feedback_count: int,
    dataset_sha256: str | None = None,
) -> str | None:
    """Trace un arbitrage de promotion — **y compris un rejet**.

    Un rejet est une issue normale de la boucle (cf. ``promotion.py``), et
    c'est la plus instructive : une série de rejets pour « gain insuffisant »
    dit que le flux de feedback n'apporte plus d'information, un rejet pour
    « régression critique » dit l'inverse. Ne tracer que les promotions
    reviendrait à ne garder que les runs qui arrangent.
    """
    metadata: dict[str, Any] = {
        "type_de_run": "promotion",
        "feedback_count": feedback_count,
        "promote": promote,
        "reason": reason,
        "metrics_reference": candidate_metrics,
    }
    if dataset_sha256:
        metadata["dataset_sha256"] = dataset_sha256

    # Les métriques de production sont préfixées pour cohabiter avec celles du
    # candidat dans un même run : c'est cette comparaison qui est l'objet du run.
    metadata["metrics_reference"] = {
        **{nom: valeur for nom, valeur in candidate_metrics.items()},
        **{f"prod_{nom}": valeur for nom, valeur in production_metrics.items()},
    }

    return log_run(
        nom=f"promotion-{'acceptee' if promote else 'rejetee'}",
        metadata=metadata,
        tags={
            "statut": "promu" if promote else "rejete",
            "etape": "retrain",
        },
    )
