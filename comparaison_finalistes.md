# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.692 | 0.683 | 0.625 | 0.638 | 🟢 8.3 % | 3.3 % | 🟢 0.806 | 🟢 1.265 | 16.484 | 24.056 | 26.0 % | ⭐🟢 69 470 € | 🔴 10 400 € | ⭐🟢 79 870 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.69 | 🔴 0.671 | 🔴 0.556 | 🔴 0.584 | 🔴 12.5 % | ⭐🟢 2.7 % | 1.057 | 1.581 | 🟢 15.947 | 🟢 21.625 | 24.6 % | 🔴 70 680 € | ⭐🟢 9 860 € | 🔴 80 540 € |
| RandomForestClassifier (n_estimators=300, class_weight=balanced) | ⭐🟢 0.712 | ⭐🟢 0.703 | ⭐🟢 0.681 | ⭐🟢 0.653 | 9.7 % | 🔴 5.3 % | 🔴 27.505 | 🔴 1.728 | 🔴 20.828 | 🔴 35.779 | nan % | nan € | nan € | nan € |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight=balanced, max_depth=10) | 0.64 | 0.615 | 🔴 0.486 | 0.496 | 6.9 % | 🔴 4.7 % | ⭐🟢 0.741 | ⭐🟢 0.966 | 16.063 | 23.056 | 28.9 % | 🟢 92 500 € | 🔴 11 580 € | 🟢 104 080 € |
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.638 | 🔴 0.612 | 🔴 0.486 | 🔴 0.493 | 🔴 9.7 % | 🔴 4.7 % | 1.055 | 1.704 | ⭐🟢 15.909 | ⭐🟢 20.806 | 26.7 % | 🔴 95 630 € | 🟢 10 660 € | 🔴 106 290 € |
| RandomForestClassifier (n_estimators=300, class_weight=balanced) | 🟢 0.692 | 🟢 0.67 | 🟢 0.514 | 🟢 0.574 | ⭐🟢 4.2 % | 🟢 3.3 % | 🔴 29.194 | 🔴 2.285 | 🔴 22.54 | 🔴 39.815 | nan % | nan € | nan € | nan € |
