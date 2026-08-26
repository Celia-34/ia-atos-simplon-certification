# Benchmark des scénarios × modèles — métriques §1.4

Généré automatiquement depuis `notebooks/certification-cas-usage.ipynb` (§5.2). Chaque scénario est rejoué sur chacun des modèles candidats (métriques calculées par `src/metrics.py`, qui n'entraîne aucun modèle lui-même).

Légende : 🟢 meilleure valeur de la colonne · 🔴 pire valeur de la colonne (sur l'ensemble scénarios × modèles).

| Modèle | Scénario | Accuracy | F1 macro | Recall classe 2 | F1 classe 2 | Taux erreur grave (2→0) | Taux erreur (0→2) |
|---|---|---|---|---|---|---|---|
| HistGradientBoostingClassifier (default) | s1 | 0.607 | 0.573 | 0.376 | 0.435 | 12.4 % | 3.7 % |
| HistGradientBoostingClassifier (default) | s2 | 0.456 | 0.401 | 0.171 | 0.213 | 28.7 % | 8.0 % |
| HistGradientBoostingClassifier (default) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| HistGradientBoostingClassifier (default) | s4a | 0.538 | 0.515 | 0.37 | 0.421 | 15.5 % | 5.2 % |
| HistGradientBoostingClassifier (default) | s4b | 0.462 | 0.422 | 0.232 | 0.275 | 22.7 % | 7.2 % |
| HistGradientBoostingClassifier (default) | s4c | 0.454 | 0.419 | 0.249 | 0.286 | 23.5 % | 7.2 % |
| HistGradientBoostingClassifier (default) | s4d | 0.532 | 0.512 | 0.39 | 0.433 | 15.5 % | 5.5 % |
| HistGradientBoostingClassifier (default) | s4e | 0.4 | 0.327 | 0.097 | 0.151 | 27.9 % | 2.9 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s1 | 0.601 | 0.568 | 0.378 | 0.435 | 13.0 % | 3.9 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s2 | 0.459 | 0.408 | 0.188 | 0.226 | 28.5 % | 8.3 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s4a | 0.531 | 0.507 | 0.37 | 0.409 | 16.6 % | 6.5 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s4b | 0.457 | 0.417 | 0.232 | 0.273 | 24.6 % | 7.9 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s4c | 0.442 | 0.408 | 0.246 | 0.273 | 23.2 % | 8.3 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s4d | 0.529 | 0.509 | 0.392 | 0.425 | 16.3 % | 6.3 % |
| HistGradientBoostingClassifier (learning_rate=0.05, max_iter=300) | s4e | 0.398 | 0.328 | 0.099 | 0.156 | 28.7 % | 2.8 % |
| HistGradientBoostingClassifier (max_depth=5) | s1 | 🟢 0.656 | 0.615 | 0.373 | 0.464 | 🟢 9.9 % | 2.5 % |
| HistGradientBoostingClassifier (max_depth=5) | s2 | 0.481 | 0.41 | 0.13 | 0.195 | 27.3 % | 2.9 % |
| HistGradientBoostingClassifier (max_depth=5) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| HistGradientBoostingClassifier (max_depth=5) | s4a | 0.584 | 0.56 | 0.37 | 0.474 | 16.0 % | 2.3 % |
| HistGradientBoostingClassifier (max_depth=5) | s4b | 0.487 | 0.436 | 0.21 | 0.273 | 17.4 % | 4.0 % |
| HistGradientBoostingClassifier (max_depth=5) | s4c | 0.467 | 0.423 | 0.204 | 0.267 | 23.2 % | 3.9 % |
| HistGradientBoostingClassifier (max_depth=5) | s4d | 0.57 | 0.552 | 0.392 | 0.488 | 14.9 % | 3.2 % |
| HistGradientBoostingClassifier (max_depth=5) | s4e | 0.416 | 0.326 | 🔴 0.088 | 🔴 0.145 | 24.6 % | 🟢 1.9 % |
| LogisticRegression (C=0.1) | s1 | 0.541 | 0.53 | 0.61 | 0.467 | 14.1 % | 9.2 % |
| LogisticRegression (C=0.1) | s2 | 0.422 | 0.406 | 0.395 | 0.292 | 30.9 % | 25.0 % |
| LogisticRegression (C=0.1) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| LogisticRegression (C=0.1) | s4a | 0.466 | 0.46 | 0.569 | 0.435 | 18.8 % | 11.9 % |
| LogisticRegression (C=0.1) | s4b | 0.462 | 0.456 | 0.494 | 0.416 | 19.6 % | 10.0 % |
| LogisticRegression (C=0.1) | s4c | 0.388 | 0.38 | 0.58 | 0.38 | 26.5 % | 23.6 % |
| LogisticRegression (C=0.1) | s4d | 0.473 | 0.469 | 0.586 | 0.453 | 18.2 % | 10.5 % |
| LogisticRegression (C=0.1) | s4e | 0.324 | 🔴 0.271 | 0.37 | 0.259 | 🔴 59.4 % | 32.2 % |
| LogisticRegression (C=10) | s1 | 0.521 | 0.508 | 0.536 | 0.421 | 14.9 % | 12.0 % |
| LogisticRegression (C=10) | s2 | 0.417 | 0.4 | 0.401 | 0.289 | 32.0 % | 26.2 % |
| LogisticRegression (C=10) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| LogisticRegression (C=10) | s4a | 0.46 | 0.454 | 0.533 | 0.412 | 18.5 % | 12.8 % |
| LogisticRegression (C=10) | s4b | 0.446 | 0.439 | 0.492 | 0.392 | 20.4 % | 14.0 % |
| LogisticRegression (C=10) | s4c | 0.383 | 0.379 | 0.489 | 0.344 | 21.3 % | 23.0 % |
| LogisticRegression (C=10) | s4d | 0.474 | 0.471 | 0.586 | 0.455 | 18.0 % | 10.3 % |
| LogisticRegression (C=10) | s4e | 0.324 | 0.273 | 0.37 | 0.259 | 🔴 59.4 % | 32.2 % |
| LogisticRegression (default) | s1 | 0.526 | 0.514 | 0.561 | 0.438 | 14.1 % | 11.6 % |
| LogisticRegression (default) | s2 | 0.418 | 0.402 | 0.401 | 0.291 | 32.3 % | 26.0 % |
| LogisticRegression (default) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| LogisticRegression (default) | s4a | 0.463 | 0.457 | 0.547 | 0.419 | 18.2 % | 12.6 % |
| LogisticRegression (default) | s4b | 0.452 | 0.445 | 0.503 | 0.402 | 20.2 % | 13.4 % |
| LogisticRegression (default) | s4c | 0.386 | 0.382 | 0.508 | 0.354 | 22.1 % | 23.0 % |
| LogisticRegression (default) | s4d | 0.474 | 0.471 | 0.586 | 0.455 | 18.0 % | 10.3 % |
| LogisticRegression (default) | s4e | 0.324 | 0.273 | 0.37 | 0.259 | 🔴 59.4 % | 32.2 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s1 | 0.636 | 0.617 | 0.53 | 0.518 | 🟢 9.9 % | 3.9 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s2 | 0.394 | 0.369 | 0.276 | 0.241 | 28.7 % | 18.4 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s3 | 0.64 | 0.623 | 0.669 | 0.519 | 18.2 % | 22.0 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s4a | 0.542 | 0.534 | 0.522 | 0.493 | 14.1 % | 7.9 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s4b | 0.428 | 0.415 | 0.39 | 0.348 | 21.3 % | 14.2 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s4c | 0.43 | 0.419 | 0.414 | 0.361 | 21.0 % | 13.5 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s4d | 0.501 | 0.49 | 0.478 | 0.422 | 15.2 % | 11.5 % |
| RandomForestClassifier (class_weight={0:1,1:1,2:3}) | s4e | 🔴 0.278 | 0.273 | 0.503 | 0.265 | 16.6 % | 🔴 50.3 % |
| RandomForestClassifier (default) | s1 | 0.642 | 0.616 | 0.481 | 0.501 | 11.3 % | 4.4 % |
| RandomForestClassifier (default) | s2 | 0.396 | 0.371 | 0.271 | 0.246 | 30.7 % | 16.8 % |
| RandomForestClassifier (default) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| RandomForestClassifier (default) | s4a | 0.548 | 0.538 | 0.489 | 0.492 | 16.0 % | 7.2 % |
| RandomForestClassifier (default) | s4b | 0.432 | 0.417 | 0.367 | 0.346 | 23.5 % | 12.6 % |
| RandomForestClassifier (default) | s4c | 0.438 | 0.423 | 0.384 | 0.343 | 26.2 % | 12.7 % |
| RandomForestClassifier (default) | s4d | 0.497 | 0.486 | 0.464 | 0.422 | 15.7 % | 10.3 % |
| RandomForestClassifier (default) | s4e | 0.344 | 0.33 | 0.307 | 0.243 | 36.5 % | 26.3 % |
| RandomForestClassifier (max_depth=10) | s1 | 0.568 | 0.544 | 0.591 | 0.48 | 16.3 % | 7.6 % |
| RandomForestClassifier (max_depth=10) | s2 | 0.424 | 0.395 | 0.271 | 0.26 | 32.6 % | 13.8 % |
| RandomForestClassifier (max_depth=10) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| RandomForestClassifier (max_depth=10) | s4a | 0.516 | 0.495 | 0.599 | 0.477 | 19.6 % | 9.1 % |
| RandomForestClassifier (max_depth=10) | s4b | 0.466 | 0.464 | 0.528 | 0.444 | 18.8 % | 9.1 % |
| RandomForestClassifier (max_depth=10) | s4c | 0.458 | 0.42 | 0.591 | 0.45 | 32.0 % | 12.1 % |
| RandomForestClassifier (max_depth=10) | s4d | 0.529 | 0.514 | 0.483 | 0.453 | 19.3 % | 7.9 % |
| RandomForestClassifier (max_depth=10) | s4e | 0.346 | 0.33 | 0.29 | 0.238 | 36.5 % | 24.8 % |
| RandomForestClassifier (min_samples_leaf=5) | s1 | 0.56 | 0.538 | 0.655 | 0.479 | 16.0 % | 9.7 % |
| RandomForestClassifier (min_samples_leaf=5) | s2 | 0.438 | 0.422 | 0.417 | 0.323 | 29.0 % | 20.8 % |
| RandomForestClassifier (min_samples_leaf=5) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| RandomForestClassifier (min_samples_leaf=5) | s4a | 0.477 | 0.441 | 🟢 0.677 | 0.467 | 21.0 % | 11.7 % |
| RandomForestClassifier (min_samples_leaf=5) | s4b | 0.468 | 0.465 | 0.533 | 0.438 | 18.0 % | 10.5 % |
| RandomForestClassifier (min_samples_leaf=5) | s4c | 0.45 | 0.42 | 0.624 | 0.441 | 26.2 % | 13.9 % |
| RandomForestClassifier (min_samples_leaf=5) | s4d | 0.536 | 0.526 | 0.525 | 0.476 | 16.6 % | 8.1 % |
| RandomForestClassifier (min_samples_leaf=5) | s4e | 0.336 | 0.323 | 0.304 | 0.235 | 37.6 % | 27.6 % |
| RandomForestClassifier (n_estimators=300) | s1 | 0.641 | 0.617 | 0.486 | 0.505 | 10.2 % | 4.3 % |
| RandomForestClassifier (n_estimators=300) | s2 | 0.4 | 0.375 | 0.279 | 0.254 | 28.7 % | 17.0 % |
| RandomForestClassifier (n_estimators=300) | s3 | 0.652 | 🟢 0.635 | 0.66 | 🟢 0.542 | 19.1 % | 18.7 % |
| RandomForestClassifier (n_estimators=300) | s4a | 0.553 | 0.543 | 0.5 | 0.498 | 16.0 % | 7.1 % |
| RandomForestClassifier (n_estimators=300) | s4b | 0.428 | 0.413 | 0.359 | 0.339 | 24.6 % | 12.6 % |
| RandomForestClassifier (n_estimators=300) | s4c | 0.442 | 0.425 | 0.381 | 0.342 | 25.1 % | 12.4 % |
| RandomForestClassifier (n_estimators=300) | s4d | 0.498 | 0.485 | 0.459 | 0.417 | 16.9 % | 10.5 % |
| RandomForestClassifier (n_estimators=300) | s4e | 0.345 | 0.331 | 0.304 | 0.242 | 36.7 % | 26.3 % |
