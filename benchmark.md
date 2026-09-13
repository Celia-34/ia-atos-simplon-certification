# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement).

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.681 | 0.657 | 🔴 0.525 | 0.556 | 🟢 12.4 % | 🟢 5.2 % |
| LogisticRegression (C=0.1) | 0.682 | 🟢 0.667 | 🟢 0.696 | 🟢 0.581 | 🔴 16.3 % | 12.4 % |
| LogisticRegression (C=10) | 🔴 0.646 | 🔴 0.628 | 0.613 | 🔴 0.525 | 15.5 % | 11.2 % |
| LogisticRegression (default) | 0.676 | 0.661 | 0.674 | 0.573 | 13.8 % | 11.1 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.671 | 0.654 | 0.649 | 0.563 | 13.5 % | 12.7 % |
| RandomForestClassifier (default) | 🟢 0.684 | 0.666 | 0.63 | 0.576 | 15.7 % | 10.1 % |
| RandomForestClassifier (max_depth=10) | 0.659 | 0.644 | 0.688 | 0.555 | 15.2 % | 18.3 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.655 | 0.639 | 0.682 | 0.546 | 🔴 16.3 % | 🔴 19.1 % |
| RandomForestClassifier (n_estimators=300) | 0.684 | 0.665 | 0.63 | 0.574 | 🔴 16.3 % | 10.4 % |

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

## Scénario `s3+s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.651 | 0.622 | 🔴 0.47 | 0.502 | 🟢 16.9 % | 🟢 6.8 % |
| LogisticRegression (default) | 🟢 0.666 | 🟢 0.648 | 🟢 0.669 | 🟢 0.548 | 17.1 % | 🔴 15.6 % |
| RandomForestClassifier (default) | 🔴 0.586 | 🔴 0.57 | 0.555 | 🔴 0.48 | 🔴 17.7 % | 12.7 % |

## Scénario `s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.541 | 🟢 0.504 | 🔴 0.29 | 🔴 0.376 | 16.0 % | 🟢 2.7 % |
| LogisticRegression (C=0.1) | 🔴 0.432 | 🔴 0.421 | 0.619 | 0.42 | 🔴 19.1 % | 17.2 % |
| LogisticRegression (C=10) | 🔴 0.432 | 0.422 | 0.619 | 0.421 | 18.5 % | 17.1 % |
| LogisticRegression (default) | 🔴 0.432 | 0.422 | 0.619 | 0.421 | 18.5 % | 17.1 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.47 | 0.467 | 🟢 0.63 | 0.428 | 🟢 12.4 % | 🔴 20.0 % |
| RandomForestClassifier (default) | 0.481 | 0.475 | 0.577 | 0.449 | 16.6 % | 11.6 % |
| RandomForestClassifier (max_depth=10) | 0.489 | 0.482 | 0.586 | 🟢 0.463 | 17.1 % | 10.7 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.493 | 0.486 | 0.577 | 0.457 | 16.9 % | 10.3 % |
| RandomForestClassifier (n_estimators=300) | 0.478 | 0.472 | 0.583 | 0.443 | 16.3 % | 13.2 % |

## Scénario `s4-age-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.544 | 0.521 | 🔴 0.381 | 0.431 | 16.9 % | 🟢 5.3 % |
| LogisticRegression (C=0.1) | 0.458 | 0.449 | 0.627 | 0.437 | 18.5 % | 🔴 15.8 % |
| LogisticRegression (C=10) | 🔴 0.453 | 0.446 | 0.536 | 🔴 0.4 | 17.7 % | 15.0 % |
| LogisticRegression (default) | 0.455 | 0.448 | 0.547 | 0.404 | 17.7 % | 15.2 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.544 | 0.535 | 0.519 | 0.488 | 🟢 12.2 % | 8.5 % |
| RandomForestClassifier (default) | 0.549 | 0.539 | 0.494 | 0.491 | 15.5 % | 7.2 % |
| RandomForestClassifier (max_depth=10) | 0.515 | 0.491 | 0.63 | 0.481 | 🔴 20.2 % | 10.8 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.48 | 🔴 0.446 | 🟢 0.74 | 0.463 | 18.5 % | 15.6 % |
| RandomForestClassifier (n_estimators=300) | 🟢 0.554 | 🟢 0.544 | 0.503 | 🟢 0.498 | 16.0 % | 6.9 % |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.613 | 0.577 | 🔴 0.373 | 0.434 | 12.4 % | 🟢 3.5 % |
| LogisticRegression (C=0.1) | 0.506 | 0.495 | 0.622 | 0.436 | 16.6 % | 🔴 15.6 % |
| LogisticRegression (C=10) | 🔴 0.501 | 🔴 0.488 | 0.525 | 🔴 0.398 | 🔴 18.2 % | 13.9 % |
| LogisticRegression (default) | 0.509 | 0.497 | 0.547 | 0.41 | 17.1 % | 14.0 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.636 | 0.614 | 0.511 | 0.503 | 9.7 % | 4.4 % |
| RandomForestClassifier (default) | 0.648 | 0.627 | 0.517 | 0.529 | 🟢 9.4 % | 4.1 % |
| RandomForestClassifier (max_depth=10) | 0.55 | 0.526 | 0.646 | 0.49 | 16.6 % | 8.8 % |
| RandomForestClassifier (min_samples_leaf=5) | 0.562 | 0.543 | 🟢 0.669 | 0.475 | 13.8 % | 10.9 % |
| RandomForestClassifier (n_estimators=300) | 🟢 0.654 | 🟢 0.633 | 0.511 | 🟢 0.535 | 9.7 % | 3.6 % |
