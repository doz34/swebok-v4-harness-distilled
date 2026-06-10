# PLAN — SWEBOK v4 Anti-Drift Auto-Trigger Sprint

> **Date** : 2026-06-10
> **Source** : SPEC.md (Ready) + design doc §7 (Architecture) + ledger §6 (8 décisions)
> **Plan version** : 1.0
> **Hand-off** : → `/speckit.tasks` (atomic task list) → `/speckit.implement` (code)

## 1. Plan Overview

| Field | Value |
|---|---|
| **feature** | antidrift-auto-trigger |
| **version** | 1.0 |
| **estimated_duration** | 6.5h dev + 30 min live validation = ~7h total |
| **team_size** | 1 (maintainer solo + Claude Code) |
| **phases** | 7 (Phase 0 quick wins → Phase 6 ship) |
| **tasks** | 21 atomic tasks (T-001 → T-021) |
| **milestones** | 6 (M0 prep → M5 ship) |
| **dependencies_blocking** | None (all deps exist per SPEC §7) |

## 2. Execution Strategy

### 2.1 Sequencing principle
**Critical path** : T-001 (quick wins) → T-002 (state schema) → T-003/T-008/T-010/T-014 (4 feature cores, parallel possible) → T-019 (test suite) → T-020 (live validation) → T-021 (ship).

### 2.2 Parallel workstreams
- **WS-A** (state schema + G1) : T-002 → T-003 → T-004/T-006/T-007
- **WS-B** (G3 phase change) : T-008 → T-009 (dépend de T-005 settings.json)
- **WS-C** (G5 council scheduler) : T-010 → T-011/T-012 → T-013
- **WS-D** (G6 mini-council) : T-014 → T-015 → T-016
- **WS-E** (kill-switch + doc) : T-017 → T-018

WS-A, WS-B, WS-C, WS-D peuvent être exécutés en parallèle si l'équipe grandit. Solo : séquentiel.

### 2.3 Risk-driven checkpoints
- Après T-005 (settings.json update) : vérifier que les 20 self-tests existants passent toujours (régression check)
- Après T-011 (auto-verify counter) : vérifier que le lint existant fonctionne toujours
- Après T-019 (test suite full) : obligatoire avant T-020

## 3. Phases

### Phase 0 — Quick Wins (15 min, M0)
**Goal** : fermer G8 + G2 + G4 (audit gaps) avant le sprint principal, démontrer le câblage.

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-001 | Quick wins bundle : `git push origin master` (3 commits S1+S2+S3) + commit 12 audits MODIFIED + `ln -s ../../pre-commit-hook.sh .git/hooks/pre-commit` + `chmod +x` + seed steering DB via `bin/adv-loop 0` | 15 min | none | `git status` clean, `.git/hooks/pre-commit` symlink existe, `.swebok_steering_state.db` size > 0 |

### Phase 1 — State Schema Foundation (15 min, M1)
**Goal** : state DB prêt pour les nouvelles clés (intent.*, edits_since_council, council.last_at, phase_history).

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-002 | Étendre `lib/state_engine.py` pour supporter les nouvelles clés (set/get/incr/list_append) ; migration additive non-destructive ; tests unitaires 5 | 15 min | T-001 | `python3 -c "from lib.state_engine import *; print(state.get('intent.phase', 'P0'))"` retourne 'P0' (default) |

### Phase 2 — G1 Intent Detection (2h15, M2)
**Goal** : US-1 fonctionnel. UserPromptSubmit hook → auto-detect intent → state write.

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-003 | Créer `lib/auto_trigger.py` : 4 layers (cache 50ms / pattern 100ms / semantic 500ms / fallback) + subprocess call à `intent-detector.py` (B7 merge) + D1 confidence threshold 0.5 | 1h | T-002 | `bin/adv-loop auto-trigger "Write tests"` retourne phase=6 confidence>0.8 |
| T-004 | Créer `pre-tool-use/auto-trigger-hook.sh` (~40 LOC) : lit stdin JSON, appelle `python3 lib/auto_trigger.py`, écrit state DB ; fail-open trap | 15 min | T-003 | bash dry-run : `echo '{}' \| bash pre-tool-use/auto-trigger-hook.sh` exit 0 silencieux |
| T-005 | Modifier `settings.json` + `settings.template.json` : +1 matcher `UserPromptSubmit` → `auto-trigger-hook.sh` ; merge idempotent | 10 min | T-004 | `jq '.hooks.UserPromptSubmit' settings.json` retourne le matcher |
| T-006 | Ajouter `bin/adv-loop auto-trigger <prompt>` subcommand + `bin/adv-loop help` update | 15 min | T-003 | `bin/adv-loop help` liste "auto-trigger" |
| T-007 | Écrire `tests/test_auto_trigger.py` : 10 tests T1-T10 (acceptance criteria G1) | 30 min | T-003 | `pytest tests/test_auto_trigger.py -v` → 10 PASS |

### Phase 3 — G3 Phase Change Detection (1h15, M3)
**Goal** : US-2 fonctionnel. Phase change → adversarial-gate --council auto-fire.

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-008 | Étendre `pre-tool-use/phase-guard.sh` : +30 LOC pour lire `intent.phase` vs `current_phase`, emit `<MULTIAGENT_LAUNCH>` envelope sur diff, append `phase_history[]` (FIFO 10), fail-secure | 45 min | T-005 | mock state DB avec intent.phase=5 current_phase=2, run Write, log contient `<MULTIAGENT_LAUNCH>` |
| T-009 | Écrire tests G3 (T11-T15) : 5 tests intégrés dans `tests/test_phase_guard.sh` ou pytest wrapper | 30 min | T-008 | `pytest tests/test_phase_guard.py -v` → 5 PASS |

### Phase 4 — G5 Council Scheduler (1h30, M4)
**Goal** : US-3 fonctionnel. Counter + cooldown → fire full Council tous les 5 edits.

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-010 | Créer `lib/adv-loop/council_scheduler.py` : state counter `edits_since_council`, threshold default 5 (env var overridable), cooldown 1h, whitelist `*.md`/`*.json`/`tests/*`, fire envelope if conditions met | 45 min | T-002 | `python3 -c "from lib.adv_loop.council_scheduler import *; print(should_fire(5, 1234567890, 3600))"` retourne True |
| T-011 | Étendre `post-tool-use/auto-verify.sh` : +40 LOC pour counter increment, whitelist check, council scheduler call, fail-open | 30 min | T-010 | 5 edits sur src/foo.py → 5ème déclenche envelope |
| T-012 | Ajouter `bin/adv-loop council-status` subcommand : human-readable output (counter, last_at, threshold) | 15 min | T-010 | `bin/adv-loop council-status` affiche 3 lignes lisibles |
| T-013 | Écrire `tests/test_council_scheduler.py` : 5 tests T16-T20 | 15 min | T-011 | `pytest tests/test_council_scheduler.py -v` → 5 PASS |

### Phase 5 — G6 Mini-Council (1h05, M5)
**Goal** : US-4 fonctionnel. Mini-council 1 Haiku judge par edit non-whitelist.

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-014 | Créer `lib/adv-loop/mini_council.py` : 1 Haiku judge cheap, prompt template per phase, DSL output `mini_council:finding=OK\|VULN:<sev>;;...`, fail-open si Haiku indispo, escalate logic (1 finding/3 edits) | 30 min | T-002 | `python3 lib/adv-loop/mini_council.py src/foo.py` retourne DSL line < 2s |
| T-015 | Étendre `post-tool-use/auto-verify.sh` : +30 LOC pour mini-council call après lint, whitelist check, escalate trigger | 20 min | T-014 | 3 edits avec 1+ finding → 3ème déclenche full Council |
| T-016 | Écrire `tests/test_mini_council.py` : 5 tests T21-T25 (perf, fail-open, escalation, regression, DSL format) | 15 min | T-015 | `pytest tests/test_mini_council.py -v` → 5 PASS |

### Phase 6 — Kill-Switch + Doc (25 min, M5.5)
**Goal** : US-5 + NFR-M5 (env vars documentés).

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-017 | Ajouter check `HARNESS_AUTO_TRIGGER=0` en début de `pre-tool-use/auto-trigger-hook.sh`, `pre-tool-use/phase-guard.sh`, `post-tool-use/auto-verify.sh` (3 hooks) ; exit 0 immédiat si désactivé | 15 min | T-004, T-008, T-011, T-015 | `HARNESS_AUTO_TRIGGER=0 bash pre-tool-use/auto-trigger-hook.sh` exit 0 sans log |
| T-018 | Mettre à jour `CLAUDE.md` : +1 ligne dans Laws "8. **KILL-SWITCH** — `HARNESS_AUTO_TRIGGER=0` désactive FR-1/FR-3/FR-5/FR-7 globalement" ; +1 ligne dans env vars | 10 min | T-017 | `rg "KILL-SWITCH\|HARNESS_AUTO_TRIGGER" CLAUDE.md` retourne 2 hits |

### Phase 7 — Integration & Validation (45 min, M6)
**Goal** : tous les tests passent + validation live + commit.

| Task | Description | Effort | Deps | Verification |
|---|---|---|---|---|
| T-019 | Run full test suite : `bin/adv-loop test` + `pytest tests/test_*.py` ; fix régressions si nécessaire | 10 min | T-007, T-009, T-013, T-016, T-017 | 45/45 PASS (20 existing + 25 new) + 5 cross-cutting |
| T-020 | Live validation : 1 vraie session Claude Code, 5 prompts variés (refactor/test/discover/deploy/hello), 10 edits sur fichiers src/, vérifie intent.phase correct, Council fire au 5ème edit, mini-council sur chaque edit | 30 min | T-019 | SM-2, SM-4, SM-6, SM-7 |
| T-021 | Update `CHANGELOG.md` (entrée v1.6.0 = "Anti-drift auto-trigger sprint") + `git add -A && git commit -m "feat(antidrift): G1+G3+G5+G6+G8 auto-trigger sprint (closes G1+G3+G5+G6+G8)"` + push | 15 min | T-020 | `git log --oneline -3` montre le commit, CHANGELOG.md updated |

## 4. Milestones

| ID | Name | Criteria (Definition of Done) | Target Time |
|---|---|---|---|
| **M0** | Quick wins done | 3 commits pushed, pre-commit symlink installed, steering DB seeded | T+0:15 |
| **M1** | State schema ready | New keys gettable/settable, 5 unit tests pass | T+0:30 |
| **M2** | G1 functional | 10 acceptance tests pass, live UserPromptSubmit hook works | T+2:45 |
| **M3** | G3 functional | 5 tests pass, phase change fires Council | T+4:00 |
| **M4** | G5 functional | 5 tests pass, Council fires every 5 edits | T+5:30 |
| **M5** | G6 functional + kill-switch | 5 tests pass, mini-council per edit, kill-switch verified | T+6:35 |
| **M5.5** | Doc updated | CLAUDE.md mentions kill-switch, env vars documented | T+7:00 |
| **M6** | Sprint shipped | 45+5 tests pass, live validation green, CHANGELOG updated, commit pushed | T+7:30 |

## 5. Risk Mitigation (per task)

| Task | Risk | Mitigation |
|---|---|---|
| T-003 (auto_trigger) | intent-detector.py 22K LOC dependency might fail | Subprocess isolation, fail-open on non-zero exit |
| T-005 (settings.json) | Merge might break user custom config | `install-harness.sh` idempotent, backup before modif (mais ce sprint n'auto-install pas — user manuel) |
| T-008 (phase-guard ext) | Backward compat with 20 existing tests | Wrap new code in `if [[ -n "$intent_phase" ]]` ; existing tests run unchanged |
| T-011 (auto-verify ext) | Counter might run on every edit (noise) | Whitelist tests/config early ; counter only non-whitelist |
| T-014 (mini_council) | Haiku 4.5 indispo | Fail-open exit 0, no finding logged |
| T-017 (kill-switch) | 4 files to modify, easy to miss | T-018 doc update as checklist verification |
| T-019 (test suite) | Existing 20 tests might break | Run `bin/adv-loop test` BEFORE any modification as baseline ; if any fail post-modif, fix before continue |
| T-020 (live validation) | Real session is non-deterministic | Run 5+ varied prompts to average out noise ; manual verification of intent.phase correct |

## 6. Quality Gates (between phases)

- **After Phase 1** (T-002) : existing 20 self-tests pass (regression check)
- **After Phase 2** (T-007) : T1-T10 PASS, 20 existing still pass
- **After Phase 3** (T-009) : T11-T15 PASS, 30 total
- **After Phase 4** (T-013) : T16-T20 PASS, 35 total
- **After Phase 5** (T-016) : T21-T25 PASS, 40 total
- **After Phase 6** (T-018) : T26-T30 PASS, 45 total
- **After Phase 7** (T-021) : 50/50 PASS + live validation green + CHANGELOG + commit

## 7. SWEBOK v4 Alignment

| KA | Coverage |
|---|---|
| KA-2 Architecture | T-002 state schema, T-008 phase diff detect, T-011 counter |
| KA-4 Construction | T-003, T-010, T-014 (3 new Python modules following lib/adv-loop/ pattern) |
| KA-5 Testing | T-007, T-009, T-013, T-016 (4 test files, 25 tests) |
| KA-6 Management | Phase/milestone breakdown, risk mitigation per task |
| KA-8 Quality | NFR checks per phase, regression gates |

**Status : Ready for /speckit.tasks.**
