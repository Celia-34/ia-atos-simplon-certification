"""Tests de l'audit d'équité §7.2 rejoué en production — `scripts/audit_equite.py`.

L'audit porte les conditions **C3** (marquage des effectifs non fiables) et
**C4** (clause de retrait automatique de ``nationalite_hors_ue``) de l'arbitrage
`J0`. Ces deux règles sont testées sur des tableaux construits à la main : leur
correction ne doit dépendre ni du modèle servi, ni du volume de feedbacks
réellement collectés — sinon elles ne seraient vérifiables qu'en production,
c'est-à-dire trop tard.
"""

from __future__ import annotations

import pandas as pd
import pytest

from audit_equite import (
    SEUIL_EFFECTIF_FIABLE,
    controler_clause_c4,
    filet_de_securite,
    recall_classe_2_par_groupe,
)


def _analyse(lignes: list[tuple[int, int, int]]) -> pd.DataFrame:
    """(nationalite_hors_ue, classe_reelle, classe_predite) → tableau d'analyse."""
    return pd.DataFrame(
        lignes, columns=["nationalite_hors_ue", "classe_reelle", "classe_predite"]
    )


def _tableau_nationalite(
    *, effectif_ue: int, detectes_ue: int, effectif_hors_ue: int, detectes_hors_ue: int
) -> pd.DataFrame:
    lignes = [(0, 2, 2)] * detectes_ue + [(0, 2, 0)] * (effectif_ue - detectes_ue)
    lignes += [(1, 2, 2)] * detectes_hors_ue
    lignes += [(1, 2, 0)] * (effectif_hors_ue - detectes_hors_ue)
    return recall_classe_2_par_groupe(_analyse(lignes), "nationalite_hors_ue")


# --- C3 : marquage des effectifs sous le seuil de fiabilité -----------------


def test_le_recall_est_calcule_sur_le_bon_denominateur():
    """Le dénominateur est l'effectif RÉEL de classe 2, pas le nombre de
    prédictions de classe 2 : confondre les deux transformerait un recall en
    précision et inverserait la lecture de l'audit."""
    analyse = _analyse([(0, 2, 2), (0, 2, 0), (0, 2, 0), (0, 0, 2)])

    tableau = recall_classe_2_par_groupe(analyse, "nationalite_hors_ue")

    assert tableau.loc[0, "effectif_classe_2"] == 3
    assert tableau.loc[0, "detectes"] == 1
    assert tableau.loc[0, "recall_classe_2"] == pytest.approx(0.333, abs=1e-3)


def test_un_sous_groupe_sous_le_seuil_est_marque_non_fiable():
    """Condition C3 : sans ce marquage, l'audit reproduirait le défaut que le
    notebook dénonce lui-même — conclure sur des effectifs trop faibles."""
    tableau = _tableau_nationalite(
        effectif_ue=SEUIL_EFFECTIF_FIABLE,
        detectes_ue=10,
        effectif_hors_ue=SEUIL_EFFECTIF_FIABLE - 1,
        detectes_hors_ue=5,
    )

    assert tableau.loc[0, "fiabilite"] == "fiable"
    assert tableau.loc[1, "fiabilite"] == "effectif insuffisant"


# --- C4 : clause de retrait automatique -------------------------------------


def test_c4_est_declenchee_quand_le_recall_hors_ue_passe_sous_le_recall_ue():
    """C'est l'hypothèse qui fonde tout l'arbitrage `J0` : la variable est
    conservée parce qu'elle AMÉLIORE la détection des usagers hors UE. Si le
    constat s'inverse, la justification tombe et le retrait est dû."""
    tableau = _tableau_nationalite(
        effectif_ue=40, detectes_ue=30, effectif_hors_ue=40, detectes_hors_ue=10
    )

    resultat = controler_clause_c4(tableau)

    assert resultat["statut"] == "declenchee"
    assert resultat["recall_hors_ue"] < resultat["recall_ue"]


def test_c4_est_respectee_quand_la_detection_hors_ue_reste_superieure():
    tableau = _tableau_nationalite(
        effectif_ue=40, detectes_ue=20, effectif_hors_ue=40, detectes_hors_ue=32
    )

    assert controler_clause_c4(tableau)["statut"] == "respectee"


def test_c4_reste_indeterminee_sur_un_effectif_insuffisant():
    """Le point le plus important du contrôle.

    Un effectif trop faible ne permet ni de déclencher la clause, ni de la
    déclarer respectée. La déclarer respectée par défaut transformerait un
    manque de données en satisfecit — exactement l'erreur que C3 interdit.
    """
    tableau = _tableau_nationalite(
        effectif_ue=40, detectes_ue=20, effectif_hors_ue=5, detectes_hors_ue=1
    )

    resultat = controler_clause_c4(tableau)

    assert resultat["statut"] == "indeterminee"
    assert "seuil de fiabilité" in resultat["motif"]


def test_c4_reste_indeterminee_si_une_modalite_est_absente():
    """Un flux annoté ne contenant que des usagers UE ne dit rien de l'équité."""
    tableau = recall_classe_2_par_groupe(_analyse([(0, 2, 2), (0, 2, 0)]), "nationalite_hors_ue")

    assert controler_clause_c4(tableau)["statut"] == "indeterminee"


def test_une_egalite_stricte_des_recalls_ne_declenche_pas_le_retrait():
    """C4 vise une **infériorité**. Déclencher sur l'égalité rendrait la clause
    instable au bruit d'échantillonnage sans gain de protection."""
    tableau = _tableau_nationalite(
        effectif_ue=40, detectes_ue=20, effectif_hors_ue=40, detectes_hors_ue=20
    )

    assert controler_clause_c4(tableau)["statut"] == "respectee"


# --- Filet de sécurité §5.2.3 -----------------------------------------------


def test_le_filet_compte_les_erreurs_graves_rattrapees():
    """Réserve n° 1 du §7.3, restée ouverte et bloquante : l'audit doit exposer
    combien d'erreurs graves échappent au filet, pas seulement combien il en
    attrape."""
    analyse = pd.DataFrame(
        {
            "erreur_grave_2_vers_0": [True, True, False, False],
            "a_valider": [True, False, True, False],
        }
    )

    resultat = filet_de_securite(analyse, cout_revue=20)

    assert resultat["erreurs_graves"] == 2
    assert resultat["erreurs_graves_rattrapees"] == 1
    assert resultat["erreurs_graves_non_rattrapees"] == 1
    assert resultat["dossiers_a_valider"] == 2
    assert resultat["cout_revue_eur"] == 40
