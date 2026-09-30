# Service `model` — API de scoring du risque de non-retour à l'emploi

Service **interne** : il est appelé par le `backend`, jamais directement par le
navigateur. Il charge le pipeline retenu en §6.1 du notebook
(`ColumnTransformer` + `RandomForestClassifier(n_estimators=300,
class_weight="balanced", random_state=42)`) et expose `/health`, `/info`,
`/predict` et `/metrics`.

## Contrat d'entrée

`POST /predict` exige **8 champs**, qui sont exactement les 8 features du
scénario s1. Aucune colonne n'est ajoutée, retirée ou réécrite entre le payload
et le pipeline — c'est ce qui rend les métriques annoncées par `/info`
opposables, et l'audit d'équité §7.2 rejouable sur données de production.

Un payload à 7 champs (contrat `v2.0.0`) est rejeté en `422` : le passage en
`v3.0.0` est une rupture assumée du contrat d'entrée.

## Traitement de `nationalite_hors_ue`

Cette section vaut documentation de traitement au sens de l'article 30 du RGPD
pour la partie technique. Elle est la contrepartie opérationnelle des conditions
`C1` à `C7` de l'arbitrage métier et juridique `J0`.

| | |
|---|---|
| **Nature** | Donnée sensible au sens commun — **pas** une catégorie particulière de l'art. 9 RGPD (la nationalité n'y figure pas), mais un possible **proxy d'origine**, donc traitée avec la vigilance correspondante. |
| **Base légale** | Art. 6.1.e RGPD — mission d'intérêt public (service public de l'emploi). |
| **Finalité (C1)** | **Strictement limitée** à la priorisation vers un accompagnement renforcé. Tout usage de contrôle, de sanction, de radiation ou de refus est exclu. |
| **Éléments d'arbitrage (J0)** | Sur le test set, le rappel classe 2 observé était de 0.800 hors UE (16/20) contre 0.529 UE (37/70), mais ces valeurs conditionnelles ne démontrent pas que la feature cause l'écart. Une ablation dédiée sur la sous-validation (notebook §5.2.3) compare S1 à S1-sans-nationalite, identique sauf cette feature : hors UE 16/20 (0.800) contre 9/20 (0.450), UE 33/52 (0.635) contre 34/52 (0.654), avec n=20 sous le seuil de fiabilité de 30. L'erreur grave globale passe de 7/72 (9,7 %) à 10/72 (13,9 %) et le coût hypothétique de 13 580 € à 14 620 €. Cela informe un maintien provisoire, sans conclusion causale ni fiabilité suffisante pour le groupe hors UE. Diplôme, famille thématique et autres variables peuvent porter un signal redondant. |
| **Collecte** | Saisie par le conseiller dans un `<fieldset>` dédié du formulaire, portant la mention d'information des art. 13-14 RGPD (condition **C7**). |
| **Conservation** | Aucune persistance par ce service. La donnée ne vit que le temps de la requête HTTP (objet `UsagerFeatures` en mémoire). Sa seule trace durable est `data/prod_scored.csv`, journal du trafic scoré, dont la durée de conservation est alignée sur celle du cycle de réentraînement. |
| **Exclusion des logs** | Voir ci-dessous. |
| **Exclusion de la supervision (C2)** | Aucune métrique Prometheus, aucun tableau Grafana ne porte la nationalité en label. Voir `app/metrics.py`. |
| **Audit (C3, C4)** | `scripts/audit_equite.py`, hors ligne, sur le seul jeu annoté. |
| **Droits des personnes** | Accès et rectification exercés sur le dossier usager amont, ce service n'étant pas le système de référence. |
| **À finaliser (C6)** | AIPD (art. 35 RGPD) et inscription au registre des traitements, **avant mise en service**. |

Les conditions C1 à C7 demeurent applicables. Si la nationalité est ultérieurement
retirée des features, elle reste nécessaire à l'audit d'équité, sous réserve de
validation juridique et de gouvernance. L'ablation n'a ni modifié le modèle servi
ni promu un nouvel artefact.

### Exclusion des logs applicatifs

Deux canaux distincts devaient être fermés, et le second n'est pas évident :

1. **`LoggingMiddleware`** (`app/middleware.py`) ne journalise que méthode,
   chemin, code retour, latence et `request_id`. Le corps des requêtes n'est
   jamais lu ni écrit.

2. **Les tracebacks de `loguru`.** Par défaut, loguru enrichit les exceptions
   avec la *valeur des variables locales* (`diagnose=True`). Une erreur dans
   `/predict` inscrivait ainsi l'objet `UsagerFeatures` complet — nationalité
   comprise — en clair dans `logs/api.log`, pour 7 jours de rétention. Les deux
   sinks sont donc configurés avec `backtrace=False, diagnose=False`
   (`app/main.py`).

   Le test `test_une_erreur_de_prediction_ne_journalise_pas_la_nationalite`
   provoque une vraie erreur de prédiction et relit le fichier : il échoue si
   ces options sont réactivées.

Pour investiguer un incident en local, réactiver temporairement `diagnose` est
acceptable **sur données factices uniquement**.

## Portée

L'alignement technique de la production sur la démarche du notebook ne vaut
**pas** autorisation de mise en production. La réserve n° 1 du §7.3 — le filet
de sécurité §5.2.3 ne rattrape qu'une partie des erreurs graves 2→0 — reste
ouverte et bloquante.

## Lancer les tests

```bash
pytest services/model/tests
```
