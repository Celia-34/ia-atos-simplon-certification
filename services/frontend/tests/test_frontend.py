"""Tests statiques du formulaire frontend (services/frontend/html/index.html).

pytest n'exécute pas le JavaScript : on vérifie les CONTRATS du formulaire,
pas son comportement dynamique.
  - les 8 champs correspondent au schéma Pydantic UsagerFeatures ;
  - les <select> catégoriels n'exposent que des modalités connues du modèle ;
  - la mention d'information de la condition C7 est présente (donnée sensible) ;
  - l'appel API reste en chemin relatif (proxy nginx, pas de CORS).
"""
from __future__ import annotations

import importlib.util
import sys
import typing
from html.parser import HTMLParser
from pathlib import Path

import joblib
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
INDEX_HTML = REPO_ROOT / "services" / "frontend" / "html" / "index.html"
MODEL_PATH = REPO_ROOT / "services" / "model" / "models" / "emploi_retour_s1.joblib"
SCHEMAS_PY = REPO_ROOT / "services" / "backend" / "app" / "schemas.py"

NUMERIC_FIELDS = {"age", "anciennete_poste_ans"}
# est_allocataire et nationalite_hors_ue sont des <select> numériques (0/1),
# pas des saisies libres.
NUMERIC_SELECT_FIELDS = {"est_allocataire", "nationalite_hors_ue"}


class FormParser(HTMLParser):
    """Collecte les champs nommés et les options de chaque <select>."""

    def __init__(self) -> None:
        super().__init__()
        self.fields: dict[str, dict] = {}   # name -> attributs
        self.options: dict[str, set] = {}   # name du select -> valeurs
        self.sentinels: set[str] = set()    # selects avec placeholder vide
        self._current: str | None = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("input", "select") and d.get("name"):
            self.fields[d["name"]] = d
            if tag == "select":
                self._current = d["name"]
                self.options[d["name"]] = set()
        elif tag == "option" and self._current:
            if d.get("value"):
                self.options[self._current].add(d["value"])
            elif "disabled" in d and "selected" in d:
                self.sentinels.add(self._current)

    def handle_endtag(self, tag):
        if tag == "select":
            self._current = None


@pytest.fixture(scope="module")
def html_text() -> str:
    return INDEX_HTML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def form(html_text) -> FormParser:
    p = FormParser()
    p.feed(html_text)
    return p


@pytest.fixture(scope="module")
def schema():
    """UsagerFeatures chargé par chemin, sans polluer le package `app`."""
    spec = importlib.util.spec_from_file_location("backend_schemas", SCHEMAS_PY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["backend_schemas"] = mod
    spec.loader.exec_module(mod)
    return mod.UsagerFeatures


@pytest.fixture(scope="module")
def encoder_categories() -> dict[str, set]:
    """Modalités réellement apprises par les encodeurs du pipeline.

    Le préprocesseur en contient deux (OrdinalEncoder pour `niveau_diplome`,
    OneHotEncoder pour le reste) : on les agrège tous, sinon le premier trouvé
    masquerait les modalités de l'autre et le test ne vérifierait qu'un champ.
    """
    pre = joblib.load(MODEL_PATH).named_steps["preprocessing"]
    categories: dict[str, set] = {}
    for _, trans, cols in pre.transformers_:
        inner = trans.named_steps.values() if hasattr(trans, "named_steps") else [trans]
        for step in inner:
            if hasattr(step, "categories_"):
                categories.update({c: set(cat) for c, cat in zip(cols, step.categories_)})
    if not categories:
        pytest.fail("Aucun encodeur catégoriel trouvé dans le pipeline")
    return categories


# --- Contrat formulaire <-> schéma Pydantic ---------------------------------

def test_les_champs_du_schema_sont_presents(form, schema):
    assert set(form.fields) == set(schema.model_fields)


def test_la_nationalite_est_collectee_par_le_formulaire(form):
    """Condition C7 de l'arbitrage `J0` : la variable est collectée auprès du
    conseiller, plus injectée côté serveur. Sa présence au formulaire est ce qui
    rend la collecte visible — donc contestable — par la personne concernée."""
    assert "nationalite_hors_ue" in form.fields
    assert form.options["nationalite_hors_ue"] == {"0", "1"}


def test_la_donnee_sensible_porte_sa_mention_d_information(html_text):
    """Condition C7 (art. 13-14 RGPD) : la finalité et ses limites doivent être
    affichées, pas seulement documentées ailleurs.

    Le test porte sur des marqueurs de fond, pas sur une formulation exacte :
    reformuler la mention reste possible, la supprimer ne l'est pas.
    """
    assert 'class="sensible"' in html_text, "la donnée sensible doit être isolée"
    for marqueur in ("accompagnement renforcé", "6.1.e", "sanction", "rectification"):
        assert marqueur in html_text, f"mention d'information incomplète : {marqueur!r}"


def test_les_champs_numeriques_libres_portent_le_marqueur_de_conversion(form):
    """Sans data-type="number", FormData enverrait des chaînes -> 422."""
    for name in NUMERIC_FIELDS | NUMERIC_SELECT_FIELDS:
        assert form.fields[name].get("data-type") == "number", name


def test_les_bornes_ne_sont_pas_dupliquees_en_html(form):
    """Choix d'architecture : la validation des bornes est SERVEUR uniquement.

    Pas de min/max sur les <input> : une borne recopiée en HTML est une
    duplication de la règle métier définie dans UsagerFeatures, qui dérive
    dès que le schéma change. Le navigateur laisse passer, Pydantic tranche,
    et le bloc 422 du script affiche le champ fautif.
    """
    for name in NUMERIC_FIELDS:
        attrs = form.fields[name]
        assert "min" not in attrs and "max" not in attrs, name


# --- Contrat formulaire <-> modèle ------------------------------------------

def test_les_options_correspondent_aux_modalites_du_modele(form, encoder_categories):
    """L'encodeur est en handle_unknown='ignore' : une modalité inconnue ne
    lève pas d'erreur, elle produit un vecteur nul et une prédiction fausse.
    Le formulaire est le seul garde-fou."""
    for field, expected in encoder_categories.items():
        if field in NUMERIC_SELECT_FIELDS:
            # est_allocataire est appris comme des floats ("0.0"/"1.0") mais
            # soumis par le formulaire comme des entiers ("0"/"1") — même
            # valeur métier, l'API/le modèle acceptent int (cf. UsagerFeatures).
            expected_as_int = {str(int(float(v))) for v in expected}
            assert form.options[field] == expected_as_int, field
        else:
            assert form.options[field] == expected, field


def test_les_options_sont_acceptees_par_le_schema(form, schema):
    """Inclusion, pas égalité : niveau_diplome est un Literal fermé."""
    hints = typing.get_type_hints(schema)
    for field, values in form.options.items():
        if field in NUMERIC_SELECT_FIELDS:
            continue
        allowed = typing.get_args(hints[field])
        if allowed:  # les champs typés `str` libre n'ont rien à vérifier ici
            assert values <= set(allowed), field


def test_chaque_select_a_une_option_placeholder(form):
    """`required` sur un <select> n'agit que si l'option retenue a value="".
    Sans placeholder, la première option est choisie automatiquement."""
    assert form.sentinels == set(form.options)


# --- Contrat formulaire <-> réseau ------------------------------------------

def test_l_appel_api_reste_en_chemin_relatif(html_text):
    """nginx proxifie /api/ vers le backend : même origine, pas de CORS.
    Une URL absolue casserait dès que les ports changent."""
    assert "'/api/score'" in html_text or '"/api/score"' in html_text
    assert "http://localhost:8001" not in html_text
    assert "http://backend:8001" not in html_text


def test_aucun_todo_residuel(html_text):
    assert "TODO" not in html_text
