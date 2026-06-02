#!/usr/bin/env bash
# SWEBOK v4 Harness - Bootstrap for existing codebases
# Auto-detects SDLC phase and writes to .swebok_state.db via state_engine.py.
# Source of truth: SQLite ONLY. NEVER write the .swebok_state YAML.
# Usage: bash scripts/swebok-bootstrap.sh [--force-phase P5]

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
FORCE_PHASE=""

if [[ "${1:-}" == "--force-phase" ]] && [[ -n "${2:-}" ]]; then
    FORCE_PHASE="$2"
fi

echo "[BOOTSTRAP] SWEBOK v4 Harness - Bootstrap Protocol"
echo "[BOOTSTRAP] Scanning existing codebase..."

# Detect phase based on file structure
detect_phase() {
    if [[ -n "$FORCE_PHASE" ]]; then
        echo "$FORCE_PHASE"
        return
    fi

    # Check for implementation files
    if [[ -d "$HARNESS_DIR/src" ]] || [[ -d "$HARNESS_DIR/lib" ]] || [[ -d "$HARNESS_DIR/include" ]]; then
        if ls "$HARNESS_DIR"/*.py "$HARNESS_DIR"/*.ts "$HARNESS_DIR"/*.js "$HARNESS_DIR"/*.go "$HARNESS_DIR"/*.java 2>/dev/null | head -1 >/dev/null; then
            echo "P5_CONSTRUCTION"
            return
        fi
    fi

    # Check for design docs
    if [[ -f "$HARNESS_DIR/ARCHITECTURE.md" ]] || [[ -f "$HARNESS_DIR/design/"* ]] 2>/dev/null; then
        echo "P4_DESIGN"
        return
    fi

    # Check for requirements
    if [[ -f "$HARNESS_DIR/requirements.txt" ]] || [[ -f "$HARNESS_DIR/SPEC.md" ]]; then
        echo "P2_REQUIREMENTS"
        return
    fi

    # Default to P5 if code exists
    echo "P5_CONSTRUCTION"
}

ESTIMATED_PHASE=$(detect_phase)
PROJECT_NAME=$(basename "$HARNESS_DIR")

echo "[BOOTSTRAP] Detected phase: $ESTIMATED_PHASE"
echo "[BOOTSTRAP] Project: $PROJECT_NAME"

# Pre-validate all gates for existing code
case "$ESTIMATED_PHASE" in
    P5_CONSTRUCTION)
        VALIDATED_GATES='["P1_EXIT", "P2_EXIT", "P3_EXIT", "P4_EXIT"]'
        ;;
    P4_DESIGN)
        VALIDATED_GATES='["P1_EXIT", "P2_EXIT", "P3_EXIT"]'
        ;;
    P3_ARCHITECTURE)
        VALIDATED_GATES='["P1_EXIT", "P2_EXIT"]'
        ;;
    P2_REQUIREMENTS)
        VALIDATED_GATES='["P1_EXIT"]'
        ;;
    *)
        VALIDATED_GATES='[]'
        ;;
esac

# Initialize state using Python state_engine (SQLite ONLY - source of truth)
python3 -c "
import sys
sys.path.insert(0, '$HARNESS_DIR/scripts')
from lib.state_engine import set, get

# Set core state values using state_engine (SQLite)
set('current_phase', '$ESTIMATED_PHASE')
set('gates_validated', '$VALIDATED_GATES')
set('last_action', 'BOOTSTRAP: Auto-detected existing codebase')
set('project_scope', 'Legacy Onboarding')
set('project_name', '$PROJECT_NAME')

print('[BOOTSTRAP] State written to SQLite via state_engine')
"

echo "[BOOTSTRAP] BOOTSTRAP COMPLETE (SQLite ONLY - no YAML)"
echo "[BOOTSTRAP] State initialized to $ESTIMATED_PHASE"
echo "[BOOTSTRAP] Validated gates: $VALIDATED_GATES"