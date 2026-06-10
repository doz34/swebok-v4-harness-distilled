#!/bin/bash
# Adversarial patterns for Phase 7 (Deployment)
# Per swebok spec phase-7-deployment.md:
# Required deliverables: deployment_plan.md, rollback_plan.md, release_notes.md, smoke_tests.md
# Demarcation: P7 != P6 (no test refactor) and P7 != P8 (no runbook)
# Stop conditions: time varies (production-grade), tokens ~5k/8k/15k

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 7 (Deployment) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P7 required deliverables:"
for d in deployment_plan.md rollback_plan.md release_notes.md smoke_tests.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done

# Feedback (sensors) — rollback plan must be TESTED
echo ""
echo "[feedback] Rollback plan validation:"
if [ -f "$PROJECT_ROOT/rollback_plan.md" ]; then
  if grep -qiE "rollback.*test|test.*rollback|dry.?run" "$PROJECT_ROOT/rollback_plan.md" 2>/dev/null; then
    echo "  [OK] Rollback plan includes testing"
  else
    echo "  [HIGH] rollback plan NOT tested (per swebok spec EG-7.2)"
  fi
  if grep -qiE "smoke|canary|blue.?green|feature.?flag" "$PROJECT_ROOT/rollback_plan.md" 2>/dev/null; then
    echo "  [OK] Rollback plan mentions safe deployment patterns"
  else
    echo "  [MED] rollback plan missing safe deployment patterns"
  fi
fi

# Demarcation check — no P8 keywords
echo ""
echo "[feedback] P7 demarcation (no P8 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P8keywords=$(grep -rhoE "SLO|on.?call rotation|runbook|monitoring" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P8keywords" ] || [ "$P8keywords" = "(none)" ]; then
  echo "  [OK] No P8 keywords found (smoke tests only)"
else
  echo "  [WARN] P8 keywords found (move to phase 8): $P8keywords"
fi

echo ""
echo "=== Run via: adv-loop 7 [work_dir] ==="
exit 0
