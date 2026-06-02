#!/usr/bin/env bash
# SWEBOK v4 Harness - Self-Healing (MCP-BRIDGE)
# Diagnoses and corrects Browser Use failures via MCP Bridge instructions
# Usage:
#   ./self-heal.sh <error_message> <screenshot_path> [step_context]
#   ./self-heal.sh --verify-result <result_file>     # Verify MCP result

set -euo pipefail
trap 'echo "WARN:HEAL_INTERNAL_ERROR"; exit 1' ERR

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
# State of truth: .swebok_state.db. STATE_FILE is NOT read.
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
MCP_RESULT="/tmp/mcp_result.json"
DSL_PREFIX="HEAL"

# Source shared MCP precheck library
MCP_PRECHECK_LIB="$HARNESS_DIR/scripts/lib/mcp_precheck.sh"
# shellcheck disable=SC1090
[[ -f "$MCP_PRECHECK_LIB" ]] && source "$MCP_PRECHECK_LIB" || true

# H8: precheck MCP availability before emitting instructions. A HEAL
# diagnosis that emits <MCP_CALL> when no MCP tool is reachable is just
# noise to the operator; the dispatcher silently drops the call.
mcp_precheck_required() {
    if ! mcp_precheck "$DSL_PREFIX"; then
        echo "HEAL:FAIL|REASON:MCP_UNAVAILABLE"
        exit 1
    fi
}

# H5: clean up /tmp/mcp_result.json on every exit path of this script.
cleanup_mcp_result() {
    rm -f "$MCP_RESULT" 2>/dev/null || true
}
trap 'cleanup_mcp_result' EXIT

log_dsl() {
    echo "[$DSL_PREFIX] $1"
}

# === VERIFY RESULT MODE ===
if [[ "$1" == "--verify-result" ]]; then
    RESULT_FILE="${2:-}"
    if [[ -z "$RESULT_FILE" ]]; then
        log_dsl "ERROR: Result file missing: $RESULT_FILE"
        echo "HEAL:FAIL|REASON:RESULT_FILE_MISSING"
        exit 1
    fi
    # M9: reject symlinks and require path be under /tmp.
    if [[ -L "$RESULT_FILE" ]]; then
        log_dsl "REJECT: RESULT_FILE is a symlink: $RESULT_FILE"
        echo "HEAL:FAIL|REASON:SYMLINK_RESULT"
        exit 1
    fi
    RP_RF=$(realpath "$RESULT_FILE" 2>/dev/null || echo "")
    case "$RP_RF" in
        /tmp/*) ;;
        *)
            log_dsl "REJECT: RESULT_FILE not under /tmp: $RP_RF"
            echo "HEAL:FAIL|REASON:RESULT_NOT_SANDBOXED"
            exit 1
            ;;
    esac
    if [[ ! -f "$RP_RF" ]]; then
        log_dsl "ERROR: Result file missing: $RESULT_FILE"
        echo "HEAL:FAIL|REASON:RESULT_FILE_MISSING"
        exit 1
    fi

    RESULT_CONTENT=$(cat "$RP_RF" 2>/dev/null || echo "")

    log_dsl "VERIFY: result file size=${#RESULT_CONTENT} bytes"

    # M15: require JSON envelope with status:ok|error instead of textual
    # heuristic. The grep-for-error approach was a known bypass.
    ENVELOPE_OK=$(python3 -c "
import json, sys
try:
    with open('$RP_RF') as f:
        d = json.load(f)
    status = d.get('status', '')
    if status in ('ok', 'error'):
        print('OK:' + status)
    else:
        print('NO_ENVELOPE')
except Exception as e:
    print(f'NO_ENVELOPE:{type(e).__name__}')
" 2>/dev/null || echo "NO_ENVELOPE")
    case "$ENVELOPE_OK" in
        OK:ok)
            log_dsl "RESULT: Verification passed (status:ok envelope)"
            echo "HEAL:PASS"
            # Update state with successful heal
            python3 "$STATE_ENGINE" set "phase_data.P6.heal_success" "true" 2>/dev/null || true
            # H5: clean mcp_result after a successful verify.
            cleanup_mcp_result
            exit 0
            ;;
        OK:error)
            log_dsl "RESULT: MCP reported error envelope"
            echo "HEAL:FAIL|REASON:MCP_STATUS_ERROR"
            cleanup_mcp_result
            exit 1
            ;;
        *)
            log_dsl "RESULT: Verification failed - missing JSON envelope (got: $ENVELOPE_OK)"
            echo "HEAL:FAIL|REASON:NO_ENVELOPE"
            cleanup_mcp_result
            exit 1
            ;;
    esac
fi

# === NORMAL MODE ===
ERROR_MSG="$1"
SCREENSHOT="$2"
STEP_CONTEXT="${3:-}"

# === ANTI-LOOP: Check heal_iterations to prevent infinite self-heal loops ===
HEAL_ITERATIONS=$(python3 "$STATE_ENGINE" get_heal_iterations 2>/dev/null || echo "0")
if [[ "${HEAL_ITERATIONS:-0}" -ge 3 ]]; then
    log_dsl "HEAL:LOOP_BLOCKED: heal_iterations=$HEAL_ITERATIONS >= 3"
    echo "HEAL:FAIL|REASON:INFINITE_LOOP_DETECTED"
    exit 1
fi
python3 "$STATE_ENGINE" increment_heal_iterations 2>/dev/null || true

# === DIAGNOSE: Pattern match error type ===
diagnose_error_type() {
    local msg="$1"

    case "$msg" in
        *"not found"*|*"element not found"*|*"unable to locate"*|*"no such element"*)
            echo "ELEMENT_NOT_FOUND"
            ;;
        *"timeout"*|*"timed out"*|*"takes too long"*|*"slow"*|*"Timed out"*)
            echo "TIMEOUT"
            ;;
        *"wrong element"*|*"unexpected element"*|*"element mismatch"*)
            echo "WRONG_ELEMENT"
            ;;
        *"stale element"*|*"no longer attached"*)
            echo "STALE_ELEMENT"
            ;;
        *"disabled"*|*"not clickable"*|*"obscured"*|*"intercepted"*)
            echo "ELEMENT_NOT_INTERACTABLE"
            ;;
        *"assertion"*|*"verification"*|*"expected"*|*"actual"*|*"mismatch"*)
            echo "ASSERTION_FAILURE"
            ;;
        *"403"*|*"401"*|*"forbidden"*|*"unauthorized"*)
            echo "AUTH_FAILURE"
            ;;
        *"500"*|*"502"*|*"503"*|*"server error"*)
            echo "SERVER_ERROR"
            ;;
        *"network"*|*"connection"*|*"ECONNREFUSED"*)
            echo "NETWORK_FAILURE"
            ;;
        *)
            echo "UNKNOWN"
            ;;
    esac
}

# === OUTPUT MCP BRIDGE INSTRUCTIONS IN XML FORMAT ===
mcp_diagnose() {
    local screenshot="$1"
    local context="$2"

    log_dsl "MCP_BRIDGE: Preparing diagnose_error_screenshot instruction"
    # M28: JSON-escape args via python3 to prevent XML/quote injection.
    local _args
    _args=$(SCREENSHOT="$screenshot" CONTEXT="$context" ERR="$ERROR_MSG" python3 -c '
import json, os
print(json.dumps({
    "image_source": os.environ["SCREENSHOT"],
    "prompt": "Diagnose error: " + os.environ["CONTEXT"],
    "context": os.environ["ERR"],
}))
')
    echo "<MCP_CALL><tool>mcp__zai-mcp-server__diagnose_error_screenshot</tool><args>${_args}</args></MCP_CALL>"
}

mcp_extract() {
    local screenshot="$1"

    log_dsl "MCP_BRIDGE: Preparing extract_text_from_screenshot instruction"
    local _args
    _args=$(SCREENSHOT="$screenshot" python3 -c '
import json, os
print(json.dumps({
    "image_source": os.environ["SCREENSHOT"],
    "prompt": "Extract all visible text",
    "context": "",
}))
')
    echo "<MCP_CALL><tool>mcp__zai-mcp-server__extract_text_from_screenshot</tool><args>${_args}</args></MCP_CALL>"
}

mcp_ui_diff() {
    local screenshot_a="$1"
    local screenshot_b="$2"
    local context="${3:-}"

    log_dsl "MCP_BRIDGE: Preparing ui_diff_check instruction"
    local _args
    _args=$(SA="$screenshot_a" SB="$screenshot_b" CTX="$context" python3 -c '
import json, os
print(json.dumps({
    "expected_image_source": os.environ["SA"],
    "actual_image_source": os.environ["SB"],
    "prompt": "Verify UI state after fix",
    "context": os.environ["CTX"],
}))
')
    echo "<MCP_CALL><tool>mcp__zai-mcp-server__ui_diff_check</tool><args>${_args}</args></MCP_CALL>"
}

# === DETERMINE RECOMMENDED ACTION ===
get_recommended_action() {
    local error_type="$1"

    case "$error_type" in
        ELEMENT_NOT_FOUND)
            echo "UPDATE_SELECTOR"
            ;;
        TIMEOUT)
            echo "INCREASE_TIMEOUT"
            ;;
        WRONG_ELEMENT)
            echo "USE_VISUAL_GROUNDING"
            ;;
        STALE_ELEMENT)
            echo "REFRESH_AND_RETRY"
            ;;
        ELEMENT_NOT_INTERACTABLE)
            echo "WAIT_FOR_VISIBLE"
            ;;
        ASSERTION_FAILURE)
            echo "UPDATE_ASSERTION"
            ;;
        AUTH_FAILURE)
            echo "REAUTHENTICATE"
            ;;
        SERVER_ERROR)
            echo "RETRY_WITH_BACKOFF"
            ;;
        NETWORK_FAILURE)
            echo "CHECK_CONNECTIVITY"
            ;;
        *)
            echo "HUMAN_REVIEW"
            ;;
    esac
}

# === GET POSSIBLE CAUSES ===
get_possible_causes() {
    local error_type="$1"
    local causes=""

    case "$error_type" in
        ELEMENT_NOT_FOUND)
            causes="Selector changed after refactor;;Element behind overlay;;Dynamic ID regeneration;;Wrong page loaded"
            ;;
        TIMEOUT)
            causes="Slow network;;API not responding;;Infinite loading spinner;;JavaScript not executing"
            ;;
        WRONG_ELEMENT)
            causes="Selector matches multiple elements;;DOM structure changed;;A/B test variation;;i18n mismatch"
            ;;
        STALE_ELEMENT)
            causes="Page re-rendered during interaction;;React/Vue rehydration;;AJAX update replacing DOM"
            ;;
        ELEMENT_NOT_INTERACTABLE)
            causes="Element not yet visible;;Modal overlay blocking;;CSS animation in progress;;z-index issue"
            ;;
        ASSERTION_FAILURE)
            causes="Expected content not present;;Incorrect test data;;Localization mismatch;;API response changed"
            ;;
        AUTH_FAILURE)
            causes="Token expired;;Session invalidated;;Permissions revoked;;Credential rotation"
            ;;
        SERVER_ERROR)
            causes="Backend service down;;Database overloaded;;Microservice unavailable;;Dependency failure"
            ;;
        NETWORK_FAILURE)
            causes="DNS resolution failed;;Firewall blocking;;Proxy issue;;SSL handshake failure"
            ;;
        *)
            causes="Unknown error;;Requires manual review;;Check browser console;;Verify app state"
            ;;
    esac

    echo "$causes"
}

# === GET SPECIFIC FIXES ===
get_specific_fixes() {
    local error_type="$1"

    case "$error_type" in
        ELEMENT_NOT_FOUND)
            echo "Use analyze_image on screenshot to identify element visually;;Use understand-diff to check selector changes;;Run visual grounding from Phase3/4 maquettes;;Update test script with new selector"
            ;;
        TIMEOUT)
            echo "Increase wait time for this step;;Check if API endpoint is responding;;Verify network connectivity;;Add explicit wait for element"
            ;;
        WRONG_ELEMENT)
            echo "Use ui_to_artifact to analyze maquette;;Get visual description of expected element;;Use more specific selector (data-testid, aria-label);;Apply visual grounding with analyze_image"
            ;;
        STALE_ELEMENT)
            echo "Refresh page reference before interaction;;Add explicit wait for element re-attachment;;Re-query element within same context"
            ;;
        ELEMENT_NOT_INTERACTABLE)
            echo "Wait for element visibility (scrollIntoView);;Dismiss modal overlays first;;Wait for CSS animations;;Use JavaScript click as fallback"
            ;;
        ASSERTION_FAILURE)
            echo "Verify expected content is correct;;Check for localization/i18n issues;;Use extract_text_from_screenshot to verify actual content;;Update test data or assertion"
            ;;
        AUTH_FAILURE)
            echo "Refresh authentication token;;Check session validity;;Update credentials in vault;;Verify permissions scope"
            ;;
        SERVER_ERROR)
            echo "Retry with exponential backoff;;Check service health dashboard;;Verify dependency status;;Alert on-call if persistent"
            ;;
        NETWORK_FAILURE)
            echo "Check network connectivity;;Ping API endpoint;;Verify DNS resolution;;Test via proxy"
            ;;
        *)
            echo "Manual review required;;Check browser console;;Verify application state;;Debug with network tab"
            ;;
    esac
}

# === MAIN DIAGNOSTIC LOGIC ===
log_dsl "=========================================="
log_dsl "  SELF-HEAL DIAGNOSTIC (MCP-BRIDGE)"
log_dsl " Error: $ERROR_MSG"
log_dsl "=========================================="

# H8: MCP-unavailable precheck. Abort early if dispatcher cannot reach MCP.
mcp_precheck_required

# DIAGNOSE error type
ERROR_TYPE=$(diagnose_error_type "$ERROR_MSG")
RECOMMENDED_ACTION=$(get_recommended_action "$ERROR_TYPE")
POSSIBLE_CAUSES=$(get_possible_causes "$ERROR_TYPE")
SPECIFIC_FIXES=$(get_specific_fixes "$ERROR_TYPE")

log_dsl "Error Type: $ERROR_TYPE"
log_dsl "Recommended Action: $RECOMMENDED_ACTION"

# === MCP BRIDGE ANALYSIS ===
log_dsl ""
log_dsl "--- MCP Bridge Instructions ---"

if [[ -f "$SCREENSHOT" ]] && [[ -s "$SCREENSHOT" ]]; then
    DIAGNOSE_XML=$(mcp_diagnose "$SCREENSHOT" "$ERROR_MSG")
    EXTRACT_XML=$(mcp_extract "$SCREENSHOT")
    echo "$DIAGNOSE_XML"
    echo "$EXTRACT_XML"
else
    log_dsl "MCP_BRIDGE: No valid screenshot provided - skipping MCP instructions"
fi

# Output HEAL: DSL (using ;; delimiter per DSL spec)
echo "HEAL: $ERROR_TYPE;;ACTION:$RECOMMENDED_ACTION;;CONTEXT:$STEP_CONTEXT"

# === DISPLAY POSSIBLE CAUSES ===
log_dsl ""
log_dsl "--- Possible Causes ---"
IFS=';;' read -ra CAUSES <<< "$POSSIBLE_CAUSES"
for i in "${!CAUSES[@]}"; do
    log_dsl "  $((i+1)). ${CAUSES[$i]}"
done

# === DISPLAY SPECIFIC FIXES ===
log_dsl ""
log_dsl "--- Recommended Fixes ---"
IFS=';;' read -ra FIXES <<< "$SPECIFIC_FIXES"
for i in "${!FIXES[@]}"; do
    log_dsl "  $((i+1)). ${FIXES[$i]}"
done

# === MCP TOOL RECOMMENDATIONS ===
log_dsl ""
log_dsl "--- MCP Tool Recommendations ---"

case "$ERROR_TYPE" in
    ELEMENT_NOT_FOUND|WRONG_ELEMENT)
        log_dsl "  - <MCP_CALL><tool>analyze_image</tool><args>{...}</args></MCP_CALL>"
        log_dsl "  - <MCP_CALL><tool>understand-diff</tool><args>{...}</args></MCP_CALL>"
        ;;
    ASSERTION_FAILURE)
        log_dsl "  - <MCP_CALL><tool>extract_text_from_screenshot</tool><args>{...}</args></MCP_CALL>"
        log_dsl "  - <MCP_CALL><tool>diagnose_error_screenshot</tool><args>{...}</args></MCP_CALL>"
        ;;
    TIMEOUT)
        log_dsl "  - <MCP_CALL><tool>understand-chat</tool><args>{...}</args></MCP_CALL>"
        ;;
    STALE_ELEMENT)
        log_dsl "  - <MCP_CALL><tool>analyze_image</tool><args>{...}</args></MCP_CALL>"
        ;;
esac

# === DSL OUTPUT FOR JUDGE ===
log_dsl ""
log_dsl "--- DSL Output for Judge ---"
DSL_OUTPUT="HEAL:$ERROR_TYPE;;ACTION:$RECOMMENDED_ACTION;;CONTEXT:$STEP_CONTEXT"
log_dsl "DSL: $DSL_OUTPUT"

log_dsl ""
log_dsl "=========================================="
log_dsl "  SELF-HEAL COMPLETE"
log_dsl "  Action: $RECOMMENDED_ACTION"
log_dsl "=========================================="

# Return recommended action and MCP instructions for orchestrator
# Output format: RECOMMENDATION|INSTRUCTION:...
echo "$RECOMMENDED_ACTION"
echo ""
echo "INSTRUCTION:SUMMARY:ERROR_TYPE=$ERROR_TYPE;;ACTION=$RECOMMENDED_ACTION;;FIXES=${SPECIFIC_FIXES//;;//}"
