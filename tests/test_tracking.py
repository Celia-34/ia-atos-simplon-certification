"""Tests du tracking MLflow — l'essentiel est qu'il ne casse **rien**.

Un module de tracking est un ajout de confort : la propriété la plus
importante n'est pas qu'il trace bien, c'est qu'il se taise et laisse passer
quand le serveur est absent, injoignable ou cassé. Ces tests vérifient donc
d'abord la dégradation, ensuite la répartition params/metrics.
"""

from __future__ import annotations

import logging

import pytest

from src import tracking


@pytest.fixture(autouse=True)
def _reinitialiser_avertissement():
    """L'avertissement est volontairement émis une seule fois par processus."""
    tracking._avertissement_emis = False
    yield
    tracking._avertissement_emis = False


# --- Dégradation (la propriété critique) -------------------------------------


def test_sans_uri_le_tracking_est_un_no_op(monkeypatch):
    monkeypatch.delenv(tracking.VARIABLE_URI, raising=False)
    assert tracking.log_run("run", {"scenario": "s1"}) is None


def test_sans_uri_le_contexte_cede_none(monkeypatch):
    monkeypatch.delenv(tracking.VARIABLE_URI, raising=False)
    with tracking.run("run") as actif:
        assert actif is None


def test_un_serveur_injoignable_ne_leve_pas(monkeypatch, caplog):
    """LE test qui justifie le module.

    Sans cette garantie, une panne du serveur de métadonnées ferait perdre un
    entraînement déjà payé en temps de calcul.
    """
    monkeypatch.setenv(tracking.VARIABLE_URI, "http://127.0.0.1:1/")

    class MlflowCasse:
        def set_experiment(self, *_args, **_kwargs):
            raise ConnectionError("serveur injoignable")

    monkeypatch.setattr(tracking, "_mlflow", lambda: MlflowCasse())

    with caplog.at_level(logging.WARNING):
        assert tracking.log_run("run", {"scenario": "s1"}) is None
    assert any("désactivé" in message for message in caplog.messages)


def test_l_avertissement_n_est_emis_qu_une_fois(monkeypatch, caplog):
    """Un benchmark produit des dizaines de runs : sans ce garde, l'absence de
    serveur noierait la sortie du notebook."""
    monkeypatch.delenv(tracking.VARIABLE_URI, raising=False)
    with caplog.at_level(logging.WARNING):
        for _ in range(5):
            tracking.log_run("run", {})
    assert len(caplog.messages) == 1


def test_un_mlflow_non_installe_degrade(monkeypatch):
    monkeypatch.setenv(tracking.VARIABLE_URI, "file:./mlruns")
    monkeypatch.setitem(__import__("sys").modules, "mlflow", None)
    # `import mlflow` sur une entrée None lève ImportError : c'est exactement
    # le cas « paquet absent » que le module doit absorber.
    assert tracking._mlflow() is None


# --- Répartition params / metrics --------------------------------------------


def test_les_blocs_de_metriques_partent_en_metrics():
    """Ranger une métrique en `param` la rend invisible aux comparaisons
    MLflow — c'est le défaut que cette séparation existe pour éviter."""
    params, metriques = tracking.separer_params_et_metriques(
        {
            "scenario": "s1",
            "metriques_test": {"accuracy": 0.714, "f1_macro": 0.6899},
        }
    )
    assert metriques == {"accuracy": 0.714, "f1_macro": 0.6899}
    assert params["scenario"] == "s1"
    assert "metriques_test" not in params


def test_les_metadonnees_imbriquees_sont_aplaties():
    params, _ = tracking.separer_params_et_metriques(
        {"dataset": {"version": "2026-08-14_initiale", "n_train": 2000}}
    )
    assert params["dataset.version"] == "2026-08-14_initiale"
    assert params["dataset.n_train"] == 2000


def test_les_listes_sont_rendues_lisibles():
    params, _ = tracking.separer_params_et_metriques(
        {"features_entree": ["age", "departement"]}
    )
    assert params["features_entree"] == "age, departement"


def test_la_matrice_de_confusion_n_encombre_pas_les_params():
    params, _ = tracking.separer_params_et_metriques(
        {"matrice_confusion_test": [[142, 36, 9], [27, 162, 34]]}
    )
    assert "matrice_confusion_test" not in params


def test_une_metrique_non_numerique_est_ignoree_sans_lever():
    _, metriques = tracking.separer_params_et_metriques(
        {"metrics_holdout": {"accuracy": 0.71, "commentaire": "n/a"}}
    )
    assert metriques == {"accuracy": 0.71}


def test_les_metriques_de_production_sont_prefixees(monkeypatch):
    """Candidat et production cohabitent dans un même run : c'est la
    comparaison qui est l'objet du run, pas chaque modèle pris isolément."""
    captures: dict = {}

    def faux_log_run(nom, metadata, **_kwargs):
        captures["nom"] = nom
        captures["metadata"] = metadata
        return "run-id"

    monkeypatch.setattr(tracking, "log_run", faux_log_run)

    tracking.log_decision_promotion(
        candidate_metrics={"accuracy": 0.72},
        production_metrics={"accuracy": 0.70},
        promote=False,
        reason="Gain insuffisant",
        feedback_count=120,
    )

    metriques = captures["metadata"]["metrics_reference"]
    assert metriques["accuracy"] == 0.72
    assert metriques["prod_accuracy"] == 0.70
    assert "rejetee" in captures["nom"]


def test_un_rejet_de_promotion_est_trace_comme_une_acceptation(monkeypatch):
    """Ne tracer que les promotions reviendrait à ne garder que les runs qui
    arrangent — or un rejet est l'issue la plus instructive de la boucle."""
    noms: list[str] = []
    monkeypatch.setattr(
        tracking, "log_run", lambda nom, metadata, **_k: noms.append(nom) or "id"
    )

    for promote in (True, False):
        tracking.log_decision_promotion({}, {}, promote, "motif", 100)

    assert noms == ["promotion-acceptee", "promotion-rejetee"]
