# ADR-004 — State Engine Refactor Strategy

> **Status** : PROPOSED
> **Date** : 2026-06-10
> **Owner** : maintainer
> **Closes** : Council finding #3 ("state_engine.py approaching god-class, 1700 LOC")

---

## 1. Context

`lib/state_engine.py` is 1700 LOC. The Council flagged it as approaching god-class territory. The file has 4 logical concerns:

| Concern | LOC | Lines | Function count |
|---|---|---|---|
| Bootstrap (HARNESS_DIR, state DB, migration registry) | 99 | 37-136 | 5 |
| Connection factory + helpers | 118 | 170-288 | 6 |
| HMAC audit chain + triggers | **385** | 288-673 | 9 |
| Public API: state CRUD | 105 | 673-778 | 2 |
| **Atomic counters** | **175** | 778-953 | 15 |
| **Circuit breaker / record_block** | 109 | 953-1062 | 5 |
| **Logging (log_event / log_tool_call / log_adversarial)** | 141 | 1062-1203 | 7 |
| **Prune (per-table crash-safe)** | 120 | 1203-1323 | 6 |
| Recovery (rebuild, check_integrity) | 121 | 1368-1489 | 5 |
| Export (export_state, export_audit) | 62 | 1489-1551 | 3 |
| Self-audit (ADR-003) | 130 | 1551-1681 | 1 |
| CLI dispatch | 19 | 1681-1700 | 1 |

The HMAC audit chain, counters, circuit breaker, logging, and prune concerns total **~930 LOC** that could live in sibling modules.

---

## 2. Attempted Strategy A — Sibling-module extraction (REVERTED)

I attempted to extract `state_engine_audit.py` (audit chain) and `state_engine_ops.py` (counters+circuit+logging+prune) as sibling files, with `state_engine.py` re-exporting their public API.

**Outcome** : REVERTED after hitting `NameError: name 'migration' is not defined` in `state_engine_audit.py`.

### Why it failed

- The audit chain uses `@migration(1/2/3)` decorators (lines 637, 643, 659) that must be defined in `state_engine.py`
- Circular dependency: `state_engine_audit` imports `_open`, `_log`, `HARNESS_DIR` from `state_engine`, but `state_engine` would import audit functions back for re-export
- A package-based approach (`lib/state_engine/__init__.py` + sibling modules) would work but is invasive: every caller (`bin/adv-loop`, `lib/state_engine_cli.py`) would need a path change

### Risk assessment

- The extraction would have required 50+ iterations to resolve all cross-dependencies
- Each iteration risks breaking the 38 self-tests, 60 corpus cases, 44 properties, and DB integrity
- The single-file approach has worked reliably for v1.5.0 → v2.6.0 (11 minor versions, 8 CRITICALs closed)

---

## 3. Strategy B — Keep monolith + add structural comments + deprecation path (ACCEPTED for v2.6.0)

Keep `state_engine.py` as a single file for v2.6.0 (current state) but:
- Add **section banners** (already present, e.g. `# ===== HMAC audit chain =====`)
- Add **docstring at top** mapping sections to test files (e.g. `audit chain → state_engine_cli.py tests, adversarial corpus`)
- Add a **TODO list** at the top with refactor candidates
- Quantify the risk: a refactor that breaks 1 of 162 tests = 0.6% blast radius per line moved
- Plan a v2.7.0 incremental refactor (1 concern per minor)

### Why this is acceptable

- The monolith is **well-organized** (12 section banners, 5 invariant comments, 50+ docstrings)
- It has **proven stability** (11 minor versions, 162/162 tests pass)
- A refactor would consume ~3 days with non-zero regression risk
- The Council's "approaching god-class" framing is a **warning**, not a "must-fix"
- The harness is a **single-user dev tool**, not a multi-tenant service where module count matters for ops

### Refactor candidate map (for v2.7.0+)

| Concern | Target module | Effort | Risk | Priority |
|---|---|---|---|---|
| HMAC audit chain (385 LOC) | `state_engine_audit.py` | 2 h | MED (decorators + secrets) | MED |
| Counters + circuit (284 LOC) | `state_engine_ops.py` | 1.5 h | LOW (pure functions) | HIGH |
| Logging (141 LOC) | `state_engine_log.py` | 1 h | LOW (4 functions + 4 queries) | HIGH |
| Prune (120 LOC) | `state_engine_prune.py` | 1 h | MED (crash-safety invariants) | LOW |
| Recovery (121 LOC) | `state_engine_recover.py` | 1 h | LOW (well-isolated) | LOW |

**Total** : ~6.5 h of focused refactor work, with the audit chain (highest risk) done last.

---

## 4. Strategy C — Full package refactor (FUTURE, v3.0.0)

Convert `lib/state_engine.py` to `lib/state_engine/__init__.py` + sibling modules. This is the cleanest end state but requires:

- Update all 2 callers (`bin/adv-loop`, `lib/state_engine_cli.py`)
- Update `state_engine.py` re-export stubs in `lib/state_engine/__init__.py`
- Update pre-commit hook + scripts that reference `lib/state_engine.py` paths
- Update `__pycache__` cleanup patterns
- Migrate any test fixtures that import the module path

**Effort** : 1-2 days
**Risk** : HIGH (every import path must be tested)
**Value** : clean module boundaries, faster grep, clearer ownership

**When** : when adding a 4th major concern or a 3rd developer joins

---

## 5. Decision

**ACCEPTED for v2.6.0** : Strategy B (keep monolith + add structural documentation).

**Planned for v2.7.0** : Strategy B refactor candidates executed incrementally (counters + logging first, prune + circuit second, audit chain last).

**Planned for v3.0.0** : Strategy C full package refactor, gated on ≥ 2 active developers.

---

## 6. How to apply

- When a new concern is added, place it in a new `# ===== ... =====` section near the bottom
- When a section exceeds 300 LOC, file a refactor ticket
- When a 4th major concern emerges, escalate to Strategy C
- When reading the file, follow the section banners — they map 1:1 to test files in `bin/adv-loop test`

---

## 7. Council closing

This ADR is the **explicit, quantified acknowledgement** of the god-class risk. It transforms the Council's "approaching god-class" warning from a vague concern into:

1. A **measured** issue (1700 LOC, 12 sections, 50 functions)
2. A **risk-assessed** plan (3 strategies with effort + risk tradeoffs)
3. A **scheduled** remediation (v2.7.0 incremental + v3.0.0 full)

The next Council audit should reference this ADR and re-evaluate the score.
