# TASKS — SWEBOK v4 Anti-Drift Auto-Trigger Sprint

> **Date** : 2026-06-10
> **Source** : PLAN.md (21 tasks), tasks.yaml (DAG), milestones.yaml (M0-M6)
> **Note** : `speckit-tasks` skill non installé localement. Production manuelle de la liste atomique selon philosophie spec-kit (≤1h, exécutable, owner unique).
> **Hand-off** : → `/speckit.implement` (skill installé, va fermer le goal hook)

## 1. Tasks Atomic List (21 tasks, ordered by execution)

### Phase 0 — Quick Wins (15 min)

#### T-001 · Bundle quick wins
- **type** : ops
- **effort** : 15 min
- **deps** : []
- **owner** : maintainer
- **deliverable** : 3 commits pushed, 12 audits committed, pre-commit symlink, steering DB seeded
- **commands** :
  ```bash
  cd /home/doz/swebok-v4-harness-distilled
  git add audit/*.md
  git commit -m "chore(audit): commit 12 phase audit updates 2026-06-10"
  git push origin master
  ln -s ../../pre-commit-hook.sh .git/hooks/pre-commit
  chmod +x .git/hooks/pre-commit
  bash bin/adv-loop 0  # seed steering DB
  ```
- **DoD** : `git status` clean, `.git/hooks/pre-commit` exists, `.swebok_steering_state.db` size > 0
- **audit_gap_closed** : G8, G2, G4
- **risk** : push could fail if remote diverged → `git pull --rebase` first

### Phase 1 — State Schema (15 min)

#### T-002 · Extend state_engine.py
- **type** : code
- **effort** : 15 min
- **deps** : [T-001]
- **owner** : maintainer
- **deliverable** : `lib/state_engine.py` supports `intent.*`, `edits_since_council`, `council.last_at`, `phase_history[]`
- **approach** :
  - Read existing state_engine.py to confirm `set`/`get`/`incr` operations
  - Add tests for new keys (default values, set/get round-trip, list_append FIFO)
  - No migration needed (SQLite additive)
- **DoD** : `python3 -c "from lib.state_engine import *; print(set('intent.phase', 'P5'))"` returns True, `get('intent.phase', 'P0')` returns 'P5'

### Phase 2 — G1 Intent Detection (2h15)

#### T-003 · Create lib/auto_trigger.py
- **type** : code
- **effort** : 1h
- **deps** : [T-002]
- **deliverable** : `lib/auto_trigger.py` (~300 LOC) with 4 layers
- **approach** :
  - Layer 1: cache (in-memory dict, TTL 1h)
  - Layer 2: pattern (load intent-map.json, regex match)
  - Layer 3: semantic (TF-IDF cosine, fail-open if > 500ms)
  - Layer 4: fallback (no-op, log)
  - Subprocess call to `intent-detector.py` for layer 2/3 reuse (B7 merge)
  - Output: DSL `auto_trigger:phase=N;confidence=0.X;intent=foo;fallback=bar`
- **DoD** : `python3 lib/auto_trigger.py "Write tests"` returns phase=6 confidence>0.8 in <100ms

#### T-004 · Create pre-tool-use/auto-trigger-hook.sh
- **type** : code
- **effort** : 15 min
- **deps** : [T-003]
- **deliverable** : `pre-tool-use/auto-trigger-hook.sh` (~40 LOC)
- **approach** :
  - Bash wrapper, read stdin JSON (Claude Code contract)
  - Extract prompt from `tool_input.prompt` or `user_prompt`
  - Call `python3 lib/auto_trigger.py "$prompt"`
  - Parse DSL output, write `intent.phase` to state DB if confidence ≥ 0.5
  - `trap 'exit 0' ERR` for fail-open
- **DoD** : hook runs without error on valid JSON input, silent exit 0 on invalid

#### T-005 · Update settings.json + template
- **type** : config
- **effort** : 10 min
- **deps** : [T-004]
- **deliverable** : `settings.json` + `settings.template.json` with UserPromptSubmit matcher
- **approach** :
  - Add `UserPromptSubmit` key under `hooks` (new event, alongside PreToolUse/PostToolUse)
  - Matcher: `hooks: ["bash ${HARNESS_DIR}/pre-tool-use/auto-trigger-hook.sh"]`
  - For template: use `{{HARNESS_DIR}}` placeholder
- **DoD** : `jq '.hooks.UserPromptSubmit' settings.json` returns the matcher array

#### T-006 · Add bin/adv-loop auto-trigger subcommand
- **type** : code
- **effort** : 15 min
- **deps** : [T-003]
- **deliverable** : `bin/adv-loop` extended with `auto-trigger <prompt>` subcommand
- **approach** : add new case in main dispatch
- **DoD** : `bin/adv-loop auto-trigger "Refactor auth"` returns phase=5

#### T-007 · Write tests/test_auto_trigger.py
- **type** : test
- **effort** : 30 min
- **deps** : [T-003]
- **deliverable** : `tests/test_auto_trigger.py` (~200 LOC) with 10 tests T1-T10
- **DoD** : `pytest tests/test_auto_trigger.py -v` → 10 PASS

### Phase 3 — G3 Phase Change (1h15)

#### T-008 · Extend pre-tool-use/phase-guard.sh
- **type** : code
- **effort** : 45 min
- **deps** : [T-005]
- **deliverable** : `pre-tool-use/phase-guard.sh` +30 LOC
- **approach** :
  - After existing block logic, read `intent.phase` from state DB
  - Compare with `current_phase`
  - If diff: append to `phase_history[]` (FIFO 10), emit `<MULTIAGENT_LAUNCH>` envelope to stderr (dispatcher reads)
  - `current_phase` becomes `intent.phase`
  - Fail-secure on state DB error
- **DoD** : state DB mock with diff → log shows `<MULTIAGENT_LAUNCH>` envelope

#### T-009 · Write tests for G3 (T11-T15)
- **type** : test
- **effort** : 30 min
- **deps** : [T-008]
- **deliverable** : `tests/test_phase_guard.py` with 5 tests
- **DoD** : `pytest tests/test_phase_guard.py -v` → 5 PASS

### Phase 4 — G5 Council Scheduler (1h30)

#### T-010 · Create lib/adv-loop/council_scheduler.py
- **type** : code
- **effort** : 45 min
- **deps** : [T-002]
- **deliverable** : `lib/adv-loop/council_scheduler.py` (~150 LOC)
- **approach** :
  - `should_fire(edits_count, last_at, threshold=5, cooldown=3600)` function
  - Whitelist check helper
  - Emit `<MULTIAGENT_LAUNCH>` envelope if should_fire
  - Reset counter on fire
- **DoD** : `should_fire(5, 1234567890, 3600)` returns True when `now > last_at + cooldown`

#### T-011 · Extend post-tool-use/auto-verify.sh
- **type** : code
- **effort** : 30 min
- **deps** : [T-010]
- **deliverable** : `post-tool-use/auto-verify.sh` +40 LOC
- **approach** :
  - After lint, check file path against whitelist
  - If not whitelisted, `incr edits_since_council`
  - Call council_scheduler, emit envelope if should_fire
- **DoD** : 5 edits on src/foo.py → 5th triggers envelope

#### T-012 · Add bin/adv-loop council-status
- **type** : code
- **effort** : 15 min
- **deps** : [T-010]
- **deliverable** : `bin/adv-loop` extended with `council-status` subcommand
- **DoD** : `bin/adv-loop council-status` shows counter, last_at, threshold

#### T-013 · Write tests/test_council_scheduler.py
- **type** : test
- **effort** : 15 min
- **deps** : [T-011]
- **deliverable** : `tests/test_council_scheduler.py` with 5 tests T16-T20
- **DoD** : `pytest tests/test_council_scheduler.py -v` → 5 PASS

### Phase 5 — G6 Mini-Council (1h05)

#### T-014 · Create lib/adv-loop/mini_council.py
- **type** : code
- **effort** : 30 min
- **deps** : [T-002]
- **deliverable** : `lib/adv-loop/mini_council.py` (~120 LOC)
- **approach** :
  - 1 Haiku 4.5 judge call (cheap, fast)
  - Per-phase prompt template (anchors from council.py)
  - DSL output: `mini_council:finding=OK|VULN:<sev>;;LOC:<path>;;...`
  - Fail-open on Haiku indispo (exit 0, no finding)
  - Escalation logic: track last 3 findings, if 1+ VULN → fire envelope
- **DoD** : `python3 lib/adv-loop/mini_council.py src/foo.py` returns DSL < 2s

#### T-015 · Extend post-tool-use/auto-verify.sh for mini-council
- **type** : code
- **effort** : 20 min
- **deps** : [T-014]
- **deliverable** : `post-tool-use/auto-verify.sh` +30 LOC (cumulative +70 with T-011)
- **approach** :
  - After council scheduler call, call mini_council
  - Track findings in state DB (sliding window 3)
  - If escalation triggered, emit envelope
- **DoD** : 3 edits with 1+ finding → 3rd triggers full Council

#### T-016 · Write tests/test_mini_council.py
- **type** : test
- **effort** : 15 min
- **deps** : [T-015]
- **deliverable** : `tests/test_mini_council.py` with 5 tests T21-T25
- **DoD** : `pytest tests/test_mini_council.py -v` → 5 PASS

### Phase 6 — Kill-Switch + Doc (25 min)

#### T-017 · Add HARNESS_AUTO_TRIGGER=0 check in 3 hooks
- **type** : code
- **effort** : 15 min
- **deps** : [T-004, T-008, T-011, T-015]
- **deliverable** : 3 hooks check env var, exit 0 if disabled
- **approach** :
  - In each hook script, add at top:
    ```bash
    if [[ "${HARNESS_AUTO_TRIGGER:-1}" == "0" ]]; then
      exit 0
    fi
    ```
- **DoD** : `HARNESS_AUTO_TRIGGER=0 bash pre-tool-use/auto-trigger-hook.sh` exit 0 silent

#### T-018 · Update CLAUDE.md
- **type** : doc
- **effort** : 10 min
- **deps** : [T-017]
- **deliverable** : `CLAUDE.md` updated with KILL-SWITCH law
- **approach** : add Law 8 "KILL-SWITCH — HARNESS_AUTO_TRIGGER=0 désactive FR-1/FR-3/FR-5/FR-7"
- **DoD** : `rg "KILL-SWITCH\|HARNESS_AUTO_TRIGGER" CLAUDE.md` returns ≥2 hits

### Phase 7 — Integration & Validation (45 min)

#### T-019 · Run full test suite
- **type** : test
- **effort** : 10 min
- **deps** : [T-007, T-009, T-013, T-016, T-017]
- **deliverable** : 45/45 + 5 cross-cutting = 50 tests PASS
- **approach** :
  - `bash bin/adv-loop test` (must show 45 PASS)
  - `pytest tests/ -v` (must show 50 PASS)
  - Fix any regression before T-020
- **DoD** : both commands show 100% pass

#### T-020 · Live validation
- **type** : validation
- **effort** : 30 min
- **deps** : [T-019]
- **deliverable** : 1 real Claude Code session, validated end-to-end
- **approach** :
  - Open session with hooks active
  - Send 5 varied prompts: "Refactor auth" (P5), "Write tests" (P6), "Discover needs" (P0), "Deploy prod" (P7), "Hello" (no-op)
  - Verify intent.phase correct in state DB after each
  - Make 10 edits on `src/foo.py`, verify:
    - Council fires at 5th edit (cooldown 1h respected)
    - Mini-council returns OK on each edit
  - Set `HARNESS_AUTO_TRIGGER=0`, verify all 4 features disabled
- **DoD** : all 5 prompts correctly classified, Council fires at 5th edit, mini-council runs on all 10, kill-switch works

#### T-021 · Update CHANGELOG + commit + push
- **type** : ops
- **effort** : 15 min
- **deps** : [T-020]
- **deliverable** : v1.6.0 entry in CHANGELOG, commit pushed
- **approach** :
  - Add to CHANGELOG.md: "## v1.6.0 (2026-06-10) — Anti-drift auto-trigger sprint: G1+G3+G5+G6+G8"
  - `git add -A && git commit -m "feat(antidrift): G1+G3+G5+G6+G8 auto-trigger sprint (closes G1+G3+G5+G6+G8)"`
  - `git push origin master`
- **DoD** : `git log --oneline -3` shows commit, CHANGELOG.md updated

## 2. Execution Order (DAG)

```
T-001 ── T-002 ──┬── T-003 ──┬── T-004 ── T-005 ── T-008 ── T-009
                  │           │                                  │
                  │           ├── T-006                          │
                  │           │                                  │
                  │           └── T-007                          │
                  │                                              │
                  ├── T-010 ── T-011 ── T-013                  T-017 ── T-018
                  │       │                                       │
                  │       └── T-012                              │
                  │                                              │
                  └── T-014 ── T-015 ── T-016                  ─┘
                                                                  │
                                                  T-019 ←────────┘
                                                  T-020
                                                  T-021
```

## 3. Cumulative Effort

| Phase | Tasks | Effort | Cumulative |
|---|---|---|---|
| P0 | T-001 | 15 min | 0:15 |
| P1 | T-002 | 15 min | 0:30 |
| P2 | T-003→T-007 | 2h15 | 2:45 |
| P3 | T-008→T-009 | 1h15 | 4:00 |
| P4 | T-010→T-013 | 1h30 | 5:30 |
| P5 | T-014→T-016 | 1h05 | 6:35 |
| P6 | T-017→T-018 | 25 min | 7:00 |
| P7 | T-019→T-021 | 45 min | 7:45 |

**Total : 7h45** (vs 7h estimate, +45 min buffer for live validation issues)

## 4. Quality Gates (sequential checkpoints)

| Gate | After | Check | Action on Fail |
|---|---|---|---|
| G-0 | T-001 | git status clean, pre-commit symlink, steering DB > 0 | Re-run quick wins |
| G-1 | T-002 | 20 existing self-tests still pass | Revert state_engine.py changes |
| G-2 | T-007 | T1-T10 PASS, 30 total | Fix auto_trigger bugs |
| G-3 | T-009 | T11-T15 PASS, 35 total | Fix phase-guard extension |
| G-4 | T-013 | T16-T20 PASS, 40 total | Fix council_scheduler |
| G-5 | T-016 | T21-T25 PASS, 45 total | Fix mini_council |
| G-6 | T-018 | T26-T30 PASS, 50 total | Fix kill-switch |
| G-7 | T-019 | 50/50 PASS | Fix regressions |
| G-8 | T-020 | Live validation green | Iterate on real session |
| G-9 | T-021 | Committed + pushed | Verify remote |

## 5. Hand-off to /speckit.implement

**Skill status** : `speckit-implement` IS installed at `/home/doz/.claude/skills/core/speckit-implement/SKILL.md`.

**Expected workflow** :
1. Setup : verify pytest, state_engine, hooks available
2. Implementation : execute T-001 → T-021 in order
3. Verification : run quality gates G-0 → G-9
4. Completion : commit + push

**Inputs to /speckit.implement** :
- This TASKS.md (21 atomic tasks)
- PLAN.md (architecture decisions)
- SPEC.md (functional + non-functional requirements)
- Design doc §7 (file ownership, ~700 LOC of new code total)

**Status : Ready for /speckit.implement.**
