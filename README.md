# Certification IA - Trajectoire emploi

Ce dépôt présente un cas d'usage d'intelligence artificielle pour estimer le délai de retour à l'emploi d'un demandeur d'emploi (moins de 6 mois, 6 à 12 mois, plus de 12 mois). Il contient l'analyse et l'évaluation du modèle dans un notebook, ainsi qu'une application web conteneurisée pour tester des prédictions.

## Contexte

Projet réalisé dans le cadre de la formation certifiante en intelligence artificielle Simplon / ATOS Atlas IA, parcours 2 (Pros IT), du 18 mai au 15 octobre 2026. Le sujet de certification porte sur le cadrage, l'analyse et la modélisation d'un cas d'usage IA à partir du jeu de données « Trajectoire Emploi », avec une attention particulière aux erreurs de prédiction, aux biais et aux enjeux réglementaires.
Auteur : Célia Fortuna

## Lancer le notebook

Le notebook principal est [`notebooks/certification-cas-usage.ipynb`](notebooks/certification-cas-usage.ipynb). Depuis la racine du dépôt, créez un environnement Python 3.11+ et installez les dépendances :

```bash
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd notebooks
jupyter lab certification-cas-usage.ipynb
```

Exécutez les cellules dans l'ordre. Le démarrage depuis `notebooks/` est nécessaire pour que les chemins relatifs trouvent les fichiers `data/` et `resources/` à la racine. Le jeu de données et les ressources nécessaires sont déjà présents dans le dépôt.

## Lancer l'application avec Docker

Installez et démarrez Docker Desktop, puis lancez depuis la racine du dépôt :

```bash
docker compose up --build
```

Ouvrez l'application sur [http://localhost:8088](http://localhost:8088). Les services et outils de suivi sont également disponibles sur [Prometheus](http://localhost:9090), [Grafana](http://localhost:3001) (identifiants initiaux `admin` / `admin`) et [MLflow](http://localhost:5000). Pour arrêter les conteneurs, utilisez `Ctrl+C`, puis :

```bash
docker compose down
```
