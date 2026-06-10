#!/bin/bash
# Adversarial patterns for Phase 8 (Operations)
# Per swebok spec phase-8-operations.md (v2):
# Required deliverables: runbooks.md, slos.md, on_call_rotation.md, incident_postmortems.md
# Demarcation: P8 ≠ P7 (no new deploy) and P8 ≠ P9 (no refactor)
# Stop conditions: adaptatif par sévérité (1k/2k/3k + 2k/4k/6k + 5k/8k/15k)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 8 (Operations) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P8 required deliverables:"
for d in runbooks.md slos.md on_call_rotation.md incident_postmortems.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done

# Feedback (sensors) — SLO measurability (per SRE: SLI + SLO + error budget)
echo ""
echo "[feedback] SLO measurability (per SRE):"
if [ -f "$PROJECT_ROOT/slos.md" ]; then
  for concept in "SLI" "SLO" "error.budget" "availability" "latency"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/slos.md" 2>/dev/null; then
      echo "  [OK] SLO concept '$concept' addressed"
    else
      echo "  [LOW] SLO concept '$concept' missing"
    fi
  done
  # Check for measurable thresholds (p95, p99, 99.9%, etc.)
  if grep -qiE "(p95|p99|99\\.[0-9]+%|<[0-9]+m?s)" "$PROJECT_ROOT/slos.md" 2>/dev/null; then
    echo "  [OK] SLO has measurable threshold"
  else
    echo "  [HIGH] SLO has no measurable threshold (p95/p99/<Xms)"
  fi
fi

# Feedback (sensors) — runbook quality (actionable, not vague)
echo ""
echo "[feedback] Runbook quality:"
if [ -f "$PROJECT_ROOT/runbooks.md" ]; then
  vague=$(grep -ciE "\\b(should|might|maybe|consider|perhaps)\\b" "$PROJECT_ROOT/runbooks.md" 2>/dev/null || echo 0)
  if [ "$vague" -gt 5 ]; then
    echo "  [MED] $vague vague terms in runbook (actionability compromised)"
  else
    echo "  [OK] runbook language is actionable"
  fi
  # Check for escalation paths
  if grep -qiE "escalat" "$PROJECT_ROOT/runbooks.md" 2>/dev/null; then
    echo "  [OK] escalation paths documented"
  else
    echo "  [HIGH] no escalation paths (incident response blind)"
  fi
fi

# Feedback (sensors) — on-call rotation defined
echo ""
echo "[feedback] On-call rotation:"
if [ -f "$PROJECT_ROOT/on_call_rotation.md" ]; then
  # Should have people, schedule, contact
  for concept in "primary\|P1" "secondary\|P2\|backup" "schedule\|rotation\|semaine" "contact\|pager\|phone"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/on_call_rotation.md" 2>/dev/null; then
      echo "  [OK] on-call concept '$concept' present"
    else
      echo "  [LOW] on-call concept '$concept' missing"
    fi
  done
fi

# Demarcation check (computational) — no P7 or P9 keywords
echo ""
echo "[feedback] P8 demarcation (no P7/P9 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P7P9keywords=$(grep -rhoE "deploy.script|rollback.plan|release.notes|new.feature|refactor|tech.debt" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P7P9keywords" ] || [ "$P7P9keywords" = "(none)" ]; then
  echo "  [OK] No P7/P9 keywords found (monitoring only, no deploy or refactor)"
else
  echo "  [WARN] P7/P9 keywords found (escalate to adjacent phase): $P7P9keywords"
fi

# Feedback (sensors) — incident post-mortem quality
echo ""
echo "[feedback] Post-mortem quality (per XG-8.x):"
if [ -f "$PROJECT_ROOT/incident_postmortems.md" ]; then
  pm_count=$(grep -cE "^#+.*[Pp]ost.?[Mm]ortem|^#+.*[Ii]ncident.*[Rr]eview|^#+\s*PM[-.][0-9]+" "$PROJECT_ROOT/incident_postmortems.md" 2>/dev/null || echo 0)
  echo "  Post-mortems documented: $pm_count"
  if [ "$pm_count" -gt 0 ]; then
    # Check for blameless + action items
    for concept in "blameless\|no.blame" "action.item\|follow.up" "root.cause\|5.whys"; do
      if grep -qiE "$concept" "$PROJECT_ROOT/incident_postmortems.md" 2>/dev/null; then
        echo "  [OK] post-mortem concept '$concept' addressed"
      else
        echo "  [LOW] post-mortem concept '$concept' missing"
      fi
    done
  fi
fi

echo ""
echo "=== Run via: adv-loop 8 [work_dir] ==="
exit 0
