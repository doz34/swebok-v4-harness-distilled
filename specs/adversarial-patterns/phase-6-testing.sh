#!/bin/bash
# Adversarial patterns for Phase 6 (Testing)
# Per swebok spec phase-6-testing.md (v2):
# Required deliverables: test_plan.md, integration_tests/, mutation_report.md, coverage_report.md
# Demarcation: P6 ≠ P5 (no new features) and P6 ≠ P7 (no deploy)
# Stop conditions: hard cap 15k tokens, 11 livrables, XG-6.1-XG-6.10

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 6 (Testing) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P6 required deliverables:"
for d in test_plan.md mutation_report.md coverage_report.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done
if [ -d "$PROJECT_ROOT/integration_tests" ]; then
  files=$(find "$PROJECT_ROOT/integration_tests" -type f 2>/dev/null | wc -l)
  echo "  [OK] integration_tests/ exists ($files files)"
else
  echo "  [MISSING] integration_tests/"
fi

# Feedback (sensors) — coverage threshold (per XG-6.2: ≥80% line + ≥70% branch)
echo ""
echo "[feedback] Coverage threshold check:"
if [ -f "$PROJECT_ROOT/coverage_report.md" ]; then
  for metric in "line.*[0-9]+%\|line.*coverage\|Lines.*[0-9]+%" "branch.*[0-9]+%\|branch.*coverage\|Branches.*[0-9]+%"; do
    if grep -qiE "$metric" "$PROJECT_ROOT/coverage_report.md" 2>/dev/null; then
      echo "  [OK] coverage metric found"
    fi
  done
  # Check for threshold declaration
  if grep -qiE "(>=|≥|target|seuil|threshold).*[0-9]+%" "$PROJECT_ROOT/coverage_report.md" 2>/dev/null; then
    echo "  [OK] coverage threshold declared"
  else
    echo "  [MED] coverage threshold not declared (XG-6.2: ≥80% line + ≥70% branch)"
  fi
fi

# Feedback (sensors) — mutation score (per XG-6.3: ≥70% mutation score)
echo ""
echo "[feedback] Mutation score check:"
if [ -f "$PROJECT_ROOT/mutation_report.md" ]; then
  if grep -qiE "(mutation.*score|mutation.*[0-9]+%|killed|survived)" "$PROJECT_ROOT/mutation_report.md" 2>/dev/null; then
    echo "  [OK] mutation score reported"
  else
    echo "  [MED] mutation score not reported (per XG-6.3: ≥70%)"
  fi
fi

# Feedback (sensors) — defect backlog stability (per XG-6.4: ≤1 crit, ≤5 high, ≤20 med)
echo ""
echo "[feedback] Defect backlog (heuristic):"
if [ -f "$PROJECT_ROOT/test_plan.md" ]; then
  crit=$(grep -ciE "critical|severity.*1|S1" "$PROJECT_ROOT/test_plan.md" 2>/dev/null || echo 0)
  high=$(grep -ciE "high|severity.*2|S2" "$PROJECT_ROOT/test_plan.md" 2>/dev/null || echo 0)
  if [ "$crit" -gt 5 ] || [ "$high" -gt 10 ]; then
    echo "  [MED] defect backlog heuristic: crit=$crit high=$high (per XG-6.4)"
  else
    echo "  [OK] defect backlog appears stable"
  fi
fi

# Demarcation check (computational) — no P5 or P7 keywords
echo ""
echo "[feedback] P6 demarcation (no P5/P7 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P5P7keywords=$(grep -rhoE "new.feature|refactor|production.code|deploy.script|rollback.plan|smoke.test" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P5P7keywords" ] || [ "$P5P7keywords" = "(none)" ]; then
  echo "  [OK] No P5/P7 keywords found (testing only, no code changes or deploy)"
else
  echo "  [WARN] P5/P7 keywords found (escalate to adjacent phase): $P5P7keywords"
fi

# Feedback (sensors) — test traceability to P2 acceptance criteria
echo ""
echo "[feedback] AC traceability (per XG-6.10):"
if [ -f "$PROJECT_ROOT/test_plan.md" ] && [ -f "$PROJECT_ROOT/acceptance_criteria.md" ]; then
  ac_ids=$(grep -oE "AC[-.][0-9]+" "$PROJECT_ROOT/acceptance_criteria.md" 2>/dev/null | sort -u | wc -l)
  ac_referenced=$(grep -oE "AC[-.][0-9]+" "$PROJECT_ROOT/test_plan.md" 2>/dev/null | sort -u | wc -l)
  if [ "$ac_ids" -gt 0 ]; then
    coverage=$((ac_referenced * 100 / ac_ids))
    echo "  AC traceability: $ac_referenced/$ac_ids ACs referenced (${coverage}%)"
    if [ "$coverage" -lt 100 ]; then
      echo "  [HIGH] AC traceability < 100% (per XG-6.10, 100% required)"
    fi
  fi
fi

# Adversarial — known antipatterns in tests
echo ""
echo "[feedback] Test antipatterns check:"
for antipattern in "skip\|@skip\|\\.skip(" "todo\|@todo" "test.skip\|xit\\(\|xdescribe\\("; do
  count=$(grep -rE "$antipattern" "$PROJECT_ROOT/integration_tests" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "  [MED] $count skipped/todo tests found (resolve before P7)"
  fi
done

echo ""
echo "=== Run via: adv-loop 6 [work_dir] ==="
exit 0
