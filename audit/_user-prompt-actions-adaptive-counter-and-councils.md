[CONTEXTE PROJET — à lire en premier]

    Tu es une instance de Claude Code qui prend la suite d'un projet **complet à 🟢** : SWEBOK v4 Harness Distilled a terminé son audit systématique des 10 phases du cycle de vie SDLC. Le mainteneur (utilisateur) a déjà :
    - cadré le projet stratégiquement (2026-06-04, A1 séquentiel strict, B seuil fort impact, C T1+T2 standard + T3 optionnel, cible universelle)
    - fermé les 10 phases à 🟢 verdict global (P0 Discovery 2026-06-04 → P10 Retirement 2026-06-07)
    - appliqué le fix structurel majeur 2026-06-05 (modèle 9-phases → 10-phases canonique 1-par-1 SWEBOK v4)
    - commité le récap final et tagué **v2.0.0-audit-complete** (commit c3a1b76 sur master, 42 fichiers, 15 927 insertions, tag annoté poussé sur origin)
    - laissé en untracké les 497 MB de PDFs open-access dans `audit/corpus-references/downloads/` (décision à traiter plus tard)

    **Le projet est COMPLET côté audit SDLC.** Tu n'as PAS de nouvelle phase à auditer. Tu as **2 actions de suivi nice-to-have** à implémenter, regroupées ici car elles partagent le même thème "mécanique adaptative selon criticité/sévérité/conformité" :

    1. **Action P8-1 / P9-1 / P10-1** : faire évoluer `pre-tool-use/token-counter.sh` pour supporter un mode adaptatif 3-niveaux (env var ou flag).
    2. **Action P8-3 / P9-4 / P10-3** : formaliser les 3 Councils (post-incident P0/P1, structurante maintenance, clôture retirement) qui sont mentionnés dans les specs P8/P9/P10 v2 finale mais n'ont pas de fiche dédiée.

    Ces 2 actions sont **non bloquantes**, **nice-to-have**, mais **techniquement nécessaires** pour que les modes adaptatifs (P8=3 niveaux par sévérité, P9=3 niveaux par criticité, P10=3 niveaux par conformité) fonctionnent réellement, et pour que les 3 Councils aient une procédure vérifiable au lieu d'être juste "Council CISO+DevOps-Lead+SM" dans la spec.

    1. PROJET

    - Nom : SWEBOK v4 Harness Distilled — framework SDLC pour Claude Code (10 phases canoniques, multi-agent, adversarial gate, state machine SQLite, token counter live, hooks PreToolUse).
    - Localisation : /home/doz/swebok-v4-harness-distilled/
    - Mainteneur : technique, pressé, veut du concret. Il parle français, communication simple SANS jargon.
    - État GitHub : repo public doz34/swebok-v4-harness-distilled, MIT, **tag v2.0.0-audit-complete** annoté (audit SDLC complet 2026-06-08). Versions production code = v1.5.4 → v1.5.11 (inchangées, le tag v2.0.0 marque la fin de l'audit SDLC pas une release code).
    - But ultime : outillage parfait pour le mainteneur, audit-certified sur les 10 phases, prêt à l'emploi sur n'importe quel nouveau projet.

    2. DÉCISIONS STRATÉGIQUES DÉJÀ CADRÉES (NON NÉGOCIABLES)

    - A1 — Modèle de phases : UNE SEULE phase active à la fois (séquentiel strict). Au sein d'une phase, parallélisme libre. Les autres phases sont consultables en lecture seule (cache).
    - B — Seuil question utilisateur : uniquement les décisions à fort impact / irréversibles. Réversibles à faible coût = documentées + reportées. Triviales = silencieuses. Si l'utilisateur n'a pas d'avis = système choisit en autonomie.
    - C — Pattern adversarial : T1 (producteur vs casseur) + T2 (spec-compliance) en standard. T3 (conséquentialiste aval) en option, activé selon la phase.
    - Cible utilisateur : universelle (vibecodeur à développeur senior). Le même install, le même workflow, l'assistance s'adaptant au profil.
    - Un seul produit canonique : la version "anonymisation du corpus" (v2 multi-view, distilled). L'ancienne version doit être archivée.
    - **Nexus-Critic ADAPTATIF** : T1+T2+T3 obligatoire (P3-P7), adaptatif sévérité (P8), adaptatif criticité (P9), adaptatif criticité conformité (P10).
    - **Mécanique agent par phase** : P0/P1/P2 = single, P3-P7 = multi justifié, P8 = adaptatif sévérité, P9 = adaptatif criticité 3-niveaux, P10 = adaptatif criticité conformité 3-niveaux.
    - **Démarcations complètes** : P3↔P4, P4↔P5, P5↔P6, P6↔P7, P7↔P8, P8↔P9, P9↔P10, P10↔P0. Toutes les frontières de phase sont explicites.
    - **Fail-open sur hooks et compteur** : le token counter est de l'observabilité, pas une security gate. Il ne doit JAMAIS bloquer le travail légitime. Si l'env var est invalide, fallback silencieux au budget par défaut de la phase. Si un mode n'est pas reconnu, ignorer et continuer.
    - **Pas de modification de ~/.claude/settings.json** : le mainteneur a cette contrainte dure (cf. § 9). Le settings.json du repo (chemin relatif) peut être modifié si nécessaire.

    3. ÉTAT DE L'AUDIT (au 2026-06-08) — **COMPLET, RÉCAP TAGUÉ**

    ┌───────┬─────────────────────┬──────────────────────┬───────────┬─────────────┐
    │ Phase │         Nom         │      SWEBOK v4       │   Spec    │   Statut    │
    ├───────┼─────────────────────┼──────────────────────┼───────────┼─────────────┤
    │ P0    │ Discovery           │ (hors SWEBOK)        │ v2        │ ✅ FERMÉ 🟢 │
    │ P1    │ Concept/Feasibility │ Software Eng Mgmt    │ v2        │ ✅ FERMÉ 🟢 │
    │ P2    │ Requirements        │ P1                   │ v2        │ ✅ FERMÉ 🟢 │
    │ P3    │ Architecture        │ P2                   │ v2 finale │ ✅ FERMÉ 🟢 │
    │ P4    │ Design              │ P3                   │ v2 finale │ ✅ FERMÉ 🟢 │
    │ P5    │ Implementation      │ P4                   │ v2.1 fin. │ ✅ FERMÉ 🟢 │
    │ P6    │ Testing             │ P5                   │ v2 finale │ ✅ FERMÉ 🟢 │
    │ P7    │ Deployment          │ Software Config Mgmt │ v2 finale │ ✅ FERMÉ 🟢 │
    │ P8    │ Operations          │ (hors core)          │ v2 finale │ ✅ FERMÉ 🟢 │
    │ P9    │ Maintenance         │ P6                   │ v2 finale │ ✅ FERMÉ 🟢 │
    │ P10   │ Retirement          │ Software Eng Process │ v2 finale │ ✅ FERMÉ 🟢 │
    └───────┴─────────────────────┴──────────────────────┴───────────┴─────────────┘

    **Total** : 10 phases validées en ~3 jours (2026-06-04 → 2026-06-07), pattern reproductible vague 1 + transformations implicites = 3-4 questions par phase, ~25-35 min par phase. Récap final committé en `c3a1b76` et tagué `v2.0.0-audit-complete` (annoté) le 2026-06-08.

    4. MISSION 1 — ACTION P8-1 / P9-1 / P10-1 : TOKEN COUNTER ADAPTATIF 3-NIVEAUX

    4.1 État actuel

    Le fichier `pre-tool-use/token-counter.sh` (105 lignes, +rwxr-xr-x) implémente un compteur de tokens par phase. Il est appelé en pre-tool-use hook sur 4 matchers (Write/Edit, Bash, Skill/Task/mcp, mcp__*/Glob/Grep). Il :
    - Lit le payload JSON via stdin
    - Estime les tokens (len/4 heuristic)
    - Lit la phase courante depuis le state engine (`current_phase`)
    - Applique un budget hardcodé par phase via un `case` (lignes 57-70)
    - Persiste dans le state engine (clé `${phase}.tokens.used`)
    - Warn à soft cap et 85% du hard cap, block au hard cap
    - **Fail-open** : si state DB manque, pas de stdin, ou erreur python → exit 0 silencieux (ligne 14-15 `trap 'exit 0' ERR`)

    Budgets hardcodés actuels (extraits lignes 66-68) :
    ```bash
    P8|P8_OPERATIONS)             base=2000; soft=4000; hard=6000  ;;  # défaut = incident standard, couvre 90% des cas
    P9|P9_MAINTENANCE)            base=3000; soft=5000; hard=8000  ;;  # défaut = corrective standard, couvre 50% des cas
    P10|P10_RETIREMENT)           base=2000; soft=3000; hard=5000  ;;  # défaut = RGPD, couvre 60% des cas
    ```

    4.2 Spec cible : 3 budgets adaptatifs par phase

    D'après les specs v2 finale (cf. P8 §8.1, P9 §8.1, P10 §8.1) :

    **P8 Operations — adaptatif par sévérité incident** :
    - `monitoring` (courant, single Nexus-SM sans Critic) : base=1000, soft=2000, hard=3000
    - `standard` (incident P2/P3, single + Critic T2) : base=2000, soft=4000, hard=6000 (= défaut actuel)
    - `critical` (incident P0/P1, multi + Critic T1+T2+T3 + Council) : base=5000, soft=8000, hard=15000

    **P9 Maintenance — adaptatif par criticité maintenance** :
    - `hotfix` (typo/micro-tâche, single --lite sans Critic) : base=1000, soft=2000, hard=3000
    - `standard` (corrective/adaptive/preventive, single + Critic T1+T2+T3) : base=3000, soft=5000, hard=8000 (= défaut actuel)
    - `structurant` (perfective lourde, multi + Critic T1+T2+T3 + Council) : base=5000, soft=8000, hard=15000

    **P10 Retirement — adaptatif par criticité conformité** :
    - `simple` (archivage simple, single + T2 seul) : base=1000, soft=2000, hard=3000
    - `rgpd` (RGPD/standard métier, single + T1 casseur + T2 conformité) : base=3000, soft=5000, hard=8000 (= défaut actuel, couvre 60% des cas)
    - `regulated` (Finance/Santé/Défense, multi + T1+T2+T3 + Council) : base=5000, soft=8000, hard=15000

    4.3 Mécanisme technique proposé

    **Option A — env var (recommandée, plus simple pour hooks)** : `SWEBOK_P{PHASE}_MODE` où PHASE = P8|P9|P10. Valeurs reconnues :
    - P8 : `monitoring|standard|critical`
    - P9 : `hotfix|standard|structurant`
    - P10 : `simple|rgpd|regulated`

    Le hook lit l'env var en début de script. Si définie et valide → applique le budget correspondant. Si non définie ou invalide → fallback silencieux au budget hardcodé par défaut (comportement actuel préservé).

    **Option B — flag passé via stdin JSON** : modifier le matcher pour passer un argument additionnel. Plus complexe, requires coordination avec les matchers Claude Code. Non recommandé.

    **Recommandation** : Option A (env var). Le mainteneur (ou l'orchestrateur) définit `SWEBOK_P8_MODE=critical` en début de session incident P0/P1, etc. Cohérent avec le fail-open hook (l'env var n'est jamais bloquante).

    4.4 Livrables Mission 1

    - `pre-tool-use/token-counter.sh` modifié (Edit ciblé, lignes 66-68 du `case`) :
      - Ajouter lecture env var `SWEBOK_P{PHASE}_MODE` après le `case` (ou dans le case via une fonction `get_budget_for_phase()`)
      - Si mode défini et reconnu → override base/soft/hard
      - Si mode non reconnu → fallback silencieux + log `[TOKEN-COUNTER] WARN: unknown mode X for phase Y, using default`
      - Pour les phases non-adaptatives (P0-P7), comportement strictement inchangé
    - Commentaire en tête de section indiquant les 3 modes supportés par phase
    - (optionnel) `tests/pre-tool-use/test-token-counter-modes.sh` : 9 cas de test (3 niveaux × 3 phases) + 1 cas fallback défaut + 1 cas mode invalide. Tests bash simples, exit 0 = PASS.
    - (optionnel) Mise à jour de la stratégie `audit/00-context-engineering-strategy.md` section 5 (note : déjà à jour depuis P8/P9/P10 audits, juste vérifier cohérence)
    - CHANGELOG.md : entrée sous "v2.1.0" ou "v2.0.1" avec "Token counter : support mode adaptatif 3-niveaux P8/P9/P10"

    4.5 Critères de validation Mission 1

    - [ ] Le script reste fail-open (test : `unset SWEBOK_P8_MODE && pre-tool-use/token-counter.sh < input.json` → exit 0, budget par défaut)
    - [ ] Le script respecte le mode quand l'env var est valide (test : `SWEBOK_P8_MODE=critical ...` → utilise 5k/8k/15k)
    - [ ] Mode invalide → fallback silencieux + warn non bloquant
    - [ ] Phases non-adaptatives (P0-P7) strictement inchangées
    - [ ] Pas de régression sur les 92+ tests existants (bash-based test runners, cf. mémoire v1.5.11)
    - [ ] Script reste lisible (~120-140 lignes max, pas de complexité inutile)

    5. MISSION 2 — ACTIONS P8-3 / P9-4 / P10-3 : FORMALISER LES 3 COUNCILS

    5.1 État actuel

    Les 3 Councils sont mentionnés dans les specs v2 finale (cf. extraits grep ci-dessus) mais n'ont pas de fiche dédiée. Voici ce qui est documenté :

    **P8-3 : Council post-incident P0/P1**
    - Membres : CISO + DevOps-Lead + SM (Site Reliability / Service Manager)
    - Déclencheur : incident P0 (service down, security breach) ou P1 (SLO breach)
    - Timing : examen 1h dans les 5 jours suivant l'incident
    - Input : post-mortem complet (full RCA), runbook P7, SLA P2
    - Output : sign-off, action correctrice validée, leçons à intégrer (escalade P9 si code, escalade P7 si monitoring)
    - Référentiel : cohérent avec Google SRE Book (chap. Postmortem Culture) + ITIL v4 (Incident Management)

    **P9-4 : Council structurante**
    - Membres : CISO + DevOps-Lead + Architect
    - Déclencheur : Q3 user 5.5 = OUI (CAB approval requise pour changement structurant)
    - Timing : examen 1h avant deploy
    - Input : patch + impact analysis + DDS P4 + ADRs P3 + NFR P2
    - Output : sign-off, approbation finale, conditions de deploy
    - Référentiel : cohérent avec ITIL v4 (Change Advisory Board) + IEEE 1219 (Maintenance)

    **P10-3 : Council de clôture conditionnel par criticité**
    - 3 niveaux :
      - **archivage simple** : signature Nexus-DevOps-Lead seul (pas de Council formel)
      - **RGPD/standard métier** : signature Nexus-DevOps-Lead + CISO + Legal (mini-council 3 personnes, pas d'examen 1h formel)
      - **Finance/Santé/Défense** : Council formel obligatoire = CISO + Legal + PM + DevOps-Lead, examen 1h avant `PROJECT_RETIRED`
    - Input : EOL decision, retirement type, criticité conformité, data inventory, ownership transfer plan
    - Output : signature collective (regulated) ou signatures individuelles (RGPD/simple), compliance sign-off, réversibilité window configurée
    - Référentiel : ISO/IEC/IEEE 12207:2017 + RGPD + Data Retention Policies

    5.2 Format de formalisation proposé

    Créer un dossier `docs/councils/` (à la racine du repo) avec 3 fichiers `P8-incident-council.md`, `P9-structurante-council.md`, `P10-cloture-council.md`, chacun suivant la structure commune :

    ```markdown
    # Council {Nom} ({phase})

    ## Purpose
    {1 phrase : raison d'être du Council}

    ## Trigger
    {Conditions de convocation : sévérité, criticité, conformité, etc.}

    ## Membership
    {Rôles + agents nexus-* correspondants}

    ## Process
    {Timing, durée, input, output}

    ## Input artifacts
    {Liste des livrables à fournir au Council}

    ## Output artifacts
    {Liste des livrables produits par le Council (sign-off, action correctrice, etc.)}

    ## Failures & escalations
    {Que faire si le Council ne peut pas se réunir, désaccord, refus de signature, etc.}

    ## References
    {Référentiels externes (SRE Book, ITIL, ISO, RGPD) + liens internes (spec phase, audit)}
    ```

    5.3 Vérification technique des agents nexus-*

    Le mainteneur a noté dans la spec P10 v2 finale (action P10-3) : "Vérifier que `nexus-ciso`, `legal-advisor`, `nexus-pm`, `nexus-devops-lead` peuvent être convoqués ensemble." Les agents `nexus-*` sont des **subagent types** disponibles via la tool `Agent` (cf. liste des agents disponibles en début de conversation). Il n'y a PAS de fichiers `agents/` ou `skills/` locaux dans ce repo — les nexus-* sont des types d'agents externes fournis par l'environnement Claude Code.

    **Vérification à faire** : les types d'agents suivants doivent être disponibles (subagent_type valide pour le tool Agent) :
    - `nexus-ciso` (utilisé par P8, P9, P10)
    - `nexus-devops-lead` (utilisé par P8, P9, P10)
    - `nexus-sm` (utilisé par P8 uniquement)
    - `nexus-architect` (utilisé par P9)
    - `legal-advisor` ou équivalent (utilisé par P10 — vérifier la disponibilité)
    - `nexus-pm` (utilisé par P10 — vérifier la disponibilité)

    Si un type d'agent n'est pas disponible, le mentionner dans le fichier Council concerné et proposer un fallback (par exemple, "Legal" → escalade mainteneur ou utilisation d'un agent généraliste avec un brief spécifique).

    5.4 Livrables Mission 2

    - `docs/councils/README.md` (≤ 50 lignes) : vue d'ensemble des 3 Councils, table de référence rapide (déclencheur, membres, timing).
    - `docs/councils/P8-incident-council.md` (~80-120 lignes) : structure commune §5.2 + spécificités P8.
    - `docs/councils/P9-structurante-council.md` (~80-120 lignes) : structure commune + spécificités P9.
    - `docs/councils/P10-cloture-council.md` (~120-160 lignes) : structure commune + 3 sections différenciées par criticité (simple / RGPD / regulated).
    - Mise à jour de la stratégie `audit/00-context-engineering-strategy.md` section 9 (questions ouvertes) : ajouter "Tranchées par Mission 2 (2026-06-XX)" avec les décisions de formalisation.
    - CHANGELOG.md : entrée sous "v2.1.0" ou "v2.0.1" avec "Docs : 3 Councils formalisés (P8 incident, P9 structurante, P10 clôture)".
    - (optionnel) Mise à jour croisée des specs P8/P9/P10 : section "Responsible Agents" → remplacer "Council CISO+DevOps-Lead+SM" par un lien vers `docs/councils/P8-incident-council.md` (idem P9, P10).

    5.5 Critères de validation Mission 2

    - [ ] Chaque fichier Council est autonome (lisible sans avoir besoin de la spec v2 sous les yeux)
    - [ ] Chaque fichier référence la spec source (lien vers `specs/workflows/by-phase/phase-N-*.md`)
    - [ ] Membership vérifié contre les subagent_type disponibles (note explicite si fallback nécessaire)
    - [ ] Structure commune respectée (8 sections §5.2)
    - [ ] Spécificités par phase documentées (déclencheur, timing, output)
    - [ ] Pour P10 : 3 sections différenciées par criticité (simple / RGPD / regulated)
    - [ ] Références externes citées avec URL + date (SRE Book ch.Postmortem, ITIL v4 CAB, ISO/IEC 12207, RGPD)
    - [ ] Pas de jargon dans les titres, français simple, actionnable

    6. STRUCTURE GLOBALE (rappel des 2 missions)

    Les 2 missions sont **indépendantes techniquement** (Mission 1 = bash, Mission 2 = markdown) mais **liées thématiquement** (adaptatif par criticité/sévérité/conformité). Le mainteneur peut vouloir :
    - **Option A** : faire les 2 dans la même conversation (1 seul commit / 1 seule PR)
    - **Option B** : faire Mission 1 puis Mission 2 dans 2 conversations séparées (2 commits / 2 PR)
    - **Option C** : ne faire que l'une des 2 (donner le choix au mainteneur en début de conversation)

    **Recommandation** : Option A dans la même conversation, **2 commits séparés** (1 par mission) pour traçabilité. Si Mission 1 échoue, Mission 2 reste valide. Si Mission 2 doit être révisée, Mission 1 n'est pas impactée.

    7. CONTRAINTES STRICTES (rappel)

    - ❌ NE PAS modifier `~/.claude/settings.json` (settings utilisateur)
    - ❌ NE PAS utiliser WebSearch natif (cassé, erreur 400 systématique)
    - ❌ NE PAS tenter de SSH distant (pas d'accès)
    - ❌ NE PAS poser des questions évidentes (par exemple, "quel nom pour le Council ?" — utiliser les noms des specs)
    - ❌ NE PAS utiliser de jargon dans les questions au mainteneur
    - ❌ NE PAS modifier le scope des 2 missions sans validation explicite du mainteneur
    - ✅ Lire les fichiers existants avant de répondre (cf. § 11)
    - ✅ Citer les sources primaires avec URL + date (pour les référentiels externes SRE/ITIL/ISO/RGPD)
    - ✅ Être économe en tokens (Edit > Write pour minimiser le diff)
    - ✅ Répondre en français (le mainteneur communique en français)
    - ✅ Toujours proposer un verdict/action concrète à la fin
    - ✅ Utiliser `mcp__web-search-prime__webSearchPrime` pour recherche web (MCP Z.AI, PRINCIPAL)
    - ✅ Utiliser `WebFetch` pour récupérer une URL spécifique
    - ✅ Respecter le fail-open (token counter = observabilité, pas security gate)
    - ✅ Le settings.json du repo (chemin relatif) peut être modifié si justifié (mais éviter — les env vars sont plus propres)

    8. OUTILS DISPONIBLES

    - ✅ `mcp__web-search-prime__webSearchPrime` : recherche web (PRINCIPAL)
    - ✅ `WebFetch` : récupération URL spécifique
    - ✅ MCP zai tools (8) : analyse d'image/vidéo/OCR (peu probable utile ici)
    - ✅ Bash, Read, Edit, Write, Grep, Glob : outils natifs Claude Code

    9. PREMIER RÉFLEXE (ordre de lecture)

    1. **Lis** `pre-tool-use/token-counter.sh` (script à modifier, 105 lignes)
    2. **Lis** `specs/workflows/by-phase/phase-8-operations.md` (référence spec P8 v2 finale, sections 5.5 + 8.1 + action P8-1)
    3. **Lis** `specs/workflows/by-phase/phase-9-maintenance.md` (référence spec P9 v2 finale, sections 5.5 + 8.1 + action P9-1)
    4. **Lis** `specs/workflows/by-phase/phase-10-retirement.md` (référence spec P10 v2 finale, sections 5.5 + 8.1 + action P10-1 + action P10-3 sur Council)
    5. **Lis** `audit/00-context-engineering-strategy.md` section 5 (budgets par phase) + section 9 (questions ouvertes tranchées)
    6. **Vérifie** l'état git : `cd /home/doz/swebok-v4-harness-distilled && git log --oneline -5 && git status`
    7. **Vérifie** la disponibilité des subagent_type `nexus-ciso`, `nexus-devops-lead`, `nexus-sm`, `nexus-architect`, `legal-advisor` (ou équivalent), `nexus-pm` — soit via la liste en début de conversation, soit en testant un appel Agent factice
    8. **Identifie** les zones d'incertitude : par exemple, le mainteneur a-t-il une préférence sur l'option A/B/C du § 6 ? Le mainteneur veut-il les 2 missions en 1 commit ou 2 ?

    10. QUESTIONS COMPLÉMENTAIRES (si nécessaire, vagues)

    VAGUE 1 — 2-3 questions max, en français simple, options mutuellement exclusives, 2-4 options par question :

    Q1. **Stratégie de livraison** : faire les 2 missions en combien de commits ?
    - (a) 1 commit combiné "v2.1.0: token counter adaptatif + 3 Councils formalisés" (1 seul diff atomique)
    - (b) 2 commits séparés "v2.1.0-token-counter" puis "v2.1.0-councils" (recommandé : si Mission 1 casse, Mission 2 reste)
    - (c) Mission 1 seulement, Mission 2 reportée à plus tard
    - (d) Mission 2 seulement, Mission 1 reportée à plus tard

    Q2. **Mode de sélection du budget** pour le token counter : env var, flag stdin JSON, ou les deux ?
    - (a) env var uniquement (`SWEBOK_P8_MODE=critical`) — recommandé, fail-open, simple
    - (b) flag stdin JSON (nécessite coordination avec les matchers Claude Code)
    - (c) les deux (env var prioritaire, fallback stdin)

    Q3. **Vérification des agents nexus-*** : si un type d'agent (par exemple `legal-advisor`) n'est pas disponible en subagent_type, que faire ?
    - (a) Documenter le fallback dans le fichier Council (escalade mainteneur, agent généraliste avec brief spécifique)
    - (b) Demander au mainteneur de clarifier avant de continuer
    - (c) Supposer disponibilité et documenter comme TODO

    Q4 (optionnel, selon le scope choisi). **Tag version** : après les 2 missions, créer quel tag ?
    - (a) `v2.1.0` (incrément mineur, suit semver, reflète nouvelles features)
    - (b) `v2.0.1-audit-extensions` (patch, reflète actions de suivi audit)
    - (c) Pas de tag, juste commit sur master

    Si le mainteneur a déjà tranché ces questions dans son brief initial, ne pas reposer. Adapter au scope.

    11. FORMAT DE FIN

    À la fin de la conversation, dis :
    "Terminé. X fait, Y à faire ensuite. Prochaine action suggérée : Z."

    - X = ce que tu as effectivement fait (commits, fichiers créés/modifiés, tests passés)
    - Y = ce qui reste à faire (par exemple, action P10-2 acquisition livres, ou validation terrain)
    - Z = l'action concrète que le mainteneur peut lancer ensuite (par exemple, "git push" ou "démarrer mini-projet test P0→P10")

    Pas plus, pas moins. Le mainteneur décidera de la suite.

    12. OBJECTIF FINAL

    Livrer 2 modifications propres, testées, committées sur master :
    1. `pre-tool-use/token-counter.sh` supporte le mode adaptatif 3-niveaux (P8=monitoring/standard/critical, P9=hotfix/standard/structurant, P10=simple/rgpd/regulated) via env var, fail-open, défaut préservé.
    2. `docs/councils/` contient 3 fichiers (P8 incident, P9 structurante, P10 clôture) suivant la structure commune §5.2, avec membership vérifié et références externes.

    Les 2 missions sont **nice-to-have** mais **techniquement nécessaires** pour fermer la boucle des audits P8/P9/P10 (les specs v2 finale mentionnent ces mécaniques mais sans implémentation). Durée estimée : 15-30 min de travail (2 fichiers bash + 4 fichiers markdown, pas de logique complexe).

    13. INSTRUCTIONS SPÉCIFIQUES

    - Le settings.json du repo a été modifié dans le commit `c3a1b76` pour ajouter le hook `token-counter.sh` sur 4 matchers. **Ne PAS re-modifier settings.json** sauf si une vraie raison technique l'exige (ce qui ne devrait pas être le cas ici, l'env var suffit).
    - Les tests du projet sont bash-based (cf. mémoire v1.5.11). Pour Mission 1, si tu ajoutes des tests (`tests/pre-tool-use/test-token-counter-modes.sh`), utilise la même convention (bash + exit 0/1).
    - Pour Mission 2, pas de test runtime (les Councils sont des procédures, pas du code exécutable). Validation = revue manuelle du mainteneur.
    - **Ne pas créer de branche** sauf si le mainteneur le demande explicitement. Travailler directement sur master.
    - **Si Mission 1 nécessite de modifier `state_engine.py`** pour supporter le mode adaptatif (par exemple, stocker le mode dans le state DB), le mentionner au mainteneur avant de le faire. C'est hors scope initial.

    ---DÉMARRAGE : lis § 9 (premier réflexe), puis identifie les zones d'incertitude, puis pose 2-4 questions vague 1 si nécessaire, puis procède. Si le mainteneur a déjà tout tranché dans son brief initial, va directement à l'implémentation.

    Référence projet : /home/doz/swebok-v4-harness-distilled/
    Commit de référence : c3a1b76 (v2.0.0-audit-complete)
    Date : 2026-06-08
