#!/usr/bin/env bash
# SWEBOK v4 Harness - Adversarial Gate with DSL Strict Parser
# Red/Blue/Judge with strict DSL parsing (no natural language to Judge)
#
# ============================================================================
# AUDIT-2026-06-01 HONESTY NOTICE (CRIT-2):
#
# This script is a FIXTURE-with-real-Judge-path, not an end-to-end Red/Blue
# gate. The default RED_ACTUAL and BLUE_ACTUAL strings are HARDCODED per
# phase (later in this file). The <MULTIAGENT_LAUNCH> XML tag this script
# emits is NOT followed by any code in the harness — the dispatcher (Claude)
# is expected to spawn nexus-attacker/nexus-defender via the Agent tool,
# parse their real DSL output, and call this script with --judge-only to
# compute the final verdict from the real output.
#
# When invoked WITHOUT --judge-only and --red/--blue, this script returns
# the canned fixture output. That is intentional for development and unit
# tests, but MUST NOT be used as evidence of a real Red/Blue review.
#
# To rename this to ".../adversarial-gate-fixture.sh" requires updating
# every script and doc that references the path. This banner is the
# contract: callers MUST drive the real multiagent path before relying
# on a GATE:PASS verdict in production.
# ============================================================================
# Usage:
#   ./adversarial-gate.sh <from_phase> <to_phase>
#   ./adversarial-gate.sh <from_phase> <to_phase> --judge-only --red "RED: VULN:CRIT;;..." --blue "BLUE: DEFENDED;;..."

set -euo pipefail

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
DSL_ENGINE="$HARNESS_DIR/scripts/lib/dsl_engine.py"
TEMP_DIR="${TEMP_DIR:-/tmp/swebok-adversarial}"

mkdir -p "$TEMP_DIR"

# === CHECK FOR JUDGE-ONLY MODE ===
JUDGE_ONLY=false
COUNCIL=false
REDO_DSL=""
BLUE_DSL=""
FROM_P=""
TO_P=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --judge-only)
            JUDGE_ONLY=true
            shift
            ;;
        --council)
            # AUDIT-2026-06-02 (ADR-003 / G.3): opt-in real council bridge.
            # Closes CRIT-2 from the original 2026-06-01 audit (gate fixture).
            COUNCIL=true
            shift
            ;;
        --red)
            RED_DSL="$2"
            shift 2
            ;;
        --blue)
            BLUE_DSL="$2"
            shift 2
            ;;
        *)
            if [[ -z "$FROM_P" ]]; then
                FROM_P="$1"
            elif [[ -z "$TO_P" ]]; then
                TO_P="$1"
            fi
            shift
            ;;
    esac
done

# === COUNCIL MODE (ADR-003 / G.3) — opt-in real council bridge ===
# When --council is passed, delegate the WHOLE envelope to multiagent-launcher.sh
# (single owner of the bridge envelope per CLAUDE.md L6 / L6.1), surface any
# launcher stderr instead of swallowing it, validate the from/to phase, and
# exit 99 (signal: "please spawn agents and re-invoke with --judge-only").
if [[ "$COUNCIL" == true ]]; then
    if [[ -z "$FROM_P" || -z "$TO_P" ]]; then
        echo "Usage: adversarial-gate.sh --council <from_phase> <to_phase>" >&2
        exit 1
    fi
    # Input validation (CISO INJ-1 / Architect F-04): reject anything that is
    # not a P<digit> phase. Prevents prompt-injection through the role prompts
    # and the latent P10/P11 phase_num truncation bug in the launcher.
    if [[ ! "$FROM_P" =~ ^P[0-9]+$ ]] || [[ ! "$TO_P" =~ ^P[0-9]+$ ]]; then
        echo "[GATE] FATAL: --council requires P<digit> phases (got from='$FROM_P' to='$TO_P')" >&2
        exit 1
    fi
    if [[ "${MULTIAGENT_BRIDGE_ENABLED:-0}" != "1" ]]; then
        echo "[GATE] WARN: --council requested but MULTIAGENT_BRIDGE_ENABLED is not set;" >&2
        echo "[GATE]       emitting envelope anyway. Set the env var before re-invoking" >&2
        echo "[GATE]       with --judge-only to ensure the dispatcher honours the spawn." >&2
    fi
    LAUNCHER="$HARNESS_DIR/scripts/multiagent-launcher.sh"
    if [[ ! -x "$LAUNCHER" ]]; then
        echo "[GATE] FATAL: multiagent-launcher.sh missing or not executable: $LAUNCHER" >&2
        exit 1
    fi
    # FIX (F-001, 3-council convergence): capture launcher stderr to a file,
    # do NOT swallow it with 2>/dev/null, do NOT use `|| true`, and require
    # a non-empty envelope before exiting 99. An empty body would let a
    # dispatcher interpret "no prompts" as "no council needed", re-opening
    # CRIT-2 from the original 2026-06-01 audit.
    COUNCIL_STDERR="$TEMP_DIR/council_stderr.$$.log"
    COUNCIL_ENVELOPE="$(bash "$LAUNCHER" emit-envelope "$FROM_P" "$TO_P" 2>"$COUNCIL_STDERR")"
    LAUNCHER_EXIT=$?
    if [[ $LAUNCHER_EXIT -ne 0 ]]; then
        echo "[GATE] FATAL: multiagent-launcher.sh emit-envelope exited $LAUNCHER_EXIT" >&2
        echo "[GATE] --- launcher stderr (first 20 lines) ---" >&2
        head -n 20 "$COUNCIL_STDERR" >&2 || true
        exit 1
    fi
    if [[ -z "$COUNCIL_ENVELOPE" ]]; then
        echo "[GATE] FATAL: multiagent-launcher.sh emit-envelope returned an empty envelope" >&2
        echo "[GATE] --- launcher stderr (first 20 lines) ---" >&2
        head -n 20 "$COUNCIL_STDERR" >&2 || true
        exit 1
    fi
    if [[ "$COUNCIL_ENVELOPE" != *"<MULTIAGENT_LAUNCH"* ]] || [[ "$COUNCIL_ENVELOPE" != *"</MULTIAGENT_LAUNCH>" ]]; then
        echo "[GATE] FATAL: launcher output is not a well-formed <MULTIAGENT_LAUNCH> envelope" >&2
        echo "[GATE] --- output ---" >&2
        echo "$COUNCIL_ENVELOPE" | head -n 5 >&2
        exit 1
    fi
    echo "$COUNCIL_ENVELOPE"
    # Log the council request through the chained audit path.
    python3 "$STATE_ENGINE" log_adversarial \
        "COUNCIL_REQUEST" "REQUEST" "from=${FROM_P} to=${TO_P} env=${MULTIAGENT_BRIDGE_ENABLED:-0} launcher_exit=${LAUNCHER_EXIT}" \
        >/dev/null 2>&1 || true
    # Best-effort cleanup of the per-invocation stderr log.
    rm -f "$COUNCIL_STDERR" 2>/dev/null || true
    exit 99
fi

if [[ "$JUDGE_ONLY" == true ]]; then
    if [[ -z "$RED_DSL" || -z "$BLUE_DSL" ]]; then
        echo "Usage: adversarial-gate.sh <from_phase> <to_phase> --judge-only --red 'RED:...' --blue 'BLUE:...'"
        exit 1
    fi

    echo "=========================================="
    echo "  JUDGE-ONLY MODE"
    echo "=========================================="

    # Parse RED DSL
    RED_PARSED=$(python3 "$DSL_ENGINE" parse "$RED_DSL" 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "[ERROR] Failed to parse RED DSL: $RED_PARSED"
        exit 1
    fi

    # Parse BLUE DSL
    BLUE_PARSED=$(python3 "$DSL_ENGINE" parse "$BLUE_DSL" 2>&1)
    if [[ $? -ne 0 ]]; then
        echo "[ERROR] Failed to parse BLUE DSL: $BLUE_PARSED"
        exit 1
    fi

    # Extract key fields
    RED_VULN=$(echo "$RED_PARSED" | grep -i "^VULN:" | cut -d: -f2- | tr -d ' ')
    RED_TYPE=$(echo "$RED_PARSED" | grep -i "^TYPE:" | cut -d: -f2- | tr -d ' ')
    BLUE_STATUS=$(echo "$BLUE_PARSED" | grep -i "^STATUS:" | cut -d: -f2- | tr -d ' ')

    # Judge decision
    if [[ "$RED_VULN" == "CRIT" || "$RED_VULN" == "HIGH" ]]; then
        VERDICT="DENY"
        REASON="${RED_VULN}_SEVERITY_ISSUE"
    else
        VERDICT="PASS"
        REASON="NO_CRITICAL_FLAWS"
    fi

    JUDGE_OUTPUT="JUDGE: GATE:${VERDICT};;FIX_REQ:NONE;;REASON:${REASON}"
    echo "[JUDGE] $JUDGE_OUTPUT"

    # Log to state
    python3 "$STATE_ENGINE" log_adversarial "JUDGE_ONLY" "$VERDICT" "$REASON" 2>/dev/null || true

    echo "=========================================="
    echo "  RESULT: $VERDICT"
    echo "=========================================="

    if [[ "$VERDICT" == "PASS" ]]; then
        exit 0
    else
        exit 1
    fi
fi

# === NORMAL MODE ===
# v1.5.5: NORMAL MODE returns canned fixtures and is intended for development
# and CI only. Production callers MUST use --council (4 real agents) or
# --judge-only (pre-computed real DSL). Set HARNESS_TEST_FIXTURE=1 to opt
# in to the canned fixture path; otherwise the gate refuses to run.
if [[ -z "$FROM_P" || -z "$TO_P" ]]; then
    echo "Usage: adversarial-gate.sh <from_phase> <to_phase>"
    exit 1
fi
if [[ "${HARNESS_TEST_FIXTURE:-0}" != "1" ]]; then
    cat <<'MSG' >&2
[FATAL] adversarial-gate.sh NORMAL MODE returns canned fixtures and is not
a real adversarial review. It exists only for development smoke tests.

For a real gate review, use one of:
  bash adversarial-gate.sh <from> <to> --council   # spawn 4 nexus-* subagents
  bash adversarial-gate.sh <from> <to> --judge-only --red "..." --blue "..."

To opt in to the canned fixture path (development only):
  HARNESS_TEST_FIXTURE=1 bash adversarial-gate.sh <from> <to>

Refusing to run without one of the above.
MSG
    exit 1
fi

STATE_FILE_PLACEHOLDER=  # removed - state of truth is .swebok_state.db
RED_OUTPUT_FILE="$TEMP_DIR/red_output.txt"
BLUE_OUTPUT_FILE="$TEMP_DIR/blue_output.txt"
COMBINED_OUTPUT_FILE="$TEMP_DIR/combined_output.txt"

GATE="${FROM_P}_EXIT"
PHASE_NUM="${FROM_P:1:1}"

echo "=========================================="
echo "  ADVERSARIAL GATE VALIDATION"
echo "  Gate: $GATE → $TO_P"
echo "=========================================="

# === STEP 1: OUTPUT MULTIAGENT LAUNCH XML ===
echo ""
echo "[ADVERSARIAL] Generating Red/Blue agent launch XML..."

cat <<MULTIAGENT_XML
<MULTIAGENT_LAUNCH
    blue="Nexus_Defender"
    red="Nexus_Attacker"
    prompt="Analyze vulnerabilities for $GATE transition. RED: VULN:<severity>;;LOC:<location>;;TYPE:<vulnerability_type>;;FIX_REQ:<fix_requirement>. Output ONE DSL line. BLUE: DEFENDED;;NORMS:<ka_numbers>;;STATUS:<ok|failed>. Output ONE DSL line." />
MULTIAGENT_XML

echo ""
echo "[ADVERSARIAL] === RED OUTPUT PLACEHOLDER ===" > "$RED_OUTPUT_FILE"
echo "RED_OUTPUT_PLACEHOLDER" >> "$RED_OUTPUT_FILE"

echo ""
echo "[ADVERSARIAL] === BLUE OUTPUT PLACEHOLDER ===" > "$BLUE_OUTPUT_FILE"
echo "BLUE_OUTPUT_PLACEHOLDER" >> "$BLUE_OUTPUT_FILE"

# === STEP 2: SIMULATE RED/BLUE OUTPUTS FOR INTERNAL TESTING ===
case "$FROM_P" in
    P1)
        RED_ACTUAL="RED: VULN:LOW;;LOC:REQUIREMENTS;;TYPE:REQ_AMBIGUITY;;FIX_REQ:NONE"
        ;;
    P2)
        RED_ACTUAL="RED: VULN:MED;;LOC:MICROSERVICE_FLOW;;TYPE:ARCH_FRAGILITY;;FIX_REQ:ADD_CIRCUIT_BREAKER"
        ;;
    P3)
        RED_ACTUAL="RED: VULN:MED;;LOC:API_SURFACE;;TYPE:DESIGN_COMPLEXITY;;FIX_REQ:SIMPLIFY_INTERFACE"
        ;;
    P4)
        RED_ACTUAL="RED: VULN:LOW;;LOC:ESTIMATION;;TYPE:IMPL_FEASIBILITY;;FIX_REQ:REFINE_ESTIMATE"
        ;;
    P5)
        RED_ACTUAL="RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION_RISK;;FIX_REQ:SANITIZE_ALL_INPUTS"
        ;;
    P6)
        RED_ACTUAL="RED: VULN:HIGH;;LOC:CONFIG;;TYPE:ENV_DIVERGENCE;;FIX_REQ:UNIFY_ENV_CONFIGS"
        ;;
    P7)
        RED_ACTUAL="RED: VULN:MED;;LOC:MONITORING;;TYPE:OPS_READINESS;;FIX_REQ:ADD_SLO_MONITORING"
        ;;
    P8)
        RED_ACTUAL="RED: VULN:MED;;LOC:MONITORING;;TYPE:OPS_READINESS;;FIX_REQ:ADD_SLO_MONITORING"
        ;;
    *)
        RED_ACTUAL="RED: VULN:LOW;;LOC:GENERIC;;TYPE:GENERIC;;FIX_REQ:NONE"
        ;;
esac

case "$FROM_P" in
    P1) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-1+KA-2;;STATUS:OK" ;;
    P2) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-2+KA-13;;STATUS:OK" ;;
    P3) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-3+KA-4;;STATUS:OK" ;;
    P4) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-4+KA-5;;STATUS:OK" ;;
    P5) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-4+KA-5;;STATUS:OK" ;;
    P6) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-5+KA-11;;STATUS:OK" ;;
    P7) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-6+KA-7;;STATUS:OK" ;;
    P8) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-6+KA-7;;STATUS:OK" ;;
    *) BLUE_ACTUAL="BLUE: DEFENDED;;NORMS:KA-GENERIC;;STATUS:OK" ;;
esac

echo "$RED_ACTUAL" > "$RED_OUTPUT_FILE"
echo "$BLUE_ACTUAL" > "$BLUE_OUTPUT_FILE"

# === STEP 3: PARSE WITH DSL ENGINE ===
echo ""
echo "[ADVERSARIAL] Parsing Red/Blue outputs with dsl_engine.py..."

RED_CONTENT=$(cat "$RED_OUTPUT_FILE")
BLUE_CONTENT=$(cat "$BLUE_OUTPUT_FILE")

RED_PARSED=$(python3 "$DSL_ENGINE" parse "$RED_CONTENT" 2>&1)
RED_PARSED_EXIT=$?

if [[ $RED_PARSED_EXIT -ne 0 ]]; then
    echo "[ADVERSARIAL] FORMAT_ERROR: Red output parse failed"
    exit 1
fi

BLUE_PARSED=$(python3 "$DSL_ENGINE" parse "$BLUE_CONTENT" 2>&1)
BLUE_PARSED_EXIT=$?

if [[ $BLUE_PARSED_EXIT -ne 0 ]]; then
    echo "[ADVERSARIAL] FORMAT_ERROR: Blue output parse failed"
    exit 1
fi

echo "[ADVERSARIAL] Red parsed: $RED_PARSED"
echo "[ADVERSARIAL] Blue parsed: $BLUE_PARSED"

RED_VULN=$(echo "$RED_PARSED" | grep -i "^VULN:" | cut -d: -f2- | tr -d ' ')
RED_TYPE=$(echo "$RED_PARSED" | grep -i "^TYPE:" | cut -d: -f2- | tr -d ' ')
BLUE_STATUS=$(echo "$BLUE_PARSED" | grep -i "^STATUS:" | cut -d: -f2- | tr -d ' ')

# === STEP 4: JUDGE DECISION ===
echo ""
echo "[JUDGE] Making gate decision based on strict DSL dict..."

if [[ "$RED_VULN" == "CRIT" ]]; then
    VERDICT="DENY"
    REASON="CRITICAL_FLAW_FOUND"
elif [[ "$RED_VULN" == "HIGH" ]]; then
    VERDICT="DENY"
    REASON="HIGH_SEVERITY_ISSUE"
else
    VERDICT="PASS"
    REASON="NO_CRITICAL_FLAWS"
fi

JUDGE_OUTPUT="JUDGE: GATE:${VERDICT};;FIX_REQ:NONE;;REASON:${REASON}"
echo "[JUDGE] $JUDGE_OUTPUT"

# === STEP 5: LOG AND RESET CIRCUITS ON PASS ===
echo ""
echo "=========================================="

if [[ "$VERDICT" == "PASS" ]]; then
    echo "  ADVERSARIAL RESULT: PASS"
    echo "  Blue team defended successfully"
    echo "  Red team found no critical issues"
    echo "=========================================="

    python3 "$STATE_ENGINE" reset_all_circuits "$TO_P" 2>/dev/null || true
    python3 "$STATE_ENGINE" log_adversarial "$GATE" "PASS" "$REASON" 2>/dev/null || true
    exit 0
else
    echo "  ADVERSARIAL RESULT: DENY"
    echo "  Reason: $REASON"
    echo "=========================================="
    python3 "$STATE_ENGINE" log_adversarial "$GATE" "DENY" "$REASON" 2>/dev/null || true
    exit 1
fi