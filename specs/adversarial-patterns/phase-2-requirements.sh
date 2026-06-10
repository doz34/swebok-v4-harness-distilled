#!/bin/bash
# Adversarial patterns for Phase 2 (Requirements)
# Per swebok spec phase-2-requirements.md (v2):
# Required deliverables: srs.md, user_stories.md, acceptance_criteria.md, rtm.md
# Demarcation: P2 ≠ P1 (no feasibility) and P2 ≠ P3 (no architecture)
# Stop conditions: cap 35 min, tokens 4k/7k/10k

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 2 (Requirements) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P2 required deliverables:"
for d in srs.md user_stories.md acceptance_criteria.md rtm.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done

# Feedback (sensors) — acceptance criteria testability
echo ""
echo "[feedback] Acceptance criteria testability:"
if [ -f "$PROJECT_ROOT/acceptance_criteria.md" ]; then
  ac_count=$(grep -cE "^\s*[-*]?\s*AC[-.][0-9]+|^###?\s*AC[-.][0-9]+|^\| AC[-.][0-9]+" "$PROJECT_ROOT/acceptance_criteria.md" 2>/dev/null || echo 0)
  echo "  Acceptance criteria identified: $ac_count"
  if [ "$ac_count" -lt 3 ]; then
    echo "  [MED] few ACs identified (target >= 3 per requirement spec)"
  fi
  # Check for testability: each AC should have a measurable criterion
  vague=$(grep -ciE "should|might|maybe|fast|slow|good|bad|nice" "$PROJECT_ROOT/acceptance_criteria.md" 2>/dev/null || echo 0)
  if [ "$vague" -gt 3 ]; then
    echo "  [HIGH] $vague vague terms in AC (testability compromise per ISO/IEC/IEEE 29148)"
  fi
fi

# Feedback (sensors) — requirements traceability matrix
echo ""
echo "[feedback] Traceability matrix (RTM) check:"
if [ -f "$PROJECT_ROOT/rtm.md" ]; then
  # RTM should reference both P0 (charter) and trace forward to design (P3/P4)
  refs_p0=$(grep -ciE "charter|P0|stakeholder|scope" "$PROJECT_ROOT/rtm.md" 2>/dev/null || echo 0)
  if [ "$refs_p0" -lt 1 ]; then
    echo "  [MED] RTM does not reference P0 charter (traceability backward)"
  else
    echo "  [OK] RTM traces backward to P0 ($refs_p0 refs)"
  fi
  # Check that ACs are mapped to tests in RTM
  test_refs=$(grep -ciE "test|verif" "$PROJECT_ROOT/rtm.md" 2>/dev/null || echo 0)
  if [ "$test_refs" -lt 1 ]; then
    echo "  [MED] RTM missing test references (forward traceability to P6)"
  fi
fi

# Demarcation check (computational) — no P1 or P3 keywords
echo ""
echo "[feedback] P2 demarcation (no P1/P3 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P1P3keywords=$(grep -rhoE "feasibility|ROI|go.no.go|architecture style|ADR|tech.stack" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P1P3keywords" ] || [ "$P1P3keywords" = "(none)" ]; then
  echo "  [OK] No P1/P3 keywords found (requirements only per swebok v2)"
else
  echo "  [WARN] P1/P3 keywords found (move to adjacent phase): $P1P3keywords"
fi

# Adversarial — NFR coverage check
echo ""
echo "[feedback] NFR coverage (heuristic):"
if [ -f "$PROJECT_ROOT/srs.md" ]; then
  for nfr in "performance" "security" "scalability" "availability" "usability"; do
    if grep -qiE "$nfr" "$PROJECT_ROOT/srs.md" 2>/dev/null; then
      echo "  [OK] NFR '$nfr' addressed"
    else
      echo "  [LOW] NFR '$nfr' not mentioned (consider documenting)"
    fi
  done
fi

echo ""
echo "=== Run via: adv-loop 2 [work_dir] ==="
exit 0
