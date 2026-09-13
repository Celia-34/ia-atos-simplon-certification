# Synthèse des décisions — Étapes 1 à 5

> Ce document consolide les décisions importantes prises pendant les 5 premières phases du cas d'usage (Cadrer, Explorer, Préparer, Modéliser & comparer, Arbitrer), telles que documentées dans le notebook (`journal-de-bord.ipynb`, canvas), `criteria.md`, `scenarii.md` et `baseline.md`.

---

## Étape 1 — Cadrer

### Nature de la tâche ML

**Choix** : Classification supervisée multi-classe (3 classes : 0 = retour rapide <6 mois, 1 = retour moyen 6-12 mois, 2 = risque de longue durée >12 mois), sur données hybrides (tabulaires + texte libre).

**Justification** : Besoin métier de l'agence de classer le délai potentiel de retour à l'emploi d'un usager.

### Critère de succès prioritaire (métrique dominante)

**Choix** : Ne pas retenir l'accuracy globale comme critère principal, mais privilégier la limitation des erreurs asymétriques graves (classe 2 prédite en classe 0) : recall classe 2 et taux d'erreur "0↔2".

**Justification** : Classer à tort un usager à risque de longue durée en retour rapide le prive d'un accompagnement renforcé — impact humain et financier direct.

### Variables à risque identifiées

**Choix** : Identification de variables à risque : `usager_id`, `age`, `niveau_diplome`, `anciennete_poste_ans`, `code_rome_vise`, `code_insee_commune`, `est_allocataire`, `nationalite_hors_ue`, `synthese_entretien`, chacune associée à un risque spécifique (RGPD, discrimination, proxy).

**Justification** : `nationalite_hors_ue` est une variable sensible explicite (RGPD art. 9) ; `age` est une variable protégée ; `code_insee_commune` est un proxy territorial à haute granularité.

### Cadre réglementaire applicable

**Choix** : Application du RGPD (art. 9, minimisation, base légale à documenter), de l'AI Act (classement probable "haut risque" — Annexe III emploi), et du droit sectoriel (non-discrimination).

**Justification** : Le traitement porte sur des données personnelles/sensibles et le système influence l'accompagnement vers l'emploi des usagers.

### Supervision humaine (principe)

**Choix** : Pas d'automatisation intégrale de la décision ; nécessité d'un fallback / human-in-the-loop (conception détaillée prévue en étape ultérieure).

**Justification** : Art. 22 RGPD (droit à intervention humaine sur décision automatisée) ; risque de responsabilité juridique en cas de préjudice.

---

## Étape 2 — Explorer

### Gestion des doublons

**Choix** : Aucun traitement nécessaire.

**Justification** : Aucun doublon détecté dans le dataset global.

### Gestion des manquants

**Choix** : Conserver les lignes avec manquants pour `age` (122, 4,9 %), `niveau_diplome` (84, 3,4 %) et `est_allocataire` (44, 1,8 %), avec une stratégie d'imputation à définir en préparation ; pour `synthese_entretien` (81 manquants, 3,2 %), possibilité d'écarter ces lignes.

**Justification** : Pour `synthese_entretien`, "seul 81 absent sur 2450 lignes, c'est faible, on pourra donc les écarter" ; pour les autres variables, "on mettra en place une stratégie pour conserver les lignes avec des valeurs manquantes."

### Gestion des valeurs erratiques / aberrantes

**Choix** : Les 126 personnes avec une ancienneté de poste >9 ans (détectées par méthode IQR) sont conservées telles quelles.

**Justification** : "Cela ne constitue pas, du point de vue métier, une valeur aberrante" — ces valeurs sont réalistes malgré leur détection statistique comme outliers.

### Déséquilibre de la variable cible

**Choix** : Constat d'un déséquilibre (classe 1 = 44,5 %, classe 0 = 37,4 %, classe 2 = 18,1 % minoritaire) conduisant à la nécessité d'un split stratifié et de métriques macro/F1 plutôt que l'accuracy seule.

**Justification** : Le déséquilibre "confirme dès maintenant l'usage de métriques macro/F1 plutôt que l'accuracy seule et la nécessité d'un split stratifié."

### Variables sensibles / proxy — orientations préliminaires pour la modélisation

**Choix** : `nationalite_hors_ue` exclue des features (conservée uniquement pour l'audit d'équité) ; `age` et `niveau_diplome` comparés en scénarios avec/sans ; `code_insee_commune` écarté au profit d'une version agrégée par département.

**Justification** : Disparate impact confirmé empiriquement (ratio ×2,46 UE/hors UE ; écart de 32,4 points par tranche d'âge ; écart de 34,2 points par diplôme ; écarts territoriaux de 9,7 % à 39 %).

### Traitement des données textuelles (`synthese_entretien`)

**Choix** : Nettoyage léger, remplacement des manquants par une chaîne vide + indicateur `texte_manquant`, anonymisation (détection téléphone/email), classification zero-shot avec une taxonomie de 9 familles thématiques via CamemBERT (`cmarkea/distilcamembert-base-nli`) exécuté en local.

**Justification** : Exécution locale car "aucune donnée n'est envoyée à un service externe" (protection RGPD) ; approche zero-shot retenue car "les commentaires ne disposent d'aucun label thématique fiable", rendant un fine-tuning supervisé non pertinent.

### Risque de biais encodé dans le texte

**Choix** : Les 9 templates de commentaires sont audités par sous-groupe sensible (nationalité, diplôme, âge) avant usage.

**Justification** : Certaines formulations ("barrière de la langue", "illettrisme numérique") peuvent encoder indirectement des variables sensibles déjà identifiées ; leur usage doit être audité au même titre que les proxys tabulaires.

### Scénarios de données retenus (issus de l'EDA)

**Choix** : Quatre scénarios principaux — S1 (multimodal complet), S2 (sans variables sensibles), S3 (texte seul), S4 (tabulaire seul) — complétés par des sous-scénarios S4a-e (ablation d'un proxy à la fois).

**Justification** : Comparer plusieurs configurations de données pour évaluer le compromis performance / éthique associé à chaque variable (détail dans `scenarii.md`).

---

## Étape 3 — Préparer

### Split train/test

**Choix** : Split 80/20, stratifié selon la cible (`stratify=y`), `random_state=42`.

**Justification** : `stratify=y` conserve la proportion des trois classes dans train et test, notamment la classe 2 qui ne représente que 18,1 % du dataset ; le `random_state` fixe garantit la reproductibilité.

### Ordre split → preprocessing (prévention de la fuite de données)

**Choix** : Le split précède toute transformation ; imputations, vectorisations et encodages sont ajustés (fit) sur le train uniquement.

**Justification** : Éviter la fuite de données ("le train/test split DOIT précéder tout calcul d'imputation/normalisation, sinon fuite de données").

### Exclusion de `nationalite_hors_ue` des features

**Choix** : Variable exclue de toutes les features de tous les scénarios, conservée uniquement pour l'audit d'équité.

**Justification** : Son signal est associé à un risque de discrimination directe (variable sensible explicite, RGPD art. 9).

### Traitement de `code_insee_commune`

**Choix** : Remplacé par le département (2 premiers chiffres) plutôt que le code brut.

**Justification** : Limiter sa sensibilité et sa granularité (haute cardinalité + proxy territorial).

### Détail des 4 scénarios principaux

**Choix** :
- S1 (multimodal complet) : toutes les variables non directement sensibles + TF-IDF du texte concaténé.
- S2 (éthique, sans sensibles) : retrait de `nationalite_hors_ue`, `age`, `niveau_diplome`, `departement`.
- S3 (texte seul) : `synthese_entretien` uniquement, imputation par chaîne vide + TF-IDF.
- S4 (tabulaire seul) : `age`, `niveau_diplome`, `anciennete_poste_ans`, `departement`, imputation par médiane (numériques) / modalité la plus fréquente (catégorielles).

**Justification** : S2 applique les principes de minimisation, non-discrimination et protection des données dès la conception (RGPD/CNIL) ; S3 mesure la robustesse du signal textuel seul ; S4 sert de référence face à S3 pour mesurer le gain apporté par la multimodalité.

### Sous-scénarios S4a-e (ablation de proxies)

**Choix** : S4a (baseline, 3 proxies), S4b (sans âge), S4c (sans diplôme), S4d (sans département), S4e (sans proxies majeurs, seulement ancienneté) — puis renommés d'après les features conservées (ex. S4a → S4-age-dip-anc-dep), avec ajout d'un S4-age-dip isolant les 2 proxies les plus déterminants.

**Justification** : Isoler l'effet de chaque proxy, sans qu'un signal équivalent contenu dans le texte ne masque son retrait ; un proxy n'est retenu que si son gain de performance est démontré sans dégrader les critères de sécurité et d'équité fixés en étape 1. Le renommage vise la clarté (nommage explicite des features conservées) ; S4-age-dip a été ajouté car âge + diplôme "portent l'essentiel du signal tabulaire" (constat du premier benchmark baseline).

### Modèle utilisé pour la baseline pré-modélisation

**Choix** : `RandomForestClassifier(class_weight="balanced")` utilisé comme référence unique pour comparer les scénarios, non retenu comme modèle final.

**Justification** : Sert uniquement à comparer les scénarios entre eux sur un pied d'égalité, pas à présélectionner un modèle.

### Pipeline générique (ColumnTransformer)

**Choix** : Pipeline reproductible construit avec `Pipeline` + `ColumnTransformer`, via des fonctions dédiées (`src/pipeline_tabulaire.py`, `src/pipeline_texte.py`, `src/pipeline_tabulaire_hybride.py`).

**Justification** : Éviter les transformations one-shot dispersées et garantir la reproductibilité du prétraitement (imputation, encodage, texte).

### Vectorisation du texte

**Choix** : TF-IDF (`TfidfVectorizer(max_features=300, min_df=2)`), ajusté sur le train uniquement.

**Justification** : Non détaillée explicitement dans les documents au-delà de l'usage standard en NLP pour le scénario S3 — choix des hyperparamètres non justifié en détail dans les sources disponibles.

### Assertions qualité avant modélisation

**Choix** : Vérifications automatiques (`assert`) : pas de manquants résiduels dans la cible, pas de doublons, split complet et sans intersection train/test, stratification respectée à ±3 points pour la classe 2, matrices alignées et sans NaN.

**Justification** : Constituer une première ligne de tests automatisés ("Si l'une d'elles casse, ne la commente pas. Cherche pourquoi avant de modéliser.").

---

## Étape 4 — Modéliser & comparer

### Famille de modèles retenue

**Choix** : Seul le ML classique (scikit-learn) est retenu ; Deep Learning, SLM local, LLM+RAG et architecture agentique sont écartés.

**Justification** : Les données sont tabulaires et textuelles déjà vectorisées, le volume est modeste (2000 lignes de train) et l'explicabilité est une contrainte forte pour une décision administrative. Le Deep Learning est écarté par manque de volume et de gain démontré ; les approches LLM/agentiques sont jugées hors scope car la tâche ne nécessite ni génération de texte, ni recherche documentaire, ni orchestration multi-étapes.

### Modèles candidats sélectionnés

**Choix** : `LogisticRegression` (class_weight="balanced"), `RandomForestClassifier` (class_weight="balanced"), `HistGradientBoostingClassifier`.

**Justification** : LogisticRegression = baseline rapide, explicable, gère nativement le déséquilibre ; RandomForest = robuste aux features hétérogènes, peu de tuning nécessaire ; HistGradientBoosting = souvent la meilleure performance brute sur données tabulaires.

### Validation croisée stratifiée

**Choix** : `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.

**Justification** : Permet d'avoir des folds représentatifs de la distribution des classes, garantissant la robustesse de l'évaluation face au déséquilibre de la cible.

### Règle du test set

**Choix** : Le jeu de test n'est utilisé qu'une seule fois, à la toute fin, pour l'évaluation finale du modèle retenu.

**Justification** : Éviter tout leakage ou sur-optimisation sur le test ("le test set ne sert qu'à la fin").

### Gestion du déséquilibre des classes

**Choix** : `class_weight="balanced"` par défaut sur les modèles candidats, puis test d'un poids ciblé `class_weight={0:1,1:1,2:3}` pour RandomForest.

**Justification** : "balanced" équilibre selon la fréquence des classes, mais ne cible pas spécifiquement l'erreur 2→0 ; le poids {0:1,1:1,2:3} vise à pénaliser 3 fois plus fort les erreurs sur la classe 2, dans l'objectif de réduire spécifiquement le taux d'erreur grave.

### Élimination de HistGradientBoostingClassifier

**Choix** : HGB écarté après le benchmark initial, non rejoué avec les hyperparamètres affinés.

**Justification** : Sur la métrique prioritaire (recall classe 2), il est nettement dominé par LogisticRegression et RandomForestClassifier sur chaque scénario où les modèles se différencient, sans compensation suffisante sur le taux d'erreur grave (recall classe 2 systématiquement le plus faible, ex. 0,376 sur S1, 0,293 sur S4-age-dip).

### Métriques retenues et priorisation

**Choix** : F1 macro, recall classe 2, F1 classe 2, taux d'erreur grave 2→0 (prioritaire), taux d'erreur 0→2 ; accuracy reléguée en indicateur secondaire ; ROC-AUC et métriques de régression (RMSE/MAE/R²) explicitement exclues.

**Justification** : L'accuracy peut être trompeuse sur une cible déséquilibrée (ex. S3 a la meilleure accuracy 0,652 mais un taux d'erreur grave de 19,1 %, très au-dessus du seuil de 5 % visé). ROC-AUC n'est pas directement interprétable pour arbitrer sur l'erreur asymétrique prioritaire ; RMSE/MAE/R² sont des métriques de régression, non applicables à une classification multi-classe.

### Hyperparamètres testés

**Choix** : LogisticRegression → C=0,1 et C=10 (vs défaut 1,0) ; RandomForest → n_estimators=300, max_depth=10, class_weight={0:1,1:1,2:3}, min_samples_leaf=5.

**Justification** : Chaque hyperparamètre est justifié individuellement — ex. `class_weight` ciblé pour réduire spécifiquement le taux d'erreur grave, au prix probable d'un F1 macro plus faible ; `min_samples_leaf=5` testé pour vérifier si des feuilles moins spécifiques réduisent le taux d'erreur grave sans trop dégrader le F1 macro.

### Choix du scénario / modèle final

> ⚠️ **Correction post-hoc (cf. Étape 5 ci-dessous)** : les choix décrits ci-dessous ont été révisés après la découverte que le scénario "S1" était mal implémenté (tabulaire seul au lieu de multimodal). Voir la section "Correction du scénario S1" en Étape 5 pour le détail de la correction et de la nouvelle décision finale.

**Choix** : Scénario **S4-all** (tabulaire seul, 6 variables) avec `RandomForestClassifier(class_weight="balanced")` (configuration par défaut).

**Justification** : Cette configuration obtient le meilleur taux d'erreur grave de tout le benchmark corrigé (9,4 % en validation croisée, 10,0 % sur le test set), le critère explicitement désigné comme "risque métier prioritaire" par `criteria.md`. Le scénario S1 hybride (vrai multimodal, tabulaire + texte, cf. correction ci-dessous) obtient un meilleur recall classe 2 (jusqu'à 0,674-0,696) et un meilleur F1 macro (jusqu'à 0,661-0,667, seul à dépasser la cible de 0,65), mais un taux d'erreur grave supérieur (13,8 % au mieux) : le choix de S4-all privilégie donc la sécurité (moins d'erreurs graves), conformément à la priorité explicite du cahier des charges, au prix d'une détection moins complète des cas à risque (recall test = 0,456, loin de la cible de 0,80).

### Courbes d'apprentissage / early stopping

**Choix** : Tracé des courbes d'apprentissage (train vs CV) pour RandomForest et HGB (early stopping natif activé sur HGB, `n_iter_no_change=3`, `validation_fraction=0.2`) ; LogisticRegression exclu de cette analyse.

**Justification** : Diagnostiquer le sous/sur-apprentissage. LogisticRegression est exclu car son solveur convexe n'a pas de notion d'itération qui overfit ; RandomForest n'a pas d'early stopping natif car les arbres ne sont pas ajoutés séquentiellement.

### Persistance du modèle final

**Choix** : Pipeline complet (préprocesseur + modèle) sauvegardé via joblib dans `models/modele_final_s4-all_random_forest.joblib` (renommé après correction ; l'ancien fichier `modele_final_s1_random_forest_class_weight.joblib`, mal étiqueté, a été supprimé).

**Justification** : Pour un usage ultérieur (API de service en phase d'industrialisation). Le renommage reflète le scénario réellement utilisé (S4-all, tabulaire seul), après correction du bug documenté en Étape 5.

### Constat sur la cible de recall classe 2

**Choix** : Le recall classe 2 obtenu (0,456 sur le test set, 0,517 en CV) reste très en-deçà de la cible de 0,80 fixée dans `criteria.md` ; ce point est reconnu comme une limite assumée du modèle.

**Justification** : Le choix du scénario S4-all (cf. correction en Étape 5) privilégie explicitement la réduction du taux d'erreur grave au détriment du recall classe 2 — un arbitrage documenté, pas un défaut non maîtrisé.

### Points restant à traiter avant mise en production

**Choix** : L'audit d'équité par sous-groupe (recall classe 2 par nationalité, âge, diplôme) reste à mener ; seule la famille ML classique a été testée ; pas de recherche d'hyperparamètres exhaustive (GridSearch).

**Justification** : Explicitement listé comme limite à traiter avant toute mise en production.

---

## Étape 5 — Arbitrer

> **Constat préalable** : dans le canvas (`notebooks/certification-cas-usage.ipynb`), les sections §6 (Analyse des scénarios & arbitrages) et §7 (Interprétation pour la communication client) ont depuis été complétées (voir ci-dessous), après correction du bug décrit dans cette section.

### Correction du scénario S1 (bug découvert et corrigé)

**Choix** : Le scénario **S1**, décrit dans `scenarii.md` comme "approche multimodale complète" (tabulaire + synthèse d'entretien), était implémenté dans `src/pipeline_tabulaire.py` en **tabulaire seul** (sans vectorisation TF-IDF du texte) — un écart entre le plan documenté et le code. Ce bug a été corrigé : `src/pipeline_tabulaire_hybride.py` a été généralisé (paramètre `tabular_scenario`) pour assembler n'importe quel scénario tabulaire avec le texte, et un nouveau scénario **S4-all** a été créé pour désigner explicitement l'ancienne variante tabulaire-seule (les 6 mêmes variables que S1, sans texte), utilisée pour comparer l'apport réel du texte.

**Justification** : Le code (`src/pipeline_tabulaire.py`, `SCENARIO_FEATURES["s1"]`) ne contenait que des variables tabulaires ; aucune concaténation TF-IDF n'existait pour "s1" avant correction. Ce constat a été fait lors de la rédaction de la section §7 du notebook (analyse de feature importance), où il est apparu que le modèle persisté n'utilisait pas `synthese_entretien` contrairement à sa description.

### Re-benchmark complet après correction

**Choix** : L'ensemble du benchmark (tous scénarios × 3 modèles × hyperparamètres, 5-fold CV stratifié) a été rejoué avec la définition corrigée (S1 = vrai hybride, S4-all = ancien "S1" renommé). Résultat central : le texte améliore de façon cohérente le recall classe 2 et le F1 macro sur les 3 scénarios qui l'intègrent (S1 hybride, S3, S3+S4-age-dip), mais dégrade systématiquement le taux d'erreur grave par rapport à la meilleure option purement tabulaire (S4-all : 9,4 % vs 12,4 % ou plus pour toute configuration avec texte).

**Justification** : Ce n'est pas un artefact isolé mais une tendance reproductible sur l'ensemble du re-benchmark (`benchmark.md` régénéré), ce qui en fait un constat empirique robuste plutôt qu'un simple effet de hasard sur un split particulier.

### Choix final du modèle/scénario (arbitrage tranché avec l'utilisateur)

**Choix** : Scénario **S4-all** (tabulaire seul) avec `RandomForestClassifier(class_weight="balanced")`, configuration par défaut — confirmé comme décision finale du projet après consultation explicite de l'utilisateur sur l'arbitrage révélé par la correction.

**Justification** : Une fois le vrai S1 hybride benchmarké, le compromis s'est avéré être un arbitrage entre deux critères contradictoires de `criteria.md` (taux d'erreur grave "prioritaire" vs F1 macro/recall classe 2, chacun avec sa propre cible), et non un cas où un scénario domine l'autre. Face à ce choix, l'utilisateur a explicitement tranché en faveur de la **sécurité maximale** : retenir S4-all, qui minimise le taux d'erreur grave (9,4 % en CV / 10,0 % sur le test set — le meilleur de tout le benchmark), plutôt que S1 hybride ou S3, qui offrent un meilleur recall/F1 macro mais un taux d'erreur grave 1,2 à 1,9× supérieur. Ce choix est documenté comme un arbitrage assumé, réversible si la priorité métier évolue (cf. notebook §6.3).

**Alternatives documentées et écartées** :
- S1 hybride (`LogisticRegression`, default) : recall 0,674, taux d'erreur grave 13,8 %, F1 macro 0,661 (seul à dépasser la cible de 0,65) — écarté malgré ses meilleures performances globales, car le taux d'erreur grave est jugé prioritaire.
- S3 (texte seul) : recall jusqu'à 0,669, mais taux d'erreur grave 18,2-19,1 % — écarté pour la même raison, à plus forte raison.

### Exclusion des familles GenAI / LLM / agents (repris et confirmé en arbitrage)

**Choix** : Seul le ML classique (scikit-learn) est retenu comme famille de modèles ; Deep Learning, SLM local, LLM+RAG et architecture agentique restent écartés.

**Justification** :
- DL : pas de volume suffisant (2000/500 lignes), explicabilité dégradée pour un gain incertain vs sklearn ; à réévaluer en M6 si le corpus texte grossit.
- SLM local : hors scope, rôle déjà couvert par le zero-shot CamemBERT utilisé en amont pour classifier les commentaires (pas comme modèle final).
- LLM API + RAG : pas de question ouverte sur corpus documentaire, sortie attendue = classe structurée ; enverrait des données socio-démographiques d'usagers à un tiers sans bénéfice pour une classification structurée.
- Architecture agentique : une seule prédiction en sortie, pas d'orchestration multi-étapes ni d'actions, aucun besoin d'orchestration.

### Compromis coût / latence

**Choix** : Aucun chiffrage précis retenu à ce stade pour le modèle final ; seule une appréciation qualitative existe (ML classique = coût "faible" vs DL = "élevé (GPU train)", LLM API+RAG = "élevé (€/token)", architecture agentique = "très élevé").

**Justification** : Non disponible — le tableau §6.1 du notebook renseigne ces colonnes qualitativement, cohérent avec la famille de modèles retenue, mais aucune mesure chiffrée (latence réelle, coût €/1k prédictions) n'a été réalisée. *À instrumenter en production (§8/§9).*

### Explicabilité du modèle

**Choix** : Feature importance native de `RandomForestClassifier` (impureté Gini) calculée en §7.1 du notebook ; aucun calcul SHAP réalisé à ce stade (optionnel dans le canvas).

**Justification** : Donne une première lecture globale des variables les plus influentes (probablement `age`, `niveau_diplome`, `anciennete_poste_ans` d'après les gradients déjà mesurés en §3.6/§3.7), mais ne permet pas d'expliquer une prédiction individuelle.

### Fallback / seuils de décision / human-in-the-loop

**Choix** : Trois leviers tranchés en §7.2 du notebook : seuil de rejet initial proposé à 0,45 (à calibrer), abstention renvoyée en HTTP 200 avec `decision: "a_valider"`, escalade vers le conseiller référent sous 48h ouvrées.

**Justification** : Le principe général (nécessité d'un human-in-the-loop, pas d'automatisation intégrale) avait été acté dès l'étape 1 (art. 22 RGPD, risque de responsabilité juridique). Le recall du modèle retenu (0,456 sur le test set — un cas à risque sur deux non détecté) renforce d'autant la nécessité de ce filet de sécurité humain : ce n'est plus une option mais une condition de déploiement responsable.

*Note distincte* : un seuil de confiance est aussi défini pour la classification thématique des commentaires (NLP, étape 2), mais ne concerne pas le verdict final du modèle de classification du délai de retour à l'emploi.

### Cible de taux d'abstention

**Choix** : Cible fixée à ≤ 15 % des prédictions pour le mécanisme de rejet/abstention (seuil proposé à 0,45 de confiance maximale, à calibrer précisément par le code du notebook §7.2).

**Justification** : "Le seuil de confiance sera calibré après validation afin de réduire les erreurs graves tout en gardant un outil utilisable." Le taux d'abstention réel pour le seuil proposé n'a pas encore été mesuré (calcul disponible dans le code du notebook, à exécuter).

### Analyse des erreurs critiques et audit d'équité

**Choix** : L'audit d'équité par sous-groupe (recall classe 2 par nationalité, âge, diplôme, département) reste à mener, condition préalable à la mise en production ; le code correspondant est écrit en §7.2 du notebook mais pas encore exécuté avec les vraies données.

**Justification** : Les proxies utilisés par le modèle retenu (`age`, `niveau_diplome`, `departement`) sont les mêmes, qu'on choisisse S4-all ou S1 hybride : passer à S1 hybride n'aurait pas réduit ce risque, seulement ajouté un risque supplémentaire non audité (le texte). Le choix de S4-all ne dispense donc pas de cet audit.

### Message client et recommandation finale

**Choix** : Rédigés en §6.2 et §7.3 du notebook, en langage métier, expliquant le choix de S4-all et le compromis face à S1 hybride/S3.

**Justification** : Permettre au client de comprendre l'arbitrage (sécurité vs détection) et ses implications opérationnelles (contrôle humain nécessaire, recall limité).

---

## Note méthodologique

Le fichier `decisions.md` (squelette initial du projet) prévoyait des sections "Gestion des doublons", "Gestion des manquants", "Gestion des valeurs erratiques" et "Préparation" restées vides. Le présent document (`decision.md`) consolide ces décisions à partir du notebook (`journal-de-bord.ipynb`, canvas §1 à §5), de `criteria.md`, `scenarii.md` et `baseline.md`, qui font foi pour le détail des choix et justifications.

Certains éléments n'ont pas de justification textuelle explicite dans les sources disponibles (ex. hyperparamètres TF-IDF `max_features=300`, `min_df=2`) : cela est signalé dans les sections concernées plutôt que d'inventer une justification.
