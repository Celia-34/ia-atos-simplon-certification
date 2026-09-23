"""Isolation des packages `app` entre les services — conftest racine.

Les quatre services (`model`, `backend`, `frontend`, `feedback`) exposent
chacun un package nommé `app`. Collectés dans un même processus, le premier
`app` importé gagne et les suites suivantes testent le mauvais service.

Ces deux hooks garantissent qu'au moment d'importer un module de test — et
au moment de l'exécuter — le package `app` résolu est bien celui du service
auquel le test appartient :

* purge des entrées `app` / `app.*` de `sys.modules` ;
* la racine du service concerné est replacée en tête de `sys.path`.

Les suites déjà collectées conservent leur référence au module objet : purger
`sys.modules` ne casse pas les objets FastAPI déjà construits.

Sans cela, la commande de vérification du plan d'alignement
(`pytest tests services/model/tests services/backend/tests services/frontend/tests`)
ne peut pas passer en une seule invocation.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()
SERVICES_DIR = REPO_ROOT / "services"


def _service_root_for(path: Path | None) -> Path | None:
    """Racine du service auquel `path` appartient, sinon None."""
    if path is None:
        return None
    try:
        relative = Path(path).resolve().relative_to(SERVICES_DIR)
    except (ValueError, OSError):
        return None
    if not relative.parts:
        return None
    return SERVICES_DIR / relative.parts[0]


_active_service: Path | None = None


def _activate_service(service_root: Path) -> None:
    """Rend `app` résolvable vers `service_root`.

    La purge n'a lieu que si un autre service est actif : réimporter le même
    service ferait ré-enregistrer ses collecteurs dans le registre global
    Prometheus (`Duplicated timeseries in CollectorRegistry`).
    """
    global _active_service
    if _active_service != service_root:
        for name in [n for n in sys.modules if n == "app" or n.startswith("app.")]:
            del sys.modules[name]
        _active_service = service_root
    entry = str(service_root)
    while entry in sys.path:
        sys.path.remove(entry)
    sys.path.insert(0, entry)


def _node_path(node: object) -> Path | None:
    path = getattr(node, "path", None)
    if path is None:
        fspath = getattr(node, "fspath", None)
        path = Path(str(fspath)) if fspath is not None else None
    return Path(str(path)) if path is not None else None


def pytest_collectstart(collector) -> None:
    """Avant l'import d'un module de test, active le bon service."""
    service_root = _service_root_for(_node_path(collector))
    if service_root is not None:
        _activate_service(service_root)


def pytest_runtest_setup(item) -> None:
    """Avant l'exécution d'un test (imports différés en fixture), idem."""
    service_root = _service_root_for(_node_path(item))
    if service_root is not None:
        _activate_service(service_root)
