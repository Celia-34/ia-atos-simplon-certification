# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.692 | 0.683 | 0.625 | 0.638 | 🟢 8.3 % | 3.3 % | 🟢 0.806 | 1.582 | 🔴 19.699 | 🔴 26.093 | 24.1 % | ⭐🟢 71 710 € | 🔴 9 640 € | ⭐🟢 81 350 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.69 | 🔴 0.671 | 🔴 0.556 | 🔴 0.584 | 🔴 12.5 % | ⭐🟢 2.7 % | 1.057 | 🔴 2.178 | 19.379 | 26.015 | 23.1 % | 🔴 80 840 € | ⭐🟢 9 240 € | 🔴 90 080 € |
| RandomForestClassifier (n_estimators=300, class_weight=balanced) | ⭐🟢 0.712 | ⭐🟢 0.703 | ⭐🟢 0.681 | ⭐🟢 0.653 | 9.7 % | 🔴 5.3 % | 🔴 27.505 | 🟢 1.455 | ⭐🟢 18.132 | 🟢 25.759 | nan % | nan € | nan € | nan € |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.64 | 0.615 | 🔴 0.486 | 0.496 | 6.9 % | 🔴 4.7 % | ⭐🟢 0.741 | 1.733 | 🔴 21.607 | 🔴 34.931 | 26.0 % | 🟢 94 920 € | 🔴 10 380 € | 🟢 105 300 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.638 | 🔴 0.612 | 🔴 0.486 | 🔴 0.493 | 🔴 9.7 % | 🔴 4.7 % | 1.055 | 🔴 3.046 | 20.735 | 29.266 | 24.6 % | 🔴 97 850 € | 🟢 9 860 € | 🔴 107 710 € |
| RandomForestClassifier (n_estimators=300, class_weight=balanced) | 🟢 0.692 | 🟢 0.67 | 🟢 0.514 | 🟢 0.574 | ⭐🟢 4.2 % | 🟢 3.3 % | 🔴 29.194 | ⭐🟢 1.259 | 🟢 18.947 | ⭐🟢 25.169 | nan % | nan € | nan € | nan € |
