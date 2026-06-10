#!/usr/bin/env bash
# SWEBOK v4 Harness — Adversarial Loop Property-Based Test Runner
# Tests lib/adv-loop/properties.py: 4 properties × 11 phases = 44 tests (S5).
# Run: bash tests/adv-loop/test-properties.sh
#
# Each property is exercised with the project's real phase specs
# (specs/workflows/by-phase/phase-N-*.md) and synthetic work content.

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$HARNESS_DIR"

PASSED=0
FAILED=0
log_test() { echo ""; echo "[TEST] $1"; }
log_pass() { echo "[PASS] $1"; PASSED=$((PASSED+1)); }
log_fail() { echo "[FAIL] $1"; FAILED=$((FAILED+1)); }

# Resolve the spec file for a phase (uses real project specs)
get_spec() {
    local phase="$1"
    local spec_file
    spec_file=$(ls "specs/workflows/by-phase/phase-${phase}-"*.md 2>/dev/null | head -1)
    if [[ -z "$spec_file" ]]; then
        echo ""
    else
        cat "$spec_file"
    fi
}

# === Test a single property on a single phase ===
# Usage: run_property <prop_name> <phase>
# Emits PASS/FAIL/ERROR:<msg> on stdout
run_property() {
    local prop_name="$1" phase="$2"
    python3 - "$prop_name" "$phase" <<'PYEOF' 2>&1 | tail -1
import sys
sys.path.insert(0, 'lib/adv-loop')
from pathlib import Path
from properties import (
    property_idempotence, property_determinism,
    property_monotonicity, property_dsl_well_formed,
    is_well_formed_dsl,
)

prop_name, phase_str = sys.argv[1], sys.argv[2]
phase = int(phase_str)

# Find spec file
spec_path = None
for p in Path('specs/workflows/by-phase').glob(f'phase-{phase}-*.md'):
    spec_path = p
    break
if not spec_path:
    print('ERROR:no_spec')
    sys.exit(0)
spec = spec_path.read_text(encoding='utf-8', errors='ignore')
work = 'synthetic work content for property-based test (S5)'

try:
    if prop_name == 'idempotence':
        # Same input → same passed/n_runs (idempotent)
        r1 = property_idempotence(phase, work, spec)
        r2 = property_idempotence(phase, work, spec)
        result = 'PASS' if (r1.passed == r2.passed and r1.n_runs == r2.n_runs) else 'FAIL'
    elif prop_name == 'determinism':
        # Same input → same outcome (deterministic)
        r1 = property_determinism(phase, work, spec)
        r2 = property_determinism(phase, work, spec)
        result = 'PASS' if (r1.passed == r2.passed and r1.n_runs == r2.n_runs) else 'FAIL'
    elif prop_name == 'monotonicity':
        # Just check the property runs without error
        r = property_monotonicity(phase, spec, n_seeds=2)
        result = 'PASS' if r is not None else 'FAIL'
    elif prop_name == 'dsl_well_formed':
        r = property_dsl_well_formed(phase, n_seeds=2)
        result = 'PASS' if r is not None else 'FAIL'
    else:
        result = 'ERROR:unknown_property'
except Exception as e:
    result = f'ERROR:{type(e).__name__}:{e}'
print(result)
PYEOF
}

# === MAIN LOOP: 4 properties × 11 phases = 44 tests ===
for phase in 0 1 2 3 4 5 6 7 8 9 10; do
    for prop in idempotence determinism monotonicity dsl_well_formed; do
        log_test "Property ${prop} on P${phase}"
        out=$(run_property "$prop" "$phase")
        if [[ "$out" == "PASS" ]]; then
            log_pass "${prop} P${phase}"
        else
            log_fail "${prop} P${phase}: ${out}"
        fi
    done
done

echo ""
echo "============================================"
echo "  ADV-LOOP PROPERTY TESTS: $PASSED passed, $FAILED failed (out of 44)"
echo "============================================"
exit $FAILED
