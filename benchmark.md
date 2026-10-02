# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced) | 0.711 | 0.692 | 0.613 | 0.603 | 11.9 % | 6.4 % | 22.1 % | 82 910 € | 8 820 € | 91 730 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | ⭐🟢 0.72 | ⭐🟢 0.706 | 0.649 | ⭐🟢 0.638 | 🟢 10.2 % | 4.9 % | 24.1 % | 71 710 € | 9 640 € | 81 350 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.707 | 0.69 | 0.63 | 0.609 | 🟢 10.2 % | 6.0 % | 23.1 % | 80 840 € | 9 240 € | 90 080 € |
| HistGradientBoostingClassifier (default) | 0.714 | 0.692 | 🔴 0.561 | 0.607 | 12.2 % | 🟢 4.3 % | 19.1 % | 🔴 92 610 € | 🟢 7 620 € | 🔴 100 230 € |
| LogisticRegression (C=0.1) | 0.688 | 0.672 | 0.685 | 0.583 | 15.2 % | 11.2 % | 37.5 % | 50 740 € | 15 000 € | 65 740 € |
| LogisticRegression (C=10) | 0.666 | 0.649 | 0.638 | 0.553 | 15.5 % | 10.1 % | 30.4 % | 79 640 € | 12 160 € | 91 800 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.654 | 🔴 0.642 | 0.735 | 🔴 0.55 | 11.6 % | 🔴 15.5 % | 39.8 % | 52 690 € | 15 920 € | 68 610 € |
| LogisticRegression (default) | 0.682 | 0.666 | 0.674 | 0.579 | 14.6 % | 10.5 % | 33.3 % | 62 930 € | 13 300 € | 76 230 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.71 | 0.694 | 0.666 | 0.61 | 11.9 % | 8.3 % | 32.6 % | 51 660 € | 13 040 € | 64 700 € |
| RandomForestClassifier (default) | 0.71 | 0.695 | 0.66 | 0.622 | 14.1 % | 6.1 % | 31.9 % | 50 870 € | 12 740 € | 63 610 € |
| RandomForestClassifier (max_depth=10) | 0.7 | 0.686 | 0.677 | 0.615 | 🔴 18.8 % | 7.6 % | 46.1 % | ⭐🟢 31 050 € | 🔴 18 440 € | 49 490 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.7 | 0.687 | ⭐🟢 0.754 | 0.612 | 13.5 % | 11.3 % | 41.5 % | 31 180 € | 16 620 € | ⭐🟢 47 800 € |
| RandomForestClassifier (n_estimators=300) | 0.713 | 0.695 | 0.641 | 0.607 | 13.8 % | 7.1 % | 31.3 % | 55 180 € | 12 520 € | 67 700 € |

## Scénario `s2`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.601 | 0.563 | 🔴 0.395 | 🔴 0.412 | 🔴 26.5 % | 🟢 11.7 % | 25.1 % | 🔴 122 470 € | 🟢 10 040 € | 🔴 132 510 € |
| LogisticRegression (default) | 🟢 0.647 | 🟢 0.628 | 🟢 0.63 | 🟢 0.519 | 🟢 18.5 % | 🔴 18.6 % | 43.2 % | 🟢 63 340 € | 🔴 17 300 € | 🟢 80 640 € |
| RandomForestClassifier (default) | 🔴 0.575 | 🔴 0.55 | 0.475 | 0.426 | 26.0 % | 15.9 % | 32.5 % | 89 050 € | 12 980 € | 102 030 € |

## Scénario `s3`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 26.6 % | 🔴 102 020 € | 🟢 10 640 € | 🔴 112 660 € |
| LogisticRegression (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 60.1 % | 🟢 44 760 € | 🔴 24 020 € | 🟢 68 780 € |
| RandomForestClassifier (default) | 🟢 0.652 | 🟢 0.635 | 🟢 0.66 | 🟢 0.542 | 🟢 19.1 % | 🟢 18.7 % | 57.6 % | 51 080 € | 23 040 € | 74 120 € |

## Scénario `s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 🟢 0.541 | 🟢 0.504 | 🔴 0.29 | 🔴 0.376 | 🟢 16.0 % | 🟢 2.7 % | 17.3 % | 🔴 150 590 € | ⭐🟢 6 940 € | 🔴 157 530 € |
| LogisticRegression (default) | 🔴 0.432 | 🔴 0.422 | 🟢 0.619 | 0.421 | 🔴 18.5 % | 🔴 17.1 % | 55.2 % | 🟢 70 250 € | 🔴 22 080 € | 🟢 92 330 € |
| RandomForestClassifier (default) | 0.481 | 0.475 | 0.577 | 🟢 0.449 | 16.6 % | 11.6 % | 45.8 % | 80 600 € | 18 300 € | 98 900 € |

## Scénario `s4-age-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | 0.544 | 0.521 | 🔴 0.381 | 0.431 | 16.9 % | 🟢 5.3 % | 18.9 % | 🔴 140 140 € | 🟢 7 560 € | 🔴 147 700 € |
| LogisticRegression (default) | 🔴 0.455 | 🔴 0.448 | 🟢 0.547 | 🔴 0.404 | 🔴 17.7 % | 🔴 15.2 % | 44.5 % | 🟢 88 840 € | 🔴 17 780 € | 🟢 106 620 € |
| RandomForestClassifier (default) | 🟢 0.549 | 🟢 0.539 | 0.494 | 🟢 0.491 | 🟢 15.5 % | 7.2 % | 29.0 % | 108 000 € | 11 620 € | 119 620 € |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced) | 0.644 | 0.622 | 0.508 | 0.511 | 10.5 % | 4.5 % | 23.6 % | 101 410 € | 9 440 € | 110 850 € |
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.662 | 0.641 | 0.547 | 0.544 | 9.4 % | 4.9 % | 26.0 % | 94 920 € | 10 380 € | 105 300 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 0.645 | 0.625 | 0.533 | 0.526 | 8.8 % | 5.2 % | 24.6 % | 97 850 € | 9 860 € | 107 710 € |
| HistGradientBoostingClassifier (default) | 0.658 | 0.632 | 🔴 0.467 | 0.525 | 9.9 % | 3.5 % | 17.4 % | 🔴 114 700 € | 🟢 6 960 € | 🔴 121 660 € |
| LogisticRegression (C=0.1) | 0.547 | 0.536 | 0.652 | 0.477 | 14.1 % | 12.6 % | 44.5 % | 74 680 € | 17 800 € | 92 480 € |
| LogisticRegression (C=10) | 0.532 | 0.519 | 0.55 | 🔴 0.425 | 15.5 % | 11.3 % | 36.5 % | 93 830 € | 14 620 € | 108 450 € |
| LogisticRegression (class_weight={0:1,1:1,2:3}) | 🔴 0.5 | 🔴 0.495 | 🟢 0.685 | 0.432 | 12.2 % | 🔴 17.8 % | 51.1 % | 62 500 € | 20 460 € | 82 960 € |
| LogisticRegression (default) | 0.54 | 0.526 | 0.566 | 0.436 | 14.9 % | 11.2 % | 39.1 % | 86 930 € | 15 620 € | 102 550 € |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | 0.693 | 0.674 | 0.561 | 0.589 | 9.7 % | ⭐🟢 2.5 % | 26.9 % | 86 760 € | 10 760 € | 97 520 € |
| RandomForestClassifier (default) | 0.69 | 0.674 | 0.569 | 0.601 | 9.4 % | ⭐🟢 2.5 % | 25.2 % | 87 900 € | 10 060 € | 97 960 € |
| RandomForestClassifier (max_depth=10) | 0.632 | 0.619 | 0.594 | 0.573 | 🔴 15.7 % | 3.7 % | 60.9 % | 🟢 50 620 € | 🔴 24 360 € | 🟢 74 980 € |
| RandomForestClassifier (min_samples_leaf=5) | 0.628 | 0.611 | 0.622 | 0.52 | 11.9 % | 7.2 % | 43.1 % | 67 940 € | 17 260 € | 85 200 € |
| RandomForestClassifier (n_estimators=300) | 🟢 0.698 | 🟢 0.68 | 0.561 | 🟢 0.601 | ⭐🟢 8.3 % | 2.7 % | 24.1 % | 87 700 € | 9 660 € | 97 360 € |
