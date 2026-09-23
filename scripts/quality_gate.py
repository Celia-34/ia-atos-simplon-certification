"""Quality gate de la CI — le modèle servi a-t-il le droit d'être déployé ?

Question distincte des deux autres barrières du projet :

* ``promotion.py`` répond à *« ce candidat mérite-t-il de remplacer la prod ? »*
  — arbitrage entre **deux** modèles, joué dans la boucle de rétroaction ;
* ``tests/test_modele_servi.py`` répond à *« les fichiers se contredisent-ils ? »*
  — concordance documentaire, sans jamais charger de données ;
* **ce script** répond à *« l'artefact qu'on s'apprête à mettre en image tient-il
  encore ses promesses ? »* — il **rejoue** le golden run depuis le ``.joblib``
  servi et confronte le résultat aux chiffres publiés.

C'est le seul contrôle qui puisse détecter un ``reference_baseline.json``
périmé : les tests comparent ce fichier à lui-même et à des constantes, jamais
à une prédiction réelle. Un artefact remplacé sans régénérer la baseline
passerait toutes les suites et partirait en production.

Ne dépend que de fichiers **versionnés dans Git** (``emploi_retour_s1.joblib``,
``reference_set.csv``, ``reference_baseline.json``, les deux métadonnées) : la
gate est donc rejouable sur un runner vierge, sans artefact d'entraînement.

Usage::

    python scripts/quality_gate.py            # 0 = passe, 1 = bloque
    python scripts/quality_gate.py --json     # rapport machine
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import joblib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preprocess import (  # noqa: E402
    DATA,
    ROOT,
    build_pipeline,
    evaluate,
    load_prepared_csv,
)
from promotion import HIGHER_IS_BETTER, THRESHOLDS  # noqa: E402

SERVED_DIR = ROOT / "services" / "model" / "models"
SERVED_MODEL_PATH = SERVED_DIR / "emploi_retour_s1.joblib"
SERVED_META_PATH = SERVED_DIR / "emploi_retour_s1.json"
SOURCE_META_PATH = (
    ROOT / "models" / "modele_final_s1_RandomForestClassifier__n_estimators_300_.metadata.json"
)
REFERENCE_PATH = DATA / "reference_set.csv"
BASELINE_PATH = DATA / "reference_baseline.json"

# Le golden run est **déterministe** : même artefact, mêmes 350 lignes, aucun
# tirage. Un écart au-delà du bruit de sérialisation flottante signale un
# artefact et une baseline désynchronisés — pas une variation d'échantillonnage.
# La tolérance est donc trois ordres de grandeur sous celle de `promotion.py`
# (0.01), qui couvre, elle, un vrai bruit d'échantillonnage entre deux modèles.
GOLDEN_RUN_TOLERANCE = 1e-4

# Clés dont la présence dans le fichier servi signe une régression déjà vécue :
# la neutralisation serveur de `nationalite_hors_ue` (#7) et la coexistence de
# deux jeux de métriques « finales » (#14).
CLES_INTERDITES = ("feature_columns_forced", "metrics_holdout_notebook", "metrics_note")

PARAMETRES_SUIVIS = ("n_estimators", "class_weight", "random_state")

METRIQUES_PUBLIEES = (
    "accuracy",
    "f1_macro",
    "recall_classe_2",
    "f1_classe_2",
    "taux_erreur_grave_2_vers_0",
    "taux_erreur_0_vers_2",
)


@dataclass
class Rapport:
    """Accumule les verdicts pour tout rejouer avant de conclure.

    La gate ne s'arrête pas au premier échec : sur une CI, savoir *combien* de
    contrôles tombent distingue une baseline périmée (1 échec) d'un mauvais
    artefact copié (4 échecs).
    """

    controles: list[dict] = field(default_factory=list)

    def verdict(self, code: str, libelle: str, ok: bool, detail: str = "") -> None:
        self.controles.append(
            {"code": code, "libelle": libelle, "ok": bool(ok), "detail": detail}
        )

    @property
    def echecs(self) -> list[dict]:
        return [c for c in self.controles if not c["ok"]]

    @property
    def ok(self) -> bool:
        return not self.echecs


def _classifieur(pipeline):
    return pipeline.named_steps["model"] if hasattr(pipeline, "named_steps") else pipeline


def _viole_plancher(metric: str, value: float) -> bool:
    plancher = THRESHOLDS[metric]
    return value < plancher if HIGHER_IS_BETTER[metric] else value > plancher


def controler_contrat_servi(rapport: Rapport, served_meta: dict, baseline: dict) -> None:
    """G1 — le fichier servi décrit-il le contrat attendu ?"""
    presentes = [cle for cle in CLES_INTERDITES if cle in served_meta]
    rapport.verdict(
        "G1.1",
        "Aucune clé de neutralisation ni second jeu de métriques",
        not presentes,
        f"clés interdites présentes : {presentes}" if presentes else "",
    )

    version_servie = served_meta.get("model_version")
    version_baseline = baseline.get("model_version")
    rapport.verdict(
        "G1.2",
        "Version du modèle servi alignée sur le golden run",
        version_servie == version_baseline,
        f"servi={version_servie!r} vs baseline={version_baseline!r}"
        if version_servie != version_baseline
        else "",
    )

    features = list(served_meta.get("feature_columns_numeric", [])) + list(
        served_meta.get("feature_columns_categorical", [])
    )
    attendues = set(build_pipeline_features())
    rapport.verdict(
        "G1.3",
        "Contrat d'entrée conforme au scénario s1",
        set(features) == attendues,
        f"déclarées={sorted(features)} vs attendues={sorted(attendues)}"
        if set(features) != attendues
        else f"{len(features)} champs",
    )


def build_pipeline_features() -> list[str]:
    from preprocess import FEATURES

    return list(FEATURES)


def controler_configuration(rapport: Rapport, modele_servi) -> None:
    """G2 — le pipeline de réentraînement reproduit-il le modèle servi ?

    Doublon assumé avec ``tests/test_modele_servi.py`` : ce contrôle doit rester
    exécutable **sans pytest**, parce qu'il conditionne un déploiement et non
    une revue de code.
    """
    candidat = _classifieur(build_pipeline()).get_params()
    servi = _classifieur(modele_servi).get_params()
    ecarts = {
        nom: (candidat.get(nom), servi.get(nom))
        for nom in PARAMETRES_SUIVIS
        if candidat.get(nom) != servi.get(nom)
    }
    rapport.verdict(
        "G2.1",
        "build_pipeline() reproduit la configuration du modèle servi",
        not ecarts,
        f"(candidat, servi) divergents : {ecarts}" if ecarts else "",
    )


def controler_concordance(rapport: Rapport, served_meta: dict) -> None:
    """G3 — les trois sources de métriques publiées disent-elles la même chose ?"""
    if not SOURCE_META_PATH.exists():
        rapport.verdict(
            "G3.1",
            "Concordance avec la métadonnée de persistance du notebook",
            False,
            f"{SOURCE_META_PATH.name} absent",
        )
        return

    servies = served_meta.get("metrics_holdout", {})
    source = json.loads(SOURCE_META_PATH.read_text(encoding="utf-8"))["metriques_test"]
    ecarts = {
        nom: (servies.get(nom), round(float(source[nom]), 4))
        for nom in METRIQUES_PUBLIEES
        if nom in source and servies.get(nom) != round(float(source[nom]), 4)
    }
    rapport.verdict(
        "G3.1",
        "Concordance avec la métadonnée de persistance du notebook",
        not ecarts,
        f"(servi, notebook) divergents : {ecarts}" if ecarts else "",
    )


def controler_golden_run(
    rapport: Rapport, modele_servi, baseline: dict
) -> dict[str, float]:
    """G4 — l'artefact servi reproduit-il le golden run publié ?

    C'est le contrôle central : il est le seul du dépôt à confronter un
    **fichier de métriques** à une **prédiction réellement calculée**.
    """
    reference = load_prepared_csv(REFERENCE_PATH)
    mesurees = evaluate(modele_servi, reference)
    publiees = baseline["metrics"]

    ecarts = {
        nom: (round(valeur, 6), round(float(publiees[nom]), 6))
        for nom, valeur in mesurees.items()
        if nom in publiees and abs(valeur - float(publiees[nom])) > GOLDEN_RUN_TOLERANCE
    }
    rapport.verdict(
        "G4.1",
        f"Golden run rejoué sur {len(reference)} lignes de référence",
        not ecarts,
        f"(mesuré, publié) divergents au-delà de {GOLDEN_RUN_TOLERANCE} : {ecarts}"
        if ecarts
        else "",
    )

    manquantes = [nom for nom in THRESHOLDS if nom not in mesurees]
    if manquantes:
        rapport.verdict(
            "G4.2",
            "Le modèle servi franchit ses propres planchers de promotion",
            False,
            f"métriques non mesurées : {manquantes}",
        )
        return mesurees

    violations = [
        f"{nom}={mesurees[nom]:.4f} hors du plancher {THRESHOLDS[nom]:.2f}"
        for nom in THRESHOLDS
        if _viole_plancher(nom, mesurees[nom])
    ]
    rapport.verdict(
        "G4.2",
        "Le modèle servi franchit ses propres planchers de promotion",
        not violations,
        " ; ".join(violations),
    )
    return mesurees


def rendre_markdown(rapport: Rapport, mesurees: dict[str, float]) -> str:
    lignes = ["## Quality gate — modèle servi", ""]
    lignes.append("| | Contrôle | Détail |")
    lignes.append("|---|---|---|")
    for controle in rapport.controles:
        icone = "✅" if controle["ok"] else "❌"
        detail = controle["detail"] or "—"
        lignes.append(f"| {icone} | `{controle['code']}` {controle['libelle']} | {detail} |")

    if mesurees:
        lignes += ["", "### Golden run mesuré vs planchers", ""]
        lignes.append("| Métrique | Mesurée | Plancher | Cible §1.4 |")
        lignes.append("|---|---|---|---|")
        from promotion import CIBLES_METIER

        for nom, plancher in THRESHOLDS.items():
            valeur = mesurees.get(nom)
            affiche = f"{valeur:.4f}" if valeur is not None else "—"
            lignes.append(
                f"| `{nom}` | {affiche} | {plancher:.2f} | {CIBLES_METIER[nom]:.2f} |"
            )

    lignes += ["", "**Verdict : " + ("PASSE" if rapport.ok else "BLOQUE") + "**"]
    return "\n".join(lignes) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="rapport machine sur stdout")
    args = parser.parse_args()

    for chemin in (SERVED_MODEL_PATH, SERVED_META_PATH, REFERENCE_PATH, BASELINE_PATH):
        if not chemin.exists():
            print(f"Quality gate impossible : {chemin} est absent.", file=sys.stderr)
            return 1

    served_meta = json.loads(SERVED_META_PATH.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    modele_servi = joblib.load(SERVED_MODEL_PATH)

    rapport = Rapport()
    controler_contrat_servi(rapport, served_meta, baseline)
    controler_configuration(rapport, modele_servi)
    controler_concordance(rapport, served_meta)
    mesurees = controler_golden_run(rapport, modele_servi, baseline)

    markdown = rendre_markdown(rapport, mesurees)

    # Restitution dans le résumé de job GitHub : un échec de gate doit être
    # lisible sans dérouler les logs.
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as flux:
            flux.write(markdown)

    if args.json:
        print(
            json.dumps(
                {
                    "ok": rapport.ok,
                    "model_version": served_meta.get("model_version"),
                    "controles": rapport.controles,
                    "golden_run": mesurees,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(markdown)

    if not rapport.ok:
        print(
            f"Quality gate BLOQUE : {len(rapport.echecs)} contrôle(s) en échec.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
