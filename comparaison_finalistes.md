# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement) · ⭐ meilleure valeur de la colonne tous scénarios × modèles confondus.

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🟢 0.682 | 🟢 0.67 | ⭐🟢 0.625 | ⭐🟢 0.608 | 🟢 9.7 % | 🟢 5.3 % | 21.1 % | 🔴 75 620 € | 🟢 6 740 € | 🔴 82 360 € | 🟢 1.064 | 🔴 6.171 | 🔴 25.252 | 🔴 40.169 |
| RandomForestClassifier (n_estimators=300) | 🔴 0.678 | 🔴 0.661 | ⭐🟢 0.625 | 🔴 0.577 | 🔴 11.1 % | 🔴 10.0 % | 28.4 % | ⭐🟢 49 640 € | 🔴 9 080 € | ⭐🟢 58 720 € | 🔴 28.393 | ⭐🟢 1.247 | 🟢 23.972 | 🟢 34.207 |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) | Part dossiers en alerte (validation manuelle) | Coût erreurs résiduelles (€) | Coût revues manuelles (€) | Coût métier total (€) | Taille modèle (Mo) | Temps de fit (s) | Latence predict p50 (ms) | Latence predict p95 (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (class_weight={0:1,1:1,2:3}) | 🔴 0.638 | 🔴 0.612 | 🔴 0.486 | 🔴 0.493 | 🔴 9.7 % | 🔴 4.7 % | 22.9 % | 🔴 90 210 € | 🔴 7 340 € | 🔴 97 550 € | ⭐🟢 1.055 | 🔴 2.068 | ⭐🟢 19.943 | ⭐🟢 31.087 |
| RandomForestClassifier (n_estimators=300) | ⭐🟢 0.692 | ⭐🟢 0.67 | 🟢 0.514 | 🟢 0.574 | ⭐🟢 4.2 % | ⭐🟢 3.3 % | 20.7 % | 🟢 78 680 € | ⭐🟢 6 640 € | 🟢 85 320 € | 🔴 29.194 | 🟢 1.473 | 🔴 25.543 | 🔴 64.012 |
