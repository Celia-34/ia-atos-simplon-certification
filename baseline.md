# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même).

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (sur l'ensemble scénarios × modèles).

| Modèle | Scénario | Accuracy | F1 macro | Recall classe 2 | F1 classe 2 | Taux erreur grave (2→0) | Taux erreur (0→2) |
|---|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s1 | 🟢 0.664 | 0.634 | 0.456 | 0.509 | 🟢 8.9 % | 🟢 2.1 % |
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s2 | 0.374 | 0.352 | 🔴 0.278 | 🔴 0.236 | 32.2 % | 21.4 % |
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s3 | 0.654 | 🟢 0.637 | 🟢 0.644 | 🟢 0.55 | 13.3 % | 17.1 % |
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s4a | 0.616 | 0.592 | 0.489 | 0.471 | 11.1 % | 7.5 % |
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s4b | 0.458 | 0.426 | 0.289 | 0.265 | 27.8 % | 15.5 % |
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s4c | 0.428 | 0.417 | 0.411 | 0.352 | 24.4 % | 12.8 % |
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s4d | 0.528 | 0.511 | 0.456 | 0.425 | 14.4 % | 8.0 % |
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | s4e | 🔴 0.368 | 🔴 0.352 | 0.322 | 0.244 | 🔴 36.7 % | 🔴 29.4 % |
