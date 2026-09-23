"""Encodage de la synthèse d'entretien en variable **catégorielle**.

Les commentaires sont nettoyés/anonymisés en amont (§3.3.2.1, notebook) et se
réduisent à 9 templates réutilisés (§3.6), en correspondance 1-1 avec 9 familles
thématiques (§4.2.2). Le texte n'est donc pas une donnée textuelle libre : il
s'agit d'une variable catégorielle à 9 modalités (+ ``texte_manquant``).

Conséquences, actées en phases 0-2 :

- la **classification zero-shot** (CamemBERT `cmarkea/distilcamembert-base-nli`)
  a servi une seule fois à produire `data/referentiel_familles.csv`, désormais une
  simple donnée versionnée : plus aucun modèle NLP n'est chargé, ni à
  l'entraînement ni à l'inférence (`transformers`/`torch` retirés du projet) ;
- la **vectorisation TF-IDF** est supprimée : elle dépensait ~68 colonnes pour
  ré-encoder 9 modalités. Le texte est désormais traité par le pipeline tabulaire
  via un ``OneHotEncoder`` sur ``famille_thematique``
  (cf. ``src.pipeline_tabulaire``).

Ce module ne conserve donc que le chargement du référentiel et l'affectation de
la famille thématique.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


# Référentiel figé des 9 familles thématiques (§4.2.2). Résolu par rapport à la
# racine du dépôt et non au cwd, pour rester valide depuis un notebook.
ROOT = Path(__file__).resolve().parent.parent
REFERENTIEL_FAMILLES_PATH = ROOT / "data" / "referentiel_familles.csv"

TEXT_COLUMN = "synthese_entretien_prepare"
FAMILLE_COLUMN = "famille_thematique"
FAMILLE_TEXTE_MANQUANT = "texte_manquant"


def charger_referentiel_familles(chemin=None) -> pd.DataFrame:
    """Charge le référentiel statique template → famille thématique (9 lignes).

    Aucun modèle NLP n'est chargé : le zero-shot CamemBERT a servi **une seule
    fois** à produire ce fichier (cf. §4.2.2), qui est désormais une simple donnée
    versionnée. ``chemin`` est résolu relativement à la racine du dépôt par défaut.
    """
    chemin = Path(chemin) if chemin is not None else REFERENTIEL_FAMILLES_PATH
    if not chemin.exists():
        raise FileNotFoundError(f"Référentiel des familles thématiques introuvable : {chemin}")
    referentiel = pd.read_csv(chemin, encoding="utf-8")
    colonnes_attendues = {
        TEXT_COLUMN,
        FAMILLE_COLUMN,
        "score_confiance",
        "modele",
        "date_etiquetage",
    }
    manquantes = colonnes_attendues - set(referentiel.columns)
    if manquantes:
        raise ValueError(f"Colonnes manquantes dans le référentiel : {sorted(manquantes)}")
    return referentiel


def assigner_famille(df: pd.DataFrame, text_column: str = TEXT_COLUMN) -> pd.DataFrame:
    """Ajoute ``famille_thematique`` par simple ``map`` sur le référentiel figé.

    Contrat : **aucun texte non vide ne doit rester non mappé**. Les chaînes vides
    (ou ``NaN``) reçoivent la modalité ``"texte_manquant"`` ; tout autre texte absent
    du référentiel lève une ``ValueError`` explicite.
    """
    if text_column not in df.columns:
        raise KeyError(f"Colonne texte absente du DataFrame : {text_column}")

    referentiel = charger_referentiel_familles()
    correspondance = dict(
        zip(referentiel[TEXT_COLUMN], referentiel[FAMILLE_COLUMN])
    )

    textes = df[text_column].fillna("").astype(str)
    mask_vide = textes.str.strip() == ""

    non_mappes = sorted(set(textes[~mask_vide]) - set(correspondance))
    if non_mappes:
        apercu = " | ".join(t[:60] for t in non_mappes[:3])
        raise ValueError(
            f"{len(non_mappes)} texte(s) absent(s) du référentiel des familles thématiques "
            f"({REFERENTIEL_FAMILLES_PATH}). Exemples : {apercu}"
        )

    resultat = df.copy()
    resultat[FAMILLE_COLUMN] = textes.map(correspondance).where(~mask_vide, FAMILLE_TEXTE_MANQUANT)
    return resultat
