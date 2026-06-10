# Feature 3 — Elaborate Adversarial Harness per Phase

> **Date** : 2026-06-10
> **Goal** : each phase has an elaborate adversarial harness for serene + reliable validation
> **Status** : 🚧 In progress

## 1. Problem statement

Currently `specs/adversarial-patterns/` has:
- ✅ 3 useful patterns (P0, P5, P7)
- ⚠️ 8 stub patterns (P1, P2, P3, P4, P6, P8, P9, P10)

Each stub needs to be implemented with:
- Feedforward controls (computational, deterministic)
- Feedback controls (computational + inferential)
- Stop conditions (mechanical)
- Self-tests
- Documentation

## 2. Per-phase adversarial harness design

### 2.1 Standardized pattern template

Each `specs/adversarial-patterns/phase-N-*.sh` should have:

```bash
#!/bin/bash
# Phase N (Name) — Adversarial Harness
# Per swebok spec phase-N-name.md
# Required deliverables: [list]
# Demarcation: [N] ≠ [N-1] and [N] ≠ [N+1]
# Stop conditions: [time/tokens/value]

set -e

# === 1. Feedforward (pre-phase) ===
echo "[feedforward] P{N} required deliverables:"
for d in [deliv1, deliv2, ...]; do
  [ -f "$PROJECT_ROOT/$d" ] && echo "  [OK] $d" || echo "  [MISSING] $d"
done

# === 2. Feedback (post-phase) ===
echo "[feedback] P{N} section validation:"
[validation checks]

# === 3. Demarcation check ===
echo "[feedback] P{N} demarcation (no P{N-1} or P{N+1} keywords):"
[N-1 and N+1 keywords check]

# === 4. Adversarial patterns ===
echo "[feedback] P{N} specific antipatterns:"
[domain-specific patterns]

# === 5. Stop conditions ===
# Time: 30 min default
# Tokens: 4k/7k/10k default
# Iterations: 5 max
# Value: 3 LOW in a row = stop
```

## 3. Per-phase implementation plan

| Phase | Specific checks needed | Effort |
|---|---|---|
| P1 Feasibility | ROI calcul, GO/NO-GO memo, alternatives document | 1h |
| P2 Requirements | SRS structure (IEEE 830), RTM, user stories format | 1h |
| P3 Architecture | ADRs (min 1 per structurant decision), C4 diagrams | 1h |
| P4 Design | API contracts (OpenAPI), data_model, sequence diagrams | 1h |
| P6 Testing | Test plan, mutation report, coverage report | 1h |
| P8 Operations | SLOs defined, runbooks exist, on-call rotation | 1h |
| P9 Maintenance | Tech debt register, refactoring plan, ADRs | 1h |
| P10 Retirement | Data archival, user migration, closure memo, RGPD | 1h |

**Total** : 8h for all 8 patterns

## 4. Self-tests per pattern

Each pattern script must have:

```bash
# tests/adv-loop/test_phase_N_pattern.sh
# - Run pattern on a clean dir → should pass
# - Run pattern on a dir with missing deliv → should fail
# - Run pattern on a dir with forbidden keywords → should flag
```

## 5. Tests (acceptance criteria)

- [ ] Test 1: `bin/adv-loop N` returns 🟢 OK on clean dir for all 11 phases
- [ ] Test 2: `bin/adv-loop N` returns 🟠 HIGH on dir with missing deliverables
- [ ] Test 3: `bin/adv-loop N` flags forbidden keywords for adjacent phases
- [ ] Test 4: stop conditions trigger correctly (time, tokens, value)
- [ ] Test 5: each phase has ≥3 feedforward + ≥3 feedback checks
- [ ] Test 6: each pattern has self-tests passing
- [ ] Test 7: end-to-end test: run all 11 patterns on real swebok dir → all 🟢 OK
- [ ] Test 8: latency <1s per phase
- [ ] Test 9: works offline (no network)
- [ ] Test 10: docs (README) updated with all 11 patterns

## 6. Status

- 🚧 In progress
- 3/11 patterns done (P0, P5, P7)
- Next: implement P1, P2, P3, P4, P6, P8, P9, P10
- Effort: 8h

## 7. Implementation log

```
[2026-06-10] Sprint 3 START. Patterns P0, P5, P7 done
[2026-06-10] Implementing P1 (feasibility)
[2026-06-10] Implementing P2 (requirements)
[2026-06-10] Implementing P3 (architecture)
[2026-06-10] Implementing P4 (design)
[2026-06-10] Implementing P6 (testing)
[2026-06-10] Implementing P8 (operations)
[2026-06-10] Implementing P9 (maintenance)
[2026-06-10] Implementing P10 (retirement)
```

(Each iteration adds a line here)
