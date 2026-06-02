# Operations Runbook — SWEBOK v4 Harness

Procedures for SREs and on-call engineers. Read this first when something breaks.

## 1. Symptom: Claude Code feels frozen / unresponsive

The phase-guard hook can take ~3ms p99 steady-state (cold-start first-call ~430ms; documented in TEST_STABILITY.md) on a Write/Edit tool call (Python startup + WAL SQLite read). This is expected on cold DB / first call of a session.

**Check**: `time bash hooks/pre-tool-use/phase-guard.sh < /dev/null` should return in <100ms.

If a hook is hung > 30s:
```bash
ps -ef | grep -E "phase-guard|state_engine|bash_scanner"
```
Kill the runaway Python (`kill <PID>`) and check `.swebok_state.db-wal` size:
```bash
ls -la <HARNESS_DIR>/.swebok_state.db-wal
```
If > 64 MiB the journal_size_limit got bypassed somehow — proceed to "Recover from WAL bloat" below.

## 2. Symptom: state DB is corrupt

Error: `sqlite3.DatabaseError: database disk image is malformed`

**Fix**:
```bash
python3 <HARNESS_DIR>/scripts/lib/state_engine.py rebuild
```

This renames the corrupt DB to `.swebok_state.db.corrupt.<ts>` for forensics, re-initializes a fresh DB with default state, and copies the audit tables forward from a pre-rebuild snapshot.

**Verify**:
```bash
python3 <HARNESS_DIR>/scripts/lib/state_engine.py check_integrity
# expected: ok
python3 <HARNESS_DIR>/scripts/lib/state_engine.py get current_phase
# expected: P5_CONSTRUCTION (or your last-known phase if audit restore worked)
```

If `check_integrity` still fails, you have catastrophic corruption. See "Restore from .bak" below.

## 3. Symptom: hook always reports BLOCKED, even on legitimate actions

Likely cause: a previous block tripped the circuit breaker to ≥3 attempts.

**Check**:
```bash
python3 <HARNESS_DIR>/scripts/lib/state_engine.py get circuit_breaker
# JSON object; look at blocked_attempts
```

If `blocked_attempts >= 3`, the harness is now HARD-LOCKED on that file (fail-secure, post-2026-06-01 CRIT-1 fix). To unlock:
```bash
# Operator override — explicitly authorized unblock for 5 minutes:
python3 <HARNESS_DIR>/scripts/lib/state_engine.py set circuit_breaker.override_active true
python3 <HARNESS_DIR>/scripts/lib/state_engine.py set circuit_breaker.override_timestamp "$(date +%s)"

# Or reset entirely:
python3 <HARNESS_DIR>/scripts/lib/state_engine.py reset_all_circuits
```

## 4. Restore from .bak

State DB backups exist at `<HARNESS_DIR>/.swebok_state.db.bak.<ts>`. By default the 3 most recent are kept (R2 invariant).

```bash
# List backups
ls -lt <HARNESS_DIR>/.swebok_state.db.bak.* | head -3

# Stop any running Claude Code session first (so the DB isn't being read)
pkill -f "claude" 2>/dev/null

# Replace
cp <HARNESS_DIR>/.swebok_state.db.bak.<ts> <HARNESS_DIR>/.swebok_state.db
# Wipe WAL/SHM sidecars so SQLite re-creates them clean from the restored .db
rm -f <HARNESS_DIR>/.swebok_state.db-wal <HARNESS_DIR>/.swebok_state.db-shm

# Verify
python3 <HARNESS_DIR>/scripts/lib/state_engine.py check_integrity
```

## 5. Recover from WAL bloat

If `.swebok_state.db-wal` grows past 64 MiB despite `journal_size_limit`, force a TRUNCATE checkpoint:

```bash
python3 -c "
import sqlite3
c = sqlite3.connect('<HARNESS_DIR>/.swebok_state.db', timeout=10.0)
c.execute('PRAGMA wal_checkpoint(TRUNCATE)')
c.close()
"
```

## 6. Tail the audit log

```bash
# Latest 20 log_events
python3 <HARNESS_DIR>/scripts/lib/state_engine.py query_log_events 20

# State transitions in the last hour
python3 <HARNESS_DIR>/scripts/lib/state_engine.py query_state_events 100 "" "$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S)"

# Circuit-breaker events
python3 <HARNESS_DIR>/scripts/lib/state_engine.py query_circuit_breaker_events 50

# Adversarial gate verdicts
python3 <HARNESS_DIR>/scripts/lib/state_engine.py query_adversarial 50

# Full export (JSON, both state and audit)
python3 <HARNESS_DIR>/scripts/lib/state_engine.py export_audit | jq .
```

## 7. Pre-mortem inspection (post-incident replay)

```bash
T0="2026-06-01T10:00:00"
T1="2026-06-01T11:00:00"
python3 -c "
import sys
sys.path.insert(0, '<HARNESS_DIR>/scripts/lib')
import state_engine
for row in state_engine.replay_session('$T0', '$T1'):
    print(row)
"
```

## 8. Health check (CI / cron)

```bash
#!/bin/bash
# health-check.sh — run from cron every 5 min
set -e
cd <HARNESS_DIR>
status=$(python3 scripts/lib/state_engine.py check_integrity)
if [[ "$status" != "ok" ]]; then
    echo "ALERT: state DB integrity_check failed: $status"
    exit 1
fi
phase=$(python3 scripts/lib/state_engine.py get current_phase)
if [[ -z "$phase" ]]; then
    echo "ALERT: state DB has empty current_phase"
    exit 1
fi
echo "OK: phase=$phase integrity=ok"
```

## 9. Uninstall

See [UNINSTALL.md](UNINSTALL.md).

## 10. Escalation contacts

- Security issues: see [SECURITY.md](SECURITY.md) for the disclosure process
- Concurrency races / atomicity bugs: see [docs/v1/TEST_STABILITY.md](docs/v1/TEST_STABILITY.md) for known surface
- Threat model questions: see [docs/v1/THREAT_MODEL.md](docs/v1/THREAT_MODEL.md)

## 11. Health-check (one-shot) & metrics

```bash
# Run all 7 readiness probes
bash scripts/health-check.sh
# exit 0 = HEALTHY, 1 = DEGRADED, 2 = BROKEN

# Cheap live metrics view (phase, tool_call_count, circuit breaker, table sizes)
python3 scripts/lib/state_engine.py metrics

# Verify HMAC audit chain
python3 scripts/lib/state_engine.py verify_audit_chain
# exit 0 = intact, 1 = chain BROKEN at row N

# Re-attach the chain after a legitimate prune that removed earlier rows
python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts/lib')
import state_engine
for t in ('adversarial_log','log_events','state_events','circuit_breaker_events'):
    print(t, state_engine.recompute_audit_chain(t))
"
```

## 12. Opt-in council bridge (ADR-003 / G.3)

The harness ships with a 4-role council bridge that closes the original
2026-06-01 CRIT-2 (gate fixture). The bridge is **opt-in** — the default
`adversarial-gate.sh` path stays fixture-based so unit tests, CI, and local
development remain deterministic.

### Enable

```bash
export MULTIAGENT_BRIDGE_ENABLED=1
```

The installer writes `MULTIAGENT_BRIDGE_ENABLED=0` (default off) into
`.claude/settings.json` env block. Override with `export` in the active shell.

### Invoke

```bash
bash "$HARNESS_DIR/scripts/adversarial-gate.sh" --council <from> <to>
# e.g. for P5 → P6 transition
bash "$HARNESS_DIR/scripts/adversarial-gate.sh" --council P5 P6
```

### What happens

1. The gate validates `<from>` and `<to>` against `^P[0-9]+$` and exits 1 on
   non-conforming input (CISO INJ-1 mitigation).
2. If `MULTIAGENT_BRIDGE_ENABLED` is unset, the gate writes a `WARN:` to
   STDERR and continues (cost guard against accidental ~200k-token spawns).
3. The gate delegates to `multiagent-launcher.sh emit-envelope` (the SINGLE
   OWNER of the bridge envelope per CLAUDE.md L6 / L6.1).
4. STDOUT receives a single well-formed envelope:
   ```
   <MULTIAGENT_LAUNCH gate="<from>_EXIT" target="<to>">
   {"role": "ciso", "subagent_type": "nexus-ciso", "prompt": "...", ...}
   {"role": "qa-lead", "subagent_type": "nexus-qa-lead", "prompt": "...", ...}
   {"role": "architect", "subagent_type": "nexus-architect", "prompt": "...", ...}
   {"role": "devops-lead", "subagent_type": "nexus-devops-lead", "prompt": "...", ...}
   </MULTIAGENT_LAUNCH>
   ```
5. The gate exits **99** (signal: "please spawn the agents and re-invoke
   with `--judge-only`"). A `COUNCIL_REQUEST` row is written to
   `adversarial_log` (HMAC chained) before exit.
6. The dispatcher (Claude Code) reads each JSONL line, invokes the
   `Agent` tool with the line's `subagent_type` and `prompt`, and
   collects each agent's single DSL output.
7. The dispatcher aggregates (RED: worst-severity wins; BLUE: any FAIL → FAIL)
   and re-invokes:
   ```bash
   bash "$HARNESS_DIR/scripts/adversarial-gate.sh" <from> <to> \
       --judge-only \
       --red "<aggregated RED DSL>" \
       --blue "<aggregated BLUE DSL>"
   ```

### What it costs

- Single gate transition: ~40k output tokens (4 reviewers × ~10k each).
- Full SDLC run (5 transitions): ~200k output tokens.
- For comparison, the harness's D→S journey consumed ~18M tokens.

### What if the env var is unset?

The gate still emits the envelope but writes:
```
[GATE] WARN: --council requested but MULTIAGENT_BRIDGE_ENABLED is not set;
[GATE]       emitting envelope anyway. Set the env var before re-invoking
[GATE]       with --judge-only to ensure the dispatcher honours the spawn.
```

This is intentional (cost guard): the dispatcher can still parse the
envelope and decide to spawn agents even without the env var.

### What if the launcher's stderr is needed for debugging?

The gate captures the launcher's stderr to
`$TEMP_DIR/council_stderr.<pid>.log` and surfaces it on gate failure
(non-zero launcher exit, empty envelope, malformed envelope). Best-effort
cleanup deletes the log on successful exit.

### Rollback

PR-B is a 5-file revert (see `ADR-003-multiagent-bridge.md` §"Rollback path"):
- `scripts/adversarial-gate.sh`
- `scripts/multiagent-launcher.sh`
- `tests/adversarial-test.sh` (Tests 97-100)
- `docs/v1/THREAT_MODEL.md` A6 row
- This OPERATIONS.md §12

No SQL migration, no schema change. The fixture path resumes immediately.
