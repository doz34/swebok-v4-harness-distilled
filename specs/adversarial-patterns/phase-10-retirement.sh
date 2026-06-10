#!/bin/bash
# Adversarial patterns for Phase 10 (Retirement)
# Per swebok spec phase-10-retirement.md (v2):
# Required deliverables: retirement_plan.md, data_archival.md, user_migration.md, closure_memo.md
# Demarcation: P10 ≠ P9 (no maintenance) and P10 ≠ P0 (no new project)
# Stop conditions: adaptatif 3-niveaux par criticité conformité (1k/2k/3k + 3k/5k/8k + 5k/8k/15k)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Adversarial patterns for Phase 10 (Retirement) ==="

# Feedforward (guides) — run before phase
echo "[feedforward] P10 required deliverables:"
for d in retirement_plan.md data_archival.md user_migration.md closure_memo.md; do
  if [ -f "$PROJECT_ROOT/$d" ]; then
    size=$(wc -l < "$PROJECT_ROOT/$d")
    echo "  [OK] $d exists ($size lines)"
  else
    echo "  [MISSING] $d"
  fi
done

# Feedback (sensors) — RGPD/compliance coverage (per XG-10.1 + XG-10.6)
echo ""
echo "[feedback] RGPD/compliance coverage (per XG-10.1, XG-10.6):"
if [ -f "$PROJECT_ROOT/data_archival.md" ]; then
  for concept in "RGPD\|GDPR" "data.*retention\|retention.*policy" "consent" "anonymization\|pseudonymization" "DPO\|DPO.*sign" "checksum\|integrity\|hash"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/data_archival.md" 2>/dev/null; then
      echo "  [OK] compliance concept '$concept' addressed"
    else
      echo "  [HIGH] compliance concept '$concept' missing (per RGPD)"
    fi
  done
fi

# Feedback (sensors) — user migration status (per XG-10.2)
echo ""
echo "[feedback] User migration / notification:"
if [ -f "$PROJECT_ROOT/user_migration.md" ]; then
  for concept in "migrat" "notif" "email\|in.app" "deadline\|EOL.*date" "replacement.*system\|new.*system"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/user_migration.md" 2>/dev/null; then
      echo "  [OK] user migration concept '$concept' present"
    else
      echo "  [HIGH] user migration concept '$concept' missing (per XG-10.2)"
    fi
  done
fi

# Feedback (sensors) — ownership transfer (per XG-10.4)
echo ""
echo "[feedback] Ownership transfer (per XG-10.4):"
if [ -f "$PROJECT_ROOT/retirement_plan.md" ]; then
  for concept in "ownership\|responsibility" "transfer" "sign.*off\|signé" "replacement.*team\|new.*owner"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/retirement_plan.md" 2>/dev/null; then
      echo "  [OK] ownership concept '$concept' present"
    else
      echo "  [HIGH] ownership concept '$concept' missing (liability gap)"
    fi
  done
fi

# Feedback (sensors) — system shutdown checklist (per XG-10.3)
echo ""
echo "[feedback] System shutdown completeness (per XG-10.3):"
if [ -f "$PROJECT_ROOT/retirement_plan.md" ]; then
  for component in "server\|compute" "DNS" "monitoring\|alert" "log" "database\|data.*store"; do
    if grep -qiE "$component" "$PROJECT_ROOT/retirement_plan.md" 2>/dev/null; then
      echo "  [OK] shutdown component '$component' addressed"
    else
      echo "  [MED] shutdown component '$component' missing (cleanup incomplet)"
    fi
  done
fi

# Demarcation check (computational) — no P9 or P0 keywords
echo ""
echo "[feedback] P10 demarcation (no P9/P0 keywords):"
work_dir="${1:-$PROJECT_ROOT}"
P9P0keywords=$(grep -rhoE "refactor|tech.debt|new.feature|next.project|P0.charter|new.sprint" "$work_dir" 2>/dev/null | head -3 || echo "(none)")
if [ -z "$P9P0keywords" ] || [ "$P9P0keywords" = "(none)" ]; then
  echo "  [OK] No P9/P0 keywords found (retirement only, no maintenance or new project)"
else
  echo "  [WARN] P9/P0 keywords found (escalate to adjacent phase): $P9P0keywords"
fi

# Feedback (sensors) — réversibilité (per spec: 30j/90j/180j+ read-only par criticité)
echo ""
echo "[feedback] Réversibilité window (per spec):"
if [ -f "$PROJECT_ROOT/retirement_plan.md" ]; then
  for window in "30.*jour\|30.*day" "90.*jour\|90.*day" "180.*jour\|180.*day\|read.only"; do
    if grep -qiE "$window" "$PROJECT_ROOT/retirement_plan.md" 2>/dev/null; then
      echo "  [OK] réversibilité window '$window' configured"
    fi
  done
  if ! grep -qiE "read.only\|read.only.window" "$PROJECT_ROOT/retirement_plan.md" 2>/dev/null; then
    echo "  [HIGH] no read-only réversibilité window (rollback impossible)"
  fi
fi

# Feedback (sensors) — closure memo completeness (per XG-10.7 + XG-10.8)
echo ""
echo "[feedback] Closure memo (per XG-10.7 + XG-10.8):"
if [ -f "$PROJECT_ROOT/closure_memo.md" ]; then
  for concept in "tag.*EOL\|final.*tag" "signature\|HMAC\|GPG" "lessons.*learned\|post.mortem.*EOL" "communication.*sent\|stakeholder.*notif"; do
    if grep -qiE "$concept" "$PROJECT_ROOT/closure_memo.md" 2>/dev/null; then
      echo "  [OK] closure concept '$concept' present"
    else
      echo "  [MED] closure concept '$concept' missing"
    fi
  done
fi

echo ""
echo "=== Run via: adv-loop 10 [work_dir] ==="
exit 0
