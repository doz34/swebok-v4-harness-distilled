#!/bin/bash
# Adversarial patterns for Phase 1 (Concept/Feasibility)
# Per swebok spec phase-1-concept-feasibility.md (v2):
# Required deliverables: feasibility_report.md, roi_analysis.md, go_no_go_memo.md
# Demarcation: P1 ≠ P0 (no new discovery) and P1 ≠ P2 (no requirements)
# Stop conditions: cap 35 min strict, tokens 3k/5k/8k (serre vs P0/P2)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 1 (Concept/Feasibility) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P1 required deliverables:"
for d in feasibility_report.md roi_analysis.md go_no_go_memo.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done

# Feedback (sensors) — feasibility study must cover 4 dimensions
echo ""
echo "[feedback] Feasibility study 4 dimensions coverage:"
if [ -f "$PROJECT_ROOT/feasibility_report.md" ]; then
  for dim in "technique" "économique" "organisationnelle" "réglementaire"; do
    if grep -qiE "$dim" "$PROJECT_ROOT/feasibility_report.md" 2>/dev/null; then
      echo "  [OK] dimension '$dim' couverte"
    else
      echo "  [HIGH] dimension '$dim' manquante (per swebok spec XG-1.1)"
    fi
  done
fi

# Feedback (sensors) — ROI + payback must be quantified
echo ""
echo "[feedback] ROI quantification check:"
if [ -f "$PROJECT_ROOT/roi_analysis.md" ]; then
  vague=$(grep -ciE "\\b(TBD|FIXME|\\?\\?\\?|to.?be.?determined)\\b" "$PROJECT_ROOT/roi_analysis.md" 2>/dev/null || echo 0)
  if [ "$vague" -gt 0 ]; then
    echo "  [HIGH] $vague placeholders in roi_analysis.md (chiffres requis)"
  else
    echo "  [OK] roi_analysis.md fully quantified"
  fi
  if grep -qiE "payback" "$PROJECT_ROOT/roi_analysis.md" 2>/dev/null; then
    echo "  [OK] payback period mentioned"
  else
    echo "  [MED] payback period not mentioned (per XG-1.3)"
  fi
fi

# Feedback (sensors) — go/no-go decision must be signed
echo ""
echo "[feedback] Go/no-go decision signature:"
if [ -f "$PROJECT_ROOT/go_no_go_memo.md" ]; then
  if grep -qiE "(go|no.go|signé|signed|apprové|approved)" "$PROJECT_ROOT/go_no_go_memo.md" 2>/dev/null; then
    echo "  [OK] go/no-go decision documented"
  else
    echo "  [HIGH] no clear go/no-go decision (per XG-1.4)"
  fi
fi

# Demarcation check (computational) — no P0 or P2 keywords
echo ""
echo "[feedback] P1 demarcation (no P0/P2 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P0P2keywords=$(grep -rhoE "stakeholder map|P0 charter|discovery report|user.story|acceptance criteria|architecture choice" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P0P2keywords" ] || [ "$P0P2keywords" = "(none)" ]; then
  echo "  [OK] No P0/P2 keywords found (feasibility only per swebok v2)"
else
  echo "  [WARN] P0/P2 keywords found (split per demarcation): $P0P2keywords"
fi

echo ""
echo "=== Run via: adv-loop 1 [work_dir] ==="
exit 0
