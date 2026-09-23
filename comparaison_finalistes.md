# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.692 | 0.683 | 0.625 | 0.638 | 🟢 8.3 % | 3.3 % | 🟢 0.806 | ⭐🟢 1.217 | 17.787 | 29.48 | 22.9 % | ⭐🟢 74 810 € | 🔴 9 140 € | ⭐🟢 83 950 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.69 | 🔴 0.671 | 🔴 0.556 | 🔴 0.584 | 🔴 12.5 % | ⭐🟢 2.7 % | 1.057 | 🔴 1.796 | 🟢 16.402 | 🟢 23.537 | 22.4 % | 🔴 82 960 € | ⭐🟢 8 960 € | 🔴 91 920 € |
| RandomForestClassifier (n_estimators=300, class_weight=balanced) | ⭐🟢 0.712 | ⭐🟢 0.703 | ⭐🟢 0.681 | ⭐🟢 0.653 | 9.7 % | 🔴 5.3 % | 🔴 27.505 | 1.769 | 🔴 23.391 | 🔴 54.285 | nan % | nan € | nan € | nan € |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.64 | 0.615 | 🔴 0.486 | 0.496 | 6.9 % | 🔴 4.7 % | ⭐🟢 0.741 | 🟢 1.226 | 16.557 | 25.906 | 23.7 % | 🟢 98 320 € | 🔴 9 480 € | 🟢 107 800 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.638 | 🔴 0.612 | 🔴 0.486 | 🔴 0.493 | 🔴 9.7 % | 🔴 4.7 % | 1.055 | 1.494 | ⭐🟢 16.133 | ⭐🟢 22.243 | 23.0 % | 🔴 100 250 € | 🟢 9 180 € | 🔴 109 430 € |
| RandomForestClassifier (n_estimators=300, class_weight=balanced) | 🟢 0.692 | 🟢 0.67 | 🟢 0.514 | 🟢 0.574 | ⭐🟢 4.2 % | 🟢 3.3 % | 🔴 29.194 | 🔴 1.661 | 🔴 23.475 | 🔴 48.857 | nan % | nan € | nan € | nan € |
