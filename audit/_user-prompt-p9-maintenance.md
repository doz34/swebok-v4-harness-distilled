[CONTEXTE PROJET — à lire en premier]

    Tu es une instance de Claude Code qui prend la suite d'un travail d'audit structuré du projet SWEBOK v4 Harness Distilled. Le mainteneur (utilisateur) a déjà :
    - cadré le projet stratégiquement (2026-06-04)
    - fermé la phase 0 (Discovery) à 100% (spec v2, 2026-06-04)
    - fermé la phase 1 (Concept/Feasibility) à 100% (spec v2, 2026-06-06)
    - fermé la phase 2 (Requirements) à 100% (spec v2, 2026-06-05)
    - fermé la phase 3 (Architecture) à 100% (spec v2 finale 🟢, 2026-06-06, 8 décisions tranchées, 15/15 P1 closes)
    - fermé la phase 4 (Design) à 100% (spec v2 finale 🟢, 2026-06-07, 4 décisions tranchées vague 1, matrice ADR P3 obligatoire)
    - fermé la phase 5 (Implementation) à 100% (spec v2.1 finale 🟢, 2026-06-07, 4 décisions tranchées vague 1, matrice DDS P4 XG-5.7, effort-report.md livrable formel, Nexus-Critic T1+T2+T3 obligatoire, v2.1 le 2026-06-07 suite à bascule coverage/mutation vers P6)
    - fermé la phase 6 (Testing) à 100% (spec v2 finale 🟢, 2026-06-07, 4 décisions vague 1 + 3 décisions section 7, démarcation P5↔P6 explicite P5=unit seul P6=coverage+mutation+reste, Nexus-Critic T1+T2+T3 obligatoire, budget 5k/8k/15k, 11+1 livrables)
    - fermé la phase 7 (Deployment) à 100% (spec v2 finale 🟢, 2026-06-07, 4 décisions vague 1, démarcation P6↔P7 explicite P6=code-va-passer-en-prod P7=prod-tourne-après-deploy, Nexus-Critic T1+T2+T3 obligatoire, P7 passe de single-agent à multi justifié pour cohérence P3-P6, budget 5k/8k/15k, 7+4 livrables, stratégie rollout big-bang par défaut, hotfix pas de bypass)
    - fermé la phase 8 (Operations) à 100% (spec v2 finale 🟢, 2026-06-07, 4 décisions vague 1, mécanique ADAPTATIVE par sévérité incident — single courant sans Critic, single+T2 standard P2/P3, multi+T1+T2+T3+Council critique P0/P1 — démarcations triple P7↔P8↔P9 explicites Setup vs Run vs Change, budget ADAPTATIF par incident 1k/2k/3k + 2k/4k/6k + 5k/8k/15k, 11 livrables 6 standard + 5 ajouts post-mortem/capacity/CR/on-call/audit-trail, 4 décisions opérationnelles user calibration+priorisation+post-mortem+deferred, spécificité P8 unique phase vivante longue durée)
    - appliqué un fix structurel majeur le 2026-06-05 (modèle 9-phases → 10-phases)

    Ta mission : auditer la phase 9 (Maintenance) en suivant le nouveau process (décrit § 13 ci-dessous).

    1. PROJET

    - Nom : SWEBOK v4 Harness Distilled — framework SDLC pour Claude Code (10 phases canoniques, multi-agent, adversarial gate, state machine SQLite).
    - Localisation : /home/doz/swebok-v4-harness-distilled/
    - Mainteneur : technique, pressé, veut du concret. Il parle français, communication simple SANS jargon.
    - État GitHub : repo public doz34/swebok-v4-harness-distilled, MIT, version v1.5.11 stable.
    - But ultime : auditer chaque phase pour vérifier design + utilité, aboutir à un outil qui matche parfaitement les besoins du mainteneur.

    2. DÉCISIONS STRATÉGIQUES DÉJÀ CADRÉES (NON NÉGOCIABLES)

    - A1 — Modèle de phases : UNE SEULE phase active à la fois (séquentiel strict). Au sein d'une phase, parallélisme libre. Les autres phases sont consultables en lecture seule (cache).
    - B — Seuil question utilisateur : uniquement les décisions à fort impact / irréversibles. Réversibles à faible coût = documentées + reportées. Triviales = silencieuses. Si l'utilisateur n'a pas d'avis = système choisit en autonomie.
    - C — Pattern adversarial : T1 (producteur vs casseur) + T2 (spec-compliance) en standard. T3 (conséquentialiste aval) en option, activé selon la phase.
    - Cible utilisateur : universelle (vibecodeur à développeur senior). Le même install, le même workflow, l'assistance s'adaptant au profil.
    - Un seul produit canonique : la version "anonymisation du corpus" (v2 multi-view, distilled). L'ancienne version doit être archivée.
    - Audit en cours : par phase, un par un, avec une grille commune de 8 sections + verdict 🟢/🟡/🔴. Verdict = un seul choix tranché, jamais les 3 ensemble.
    - Méthode audit : grille offline + questions AskUserQuestion ciblées (validée pour P1 v2, P3 v2 finale, P4 v2 finale, P5 v2 finale, P6 v2 finale, P7 v2 finale, P8 v2 finale). L'ancien process 5 rounds × 4 questions (P0/P2) reste valide pour les phases complexes.
    - **Nexus-Critic T1+T2+T3 OBLIGATOIRE** sur les 5 phases multi-agent (P3, P4, P5, P6, P7) : 3 invocations systématiques, hard cap 15k. **Pour P8 (phase vivante) : adaptatif par sévérité incident (aucun courant / T2 seul P2/P3 / T1+T2+T3 + Council P0/P1)**. **Pour P9 (single-agent justifié sauf gros refactoring) : Nexus-Critic à arbitrer en audit** — T1+T2+T3 obligatoire (cohérence P3-P7) ou adaptatif par type de maintenance (corrective rapide vs perfective structurante) ou allégé (P9 = patch + regression, pas création archi) ?

    3. ÉTAT DE L'AUDIT (au 2026-06-07)

    Fix structurel appliqué 2026-06-05 (cf. mémoire swebok-v4-structural-fix-2026-06-05.md).
    Le modèle canonique est désormais 10 phases, 1-par-1 SWEBOK v4 KAs :

    ┌───────┬─────────────────────┬──────────────────────┬───────────────────┬───────────────┬───────────────┐
    │ Phase │         Nom         │      SWEBOK v4       │       Spec        │    Grille     │    Statut     │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P0    │ Discovery           │ (hors SWEBOK)        │ v2                │ v2            │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P1    │ Concept/Feasibility │ Software Eng Mgmt    │ v2                │ v2            │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P2    │ Requirements        │ P1                   │ v2                │ v2            │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P3    │ Architecture        │ P2                   │ v2 finale         │ v2 finale     │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P4    │ Design              │ P3                   │ v2 finale         │ v2 finale     │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P5    │ Implementation      │ P4                   │ v2.1 finale       │ v2 finale     │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P6    │ Testing             │ P5                   │ v2 finale         │ v2 finale     │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P7    │ Deployment          │ Software Config Mgmt │ v2 finale         │ v2 finale     │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P8    │ Operations          │ (hors core)          │ v2 finale         │ v2 finale     │ ✅ FERMÉ (🟢) │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P9    │ Maintenance         │ P6                   │ v2-renum          │ v1 (template) │ ⬜ PROCHAINE  │
    ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
    │ P10   │ Retirement          │ Software Eng Process │ v2-renum          │ v1            │ ⬜ À faire    │
    └───────┴─────────────────────┴──────────────────────┴───────────────────┴───────────────┴───────────────┘

    Mémoire projet :
    - swebok-v4-structural-fix-2026-06-05.md : détails du fix 9→10 phases
    - swebok-v4-strategic-cadrage-2026-06-04.md : décisions A1/B/C
    - swebok-v4-p0-spec-v2-2026-06-04.md : référence process audit ancien (5×4 questions)
    - swebok-v4-p1-spec-v2-2026-06-06.md : référence process audit nouveau vague 1
    - swebok-v4-p2-spec-v2-2026-06-05.md : référence process audit ancien
    - swebok-v4-p3-spec-v2-2026-06-06.md : vague 1, verdict 🟡 initial
    - swebok-v4-p3-spec-v2-vert-2026-06-06.md : vague 2, verdict 🟢 final
    - swebok-v4-p4-spec-v2-vert-2026-06-07.md : vague 1, verdict 🟢 direct
    - swebok-v4-p5-spec-v2-vert-2026-06-07.md : vague 1, verdict 🟢 direct (référence v2 → v2.1)
    - swebok-v4-p6-spec-v2-vert-2026-06-07.md : vague 1, verdict 🟢 direct (référence pour P7, démarcation P5↔P6)
    - swebok-v4-p7-spec-v2-vert-2026-06-07.md : vague 1, verdict 🟢 direct (référence pour P8, démarcation P6↔P7)
    - **swebok-v4-p8-spec-v2-vert-2026-06-07.md : vague 1, verdict 🟢 direct (référence pour P9, démarcations triple P7↔P8↔P9 Setup vs Run vs Change, spécificité P8 phase vivante)**

    4. NOUVEAU PROCESS (validé 2026-06-07, à suivre pour chaque phase)

    Ancien process (P0 et P2) : 5 rounds × 4 questions AskUserQuestion = 20 décisions tranchées en une seule conversation.

    Nouveau process vague 1 (validée pour P1, P3 vague 1, P4 vague 1, P5 vague 1, P6 vague 1, P7 vague 1, P8 vague 1) :
    1. Le mainteneur remplit la grille d'audit offline dans son éditeur (VSCode, vim, etc.).
    2. Le mainteneur ouvre une nouvelle conversation Claude Code.
    3. Il colle en début de conversation : (a) le user prompt transfert (celui que tu es en train de lire) + (b) le contenu rempli de la grille de la phase en question.
    4. L'instance Claude de cette nouvelle conversation : (a) analyse la grille remplie, (b) pose toutes les questions complémentaires nécessaires pour avoir un rapport très précis et exhaustif (AskUserQuestion, en français simple sans jargon), (c) attend les réponses, (d) rédige la spec v2 + met à jour la grille (verdict tranché, sections 5.5 et 8.5 comblées), (e) met à jour le budget dans la stratégie.
    5. À la fin, l'instance Claude fournit un nouveau user prompt exhaustif pour que le mainteneur puisse continuer le process dans la conversation suivante.

    Nouveau process vague 2 (validé pour P3, P6) : après la vague 1, si des sections restent 🟡 (notamment section 7 utilité réelle) ou si la section 5.5 est en format "catégories" au lieu de "questions précises", Claude pose 2-3 questions supplémentaires pour atteindre 🟢 dès la première conversation. But : ne pas reporter la fermeture des sections en v2.1.

    Pattern reproductible (validé P3, P4 vague 1, P5 vague 1, P6 vague 1, P7 vague 1, P8 vague 1, 2026-06-06/07) : atteindre 🟢 dès la première conversation en combinant vague 1 + transformations implicites (5.5 → questions précises, 7 → projection, 8.5 → UDL). **P9 a 3-5 questions max vague 1 (single-agent justifié sauf gros refactoring, plus simple que P3/P4/P5/P6/P7 multi mais avec spécificité 4 types maintenance à arbitrer)**.

    Différence clé : l'utilisateur garde le contrôle de la grille (remplie offline) et Claude n'intervient qu'en analyse + questions + rédaction. Le rythme est 1 phase = 1 conversation (avec éventuellement 2 vagues de questions dans la même conversation).

    5. SPÉCIFICITÉS DE LA PHASE 9 (Maintenance)

    5.1 Mission

    Sustain and enhance software through corrective, adaptive, perfective, and preventive maintenance. P9 = changement de code planifié (4 types : Corrective bugfix, Adaptive env/dépendances/migrations, Perfective feature mineure/refactoring/optimisation, Preventive refactoring proactif/dette technique). P9 inclut l'impact analysis, le CAB approval pour les changements structurants, l'implémentation, le regression testing, la maintenance documentation, et la mise à jour de la knowledge base. P9 se concentre sur "modifier le code sans casser ce qui marche, avec traçabilité de chaque changement".

    5.2 Budget tokens (à confirmer en audit)

    - Stratégie actuelle : **3k/5k/8k** (P9 = single-agent sauf gros refactoring justifié)
    - À trancher : Nexus-Critic obligatoire ou adaptatif par type de maintenance ? P9 = patch + regression, pas création archi → Nexus-Critic = utile pour T2 spec-compliance + T3 régression predictor, T1 casseur si refactoring structurant ?
    - **Réflexion** : le mainteneur a tranché adaptatif par sévérité en P8 (mode unique au projet). Il pourrait vouloir adaptatif par type de maintenance en P9 (corrective rapide vs perfective structurante). Ou T1+T2+T3 obligatoire (cohérence P3-P7) si gros refactoring. À discuter.

    5.3 Concurrence

    - Single-agent justifié sauf gros refactoring (F13 recherche 2026 — P9 = patch + regression, pas multi-agent en standard)
    - Agent principal : Nexus-Backend OU Nexus-Frontend OU Nexus-DevOps (selon zone du patch) ou Nexus-Architect si refactoring structurant
    - Agents support : Nexus-Security (security patches), Nexus-QA (regression), Nexus-PM (priorisation)
    - Nexus-Critic : à trancher (cohérence P3-P7 = obligatoire, P9 = adaptatif par type ?)

    5.4 Livrables (à confirmer en audit)

    - maintenance-request.md (spec)
    - impact-analysis.md (spec)
    - change-implementation-report.md (spec)
    - regression-test-report.md (spec)
    - maintenance-log.md (spec)
    - updated-documentation.md (spec)
    - **Suggestions supplémentaires** (à confirmer) : diff/patch concret (PR + commits + tags), ADR si décision structurante, changelog public (semver, breaking changes), post-mortem si incident causé par patch, decision rationale (pourquoi cette approche)

    5.5 DÉMARCATION P8 ↔ P9 — DÉJÀ TRANCHÉE en P8 audit 2026-06-07

    **Démarcation P8 ↔ P9 = Run vs Change** (déjà inscrite dans P8 v2 finale) :
    - P8 = monitoring + incidents **sans modification code** (calibration alertes, post-mortem, escalade)
    - P9 = **changement de code planifié** (corrective/adaptive/perfective/preventive avec impact analysis + regression testing)
    - Cas limite type : "Calibrer un seuil d'alerte" = P8 (config monitoring). "Modifier le code pour réduire les alertes" = P9 (fix corrective). "Écrire post-mortem" = P8. "Implémenter action correctrice du post-mortem" = P9.

    5.6 DÉMARCATION P9 ↔ P10 — À TRANCHER EN AUDIT

    Critère à établir : P9 = changement de code (sustain + enhance system tournant). P10 = retirement (système EOL, archivage, conformité de fermeture). Si la décision = "modifier le code d'un système qui tourne" = P9. Si la décision = "arrêter, archiver, retirer le système" = P10. **Cas limite type** : "Maintenance d'un système en fin de vie" = P9 (encore en run) ou P10 (préparation EOL) ? "Refactoring lourd avant migration vers nouvelle version" = P9 (current version) ou P10 (préparation EOL) ?

    5.7 UDL — 7 éléments P9-spécifiques (suggestion, à valider)

    1. Maintenance type chosen (corrective/adaptive/perfective/preventive + rationale)
    2. Impact analysis result (scope, modules touchés, risque régression)
    3. CAB approval (si changement structurant, signature + date)
    4. Change implemented (commit hash + tag + PR URL)
    5. Regression test result (suite passée, taux, nouveaux défauts)
    6. Documentation updated (liste docs mis à jour, link)
    7. Post-maintenance review (sign-off, lessons learned, prochain cycle)

    5.8 Refus catégoriques (à confirmer en audit)

    - Pas de modif code sans impact analysis (impact obligatoire)
    - Pas de refonte déguisée en maintenance (escalade P3)
    - Pas de nouvelle feature structurante (escalade P2)
    - Pas de fix sans regression test (regression obligatoire)
    - Pas de fix rapide sans doc (dette explicite si pressé)
    - Pas de deploy en prod sans staging validé (escalade P7)
    - Pas de skip de CAB approval pour changement structurant
    - Pas de modification d'un système EOL (escalade P10)

    5.9 Critères d'échec (à confirmer en audit)

    - Régression après patch → hotfix urgent + rollback
    - Scope creep détecté (le "petit fix" devient feature) → retour P3
    - Nouveau défaut critique introduit → rollback + post-mortem
    - Documentation pas à jour 24h après → escalade mainteneur

    5.10 Couverture corpus (état 2026-06-06)

    - **30% de couverture** (faible, 3 livres canoniques disponibles localement sur ~10 recommandés)
    - 3 New Books : Refactoring at Scale (Lemaire 2020), Retrospectives Antipatterns (Corry 2020), Beyond Legacy Code (Bernstein 2015)
    - 1 Standard NIST/OWASP : NIST 800-161r1 (SCRM)
    - **2 lacunes critiques** : Working Effectively with Legacy Code (Feathers 2004) — 🔴 indispensable pour P9, Refactoring Databases (Sadalage 2006) — schéma evolution
    - Décision mainteneur 2026-06-06 : 30% accepté pour cadrage, batch d'acquisition ultérieur (acquérir Feathers + Sadalage en priorité)

    5.11 Spécificité P9 = consommation des CR émises par P8 + escalade vers P10

    P9 ne re-décide PAS le monitoring/incidents (P8) ni le retirement (P10). P9 se concentre sur "modifier le code planifié, regression testing, doc à jour". Toute déviation monitoring/incident = escalade P8. Toute déviation EOL/retirement = escalade P10. **CR formelles émises par P8** (depuis post-mortems action correctrice OU capacity planning scaling code OU incident systémique) = inputs principaux de P9.

    6. STRUCTURE D'UNE GRILLE DE PHASE (rappel)

    Chaque grille a 8 sections identiques :
    1. Charte (mission, périmètre, hors-périmètre)
    2. Conditions d'entrée/sortie (trigger, complétion, escalade)
    3. Inputs (depuis phases précédentes, utilisateur, sources externes)
    4. Outputs (deliverables, format, présentation, auditabilité)
    5. Mécanique opérationnelle (agents, tools, knowledge, adversarial, décisions user)
    6. Bornes & modes d'échec (refus, échecs, cas limites, escalade)
    7. Adéquation aux besoins (usage réel, friction, contournement, valeur, dette)
    8. Context Engineering (token budget, compaction, consultation, adversarial, UDL, + section 8.7 "Validation empirique 2026")

    Chaque section finit par un verdict 🟢/🟡/🔴. Verdict = un seul choix tranché.
    Verdict global en fin de grille. Sections 5.5 et 8.5 sont des points d'attention systématiques.

    Pattern reproductible (validé P3, P4, P5, P6, P7, P8 2026-06-06/07) : viser 🟢 dès la première conversation. Si la section 7 (utilité réelle) est vide, la remplir par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7/P8 v2. Si la section 5.5 est en format "catégories", la transformer en 3-5 questions précises avec options AskUserQuestion.

    7. RÉFÉRENCES P0 v2 → P8 v2 (pour P9)

    Budget & durée (alignés P0-P8 par défaut)
    - P0 = 4k/7k/10k ; P1 = 3k/5k/8k ; P2 = 4k/7k/10k ; P3-P7 = 5k/8k/15k (multi-agent justifié) ; P8 = adaptatif par sévérité incident (1k/2k/3k + 2k/4k/6k + 5k/8k/15k) ; **P9 = 3k/5k/8k (à confirmer en audit, possible adaptatif par type maintenance)**
    - Cap durée : 35 min partout
    - Token counter live : pre-tool-use/token-counter.sh (P9 hardcodé à 8k déjà — à vérifier)

    Mécanique agents (pattern P9 — single-agent justifié sauf gros refactoring)

    - Single-agent justifié (F13 recherche 2026) : Nexus-Backend OU Frontend OU DevOps OU Architect (selon zone)
    - P3-P7 = Nexus-Critic T1+T2+T3 obligatoire (multi-agent justifié)
    - P8 = Nexus-Critic adaptatif par sévérité incident (aucun courant / T2 standard / T1+T2+T3+Council critique)
    - **P9 = à trancher en audit** : T1+T2+T3 obligatoire (cohérence P3-P7) ? Adaptatif par type de maintenance (corrective rapide vs perfective structurante) ? T2 seul (spec-compliance vs design) ? T2+T3 (spec-compliance + regression predictor) ?

    Livrables (pattern P9)

    - 6 livrables par défaut (à confirmer + ajouts possibles : diff/patch, ADR, changelog, post-mortem, decision rationale)
    - Format : md pour les procédures, JSON pour les rapports machine, git (PR + commits + tags) pour le code

    Questions user (pattern P9 vague 1)

    - Vague 1 : 3-5 max (P9 = single-agent justifié sauf gros refactoring, plus simple que P3-P7 multi mais avec spécificité 4 types maintenance)
    - Format actionnable identique à AskUserQuestion (header + 2-4 options mutuellement exclusives par question)

    UDL

    - 7 éléments P9-spécifiques (aligné P3-P8)

    Couverture

    - Universelle adaptative (6 cas : greenfield, maintenance legacy, interne, externe, compliance, R&D)

    Rejouabilité

    - Oui + alternatives documentées par décision structurante

    Traçabilité

    - Max : source + alternatives + historique + UDL par item
    - CR → impact analysis → change implementation → regression test → maintenance log (chaque changement tracé)
    - Patch → commit hash → tag → PR URL (audit trail git)
    - Documentation → liste docs mis à jour + lien (chaque doc tracée)

    8. FINDINGS CAPITAUX À GARDER EN TÊTE (recherche 2026)

    - F1 : 80% de la variance perf = token usage (donc budget = proxy de qualité)
    - F2 : Multi-agent = 15× tokens chat ; single-agent = 4×
    - F3 : Subagent brief doit porter 4 champs : OBJECT/FORMAT/TOOLS/BOUND
    - F4 : Context rot : 18/18 modèles se dégradent à TOUT incrément
    - F5 : Lost-in-the-middle = -30% accuracy en positions 5-15
    - F6 : Mur à 35 min : failure rate × 4 quand durée × 2
    - F7 : 60% du 1er tour agent = retrieval (donc pre-hydrate critique)
    - F8 : Compaction à 95% = trop tard (Claude Code lui-même), viser 60-70%
    - F10 : Subagent output → filesystem (artefact persistant)
    - F11 : Prompt caching : stable prefix en tête uniquement
    - F12 : BM25 > embedding sur code → pour trouver le bug, grep + git log + AST > embedding search (TRÈS pertinent pour P9)
    - F13 : Single-agent ≥ multi-agent à budget tokens égal (Tran & Kiela 2026)

    Phases single-agent justifié : P0, P1, P2, P9 (sauf gros refactoring), P10
    Phases multi-agent justifié : P3, P4, P5, P6, P7
    Phases adaptatives : P8 (par sévérité incident), P9 (potentiellement par type maintenance, à trancher)

    4 failure modes Drew Breunig : poisoning, distraction, confusion, clash (audit obligatoire par grille)

    9. CONTRAINTES STRICTES (rappel)

    - ❌ NE PAS modifier ~/.claude/settings.json
    - ❌ NE PAS utiliser WebSearch natif (cassé, erreur 400 systématique)
    - ❌ NE PAS tenter de SSH distant (pas d'accès)
    - ❌ NE PAS poser des questions évidentes
    - ❌ NE PAS utiliser de jargon dans les questions
    - ✅ Lire les fichiers existants avant de répondre
    - ✅ Citer les sources primaires avec URL + date (pour les sources externes)
    - ✅ Être économe en tokens (Edit > Write pour minimiser le diff)
    - ✅ Répondre en français (le mainteneur communique en français)
    - ✅ Toujours proposer un verdict/action concrète à la fin
    - ✅ Utiliser mcp__web-search-prime__webSearchPrime pour recherche web (MCP Z.AI, PRINCIPAL)
    - ✅ Utiliser WebFetch pour récupérer une URL spécifique

    10. OUTILS DISPONIBLES

    - ✅ mcp__web-search-prime__webSearchPrime : recherche web (PRINCIPAL)
    - ✅ WebFetch : récupération URL spécifique
    - ✅ MCP zai tools (8) : analyse d'image/vidéo/OCR

    11. PREMIER RÉFLEXE
    12. Lis la grille d'audit audit/phase-9-maintenance-audit.md (template v1 que le mainteneur a rempli offline)
    13. Lis la spec specs/workflows/by-phase/phase-9-maintenance.md (v2-renum, à enrichir avec critères démarcation P8/P9 [déjà tranché] et P9/P10 [à trancher])
    14. Lis la stratégie audit/00-context-engineering-strategy.md (référence transverse, budgets)
    15. Lis les specs validées P0 v2 → P8 v2 finale (références du process d'audit) — fichiers specs/workflows/by-phase/phase-0-discovery.md, phase-1-concept-feasibility.md, phase-2-requirements.md, phase-3-architecture.md, phase-4-design.md, phase-5-implementation.md, phase-6-testing.md, phase-7-deployment.md, phase-8-operations.md
    16. Lis la mémoire swebok-v4-p8-spec-v2-vert-2026-06-07.md (référence process audit vague 1 pour P9, démarcations triple P7↔P8↔P9 Setup vs Run vs Change, spécificité P8 phase vivante, à appliquer tel quel pour la démarcation P8↔P9 [déjà tranchée])
    17. Lis la mémoire swebok-v4-structural-fix-2026-06-05.md (contexte du fix)
    18. Identifie les zones où la grille remplie est ambiguë, incomplète, ou en tension avec la spec
    19. Pose toutes les questions complémentaires nécessaires pour avoir un rapport très précis et exhaustif
    20. QUAND TU AS FINI

    Dis : "Terminé. X fait, Y à faire ensuite. Prochaine action suggérée : Z."
    Pas plus, pas moins. Le mainteneur décidera de la suite.

    À la fin, fournis le user prompt exhaustif pour la phase suivante (P10 Retirement) en suivant le même format, pour que le mainteneur puisse continuer le process dans une nouvelle conversation.

    Objectif final : atteindre 🟢 dès la première conversation, sans reporter la fermeture des sections en v2.1. Pattern vague 1 + transformations implicites = 3-5 questions total dans la même conversation, ~25-35 min de travail (P9 = single-agent justifié sauf gros refactoring, plus simple que P3-P7 multi mais avec spécificité 4 types maintenance à arbitrer).

    13. INSTRUCTIONS SPÉCIFIQUES POUR LE NOUVEAU PROCESS (vague 1 + transformations implicites)

    Tu es dans une nouvelle conversation dédiée à la phase 9. Le mainteneur a déjà rempli la grille audit/phase-9-maintenance-audit.md offline. Il va te la coller ci-dessous (cf. § 14) — OU elle est déjà à son emplacement habituel (cas P8) auquel cas tu la retrouves directement. Ton job :

    VAGUE 1 :
    1. Lire la grille remplie + la spec v2-renum + la stratégie + les références (P0 v2 → P8 v2 finale, mémoire structural-fix, mémoire P3/P4/P5/P6/P7/P8 spec v2 finale)
    2. Analyser la grille : qu'est-ce qui est cohérent, qu'est-ce qui manque, qu'est-ce qui est ambigu, qu'est-ce qui est en tension
    3. Identifier les zones d'incertitude où tu as besoin d'éclaircissement
    4. Poser 3-5 questions complémentaires via AskUserQuestion (en français simple, sans jargon, options mutuellement exclusives, 2-4 options par question). L'objectif : avoir un rapport très précis et exhaustif pour valider la phase
    5. Une fois les réponses obtenues : rédiger une spec v2 (réécriture complète si nécessaire, ou aménagement ciblé de la v2-renum — N'OUBLIE PAS D'AJOUTER LE CRITÈRE DE DÉMARCATION P9↔P10 ET DE RAPPELER P8↔P9), mettre à jour la grille (verdict 🟢/🟡/🔴 tranché, sections 5.5 et 8.5 comblées par les réponses du mainteneur), mettre à jour le budget dans la stratégie
    6. Appliquer le pattern P3/P4/P5/P6/P7/P8 : si la section 7 (utilité réelle) est vide, demander 2-3 questions supplémentaires pour la remplir par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7/P8 v2 ; si la section 5.5 est en format "catégories", la transformer en 3-5 questions précises avec options AskUserQuestion
    7. Atteindre verdict global 🟢 avant de passer à la phase suivante
    8. À la fin : fournir le user prompt exhaustif pour la phase suivante (P10 Retirement) en suivant le même format

    TRANSFORMATIONS IMPLICITES (dans la rédaction, sans questions supplémentaires) :
    - Si la section 7 reste 🟡 après vague 1, demander 2-3 questions pour la fermer par projection
    - Si la section 5.5 reste en "catégories", poser 2 questions pour la transformer en "questions précises"
    - Total vague 1 + transformations implicites = 3-5 questions, ~25-35 min

    Ne fais PAS les 5 rounds × 4 questions en une seule fois (ancien process). Le nouveau process est : grille offline → analyse → questions ciblées sur les zones d'incertitude (vague 1) → rédaction v2 → transformations implicites 5.5/7 (sans questions supplémentaires si possible) → user prompt pour phase suivante.

    Nombre de questions : à ta discrétion, en fonction de ce que la grille révèle. Pas de plafond, mais pas de questions évidentes non plus. Suggestion : **3-4 questions vague 1** = 3-4 questions total pour P9 (single-agent justifié sauf gros refactoring, plus simple que P3-P7 mais avec spécificité 4 types maintenance).

    14. GRILLE FOURNIE PAR L'UTILISATEUR (P9 Maintenance)

    ▎ ⚠️    Le mainteneur collera ci-dessous le contenu rempli de audit/phase-9-maintenance-audit.md (la grille qu'il a remplie offline dans son éditeur). OU la grille est dans son folder habituel /home/doz/swebok-v4-harness-distilled/audit/phase-9-maintenance-audit.md (cas P8) — auquel cas la retrouver directement.
    ▎
    ▎ espace réservé pour la grille remplie

    ---DÉMARRAGE : lis la grille remplie que le mainteneur va coller ci-dessous (OU retrouve-la dans /home/doz/swebok-v4-harness-distilled/audit/phase-9-maintenance-audit.md si elle n'est pas collée), puis suis le process § 13 (vague 1 + transformations implicites). Si la grille n'est pas encore collée ET non trouvée à l'emplacement habituel, demande au mainteneur de la coller.

    La grille P9 est dans son folder habituel, donc je ne la copie colle pas ici, retrouve la.
