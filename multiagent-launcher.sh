#!/usr/bin/env bash
# SWEBOK v4 Harness - Multiagent Launcher (MCP-WIRED)
# Parallel execution via Claude Code native multiagent tool
# Usage: ./multiagent-launcher.sh <task_type> [args]
# This script outputs Agent tool calls for parallel execution

set -euo pipefail

TASK_TYPE="$1"
shift
ARGS="$@"
HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
# State of truth: .swebok_state.db. STATE_FILE kept only for diagnostic reads
# of the deprecated YAML (do NOT add new code paths that use it).
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"

DSL_PREFIX="MULTIAGENT"

log_dsl() {
    # Operator-facing diagnostic lines go to STDERR so STDOUT stays clean
    # for the data stream (JSONL for emit-prompts, <MULTIAGENT_LAUNCH>
    # envelope for emit-envelope). This is required for the gate's
    # well-formed envelope check to succeed.
    echo "[$DSL_PREFIX] $1" >&2
}

# === LAUNCH PARALLEL AGENTS VIA AGENT TOOL ===
launch_parallel_agents() {
    local task_type="$1"
    shift
    local agent_specs=("$@")

    log_dsl "LAUNCH: $task_type"
    log_dsl "Agents: ${#agent_specs[@]}"

    for spec in "${agent_specs[@]}"; do
        log_dsl "  AGENT: $spec"
    done
}

# === TASK CONFIGS ===
case "$TASK_TYPE" in
    emit-envelope)
        # AUDIT-2026-06-02 (ADR-003 / G.3) — FIX (Architect F-02):
        # the launcher is the SINGLE OWNER of the bridge envelope. This task
        # emits the full <MULTIAGENT_LAUNCH> wrapper + JSONL body + close tag.
        # The gate just calls us and prints whatever we produce. This closes
        # the "envelope split across two files" finding from the Architect.
        FROM_P="${1:-P5}"
        TO_P="${2:-P6}"
        # FIX (Architect F-04 / DevOps F-DO-08): extract full phase digits so
        # P10/P11 don't silently truncate to P1 in the SWEBOK KA references.
        if [[ "$FROM_P" =~ ^P([0-9]+)$ ]]; then
            PHASE_NUM="${BASH_REMATCH[1]}"
        else
            echo "[LAUNCHER] FATAL: emit-envelope FROM_P must match ^P[0-9]+$ (got '$FROM_P')" >&2
            exit 1
        fi
        if [[ ! "$TO_P" =~ ^P[0-9]+$ ]]; then
            echo "[LAUNCHER] FATAL: emit-envelope TO_P must match ^P[0-9]+$ (got '$TO_P')" >&2
            exit 1
        fi
        # Emit the wrapper, then the JSONL body (via emit-prompts), then close.
        # Subshell captures body to a variable so any emit-prompts stderr stays
        # on the launcher's stderr (gate captures it via 2>file, no swallow).
        BODY="$(bash "$0" emit-prompts "$FROM_P" "$TO_P" "$PHASE_NUM")"
        BODY_EXIT=$?
        if [[ $BODY_EXIT -ne 0 ]]; then
            echo "[LAUNCHER] FATAL: emit-prompts exited $BODY_EXIT" >&2
            exit $BODY_EXIT
        fi
        if [[ -z "$BODY" ]]; then
            echo "[LAUNCHER] FATAL: emit-prompts returned an empty body" >&2
            exit 1
        fi
        echo "<MULTIAGENT_LAUNCH gate=\"${FROM_P}_EXIT\" target=\"$TO_P\">"
        echo "$BODY"
        echo "</MULTIAGENT_LAUNCH>"
        ;;

    emit-prompts)
        # AUDIT-2026-06-02 (ADR-003 / G.3): real council bridge.
        # Emit one JSON line per reviewer role on STDOUT. The dispatcher
        # reads each line, spawns the named subagent_type via Agent tool,
        # collects the DSL output, and calls adversarial-gate.sh
        # --judge-only --red <RED_DSL> --blue <BLUE_DSL>.
        FROM_P="${1:-P5}"
        TO_P="${2:-P6}"
        # PHASE_NUM passed by emit-envelope (validated ^P[0-9]+$ upstream).
        # Default to single digit for direct invocations (back-compat).
        PHASE_NUM="${3:-${FROM_P#P}}"
        # Use python3 for JSON-safe escaping; no jq dependency.
        python3 - "$FROM_P" "$TO_P" "$PHASE_NUM" <<'PY_EOF'
import json, sys
from_p, to_p, phase_num = sys.argv[1], sys.argv[2], sys.argv[3]
roles = [
    {
        "role": "ciso",
        "subagent_type": "nexus-ciso",
        "prompt": (
            f"You are an INDEPENDENT CISO reviewing the gate transition "
            f"{from_p} → {to_p}. Read the harness state via "
            f"`python3 scripts/lib/state_engine.py export_state` and the "
            f"last 50 adversarial_log rows via `query_adversarial 50`. "
            f"Produce a SINGLE DSL line with these keys: "
            f"RED: VULN:<CRIT|HIGH|MED|LOW>;;LOC:<location>;;TYPE:<vulnerability_type>;;FIX_REQ:<required_fix>. "
            f"Default: VULN:LOW if no findings."
        ),
        "expected_dsl_keys": ["RED:VULN", "RED:LOC", "RED:TYPE", "RED:FIX_REQ"],
    },
    {
        "role": "qa-lead",
        "subagent_type": "nexus-qa-lead",
        "prompt": (
            f"You are an INDEPENDENT QA Lead reviewing the gate transition "
            f"{from_p} → {to_p}. Run `bash tests/adversarial-test.sh` and "
            f"`bash tests/attack-payloads-test.sh`. Produce a SINGLE DSL "
            f"line: BLUE: DEFENDED;;NORMS:KA-{phase_num}+KA-11;;STATUS:<OK|FAIL>. "
            f"STATUS:OK if all tests PASS, else STATUS:FAIL."
        ),
        "expected_dsl_keys": ["BLUE:DEFENDED", "BLUE:NORMS", "BLUE:STATUS"],
    },
    {
        "role": "architect",
        "subagent_type": "nexus-architect",
        "prompt": (
            f"You are an INDEPENDENT principal architect reviewing the gate "
            f"transition {from_p} → {to_p}. Read docs/v1/ARCHITECTURE.md and "
            f"the recent state_events. Check for spec-vs-code drift. Produce "
            f"a SINGLE DSL line: BLUE: DEFENDED;;NORMS:KA-{phase_num}+KA-2;;STATUS:<OK|FAIL>."
        ),
        "expected_dsl_keys": ["BLUE:DEFENDED", "BLUE:NORMS", "BLUE:STATUS"],
    },
    {
        "role": "devops-lead",
        "subagent_type": "nexus-devops-lead",
        "prompt": (
            f"You are an INDEPENDENT DevOps Lead reviewing the gate transition "
            f"{from_p} → {to_p}. Run `bash scripts/health-check.sh` and check "
            f"hook latency. Produce a SINGLE DSL line: "
            f"RED: VULN:<sev>;;LOC:OPS;;TYPE:<reliability_issue>;;FIX_REQ:<fix> "
            f"OR BLUE: DEFENDED;;NORMS:KA-7;;STATUS:OK if no issues."
        ),
        "expected_dsl_keys": ["RED:VULN", "BLUE:STATUS"],
    },
]
for r in roles:
    print(json.dumps(r))
PY_EOF
        ;;

    e2e_parallel)
        log_dsl "TASK: e2e_parallel (API + Browser Use)"
        log_dsl ""
        log_dsl "=== AGENT CALLS ==="
        echo "AGENT:nexus-backend|TASK:api_integration_tests|PARALLEL:true"
        echo "AGENT:nexus-frontend|TASK:browser_e2e_scenarios|PARALLEL:true"
        echo ""
        echo "# To execute, run these Agent calls in parallel:"
        echo 'Agent(--description:"API Integration Tests", --prompt:"Run API integration tests against $APP_URL. Verify all endpoints return expected status codes. Report: PASS/FAIL per endpoint.", --subagent_type:"general-purpose", --run_in_background:true)'
        echo 'Agent(--description:"Browser Use E2E", --prompt:"Execute Browser Use E2E scenarios from $SCENARIO_FILE against $APP_URL. Use act-observe-verify loop. Report: PASS/FAIL per step.", --subagent_type:"general-purpose", --run_in_background:true)'
        ;;

    security_scan)
        log_dsl "TASK: security_scan (Red + Blue)"
        log_dsl ""
        echo "AGENT:nexus-security|MODE:offensive|TASK:penetration_test"
        echo "AGENT:nexus-ciso|MODE:defensive|TASK:security_review"
        echo ""
        echo "# To execute:"
        echo 'Agent(--description:"Offensive Security (Red Team)", --prompt:"Perform offensive security testing: SQL injection, XSS, CSRF, auth bypass. Target: $APP_URL. Report findings in DSL: VULN:CRIT|HIGH|MED|LOW.", --subagent_type:"general-purpose", --run_in_background:true)'
        echo 'Agent(--description:"Defensive Security (Blue Team)", --prompt:"Review security controls: auth, encryption, input validation, session management. Target: $APP_URL. Report in DSL: DEFENDED|NORMS:KA-13|STATUS:OK.", --subagent_type:"general-purpose", --run_in_background:true)'
        ;;

    architecture_review)
        log_dsl "TASK: architecture_review (Architect + CTO)"
        log_dsl ""
        echo "AGENT:nexus-architect|TASK:design_review"
        echo "AGENT:nexus-cto|TASK:strategic_review"
        echo ""
        echo "# To execute:"
        echo 'Agent(--description:"Architecture Review", --prompt:"Review architecture in $HARNESS_DIR. Check C4 diagrams, interface definitions, non-functional requirements. Report in DSL: NORMS:KA-2+KA-13|STATUS:OK.", --subagent_type:"general-purpose", --run_in_background:true)'
        echo 'Agent(--description:"CTO Strategic Review", --prompt:"Review technical strategy in $HARNESS_DIR. Assess alignment with business goals, scalability, tech debt. Report in DSL: STRATEGIC:OK|WARNINGS:...", --subagent_type:"general-purpose", --run_in_background:true)'
        ;;

    qa_triptych)
        log_dsl "TASK: qa_triptych (QA-1 + QA-2 + QA-3)"
        log_dsl ""
        echo "AGENT1:verify|TASK:static_unit_shield"
        echo "AGENT2:browser-use|TASK:e2e_surveillance"
        echo "AGENT3:continuity-council|TASK:adversarial_review"
        echo ""
        echo "# To execute:"
        echo 'Agent(--description:"QA-1: Static & Unit Shield", --prompt:"Run linter (ruff/pyflakes), SAST (bandit), and unit tests on $HARNESS_DIR. Report in DSL: QA1:PASS|FAIL|ISSUES:N.", --subagent_type:"general-purpose", --run_in_background:true)'
        echo 'Agent(--description:"QA-2: Browser Use E2E", --prompt:"Execute Browser Use E2E via act-observe-verify.sh against $APP_URL. Use MCP tools for verification. Report in DSL: QA2:PASS|FAIL|STEPS:N.", --subagent_type:"general-purpose", --run_in_background:true)'
        echo 'Agent(--description:"QA-3: Adversarial Council", --prompt:"Run adversarial-gate.sh for current phase. Blue defends, Red attacks, Judge decides. Report in DSL: JUDGE:GATE:PASS|DENY.", --subagent_type:"general-purpose", --run_in_background:true)'
        ;;

    adversarial)
        log_dsl "TASK: adversarial (Blue + Red teams)"
        log_dsl ""

        # Get current phase for context
        CURRENT=$(python3 "$STATE_ENGINE" get "current_phase" 2>/dev/null || echo "P5")
        PHASE_NUM="${CURRENT:1:1}"

        echo "AGENT-BLUE:defender|TASK:cite_norms|PHASE:$CURRENT"
        echo "AGENT-RED:attacker|TASK:find_flaws|PHASE:$CURRENT"
        echo ""
        echo "# To execute:"
        echo 'Agent(--description:"Blue Team (Defender)", --prompt:"Defend the $CURRENT artifact. Cite SWEBOK v4 KA-$PHASE_NUM norms. Output DSL: BLUE:DEFENDED|NORMS:KA-$PHASE_NUM|STATUS:OK.", --subagent_type:"general-purpose", --run_in_background:true)'
        echo 'Agent(--description:"Red Team (Attacker)", --prompt:"Attack the $CURRENT artifact with phase-specific vulnerabilities. Output DSL: RED:VULN:CRIT|HIGH|MED|LOW|TYPE:ATTACK|FIX:FIX_REQ.", --subagent_type:"general-purpose", --run_in_background:true)'
        ;;

    *)
        log_dsl "ERROR: Unknown task type: $TASK_TYPE"
        echo ""
        echo "Available task types:"
        echo "  emit-envelope <from> <to> - full <MULTIAGENT_LAUNCH> wrapper + JSONL body (gate --council)"
        echo "  emit-prompts  <from> <to> - JSONL per-role council prompts only (ADR-003)"
        echo "  e2e_parallel       - API tests + Browser Use E2E in parallel"
        echo "  security_scan     - nexus-security + nexus-ciso in parallel"
        echo "  architecture_review - nexus-architect + nexus-cto in parallel"
        echo "  qa_triptych       - QA-1 + QA-2 + QA-3 in parallel"
        echo "  adversarial - Blue + Red teams in parallel"
        exit 1
        ;;
esac

log_dsl ""
log_dsl "=========================================="
log_dsl "  MULTIAGENT LAUNCH: $TASK_TYPE"
log_dsl " Note: Agent tool calls above"
log_dsl "  Execute via Claude Code Agent tool"
log_dsl "=========================================="
