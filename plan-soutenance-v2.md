# Plan de soutenance v2 - Cas d'usage CISIA (document autoporteur)

Ce document contient tout ce qu'il faut pour construire le support et préparer l'oral : cadre, déroulé minuté, contenus, questions du jury avec réponses courtes, annexes, répétition, et en fin de document (§10) les règles de formulation et les limites majeures. Il ne renvoie à aucun autre fichier. Les chiffres sont ceux du projet à la date de rédaction ; les revérifier dans le notebook et les artefacts avant de figer les slides.

---

## 1. Cadre

- **Format** : 30 min d'exposé, suivies de 30 min de questions, devant un jury de 2 professionnels externes. Aucune démonstration en direct : support statique, captures d'écran seulement, aucun service à lancer.
- **Support** : **14 slides** + annexes hors temps d'exposé.
- **Timing** : **27 min prévues + 3 min de réserve**, avec un plan de coupe (§5).
- **Compétences évaluées** : référentiel technique CISIA C1 à C9 (notebook, soutenance, questionnaire de 15 questions portant sur C1, C2 et C4). Côté transversal, la soutenance mobilise CT6 (présenter un travail au commanditaire en synthétisant résultats et démarche, et répondre aux questions) et CT7 (codes et posture professionnels face au jury).
- **Niveau attendu** : « transposer », c'est-à-dire construire dans un contexte nouveau. Le jury doit voir des choix argumentés, pas une application guidée.
- **Questionnaire** : à confirmer auprès de l'organisme s'il est distinct des 30 min de questions orales (écrit ou oral, avant ou après). S'il est distinct, prévoir un entraînement spécifique sur C1, C2 et C4 : définitions (annexe A1), vocabulaire des risques, choix de modèle. À clarifier avant J-14 (§9).

### Règles de densité (valables pour toutes les slides)

- **Un message central, trois éléments visibles maximum** (un schéma, un tableau et une capture comptent chacun pour un).
- **Trois puces orales maximum** par slide dans « À dire », **chaque puce tenant en une à deux phrases**. Tout le reste est une réserve pour les questions ou l'annexe, pas un texte à recopier.
- **Budget de mots à l'oral** : environ 130 mots par minute, soit ~190 mots pour 1:30, ~260 pour 2:00, ~330 pour 2:30. Au-delà, couper.
- **Une à deux limites par slide**, pas plus. Les cinq limites majeures (§10) sont annoncées une fois en slide 3 et rappelées en slide 14.
- **Une punchline par slide au maximum** (table §8) et **une phrase-pivot par fin de section** (table §2). Ce sont deux choses différentes : la punchline marque un message, le pivot répond à la question directrice.
- **Pictogramme « H »** (hypothèse) sur les slides pour tout chiffre ou choix qui n'a pas été validé par le métier (coûts, seuils, nationalité, capacité de revue). Il remplace les mentions répétées « à valider » dans le texte projeté.

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

La section en cours est en surbrillance. Chaque fin de section se termine par une phrase-pivot qui répond à la question directrice (tableau des pivots en §2).

### Trois chiffres à retenir (répétés, le reste en annexe)

| Chiffre | Rôle dans le récit |
|---|---|
| **9 templates** (au lieu de texte libre) | La donnée a changé la démarche |
| **9/90 = 10 % d'erreurs graves** sur le test (cible < 5 %) | Le résultat ne suffit pas |
| **25,6 % de dossiers en revue** (cible ≤ 15 %) | Le filet humain est partiel et coûteux |

Le chiffre 9/90 est toujours affiché avec la mention « test consulté avant correction du protocole » (limite 3, §10).

---

## 2. Vue d'ensemble minutée

| # | Section | Slide | Durée | Créneau | Compétences | Punchline |
|---|---|---|---:|---|---|---|
| 1 | Comprendre | Question directrice, profil, trajectoire | 1:30 | 00:00-01:30 | CT6, CT7 | « Orienter, sans décider à la place » |
| 2 | Comprendre | Besoin métier, conseiller, trois classes | 1:30 | 01:30-03:00 | C1 | « Du dossier à l'accompagnement » |
| 3 | Comprendre | Risque prioritaire, critères, limites majeures | 2:00 | 03:00-05:00 | C2, C4 | « Une erreur grave peut retarder un accompagnement nécessaire » |
| 4 | Explorer | Données et neuf templates | 2:30 | 05:00-07:30 | C1, C3 | « Les commentaires ne sont pas libres : 9 formulations types » |
| 5 | Explorer | Préparation et prévention des fuites | 1:30 | 07:30-09:00 | C3 | « Préparer sans contaminer l'évaluation » |
| 6 | Évaluer | Scénarios, modèles, protocole | 2:00 | 09:00-11:00 | C4, C5 | « Le texte seul ne suffit pas, le tabulaire seul manque des cas » |
| 7 | Évaluer | Choix du prototype et compromis | 2:00 | 11:00-13:00 | C4 | « Le meilleur score ne suffit pas à justifier un déploiement » |
| 8 | Évaluer | Résultats finaux, baseline et lecture des erreurs | 2:30 | 13:00-15:30 | C8 | « 53 cas repérés sur 90, 9 qui passent à côté » |
| 9 | Encadrer | Revue humaine : bénéfice et coût | 2:00 | 15:30-17:30 | C2, C8 | « Les seuils de revue restent à valider avec le métier » |
| 10 | Encadrer | Explicabilité et équité | 1:30 | 17:30-19:00 | C2, C8 | « Les écarts entre profils restent préoccupants et incertains » |
| 11 | Encadrer | Éthique, conformité, nationalité | 1:30 | 19:00-20:30 | C2 | « La conformité conditionne le déploiement, elle ne le suit pas » |
| 12 | Industrialiser | Architecture, preuves, interface, supervision, feedback | 3:00 | 20:30-23:30 | C5, C6, C7, C8, C9 | « Industrialisé ne vaut pas autorisé » |
| 13 | Décider | Retour d'expérience (synthèse) | 1:30 | 23:30-25:00 | C9, CT6 | « Trois difficultés, trois apprentissages » |
| 14 | Décider | Verdict, préconisations, recul | 2:00 | 25:00-27:00 | C9, CT6 | « Prototype industrialisé, pas de mise en production décisionnelle à ce stade » |
| | **Total** | | **27:00** | | | **3 min de réserve** |

### Phrases-pivots de fin de section (réponse à la question directrice)

| Fin de section | Après la slide | Phrase-pivot |
|---|---|---|
| 1 Comprendre | 3 | « J'ai identifié où l'erreur coûte le plus et fixé mes critères pour lire les résultats. » |
| 2 Explorer | 5 | « La donnée a changé la méthode, et le protocole sépare préparation et évaluation. » |
| 3 Évaluer | 8 | « Le score global est bon, mais la classe la plus à risque est mal détectée : une prédiction seule ne suffit pas. » |
| 4 Encadrer | 11 | « Le filet humain et le cadre éthique réduisent le risque sans le lever. » |
| 5 Industrialiser | 12 | « La chaîne est reproductible, mais industrialisé ne vaut pas autorisé. » |
| 6 Décider | 14 | « Oui comme aide à l'orientation, non comme décideur : pas de mise en production décisionnelle à ce stade. » |

---

## 3. Déroulé slide par slide

Chaque slide donne : objectif, à afficher, à dire (3 puces maximum), limites (1 à 2), recul le cas échéant, questions probables du jury avec réponse courte.

### Section 1 - Comprendre

#### Slide 1 - Question directrice et trajectoire (1:30 | 00:00-01:30)

**Objectif** : donner au jury une question directrice et annoncer une présentation centrée sur les décisions prises, pas sur une succession d'outils.

**À afficher** : titre du cas d'usage, identité, contexte de certification ; question directrice ; frise « besoin -> expérimentation -> prototype -> décision de déploiement ». Pas de capture technique.

**À dire** :
- Votre point de départ face à l'IA, en 20 à 30 secondes, à renseigner sans inventer de biographie ; le relier à ce que le projet vous a appris.
- La finalité (aide à l'accompagnement des demandeurs d'emploi), le plan en six temps et la réponse annoncée : aide oui, décideur non.
- Les résultats et leurs limites seront présentés ensemble.

**Limite** : le jeu est qualifié de synthétique dans le notebook ; la soutenance ne démontre aucune efficacité constatée auprès de vrais usagers.

**Questions probables** :
- *Quel problème précis résolvez-vous ?* Orienter plus tôt vers un accompagnement adapté les demandeurs d'emploi susceptibles de rester longtemps sans emploi, sans que la machine décide.
- *Qu'avez-vous réalisé personnellement, quel périmètre ?* À préparer précisément : cadrage, exploration, modélisation, évaluation, audit, industrialisation du prototype ; sans validation métier réelle.

#### Slide 2 - Besoin métier et place du conseiller (1:30 | 01:30-03:00) - C1

**Objectif** : relier la sortie du modèle à une action métier compréhensible et délimiter ce que le système ne doit pas décider.

**À afficher** : schéma du parcours d'un dossier (de l'entretien à l'orientation) ; trois classes en langage usager : **0** retour rapide (avant 6 mois), **1** retour moyen (6 à 12 mois), **2** risque de longue durée (au-delà de 12 mois).

**À dire** :
- La sortie est une classe de délai estimée, pas une date exacte.
- Le conseiller conserve la responsabilité de l'orientation ; aucun refus automatique de droits ou de prestations.
- Réserve sur les labels : le sujet évoque une décision de parcours ou un constat terrain validé par les conseillers ; on ne présume pas que chaque label correspond à un délai observé.

**Limite** : les classes réduisent une situation sociale complexe ; le bénéfice réel de la priorisation n'est pas validé sur le terrain.

**Questions probables** :
- *Pourquoi une classification plutôt qu'une régression du délai ?* Le besoin est d'orienter vers un niveau d'accompagnement (trois paliers d'action), pas de prédire un nombre de jours ; les labels disponibles sont des classes.
- *Comment éviter d'enfermer la personne dans une catégorie ?* La classe est une aide à la priorisation, le conseiller décide et peut passer outre ; contestation et réexamen doivent être prévus (slide 11).
- *Quel bénéfice concret pour le conseiller ?* Repérer plus tôt les dossiers à risque pour mobiliser un accompagnement renforcé ; bénéfice non mesuré sur le terrain.

#### Slide 3 - Risque prioritaire, critères, limites majeures (2:00 | 03:00-05:00) - C2, C4

**Objectif** : expliquer pourquoi une bonne accuracy ne suffit pas, poser les critères de lecture avant de montrer les résultats, et annoncer les limites.

**À afficher** (trois éléments) :
- deux exemples fictifs d'erreurs (2 vers 0, personne à risque qui ne reçoit pas l'accompagnement renforcé ; 0 vers 2, ressources mobilisées à tort) ;
- grille compacte des cibles (pictogramme H : seuils posés par le projet) :
  - rappel classe 2 ≥ 0,80 ;
  - F1 classe 2 ≥ 0,60 ;
  - erreur grave (2 prédit 0) < 5 % des vrais cas de classe 2 ;
  - part de dossiers en revue ≤ 15 % ;
  - écart de rappel entre groupes < 10 points, sur effectifs suffisants ;
  - en gris, complémentaires et non probantes pour la sécurité : accuracy ≥ 70 % (erreur globale ≤ 30 %), F1 macro ≥ 0,65 ;
- bandeau « 5 limites » en une ligne (données, métier, protocole, équité, production).

**À dire** :
- La matrice de coûts traduit l'asymétrie métier (2 vers 0 plus coûteuse que 0 vers 2) ; montants et seuils sont des **hypothèses**, faute d'échange possible avec le métier. Je les présente **en premier pour lire les résultats ensuite** ; ils ont été posés comme hypothèses de travail, pas figés avant toute expérience (limite 3).
- Le terme historique « abstention » désigne ici l'envoi en revue : le modèle produit toujours une prédiction.
- Les cinq limites majeures, en une phrase chacune (formule : ce que je sais / ce que je ne sais pas / ce qu'il faut pour savoir).

**Limite** : seuils et coûts à confirmer avec le métier.

**Questions probables** :
- *Qui a fixé ces seuils et pourquoi ?* Moi, comme hypothèses de travail, à partir du risque identifié (perte de chance) et de la capacité de revue supposée ; à arbitrer avec le métier.
- *Quel est le dénominateur du taux d'erreur grave ?* Le nombre de vrais cas de classe 2 (90 sur le test), pas les 500 dossiers.
- *Comment arbitrer sécurité contre charge de revue ?* Plus on signale de dossiers, plus on protège mais plus on surcharge ; c'est le compromis des slides 9 et 14.
- *Pourquoi ces critères sont-ils présentés avant les résultats ?* Pour que le jury lise les résultats avec la même grille que moi ; mais ce sont des hypothèses de travail, et le test a été consulté tôt (limite 3).

### Section 2 - Explorer

#### Slide 4 - Données et neuf templates (2:30 | 05:00-07:30) - C1, C3

**Objectif** : montrer que l'exploration a conditionné la suite du projet et justifier l'absence de NLP en production.

**À afficher** :
- Volume : **2 500 dossiers, 10 colonnes**. Répartition de la cible : classe 0 environ 37,4 %, classe 1 44,5 %, classe 2 18,1 %.
- Comptage des textes : **2 419 synthèses renseignées, 9 formulations uniques, 81 manquantes**, avec deux ou trois exemples.
- Schéma « 9 templates -> famille thématique (+ `texte_manquant`) -> encodage catégoriel ».

**À dire** :
- Contrôles : pas de doublons, manquants limités, anciennetés atypiques mais plausibles conservées. Variables à risque : âge, diplôme, territoire, nationalité, informations indirectes dans la synthèse.
- Démarche en quatre temps : texte libre supposé -> neuf templates constatés -> variable catégorielle -> comparaison avant/après sur les **mêmes plis** : suppression de TF-IDF et de la couche NLP, sans dégradation observée (F1 macro moyen +0,004, rappel classe 2 moyen +0,006, scénario texte seul inchangé).
- Un modèle de langue zero-shot local a servi **une seule fois** pour étiqueter les neuf textes ; référentiel figé dans un CSV avec mapping déterministe, aucun appel à chaque prédiction.

**Limites** :
- Signal très propre pouvant rendre les performances optimistes, sans preuve de son procédé de fabrication ; templates fortement associés à la cible sans être purs à 100 %.
- Le sujet envisageait du NLP sur texte bruité : cette robustesse n'a pas été évaluée sur de vrais verbatims.

**Difficulté 1 du retour d'expérience** (racontée en slide 13, non redite ici).

**Questions probables** :
- *Le projet est-il réellement multimodal ?* Non : tabulaire + une variable catégorielle dérivée du texte. Je le dis clairement.
- *Pourquoi un zero-shot pour neuf textes ?* Pour étiqueter rapidement et de façon reproductible les familles ; une fois le référentiel figé, plus aucun appel.
- *Et avec une nouvelle formulation d'entretien ?* Elle tomberait hors référentiel : texte inconnu à traiter explicitement (catégorie dédiée ou escalade) ; non évalué.
- *Fuite de cible ou artefact de génération ?* Je ne peux pas trancher : aucune mention explicite de la cible dans les textes, mais le risque d'artefact subsiste ; hypothèse de risque à lever avec le fournisseur des données.
- *Comment savoir que les données représentent les futurs usagers ?* On ne le sait pas ; c'est la limite 1. Volume modeste, associations non causales, familles à valider par le métier.
- *Pourquoi conserver les valeurs aberrantes ?* Plausibles métier ; les supprimer aurait retiré des cas réels.
- *Les manquants portent-ils un biais ?* Possible ; 81 textes manquants traités par une catégorie explicite, à surveiller.

#### Slide 5 - Préparation et prévention des fuites (1:30 | 07:30-09:00) - C3

**Objectif** : rendre l'évaluation crédible en montrant comment le prétraitement est séparé de l'évaluation.

**À afficher** : un seul schéma des partitions : split stratifié 80/20, **2 000 dossiers d'entraînement / 500 de test final**, puis second split 80/20 dans les 2 000 : **1 600 de sous-train / 400 de sous-validation** (arbitrage entre finalistes, sans toucher le test final). Les transformations apprises sont ajustées sur chaque train, jamais sur le test.

**À dire** :
- Pipeline unique : imputation, encodage catégoriel, estimateur. Identifiant retiré ; code commune agrégé au département ; graine fixée (`random_state=42`) : l'essai est rejouable, pas statistiquement plus fiable.
- Correction du protocole : le journal rapporte un usage anticipé de `X_test` ; les étapes ont ensuite été séparées.
- Je ne revendique pas un test historiquement vierge.

**Limites** :
- Split aléatoire stratifié, pas de généralisation temporelle ou à une autre agence.
- Test consulté avant correction : une évaluation indépendante reste nécessaire.

**Difficulté 2 du retour d'expérience** (racontée en slide 13, non redite ici).

**Questions probables** :
- *Où une fuite aurait-elle pu se produire ?* Dans l'ajustement des transformations sur toutes les données, dans le choix de variantes sur le test, et dans les features dérivées de la cible ; chaque point est traité par le pipeline unique et la séparation des partitions.
- *Pourquoi pas un split temporel ?* Non réalisé ; limite reconnue.
- *Catégories inconnues ?* L'encodeur est configuré pour les gérer sans erreur ; à vérifier en annexe A3.
- *Agréger le territoire supprime-t-il le proxy ?* Non : cela réduit la granularité sans supprimer son caractère de proxy.

### Section 3 - Évaluer

#### Slide 6 - Scénarios, modèles, protocole (2:00 | 09:00-11:00) - C4, C5

**Objectif** : montrer que les scénarios testent des hypothèses, justifier le choix du ML classique et la méthode de comparaison.

**À afficher** :
- Grille « scénario / question / conclusion courte » :
  - **S1** données complètes avec famille : apport conjoint des sources -> combine les sources ;
  - **S2** retrait des variables à risque désignées -> dégrade les résultats observés sans garantir l'équité ;
  - **S3** famille seule -> ne suffit pas ;
  - **S4** sous-ensemble tabulaire sans famille. Le témoin **S4-all** reprend les sept variables de S1 sans la famille et isole l'apport de celle-ci -> réduit les erreurs graves mais détecte moins de cas à risque.
- Trois modèles : régression logistique, Random Forest, HistGradientBoosting (HGB), chacun avec une raison courte.
- Schéma du protocole : CV stratifiée à 5 plis sur le train -> sous-validation des finalistes -> test final du modèle retenu.

**À dire** :
- Rejet de S3 (légende « CV train ») : rappel classe 2 de 0,660 mais **19,1 % d'erreurs graves**. S2 : meilleur F1 macro des configurations rapportées (0,628) avec 18,5 % d'erreurs graves ; ne pas attribuer cette dégradation à une variable précise.
- Apport de la famille, en sous-validation avec une même configuration RF 300 arbres : S1 rappel 0,681 et erreur grave 9,7 %, contre S4-all 0,514 et 4,2 %. C'est un compromis, pas un gain sur tous les critères ; ne pas mélanger avec les chiffres CV de S2/S3.
- Choix du ML classique : sortie structurée, données modestes, aucun besoin de génération ni de recherche documentaire (donc ni LLM, ni RAG, ni agents, ni deep learning) ; `class_weight="balanced"` pour compenser le déséquilibre.

**Limites** :
- Une seule famille d'approches explorée (trois estimateurs classiques) ; recherche d'hyperparamètres non exhaustive.
- S2 ne garantit pas l'absence de biais (proxys) ; dans le protocole corrigé, le test ne sert pas à choisir les variantes (mais il a été consulté avant la correction, limite 3).

**Questions probables** :
- *Pourquoi ces modèles plutôt que XGBoost ou un réseau de neurones ?* Données tabulaires modestes ; trois estimateurs classiques suffisent à poser le compromis ; extension possible, non réalisée.
- *Pourquoi cinq plis plutôt que dix ?* Compromis entre stabilité et coût de calcul sur 2 000 dossiers ; pas d'étude de sensibilité.
- *Pourquoi pas un GridSearch exhaustif ?* Ciblage sur les leviers qui touchent l'erreur grave ; recherche non exhaustive reconnue.
- *Avez-vous essayé du rééchantillonnage (SMOTE, sur-échantillonnage) ?* Non, ou à confirmer dans le notebook ; j'ai utilisé `class_weight` et des poids de classe, sans créer de dossiers synthétiques. Piste non explorée.
- *Que fait `class_weight="balanced"` ?* Poids inversement liés aux fréquences observées, sans ajout de dossiers ni garantie d'équité entre groupes ; à distinguer d'un poids ciblé sur la classe 2.
- *Quand un LLM deviendrait-il pertinent ?* Avec de vrais verbatims libres et bruités à interpréter, et une validation métier de leur usage.
- *Pourquoi retirer des variables ne garantit-il pas l'équité ?* Des proxys (territoire, diplôme, texte) peuvent subsister.
- *Quelle différence entre S4 et S4-all ?* S4-all garde exactement les sept variables de S1, sauf la famille : seul témoin qui isole son apport.
- *Comment isoler l'effet de la nationalité ?* Ablation dédiée « S1 sans nationalité » (annexe A5) : résultats limités, pas de bénéfice causal démontré.

#### Slide 7 - Choix du prototype et compromis (2:00 | 11:00-13:00) - C4

**Objectif** : expliquer un arbitrage multicritère assumé et distinguer sélection expérimentale et validation pour la production.

**À afficher** : tableau homogène de trois finalistes S1, **sous-validation sur 400 dossiers dont 72 de classe 2** (légende obligatoire) :

| Finalistes (S1) | Rappel classe 2 | Erreur grave | F1 macro | Taille |
|---|---:|---:|---:|---:|
| RF 300 arbres, `class_weight="balanced"`, `random_state=42` | 0,681 | 9,7 % | 0,703 | 27,5 Mo |
| HGB balanced, profondeur 10 | 0,625 | 8,3 % | 0,683 | 0,806 Mo |
| HGB, poids de classe 2 renforcé | 0,556 | 12,5 % | 0,671 | 1,057 Mo |

Mettre en évidence les gains et les contreparties de RF. Pas de capture brute d'un tableau mélangeant des protocoles.

**À dire** (argument en trois temps, à tenir de bout en bout) :
- **Mon critère** : j'ai retenu RF parce que ma priorité est de rater le moins possible de cas à risque (rappel classe 2). C'est un arbitrage assumé, pas une domination : RF ne gagne pas sur toutes les métriques.
- **Ce que cela coûte, en cas concrets sur 72** : RF repère environ 4 cas de classe 2 de plus que HGB balanced (49 contre 45) mais commet environ 1 erreur grave de plus (7 contre 6), et pèse 27,5 Mo contre 0,806 Mo. HGB reste une option crédible si le métier privilégie la sobriété ou l'erreur grave. Valeurs à recalculer depuis l'export avant de figer le support.
- **Ce que cela ne dit pas** : « retenu pour le prototype » ne signifie pas « conforme aux critères de mise en service ». Aucune configuration n'atteint les exigences prioritaires.

**Limites** :
- La priorité « rappel » est une hypothèse que le métier doit trancher.
- Coûts incomplets (valeur manquante pour RF dans l'export) et latences de campagnes différentes exclus du tableau ; les coûts restent des hypothèses. Une pondération plus forte de la classe 2 ne résout pas mécaniquement l'erreur 2 vers 0.

**Questions probables** :
- *Pourquoi retenir un modèle qui ne satisfait pas les seuils ?* Sélection expérimentale entre candidats, pas validation ; d'où le verdict final « pas de mise en production ».
- *Pourquoi pas le modèle le plus sobre (HGB) ?* Meilleur sur l'erreur grave et plus de 30 fois plus léger ; je privilégie le rappel, mais c'est au métier de trancher.
- *Et la sobriété (taille, énergie) ?* RF pèse 27,5 Mo contre 0,806 Mo pour HGB ; à ce volume de données l'impact reste modeste, mais l'empreinte carbone n'a pas été mesurée (annexe A7).
- *« Cinq cas de plus sur 90 » ?* Non : la comparaison porte sur 72 cas de classe 2, pas sur les 90 du test.
- *Comment avez-vous détecté le problème d'implémentation de S1 ?* Voir slide 12.

#### Slide 8 - Résultats finaux et lecture des erreurs (2:30 | 13:00-15:30) - C8

**Objectif** : transformer les scores en conséquences compréhensibles et confronter les résultats aux cibles.

**À afficher** : matrice de confusion du test final de 500 dossiers (lignes « réel », colonnes « prédit »), annotée, avec la mention « test consulté avant correction du protocole » ; tableau « atteint / non atteint » face aux cibles ; une ligne de référence **baseline** :

```
            prédit 0  prédit 1  prédit 2
réel 0        142        36         9
réel 1         27       162        34
réel 2          9        28        53
```

Ligne baseline (légende : test final, 500 dossiers) : prédire toujours la classe majoritaire (classe 1, environ 44,5 % des dossiers) donne une accuracy d'environ 44,5 %, un rappel de 0 sur la classe 2 et 100 % d'erreurs graves. Ajouter la régression logistique (résultat à relever dans le notebook et à comparer avec le même protocole), faute de quoi la baseline reste la seule référence.

**À dire** :
- Accuracy 71,4 % (contre environ 44,5 % pour la baseline majoritaire), F1 macro 0,690 : la performance globale est satisfaisante (≥ 70 %, ≥ 0,65).
- Sur les **90 cas réels de classe 2** : 53 détectés, 28 prédits en classe 1, **9 prédits en classe 0**. Erreur grave : **9/90 = 10 %, et non 9/500**. Erreurs 0 vers 2 suivies séparément : 9/187, environ 4,8 %.
- Critères sur la classe 2 **non atteints** : rappel 0,589 (cible ≥ 0,80), erreur grave 10,0 % (cible < 5 %), F1 classe 2 0,570 (cible ≥ 0,60, juste sous la cible). Revue à 25,6 % contre 15 % maximum : non atteint.

**Limites** :
- 90 cas de classe 2 seulement ; pas d'intervalle de confiance, pas de validation externe.
- Les probabilités ne sont ni une certitude individuelle ni une calibration démontrée.

**Questions probables** :
- *Pourquoi 71,4 % ne suffit-il pas ?* Il masque que la classe la plus à risque est la moins bien détectée (rappel 0,589).
- *71,4 %, par rapport à quoi ?* Baseline majoritaire : environ 44,5 % d'accuracy mais aucun cas de classe 2 détecté ; le gain est réel sur l'accuracy, mais la cible sur la classe 2 reste hors d'atteinte. Résultat de la régression logistique : à relever dans le notebook (annexe A2).
- *Différence rappel / précision / F1 ?* Rappel : part des vrais cas de classe 2 détectés (53/90). Précision : part des prédits classe 2 qui sont justes. F1 : moyenne harmonique des deux.
- *Intervalles de confiance, calibration ?* Non réalisés ; priorité d'une évaluation indépendante.
- *Pourquoi ne pas traiter toutes les erreurs pareil ?* Leur coût métier diffère : 2 vers 0 prive d'accompagnement, 0 vers 2 mobilise des ressources en trop.

### Section 4 - Encadrer

#### Slide 9 - Revue humaine : bénéfice et coût (2:00 | 15:30-17:30) - C2, C8

**Objectif** : évaluer le contrôle humain comme un mécanisme mesurable, pas comme une garantie abstraite.

**À afficher** : arbre des deux règles servies ; schéma des 9 erreurs graves (4 signalées, 5 non signalées) ; chiffre **128/500 = 25,6 % en revue, contre 15 % maximum**.
- Règle A : revue si P(classe 2) ≥ 0,40, quelle que soit la classe prédite.
- Règle B : revue si classe prédite 0 et P(classe 2) ≥ 0,20.

**À dire** :
- Protection partielle : **4 des 9 erreurs graves signalées, 5 non signalées** (filet servi à B = 0,20). Signalé pour revue ne veut pas dire corrigé ; coût illustratif de 20 euros par revue, avec hypothèse de correction humaine parfaite.
- A, B, coût de revue et délais sont des choix de conception faute d'interlocuteur métier ; avec lui, j'aurais arbitré capacité de revue, coût d'une erreur et délai de traitement.
- Une phrase sur la piste B = 0,15 : en sous-validation, 5 erreurs graves sur 7 signalées mais 33,0 % des dossiers en revue, au-dessus du plafond de 15 % ; recommandation hors ligne, non réexportée, pas un feu vert (détail en annexe A4).

**Limites** :
- Filet incomplet et charge excessive ; capacité de revue non validée.
- Risque d'erreur humaine et de biais d'automatisation ; la revue ciblée ne remplace pas la responsabilité du conseiller sur l'orientation de tous les dossiers.

**Questions probables** :
- *Pourquoi ne pas tout envoyer en revue ?* Cela annulerait l'intérêt de l'outil et dépasserait la capacité supposée des conseillers.
- *Que signifie `auto` dans l'API ?* Statut technique « pas de revue déclenchée », pas une décision administrative automatique.
- *Comment fixer les seuils et mesurer la capacité ?* Avec le métier, sur des données distinctes, en comparant sécurité, équité et charge ; ici hypothèses.
- *Que deviennent les cinq erreurs graves non signalées ?* Elles échappent au filet : raison majeure du verdict négatif.
- *B = 0,15 est-il actif ?* Non : ce n'est pas un routage assuré par l'API ; les délais de revue sont des règles d'organisation envisagées, pas des engagements éprouvés.

#### Slide 10 - Explicabilité et équité (1:30 | 17:30-19:00) - C2, C8

**Objectif** : séparer compréhension globale du modèle, justification individuelle et évaluation des écarts entre groupes.

**À afficher** : importance par permutation réduite aux principales variables (rôle de la famille thématique) ; **un seul** exemple d'audit : UE, 37/70 cas de classe 2 détectés (rappel 0,529) ; hors UE, 16/20 (0,800) ; écart d'environ 27 points ; avertissement visible « groupe insuffisant ».

**À dire** :
- Permutation, **calculée sur le jeu de test (je le signale à l'écran)** : mélanger une variable et mesurer la baisse du score ; l'importance n'est pas une causalité, et des variables corrélées peuvent partager leur importance.
- Écart UE / hors UE : signal préoccupant, mais avertissement sous 30 cas de classe 2 (repère qui ne garantit pas une puissance suffisante) ; on ne parle pas de discrimination.
- Distinguer écarts de répartition des classes dans les données et écarts de rappel du modèle : mesures différentes (annexe A5).

**Limites** :
- Explication globale seulement, pas d'attribution locale (SHAP non réalisé).
- Écarts instables sur petits groupes, aucune conclusion robuste.

**Questions probables** :
- *Comment expliquer une prédiction à un conseiller ?* Aujourd'hui : classe, probabilités et raison de revue. Pas d'explication locale ; piste d'amélioration.
- *Peut-on parler de discrimination ?* Non, les effectifs ne le permettent pas ; signal à vérifier.
- *Quelle définition d'équité ?* Égalité des rappels entre groupes (écart < 10 points) car l'erreur la plus grave est de rater un cas de classe 2.
- *Comment améliorer l'audit ?* Plus de données par groupe, intervalles de confiance, audit récurrent après mise en service.

#### Slide 11 - Éthique, conformité, nationalité (1:30 | 19:00-20:30) - C2

**Objectif** : montrer que conformité et non-discrimination conditionnent le déploiement, sans présenter l'analyse comme une validation juridique.

**À afficher** : grille « risque / mesure / validation restante », extrait de l'arbitrage sur la nationalité, sans donnée personnelle.

**À dire** :
- Minimisation : identifiant retiré, territoire agrégé, aucun verbatim brut dans l'API. Base légale envisagée : mission d'intérêt public, à valider ; la nationalité n'est pas une catégorie particulière au sens de l'article 9 du RGPD, mais reste sensible.
- `nationalite_hors_ue` : maintien **conditionnel et réversible**, ablation dédiée aux résultats limités, aucune validation métier obtenue.
- Conditions de mise en service : audit récurrent, information et droits des personnes, AIPD et registre validés ; un circuit de réexamen et de contestation de l'erreur 2 vers 0. Qualification probable à haut risque au titre de l'AI Act, à confirmer : jamais de décision automatique à fort impact.

**Limites** :
- Aucune autorisation juridique définitive ; retirer une variable ne supprime pas ses proxys, et convertir le texte en catégorie n'anonymise pas le dossier.
- L'intervention humaine doit être réelle, pas une validation de façade.

**Questions probables** :
- *Pourquoi conserver la nationalité hors UE ?* Hypothèse de travail pour mesurer son apport et ses effets ; réversible, soumise à validation métier et juridique ; à retirer si non justifiée.
- *Qui valide l'AIPD et l'arbitrage ?* DPO et direction métier ; livrables non produits à ce stade.
- *Que peut contester un usager ?* L'orientation retenue et l'usage de ses données, via un circuit à définir (information, accès, contestation).
- *Entre-t-on dans les décisions automatisées du RGPD ?* Pas tant qu'un conseiller décide réellement ; une revue de façade changerait l'analyse. L'intervention d'un conseiller n'efface pas la responsabilité de l'organisation ou de l'éditeur.
- *Qui porte la responsabilité d'une perte de chance ?* À définir avec la direction métier et le DPO : qui réexamine, qui traite une contestation, qui trace la décision. Le retrait d'une variable ne supprime pas ses proxys.
- *Quelles mesures de minimisation côté exploitation ?* Restrictions de logs et de tableaux de bord, pas de verbatim brut, territoire agrégé.

### Section 5 - Industrialiser

#### Slide 12 - Architecture, preuves, interface, supervision, feedback (3:00 | 20:30-23:30) - C5, C6, C7, C8, C9

**Objectif** : montrer le passage du notebook à un service reproductible et la boucle d'amélioration, sans confondre stack du prototype et production complète. Cette slide porte C5 (entraînement scripté et automatisé), C6 et C7.

**À afficher** (trois éléments) :
- schéma d'architecture (interface conseiller -> backend -> API modèle ; service feedback séparé ; supervision Prometheus/Grafana), avec une capture de CI réussie ; à droite, en pointillé, les **contraintes de la cible** non traitées (hébergement, charge, RGPD) ;
- une capture annotée d'un dossier fictif : résultat `a_valider` avec classe, probabilités et raison de revue ;
- schéma de la boucle **entraîner un candidat -> évaluer -> accepter ou rejeter -> promouvoir sous contrôle humain**, étapes manuelles marquées.

**À dire** :
- **Reproductible** : quatre services dockerisés (frontend, backend, modèle, feedback), entraînement scripté, pipeline persisté avec métadonnées, golden run et CI verte. `auto` reste un statut technique, pas une décision métier.
- **Cohérence servi/évalué** : S1 était documenté mais pas implémenté comme décrit ; détecté, corrigé, témoin S4-all ajouté. Les contrôles comparent configuration, modèle évalué et modèle servi.
- **Amélioration continue** : on supervise disponibilité et distributions ; la qualité exige des labels différés. Réentraînement manuel sur feedbacks validés, jamais de remplacement automatique du modèle servi.

**Limites** :
- Stack locale, aucun déploiement distant démontré ; p95 = 50,1 ms (p50 = 27,3 ms) mesure le pipeline seul sur 1 000 appels unitaires, pas la latence de bout en bout.
- Boucle de feedback non éprouvée avec de vrais retours ; pas d'alerting automatique (détail en annexe A7).

**Difficulté 3 du retour d'expérience** (racontée en slide 13, non redite ici).

**Script oral unique sur l'écart de seuil et la portée des contrôles (à valider avant de figer le support)** :
- Vérifier dans le code si les contrôles de cohérence incluent le seuil de revue B.
- **Si oui** : expliquer pourquoi l'écart est alors volontaire (réglage servi B = 0,20 ; recommandation hors ligne B = 0,15 inscrite dans les métadonnées d'export).
- **Si non** : le dire sans détour : « les contrôles couvrent le modèle et la configuration d'entraînement, pas le seuil de revue ; l'artefact de l'API (v3.0.0) porte B = 0,20, qui est le réglage servi, tandis que les métadonnées exportées par le notebook portent B = 0,15 ; c'est un écart connu, à aligner par une réexportation ». Ne pas affirmer alors que « tout est vérifié ».
- Autre limite à citer si interrogé : le hash du jeu de données n'est pas renseigné dans les métadonnées servies.

**Questions probables** :
- *Comment garantir que le modèle servi est celui évalué ?* Métadonnées du modèle exporté, contrôles de cohérence et golden run comparent configuration, évaluation et artefact servi ; portée exacte sur le seuil B à préciser selon le script ci-dessus.
- *Comment l'entraînement est-il automatisé (C5) ?* Script d'entraînement et d'évaluation rejouable (graine fixée), pipeline persisté, export contrôlé, CI ; réentraînement lancé manuellement, pas d'ordonnanceur.
- *Quelles contraintes pour l'architecture cible (C7) ?* Hébergement (on-premise ou cloud souverain), dimensionnement CPU/RAM, intégration au référentiel des usagers, conservation et accès aux données ; non traités (annexe A7).
- *Que teste le golden run ?* Qu'un jeu d'entrées de référence redonne les mêmes sorties avec le modèle exporté.
- *Panne ou retour arrière ?* Versions de modèle tracées ; procédure de retour arrière à formaliser, non éprouvée.
- *Les 50,1 ms incluent-ils réseau et frontend ?* Non.
- *Détecter une baisse de performance sans labels ?* Seulement des signaux indirects (dérive de distributions) ; la qualité exige des labels.
- *Qui reçoit une alerte aujourd'hui ?* Personne : pas d'alerting automatique ni d'ordonnanceur.
- *Pourquoi 100 feedbacks, et le biais de sélection ?* Seuil pragmatique, insuffisant seul ; retours possiblement non représentatifs.
- *Un candidat accepté remplace-t-il le modèle ?* Non, promotion explicite sous contrôle humain.
- *Peut-on rejouer une prédiction ?* En principe via `request_id` et version enregistrée ; sans features stockées, il faut les redemander.

### Section 6 - Décider

#### Slide 13 - Retour d'expérience, synthèse (1:30 | 23:30-25:00) - C9, CT6

**Objectif** : donner au jury la prise de recul sur la démarche en synthétisant les trois difficultés rencontrées dans le déroulé (slides 4, 5, 12) et en ajoutant la quatrième, sans les raconter à nouveau.

**À afficher** : tableau « difficulté / ce que j'ai fait / ce que je ferais autrement » :

| Difficulté | Ce que j'ai fait | Ce que je ferais autrement |
|---|---|---|
| Données trop propres : texte réduit à 9 templates, provenance floue | Suppression du NLP, variable catégorielle, comparaison avant/après sur mêmes plis, réserve explicite | Demander dès le cadrage le procédé de génération et tester une robustesse sur des textes bruités |
| Usage anticipé de `X_test` | Séparation train / sous-validation / test, correction documentée | Figer le protocole et le jeu de test avant toute exploration |
| Scénario S1 non conforme à sa documentation | Détection, correction, témoin S4-all, contrôles de cohérence | Mettre les contrôles de cohérence en place dès la première itération |
| Aucun échange métier possible | Hypothèses explicites (coûts, seuils A/B, nationalité) | Faire arbitrer ces points avant de modéliser, avec la capacité de revue |

**À dire** :
- Compris : un bon score ne vaut pas sécurité ; le risque prioritaire se définit avant les résultats.
- Fait et repris : un prototype reproductible, un filet de revue mesuré, un audit, trois corrections (données, protocole, S1) ; j'ai relevé et documenté l'usage anticipé de `X_test` plutôt que de le masquer (à confirmer dans le journal de bord avant de l'affirmer).
- Ferais autrement : protocole figé d'abord, échange métier ensuite. N'affirmer que ce qui est documenté dans le journal (A8).

**Limite** : exercice sans validation métier réelle ; le test a été consulté avant correction.

**Questions probables** :
- *Qu'auriez-vous fait autrement ?* Reprendre le tableau, en priorisant : protocole figé dès le départ, puis échange métier.
- *Quelle est votre plus grosse erreur ?* L'usage anticipé de `X_test` : il fragilise la valeur du chiffre final, d'où l'évaluation indépendante.
- *Pourquoi n'avoir pas échangé avec un conseiller réel ?* Aucun échange n'était possible dans le cas d'étude ; c'est la limite 2, d'où des hypothèses explicites et une feuille de route qui commence par cet arbitrage.

#### Slide 14 - Verdict, préconisations, recul (2:00 | 25:00-27:00) - C9, CT6

**Objectif** : conclure en langage client, avec trois messages et une phrase de recul.

**À afficher** : trois blocs « démontré / non autorisé / conditions pour réexaminer », avec la feuille de route en trois priorités dans le bloc « conditions ». Pas de nouvelle capture technique.

**À dire** (environ 260 mots) :
- **Ce que le prototype démontre** : une chaîne technique reproductible et un compromis de classification mesuré sur le jeu fourni ; ni bénéfice terrain établi, ni décideur autonome.
- **Pourquoi je ne recommande pas la mise en service** : 9 erreurs graves sur le test, dont 5 non signalées par le filet servi ; revue à 25,6 % ; équité non établie. Verdict : **pas de mise en production décisionnelle à ce stade**.
- **Ce qui permettrait de reconsidérer, dans cet ordre** : 1) données et labels réels et représentatifs ; 2) arbitrage métier (seuils, capacité de revue, nationalité) ; 3) évaluation indépendante, audit d'équité, validations DPO et direction. Un simple changement de seuil ne suffit pas. Terminer par **une phrase de recul personnel** en écho à la slide 1.

**Limite** : une CI verte, une interface fonctionnelle ou un filet humain partiel ne valent pas autorisation de déploiement ; aucune promesse de seuil atteint après un simple réglage.

**Questions probables** :
- *Déploieriez-vous ce système aujourd'hui ?* Non, pour les trois raisons du message 2.
- *Première priorité avec plus de temps ?* Obtenir des données et labels réels, car tout le reste en dépend.
- *Qu'est-ce qui vous ferait abandonner le cas d'usage ?* Une équité non atteignable, des labels non fiables, ou une capacité de revue incompatible avec la sécurité requise.

---

## 4. Correspondance compétences / slides

| Compétence | Slides | Preuve principale |
|---|---|---|
| C1 Jeu de données | 2, 4 | Cohérence données/besoin, réserve de provenance |
| C2 Risques éthiques et cadre réglementaire | 3, 9, 10, 11 | Erreur 2 vers 0, nationalité, AIPD, AI Act |
| C3 Préparation des données | 4, 5 | Neuf templates, split, pipeline sans fuite |
| C4 Choix du modèle | 3, 6, 7 | Scénarios, finalistes, compromis RF/HGB |
| C5 Entraînement | 6, 12 | CV 5 plis, pondération, entraînement scripté et rejouable |
| C6 Implémentation | 12 | Services, golden run, interface |
| C7 Architecture cible | 12 | Schéma, contraintes de la cible, limites de déploiement |
| C8 Performance et impacts | 8, 9, 10, 12 | Matrice, taux d'erreur grave, supervision |
| C9 Amélioration continue | 12, 13, 14 | Boucle de feedback, retour d'expérience, feuille de route |
| CT6 Présenter au commanditaire | 1, 13, 14 | Messages en langage client, réponses aux questions |
| CT7 Posture face au jury | toute la soutenance | Reconnaissance des limites, réponses courtes |

Le questionnaire porte sur C1, C2 et C4 : maîtriser en priorité les slides 2 à 4, 6 à 7 et 9 à 11. C5 et C7 reposent sur peu de slides (6 et 12) : prévoir une annexe prête (A2 pour C5, A7 pour C7) en cas de question.

---

## 5. Gestion du temps et répétition

**Réserve : 3 minutes.** Si le retard dépasse 2 minutes, couper dans cet ordre :
1. slide 10 : ne garder que l'exemple UE / hors UE (30 s) ;
2. slide 12 : supprimer la capture de l'interface (30 s) ;
3. slide 6 : ne présenter que S3 et S4-all (1 min) ;
4. ne jamais couper les slides 8, 9, 13 et 14.

**Repères de passage** : slide 5 terminée à 09:00 ; slide 8 terminée à 15:30 ; slide 11 terminée à 20:30 ; slide 13 démarrée à 23:30.

**Répétition** : trois passages chronométrés (seul, devant un tiers, avec questions). Noter l'écart à chaque repère. Ne pas accélérer en lisant toutes les notes.

**Séance de questions (30 min)** : elle est aussi longue que l'exposé. Préparer 15 à 20 réponses de 20 secondes en puisant dans les « questions probables » de chaque slide et dans le §6, et s'entraîner à renvoyer vers une annexe plutôt que de s'étendre.

**Avant de figer le support** :
- Vérifier chaque chiffre contre le notebook et les artefacts (B = 0,15 recommandé et B = 0,20 servi, A = 0,40 inchangé), et recalculer les cas concrets de la slide 7 (49 contre 45, 7 contre 6).
- Vérifier les réserves de provenance et de labels ; vérifier la cohérence entre tableau comparatif, export des finalistes et messages au client ; ne pas transformer des données incomplètes en arguments de performance.
- Vérifier que chaque détail technique répond à une question du récit : compris, fait, repris, ferais autrement.
- Préparer un support autonome : aucune navigation dans l'application.

---

## 6. Questions transversales prioritaires (réponse en 20 secondes)

1. **Pourquoi garder la nationalité hors UE ?** Arbitrage conditionnel, réversible, non validé par le métier, avec ablation dédiée et audit récurrent.
2. **Pourquoi retenir RF alors qu'aucun seuil n'est atteint ?** Sélection expérimentale pour le rappel en sous-validation (environ 4 cas de plus sur 72 contre environ 1 erreur grave de plus que HGB) ; priorité à valider avec le métier ; aucune mise en service recommandée.
3. **Les données sont-elles réelles ?** Notebook : synthétiques ; sujet : collectées en agence ; procédé non documenté ; signal trop propre.
4. **Que feriez-vous autrement ?** Protocole figé dès le départ, échange métier avant de modéliser, contrôles de cohérence dès la première itération.
5. **Déploieriez-vous aujourd'hui ?** Non : 9 erreurs graves dont 5 non signalées, revue à 25,6 %, équité non établie.
6. **Que signifie `auto` ?** Statut technique de l'API, pas une décision administrative automatique.
7. **Le test est-il resté vierge ?** Non : usage anticipé documenté dans le journal, protocole corrigé ; évaluation indépendante nécessaire.
8. **71,4 % d'accuracy, par rapport à quoi ?** Baseline majoritaire à environ 44,5 % sans aucun cas de classe 2 détecté ; le gain est réel mais la classe à risque reste mal détectée (rappel 0,589).

---

## 7. Annexes (hors temps, à ouvrir sur question)

**A1 - Métriques.** Rappel = vrais positifs / vrais cas de la classe. Précision = vrais positifs / prédits de la classe. F1 = moyenne harmonique. F1 macro = moyenne des F1 par classe. Erreur grave = cas réels de classe 2 prédits classe 0 / cas réels de classe 2. Matrice de confusion complète. Limite : ces métriques ne mesurent pas le bénéfice de l'accompagnement.

**A2 - Benchmark.** Tableaux complets par scénario et modèle, avec protocole identifié (CV, sous-validation, test) ; réglages testés. **Baselines** : classe majoritaire (environ 44,5 % d'accuracy, rappel classe 2 nul) et régression logistique (résultats à relever dans le notebook, avec le même protocole que les finalistes). Exemple de compromis d'hyperparamétrage (S1, CV 5 plis sur le train) : `RandomForestClassifier(min_samples_leaf=5)` atteint un rappel classe 2 de **0,754** mais **13,5 % d'erreurs graves** ; cela répond à « pourquoi ne pas simplement maximiser le rappel ? ». Ce n'est ni un résultat du test final ni l'effet d'un poids plus fort sur la classe 2 : c'est un autre hyperparamètre.

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

**A7 - Architecture, CI, supervision et boucle de feedback.**
- Architecture : schéma détaillé, endpoints, historique SQLite sans features, métadonnées du modèle, tests, export, p50 et détail de la mesure p95. Infrastructure cible envisagée (on-premise ou cloud souverain, CPU/RAM, charge), intégration au référentiel national des usagers, coût réel, empreinte carbone, règles d'accès et de conservation. Publier ou retagger des images ne prouve pas un déploiement sur l'infrastructure cible.
- Supervision : trois niveaux (technique : disponibilité, erreurs HTTP, latence ; distributions entrées/sorties ; qualité prédictive avec vérité terrain). Historique `/history` (`request_id`, classe prédite, probabilité, version, date), sans features d'entrée : il ne suffit pas seul pour audit et réentraînement. Feedbacks d'exemple simulés.
- Boucle de feedback : distinguer annotation du conseiller, décision de parcours et délai réellement observé, pour ne pas entraîner le modèle sur sa propre recommandation. Réentraînement manuel par script (cadence hebdomadaire et seuil de 100 feedbacks envisagés, sans garantie d'effectif par classe ou groupe). Escalade humaine pour situations inhabituelles : circuit, déclencheurs et responsabilités à définir. Réexamen des seuils avec le métier si la charge ou les erreurs évoluent, sur données distinctes, avec promotion explicite ; jamais de relèvement automatique d'un seuil pour réduire la charge. Règle de résolution des feedbacks contradictoires à définir (priorité à un référent).
- Limites : PSI non implémenté, pas de score de nouveauté ni de calibration, pas de route API de réentraînement, labels possiblement retardés ou biaisés, utilisabilité terrain non prouvée, jeu de référence réutilisé.

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
| 6 | « Le texte seul ne suffit pas, le tabulaire seul manque des cas » | Conclusion sur le jeu fourni, pas générale |
| 7 | « Le meilleur score ne suffit pas à justifier un déploiement » | À associer au tableau RF/HGB |
| 8 | « 53 cas repérés sur 90, 9 qui passent à côté » | Montrer les 9 erreurs graves, rappeler « test consulté » |
| 9 | « Les seuils de revue restent à valider avec le métier » | Distinguer B = 0,20 servi et B = 0,15 recommandé |
| 10 | « Les écarts entre profils restent préoccupants et incertains » | Citer les effectifs réels |
| 11 | « La conformité conditionne le déploiement, elle ne le suit pas » | Pas une validation juridique |
| 12 | « Industrialisé ne vaut pas autorisé » | Ne pas dire « prête pour la production » |
| 13 | « Trois difficultés, trois apprentissages » | N'affirmer que ce que le journal documente |
| 14 | « Prototype industrialisé, pas de mise en production décisionnelle à ce stade » | Verdict précis, sans adjectif promotionnel |

---

## 9. Préparer le support (actions, captures, annexes)

### Actions (ordre à suivre, échéances relatives au jour de la soutenance)

| Échéance | Action | Durée estimée | Critère de fin |
|---|---|---|---|
| J-14 | Clarifier le statut du questionnaire (§1) ; valider la slide 13 contre le journal de bord ; recalculer les cas concrets de la slide 7 depuis l'export ; relever la régression logistique dans le notebook ; vérifier la portée des contrôles de cohérence sur le seuil B (slide 12) | 3 h | Réponses écrites en tête de document, chiffres vérifiés dans le notebook |
| J-12 | Rédiger la phrase de recul personnel (slides 1 et 14) et le point de départ personnel (slide 1) | 1 h | Deux textes lus à voix haute en moins de 30 s chacun |
| J-10 | Fabriquer le bandeau de progression, les tags de compétences et le pictogramme « H » | 2 h | Gabarit de slide validé, appliqué aux 14 slides |
| J-9 | Reconstruire les tableaux (slides 6, 7, 8) avec légendes de protocole, sans captures brutes mélangeant les protocoles | 3 h | Chaque tableau porte son protocole et son effectif (dont 72 et 90) |
| J-8 | Produire les captures de l'inventaire ci-dessous et monter les annexes A1 à A8 | 4 h | Toutes les captures présentes, annexes masquées avec index |
| J-7 | Première répétition chronométrée ; couper ce qui dépasse | 1 h | Écart aux quatre repères de passage noté |
| J-5 | Rédiger les 15 à 20 réponses de 20 secondes pour les questions | 2 h | Liste de réponses relue à voix haute, sans notes |
| J-3 et J-1 | Répétitions devant un tiers, puis avec questions | 2 h chacune | Temps total ≤ 28 min, réponses aux questions sans dépasser 30 s |

### Inventaire des captures et visuels à produire

Tous les visuels utilisent des dossiers fictifs, aucune donnée personnelle. Chaque capture est annotée et recadrée ; pas de capture brute d'un tableau mélangeant des protocoles.

| Slide | Visuel | Source | Précaution |
|---|---|---|---|
| 2 | Schéma du parcours d'un dossier, trois classes | À dessiner | Langage usager |
| 3 | Exemples d'erreurs 2 vers 0 et 0 vers 2, grille des cibles | À dessiner | Pictogramme H sur les seuils |
| 4 | Extrait des 9 templates (2 ou 3 exemples) et comptage des textes | Référentiel CSV, notebook | Dossiers fictifs ; pas de donnée identifiante |
| 5 | Schéma des partitions 2 000 / 500 puis 1 600 / 400 | À dessiner | Une seule vue |
| 6 | Grille des scénarios S1 à S4-all et schéma du protocole | À dessiner, chiffres du notebook | Légende « CV train » ou « sous-validation » |
| 7 | Tableau des trois finalistes | Export des finalistes, recalculé | Légende « sous-validation, 400 dossiers dont 72 de classe 2 » |
| 8 | Matrice de confusion, tableau atteint / non atteint, ligne baseline | Notebook, test final | Mention « test consulté avant correction » |
| 9 | Arbre des règles A et B, schéma des 9 erreurs graves | À dessiner, artefacts servis | Pictogramme H sur A, B, coût de revue |
| 10 | Importance par permutation, tableau UE / hors UE | Notebook | Signaler « calculé sur le test » et « groupe insuffisant » |
| 11 | Grille risque / mesure / validation restante | À dessiner | Pas une validation juridique |
| 12 | Schéma d'architecture avec contraintes de la cible en pointillé, CI réussie, capture `a_valider`, schéma de la boucle de feedback | Dépôt, CI, interface | Dossier fictif ; capture du tableau de bord Grafana recadrée en annexe A7 |
| 13 | Tableau des quatre difficultés | À rédiger | Contenu relu contre le journal |
| 14 | Trois blocs et feuille de route | À rédiger | Pas de nouvelle capture technique |

### Format des annexes dans le support

- Annexes A1 à A8 en **diapositives masquées** à la fin du support, une par annexe (A4 : le tableau des seuils ; A7 : schéma détaillé, p50/p95, tableau de bord).
- Une **slide d'index** avant les annexes, avec un lien par annexe, plus un lien de retour vers la slide d'origine.
- En mode présentation, accès direct par numéro de slide ; noter les numéros des annexes sur une fiche papier.
- Les annexes s'ouvrent uniquement sur question du jury ; ne jamais les présenter spontanément.

---

## 10. Référence : limites majeures et règles de formulation

### Les cinq limites majeures

Formule : **ce que je sais / ce que je ne sais pas / ce qu'il faut pour savoir**. Dites-les une fois en slide 3, rappelez-les en slide 14. Ailleurs, une à deux limites par slide.

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

Dans le récit : **A = 0,40 / B = 0,20 (servi)**, soit 128/500 dossiers signalés et 4 erreurs graves signalées sur 9. **B = 0,15** (recommandé hors ligne) est mentionné en **une phrase** (slide 9) comme piste à arbitrer avec le métier, détail en annexe A4.
