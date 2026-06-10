#!/bin/bash
# Adversarial patterns for Phase 0 (Discovery)
# Per swebok spec phase-0-discovery.md:
# Required deliverables: charter.md, context_map.md, stakeholders.md, constraints.md,
#                      success_criteria.md, alternatives.md, discovery_report.md
# Demarcation: P0 != P1 (no feasibility study)
# Stop conditions: 35 min cap, 4k/7k/10k tokens

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 0 (Discovery) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P0 required deliverables:"
for d in charter.md context_map.md stakeholders.md constraints.md success_criteria.md alternatives.md discovery_report.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    echo "  [OK] $d exists"
  else
    echo "  [MISSING] $d (use Project Charter template)"
  fi
done

# Demarcation check (computational)
echo ""
echo "[feedback] P0 demarcation (no P1 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P1keywords=$(grep -rhoE "feasibility study|ROI|go.no.go|P1 deliverable" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P1keywords" ] || [ "$P1keywords" = "(none)" ]; then
  echo "  [OK] No P1 keywords found in work dir"
else
  echo "  [WARN] P1 keywords found (move to phase 1): $P1keywords"
fi

# Feedback sensor (computational) — vague language in charter
echo ""
echo "[feedback] Charter vagueness check:"
if [ -f "$PROJECT_ROOT/charter.md" ]; then
  vague=$(grep -ciE "\\b(should|might|maybe|TBD|FIXME|etc\\.?)\\b" "$PROJECT_ROOT/charter.md" 2>/dev/null || echo 0)
  echo "  Vague words in charter.md: $vague (target: 0)"
  if [ "$vague" -gt 3 ]; then
    echo "  [HIGH] too many vague words, replace with measurable criteria"
  fi
fi

echo ""
echo "=== Run via: adv-loop 0 [work_dir] ==="
exit 0
