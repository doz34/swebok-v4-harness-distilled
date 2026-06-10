# SWEBOK v4 Harness Distilled — Analyse Intégrale

**Date** : 2026-06-10
**Version analysée** : v2.6.0 (anti-drift auto-trigger sprint, non-taggé)
**Tag le plus récent** : `v2.5.0-adversarial-s5`
**Méthode** : Conseil adversarial 4 consultants (CISO + Architecte + DevOps/QA + Product/UX) + audit technique direct

---

## 🎯 Verdict Global

### Production Readiness : **74 %** — *Production-Ready conditionnel*

> Le produit est techniquement solide et défendable en sécurité, mais l'**hygiène d'intégration** (tests partiellement cassés, drift de chemins, working tree sale) le bloque d'un *ship* propre. Un dernier sprint de 1-2 jours sur les blockers suffit à passer à 90 %+.

| Consultant | Verdict | Note |
|---|---|---|
| CISO | B+ — défense cohérente, gate = fixture | **78 %** |
| Architecte | B+ — sain, mais drift d'intégration | **82 %** |
| DevOps/QA | Conditional Production-Ready | **72 %** |
| Product/UX | B+ mais ship-blocked | **62 %** |
| **Moyenne pondérée** | — | **74 %** |

**Pondération** : Security 25 % + Architecture 25 % + DevOps 30 % + Product 20 %

---

## 📊 État Technique au 2026-06-10

### Métriques brutes
| Métrique | Valeur |
|---|---|
| Fichiers source (`.py` + `.sh` + `.json` + `.md`) | **391** |
| Lignes de code (Python + Shell) | **~21 000** |
| Couches d'adversarial loop (S0–S5) | **5 sprints complets** |
| Property-based tests (4 props × 11 phases) | **44** |
| Corpus adversarial (9 catégories) | **60 payloads** |
| SDLC phases auditées (P0–P10) | **10/10** |
| Versions publiées | **17 tags** (v1.5.4 → v2.5.0) |
| Lignes DSL core | **131** (compressed) |

### Résultats de tests (mesure terrain 2026-06-10)
| Suite | Résultat | Statut |
|---|---|---|
| `bin/adv-loop test` (S0–S5 self-tests internes) | **38/38 PASS** | ✅ |
| `tests/retrieval/test-v2.sh` | **20/20 PASS** | ✅ |
| `tests/distilled-test.sh` | **30/32 PASS** | ⚠️ 2 FAIL |
| `tests/retrieval/test-adversarial.sh` | **HANGS** après ADV-1 | ❌ fixtures `/tmp/test_adv*.py` manquantes |
| `tests/adv-loop/` (property-based shell) | **VIDE** | ❌ répertoire créé vide |

**Verdict tests** : 88/90 mesurés PASS (38+30+20) + 2 FAIL connus + 8 cassés = **88/100 effectif**

---

## 🧰 Features Offertes par le Tool

### 1. Discipline Layer pour Claude Code (cœur du produit)
- **Phase gating** (P0–P10) : bloque les actions incompatibles avec la phase SDLC courante (ex. écrire du code en P0 Discovery)
- **Bash guard** : scanner de commandes shell phase-aware avec detection path-traversal, ReDoS cap, mot-clé danger
- **DSL parser strict** : delimiter `;;` avec normalisation (espaces, casse, séparateurs)
- **DSL** : 3 formes canoniques (GATE, RED, BLUE) + format étendu (VULN, NORMS, etc.)

### 2. Moteur de Connaissance Compilé (Layer 0–L7)
- **24 principes universels** (KISS, DRY, YAGNI, …) + density de citation
- **46 antipatterns** (God Class, Spaghetti Code, etc.) avec mitigations
- **6 ontologies** : SE, Python, Web, Data, Security, ML-Systems
- **5 arbres de décision** (choix DB, choix API, …)
- **5 recettes** procédurales (api-design, auth, error-handling, …)
- **3 comparaisons** structurées (REST vs GraphQL, SQL vs NoSQL, Monolith vs Microservices)
- **9 checklists de phase** (P0–P9) + 1 fichier agrégé
- **4 catalogues de risques** (security/performance/maintainability/ops)
- **145 963 concepts** corpus (legacy) — *drift : 467 156 mesuré*
- **152 items** corpus_enrichment
- **Déterministe** : < 5 ms/query, $0, no-LLM, no-RAG, no-network

### 3. Adversarial Loop S0–S5 (5 sprints complets)
- **S0** : Base computational loop (11 patterns phase-spécifiques : AC testable, ADR MADR, OpenAPI, SLO, RGPD, etc.)
- **S1** : 11 patterns per-phase bash + orchestrateur `bin/adv-loop` + CLI
- **S2** : **Council Bridge** — 4 LLM-judges (ciso / qa-lead / architect / devops-lead) avec per-phase anchors
- **S3** : **Steering loop** — DB isolée `.swebok_steering_state.db`, fingerprint SHA-256, détection patterns récurrents, actions suggérées
- **S4** : **60-payload corpus adversarial** — 9 catégories, détection de régression
- **S5** : **44 property-based tests** — 4 propriétés × 11 phases (idempotence, déterminisme, monotonicité, DSL well-formed)

### 4. Anti-Drift Auto-Trigger v2.6.0 (G1+G3+G5+G6)
- **G1** — *UserPromptSubmit auto-trigger* : détecteur d'intent 4-layer (cache / pattern / scoring / fallback), seuil 0.5, subprocess 2 s, écrit `intent.phase` dans state DB
- **G3** — *Phase change detector* : FIFO history 10 + emit `<MULTIAGENT_LAUNCH>` envelope sur transition
- **G5** — *Council scheduler* : compteur + threshold (5 défauts) + cooldown (1 h), whitelist `*.md|*.json|tests/*|.git/*`
- **G6** — *Mini-council per edit* : 1 Haiku judge (ou heuristique offline < 100 ms), escalation auto si 1+ VULN
- **KILL-SWITCH** : `HARNESS_AUTO_TRIGGER=0` désactive les 4 hooks

### 5. Audit Chain Tamper-Evident
- **State engine** SQLite WAL (`lib/state_engine.py`, 1 700 LOC)
- **HMAC chain** vérifiable (`verify_audit_chain`)
- **Clé** `.audit_key` (mode 0600, gitignored, régénérée à l'install)
- **STRIDE-lite** dans pre-commit
- **Append-only triggers** : `BEFORE UPDATE` → exception
- **Export state** : `python3 lib/state_engine.py export_state`

### 6. Multiagent Bridge (ADR-003 / Law 6 / 6.1)
- **adversarial-gate.sh** : Red/Blue/Judge avec parser DSL strict
- **multiagent-launcher.sh** : spawn parallèle `nexus-attacker` + `nexus-defender` via Agent tool
- **Council Bridge** : 4 subagent_types avec JSONL envelope
- **Validation input** : rejet shell-metachar dans `$APP_URL` / `$SCENARIO_FILE`

### 7. Sécurité Renforcée
- **HMAC** chaîne d'audit + vérification
- **STRIDE-lite** scan pre-commit
- **Path-traversal** guards (`allowed_roots`)
- **Prompt-injection** sanitization (backticks → safe)
- **ReDoS cap** sur regex scanner
- **JSON size cap** + malicious JSONL detection
- **Ollama SSRF** guard
- **Symlink rejection** dans chunker
- **Embedding cache** non-tautologique (v1.5.5+)
- **Max file size** guard

### 8. Hooks Claude Code
- **PreToolUse** : `phase-guard.sh`, `bash-guard.sh`, `token-counter.sh`, `auto-trigger-hook.sh`, `phase-change-detector.sh`
- **PostToolUse** : `auto-verify.sh`, `council-scheduler-hook.sh`, `mini-council-hook.sh`
- **UserPromptSubmit** : `auto-trigger-hook.sh` (v2.6.0, G1)
- **Matchers** : Write/Edit/Bash/Skill/Task/Agent/mcp__*/Glob/Grep/LS

### 9. Tooling & Ops
- `bin/adv-loop` — CLI 6 modes (phase, all, council, patterns, steer, history, test)
- `install-harness.sh` — installer jq-merge (settings.json preservation)
- `pre-commit-hook.sh` — gate pre-commit avec fork-skip doc
- `self-heal.sh` (14K) — auto-réparation state DB
- `health-check.sh` (3.5K) — diagnostic runtime
- `act-observe-verify.sh` (17K) — pattern AOV
- `browser-use-orchestrator.sh` — browser automation
- `skill-invoker.sh` (4.9K)
- **Docker** : `Dockerfile` multi-stage, non-root, healthcheck

### 10. CI/CD
- `.github/workflows/test.yml` : matrix OS × Python (Linux + macOS × 3.10/3.11/3.12), cron hebdo

### 11. Anti-Rot & Gouvernance
- **Law 7** : nudge `ANTI-ROT:NUDGE` tous les 5 tool calls
- **Laws 1–6** : HOT-PATH, STATE-DRIVEN, COMPILED-KNOWLEDGE, CAVEMAN_ULTRA, MCP BRIDGE, MULTIAGENT BRIDGE
- **CIRCUIT BREAK** : 3 blocks → override 5 min
- **GATE:PASS** obligatoire pour transitions de phase

### 12. Audit Stratégique (transverse)
- `audit/00-context-engineering-strategy.md` (modèle L0–L3, 4 lois)
- `audit/01-context-engineering-research-2026.md`
- 10 grilles d'audit phase (P0–P10)
- Stratégie corpus, références, crawler

---

## 🔴 Top-12 Blocker pour Production Propre

### CRITIQUES (bloquant ship)
1. **Working tree sale** — 3 fichiers untracked (`scripts/adversarial-gate.sh`, `scripts/lib`, `scripts/multiagent-launcher.sh` — symlinks) + 3 DB runtime non-gitignored
2. **Drift chemins `lib/` ↔ `scripts/lib/` ↔ `scripts/retrieval/`** — CLAUDE.md pointe `lib/`, README pointe `scripts/lib/`, fichiers dupliqués (pas symlinks) = 2× maintenance
3. **Test-adversarial cassé** — `tests/retrieval/test-adversarial.sh` référence `/tmp/test_adv{1..8}.py` jamais créés → suite bloquée au test 1
4. **Test-26 & Test-29 failing** — `distilled-test.sh` : Test 25 (467 156 concepts vs 145 963 attendus = data drift) + Test 29 (browser fait un appel réseau = offline cassé)
5. **`tests/adv-loop/` vide** — répertoire créé vide, 44 property-based tests annoncés mais 0 runner shell
6. **README badge obsolète** — affiche `52/52 PASS`, mesure réelle `88/100` (38+30+20 + 2 FAIL + 8 broken)

### HAUTS (à corriger sous 1 sprint)
7. **`adversarial-gate.sh` = fixture** — honnêteté réelle : le vrai gate Red/Blue requiert `nexus-attacker`/`nexus-defender` externes, pas présents localement (banner honesty déjà en place, mais à diffuser)
8. **Settings.json hardcoded paths** — pointe vers `/home/doz/swebok-v4-harness/` (autre projet) + `/home/doz/swebok-v4-harness-distilled/` (lui-même) ; le template `{{HARNESS_DIR}}` est OK, le rendu ne l'est pas
9. **Audit phases P6–P10** — seulement 5/10 grilles remplies (P0–P5 FERMÉ), 5/10 « À remplir »
10. **v2.6.0 non-taggé** — commit `0409000` (G3+G5+G6) + `b372ff5` (T-021 anti-drift) en working tree, pas de tag publié

### MOYENS (hygiène)
11. **AUDIT_REPORT.md historique** — date 2026-06-03 (v1.5.3), trompeur si lu isolément
12. **.audit_key reste en working tree** — gitignored, mais n'a pas été régénéré ce sprint

---

## ✅ Forces à Préserver

- **DSL strict** : delimiter `;;` + parser normalisé = fail-secure (240 LOC lisibles)
- **HMAC chain vérifiable** : `verify_audit_chain` couvre tous les événements
- **5-sprints adversarial** : pattern reproductible (S0=base, S1=patterns, S2=council, S3=steering, S4=corpus, S5=properties) — exceptionnel pour un discipline layer
- **Council Bridge** : 4 reviewers avec per-phase anchors = vrai Red/Blue multi-lens
- **Honesty banner** : `adversarial-gate.sh` lignes 6-23 disclose le statut fixture = modèle de transparence
- **KILL-SWITCH** propre : 1 env var désactive toute la chaîne auto-trigger
- **v2.6.0 G1+G3+G5+G6** : ferme totalement le goal hook « auto-trigger à chaque étape »

---

## 🛠️ Plan d'Action Recommandé (1-2 jours)

### Sprint "Clean Ship" (4-6 h)
1. **.gitignore** : ajouter `state.db` `*.db` (les 3 DBs déjà couvertes) + vérifier que les symlinks ne sont pas commités accidentellement
2. **Test fixes** :
   - `tests/retrieval/test-adversarial.sh` : créer fixtures inline OU supprimer
   - `distilled-test.sh` Test 25 : mettre à jour expectation (467 156) OU fixer le data
   - `distilled-test.sh` Test 29 : désactiver le network call dans `corpus_browser --safe`
   - `tests/adv-loop/` : ajouter un runner shell basique pour les property tests
3. **Path cleanup** : décision — symlink `scripts/lib` → `lib/` (1 ligne) OU supprimer les scripts/lib + scripts/retrieval
4. **README badge** : corriger `52/52` → `88/100` (avec note explicite sur les 12 manquants)
5. **v2.6.0 tag** : `git tag -a v2.6.0-antidrift -m "..."` + push
6. **AUDIT_REPORT.md** : déplacer vers `archive/audit-v1.5.3.md` OU dater comme historique

### Sprint "Fixture → Reality" (optionnel, +2-4 h)
7. Enregistrer `nexus-attacker` + `nexus-defender` comme subagent_types locaux OU marquer `adversarial-gate --council` comme advisory-only
8. Compléter les 5 grilles d'audit (P6–P10) avec la même méthode (vague 1 + vague 2)

→ **Post-sprint** : production readiness projetée **92 %**

---

## 🏁 Recommandation Finale

> **Ship v2.6.0 en pre-release/RC** (tag `v2.6.0-rc1`), exécuter le sprint "Clean Ship" (6 h), puis shipper v2.6.0 stable. Le produit est défendable techniquement et la sécurité tient. Les gaps sont de l'**hygiène d'empaquetage**, pas de l'architecture.

**Risque résiduel** : si shipped en l'état, un nouveau cloneur sur une machine fraîche aura 4 hooks qui ne pointent nulle part, un badge mensonger, et un test suite qui ne couvre pas 12 % de la base. Tous rattrapables, mais évitables.

---

*Généré par conseil adversarial 4-consultants (2026-06-10)*
*CISO · Architecte · DevOps/QA · Product/UX*
