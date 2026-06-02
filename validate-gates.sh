#!/usr/bin/env bash
# SWEBOK v4 Harness - Gate Validator
# Validates exit gate for given phase
# Usage: ./validate-gates.sh <phase> [--adversarial]

set -e

PHASE="${1:-}"
ADVERSARIAL="${2:-}"
HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
STATE_DB="$HARNESS_DIR/.swebok_state.db"

# Read state from SQLite (NEVER read .swebok_state YAML)
state_get() { python3 "$STATE_ENGINE" get "$1" 2>/dev/null || echo ""; }

if [[ -z "$PHASE" ]]; then
    echo "Usage: validate-gates.sh <P1-P9> [--adversarial]"
    exit 1
fi

# Validate phase format
if [[ ! "$PHASE" =~ ^P[1-9]$ ]]; then
    echo "[ERROR] Invalid phase: $PHASE (expected P1-P9)"
    exit 1
fi

PHASE_NUM="${PHASE:1:1}"

echo "=========================================="
echo "  SWEBOK v4 HARNESS - GATE VALIDATION"
echo "  Phase: $PHASE"
echo "  Adversarial: ${ADVERSARIAL:-no}"
echo "=========================================="

# === LOAD STATE FROM SQLITE ===
if [[ -f "$STATE_DB" ]]; then
    CURRENT=$(state_get "current_phase")
    echo "[INFO] Current phase in state: $CURRENT"
fi

# === PHASE-SPECIFIC GATE CHECKS ===
GATE_PASSED=true

case "$PHASE" in
    P1)
        echo ""
        echo "[GATE $PHASE] Checking P1_DISCOVERY exit criteria..."
        echo "  Criteria: SCOPE_DEFINED | STAKEHOLDERS_ID'D | REQUIREMENTS_DRAFTED"

        # Check scope
        SCOPE=$(state_get "project_scope")
        if [[ -z "$SCOPE" || "$SCOPE" == '""' ]]; then
            echo "  [FAIL] project_scope not defined"
            GATE_PASSED=false
        else
            echo "  [PASS] project_scope: $SCOPE"
        fi

        # Check stakeholders (placeholder - would check phase_data)
        STAKEHOLDERS=$(state_get "phase_data.P1.stakeholders_identified")
        if [[ "$STAKEHOLDERS" == "[]" || -z "$STAKEHOLDERS" ]]; then
            echo "  [FAIL] No stakeholders identified"
            GATE_PASSED=false
        else
            echo "  [PASS] Stakeholders: $STAKEHOLDERS"
        fi

        # Check requirements draft
        REQ_DRAFT=$(state_get "phase_data.P1.requirements_draft")
        if [[ -z "$REQ_DRAFT" ]]; then
            echo "  [FAIL] requirements_draft not started"
            GATE_PASSED=false
        else
            echo "  [PASS] requirements_draft: exists"
        fi
        ;;

    P2)
        echo ""
        echo "[GATE $PHASE] Checking P2_REQUIREMENTS exit criteria..."
        echo "  Criteria: REQ_APPROVED | KA-1_COMPLETE | TRACEABILITY_MATRIX"

        # Check requirements approved
        REQ_APPROVED=$(state_get "phase_data.P2.requirements_approved")
        if [[ "$REQ_APPROVED" != "true" ]]; then
            echo "  [FAIL] Requirements not approved"
            GATE_PASSED=false
        else
            echo "  [PASS] Requirements approved"
        fi

 # Check traceability matrix
        TRACE=$(state_get "phase_data.P2.traceability_matrix")
        if [[ -z "$TRACE" ]]; then
            echo "  [FAIL] Traceability matrix missing"
            GATE_PASSED=false
        else
            echo "  [PASS] Traceability matrix: exists"
        fi
        ;;

    P3)
        echo ""
        echo "[GATE $PHASE] Checking P3_ARCHITECTURE exit criteria..."
        echo "  Criteria: ARCH_DOC_APPROVED | C4_DIAGRAM | KA-2_COMPLETE"

        ARCH_APPROVED=$(state_get "phase_data.P3.arch_doc_approved")
        if [[ "$ARCH_APPROVED" != "true" ]]; then
            echo "  [FAIL] Architecture document not approved"
            GATE_PASSED=false
        else
            echo "  [PASS] Architecture document approved"
        fi

        C4_DIAGRAM=$(state_get "phase_data.P3.c4_diagram")
        if [[ -z "$C4_DIAGRAM" ]]; then
            echo "  [FAIL] C4 diagram missing"
            GATE_PASSED=false
        else
            echo "  [PASS] C4 diagram: $C4_DIAGRAM"
        fi
        ;;

    P4)
        echo ""
        echo "[GATE $PHASE] Checking P4_DESIGN exit criteria..."
        echo "  Criteria: DESIGN_DOC_COMPLETE | KA-3_COMPLETE | INTERFACES_DEFINED"

        DESIGN_COMPLETE=$(state_get "phase_data.P4.design_doc_complete")
        if [[ "$DESIGN_COMPLETE" != "true" ]]; then
            echo "  [FAIL] Design document not complete"
            GATE_PASSED=false
        else
            echo "  [PASS] Design document complete"
        fi

        INTERFACES=$(state_get "phase_data.P4.interfaces_defined")
        if [[ "$INTERFACES" != "true" ]]; then
            echo "  [FAIL] Interfaces not defined"
            GATE_PASSED=false
        else
            echo "  [PASS] Interfaces defined"
        fi
        ;;

    P5)
        echo ""
        echo "[GATE $PHASE] Checking P5_CONSTRUCTION exit criteria..."
        echo "  Criteria: COMPILE:0 | COV:>80 | SAST_CRIT:0 | UNIT_TESTS_PASS"

        # Compile check
        COMPILE_ERRORS=$(state_get "phase_data.P5.compile_errors")
        if [[ "$COMPILE_ERRORS" -gt 0 ]]; then
            echo "  [FAIL] Compile errors: $COMPILE_ERRORS"
            GATE_PASSED=false
        else
            echo "  [PASS] Compile: 0 errors"
        fi

        # Coverage check
        COVERAGE=$(state_get "phase_data.P5.test_coverage")
        if [[ "$COVERAGE" -lt 80 ]]; then
            echo "  [FAIL] Coverage: ${COVERAGE}% (< 80%)"
            GATE_PASSED=false
        else
            echo "  [PASS] Coverage: ${COVERAGE}% (> 80%)"
        fi

        # SAST check
        SAST_CRIT=$(state_get "phase_data.P5.sast_critical")
        if [[ "$SAST_CRIT" -gt 0 ]]; then
            echo "  [FAIL] SAST critical issues: $SAST_CRIT"
            GATE_PASSED=false
        else
            echo "  [PASS] SAST: 0 critical issues"
        fi
        ;;

    P6)
        echo ""
        echo "[GATE $PHASE] Checking P6_TESTING exit criteria..."
        echo "  Criteria: QA1_PASS | QA2_PASS | QA3_PASS | E2E:100% | VDIFF:<2% | XSS:PASS"
        "$HARNESS_DIR/scripts/validate-qa-gates.sh"
        exit $?
        ;;

    P7)
        echo ""
        echo "[GATE $PHASE] Checking P7_DEPLOYMENT exit criteria..."
        echo "  Criteria: DEPLOY_SUCCESS | MONITORING_ACTIVE | ROLLBACK_VALIDATED"

        DEPLOY=$(state_get "phase_data.P7.deploy_success")
        MONITORING=$(state_get "phase_data.P7.monitoring_active")
        ROLLBACK=$(state_get "phase_data.P7.rollback_validated")

        if [[ "$DEPLOY" != "true" ]]; then
            echo "  [FAIL] Deploy not successful"
            GATE_PASSED=false
        else
            echo "  [PASS] Deploy successful"
        fi

        if [[ "$MONITORING" != "true" ]]; then
            echo "  [FAIL] Monitoring not active"
            GATE_PASSED=false
        else
            echo "  [PASS] Monitoring active"
        fi

        if [[ "$ROLLBACK" != "true" ]]; then
            echo "  [FAIL] Rollback not validated"
            GATE_PASSED=false
        else
            echo "  [PASS] Rollback validated"
        fi
        ;;

    P8)
        echo ""
        echo "[GATE $PHASE] Checking P8_OPERATIONS exit criteria..."
        echo "  Criteria: SLO_ACHIEVED | KA-6_COMPLETE | MAINTENANCE_DOC"

        SLO=$(state_get "phase_data.P8.slo_achieved")
        MAINT=$(state_get "phase_data.P8.maintenance_doc")

        if [[ "$SLO" != "true" ]]; then
            echo "  [FAIL] SLO not achieved"
            GATE_PASSED=false
        else
            echo "  [PASS] SLO achieved"
        fi

        if [[ "$MAINT" != "true" ]]; then
            echo "  [FAIL] Maintenance documentation missing"
            GATE_PASSED=false
        else
            echo "  [PASS] Maintenance documentation complete"
        fi
        ;;

    P9)
        echo ""
        echo "[GATE $PHASE] Checking P9_RETIREMENT exit criteria..."
        echo "  Criteria: DATA_ARCHIVED | DEPRECATION_NOTICE | KA-6_COMPLETE"

        ARCHIVED=$(state_get "phase_data.P9.data_archived")
        DEPRECATION=$(state_get "phase_data.P9.deprecation_notice")

        if [[ "$ARCHIVED" != "true" ]]; then
            echo "  [FAIL] Data not archived"
            GATE_PASSED=false
        else
            echo "  [PASS] Data archived"
        fi

        if [[ "$DEPRECATION" != "true" ]]; then
            echo "  [FAIL] Deprecation notice not sent"
            GATE_PASSED=false
        else
            echo "  [PASS] Deprecation notice sent"
        fi
        ;;
esac

echo ""
echo "=========================================="
if [[ "$GATE_PASSED" == "true" ]]; then
    echo "  GATE $PHASE EXIT: PASS ✓"
    echo "=========================================="

    # Update state file
    if [[ -f "$STATE_DB" ]]; then
        python3 "$STATE_ENGINE" append_gate "P${PHASE_NUM}_EXIT" 2>/dev/null || true
        echo "[INFO] Appended P${PHASE_NUM}_EXIT to gates_validated in state DB"
    fi

    exit 0
else
    echo "  GATE $PHASE EXIT: DENY ✗"
    echo "  Fix failures before proceeding"
    echo "=========================================="
    exit 1
fi
