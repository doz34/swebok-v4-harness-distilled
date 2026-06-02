# INDEPENDENT AUDIT REPORT — SWEBOK v4 Harness v1.4.1

**Date**: 2026-06-01 (16:50 CEST)  
**Auditor**: Independent (Claude main loop + 5 sub-agents + ICD design review)  
**Methodology**: Adversarial — refute the "100% production-ready" self-claim

## VERDICT

**Claim**: "100% / 100% / 100% production-ready" (auto-declared by 4 waves of self-fix).

**Verdict**: ❌ **REFUTED**. The harness is a working **prototype with safety theater** (architect: C+). It passes its own test suite by construction, but multiple core safety primitives are non-functional or actively backwards (fail-open instead of fail-secure).

The tautology hypothesis the user raised is **confirmed**: tests written by the same agents that wrote the code exercise paths designed to pass. The adversarial finders here exercised paths the harness's authors didn't think of, and a non-trivial fraction failed.

---

## CRITICAL FINDINGS (must fix before production)

### CRIT-1 — Circuit breaker is **fail-OPEN**, not fail-secure
**File**: `hooks/pre-tool-use/phase-guard.sh:321-325`  
**Evidence**:
```bash
if [[ "$blocked_count" -ge 3 ]] && [[ "$override_active" != "True" ]]; then
    activate_override
    echo "[PHASE-GUARD] DEADLOCK_WARNING: Hook blocked $blocked_count times on $FILE_PATH"
    echo "[PHASE-GUARD] Override active. Action allowed with warning."
    exit 0           # ← ALLOWS the blocked action
fi
```
**Impact**: After 3 blocked actions, the next 5 minutes (`MAX_OVERRIDE_AGE=300`) permit **every** action that would have been blocked. Adversary just needs to attempt the bypass 3 times to unlock arbitrary writes/commands for 5 min.  
**Severity**: **CRITICAL** — this is the inverse of a security gate.  
**Mitigation**: Hard-lock for the 5-minute window (`exit 1` + operator log), OR rename to "cooldown UX" and stop claiming security properties.

### CRIT-2 — `adversarial-gate.sh` is a **hardcoded fixture**, not an adversarial gate
**File**: `scripts/adversarial-gate.sh:145-182`  
**Evidence**:
```bash
P5)
    RED_ACTUAL="RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION_RISK;;FIX_REQ:SANITIZE_ALL_INPUTS"
    BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-4+KA-5;;STATUS:OK"
    ;;
```
**Impact**: CLAUDE.md LAW 6 and `docs/v1/ADVERSARIAL.md` claim strict Red/Blue with DSL adversarial validation. The reality is a phase-keyed table lookup returning canned strings. Every gate transition reports the same `RED:` and `BLUE:` content for the same phase, regardless of what the agent did. **The adversarial review is theater.**  
**Severity**: **CRITICAL** — the central safety property advertised by the harness is non-functional.  
**Mitigation**: Either wire to `multiagent-launcher.sh` and parse real responses, or rename to `adversarial-gate-fixture.sh` and remove from `validate-gates.sh` production paths.

### CRIT-3 — Append-only audit log is **enforced by honesty**
**File**: `scripts/lib/state_engine.py:393-420` (triggers) + `:1211-1238` (`_prune_with_trigger`)  
**Evidence**: The same module that creates the `BEFORE DELETE` triggers also contains `_prune_with_trigger()` which does `DROP TRIGGER → DELETE → CREATE TRIGGER`. The "append-only" property is uninstallable by any code path that can `import sqlite3`. There is no separate maintenance-role boundary.  
**Compounding**: If the Python process is killed between `DROP TRIGGER` and `CREATE TRIGGER` (line 1215-1236), the table loses its append-only protection **permanently** with no startup recovery.  
**Severity**: **CRITICAL** — audit forensics cannot be relied on.  
**Mitigation**: 
1. Wrap the DROP+DELETE+CREATE sequence in a single `BEGIN EXCLUSIVE` transaction (SQLite supports DDL in transactions).
2. In `_init_db()`, re-issue `CREATE TRIGGER IF NOT EXISTS` for all 4 audit triggers on every startup (defense in depth).
3. Long-term: move audit tables to a separate DB file the harness opens read-only and a separate process appends to (real separation of duties).

### CRIT-4 — SQLite DB observed in **`database disk image is malformed`** state during this audit
**Evidence**: This auditor's own `python3 scripts/lib/state_engine.py get current_phase` returned `sqlite3.DatabaseError: database disk image is malformed` on the same DB that "1000/1000 concurrent" test had just claimed to pass. The DB auto-rebuilt (visible: `.swebok_state.db.corrupt.1780324510`), but the corruption window between corruption and rebuild is unbounded — during that window, hooks fail (probably fail-open).  
**Severity**: **CRITICAL** — the "1000 concurrent atomic" claim is the most-cited reliability claim; this is the strongest possible refutation.  
**Mitigation**:
1. The 1000-concurrent test must be re-run with `PRAGMA integrity_check` BEFORE and AFTER and assert both return `ok`. Today the test only counts increments.
2. Add a recovery latency budget (e.g. "rebuild() completes in <1s") and a circuit-breaker test that proves hooks block (not allow) during the rebuild window.

### CRIT-5 — `bash-guard.sh` blocks **legitimate read-only commands**
**Phase**: P5_CONSTRUCTION (the current phase)  
**Evidence** (auditor's tests):
```
BLOCKED: echo "src"
BLOCKED: echo source
BLOCKED: ls /etc/src.conf
BLOCKED: cat README.md | grep src
BLOCKED: man rsrc
BLOCKED: ls /usr/src
BLOCKED: apt-get source vim
```
**Impact**: The substring-matching is so aggressive that documentation reading, package management, and basic shell usage are all blocked. In real Claude sessions, this would force the user to either disable the harness or override the circuit breaker (see CRIT-1). The combination of CRIT-5 (over-block) and CRIT-1 (3-strikes-unlock) is **especially bad**: legitimate friction trains the user to repeatedly trigger the override, defeating the harness.  
**Severity**: **HIGH→CRITICAL** depending on usage pattern.  
**Mitigation**: 
1. Disambiguate "src is a path I'm writing to" from "src is text in a string I'm reading" — the existing word-boundary regex (line 93 comment claims this) is incomplete.
2. Phase rules should distinguish READ from WRITE intent; today P5/P6 block on substring presence regardless.

---

## HIGH SEVERITY FINDINGS

### HIGH-6 — Phase rules duplicated in two languages, **already drifted**
**Files**: `scripts/lib/bash_scanner.py:34-80` (Python dict) + `hooks/pre-tool-use/phase-guard.sh:268-309` (bash conditions)  
**Evidence**: 
- bash_scanner P5 has `block_destructive: True` (rm -rf, DROP TABLE blocked).
- phase-guard.sh P5 has **no** destructive-command block — phase-guard only inspects Write/Edit, while destructive shell commands are scanned by bash-guard which delegates to bash_scanner. If a destructive command is invoked via `MultiEdit` or via a non-Bash matcher path, the destructive block does not fire.  
- bash_scanner P9 allows exceptions for package managers; phase-guard P9 only checks `/src/` and `/lib/` paths.
**Severity**: HIGH — two enforcement layers that diverge silently are worse than one layer that's complete.  
**Mitigation**: Single source of truth `config/phase_rules.json` consumed by both `bash_scanner.py` (via `json.load`) and `phase-guard.sh` (via `jq`).

### HIGH-7 — Phase transitions are not transactional; `current_phase` is freely writable
**File**: `scripts/lib/state_engine.py:533+593` (`get`/`set` on any key, no transition gate)  
**Evidence**: `set current_phase P2` accepts any value. There is no check that `from_phase + "_EXIT"` is in `gates_validated`. The `validate-gates.sh` script appends gates correctly, but enforcement of the transition itself is missing.  
**Severity**: HIGH — the state machine is documentation-only.  
**Mitigation**: Introduce `transition_phase(from, to)` as the only writer of `current_phase`. Inside: `BEGIN EXCLUSIVE`, verify gate, write, audit, COMMIT.

### HIGH-8 — `_get_db()` runs `PRAGMA integrity_check` on **every call** (latency tax)
**File**: `scripts/lib/state_engine.py:243-264`  
**Impact**: O(rows + indexes) on every read or write — at 10k audit rows, ~10ms per call. Hooks call `_get_db` per invocation; ~100 hook calls per Claude tool sequence = ~1s tax per session.  
**Severity**: HIGH (performance) — and the cost will grow.  
**Mitigation**: Run integrity_check once per process in `_init_db()`. Expose `check_integrity()` as a separate operator command.

### HIGH-9 — Hook output contract is **undefined and self-contradictory**
**File**: `hooks/pre-tool-use/phase-guard.sh` (multiple)  
**Evidence**: Three different output modes:
- EMPTY_TOOL_INPUT emits JSON `{"decision":"block",...}`
- Most errors emit plain text `WARN:HOOK_INTERNAL_ERROR: ...` to stderr and `exit 1`
- ANTI-ROT emits `ANTI-ROT:NUDGE ...` and `exit 2` (decoded by Claude as model feedback)
**Severity**: HIGH — Claude's hook decoder must guess the format.  
**Mitigation**: Single output schema — JSON envelope `{"decision","reason","metadata"}` per Claude Code's documented hook contract.

### HIGH-10 — 24 YAML hook files are **dead scaffolding**
**Files**: `hooks/pre-prompt/`, `hooks/post-prompt/`, `hooks/pre-task/`, `hooks/post-task/`, `hooks/event/` + `config/hook-phase-binding.yaml`  
**Evidence**: `grep -r "hook-phase-binding\|hook_1_pre_intent_detection"` returns only the YAML files themselves. `.claude/settings.json` only wires `PreToolUse` + `PostToolUse`. The lifecycle events `pre-prompt`/`post-prompt`/`pre-task`/`post-task`/`event` are **not declared** in settings — Claude Code never invokes the scripts pointed to by these YAMLs.  
**Severity**: HIGH (rot) — 890+ lines of confusing scaffolding that future maintainers will treat as live.  
**Mitigation**: Delete, or wire and test.

---

## MEDIUM FINDINGS

### MED-11 — `prune_*` returns `-1` sentinel, silently coerced by truthiness
**File**: `scripts/lib/state_engine.py:1241-1305`  
**Impact**: `if prune_log_events():` treats `-1` (trigger-blocked) as success.  
**Mitigation**: Typed result (`Result(removed, blocked)`), or raise on blocked.

### MED-12 — `_coerce_for_field` infers type from stringified existing value
**File**: `scripts/lib/state_engine.py:568-590`  
**Impact**: First writer determines type for row lifetime. A migration changing field type from int to string is silently lossy.  
**Mitigation**: Schema map `{state_key: type}`.

### MED-13 — `phase-0-discovery.md` is an orphan
**File**: `specs/specs/workflows/by-phase/phase-0-discovery.md`  
**Evidence**: No P0 in `phase-guard.sh` regex `^[1-9]$`. No P0 in state engine. 10 files for 9 phases.  
**Mitigation**: Delete the file, OR commit to P0 with real hooks + gate + state field. Also flatten `specs/specs/` → `specs/`.

### MED-14 — Documentation drift: `CLAUDE.md` says "47/47 PASS" but tests are 92
**File**: `CLAUDE.md:28`  
**Mitigation**: One-line update.

### MED-15 — Dead test code after `exit 0` in adversarial-test.sh
**File**: `tests/adversarial-test.sh:2134-2138`  
**Evidence**: 4 Sprint 2 regression tests appear duplicated — once at line 1471 (live), once at line 2134 (after `exit 0`, dead).  
**Mitigation**: Delete the dead block.

### MED-16 — `atexit` handler disabled with 14-line tombstone
**File**: `scripts/lib/state_engine.py:148-162`  
**Mitigation**: Replace tombstone with a clear "you must close()" docstring on `_get_pooled_conn`; delete `_close_pooled_conns`.

---

## What was **NOT** refuted (kept)

The audit confirmed the following claims are accurate:
- ✅ Backup-before-migrate via `shutil.copy2` is sound (B1/C10).
- ✅ `set()` audit + state in one `BEGIN EXCLUSIVE` is correct (B7/C11).
- ✅ The 1000-concurrent increment count is atomic *when the DB is healthy* — but see CRIT-4 for what happens when it isn't.
- ✅ The 14 mkdir-src bypass payloads tried by the auditor are all blocked (P5 mkdir-src enforcement is robust).
- ✅ The schema version newer-than-code check refuses (line 463-468 in state_engine.py).
- ✅ M16 audit-restore on rebuild() copies forensic data (though untested end-to-end).

---

## PRIORITY FIX PLAN

| # | Severity | Effort | Fix |
|---|---|---|---|
| 1 | CRIT-1 | 5 min | Replace `exit 0` after override-activate with `exit 1` (fail-closed). Update tests. |
| 2 | CRIT-3 | 15 min | Wrap `_prune_with_trigger` DROP+DELETE+CREATE in BEGIN EXCLUSIVE; add `CREATE TRIGGER IF NOT EXISTS` re-issue in `_init_db()`. |
| 3 | CRIT-5 + HIGH-6 | 60 min | Tighten bash_scanner regexes to distinguish read-only vs write-intent. Consolidate phase rules in one JSON. |
| 4 | CRIT-2 | 30 min | Either rename `adversarial-gate.sh` → `adversarial-gate-fixture.sh` and stop claiming Red/Blue in docs, OR wire to `multiagent-launcher.sh`. |
| 5 | HIGH-7 | 30 min | Introduce `transition_phase()` as sole writer of `current_phase`. |
| 6 | HIGH-8 | 5 min | Move `integrity_check` out of `_get_db()` hot path. |
| 7 | HIGH-10 | 5 min | Delete the 24 unwired YAML hook files. |
| 8 | MED-14, MED-15 | 5 min | Sync doc count to 92; delete dead test block. |

Total fix budget: ~2.5h of focused work.
