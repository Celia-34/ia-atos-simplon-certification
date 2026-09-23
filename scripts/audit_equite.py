"""Rejoue l'audit d'équité §7.2 sur le flux de production annoté — brique E.

Le notebook conditionne le déploiement à la **reconfirmation** de l'audit
d'équité sur volume de production (§5.7, §6.3, §7.2, §7.4). Tant que ce rejeu
n'était pas outillé, la condition était invérifiable : c'est le point #3 du
relevé d'incohérences, et le plus structurant.

L'audit croise le recall de la classe 2 par sous-groupe. Il exige donc, pour
chaque dossier, **features d'entrée + prédiction servie + vérité terrain**. Les
trois briques existent déjà :

- ``data/prod_scored.csv`` porte les features, la prédiction et le ``request_id`` ;
- ``POST /feedback`` (service ``feedback``) rattache la vérité terrain au ``request_id`` ;
- ``feedback_store.load_labeled_feedback`` réalise la jointure.

Ce script n'invente donc aucune mesure : il rejoue les **mêmes fonctions** que
la cellule 148 du notebook — ``recall_classe_2_par_groupe`` et les règles de
validation manuelle §5.2.3 (``src.metrics.appliquer_regles_validation_manuelle``,
seuils lus dans les métadonnées du modèle servi) — sur le flux annoté plutôt
que sur le test set.

Deux garanties y sont attachées, qui viennent des conditions de l'arbitrage `J0` :

* **C3** — tout sous-groupe dont l'effectif de classe 2 est sous le seuil de
  fiabilité de 30 (§3.6) est marqué comme tel. Sans ce marquage on reproduirait
  le défaut que le notebook dénonce lui-même : conclure sur des effectifs trop
  faibles.
* **C4** — clause de retrait automatique : si le recall classe 2 des usagers
  hors UE devient **inférieur** à celui des usagers UE, la variable
  ``nationalite_hors_ue`` est retirée sans nouvel arbitrage. Le contrôle est
  implémenté ici et sort en code retour 2.

L'audit est délibérément **hors ligne** (condition C2) : la nationalité ne doit
apparaître ni dans les métriques Prometheus, ni dans les dashboards, ni dans les
logs applicatifs. Elle n'est lue que sur le périmètre restreint et tracé du jeu
annoté.

Usage::

    python scripts/audit_equite.py
    python scripts/audit_equite.py --json rapports/audit_equite.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feedback_store import load_labeled_feedback  # noqa: E402
from preprocess import DATA, ROOT, build_features  # noqa: E402
from src import metrics as metrics_module  # noqa: E402

PROD_SCORED_PATH = DATA / "prod_scored.csv"
FEEDBACK_DB = DATA / "feedbacks.db"
MODELS = ROOT / "services" / "model" / "models"
PRODUCTION_PATH = MODELS / "emploi_retour_s1.joblib"
PRODUCTION_META_PATH = MODELS / "emploi_retour_s1.json"

# Seuil de fiabilité §3.6 : en dessous, un écart de recall n'est pas un signal.
SEUIL_EFFECTIF_FIABLE = 30

# Tranches d'âge du §3.6 (cellule 70), reprises à l'identique : un découpage
# différent produirait des écarts non comparables à ceux du notebook.
AGE_BINS = [0, 20, 30, 40, 50, 60, 100]
AGE_LABELS = ["0-20", "21-30", "31-40", "41-50", "51-60", "61+"]

CLASSE_A_RISQUE = 2
CLASSE_RETOUR_RAPIDE = 0

# Axes d'audit du §7.2. `departement` est traité à part (top 10 par effectif).
AXES = [
    ("nationalite_hors_ue", "nationalité hors UE (feature du modèle, variable sensible)"),
    ("niveau_diplome", "niveau de diplôme (feature du modèle, proxy §1.5)"),
    ("tranche_age", "tranche d'âge (dérivée de age, feature du modèle, proxy §1.5)"),
    ("famille_thematique", "famille thématique de la synthèse d'entretien (§4.2.2)"),
]
N_DEPARTEMENTS = 10


def recall_classe_2_par_groupe(df: pd.DataFrame, colonne: str) -> pd.DataFrame:
    """Recall de la classe 2 par modalité — fonction du §7.2, à l'identique.

    ``effectif_classe_2`` est renvoyé à côté du recall parce qu'un recall n'a
    pas de sens sans son dénominateur : c'est lui qui porte le jugement de
    fiabilité, pas la valeur du ratio.
    """
    est_classe_2 = df["classe_reelle"] == CLASSE_A_RISQUE
    detectes = est_classe_2 & (df["classe_predite"] == CLASSE_A_RISQUE)
    tableau = pd.DataFrame(
        {
            "effectif_classe_2": est_classe_2.groupby(df[colonne], observed=True).sum(),
            "detectes": detectes.groupby(df[colonne], observed=True).sum(),
        }
    )
    tableau["recall_classe_2"] = (
        tableau["detectes"] / tableau["effectif_classe_2"]
    ).round(3)
    # Condition C3 : le marquage n'est pas décoratif, c'est lui qui interdit de
    # tirer une conclusion d'équité d'un sous-groupe trop petit.
    tableau["fiabilite"] = tableau["effectif_classe_2"].apply(
        lambda n: "fiable" if n >= SEUIL_EFFECTIF_FIABLE else "effectif insuffisant"
    )
    return tableau


def charger_flux_annote(feedback_db: Path, prod_scored: Path) -> pd.DataFrame:
    """Jointure feedbacks ⋈ prod_scored, sur **tous** les dossiers annotés.

    ``only_new=False`` : l'audit porte sur l'historique complet, y compris les
    feedbacks déjà consommés par un réentraînement. Se limiter aux nouveaux
    réduirait l'effectif sans raison et rendrait la condition C3 encore plus
    difficile à satisfaire.
    """
    if not feedback_db.exists():
        raise SystemExit(
            f"{feedback_db} est absente : aucun feedback à auditer.\n"
            "Démarrez la stack et alimentez POST /feedback (ou GET /mock-feedback)."
        )
    if not prod_scored.exists():
        raise SystemExit(
            f"{prod_scored} est absent : lancez d'abord scripts/build_prod_scored.py."
        )

    flux = load_labeled_feedback(feedback_db, prod_scored, only_new=False)
    if flux.empty:
        raise SystemExit(
            "Aucun dossier annoté : l'audit d'équité est sans objet tant que la "
            "vérité terrain n'a pas été remontée par les conseillers."
        )
    return flux


def construire_analyse(flux: pd.DataFrame, seuil_a: float, seuil_b: float) -> pd.DataFrame:
    """Reconstitue le tableau ``analyse_erreurs`` du §7.2 sur le flux annoté.

    La prédiction retenue est celle **réellement servie** (colonne ``prediction``
    de ``prod_scored``), pas une reprédiction : auditer autre chose que ce que
    l'usager a reçu n'aurait aucune valeur probante. Les probabilités, elles,
    doivent être recalculées — le journal ne conserve que celle de la classe
    prédite, alors que les règles §5.2.3 portent sur P(classe 2).
    """
    modele = joblib.load(PRODUCTION_PATH)
    features = build_features(flux)
    probabilites = modele.predict_proba(features)
    index_classe_2 = list(modele.classes_).index(CLASSE_A_RISQUE)

    analyse = features.copy()
    analyse["classe_reelle"] = flux["true_label"].astype(int).to_numpy()
    analyse["classe_predite"] = flux["prediction"].astype(int).to_numpy()
    analyse["proba_classe_2"] = probabilites[:, index_classe_2]
    analyse["confiance_max"] = probabilites.max(axis=1)
    analyse["erreur_grave_2_vers_0"] = (analyse["classe_reelle"] == CLASSE_A_RISQUE) & (
        analyse["classe_predite"] == CLASSE_RETOUR_RAPIDE
    )
    # Règles §5.2.3, appliquées par la fonction du notebook — pas une réécriture.
    analyse["a_valider"] = metrics_module.appliquer_regles_validation_manuelle(
        analyse["classe_predite"].to_numpy(), probabilites, seuil_a, seuil_b
    )
    analyse["tranche_age"] = pd.cut(
        analyse["age"], bins=AGE_BINS, labels=AGE_LABELS, right=False
    )
    return analyse


def controler_clause_c4(tableau_nationalite: pd.DataFrame) -> dict:
    """Condition C4 — clause de retrait automatique de ``nationalite_hors_ue``.

    L'arbitrage `J0` repose entièrement sur un constat empirique : la variable
    **améliore** la détection des usagers hors UE (recall 0.800 contre 0.529,
    §7.2). Si ce constat s'inverse, la justification tombe et la variable doit
    être retirée sans nouvel arbitrage.

    Trois issues, et la troisième est la plus importante : un effectif
    insuffisant ne permet ni de déclencher la clause, ni de la déclarer
    respectée. La déclarer respectée par défaut reviendrait à transformer un
    manque de données en satisfecit.
    """
    resultat = {"statut": "indeterminee", "recall_ue": None, "recall_hors_ue": None}
    if not {0, 1} <= set(tableau_nationalite.index):
        resultat["motif"] = "une des deux modalités est absente du flux annoté"
        return resultat

    ue = tableau_nationalite.loc[0]
    hors_ue = tableau_nationalite.loc[1]
    resultat["recall_ue"] = float(ue["recall_classe_2"])
    resultat["recall_hors_ue"] = float(hors_ue["recall_classe_2"])
    resultat["effectif_classe_2_ue"] = int(ue["effectif_classe_2"])
    resultat["effectif_classe_2_hors_ue"] = int(hors_ue["effectif_classe_2"])

    insuffisants = [
        libelle
        for libelle, ligne in (("UE", ue), ("hors UE", hors_ue))
        if ligne["effectif_classe_2"] < SEUIL_EFFECTIF_FIABLE
    ]
    if insuffisants:
        resultat["motif"] = (
            "effectif de classe 2 sous le seuil de fiabilité de "
            f"{SEUIL_EFFECTIF_FIABLE} pour : {', '.join(insuffisants)}"
        )
        return resultat

    if resultat["recall_hors_ue"] < resultat["recall_ue"]:
        resultat["statut"] = "declenchee"
        resultat["motif"] = (
            f"recall classe 2 hors UE ({resultat['recall_hors_ue']:.3f}) inférieur "
            f"au recall UE ({resultat['recall_ue']:.3f}) : retrait de "
            "nationalite_hors_ue requis sans nouvel arbitrage"
        )
    else:
        resultat["statut"] = "respectee"
        resultat["motif"] = (
            f"recall classe 2 hors UE ({resultat['recall_hors_ue']:.3f}) toujours "
            f"supérieur ou égal au recall UE ({resultat['recall_ue']:.3f})"
        )
    return resultat


def filet_de_securite(analyse: pd.DataFrame, cout_revue: float) -> dict:
    """Efficacité du filet §5.2.3 — réserve n° 1 du §7.3, restée ouverte."""
    erreurs_graves = analyse["erreur_grave_2_vers_0"]
    rattrapees = erreurs_graves & analyse["a_valider"]
    return {
        "dossiers_a_valider": int(analyse["a_valider"].sum()),
        "part_a_valider": round(float(analyse["a_valider"].mean()), 4),
        "cout_revue_eur": round(float(analyse["a_valider"].sum() * cout_revue), 2),
        "erreurs_graves": int(erreurs_graves.sum()),
        "erreurs_graves_rattrapees": int(rattrapees.sum()),
        "erreurs_graves_non_rattrapees": int((erreurs_graves & ~analyse["a_valider"]).sum()),
    }


def _afficher(titre: str, tableau: pd.DataFrame) -> None:
    print(f"\n{titre}")
    print(tableau.to_string())
    petits = tableau[tableau["fiabilite"] != "fiable"]
    if not petits.empty:
        print(
            f"  ⚠️  {len(petits)} modalité(s) sous le seuil de fiabilité de "
            f"{SEUIL_EFFECTIF_FIABLE} : écarts non interprétables."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--feedback-db", type=Path, default=FEEDBACK_DB)
    parser.add_argument("--prod-scored", type=Path, default=PROD_SCORED_PATH)
    parser.add_argument(
        "--json", type=Path, default=None, help="Écrit le rapport complet en JSON."
    )
    args = parser.parse_args(argv)

    metadata = json.loads(PRODUCTION_META_PATH.read_text(encoding="utf-8"))
    regles = metadata["regles_validation_manuelle"]

    flux = charger_flux_annote(args.feedback_db, args.prod_scored)
    analyse = construire_analyse(flux, regles["seuil_a"], regles["seuil_b"])

    n_classe_2 = int((analyse["classe_reelle"] == CLASSE_A_RISQUE).sum())
    print(
        f"Audit d'équité §7.2 — modèle {metadata['model_version']} — "
        f"{len(analyse)} dossiers annotés, dont {n_classe_2} de classe 2."
    )
    if n_classe_2 < SEUIL_EFFECTIF_FIABLE:
        print(
            f"⚠️  L'effectif TOTAL de classe 2 ({n_classe_2}) est déjà sous le seuil "
            f"de fiabilité de {SEUIL_EFFECTIF_FIABLE} : aucun sous-groupe ne pourra "
            "être conclusif. Poursuivre la collecte de feedbacks."
        )

    tableaux: dict[str, pd.DataFrame] = {}
    for colonne, libelle in AXES:
        tableau = recall_classe_2_par_groupe(analyse, colonne)
        tableaux[colonne] = tableau
        _afficher(f"Recall classe 2 selon {libelle} :", tableau)

    tops = analyse["departement"].value_counts().head(N_DEPARTEMENTS).index
    tableau_dep = recall_classe_2_par_groupe(
        analyse[analyse["departement"].isin(tops)], "departement"
    ).sort_values("effectif_classe_2", ascending=False)
    tableaux["departement"] = tableau_dep
    _afficher(
        f"Recall classe 2 selon departement (top {N_DEPARTEMENTS} par effectif) :",
        tableau_dep,
    )

    filet = filet_de_securite(analyse, regles["cout_revue_manuelle_eur"])
    print(
        f"\nFilet de sécurité §5.2.3 (seuils A={regles['seuil_a']}, B={regles['seuil_b']}) :"
        f"\n  {filet['dossiers_a_valider']} dossiers signalés pour revue "
        f"({filet['part_a_valider']:.1%}), coût {filet['cout_revue_eur']:.0f} €"
        f"\n  erreurs graves 2→0 : {filet['erreurs_graves']} au total, "
        f"{filet['erreurs_graves_rattrapees']} rattrapées, "
        f"{filet['erreurs_graves_non_rattrapees']} non rattrapées"
    )

    c4 = controler_clause_c4(tableaux["nationalite_hors_ue"])
    print(f"\nCondition C4 — clause de retrait automatique : {c4['statut'].upper()}")
    print(f"  {c4.get('motif', '')}")

    rapport = {
        "model_version": metadata["model_version"],
        "n_dossiers_annotes": len(analyse),
        "n_classe_2": n_classe_2,
        "seuil_effectif_fiable": SEUIL_EFFECTIF_FIABLE,
        "recall_classe_2_par_groupe": {
            nom: tableau.reset_index().to_dict(orient="records")
            for nom, tableau in tableaux.items()
        },
        "filet_de_securite": filet,
        "condition_c4": c4,
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(rapport, indent=2, ensure_ascii=False, default=str) + "\n",
            encoding="utf-8",
        )
        print(f"\nRapport → {args.json}")

    # Code retour 2 : la clause C4 est déclenchée, le retrait de la variable est
    # dû. Un cron ou une CI doit pouvoir s'en apercevoir sans lire la sortie.
    return 2 if c4["statut"] == "declenchee" else 0


if __name__ == "__main__":
    sys.exit(main())
