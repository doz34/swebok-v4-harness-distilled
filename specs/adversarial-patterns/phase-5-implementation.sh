#!/bin/bash
# Adversarial patterns for Phase 5 (Implementation)
# Per swebok spec phase-5-implementation.md (v2.1):
# - P5 = unit tests ONLY, P6 = coverage + mutation + reste
# Required deliverables: source_code/, unit_tests/
# Demarcation: P5 != P4 (no arch style) and P5 != P6 (no coverage report)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 5 (Implementation) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P5 required deliverables:"
if [ -d "$PROJECT_ROOT/source_code" ]; then
  files=$(find "$PROJECT_ROOT/source_code" -name "*.py" -o -name "*.js" -o -name "*.java" 2>/dev/null | wc -l)
  echo "  [OK] source_code/ exists ($files source files)"
else
  echo "  [MISSING] source_code/"
fi
if [ -d "$PROJECT_ROOT/unit_tests" ]; then
  tests=$(find "$PROJECT_ROOT/unit_tests" -name "test_*.py" -o -name "*.test.js" -o -name "*Test.java" 2>/dev/null | wc -l)
  echo "  [OK] unit_tests/ exists ($tests test files)"
else
  echo "  [MISSING] unit_tests/"
fi

# Demarcation check — no P6 keywords
echo ""
echo "[feedback] P5 demarcation (no P6 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P6keywords=$(grep -rhoE "coverage|mutation|integration test|e2e|end.?to.?end" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P6keywords" ] || [ "$P6keywords" = "(none)" ]; then
  echo "  [OK] No P6 keywords found (unit tests only per swebok v2.1)"
else
  echo "  [WARN] P6 keywords found (move to phase 6): $P6keywords"
fi

# Feedback (sensors) — test coverage
echo ""
echo "[feedback] Test coverage (heuristic):"
if [ -d "$PROJECT_ROOT/unit_tests" ]; then
  src_count=$(find "$PROJECT_ROOT/source_code" -name "*.py" 2>/dev/null | wc -l)
  test_count=$(find "$PROJECT_ROOT/unit_tests" -name "test_*.py" 2>/dev/null | wc -l)
  if [ "$src_count" -gt 0 ]; then
    ratio=$((test_count * 100 / src_count))
    echo "  test_count/source_count ratio: ${ratio}%"
    if [ "$ratio" -lt 50 ]; then
      echo "  [MED] low test ratio (target >= 50%)"
    fi
  fi
fi

# Adversarial — check for known antipatterns
echo ""
echo "[feedback] Antipatterns check:"
for antipattern in "TODO" "FIXME" "XXX" "console.log" "print("; do
  count=$(grep -rE "\\b$antipattern\\b" "$PROJECT_ROOT/source_code" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "  [WARN] $antipattern found $count times in source_code (resolve before phase 6)"
  fi
done

echo ""
echo "=== Run via: adv-loop 5 [work_dir] ==="
exit 0
