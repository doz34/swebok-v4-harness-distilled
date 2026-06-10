#!/usr/bin/env bash
# SWEBOK v4 Harness — pre-commit hook
#
# AUDIT-2026-06-01 (QA S blocker): pre-commit gate.
#
# Install by symlinking into your project's .git/hooks/:
#   ln -s $HARNESS_DIR/scripts/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# What it does:
#   1. Rebuilds the per-project state DB (cold start)
#   2. Runs the warm-up test pass (ignores failures)
#   3. Runs the authoritative test pass — fail commit on FAIL
#   4. Verifies audit-log HMAC chain integrity
#   5. Runs STRIDE-lite

set -euo pipefail

# Resolve symlink (BASH_SOURCE gives the symlink path, not the target).
# Without this, when invoked via .git/hooks/pre-commit → ../../pre-commit-hook.sh,
# the relative cd lands inside .git/ rather than the project root.
_HOOK_PATH="${BASH_SOURCE[0]}"
if command -v readlink >/dev/null 2>&1; then
    _RESOLVED=$(readlink -f "$_HOOK_PATH" 2>/dev/null || echo "$_HOOK_PATH")
else
    _RESOLVED="$_HOOK_PATH"
fi
# pre-commit-hook.sh lives at the project root, so dirname is enough.
HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "$_RESOLVED")" && pwd)}"
if [[ ! -d "$HARNESS_DIR" ]]; then
    echo "[pre-commit] HARNESS_DIR=$HARNESS_DIR not found. Skipping."
    exit 0
fi

cd "$HARNESS_DIR"

# Fork detection: this hook was designed for the upstream harness
# (/home/doz/swebok-v4-harness/) which has tests/adversarial-test.sh and
# tests/attack-payloads-test.sh at the root. Forks (e.g. -distilled) do not
# have these scripts, so the gate would always fail. Skip cleanly.
if [[ ! -f "$HARNESS_DIR/tests/adversarial-test.sh" ]]; then
    echo "[pre-commit] SKIP: upstream-only test suite not present in fork. Skipping."
    exit 0
fi

echo "[pre-commit] Running SWEBOK v4 harness test gate..."

# 1. Cold rebuild
python3 lib/state_engine.py rebuild >/dev/null 2>&1
python3 lib/state_engine.py check_integrity > /tmp/swebok_precommit_integrity.log
if ! grep -q '^ok$' /tmp/swebok_precommit_integrity.log; then
    echo "[pre-commit] FAIL: state DB integrity not 'ok' after rebuild"
    cat /tmp/swebok_precommit_integrity.log
    exit 1
fi

# 2. Warm-up
bash tests/adversarial-test.sh >/dev/null 2>&1 || true

# 3. Authoritative
if ! bash tests/adversarial-test.sh > /tmp/swebok_precommit_tests.log 2>&1; then
    echo "[pre-commit] FAIL: adversarial-test.sh exited non-zero"
    grep '^\[FAIL\]' /tmp/swebok_precommit_tests.log
    exit 1
fi
fail=$( { grep -c '^\[FAIL\]' /tmp/swebok_precommit_tests.log 2>/dev/null || true; } | tr -d '[:space:]')
fail="${fail:-0}"
if [[ "$fail" -gt 0 ]]; then
    echo "[pre-commit] FAIL: $fail tests failed"
    grep '^\[FAIL\]' /tmp/swebok_precommit_tests.log
    exit 1
fi

# 4. HMAC chain
if ! python3 -c "
import sys
sys.path.insert(0, '$HARNESS_DIR/lib')
import state_engine
for tbl in ('adversarial_log', 'log_events', 'state_events', 'circuit_breaker_events'):
    ok, broken_at = state_engine.verify_audit_chain(tbl)
    if not ok:
        print(f'CHAIN BROKEN: {tbl} at row {broken_at}')
        sys.exit(1)
"; then
    echo "[pre-commit] FAIL: audit chain broken"
    exit 1
fi

# 5. STRIDE-lite
if ! bash tests/attack-payloads-test.sh > /tmp/swebok_precommit_attacks.log 2>&1; then
    echo "[pre-commit] FAIL: attack-payloads-test.sh exited non-zero"
    grep -E '^\[(FAIL|PASS)\]' /tmp/swebok_precommit_attacks.log | tail -10
    exit 1
fi

# 6. Health check — fail on BROKEN (exit 2). DEGRADED (exit 1) is a soft pass.
if ! bash "$HARNESS_DIR/scripts/health-check.sh" > /tmp/swebok_precommit_health.log 2>&1; then
    hc_exit=$?
    if [[ "$hc_exit" -ge 2 ]]; then
        echo "[pre-commit] FAIL: health-check reported BROKEN (exit $hc_exit)"
        cat /tmp/swebok_precommit_health.log
        exit 1
    fi
    echo "[pre-commit] WARN: health-check reported DEGRADED — continuing"
fi

echo "[pre-commit] OK: tests + HMAC + STRIDE + health all green"
exit 0
