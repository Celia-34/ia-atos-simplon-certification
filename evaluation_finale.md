# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même).

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (sur l'ensemble scénarios × modèles).

| Modèle | Scénario | Accuracy | F1 macro | Recall classe 2 | F1 classe 2 | Taux erreur grave (2→0) | Taux erreur (0→2) |
|---|---|---|---|---|---|---|---|
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) — évaluation finale test set | s1 | 🟢 0.652 | 🟢 0.626 | 🟢 0.489 | 🟢 0.503 | 🟢 7.8 % | 🟢 2.7 % |
