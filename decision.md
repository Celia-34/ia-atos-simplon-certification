# Synthèse des décisions — Étapes 1 à 4

> Ce document consolide les décisions importantes prises pendant les 4 premières phases du cas d'usage (Cadrer, Explorer, Préparer, Modéliser & comparer), telles que documentées dans le notebook (`journal-de-bord.ipynb`, canvas), `criteria.md`, `scenarii.md` et `baseline.md`.

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

**Choix** : Scénario **S1** (multimodal complet) avec `RandomForestClassifier(class_weight={0:1,1:1,2:3})`.

**Justification** : Cette configuration améliore strictement les deux métriques prioritaires par rapport à `n_estimators=300` seul : recall classe 2 de 0,486 à 0,53 et taux d'erreur grave de 10,2 % à 9,9 %, pour un F1 macro identique (0,617). Le scénario S3 (texte seul) avait un meilleur recall (0,66) mais un taux d'erreur grave bien plus élevé (19,1 % vs 9,9 %) : le choix de S1 privilégie donc la sécurité (moins d'erreurs graves) au prix d'une détection moins complète des cas à risque.

### Courbes d'apprentissage / early stopping

**Choix** : Tracé des courbes d'apprentissage (train vs CV) pour RandomForest et HGB (early stopping natif activé sur HGB, `n_iter_no_change=3`, `validation_fraction=0.2`) ; LogisticRegression exclu de cette analyse.

**Justification** : Diagnostiquer le sous/sur-apprentissage. LogisticRegression est exclu car son solveur convexe n'a pas de notion d'itération qui overfit ; RandomForest n'a pas d'early stopping natif car les arbres ne sont pas ajoutés séquentiellement.

### Persistance du modèle final

**Choix** : Pipeline complet (préprocesseur + modèle) sauvegardé via joblib dans `models/modele_final_s1_random_forest_class_weight.joblib`.

**Justification** : Pour un usage ultérieur (API de service en phase d'industrialisation).

### Constat sur la cible de recall classe 2

**Choix** : Le recall classe 2 obtenu (~0,53) reste en-deçà de la cible de 0,80 fixée dans `criteria.md` ; ce point est reconnu comme une limite du modèle.

**Justification** : Le modèle tabulaire+texte structuré atteint un compromis correct mais insuffisant pour le critère de succès le plus exigeant.

### Points restant à traiter avant mise en production

**Choix** : L'audit d'équité par sous-groupe (recall classe 2 par nationalité, âge, diplôme) reste à mener ; seule la famille ML classique a été testée ; pas de recherche d'hyperparamètres exhaustive (GridSearch).

**Justification** : Explicitement listé comme limite à traiter avant toute mise en production.

---

## Étape 5 — Arbitrer

> **Constat préalable** : dans le canvas (`notebooks/certification-cas-usage.ipynb`), les sections §6 (Analyse des scénarios & arbitrages) et §7 (Interprétation pour la communication client) sont encore largement à l'état de gabarit non rempli (tableau §6.1 avec cellules `…`, placeholders `*[...]*` en §6.2, §6.3, §7.3, §7.4). Le journal de bord (Jour 5) le confirme explicitement : *« Etape 6 et 7 à compléter. Des éléments de l'étape 6 sont déjà dans 5.6 et 5.7. »* Les décisions ci-dessous distinguent donc ce qui est réellement tranché de ce qui reste en attente.

### Choix final du modèle/scénario (cœur de l'arbitrage multi-critères)

**Choix** : Scénario **S1** (multimodal complet) avec `RandomForestClassifier(class_weight={0:1,1:1,2:3})`, repris de l'étape 4 comme verdict d'arbitrage.

**Justification** : Cette configuration améliore strictement les deux métriques prioritaires (recall classe 2 : 0,486→0,53 ; taux d'erreur grave : 10,2 %→9,9 %) pour un F1 macro identique (0,617). S3 (texte seul) avait un meilleur recall (0,66) mais un taux d'erreur grave bien plus élevé (19,1 % vs 9,9 %) : le choix de S1 privilégie donc la sécurité (moins d'erreurs graves) au prix d'une détection moins complète des cas à risque. *Ce compromis, formulé en §5.7, est explicitement renvoyé pour être documenté "en §6" mais n'y a pas encore été formellement repris.*

### Exclusion des familles GenAI / LLM / agents (repris et confirmé en arbitrage)

**Choix** : Seul le ML classique (scikit-learn) est retenu comme famille de modèles ; Deep Learning, SLM local, LLM+RAG et architecture agentique restent écartés.

**Justification** :
- DL : pas de volume suffisant (2000/500 lignes), explicabilité dégradée pour un gain incertain vs sklearn ; à réévaluer en M6 si le corpus texte grossit.
- SLM local : hors scope, rôle déjà couvert par le zero-shot CamemBERT utilisé en amont pour classifier les commentaires (pas comme modèle final).
- LLM API + RAG : pas de question ouverte sur corpus documentaire, sortie attendue = classe structurée ; enverrait des données socio-démographiques d'usagers à un tiers sans bénéfice pour une classification structurée.
- Architecture agentique : une seule prédiction en sortie, pas d'orchestration multi-étapes ni d'actions, aucun besoin d'orchestration.

### Compromis coût / latence

**Choix** : Aucun chiffrage précis retenu à ce stade pour le modèle final ; seule une appréciation qualitative existe (ML classique = coût "faible" vs DL = "élevé (GPU train)", LLM API+RAG = "élevé (€/token)", architecture agentique = "très élevé").

**Justification** : Non disponible — le tableau §6.1 (colonnes coût inférence, latence p95, explicabilité, dépendance fournisseur, biais, verdict) reste vide dans le canvas à ce jour. *Décision non finalisée, à signaler comme telle plutôt qu'à inventer.*

### Explicabilité du modèle

**Choix** : Aucun outil d'explicabilité (feature importance, SHAP) n'a encore été calculé ni tranché formellement.

**Justification** : Non disponible — §7 mentionne comme piste "Feature importance, SHAP (optionnel), matrice de confusion commentée. Trois messages-clés maximum", mais reste au stade de consigne du gabarit, non renseigné.

### Fallback / seuils de décision / human-in-the-loop

**Choix** : Trois leviers de conception sont identifiés comme devant être tranchés (rejection threshold, abstention contrôlée, escalade humaine HITL), mais **aucune valeur concrète n'est encore retenue** — les cellules du canvas restent des exemples génériques du gabarit (ex. "*si proba ∈ [0.4, 0.6]...*").

**Justification** : Le principe général (nécessité d'un human-in-the-loop, pas d'automatisation intégrale) avait été acté dès l'étape 1, au nom de l'art. 22 RGPD et du risque de responsabilité juridique. Le gabarit du canvas rappelle que "sans ces 3 éléments, ton modèle n'a pas de plan de fallback — il n'est pas déployable en prod sur un usage à enjeu", mais aucune réponse chiffrée n'est encore apportée. *Décision de conception amorcée mais non finalisée.*

*Note distincte* : un seuil de confiance est bien défini, mais uniquement pour la classification thématique des commentaires (NLP, étape 2) : "en dessous du seuil de confiance, le commentaire est marqué `a_valider` pour une revue humaine (cf. §7.2) plutôt que d'être affecté automatiquement" — ce seuil ne concerne pas le verdict final du modèle de classification du délai de retour à l'emploi.

### Cible de taux d'abstention

**Choix** : Cible fixée à ≤ 15 % des prédictions pour le mécanisme de rejet/abstention.

**Justification** : "Le seuil de confiance sera calibré après validation afin de réduire les erreurs graves tout en gardant un outil utilisable." Le document précise cependant explicitement que cette cible n'est pas encore mesurée : "aucune métrique à l'étape 4 sur ces 2 métriques (...) le benchmark n'implémente aucun mécanisme de seuil de confiance/rejet à ce stade (les modèles évalués prédisent systématiquement une classe), donc cette métrique ne peut pas encore être mesurée."

### Analyse des erreurs critiques et audit d'équité

**Choix** : L'audit d'équité par sous-groupe (recall classe 2 par nationalité, âge, diplôme) est identifié comme une action restant à mener, condition préalable à la mise en production.

**Justification** : "Le modèle utilise des proxies socio-économiques identifiés comme sensibles (...) l'audit d'équité par sous-groupe (...) reste à conduire avant toute mise en production (cf. §7.2)."

### Message client et recommandation finale

**Choix** : Non rédigés à ce stade.

**Justification** : Non disponible — §6.2 ("Recommandation finale au client") et §7.3 ("Message au client") restent des placeholders non complétés dans le canvas (`*[Quel scénario ? Pourquoi ? Quels compromis ?]*` ; `*[2-3 paragraphes lisibles par un décideur non technique...]*`).

---

## Note méthodologique

Le fichier `decisions.md` (squelette initial du projet) prévoyait des sections "Gestion des doublons", "Gestion des manquants", "Gestion des valeurs erratiques" et "Préparation" restées vides. Le présent document (`decision.md`) consolide ces décisions à partir du notebook (`journal-de-bord.ipynb`, canvas §1 à §5), de `criteria.md`, `scenarii.md` et `baseline.md`, qui font foi pour le détail des choix et justifications.

Certains éléments n'ont pas de justification textuelle explicite dans les sources disponibles (ex. hyperparamètres TF-IDF `max_features=300`, `min_df=2`) : cela est signalé dans les sections concernées plutôt que d'inventer une justification.
