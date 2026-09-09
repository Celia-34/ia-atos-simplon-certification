# Schéma des flux de données — Acerox Métallurgie

> Schéma Mermaid à compléter. Doit montrer :
> - **Sources** (tabulaire, textuelle)
> - **Ingestion** (transformers)
> - **BDD pivot** (si utile)
> - **Modèle** (modèle retenu)
> - **Interface graphique** utilisée par l'opérateur
> - **API de consultation du modèle**
>
> Légende explicite : qui produit, qui consomme, contraintes.

## Schéma

Exemple à transformer :
```mermaid
flowchart LR
    SRC1[📡 capteurs_iot.csv<br/>----------------<br/>Format: CSV<br/>Volume: 51K mesures/mois, 3 sites - Taille: 3,6 Mo<br/>Fréquence: plusieurs fois/jour/capteur<br/>Version: avril 2026]
    SRC2[📋 erp_export.json<br/>----------------<br/>Format: JSON<br/>Volume: 2000 commandes/mois, 2 sites - Taille: 1,8 Mo<br/>Fréquence: à chaque nouvelle commande ou changement de statut<br/>Version: avril 2026]
    SRC3[📝 logs_machines.log<br/>----------------<br/>Format: texte brut<br/>Volume: 30K événements/mois, 3 sites - Taille: 0.5 Mo<br/>Fréquence: à chaque événement machine, environ chaque minute<br/>Version: avril 2026]

    INGEST[🔄 Ingestion<br/>à concevoir en M3-B2]
    BDD[(🗄️ BDD pivot<br/>SQLite)]
    MODEL[🧠 Modèle existant Acerox<br/>prédiction défauts qualité]

    SRC1 -->|données structurées qui représentent les valeurs des capteurs IoT| INGEST
    SRC2 -->|données structurées qui représentent les commandes| INGEST
    SRC3 -->|données à formater qui représentent les évènements qui se sont produits sur les lignes de production| INGEST
    INGEST -->|normalisation + dédup| BDD
    BDD -->|consommée par| MODEL

    classDef source fill:#e1f5ff,stroke:#0277bd,color:#333333
    classDef tofix fill:#fff4e1,stroke:#c97a00,color:#333333,stroke-dasharray: 5 5
    class SRC1,SRC2,SRC3 source
    class INGEST tofix
```

## Légende

> Reformule en 5 lignes max ce que le schéma raconte (qui produit quelle
> donnée, qui consomme, contraintes critiques).
Exemple :

- **Producteur** : les capteurs IoT des 3 sites (mesures), les machines industrielles (logs événements) et l'ERP sur 2 sites (commandes/statuts).
- **Consommateur final** : le modèle Acerox de prédiction des défauts qualité, via la BDD pivot SQLite alimentée par la couche d'ingestion.
- **Contraintes critiques** (fréquence / RGPD / qualité) : ingestion quasi continue qui peut représenter un volume important de données (ici on ne dispose que d'un mois de données), formatage obligatoire des logs texte brut, normalisation + déduplication avant stockage, contrôle de qualité des données et gouvernance des données opérationnelles.

## Décisions associées


---

*Schéma produit par Célia, DD-MM-YYYY.*
