# SLOs & Alerting — SWEBOK v4 Harness

> **Doc version** : 1.0
> **Date** : 2026-06-10
> **Owner** : maintainer
> **Scope** : the SWEBOK v4 distilled harness (this repo) — single-user / single-team
> **Goal** : close the DevOps gap (no SLO / no alerting) flagged in COUNCIL_REPORT.md

---

## 1. Service Definition

The harness is a **local, single-user development tool** wrapping Claude Code with adversarial gates. It is not a 24/7 web service. The SLOs therefore target **interactive developer workflows** (latency, correctness, durability) rather than classical availability.

### User-facing surfaces

| Surface | Trigger | Expected cadence | Criticality |
|---|---|---|---|
| `bin/adv-loop test` | CI / pre-commit | per commit | HIGH (gates commit) |
| `bin/adv-loop corpus` | pre-commit / dev | per commit | HIGH (regression detector) |
| Mini-council (per Write) | PostToolUse hook | per edit | MED (defense, not blocking) |
| Council (every 5 edits) | PostToolUse hook | every 5 edits + 1h cooldown | MED (escalation only) |
| `bin/adv-loop auto-trigger` | UserPromptSubmit | per user prompt | LOW (intent hint) |
| `bin/adv-loop steer` | manual | on demand | LOW (developer query) |

---

## 2. SLIs (Service Level Indicators)

| SLI | Definition | Measurement | Source |
|---|---|---|---|
| **Hook latency (p50/p95/p99)** | wall time of hook script | bash `$EPOCHREALTIME` | `pre-tool-use/token-counter.sh` |
| **Council round-trip** | envelope emit → judge response → judge DSL parse | manual / fixture | `lib/adv-loop/council.py` |
| **Test pass rate** | `(pass / total)` per suite | `bin/adv-loop test` | self-tests |
| **State DB integrity** | HMAC chain valid + schema version | `check_integrity` | `lib/state_engine.py` |
| **Hook fail-open rate** | hooks that exit 0 on internal error | `adversarial_log` table | audit trail |
| **Circuit breaker trips** | blocked attempts ≥ cap | `circuit_breaker` state | audit trail |
| **Push success rate** | force-pushes that pass pre-receive | `git push` exit code | git history |

---

## 3. SLOs (Service Level Objectives)

### Tier-1 SLOs (gating-critical)

| SLO | Target | Measurement window | Error budget |
|---|---|---|---|
| **`bin/adv-loop test` exit 0** | **≥ 99%** of runs in 30 d | rolling 30 d | 3% of commits may fail |
| **HMAC chain integrity** | **100%** after every rebuild | per event | 0% — every break is incident |
| **Mini-council hook latency p95** | **< 500 ms** | per edit | 5% of edits may be slower |
| **Council scheduler latency** | **< 1 s** to fire envelope (excluding LLM judge time) | per fire | 1% of fires may stall |

### Tier-2 SLOs (degraded, but not blocking)

| SLO | Target | Window | Error budget |
|---|---|---|---|
| **Auto-trigger latency p95** | **< 1 s** | per prompt | 10% may be slower (cache miss path) |
| **Steering summary latency** | **< 200 ms** | per `steer` call | 5% may be slower |
| **State DB rebuild time** | **< 2 s** | per cold start | 2% may exceed |
| **Token counter hook p99** | **< 100 ms** | per tool call | 1% may exceed |

### Tier-3 SLOs (informational, no budget)

| SLO | Target | Notes |
|---|---|---|
| Adversarial corpus coverage | **60 payloads × 11 phases** | growth measured in commits |
| Property-based test count | **≥ 44** (4 props × 11 phases) | growth = quality signal |
| Self-test count | **≥ 38** (5 S-units) | growth = feature coverage |

---

## 4. Alerting Thresholds

This is a local dev tool, so alerts are **stderr messages + log lines + circuit-breaker state**, not PagerDuty. The dispatcher (Claude) reads these and surfaces them to the user.

| Condition | Severity | Action | Surface |
|---|---|---|---|
| `check_integrity` ≠ `ok` | **CRIT** | halt, restore from `.db.corrupt.<ts>` | pre-commit stderr + log_events |
| Circuit breaker cap reached (1000) | **HIGH** | auto-override 5 min, emit `circuit_breaker:override_active=true` | `circuit_breaker` state |
| Mini-council p95 > 2 s for 10 consecutive edits | **MED** | emit warning DSL `mini_council:degraded=true` | mini_council hook stderr |
| Council scheduler fails to fire | **MED** | write to `adversarial_log`, log_events | audit log |
| Auto-trigger cache miss > 50% | **LOW** | warn, consider pattern layer | `lib/auto_trigger.py` |
| State DB size > 10 MB | **LOW** | suggest `clear_history` or rebuild | health check |
| Push failure on pre-receive | **HIGH** | display LFS / size guidance | git push stderr |

### Local alerting mechanism (no Prometheus)

The harness writes to **4 audit tables** in `.swebok_state.db` (HMAC-chained). An operator can query:

```sql
-- Recent circuit breaker events
SELECT * FROM circuit_breaker_events ORDER BY id DESC LIMIT 20;

-- Slow hook runs
SELECT * FROM log_events WHERE event_type='hook_latency' AND elapsed_ms > 500;

-- Mini-council escalations
SELECT * FROM adversarial_log WHERE severity IN ('CRIT', 'HIGH') ORDER BY id DESC LIMIT 20;
```

A `bin/adv-loop health` subcommand (see §6) aggregates these into a single verdict.

---

## 5. Observability Surfaces

| Surface | Format | Retention | Where |
|---|---|---|---|
| `adversarial_log` | DSL rows | forever (HMAC-chained) | `.swebok_state.db` |
| `log_events` | (ts, level, event_type, payload) | forever | `.swebok_state.db` |
| `state_events` | (ts, key, old_val, new_val) | forever | `.swebok_state.db` |
| `circuit_breaker_events` | (ts, file, attempt_count) | forever | `.swebok_state.db` |
| `.swebok_steering_state.db` | steering loop | forever | repo root |
| Stdout/stderr from hooks | human-readable + DSL | ephemeral | console |
| Git history (commits + force-pushes) | permanent | permanent | origin/master |

---

## 6. `bin/adv-loop health` Subcommand (new)

To make observability queryable, add a new CLI subcommand that aggregates SLO violations:

```bash
$ bin/adv-loop health
health:state_db=ok;;health:hmac_chain=ok;;health:circuit_breaker=clean
;;health:edits_since_council=2/5;;health:intent_phase=P3;;health:gates_validated=P1-P4
;;health:hooks_wired=14;;health:degraded=0;;health:verdict=🟢 OK
```

Exit codes:
- `0` = healthy
- `1` = degraded (one SLO at MED)
- `2` = broken (one SLO at CRIT or HMAC chain invalid)

This subcommand is the **single entry point** for "is the harness OK right now?".

---

## 7. Rollback / Recovery Runbook

| Failure | Recovery | Time to recover |
|---|---|---|
| State DB corrupt | `python3 lib/state_engine.py rebuild` (auto-renames corrupt to `.db.corrupt.<ts>`) | < 5 s |
| Audit chain broken | rebuild from `state_events` log; if unrecoverable, restore from last `git pull` | < 30 s |
| Hook spam / hang | `HARNESS_AUTO_TRIGGER=0` (kill-switch) | 0 s |
| Circuit breaker overflow | wait 5 min for override window OR delete `.swebok_state.db` | < 5 min |
| Council DSL parse fail | `bin/adv-loop corpus` to detect + manual review of `adversarial_log` | < 10 min |
| Push pre-receive rejected | follow size/LFS guidance, amend or `git lfs migrate` | < 1 h |
| Steering DB corrupt | `bin/adv-loop clear` to reset | < 1 s |
| `state_engine.py` 500 error | check `phase.history` for invalid value, restore from reflog | < 5 min |

---

## 8. Pre-commit Gate (already exists, documented here)

5-step gate (`.git/hooks/pre-commit`):
1. State DB cold rebuild + integrity
2. Warm-up `tests/adversarial-test.sh` (best-effort)
3. Authoritative `tests/adversarial-test.sh` (fails commit on FAIL)
4. HMAC chain walk
5. STRIDE-lite + health check

This is the **de-facto** SLO enforcement point for the harness itself.

---

## 9. What This Doc Closes (Council gaps)

| Council finding | Section that closes it |
|---|---|
| "no SLO" | §3 (SLOs), §4 (alerting) |
| "no alerting" | §4 (alerting thresholds + audit query patterns) |
| "no rollback runbook" | §7 (recovery runbook) |
| "no observability summary" | §5 (surfaces), §6 (health subcommand) |
| "steering CLI broken" | (separate fix in bin/adv-loop `steer\|steering` alias) |

---

## 10. Acceptance Criteria

- [ ] `bin/adv-loop health` returns `🟢 OK` on a clean install
- [ ] `bin/adv-loop health` returns exit 1 with `degraded=N` reason when a SLO is violated
- [ ] `bin/adv-loop health` returns exit 2 when HMAC chain breaks
- [ ] All 4 audit tables queryable via documented SQL
- [ ] Recovery runbook validated end-to-end (state DB rebuild + steering clear + push amend)
- [ ] Doc reviewed in next Council audit (CISO + DevOps judges)
