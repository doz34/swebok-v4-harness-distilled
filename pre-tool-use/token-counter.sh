#!/usr/bin/env bash
# SWEBOK v4 Harness - Pre-Tool-Use Token Counter
# Tracks live token usage per phase, enforces phase budget (base/soft/hard).
# AUDIT-2026-06-04: implements action #10 of P0 audit (token counter live, E1 strategy).
#
# Design:
#   - Reads current phase from state engine
#   - Estimates token cost of the incoming tool call (chars/4 heuristic)
#   - Adds to running total in state (key = ${PHASE}.tokens.used)
#   - Warns at soft cap, blocks at hard cap
#   - FAIL-OPEN: counter issues must NEVER block legitimate work

set -uo pipefail
# Fail-open on internal errors (counter is observability, not a security gate).
trap 'exit 0' ERR

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
STATE_ENGINE="$HARNESS_DIR/lib/state_engine.py"
STATE_DB="$HARNESS_DIR/.swebok_state.db"

# No DB or no engine → no-op (do not block)
if [[ ! -f "$STATE_DB" ]] || [[ ! -f "$STATE_ENGINE" ]]; then
    exit 0
fi

# Read stdin (Claude Code contract). Empty stdin = no tool input = no-op.
json_input=$(cat 2>/dev/null || true)
if [[ -z "${json_input}" ]]; then
    exit 0
fi

# Estimate tokens: full JSON payload / 4 chars per token (English/code heuristic).
# Min 1 token if any payload present. We do NOT try to compute exact LLM tokens
# (no tokenizer available); the estimate is good enough for budget gating.
tokens=$(HARNESS_DIR="$HARNESS_DIR" SWEBOK_STATE_DB="$SWEBOK_STATE_DB" python3 -c '
import json, sys
try:
    raw = sys.stdin.read()
    d = json.loads(raw)
    payload = json.dumps(d, ensure_ascii=False)
    print(max(1, len(payload) // 4))
except Exception:
    print(0)
' <<< "$json_input" 2>/dev/null || echo "0")
tokens=${tokens:-0}
if [[ "$tokens" -eq 0 ]]; then
    exit 0
fi

# Read current phase (default P0 if unset).
phase=$(HARNESS_DIR="$HARNESS_DIR" python3 "$STATE_ENGINE" get "current_phase" 2>/dev/null | tr '[:lower:]' '[:upper:]' | tr -d ' \n' || true)
phase=${phase:-P0}

# Budget lookup (must match spec v2 phase specs and strategy table).
# AUDIT-2026-06-05: structural fix — P3 split into P3 (Architecture) + P4 (Design),
# and renumbered cascade P5-P10. New P1 (Concept/Feasibility) added.
case "$phase" in
    P0|P0_DISCOVERY)              base=4000; soft=7000; hard=10000 ;;
    P1|P1_CONCEPT_FEASIBILITY)    base=3000; soft=5000; hard=8000  ;;
    P2|P2_REQUIREMENTS)           base=4000; soft=7000; hard=10000 ;;
    P3|P3_ARCHITECTURE)           base=5000; soft=8000; hard=15000 ;;
    P4|P4_DESIGN)                 base=5000; soft=8000; hard=15000 ;;
    P5|P5_IMPLEMENTATION)         base=5000; soft=10000; hard=15000;;
    P6|P6_TESTING)                base=5000; soft=8000; hard=15000 ;;
    P7|P7_DEPLOYMENT)             base=3000; soft=5000; hard=8000  ;;
    P8|P8_OPERATIONS)             base=2000; soft=4000; hard=6000  ;;
    P9|P9_MAINTENANCE)            base=3000; soft=5000; hard=8000  ;;
    P10|P10_RETIREMENT)           base=2000; soft=3000; hard=5000  ;;
    *)                            base=4000; soft=7000; hard=10000 ;;
esac

# Read running total for this phase.
key="${phase}.tokens.used"
current=$(HARNESS_DIR="$HARNESS_DIR" python3 "$STATE_ENGINE" get "$key" 2>/dev/null | tr -d ' \n' || echo "0")
current=${current:-0}
# Default to 0 if non-numeric (state can return empty string or JSON null).
if ! [[ "$current" =~ ^[0-9]+$ ]]; then
    current=0
fi

# Compute new total and persist.
new_total=$((current + tokens))
HARNESS_DIR="$HARNESS_DIR" python3 "$STATE_ENGINE" set "$key" "$new_total" 2>/dev/null || true

# Decide: warn or block. Block at hard cap (forced compaction required).
# Warn at soft cap and at 85% of hard cap.
if [[ $new_total -ge $hard ]]; then
    echo "[TOKEN-COUNTER] BLOCKED: $phase budget exhausted ($new_total/$hard tokens)."
    echo "[TOKEN-COUNTER] Forced compaction required before continuing."
    echo "[TOKEN-COUNTER] Reset: HARNESS_DIR=$HARNESS_DIR python3 $STATE_ENGINE set $key 0"
    exit 1
fi

if [[ $new_total -ge $((hard * 85 / 100)) ]]; then
    echo "[TOKEN-COUNTER] WARN: $phase budget 85% used ($new_total/$hard tokens, $((new_total * 100 / hard))%)."
    exit 0
fi

if [[ $new_total -ge $soft ]]; then
    echo "[TOKEN-COUNTER] WARN: $phase soft cap reached ($new_total/$soft tokens). Compaction recommended."
    exit 0
fi

# No threshold reached; silent success.
exit 0
