#!/usr/bin/env bash
# SWEBOK v4 Harness - PreToolUse Bash Guard
# Phase-aware raw string scanning for Bash tool
# FAIL-SECURE: trap exits 1 on any internal error
#
# v1.4.1+ changes:
#   H7: stdin size limited to 1MB
#   H8: HARNESS_DIR validated at startup
#   H2: description field concatenated to command before scanning
#   C10: ANTI-ROT soft-block (exit 2 with ANTI-ROT:NUDGE) on every 5th call

set -euo pipefail
# FAIL-SECURE: Block on internal errors (crash, missing deps, etc.)
trap 'echo "WARN:HOOK_INTERNAL_ERROR: Blocking action due to script crash"; exit 1' ERR

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
# H8: refuse to run against a non-harness HARNESS_DIR
if [[ ! -d "$HARNESS_DIR" ]] || [[ ! -d "$HARNESS_DIR/scripts/lib" ]]; then
    echo "[BASH-GUARD] FATAL: HARNESS_DIR=$HARNESS_DIR is not a SWEBOK harness checkout."
    exit 1
fi
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
BASH_SCANNER="$HARNESS_DIR/scripts/lib/bash_scanner.py"
STATE_DB="${SWEBOK_STATE_DB:-$HARNESS_DIR/.swebok_state.db}"
MAX_STDIN_BYTES=1048576  # H7: 1 MiB

TOOL_NAME=""
COMMAND=""
DESCRIPTION=""

# Read JSON from stdin and extract fields using Python.
# FAIL-SECURE: malformed/empty input -> exit 1 (block the action).
# H7: rejects payloads > MAX_STDIN_BYTES.
read_json() {
    # H7: read stdin once so the size check and parse both work.
    local json_input
    json_input=$(cat)
    local stdin_size=${#json_input}
    if [[ "$stdin_size" -gt "$MAX_STDIN_BYTES" ]]; then
        echo "[BASH-GUARD] FATAL: stdin exceeds $MAX_STDIN_BYTES bytes (got $stdin_size). Blocking action."
        exit 1
    fi
    if [[ -z "$json_input" ]]; then
        echo "[BASH-GUARD] FATAL: empty stdin. Blocking action."
        exit 1
    fi
    local parsed
    if ! parsed=$(python3 -c "
import sys, json
try:
    raw = sys.stdin.read()
    d = json.loads(raw)
except Exception as e:
    print('PARSE_ERROR:' + str(e), file=sys.stderr)
    sys.exit(2)
if 'tool_name' not in d:
    print('SCHEMA_ERROR: missing tool_name', file=sys.stderr)
    sys.exit(3)
if 'tool_input' not in d and 'params' not in d:
    print('SCHEMA_ERROR: missing tool_input/params', file=sys.stderr)
    sys.exit(4)
ti = d.get('tool_input', d.get('params', {}))
# H2: include description so the scanner sees the full attacker-controlled text
print(d.get('tool_name','') + '\x1f' + ti.get('command','') + '\x1f' + ti.get('description',''))
" <<< "$json_input" 2>&1); then
        local exit_code=$?
        if [[ $exit_code -eq 2 ]]; then
            echo "[BASH-GUARD] FATAL: stdin is not valid JSON. Blocking action."
        elif [[ $exit_code -eq 3 || $exit_code -eq 4 ]]; then
            echo "[BASH-GUARD] FATAL: stdin JSON does not match hook contract. Blocking action."
        else
            echo "[BASH-GUARD] FATAL: stdin parse error (exit=$exit_code). Blocking action."
        fi
        exit 1
    fi
    TOOL_NAME="${parsed%%$'\x1f'*}"
    local rest="${parsed#*$'\x1f'}"
    COMMAND="${rest%%$'\x1f'*}"
    DESCRIPTION="${rest#*$'\x1f'}"
}

# Get current phase from state_engine.py
get_phase() {
    # M2: distinguish "phase is unset" (empty string) from "DB lookup
    # failed" (non-zero exit). The latter still defaults to P5 so the
    # harness keeps working when the DB is briefly unavailable.
    local phase
    if ! phase=$(python3 "$STATE_ENGINE" get "current_phase" 2>/dev/null); then
        echo "P5_CONSTRUCTION"
        return
    fi
    if [[ -z "${phase// }" ]]; then
        echo ""
    else
        echo "$phase"
    fi
}

# Main logic
main() {
    if [[ $# -eq 0 ]] || [[ "$1" == "__JSON__" ]]; then
        read_json
    else
        COMMAND="$1"
        TOOL_NAME="Bash"
    fi

    # C10: ANTI-ROT soft-block — if the dispatcher should run project-continuity
    # on this call, emit ANTI-ROT:NUDGE and exit 2. The hook contract treats
    # exit 2 as "the model should run project-continuity and re-attempt".
    cont=$(python3 "$STATE_ENGINE" should_run_continuity 2>/dev/null || echo "NO")
    if [[ "$cont" == "YES" ]]; then
        echo "ANTI-ROT:NUDGE run project-continuity (tool_call_count=multiple of 5)"
        exit 2
    fi

    # E1: structured log event
    python3 "$STATE_ENGINE" log_event INFO bash-guard "TOOL=$TOOL_NAME CMD=$COMMAND" "${CURRENT:-P?}" >/dev/null 2>&1 || true

    # AUDIT-2026-06-02 CI1 fix: ${VAR,,} is bash 4+ only (fails on macOS bash 3.2).
    # Use POSIX-portable tr instead.
    if [[ "$(echo "$TOOL_NAME" | tr '[:upper:]' '[:lower:]')" != "bash" ]]; then
        exit 0
    fi

    if [[ -z "$COMMAND" ]]; then
        exit 0
    fi

    if [[ ! -f "$STATE_DB" ]]; then
        echo "[BASH-GUARD] State DB missing - blocking for safety"
        exit 1
    fi

    local CURRENT
    CURRENT=$(get_phase)
    CURRENT=$(echo "$CURRENT" | tr -d ' ' | tr '[:lower:]' '[:upper:]')

    if [[ -z "$CURRENT" ]]; then
        echo "[BASH-GUARD] Phase unknown - blocking for safety"
        exit 1
    fi

    # H2: scan command + description (description is part of the attack surface)
    local SCAN_INPUT="$COMMAND"
    if [[ -n "$DESCRIPTION" ]]; then
        SCAN_INPUT="$COMMAND ; $DESCRIPTION"
    fi

    # Call Python bash_scanner - FAIL-SECURE: any error = block
    local scan_result
    scan_result=$(python3 "$BASH_SCANNER" "$CURRENT" "$SCAN_INPUT" 2>&1)
    local scan_exit=$?

    if [[ $scan_exit -ne 0 ]] || [[ -z "$scan_result" ]]; then
        echo "[BASH-GUARD] SCANNER_ERROR: Scanner failed (exit=$scan_exit) - blocking for safety"
        echo "[BASH-GUARD] Command: $COMMAND"
        exit 1
    fi

    # Trim whitespace from scan_result before comparison
    scan_result=$(echo "$scan_result" | tr -d '[:space:]')

    if [[ "$scan_result" != "NONE" ]]; then
        echo "[BASH-GUARD] BLOCKED: $scan_result in phase $CURRENT"
        echo "[BASH-GUARD] Command contained forbidden pattern"
        echo "[BASH-GUARD] Raw command: $COMMAND"
        exit 1
    fi

    exit 0
}

main "$@"