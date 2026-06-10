# Acceptance Criteria — SWEBOK v4 Anti-Drift Auto-Trigger Sprint

> **Date** : 2026-06-10
> **Source** : SPEC.md, design doc §12 (validation plan)
> **Total** : 25 testable criteria (10 G1 + 5 G3 + 5 G5 + 5 G6)

## G1 — UserPromptSubmit Auto-Trigger (10 tests)

### T1
- **criterion** : prompt "Write tests for the user model" → intent.phase=6, confidence > 0.8
- **verification** : `bin/adv-loop auto-trigger "Write tests for the user model"` returns `intent.phase=6;;intent.confidence=0.85;;...`
- **type** : functional

### T2
- **criterion** : prompt "Refactor the auth module" → intent.phase=5, confidence > 0.7
- **verification** : `bin/adv-loop auto-trigger "Refactor the auth module"` returns phase=5
- **type** : functional

### T3
- **criterion** : prompt "Discover stakeholder needs" → intent.phase=0, confidence > 0.8
- **verification** : same pattern as T1, phase=0
- **type** : functional

### T4
- **criterion** : empty prompt → fallback chain, no state write
- **verification** : `bin/adv-loop auto-trigger ""` returns confidence=0.0, state DB `intent.phase` unchanged
- **type** : edge case

### T5
- **criterion** : prompt "Hello" → fallback + human-escalation log
- **verification** : log line `[AUTO-TRIGGER] human-escalation: prompt='Hello' confidence=0.0`
- **type** : edge case

### T6
- **criterion** : prompt "Deploy to production" → intent.phase=7, confidence > 0.7
- **verification** : phase=7, confidence > 0.7
- **type** : functional

### T7
- **criterion** : 100 varied prompts latency < 1s p95
- **verification** : benchmark script `tests/bench_auto_trigger.sh` runs 100 prompts, reports p95 < 1000ms
- **type** : performance (NFR-P1)

### T8
- **criterion** : works offline (no network)
- **verification** : with `unset ANTHROPIC_API_KEY`, `bin/adv-loop auto-trigger "..."` still returns phase via cache+pattern
- **type** : reliability (NFR-R1)

### T9
- **criterion** : cache hit < 50ms
- **verification** : run same prompt twice, second call < 50ms (timing wrapper)
- **type** : performance (NFR-P1)

### T10
- **criterion** : manual override `phase=5` in prompt → force P5
- **verification** : `bin/adv-loop auto-trigger "phase=5 do something"` returns phase=5 regardless of content
- **type** : usability

## G3 — Adversarial Gate on Phase Change (5 tests)

### T11
- **criterion** : phase-guard.sh reads intent.phase, detects diff with current_phase
- **verification** : pre-set state DB `intent.phase=5 current_phase=2`, run a Write, log line `[PHASE-GUARD] phase diff detected: 2→5`
- **type** : functional (FR-3)

### T12
- **criterion** : diff detected → emit `<MULTIAGENT_LAUNCH>` envelope
- **verification** : same setup as T11, hook output contains `<MULTIAGENT_LAUNCH ...>` XML
- **type** : functional (FR-3)

### T13
- **criterion** : no diff → no envelope emit, normal lint
- **verification** : pre-set `intent.phase=5 current_phase=5`, run a Write, no envelope, no block
- **type** : regression

### T14
- **criterion** : phase_history append + FIFO eviction at 10
- **verification** : run 12 phase changes, state DB `phase_history` has exactly 10 entries, oldest 2 evicted
- **type** : functional (FR-13)

### T15
- **criterion** : phase change fail-secure (state DB write error → no fire)
- **verification** : mock state_engine.py get/set to raise, verify hook exits 1, no envelope emitted
- **type** : security (NFR-S2)

## G5 — Council Auto-Fire Every N Edits (5 tests)

### T16
- **criterion** : counter increments on each non-whitelist edit
- **verification** : pre-set counter=0, run 3 `Write src/foo.py` ops, counter=3
- **type** : functional (FR-5)

### T17
- **criterion** : counter resets after Council fire
- **verification** : pre-set counter=5, run 1 Write, Council fires, counter=0
- **type** : functional (FR-6)

### T18
- **criterion** : threshold default 5, configurable via env var
- **verification** : `HARNESS_COUNCIL_THRESHOLD=3` + counter=2 + 1 Write = fire
- **type** : configurability

### T19
- **criterion** : whitelist `*.md`/`*.json`/`tests/*` skips counter
- **verification** : pre-set counter=0, run 3 `Write README.md` + 2 `Write src/foo.py`, counter=2 (not 5)
- **type** : functional (FR-9)

### T20
- **criterion** : `adv-loop council-status` shows correct counter + last_at
- **verification** : pre-set counter=2, council.last_at=1234567890, run `bin/adv-loop council-status`, output contains both
- **type** : usability (NFR-U2)

## G6 — Mini-Council Per Edit (5 tests)

### T21
- **criterion** : mini_council.py call returns DSL line within 2s
- **verification** : `python3 lib/adv-loop/mini_council.py src/foo.py` returns `mini_council:finding=OK;;...` in < 2s
- **type** : performance (NFR-P2)

### T22
- **criterion** : Haiku unavailable → fail-open exit 0
- **verification** : mock API to 500 error, run mini_council.py, exit 0, no finding logged
- **type** : reliability (NFR-R1)

### T23
- **criterion** : 1 finding in 3 edits → escalate to full Council
- **verification** : inject 3 mini-council findings, verify full Council envelope emitted (override cooldown)
- **type** : functional (FR-10)

### T24
- **criterion** : 0 findings in 3 edits → no escalation
- **verification** : inject 3 OK findings, verify no Council envelope
- **type** : regression

### T25
- **criterion** : mini_council DSL output well-formed (KEY=VALUE;;...)
- **verification** : regex match `^mini_council:[a-z_]+=[A-Za-z0-9:_-]+;;` against actual output
- **type** : correctness (NFR-M2)

## Cross-cutting Tests (5 from design doc, to be added)

### T26
- **criterion** : HARNESS_AUTO_TRIGGER=0 disables all 4 features
- **verification** : export HARNESS_AUTO_TRIGGER=0, run 10 varied ops, verify no auto-trigger, no Council, no mini-council
- **type** : safety (FR-11, SM-7)

### T27
- **criterion** : `bin/adv-loop test` reports 45/45 PASS (20 existing + 25 new + this = 45)
- **verification** : run `bin/adv-loop test`, expect PASS count = 45 (was 20)
- **type** : integration (SM-1)

### T28
- **criterion** : settings.json merge idempotent (re-install safe)
- **verification** : run `install-harness.sh` twice, settings.json content identical (modulo timestamps)
- **type** : maintainability

### T29
- **criterion** : steering DB TTL 90 days enforced
- **verification** : insert run with timestamp=now-91d, run `clear`, verify it's removed
- **type** : reliability (NFR-R3)

### T30
- **criterion** : phase_history FIFO at 10
- **verification** : same as T14, included for cross-coverage
- **type** : functional (FR-13)

## Test Execution Plan

| Step | Command | Expected |
|---|---|---|
| 1. Install pytest | `pip3 install pytest` | success |
| 2. Run unit tests | `python3 -m pytest tests/test_auto_trigger.py tests/test_council_scheduler.py tests/test_mini_council.py -v` | 30 PASS |
| 3. Run self-tests | `bin/adv-loop test` | 45 PASS (was 20) |
| 4. Run live validation | 1 real session, 5 varied prompts, 10 edits | SM-2, SM-4, SM-6 |

## Pass/Fail Criteria

- **PASS** : 45/45 + 5 cross-cutting + 1 live validation = 51/51
- **BLOCK** : any P0 test fail (T1-T6, T11-T13, T15-T19, T21-T22, T25-T27)
- **ACCEPTABLE** : P1 tests fail (T14, T20, T23-T24, T28-T30), 1-2 acceptable with rationale
- **REGRESSION** : any existing 20 self-test fail → sprint blocked, must fix before proceed
