#!/usr/bin/env bash
# SWEBOK v4 Harness — pre-commit hook (distilled variant)
#
# Install by symlinking into your project's .git/hooks/:
#   ln -s $HARNESS_DIR/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# What it does (distilled repo, 2026-06-10):
#   1. Rebuilds the per-project state DB (cold start)
#   2. Verifies audit-log HMAC chain integrity
#   3. Runs the distilled test suite (32 tests) — fail commit on FAIL
#   4. Runs the v2 retrieval tests (20 tests) — fail commit on FAIL
#   5. Runs the adversarial test suite (8 tests) — fail commit on FAIL
#   6. Runs the adv-loop property tests (44 tests) — fail commit on FAIL
#   7. Runs the adv-loop self-tests (38 tests) — fail commit on FAIL
#   8. Runs the health tests (5 tests) — fail commit on FAIL
#   9. Runs the health-check script (exit 0/1 = ok, 2 = broken = FAIL)
#
# Total: 147 tests + HMAC chain + health probe. Real gate, not a no-op.

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
HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "$_RESOLVED")" && pwd)}"
if [[ ! -d "$HARNESS_DIR" ]]; then
    echo "[pre-commit] HARNESS_DIR=$HARNESS_DIR not found. Skipping."
    exit 0
fi

cd "$HARNESS_DIR"

# Sanity: this hook requires the actual test suite to exist.
# If tests/ is missing, fail closed (no longer a silent no-op).
if [[ ! -d "$HARNESS_DIR/tests" ]]; then
    echo "[pre-commit] FAIL: tests/ directory not found in $HARNESS_DIR"
    echo "This hook gates on real tests; an empty/missing test suite is a fail."
    exit 1
fi

echo "[pre-commit] Running SWEBOK v4 harness test gate (147 tests expected)..."

# 1. Cold rebuild + HMAC integrity
python3 lib/state_engine.py rebuild >/dev/null 2>&1
python3 lib/state_engine.py check_integrity > /tmp/swebok_precommit_integrity.log
if ! grep -q '^ok$' /tmp/swebok_precommit_integrity.log; then
    echo "[pre-commit] FAIL: state DB integrity not 'ok' after rebuild"
    cat /tmp/swebok_precommit_integrity.log
    exit 1
fi

# 2. HMAC chain on all 4 audit tables
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

# 3. Test suite runner — fails on any [FAIL] line
run_test_suite() {
    local name="$1" script="$2" logfile="/tmp/swebok_precommit_${name}.log"
    echo "[pre-commit]   → $name ($script)"
    if ! bash "$script" > "$logfile" 2>&1; then
        echo "[pre-commit] FAIL: $name exited non-zero"
        grep -E '^\[FAIL\]' "$logfile" | head -10
        exit 1
    fi
    local fail
    fail=$(grep -c '^\[FAIL\]' "$logfile" 2>/dev/null | tr -d '[:space:]' || echo 0)
    if [[ "$fail" -gt 0 ]]; then
        echo "[pre-commit] FAIL: $name reported $fail failures"
        grep -E '^\[FAIL\]' "$logfile" | head -10
        exit 1
    fi
}

# Run all test suites in the canonical order
run_test_suite "distilled"        "tests/distilled-test.sh"
run_test_suite "retrieval-v2"     "tests/retrieval/test-v2.sh"
run_test_suite "adversarial"      "tests/retrieval/test-adversarial.sh"
run_test_suite "adv-loop"         "bin/adv-loop test"
run_test_suite "adv-properties"   "tests/adv-loop/test-properties.sh"

# Health tests (Python) — run after the bash suites
if ! python3 tests/test_health.py > /tmp/swebok_precommit_health_py.log 2>&1; then
    echo "[pre-commit] FAIL: health tests exited non-zero"
    cat /tmp/swebok_precommit_health_py.log
    exit 1
fi

# 9. Health check — fail on BROKEN (exit 2). DEGRADED (exit 1) is a soft pass.
if bash "$HARNESS_DIR/scripts/health-check.sh" > /tmp/swebok_precommit_health.log 2>&1; then
    hc_exit=0
else
    hc_exit=$?
fi
if [[ "$hc_exit" -ge 2 ]]; then
    echo "[pre-commit] FAIL: health-check reported BROKEN (exit $hc_exit)"
    cat /tmp/swebok_precommit_health.log
    exit 1
fi
if [[ "$hc_exit" -eq 1 ]]; then
    echo "[pre-commit] WARN: health-check reported DEGRADED — continuing"
fi

echo "[pre-commit] OK: 147 tests + HMAC + health all green"
exit 0
