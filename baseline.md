# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement).

## Scénario `s1`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.664 | 🟢 0.634 | 🟢 0.456 | 🟢 0.509 | 🟢 8.9 % | 🟢 2.1 % |

## Scénario `s2`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.374 | 🟢 0.352 | 🟢 0.278 | 🟢 0.236 | 🟢 32.2 % | 🟢 21.4 % |

## Scénario `s3`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.654 | 🟢 0.637 | 🟢 0.644 | 🟢 0.55 | 🟢 13.3 % | 🟢 17.1 % |

## Scénario `s4-age-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.428 | 🟢 0.417 | 🟢 0.411 | 🟢 0.352 | 🟢 24.4 % | 🟢 12.8 % |

## Scénario `s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.504 | 🟢 0.49 | 🟢 0.544 | 🟢 0.438 | 🟢 15.6 % | 🟢 8.6 % |

## Scénario `s4-age-dip-anc`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.528 | 🟢 0.511 | 🟢 0.456 | 🟢 0.425 | 🟢 14.4 % | 🟢 8.0 % |

## Scénario `s4-age-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.616 | 🟢 0.592 | 🟢 0.489 | 🟢 0.471 | 🟢 11.1 % | 🟢 7.5 % |

## Scénario `s4-anc`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.368 | 🟢 0.352 | 🟢 0.322 | 🟢 0.244 | 🟢 36.7 % | 🟢 29.4 % |

## Scénario `s4-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.458 | 🟢 0.426 | 🟢 0.289 | 🟢 0.265 | 🟢 27.8 % | 🟢 15.5 % |
