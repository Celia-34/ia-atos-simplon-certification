"""Garde-fous sur le modèle servi : configuration et métriques.

Ces tests ne valident pas une performance, ils valident une **concordance**.
Ils existent parce que deux régressions silencieuses se sont déjà produites :

* A1.3 / #13 — ``class_weight="balanced"`` avait disparu de ``build_pipeline``,
  parce que le descripteur textuel du notebook (``"n_estimators=300"``) n'en
  faisait pas mention. Le retrain produisait alors des candidats d'une
  configuration différente du modèle servi : la boucle de promotion comparait
  deux réglages et non deux jeux de données.
* A5.2 / #14 — deux jeux de métriques « finales » ont coexisté, l'un mesurant
  le modèle du notebook, l'autre le modèle servi après neutralisation de
  ``nationalite_hors_ue``. Il n'existe plus qu'**une seule source de vérité**,
  et trois fichiers doivent la porter à l'identique.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import joblib
import pytest

ROOT = Path(__file__).resolve().parent.parent
SERVED_MODEL_PATH = ROOT / "services" / "model" / "models" / "emploi_retour_s1.joblib"
SERVED_META_PATH = SERVED_MODEL_PATH.with_suffix(".json")
SOURCE_META_PATH = (
    ROOT / "models" / "modele_final_s1_RandomForestClassifier__n_estimators_300_.metadata.json"
)
EVALUATION_FINALE_PATH = ROOT / "evaluation_finale.md"

# Paramètres qui définissent la configuration du classifieur retenu en §6.1.
# `class_weight` est le paramètre historiquement perdu (#13).
PARAMETRES_SUIVIS = ("n_estimators", "class_weight", "random_state")


def _classifieur(pipeline):
    return pipeline.named_steps["model"]


@pytest.fixture(scope="module")
def modele_servi():
    if not SERVED_MODEL_PATH.exists():
        pytest.skip(f"{SERVED_MODEL_PATH} absent : lancez scripts/export_model_prod.py")
    return joblib.load(SERVED_MODEL_PATH)


def test_le_pipeline_de_retrain_a_la_configuration_du_modele_servi(modele_servi):
    """A1.3 — garde-fou permanent contre la réapparition de #13.

    Le candidat du retrain doit différer du modèle de production **par les
    données uniquement**. Toute divergence d'hyperparamètre fausse
    silencieusement la décision de promotion.
    """
    from preprocess import build_pipeline

    candidat = _classifieur(build_pipeline()).get_params()
    servi = _classifieur(modele_servi).get_params()

    ecarts = {
        nom: (candidat.get(nom), servi.get(nom))
        for nom in PARAMETRES_SUIVIS
        if candidat.get(nom) != servi.get(nom)
    }
    assert not ecarts, (
        "build_pipeline() ne reproduit pas la configuration du modèle servi "
        f"(candidat, servi) : {ecarts}"
    )


def test_le_modele_servi_est_bien_un_random_forest_pondere(modele_servi):
    """Le descripteur `algorithm` des métadonnées doit dire vrai (#13)."""
    metadata = json.loads(SERVED_META_PATH.read_text(encoding="utf-8"))
    params = _classifieur(modele_servi).get_params()

    assert type(_classifieur(modele_servi)).__name__ in metadata["algorithm"]
    for nom in PARAMETRES_SUIVIS:
        assert repr(params[nom]) in metadata["algorithm"], (
            f"{nom}={params[nom]!r} absent du descripteur "
            f"« {metadata['algorithm']} »"
        )


# --- A5.2 / #14 : une seule source de vérité, trois fichiers concordants -----

# Correspondance entre les clés de `metrics_holdout` (fichier servi) et celles
# de `metriques_test` (métadonnée de persistance du notebook).
METRIQUES = (
    "accuracy",
    "f1_macro",
    "recall_classe_2",
    "f1_classe_2",
    "taux_erreur_grave_2_vers_0",
    "taux_erreur_0_vers_2",
)


def _metriques_servies() -> dict:
    return json.loads(SERVED_META_PATH.read_text(encoding="utf-8"))["metrics_holdout"]


def test_les_metriques_servies_concordent_avec_la_metadonnee_du_notebook():
    """A5.2 — le fichier servi et la métadonnée de persistance du modèle final
    doivent porter les mêmes six chiffres.

    C'est ce test qui garantit durablement qu'aucune phase future ne pourra
    réintroduire deux jeux de chiffres concurrents sur « le modèle final ».
    """
    servies = _metriques_servies()
    source = json.loads(SOURCE_META_PATH.read_text(encoding="utf-8"))["metriques_test"]

    ecarts = {
        nom: (servies[nom], round(float(source[nom]), 4))
        for nom in METRIQUES
        if servies[nom] != round(float(source[nom]), 4)
    }
    assert not ecarts, f"(servi, notebook) divergents : {ecarts}"


def test_le_fichier_servi_ne_porte_qu_un_seul_jeu_de_metriques():
    """#14 — la coexistence de `metrics_holdout` et `metrics_holdout_notebook`
    était la racine du problème : deux définitions concurrentes de « ce que
    mesure le modèle final »."""
    metadata = json.loads(SERVED_META_PATH.read_text(encoding="utf-8"))

    cles_de_metriques = [c for c in metadata if c.startswith("metrics")]
    assert cles_de_metriques == ["metrics_holdout"], cles_de_metriques


def test_les_metriques_servies_concordent_avec_evaluation_finale_md():
    """Troisième fichier de la concordance : le livrable lu par l'humain.

    `evaluation_finale.md` est généré par le notebook et n'est pas modifiable
    ici ; ce test ne le corrige pas, il **détecte** sa divergence. Un échec
    signifie que le notebook doit être rejoué, pas que la prod doit s'ajuster.

    Le markdown arrondit (0.69 pour 0.6899, 10.0 % pour 0.1) : la comparaison
    se fait donc à la précision affichée, pas au chiffre exact.
    """
    ligne = next(
        l
        for l in EVALUATION_FINALE_PATH.read_text(encoding="utf-8").splitlines()
        if "évaluation finale test set" in l
    )
    # | Modèle | accuracy | f1_macro | recall_2 | f1_2 | erreur 2→0 | erreur 0→2 |
    cellules = [c.strip() for c in ligne.strip("|").split("|")][1:]
    nombres = [float(re.search(r"[\d.]+", c).group()) for c in cellules]
    affichees = dict(
        zip(
            ("accuracy", "f1_macro", "recall_classe_2", "f1_classe_2"),
            nombres[:4],
        )
    )
    # Les deux dernières colonnes sont en pourcentage.
    affichees["taux_erreur_grave_2_vers_0"] = nombres[4] / 100
    affichees["taux_erreur_0_vers_2"] = nombres[5] / 100

    servies = _metriques_servies()
    for nom, affichee in affichees.items():
        decimales = len(str(affichee).split(".")[1])
        arrondie = round(servies[nom], decimales)
        assert arrondie == pytest.approx(affichee, abs=1e-9), (
            f"{nom} : evaluation_finale.md affiche {affichee}, "
            f"le modèle servi porte {servies[nom]} (arrondi {arrondie})"
        )
