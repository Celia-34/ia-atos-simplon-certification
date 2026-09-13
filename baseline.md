# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même). Un tableau par scénario, pour comparer les modèles entre eux à features constantes.

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (comparaison entre modèles, pour ce scénario uniquement).

## Scénario `s2`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.43 | 🟢 0.41 | 🟢 0.347 | 🟢 0.305 | 🟢 34.7 % | 🟢 16.0 % |

## Scénario `s3`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.63 | 🟢 0.615 | 🟢 0.639 | 🟢 0.526 | 🟢 23.6 % | 🟢 18.7 % |

## Scénario `s4-age-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.432 | 🟢 0.416 | 🟢 0.361 | 🟢 0.34 | 🟢 29.2 % | 🟢 12.7 % |

## Scénario `s4-age-dip`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.46 | 🟢 0.457 | 🟢 0.597 | 🟢 0.446 | 🟢 18.1 % | 🟢 17.3 % |

## Scénario `s4-age-dip-anc`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.498 | 🟢 0.481 | 🟢 0.431 | 🟢 0.395 | 🟢 18.1 % | 🟢 10.0 % |

## Scénario `s4-age-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.555 | 🟢 0.548 | 🟢 0.5 | 🟢 0.514 | 🟢 16.7 % | 🟢 7.3 % |

## Scénario `s4-all`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.652 | 🟢 0.633 | 🟢 0.514 | 🟢 0.548 | 🟢 11.1 % | 🟢 4.0 % |

## Scénario `s4-anc`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.412 | 🟢 0.399 | 🟢 0.403 | 🟢 0.326 | 🟢 26.4 % | 🟢 25.3 % |

## Scénario `s4-dip-anc-dep`

| Modèle | Accuracy globale | F1-score macro | Recall classe 2 | F1-score classe 2 (minoritaire) | Matr. confusion : Taux erreur grave (2→0) | Matr. confusion : Taux erreur (0→2) |
|---|---|---|---|---|---|---|
| `RandomForestClassifier` de référence pour la baseline (§4.2, pas encore le modèle retenu — cf. §5) | 🟢 0.432 | 🟢 0.425 | 🟢 0.431 | 🟢 0.383 | 🟢 22.2 % | 🟢 13.3 % |
