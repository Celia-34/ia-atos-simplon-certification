# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement).

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.607 | 0.573 | 🔴 0.376 | 0.435 | 12.4 % | 🟢 3.7 % |
| LogisticRegression (C=0.1) | 0.541 | 0.53 | 0.61 | 0.467 | 14.1 % | 9.2 % |
| LogisticRegression (C=10) | 🔴 0.521 | 🔴 0.508 | 0.536 | 🔴 0.421 | 14.9 % | 🔴 12.0 % |
| LogisticRegression (default) | 0.526 | 0.514 | 0.561 | 0.438 | 14.1 % | 11.6 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.636 | 🟢 0.617 | 0.53 | 🟢 0.518 | 🟢 9.9 % | 3.9 % |
| RandomForestClassifier (default) | 🟢 0.642 | 0.616 | 0.481 | 0.501 | 11.3 % | 4.4 % |
| RandomForestClassifier (max_depth=10) | 0.568 | 0.544 | 0.591 | 0.48 | 🔴 16.3 % | 7.6 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.56 | 0.538 | 🟢 0.655 | 0.479 | 16.0 % | 9.7 % |
| RandomForestClassifier (n_estimators=300) | 0.641 | 0.617 | 0.486 | 0.505 | 10.2 % | 4.3 % |

## Scénario `s2`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.456 | 0.401 | 🔴 0.171 | 🔴 0.213 | 🟢 28.7 % | 🟢 8.0 % |
| LogisticRegression (C=0.1) | 0.422 | 0.406 | 0.395 | 0.292 | 30.9 % | 25.0 % |
| LogisticRegression (C=10) | 0.417 | 0.4 | 0.401 | 0.289 | 32.0 % | 🔴 26.2 % |
| LogisticRegression (default) | 0.418 | 0.402 | 0.401 | 0.291 | 32.3 % | 26.0 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.394 | 🔴 0.369 | 0.276 | 0.241 | 🟢 28.7 % | 18.4 % |
| RandomForestClassifier (default) | 0.396 | 0.371 | 0.271 | 0.246 | 30.7 % | 16.8 % |
| RandomForestClassifier (max_depth=10) | 0.424 | 0.395 | 0.271 | 0.26 | 🔴 32.6 % | 13.8 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.438 | 🟢 0.422 | 🟢 0.417 | 🟢 0.323 | 29.0 % | 20.8 % |
| RandomForestClassifier (n_estimators=300) | 0.4 | 0.375 | 0.279 | 0.254 | 🟢 28.7 % | 17.0 % |

## Scénario `s3`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |
| LogisticRegression (C=0.1) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |
| LogisticRegression (C=10) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |
| LogisticRegression (default) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.64 | 🔴 0.623 | 🟢 0.669 | 🔴 0.519 | 🟢 18.2 % | 🔴 22.0 % |
| RandomForestClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |
| RandomForestClassifier (max_depth=10) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |
| RandomForestClassifier (min_samples_leaf=5) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |
| RandomForestClassifier (n_estimators=300) | 🟢 0.652 | 🟢 0.635 | 🔴 0.66 | 🟢 0.542 | 🔴 19.1 % | 🟢 18.7 % |

## Scénario `s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.544 | 🟢 0.507 | 🔴 0.293 | 🔴 0.379 | 15.2 % | 🟢 2.5 % |
| LogisticRegression (C=0.1) | 🔴 0.46 | 🔴 0.457 | 0.591 | 0.453 | 🔴 19.3 % | 9.5 % |
| LogisticRegression (C=10) | 0.46 | 0.458 | 0.586 | 0.452 | 🔴 19.3 % | 9.5 % |
| LogisticRegression (default) | 0.46 | 0.458 | 0.586 | 0.452 | 🔴 19.3 % | 9.5 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.469 | 0.467 | 🟢 0.63 | 0.428 | 🟢 12.4 % | 🔴 20.0 % |
| RandomForestClassifier (default) | 0.48 | 0.475 | 0.577 | 0.45 | 16.3 % | 11.6 % |
| RandomForestClassifier (max_depth=10) | 0.486 | 0.48 | 0.591 | 🟢 0.463 | 16.6 % | 10.9 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.492 | 0.485 | 0.583 | 0.458 | 16.9 % | 10.1 % |
| RandomForestClassifier (n_estimators=300) | 0.478 | 0.472 | 0.583 | 0.443 | 16.3 % | 13.2 % |

## Scénario `s4-age-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.538 | 0.515 | 🔴 0.37 | 0.421 | 15.5 % | 🟢 5.2 % |
| LogisticRegression (C=0.1) | 0.466 | 0.46 | 0.569 | 0.435 | 18.8 % | 11.9 % |
| LogisticRegression (C=10) | 🔴 0.46 | 0.454 | 0.533 | 🔴 0.412 | 18.5 % | 🔴 12.8 % |
| LogisticRegression (default) | 0.463 | 0.457 | 0.547 | 0.419 | 18.2 % | 12.6 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.542 | 0.534 | 0.522 | 0.493 | 🟢 14.1 % | 7.9 % |
| RandomForestClassifier (default) | 0.548 | 0.538 | 0.489 | 0.492 | 16.0 % | 7.2 % |
| RandomForestClassifier (max_depth=10) | 0.516 | 0.495 | 0.599 | 0.477 | 19.6 % | 9.1 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.477 | 🔴 0.441 | 🟢 0.677 | 0.467 | 🔴 21.0 % | 11.7 % |
| RandomForestClassifier (n_estimators=300) | 🟢 0.553 | 🟢 0.543 | 0.5 | 🟢 0.498 | 16.0 % | 7.1 % |
