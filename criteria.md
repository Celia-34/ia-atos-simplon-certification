
⚠️ Le risque métier prioritaire identifié en §1.1 est l'**erreur asymétrique** (classer un usager classe 2 — risque de longue durée — en classe 0). C'est cette asymétrie qui doit guider le choix des métriques, pas la seule accuracy globale (peu informative si les classes sont déséquilibrées, ce qui est confirmé par l'EDA : classe 1 = 44,5 %, classe 0 = 37,4 %, classe 2 = 18,1 %).

#### Groupe 1 — Suivi des erreurs et des erreurs graves

Ces critères mesurent la capacité à détecter la classe 2 (recall), à ne pas la confondre avec la classe 0 (matrice de confusion) et à limiter l'impact des erreurs via le fallback et l'équité entre sous-groupes.

| Type | Critère | Description | Cible initiale (client) | Cible révisée après EDA | Justification de la révision |
|---|---|---|---|---|---|
| Métier | Recall classe 2 (risque de longue durée) | Détecte les cas de classe 2 mal classés (faux négatifs), c'est-à-dire les usagers à risque non identifiés comme tels | ≥ 0.75 | ≥ 0.80 | L'EDA identifie une classe 2 minoritaire (18,1 %) et un enjeu humain fort : la priorité est de détecter les personnes à risque, quitte à générer davantage de faux positifs à faire valider par un conseiller. |
| Métier | **Score de la matrice de confusion : % d'erreurs "classe 0 ↔ classe 2"** (= taux d'erreurs "graves", classe 2 prédite en classe 0) | Mesure la confusion entre classes non adjacentes en gravité, en particulier les usagers à risque (classe 2) classés à tort comme sans risque (classe 0) | minimiser en priorité vs erreurs classe 0 ↔ classe 1 | **< 5 % des cas réels de classe 2 prédits en classe 0 (cible métier prioritaire, maintenue** — environ 452 cas de classe 2 dans le dataset, à vérifier sur le jeu de test et par validation croisée) ; suivi séparé du taux classe 0 → classe 2 | Les erreurs entre classes adjacentes sont moins graves. Les deux sens sont reportés séparément car l'erreur 2 → 0 est l'erreur métier prioritaire pour l'accompagnement ; le "taux d'erreurs graves" et cette lecture de la matrice de confusion sont la même métrique (classe 2 → classe 0), fusionnées ici pour éviter la redondance. |
| Modèle | F1-score classe minoritaire | Équilibre précision et recall spécifiquement sur la classe 2, pour éviter qu'un bon recall soit obtenu au prix d'une précision trop faible | ≥ 0.65 | ≥ 0.60 | Seuil réaliste pour la classe 2, qui compte environ 452 observations. Il sera interprété avec le recall classe 2 afin d'éviter une précision insuffisante. |
| Opérationnel | Taux d'abstention (fallback §7.2) | Proportion de prédictions renvoyées à un conseiller humain faute de confiance suffisante, pour éviter de forcer une décision automatique incertaine | < 15 % des prédictions | ≤ 15 % des prédictions | Cible maintenue. Le seuil de confiance sera calibré après validation afin de réduire les erreurs graves tout en gardant un outil utilisable. |
| Éthique | Écart de recall classe 2 entre sous-groupes sensibles (§3.6) | Vérifie que la détection de la classe 2 est aussi bonne pour tous les sous-groupes (âge, diplôme, nationalité, territoire), et pas seulement en moyenne globale | écart < 10 points | écart < 10 points, pour les sous-groupes avec effectif suffisant | Cible maintenue et rendue vérifiable : l'EDA montre des écarts bruts importants selon l'âge, le diplôme, la nationalité et le territoire. Les métriques d'équité seront calculées par sous-groupe, sans utiliser `nationalite_hors_ue` comme feature. |

#### Groupe 2 — Performance globale (incluant la latence)

Ces critères donnent une vue d'ensemble de la qualité des prédictions et de l'utilisabilité du service, sans distinguer la gravité des erreurs par classe ; ils sont complétés, et non remplacés, par le groupe 1.

| Type | Critère | Description | Cible initiale (client) | Cible révisée après EDA | Justification de la révision |
|---|---|---|---|---|---|
| Métier | Accuracy globale | Proportion globale de prédictions correctes, toutes classes confondues | > 80 % | ≥ 70 % | La classe 2 ne représente que 18,1 % des données : une accuracy élevée peut masquer de mauvaises prédictions de cette classe. L'accuracy devient une métrique secondaire, complétée par les métriques du groupe 1. |
| Métier | Taux d'erreur global | Complément de l'accuracy (1 − accuracy), pour exprimer la performance globale sous l'angle du taux d'erreur toléré | < 20 % | ≤ 30 % | Cohérent avec une accuracy minimale de 70 % et avec le compromis recherché en faveur du recall de la classe 2. |
| Modèle | F1-score macro (moyenne à poids égal entre classes) | Donne une vue équilibrée de la performance sur les trois classes, sans laisser la classe majoritaire dominer le score | ≥ 0.70 | ≥ 0.65 | La moyenne non pondérée reste indispensable pour donner le même poids aux trois classes. Le seuil est ajusté au volume de données et à la minorité de la classe 2, sans relâcher le contrôle spécifique de cette classe. |
| Opérationnel | **Temps de réponse API (`/predict`)** | Mesure la rapidité de réponse du service en production, condition d'utilisabilité pour les conseillers | < 200 ms | **À confirmer après déploiement : p95 < 200 ms** | L'EDA ne permet pas de mesurer la latence ; elle sera mesurée sur l'API et le matériel cible. |

Les seuils révisés devront être confirmés après validation croisée sur le train et une unique évaluation sur le jeu de test stratifié. Un modèle satisfaisant l'accuracy mais échouant sur le recall de la classe 2, les erreurs graves ou l'écart d'équité sera écarté.

====
Attention TODO
Aucune métrique à l'étape 4 sur  ces 2 métriques : a voir si on le fait ensuite ou les supprimer :
* Taux d'abstention (fallback §7.2) — absent de §4.3. Le benchmark n'implémente aucun mécanisme de seuil de confiance/rejet à ce stade (les modèles évalués prédisent systématiquement une classe), donc cette métrique ne peut pas encore être mesurée.
* Écart de recall classe 2 entre sous-groupes sensibles (§3.6) — absent de §4.3. Il n'est calculé qu'en amont sur les données brutes (§3.6.1, écarts de taux de classe 2 par sous-groupe), pas sur les prédictions du modèle par sous-groupe.

====

Note :
_ROC-AUC n'est pas retenu car il est conçu pour la classification binaire (ou en one-vs-rest peu lisible en multi-classe) et n'est pas directement interprétable pour arbitrer sur l'erreur asymétrique prioritaire (classe 2 → classe 0). Les métriques choisies (recall/F1 classe 2, taux d'erreur grave) sont plus directement alignées avec le risque métier identifié en §1.1, tandis que ROC-AUC mesurerait un ordonnancement global des probabilités moins actionnable pour ce cas d'usage._

_RMSE, MAE et R² ne sont pas retenus car ce sont des métriques de régression (écart entre une valeur prédite et une valeur continue réelle). Or le problème posé est une classification multi-classe (3 classes discrètes non ordonnées comme des valeurs numériques à proprement parler, même si elles ont un ordre logique de gravité) : il n'y a pas de valeur continue à prédire, donc ces métriques ne s'appliquent pas techniquement au problème._