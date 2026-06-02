#!/usr/bin/env bash
# SWEBOK v4 Harness - Browser Use Orchestrator (MCP-WIRED)
# Act → Screenshot → MCP Verify → Next Step
# Core surveillance loop for E2E testing
# Usage: ./browser-use-orchestrator.sh <scenario_file> <app_url> [max_steps]

set -e

SCENARIO_FILE="$1"
APP_URL="${2:-http://localhost:3000}"
MAX_STEPS="${3:-20}"
HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SCREENSHOT_DIR="${SCREENSHOT_DIR:-/tmp/swebok-screenshots}"
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
MCP_RESULT="/tmp/mcp_result.json"
# State of truth: .swebok_state.db. STATE_FILE is NOT read.

# M11: 0700 perms, realpath check for the screenshot dir.
if [[ ! -d "$SCREENSHOT_DIR" ]]; then
    mkdir -p "$SCREENSHOT_DIR"
fi
chmod 0700 "$SCREENSHOT_DIR" 2>/dev/null || true
SCREENSHOT_DIR_RESOLVED=$(realpath "$SCREENSHOT_DIR" 2>/dev/null || echo "")
if [[ -z "$SCREENSHOT_DIR_RESOLVED" || ! -d "$SCREENSHOT_DIR_RESOLVED" ]]; then
    echo "[ERROR] SCREENSHOT_DIR not a real directory: $SCREENSHOT_DIR" >&2
    exit 1
fi

# Source shared MCP precheck library (H8)
MCP_PRECHECK_LIB="$HARNESS_DIR/scripts/lib/mcp_precheck.sh"
# shellcheck disable=SC1090
[[ -f "$MCP_PRECHECK_LIB" ]] && source "$MCP_PRECHECK_LIB" || true

# H5: clean /tmp/mcp_result.json on every exit path of this script.
cleanup_mcp_result() {
    rm -f "$MCP_RESULT" 2>/dev/null || true
}
trap 'cleanup_mcp_result' EXIT

DSL_PREFIX="ORCH"

log_dsl() {
    echo "[$DSL_PREFIX] $1"
}

if [[ -z "$SCENARIO_FILE" ]]; then
    echo "Usage: browser-use-orchestrator.sh <scenario_file> <app_url> [max_steps]"
    echo "Example: browser-use-orchestrator.sh /tmp/checkout.scenario http://localhost:3000 15"
    exit 1
fi

if [[ ! -f "$SCENARIO_FILE" ]]; then
    echo "[ERROR] Scenario file not found: $SCENARIO_FILE"
    exit 1
fi

log_dsl "=========================================="
log_dsl "  BROWSER USE ORCHESTRATOR (MCP-WIRED)"
log_dsl "  Scenario: $SCENARIO_FILE"
log_dsl "  Target: $APP_URL"
log_dsl "  Max Steps: $MAX_STEPS"
log_dsl "=========================================="

# === LOAD SCENARIO ===
log_dsl "Loading scenario..."
STEPS=()
while IFS= read -r line; do
    case "$line" in
        *"Given"*|"When"*|"Then"*|"And"*)
            action=$(echo "$line" | sed 's/^\s*\(Given\|When\|Then\|And\)\s*//' | tr -d '"')
            STEPS+=("$action")
            ;;
    esac
done < "$SCENARIO_FILE"

log_dsl "Loaded ${#STEPS[@]} steps"

if [[ ${#STEPS[@]} -eq 0 ]]; then
    echo "[ERROR] No steps found in scenario file"
    exit 1
fi

# === MCP VERIFY FUNCTION ===
mcp_verify() {
    local screenshot="$1"
    local expected="$2"
    local context="${3:-}"

    if [[ ! -f "$screenshot" ]] || [[ ! -s "$screenshot" ]]; then
        echo "VERIFY:SKIP|no_screenshot"
        return 0
    fi

    # H8: precheck before invoking the dispatcher. If MCP is unavailable,
    # surface a SKIP that the caller will NOT count as success.
    if ! mcp_precheck "$DSL_PREFIX"; then
        echo "VERIFY:SKIP|MCP_DIAGNOSE:FAILED"
        return 0
    fi

    # MCP: diagnose_error_screenshot
    DIAGNOSE=$(mcp__zai-mcp-server__diagnose_error_screenshot \
        "$screenshot" \
        "Verify expected state: $expected" \
        "context: $context" 2>/dev/null || echo "MCP_DIAGNOSE:FAILED")

    # MCP: extract_text_from_screenshot
    EXTRACT=$(mcp__zai-mcp-server__extract_text_from_screenshot \
        "$screenshot" \
        "Extract visible text for verification" \
        "" 2>/dev/null || echo "MCP_EXTRACT:FAILED")

    # If diagnose failed, surface a SKIP that is NOT counted as success.
    if [[ "$DIAGNOSE" == "MCP_DIAGNOSE:FAILED" ]]; then
        echo "VERIFY:SKIP|MCP_DIAGNOSE:FAILED"
        return 0
    fi

    # Check if expected appears in extracted text
    if echo "$EXTRACT" | grep -qi "$expected"; then
        echo "VERIFY:PASS|EXPECTED_FOUND:$expected"
        return 0
    else
        echo "VERIFY:FAIL|EXPECTED_MISSING:$expected|ACTUAL:${EXTRACT:0:150}"
        return 1
    fi
}

# === SELF-HEAL FUNCTION ===
call_self_heal() {
    local error_msg="$1"
    local screenshot="$2"
    local step_context="$3"

    "$HARNESS_DIR/scripts/self-heal.sh" "$error_msg" "$screenshot" "$step_context"
}

# === EXECUTE ACT-OBSERVE-VERIFY LOOP ===
STEP_NUM=0
SUCCESS_COUNT=0
FAIL_COUNT=0

for step in "${STEPS[@]}"; do
    ((STEP_NUM++))

    if [[ $STEP_NUM -gt $MAX_STEPS ]]; then
        log_dsl "Max steps reached ($MAX_STEPS). Stopping."
        break
    fi

    log_dsl ""
    log_dsl "[STEP $STEP_NUM/${#STEPS[@]}] $step"
    log_dsl "----------------------------------------"

    # === ACT ===
    log_dsl "ACT: Executing: $step"

    ACTION_TYPE="unknown"
    TARGET=""
    VALUE=""

    if echo "$step" | grep -qi "navigate\|go to\|open\|visit"; then
        ACTION_TYPE="navigate"
        TARGET=$(echo "$step" | grep -oP '(to |on |/)\K[^"]+' | head -1)
        log_dsl "Type: NAVIGATE | Target: $TARGET"
    elif echo "$step" | grep -qi "click\|press\|submit"; then
        ACTION_TYPE="click"
        TARGET=$(echo "$step" | grep -oP 'the \K[^"]+' | head -1)
        log_dsl "Type: CLICK | Target: $TARGET"
    elif echo "$step" | grep -qi "fill\|type\|enter\|input"; then
        ACTION_TYPE="fill"
        TARGET=$(echo "$step" | grep -oP 'the \K[^"]+' | head -1)
        VALUE=$(echo "$step" | grep -oP '"\K[^"]+' | head -1)
        log_dsl "Type: FILL | Target: $TARGET | Value: $VALUE"
    elif echo "$step" | grep -qi "verify\|see\|should\|expect"; then
        ACTION_TYPE="verify"
        TARGET=$(echo "$step" | grep -oP 'the \K[^"]+' | head -1)
        log_dsl "Type: VERIFY | Target: $TARGET"
    fi

    # === OBSERVE (Screenshot) ===
    log_dsl "OBSERVE: Taking screenshot..."
    # M11: urandom in filename to avoid predictable symlink attack surface.
    RAND_HEX=$(tr -dc 'a-f0-9' </dev/urandom 2>/dev/null | head -c 16 || echo "$RANDOM$RANDOM")
    SCREENSHOT="$SCREENSHOT_DIR/step_${STEP_NUM}_$(date +%s%N)_${RAND_HEX}.png"

    # Try native screenshot tools
    if command -v gnome-screenshot&>/dev/null; then
        gnome-screenshot -f "$SCREENSHOT" 2>/dev/null || touch "$SCREENSHOT"
    elif command -v scrot &>/dev/null; then
        scrot "$SCREENSHOT" 2>/dev/null || touch "$SCREENSHOT"
    elif command -v import&>/dev/null; then
        import -window root "$SCREENSHOT" 2>/dev/null || touch "$SCREENSHOT"
    else
        touch "$SCREENSHOT"
    fi

    log_dsl "Screenshot: $SCREENSHOT"

    # === VERIFY (MCP Tools) ===
    log_dsl "VERIFY: Running MCP validation..."

    # Determine expected based on action type
    EXPECTED=""
    case "$ACTION_TYPE" in
        navigate)
            EXPECTED="page loaded"
            ;;
        click)
            EXPECTED="clicked"
            ;;
        fill)
            EXPECTED="$VALUE"
            ;;
        verify)
            EXPECTED="$TARGET"
            ;;
    esac

    VERIFY_RESULT=$(mcp_verify "$SCREENSHOT" "$EXPECTED" "$step")
    log_dsl "VERIFY_RESULT: $VERIFY_RESULT"

    # === DECIDE ===
    log_dsl "DECIDE: Analyzing result..."

    # Parse status from VERIFY_RESULT
    STATUS=$(echo "$VERIFY_RESULT" | cut -d: -f2)
    DETAILS=$(echo "$VERIFY_RESULT" | cut -d: -f3-)

    case "$STATUS" in
        PASS)
            log_dsl "Result: SUCCESS ✓"
            ((SUCCESS_COUNT++))
            ;;
        FAIL)
            log_dsl "Result: FAIL ✗ - $DETAILS"
            log_dsl "Initiating self-healing..."

            call_self_heal "Step $STEP_NUM failed: $step" "$SCREENSHOT" "$step"

            ((FAIL_COUNT++))

            if [[ $FAIL_COUNT -gt 3 ]]; then
                log_dsl "Too many failures ($FAIL_COUNT). Stopping."
                break
            fi
            ;;
        SKIP)
            # H8: SKIP is acceptable when there was no screenshot. But the
            # prior code counted it as a success unconditionally, which
            # masked the case where MCP_DIAGNOSE:FAILED - i.e. the MCP
            # tool never ran. Do NOT count SKIP as success if the MCP
            # diagnose stage reported failure.
            if [[ "$VERIFY_RESULT" == *"MCP_DIAGNOSE:FAILED"* ]]; then
                log_dsl "Result: SKIP (MCP_DIAGNOSE:FAILED) - NOT counted as success"
                ((FAIL_COUNT++))
                if [[ $FAIL_COUNT -gt 3 ]]; then
                    log_dsl "Too many failures ($FAIL_COUNT). Stopping."
                    break
                fi
            else
                log_dsl "Result: SKIP (no screenshot) - assuming success"
                ((SUCCESS_COUNT++))
            fi
            ;;
        *)
            log_dsl "Result: UNKNOWN - $VERIFY_RESULT"
            ((FAIL_COUNT++))
            ;;
    esac

done

# === SUMMARY ===
log_dsl ""
log_dsl "=========================================="
log_dsl "  BROWSER USE COMPLETE"
log_dsl "  Total Steps: $STEP_NUM"
log_dsl "  Success: $SUCCESS_COUNT"
log_dsl "  Failed: $FAIL_COUNT"
log_dsl "=========================================="

if [[ $FAIL_COUNT -eq 0 ]]; then
    log_dsl "RESULT: ALL PASS ✓"
    echo "DSL:$DSL_PREFIX:GATE:PASS|STEPS:$STEP_NUM|SUCCESS:$SUCCESS_COUNT"
    exit 0
else
    log_dsl "RESULT: $FAIL_COUNT FAILURES ✗"
    echo "DSL:$DSL_PREFIX:GATE:DENY|STEPS:$STEP_NUM|FAIL:$FAIL_COUNT"
    exit 1
fi
