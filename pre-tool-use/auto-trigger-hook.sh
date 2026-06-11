#!/usr/bin/env bash
# SWEBOK v4 Harness — UserPromptSubmit Auto-Trigger Hook
# SPRINT-2026-06-10 G1: detect intent from user prompt → write intent.phase to state DB
#
# Fires on the UserPromptSubmit Claude Code hook event.
# Reads stdin JSON (Claude Code contract), extracts prompt, calls lib/auto_trigger.py,
# parses DSL output, writes intent.phase to state DB if confidence >= 0.5.
#
# FAIL-OPEN: never blocks legitimate work.
# KILL-SWITCH: set HARNESS_AUTO_TRIGGER=0 to disable globally.

set -uo pipefail
# FAIL-OPEN: never block, even on internal error
trap 'echo "[AUTO-TRIGGER] WARN: internal error, continuing" >&2; exit 0' ERR

# KILL-SWITCH check
if [[ "${HARNESS_AUTO_TRIGGER:-1}" == "0" ]]; then
    echo "[AUTO-TRIGGER] disabled via HARNESS_AUTO_TRIGGER=0" >&2
    exit 0
fi

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
STATE_CLI="$HARNESS_DIR/lib/state_engine_cli.py"
AUTO_TRIGGER="$HARNESS_DIR/lib/auto_trigger.py"

# Sanity checks
if [[ ! -f "$AUTO_TRIGGER" ]]; then
    echo "[AUTO-TRIGGER] lib/auto_trigger.py not found at $AUTO_TRIGGER" >&2
    exit 0
fi
if [[ ! -f "$STATE_CLI" ]]; then
    echo "[AUTO-TRIGGER] state_engine_cli.py not found at $STATE_CLI" >&2
    exit 0
fi

# Read stdin JSON (Claude Code contract)
json_input=""
if read -r -t 2 -d '' json_input < /dev/stdin 2>/dev/null || true; then
    :
fi

# Extract prompt from various possible fields
prompt=""
if [[ -n "$json_input" ]]; then
    prompt=$(echo "$json_input" | HARNESS_DIR="$HARNESS_DIR" python3 -c "
import sys, json
try:
    raw = sys.stdin.read()
    d = json.loads(raw)
    # Try various field names Claude Code might use
    for key in ('prompt', 'user_prompt', 'message', 'text', 'content'):
        if key in d and isinstance(d[key], str):
            print(d[key])
            sys.exit(0)
    # Nested
    for parent in ('tool_input', 'params', 'input'):
        if parent in d and isinstance(d[parent], dict):
            for key in ('prompt', 'user_prompt', 'message'):
                if key in d[parent] and isinstance(d[parent][key], str):
                    print(d[parent][key])
                    sys.exit(0)
except Exception:
    pass
" 2>/dev/null || true)
fi

# No prompt → silent no-op
if [[ -z "$prompt" ]]; then
    exit 0
fi

# Call auto_trigger.py — it writes to state DB itself if confidence >= 0.5
result=$(HARNESS_DIR="$HARNESS_DIR" python3 "$AUTO_TRIGGER" "$prompt" 2>/dev/null || true)

# Parse DSL output for logging
phase=$(echo "$result" | grep -oP "phase=\K[A-Z0-9]+" | head -1)
conf=$(echo "$result" | grep -oP "confidence=\K[0-9.]+" | head -1)
layer=$(echo "$result" | grep -oP "fallback=\K[A-Z0-9]+" | head -1)

# Log for observability
echo "[AUTO-TRIGGER] prompt='${prompt:0:60}...' phase=${phase:-P0} confidence=${conf:-0.0} layer=${layer:-L4}" >&2

exit 0
