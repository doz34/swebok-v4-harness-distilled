#!/usr/bin/env bash
# SWEBOK v4 Harness — Health Check
#
# AUDIT-2026-06-01 ITER6 (DevOps S blocker): operator-friendly readiness probe.
# Usage:
#   bash scripts/health-check.sh                    # check this project's state
#   HARNESS_DIR=/path/to/harness bash health-check.sh
# Exit 0 = healthy. Exit 1 = degraded. Exit 2 = broken.

set -euo pipefail

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
STATE_ENGINE="$HARNESS_DIR/lib/state_engine.py"

if [[ ! -d "$HARNESS_DIR" ]] || [[ ! -f "$STATE_ENGINE" ]]; then
    echo "BROKEN: HARNESS_DIR=$HARNESS_DIR invalid"
    exit 2
fi

declare -A status

# 1. State DB integrity
integrity=$(python3 "$STATE_ENGINE" check_integrity 2>&1 || echo "error")
if [[ "$integrity" == "ok" ]]; then
    status[integrity]="OK"
else
    status[integrity]="FAIL: $integrity"
fi

# 2. Current phase set
phase=$(python3 "$STATE_ENGINE" get current_phase 2>/dev/null)
if [[ -n "$phase" ]]; then
    status[phase]="OK ($phase)"
else
    status[phase]="DEGRADED (phase unset)"
fi

# 3. Audit chain intact (4 tables)
if python3 "$STATE_ENGINE" verify_audit_chain >/tmp/_swebok_health_chain.log 2>&1; then
    status[chain]="OK (all 4 tables intact)"
else
    status[chain]="FAIL: $(cat /tmp/_swebok_health_chain.log | head -1)"
fi

# 4. Hook latency probe (single phase-guard call)
hook_t_start=$(date +%s%N)
bash "$HARNESS_DIR/pre-tool-use/phase-guard.sh" < /dev/null >/dev/null 2>&1 || true
hook_t_end=$(date +%s%N)
hook_ms=$(( (hook_t_end - hook_t_start) / 1000000 ))
if [[ "$hook_ms" -le 500 ]]; then
    status[latency]="OK (${hook_ms}ms)"
elif [[ "$hook_ms" -le 3000 ]]; then
    status[latency]="DEGRADED (${hook_ms}ms — cold-start expected; warm-up reduces to <100ms)"
else
    status[latency]="FAIL (${hook_ms}ms)"
fi

# 5. Backups present (R2 invariant: 3 most recent)
backup_count=$(find "$HARNESS_DIR" -maxdepth 1 -name '.swebok_state.db.bak.*' 2>/dev/null | wc -l)
if [[ "$backup_count" -le 3 ]]; then
    status[backups]="OK ($backup_count snapshots, ≤3 invariant)"
else
    status[backups]="DEGRADED ($backup_count snapshots, expected ≤3)"
fi

# 6. .audit_key permissions
if [[ -f "$HARNESS_DIR/.audit_key" ]]; then
    mode=$(stat -c %a "$HARNESS_DIR/.audit_key" 2>/dev/null || stat -f %p "$HARNESS_DIR/.audit_key" 2>/dev/null | sed 's/^.*\(...\)$/\1/')
    if [[ "$mode" == "600" ]]; then
        status[audit_key]="OK (mode 0600)"
    else
        status[audit_key]="FAIL: mode=$mode (expected 0600)"
    fi
else
    status[audit_key]="DEGRADED (no .audit_key yet — created on first audit log)"
fi

# 7. Hooks wired
if [[ -f "$HARNESS_DIR/settings.json" ]]; then
    wired=$(jq -r '(.hooks.PreToolUse // [] | length) + (.hooks.PostToolUse // [] | length)' "$HARNESS_DIR/settings.json" 2>/dev/null || echo 0)
    if [[ "$wired" -ge 4 ]]; then
        status[hooks]="OK ($wired hook entries)"
    else
        status[hooks]="DEGRADED ($wired hook entries)"
    fi
else
    status[hooks]="DEGRADED (settings.json missing)"
fi

# Summary
echo "==== SWEBOK v4 Harness Health Check ===="
fail=0 degraded=0
for k in integrity phase chain latency backups audit_key hooks; do
    v="${status[$k]}"
    echo "  $k: $v"
    case "$v" in
        FAIL*) fail=$((fail+1)) ;;
        DEGRADED*) degraded=$((degraded+1)) ;;
    esac
done
echo
if [[ "$fail" -gt 0 ]]; then
    echo "Status: BROKEN ($fail failed, $degraded degraded)"
    exit 2
elif [[ "$degraded" -gt 0 ]]; then
    echo "Status: DEGRADED ($degraded degraded)"
    exit 1
else
    echo "Status: HEALTHY"
    exit 0
fi
