"""Génère du trafic de scoring valide pour alimenter le dashboard Grafana.

Les payloads sont échantillonnés dans `data/dataset_trajectoire_emploi.csv`
(et non générés aléatoirement) pour que la répartition des classes prédites
affichée dans Grafana reflète la distribution réelle des usagers.

Exemples:
    python scripts/generate_traffic.py --requests 500 --concurrency 20
    python scripts/generate_traffic.py --duration 300 --rate 5 --error-rate 0.05
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = REPO_ROOT / "data" / "dataset_trajectoire_emploi.csv"
REFERENTIEL_FAMILLES = REPO_ROOT / "data" / "referentiel_familles.csv"

sys.path.insert(0, str(Path(__file__).resolve().parent))
# Le nettoyage/anonymisation du texte (§3.3.2.1) n'est pas redupliqué ici : sans
# la transformation EXACTE utilisée à l'entraînement, la synthèse ne retomberait
# pas sur une clé du référentiel et le trafic généré n'aurait pas la même
# distribution de familles que le dataset.
from preprocess import anonymiser_texte, nettoyer_texte  # noqa: E402

NIVEAUX_DIPLOME = {"Sans diplôme", "Bac", "Bac+2", "Bac+5"}
ROME_PATTERN = re.compile(r"^[A-Z]\d{4}$")
DEPARTEMENT_PATTERN = re.compile(r"^(\d{2}|2A|2B)$")
FAMILLE_TEXTE_MANQUANT = "texte_manquant"


def load_familles() -> dict[str, str]:
    """Correspondance texte préparé → famille thématique (référentiel figé §4.2.2)."""
    with REFERENTIEL_FAMILLES.open(encoding="utf-8", newline="") as handle:
        return {
            row["synthese_entretien_prepare"]: row["famille_thematique"]
            for row in csv.DictReader(handle)
        }


FAMILLES = load_familles()


@dataclass
class Result:
    status: int | None
    elapsed: float
    error: str | None = None


def row_to_payload(row: dict[str, str]) -> dict[str, object] | None:
    """Convertit une ligne du dataset en payload `UsagerFeatures`, ou None si invalide."""
    try:
        age = int(float(row["age"]))
        anciennete = float(row["anciennete_poste_ans"])
        est_allocataire = int(float(row["est_allocataire"]))
    except (KeyError, TypeError, ValueError):
        return None

    niveau = (row.get("niveau_diplome") or "").strip()
    rome = (row.get("code_rome_vise") or "").strip().upper()
    # Le dataset porte le code INSEE commune ; l'API attend le département (cf. prepare_tabular_features).
    departement = (row.get("code_insee_commune") or "").strip().zfill(5)[:2].upper()
    # La synthèse d'entretien n'est plus envoyée en texte : l'API attend la
    # famille thématique correspondante (phase 2).
    texte = anonymiser_texte(nettoyer_texte(row.get("synthese_entretien") or ""))
    famille = FAMILLES.get(texte, FAMILLE_TEXTE_MANQUANT) if texte else FAMILLE_TEXTE_MANQUANT

    if not (18 <= age <= 70 and 0 <= anciennete <= 40 and est_allocataire in (0, 1)):
        return None
    if niveau not in NIVEAUX_DIPLOME:
        return None
    if not ROME_PATTERN.match(rome) or not DEPARTEMENT_PATTERN.match(departement):
        return None

    return {
        "age": age,
        "anciennete_poste_ans": round(anciennete, 1),
        "niveau_diplome": niveau,
        "code_rome_vise": rome,
        "est_allocataire": est_allocataire,
        "departement": departement,
        "famille_thematique": famille,
    }


def load_payloads(dataset: Path) -> list[dict[str, object]]:
    """Charge tous les payloads valides du dataset."""
    if not dataset.is_file():
        raise SystemExit(f"Dataset introuvable : {dataset}")

    with dataset.open(encoding="utf-8", newline="") as handle:
        payloads = [p for row in csv.DictReader(handle) if (p := row_to_payload(row))]

    if not payloads:
        raise SystemExit(f"Aucune ligne exploitable dans {dataset}")
    return payloads


def corrupt(payload: dict[str, object], randomizer: random.Random) -> dict[str, object]:
    """Casse une contrainte du schéma pour provoquer un 422 (alimente le panel 4xx)."""
    broken = dict(payload)
    field, value = randomizer.choice(
        [
            ("age", 12),
            ("anciennete_poste_ans", 99.0),
            ("code_rome_vise", "XX"),
            ("departement", "999"),
            ("niveau_diplome", "Doctorat"),
            # Modalité hors référentiel : c'est précisément ce que le Literal du
            # schéma doit rejeter, plutôt que de laisser l'encodeur la traiter
            # silencieusement en vecteur nul.
            ("famille_thematique", "profil en or massif"),
        ]
    )
    broken[field] = value
    return broken


def send_request(url: str, payload: dict[str, object], timeout: float) -> Result:
    started = time.perf_counter()
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            response.read()
            return Result(response.status, time.perf_counter() - started)
    except HTTPError as error:
        return Result(error.code, time.perf_counter() - started, str(error))
    except (URLError, TimeoutError, OSError) as error:
        return Result(None, time.perf_counter() - started, str(error))


def run_worker(
    url: str,
    payloads: list[dict[str, object]],
    timeout: float,
    budget: int | None,
    deadline: float | None,
    delay: float,
    error_rate: float,
    seed: int,
) -> list[Result]:
    """Envoie des requêtes jusqu'à épuisement du budget ou expiration du deadline."""
    randomizer = random.Random(seed)
    results: list[Result] = []
    sent = 0
    while True:
        if budget is not None and sent >= budget:
            break
        if deadline is not None and time.monotonic() >= deadline:
            break

        payload = randomizer.choice(payloads)
        if error_rate and randomizer.random() < error_rate:
            payload = corrupt(payload, randomizer)

        results.append(send_request(url, payload, timeout))
        sent += 1
        if delay:
            time.sleep(delay)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        default="http://localhost:8001/score",
        help="Endpoint de scoring (défaut: %(default)s)",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        help="CSV source des payloads (défaut: data/dataset_trajectoire_emploi.csv)",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=100,
        help="Nombre total de requêtes à envoyer (ignoré si --duration; défaut: %(default)s)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Durée en secondes d'un trafic soutenu (0 = mode --requests; ex. 300 pour 5 min)",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=0.0,
        help="Débit cible global en req/s (0 = aussi vite que possible)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Nombre de requêtes simultanées (défaut: %(default)s)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout par requête en secondes (défaut: %(default)s)",
    )
    parser.add_argument(
        "--error-rate",
        type=float,
        default=0.0,
        help="Fraction de payloads volontairement invalides (0.0-1.0) pour alimenter le panel 4xx",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Graine pour un échantillonnage reproductible",
    )
    args = parser.parse_args()
    if args.requests < 1 or args.concurrency < 1 or args.timeout <= 0:
        parser.error("--requests, --concurrency et --timeout doivent être positifs")
    if args.duration < 0 or args.rate < 0:
        parser.error("--duration et --rate ne peuvent pas être négatifs")
    if not 0.0 <= args.error_rate <= 1.0:
        parser.error("--error-rate doit être compris entre 0.0 et 1.0")
    return args


def main() -> int:
    args = parse_args()
    payloads = load_payloads(args.dataset)
    base_seed = args.seed if args.seed is not None else random.randrange(2**32)

    delay = args.concurrency / args.rate if args.rate else 0.0
    deadline = time.monotonic() + args.duration if args.duration else None
    if deadline:
        budgets = [None] * args.concurrency
    else:
        base, extra = divmod(args.requests, args.concurrency)
        budgets = [base + (i < extra) for i in range(args.concurrency)]

    print(
        f"{len(payloads)} payloads charges depuis {args.dataset.name} -> {args.url} "
        f"({'duree ' + str(args.duration) + 's' if deadline else str(args.requests) + ' requetes'}, "
        f"concurrence {args.concurrency})"
    )

    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [
            executor.submit(
                run_worker,
                args.url,
                payloads,
                args.timeout,
                budget,
                deadline,
                delay,
                args.error_rate,
                base_seed + worker_id,
            )
            for worker_id, budget in enumerate(budgets)
        ]
        results = [result for future in futures for result in future.result()]

    elapsed = time.perf_counter() - started
    if not results:
        print("Aucune requete envoyee.")
        return 1

    successful = sum(r.status is not None and 200 <= r.status < 300 for r in results)
    client_errors = sum(r.status is not None and 400 <= r.status < 500 for r in results)
    server_errors = sum(r.status is not None and r.status >= 500 for r in results)
    unreachable = sum(r.status is None for r in results)
    average_latency = sum(r.elapsed for r in results) / len(results)

    print(f"Envoyees        : {len(results)}")
    print(f"Succes (2xx)    : {successful}")
    print(f"Erreurs 4xx     : {client_errors}")
    print(f"Erreurs 5xx     : {server_errors}")
    print(f"Injoignables    : {unreachable}")
    print(f"Duree           : {elapsed:.2f}s")
    print(f"Debit           : {len(results) / elapsed:.2f} req/s")
    print(f"Latence moyenne : {average_latency * 1000:.1f} ms")

    unexpected = server_errors + unreachable
    if unexpected:
        for result in results:
            if result.error and (result.status is None or result.status >= 500):
                print(f"Exemple d'echec : status={result.status} detail={result.error}")
                break
    return 0 if unexpected == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
