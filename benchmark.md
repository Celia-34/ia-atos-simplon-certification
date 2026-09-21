# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced) | 0.699 | 0.679 | 0.593 | 0.586 | 12.8 % | 6.3 % | 20.6 % | 78 450 € | 🟢 6 580 € | 85 030 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.707 | 0.688 | 0.617 | 0.598 | 11.7 % | 7.3 % | 22.3 % | 70 080 € | 7 140 € | 77 220 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.696 | 0.677 | 0.597 | 0.587 | 12.1 % | 6.7 % | 21.1 % | 75 620 € | 6 740 € | 82 360 € |
| HistGradientBoostingClassifier (default) | ⭐🟢 0.716 | ⭐🟢 0.696 | 🔴 0.569 | ⭐🟢 0.611 | 🟢 10.8 % | 🟢 4.5 % | 18.8 % | 🔴 91 960 € | 7 520 € | 🔴 99 480 € |
| LogisticRegression (C=0.1) | 0.696 | 0.683 | 0.7 | 0.609 | 15.5 % | 9.7 % | 33.4 % | 45 740 € | 10 700 € | 56 440 € |
| LogisticRegression (C=10) | 0.647 | 🔴 0.632 | 0.624 | 0.548 | 14.5 % | 9.0 % | 28.0 % | 71 280 € | 8 960 € | 80 240 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.646 | 0.634 | ⭐🟢 0.71 | 🔴 0.544 | 11.0 % | 15.4 % | 35.8 % | 50 760 € | 11 460 € | 62 220 € |
| LogisticRegression (default) | 0.681 | 0.665 | 0.666 | 0.574 | 14.9 % | 10.4 % | 30.0 % | 71 430 € | 🔴 12 020 € | 83 450 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.691 | 0.677 | 0.686 | 0.606 | 12.1 % | 10.7 % | 30.0 % | 47 940 € | 9 600 € | 57 540 € |
| RandomForestClassifier (default) | 0.685 | 0.668 | 0.627 | 0.582 | 15.7 % | 8.7 % | 28.8 % | 67 020 € | 11 520 € | 78 540 € |
| RandomForestClassifier (max_depth=10) | 0.668 | 0.652 | 0.679 | 0.56 | 🔴 16.6 % | 17.0 % | 33.7 % | ⭐🟢 41 650 € | 10 780 € | ⭐🟢 52 430 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.662 | 0.646 | 0.686 | 0.554 | 15.2 % | 🔴 19.0 % | 34.7 % | 42 760 € | 11 120 € | 53 880 € |
| RandomForestClassifier (n_estimators=300) | 0.691 | 0.675 | 0.659 | 0.6 | 14.8 % | 10.0 % | 28.4 % | 49 640 € | 9 080 € | 58 720 € |

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
| HistGradientBoostingClassifier (class_weight=balanced) | 0.62 | 0.6 | 0.497 | 0.511 | 13.4 % | 5.3 % | 21.3 % | 92 410 € | 6 820 € | 99 230 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.625 | 0.604 | 0.507 | 0.507 | 14.1 % | 6.0 % | 24.6 % | 82 770 € | 7 880 € | 90 650 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.618 | 0.596 | 0.497 | 0.497 | 13.4 % | 7.3 % | 22.9 % | 90 210 € | 7 340 € | 97 550 € |
| HistGradientBoostingClassifier (default) | 0.658 | 0.632 | 🔴 0.467 | 0.525 | 9.9 % | 3.5 % | 16.6 % | 🔴 115 840 € | 🟢 6 620 € | 🔴 122 460 € |
| LogisticRegression (C=0.1) | 0.534 | 0.523 | 0.631 | 0.47 | 15.9 % | 12.4 % | 36.9 % | 70 220 € | 11 800 € | 82 020 € |
| LogisticRegression (C=10) | 0.504 | 0.491 | 0.497 | 🔴 0.406 | 14.8 % | 9.3 % | 32.9 % | 87 990 € | 10 540 € | 98 530 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.481 | 🔴 0.478 | 🟢 0.634 | 0.418 | 11.7 % | 🔴 18.4 % | 45.7 % | 🟢 63 650 € | 🔴 14 620 € | 78 270 € |
| LogisticRegression (default) | 0.54 | 0.526 | 0.566 | 0.436 | 14.9 % | 11.2 % | 35.1 % | 93 550 € | 14 040 € | 107 590 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.687 | 0.663 | 0.528 | 0.552 | ⭐🟢 9.3 % | 3.0 % | 23.2 % | 73 360 € | 7 420 € | 80 780 € |
| RandomForestClassifier (default) | 🟢 0.69 | 🟢 0.674 | 0.569 | 🟢 0.601 | 9.4 % | 2.5 % | 21.5 % | 92 400 € | 8 600 € | 101 000 € |
| RandomForestClassifier (max_depth=10) | 0.629 | 0.611 | 0.572 | 0.548 | 🔴 19.0 % | 4.7 % | 32.4 % | 66 310 € | 10 360 € | 76 670 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.626 | 0.609 | 0.617 | 0.523 | 14.8 % | 7.7 % | 31.9 % | 65 420 € | 10 220 € | 🟢 75 640 € |
| RandomForestClassifier (n_estimators=300) | 0.688 | 0.666 | 0.528 | 0.568 | 10.0 % | ⭐🟢 2.3 % | 20.7 % | 78 680 € | 6 640 € | 85 320 € |
