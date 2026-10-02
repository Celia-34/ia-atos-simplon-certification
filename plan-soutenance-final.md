# Plan de soutenance final - Cas d'usage CISIA

## Statut et cadre

Ce document est un **brouillon de construction du support**, pas le texte final des slides ni un script à réciter. Pour chaque slide, il précise le contenu à préparer, l'objectif, les visuels possibles, les limites à expliciter et les questions à anticiper.

- Durée prévue : **30 minutes d'exposé et transitions comprises, sans démonstration**. Les échanges avec le jury sont supposés se tenir après ces 30 minutes.
- Support principal : **17 slides**, complétées par des annexes hors temps d'exposé.
- Sources principales : `plan-soutenance.md`, dont le déroulé initial de 15 minutes est développé ici, et `notes-soutenance.txt`, désormais complété.
- Vérifications complémentaires : `decision.md`, `criteria.md`, `evaluation_finale.md`, `comparaison_finalistes.md`, le notebook, le journal de bord et le code des services. Les formulations de `slides/` sont utilisées comme pistes éditoriales, pas comme preuves numériques.
- Les captures sont seulement indiquées : aucune image n'est intégrée à ce brouillon. Le support est autonome, sans navigation dans l'application ni exécution en direct.

### Fil rouge

**Peut-on utiliser une prédiction pour mieux orienter les demandeurs d'emploi sans automatiser une décision à fort impact ?**

Le récit doit montrer une chaîne d'arbitrages : besoin métier, risque prioritaire, examen des données, simplification du pipeline, comparaison des modèles, résultats, contrôle humain, conditions de déploiement. La conclusion attendue est celle d'un prototype techniquement industrialisé, mais **non prêt pour une mise en production décisionnelle**.

Suivre la trame personnelle des notes : **ce que j'ai compris, ce que j'ai fait, ce que j'ai repris ou corrigé, ce que je ferais autrement**. Les éléments techniques servent de preuves à ce récit. La synthèse comparative (§6.1 du notebook) et la communication au client (§7.3, à confronter aux réserves de §7.4) constituent le cœur de l'argumentation, pas des annexes secondaires. Reconstruire leurs tableaux et messages plutôt que reprendre des captures contenant des protocoles mélangés ou des conclusions trop optimistes.

### Précautions avant fabrication du support

- Distinguer systématiquement validation croisée, sous-validation et test final. Ne pas réunir leurs chiffres dans un classement sans préciser le protocole.
- Utiliser comme référence opérationnelle les règles actuellement servies : **A = 0,40 et B = 0,20**.
- **Seuil B clarifié : A = 0,40 / B = 0,15 est la recommandation du notebook, confirmée par `criteria.md` ; les artefacts servis restent à A = 0,40 / B = 0,20.** Le candidat a été choisi sur la sous-validation, pas sur le test descriptif. Sa charge de revue dépasse le plafond de 15 % et exige un arbitrage métier avant toute adoption, puis un export et une promotion contrôlés. Les mentions de B = 0,10 dans les notes et `decision.md` ne sont plus la référence pour la recommandation actuelle. Le TODO de clarification est levé, pas les conditions de mise en service.
- Expliquer qu'aucun échange métier n'était possible dans le cas d'étude : matrice de coûts, seuils A/B et conditions d'usage de la nationalité sont des hypothèses ou arbitrages du projet, non des validations obtenues auprès du métier.
- Ne pas confondre `auto`, statut technique de l'API, avec une autorisation de décision administrative automatique.
- Présenter les écarts d'équité comme des signaux préoccupants à vérifier, pas comme une discrimination statistiquement démontrée.
- Ne pas présenter les 50,1 ms de p95 du pipeline comme une mesure de latence de bout en bout de l'API.
- Présenter le split comme le protocole final corrigé, pas comme la preuve que le test est resté intact pendant toute l'histoire du projet : le journal rapporte des utilisations antérieures de `X_test`. Une nouvelle évaluation indépendante reste nécessaire pour une validation externe robuste.
- Nuancer la provenance : le notebook qualifie le jeu de synthétique, le sujet le présente comme collecté en agence, et le procédé de génération n'est pas documenté. Ne pas affirmer que les templates ont été fabriqués à partir de la cible : c'est une hypothèse de risque, pas un fait établi.

## Vue d'ensemble des 30 minutes

| Slide | Sujet | Durée | Créneau |
|---|---|---:|---|
| 1 | Point de départ, profil et trajectoire du projet | 1 min 30 | 00:00-01:30 |
| 2 | Besoin métier et place du conseiller | 1 min 30 | 01:30-03:00 |
| 3 | Risque prioritaire et critères de réussite | 1 min 30 | 03:00-04:30 |
| 4 | Données et premiers constats | 1 min 30 | 04:30-06:00 |
| 5 | Découverte déterminante : neuf templates | 2 min | 06:00-08:00 |
| 6 | Préparation reproductible et prévention des fuites | 1 min 30 | 08:00-09:30 |
| 7 | Scénarios et questions expérimentales | 1 min | 09:30-10:30 |
| 8 | Modèles comparés et protocole d'évaluation | 2 min | 10:30-12:30 |
| 9 | Tableau comparatif, choix du prototype et compromis | 2 min 30 | 12:30-15:00 |
| 10 | Résultats finaux et lecture des erreurs | 2 min 30 | 15:00-17:30 |
| 11 | Revue humaine : bénéfice et coût | 2 min | 17:30-19:30 |
| 12 | Explicabilité et audit d'équité | 2 min | 19:30-21:30 |
| 13 | Éthique, conformité et arbitrage sur la nationalité | 2 min | 21:30-23:30 |
| 14 | Reproduire : architecture et preuves d'industrialisation | 2 min | 23:30-25:30 |
| 15 | Interface et parcours conseiller sur captures | 1 min | 25:30-26:30 |
| 16 | Observer et changer sans régression : supervision et feedback | 2 min | 26:30-28:30 |
| 17 | Trois messages au client et recul sur le projet | 1 min 30 | 28:30-30:00 |
| **Total** | **Exposé + transitions, sans démonstration** | **30 min** | **00:00-30:00** |

Les durées incluent les changements de slide. Les questions ci-dessous servent à préparer les échanges, elles ne sont pas toutes à afficher ni à traiter pendant l'exposé.

### Hiérarchie du support

Les listes « contenu à préparer » constituent une réserve de travail, **pas des listes à recopier intégralement sur les slides**. Suivre cette répartition pour tenir les 30 minutes : un message central, trois éléments visibles maximum et une limite importante. Les annexes restent hors temps d'exposé.

| Slide | À afficher | À expliquer à l'oral | À garder en annexe |
|---|---|---|---|
| 1 | Question directrice et trajectoire courte | Votre point de départ, en 20 à 30 secondes | Parcours détaillé |
| 2 | Parcours métier et trois classes | Responsabilité prévue du conseiller et sens des labels | Construction détaillée de la cible |
| 3 | Erreur 2 vers 0 et critères prioritaires | Pourquoi les coûts et seuils sont des hypothèses | Matrice de coûts complète et définitions |
| 4 | Volume, répartition cible, réserve de provenance | Deux constats qui ont changé la suite | Manquants détaillés et valeurs extrêmes |
| 5 | Neuf templates, mapping, réserve sur les verbatims | Hypothèse -> constat -> simplification -> comparaison | Étiquetage zero-shot et résultats avant/après complets |
| 6 | Schéma 2 000/500 puis 1 600/400 | Fit sur train et correction du protocole | Assertions, graine et détails du preprocessing |
| 7 | Scénarios, question testée et conclusion courte | Famille seule insuffisante ; S4-all réduit les erreurs graves mais détecte moins de risques | Features exactes, chiffres complets et ablations |
| 8 | Trois modèles et validation à cinq plis | Pondération et choix du ML classique | Hyperparamètres et benchmark exhaustif |
| 9 | Tableau homogène de trois finalistes et compromis | Pourquoi retenir RF malgré l'avantage sécurité de HGB | Coûts incomplets, variantes CV et historique S1 |
| 10 | Matrice annotée, 53/90 et 9/90 | Dénominateurs et critères non atteints | Toutes les métriques et leurs formules |
| 11 | Référence servie B = 0,20, 128/500, quatre signalées sur neuf | Recommandation B = 0,15 non servie ; signalement n'est pas correction | Comparaison des seuils, délais et hypothèses de coût |
| 12 | Importance globale et un exemple d'écart avec effectifs | Corrélation, petits groupes et équité non établie | Audit complet et distinctions entre mesures d'équité |
| 13 | Risques, protections prévues, validations restantes | Arbitrage nationalité et responsabilité en cas de préjudice | Articles, conditions C1-C7 et ablation détaillée |
| 14 | Architecture simplifiée et une preuve de reproductibilité | Golden run, correction S1 et périmètre de la CI | Ports, contrats, mesures de latence et infrastructure cible |
| 15 | Deux captures fictives annotées | Action du conseiller et lien vers le feedback | Historique et détails de l'interface |
| 16 | Boucle observer -> évaluer -> promouvoir et limite terrain | Persistance, labels requis, escalade des cas inhabituels et réexamen contrôlé des seuils | Circuit d'escalade à concevoir, PSI absent, gates et seuil des 100 feedbacks |
| 17 | Trois messages : acquis, verdict, conditions | Une phrase de recul personnel | Feuille de route détaillée |

L'industrialisation dispose désormais de cinq minutes, organisée autour de **reproduire**, **observer**, puis **changer sans régression**, plutôt que d'une énumération d'outils.

## Déroulé slide par slide

### Slide 1 - Point de départ, profil et trajectoire du projet

**Durée : 1 min 30 | 00:00-01:30**

**Objectif** : donner une question directrice au jury et annoncer une présentation centrée sur les décisions prises, pas sur une succession d'outils.

**Contenu à préparer** :
- Prévoir le titre du cas d'usage, l'identité du candidat et le contexte de certification.
- Prévoir deux ou trois éléments de votre parcours/profil et de votre point de départ face à l'IA, à renseigner sans inventer de biographie ; relier cette trajectoire à ce que le projet vous a appris.
- Poser la question du fil rouge et indiquer la finalité d'aide à l'accompagnement.
- Annoncer trois étapes du récit : comprendre les risques, évaluer un prototype, déterminer les conditions de déploiement.
- Annoncer que les résultats et leurs limites seront présentés ensemble.

**Visuel / capture à prévoir** : une frise courte « besoin -> expérimentation -> prototype -> décision de déploiement », sans capture technique.

**Limites à expliciter** : jeu qualifié de synthétique dans le notebook, provenance à clarifier ; la soutenance ne démontre pas une efficacité déjà constatée auprès de vrais usagers.

**Questions possibles du jury** :
- Quel problème précis cherchez-vous à résoudre ?
- Qu'avez-vous réalisé personnellement et quel est le périmètre du prototype ?

### Slide 2 - Besoin métier et place du conseiller

**Durée : 1 min 30 | 01:30-03:00**

**Objectif** : relier la sortie du modèle à une action métier compréhensible et délimiter ce que le système ne doit pas décider.

**Contenu à préparer** :
- Décrire le parcours d'un dossier, de l'entretien à l'orientation vers un accompagnement adapté.
- Définir les classes : 0, retour rapide avant 6 mois ; 1, retour moyen entre 6 et 12 mois ; 2, risque de longue durée au-delà de 12 mois.
- Distinguer une classe de délai estimée d'une prédiction de date exacte.
- Préciser la réserve sur les labels : le sujet évoque une décision de parcours ou un constat terrain validé par les conseillers. Ne pas présumer que chaque label correspond à un délai effectivement observé ; c'est une condition à vérifier avant d'interpréter la prédiction comme un pronostic de retour à l'emploi.
- Préciser que le conseiller conserve la responsabilité de l'orientation ; exclure tout refus automatique de droits ou de prestations.

**Visuel / capture à prévoir** : schéma du parcours métier et trois classes nommées en langage usager.

**Limites à expliciter** : les classes réduisent une situation sociale complexe ; la disponibilité des ressources d'accompagnement et le bénéfice réel de la priorisation ne sont pas validés sur le terrain.

**Questions possibles du jury** :
- Pourquoi une classification plutôt qu'une régression du délai ?
- Comment éviter que la prédiction enferme la personne dans une catégorie ?
- Quel bénéfice concret le conseiller en retire-t-il ?

### Slide 3 - Risque prioritaire et critères de réussite

**Durée : 1 min 30 | 03:00-04:30**

**Objectif** : expliquer pourquoi une bonne accuracy ne suffit pas et fixer les critères avant de montrer les résultats.

**Contenu à préparer** :
- Illustrer l'erreur prioritaire 2 vers 0 : une personne à risque pourrait ne pas recevoir l'accompagnement renforcé nécessaire.
- Distinguer cette erreur de 0 vers 2, qui mobilise à tort des ressources supplémentaires.
- Prévoir un tableau compact des cibles : rappel classe 2 ≥ 0,80 ; erreur grave < 5 % des vrais cas de classe 2 ; revue ≤ 15 % ; écart de rappel entre groupes < 10 points sur effectifs suffisants.
- Garder accuracy ≥ 70 % et F1 macro ≥ 0,65 comme critères complémentaires, non comme preuve de sécurité.
- Expliquer la matrice de coûts : traduire l'asymétrie métier en pénalités comparables, avec un exemple d'erreur plus coûteuse qu'une autre. Signaler que les montants et seuils sont des hypothèses faute d'échange possible avec le métier.

**Visuel / capture à prévoir** : deux exemples fictifs d'erreurs et une grille de critères issue de `criteria.md`, reformulée plutôt que capturée intégralement.

**Limites à expliciter** : seuils et coûts à confirmer avec le métier ; les montants de la matrice de coût sont hypothétiques. Le terme historique « abstention » désigne ici l'envoi en revue, le modèle produisant toujours une prédiction.

**Questions possibles du jury** :
- Qui a fixé ces seuils et pourquoi ?
- Quel est le dénominateur du taux d'erreur grave ?
- Comment arbitrer entre sécurité et charge de revue ?

### Slide 4 - Données et premiers constats

**Durée : 1 min 30 | 04:30-06:00**

**Objectif** : montrer que l'exploration des données a conditionné la suite du projet.

**Contenu à préparer** :
- Présenter les 2 500 dossiers et 10 colonnes, dont l'identifiant, la cible, les données de profil et la synthèse d'entretien.
- Montrer la distribution de la cible : classe 0, environ 37,4 % ; classe 1, 44,5 % ; classe 2, 18,1 %.
- Résumer à l'oral les contrôles : absence de doublons et manquants limités. Garder le détail des anciennetés atypiques mais plausibles métier en annexe.
- Identifier les variables à risque : âge, diplôme, territoire, nationalité et informations indirectes présentes dans la synthèse.

**Visuel / capture à prévoir** : histogramme des classes, volume et réserve sur la provenance ; synthèse détaillée des manquants en annexe. Ne pas montrer de dossiers identifiants.

**Limites à expliciter** : volume modeste et représentativité non démontrée. Le notebook qualifie les données de synthétiques tandis que le sujet les décrit comme collectées en agence ; aucun procédé de génération n'est documenté. Les associations observées ne sont pas des relations causales.

**Questions possibles du jury** :
- Comment savez-vous que ces données représentent les futurs usagers ?
- Pourquoi conserver les valeurs détectées comme aberrantes ?
- Les valeurs manquantes pourraient-elles porter un biais ?

### Slide 5 - Découverte déterminante : neuf templates, pas du texte libre

**Durée : 2 min | 06:00-08:00**

**Objectif** : valoriser un changement d'approche motivé par les données et expliquer pourquoi le pipeline final n'utilise pas de NLP en production.

**Contenu à préparer** :
- Montrer que les 2 419 synthèses renseignées ne contiennent que neuf formulations uniques ; 81 sont manquantes.
- Expliquer la conversion en neuf familles thématiques plus `texte_manquant`.
- Résumer l'étiquetage zero-shot local ponctuel, puis le référentiel CSV figé et le mapping déterministe. Ne pas laisser croire que le modèle de langue est appelé à chaque prédiction.
- Présenter la suppression de TF-IDF et de la couche NLP : pipeline plus simple, représentation lisible, dépendances réduites, sans dégradation observée de la validation croisée.
- Raconter cette correction en quatre étapes : texte libre supposé -> neuf templates constatés -> variable catégorielle -> comparaison avant/après sur les mêmes folds. Prévoir une preuve discrète : F1 macro moyen +0,004 et rappel classe 2 moyen +0,006 dans la comparaison documentée, avec S3 inchangé ; conserver les détails en annexe.
- Illustrer l'association forte entre templates et cible sans employer « déterministe » : aucune modalité n'est pure à 100 %.

**Visuel / capture à prévoir** : résultat du comptage des textes uniques et extrait du référentiel avec deux ou trois exemples ; petit schéma « neuf templates -> famille -> encodage catégoriel ».

**Limites à expliciter** : signal très propre qui peut rendre les performances optimistes, sans preuve de son procédé de fabrication. Le sujet envisageait une approche NLP sur texte bruité : cette robustesse n'a pas été évaluée sur de vrais verbatims. L'absence de mention explicite de la cible n'élimine pas le risque d'artefact. Les familles doivent être validées par le métier avant un usage réel.

**Questions possibles du jury** :
- Le projet est-il réellement multimodal ?
- Pourquoi avoir utilisé un modèle zero-shot pour seulement neuf textes ?
- Que se passerait-il avec une nouvelle formulation d'entretien ?
- Comment distinguez-vous une fuite de cible d'un artefact de génération ?

### Slide 6 - Préparation reproductible et prévention des fuites

**Durée : 1 min 30 | 08:00-09:30**

**Objectif** : rendre crédible l'évaluation en montrant comment le prétraitement est séparé de l'évaluation.

**Contenu à préparer** :
- Présenter le split stratifié 80/20 : 2 000 dossiers d'entraînement et 500 de test, avec graine fixée.
- Montrer le second split 80/20 à l'intérieur des 2 000 dossiers : 1 600 de sous-train et 400 de sous-validation pour les arbitrages des finalistes, sans utiliser les 500 dossiers de test final.
- Décrire à l'oral le pipeline unique : imputation, encodage catégoriel et estimateur ; pas de page de code sur la slide.
- Préciser que les transformations apprises sont ajustées dans chaque train de validation croisée, jamais sur le test.
- Mentionner le retrait de l'identifiant et l'agrégation du code commune au département.
- Expliquer brièvement la correction du protocole rapportée dans le journal : usage anticipé de `X_test` puis séparation des étapes. Ne pas revendiquer un test historiquement vierge ; c'est une limite à lever par une nouvelle évaluation indépendante.
- Garder en annexe les assertions de qualité et `random_state=42` : la graine rend l'essai rejouable, pas statistiquement plus fiable.

**Visuel / capture à prévoir** : un seul schéma des partitions et des transformations apprises, avec les effectifs et la frontière du test final. Extrait du pipeline en annexe.

**Limites à expliciter** : un split aléatoire stratifié ne mesure pas la généralisation temporelle ou à une autre agence ; agréger le territoire réduit sa granularité sans supprimer son caractère de proxy.

**Questions possibles du jury** :
- Où une fuite de données aurait-elle pu se produire ?
- Pourquoi ne pas utiliser un split temporel ?
- Comment traitez-vous les catégories inconnues ?

### Slide 7 - Scénarios et questions expérimentales

**Durée : 1 min | 09:30-10:30**

**Objectif** : montrer que les scénarios servent à tester des hypothèses, pas seulement à multiplier les scores.

**Contenu à préparer** :
- Prévoir une grille des quatre scénarios : S1, données complètes avec famille ; S2, retrait des variables à risque désignées ; S3, famille seule ; S4, sous-ensemble tabulaire sans famille.
- Associer une question à chacun : apport conjoint des sources, effet du retrait des variables à risque, valeur de l'entretien seul, niveau de performance du tabulaire seul.
- Distinguer S4 du témoin S4-all : ce dernier reprend exactement les sept variables de S1 sans la famille et isole mieux son apport.
- Ajouter une conclusion courte par scénario, sans dérouler un nouveau benchmark : S1 combine les sources ; S3 ne suffit pas seul ; S4-all réduit certaines erreurs graves mais manque davantage de cas à risque ; S2 dégrade les résultats observés sans garantir l'équité.
- Appuyer le rejet de S3 sur le benchmark CV à cinq plis du train (`benchmark.md`) : rappel classe 2 0,660, mais **19,1 % d'erreurs graves**. Pour S2, le meilleur F1 macro des configurations rapportées est 0,628, avec 18,5 % d'erreurs graves ; ne pas attribuer cette dégradation à une variable précise retirée.
- Pour isoler l'apport de la famille, garder les détails en annexe : à configuration RF 300 arbres identique en sous-validation, S1 donne rappel 0,681 et erreur grave 9,7 %, contre 0,514 et 4,2 % pour S4-all. C'est un compromis, pas un gain sur tous les critères. Ne pas mélanger ces valeurs de sous-validation avec les chiffres CV de S2/S3 dans un classement unique.
- Mentionner les ablations ciblées en annexe, dont S1 sans nationalité.

**Visuel / capture à prévoir** : grille synthétique « scénario / question / conclusion courte », à partir de `scenarii.md` et des benchmarks ; mettre le chiffre 19,1 % de S3 avec la légende « CV train ». Les autres chiffres détaillés restent en annexe pour tenir la minute prévue.

**Limites à expliciter** : S2 ne garantit pas l'absence de biais, car des proxys peuvent subsister ; retirer plusieurs variables simultanément ne permet pas d'attribuer un écart à une seule variable.

**Questions possibles du jury** :
- Pourquoi le retrait des variables sensibles ne suffit-il pas à garantir l'équité ?
- Quelle différence entre S4 et S4-all ?
- Comment avez-vous isolé l'effet propre de la nationalité ?

### Slide 8 - Modèles comparés et protocole d'évaluation

**Durée : 2 min | 10:30-12:30**

**Objectif** : justifier le choix d'une approche classique et la méthode de comparaison.

**Contenu à préparer** :
- Présenter les trois candidats : régression logistique, Random Forest et HistGradientBoosting, avec une raison courte pour chacun.
- Décrire la validation croisée stratifiée à cinq plis sur le train, puis la sous-validation des finalistes et l'évaluation finale du modèle retenu sur le test.
- Montrer un extrait lisible du benchmark train/CV avec rappel classe 2, erreur grave et F1 macro ; réserver le tableau complet aux annexes.
- Résumer les essais ciblés de pondération et d'hyperparamètres, sans faire l'inventaire exhaustif.
- Relier `class_weight="balanced"` au déséquilibre observé : poids inversement liés aux fréquences, sans ajout de dossiers ni garantie d'équité entre groupes. Distinguer cet équilibrage du poids ciblé de la classe 2.
- Expliquer l'exclusion de LLM, RAG, agents et deep learning : sortie structurée, données modestes, absence de besoin de génération ou de recherche documentaire.

**Visuel / capture à prévoir** : capture recadrée du benchmark CV du notebook et schéma du protocole d'évaluation.

**Limites à expliciter** : recherche d'hyperparamètres non exhaustive ; une seule famille d'approches, le ML classique, explorée. Les trois estimateurs ne constituent pas trois familles technologiques différentes. Le test ne doit pas servir à choisir les variantes après coup.

**Questions possibles du jury** :
- Pourquoi ces modèles plutôt que XGBoost ou un réseau de neurones ?
- Pourquoi cinq plis et pas dix ?
- Pourquoi ne pas avoir réalisé un GridSearch exhaustif ?
- Dans quelles conditions un LLM deviendrait-il pertinent ?

### Slide 9 - Tableau comparatif, choix du prototype et compromis

**Durée : 2 min 30 | 12:30-15:00**

**Objectif** : expliquer un arbitrage multicritère et distinguer sélection expérimentale et validation pour la production.

**Contenu à préparer** :
- Présenter la configuration retenue : S1 et `RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)`.
- Utiliser §6.1 comme structure de l'arbitrage, mais reconstruire un tableau homogène de trois finalistes S1 : rappel classe 2, erreur grave, F1 macro et taille. Source numérique : `comparaison_finalistes.md`, métriques de sous-validation sur 400 dossiers, dont 72 cas de classe 2 ; ne pas mélanger avec le test de 500 dossiers.
- Expliquer que le choix s'appuie sur les métriques prioritaires en sous-validation, pas seulement sur l'accuracy ou le meilleur F1 macro CV.
- Rendre explicite le compromis RF/HGB balanced : rappel 0,681 contre 0,625 et F1 macro 0,703 contre 0,683, mais erreur grave 9,7 % contre 8,3 % et modèle plus lourd. RF ne domine donc pas toutes les métriques prioritaires ; expliquer la priorité effectivement arbitrée et reconnaître qu'elle reste à valider avec le métier.
- Prévoir les lignes suivantes comme matériau du tableau, pas comme classement absolu : RF 300 arbres, 0,681 / 9,7 % / 0,703 / 27,5 Mo ; HGB balanced profondeur 10, 0,625 / 8,3 % / 0,683 / 0,806 Mo ; HGB poids classe 2 renforcé, 0,556 / 12,5 % / 0,671 / 1,057 Mo.
- Garder `min_samples_leaf=5` en annexe avec son protocole CV. Ne pas transformer une différence de rappel en « cinq cas de plus sur 90 » : les finalistes sont comparés sur 72 cas de classe 2.
- Écarter du tableau principal les coûts incomplets (`nan` pour RF dans l'export) et les latences issues de campagnes différentes. Les coûts restent des hypothèses ; ne pas les utiliser comme preuve non vérifiée d'un optimum.
- Indiquer explicitement que « retenu pour le prototype » ne signifie pas « conforme aux critères de mise en service ».

**Visuel / capture à prévoir** : tableau reconstruit à trois lignes et quatre colonnes numériques, protocole et effectifs en légende ; mettre en évidence les gains et les contreparties de RF. Pas de capture brute de §6.1. Historique S1 en slide 14 et annexe A8.

**Limites à expliciter** : aucune configuration testée n'atteint simultanément les exigences prioritaires ; une pondération plus forte de la classe 2 ne résout pas mécaniquement l'erreur 2 vers 0.

**Questions possibles du jury** :
- Pourquoi retenir un modèle qui ne satisfait pas les seuils ?
- Pourquoi ne pas privilégier le modèle le plus sobre ?
- Comment avez-vous détecté et corrigé le problème d'implémentation de S1 ?

### Slide 10 - Résultats finaux et lecture des erreurs

**Durée : 2 min 30 | 15:00-17:30**

**Objectif** : transformer les scores en conséquences compréhensibles pour les usagers et confronter les résultats aux cibles.

**Contenu à préparer** :
- Afficher la matrice de confusion du test final de 500 dossiers, avec les lignes « réel » et colonnes « prédit » clairement identifiées : `[[142, 36, 9], [27, 162, 34], [9, 28, 53]]`.
- Centrer le commentaire sur les 90 cas réels de classe 2 : 53 détectés, 28 prédits en classe 1, neuf prédits en classe 0.
- Présenter accuracy 71,4 %, F1 macro 0,690, rappel classe 2 0,589 et F1 classe 2 0,570.
- Expliquer les neuf erreurs graves : **9/90 = 10 %**, et non 9/500 ; suivre séparément les neuf erreurs 0 vers 2 : 9/187, environ 4,8 %.
- Construire un bilan « atteint / non atteint » : performance globale satisfaisante au regard des cibles révisées, critères de protection de la classe 2 non atteints.

**Visuel / capture à prévoir** : matrice de confusion annotée du notebook et tableau de confrontation aux seuils, pas uniquement des cartes de scores.

**Limites à expliciter** : 90 cas de classe 2 seulement ; incertitude statistique et absence de validation externe. Les probabilités renvoyées ne sont pas une certitude individuelle ni une calibration démontrée.

**Questions possibles du jury** :
- Pourquoi 71,4 % d'accuracy ne suffit-il pas ?
- Quelle différence entre rappel, précision et F1 ?
- Avez-vous calculé des intervalles de confiance ou évalué la calibration ?
- Pourquoi ne pas traiter toutes les erreurs de la même manière ?

### Slide 11 - Revue humaine : bénéfice et coût

**Durée : 2 min | 17:30-19:30**

**Objectif** : évaluer le contrôle humain comme un mécanisme mesurable, pas comme une garantie abstraite.

**Contenu à préparer** :
- Décrire les règles servies : A, revue si P(classe 2) ≥ 0,40 quelle que soit la classe prédite ; B, revue si classe prédite 0 et P(classe 2) ≥ 0,20.
- Garder les délais et priorités de revue en annexe : ce sont des règles d'organisation envisagées, pas des engagements déjà éprouvés.
- Montrer le résultat : 128 dossiers sur 500 signalés, soit 25,6 %, contre une cible de 15 % maximum.
- Montrer la protection partielle : quatre des neuf erreurs graves sont signalées ; cinq restent non signalées.
- Vérifier ce « cinq sur neuf » contre les sorties du notebook et les métadonnées utilisées pour le support : il concerne le filet servi à B = 0,20, pas indistinctement toutes les variantes exploratoires.
- Distinguer « signalé pour revue » de « effectivement corrigé » ; rappeler le coût illustratif de 20 euros par revue et l'hypothèse de correction humaine parfaite.
- Présenter la clarification : **B = 0,15 recommandé, B = 0,20 enregistré dans les artefacts servis**, A restant à 0,40. Les chiffres ci-dessus concernent B = 0,20 ; ils ne décrivent ni le candidat B = 0,15 ni une revue réellement exécutée par des conseillers.
- Expliquer à l'oral le compromis du candidat B = 0,15 : en sous-validation, cinq erreurs graves sur sept signalées et 33,0 % des dossiers en revue. La baisse du risque s'accompagne d'une charge supérieure au plafond de 15 % ; la recommandation n'est pas un feu vert. Garder le résultat test descriptif et les taux résiduels conditionnels en annexe A4.
- Expliquer qu'A, B, le coût de revue et les délais sont des choix de conception faute d'interlocuteur métier ; préciser ce qui aurait été arbitré avec lui.

**Visuel / capture à prévoir** : arbre des deux règles et schéma des neuf erreurs graves, quatre signalées et cinq non signalées ; éventuellement capture des métadonnées A/B.

**Limites à expliciter** : filet incomplet, charge excessive, capacité métier non validée, risque d'erreur humaine et de biais d'automatisation. B = 0,15 est une règle évaluée hors ligne, non réexportée, pas un routage de revue actuellement assuré par l'API. La revue ciblée ne remplace pas la responsabilité du conseiller sur l'orientation de tous les dossiers.

**Questions possibles du jury** :
- Pourquoi ne pas envoyer tous les dossiers en revue ?
- Que signifie exactement `auto` dans votre API ?
- Comment fixer les seuils et mesurer la capacité de revue ?
- Qu'arrive-t-il aux cinq erreurs graves non signalées ?

### Slide 12 - Explicabilité et audit d'équité

**Durée : 2 min | 19:30-21:30**

**Objectif** : séparer compréhension globale du modèle, justification individuelle et évaluation des écarts entre groupes.

**Contenu à préparer** :
- Présenter l'importance par permutation et le rôle de la famille thématique, sans assimiler importance et causalité.
- Expliquer le principe de permutation : mélanger une variable et mesurer la baisse de score ; signaler que des variables corrélées peuvent masquer ou partager leur importance.
- Montrer un seul exemple d'audit : UE, 37/70 cas de classe 2 détectés, rappel 0,529 ; hors UE, 16/20, rappel 0,800 ; écart observé d'environ 27 points, groupe hors UE insuffisant pour conclure.
- Garder le détail des diplômes, âges et familles en annexe. Y distinguer les écarts de répartition des classes dans les données des écarts de rappel du modèle : ce ne sont pas les mêmes mesures.
- Afficher l'avertissement pour les groupes sous 30 cas de classe 2 ; expliquer que ce repère ne garantit pas à lui seul une puissance statistique suffisante.

**Visuel / capture à prévoir** : graphique d'importance réduit aux principales variables et exemple d'audit à deux groupes avec numérateurs, effectifs et avertissement visible. Audit exhaustif en annexe.

**Limites à expliciter** : explication globale, pas d'attribution locale SHAP réalisée ; écarts instables sur les petits groupes, absence de conclusion robuste sur l'équité. Une bonne moyenne ne démontre pas une protection équivalente pour tous.

**Questions possibles du jury** :
- Comment expliquer une prédiction particulière à un conseiller ?
- Peut-on parler de discrimination avec ces effectifs ?
- Quelle définition de l'équité avez-vous choisie et pourquoi ?
- Comment améliorer l'audit avant une mise en service ?

### Slide 13 - Éthique, conformité et arbitrage sur la nationalité

**Durée : 2 min | 21:30-23:30**

**Objectif** : montrer que la conformité et la non-discrimination conditionnent le déploiement, sans présenter l'analyse du projet comme une validation juridique.

**Contenu à préparer** :
- Présenter la minimisation : retrait de l'identifiant des features, territoire agrégé, absence de verbatim brut dans l'API, restrictions de logs et de dashboards.
- Indiquer la base légale envisagée, mission d'intérêt public, à valider dans le contexte réel ; distinguer nationalité et catégories particulières de l'article 9 du RGPD.
- Résumer le maintien conditionnel et réversible de `nationalite_hors_ue`, avec une ablation dédiée et des résultats limités, sans prétendre démontrer un bénéfice causal.
- Préciser qu'aucune validation métier de cet usage n'a été obtenue dans l'exercice ; expliquer la validation que vous auriez demandée et les alternatives que vous auriez discutées.
- Prévoir les conditions : audit récurrent, revue de gouvernance en cas de dégradation, information et droits des personnes, AIPD et registre validés avant mise en service.
- Relier l'erreur 2 vers 0 à une possible perte de chance d'accompagnement : préciser qui doit pouvoir réexaminer l'orientation, traiter une contestation et tracer la responsabilité. L'intervention d'un conseiller n'efface pas automatiquement celle de l'organisation ou de l'éditeur.
- Évoquer la qualification probable à haut risque au titre de l'AI Act, à confirmer selon la finalité et le cadre réels ; rappeler l'interdiction de transformer ce prototype en décision automatique à fort impact.

**Visuel / capture à prévoir** : grille « risque / mesure / validation restante » et extrait de l'arbitrage J0, sans exposer de données personnelles.

**Limites à expliciter** : aucune autorisation juridique définitive ; retirer une variable ne supprime pas ses proxys ; convertir le texte en catégorie n'anonymise pas le dossier. L'intervention humaine doit être réelle, pas une validation de façade.

**Questions possibles du jury** :
- Pourquoi conserver la nationalité hors UE ?
- Qui doit valider l'AIPD et l'arbitrage métier ?
- Que peut demander ou contester un usager ?
- Le système entre-t-il dans le champ des décisions automatisées du RGPD ?

### Slide 14 - Reproduire : architecture et preuves d'industrialisation

**Durée : 2 min | 23:30-25:30**

**Objectif** : montrer le passage du notebook à un service reproductible, sans confondre stack du prototype et production complète.

**Contenu à préparer** :
- Présenter le flux principal : interface conseiller -> backend -> API modèle ; service feedback séparé ; supervision Prometheus/Grafana.
- Identifier les quatre services applicatifs dockerisés : frontend, backend, modèle et feedback ; distinguer les composants additionnels de supervision.
- Distinguer la chaîne hors ligne : entraînement, pipeline persisté avec métadonnées, contrôle qualité, export contrôlé du modèle servi.
- Choisir une preuve centrale plutôt qu'énumérer les outils : golden run et contrôle du modèle exporté, appuyés par une CI réussie. Garder le détail Docker/MLflow et les contrats en annexe.
- Raconter une correction concrète : S1 documenté complet -> features textuelles absentes détectées -> scénario corrigé et témoin S4-all -> contrôles de cohérence entre configuration, modèle évalué et modèle servi. Montrer une trace existante, sans prétendre que la correction suffit à prouver toute la qualité.
- Indiquer en légende p95 50,1 ms du pipeline final, mesuré sur 1 000 appels unitaires ; ne pas en faire une preuve de latence API. p50 et détails de mesure en annexe.
- Adapter le schéma pour montrer l'historique minimal des inférences déjà persisté en SQLite, et distinguer le raccordement aux features/feedbacks pour audit et réentraînement qui reste à compléter.

**Visuel / capture à prévoir** : version simplifiée de `schema_architecture.md`, capture d'une CI réussie et extrait des métadonnées du modèle. Mettre les détails des ports en annexe.

**Limites à expliciter** : stack locale industrialisée, pas déploiement distant démontré. La publication ou le retag d'images dans GHCR ne prouve pas un déploiement sur infrastructure cible. Restent l'intégration au référentiel national des usagers, le choix on-premise/cloud souverain, le dimensionnement CPU/RAM et les mesures de charge/latence de bout en bout. Coût réel, empreinte carbone, règles d'accès et conservation restent à compléter ; détailler ces points en annexe plutôt que les développer tous à l'oral.

**Questions possibles du jury** :
- Comment garantir que le modèle servi est celui évalué ?
- Que teste le golden run ?
- Comment gérer une panne ou revenir à une version antérieure ?
- Les 50,1 ms incluent-ils le réseau et le frontend ?

### Slide 15 - Interface et parcours conseiller sur captures

**Durée : 1 min | 25:30-26:30**

**Objectif** : montrer comment les choix techniques se traduisent dans l'interface, uniquement sur le support, sans démonstration.

**Contenu à préparer** :
- Prévoir deux captures annotées d'un dossier fictif : formulaire d'entrée et résultat envoyé en revue.
- Identifier la classe, les probabilités, le statut `a_valider` et la raison de la revue ; rappeler que `auto` est un statut technique, pas une décision métier automatique.
- Situer l'action attendue du conseiller et le lien au `request_id`, sans rejouer le parcours ni ouvrir l'application.
- Faire la transition vers le feedback : distinguer annotation conseiller, décision de parcours et délai réellement observé. Un résultat temporel nécessite un suivi ; la nature, la date et la validation du label doivent être définies pour ne pas entraîner le modèle sur sa propre recommandation.

**Visuel / capture à prévoir** : captures statiques du formulaire et du résultat `a_valider`, avec données fictives ; réserver le dashboard à la slide suivante. Aucune capture de données personnelles réelles.

**Limites à expliciter** : interface de prototype, pas dispositif opérationnel validé ; les captures ne prouvent ni la disponibilité ni l'utilisabilité terrain. Les probabilités ne démontrent pas la fiabilité du cas particulier.

**Questions possibles du jury** :
- Quelle action le conseiller réalise-t-il après ce résultat ?
- Quand et comment obtient-on la vérité terrain ?
- Que se passe-t-il si un feedback contredit un précédent ?
- Peut-on rejouer la prédiction avec la même version du modèle ?

### Slide 16 - Observer et changer sans régression : supervision et feedback

**Durée : 2 min | 26:30-28:30**

**Objectif** : décrire ce qui peut être surveillé immédiatement et ce qui nécessite des labels différés.

**Contenu à préparer** :
- Séparer supervision technique, distributions des entrées/sorties et qualité prédictive mesurée avec vérité terrain.
- Présenter disponibilité, erreurs HTTP, latence, classes prédites et distribution des familles dans Prometheus/Grafana.
- Décrire la boucle de feedback SQLite puis audit hors ligne de la qualité et de l'équité.
- Préciser ce qui est réalisé : feedbacks persistés et historique SQLite des inférences exposé par `/history`, avec `request_id`, classe prédite, probabilité, version et date. Les features d'entrée ne sont pas stockées dans cet historique : il ne suffit pas à alimenter seul l'audit et le réentraînement. Les feedbacks d'exemple sont simulés.
- Expliquer à l'oral le lancement manuel d'un candidat à partir de feedbacks validés. Garder la cadence hebdomadaire et le seuil des 100 feedbacks en annexe : ce nombre ne garantit pas un effectif suffisant par classe ou groupe.
- Montrer les étapes distinctes : entraîner un candidat, évaluer, accepter ou rejeter, puis promouvoir et mettre en service sous contrôle humain.
- Prévoir une escalade humaine pour les situations inhabituelles repérées par un conseiller ou une anomalie technique : conserver l'accompagnement hors outil et transmettre au référent métier/technique selon le problème. Le circuit, les déclencheurs et les responsabilités restent à concevoir ; aucune détection automatique OOD n'est démontrée.
- Prévoir le réexamen des seuils si la charge de revue ou les erreurs évoluent : examiner conjointement sécurité, équité et capacité avec le métier, évaluer sur des données distinctes puis promouvoir explicitement les nouveaux paramètres. Ne pas relever automatiquement un seuil pour réduire la charge, ni confondre cette gouvernance future avec l'adoption déjà acquise de B = 0,15.

**Visuel / capture à prévoir** : capture recadrée du dashboard et schéma de la boucle de feedback avec les étapes manuelles explicites.

**Limites à expliciter** : boucle non éprouvée avec de vrais retours métier et raccordement complet inférences/features/feedbacks à finaliser ; les distributions surveillées ne prouvent pas la qualité sans labels fiables. Pas d'alerting automatique ni d'ordonnanceur. Garder en annexe **PSI non implémenté**, absence de score OOD/calibration et de route API de réentraînement : le réentraînement est lancé par script, pas comme une action automatique du service. Les labels peuvent être retardés ou biaisés et l'usage répété du même jeu de référence appelle une validation indépendante.

**Questions possibles du jury** :
- Comment détecter une baisse de performance sans labels ?
- Qui reçoit une alerte aujourd'hui ?
- Pourquoi attendre 100 feedbacks et comment éviter le biais de sélection ?
- Un candidat accepté remplace-t-il automatiquement le modèle servi ?

### Slide 17 - Trois messages au client et recul sur le projet

**Durée : 1 min 30 | 28:30-30:00**

**Objectif** : conclure en langage client avec trois messages et montrer le recul acquis sur la démarche.

**Contenu à préparer** :
- Préparer trois réponses décisionnelles à partir de §7.3 et §7.4, sans jargon ni reprise de la formule « réserve d'équité levée » : les petits effectifs ne permettent pas cette conclusion.
- Message 1, **ce que le prototype démontre** : une chaîne technique reproductible et un compromis de classification mesuré sur le jeu fourni ; pas un bénéfice terrain établi ni un décideur autonome.
- Message 2, **pourquoi je ne recommande pas la mise en service** : neuf erreurs graves sur le test, dont cinq non signalées par le filet servi ; charge de revue excessive et équité non établie. Verdict : **pas de mise en production décisionnelle à ce stade**.
- Message 3, **quelles preuves permettraient de reconsidérer la décision** : labels et données représentatifs, nouvelle évaluation indépendante, sécurité et capacité de revue validées avec le métier, audit d'équité concluant et validations DPO/direction métier. Un simple changement de seuil ne suffit pas.
- Terminer par une seule phrase de recul personnel reliant vos corrections à votre trajectoire. Garder le détail de ce que vous feriez autrement dans la feuille de route en annexe.

**Visuel / capture à prévoir** : trois blocs « démontré / non autorisé / conditions pour réexaminer », avec un renvoi aux preuves des slides 9 à 16. Feuille de route détaillée en annexe, pas de nouvelle capture technique.

**Limites à expliciter** : aucune promesse de seuil atteint après un simple réglage ; une CI verte, une interface fonctionnelle ou un filet humain partiel ne valent pas autorisation de déploiement.

**Questions possibles du jury** :
- Déploieriez-vous ce système aujourd'hui ?
- Quelle est votre première priorité avec davantage de temps ?
- Quels éléments pourraient vous conduire à abandonner ce cas d'usage ?

## Annexes hors des 30 minutes

Ne pas les parcourir pendant l'exposé. Chaque annexe doit pouvoir être ouverte directement pour une question précise.

| Annexe | Contenu à préparer | Objectif | Limite à rappeler | Question probable |
|---|---|---|---|---|
| A1 - Métriques | Définitions, formules, dénominateurs et matrice complète | Justifier la lecture des résultats | Les métriques ne mesurent pas directement le bénéfice de l'accompagnement | Pourquoi ce rappel et ce taux d'erreur grave ? |
| A2 - Benchmark | Tableaux complets par scénario/modèle, protocole identifié, réglages testés | Étayer la comparaison et le choix | Ne pas mélanger CV, sous-validation et test | Quel autre modèle aurait pu être retenu ? |
| A3 - Préparation | Features exactes S1/S2/S3/S4/S4-all, imputations, contrôles et référentiel | Montrer la reproductibilité | Split non temporel, vrais verbatims non évalués | Comment éviter les fuites et gérer un texte inconnu ? |
| A4 - Seuils de revue | A = 0,40 ; B = 0,20 servi et B = 0,15 recommandé ; tableau séparant sous-validation et test descriptif | Montrer le compromis sécurité/capacité | Recommandation non réexportée, revue au-delà de 15 %, correction humaine parfaite supposée | Pourquoi ne pas adopter immédiatement B = 0,15 ? |
| A5 - Équité et J0 | Effectifs par groupe, ablation S1 sans nationalité, conditions C1-C7 | Documenter l'arbitrage sensible | Petits effectifs et absence de preuve causale | Pourquoi conserver la nationalité ? |
| A6 - Conformité | Mesures de minimisation, information, droits, AIPD, registre et validations restantes | Séparer mesures réalisées et obligations à valider | Pas de feu vert juridique acquis | Quels livrables manquent avant déploiement ? |
| A7 - Architecture et CI | Schéma détaillé, endpoints, historique SQLite, métadonnées, tests, export et infrastructure cible envisagée | Prouver la cohérence de la chaîne technique | Historique sans features, intégration complète et déploiement distant non démontrés | Comment tracer, promouvoir ou retirer une version ? |
| A8 - Décisions et recul | Journal : correction du protocole de test, correction S1, comparaison TF-IDF/one-hot et feuille de route | Étayer le récit personnel et les choix repris | Test historiquement consulté, exercice sans validation métier réelle | Qu'auriez-vous fait autrement ? |

### A2 - Exemple de compromis d'hyperparamétrage

Préparer une comparaison de configurations sur S1, **CV stratifiée à cinq plis sur le train**, à partir de `benchmark.md` : `RandomForestClassifier(min_samples_leaf=5)` atteint un rappel classe 2 de **0,754**, mais **13,5 % d'erreurs graves**. Cet exemple répond à « pourquoi ne pas simplement maximiser le rappel ? ». Ne pas le présenter comme un résultat du test final ou comme l'effet démontré d'une augmentation du poids de la classe 2 : il s'agit d'un autre hyperparamètre. Garder ce point hors du récit principal.

### A4 - Comparaison du seuil servi et du seuil recommandé

Préparer un tableau en séparant les protocoles ; A reste à 0,40 dans tous les cas.

| Configuration / protocole | Erreurs graves signalées | Part des dossiers en revue | Statut |
|---|---|---|---|
| B = 0,20, référence test des artefacts servis | 4/9 | 25,6 % (128/500) | Paramètre enregistré dans les artefacts actuellement servis |
| B = 0,15, sous-validation de sélection | 5/7 | 33,0 % | Recommandation hors ligne, à arbitrer par le métier |
| B = 0,15, test descriptif distinct | 5/9 | 28,4 % | Lecture descriptive, non utilisée pour choisir B |

Sous l'hypothèse de correction sans erreur des dossiers revus, le résiduel du candidat est **2/72 = 2,8 %** en sous-validation et **4/90 = 4,4 %** sur le test descriptif. Ces taux ne sont pas une efficacité constatée de conseillers ni une modification du taux brut du modèle, toujours 9/90 sur le test. Ils passent sous la cible de 5 %, mais la revue dépasse 15 % ; la validation opérationnelle, l'évaluation indépendante et la promotion du paramètre restent nécessaires. Sources actuelles : notebook §5.2.3/§7.2 et `criteria.md`.

## Punchlines réutilisables

Ce sont des **candidates pour les titres ou l'oral**, pas le contenu final des slides. En retenir cinq ou six après répétition, au maximum une par slide : chaque formule doit être accompagnée d'une preuve ou d'une réserve. Les fichiers de `slides/` restent inchangés.

| Slide cible | Formulation candidate | Source | Usage et précaution |
|---|---|---|---|
| 1 | « Orienter, sans décider à la place » | `slides/01_Titre.md`, titre, reprise exacte | Ouverture ; rappeler la finalité et le statut de prototype |
| 2 | « Du dossier à l'accompagnement » | `slides/02_Introduction.md`, titre | Titre métier ; ne promet pas un bénéfice déjà mesuré |
| 3 | « Une erreur grave peut retarder un accompagnement nécessaire » | `slides/02_Introduction.md`, reprise exacte | Associer à l'exemple 2 vers 0 ; dommage possible, pas observé dans l'étude |
| 5 | « Les commentaires ne sont pas libres : 9 formulations types » | `slides/04_Exploration_Donnees.md`, reprise exacte | Pivot du récit, appuyé par le comptage des textes uniques |
| 6 | « Préparer sans contaminer l'évaluation » | Adaptation de « Préparer sans déformer », `slides/05_Preparation_Donnees.md` | Décrit l'objectif du protocole corrigé, pas une absence historique de fuite |
| 9 | « Le meilleur score ne suffit pas à justifier un déploiement » | `slides/06_Benchmark_baseline_scenarii.md`, reprise exacte | Associer au tableau RF/HGB et à leurs contreparties |
| 10 | « Sur le test final : 53 cas de classe 2 repérés sur 90 » | Adaptation de `slides/09_Choix_Modele.md` | Préférer l'effectif au seul « 59 % » ; neuf erreurs graves à montrer aussi |
| 11 | « Les seuils de revue sont des choix de conception à valider avec le métier » | Adaptation de `slides/08_Benchmark_hyperparams.md` | Distinguer B = 0,20 servi et B = 0,15 recommandé, dont l'adoption reste à arbitrer |
| 12 | « Les écarts entre profils restent préoccupants et incertains » | `slides/16_Conclusion.md`, reprise exacte | Associer aux effectifs réels de classe 2 |
| 14 | « Une architecture industrialisée ne vaut pas autorisation de mise en service » | Adaptation de `slides/10_Industrialisation.md` | Ne pas qualifier toute l'architecture de « prête » pour la production |
| 16 | « Les nouvelles données servent à entraîner un candidat, pas à remplacer le modèle » | `slides/13_Prod_feedback.md`, reprise exacte | Appuyer sur la séparation entraînement, évaluation et promotion |
| 17 | « Prototype industrialisé, pas de mise en production décisionnelle à ce stade » | Adaptation de `slides/16_Conclusion.md` | Verdict précis, sans adjectif promotionnel |

**Formulations à ne pas reprendre en l'état** :
- « La forêt repère environ 5 cas à risque de plus sur 90 » (`slides/07_Benchmark_modeles.md`) : les finalistes sont comparés sur 72 cas de classe 2, pas les 90 du test.
- « Une erreur grave sur dix persiste, malgré les alertes humaines » (`slides/16_Conclusion.md`) : mélange le taux brut 9/90 et le signalement par le filet, quatre sur neuf. Le signalement ne prouve pas une correction.
- « Le conseiller garde la main sur chaque décision » (`slides/03_Risque_Ethiques.md`) : responsabilité prévue, pas contrôle opérationnel effectivement démontré.
- « Des indicateurs pour détecter les dérives et préserver la qualité du service » (`slides/12_Prod_suivi.md`) : supervision de distributions réalisée, mais ni alerting automatique ni maintien de qualité démontré.

## Préparation et répétition

- Limiter chaque slide principale à une idée centrale et un visuel lisible ; garder les détails dans les notes orateur et les annexes.
- Conserver les limites importantes sur le support principal, en particulier slides 5, 10, 11, 12 et 17 : ne pas les cacher dans les annexes.
- Vérifier les chiffres et versions contre le notebook et les artefacts : **B = 0,15 recommandé et B = 0,20 servi**, A = 0,40 inchangé. Le TODO de clarification est clos ; l'arbitrage métier et la promotion ne sont pas acquis. Ne pas reprendre les anciennes mentions de B = 0,10 dans les notes ou `decision.md` comme recommandation actuelle.
- Préparer uniquement le support et ses captures statiques : aucun navigateur, service disponible ou réentraînement n'est nécessaire pendant la soutenance.
- Répéter avec les repères de passage : tableau comparatif à 12:30, résultats à 15:00, conformité terminée à 23:30, trois messages client à 28:30.
- En cas de retard, raccourcir les détails de modèles de la slide 8 et les exemples de la slide 15 ; préserver le tableau comparatif, les erreurs, les limites du filet, les preuves d'industrialisation et les trois messages au client. Ne pas accélérer en lisant toutes les notes de préparation.
- Vérifier avant de figer le support les réserves de provenance/labels et les écarts entre tableau §6.1, export des finalistes et communication §7.3/§7.4 ; ne pas transformer des données incomplètes en arguments de performance.
- Vérifier que chaque détail technique répond à une question du récit : ce que j'ai compris, fait, repris ou ce que je ferais autrement.
- Si les 30 minutes doivent aussi inclure les questions du jury, recalibrer le déroulé : le présent plan réserve les 30 minutes à l'exposé, sans démonstration.
