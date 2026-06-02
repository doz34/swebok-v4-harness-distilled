#!/usr/bin/env bash
# SWEBOK v4 Harness - QA Gates Validator (P6)
# Validates all P6_EXIT criteria
# Usage: ./validate-qa-gates.sh

set -e

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
# Read state from SQLite (NEVER read .swebok_state YAML)
state_get() { python3 "$STATE_ENGINE" get "$1" 2>/dev/null || echo ""; }

echo "=========================================="
echo "  QA GATES VALIDATION (P6_TESTING)"
echo "=========================================="

GATES_MET=true

# === 1. Unit Coverage >80% ===
echo ""
echo "[QA-1] Static& Unit Shield"
echo "  Checking: unit_coverage > 80%"

if command -v pytest &>/dev/null; then
    COV_OUTPUT=$(pytest --cov=src --cov-report=term 2>/dev/null | grep "TOTAL" | tail -1 || echo "")
    COV_PERCENT=$(echo "$COV_OUTPUT" | grep -oP '\d+%' | tail -1 | tr -d '%' || echo "0")

    if [[ "$COV_PERCENT" -lt 80 ]]; then
        echo "  [FAIL] unit_coverage: ${COV_PERCENT}% (< 80%)"
        GATES_MET=false
    else
        echo "  [PASS] unit_coverage: ${COV_PERCENT}% (> 80%)"
    fi
elif command -v jest&>/dev/null; then
    COV_OUTPUT=$(jest --coverage --coverageReporters=text-summary 2>/dev/null | grep "All files" | tail -1 || echo "")
    COV_PERCENT=$(echo "$COV_OUTPUT" | grep -oP '\d+%' | tail -1 | tr -d '%' || echo "0")

    if [[ "$COV_PERCENT" -lt 80 ]]; then
        echo "  [FAIL] unit_coverage: ${COV_PERCENT}% (< 80%)"
        GATES_MET=false
    else
        echo "  [PASS] unit_coverage: ${COV_PERCENT}% (> 80%)"
    fi
else
    echo "  [SKIP] No test coverage tool found (pytest/jest)"
    # Check state file as fallback
    COV=$(state_get "phase_data.P6.qa1_pass")
    if [[ "$COV" == "true" ]]; then
        echo "  [PASS] unit_coverage: (state file verified)"
    else
        echo "  [WARN] unit_coverage: not verified"
    fi
fi

# === 2. Static Analysis 0 CRITICAL ===
echo ""
echo "  Checking: static_analysis = 0 CRITICAL"

if command -v ruff&>/dev/null; then
    CRIT_COUNT=$(ruff check src/ 2>/dev/null | grep -cE "CRIT|FATAL" || echo "0")
    if [[ "$CRIT_COUNT" -gt 0 ]]; then
        echo "  [FAIL] static_analysis: $CRIT_COUNT critical issues"
        GATES_MET=false
    else
        echo "  [PASS] static_analysis: 0 critical"
    fi
elif command -v eslint&>/dev/null; then
    CRIT_COUNT=$(npx eslint src/ 2>/dev/null | grep -cE "error" || echo "0")
    if [[ "$CRIT_COUNT" -gt 0 ]]; then
        echo "  [FAIL] static_analysis: $CRIT_COUNT errors"
        GATES_MET=false
    else
        echo "  [PASS] static_analysis: 0 errors"
    fi
else
    echo "  [SKIP] No SAST tool found (ruff/eslint)"
fi

# ===3. E2E Critical Paths 100% ===
echo ""
echo "[QA-2] Visual & Behavioral E2E"
echo "  Checking: e2e_critical_paths = 100%"

E2E_PASS=$(state_get "phase_data.P6.e2e_pass")
if [[ "$E2E_PASS" != "true" ]]; then
    echo "  [FAIL] e2e_critical_paths: not100%"
    GATES_MET=false
else
    echo "  [PASS] e2e_critical_paths: 100%"
fi

# === 4. Visual Diff <2% ===
echo ""
echo "  Checking: visual_diff < 2%"

VDIFF=$(state_get "phase_data.P6.visual_diff")
if [[ "$VDIFF" -gt 2 ]]; then
    echo "  [FAIL] visual_diff: ${VDIFF}% (> 2%)"
    GATES_MET=false
else
    echo "  [PASS] visual_diff: ${VDIFF}% (< 2%)"
fi

# === 5. Security XSS PASS ===
echo ""
echo "[QA-3] Adversarial Council"
echo "  Checking: security_xss = PASS"

XSS_PASS=$(state_get "phase_data.P6.xss_pass")
if [[ "$XSS_PASS" != "true" ]]; then
    echo "  [FAIL] security_xss: not PASS"
    GATES_MET=false
else
    echo "  [PASS] security_xss: PASS"
fi

# === QA-1/QA-2/QA-3 sub-gates ===
echo ""
echo "  Checking: QA sub-gates"

QA1=$(state_get "phase_data.P6.qa1_pass")
QA2=$(state_get "phase_data.P6.qa2_pass")
QA3=$(state_get "phase_data.P6.qa3_pass")

if [[ "$QA1" != "true" ]]; then
    echo "  [FAIL] QA1 (Static & Unit Shield): not passed"
    GATES_MET=false
else
    echo "  [PASS] QA1: passed"
fi

if [[ "$QA2" != "true" ]]; then
    echo "  [FAIL] QA2 (Browser Use E2E): not passed"
    GATES_MET=false
else
    echo "  [PASS] QA2: passed"
fi

if [[ "$QA3" != "true" ]]; then
    echo "  [FAIL] QA3 (Adversarial Council): not passed"
    GATES_MET=false
else
    echo "  [PASS] QA3: passed"
fi

# === FINAL RESULT ===
echo ""
echo "=========================================="
if [[ "$GATES_MET" == "true" ]]; then
    echo "  P6_EXIT GATE: ALL PASS ✓"
    echo "=========================================="
    exit 0
else
    echo "  P6_EXIT GATE: FAILURES FOUND ✗"
    echo "  Fix all failures before P6→P7 transition"
    echo "=========================================="
    exit 1
fi
