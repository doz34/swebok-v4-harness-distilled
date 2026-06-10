#!/bin/bash
# Adversarial patterns for Phase 4 (Design)
# Per swebok spec phase-4-design.md (v2):
# Required deliverables: design_doc.md, api_contracts.md, data_model.md, sequence_diagrams/
# Demarcation: P4 ≠ P3 (no arch style) and P4 ≠ P5 (no code)
# Stop conditions: hard cap 15k tokens (cohérence P3)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 4 (Design) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P4 required deliverables:"
for d in design_doc.md api_contracts.md data_model.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done
if [ -d "$PROJECT_ROOT/sequence_diagrams" ]; then
  files=$(find "$PROJECT_ROOT/sequence_diagrams" -type f 2>/dev/null | wc -l)
  echo "  [OK] sequence_diagrams/ exists ($files files)"
else
  echo "  [MISSING] sequence_diagrams/"
fi

# Feedback (sensors) — API contracts format (per spec: OpenAPI 3.0 for REST, AsyncAPI 3.0 for events)
echo ""
echo "[feedback] API contract format check:"
if [ -f "$PROJECT_ROOT/api_contracts.md" ]; then
  if grep -qiE "openapi|swagger" "$PROJECT_ROOT/api_contracts.md" 2>/dev/null; then
    echo "  [OK] OpenAPI/Swagger referenced"
  else
    echo "  [MED] OpenAPI/Swagger not referenced (per P4 spec format différencié)"
  fi
  # Check for HTTP methods + status codes coverage
  for method in "GET" "POST" "PUT" "DELETE"; do
    if grep -qE "\\b$method\\b" "$PROJECT_ROOT/api_contracts.md" 2>/dev/null; then
      echo "  [OK] HTTP method '$method' covered"
    fi
  done
  # Check for error handling specification
  if grep -qiE "(4[0-9][0-9]|5[0-9][0-9]|error.*handling|error.*response)" "$PROJECT_ROOT/api_contracts.md" 2>/dev/null; then
    echo "  [OK] error responses documented"
  else
    echo "  [HIGH] error responses not documented (per DDS)"
  fi
fi

# Feedback (sensors) — data model integrity
echo ""
echo "[feedback] Data model integrity:"
if [ -f "$PROJECT_ROOT/data_model.md" ]; then
  # Should have entities, relationships, constraints
  for concept in "entity" "relationship" "constraint" "primary.key\|PK\|id"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/data_model.md" 2>/dev/null; then
      echo "  [OK] data model concept '$concept' present"
    fi
  done
  # Check that data model references P3 architecture
  if grep -qiE "bounded.context|aggregate|domain" "$PROJECT_ROOT/data_model.md" 2>/dev/null; then
    echo "  [OK] data model uses DDD concepts (alignment P3 archi)"
  else
    echo "  [LOW] data model doesn't reference P3 DDD concepts"
  fi
fi

# Demarcation check (computational) — no P3 or P5 keywords
echo ""
echo "[feedback] P4 demarcation (no P3/P5 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P3P5keywords=$(grep -rhoE "microservice.*choice|architecture.style|production.code|unit.test|P5.deliverable" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P3P5keywords" ] || [ "$P3P5keywords" = "(none)" ]; then
  echo "  [OK] No P3/P5 keywords found (detailed design only, not arch style or code)"
else
  echo "  [WARN] P3/P5 keywords found (move to adjacent phase): $P3P5keywords"
fi

# Feedback (sensors) — sequence diagrams coverage
echo ""
echo "[feedback] Sequence diagrams coverage:"
if [ -d "$PROJECT_ROOT/sequence_diagrams" ]; then
  # Critical flows: auth, main use case, error path
  for flow in "auth" "main\|primary\|happy.path" "error\|failure"; do
    if find "$PROJECT_ROOT/sequence_diagrams" -iname "*${flow%%\\|*}.*" 2>/dev/null | grep -q .; then
      echo "  [OK] sequence diagram for '$flow' present"
    else
      echo "  [LOW] sequence diagram for '$flow' missing"
    fi
  done
fi

echo ""
echo "=== Run via: adv-loop 4 [work_dir] ==="
exit 0
