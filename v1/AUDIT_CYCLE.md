# Audit Cycle — Karpathy-aligned recurring discipline

> Codifies the harness's **recurring audit methodology**, drawing on Andrej Karpathy's five principles for evidence-driven iteration. The methodology is what carried the harness from grade D to grade S in 8 iterations (documented in `.ai/docs/designs/FINAL_TRAJECTORY_2026-06-01.md`).

**Status**: methodology document. Operationalized via the `state_engine.py self_audit` CLI subcommand (one-shot) and the [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md) (durable record).

---

## The 5 Karpathy principles

The harness adopts the discipline from `~/.claude/skills/karpathy-skills/SKILL.md`. Status of implementation:

| # | Principle | Status | How it shows up in the harness |
|---|---|---|---|
| 1 | **Human-authored instruction documents** | ✅ implemented | `CLAUDE.md`, `docs/v1/*.md`, ADRs are the canonical instruction surface for the dispatcher. |
| 2 | **Iteration with evidence** | ✅ implemented | The 8-iteration trajectory is codified in `FINAL_TRAJECTORY_2026-06-01.md` + [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md). |
| 3 | **Skill composition** (`[[skill:name]]` syntax) | ✅ documented | [`PHASE_SKILLS.md`](PHASE_SKILLS.md) uses the notation. The harness does not resolve the references at runtime. |
| 4 | **Fixed-budget experimentation** | ✅ codified here | See §"Audit cadence + budget" below. |
| 5 | **Multi-model collaboration** | ⚠️ opt-in | v1 ships single-model. Documented in §"Multi-model collaboration" with explicit "opt-in, requires manual setup" disclaimer. |

---

## Audit cadence + budget

### Quarterly cycle

Run the full 4-role council (CISO, QA Lead, Architect, DevOps) every 90 days (or whenever a CRIT finding suggests a regression). The cycle is **operator-triggered**, not automatic.

```bash
# One-shot audit (no external agent calls — uses the harness's own DB)
python3 scripts/lib/state_engine.py self_audit

# Council mode (opt-in; requires MULTIAGENT_BRIDGE_ENABLED=1)
MULTIAGENT_BRIDGE_ENABLED=1 python3 scripts/lib/state_engine.py self_audit --council
```

### Token budget

For a full SDLC run with `--council`:

- 4 reviewers × ~10k output tokens per role × 5 phase transitions ≈ **200k output tokens per cycle**
- Per-quarter cost: ≈ 200k tokens
- Per-year cost: ≈ 800k tokens

This is the order-of-magnitude estimate documented in `ADR-003-multiagent-bridge.md` §"Cost envelope".

### Rotation rule (Karpathy principle 5 — partial)

Across consecutive audit cycles, **rotate the auditor agents** so the same agent does not grade the same role twice in a row. The rotation matters more for evidence diversity than for raw quality; a single agent re-grading the same code will tend to confirm its prior verdict.

In v1, the harness has only one model available, so rotation happens at the *role prompt level* (different reviewer system prompts) — not at the model level. v2 (post-G.4) may introduce multi-model rotation; for now, treat the rotation rule as a documented best practice.

---

## Audit cycle workflow

```
┌──────────────────────────────────────────────────────────────────────┐
│  MEASURE  →  PRIORITIZE  →  FIX  →  ISOLATE-VERIFY  →  REGRESSION   │
│                                  │                                    │
│                                  │  (verifier-agent ≠ fixer-agent)    │
└──────────────────────────────────────────────────────────────────────┘
                                  ↑
                                  └─── repeat until ∀ grade ≥ S
                                       OR 2 iterations no progress
                                          → ESCALATE to refactor
```

### Step 1 — MEASURE

Run `state_engine.py self_audit` for the data baseline. Then, if `MULTIAGENT_BRIDGE_ENABLED=1`, run with `--council` to get four independent opinions.

The output is a markdown report listing:
- Current `adversarial_log` verdict counts (PASS / DENY / FIXTURE)
- Last 30 days of `state_events` transitions
- Last 30 days of `circuit_breaker_events` (blocked counts per file)
- HMAC chain integrity status for all 4 audit tables

### Step 2 — PRIORITIZE

For each finding from the council, score:
- **Severity** (CRIT / HIGH / MED / LOW)
- **Blast radius** (single file / cross-file / cross-phase)

Top priority = lowest current grade × highest blast radius.

### Step 3 — FIX

Apply fixes in batches of ≤ 3 changes per iteration. Each fix lands as an `AUDIT-YYYY-MM-DD FIX (<finding-id>)` comment in the affected file.

### Step 4 — ISOLATE-VERIFY (the anti-tautology rule)

**The agent that verifies a fix is NEVER the agent that applied it.** This is the discipline that broke the previous "92/92 PASS" tautology trap (an agent grading its own code always confirms its own claims).

Operational rules:
- Council audits MUST be run sequentially, not in parallel (parallel agents writing to the same SQLite DB cause contention — see [`TEST_STABILITY.md`](TEST_STABILITY.md)).
- The verifier agent prompt MUST NOT include "you fixed X" — only "audit fresh".
- The verifier agent reads the code from scratch, no prior context about what was done.

### Step 5 — REGRESSION

Full test suite MUST stay green. The pre-commit gate (`bash scripts/pre-commit-hook.sh`) is the gating mechanism.

### Escalation rule

If 2 consecutive iterations show no grade movement for any category, escalate from patch to refactor. Patches alone will not break a structural ceiling — sometimes the engine itself needs to change (e.g. the ITER4 atomic-UPSERT fix replaced a SELECT-then-UPDATE pattern; no amount of retry tuning would have worked).

---

## Multi-model collaboration (Karpathy principle 5)

**v1 ships single-model by design.** The 4-role council uses 4 different *prompts* against 1 model. Multi-model rotation would require:

1. A second LLM provider configured (e.g. via `~/.claude/skills/llm/` skill which wraps `z.ai` and local MLX).
2. A routing layer that dispatches each role to a different model.
3. Reconciliation logic when models disagree on severity.

None of this exists in v1. The opt-in path for downstream users:

```bash
# Configure a second provider (out of scope for the harness — see ~/.claude/skills/llm/)
export SWEBOK_SECONDARY_LLM=mlx:Qwen3.6-27B

# When self_audit --council is run, the dispatcher can choose to route
# (e.g.) the CISO and Architect roles to the secondary provider while keeping
# QA-Lead and DevOps on the primary. This is a DISPATCHER policy, not a
# HARNESS feature.
```

The harness emits the role list (via `<MULTIAGENT_LAUNCH>`); the dispatcher decides which model serves each role. The harness stays provider-neutral.

---

## Where evidence lives

- **`adversarial_log` table** (SQLite, HMAC-chained) — verdicts produced by gate transitions and self-audits. Queryable via `state_engine.py query_adversarial`.
- **[`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md)** — durable markdown ledger linking findings to fix commits and verification commands.
- **`.ai/docs/designs/AUDIT_*.md`** — point-in-time council reports (from the D→S trajectory and from each quarterly cycle).
- **`docs/v1/THREAT_MODEL.md`** — evolving threat surface. Updated when an OUT-OF-SCOPE row becomes an OPT-IN MITIGATED row (or vice versa).

The four sources are linked by **finding ID**: every CRIT-N / HIGH-N / MED-N tag appears in exactly one place (the originating audit), is fixed via a commit referencing that ID, and is verified via a re-run command logged in the ledger.

---

## Concrete worked example — the D→S journey

The 2026-06-01 / 06-02 trajectory is the worked example for this methodology. Summary (full detail in [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md)):

| Iteration | Council grade (CISO / QA / Architect / DevOps) | Key fix landed |
|---|---|---|
| 0 (claimed) | "100% / 100% / 100% / 100%" | (refuted by independent audit) |
| 0 (real) | D / D / C+ / C- | Baseline measurement |
| 1+2 | B / B / B- / B | Circuit-breaker fail-secure, auto-verify $2 unbound, rm -rf global block, YAML rot purge |
| 3 | B+ / B- / B+ / A | HMAC chain scaffolding, per-project isolation, CI workflow |
| 4 | _atomic UPSERT escalation_ | Replaced SELECT-then-UPDATE with single-statement UPSERT → 1000/1000 atomic |
| 5 | S / A / A- / A | HMAC wired into 4 audit INSERTs; tamper detection live |
| 6-7 (regression) | A / C / B- / F | Concurrent multi-agent test load caused flakes; reverted bad changes |
| **8 (sequential council)** | **S / S / S / S** | Council audits run sequentially; per-PID isolated counter; CI matrix green |

This trajectory is the canonical example: 8 iterations, anti-tautology rule applied, escalation triggered once (ITER4), final result documented and reproducible.

---

## When to skip this cycle

The methodology has cost. Skip the council in these cases:

- **Hotfix for a single CRIT** that has a clear regression test. Land the fix + the test; the next quarterly cycle will surface any side-effect.
- **Documentation-only changes** (typos, broken links). No council needed.
- **Refactor under an existing passing test suite** where the test suite IS the contract (e.g. the ITER6 CLI extraction). The tests are the council.

Skipping is a choice. The ledger records *what* was skipped and *why*.
