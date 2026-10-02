# Plan de soutenance v2 - Cas d'usage CISIA (document autoporteur)

Ce document contient tout ce qu'il faut pour construire le support et préparer l'oral : cadre, chiffres de référence, déroulé minuté, contenus, limites, questions du jury avec réponses courtes, annexes, punchlines, répétition. Il ne renvoie à aucun autre fichier. Les chiffres sont ceux du projet à la date de rédaction ; les revérifier dans le notebook et les artefacts avant de figer les slides.

---

## 1. Cadre

- **Format** : 30 min d'exposé, suivies de 30 min de questions, devant un jury de 2 professionnels externes. Aucune démonstration en direct : support statique, captures d'écran seulement, aucun service à lancer.
- **Support** : **15 slides** + annexes hors temps d'exposé.
- **Timing** : **29 min prévues + 1 min de réserve**, avec un plan de coupe (§5).
- **Compétences évaluées** : référentiel technique CISIA C1 à C9 (notebook, soutenance, questionnaire de 15 questions portant sur C1, C2 et C4). Côté transversal, la soutenance mobilise CT6 (présenter un travail au commanditaire en synthétisant résultats et démarche, et répondre aux questions) et CT7 (codes et posture professionnels face au jury).
- **Niveau attendu** : « transposer », c'est-à-dire construire dans un contexte nouveau. Le jury doit voir des choix argumentés, pas une application guidée.

### Intitulés des compétences (pour les tags de slides)

| Code | Intitulé abrégé |
|---|---|
| C1 | Identifier un jeu de données adapté au besoin métier (pertinence, cohérence) |
| C2 | Identifier les risques éthiques et sociétaux, dans le cadre réglementaire |
| C3 | Préparer les données (intégrité, pertinence, techniques adaptées au cadrage) |
| C4 | Choisir un modèle par une démarche scientifique, en mesurant sa pertinence |
| C5 | Entraîner le modèle de façon automatique et supervisée |
| C6 | Implémenter le modèle et ses briques (moteurs, reporting, suivi) |
| C7 | Contribuer à l'architecture cible, en identifiant les contraintes |
| C8 | Mesurer la performance et les impacts pour maintenir la solution fonctionnelle |
| C9 | Amélioration continue, selon la commande initiale et l'évolution des besoins et données |

### Fil rouge

**Peut-on utiliser une prédiction pour mieux orienter les demandeurs d'emploi sans automatiser une décision à fort impact ?**

Réponse annoncée dès la slide 1 : **oui comme aide à l'orientation, non comme décideur**. Le prototype est techniquement industrialisé mais **non prêt pour une mise en production décisionnelle**.

Trame personnelle à suivre de bout en bout : **ce que j'ai compris, ce que j'ai fait, ce que j'ai repris ou corrigé, ce que je ferais autrement**. Les éléments techniques sont des preuves de ce récit, pas une fin en soi.

### Bandeau de progression (sur toutes les slides)

`1 Comprendre -> 2 Explorer -> 3 Évaluer -> 4 Encadrer -> 5 Industrialiser -> 6 Décider`

La section en cours est en surbrillance. Chaque fin de section se termine par une phrase-pivot qui répond à la question directrice.

### Trois chiffres à retenir (répétés, le reste en annexe)

| Chiffre | Rôle dans le récit |
|---|---|
| **9 templates** (au lieu de texte libre) | La donnée a changé la démarche |
| **9/90 = 10 % d'erreurs graves** sur le test (cible < 5 %) | Le résultat ne suffit pas |
| **25,6 % de dossiers en revue** (cible ≤ 15 %) | Le filet humain est partiel et coûteux |

### Les cinq limites majeures

Formule : **ce que je sais / ce que je ne sais pas / ce qu'il faut pour savoir**. Dites-les une fois en slide 3, rappelez-les en slide 15. Ailleurs, une seule réserve par slide.

1. **Données** : jeu qualifié de synthétique dans le notebook, présenté comme collecté en agence dans le sujet ; procédé de génération non documenté ; signal très propre ; représentativité non démontrée.
2. **Métier** : aucun échange avec le métier n'était possible dans le cas d'étude. Matrice de coûts, seuils A/B et conditions d'usage de la nationalité sont des hypothèses ou arbitrages du projet, jamais des validations.
3. **Protocole** : le split final est corrigé, mais le journal de bord rapporte des usages antérieurs de `X_test`. On ne revendique pas un test vierge ; une nouvelle évaluation indépendante est nécessaire.
4. **Équité** : écarts préoccupants mais sur petits effectifs, donc non établis.
5. **Production** : stack locale, pas de déploiement distant démontré, boucle de feedback non éprouvée avec de vrais retours métier.

### Précautions de formulation (à relire avant de fabriquer le support)

- Toujours préciser le protocole d'un chiffre : **validation croisée (CV) sur le train**, **sous-validation (400 dossiers)** ou **test final (500 dossiers)**. Ne jamais les réunir dans un même classement.
- Référence opérationnelle servie : **A = 0,40 et B = 0,20**. La recommandation hors ligne est **B = 0,15**, non réexportée : les artefacts servis restent à B = 0,20. D'anciennes mentions de B = 0,10 sont obsolètes.
- `auto` est un statut technique de l'API, pas une autorisation de décision administrative automatique.
- Écarts d'équité : signaux à vérifier, pas discrimination démontrée.
- p95 = 50,1 ms mesure le pipeline seul sur 1 000 appels unitaires, pas la latence de bout en bout de l'API (réseau et frontend exclus).
- Ne pas affirmer que les templates ont été fabriqués à partir de la cible : c'est une hypothèse de risque, pas un fait.
- Ne pas qualifier de « déterministe » le lien templates/cible : aucune modalité n'est pure à 100 %.
- Données et captures : dossiers fictifs uniquement, aucune donnée personnelle réelle.

### Formulations à éviter

- « La forêt repère environ 5 cas à risque de plus sur 90 » : les finalistes sont comparés sur 72 cas de classe 2, pas sur les 90 du test.
- « Une erreur grave sur dix persiste malgré les alertes humaines » : mélange le taux brut (9/90) et le signalement par le filet (4 sur 9). Un signalement n'est pas une correction.
- « Le conseiller garde la main sur chaque décision » : responsabilité prévue, pas contrôle opérationnel démontré.
- « Des indicateurs pour détecter les dérives et préserver la qualité » : on supervise des distributions, mais ni alerting automatique ni maintien de qualité ne sont démontrés.
- « Réserve d'équité levée » : les petits effectifs ne permettent pas cette conclusion.
- Toute phrase suggérant que « retenu pour le prototype » vaut « conforme aux critères de mise en service ».

### Un seul seuil de revue dans le récit

Dans le récit : **A = 0,40 / B = 0,20 (servi)**, soit 128/500 dossiers signalés et 4 erreurs graves signalées sur 9. **B = 0,15** (recommandé hors ligne) est mentionné en **une phrase** comme piste à arbitrer avec le métier, détail en annexe A4.

---

## 2. Vue d'ensemble minutée

| # | Section | Slide | Durée | Créneau | Compétences | Phrase-pivot |
|---|---|---|---:|---|---|---|
| 1 | Comprendre | Question directrice, profil, trajectoire | 1:30 | 00:00-01:30 | CT6, CT7 | « Orienter, sans décider à la place » |
| 2 | Comprendre | Besoin métier, conseiller, trois classes | 1:30 | 01:30-03:00 | C1 | « Du dossier à l'accompagnement » |
| 3 | Comprendre | Risque prioritaire, critères, limites majeures | 1:30 | 03:00-04:30 | C2, C4 | Une erreur grave peut retarder un accompagnement nécessaire : je fixe les critères avant de montrer les résultats. |
| 4 | Explorer | Données et neuf templates | 2:30 | 04:30-07:00 | C1, C3 | « Les commentaires ne sont pas libres : 9 formulations types » |
| 5 | Explorer | Préparation et prévention des fuites | 1:30 | 07:00-08:30 | C3 | « Préparer sans contaminer l'évaluation » |
| 6 | Évaluer | Scénarios, modèles, protocole | 2:30 | 08:30-11:00 | C4, C5 | Le texte seul ne suffit pas, le tabulaire seul manque des cas. |
| 7 | Évaluer | Choix du prototype et compromis | 2:00 | 11:00-13:00 | C4 | « Le meilleur score ne suffit pas à justifier un déploiement » |
| 8 | Évaluer | Résultats finaux et lecture des erreurs | 2:30 | 13:00-15:30 | C8 | « 53 cas de classe 2 repérés sur 90 » |
| 9 | Encadrer | Revue humaine : bénéfice et coût | 2:00 | 15:30-17:30 | C2, C8 | « Les seuils de revue sont des choix de conception à valider avec le métier » |
| 10 | Encadrer | Explicabilité et équité | 1:30 | 17:30-19:00 | C2, C8 | « Les écarts entre profils restent préoccupants et incertains » |
| 11 | Encadrer | Éthique, conformité, nationalité | 1:30 | 19:00-20:30 | C2 | La conformité conditionne le déploiement, elle ne le suit pas. |
| 12 | Industrialiser | Reproduire : architecture et preuves | 2:00 | 20:30-22:30 | C6, C7 | « Une architecture industrialisée ne vaut pas autorisation de mise en service » |
| 13 | Industrialiser | Interface, supervision, feedback | 2:00 | 22:30-24:30 | C6, C8, C9 | « Les nouvelles données servent à entraîner un candidat, pas à remplacer le modèle » |
| 14 | Décider | Retour d'expérience | 3:00 | 24:30-27:30 | C9, CT6 | Trois difficultés, trois apprentissages. |
| 15 | Décider | Verdict, préconisations, recul | 1:30 | 27:30-29:00 | C9, CT6 | « Prototype industrialisé, pas de mise en production décisionnelle à ce stade » |
| | **Total** | | **29:00** | | | **1 min de réserve** |

Règle de densité : par slide, **un message central, trois éléments visibles maximum, une limite importante**. Les listes « à dire » ci-dessous sont une réserve, pas un texte à recopier. Au maximum une punchline par slide.

---

## 3. Déroulé slide par slide

Chaque slide donne : objectif, à afficher, à dire, limite, recul le cas échéant, questions probables du jury avec réponse courte.

### Section 1 - Comprendre

#### Slide 1 - Question directrice et trajectoire (1:30 | 00:00-01:30)

**Objectif** : donner au jury une question directrice et annoncer une présentation centrée sur les décisions prises, pas sur une succession d'outils.

**À afficher** : titre du cas d'usage, identité, contexte de certification ; question directrice ; frise « besoin -> expérimentation -> prototype -> décision de déploiement ». Pas de capture technique.

**À dire** :
- Votre point de départ face à l'IA, en 20 à 30 secondes, à renseigner sans inventer de biographie ; relier cette trajectoire à ce que le projet vous a appris.
- La finalité : aide à l'accompagnement des demandeurs d'emploi.
- Le plan en six temps (bandeau) et la réponse annoncée : aide oui, décideur non.
- Les résultats et leurs limites seront présentés ensemble.

**Limite** : le jeu est qualifié de synthétique dans le notebook ; la soutenance ne démontre aucune efficacité constatée auprès de vrais usagers.

**Questions probables** :
- *Quel problème précis résolvez-vous ?* Orienter plus tôt vers un accompagnement adapté les demandeurs d'emploi susceptibles de rester longtemps sans emploi, sans que la machine décide.
- *Qu'avez-vous réalisé personnellement, quel périmètre ?* À préparer précisément : cadrage, exploration, modélisation, évaluation, audit, industrialisation du prototype ; sans validation métier réelle.

**Punchline** : « Orienter, sans décider à la place ».

#### Slide 2 - Besoin métier et place du conseiller (1:30 | 01:30-03:00) - C1

**Objectif** : relier la sortie du modèle à une action métier compréhensible et délimiter ce que le système ne doit pas décider.

**À afficher** : schéma du parcours d'un dossier (de l'entretien à l'orientation) ; trois classes en langage usager : **0** retour rapide (avant 6 mois), **1** retour moyen (6 à 12 mois), **2** risque de longue durée (au-delà de 12 mois).

**À dire** :
- La sortie est une classe de délai estimée, pas une date exacte.
- Le conseiller conserve la responsabilité de l'orientation ; aucun refus automatique de droits ou de prestations.
- Réserve sur les labels : le sujet évoque une décision de parcours ou un constat terrain validé par les conseillers. On ne présume pas que chaque label correspond à un délai observé ; c'est à vérifier avant d'interpréter la prédiction comme un pronostic de retour à l'emploi.

**Limite** : les classes réduisent une situation sociale complexe ; la disponibilité des ressources d'accompagnement et le bénéfice réel de la priorisation ne sont pas validés sur le terrain.

**Questions probables** :
- *Pourquoi une classification plutôt qu'une régression du délai ?* Le besoin métier est d'orienter vers un niveau d'accompagnement (trois paliers d'action), pas de prédire un nombre de jours ; les labels disponibles sont des classes.
- *Comment éviter d'enfermer la personne dans une catégorie ?* La classe est une aide à la priorisation, le conseiller décide et peut passer outre ; la contestation et le réexamen doivent être prévus (voir slide 11).
- *Quel bénéfice concret pour le conseiller ?* Repérer plus tôt les dossiers à risque pour mobiliser un accompagnement renforcé ; bénéfice non mesuré sur le terrain.

**Punchline** : « Du dossier à l'accompagnement ».

#### Slide 3 - Risque prioritaire, critères, limites majeures (1:30 | 03:00-04:30) - C2, C4

**Objectif** : expliquer pourquoi une bonne accuracy ne suffit pas, fixer les critères avant de montrer les résultats, et annoncer les limites.

**À afficher** : deux exemples fictifs d'erreurs (2 vers 0, personne à risque qui ne reçoit pas l'accompagnement renforcé ; 0 vers 2, ressources mobilisées à tort) ; grille compacte des cibles :
- rappel classe 2 ≥ 0,80 ;
- F1 classe 2 ≥ 0,60 ;
- erreur grave (2 prédit 0) < 5 % des vrais cas de classe 2 ;
- part de dossiers en revue ≤ 15 % ;
- écart de rappel entre groupes < 10 points, sur effectifs suffisants.
Complémentaires, pas des preuves de sécurité : accuracy ≥ 70 % (erreur globale ≤ 30 %), F1 macro ≥ 0,65.

**À dire** :
- La matrice de coûts traduit l'asymétrie métier en pénalités comparables (erreur 2 vers 0 plus coûteuse que 0 vers 2). Montants et seuils sont des **hypothèses**, faute d'échange possible avec le métier.
- Le terme historique « abstention » désigne ici l'envoi en revue : le modèle produit toujours une prédiction.
- Annoncer les cinq limites majeures en une phrase chacune.

**Limite** : seuils et coûts à confirmer avec le métier.

**Questions probables** :
- *Qui a fixé ces seuils et pourquoi ?* Moi, comme hypothèses de travail, à partir du risque identifié (perte de chance) et de la capacité de revue supposée ; à arbitrer avec le métier.
- *Quel est le dénominateur du taux d'erreur grave ?* Le nombre de vrais cas de classe 2 (90 sur le test), pas les 500 dossiers.
- *Comment arbitrer sécurité contre charge de revue ?* Plus on signale de dossiers, plus on protège mais plus on surcharge ; c'est le compromis des slides 9 et 15.

**Punchline** : « Une erreur grave peut retarder un accompagnement nécessaire » (dommage possible, non observé dans l'étude).

### Section 2 - Explorer

#### Slide 4 - Données et neuf templates (2:30 | 04:30-07:00) - C1, C3

**Objectif** : montrer que l'exploration a conditionné la suite du projet et justifier l'absence de NLP en production.

**À afficher** :
- Volume : **2 500 dossiers, 10 colonnes** (identifiant, cible, données de profil, synthèse d'entretien). Répartition de la cible : classe 0 environ 37,4 %, classe 1 44,5 %, classe 2 18,1 %.
- Comptage des textes : **2 419 synthèses renseignées, 9 formulations uniques, 81 manquantes**, avec deux ou trois exemples.
- Schéma « 9 templates -> famille thématique (+ `texte_manquant`) -> encodage catégoriel ».
- Pas de dossiers identifiants.

**À dire** :
- Contrôles : pas de doublons, manquants limités ; anciennetés atypiques mais plausibles conservées (détail en annexe).
- Variables à risque : âge, diplôme, territoire, nationalité, informations indirectes dans la synthèse.
- Démarche en quatre temps : texte libre supposé -> neuf templates constatés -> variable catégorielle -> comparaison avant/après sur les **mêmes plis** : suppression de TF-IDF et de la couche NLP, sans dégradation observée (F1 macro moyen +0,004, rappel classe 2 moyen +0,006, scénario texte seul inchangé).
- Un modèle de langue zero-shot local a servi **une seule fois** pour étiqueter les neuf textes ; le référentiel est figé dans un CSV avec mapping déterministe. Aucun modèle de langue n'est appelé à chaque prédiction.
- Les templates sont fortement associés à la cible, sans être purs à 100 %.

**Limites** : signal très propre pouvant rendre les performances optimistes, sans preuve de son procédé de fabrication ; le sujet envisageait une approche NLP sur texte bruité, cette robustesse n'a pas été évaluée sur de vrais verbatims ; les familles doivent être validées par le métier avant tout usage réel. Volume modeste, associations non causales.

**Recul (difficulté 1)** : le sujet annonçait du NLP, la donnée a imposé autre chose ; j'ai adapté la méthode à la donnée, pas l'inverse.

**Questions probables** :
- *Le projet est-il réellement multimodal ?* Non : tabulaire + une variable catégorielle dérivée du texte. Je le dis clairement.
- *Pourquoi un zero-shot pour neuf textes ?* Pour étiqueter rapidement et de façon reproductible les familles ; une fois le référentiel figé, plus aucun appel.
- *Et avec une nouvelle formulation d'entretien ?* Elle tomberait hors référentiel : texte inconnu à traiter explicitement (catégorie dédiée ou escalade) ; non évalué.
- *Fuite de cible ou artefact de génération ?* Je ne peux pas trancher : aucune mention explicite de la cible dans les textes, mais le risque d'artefact subsiste ; c'est une hypothèse de risque à lever avec le fournisseur des données.
- *Comment savoir que les données représentent les futurs usagers ?* On ne le sait pas ; c'est la limite 1.
- *Pourquoi conserver les valeurs aberrantes ?* Plausibles métier ; les supprimer aurait retiré des cas réels.
- *Les manquants portent-ils un biais ?* Possible ; 81 textes manquants traités par une catégorie explicite, à surveiller.

**Punchline** : « Les commentaires ne sont pas libres : 9 formulations types ».

#### Slide 5 - Préparation et prévention des fuites (1:30 | 07:00-08:30) - C3

**Objectif** : rendre l'évaluation crédible en montrant comment le prétraitement est séparé de l'évaluation.

**À afficher** : un seul schéma des partitions : split stratifié 80/20, **2 000 dossiers d'entraînement / 500 de test final**, puis second split 80/20 dans les 2 000 : **1 600 de sous-train / 400 de sous-validation** (arbitrage entre finalistes, sans toucher le test final). Les transformations apprises sont ajustées sur chaque train, jamais sur le test.

**À dire** :
- Pipeline unique : imputation, encodage catégoriel, estimateur.
- Identifiant retiré ; code commune agrégé au département.
- Graine fixée (`random_state=42`) : l'essai est rejouable, pas statistiquement plus fiable.
- Correction du protocole : le journal rapporte un usage anticipé de `X_test` ; les étapes ont ensuite été séparées. Je ne revendique pas un test historiquement vierge.

**Limites** : split aléatoire stratifié, pas de généralisation temporelle ou à une autre agence ; agréger le territoire réduit sa granularité sans supprimer son caractère de proxy.

**Recul (difficulté 2)** : relever moi-même l'usage anticipé de `X_test`, le documenter et séparer les protocoles, plutôt que de le masquer.

**Questions probables** :
- *Où une fuite aurait-elle pu se produire ?* Dans l'ajustement des transformations sur toutes les données, dans le choix de variantes sur le test, et dans les features dérivées de la cible ; chaque point est traité par le pipeline unique et la séparation des partitions.
- *Pourquoi pas un split temporel ?* Non réalisé : un split aléatoire a été retenu (à justifier selon les données disponibles) ; limite reconnue.
- *Catégories inconnues ?* L'encodeur est configuré pour les gérer sans erreur ; à vérifier en annexe A3.

**Punchline** : « Préparer sans contaminer l'évaluation » (décrit l'objectif du protocole corrigé, pas une absence historique de fuite).

### Section 3 - Évaluer

#### Slide 6 - Scénarios, modèles, protocole (2:30 | 08:30-11:00) - C4, C5

**Objectif** : montrer que les scénarios testent des hypothèses, justifier le choix du ML classique et la méthode de comparaison.

**À afficher** :
- Grille « scénario / question / conclusion courte » :
  - **S1** données complètes avec famille : apport conjoint des sources -> combine les sources ;
  - **S2** retrait des variables à risque désignées : effet du retrait -> dégrade les résultats observés sans garantir l'équité ;
  - **S3** famille seule : valeur de l'entretien seul -> ne suffit pas ;
  - **S4** sous-ensemble tabulaire sans famille : niveau du tabulaire seul. Le témoin **S4-all** reprend les sept variables de S1 sans la famille et isole l'apport de celle-ci -> réduit les erreurs graves mais détecte moins de cas à risque.
- Trois modèles : régression logistique, Random Forest, HistGradientBoosting (HGB), chacun avec une raison courte.
- Schéma du protocole : CV stratifiée à 5 plis sur le train -> sous-validation des finalistes -> test final du modèle retenu.

**À dire** :
- Rejet de S3 (CV 5 plis du train, légende « CV train ») : rappel classe 2 de 0,660 mais **19,1 % d'erreurs graves**. Pour S2, meilleur F1 macro des configurations rapportées : 0,628 avec 18,5 % d'erreurs graves ; ne pas attribuer cette dégradation à une variable précise (plusieurs variables retirées ensemble).
- Apport de la famille, en sous-validation avec une même configuration RF 300 arbres : S1 rappel 0,681 et erreur grave 9,7 %, contre S4-all 0,514 et 4,2 %. C'est un compromis, pas un gain sur tous les critères. Ne pas mélanger ces valeurs avec les chiffres CV de S2/S3.
- `class_weight="balanced"` : poids inversement liés aux fréquences observées, sans ajout de dossiers ni garantie d'équité entre groupes ; à distinguer d'un poids ciblé sur la classe 2.
- Essais de pondération et d'hyperparamètres résumés, sans inventaire.
- Exclusion de LLM, RAG, agents et deep learning : sortie structurée, données modestes, aucun besoin de génération ni de recherche documentaire.

**Limites** : une seule famille d'approches explorée (les trois estimateurs ne sont pas trois familles technologiques) ; recherche d'hyperparamètres non exhaustive ; S2 ne garantit pas l'absence de biais (proxys) ; le test ne sert pas à choisir les variantes.

**Questions probables** :
- *Pourquoi ces modèles plutôt que XGBoost ou un réseau de neurones ?* Données tabulaires modestes ; trois estimateurs classiques suffisent à poser le compromis ; extension possible, non réalisée.
- *Pourquoi cinq plis plutôt que dix ?* Compromis entre stabilité et coût de calcul sur 2 000 dossiers ; pas d'étude de sensibilité.
- *Pourquoi pas un GridSearch exhaustif ?* Choix de ciblage sur les leviers qui touchent l'erreur grave ; recherche non exhaustive reconnue.
- *Quand un LLM deviendrait-il pertinent ?* Avec de vrais verbatims libres et bruités à interpréter, et une validation métier de leur usage.
- *Pourquoi retirer des variables ne garantit-il pas l'équité ?* Des proxys (territoire, diplôme, texte) peuvent subsister.
- *Quelle différence entre S4 et S4-all ?* S4-all garde exactement les sept variables de S1, sauf la famille : seul témoin qui isole son apport.
- *Comment isoler l'effet de la nationalité ?* Ablation dédiée « S1 sans nationalité » (annexe A5) : résultats limités, pas de bénéfice causal démontré.

#### Slide 7 - Choix du prototype et compromis (2:00 | 11:00-13:00) - C4

**Objectif** : expliquer un arbitrage multicritère et distinguer sélection expérimentale et validation pour la production.

**À afficher** : tableau homogène de trois finalistes S1, **sous-validation sur 400 dossiers dont 72 de classe 2** (légende obligatoire), colonnes rappel classe 2 / erreur grave / F1 macro / taille :

| Finalistes (S1) | Rappel classe 2 | Erreur grave | F1 macro | Taille |
|---|---:|---:|---:|---:|
| RF 300 arbres, `class_weight="balanced"`, `random_state=42` | 0,681 | 9,7 % | 0,703 | 27,5 Mo |
| HGB balanced, profondeur 10 | 0,625 | 8,3 % | 0,683 | 0,806 Mo |
| HGB, poids de classe 2 renforcé | 0,556 | 12,5 % | 0,671 | 1,057 Mo |

Mettre en évidence les gains et les contreparties de RF. Pas de capture brute d'un tableau mélangeant des protocoles.

**À dire** :
- Le choix s'appuie sur les métriques prioritaires en sous-validation, pas seulement sur l'accuracy ou le meilleur F1 macro en CV.
- RF contre HGB balanced : rappel 0,681 contre 0,625 et F1 0,703 contre 0,683, mais erreur grave 9,7 % contre 8,3 % et modèle plus lourd. **RF ne domine pas toutes les métriques prioritaires** : la priorité arbitrée (rappel) reste à valider avec le métier.
- Un rappel plus élevé n'est pas « cinq cas de plus sur 90 » : on compare sur 72 cas.
- Coûts incomplets (valeur manquante pour RF dans l'export) et latences issues de campagnes différentes exclus du tableau ; les coûts restent des hypothèses.
- « Retenu pour le prototype » ne signifie pas « conforme aux critères de mise en service ».

**Limites** : aucune configuration testée n'atteint simultanément les exigences prioritaires ; une pondération plus forte de la classe 2 ne résout pas mécaniquement l'erreur 2 vers 0.

**Questions probables** :
- *Pourquoi retenir un modèle qui ne satisfait pas les seuils ?* C'est une sélection expérimentale entre candidats, pas une validation ; d'où le verdict final « pas de mise en production ».
- *Pourquoi pas le modèle le plus sobre (HGB) ?* Il est meilleur sur l'erreur grave et plus de 30 fois plus léger (0,806 Mo contre 27,5 Mo) ; je privilégie le rappel, mais cette priorité est une hypothèse que le métier doit trancher, et HGB reste une option crédible.
- *Comment avez-vous détecté le problème d'implémentation de S1 ?* Voir slide 12.

**Punchline** : « Le meilleur score ne suffit pas à justifier un déploiement ».

#### Slide 8 - Résultats finaux et lecture des erreurs (2:30 | 13:00-15:30) - C8

**Objectif** : transformer les scores en conséquences compréhensibles et confronter les résultats aux cibles.

**À afficher** : matrice de confusion du test final de 500 dossiers (lignes « réel », colonnes « prédit »), annotée :

```
            prédit 0  prédit 1  prédit 2
réel 0        142        36         9
réel 1         27       162        34
réel 2          9        28        53
```

Tableau « atteint / non atteint » face aux cibles.

**À dire** :
- Accuracy 71,4 %, F1 macro 0,690, rappel classe 2 0,589, F1 classe 2 0,570.
- Sur les **90 cas réels de classe 2** : 53 détectés, 28 prédits en classe 1, **9 prédits en classe 0**.
- Erreur grave : **9/90 = 10 %, et non 9/500**. Erreurs 0 vers 2, suivies séparément : 9/187, soit environ 4,8 %.
- Bilan : performance globale satisfaisante (accuracy 71,4 % ≥ 70 %, erreur globale 28,6 % ≤ 30 %, F1 macro 0,690 ≥ 0,65) ; critères sur la classe 2 **non atteints** : rappel 0,589 (cible ≥ 0,80), erreur grave 10,0 % (cible < 5 %), F1 classe 2 0,570 (cible ≥ 0,60, juste sous la cible). Revue à 25,6 % contre 15 % maximum : non atteint.

**Limites** : 90 cas de classe 2 seulement ; incertitude statistique, pas d'intervalle de confiance calculé, pas de validation externe. Les probabilités ne sont ni une certitude individuelle ni une calibration démontrée.

**Questions probables** :
- *Pourquoi 71,4 % ne suffit-il pas ?* Il masque que la classe la plus à risque est la moins bien détectée (rappel 0,589).
- *Différence rappel / précision / F1 ?* Rappel : part des vrais cas de classe 2 détectés (53/90). Précision : part des prédits classe 2 qui sont justes. F1 : moyenne harmonique des deux.
- *Intervalles de confiance, calibration ?* Non réalisés ; priorité d'une évaluation indépendante.
- *Pourquoi ne pas traiter toutes les erreurs pareil ?* Leur coût métier diffère : 2 vers 0 prive d'accompagnement, 0 vers 2 mobilise des ressources en trop.

**Punchline** : « Sur le test final : 53 cas de classe 2 repérés sur 90 » (préférer l'effectif au « 59 % » seul ; montrer aussi les neuf erreurs graves).

### Section 4 - Encadrer

#### Slide 9 - Revue humaine : bénéfice et coût (2:00 | 15:30-17:30) - C2, C8

**Objectif** : évaluer le contrôle humain comme un mécanisme mesurable, pas comme une garantie abstraite.

**À afficher** : arbre des deux règles servies ; schéma des 9 erreurs graves (4 signalées, 5 non signalées) ; chiffre **128/500 = 25,6 % en revue, contre 15 % maximum**.
- Règle A : revue si P(classe 2) ≥ 0,40, quelle que soit la classe prédite.
- Règle B : revue si classe prédite 0 et P(classe 2) ≥ 0,20.

**À dire** :
- Protection partielle : **4 des 9 erreurs graves signalées, 5 non signalées**. Ce chiffre concerne le filet servi à B = 0,20, pas toutes les variantes exploratoires.
- Signalé pour revue ne veut pas dire corrigé. Coût illustratif : 20 euros par revue, hypothèse de correction humaine parfaite.
- Une phrase sur la piste B = 0,15 : en sous-validation, 5 erreurs graves sur 7 signalées mais 33,0 % des dossiers en revue, au-dessus du plafond de 15 % ; recommandation hors ligne, non réexportée, pas un feu vert.
- A, B, coût de revue et délais sont des choix de conception faute d'interlocuteur métier ; ce qu'on aurait arbitré avec lui : capacité de revue, coût d'une erreur, délai de traitement.

**Limites** : filet incomplet, charge excessive, capacité métier non validée, risque d'erreur humaine et de biais d'automatisation. B = 0,15 n'est pas un routage actuellement assuré par l'API. La revue ciblée ne remplace pas la responsabilité du conseiller sur l'orientation de tous les dossiers. Les délais de revue sont des règles d'organisation envisagées, pas des engagements éprouvés.

**Questions probables** :
- *Pourquoi ne pas tout envoyer en revue ?* Cela annulerait l'intérêt de l'outil et dépasserait la capacité supposée des conseillers.
- *Que signifie `auto` dans l'API ?* Statut technique « pas de revue déclenchée », pas une décision administrative automatique.
- *Comment fixer les seuils et mesurer la capacité ?* Avec le métier, sur des données distinctes, en comparant sécurité, équité et charge ; ici hypothèses.
- *Que deviennent les cinq erreurs graves non signalées ?* Elles échappent au filet : c'est une raison majeure du verdict négatif.

**Punchline** : « Les seuils de revue sont des choix de conception à valider avec le métier ».

#### Slide 10 - Explicabilité et équité (1:30 | 17:30-19:00) - C2, C8

**Objectif** : séparer compréhension globale du modèle, justification individuelle et évaluation des écarts entre groupes.

**À afficher** : importance par permutation réduite aux principales variables (rôle de la famille thématique) ; **un seul** exemple d'audit : UE, 37/70 cas de classe 2 détectés (rappel 0,529) ; hors UE, 16/20 (0,800) ; écart d'environ 27 points ; avertissement visible « groupe insuffisant ».

**À dire** :
- Permutation (calculée sur le jeu de test, à signaler) : mélanger une variable et mesurer la baisse du score ; l'importance n'est pas une causalité et des variables corrélées peuvent masquer ou partager leur importance.
- Avertissement pour les groupes sous 30 cas de classe 2 ; ce repère ne garantit pas une puissance statistique suffisante.
- Distinguer écarts de répartition des classes dans les données et écarts de rappel du modèle : ce ne sont pas les mêmes mesures (détail en annexe A5).

**Limites** : explication globale seulement, pas d'attribution locale (SHAP non réalisé) ; écarts instables sur petits groupes, aucune conclusion robuste ; une bonne moyenne ne démontre pas une protection équivalente pour tous.

**Questions probables** :
- *Comment expliquer une prédiction à un conseiller ?* Aujourd'hui : classe, probabilités et raison de revue. Pas d'explication locale ; piste d'amélioration.
- *Peut-on parler de discrimination ?* Non, les effectifs ne le permettent pas ; signal préoccupant à vérifier.
- *Quelle définition d'équité ?* Égalité des rappels entre groupes (écart < 10 points) car l'erreur la plus grave est de rater un cas de classe 2.
- *Comment améliorer l'audit ?* Plus de données par groupe, intervalles de confiance, audit récurrent après mise en service.

**Punchline** : « Les écarts entre profils restent préoccupants et incertains ».

#### Slide 11 - Éthique, conformité, nationalité (1:30 | 19:00-20:30) - C2

**Objectif** : montrer que conformité et non-discrimination conditionnent le déploiement, sans présenter l'analyse comme une validation juridique.

**À afficher** : grille « risque / mesure / validation restante », extrait de l'arbitrage sur la nationalité, sans donnée personnelle.

**À dire** :
- Minimisation : identifiant retiré des features, territoire agrégé, aucun verbatim brut dans l'API, restrictions de logs et de tableaux de bord.
- Base légale envisagée : mission d'intérêt public, à valider ; la nationalité n'est pas une catégorie particulière au sens de l'article 9 du RGPD, mais reste sensible.
- `nationalite_hors_ue` : maintien **conditionnel et réversible**, avec ablation dédiée aux résultats limités, sans prétendre démontrer un bénéfice causal. Aucune validation métier de cet usage n'a été obtenue ; la validation et les alternatives que j'aurais demandées sont à présenter.
- Conditions de mise en service : audit récurrent, revue de gouvernance en cas de dégradation, information et droits des personnes, AIPD et registre validés.
- L'erreur 2 vers 0 peut causer une perte de chance d'accompagnement : préciser qui réexamine l'orientation, traite une contestation et trace la responsabilité. L'intervention d'un conseiller n'efface pas automatiquement la responsabilité de l'organisation ou de l'éditeur.
- Qualification probable à haut risque au titre de l'AI Act, à confirmer selon la finalité réelle. Interdiction de transformer ce prototype en décision automatique à fort impact.

**Limites** : aucune autorisation juridique définitive ; retirer une variable ne supprime pas ses proxys ; convertir le texte en catégorie n'anonymise pas le dossier ; l'intervention humaine doit être réelle, pas une validation de façade.

**Questions probables** :
- *Pourquoi conserver la nationalité hors UE ?* Hypothèse de travail pour mesurer son apport et ses effets ; réversible, soumise à validation métier et juridique ; à retirer si non justifiée.
- *Qui valide l'AIPD et l'arbitrage ?* DPO et direction métier ; livrables non produits à ce stade.
- *Que peut contester un usager ?* L'orientation retenue et l'usage de ses données, via un circuit à définir (information, accès, contestation).
- *Entre-t-on dans les décisions automatisées du RGPD ?* Pas tant qu'un conseiller décide réellement ; une revue de façade changerait l'analyse.

### Section 5 - Industrialiser

#### Slide 12 - Reproduire : architecture et preuves (2:00 | 20:30-22:30) - C6, C7

**Objectif** : montrer le passage du notebook à un service reproductible, sans confondre stack du prototype et production complète.

**À afficher** : schéma simplifié (interface conseiller -> backend -> API modèle ; service feedback séparé ; supervision Prometheus/Grafana) ; capture d'une CI réussie ; extrait des métadonnées du modèle ; historique minimal des inférences en SQLite, avec en pointillé le raccordement features/feedbacks restant à compléter.

**À dire** :
- **Quatre services applicatifs dockerisés** : frontend, backend, modèle, feedback ; la supervision est un composant additionnel.
- Chaîne hors ligne : entraînement, pipeline persisté avec métadonnées, contrôle qualité, export contrôlé du modèle servi.
- Preuve centrale : **golden run** et contrôle du modèle exporté, appuyés par une CI réussie.
- Correction concrète : documentation de S1 complète mais features textuelles absentes à l'implémentation -> détectées -> scénario corrigé et témoin S4-all -> contrôles de cohérence entre configuration, modèle évalué et modèle servi. Une trace existe ; elle ne prouve pas à elle seule toute la qualité.
- Légende : p95 = 50,1 ms (p50 = 27,3 ms) sur le pipeline final, 1 000 appels unitaires, pas la latence de l'API ; cible p95 < 200 ms tenue sur le pipeline, à reconfirmer de bout en bout.
- Point de vigilance sur les seuils : l'artefact de l'API (version v3.0.0) porte B = 0,20, mais les métadonnées du modèle exporté par le notebook portent B = 0,15. Savoir expliquer cet écart si le jury interroge la cohérence servi/évalué : B = 0,20 est le réglage réellement servi, B = 0,15 la recommandation non promue. Autre limite : l'empreinte (hash) du jeu de données n'est pas renseignée dans les métadonnées servies.

**Limites** : stack locale, aucun déploiement distant démontré ; publier ou retagger des images ne prouve pas un déploiement sur l'infrastructure cible. Restent : intégration au référentiel national des usagers, choix on-premise ou cloud souverain, dimensionnement CPU/RAM, mesures de charge et de latence de bout en bout, coût réel, empreinte carbone, règles d'accès et de conservation (détail en annexe A7).

**Recul (difficulté 3)** : un scénario documenté mais pas implémenté comme décrit ; trouvé grâce aux contrôles de cohérence.

**Questions probables** :
- *Comment garantir que le modèle servi est celui évalué ?* Métadonnées du modèle exporté, contrôles de cohérence et golden run comparent configuration, évaluation et artefact servi.
- *Que teste le golden run ?* Qu'un jeu d'entrées de référence redonne les mêmes sorties avec le modèle exporté.
- *Panne ou retour arrière ?* Versions de modèle tracées (version dans l'historique) ; procédure de retour arrière à formaliser, non éprouvée.
- *Les 50,1 ms incluent-ils réseau et frontend ?* Non.

**Punchline** : « Une architecture industrialisée ne vaut pas autorisation de mise en service ».

#### Slide 13 - Interface, supervision, feedback (2:00 | 22:30-24:30) - C6, C8, C9

**Objectif** : montrer comment les choix se traduisent dans l'interface et décrire ce qui est surveillable tout de suite et ce qui exige des labels différés.

**À afficher** : deux captures annotées d'un dossier fictif (formulaire d'entrée ; résultat `a_valider` avec classe, probabilités et raison de revue) ; capture recadrée du tableau de bord ; schéma de la boucle **entraîner un candidat -> évaluer -> accepter ou rejeter -> promouvoir sous contrôle humain**, étapes manuelles marquées.

**À dire** :
- `auto` est un statut technique, pas une décision métier. Action attendue du conseiller et lien au `request_id`.
- Trois niveaux : supervision technique (disponibilité, erreurs HTTP, latence), distributions entrées/sorties (classes prédites, familles), qualité prédictive (nécessite une vérité terrain).
- Réalisé : feedbacks persistés ; historique des inférences exposé par `/history` (`request_id`, classe prédite, probabilité, version, date). Les features d'entrée n'y figurent pas : il ne suffit pas à alimenter seul audit et réentraînement. Feedbacks d'exemple simulés.
- Distinguer annotation du conseiller, décision de parcours et délai réellement observé : un résultat temporel exige un suivi ; la nature, la date et la validation du label sont à définir pour ne pas entraîner le modèle sur sa propre recommandation.
- Réentraînement lancé **manuellement** par script à partir de feedbacks validés (cadence hebdomadaire et seuil de 100 feedbacks envisagés, sans garantie d'effectif suffisant par classe ou groupe). Les données nouvelles servent à entraîner un candidat ; le modèle servi n'est jamais remplacé automatiquement.
- Escalade humaine à concevoir pour situations inhabituelles ou anomalies : accompagnement poursuivi hors outil, transmission au référent métier ou technique ; circuit, déclencheurs et responsabilités à définir ; aucune détection automatique de cas hors distribution.
- Réexamen des seuils si charge ou erreurs évoluent : sécurité, équité et capacité examinées avec le métier, évaluation sur données distinctes, promotion explicite. Jamais de relèvement automatique d'un seuil pour réduire la charge.

**Limites** : boucle non éprouvée avec de vrais retours ; raccordement inférences/features/feedbacks à finaliser ; pas d'alerting automatique ni d'ordonnanceur ; PSI non implémenté, pas de score de nouveauté ni de calibration, pas de route API de réentraînement ; labels possiblement retardés ou biaisés ; interface de prototype dont l'utilisabilité terrain n'est pas prouvée ; jeu de référence réutilisé, validation indépendante requise.

**Questions probables** :
- *Détecter une baisse de performance sans labels ?* Seulement des signaux indirects (dérive de distributions) ; la qualité exige des labels.
- *Qui reçoit une alerte aujourd'hui ?* Personne : pas d'alerting automatique.
- *Pourquoi 100 feedbacks, et le biais de sélection ?* Seuil pragmatique, insuffisant seul ; le biais de sélection est à surveiller (retours non représentatifs).
- *Un candidat accepté remplace-t-il le modèle ?* Non, promotion explicite sous contrôle humain.
- *Que faire si un feedback en contredit un autre ?* Règle de résolution à définir (priorité à la validation par un référent) ; non implémentée.
- *Peut-on rejouer une prédiction avec la même version ?* Oui en principe : `request_id`, version enregistrée ; sans features stockées, il faut les redemander.

**Punchline** : « Les nouvelles données servent à entraîner un candidat, pas à remplacer le modèle ».

### Section 6 - Décider

#### Slide 14 - Retour d'expérience (3:00 | 24:30-27:30) - C9, CT6

**Objectif** : donner au jury la prise de recul sur la démarche : difficultés, corrections, ce que je ferais autrement.

**À afficher** : tableau « difficulté / ce que j'ai fait / ce que je ferais autrement » :

| Difficulté | Ce que j'ai fait | Ce que je ferais autrement |
|---|---|---|
| Données trop propres : texte réduit à 9 templates, provenance floue | Suppression du NLP, variable catégorielle, comparaison avant/après sur mêmes plis, réserve explicite | Demander dès le cadrage le procédé de génération et tester une robustesse sur des textes bruités |
| Usage anticipé de `X_test` | Séparation train / sous-validation / test, correction documentée | Figer le protocole et le jeu de test avant toute exploration |
| Scénario S1 non conforme à sa documentation | Détection, correction, témoin S4-all, contrôles de cohérence | Mettre les contrôles de cohérence en place dès la première itération |
| Aucun échange métier possible | Hypothèses explicites (coûts, seuils A/B, nationalité) | Faire arbitrer ces points avant de modéliser, avec la capacité de revue |

**À dire** (ce que j'ai compris, fait, repris, ferais autrement) :
- Compris : un bon score ne vaut pas sécurité ; le risque prioritaire se définit avant les résultats.
- Fait : un prototype reproductible, un filet de revue mesuré, un audit.
- Repris : trois corrections (données, protocole, S1) qui ont changé les conclusions ou leur crédibilité.
- Ferais autrement : le tableau ci-dessus.
- Apprentissage : démarche scientifique (formuler une hypothèse, la tester, reconnaître ses limites) et amélioration continue (rendre les corrections traçables).
- À confronter avec votre journal de bord pour n'affirmer que ce qui y est documenté.

**Limite** : exercice sans validation métier réelle ; le test a été consulté avant correction.

**Questions probables** :
- *Qu'auriez-vous fait autrement ?* Reprendre le tableau, en priorisant : protocole figé dès le départ, puis échange métier.
- *Quelle est votre plus grosse erreur ?* L'usage anticipé de `X_test` : il fragilise la valeur du chiffre final, d'où l'évaluation indépendante.

#### Slide 15 - Verdict, préconisations, recul (1:30 | 27:30-29:00) - C9, CT6

**Objectif** : conclure en langage client, avec trois messages, une feuille de route et une phrase de recul.

**À afficher** : trois blocs « démontré / non autorisé / conditions pour réexaminer », puis feuille de route en trois priorités. Pas de nouvelle capture technique.

**À dire** :
- **Message 1, ce que le prototype démontre** : une chaîne technique reproductible et un compromis de classification mesuré sur le jeu fourni ; ni bénéfice terrain établi ni décideur autonome.
- **Message 2, pourquoi je ne recommande pas la mise en service** : 9 erreurs graves sur le test, dont 5 non signalées par le filet servi ; charge de revue excessive ; équité non établie. Verdict : **pas de mise en production décisionnelle à ce stade**.
- **Message 3, ce qui permettrait de reconsidérer** : labels et données représentatifs, nouvelle évaluation indépendante, sécurité et capacité de revue validées avec le métier, audit d'équité concluant, validations DPO et direction métier. Un simple changement de seuil ne suffit pas.
- **Feuille de route priorisée** : 1) données et labels réels et représentatifs ; 2) arbitrage avec le métier (seuils, capacité de revue, nationalité) ; 3) évaluation indépendante, audit d'équité, validations DPO/direction.
- Terminer par **une phrase de recul personnel** en écho à la slide 1.

**Limites** : aucune promesse de seuil atteint après un simple réglage ; une CI verte, une interface fonctionnelle ou un filet humain partiel ne valent pas autorisation de déploiement.

**Questions probables** :
- *Déploieriez-vous ce système aujourd'hui ?* Non, pour les trois raisons du message 2.
- *Première priorité avec plus de temps ?* Obtenir des données et labels réels, car tout le reste en dépend.
- *Qu'est-ce qui vous ferait abandonner le cas d'usage ?* Une équité non atteignable, des labels non fiables, ou une capacité de revue incompatible avec la sécurité requise.

**Punchline** : « Prototype industrialisé, pas de mise en production décisionnelle à ce stade ».

---

## 4. Correspondance compétences / slides

| Compétence | Slides | Preuve principale |
|---|---|---|
| C1 Jeu de données | 2, 4 | Cohérence données/besoin, réserve de provenance |
| C2 Risques éthiques et cadre réglementaire | 3, 9, 10, 11 | Erreur 2 vers 0, nationalité, AIPD, AI Act |
| C3 Préparation des données | 4, 5 | Neuf templates, split, pipeline sans fuite |
| C4 Choix du modèle | 3, 6, 7 | Scénarios, finalistes, compromis RF/HGB |
| C5 Entraînement | 6 | CV 5 plis, pondération |
| C6 Implémentation | 12, 13 | Services, golden run, interface |
| C7 Architecture cible | 12 | Schéma, limites de déploiement |
| C8 Performance et impacts | 8, 9, 10, 13 | Matrice, taux d'erreur grave, supervision |
| C9 Amélioration continue | 13, 14, 15 | Boucle de feedback, retour d'expérience, feuille de route |
| CT6 Présenter au commanditaire | 1, 14, 15 | Messages en langage client, réponses aux questions |
| CT7 Posture face au jury | toute la soutenance | Reconnaissance des limites, réponses courtes |

Le questionnaire porte sur C1, C2 et C4 : maîtriser en priorité les slides 2 à 4, 6 à 7 et 9 à 11.

---

## 5. Gestion du temps et répétition

**Réserve : 1 minute.** Si le retard dépasse 1 minute, couper dans cet ordre :
1. slide 10 : ne garder que l'exemple UE / hors UE (30 s) ;
2. slide 13 : supprimer la capture du formulaire (30 s) ;
3. slide 6 : ne présenter que S3 et S4-all (1 min) ;
4. ne jamais couper les slides 8, 9, 14 et 15.

**Repères de passage** : slide 5 terminée à 08:30 ; slide 8 terminée à 15:30 ; slide 11 terminée à 20:30 ; slide 14 démarrée à 24:30.

**Répétition** : trois passages chronométrés (seul, devant un tiers, avec questions). Noter l'écart à chaque repère. Ne pas accélérer en lisant toutes les notes.

**Avant de figer le support** :
- Vérifier chaque chiffre contre le notebook et les artefacts (B = 0,15 recommandé et B = 0,20 servi, A = 0,40 inchangé).
- Vérifier les réserves de provenance et de labels ; vérifier la cohérence entre tableau comparatif, export des finalistes et messages au client ; ne pas transformer des données incomplètes en arguments de performance.
- Vérifier que chaque détail technique répond à une question du récit : compris, fait, repris, ferais autrement.
- Préparer un support autonome : aucune navigation dans l'application.

---

## 6. Questions transversales prioritaires (réponse en 20 secondes)

1. **Pourquoi garder la nationalité hors UE ?** Arbitrage conditionnel, réversible, non validé par le métier, avec ablation dédiée et audit récurrent.
2. **Pourquoi retenir RF alors qu'aucun seuil n'est atteint ?** Sélection expérimentale sur rappel et F1 en sous-validation ; HGB meilleur sur l'erreur grave ; aucune mise en service recommandée.
3. **Les données sont-elles réelles ?** Notebook : synthétiques ; sujet : collectées en agence ; procédé non documenté ; signal trop propre.
4. **Que feriez-vous autrement ?** Protocole figé dès le départ, échange métier avant de modéliser, contrôles de cohérence dès la première itération.
5. **Déploieriez-vous aujourd'hui ?** Non : 9 erreurs graves dont 5 non signalées, revue à 25,6 %, équité non établie.
6. **Que signifie `auto` ?** Statut technique de l'API, pas une décision administrative automatique.
7. **Le test est-il resté vierge ?** Non : usage anticipé documenté dans le journal, protocole corrigé ; évaluation indépendante nécessaire.

---

## 7. Annexes (hors temps, à ouvrir sur question)

**A1 - Métriques.** Rappel = vrais positifs / vrais cas de la classe. Précision = vrais positifs / prédits de la classe. F1 = moyenne harmonique. F1 macro = moyenne des F1 par classe. Erreur grave = cas réels de classe 2 prédits classe 0 / cas réels de classe 2. Matrice de confusion complète. Limite : ces métriques ne mesurent pas le bénéfice de l'accompagnement.

**A2 - Benchmark.** Tableaux complets par scénario et modèle, avec protocole identifié (CV, sous-validation, test) ; réglages testés. Exemple de compromis d'hyperparamétrage (S1, CV 5 plis sur le train) : `RandomForestClassifier(min_samples_leaf=5)` atteint un rappel classe 2 de **0,754** mais **13,5 % d'erreurs graves** ; cela répond à « pourquoi ne pas simplement maximiser le rappel ? ». Ce n'est ni un résultat du test final ni l'effet d'un poids plus fort sur la classe 2 : c'est un autre hyperparamètre.

**A3 - Préparation.** Features exactes de S1, S2, S3, S4 et S4-all, imputations, contrôles qualité (assertions), référentiel des neuf templates, graine. Limites : split non temporel, vrais verbatims non évalués. Réponse type pour un texte inconnu : catégorie dédiée ou escalade, à concevoir.

**A4 - Seuils de revue.** A = 0,40 dans tous les cas. Séparer les protocoles :

| Configuration / protocole | Erreurs graves signalées | Part des dossiers en revue | Statut |
|---|---|---|---|
| B = 0,20, référence test des artefacts servis | 4/9 | 25,6 % (128/500) | Paramètre enregistré dans les artefacts servis |
| B = 0,15, sous-validation de sélection | 5/7 | 33,0 % | Recommandation hors ligne, à arbitrer par le métier |
| B = 0,15, test descriptif distinct | 5/9 | 28,4 % | Lecture descriptive, non utilisée pour choisir B |

Sous l'hypothèse de correction sans erreur des dossiers revus, le résiduel du candidat B = 0,15 est **2/72 = 2,8 %** en sous-validation et **4/90 = 4,4 %** sur le test descriptif. Ces taux ne sont pas une efficacité constatée de conseillers et ne modifient pas le taux brut du modèle (9/90). Ils passent sous la cible de 5 % mais la revue dépasse 15 % : validation opérationnelle, évaluation indépendante et promotion restent nécessaires. Candidat choisi sur la sous-validation, pas sur le test.

**A5 - Équité et arbitrage nationalité.** Effectifs par groupe (UE/hors UE, diplôme, âge, famille), distinction répartition des classes / rappel par groupe, ablation « S1 sans nationalité », conditions de maintien (audit récurrent, gouvernance, information, réversibilité). Limites : petits effectifs, absence de preuve causale.

**A6 - Conformité.** Minimisation, information, droits des personnes, AIPD, registre, base légale, AI Act ; séparer mesures réalisées et obligations à valider. Pas de feu vert juridique.

**A7 - Architecture et CI.** Schéma détaillé, endpoints, historique SQLite sans features, métadonnées du modèle, tests, export, infrastructure cible envisagée (on-premise ou cloud souverain, CPU/RAM, charge), p50 et détail de la mesure p95. Limites : intégration complète et déploiement distant non démontrés.

**A8 - Décisions et recul.** Journal de bord : correction du protocole de test, correction S1, comparaison TF-IDF / catégoriel, feuille de route détaillée. Limite : test historiquement consulté ; exercice sans validation métier réelle.

---

## 8. Punchlines (une par slide au maximum, cinq ou six retenues après répétition)

| Slide | Formulation | Précaution |
|---|---|---|
| 1 | « Orienter, sans décider à la place » | Rappeler le statut de prototype |
| 2 | « Du dossier à l'accompagnement » | Ne promet pas un bénéfice mesuré |
| 3 | « Une erreur grave peut retarder un accompagnement nécessaire » | Dommage possible, pas observé |
| 4 | « Les commentaires ne sont pas libres : 9 formulations types » | Appuyer sur le comptage des textes uniques |
| 5 | « Préparer sans contaminer l'évaluation » | Objectif du protocole corrigé, pas absence historique de fuite |
| 7 | « Le meilleur score ne suffit pas à justifier un déploiement » | À associer au tableau RF/HGB |
| 8 | « 53 cas de classe 2 repérés sur 90 » | Montrer aussi les 9 erreurs graves |
| 9 | « Les seuils de revue sont des choix de conception à valider avec le métier » | Distinguer B = 0,20 servi et B = 0,15 recommandé |
| 10 | « Les écarts entre profils restent préoccupants et incertains » | Citer les effectifs réels |
| 12 | « Une architecture industrialisée ne vaut pas autorisation de mise en service » | Ne pas dire « prête pour la production » |
| 13 | « Les nouvelles données servent à entraîner un candidat, pas à remplacer le modèle » | Entraînement, évaluation, promotion séparés |
| 15 | « Prototype industrialisé, pas de mise en production décisionnelle à ce stade » | Verdict précis, sans adjectif promotionnel |

---

## 9. Prochaines actions

- Valider le contenu de la slide 14 contre le journal de bord.
- Rédiger la phrase de recul personnel (slides 1 et 15) et le point de départ personnel (slide 1).
- Fabriquer le bandeau de progression et les tags de compétences.
- Reconstruire les tableaux (slides 6, 7, 8) avec légendes de protocole, sans captures brutes mélangeant les protocoles.
- Chronométrer une première répétition.


