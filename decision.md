# Synthèse des décisions — Étapes 1 à 5

> Ce document consolide les décisions importantes prises pendant les 5 premières phases du cas d'usage (Cadrer, Explorer, Préparer, Modéliser & comparer, Arbitrer), telles que documentées dans le notebook (`notebooks/certification-cas-usage.ipynb`), `criteria.md`, `scenarii.md` et les fichiers de résultats générés automatiquement. Le journal de bord (`journal-de-bord.ipynb`) trace la chronologie et les hésitations ; ce document trace les décisions arrêtées.

---

## Étape 1 — Cadrer

### Nature de la tâche ML

**Choix** : Classification supervisée multi-classe (3 classes : 0 = retour rapide <6 mois, 1 = retour moyen 6-12 mois, 2 = risque de longue durée >12 mois), sur données mixtes (numériques, catégorielles et — initialement — textuelles).

**Justification** : Besoin métier de l'agence de classer le délai potentiel de retour à l'emploi d'un usager. *Mise à jour phase 2 : l'EDA a montré que la colonne textuelle se réduit à 9 modalités ; la tâche est en réalité une classification sur données strictement tabulaires (cf. Étape 2).*

### Critère de succès prioritaire (métrique dominante)

**Choix** : Ne pas retenir l'accuracy globale comme critère principal, mais privilégier la limitation des erreurs asymétriques graves (classe 2 prédite en classe 0) : recall classe 2 et taux d'erreur "0↔2".

**Justification** : Classer à tort un usager à risque de longue durée en retour rapide le prive d'un accompagnement renforcé — impact humain et financier direct.

### Variables à risque identifiées

**Choix** : Identification de variables à risque : `usager_id`, `age`, `niveau_diplome`, `anciennete_poste_ans`, `code_rome_vise`, `code_insee_commune`, `est_allocataire`, `nationalite_hors_ue`, `synthese_entretien`, chacune associée à un risque spécifique (RGPD, discrimination, proxy).

**Justification** : `nationalite_hors_ue` peut constituer un proxy d'origine et relève de la vigilance non-discrimination, mais la nationalité ne figure pas parmi les catégories particulières de l'art. 9 RGPD. La base légale retenue est l'art. 6.1.e (mission d'intérêt public) ; `age` est une variable protégée et `code_insee_commune` un proxy territorial à haute granularité.

### Cadre réglementaire applicable

**Choix** : Application du RGPD (art. 6.1.e, minimisation et information des personnes), de l'AI Act (classement probable "haut risque" — Annexe III emploi), et du droit sectoriel (non-discrimination). L'art. 9 n'est pas la base légale de la nationalité.

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

**Choix** : Conserver les lignes avec manquants pour `age` (122, 4,9 %), `niveau_diplome` (84, 3,4 %) et `est_allocataire` (44, 1,8 %), avec une stratégie d'imputation à définir en préparation ; pour `synthese_entretien` (81 manquants, 3,2 %), l'option d'écarter ces lignes avait été envisagée mais **n'a finalement pas été retenue** : l'absence de synthèse est devenue une modalité à part entière, `texte_manquant`.

**Justification** : Pour `synthese_entretien`, le constat initial était "seul 81 absent sur 2450 lignes, c'est faible, on pourra donc les écarter" ; le passage à une variable catégorielle a rendu ce retrait inutile — une 10ᵉ modalité explicite conserve les lignes, évite d'introduire un biais de sélection et rend l'absence de synthèse auditable en tant que telle (son recall classe 2 est d'ailleurs suivi en §7.2). Pour les autres variables, "on mettra en place une stratégie pour conserver les lignes avec des valeurs manquantes."

### Gestion des valeurs erratiques / aberrantes

**Choix** : Les 126 personnes avec une ancienneté de poste >9 ans (détectées par méthode IQR) sont conservées telles quelles.

**Justification** : "Cela ne constitue pas, du point de vue métier, une valeur aberrante" — ces valeurs sont réalistes malgré leur détection statistique comme outliers.

### Déséquilibre de la variable cible

**Choix** : Constat d'un déséquilibre (classe 1 = 44,5 %, classe 0 = 37,4 %, classe 2 = 18,1 % minoritaire) conduisant à la nécessité d'un split stratifié et de métriques macro/F1 plutôt que l'accuracy seule.

**Justification** : Le déséquilibre "confirme dès maintenant l'usage de métriques macro/F1 plutôt que l'accuracy seule et la nécessité d'un split stratifié."

### Variables sensibles / proxy — orientations préliminaires pour la modélisation

**Choix initial** : `nationalite_hors_ue` devait être exclue des features ; `age` et `niveau_diplome` comparés en scénarios avec/sans ; `code_insee_commune` écarté au profit d'une version agrégée par département. Cette précaution a été révisée par l'arbitrage J0 après mesure du bénéfice de détection.

**Justification** : Disparate impact confirmé empiriquement (ratio ×2,46 UE/hors UE ; écart de 32,4 points par tranche d'âge ; écart de 34,2 points par diplôme ; écarts territoriaux de 9,7 % à 39 %). Ces écarts ont déclenché l'audit et les garde-fous J0, pas une conclusion automatique de discrimination du modèle.

### Nature réelle de `synthese_entretien` : 9 templates, pas du texte libre

**Choix** : `synthese_entretien` n'est pas traitée comme une donnée textuelle libre mais comme une **variable catégorielle à 10 modalités** (9 familles thématiques + `texte_manquant`).

**Justification** : L'EDA (§3.1, §3.3.2.1) établit que la colonne ne contient que **9 formulations uniques**, réutilisées telles quelles sur **2 419 des 2 500 lignes** (81 manquants, 3,2 %) ; `nunique` brut = `nunique` après nettoyage = 9, aucune variante n'est fusionnée par le nettoyage. Il n'y a donc ni vocabulaire ouvert, ni fautes de saisie, ni bruit stochastique à absorber : l'information utile tient intégralement dans l'identité du template. Distribution des 9 modalités : de 202 (8,1 %) à 338 occurrences (13,5 %), plus 81 `texte_manquant` (3,2 %).

### Méthode ayant produit les 9 familles thématiques (trace historique)

**Choix** : Les 9 libellés de familles ont été produits **une seule fois, hors pipeline**, par classification zero-shot avec CamemBERT (`cmarkea/distilcamembert-base-nli`, 68 M de paramètres) exécuté en local, le 22/09/2026. Le résultat est figé dans `data/referentiel_familles.csv` (9 lignes : template, famille, score de confiance, modèle, date d'étiquetage). En aval, la dérivation de la famille est un **simple `map` déterministe** sur ce référentiel (`src/pipeline_texte.assigner_famille`).

**Justification** : Les commentaires ne disposaient d'aucun label thématique fiable et l'étiquetage manuel par le métier n'était pas accessible ; le zero-shot local a servi d'outil d'étiquetage ponctuel (aucune donnée envoyée à un service externe). La première taxonomie (9 familles génériques : mobilité géographique, formation, compétences numériques, expérience professionnelle, freins administratifs, santé, situation familiale, projet professionnel, autre) avec un seuil de confiance de 0,5 laissait **7 templates sur 9 sous le seuil** (72,2 % des lignes non étiquetées) : les libellés ont été reformulés pour être mutuellement exclusifs et alignés sur le vocabulaire effectif des templates, aboutissant à une correspondance **strictement 1-1** avec des scores de 0,72 à 0,93. Comme il n'y a que 9 textes possibles, le référentiel est exhaustif par construction : **aucune inférence de modèle de langue n'est nécessaire ni à l'entraînement ni en production** (contrat vérifié par `tests/test_referentiel_familles.py`, qui lève une erreur si un texte du dataset n'est pas mappé).

### Association template ↔ classe cible : signal très fort, à documenter

**Choix** : Le signal porté par la famille thématique est explicitement qualifié d'**association très forte, quasi déterministe** (§3.7), et **nettement plus discriminant que n'importe quelle variable tabulaire**. Ce constat est assumé et signalé comme une limite du jeu de données, pas comme une performance du modèle.

**Justification et nuance chiffrée** : le croisement template × `classe_retour_emploi` (§3.5, `crosstab` normalisée par ligne) donne trois groupes nets :
- 3 templates « profil sans frein » (profil autonome, compétences techniques à jour, dynamisme) → 68,0 % à 71,7 % de classe 0 ;
- 3 templates « frein léger » (compétences numériques, mobilité géographique, reconversion) → 74,6 % à 78,4 % de classe 1 ;
- 3 templates « freins cumulés » (cumul de difficultés, perte de confiance, freins périphériques) → 44,6 % à 48,0 % de classe 2.

**Ce signal n'est cependant pas une fuite de cible au sens strict** : la vérification menée en §3.3.2.1 conclut qu'**aucun template ne mentionne le délai de retour à l'emploi ni une décision déjà prise par le conseiller**. Il s'agit d'un diagnostic formulé par un conseiller au moment de l'entretien, donc d'une information disponible **avant** la cible, et non d'une information dérivée de la cible.

**Réserve honnête à porter en soutenance** : (1) la pureté maximale observée est de **78,4 %**, aucune modalité n'est pure à 100 % — la formule « quasi déterministe » de §3.7 est plus forte que ce que montrent les données, et la mesure d'association (V de Cramér, khi²) **n'a pas été calculée** ; (2) le jeu de données est synthétique et ces 9 templates ont très probablement été générés **à partir** de la classe cible lors de sa fabrication — sur des verbatims réels, le signal serait moins propre et la performance de S1 se dégraderait ; (3) c'est précisément pour cette raison que S3 (famille seule) est écarté : il plafonne à 19,1 % de taux d'erreur grave, ce qui montre que le signal, aussi fort soit-il, ne suffit pas à décider seul.

### Risque de biais encodé dans le texte

**Choix** : Les 9 templates ont été audités par sous-groupe sensible (nationalité, diplôme, tranche d'âge) avant usage, y compris **à classe constante**, avec un seuil d'effectif fiable fixé à 30 (§3.6.2).

**Justification** : Certaines formulations ("barrière de la langue", "illettrisme numérique") peuvent encoder indirectement des variables sensibles déjà identifiées ; leur usage doit être audité au même titre que les proxys tabulaires. Conclusion de l'audit : l'association passe **essentiellement par la classe cible, et non par un biais rédactionnel propre au template**. Le passage à une variable catégorielle rend d'ailleurs cet audit directement lisible (9 modalités nommées), ce qui n'était pas le cas avec une représentation vectorielle où le biais se diluait sur des dizaines de colonnes.

### Minimisation RGPD renforcée par la dérivation de la famille

**Choix** : Une fois `famille_thematique` dérivée, le **verbatim brut n'est plus nécessaire en aval**. Ni l'entraînement, ni le modèle persisté, ni l'API ne manipulent de texte libre : l'API reçoit une modalité parmi 10.

**Justification** :
- **Minimisation (RGPD art. 5.1.c)** : la donnée transmise et stockée passe d'un commentaire de conseiller — potentiellement porteur de PII résiduelles, de jugements de valeur et d'informations de santé ou de situation familiale — à un **libellé catégoriel non nominatif**. C'est une réduction effective de l'assiette de données traitée, pas une simple précaution de traitement.
- **Anonymisation recentrée** : la détection/suppression de PII (téléphone, e-mail) ne sert plus qu'à l'**étape d'étiquetage initiale**, en amont et hors ligne. Elle n'est plus une dépendance du service en production, donc plus un point de défaillance RGPD à l'exécution. (Contrôle §3.3.2.1 : 0 pattern téléphone et 0 e-mail détectés sur les 9 templates.)
- **Aucun modèle de langue embarqué** : aucune inférence de transformeur n'a lieu en production ; il n'y a donc ni risque de mémorisation de données d'entraînement par un modèle de langue, ni sortie non déterministe à auditer, ni dépendance à un modèle tiers dont la provenance des données d'entraînement n'est pas maîtrisée.
- **Auditabilité (AI Act, système à haut risque)** : le mapping texte → famille est un fichier CSV de 9 lignes versionné en dépôt. Il est lisible, opposable et rejouable à l'identique, ce qu'un modèle zero-shot de 68 M de paramètres ne permet pas.

### Scénarios de données retenus (issus de l'EDA)

**Choix** : Quatre scénarios principaux — S1 (multimodal complet), S2 (sans variables sensibles), S3 (famille thématique seule), S4 (tabulaire seul) — complétés par des sous-scénarios S4a-e (ablation d'un proxy à la fois) et par un témoin S4-all (les 7 variables de S1 sans la famille thématique).

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

**Justification** : Son signal est associé à un risque de discrimination directe et de proxy d'origine ; la nationalité n'est toutefois pas une catégorie particulière de l'art. 9 RGPD, et la base légale documentée est l'art. 6.1.e.

### Traitement de `code_insee_commune`

**Choix** : Remplacé par le département (2 premiers chiffres) plutôt que le code brut.

**Justification** : Limiter sa sensibilité et sa granularité (haute cardinalité + proxy territorial).

### Détail des 4 scénarios principaux

**Choix** :
- S1 (multimodal complet) : `age`, `nationalite_hors_ue`, `niveau_diplome`, `anciennete_poste_ans`, `code_rome_vise`, `est_allocataire`, `departement` + `famille_thematique` (8 features → 163 colonnes après encodage).
- S2 (éthique, sans sensibles) : retrait de `nationalite_hors_ue`, `age`, `niveau_diplome`, `departement` → `anciennete_poste_ans`, `code_rome_vise`, `est_allocataire`, `famille_thematique` (4 features → 63 colonnes).
- S3 (famille thématique seule) : `famille_thematique` uniquement (1 feature → 10 colonnes).
- S4 (tabulaire seul) : `age`, `niveau_diplome`, `anciennete_poste_ans`, `departement`, imputation par médiane (numériques) / modalité la plus fréquente (catégorielles).

**Justification** : S2 applique les principes de minimisation, non-discrimination et protection des données dès la conception (RGPD/CNIL) ; S3 mesure le pouvoir prédictif du seul diagnostic d'entretien et fixe sa borne informationnelle ; S4 sert de référence face à S3 pour mesurer le gain apporté par la multimodalité. Le témoin S4-all (S1 privé de `famille_thematique`) isole l'apport net du diagnostic d'entretien.

### Sous-scénarios S4a-e (ablation de proxies)

**Choix** : S4a (baseline, 3 proxies), S4b (sans âge), S4c (sans diplôme), S4d (sans département), S4e (sans proxies majeurs, seulement ancienneté) — puis renommés d'après les features conservées (ex. S4a → S4-age-dip-anc-dep), avec ajout d'un S4-age-dip isolant les 2 proxies les plus déterminants.

**Justification** : Isoler l'effet de chaque proxy, sans qu'un signal équivalent contenu dans le texte ne masque son retrait ; un proxy n'est retenu que si son gain de performance est démontré sans dégrader les critères de sécurité et d'équité fixés en étape 1. Le renommage vise la clarté (nommage explicite des features conservées) ; S4-age-dip a été ajouté car âge + diplôme "portent l'essentiel du signal tabulaire" (constat du premier benchmark baseline).

### Modèle utilisé pour la baseline pré-modélisation

**Choix** : `RandomForestClassifier(class_weight="balanced")` utilisé comme référence unique pour comparer les scénarios, non retenu comme modèle final.

**Justification** : Sert uniquement à comparer les scénarios entre eux sur un pied d'égalité, pas à présélectionner un modèle.

### Pipeline générique (ColumnTransformer)

**Choix** : Pipeline reproductible unique construit avec `Pipeline` + `ColumnTransformer`, via `src/pipeline_tabulaire.py`. `src/pipeline_texte.py` ne conserve que le chargement du référentiel et l'affectation de la famille thématique (aucun estimateur scikit-learn).

**Justification** : Éviter les transformations one-shot dispersées et garantir la reproductibilité du prétraitement. La synthèse d'entretien étant devenue une colonne catégorielle, il n'y a plus qu'**un seul chemin de préprocessing** : le module `src/pipeline_tabulaire_hybride.py`, qui assemblait un bloc tabulaire et un bloc texte vectorisé, a été supprimé (cf. Étape 5).

### Encodage de la synthèse d'entretien

**Choix** : `OneHotEncoder(handle_unknown="ignore")` sur `famille_thematique` (10 modalités), dans le même `ColumnTransformer` que `code_rome_vise` et `departement`. La vectorisation TF-IDF (`TfidfVectorizer(max_features=300, min_df=2)`, qui produisait 68 termes effectifs) a été **supprimée**.

**Justification** : Dépenser 68 colonnes pour ré-encoder une information à 9 modalités est une perte de parcimonie et d'explicabilité sans contrepartie. La comparaison avant/après menée en §5.2.1 bis (5-fold CV, train uniquement, mêmes folds, modèles en configuration par défaut) montre que le one-hot **ne dégrade rien et améliore légèrement** : Δ F1 macro moyen **+0,004**, Δ recall classe 2 moyen **+0,006**, Δ taux d'erreur grave moyen **−0,1 point**. Le gain est concentré sur S1/RandomForest (**+0,027** de F1 macro, **+0,033** de recall classe 2, **−1,6 point** d'erreur grave). Contrôles de non-régression : S3 strictement identique (0,635 / 0,660 / 19,1 % avant comme après) et témoin S4-all inchangé à 10⁻³ près — ce qui confirme que l'écart observé vient bien du changement de représentation et non d'un effet de bord du refactor.

> Note de traçabilité : l'hyperparamétrage TF-IDF (`max_features=300`, `min_df=2`) n'avait jamais été justifié explicitement dans les sources du projet. Cette dette documentaire est désormais sans objet, la vectorisation ayant été retirée.

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

### Sort de `HistGradientBoostingClassifier`

**Choix** : HGB a été écarté une première fois après le benchmark initial, puis **réintégré** lors de la phase d'optimisation : deux de ses variantes (`class_weight="balanced", max_depth=10` et `class_weight={0:1,1:1,2:3}`) figurent parmi les trois finalistes comparés en §5.6, avant d'être finalement écartées au profit de RandomForest.

**Justification** : L'élimination initiale reposait sur son recall classe 2 systématiquement le plus faible (ex. 0,561 sur S1, 0,290 sur S4-age-dip en configuration par défaut). Le réglage de `class_weight` et de `max_depth` a corrigé ce défaut — la variante `balanced, max_depth=10` atteint le meilleur F1 macro du benchmark CV (**0,706** sur S1, taux d'erreur grave 10,2 %) — mais, en sous-validation, `RandomForestClassifier(n_estimators=300)` la domine sur toutes les métriques prioritaires. Son seul avantage résiduel est la sobriété : **0,806 Mo contre 27,5 Mo**, soit 34× plus léger, et une latence p95 plus faible. Cet argument n'a pas suffi, 27,5 Mo restant parfaitement gérable pour un service conteneurisé.

### Métriques retenues et priorisation

**Choix** : F1 macro, recall classe 2, F1 classe 2, taux d'erreur grave 2→0 (prioritaire), taux d'erreur 0→2 ; accuracy reléguée en indicateur secondaire ; ROC-AUC et métriques de régression (RMSE/MAE/R²) explicitement exclues.

**Justification** : L'accuracy peut être trompeuse sur une cible déséquilibrée (ex. S3 obtient une accuracy honorable de 0,652 mais un taux d'erreur grave de 19,1 %, très au-dessus du seuil de 5 % visé). ROC-AUC n'est pas directement interprétable pour arbitrer sur l'erreur asymétrique prioritaire ; RMSE/MAE/R² sont des métriques de régression, non applicables à une classification multi-classe. À partir de §5.2, une **matrice de coût métier** (arbitraire, à faire valider par le métier) et un **coût métier total en euros** complètent ces métriques : ils rendent l'arbitrage recall / erreur grave comparable sur une échelle unique.

### Hyperparamètres testés

**Choix** : LogisticRegression → C=0,1 et C=10 (vs défaut 1,0) ; RandomForest → n_estimators=300, max_depth=10, class_weight={0:1,1:1,2:3}, min_samples_leaf=5.

**Justification** : Chaque hyperparamètre est justifié individuellement — ex. `class_weight` ciblé pour réduire spécifiquement le taux d'erreur grave, au prix probable d'un F1 macro plus faible ; `min_samples_leaf=5` testé pour vérifier si des feuilles moins spécifiques réduisent le taux d'erreur grave sans trop dégrader le F1 macro.

### Choix du scénario / modèle final

**Choix** : Scénario **S1** (tabulaire complet + `famille_thematique`) avec `RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)`.

**Justification** : Sur le test set (§5.6.2, utilisé une seule fois), cette configuration obtient une accuracy de **0,714**, un F1 macro de **0,690**, un recall classe 2 de **0,589**, un F1 classe 2 de **0,570**, un taux d'erreur grave 2→0 de **10,0 %** et un taux d'erreur 0→2 de **4,8 %**. Matrice de confusion : `[[142, 36, 9], [27, 162, 34], [9, 28, 53]]` — sur les 90 usagers réellement en classe 2, 53 sont détectés et 9 sont classés à tort en classe 0. Le taux d'erreur grave, supérieur au seuil de 5 % visé par `criteria.md`, n'est jugé acceptable qu'à la condition d'une **revue par un conseiller humain** selon les règles A/B. Au réglage servi A = 0,40, B = 0,20, le test indique 25,6 % de dossiers à revoir ; le candidat B = 0,10 et ses réserves sont documentés dans la mise à jour du §5.2.3 ci-dessous.

### Courbes d'apprentissage / early stopping

**Choix** : Tracé des courbes d'apprentissage (train vs CV) pour RandomForest et HGB (early stopping natif activé sur HGB, `n_iter_no_change=3`, `validation_fraction=0.2`) ; LogisticRegression exclu de cette analyse.

**Justification** : Diagnostiquer le sous/sur-apprentissage. LogisticRegression est exclu car son solveur convexe n'a pas de notion d'itération qui overfit ; RandomForest n'a pas d'early stopping natif car les arbres ne sont pas ajoutés séquentiellement.

### Persistance du modèle final

**Choix** : Pipeline complet (préprocesseur + modèle) sauvegardé via joblib dans `models/modele_final_s1_RandomForestClassifier__n_estimators_300__class_weight_balanced_.joblib` (34,4 Mo), accompagné d'un `.metadata.json` versionnant les librairies, le commit git, les features d'entrée, les seuils de validation manuelle et les métriques de test.

**Justification** : Pour un usage ultérieur (API de service en phase d'industrialisation) et pour la traçabilité exigée d'un système à haut risque. Le modèle servi (`services/model/models/emploi_retour_s1.joblib`, v3.0.0) est exporté depuis cet artefact par `scripts/export_model_prod.py`.

### Condition C6 — AIPD et registre des traitements

La mise en service reste conditionnée à une AIPD au titre de l'art. 35 RGPD et
à l'inscription du traitement au registre. Le dossier devra décrire la finalité
C1, la base légale art. 6.1.e, les catégories de personnes et de données, les
destinataires, les durées de conservation, les droits art. 13-14, les mesures
de minimisation et d'accès, l'audit C3, la clause de retrait C4 et la revue
humaine C5. Le DPO et la direction métier doivent valider ces deux livrables
avant tout déploiement ; aucune validation n'est présumée par le code.

### Constat sur la cible de recall classe 2

**Choix** : Le recall classe 2 obtenu (**0,589** sur le test set, 0,660 en CV) reste nettement en-deçà de la cible de 0,80 fixée dans `criteria.md` ; le taux d'erreur grave (10,0 %) reste au double du seuil de 5 %. Les deux écarts sont assumés et documentés plutôt que masqués.

**Justification** : Le benchmark montre qu'aucune configuration testée n'atteint simultanément les deux cibles : la configuration au meilleur recall classe 2 (`RandomForestClassifier(min_samples_leaf=5)` sur S1, recall **0,754**) dégrade le taux d'erreur grave à 13,5 %, et celle au meilleur taux d'erreur grave (S4-all, 8,3 %) perd le bénéfice du diagnostic d'entretien. L'arbitrage retenu compense ce déficit par le filet de sécurité humain (§7.2) plutôt que par un réglage qui déplacerait simplement le problème.

### Points restant à traiter avant mise en production

**Choix** : L'audit d'équité par sous-groupe a depuis été exécuté (§7.2) et **échoue au critère de `criteria.md`** (écarts de 27 à 44 points contre une cible de 10 points) : c'est désormais le point bloquant n°1. Restent également : une seule famille de modèles testée, pas de recherche d'hyperparamètres exhaustive (GridSearch), pas de mesure d'empreinte carbone, et une matrice de coût métier encore fictive.

**Justification** : Explicitement listé comme limite à traiter avant toute mise en production.

---

## Étape 5 — Arbitrer

### Arbitrage J0 — maintien de `nationalite_hors_ue`

**Décision** : conserver `nationalite_hors_ue` comme feature du scénario S1 et
comme axe obligatoire de l'audit d'équité. La mesure ex post montre un recall de
classe 2 supérieur hors UE (0,800 contre 0,529 UE dans l'analyse de référence) :
la variable sert à mieux orienter vers un accompagnement renforcé, jamais à
contrôler, sanctionner, radier ou refuser un accompagnement.

**Conditions C1 à C7** : finalité limitée à l'accompagnement renforcé ; aucune
exposition dans Prometheus, Grafana ou les logs ; audit récurrent avec marquage
des effectifs sous 30 ; retrait de la variable si le recall hors UE devient
inférieur au recall UE, après vérification des effectifs et arbitrage prévu par
la clause C4 ; maintien de la revue humaine §5.2.3 ; AIPD art. 35 et inscription
au registre avant mise en service ; information art. 13-14. Le retrait est une
condition de gouvernance, mais il n'est pas automatisé par le prototype :
`scripts/audit_equite.py` signale le cas (code de sortie 2), sans modifier le
modèle ni les features servis.

La décision est réversible et ne vaut pas autorisation de mise en production :
le filet de sécurité ne rattrape encore qu'une partie des erreurs graves 2→0.

### Correction du scénario S1 (bug découvert et corrigé)

**Choix** : Le scénario **S1**, décrit dans `scenarii.md` comme "approche multimodale complète" (tabulaire + synthèse d'entretien), était implémenté dans `src/pipeline_tabulaire.py` en **tabulaire seul** — un écart entre le plan documenté et le code. Ce bug a été corrigé en deux temps : d'abord par la généralisation d'un module d'assemblage tabulaire + texte vectorisé (`src/pipeline_tabulaire_hybride.py`), puis, après la requalification de la synthèse en variable catégorielle, par la suppression pure et simple de ce module — `famille_thematique` étant désormais une colonne du `ColumnTransformer` tabulaire. Un scénario **S4-all** a été créé pour désigner explicitement la variante tabulaire-seule (les 7 mêmes variables que S1, sans la famille thématique), conservée comme témoin.

**Justification** : Le code (`SCENARIO_FEATURES["s1"]`) ne contenait que des variables tabulaires ; aucune concaténation du texte n'existait pour "s1" avant correction. Ce constat a été fait lors de la rédaction de la section §7 du notebook (analyse de feature importance), où il est apparu que le modèle persisté n'utilisait pas `synthese_entretien` contrairement à sa description.

### Suppression de la couche NLP (zero-shot + TF-IDF)

**Choix** : Retrait complet du zero-shot CamemBERT et de la vectorisation TF-IDF du code, du notebook, des modèles servis, de l'API, des dépendances et de la CI. Le référentiel `data/referentiel_familles.csv` est conservé comme **donnée versionnée** et unique trace exploitable de la méthode d'étiquetage.

**Justification** : Voir le raisonnement complet en Étape 2 (9 templates ⇒ donnée tabulaire). Conséquences chiffrées : métriques **améliorées** en moyenne (Δ F1 macro +0,004, Δ recall classe 2 +0,006, Δ erreur grave −0,1 point, avec +0,027 / +0,033 / −1,6 point sur la configuration retenue S1/RandomForest) ; **~2,5 Go de dépendances retirées** (`torch`, `torchvision`, `transformers`, `sentencepiece`, `protobuf`) ; plus aucune inférence de transformeur, donc un service d'inférence dont la surface d'attaque, l'empreinte et le temps de démarrage sont réduits d'autant. Le changement de représentation a également modifié le classement des finalistes : `RandomForestClassifier(n_estimators=300, class_weight="balanced")` remplace `HistGradientBoostingClassifier(class_weight={0:1,1:1,2:3})` comme modèle retenu.

### Choix final du modèle/scénario

**Choix** : Scénario **S1** (tabulaire complet + `famille_thematique`) avec `RandomForestClassifier(n_estimators=300, class_weight="balanced")`.

**Justification** : Il domine les deux autres finalistes sur toutes les métriques prioritaires en sous-validation (F1 macro 0,703, recall classe 2 0,681, erreur grave 9,7 %, coût métier 73 540 €) et confirme sur le test set (F1 macro **0,690**, recall classe 2 **0,589**, erreur grave **10,0 %**, erreur 0→2 **4,8 %**). Par rapport à l'ancien finaliste `HistGradientBoostingClassifier(class_weight={0:1,1:1,2:3})` de la version antérieure du notebook : **+0,032 de F1 macro, +0,125 de recall classe 2, +0,069 de F1 classe 2, −2,8 points de taux d'erreur grave et −18 380 € de coût métier**. Le taux d'erreur grave, supérieur au seuil de 5 % visé par `criteria.md`, n'est acceptable qu'à la condition explicite d'un **arbitrage systématique par un conseiller humain** (cf. section fallback ci-dessous).

**Alternatives considérées et écartées** :
- `HistGradientBoostingClassifier(class_weight="balanced", max_depth=10)` sur S1 : meilleur F1 macro du benchmark CV (0,706) et **34× plus léger** (0,806 Mo contre 27,5 Mo), avec une latence p95 plus favorable — écarté car dominé en sous-validation sur le recall classe 2 et le coût métier ; la sobriété ne compensait pas la perte sur la métrique prioritaire.
- S4-all (les 7 variables tabulaires, sans la famille thématique) : meilleur taux d'erreur grave du benchmark (8,3 % en CV avec `RandomForestClassifier(n_estimators=300)`) mais F1 macro et recall classe 2 inférieurs — écarté car le gain sur l'erreur grave est de toute façon absorbé par l'arbitrage humain retenu pour S1.
- S3 (famille thématique seule) : recall classe 2 honorable pour une unique variable (0,660) mais taux d'erreur grave presque deux fois plus élevé (19,1 %) — écarté. **La famille thématique n'apporte sa valeur qu'en complément des variables administratives, pas en remplacement.**
- `RandomForestClassifier(min_samples_leaf=5)` sur S1 : meilleur recall classe 2 de tout le benchmark (0,754) et meilleur coût métier (49 780 €), mais taux d'erreur grave dégradé à 13,5 % — écarté au nom de la priorité donnée à l'erreur asymétrique.

### Exclusion des familles GenAI / LLM / agents (repris et confirmé en arbitrage)

**Choix** : Seul le ML classique (scikit-learn) est retenu comme famille de modèles ; Deep Learning, SLM local, LLM+RAG et architecture agentique restent écartés.

**Justification** :
- DL : pas de volume suffisant (2000/500 lignes), explicabilité dégradée pour un gain incertain vs sklearn ; à réévaluer en M6 si le corpus texte devient réellement du texte libre et grossit.
- SLM local : hors scope. Un modèle pré-entraîné a bien servi **une seule fois**, hors pipeline, pour étiqueter 9 templates ; le résultat est figé dans un CSV de 9 lignes. Aucun modèle de langue n'est chargé à l'entraînement ni à l'inférence.
- LLM API + RAG : pas de question ouverte sur corpus documentaire, sortie attendue = classe structurée ; enverrait des données socio-démographiques d'usagers à un tiers sans bénéfice pour une classification structurée.
- Architecture agentique : une seule prédiction en sortie, pas d'orchestration multi-étapes ni d'actions, aucun besoin d'orchestration.

### Compromis coût / latence

**Choix** : Mesures désormais chiffrées sur les trois finalistes (§5.6.2, 1 000 appels `predict` unitaires) : pour le modèle retenu, **27,5 Mo sur disque, 1,37 s de fit, latence p50 27,3 ms / p95 50,1 ms**. Le coût métier est chiffré en euros via la matrice de coût §5.2.1 (73 540 € en sous-validation sur S1).

**Justification** : Ces mesures rendent l'arbitrage sobriété / performance factuel plutôt que qualitatif. Deux réserves subsistent : (1) le coût **€/1 000 prédictions en exploitation réelle** reste à instrumenter (§8/§9) ; (2) l'**empreinte carbone** (kgCO₂eq / 1 000 prédictions) n'a pas été mesurée. À noter : la cible `criteria.md` de p95 < 200 ms est confortablement tenue.

### Explicabilité du modèle

**Choix** : Importance par permutation calculée en §7.1 sur le pipeline final (`RandomForestClassifier`), complétée en §7.2 par une lecture du recall classe 2 par famille thématique. Aucun calcul SHAP réalisé à ce stade (optionnel dans le canvas).

**Justification** : Le passage à `famille_thematique` améliore directement l'explicabilité : la synthèse d'entretien occupe désormais **10 colonnes nommées et lisibles par un conseiller** au lieu des 68 termes d'un bloc vectoriel opaque. Un conseiller peut lire « ce dossier est classé à risque notamment parce que la synthèse relève un cumul de freins périphériques », ce qui était impossible avec la représentation précédente. Reste la limite d'une méthode globale : elle n'explique pas une prédiction individuelle avec la finesse d'une méthode d'attribution locale.

### Fallback / arbitrage humain systématique

**Décision initiale, toujours en vigueur dans les artefacts servis** : Le modèle ne s'abstient jamais et ne décide jamais seul. Deux règles de validation manuelle sont définies en §5.2.3 et persistées dans les métadonnées du modèle :
- **Règle A** — si P(classe 2) ≥ **0,40**, le dossier part en validation manuelle quelle que soit la classe prédite (priorité normale, 5 jours ouvrés) ;
- **Règle B** — si la classe 0 est prédite **et** P(classe 2) ≥ **0,20**, le dossier part également en validation manuelle (risque résiduel d'erreur grave, **priorité haute sous 48 h ouvrées**).

L'API retourne toujours HTTP 200 avec la classe prédite, les 3 probabilités et un champ `decision` ∈ {`a_valider`, `auto`}.

**Justification** : Le taux d'erreur grave du modèle retenu (10,0 % sur le test set) est supérieur au seuil de 5 % visé par `criteria.md`. Ce niveau de risque n'est acceptable que si aucune décision n'est prise automatiquement : c'est la condition de déploiement, pas une option de conception (art. 22 RGPD, acté dès l'étape 1). Au réglage A = 0,40, B = 0,20, les artefacts enregistrent 128 dossiers signalés sur 500 (**25,6 %**), dont 29 par la seule règle B, pour un coût de revue de **2 560 €** à 20 €/dossier. Sur les 9 erreurs graves du test set, **4 sont rattrapées par le filet (44 %) et 5 ne le sont pas**.

**Mise à jour du 29/09/2026 — balayage du seuil B** : A est maintenu à **0,40** pour comparer les seuils B sur la sous-validation, avant lecture du test. Parmi les valeurs testées (0,10 ; 0,15 ; 0,20 ; 0,30), le notebook retient **B = 0,10** comme meilleur candidat de rattrapage : **6/8 erreurs graves signalées (75,0 %)** et **28,2 %** des dossiers orientés en revue sur la sous-validation. Aucun seuil B testé n'atteint l'hypothèse de capacité minimale de revue de **30 %** sur ces données. L'évaluation descriptive a posteriori sur le test donne, pour B = 0,10, **6/9 erreurs graves (66,7 %)** et **30,8 %** de dossiers revus ; elle ne sert pas à sélectionner le seuil.

**Statut de la décision** : B = 0,10 est un **candidat exploratoire du notebook**, pas le seuil opérationnel actuellement servi. Les métadonnées du modèle final et celles du modèle API v3.0.0 portent toujours A = 0,40 et B = 0,20. Aucun artefact de production n'est mis à jour automatiquement par le sweep. Le choix métier de capacité reste à valider ; une éventuelle adoption de B = 0,10 exige une persistance, un export et une promotion contrôlés, puis une réévaluation sur des données distinctes. La réserve bloquante demeure : le candidat laisse encore 2 erreurs graves sur 8 sans revue en sous-validation, et le réglage servi en laisse 5 sur 9 sur le test.

**Autres réserves assumées** : (1) le seuil A retenu (0,40) **n'est pas le minimiseur du coût métier** selon le balayage initial — ce choix privilégie une charge de revue soutenable et reste à faire trancher par le métier. (2) La part revue au réglage servi (25,6 %) **dépasse la cible de `criteria.md`** (≤ 15 %). (3) La matrice de coût est fictive. (4) Le calcul suppose que les dossiers revus sont corrigés sans erreur, hypothèse à revalider en exploitation.

### Analyse des erreurs critiques et audit d'équité

**Choix** : L'audit d'équité par sous-groupe a été **exécuté** en §7.2 sur le test set, et son résultat est un **point bloquant** : le critère de `criteria.md` (écart de recall classe 2 < 10 points entre sous-groupes) n'est pas respecté.

**Résultats mesurés** (test set, 500 lignes, 90 cas de classe 2) :
- `nationalite_hors_ue` : recall 0,529 (UE, n=70) contre 0,800 (hors UE, n=20) → **27 points d'écart** ;
- `niveau_diplome` : de 0,385 (Bac+2) à 0,829 (sans diplôme) → **44 points d'écart** ;
- tranche d'âge : de 0,333 (41-50 ans) à 0,756 (51-60 ans) ;
- `famille_thematique` (axe d'audit nouveau, rendu possible par la variable catégorielle) : de **0,000** (réactualisation des compétences numériques, 0/7) et 0,167 (mobilité géographique, 1/6) jusqu'à 0,786 (garde d'enfants / transport, 11/14).

**Justification et réserve statistique** : avec 90 cas de classe 2 sur le test set, plusieurs sous-groupes comptent moins de 10 observations, très en-deçà du seuil de fiabilité de 30 retenu en §3.6. **Aucun de ces écarts ne peut être considéré comme établi** — mais aucun ne peut non plus être écarté. Tant que ce point n'est pas tranché sur un échantillon suffisant, la mise en production ne doit pas être engagée. L'audit reste nécessaire indépendamment de l'arbitrage humain déjà prévu, puisque le modèle utilise des proxies tabulaires (`age`, `niveau_diplome`, `departement`) en plus du diagnostic d'entretien.

### Message client et recommandation finale

**Choix** : Rédigés en §6.2 et §7.3 du notebook, en langage métier, expliquant le choix de S1, la nécessité du filet de validation manuelle et les deux réserves bloquantes (équité non établie, erreurs graves non toutes rattrapées).

**Justification** : Permettre au client de comprendre l'arbitrage (performance globale maximale, compensée par un contrôle humain ciblé plutôt que par une réduction de la performance) et ses implications opérationnelles et budgétaires (~5 € de revue par dossier traité).

---

## Étape 6 — Industrialiser et améliorer en continu

### Industrialisation, CI et reproductibilité

**Décision** : Le pipeline est industrialisé avec des services conteneurisés, Docker Compose, une CI GitHub Actions, des contrôles de qualité et de non-régression, ainsi qu'un suivi MLflow. Les tests et le golden run vérifient que le modèle servi correspond à la configuration, aux features et aux métriques attendues. Le notebook reste la source de l'analyse et les scripts/modules séparés portent l'exécution réutilisable.

**Justification** : Les commits d'industrialisation des 23 et 27 septembre ont ajouté les contrôles, l'architecture et les flux documentés. Le modèle servi ne doit pas diverger silencieusement de celui évalué ; les assertions sur des métriques sensibles aux variations de machine utilisent une tolérance adaptée plutôt qu'une égalité trop stricte. La capture d'une exécution GitHub Actions réussie documente le passage de la CI, sans constituer une décision métier.

### Boucle de feedback conseiller

**Décision** : Le prototype permet à un conseiller d'associer une classe réellement observée à un `request_id` via `POST /feedback`. Les retours sont enregistrés dans SQLite ; un rejeu identique est idempotent, un label contradictoire requiert un arbitrage humain. Les annotations peuvent être jointes aux features pour audit et entraînement candidat. Les données d'exemple restent simulées et ne sont pas des retours réels de conseillers.

**Limites** : Le raccordement durable des prédictions en ligne à `data/prod_scored.csv` et le canal opérationnel de saisie conseiller restent à réaliser. Le `request_id` prévu par l'architecture ne signifie donc pas que toute la chaîne de production est déjà persistée. L'accès et la durée de conservation des scores et feedbacks contenant potentiellement des données personnelles doivent être encadrés.

### Réentraînement et promotion contrôlée

**Décision** : La cadence retenue est une vérification hebdomadaire **manuelle** du volume d'annotations. À partir de 100 feedbacks non consommés, l'opérateur peut lancer `python scripts/retrain.py --min-feedback 100`. Le candidat est évalué sur le même jeu de référence figé que le modèle de production ; la promotion exige le respect des planchers de qualité, l'absence de régression critique supérieure à 0,01 et un gain d'au moins 0,01 sur une métrique suivie. Les décisions d'acceptation ou de rejet sont tracées dans `decisions_log.jsonl` et, si disponible, dans MLflow.

**Justification et limites** : Aucun apprentissage en ligne, ordonnanceur, déploiement ou promotion automatique n'est retenu. Un candidat accepté produit un artefact distinct ; sa mise en service demeure une étape séparée, contrôlée et humaine. Un candidat rejeté ne remplace pas le modèle servi et les feedbacks restent disponibles.

### Supervision en exploitation

**Décision** : Prometheus et Grafana fournissent une supervision visuelle de la disponibilité, des erreurs HTTP, de la latence, du débit, des classes prédites, de la confiance renvoyée et de la distribution des familles thématiques. Cette distribution d'entrée sert de signal à investiguer, pas de preuve de dérive ni de baisse de performance. L'audit de qualité et d'équité est rejoué hors ligne lorsque des labels sont disponibles.

**Limites** : Il n'y a pas de règles Prometheus ni d'Alertmanager ; le seuil visuel de latence Grafana n'envoie pas de notification. Le service ne calcule pas de score OOD, de PSI, de Brier score ou de courbe de calibration. Sans vérité terrain récente, les métriques prédictives ne sont pas mesurables. La revue humaine du §7.2 reste nécessaire et aucun signal de monitoring ne transforme une prédiction en décision automatique.

### Conditions restantes avant toute mise en service

La mise en service reste bloquée par l'arbitrage métier sur la capacité de revue et le seuil B, par le filet qui ne rattrape pas toutes les erreurs graves, et par l'audit d'équité dont les écarts observés sur le test ont des effectifs insuffisants pour conclure. Restent aussi les conditions juridiques de J0/C6 (AIPD et registre validés par le DPO et la direction métier), l'alerting, l'ordonnancement réel de la revue hebdomadaire, la journalisation durable des prédictions, le canal conseiller et les règles d'accès/conservation des données. La stack de démonstration, les feedbacks simulés et la CI verte ne valent pas autorisation de déploiement.

---

## Synthèse d'arbitrage — les trois points qu'un jury relèvera

1. **Le signal textuel est artificiellement propre.** `synthese_entretien` se réduit à 9 templates dont l'association à la classe cible est très forte (pureté de 44,6 % à 78,4 %, qualifiée de « quasi déterministe » en §3.7). Ce n'est **pas une fuite de cible au sens strict** — aucun template ne mentionne le délai ni une décision déjà prise (§3.3.2.1) — mais le jeu de données étant synthétique, ces templates ont vraisemblablement été générés à partir de la classe. **Conséquence assumée : les performances de S1 sont une borne haute optimiste et ne se transposeraient pas telles quelles à des verbatims réels.**.
2. **Les cibles de `criteria.md` ne sont pas atteintes.** Recall classe 2 : 0,589 contre 0,80 visé. Taux d'erreur grave : 10,0 % contre 5 % visé. Part revue du réglage servi : 25,6 % contre 15 % maximum visé. B = 0,10 est un candidat qui améliore le rattrapage en sous-validation mais ne satisfait pas l'hypothèse de capacité minimale de 30 % ; l'écart d'équité observé reste à confirmer sur des effectifs suffisants. Ces limites ne valent pas feu vert de mise en production.
3. **Le retrait du NLP a simplifié le dispositif ; l'industrialisation reste un prototype à finaliser.** Un mapping auditable de 9 lignes remplace l'inférence NLP en production et renforce la minimisation. CI, suivi, feedback et promotion contrôlée sont présents, mais l'alerting, la persistance réelle des scores, le canal conseiller et l'ordonnancement ne sont pas tous opérationnels. La conformité et l'autorisation de mise en service ne sont pas présumées par le code.

---

## Note méthodologique

Le fichier `decisions.md` (squelette initial du projet) prévoyait des sections "Gestion des doublons", "Gestion des manquants", "Gestion des valeurs erratiques" et "Préparation" restées vides ; il a été remplacé par le présent document, qui consolide les décisions à partir du notebook (`notebooks/certification-cas-usage.ipynb`, §1 à §9), de `criteria.md`, `scenarii.md`, des résultats générés par le notebook et des artefacts effectivement servis. Lorsqu'un seuil du notebook diffère des métadonnées ou du modèle API, ce document distingue explicitement le candidat exploratoire du réglage opérationnel. `decisions_log.jsonl` trace les décisions de promotion au fil de l'eau.

Les mentions de « zero-shot », « CamemBERT » et « TF-IDF » subsistant dans ce document, dans le notebook et dans `src/pipeline_texte.py` sont des **références historiques assumées** : elles documentent la méthode ayant produit `data/referentiel_familles.csv` et la comparaison avant/après qui justifie son retrait. Aucune de ces techniques n'est active dans le code, le modèle servi ou les dépendances du projet.
