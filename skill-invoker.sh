#!/usr/bin/env bash
# SWEBOK v4 Harness - Skill Invoker
# Maps phases to nexus-* skills via skill-invoker
# Usage: ./skill-invoker.sh <phase> [skill_override]

set -e

PHASE="$1"
SKILL_OVERRIDE="${2:-}"
HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"

if [[ -z "$PHASE" ]]; then
    echo "Usage: skill-invoker.sh <phase> [skill_override]"
    echo "Example: skill-invoker.sh P3"
    echo "         skill-invoker.sh P4 nexus-frontend"
    exit 1
fi

# Validate phase format
if [[ ! "$PHASE" =~ ^P[1-9]$ ]]; then
    echo "[ERROR] Invalid phase: $PHASE (expected P1-P9)"
    exit 1
fi

PHASE_NUM="${PHASE:1:1}"

# Read current state from SQLite (NEVER read .swebok_state YAML)
ACTIVE_KA=$(python3 "$STATE_ENGINE" get "active_ka" 2>/dev/null || echo "")
PROJECT_SCOPE=$(python3 "$STATE_ENGINE" get "project_scope" 2>/dev/null || echo "")
PROJECT_NAME=$(python3 "$STATE_ENGINE" get "project_name" 2>/dev/null || echo "")

# LAW 1 (HOT_PATH): pass --lite to downstream scripts when intent=micro_task
HOT_PATH_MODE=$(python3 "$STATE_ENGINE" hot_path_decision 2>/dev/null || echo "FULL")
LITE_FLAG=""
if [[ "$HOT_PATH_MODE" == "LITE" ]]; then
    LITE_FLAG="--lite"
    echo "[HOT-PATH] intent=micro_task -> downstream invocations will use --lite"
fi

echo "=========================================="
echo "  SKILL INVOKER"
echo "  Phase: $PHASE"
echo "  Active KA: ${ACTIVE_KA:-none}"
echo "  Override: ${SKILL_OVERRIDE:-none}"
echo "=========================================="

# === PHASE → SKILL MAPPING ===
INVOKED_SKILLS=()

case "$PHASE" in
    P1)
        echo ""
        echo "[INVOKING] discovery-orchestrator + nexus-cpo"
        echo "[REASON] Discovery phase - need needfinding + CPO perspective"
        INVOKED_SKILLS=("discovery-orchestrator" "nexus-cpo")
        ;;
    P2)
        echo ""
        echo "[INVOKING] nexus-pm + nexus-sm"
        echo "[REASON] Requirements phase - need PM + Scrum Master"
        INVOKED_SKILLS=("nexus-pm" "nexus-sm")
        ;;
    P3)
        echo ""
        echo "[INVOKING] nexus-architect + nexus-cto"
        echo "[REASON] Architecture phase - need architect + CTO review"
        INVOKED_SKILLS=("nexus-architect" "nexus-cto")
        ;;
    P4)
        echo ""
        if [[ -n "$SKILL_OVERRIDE" ]]; then
            echo "[INVOKING] $SKILL_OVERRIDE (override)"
            INVOKED_SKILLS=("$SKILL_OVERRIDE")
        elif echo "$PROJECT_SCOPE" | grep -qi "frontend\|ui\|web"; then
            echo "[INVOKING] nexus-frontend + nexus-fullstack"
            echo "[REASON] Frontend project scope detected"
            INVOKED_SKILLS=("nexus-frontend" "nexus-fullstack")
        elif echo "$PROJECT_SCOPE" | grep -qi "backend\|api\|service"; then
            echo "[INVOKING] nexus-backend + nexus-fullstack"
            echo "[REASON] Backend project scope detected"
            INVOKED_SKILLS=("nexus-backend" "nexus-fullstack")
        else
            echo "[INVOKING] nexus-fullstack"
            echo "[REASON] Default fullstack for design phase"
            INVOKED_SKILLS=("nexus-fullstack")
        fi
        ;;
    P5)
        echo ""
        echo "[INVOKING] nexus-fullstack"
        echo "[REASON] Construction phase - implementation"

        # Check for ML/AI project (use SQLite-stored name as signal)
        if echo "${PROJECT_NAME:-}${PROJECT_SCOPE:-}" | grep -qi "ML\|machine learning\|AI\|artificial intelligence"; then
            echo "[ADDITIONAL] karpathy-skills (ML project detected)"
            INVOKED_SKILLS+=("karpathy-skills")
        fi
        ;;
    P6)
        echo ""
        echo "[INVOKING] nexus-qa-lead + speckit-qa + verify"
        echo "[REASON] Testing phase - QA lead + speckit + verify skill"
        INVOKED_SKILLS=("nexus-qa-lead" "speckit-qa" "verify")
        ;;
    P7)
        echo ""
        echo "[INVOKING] nexus-devops-lead + nexus-devops"
        echo "[REASON] Deployment phase - DevOps lead + specialist"
        INVOKED_SKILLS=("nexus-devops-lead" "nexus-devops")
        ;;
    P8)
        echo ""
        echo "[INVOKING] nexus-devops + nexus-ciso"
        echo "[REASON] Operations phase - DevOps + Security"
        INVOKED_SKILLS=("nexus-devops" "nexus-ciso")
        ;;
    P9)
        echo ""
        echo "[INVOKING] nexus-cto + nexus-security"
        echo "[REASON] Retirement phase - CTO + Security review"
        INVOKED_SKILLS=("nexus-cto" "nexus-security")
        ;;
esac

# === OUTPUT DSL FOR CLAUDE ===
echo ""
echo "=========================================="
echo "  SKILL INVOCATION DSL"
echo "=========================================="

for skill in "${INVOKED_SKILLS[@]}"; do
    echo "SKILL:$skill"
done

echo ""
echo "=========================================="
echo "  INVOKED: ${INVOKED_SKILLS[*]}"
echo "=========================================="

# Return skills for chaining
printf '%s\n' "${INVOKED_SKILLS[@]}"
