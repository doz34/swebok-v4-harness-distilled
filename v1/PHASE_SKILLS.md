# Phase-to-Skill Catalogue — SWEBOK v4 Harness

> Per-phase mapping between the harness's 9 SDLC phases (P1–P9) and the recommended Claude Code skills, Speckit commands, and Karpathy discipline.
> Source of truth: the harness phase rules in [`PHASES.md`](PHASES.md). The skills referenced here live in `~/.claude/skills/` and are **NOT bundled with the harness** — they are independent skills the dispatcher (Claude) can invoke.

**Status**: documentation only. The harness does NOT auto-invoke any skill. It emits structured suggestions (see [`HOOKS.md`](HOOKS.md) §"Structured ANTI-ROT nudge"); the dispatcher decides whether to honor them.

---

## At-a-glance per-phase table

| Phase | Speckit command | Nexus skills (primary) | Companion skills | What the user should produce |
|---|---|---|---|---|
| **P1** Requirements | `/speckit.constitution` → `/speckit.specify` → `/speckit.clarify` | `nexus-product`, `nexus-pm` | `discovery-orchestrator`, `nexus-ds`, `nexus-cpo` | Requirements doc, JTBD framing, success criteria |
| **P2** Architecture | `/speckit.plan` | `nexus-architect`, `nexus-cto` | `nexus-ciso` (security architecture), `nexus-ai`, `nexus-data-eng` | Architecture decision records, component diagrams |
| **P3** Design | `/speckit.plan` (refined), `/speckit.checklist` | `nexus-architect` | `iterative-code-design`, `nexus-backend`, `nexus-frontend` | Detailed design doc, interface contracts |
| **P4** Estimation | `/speckit.tasks` | `nexus-em`, `nexus-sm`, `nexus-pm` | `nexus-architect`, `nexus-product` | Task breakdown, story-point estimates |
| **P5** Construction | `/speckit.implement` | `nexus-backend`, `nexus-frontend`, `nexus-fullstack`, `nexus-ai`, `nexus-data-eng` | `nexus-architect`, `nexus-devops` | Working code, atomic commits |
| **P6** Verification | `/speckit.analyze`, `core/code-review` | `nexus-qa`, `nexus-qa-lead` | `speckit-qa`, `qa-feature-test-expert`, `nexus-security` | Tests, code-review findings |
| **P7** Deployment | _(none)_ | `nexus-devops`, `nexus-devops-lead` | `nexus-ciso`, `nexus-security` | Release artifacts, runbooks |
| **P8** Maintenance | _(none)_ | `nexus-em`, `nexus-devops` | `nexus-docs`, `nexus-ds` (analytics) | Bug fixes, regression suite |
| **P9** Retirement | _(none)_ | `nexus-ciso` (data destruction), `nexus-docs` | `nexus-em` | Decommission docs, data-purge attestation |
| **Cross-phase** | _(any)_ | `project-continuity` | `continuity-council`, `karpathy-skills`, `caveman` | Memory handoffs, audit cycles |

---

## Per-phase detail

### P1 — Requirements

**Goal**: convert a fuzzy intent into a structured needs framing.

| Skill | When to invoke | What it produces |
|---|---|---|
| `/speckit.constitution` | Project bootstrap | Project constitution doc |
| `/speckit.specify` | After constitution | Requirements specification |
| `/speckit.clarify` | If `specify` left ambiguities | Q&A doc that resolves them |
| `discovery-orchestrator` | Vague intent, conflicting goals, no clear JTBD | Multi-expert needfinding doc with JTBD, constraints, success criteria |
| `nexus-product` | Backlog / user stories work | Stories with acceptance criteria |
| `nexus-pm` | Project planning, dependencies, timeline | Task graph + milestones |
| `nexus-cpo` | Strategic alignment | Product roadmap |

**Harness behaviour in P1**: blocks all `.py/.ts/.js/...` writes and writes to `src/`, `lib/`, `impl/`. The intent is "no code until requirements are crisp".

### P2 — Architecture

| Skill | When | Produces |
|---|---|---|
| `/speckit.plan` | After requirements stable | Architecture plan |
| `nexus-architect` | System design, architecture patterns | Architecture decision records |
| `nexus-cto` | Stack choices, build/buy | Stack decision doc |
| `nexus-ciso` | Threat modeling pre-implementation | Security architecture doc |
| `nexus-ai`, `nexus-data-eng` | If AI/data is part of the architecture | Pipeline / model architecture |

**Harness behaviour in P2**: same as P1 (no code).

### P3 — Design

| Skill | When | Produces |
|---|---|---|
| `iterative-code-design` (`/iterative-code-design`) | Non-trivial design with multiple options | 14-section design doc with baseline inventory, decision ledger, compression review |
| `nexus-architect` (refined) | Interface contracts | API specs, schema designs |
| `/speckit.checklist` | Validation step before P4 | Checklist of design quality criteria |
| `nexus-backend`, `nexus-frontend` | Per-domain design depth | Component-level designs |

**Harness behaviour in P3**: blocks `src/`, `impl/`, `implementations/`, `.py`. Interfaces and contracts only.

### P4 — Estimation

| Skill | When | Produces |
|---|---|---|
| `/speckit.tasks` | Translate design into ordered tasks | Task list with dependencies |
| `nexus-em`, `nexus-sm` | Story-point estimation | Estimated backlog |
| `nexus-pm` | Schedule + critical path | Gantt-style timeline |

**Harness behaviour in P4**: same blocks as P3.

### P5 — Construction

| Skill | When | Produces |
|---|---|---|
| `/speckit.implement` | Execute the plan | Working code per spec |
| `nexus-backend`, `nexus-frontend`, `nexus-fullstack`, `nexus-ai`, `nexus-data-eng` | Per-domain implementation | Code that meets the design's interface contracts |
| `nexus-architect` | Mid-implementation design correction | Updated ADRs if reality forces change |
| `nexus-devops` | Build / CI setup alongside code | Build scripts, CI config |

**Harness behaviour in P5**: blocks `mkdir src` (new tree only — existing src/ stays writable) AND the global destructive list (`rm -rf /...`, `mkfs.*`, `DROP TABLE`, ...).

### P6 — Verification

| Skill | When | Produces |
|---|---|---|
| `/speckit.analyze` | Coherence check before review | Cross-spec analysis report |
| `core/code-review` | Diff review | Findings list (severity-graded) |
| `nexus-qa-lead` | Test strategy / quality gate design | Quality plan |
| `nexus-qa` | Test implementation | Unit / integration / E2E tests |
| `speckit-qa` | Per-feature test design | Feature test plan |
| `qa-feature-test-expert` | Edge-case enumeration | Boundary-case test suite |
| `nexus-security` | Security testing | OWASP / STRIDE pass |

**Harness behaviour in P6**: blocks any access to `/src/`, `/impl/`, `/implementations/` UNLESS the path contains `test/`, `spec/`, `__tests__/`, or `tests/`.

### P7 — Deployment

| Skill | When | Produces |
|---|---|---|
| `nexus-devops-lead` | Pipeline architecture | CI/CD design |
| `nexus-devops` | Implementation (Docker, K8s, Terraform) | Runnable infrastructure code |
| `nexus-ciso` | Deployment-risk review, signing | Pre-deploy attestation |
| `nexus-security` | Production hardening | Hardening checklist |

**Harness behaviour in P7**: destructive commands blocked.

### P8 — Maintenance

| Skill | When | Produces |
|---|---|---|
| `nexus-em` | Coordination, mentorship | Bug-triage discipline |
| `nexus-devops` | Patches, observability | Patch releases |
| `nexus-docs` | Changelogs, ops runbooks | Doc updates |
| `nexus-ds` | Production analytics | Incident retrospectives |

**Harness behaviour in P8**: destructive commands blocked (same as P7).

### P9 — Retirement

| Skill | When | Produces |
|---|---|---|
| `nexus-ciso` | Data-destruction policy, regulatory close-out | Purge attestation |
| `nexus-docs` | Decommission documentation | EOL announcement, migration guide |
| `nexus-em` | Hand-off coordination | Migration plan to successor system |

**Harness behaviour in P9**: blocks package managers (npm/pip/apt install) UNLESS the package name contains `security` or `patch`. Also blocks `/src/` and `/lib/` paths (no new development).

### Cross-phase

| Skill | When | Produces |
|---|---|---|
| `project-continuity` | Session boundary, every-5-calls ANTI-ROT nudge | `.claude/context/latest-handoff.md`, `.claude/context/project-state.md`, append to `.claude/context/history/` |
| `continuity-council` | Recurring quarterly audit (see [`AUDIT_CYCLE.md`](AUDIT_CYCLE.md)) | 5-expert audit report |
| `karpathy-skills` | Meta — skill evolution and composition | Versioned skill updates (NOT auto-promoted in the harness; v2.0 candidate per ADR-002) |
| `caveman` | Output compression when token budget is tight | Caveman-style ultra-compressed responses |

---

## How the harness suggests these skills

The harness does **NOT** auto-invoke skills. Instead:

1. **Phase-guard logs** the current phase on every gate decision. A user (or the dispatcher) can read the phase and consult this catalogue.
2. **ANTI-ROT nudge** (every 5 tool calls) emits a structured line: `ANTI-ROT:NUDGE skill=project-continuity reason=tool_call_count_multiple_of_5 tool_call_count=<N>`. The dispatcher may invoke `project-continuity` automatically; the harness does not.
3. **`adversarial-gate.sh --council`** (opt-in, requires `MULTIAGENT_BRIDGE_ENABLED=1`) emits `<MULTIAGENT_LAUNCH>` XML naming the 4 council reviewers (`nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead`). See [`ADR-003-multiagent-bridge.md`](ADR-003-multiagent-bridge.md).
4. **`state_engine.py self_audit`** (operator-invoked) generates a markdown report from the harness's own audit log; add `--council` to also emit the bridge envelope.

Skills are independent of the harness lifecycle. The harness does not vendor, version, or pin them.

---

## Skill composition notation (Karpathy principle 3)

Per the [Karpathy 5 principles](AUDIT_CYCLE.md#the-5-karpathy-principles), skills can compose via the `[[skill:name]]` syntax. The harness's docs use this notation to flag the canonical skill for each cross-cutting concern:

- Memory: `[[skill:project-continuity]]`
- Security review: `[[skill:nexus-ciso]]`
- Design discipline: `[[skill:iterative-code-design]]`
- Recurring audit: `[[skill:continuity-council]]`

These references are **documentation pointers**. The harness does not resolve them at runtime (it does not vendor `~/.claude/skills/`).

---

## What is deliberately NOT in this catalogue

- **claude-mem**, **understand-anything**, **zai-coding-plugins** — rejected in the integration audit (`.ai/docs/designs/2026-06-02-claude-code-integration-audit.md`) for Node.js / third-party-LLM / dual-source-of-truth reasons.
- **hyperagents auto-evolution loop** — deferred to v2.0 with explicit fitness contract.
- **Multi-model verification** — documented as opt-in only in [`AUDIT_CYCLE.md`](AUDIT_CYCLE.md); v1 ships single-model by design.

These are listed for transparency, not for use.
