#!/usr/bin/env bash
# SWEBOK v4 Harness — Mini-Council Hook
# SPRINT-2026-06-10 G6: PostToolUse for Write/Edit.
# Calls 1 Haiku judge (or offline heuristic) per non-whitelist edit.
# Tracks last 3 findings; if 1+ VULN → escalate to full Council.
#
# FAIL-OPEN: never blocks.
# KILL-SWITCH: HARNESS_AUTO_TRIGGER=0 disables.

set -uo pipefail
trap 'echo "[MINI-COUNCIL] WARN: internal error, continuing" >&2; exit 0' ERR

if [[ "${HARNESS_AUTO_TRIGGER:-1}" == "0" ]]; then
    exit 0
fi

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
MINI_COUNCIL="$HARNESS_DIR/lib/adv-loop/mini_council.py"

if [[ ! -f "$MINI_COUNCIL" ]]; then
    exit 0
fi

# Read stdin JSON
json_input=$(cat 2>/dev/null || true)

# Extract file_path (top-level OR nested)
file_path=""
if [[ -n "$json_input" ]]; then
    file_path=$(echo "$json_input" | HARNESS_DIR="$HARNESS_DIR" python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    for k in ('file_path', 'notebook_path'):
        if k in d and isinstance(d[k], str) and d[k]:
            print(d[k])
            sys.exit(0)
    for parent in ('tool_input', 'params', 'input'):
        if parent in d and isinstance(d[parent], dict):
            for k in ('file_path', 'notebook_path'):
                if k in d[parent] and isinstance(d[parent][k], str) and d[parent][k]:
                    print(d[parent][k])
                    sys.exit(0)
except Exception:
    pass
" 2>/dev/null || true)
fi

if [[ -z "$file_path" ]]; then
    exit 0
fi

# Call mini_council
HARNESS_DIR="$HARNESS_DIR" python3 "$MINI_COUNCIL" on-edit "$file_path" 2>&1 || true

exit 0
