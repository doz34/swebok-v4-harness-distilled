#!/usr/bin/env bash
# SWEBOK v4 Harness - PreToolUse Phase Guard
# Blocks Write/Edit if phase constraints violated
# FAIL-SECURE: trap 'exit 1' ERR
#
# v1.4.1+ changes:
#   H7: stdin size limited to 1MB
#   H8: HARNESS_DIR validated at startup
#   M1: empty tool_input blocked (decision:block JSON)
#   M2: empty phase blocks (was exit 0)
#   M29: file_path canonicalized via realpath -m
#   C10: ANTI-ROT soft-block (exit 2 with ANTI-ROT:NUDGE) on every 5th call
#   L2: tool name normalized to lowercase

set -euo pipefail
# FAIL-SECURE: block on any internal error (crash, missing deps, etc.)
trap 'echo "WARN:HOOK_INTERNAL_ERROR: Blocking action due to script crash"; exit 1' ERR

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
# H8: refuse to run against a non-harness HARNESS_DIR
if [[ ! -d "$HARNESS_DIR" ]] || [[ ! -d "$HARNESS_DIR/scripts/lib" ]]; then
    echo "[PHASE-GUARD] FATAL: HARNESS_DIR=$HARNESS_DIR is not a SWEBOK harness checkout."
    exit 1
fi
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
BASH_SCANNER="$HARNESS_DIR/scripts/lib/bash_scanner.py"
STATE_DB="${SWEBOK_STATE_DB:-$HARNESS_DIR/.swebok_state.db}"
MAX_STDIN_BYTES=1048576  # H7: 1 MiB

# === FAIL-SECURE BOOTSTRAP ===
# If state DB is missing (fresh clone), auto-bootstrap before proceeding.
# This ensures the hook NEVER fails due to a missing database.
if [[ ! -f "$STATE_DB" ]]; then
    BOOTSTRAP_SCRIPT="$HARNESS_DIR/scripts/swebok-bootstrap.sh"
    if [[ -f "$BOOTSTRAP_SCRIPT" ]]; then
        echo "[PHASE-GUARD] State DB missing. Auto-running swebok-bootstrap.sh..."
        bash "$BOOTSTRAP_SCRIPT" >/dev/null 2>&1 || {
            echo "[PHASE-GUARD] BOOTSTRAP_FAILED: bootstrap script errored. Blocking for safety."
            exit 1
        }
    else
        echo "[PHASE-GUARD] State DB missing and bootstrap script absent. Blocking for safety."
        exit 1
    fi
fi

TOOL_NAME=""
FILE_PATH=""
COMMAND=""

# M29: canonicalize a file path so ../ traversal cannot bypass the
# phase guards. realpath -m never errors on missing components. If
# realpath fails for any reason (permission, ENOENT, etc.) fall back to
# the original path but log a warning so operators know the bypass
# gate was not enforced for this call. This is fail-safe-by-fallback:
# the phase check still runs, just on the un-canonicalized input.
canonicalize_path() {
    local p="$1"
    if [[ -z "$p" ]]; then
        echo ""
        return
    fi
    local out
    if out=$(realpath -m -- "$p" 2>/dev/null); then
        echo "$out"
    else
        echo "[PHASE-GUARD] WARN: realpath failed for '$p'; falling back to original (M29 race-safe fallback)" >&2
        echo "$p"
    fi
}

# Read JSON from stdin and extract fields using Python.
# FAIL-SECURE: malformed/empty input -> exit 1 (block the action).
# M1: distinguishes empty tool_input dict (block) from tool that simply
# has no file_path (allow).
# H7: rejects payloads > MAX_STDIN_BYTES.
read_json() {
    # H7: read stdin into a buffer once so we can both check its size
    # and parse it. wc -c would consume the stream and leave cat with
    # nothing, so we read once and use ${#json_input} for the size test.
    local json_input
    json_input=$(cat)
    local stdin_size=${#json_input}
    if [[ "$stdin_size" -gt "$MAX_STDIN_BYTES" ]]; then
        echo "[PHASE-GUARD] FATAL: stdin exceeds $MAX_STDIN_BYTES bytes (got $stdin_size). Blocking action."
        exit 1
    fi
    # Reject empty input explicitly
    if [[ -z "$json_input" ]]; then
        echo "[PHASE-GUARD] FATAL: empty stdin. Blocking action."
        exit 1
    fi
    # Single Python invocation; non-zero exit on any parse error OR
    # if the JSON doesn't match the Claude Code hook contract (must have
    # 'tool_name' and one of 'tool_input'/'params').
    local parsed
    if ! parsed=$(python3 -c "
import sys, json
try:
    raw = sys.stdin.read()
    d = json.loads(raw)
except Exception as e:
    print('PARSE_ERROR:' + str(e), file=sys.stderr)
    sys.exit(2)
# Contract validation: refuse unknown schemas
if 'tool_name' not in d:
    print('SCHEMA_ERROR: missing tool_name', file=sys.stderr)
    sys.exit(3)
if 'tool_input' not in d and 'params' not in d:
    print('SCHEMA_ERROR: missing tool_input/params', file=sys.stderr)
    sys.exit(4)
ti = d.get('tool_input', d.get('params', {}))
# M1: an explicit empty {} tool_input is malformed and must be blocked.
if not isinstance(ti, dict) or len(ti) == 0:
    print('EMPTY_TOOL_INPUT: tool_input/params is empty', file=sys.stderr)
    sys.exit(5)
# NotebookEdit uses 'notebook_path' instead of 'file_path'. Map both.
file_path = ti.get('file_path','') or ti.get('notebook_path','')
# Other tools may carry useful audit data: subject (Task), prompt (Agent), command (Skill)
audit_extra = ti.get('command','') or ti.get('subject','') or ti.get('prompt','') or ti.get('url','') or ti.get('query','')
print(d.get('tool_name','') + '\x1f' + file_path + '\x1f' + audit_extra)
" <<< "$json_input" 2>&1); then
        local exit_code=$?
        if [[ $exit_code -eq 2 ]]; then
            echo "[PHASE-GUARD] FATAL: stdin is not valid JSON. Blocking action."
        elif [[ $exit_code -eq 3 || $exit_code -eq 4 ]]; then
            echo "[PHASE-GUARD] FATAL: stdin JSON does not match hook contract. Blocking action."
        elif [[ $exit_code -eq 5 ]]; then
            # M1: structured decision JSON
            echo '{\"decision\":\"block\",\"reason\":\"EMPTY_TOOL_INPUT\"}'
        else
            echo "[PHASE-GUARD] FATAL: stdin parse error (exit=$exit_code). Blocking action."
        fi
        exit 1
    fi
    # Split on unit-separator
    TOOL_NAME="${parsed%%$'\x1f'*}"
    local rest="${parsed#*$'\x1f'}"
    FILE_PATH="${rest%%$'\x1f'*}"
    COMMAND="${rest#*$'\x1f'}"
    # M29: canonicalize file_path so ../../src/x.py cannot bypass checks.
    FILE_PATH=$(canonicalize_path "$FILE_PATH")
    # L2: normalize tool name to lowercase.
    TOOL_NAME=$(echo "$TOOL_NAME" | tr '[:upper:]' '[:lower:]')
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
    # If the value is explicitly empty (or only whitespace), emit empty
    # so the caller can detect "phase unknown" and block.
    if [[ -z "${phase// }" ]]; then
        echo ""
    else
        echo "$phase"
    fi
}

# Increment blocked counter
do_increment_blocked() {
    python3 "$STATE_ENGINE" increment_blocked 2>/dev/null || echo "0"
}

# Set last blocked file
do_set_blocked_file() {
    python3 "$STATE_ENGINE" set "circuit_breaker.last_blocked_file" "$1" 2>/dev/null || true
}

# Get blocked attempts count
get_blocked_count() {
    python3 "$STATE_ENGINE" get "circuit_breaker.blocked_attempts" 2>/dev/null || echo "0"
}

# Get override status with timeout check (max 5 minutes)
get_override() {
    local override_active
    override_active=$(python3 "$STATE_ENGINE" get "circuit_breaker.override_active" 2>/dev/null || echo "False")

    if [[ "$override_active" == "True" ]]; then
        local override_timestamp
        override_timestamp=$(python3 "$STATE_ENGINE" get "circuit_breaker.override_timestamp" 2>/dev/null || echo "0")
        local now
        now=$(date +%s)
        local age=$((now - override_timestamp))
        local MAX_OVERRIDE_AGE=300  # 5 minutes

        if [[ "$override_timestamp" != "0" ]] && [[ $age -gt $MAX_OVERRIDE_AGE ]]; then
            echo "[PHASE-GUARD] Override expired after ${age}s. Resetting."
            reset_circuit_breaker
            echo "False"
            return
        fi
    fi

    echo "$override_active"
}

# Activate override with timestamp
activate_override() {
    python3 "$STATE_ENGINE" set "circuit_breaker.override_active" "true" 2>/dev/null || true
    python3 "$STATE_ENGINE" set "circuit_breaker.override_timestamp" "$(date +%s)" 2>/dev/null || true
}

# Reset circuit breaker
reset_circuit_breaker() {
    python3 "$STATE_ENGINE" set "circuit_breaker.blocked_attempts" "0" 2>/dev/null || true
    python3 "$STATE_ENGINE" set "circuit_breaker.override_active" "false" 2>/dev/null || true
}

# Main logic
main() {
    if [[ $# -eq 0 ]] || [[ "$1" == "__JSON__" ]]; then
        read_json
    else
        FILE_PATH="$1"
        TOOL_NAME="${2:-Write}"
        FILE_PATH=$(canonicalize_path "$FILE_PATH")
        TOOL_NAME=$(echo "$TOOL_NAME" | tr '[:upper:]' '[:lower:]')
    fi

    # C10: ANTI-ROT soft-block — if the dispatcher should run project-continuity
    # on this call, emit ANTI-ROT:NUDGE and exit 2. The hook contract treats
    # exit 2 as "the model should run project-continuity and re-attempt".
    #
    # AUDIT-2026-06-01 FIX: defer ANTI-ROT to AFTER the block decision so a
    # genuine phase block is not swallowed by the nudge. The nudge only fires
    # when the action would otherwise have been ALLOWED. Save the cont flag
    # for later use after we've computed the block decision.
    cont=$(python3 "$STATE_ENGINE" should_run_continuity 2>/dev/null || echo "NO")
    # (intentionally NOT exiting here — see end of main() for deferred nudge)

    # E1: structured log event
    python3 "$STATE_ENGINE" log_event INFO phase-guard "TOOL=$TOOL_NAME PATH=$FILE_PATH" "${CURRENT:-P?}" >/dev/null 2>&1 || true

    if [[ ! -f "$STATE_DB" ]]; then
        echo "[PHASE-GUARD] State DB not found. Blocking for safety."
        exit 1
    fi

    # AUDIT-2026-06-01 FIX (CRIT-CISO-3): previously, an empty FILE_PATH and
    # empty COMMAND together caused a silent `exit 0`. For Skill/Task/Agent
    # invocations whose payload is `{prompt: ...}` or `{subagent_type: ...}`,
    # this meant the harness saw NOTHING and let the call through with no
    # audit. Now: write an explicit ALLOWED log row so the call is at least
    # traced, AND attempt to capture the payload (prompt/subject) for the
    # adversarial replay.
    if [[ -z "$FILE_PATH" ]] && [[ -z "$COMMAND" ]]; then
        # Log the bare-tool invocation so it's not invisible. The audit row
        # is best-effort — a state-engine failure here does not block the
        # action (we don't want a logging issue to stop legitimate Skill
        # calls), but it does surface in stderr if it fails.
        python3 "$STATE_ENGINE" log_event INFO phase-guard \
            "no-payload tool invocation: $TOOL_NAME" "${CURRENT:-UNKNOWN}" \
            2>/dev/null || true
        exit 0
    fi

    local CURRENT
    CURRENT=$(get_phase)
    CURRENT=$(echo "$CURRENT" | tr -d ' ' | tr '[:lower:]' '[:upper:]')

    # M2: empty phase string must block (was previously exit 0)
    if [[ -z "$CURRENT" ]]; then
        echo "[PHASE-GUARD] Phase unknown - blocking for safety"
        exit 1
    fi

    local PHASE_NUM=""
    if [[ "$CURRENT" =~ ^P([0-9]+) ]]; then
        PHASE_NUM="${BASH_REMATCH[1]}"
    else
        PHASE_NUM="${CURRENT:1}"
    fi
    local SHOULD_BLOCK="false"
    local BLOCK_REASON=""

    # === P1/P2: No code allowed ===
    if [[ "$PHASE_NUM" =~ ^[12]$ ]]; then
        if [[ "$TOOL_NAME" =~ ^(write|edit|multiedit|notebookedit)$ ]]; then
            if [[ "$FILE_PATH" =~ \.(py|ts|js|go|java|c|cpp|rs|rb|php|swift|kt|ipynb)$ ]]; then
                SHOULD_BLOCK="true"
                BLOCK_REASON="Phase=$CURRENT. Code forbidden in P1/P2. Requirements only."
            fi
        fi
    fi

    # === P3/P4: No implementation allowed ===
    if [[ "$PHASE_NUM" =~ ^[34]$ ]]; then
        if [[ "$TOOL_NAME" =~ ^(write|edit|multiedit|notebookedit)$ ]]; then
            if [[ "$FILE_PATH" =~ (/src/|/impl/|/implementations/|src/|impl/|implementations/) ]]; then
                SHOULD_BLOCK="true"
                BLOCK_REASON="Phase=$CURRENT. Implementation forbidden. Design phase."
            elif [[ "$FILE_PATH" =~ (_impl\.|_implementation\.|\.impl\.) ]]; then
                SHOULD_BLOCK="true"
                BLOCK_REASON="Phase=$CURRENT. Implementation file blocked."
            fi
        fi
    fi

    # === P6: Testing only - no new implementation ===
    if [[ "$PHASE_NUM" == "6" ]]; then
        if [[ "$TOOL_NAME" =~ ^(write|edit|multiedit|notebookedit)$ ]]; then
            if [[ "$FILE_PATH" =~ (/src/|^src/) ]] && [[ ! "$FILE_PATH" =~ (test|spec|__tests__|tests?/) ]]; then
                SHOULD_BLOCK="true"
                BLOCK_REASON="Phase=P6. New implementation forbidden. QA phase."
            fi
        fi
    fi

    # === P9: Retirement phase - only /archived/ or /docs/ allowed ===
    if [[ "$PHASE_NUM" == "9" ]]; then
        if [[ "$TOOL_NAME" =~ ^(write|edit|multiedit|notebookedit)$ ]]; then
            if [[ "$FILE_PATH" =~ (/src/|/lib/) ]] && [[ ! "$FILE_PATH" =~ (/archived/|/docs/) ]]; then
                SHOULD_BLOCK="true"
                BLOCK_REASON="Phase=P9. Only /archived/ or /docs/ allowed. Retirement phase."
            fi
        fi
    fi

    # === CIRCUIT BREAKER LOGIC ===
    if [[ "$SHOULD_BLOCK" == "true" ]]; then
        do_increment_blocked
        do_set_blocked_file "$FILE_PATH"

        local blocked_count
        blocked_count=$(get_blocked_count)
        local override_active
        override_active=$(get_override)

        # AUDIT-2026-06-01 FIX (CRIT-1): previously, 3 blocks would `exit 0`
        # (FAIL-OPEN) and grant a 5-min override window during which every
        # blocked action was allowed. That is the inverse of a security gate.
        # Now: 3 blocks → HARD LOCK with exit 1 + operator-actionable log line.
        # The override flag is kept ONLY for explicit operator-set unblock
        # (a manual `state_engine set circuit_breaker.override_active true`),
        # never automatically activated from the hook itself.
        if [[ "$blocked_count" -ge 3 ]] && [[ "$override_active" != "True" ]]; then
            echo "[PHASE-GUARD] LOCKED: $blocked_count blocked attempts on $FILE_PATH in phase $CURRENT"
            echo "[PHASE-GUARD] To unblock manually (operator action):"
            echo "[PHASE-GUARD]   python3 $STATE_ENGINE set circuit_breaker.override_active true"
            echo "[PHASE-GUARD] Block reason: $BLOCK_REASON"
            exit 1
        fi

        if [[ "$override_active" == "True" ]]; then
            # Operator-set override is still honored, but with a loud log line
            # so it is visible in the transcript.
            echo "[PHASE-GUARD] OPERATOR_OVERRIDE_ACTIVE: Allowing $TOOL_NAME on $FILE_PATH (would have blocked: $BLOCK_REASON)"
            exit 0
        fi

        echo "[PHASE-GUARD] BLOCKED: $BLOCK_REASON"
        echo "[PHASE-GUARD] Blocked attempts: $blocked_count/3"
        exit 1
    else
        local blocked_count
        blocked_count=$(get_blocked_count)
        if [[ "$blocked_count" -gt 0 ]]; then
            reset_circuit_breaker
            echo "[PHASE-GUARD] Circuit breaker reset."
        fi

        # AUDIT-2026-06-01 FIX: deferred ANTI-ROT nudge — only fires when the
        # action would have been allowed. A block never gets swallowed.
        # AUDIT-2026-06-02 FIX (ADR-003 / G.2): structured nudge format. The
        # dispatcher can parse `KEY=VALUE` pairs deterministically and decide
        # whether to invoke the named skill. The harness itself never invokes.
        if [[ "${cont:-NO}" == "YES" ]]; then
            local tcc
            tcc=$(python3 "$STATE_ENGINE" get tool_call_count 2>/dev/null || echo "0")
            echo "ANTI-ROT:NUDGE skill=project-continuity reason=tool_call_count_multiple_of_5 tool_call_count=${tcc}"
            exit 2
        fi

        echo "[PHASE-GUARD] ALLOWED: $TOOL_NAME on $FILE_PATH in phase $CURRENT"
        exit 0
    fi
}

main "$@"