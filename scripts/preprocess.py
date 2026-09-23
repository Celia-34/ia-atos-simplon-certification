"""Préparation partagée de la boucle de rétroaction (briques B, C, D).

Rejoue **hors notebook** les étapes qui définissent le modèle servi, pour que
`build_reference_set.py`, `build_prod_scored.py` et `retrain.py` travaillent
tous sur exactement les mêmes lignes et les mêmes colonnes :

- §3.3.2.1 : nettoyage puis anonymisation de ``synthese_entretien`` →
  ``synthese_entretien_prepare``, puis mise en correspondance avec
  ``famille_thematique`` via le référentiel figé (§4.2.2) ;
- §4.1 : split 80/20 stratifié (``random_state=42``) → train / holdout ;
- §6.1 : scénario retenu ``s1`` (tabulaire + famille thématique) et modèle retenu
  ``RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)``.

Le holdout (500 lignes, jamais vu à l'entraînement) est la seule réserve
disponible ; il est partagé en **jeu de référence figé** (350 lignes, évaluation
candidat vs production) et **trafic de production** (150 lignes, sur lequel
portent les feedbacks). Les deux partitions sont disjointes : sans cela, un
feedback annoté fuiterait dans le jeu qui arbitre la promotion.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import metrics as metrics_module  # noqa: E402
from src import pipeline_tabulaire, pipeline_texte  # noqa: E402

DATA = ROOT / "data"
DATASET_PATH = DATA / "dataset_trajectoire_emploi.csv"

TARGET_COLUMN = "classe_retour_emploi"
TEXT_COLUMN = pipeline_texte.TEXT_COLUMN
RAW_TEXT_COLUMN = "synthese_entretien"
TABULAR_SCENARIO = "s1"
FEATURES = list(pipeline_tabulaire.get_scenario_features(TABULAR_SCENARIO))

RANDOM_STATE = 42
HOLDOUT_SIZE = 0.20
N_REFERENCE = 350

# Métriques §1.4 suivies par la boucle. La matrice de confusion et le modèle
# renvoyés par src.metrics sont volontairement écartés : ils ne sont pas
# sérialisables dans decisions_log.jsonl.
TRACKED_METRICS = (
    "accuracy",
    "f1_macro",
    "f1_classe_2",
    "recall_classe_2",
    "taux_erreur_grave_2_vers_0",
)

PATTERN_TELEPHONE = r"\b0[1-9](?:[\s.-]?\d{2}){4}\b"
PATTERN_EMAIL = r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}"


def nettoyer_texte(texte: str) -> str:
    """Nettoyage léger : espaces multiples et caractères parasites (§3.3.2.1)."""
    texte = re.sub(r"\s+", " ", texte)
    texte = re.sub(r"[^\w\sÀ-ÿ.,;:!?'-]", "", texte)
    return texte.strip()


def anonymiser_texte(texte: str) -> str:
    """Anonymisation basique : téléphones et emails détectés (§3.3.2.1)."""
    texte = re.sub(PATTERN_TELEPHONE, "[TELEPHONE]", texte)
    return re.sub(PATTERN_EMAIL, "[EMAIL]", texte)


def prepare_text(data: pd.DataFrame) -> pd.Series:
    """Construit ``synthese_entretien_prepare`` à partir du texte brut."""
    return (
        data[RAW_TEXT_COLUMN]
        .fillna("")
        .apply(nettoyer_texte)
        .apply(anonymiser_texte)
    )


def load_dataset(path: Path = DATASET_PATH) -> pd.DataFrame:
    """Charge le dataset brut et ajoute la colonne de texte préparée."""
    data = pd.read_csv(path, dtype={"code_insee_commune": "string"})
    return data.assign(**{TEXT_COLUMN: prepare_text(data)})


def load_prepared_csv(path: Path) -> pd.DataFrame:
    """Recharge un artefact déjà préparé (jeu de référence, trafic scoré).

    Deux relectures piègent l'affectation de famille et les encodeurs : une synthèse
    vide revient en ``NaN`` (qui doit redevenir ``""`` pour tomber sur la modalité
    ``texte_manquant``) et un code commune ou un
    département à zéro initial revient en entier (``"07"`` → ``7``), catégorie
    inconnue de l'encodeur entraîné.
    """
    data = pd.read_csv(
        path, dtype={"code_insee_commune": "string", "departement": "string"}
    )
    return data.assign(**{TEXT_COLUMN: data[TEXT_COLUMN].fillna("")})


def split_train_holdout(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split §4.1 : 80 % entraînement / 20 % holdout, stratifié sur la cible."""
    train, holdout = train_test_split(
        data,
        test_size=HOLDOUT_SIZE,
        stratify=data[TARGET_COLUMN],
        random_state=RANDOM_STATE,
    )
    return train, holdout


def split_holdout(holdout: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Partage le holdout en (jeu de référence figé, trafic de production).

    Partitions disjointes et reproductibles : les deux scripts de construction
    d'artefacts appellent cette fonction plutôt que de retirer leur propre
    échantillon, sinon le trafic de production pourrait recouvrir le jeu qui
    arbitre la promotion.
    """
    reference, production = train_test_split(
        holdout,
        train_size=N_REFERENCE,
        stratify=holdout[TARGET_COLUMN],
        random_state=RANDOM_STATE,
    )
    return reference, production


def build_features(data: pd.DataFrame) -> pd.DataFrame:
    """Sélectionne les colonnes du scénario s1, ``departement`` et ``famille_thematique`` dérivés."""
    return pipeline_tabulaire.prepare_tabular_features(data, TABULAR_SCENARIO)


def evaluate(model, data: pd.DataFrame) -> dict[str, float]:
    """Métriques §1.4 suivies par la boucle, sur un jeu déjà préparé.

    Évalué sur les features du scénario s1 **telles quelles**, nationalité
    réelle comprise : c'est exactement ce que le service reçoit depuis
    l'alignement `v3.0.0`. Candidat et modèle de production sont donc comparés
    sur la même définition de « ce que voit le modèle » que le notebook.
    """
    predictions = model.predict(build_features(data))
    computed = metrics_module.compute_classification_metrics(
        data[TARGET_COLUMN], predictions
    )
    return {name: float(computed[name]) for name in TRACKED_METRICS}


def build_pipeline() -> Pipeline:
    """Assemble le pipeline du modèle retenu en §6.1, non entraîné.

    ``RandomForestClassifier(n_estimators=300, class_weight="balanced")`` : avec
    la représentation one-hot de ``famille_thematique``, il domine les deux
    variantes de ``HistGradientBoostingClassifier`` sur toutes les métriques
    §1.4 de la sous-validation (cf. `comparaison_finalistes.md`). Le candidat du
    retrain DOIT être de la même famille **et de la même configuration** que le
    modèle servi, sinon la décision de promotion compare deux algorithmes ou
    deux réglages plutôt que deux jeux de données.

    ``class_weight="balanced"`` est porté par la lambda de
    ``MODELES_FINALISTES`` (cellule 134) mais absent du descripteur textuel
    ``"n_estimators=300"`` qui s'est propagé dans les livrables : c'est par là
    que le paramètre avait disparu de cette fonction. Le test de configuration
    (`tests/test_boucle.py`) compare désormais ces paramètres à ceux du modèle
    réellement chargé depuis ``emploi_retour_s1.joblib``.

    ``densify=False`` : RandomForest accepte la matrice creuse produite par les
    OneHotEncoder du préprocesseur, contrairement à HistGradientBoosting.
    """
    model = RandomForestClassifier(
        n_estimators=300, class_weight="balanced", random_state=RANDOM_STATE
    )
    return pipeline_tabulaire.build_scenario_pipeline(
        TABULAR_SCENARIO, model, densify=False
    )
