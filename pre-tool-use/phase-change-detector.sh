#!/usr/bin/env bash
# SWEBOK v4 Harness — Phase Change Detector
# SPRINT-2026-06-10 G3: detect intent.phase vs current_phase diff
# → emit <MULTIAGENT_LAUNCH> envelope to fire adversarial-gate --council.
#
# Fires on PreToolUse for Write/Edit/MultiEdit.
# Reads intent.phase from .swebok_state.db (set by auto-trigger-hook.sh).
# Compares with current_phase. If diff: emits envelope, updates current_phase,
# appends to phase_history[] (FIFO 10).
#
# FAIL-OPEN: never blocks legitimate work.
# KILL-SWITCH: HARNESS_AUTO_TRIGGER=0 disables globally.

set -uo pipefail
trap 'echo "[PHASE-DIFF] WARN: internal error, continuing" >&2; exit 0' ERR

if [[ "${HARNESS_AUTO_TRIGGER:-1}" == "0" ]]; then
    exit 0
fi

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
STATE_CLI="$HARNESS_DIR/lib/state_engine_cli.py"

if [[ ! -f "$STATE_CLI" ]]; then
    exit 0
fi

# Read intent.phase and current_phase from state DB
intent_phase=$(HARNESS_DIR="$HARNESS_DIR" python3 "$STATE_CLI" get_nested intent.phase 2>/dev/null || true)
current_phase=$(HARNESS_DIR="$HARNESS_DIR" python3 "$STATE_CLI" get current_phase 2>/dev/null || echo "P0")

# Sanity: if intent.phase is empty or invalid, no-op
if [[ -z "$intent_phase" ]] || [[ ! "$intent_phase" =~ ^P[0-9]+(_[A-Z_]+)?$ ]]; then
    exit 0
fi

# Sanity: if current_phase is unset, init to P0
if [[ -z "$current_phase" ]] || [[ ! "$current_phase" =~ ^P[0-9]+(_[A-Z_]+)?$ ]]; then
    current_phase="P0"
fi

# No diff → no-op
if [[ "$intent_phase" == "$current_phase" ]]; then
    exit 0
fi

# Phase change detected: emit envelope
echo "[PHASE-DIFF] phase change: ${current_phase} → ${intent_phase}" >&2

# Update current_phase
HARNESS_DIR="$HARNESS_DIR" python3 "$STATE_CLI" set current_phase "$intent_phase" 2>/dev/null || true

# Append to phase_history[] (FIFO 10)
HARNESS_DIR="$HARNESS_DIR" python3 "$STATE_CLI" list_append phase.history "$intent_phase" 10 2>/dev/null || true

# Emit <MULTIAGENT_LAUNCH> envelope to stderr (dispatcher reads)
# The envelope tells the dispatcher to spawn 4 LLM-judges via Agent tool.
cat >&2 <<EOF
## <MULTIAGENT_LAUNCH phase="$intent_phase" reason="phase_change" from="$current_phase">

SPRINT-2026-06-10 G3: phase changed from $current_phase to $intent_phase.
Spawn 4 LLM-judges via Agent tool (subagent_type: nexus-ciso, nexus-qa-lead, nexus-architect, nexus-devops-lead) per CLAUDE.md L6.1 / ADR-003.
After collecting 4 DSL lines, run:
  bash scripts/adversarial-gate.sh $current_phase $intent_phase --judge-only --red "<aggregated RED>" --blue "<aggregated BLUE>"

Roles:
- nexus-ciso:        RED: VULN:CRIT;;LOC:phase_boundary;;TYPE:drift;;FIX_REQ:...
- nexus-qa-lead:     BLUE: DEFENDED;;NORMS:KA-11;;STATUS:OK
- nexus-architect:   BLUE: DEFENDED;;NORMS:KA-2+KA-1;;STATUS:OK
- nexus-devops-lead: RED: VULN:HIGH;;LOC:OPS;;TYPE:transition;;FIX_REQ:...

Expected DSL output: KEY=VALUE;;KEY=VALUE;;adv_loop:verdict=🟢|🟡|🔴
EOF

exit 0
