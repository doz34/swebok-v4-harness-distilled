#!/bin/bash
# Adversarial patterns for Phase 9 (Maintenance)
# Per swebok spec phase-9-maintenance.md (v2):
# Required deliverables: refactoring_plan.md, tech_debt_register.md, release_notes.md
# Demarcation: P9 ≠ P8 (no runbook) and P9 ≠ P10 (no retirement prep)
# Stop conditions: adaptatif 3-niveaux (1k/2k/3k hotfix + 3k/5k/8k standard + 5k/8k/15k structurant)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 9 (Maintenance) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P9 required deliverables:"
for d in refactoring_plan.md tech_debt_register.md release_notes.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done

# Feedback (sensors) — maintenance type explicit (corrective/adaptive/perfective/preventive)
echo ""
echo "[feedback] Maintenance type explicit (per IEEE 1219):"
if [ -f "$PROJECT_ROOT/refactoring_plan.md" ]; then
  for mtype in "corrective\|bugfix\|fix" "adaptive\|environment\|dependency" "perfective\|enhancement\|feature" "preventive\|debt\|hardening"; do
    if grep -qiE "$mtype" "$PROJECT_ROOT/refactoring_plan.md" 2>/dev/null; then
      echo "  [OK] maintenance type '$mtype' addressed"
    else
      echo "  [LOW] maintenance type '$mtype' not mentioned"
    fi
  done
fi

# Feedback (sensors) — tech debt register quality
echo ""
echo "[feedback] Tech debt register:"
if [ -f "$PROJECT_ROOT/tech_debt_register.md" ]; then
  debt_count=$(grep -cE "^\s*[-*]\s*\[.*\]|^\s*\|.*\".*\".*\|.*\".*\".*\|" "$PROJECT_ROOT/tech_debt_register.md" 2>/dev/null || echo 0)
  echo "  Tech debt items: $debt_count"
  # Check for severity / priority / owner fields
  for field in "severity\|priority" "owner\|assignee" "effort\|estimate" "impact"; do
    if grep -qiE "$field" "$PROJECT_ROOT/tech_debt_register.md" 2>/dev/null; then
      echo "  [OK] tech debt field '$field' present"
    else
      echo "  [LOW] tech debt field '$field' missing (prioritization compromised)"
    fi
  done
fi

# Feedback (sensors) — impact analysis + regression test plan
echo ""
echo "[feedback] Impact analysis + regression test:"
if [ -f "$PROJECT_ROOT/refactoring_plan.md" ]; then
  if grep -qiE "impact.*analysis\|impact.*assess" "$PROJECT_ROOT/refactoring_plan.md" 2>/dev/null; then
    echo "  [OK] impact analysis mentioned"
  else
    echo "  [HIGH] no impact analysis (refactoring blind)"
  fi
  if grep -qiE "regression.*test\|re.test.plan" "$PROJECT_ROOT/refactoring_plan.md" 2>/dev/null; then
    echo "  [OK] regression test plan mentioned"
  else
    echo "  [MED] regression test plan not mentioned (P6 escalation)"
  fi
fi

# Demarcation check (computational) — no P8 or P10 keywords
echo ""
echo "[feedback] P9 demarcation (no P8/P10 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P8P10keywords=$(grep -rhoE "on.call|runbook|SLO|monitoring|retirement|EOL|end.of.life|archive" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P8P10keywords" ] || [ "$P8P10keywords" = "(none)" ]; then
  echo "  [OK] No P8/P10 keywords found (code change only, no operations or retirement)"
else
  echo "  [WARN] P8/P10 keywords found (escalate to adjacent phase): $P8P10keywords"
fi

# Feedback (sensors) — release notes quality
echo ""
echo "[feedback] Release notes (per XG-9.x):"
if [ -f "$PROJECT_ROOT/release_notes.md" ]; then
  for concept in "version\|tag" "change.*type\|type" "author\|owner" "breaking.*change\|migration"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/release_notes.md" 2>/dev/null; then
      echo "  [OK] release notes concept '$concept' present"
    else
      echo "  [LOW] release notes concept '$concept' missing"
    fi
  done
fi

echo ""
echo "=== Run via: adv-loop 9 [work_dir] ==="
exit 0
