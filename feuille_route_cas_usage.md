# Feuille de route — Cas d'usage certif

> **Pour qui** : apprenant·e ATOS qui démarre son cas d'usage certif en
> parallèle des modules (à partir de la fin de M4).
> **À quoi ça sert** : savoir **quoi faire maintenant, quoi attendre**, et
> **quelle fiche ouvrir à quel moment**. Ce document ne remplace ni le sujet,
> ni le canvas : c'est le plan de vol.
>
> **Les 3 documents à garder ouverts en permanence** :
> 1. `canvas-cas-usage-v2.ipynb` — la trame de ton notebook final (tes
>    sections = ses sections) ;
> 2. `journal-de-bord.ipynb` — à remplir **dès aujourd'hui**, à chaque
>    session de travail (c'est un livrable certif, pas une option) ;
> 3. cette feuille de route.

---

## Le principe

Ton cas d'usage se construit **en parallèle** des modules restants. Tout ce
qui relève de la **modélisation** (comprendre les données, préparer, entraîner,
comparer, arbitrer) mobilise des gestes **déjà vus en M0-M4** : c'est ton
chantier de l'été. Tout ce qui relève de l'**industrialisation** (API, CI/CD,
MLflow, monitoring) sera vu en **M5-M6** : ne le commence pas avant, tu le
ferais deux fois.

```
   ÉTÉ (autonomie)                      RENTRÉE (au fil de M5-M8)
   ─────────────────────────────────    ─────────────────────────────────
   Phases 1 → 5 : cadrage, EDA,         Phases 6 → 8 : API, CI/CD, MLflow,
   éthique, pipeline, modèles,          monitoring, architecture cible,
   scénarios, arbitrages                dossier final + soutenance
   = sections 0 à 7 du canvas           = sections 8 et 9 du canvas
```

> ℹ️ **La section §7 (communication client / soutenance) est à cheval** : sa
> partie *conception* (§7.2 analyse d'erreurs & fallback, et le §7.3 message
> client rédigé à chaud pendant que l'arbitrage est frais) se fait **en été**
> avec la phase 5 ; sa **finalisation pour la soutenance** (polissage du
> message, slides) se fait **à la rentrée** avec la phase 8. Tu la commences
> maintenant, tu ne la « termines » pas en juillet.

⚠️ **Le piège n°1 des profils IT** : foncer sur Docker/CI/CD (ta zone de
confort) et garder la modélisation « pour plus tard ». C'est l'inverse qu'il
faut faire : la modélisation est la partie la plus longue à mûrir, et c'est
elle qui alimente tout le reste.

---

## Les 8 phases

| # | Phase | Sections canvas | Tu produis | Fiches & ressources à ouvrir | Modules | Statut |
|---|---|---|---|---|---|---|
| 1 | **Cadrer** — besoin métier, tâche ML, risques éthiques identifiés dès le départ | §0-§1 | Cadrage écrit, dictionnaire des risques, setup traçabilité (versions, hash, git) | `fiche_choix_famille_ML.pdf` · `fiche_cycle_vie_donnee.md` · fiche de révision C1/C2/C4 (distribuée via Discord) | M3, M8 | ✅ faisable |
| 2 | **Explorer** — EDA, qualité, dictionnaire de variables, colonne « sensible ? » | §2-§3 | EDA propre, audit qualité (manquants, cardinalités, déséquilibre de la cible), analyse de biais (disparate impact) | `fiche_pattern_preparation_donnees.md` · `fiche_preprocessing.pdf` · `fiche_pattern_anonymisation_PII.md` (si texte libre avec PII) | M2, M3 | ✅ faisable |
| 3 | **Préparer** — pipeline sans fuite, split d'abord, scénarios de données | §4 | `Pipeline` + `ColumnTransformer` (imputation, encodage, texte), jeux de données par scénario (avec/sans variables sensibles) | `fiche_preprocessing.pdf` · `fiche_pattern_texte_NLP.md` (volet TF-IDF) · galerie données mixtes 01 et 03 | M2, M4 | ✅ faisable |
| 4 | **Modéliser & comparer** — plusieurs familles, mêmes folds, mêmes métriques | §5 | Benchmark multi-modèles avec validation croisée stratifiée, test scellé, gestion du déséquilibre | `fiche_pattern_ML_supervise.md` · `cheatsheet_algos_ML_FR.pdf` · `fiche_validation_reglage.pdf` · `fiche_desequilibre_classes.pdf` · `cheatsheet_metriques.md` · `fiche_biais_variance.pdf` · galerie données mixtes 02 et 04 | M1, M4 | ✅ faisable |
| 5 | **Arbitrer** — le verdict chiffré multi-critères | §6-§7 | Tableau perf × coût × latence × explicabilité × biais, choix argumenté, fallback/seuils (erreurs critiques, human-in-the-loop) | `grille_decision_C4.md` · `cheatsheet_sobriete_couts.md` · `fiche_interpretabilite_xai.pdf` · `panorama_genai_llm_rag_agents.md` (justifier ce que tu n'as PAS mis) | M4, M7 | ✅ faisable |
| 6 | **Industrialiser** — API, conteneur, CI/CD, MLflow | §8 | API (predict/health/réentraînement), tests, Docker, GitHub Actions, tracking MLflow | `fiche_notebook_a_prod.pdf` · `cheatsheet_mlops_deploiement.md` · `cheatsheet_git_template_workflow.md` | M5 | 🔜 rentrée |
| 7 | **Surveiller** — monitoring, drift, boucle de feedback, robustesse en exploitation | §9 | Métriques de suivi, journalisation des inférences, stratégie de réentraînement, **robustesse en exploitation (OOD, drift, calibration)** — §9.4 | `cheatsheet_mlops_deploiement.md` · `fiche_donnees_synthetiques.md` | M6 | 🔜 rentrée |
| 8 | **Architecturer & défendre** — archi cible, hébergement, dossier, soutenance | §8 (archi) + dossier | Schéma d'architecture SI, arbitrage on-premise / cloud, dimensionnement, slides | `cheatsheet_cloud_hyperscalers.md` · `grille_decision_stockage.md` · `fiche_stockage_donnees.pdf` · fiche de révision C1/C2/C4 (distribuée via Discord) | M7, M8, M9 | 🔜 rentrée |

> 📓 **Le journal de bord traverse les 8 phases.** Ce n'est pas une phase à
> part, c'est un réflexe à chaque session : ce que tu as fait, ce qui t'a
> bloqué, ce que tu as **décidé et pourquoi**. Il est un **livrable certif à
> part entière** (`journal-de-bord.ipynb`), et c'est lui qui alimente ton
> dossier final et ta soutenance — le jury y lit le *cheminement*, pas
> seulement le résultat. Un arbitrage noté à chaud (phase 5) est infiniment
> plus solide à défendre qu'un souvenir reconstruit en septembre. Ouvre-le
> **dès la phase 1**, remplis-le **avant** de fermer ton notebook du jour.

---

## Cet été : fais / ne fais pas

**Fais** :
- [ ] Phases 1 à 5, dans l'ordre — objectif réaliste : arriver à la rentrée
      avec un **benchmark de modèles complet et un arbitrage argumenté**.
- [ ] Le journal de bord à chaque session (10 lignes suffisent : fait,
      bloqué, décidé, pourquoi).
- [ ] L'éthique **au fil de l'eau** (canvas §1.5 → §3.6 → §4.3 → §6.1),
      pas en annexe de dernière minute — le jury le voit immédiatement.
- [ ] Les notebooks de la **galerie données mixtes** si ton cas combine
      tabulaire + texte : c'est l'entraînement au geste, sur un autre jeu
      de données.

**Ne fais pas** :
- ✗ Docker, CI/CD, MLflow, monitoring avant M5-M6 — tu les referais.
- ✗ Un LLM/agent « parce que c'est possible » — un modèle sobre bien
      arbitré vaut plus de points qu'une usine à gaz (cf. grille C4).
- ✗ Du tuning fin avant d'avoir une baseline et un benchmark honnête.
- ✗ Conclure sur un seul split — validation croisée stratifiée, toujours.

---

## Mini-jalons conseillés

| Jalon | Tu sais que c'est bon quand… |
|---|---|
| Fin de phase 2 | Ton EDA répond à : quelle cible, quel déséquilibre, quels manquants, quelles variables sensibles, quelles cardinalités piégeuses. |
| Fin de phase 3 | `pipeline.fit(X_train, y_train)` tourne sans fuite, et tu peux régénérer chaque scénario de données en une cellule. |
| Fin de phase 4 | Un tableau : lignes = modèles, colonnes = métriques CV — reproductible avec `random_state=42`. |
| Fin de phase 5 (rentrée) | Tu peux défendre ton choix de modèle en 2 minutes face à « pourquoi pas plus simple ? » et « pourquoi pas un LLM ? ». |

*Un doute, un blocage → Discord, ou le RDV individuel du vendredi.*
