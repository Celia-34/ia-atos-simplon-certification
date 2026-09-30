# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced) | 0.711 | 0.692 | 0.613 | 0.603 | 11.9 % | 6.4 % | 22.9 % | 80 770 € | 9 160 € | 89 930 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | ⭐🟢 0.72 | ⭐🟢 0.706 | 0.649 | ⭐🟢 0.638 | 🟢 10.2 % | 4.9 % | 26.0 % | 69 470 € | 10 400 € | 79 870 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.707 | 0.69 | 0.63 | 0.609 | 🟢 10.2 % | 6.0 % | 24.6 % | 70 680 € | 9 860 € | 80 540 € |
| HistGradientBoostingClassifier (default) | 0.714 | 0.692 | 🔴 0.561 | 0.607 | 12.2 % | 🟢 4.3 % | 20.0 % | 🔴 89 450 € | 🟢 8 000 € | 🔴 97 450 € |
| LogisticRegression (C=0.1) | 0.688 | 0.672 | 0.685 | 0.583 | 15.2 % | 11.2 % | 43.5 % | 40 120 € | 17 400 € | 57 520 € |
| LogisticRegression (C=10) | 0.666 | 0.649 | 0.638 | 0.553 | 15.5 % | 10.1 % | 33.8 % | 73 220 € | 13 520 € | 86 740 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.654 | 🔴 0.642 | 0.735 | 🔴 0.55 | 11.6 % | 🔴 15.5 % | 43.2 % | 40 370 € | 17 300 € | 57 670 € |
| LogisticRegression (default) | 0.682 | 0.666 | 0.674 | 0.579 | 14.6 % | 10.5 % | 37.6 % | 55 490 € | 15 020 € | 70 510 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.71 | 0.694 | 0.666 | 0.61 | 11.9 % | 8.3 % | 36.7 % | 49 300 € | 14 680 € | 63 980 € |
| RandomForestClassifier (default) | 0.71 | 0.695 | 0.66 | 0.622 | 14.1 % | 6.1 % | 36.1 % | 50 270 € | 14 460 € | 64 730 € |
| RandomForestClassifier (max_depth=10) | 0.7 | 0.686 | 0.677 | 0.615 | 🔴 18.8 % | 7.6 % | 59.9 % | 26 450 € | 🔴 23 940 € | 50 390 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.7 | 0.687 | ⭐🟢 0.754 | 0.612 | 13.5 % | 11.3 % | 56.8 % | ⭐🟢 22 520 € | 22 720 € | ⭐🟢 45 240 € |
| RandomForestClassifier (n_estimators=300) | 0.713 | 0.695 | 0.641 | 0.607 | 13.8 % | 7.1 % | 35.2 % | 49 620 € | 14 100 € | 63 720 € |

## Scénario `s2`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.601 | 0.563 | 🔴 0.395 | 🔴 0.412 | 🔴 26.5 % | 🟢 11.7 % | 28.1 % | 🔴 115 110 € | 🟢 11 220 € | 🔴 126 330 € |
| LogisticRegression (default) | 🟢 0.647 | 🟢 0.628 | 🟢 0.63 | 🟢 0.519 | 🟢 18.5 % | 🔴 18.6 % | 50.9 % | 🟢 46 720 € | 🔴 20 380 € | 🟢 67 100 € |
| RandomForestClassifier (default) | 🔴 0.575 | 🔴 0.55 | 0.475 | 0.426 | 26.0 % | 15.9 % | 35.9 % | 77 750 € | 14 380 € | 92 130 € |

## Scénario `s3`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 31.2 % | 🔴 97 540 € | 🟢 12 480 € | 🔴 110 020 € |
| LogisticRegression (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 62.7 % | 🟢 30 540 € | 🔴 25 100 € | 🟢 55 640 € |
| RandomForestClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 62.7 % | 🟢 30 540 € | 🔴 25 100 € | 🟢 55 640 € |

## Scénario `s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.541 | 🟢 0.504 | 🔴 0.29 | 🔴 0.376 | 🟢 16.0 % | 🟢 2.7 % | 22.6 % | 🔴 143 650 € | 🟢 9 040 € | 🔴 152 690 € |
| LogisticRegression (default) | 🔴 0.432 | 🔴 0.422 | 🟢 0.619 | 0.421 | 🔴 18.5 % | 🔴 17.1 % | 62.5 % | 🟢 59 330 € | 🔴 25 020 € | 🟢 84 350 € |
| RandomForestClassifier (default) | 0.481 | 0.475 | 0.577 | 🟢 0.449 | 16.6 % | 11.6 % | 49.2 % | 76 920 € | 19 700 € | 96 620 € |

## Scénario `s4-age-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.544 | 0.521 | 🔴 0.381 | 0.431 | 16.9 % | 🟢 5.3 % | 21.4 % | 🔴 134 760 € | 🟢 8 560 € | 🔴 143 320 € |
| LogisticRegression (default) | 🔴 0.455 | 🔴 0.448 | 🟢 0.547 | 🔴 0.404 | 🔴 17.7 % | 🔴 15.2 % | 51.3 % | 🟢 73 900 € | 🔴 20 520 € | 🟢 94 420 € |
| RandomForestClassifier (default) | 🟢 0.549 | 🟢 0.539 | 0.494 | 🟢 0.491 | 🟢 15.5 % | 7.2 % | 33.1 % | 99 540 € | 13 220 € | 112 760 € |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced) | 0.644 | 0.622 | 0.508 | 0.511 | 10.5 % | 4.5 % | 25.8 % | 98 070 € | 10 320 € | 108 390 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.662 | 0.641 | 0.547 | 0.544 | 9.4 % | 4.9 % | 28.9 % | 92 500 € | 11 580 € | 104 080 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.645 | 0.625 | 0.533 | 0.526 | 8.8 % | 5.2 % | 26.7 % | 95 630 € | 10 660 € | 106 290 € |
| HistGradientBoostingClassifier (default) | 0.658 | 0.632 | 🔴 0.467 | 0.525 | 9.9 % | 3.5 % | 19.1 % | 🔴 112 360 € | ⭐🟢 7 640 € | 🔴 120 000 € |
| LogisticRegression (C=0.1) | 0.547 | 0.536 | 0.652 | 0.477 | 14.1 % | 12.6 % | 53.9 % | 62 360 € | 21 560 € | 83 920 € |
| LogisticRegression (C=10) | 0.532 | 0.519 | 0.55 | 🔴 0.425 | 15.5 % | 11.3 % | 40.3 % | 91 250 € | 16 100 € | 107 350 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.5 | 🔴 0.495 | 🟢 0.685 | 0.432 | 12.2 % | 🔴 17.8 % | 56.1 % | 55 860 € | 22 460 € | 78 320 € |
| LogisticRegression (default) | 0.54 | 0.526 | 0.566 | 0.436 | 14.9 % | 11.2 % | 44.4 % | 76 250 € | 17 760 € | 94 010 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.693 | 0.674 | 0.561 | 0.589 | 9.7 % | ⭐🟢 2.5 % | 31.7 % | 78 260 € | 12 660 € | 90 920 € |
| RandomForestClassifier (default) | 0.69 | 0.674 | 0.569 | 0.601 | 9.4 % | ⭐🟢 2.5 % | 29.6 % | 83 420 € | 11 860 € | 95 280 € |
| RandomForestClassifier (max_depth=10) | 0.632 | 0.619 | 0.594 | 0.573 | 🔴 15.7 % | 3.7 % | 64.0 % | 🟢 48 440 € | 🔴 25 620 € | 🟢 74 060 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.628 | 0.611 | 0.622 | 0.52 | 11.9 % | 7.2 % | 59.5 % | 51 820 € | 23 780 € | 75 600 € |
| RandomForestClassifier (n_estimators=300) | 🟢 0.698 | 🟢 0.68 | 0.561 | 🟢 0.601 | ⭐🟢 8.3 % | 2.7 % | 28.3 % | 85 200 € | 11 340 € | 96 540 € |
