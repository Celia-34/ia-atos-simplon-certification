
# Synthèse des décisions

## EDA 

### Stratégie de gestion des doublons, des manquants et des valeurs erratiques

#### Gestion des doublons

**Choix** : 

**Justification** : 

#### Gestion des manquants

**Choix** : 

**Justification** : 

#### Gestion des valeurs erratiques

**Choix** : 

**Justification** : 


## Préparation


## Benchmark


Les quatre scénarios utilisent le **même split 80/20 stratifié** défini en §4.1. Les imputations, vectorisations et encodages sont ajustés sur le train uniquement. La variable `nationalite_hors_ue` est exclue de toutes les features : elle est conservée uniquement pour l'audit d'équité. Le `code_insee_commune` brut est remplacé par le département, afin de limiter sa sensibilité et sa granularité.


Les scenarii sont détaillés dans le fichier scenarii.md.


## Stratégie de tests

## Industrialisation
