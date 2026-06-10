#!/bin/bash
# Adversarial patterns for Phase 3 (Architecture)
# Per swebok spec phase-3-architecture.md (v2):
# Required deliverables: architecture_doc.md, adrs.md, c4_diagrams/
# Demarcation: P3 ≠ P4 (no detailed module design) and P3 ≠ P2 (no requirements)
# Stop conditions: hard cap 15k tokens (Nexus-Critic T1+T2+T3 obligatoire)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 3 (Architecture) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P3 required deliverables:"
for d in architecture_doc.md adrs.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done
if [ -d "$PROJECT_ROOT/c4_diagrams" ]; then
  files=$(find "$PROJECT_ROOT/c4_diagrams" -type f 2>/dev/null | wc -l)
  echo "  [OK] c4_diagrams/ exists ($files files)"
else
  echo "  [MISSING] c4_diagrams/ (C4 model: context, container, component, code)"
fi

# Feedback (sensors) — ADR count (per spec: minimum 1 per structurante decision)
echo ""
echo "[feedback] ADR count check:"
if [ -f "$PROJECT_ROOT/adrs.md" ]; then
  adr_count=$(grep -cE "^#+\s*ADR[-.][0-9]+|^\s*-\s*\[ADR[-.][0-9]+\]|^##\s*ADR" "$PROJECT_ROOT/adrs.md" 2>/dev/null || echo 0)
  echo "  ADRs identified: $adr_count"
  if [ "$adr_count" -lt 1 ]; then
    echo "  [HIGH] no ADRs found (per spec: minimum 1 per structurante decision)"
  else
    echo "  [OK] $adr_count ADR(s) documented"
  fi
  # ADR must include: context, decision, consequences (MADR template)
  for section in "Context" "Decision" "Consequences"; do
    if grep -qiE "^#+.*$section" "$PROJECT_ROOT/adrs.md" 2>/dev/null; then
      echo "  [OK] ADR section '$section' present"
    else
      echo "  [MED] ADR section '$section' missing (MADR template)"
    fi
  done
fi

# Feedback (sensors) — C4 diagram coverage
echo ""
echo "[feedback] C4 model coverage:"
if [ -d "$PROJECT_ROOT/c4_diagrams" ]; then
  for level in "context" "container" "component"; do
    if find "$PROJECT_ROOT/c4_diagrams" -iname "*$level*" 2>/dev/null | grep -q .; then
      echo "  [OK] C4 level '$level' documented"
    else
      echo "  [LOW] C4 level '$level' missing (consider adding)"
    fi
  done
fi

# Demarcation check (computational) — no P2 or P4 keywords
echo ""
echo "[feedback] P3 demarcation (no P2/P4 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P2P4keywords=$(grep -rhoE "user.story|acceptance criteria.detail|API.contract.detail|data.model.schema|class.diagram|sequence.diagram.detail" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P2P4keywords" ] || [ "$P2P4keywords" = "(none)" ]; then
  echo "  [OK] No P2/P4 keywords found (architecture only, not detailed design)"
else
  echo "  [WARN] P2/P4 keywords found (P4 = detailed design level): $P2P4keywords"
fi

# Feedback (sensors) — architecture style explicit
echo ""
echo "[feedback] Architecture style documentation:"
if [ -f "$PROJECT_ROOT/architecture_doc.md" ]; then
  for style in "monolith" "microservice" "event.driven" "layered" "hexagonal" "serverless"; do
    if grep -qiE "$style" "$PROJECT_ROOT/architecture_doc.md" 2>/dev/null; then
      echo "  [OK] architecture style '$style' mentioned"
      break
    fi
  done
  # Check for security architecture section
  if grep -qiE "security.*architecture|threat.model|security.pattern" "$PROJECT_ROOT/architecture_doc.md" 2>/dev/null; then
    echo "  [OK] security architecture addressed"
  else
    echo "  [MED] security architecture not addressed (per STRIDE)"
  fi
fi

echo ""
echo "=== Run via: adv-loop 3 [work_dir] ==="
exit 0
