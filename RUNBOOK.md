# SWEBOK v4 Harness — Operator Runbook

> **For**: Operators on call when the harness misbehaves in a Claude Code
> session. If you're a user looking for "how do I use this", see
> `README.md` instead. This document is the "something is wrong, what
> now" guide.

---

## 1. Quick triage

Run the health check first — it covers the 7 most common failure modes:

```bash
bash health-check.sh
# Output: one of:
#   Status: HEALTHY    (all 7 probes OK; nothing to do)
#   Status: DEGRADED   (some probes warning; investigate but no immediate action)
#   Status: BROKEN     (exit 2; commit hooks will block)
```

If the health check reports DEGRADED or BROKEN, run the corresponding
section below. The output of `health-check.sh` includes probe names —
match them to the section titles here.

---

## 2. Common incidents

### 2.1 Audit chain broken (HMAC mismatch)

**Symptom**: `pre-commit-hook.sh` reports `FAIL: audit chain broken`,
naming a specific table and row.

**Diagnosis**:
```bash
# Identify the broken table and row
python3 lib/state_engine.py verify_audit_chain adversarial_log
python3 lib/state_engine.py verify_audit_chain log_events
python3 lib/state_engine.py verify_audit_chain state_events
python3 lib/state_engine.py verify_audit_chain circuit_breaker_events
```

**Resolution**:
1. **If you trust the chain as-is** (the row was added by a legitimate
   prune, not tampering): recompute the chain.
   ```bash
   python3 lib/state_engine.py recompute_audit_chain adversarial_log
   ```
   This rebuilds the HMAC chain from the first row forward.
2. **If you suspect tampering**: stop and inspect. The
   `.swebok_state.db` is append-only via SQL triggers (`BEFORE DELETE`
   and `BEFORE UPDATE` on all 4 audit tables — see
   `lib/state_engine_audit.py:271-290`). If a row is broken, either
   a buggy tool wrote a malformed `row_hmac`, or someone with the
   HMAC key edited the DB out-of-band. **Do not** delete the DB and
   start over — you lose the audit trail. **Do not** recompute the
   chain until you've ruled out tampering.

### 2.2 State DB corruption

**Symptom**: `python3 lib/state_engine.py check_integrity` returns
anything other than `ok`. The state DB is corrupt.

**Resolution**:
```bash
# Backup the corrupt DB for forensics
cp .swebok_state.db .swebok_state.db.evidence-$(date +%s)

# Rebuild from the audit chain (rebuilds the state table, preserves
# the 4 audit tables and the HMAC chain)
python3 lib/state_engine.py rebuild

# Verify
python3 lib/state_engine.py check_integrity
```

**WARNING**: `rebuild()` was the source of a CRITICAL data-loss bug
(d[0] vs d[1] PRAGMA table_info index) fixed in commit `7ba68c9`. The
bug is regression-tested by `tests/test_rebuild_restore.py` (5 tests
gated by pre-commit). If `rebuild` loses data, the regression test
suite will catch it on the next commit.

### 2.3 Circuit breaker tripped (3-strike lock)

**Symptom**: An operation is blocked with the message "circuit breaker
tripped, 3/3 blocks on this file".

**Diagnosis**:
```bash
python3 lib/state_engine.py get circuit_breaker
```

**Resolution**:
- **If the block is legitimate** (you tried a destructive command in
  the wrong phase): complete the current phase's deliverables and
  advance the phase. The circuit breaker resets on phase transition.
- **If the block is a false positive** (e.g. you need to run `rm -rf`
  on a test fixture in P8 maintenance): use the override.
  ```bash
  # Log the override (mandatory)
  python3 lib/state_engine.py set circuit_breaker.override_active true "removing test fixture per PR #1234"

  # Run your command
  rm -rf tests/fixtures/stale-data

  # Re-engage the harness
  python3 lib/state_engine.py set circuit_breaker.override_active false
  ```
  Every override is logged to `adversarial_log` with the reason you
  pass. The audit chain doesn't lie.

### 2.4 Phase stuck at the wrong value

**Symptom**: The harness thinks you're in P3 when you've actually
finished P5.

**Diagnosis**:
```bash
python3 lib/state_engine.py get current_phase
python3 lib/state_engine.py get gates_validated
```

**Resolution**:
```bash
# After completing the actual current-phase deliverables
python3 lib/state_engine.py set current_phase P5_CONSTRUCTION
python3 lib/state_engine.py set gates_validated '["P1", "P2", "P3", "P4"]'
```

Both writes are HMAC-chained to `state_events`, so the audit trail
records the manual override.

### 2.5 Phase-guard blocking legitimate work

**Symptom**: `[PHASE-GUARD] BLOCKED: Writing .py files is not allowed
in P2_REQUIREMENTS` — but you're actually in P5.

**Diagnosis**: The harness's `current_phase` is stale (often because
the user has been working across multiple Claude Code sessions and
the phase was set in a previous one).

**Resolution**: see section 2.4.

### 2.6 Bash-guard blocking a safe command

**Symptom**: `[BASH-GUARD] BLOCKED: rm -rf` — but you have a legitimate
reason to run it.

**Resolution**: prefix with `HARNESS_BYPASS=1` to log the bypass
without blocking, or override the circuit breaker (see 2.3) and
run the command. Both paths audit-log the bypass.

### 2.7 Adversarial gate producing a fixture verdict

**Symptom**: `adversarial-gate.sh P5 P6` returns `GATE:PASS` but
nothing happened.

**Diagnosis**: You're running the **fixture mode** (default), which
returns canned DSL strings for development. The fixture is explicitly
labeled as not a real review (see `adversarial-gate.sh` lines 6–23
and the Fixture Disclosure in `README.md`).

**Resolution**:
- **Smoke test**: keep using fixture mode.
- **Production verdict**: use `--council` for the 4-LLM-judge path,
  or `--judge-only --red "..." --blue "..."` with real agent output.

---

## 3. Diagnostic commands

```bash
# Export everything for incident forensics
python3 lib/state_engine.py export_state > incident-$(date +%s).json
python3 lib/state_state_engine.py export_audit > incident-audit-$(date +%s).json

# Replay a time range
python3 lib/state_engine.py replay_session 2026-06-01 2026-06-02

# Self-audit (markdown report)
python3 lib/state_engine.py self_audit --council
```

---

## 4. Recovery procedures

### 4.1 Full uninstall + reinstall

If the harness is in a completely broken state, the nuclear option:

```bash
# 1. Back up everything (mandatory before destructive ops)
cp -r .swebok_state.db* .swebok_state.db.bak-$(date +%s)/

# 2. Uninstall (see UNINSTALL.md)
bash <(grep -A100 "## Step 1" UNINSTALL.md)

# 3. Reinstall
bash install-harness.sh

# 4. Restore your project's phase (if you had one)
python3 lib/state_engine.py set current_phase P5_CONSTRUCTION
```

### 4.2 Reset to a known-good state

If a specific operation is wedged but the harness is otherwise healthy:

```bash
# Reset the circuit breaker (does NOT delete audit history)
python3 lib/state_engine.py set circuit_breaker '{"blocked_attempts":0,"override_active":false}'

# Re-initialize the state DB (DESTRUCTIVE — only if you have backups)
python3 lib/state_engine.py rebuild --no-audit
```

---

## 5. Reporting issues

When filing a bug, capture:

```bash
# Health check output
bash health-check.sh

# Audit chain status
python3 lib/state_engine.py verify_audit_chain adversarial_log
python3 lib/state_engine.py verify_audit_chain log_events
python3 lib/state_engine.py verify_audit_chain state_events
python3 lib/state_engine.py verify_audit_chain circuit_breaker_events

# State DB info
ls -la .swebok_state.db*
stat -c '%a %n' .audit_key

# Harness version
git rev-parse HEAD
git describe --tags --always
```

File issues at https://github.com/doz34/swebok-v4-harness-distilled/issues
with the `incident` label. **Do not** post the HMAC key or any
`.audit_key` content — it's mode 0600 for a reason.

---

## 6. When in doubt

1. **Read** the message — phase-guard and bash-guard give you the reason
   and the action to take.
2. **Check** `health-check.sh` first.
3. **Search** `CHANGELOG.md` for the version you upgraded from.
4. **Run** the pre-commit gate locally: `bash pre-commit-hook.sh` —
   if it passes, the harness is in a known-good state.
