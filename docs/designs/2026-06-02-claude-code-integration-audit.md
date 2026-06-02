# Adversarial Audit — Claude Code Integration Opportunities for SWEBOK v4 Harness

**Date**: 2026-06-02
**Scope**: Inventory of everything installed locally under `~/.claude/`, mapped against the 9 SWEBOK v4 phases, with an adversarial assessment of integration risk vs reward.

**Audit posture**: skeptical. Default is **do NOT integrate** unless the skill/hook/plugin demonstrably raises the harness's S-grade ceiling or unlocks a phase the harness currently treats as a black box. Bloat, dependency creep, and prompt-injection surface area all weigh against integration.

---

## A. Inventory — what is actually installed

### A.1 Skills (45 total)

| Family | Skills | Notes |
|---|---|---|
| **Meta / orchestration** | `karpathy-skills`, `skill-invoker`, `skill-composer-test`, `iterative-code-design`, `discovery-orchestrator`, `continuity-council`, `project-continuity`, `caveman`, `nexus` (router) | Skill-about-skills. Evolution, composition, council, compaction, brevity. |
| **Speckit (SDLC commands)** | `core/speckit-specify`, `core/speckit-plan`, `core/speckit-implement`, `core/speckit-analyze`, `core/speckit-checklist`, `core/code-review` | Direct SDLC phase commands. **Already partially aligned with SWEBOK phases.** |
| **Nexus domain specialists** | `nexus-cto`, `nexus-architect`, `nexus-security`, `nexus-qa`, `nexus-devops`, `nexus-ciso`, `nexus-ai`, `nexus-backend`, `nexus-frontend`, `nexus-data-eng`, `nexus-fullstack`, `nexus-ds`, `nexus-docs`, `nexus-qa-lead`, `nexus-devops-lead` | Domain expertise — these are the **council** that audited the harness itself. |
| **Nexus management** | `nexus-ceo`, `nexus-cpo`, `nexus-pm`, `nexus-product`, `nexus-em`, `nexus-sm` | Product / process / project roles. |
| **Domain-specific** | `qa-feature-test-expert`, `speckit-qa`, `vitalite-coach`, `llm`, `zai-glm51-cost-opt` | One-shot specialists. |
| **Private (begin with `_`)** | `_council_cache`, `_versions`, `_iteration_data`, `_examples` | Internal state for karpathy-skills. |

### A.2 Hooks (`~/.claude/hooks/`)

| Hook | Purpose | Trigger |
|---|---|---|
| `karpathy_skills_hook.sh` | Skill activation log + async orchestrator analysis + hourly maintenance | UserPromptSubmit |
| `hyperagent_hook.sh` | Post-evolution log, pre-mutation backup, improvement check | Called by hyperagents framework |
| `ContextCheck.sh` | Pre-tool-use context-window probe | PreToolUse |
| `PreCompact.sh`, `PreCompact_transfer.sh` | Capture context before auto-compaction | PreCompact |
| `SessionStart_transfer.sh`, `SessionEnd.sh` | Hand-off file refresh at session boundaries | SessionStart / SessionEnd |
| `UserPromptSubmit_with_context.sh` | Inject latest handoff into the first prompt of a session | UserPromptSubmit |
| `continuity/` (15 Python hooks) | Project-state durability, auto-handoff, debounce, sanitisation, destructive-command guard, health check, daemon | Multiple |
| `event/pr-created.yaml`, `event/branch-naming-enforcer.yaml` | Event-driven gates | Git event |
| `post-prompt/`, `post-task/`, `post-tool-use/`, `pre-prompt/`, `pre-task/`, `pre-tool-use/` | Empty directories (scaffolding) | n/a |

### A.3 Hyperagents framework (`~/.claude/hyperagents/`)

A separate evolutionary engine for **skill mutation + evaluation**. Layout:
- `core/` — engine (~25 Python files)
- `eval/`, `sandbox/`, `tests/` — fitness evaluation and isolated mutation testing
- `skills/meta/` and `skills/task/` — meta-skills and task-skills
- `continuity/` — state persistence
- `archive/snapshots/` — version history
- `run.py`, `run_tests.py`, `validate.py` — entrypoints

This is the engine the karpathy hook calls into. **Self-evolving skills**: a mutation runs in sandbox, gets evaluated, and is promoted only if its fitness exceeds the baseline.

### A.4 Plugins (`~/.claude/plugins/`)

| Plugin | Provider | Content |
|---|---|---|
| `spec-kit@anthropic` (0.0.1) | `anthropics/claude-plugins-official` | `speckit-init` skill (only init for now — implementation lives in user skills) |
| `claude-mem@thedotmack` (12.1.0) | `thedotmack/claude-mem` | Memory + RAG: `do`, `knowledge-agent`, `make-plan`, `mem-search`, `smart-explore`, `timeline-report`, `version-bump` |
| `understand-anything@understand-anything` (2.7.5) | `Lum1104/Understand-Anything` | Code-understanding suite: `understand`, `understand-chat`, `understand-dashboard`, `understand-diff`, `understand-domain`, `understand-explain`, `understand-knowledge`, `understand-onboard` + 9 reviewer/analyzer agents |
| `zai-coding-plugins` (glm-plan-bug, glm-plan-usage) | z.ai marketplace | GLM-powered planning helpers |

### A.5 Other infrastructure

- `~/.claude/qa/` — QA framework with `test-matrix.yaml`, runner scripts, project-type detection (api/web/mobile/shared_mobile)
- `~/.claude/sessions/` (private), `~/.claude/session-env/` — per-session state
- `~/.claude/projects/` (private) — per-project memory
- `~/.claude/file-history/` — file change journal
- `~/.claude/plans/` — saved plans
- `~/.claude/commands/` — slash commands

---

## B. Mapping to SWEBOK v4 phases

The harness today enforces phases P1–P9 but **does nothing positive** to *help* the user execute each phase — it only blocks. The opportunity is to wire the **right skill per phase** as a soft suggestion (not an automatic invocation).

| Phase | Current harness behavior | Skills that could help (per-phase opportunity) |
|---|---|---|
| **P1 Requirements** | Blocks code writes | `discovery-orchestrator` (cadrage), `nexus-product` (backlog/stories), `nexus-pm` (planning), `core/speckit-specify` |
| **P2 Architecture** | Blocks code writes | `nexus-architect`, `nexus-cto`, `nexus-ciso` (security architecture), `core/speckit-plan` |
| **P3 Design** | Blocks `src/`, `impl/`, `.py` | `nexus-architect` (interface contracts), `iterative-code-design` (ICD design doc, mandatory tables) |
| **P4 Estimation** | Same as P3 | `nexus-em`, `nexus-sm` (story-point estimation), `nexus-pm` |
| **P5 Construction** | Blocks `mkdir src` (new tree only), destructive cmds | `nexus-backend`, `nexus-frontend`, `nexus-fullstack`, `nexus-ai`, `nexus-data-eng` |
| **P6 Verification** | Tests only; non-test src blocked | `nexus-qa`, `nexus-qa-lead`, `speckit-qa`, `qa-feature-test-expert`, `core/code-review` |
| **P7 Deployment** | Destructive cmds blocked | `nexus-devops`, `nexus-devops-lead`, `nexus-ciso` (deployment risk) |
| **P8 Maintenance** | Destructive cmds blocked | `nexus-em`, `nexus-docs`, `nexus-ds` (analytics) |
| **P9 Retirement** | Package managers blocked (except security/patch) | `nexus-docs` (decom docs), `nexus-ciso` (data-destruction policy) |
| **Cross-phase** | — | `karpathy-skills` (skill evolution), `continuity-council` (recurring audit), `project-continuity` (memory) |

---

## C. Adversarial assessment — per integration candidate

For each candidate, I weigh:
- **Reward**: does this raise the S-grade ceiling? Does it close a real gap?
- **Risk**: dependency creep, prompt-injection surface, false-positive blocking, lock-in, bloat in `state_engine.py`, contamination of the threat model.

### C.1 The Nexus council (15 domain specialists)

**Reward (HIGH)**. The harness's own gate verdicts (`adversarial-gate.sh`) currently use **hardcoded fixture strings**. Replacing them with real council calls to `nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops` on each gate transition would close CRIT-2 from the audit ("adversarial-gate is a fixture"). This is the **single biggest S-grade win** still on the roadmap.

**Risk (MEDIUM)**.
1. Council calls cost real tokens per gate transition (5 phase transitions × 4 reviewers × ~10k tokens = 200k tokens per full SDLC run).
2. The harness becomes coupled to skills that live OUTSIDE the harness repo — un-portable.
3. A misbehaving sub-agent could write malformed DSL; the gate would have to enforce `=^[A-Z_]+:` discipline rigorously.
4. Prompt-injection: an attacker who controls the file being gated could embed text designed to manipulate the Nexus reviewer.

**Verdict**: **Integrate — but as opt-in**. Default `adversarial-gate.sh` stays a fixture (declared as such); add a `--council` flag and a `MULTIAGENT_BRIDGE` env that wires the 4 Nexus skills via the existing XML envelope. The DSL contract is already in place; the missing piece is the dispatcher loop.

**Per-phase prescription**:
- P1/P2 transitions → `nexus-product`, `nexus-architect`
- P3/P4 transitions → `nexus-architect`, `nexus-cto`
- P5/P6 transitions → `nexus-qa-lead`, `nexus-security`
- P7/P8 transitions → `nexus-devops-lead`, `nexus-ciso`
- P9 transition → `nexus-ciso`, `nexus-docs`

### C.2 Iterative-code-design skill

**Reward (HIGH)** for P3 (Design). Forces a structured design doc with baseline inventory, decision ledger, compression review — three mandatory tables that prevent append-only code. The harness used this skill during its own self-design (`.ai/docs/designs/2026-06-01-state-engine-review.md` is the artifact).

**Risk (LOW)**. Skill is well-defined, has a clock floor, refuses to implement (clear scope boundary).

**Verdict**: **Recommend (don't enforce)**. P3 entry should *suggest* `/iterative-code-design` if the spec is non-trivial. Do not block on its absence.

### C.3 Discovery-orchestrator

**Reward (HIGH)** for P1 (Requirements). Multi-expert needfinding produces JTBD framing, constraints, success criteria — directly fills the P1 deliverable.

**Risk (LOW)**. Pure discovery skill, no code-mutating tools.

**Verdict**: **Recommend on P1 entry**. The harness could detect "user typed a fuzzy idea, current phase is P1" and surface the skill via the dispatcher's hot-path log.

### C.4 Karpathy-skills (skill evolution)

**Reward (MEDIUM-HIGH)** as a *meta-tool*. Evidence-based iteration on the harness's own scripts is exactly the methodology that brought the harness from D to S grade in 8 iterations. Wiring this into a `harness self-evolve` command would let the system improve over time without manual intervention.

**Risk (HIGH)**.
1. Evolution loops can drift — the karpathy hook backs up to `~/.claude/hyperagents/backups/`; the harness would need its own backup discipline.
2. The hyperagents framework is **external Python code** (~25 files in `~/.claude/hyperagents/core/`) that the harness would now depend on. Major coupling.
3. The hourly maintenance cron in `karpathy_skills_hook.sh` would conflict with the harness's own pre-commit gate.
4. **Adversarial risk**: a mutation that *accidentally* weakens a phase rule but improves a fitness metric would be auto-promoted. The fitness function would have to include the **adversarial test suite**, not just functional tests.

**Verdict**: **DO NOT INTEGRATE in v1.0**. The risk is too high without a tight fitness contract. Document as a v2.0 candidate with a hard requirement: any mutation must pass `tests/adversarial-test.sh` + `tests/attack-payloads-test.sh` + `scripts/health-check.sh` + `verify_audit_chain` *before* being promoted.

The **Karpathy principles** themselves (evidence-based iteration, fixed-budget experimentation, multi-model collaboration) are already implemented in the harness's audit methodology. The codified loop in `karpathy-skills` is the auto-promote that introduces the risk.

### C.5 Continuity-council + project-continuity

**Reward (MEDIUM)** for P6/P7 (verification, deployment readiness) and cross-phase memory. The continuity-council skill explicitly runs a 5-expert review of the **continuity system** itself — directly parallel to our 4-expert council that audited the harness. The methodology is sound.

`project-continuity` keeps `CLAUDE.md` concise + writes handoff files. Useful for the dispatcher's anti-rot every-5-calls nudge that already exists.

**Risk (LOW)**.
1. Writes outside the harness repo (`.claude/context/`). The harness should be the source of truth.
2. Memory poisoning: an attacker could embed instructions in a handoff file.

**Verdict**: **Integrate `project-continuity` as the ANTI-ROT skill target.** Replace the current `ANTI-ROT:NUDGE run project-continuity` line with a real wire to the skill. Reuse `continuity-council` methodology as the *recurring audit* for the harness itself (quarterly, not on every commit).

### C.6 Speckit family

**Reward (HIGH)** as the **command alias layer**. The user's global `~/.claude/CLAUDE.md` already routes via `/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.checklist → /speckit.plan → /speckit.tasks → /speckit.analyze → /speckit.implement`. The harness's 9 phases map naturally:

| Phase | Speckit command |
|---|---|
| P1 | `/speckit.constitution`, `/speckit.specify`, `/speckit.clarify` |
| P2 | `/speckit.plan` |
| P3 | `/speckit.plan`, `/speckit.checklist` |
| P4 | `/speckit.tasks` |
| P5 | `/speckit.implement` |
| P6 | `core/code-review`, `speckit-qa` |
| P7-P9 | (gap — no speckit command) |

**Risk (LOW)**. These are command aliases. They invoke other skills; they don't mutate the harness.

**Verdict**: **Document the mapping in `docs/v1/PHASES.md`**, do not auto-invoke. The user already has the `/speckit.*` commands; the harness gains nothing by re-wiring them but a lot by *documenting that they exist and map cleanly*.

### C.7 Claude-mem plugin

**Reward (MEDIUM)** for cross-session memory. RAG-driven `mem-search` could replace the harness's current `replay_session(t0, t1)` raw audit dump with semantic search over past gate verdicts.

**Risk (HIGH)**.
1. Node.js dependency (the plugin is npm-based). The harness is Python + Bash + SQLite — no Node.js required today. Adding it doubles the install footprint.
2. The plugin maintains its OWN memory store; reconciling with our SQLite audit log creates a dual-source-of-truth that ADR-001 explicitly argued against.
3. macOS-only path (`/Users/dorianciet/...`) in the install metadata — portability risk.

**Verdict**: **DO NOT INTEGRATE**. The harness's `query_*` CLI commands cover the same use case without external dependencies. Plugin is useful for the *user*, not for *the harness*.

### C.8 Understand-anything plugin

**Reward (LOW-MEDIUM)** for P3/P5 (design + construction). Code-understanding via knowledge graph is interesting for onboarding to an existing codebase, but the harness's own scope is *enforcing SDLC discipline*, not *explaining code*.

**Risk (HIGH)**. Same Node.js dependency footprint as claude-mem. Plus pnpm + TypeScript tooling. Major install creep.

**Verdict**: **DO NOT INTEGRATE**. Out of scope.

### C.9 zai-coding-plugins (`glm-plan-bug`, `glm-plan-usage`)

**Reward (LOW)**. GLM-powered planning helpers. Cross-model collaboration is interesting but z.ai is a third-party LLM vendor; integrating multi-vendor support is a different project.

**Verdict**: **DO NOT INTEGRATE**.

### C.10 Hooks worth borrowing (not whole)

| Hook | Borrow what |
|---|---|
| `ContextCheck.sh` | The pre-tool-use context-window probe — useful as a soft warning before P5 long-running implementation work |
| `continuity/auto_handoff.py` | Pattern: idempotent handoff write with debounce. The harness's ANTI-ROT nudge already does this conceptually; could reuse the debounce logic. |
| `continuity/guard_destructive.py` | Cross-check with the harness's global destructive list. Make sure we're at least as strict. |
| `continuity/sanitization.py` | Read its rules — could harden the harness's `_audit_secret` HMAC paths |
| `continuity/health_check.py` | Already inspired the harness's `scripts/health-check.sh`. Confirm no missed checks. |

**Verdict**: **Borrow patterns, not files**. The harness is a self-contained repo; copying external files would re-introduce the cross-tree coupling we just removed.

### C.11 QA framework (`~/.claude/qa/`)

**Reward (MEDIUM)** for P6 + auto-deploy gate. Per-project-type test matrix (api/web/mobile/shared_mobile) with auto-deploy rules. The harness's `tests/adversarial-test.sh` is a single bash file — adding a project-type-aware matrix would let downstream users gate on relevant subset only.

**Risk (LOW)**. Test infrastructure addition, not state-engine change.

**Verdict**: **Recommend documenting the integration pattern** in `docs/v1/TEST_STABILITY.md`. The harness already provides `pre-commit-hook.sh`; the QA framework provides per-project test orchestration on top. They're complementary, not conflicting.

---

## D. Recommendation matrix — what to actually integrate

| Candidate | Reward | Risk | Decision | Phase target |
|---|---|---|---|---|
| **Nexus council (4 skills) wired to `adversarial-gate.sh --council` flag** | HIGH | MED | ✅ **Integrate** as opt-in | All transitions |
| **Project-continuity as ANTI-ROT skill target** | MED | LOW | ✅ **Integrate** (replace nudge text with real skill invocation) | Cross-phase |
| **Discovery-orchestrator suggestion on P1 entry** | HIGH | LOW | ✅ **Recommend** (hot-path log nudge) | P1 |
| **Iterative-code-design suggestion on P3 entry** | HIGH | LOW | ✅ **Recommend** | P3 |
| **Speckit command-to-phase mapping documented** | HIGH | LOW | ✅ **Document only** | All |
| **QA framework integration pattern doc** | MED | LOW | ✅ **Document only** | P6 |
| **Continuity-council methodology adopted as recurring audit cycle** | MED | LOW | ✅ **Document only** | Quarterly cross-phase |
| **Karpathy-skills auto-evolution loop** | MED-HIGH | HIGH | ❌ **Defer to v2.0** with fitness contract | Meta |
| **Claude-mem RAG memory** | MED | HIGH | ❌ Out of scope (Node.js dep, dual SoT) | — |
| **Understand-anything code RAG** | LOW-MED | HIGH | ❌ Out of scope | — |
| **zai-coding-plugins (GLM)** | LOW | LOW | ❌ Out of scope (third-party LLM) | — |
| **External hooks (borrow patterns)** | LOW | LOW | ✅ Cross-reference, do not copy | n/a |

---

## E. Karpathy rules — what is and isn't already implemented

The five Karpathy principles from `karpathy-skills/SKILL.md`:

| Principle | In harness today? | Evidence |
|---|---|---|
| 1. Human-authored instruction documents | ✅ | `CLAUDE.md`, `docs/v1/*.md`, ADRs are the instruction surface for the model. |
| 2. Iteration with evidence | ✅ Partial | The 8-iteration trajectory `D → S` was evidence-based (live test results, council audits). But there's **no codified loop** — every iteration was driven by user prompts. |
| 3. Skill composition | ❌ | No `[[skill:name]]` syntax in the harness's docs. Phase docs reference each other by relative path, not by skill ID. |
| 4. Fixed-budget experimentation | ❌ | No explicit token / iteration budget for harness self-improvement. The audit cycles ran ad-hoc. |
| 5. Multi-model collaboration | ⚠️ Implicit | The council audits used multiple agents (CISO / QA / Architect / DevOps) but all on the same model. No cross-model verification. |

**Gap**: principles 3, 4, 5 are not implemented. Principle 2 is half-done.

### E.1 Proposed Karpathy-aligned additions

Without integrating the auto-evolution risk (C.4), we can adopt the **discipline** of Karpathy's approach:

1. **Skill composition**: add `[[skill:nexus-ciso]]` markers to `docs/v1/PHASES.md` so the dispatcher / Claude knows which skill is canonical for each phase. Pure documentation change.

2. **Fixed-budget experimentation**: codify the audit cycle as `docs/v1/AUDIT_CYCLE.md` — "every quarter, spend up to N tokens on a fresh council audit; rotate auditor agents; promote a finding to a CRIT fix only if 2/3 auditors confirm it independently."

3. **Multi-model verification**: extend the council to optionally invoke a *different* model (e.g. via the `llm` skill that already wraps z.ai/MLX) for one of the four roles. Pure orchestration change.

4. **Evidence ledger**: add `docs/v1/EVIDENCE_LEDGER.md` — a table of (date, finding ID, evidence command, result). The 30+ verify-* tasks the harness already produced are exactly this; just persist them.

These four additions cost ~200 LOC of docs + a small `harness self-audit` CLI subcommand. No external dependency.

---

## F. Adversarial risks the audit DELIBERATELY rejects

Things I considered and dismissed:

1. **Hyperagents evolutionary engine as a runtime dependency** — pulls in ~25 Python files and an hourly maintenance cron. Coupling > S-grade benefit.
2. **Plugins via Node.js** (claude-mem, understand-anything) — dual SoT, install footprint doubling.
3. **Cross-model GLM/MLX as default** — third-party LLM vendor lock-in. Add as opt-in only, not default.
4. **`~/.claude/qa/` test matrix as gating** — useful for downstream USERS, not for the harness's own self-tests. Document only.
5. **Auto-invocation of skills from the harness** — the harness is a *gate*, not a *prescriber*. Soft suggestion (hot-path log) is the correct lever; auto-invoke would conflict with the gate's neutrality.

---

## G. Concrete S-grade-raising integrations — proposed scope

### G.1 P0 (minimum) — what to land in v1.1 (no behavioural risk)

1. **Document Speckit → SWEBOK phase mapping** in `docs/v1/PHASES.md` (~30 lines).
2. **Document Karpathy-aligned discipline** as `docs/v1/AUDIT_CYCLE.md` + `docs/v1/EVIDENCE_LEDGER.md` (~150 lines).
3. **Document recommended skills per phase** in `docs/v1/PHASE_SKILLS.md` (`/iterative-code-design` for P3, `/discovery-orchestrator` for P1, etc.) — pure suggestion table.
4. **Document continuity-council methodology** as the harness's own recurring audit cycle (Q4 review trigger).

Cost: ~400 LOC of docs. Zero code change. Zero behavioral change. **Raises Architect grade** (more complete spec).

### G.2 P1 — light wiring (v1.2)

5. **Wire `project-continuity` as the real ANTI-ROT target.** Replace the nudge text with an actual skill invocation when the user accepts the nudge. Keep the nudge itself as the trigger.
6. **Add a `harness self-audit` CLI subcommand** that triggers the recurring quarterly council in a one-shot. Uses existing `query_adversarial`, `query_log_events`, and emits a single markdown report.

Cost: ~150 LOC. **Raises CISO grade** (real adversarial cycle, not fixture).

### G.3 P2 — real council wired to gates (v1.3)

7. **Add `--council` mode to `scripts/adversarial-gate.sh`** that drives the existing `<MULTIAGENT_LAUNCH>` XML through real Nexus skills (`nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead`).
8. **Wire the council DSL output to `--judge-only`** path so the verdict comes from real adversarial review, not a hardcoded table.
9. **Document the cost envelope** (~200k tokens per full SDLC run) and the operator-controlled `MULTIAGENT_BRIDGE_ENABLED` flag.

Cost: ~300 LOC + a small `multiagent-launcher.sh` rewrite. **Eliminates the last CRIT (CRIT-2 from the original audit)** — the gate is no longer a fixture.

### G.4 P3 — Karpathy evolution loop (v2.0)

10. **Self-evolution sandbox** for harness rules (regex updates, new phase rules). Mutation runs in a tmpfs DB, must pass `adversarial-test.sh` + `attack-payloads-test.sh` + `verify_audit_chain` + `health-check.sh` BEFORE being promoted to the live tree.

Cost: ~800 LOC. **High risk**, gate must be airtight. Defer until v2.0 with explicit fitness contract.

---

## H. Final recommendation

**Land G.1 and G.2 now** (v1.1 + v1.2). They are pure docs + a tiny CLI command. Zero risk to the S grade. Both raise the **completeness** dimension of the Architect and CISO grades.

**Land G.3 next** (v1.3). The council wiring is the single biggest substantive win still on the roadmap and the original audit's CRIT-2 is still flagged in `SECURITY.md` and `adversarial-gate.sh`'s honesty banner. Closing it lifts the harness from "honest about being a fixture" to "real adversarial review".

**Defer G.4 to v2.0** with the explicit fitness contract: any mutation must pass the full adversarial suite *before* promotion.

**Reject everything else** in this audit — claude-mem, understand-anything, zai-coding-plugins, the hyperagents auto-loop, dual-SoT memory layers. They are useful tools for the *user* but they raise the harness's coupling without raising its S-grade ceiling.

Awaiting your direction on which of G.1 / G.2 / G.3 / G.4 to proceed with. My recommendation is: **G.1 + G.2 in one PR (low risk), then G.3 in a separate PR with the cost envelope clearly documented**.
