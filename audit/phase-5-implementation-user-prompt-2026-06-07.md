[CONTEXTE PROJET — à lire en premier]

  Tu es une instance de Claude Code qui prend la suite d'un travail d'audit structuré du projet SWEBOK v4 Harness Distilled. Le mainteneur (utilisateur) a déjà :
  - cadré le projet stratégiquement (2026-06-04)
  - fermé la phase 0 (Discovery) à 100% (spec v2, 2026-06-04)
  - fermé la phase 1 (Concept/Feasibility) à 100% (spec v2, 2026-06-06)
  - fermé la phase 2 (Requirements) à 100% (spec v2, 2026-06-05)
  - fermé la phase 3 (Architecture) à 100% (spec v2 finale 🟢, 2026-06-06, 8 décisions tranchées, 15/15 P1 closes)
  - fermé la phase 4 (Design) à 100% (spec v2 finale 🟢, 2026-06-07, 4 décisions tranchées vague 1, matrice ADR P3 obligatoire)
  - appliqué un fix structurel majeur le 2026-06-05 (modèle 9-phases → 10-phases)

  Ta mission : auditer la phase 5 (Implementation) en suivant le nouveau process (décrit § 13 ci-dessous).

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
  - Méthode audit : grille offline + questions AskUserQuestion ciblées (validée pour P1 v2, P3 v2 finale, P4 v2 finale). L'ancien process 5 rounds × 4 questions (P0/P2) reste valide pour les phases complexes.

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
  │ P5    │ Implementation      │ P4                   │ v2-renum          │ v1 (template) │ ⬜ PROCHAINE  │
  ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
  │ P6    │ Testing             │ P5                   │ v2-renum          │ v1            │ ⬜ À faire    │
  ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
  │ P7    │ Deployment          │ Software Config Mgmt │ v2-renum          │ v1            │ ⬜ À faire    │
  ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
  │ P8    │ Operations          │ (hors core)          │ v2-renum          │ v1            │ ⬜ À faire    │
  ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
  │ P9    │ Maintenance         │ P6                   │ v2-renum          │ v1            │ ⬜ À faire    │
  ├───────┼─────────────────────┼──────────────────────┼───────────────────┼───────────────┼───────────────┤
  │ P10   │ Retirement          │ Software Eng Process │ v2-renum          │ v1            │ ⬜ À faire    │
  └───────┴─────────────────────┴──────────────────────┴───────────────────┴───────────────┴───────────────┘

  Mémoire projet :
  - swebok-v4-structural-fix-2026-06-05.md : détails du fix 9→10 phases
  - swebok-v4-strategic-cadrage-2026-06-04.md : décisions A1/B/C
  - swebok-v4-p0-spec-v2-2026-06-04.md : référence process audit ancien (5×4 questions)
  - swebok-v4-p1-spec-v2-2026-06-06.md : référence process audit nouveau vague 1 (grille offline + 7 questions)
  - swebok-v4-p2-spec-v2-2026-06-05.md : référence process audit ancien (5×4 questions)
  - swebok-v4-p3-spec-v2-2026-06-06.md : référence process audit nouveau vague 1 (grille offline + 6 questions, verdict 🟡 initial)
  - swebok-v4-p3-spec-v2-vert-2026-06-06.md : référence process audit nouveau vague 2 (2 questions supplémentaires, verdict 🟢 final)
  - swebok-v4-p4-spec-v2-vert-2026-06-07.md : référence process audit nouveau vague 1 (grille offline + 4 questions, verdict 🟢 direct)

  4. NOUVEAU PROCESS (validé 2026-06-07, à suivre pour chaque phase)

  Ancien process (P0 et P2) : 5 rounds × 4 questions AskUserQuestion = 20 décisions tranchées en une seule conversation.

  Nouveau process vague 1 (validé pour P1, P3 vague 1, P4 vague 1) :
  1. Le mainteneur remplit la grille d'audit offline dans son éditeur (VSCode, vim, etc.).
  2. Le mainteneur ouvre une nouvelle conversation Claude Code.
  3. Il colle en début de conversation : (a) le user prompt transfert (celui que tu es en train de lire) + (b) le contenu rempli de la grille de la phase en question.
  4. L'instance Claude de cette nouvelle conversation : (a) analyse la grille remplie, (b) pose toutes les questions complémentaires nécessaires pour avoir un rapport très précis et exhaustif (AskUserQuestion, en français simple sans jargon), (c) attend les réponses, (d) rédige la spec v2 + met à jour la grille (verdict tranché, sections 5.5 et 8.5 comblées), (e) met à jour le budget dans la stratégie.
  5. À la fin, l'instance Claude fournit un nouveau user prompt exhaustif pour que le mainteneur puisse continuer le process dans la conversation suivante.

  Nouveau process vague 2 (validé pour P3, à appliquer pour P5-P10) : après la vague 1, si des sections restent 🟡 (notamment section 7 utilité réelle) ou si la section 5.5 est en format "catégories" au lieu de "questions précises", Claude pose 2-3 questions supplémentaires pour atteindre 🟢 dès la première conversation. But : ne pas reporter la fermeture des sections en v2.1.

  Pattern reproductible (validé P4 vague 1, 2026-06-07) : atteindre 🟢 dès la première conversation en combinant vague 1 + transformations implicites (5.5 → questions précises, 7 → projection). P5 a 4-6 questions max vague 1.

  Différence clé : l'utilisateur garde le contrôle de la grille (remplie offline) et Claude n'intervient qu'en analyse + questions + rédaction. Le rythme est 1 phase = 1 conversation (avec éventuellement 2 vagues de questions dans la même conversation).

  5. SPÉCIFICITÉS DE LA PHASE 5 (Implementation)

  5.1 Mission

  Transform the design specifications (DDS, contracts, data structures) into production-ready code — code source, intégration, CI/CD, gestion de la dette technique. P5 inclut ses propres estimations effort (absent des phases précédentes).

  5.2 Budget tokens (à confirmer en audit)

  - Base : 5k tokens (aligné P3/P4)
  - Soft cap : 10k tokens (P5 = phase la plus dense, plus que P3/P4)
  - Hard cap : 15k tokens (le plus large du projet, justifié par l'activité 1 du projet)
  - Cap durée : 35 min

  5.3 Concurrence

  - Multi-agent justifié (P5 = activité 1 du projet, read-heavy parallèle + disjoint tools) : 3-5 sub-agents max
  - Agents typiques : Nexus-Backend (lead code), Nexus-Frontend, Nexus-DevOps, Nexus-Security, Nexus-Architect (conformité ADRs P3 + DDS P4)
  - Nexus-Critic : OBLIGATOIRE pour P3/P4, à trancher pour P5 (question ouverte 3 stratégie pas encore tranchée pour P5)
  - Activités typiques : Code construction, Integration, CI/CD setup, Reuse (libraries internes), Dette technique tracking

  5.4 Livrables (7 par défaut, à confirmer)

  - source-code/ (par module, généré depuis P4 DDS)
  - integration-tests/ (intégration entre modules)
  - build-config/ (Makefile, package.json, etc.)
  - ci-cd-config/ (GitHub Actions, scripts de déploiement)
  - technical-debt-register.md (dette technique P5)
  - code-review-report.md (revues pair-à-pair + Nexus-Critic)
  - implementation-report.md (résumé 1 page : modules livrés, dette, estimations réelles vs estimées)

  5.5 DÉMARCATION P4 ↔ P5 — À TRANCHER EN AUDIT (vs P3↔P4 déjà tranchée)

  Critère à établir : P4 = COMMENT (DDS, signatures, algos), P5 = le code qui implémente. Si la décision = "comment on structure le code" (organisation fichiers, naming, classes abstraites, etc.) = P5. Si la décision = "quelle interface a tel module, quelle algo" = P4. À valider en audit.

  5.6 UDL — 7 éléments P5-spécifiques (suggestion, à valider)

  1. Module code completed (pointeur vers source-code/)
  2. Library / dependency added (avec rationale, vendor lock-in check)
  3. Estimation réelle vs estimée (effort P5 = input pour P6, P7, P8)
  4. Reuse vs create-from-scratch (décision documentée)
  5. Dette technique introduite (pointeur vers technical-debt-register.md)
  6. Rejet T1/T2 casseur (quand Nexus-Critic a trouvé un problème)
  7. Décision "pas de décision" (escaladée à P3/P4 ou mainteneur)

  5.7 Refus catégoriques (5, à confirmer)

  - Pas de re-décision architecturale (escalade P3, règle démarcation)
  - Pas de re-décision design (escalade P4)
  - Pas de tests d'acceptation (P6)
  - Pas de déploiement (P7)
  - Pas de monitoring/alerting (P8)

  5.8 Critères d'échec (6, à confirmer)

  - Big ball of mud (pas de respect des patterns P4)
  - Vendor lock-in non documenté
  - Dette technique non trackée
  - Pas de tests unitaires par module
  - Pas d'intégration continue (CI cassé ou absent)
  - Code qui ne respecte pas les NFR P2 (perf, sécurité)

  5.9 Couverture corpus (état 2026-06-06)

  - **100% de couverture** — P5 = phase la mieux couverte (Clean Code, Pragmatic Programmer, Code Complete 2nd ed, Mythical Man-Month, etc., tous disponibles localement)
  - C'est la seule phase à 100%, ce qui est attendu car Implementation = phase la plus "core" du corpus SWEBOK

  5.10 Spécificité P5 = consommation des DDS P4 + ADRs P3

  P5 ne re-décide PAS le design (escalade P4) ni l'architecture (escalade P3). P5 consomme les DDS P4 et descend au niveau code (source, intégration, CI/CD). Toute déviation DDS P4 = escalade P4. Toute déviation ADR P3 = escalade P3.

  6. STRUCTURE D'UNE GRILLE DE PHASE

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

  Pattern reproductible (validé P3, P4 2026-06-07) : viser 🟢 dès la première conversation. Si la section 7 (utilité réelle) est vide, la remplir par projection + cohérence P0/P1/P2/P3/P4 v2 (pas attendre externe/terrain). Si la section 5.5 est en format "catégories", la transformer en 5-7 questions précises avec options AskUserQuestion. Vague 2 de 2-3 questions dans la même conversation suffit.

  7. RÉFÉRENCES P0 v2 + P1 v2 + P2 v2 + P3 v2 + P4 v2 (pour P5)

  Budget & durée (alignés P0 + P1 + P2 + P3 + P4 par défaut)
  - P0 = 4k/7k/10k ; P1 = 3k/5k/8k ; P2 = 4k/7k/10k ; P3 = 5k/8k/15k ; P4 = 5k/8k/15k ; **P5 = 5k/10k/15k** (le plus large, à confirmer en audit)
  - Cap durée : 35 min partout
  - Token counter live : pre-tool-use/token-counter.sh (P5 hardcodé à 15k déjà)

  Mécanique agents (pattern P5)

  - Multi-agent justifié (P5 = activité 1 du projet, read-heavy parallèle + disjoint tools)
  - P3 = Nexus-Critic T1+T2+T3 obligatoire
  - P4 = Nexus-Critic T1+T2+T3 obligatoire
  - P5 = à trancher en audit : Nexus-Critic obligatoire / sélectif / pas de Nexus-Critic
  - Justification possible P5 sans Nexus-Critic obligatoire : code review pair-à-pair suffit ? ou Nexus-Critic sur le code compilé uniquement ?

  Livrables (pattern P5)

  - 7 livrables par défaut (à confirmer en audit)
  - Format : code source (par module) + tests intégration + CI/CD config + dette technique

  Questions user (pattern P5 vague 1 + vague 2)

  - Vague 1 : 4-6 max (cohérence P4 v2, ajustement selon complexité)
  - Vague 2 : transformer les catégories en 5-7 questions précises avec options AskUserQuestion
  - Format actionnable identique à AskUserQuestion (header + 2-4 options mutuellement exclusives par question)

  UDL

  - 7 éléments P5-spécifiques (aligné P3, P4)

  Couverture

  - Universelle adaptative (6 cas : greenfield, maintenance, interne, externe, compliance, R&D)

  Rejouabilité

  - Oui + alternatives documentées par décision structurante

  Traçabilité

  - Max : source + alternatives + historique + UDL par item
  - Module → DDS P4 → ADR P3 → NFR P2 (chaque ligne de code tracée jusqu'au requirement)
  - Conformité ADR P3 vérifiée (héritée de la matrice P4)
  - Conformité DDS P4 vérifiée (matrice DDS → code)

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
  - F13 : Single-agent ≥ multi-agent à budget tokens égal (Tran & Kiela 2026)

  Phases single-agent justifié : P0, P1, P2, P7, P8, P9, P10
  Phases multi-agent justifié : P3, P4, P5, P6

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
  12. Lis la grille d'audit audit/phase-5-implementation-audit.md (template v1 que le mainteneur a rempli offline)
  13. Lis la spec specs/workflows/by-phase/phase-5-implementation.md (v2-renum, à enrichir avec critère démarcation P4/P5)
  14. Lis la stratégie audit/00-context-engineering-strategy.md (référence transverse, budgets)
  15. Lis les specs validées P0 v2, P1 v2, P2 v2, P3 v2 finale, P4 v2 finale (références du process d'audit) — fichiers specs/workflows/by-phase/phase-0-discovery.md, phase-1-concept-feasibility.md, phase-2-requirements.md, phase-3-architecture.md, phase-4-design.md
  16. Lis la mémoire swebok-v4-p4-spec-v2-vert-2026-06-07.md (référence process audit vague 1 pour P5, à appliquer tel quel)
  17. Lis la mémoire swebok-v4-structural-fix-2026-06-05.md (contexte du fix)
  18. Identifie les zones où la grille remplie est ambiguë, incomplète, ou en tension avec la spec
  19. Pose toutes les questions complémentaires nécessaires pour avoir un rapport très précis et exhaustif
  20. QUAND TU AS FINI

  Dis : "Terminé. X fait, Y à faire ensuite. Prochaine action suggérée : Z."
  Pas plus, pas moins. Le mainteneur décidera de la suite.

  À la fin, fournis le user prompt exhaustif pour la phase suivante (P6 Testing) en suivant le même format, pour que le mainteneur puisse continuer le process dans une nouvelle conversation.

  Objectif final : atteindre 🟢 dès la première conversation, sans reporter la fermeture des sections en v2.1. Pattern vague 1 + transformations implicites = 4-6 questions total dans la même conversation, ~30-45 min de travail.

  13. INSTRUCTIONS SPÉCIFIQUES POUR LE NOUVEAU PROCESS (vague 1 + transformations implicites)

  Tu es dans une nouvelle conversation dédiée à la phase 5. Le mainteneur a déjà rempli la grille audit/phase-5-implementation-audit.md offline. Il va te la coller ci-dessous (cf. § 14). Ton job :

  VAGUE 1 :
  1. Lire la grille remplie + la spec v2-renum + la stratégie + les références (P0 v2, P1 v2, P2 v2, P3 v2, P4 v2 finale, mémoire structural-fix, mémoire P3 spec v2 finale, mémoire P4 spec v2 finale)
  2. Analyser la grille : qu'est-ce qui est cohérent, qu'est-ce qui manque, qu'est-ce qui est ambigu, qu'est-ce qui est en tension
  3. Identifier les zones d'incertitude où tu as besoin d'éclaircissement
  4. Poser 4-6 questions complémentaires via AskUserQuestion (en français simple, sans jargon, options mutuellement exclusives, 2-4 options par question). L'objectif : avoir un rapport très précis et exhaustif pour valider la phase
  5. Une fois les réponses obtenues : rédiger une spec v2 (réécriture complète si nécessaire, ou aménagement ciblé de la v2-renum — N'OUBLIE PAS D'AJOUTER LE CRITÈRE DE DÉMARCATION P4↔P5), mettre à jour la grille (verdict 🟢/🟡/🔴 tranché, sections 5.5 et 8.5 comblées par les réponses du mainteneur), mettre à jour le budget dans la stratégie
  6. Appliquer le pattern P3/P4 : si la section 7 (utilité réelle) est vide, demander 2-3 questions supplémentaires pour la remplir par projection + cohérence P0/P1/P2/P3/P4 v2 ; si la section 5.5 est en format "catégories", la transformer en 5-7 questions précises avec options AskUserQuestion
  7. Atteindre verdict global 🟢 avant de passer à la phase suivante
  8. À la fin : fournir le user prompt exhaustif pour la phase suivante (P6 Testing) en suivant le même format

  TRANSFORMATIONS IMPLICITES (dans la rédaction, sans questions supplémentaires) :
  - Si la section 7 reste 🟡 après vague 1, demander 2-3 questions pour la fermer par projection
  - Si la section 5.5 reste en "catégories", poser 2 questions pour la transformer en "questions précises"
  - Total vague 1 + transformations implicites = 4-6 questions, ~30-45 min

  Ne fais PAS les 5 rounds × 4 questions en une seule fois (ancien process). Le nouveau process est : grille offline → analyse → questions ciblées sur les zones d'incertitude (vague 1) → rédaction v2 → transformations implicites 5.5/7 (sans questions supplémentaires si possible) → user prompt pour phase suivante.

  Nombre de questions : à ta discrétion, en fonction de ce que la grille révèle. Pas de plafond, mais pas de questions évidentes non plus. Suggestion : 4-6 questions vague 1 = 4-6 questions total pour P5.

  14. GRILLE FOURNIE PAR L'UTILISATEUR (P5 Implementation)

  ▎ ⚠️   Le mainteneur collera ci-dessous le contenu rempli de audit/phase-5-implementation-audit.md (la grille qu'il a remplie offline dans son éditeur).
  ▎
  ▎ espace réservé pour la grille remplie

  ---DÉMARRAGE : lis la grille remplie que le mainteneur va coller ci-dessous, puis suis le process § 13 (vague 1 + transformations implicites). Si la grille n'est pas encore collée, demande au mainteneur de la coller.

  La grille P5 est dans son folder habituel, donc je ne la copie colle pas ici, retrouve la.
