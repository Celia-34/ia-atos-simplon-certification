# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced) | 0.714 | 0.698 | 0.624 | ⭐🟢 0.622 | 9.7 % | 6.0 % | 21.3 % | 83 450 € | 8 520 € | 91 970 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.715 | ⭐🟢 0.699 | 0.646 | 0.618 | 10.5 % | 6.5 % | 23.5 % | 75 990 € | 9 400 € | 85 390 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.702 | 0.686 | 0.638 | 0.609 | 🟢 9.4 % | 7.1 % | 22.2 % | 82 320 € | 8 880 € | 91 200 € |
| HistGradientBoostingClassifier (default) | ⭐🟢 0.716 | 0.696 | 🔴 0.569 | 0.611 | 10.8 % | 🟢 4.5 % | 18.8 % | 🔴 91 960 € | 🟢 7 520 € | 🔴 99 480 € |
| LogisticRegression (C=0.1) | 0.687 | 0.672 | 0.693 | 0.587 | 15.2 % | 11.2 % | 33.5 % | 58 090 € | 13 380 € | 71 470 € |
| LogisticRegression (C=10) | 0.667 | 0.65 | 0.644 | 0.557 | 15.5 % | 10.1 % | 29.2 % | 83 190 € | 11 700 € | 94 890 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.654 | 0.642 | ⭐🟢 0.738 | 0.552 | 11.0 % | 15.6 % | 37.1 % | 57 040 € | 🔴 14 860 € | 71 900 € |
| LogisticRegression (default) | 0.681 | 0.665 | 0.666 | 0.574 | 14.9 % | 10.4 % | 30.0 % | 71 430 € | 12 020 € | 83 450 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.684 | 0.666 | 0.655 | 0.577 | 13.3 % | 11.6 % | 30.9 % | 60 500 € | 12 380 € | 72 880 € |
| RandomForestClassifier (default) | 0.685 | 0.668 | 0.627 | 0.582 | 15.7 % | 8.7 % | 28.8 % | 67 020 € | 11 520 € | 78 540 € |
| RandomForestClassifier (max_depth=10) | 0.66 | 0.644 | 0.688 | 0.553 | 14.9 % | 18.6 % | 34.9 % | 56 100 € | 13 960 € | 70 060 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.656 | 🔴 0.64 | 0.68 | 🔴 0.544 | 15.7 % | 🔴 19.5 % | 36.1 % | ⭐🟢 53 820 € | 14 460 € | ⭐🟢 68 280 € |
| RandomForestClassifier (n_estimators=300) | 0.691 | 0.673 | 0.633 | 0.586 | 🔴 17.7 % | 8.7 % | 29.2 % | 66 280 € | 11 680 € | 77 960 € |

## Scénario `s2`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.456 | 0.401 | 🔴 0.171 | 🔴 0.213 | 🟢 28.7 % | 🟢 8.0 % | 18.0 % | 🔴 195 570 € | 🟢 7 200 € | 🔴 202 770 € |
| LogisticRegression (default) | 0.418 | 🟢 0.402 | 🟢 0.401 | 🟢 0.291 | 🔴 32.3 % | 🔴 26.0 % | 55.3 % | 🟢 82 940 € | 🔴 22 140 € | 🟢 105 080 € |
| RandomForestClassifier (default) | 🔴 0.396 | 🔴 0.371 | 0.271 | 0.246 | 30.7 % | 16.8 % | 30.9 % | 177 890 € | 12 360 € | 190 250 € |

## Scénario `s3`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 24.7 % | 🔴 103 380 € | 🟢 9 880 € | 🔴 113 260 € |
| LogisticRegression (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 28.5 % | 🟢 99 580 € | 🔴 11 420 € | 🟢 111 000 € |
| RandomForestClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 28.5 % | 🟢 99 580 € | 🔴 11 420 € | 🟢 111 000 € |

## Scénario `s3+s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.651 | 0.622 | 🔴 0.47 | 0.502 | 🟢 16.9 % | 🟢 6.8 % | 20.6 % | 🔴 117 040 € | 🟢 8 240 € | 🔴 125 280 € |
| LogisticRegression (default) | 🟢 0.666 | 🟢 0.648 | 🟢 0.669 | 🟢 0.548 | 17.1 % | 🔴 15.6 % | 35.9 % | 🟢 61 770 € | 🔴 14 380 € | 🟢 76 150 € |
| RandomForestClassifier (default) | 🔴 0.586 | 🔴 0.57 | 0.555 | 🔴 0.48 | 🔴 17.7 % | 12.7 % | 28.9 % | 101 630 € | 11 580 € | 113 210 € |

## Scénario `s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.541 | 🟢 0.504 | 🔴 0.29 | 🔴 0.376 | 🟢 16.0 % | 🟢 2.7 % | 13.6 % | 🔴 160 170 € | ⭐🟢 5 420 € | 🔴 165 590 € |
| LogisticRegression (default) | 🔴 0.432 | 🔴 0.422 | 🟢 0.619 | 0.421 | 🔴 18.5 % | 🔴 17.1 % | 40.7 % | 101 190 € | 16 300 € | 117 490 € |
| RandomForestClassifier (default) | 0.481 | 0.475 | 0.577 | 🟢 0.449 | 16.6 % | 11.6 % | 41.0 % | 🟢 89 360 € | 🔴 16 420 € | 🟢 105 780 € |

## Scénario `s4-age-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.544 | 0.521 | 🔴 0.381 | 0.431 | 16.9 % | 🟢 5.3 % | 17.4 % | 🔴 143 340 € | 🟢 6 980 € | 🔴 150 320 € |
| LogisticRegression (default) | 🔴 0.455 | 🔴 0.448 | 🟢 0.547 | 🔴 0.404 | 🔴 17.7 % | 🔴 15.2 % | 37.8 % | 🟢 100 020 € | 🔴 15 120 € | 🟢 115 140 € |
| RandomForestClassifier (default) | 🟢 0.549 | 🟢 0.539 | 0.494 | 🟢 0.491 | 🟢 15.5 % | 7.2 % | 25.7 % | 111 600 € | 10 260 € | 121 860 € |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced) | 0.644 | 0.622 | 0.508 | 0.511 | 10.5 % | 4.5 % | 22.1 % | 103 650 € | 8 820 € | 112 470 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.662 | 0.641 | 0.547 | 0.544 | 9.4 % | 4.9 % | 23.7 % | 98 320 € | 9 480 € | 107 800 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.645 | 0.625 | 0.533 | 0.526 | 8.8 % | 5.2 % | 23.0 % | 100 250 € | 9 180 € | 109 430 € |
| HistGradientBoostingClassifier (default) | 0.658 | 0.632 | 🔴 0.467 | 0.525 | 9.9 % | 3.5 % | 16.6 % | 🔴 115 840 € | 🟢 6 620 € | 🔴 122 460 € |
| LogisticRegression (C=0.1) | 0.547 | 0.536 | 0.652 | 0.477 | 14.1 % | 12.6 % | 37.6 % | 83 660 € | 15 020 € | 98 680 € |
| LogisticRegression (C=10) | 0.532 | 0.519 | 0.55 | 🔴 0.425 | 15.5 % | 11.3 % | 33.7 % | 103 150 € | 13 460 € | 116 610 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.5 | 🔴 0.495 | 🟢 0.685 | 0.432 | 12.2 % | 🔴 17.8 % | 47.4 % | 🟢 66 940 € | 🔴 18 980 € | 🟢 85 920 € |
| LogisticRegression (default) | 0.54 | 0.526 | 0.566 | 0.436 | 14.9 % | 11.2 % | 35.1 % | 93 550 € | 14 040 € | 107 590 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.693 | 0.674 | 0.561 | 0.589 | 9.7 % | ⭐🟢 2.5 % | 23.4 % | 91 020 € | 9 360 € | 100 380 € |
| RandomForestClassifier (default) | 0.69 | 0.674 | 0.569 | 0.601 | 9.4 % | ⭐🟢 2.5 % | 21.5 % | 92 400 € | 8 600 € | 101 000 € |
| RandomForestClassifier (max_depth=10) | 0.632 | 0.619 | 0.594 | 0.573 | 🔴 15.7 % | 3.7 % | 29.9 % | 82 720 € | 11 980 € | 94 700 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.628 | 0.611 | 0.622 | 0.52 | 11.9 % | 7.2 % | 32.2 % | 83 260 € | 12 860 € | 96 120 € |
| RandomForestClassifier (n_estimators=300) | 🟢 0.698 | 🟢 0.68 | 0.561 | 🟢 0.601 | ⭐🟢 8.3 % | 2.7 % | 20.9 % | 91 100 € | 8 360 € | 99 460 € |
