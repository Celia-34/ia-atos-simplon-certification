
Les quatre scénarios utilisent le **même split 80/20 stratifié** défini en §4.1. Les imputations, vectorisations et encodages sont ajustés sur le train uniquement. La variable `nationalite_hors_ue` est exclue de toutes les features : elle est conservée uniquement pour l'audit d'équité. Le `code_insee_commune` brut est remplacé par le département, afin de limiter sa sensibilité et sa granularité.

| Scénario | Variables conservées | Prétraitement prévu | Question évaluée / justification |
|---|---|---|---|
| **S1 - Approche multimodale complète** | Toutes les informations métier non directement sensibles : `age`, `niveau_diplome`, `anciennete_poste_ans`, `code_rome_vise`, `departement`, `est_allocataire` et `synthese_entretien`. | Pipeline tabulaire de §4.2 + vectorisation TF-IDF du texte, puis concaténation des deux représentations. | Mesure le gain apporté par le contexte sémantique de l'entretien par rapport aux seules données structurées. La nationalité hors UE et le code commune brut restent exclus malgré l'approche complète. |
| **S2 - Sans variables sensibles (approche éthique)** | `anciennete_poste_ans`, `code_rome_vise`, `est_allocataire` et `synthese_entretien`. Sont retirés : `nationalite_hors_ue`, `age`, `niveau_diplome` et `departement`. | Même traitement que S1, mais sans les quatre variables sensibles ou proxy. Une vérification du texte est nécessaire, car il peut contenir indirectement ces informations. | Évalue le coût de l'atténuation des biais. Le retrait applique les principes de minimisation, de non-discrimination et de protection des données dès la conception prévus par le RGPD et la CNIL. |
| **S3 - Diagnostic par le texte seul (NLP pure)** | `synthese_entretien` uniquement. | Imputation des textes manquants par chaîne vide, puis TF-IDF avec nettoyage léger et modèle de classification. | Mesure la robustesse du signal textuel seul face aux formulations variées, aux erreurs de saisie et au bruit des verbatims. Les performances et les biais potentiellement encodés dans le texte seront comparés à S1 et S2. |
| **S4 - Données contextuelles pures (tabulaire seul)** | `age`, `niveau_diplome`, `anciennete_poste_ans` et `departement`. Aucun texte ni variable métier complémentaire. | Imputation médiane pour les numériques, imputation par modalité la plus fréquente et encodage du département. | Quantifie le pouvoir prédictif des caractéristiques socio-professionnelles et territoriales sans contexte sémantique. Il sert de référence face à S3 et permet de mesurer le gain réel de la multimodalité dans S1. |

#### Sous-scénarios S4 - Étude des proxies tabulaires

Ces sous-scénarios utilisent uniquement des données tabulaires. Ils permettent d'isoler l'effet de chaque proxy, sans qu'un signal équivalent contenu dans le texte ne masque son retrait.

| Sous-scénario | Variables tabulaires conservées | Proxy retiré / question testée |
|---|---|---|
| **S4a - Baseline tabulaire** | `age`, `niveau_diplome`, `anciennete_poste_ans`, `departement` | Aucun : référence tabulaire avec les trois proxies identifiés par l'EDA. |
| **S4b - Sans âge** | `niveau_diplome`, `anciennete_poste_ans`, `departement` | Quel est l'apport de l'âge et son retrait améliore-t-il l'écart de recall entre tranches d'âge ? |
| **S4c - Sans diplôme** | `age`, `anciennete_poste_ans`, `departement` | Quel est l'apport du niveau de diplôme et son retrait limite-t-il le biais socio-économique ? |
| **S4d - Sans département** | `age`, `niveau_diplome`, `anciennete_poste_ans` | Quel est l'apport du département et son retrait limite-t-il les écarts territoriaux ? |
| **S4e - Sans proxies majeurs** | `anciennete_poste_ans` | Quelle performance reste-t-il sans âge, diplôme ni département ? Cette référence permet de quantifier le gain cumulé des trois proxies. |
