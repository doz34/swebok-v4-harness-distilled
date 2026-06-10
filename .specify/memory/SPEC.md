# SPEC — SWEBOK v4 Anti-Drift Auto-Trigger Sprint

> **Date** : 2026-06-10
> **Source** : design doc `docs/v2-plan/09-sprint-antidrift-autotrigger.md` (Ready, 4 itérations, 7/7 ICD checks)
> **Spec version** : 1.0
> **Hand-off** : → `/speckit.plan`

## 1. Feature Overview

| Field | Value |
|---|---|
| **name** | `antidrift-auto-trigger` |
| **type** | feature |
| **priority** | critical (closes 4 HIGH/CRIT gaps from audit 2026-06-10) |
| **scope** | full (4 features: G1 + G3 + G5 + G6) |
| **effort** | ~8h dev + 1h test + 30 min live validation |
| **sprint** | v2-S2 (extends v2 plan) |

## 2. User Stories (WHAT, not HOW)

### US-1: Intent Detection on User Prompt
- **as_a** : maintainer qui ouvre une session Claude Code
- **i_want** : que le harness détecte automatiquement l'intention de mon premier prompt (intent.phase)
- **so_that** : la phase correcte soit assignée et les bons patterns chargés sans que je doive dire "use P5"

### US-2: Adversarial Gate on Phase Change
- **as_a** : mainteneur en cours de projet
- **i_want** : que le adversarial-gate fire automatiquement quand la phase change (et pas seulement à ma demande)
- **so_that** : le Council 4-judges valide la transition, empêchant les drifts de phase silencieux

### US-3: Council Auto-Fire Every N Edits
- **as_a** : mainteneur qui fait des edits
- **i_want** : qu'un Council complet (4 LLM-judges) fire automatiquement tous les 5 edits non-triviaux
- **so_that** : la dimension adversariale reste élevée sans que je doive penser à la déclencher

### US-4: Mini-Council Per Edit (Cheap Adversarial)
- **as_a** : mainteneur qui édite
- **i_want** : qu'un mini-council 1 Haiku judge passe sur chaque edit non-trivial (skip `*.md`/`*.json`/`tests/*`)
- **so_that** : le drift sémantique soit détecté en temps réel, pas seulement à la prochaine revue

### US-5: Kill-Switch Safety Net
- **as_a** : mainteneur qui voit trop de bruit du nouveau système
- **i_want** : pouvoir désactiver globalement l'auto-trigger avec `HARNESS_AUTO_TRIGGER=0`
- **so_that** : je puisse travailler sans interruption si l'anti-drift devient trop bruyant

## 3. Functional Requirements

| ID | Requirement | Source design | Priority |
|---|---|---|---|
| **FR-1** | `UserPromptSubmit` hook fires on every user prompt, calls `lib/auto_trigger.py` which returns intent.phase + confidence | D1 | P0 |
| **FR-2** | If `intent.confidence >= 0.5`, write `intent.phase` to `.swebok_state.db` ; if < 0.5, no-op + log | D1 | P0 |
| **FR-3** | `pre-tool-use/phase-guard.sh` reads `intent.phase` + `current_phase` ; if diff, emit `<MULTIAGENT_LAUNCH>` envelope | D2 | P0 |
| **FR-4** | Adversarial-gate, when invoked via envelope, runs Council 4-judges (ciso/qa-lead/architect/devops-lead) per ADR-003 | D2 + B4 | P0 |
| **FR-5** | `post-tool-use/auto-verify.sh` increments `edits_since_council` counter on each non-whitelist edit | D3 | P0 |
| **FR-6** | If `edits_since_council >= 5` AND `now - council.last_at >= 3600s`, fire full Council + reset counter | D3 | P0 |
| **FR-7** | `post-tool-use/auto-verify.sh` calls `lib/adv-loop/mini_council.py` for each non-whitelist edit | D4 | P0 |
| **FR-8** | Mini-council uses Haiku 4.5 model, returns DSL line `mini_council:finding=OK\|VULN:<sev>;;...` | D4 | P0 |
| **FR-9** | Whitelist: skip counter + mini-council for `*.md`, `*.json` (config), `tests/*` | D3+D4 | P0 |
| **FR-10** | If `1+ finding in 3 consecutive edits`, escalate to full Council (override cooldown) | D4 | P1 |
| **FR-11** | `HARNESS_AUTO_TRIGGER=0` env var disables FR-1, FR-3, FR-5, FR-7 globally (kill-switch) | D8 | P0 |
| **FR-12** | State DB keys: `intent.phase`, `intent.confidence`, `intent.timestamp`, `edits_since_council`, `council.last_at`, `phase_history[]` | D5 | P0 |
| **FR-13** | `phase_history[]` is FIFO with max 10 entries, oldest evicted | D5 | P1 |
| **FR-14** | `clear` steering DB does NOT touch `intent.*` keys in main state DB | Q2 | P0 |
| **FR-15** | `settings.json` + `settings.template.json` add `UserPromptSubmit` matcher pointing to `auto-trigger-hook.sh` | D6 | P0 |
| **FR-16** | `bin/adv-loop auto-trigger <prompt>` CLI for manual testing | D1 | P1 |
| **FR-17** | `bin/adv-loop council-status` shows `edits_since_council` + `council.last_at` | D3 | P1 |
| **FR-18** | All hooks fail-open (exit 0 on internal error) — never block legitimate work | L1, L4 | P0 |

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-P1** : UserPromptSubmit hook latency < 50ms p50 (cache hit), < 100ms p95 (pattern match), < 500ms p99 (semantic), fail-open if > 500ms
- **NFR-P2** : Mini-council per edit < 2s p95
- **NFR-P3** : Council full 4-judge < 30s p95
- **NFR-P4** : Cache hit rate > 80% on repeated prompts (Fowler observation)

### 4.2 Security
- **NFR-S1** : Hooks read no secrets, write no secrets to state DB
- **NFR-S2** : State DB writes are atomic (SQLite WAL)
- **NFR-S3** : Phase diff detection uses signed state keys, not user input
- **NFR-S4** : No modification of `~/.claude/settings.json` (user constraint, hard)

### 4.3 Reliability
- **NFR-R1** : 100% of hooks fail-open on internal error
- **NFR-R2** : 100% of state DB reads tolerant of missing keys (return default)
- **NFR-R3** : Steering DB TTL 90 days on runs

### 4.4 Maintainability
- **NFR-M1** : All new code follows existing lib/adv-loop/ module pattern (Python stdlib only, no third-party deps)
- **NFR-M2** : All new DSL output uses `;;` delimiter (CLAUDE.md L4)
- **NFR-M3** : All new hooks read stdin JSON (Claude Code contract) with positional args fallback
- **NFR-M4** : All new code tested (≥ 1 test per FR)
- **NFR-M5** : All new env vars documented in CLAUDE.md

### 4.5 Usability
- **NFR-U1** : `bin/adv-loop help` lists all subcommands including new ones
- **NFR-U2** : `bin/adv-loop council-status` output is human-readable (no DSL)
- **NFR-U3** : Phase change fires a `[PHASE-CHANGE]` log line visible to user

## 5. Acceptance Criteria

See `acceptance-criteria.md` for the 25 testable criteria (10 G1 + 5 G3 + 5 G5 + 5 G6).

## 6. Out of Scope (sprint +1)

- **OOS-1** : Token counter adaptatif 3-niveaux (P8-1/P9-1/P10-1) — autre sprint
- **OOS-2** : 3 Councils formalisés (post-incident, structurante, clôture) — autre sprint
- **OOS-3** : GitHub publish v2 (S4 plan v2) — autre sprint
- **OOS-4** : Skills mapping 50+ skills → phases (S5 plan v2) — autre sprint
- **OOS-5** : v1.5.x doc updates (CHANGELOG, README)
- **OOS-6** : Pre-commit auto-install (G2 quick win) — pre-sprint quick win, hors scope formel
- **OOS-7** : Refonte des frontières P0-P10 (modèle 10-phases → 11-phases) — refonte majeure

## 7. Dependencies

| Type | Dependency | Status |
|---|---|---|
| **Code** | `lib/state_engine.py` (atomic get/set/incr) | ✅ exists |
| **Code** | `lib/adv-loop/{council,feedback,steering}.py` | ✅ exists (S1+S2+S3) |
| **Code** | `lib/dsl_engine.py` (strict `;;` parser) | ✅ exists |
| **Code** | `intent-detector.py` (22K LOC, 4 layers) | ✅ exists (NON wired) |
| **Code** | `pre-tool-use/phase-guard.sh` (fail-secure) | ✅ exists + wired |
| **Code** | `post-tool-use/auto-verify.sh` (lint) | ✅ exists + wired |
| **Code** | `adversarial-gate.sh` (Council 4-judge) | ✅ exists (--council opt-in) |
| **Code** | `bin/adv-loop` (orchestrator) | ✅ exists (5 subcommands) |
| **State** | `.swebok_state.db` (SQLite WAL) | ✅ exists |
| **State** | `.swebok_steering_state.db` | ⚠️ exists but 0 octets (S3 non tourné en prod) |
| **Config** | `settings.json` (PreToolUse/PostToolUse matchers) | ✅ exists, no UserPromptSubmit yet |
| **Tests** | pytest 7+ (Python stdlib) | ✅ assumed available |
| **Model** | Haiku 4.5 (mini-council judge) | ✅ Claude Code default |
| **User constraint** | No modification of `~/.claude/settings.json` | ✅ respected (only repo settings.json) |

## 8. Edge Cases & Error Handling

| Edge case | Behavior |
|---|---|
| User prompt = empty | layer 4 fallback : human-escalation log, no state write |
| User prompt = "Hello" (no detectable intent) | layer 4 fallback : log confidence=0.0, no state write |
| intent-map.json missing | layer 3 fallback : log error, no-op |
| Network offline (semantic layer unreachable) | layer 3 fail-open : no-op, no state write |
| State DB missing | bootstrap.sh auto-run, fail-secure if bootstrap fails |
| State DB corrupted | fail-secure : exit 1 (do not block work) |
| Haiku 4.5 unavailable | mini-council fail-open exit 0, counter continues |
| 4 LLM-judges unavailable | full Council fail-open, log error |
| Phase diff race condition | SQLite WAL atomicity guarantees serialized reads |
| Pre-commit conflict with user custom hook | G2 quick win : detect + propose, NEVER auto-overwrite |
| User has custom settings.json | `install-harness.sh` merge idempotent (additive only) |
| Intent confidence = 0.49 (just below threshold) | no state write, no fire, log only |
| 100 edits in 5 minutes (Council overload) | cooldown 1h + threshold 5 = max 1 Council per 5 edits window |

## 9. Success Metrics

- **SM-1** : `bin/adv-loop test` reports 45/45 PASS (20 existing + 25 new)
- **SM-2** : User prompt → phase assignment latency < 100ms p95 (cache hit 80%+)
- **SM-3** : Phase change → Council fire latency < 5s p95
- **SM-4** : Council full fires exactly every 5 edits (no missed, no spurious)
- **SM-5** : Mini-council fires on 100% of non-whitelist edits, fail-open rate < 1%
- **SM-6** : Live validation : 1 real Claude Code session, 5 varied prompts → 5 correct phase assignments
- **SM-7** : `HARNESS_AUTO_TRIGGER=0` correctly disables all 4 features (verified by integration test)

## 10. Architecture Summary

```
┌─────────────────────┐
│ User prompt         │ → UserPromptSubmit → auto-trigger-hook.sh → lib/auto_trigger.py
└─────────┬───────────┘   (cache/pattern/semantic/fallback) → state DB write intent.phase
          │
          ▼
┌─────────────────────┐
│ PreToolUse          │ → phase-guard.sh : read intent.phase vs current_phase
└─────────┬───────────┘   if diff → emit <MULTIAGENT_LAUNCH> → adversarial-gate --council
          │                                                       → spawn 4 LLM-judges
          ▼
┌─────────────────────┐
│ PostToolUse         │ → auto-verify.sh : lint + counter + mini-council
└─────────┬───────────┘   edits_since_council >= 5 (cooldown 1h) → fire full Council
          │                1 finding in 3 edits → escalate
          │
          ▼
┌─────────────────────┐
│ Phase change        │ → phase_history[] append (FIFO 10)
└─────────────────────┘   state DB persists across sessions
```

## 11. SWEBOK v4 Alignment

| KA | Topic | Coverage |
|---|---|---|
| KA-1 | Software Requirements | Spec doc + acceptance criteria |
| KA-2 | Software Design | Architecture + state schema |
| KA-4 | Software Construction | New code follows existing lib/ patterns |
| KA-5 | Software Testing | 25 tests planned (pytest) |
| KA-6 | Software Engineering Mgmt | Sprint scope + budget |
| KA-7 | Software Engineering Process | Iterative ICD workflow |
| KA-8 | Software Quality | DSL strict + adversarial dimension |
| KA-11 | Software Quality (advanced) | NFR section + 5 sub-categories |

## 12. Open Questions (all decided in design iter 4)

| Q | Decision |
|---|---|
| Q1: Fréquence mini-council | Every non-whitelist edit, escalation 1/3 |
| Q2: intent.phase persist clear | OUI, intent.* untouched by clear |
| Q3: G5 edits vs wall-clock | Edits + cooldown 1h |
| Q4: Budget tokens | 8h = ~50K tokens |
| Q5: Kill-switch | OUI, HARNESS_AUTO_TRIGGER=0 |

**Status : Ready for /speckit.plan.**
