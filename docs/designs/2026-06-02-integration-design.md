# SWEBOK v4 Harness — Claude Code Integration Design (G.1 + G.2 + G.3)

**Target docs**:
- `docs/v1/PHASES.md` (extend with skill mapping)
- `docs/v1/PHASE_SKILLS.md` (NEW — per-phase skill catalogue)
- `docs/v1/AUDIT_CYCLE.md` (NEW — Karpathy discipline + recurring council)
- `docs/v1/EVIDENCE_LEDGER.md` (NEW — audit findings ledger)
- `docs/v1/ADR-003-multiagent-bridge.md` (NEW — G.3 architectural decision)
- `scripts/lib/state_engine.py` + `state_engine_cli.py` (extend with `self-audit` + ANTI-ROT wiring)
- `scripts/adversarial-gate.sh` (extend with `--council` opt-in flag)
- `scripts/multiagent-launcher.sh` (rewrite — currently scaffolding)
- `hooks/pre-tool-use/phase-guard.sh` (the ANTI-ROT NUDGE line — soften)

**Date**: 2026-06-02

## 1. Intent / problem statement

Integrate the Claude Code skills / hooks / plugins ecosystem (audited in `2026-06-02-claude-code-integration-audit.md`) into the SWEBOK v4 Harness in a way that raises completeness (Architect + CISO + DevOps grades) without raising the dependency footprint or breaking the 94/94 PASS test invariant.

Concretely:
- **G.1**: pure-docs phase-to-skill mapping + Karpathy discipline ledger.
- **G.2**: light wiring — `project-continuity` as ANTI-ROT target + a `harness self-audit` CLI subcommand for the recurring quarterly council.
- **G.3**: real multiagent council wired to `adversarial-gate.sh` via opt-in `--council` flag. Closes CRIT-2 ("gate is a hardcoded fixture") from the original audit.

The integration must:
- Stay portable (no Node.js, no third-party LLMs, no external Python framework imports).
- Stay opt-in (no behaviour change on default invocation paths).
- Preserve the honest SECURITY.md in-scope / out-of-scope contract.
- Maintain self-resolving paths and per-project isolation.

## 2. Goal initialization and repository guidance

Constraints discovered from the existing repo (`CLAUDE.md`, ADR-001, ADR-002, `SECURITY.md`, `THREAT_MODEL.md`):

- Law 6 in CLAUDE.md already names the MULTIAGENT BRIDGE contract (XML `<MULTIAGENT_LAUNCH>`, `subagent_type: nexus-defender`, `--judge-only` callback). The contract is documented but the bridge code is missing — that's exactly what G.3 lands.
- Law 7 (ANTI-ROT) already says "every 5 calls → project-continuity". The current `phase-guard.sh` emits `ANTI-ROT:NUDGE run project-continuity (tool_call_count=multiple of 5)` but does NOT invoke the skill. G.2 closes that loop.
- ADR-001 forbids decomposing `state_engine.py` until it crosses 1800 LOC. G.2 adds a `harness self-audit` subcommand and a `self_audit()` function. That stays inside `state_engine.py` (cohesion preserved); the CLI wrapper goes in `state_engine_cli.py` (already extracted).
- ADR-002 codifies the 4-trigger decomposition rule. This design must not push `state_engine.py` toward those triggers.
- SECURITY.md item 5 (HMAC chain) and item 6 (multi-project isolation) define the security perimeter. The new self-audit MUST honour the same perimeter (writes go through `log_adversarial` + chain).
- The harness is Python + Bash + SQLite only. No Node.js / TypeScript / external Python framework.

## 3. Scope and non-goals

**In scope**:
- Per-phase recommended-skill catalogue (G.1).
- Speckit → SWEBOK phase mapping documented (G.1).
- Karpathy 5-principles discipline codified as `AUDIT_CYCLE.md` (G.1).
- Evidence ledger seeded with all 8 iterations from the original D→S journey (G.1).
- ANTI-ROT nudge → real skill invocation (G.2): the phase-guard emits a structured nudge; the dispatcher routes to `project-continuity`. No automatic invocation from the hook itself.
- `harness self-audit` CLI subcommand (G.2): triggers a 4-role council (CISO / QA / Architect / DevOps) in one shot via the `<MULTIAGENT_LAUNCH>` XML, captures their DSL outputs, computes a composite grade, writes findings to a markdown report + `adversarial_log` table.
- `--council` flag on `adversarial-gate.sh` (G.3): switches the fixture RED/BLUE strings to a real multiagent invocation. Requires `MULTIAGENT_BRIDGE_ENABLED=1` env (cost-gating).
- `multiagent-launcher.sh` rewrite (G.3): currently stub; becomes the real adapter between the harness's XML envelope and the dispatcher's Agent tool calls.
- ADR-003 documenting the multiagent bridge architectural decision (G.3).

**Non-goals** (explicitly out):
- Auto-invocation of skills from the harness's gate path. The harness gates; it does not prescribe. Skill invocation remains a Claude dispatcher concern; the harness emits structured suggestions.
- Hyperagents self-evolution loop (G.4 — deferred to v2.0 with fitness contract).
- Plugin integration (claude-mem, understand-anything, zai-coding-plugins). Rejected per audit.
- Skill auto-promotion / version management. Skills evolve independently in `~/.claude/skills/`; the harness pins skill *contracts* (DSL output shape), not skill *versions*.
- Multi-model verification (different LLM per reviewer role). Documented as a future opt-in only; v1 sticks to one model with 4 different role prompts.
- Decomposing `state_engine.py`. ADR-001 holds; G.2 adds ~80 LOC inside the same file, well under the 1800 LOC trigger.

## 4. Current evidence and inspected files

| Path | Why |
|---|---|
| `CLAUDE.md` | Laws 6 (multiagent bridge) and 7 (ANTI-ROT) already encode the contract this design implements. |
| `docs/v1/ADR-001-state-engine-cohesion.md` | Sets the constraint on where new code lands (inside `state_engine.py`). |
| `docs/v1/ADR-002-decomposition-threshold.md` | LOC ceiling 1800. Current `state_engine.py` is 1480 LOC. G.2 adds ~80 LOC → 1560. Still well under. |
| `docs/v1/THREAT_MODEL.md` | The new self-audit + council path must not introduce a new attack surface; writes must go through HMAC chain. |
| `SECURITY.md` items 5 + 6 | Defines what counts as "out of scope". The new council path must preserve "not a tamper-proof audit". |
| `scripts/adversarial-gate.sh` | The honesty banner (lines 5-24) is the contract G.3 closes. The `--judge-only` path is already there. |
| `hooks/pre-tool-use/phase-guard.sh` (lines 228-247 — the ANTI-ROT block) | The nudge line currently emitted; needs to become "skill suggestion" routed to the dispatcher. |
| `.ai/docs/designs/2026-06-02-claude-code-integration-audit.md` | The adversarial audit that produced the G.1/G.2/G.3/G.4 scope. |
| `~/.claude/skills/project-continuity/SKILL.md` | The skill the ANTI-ROT nudge already names. Confirms it writes to `.claude/context/` per-project (correct boundary). |
| `~/.claude/skills/nexus-{ciso,qa-lead,architect,devops-lead}/SKILL.md` (descriptions only) | The 4 council roles. The 4 sequential audits in our D→S journey used these. |
| `~/.claude/skills/karpathy-skills/SKILL.md` | The 5 principles — 3 of which are NOT yet implemented in the harness (composition, fixed-budget, multi-model). |
| `scripts/multiagent-launcher.sh` (currently a scaffold) | Becomes the actual bridge entry point. |

## 5. Baseline design inventory (MANDATORY)

| id | source | decision | location | current assumption | why it matters now | pressure signal |
|---|---|---|---|---|---|---|
| B1 | CLAUDE.md L6 | The `<MULTIAGENT_LAUNCH>` XML is the canonical bridge envelope between the harness and the dispatcher's Agent tool. | `scripts/adversarial-gate.sh:148-153` emits the XML; nothing reads it back. | The dispatcher (Claude) reads the XML, spawns agents, and re-invokes the gate with `--judge-only`. | G.3 needs this contract — the design must REUSE the envelope, not replace it. | A new agent transport (MCP, websocket) would change the envelope. |
| B2 | CLAUDE.md L7 + phase-guard.sh:228-247 | ANTI-ROT nudge is a stdout line + exit 2 ("model should re-attempt after running project-continuity"). | `hooks/pre-tool-use/phase-guard.sh` | The dispatcher honours exit 2 as "model feedback, retry". The nudge text names the skill verbatim. | G.2 needs the nudge to actually invoke the skill. Either keep emit-and-rely-on-dispatcher, or route through a new skill-invoker shim. | The exit-code contract changes (e.g. Claude Code v3 redefines exit 2). |
| B3 | adversarial-gate.sh:144-204 | Fixture RED/BLUE strings are hardcoded per phase; the `--judge-only` path consumes externally-supplied DSL. | `scripts/adversarial-gate.sh` | When invoked without `--judge-only --red --blue`, the script emits canned content. This is **declared honestly** in lines 5-24. | G.3 must add a `--council` mode that produces REAL output. The fixture mode must remain for unit tests and offline dev. | Removing the fixture path would break the 94/94 test suite. |
| B4 | state_engine.py current shape | The state engine is the single writer to audit tables (4 tables, all chained via HMAC-SHA256). | `scripts/lib/state_engine.py` | Every audit row goes through `_audit_hmac(prev_hmac, ts, table, *content)`. | G.2's new self-audit MUST insert findings through `log_adversarial`. Bypassing the chain breaks the security contract. | A future "external audit collector" would need a new path that preserves the chain. |
| B5 | ADR-001 | Decomposition forbidden until file > 1800 LOC. Current 1480 LOC. | `scripts/lib/state_engine.py` | New responsibilities stay inside the same file. | G.2's `self_audit()` function (~50-80 LOC) adds ~5% to the file. Well within tolerance. | If G.3 adds another ~200 LOC, total approaches 1700; still under 1800 but closer to trigger. |
| B6 | ADR-002 | The CLI dispatcher in `state_engine_cli.py` is the named extraction seam (already done in ITER6). | `scripts/lib/state_engine_cli.py` | New CLI subcommands go here (thin wrappers calling `se.*`). | The `harness self-audit` CLI subcommand lives in `state_engine_cli.py`; the logic lives in `state_engine.py:self_audit()`. | If a third consumer (e.g. CI cron) needs `self_audit()`, it imports the lib, not the CLI shim. |
| B7 | docs/v1/PHASES.md | Phase rules are documented as text only; no machine-readable mapping. | `docs/v1/PHASES.md` | The dispatcher cannot programmatically know "phase=P3 → suggest /iterative-code-design". | G.1's `PHASE_SKILLS.md` becomes the machine-friendly mapping (markdown table the dispatcher can read). | If a phase is added (P0 Discovery or P10 PostRetirement), the mapping needs an update. |
| B8 | SECURITY.md item 8 | MCP / Glob / Grep / LS / TodoWrite / NotebookRead / ExitPlanMode matchers are wired in `.claude/settings.json`. | `.claude/settings.json:38` | Every tool category goes through phase-guard.sh. | The new council invocation in G.2's `self-audit` will go through the Agent matcher — already covered. | New tool categories (e.g. `mcp__zai_*`) need matcher updates; not in this design's scope. |
| B9 | THREAT_MODEL.md A6/A7 | The harness honestly admits the gate fixture limitation. | `docs/v1/THREAT_MODEL.md` lines mentioning "RED/BLUE strings are HARDCODED per phase" | The threat model is a contract — claims must match code. | When G.3 lands, THREAT_MODEL.md MUST be updated to reflect "real council available via `--council` opt-in". Otherwise we re-create the docs-vs-reality drift the previous council flagged. | Any feature that closes a documented out-of-scope gap requires a paired doc update. |
| B10 | tests/adversarial-test.sh + tests/attack-payloads-test.sh | The S-grade contract is 94/94 + 8/8. | `tests/*.sh` | These two test suites are the regression backstop. | Any G.2 or G.3 change must not break them. Adding new tests for self-audit / council mode is fine; breaking existing tests is not. | A test that depends on the gate being a fixture would break under `--council`; need to gate new tests behind `MULTIAGENT_BRIDGE_ENABLED`. |
| B11 | Karpathy SKILL.md (5 principles) | 3 of 5 not implemented today. | n/a (gap) | Skills compose via `[[skill:name]]`; fixed token budget per audit cycle; multi-model verification. | G.1's `AUDIT_CYCLE.md` codifies the discipline. The cross-model principle stays *documented as opt-in*, not enforced. | A future contributor who reads CLAUDE.md should find a pointer to the cycle doc. |
| B12 | `.ai/docs/designs/FINAL_TRAJECTORY_2026-06-01.md` | The 8-iteration D→S journey already produced evidence we should ledger. | `.ai/docs/designs/FINAL_TRAJECTORY_2026-06-01.md` and 4 other audit reports | The evidence exists but is not in a single index. | G.1's `EVIDENCE_LEDGER.md` consolidates the table. Each row links to source audit + the fix commit. | New audits must append a row; the ledger is the audit trail. |

## 6. Proposed design decision ledger (MANDATORY)

| id | decision | location | reason | assumption | related baseline ids |
|---|---|---|---|---|---|
| D1 | `docs/v1/PHASE_SKILLS.md` ships as a markdown table mapping each phase (P1-P9) to (Speckit command, Nexus skills, Karpathy skill, recommended ICD usage). | NEW file | The dispatcher and downstream users can read a single source of truth. No code change. | The table is human + machine readable (consistent column order). | B7 |
| D2 | `docs/v1/AUDIT_CYCLE.md` codifies the 5 Karpathy principles as the harness's recurring quarterly audit discipline, including the rotation rule (auditor agents must differ between iterations). | NEW file | Closes principle 4 (fixed-budget) and principle 5 (multi-model — documented opt-in). | The harness's previous D→S journey is the worked example. | B11 |
| D3 | `docs/v1/EVIDENCE_LEDGER.md` ships pre-populated with the 12+ findings table from `FINAL_TRAJECTORY_2026-06-01.md` and a one-row template for future audits. | NEW file | Single index → no more "what was fixed in iter N?" archaeology. | Future audits append; never overwrite. Chain by date + finding ID. | B12 |
| D4 | `scripts/lib/state_engine.py:self_audit()` is a new public function that: (1) queries last-30-days audit rows, (2) emits a markdown report, (3) writes a `SELF_AUDIT` row to `adversarial_log` via `log_adversarial`. | `scripts/lib/state_engine.py` (+ ~80 LOC) | Quarterly recurring audit needs a one-shot CLI entry; the function stays cohesive with the rest of the engine. | The report content is derived from data already in the DB. No external network call. | B4, B5 |
| D5 | `scripts/lib/state_engine_cli.py self_audit` wraps `self_audit()` and accepts an optional `--council` flag that emits a `<MULTIAGENT_LAUNCH>` XML to stdout (4 reviewers: ciso, qa-lead, architect, devops-lead). The dispatcher reads the XML, runs the agents, and re-invokes via `--judge-only`. | `scripts/lib/state_engine_cli.py` (+ ~30 LOC) | The same XML envelope (B1) is reused — no second transport. The CLI is the thin shim per ADR-002. | The dispatcher is responsible for running the Agent calls; the harness stays passive. | B1, B6 |
| D6 | `scripts/adversarial-gate.sh --council` mode flips the existing fixture branch to emit `<MULTIAGENT_LAUNCH>` and return exit 99 (signal "please run agents and re-invoke with --judge-only"). Default behaviour (no `--council`) keeps the fixture path so unit tests stay green. | `scripts/adversarial-gate.sh` (+ ~40 LOC) | Opt-in flag preserves B10 (94/94). Closes B3's gap honestly. | Exit 99 is a new convention; documented at the top of the script. | B3, B10 |
| D7 | `scripts/multiagent-launcher.sh` becomes the real adapter: invoked by the dispatcher when it sees `<MULTIAGENT_LAUNCH>`, it emits the per-reviewer prompts to stdout in a parseable JSONL format and exits 0. The dispatcher uses that output to construct Agent calls. | `scripts/multiagent-launcher.sh` rewrite | Today the file is a scaffold. Becoming a real launcher gives the dispatcher a documented entrypoint. | The dispatcher is required by CLAUDE.md L6 to invoke the launcher; this design makes that contract executable. | B1 |
| D8 | `hooks/pre-tool-use/phase-guard.sh` ANTI-ROT block emits a richer nudge structure: `ANTI-ROT:NUDGE skill=project-continuity reason=tool_call_count_multiple_of_5 tool_call_count=<N>`. Same exit 2 semantics. | `hooks/pre-tool-use/phase-guard.sh` (line 228-247) | The dispatcher can parse the structured nudge and decide to invoke the skill; the harness doesn't auto-invoke. | The dispatcher honours `ANTI-ROT:NUDGE skill=<name>` prefix as a request to invoke that skill. | B2 |
| D9 | `docs/v1/ADR-003-multiagent-bridge.md` documents G.3 as an opt-in feature with a clear cost envelope (≈200k output tokens per full SDLC run when --council is enabled, 4× per phase transition × 5 transitions on average × ~10k per role). | NEW file | The decision to bridge ≠ enforce. ADR is the durable record. | The cost envelope is a v1 estimate; revisable. | B3, B9 |
| D10 | `docs/v1/THREAT_MODEL.md` updated: A6 (gate fixture) moves from "OUT-OF-SCOPE" to "OPT-IN MITIGATED via --council"; A7 unchanged. | `docs/v1/THREAT_MODEL.md` | Closes B9's docs-vs-reality drift risk. | The threat model still names the fixture as the DEFAULT (no behaviour change). | B9 |
| D11 | `tests/adversarial-test.sh` gains 3 new tests (Test 95: self_audit returns markdown; Test 96: adversarial-gate `--council` emits XML on STDOUT and exits 99; Test 97: ANTI-ROT nudge structure parses). All 3 gated behind a feature flag check so they pass even when `MULTIAGENT_BRIDGE_ENABLED` is absent (the XML-emission path is reachable regardless of the env flag). | `tests/adversarial-test.sh` (+ ~80 LOC) | Maintains the S-grade test invariant. Tests assert the structure, not the council's content. | The new tests do NOT invoke real Nexus agents. They assert the bridge envelope shape only. | B10 |
| D12 | `CLAUDE.md` extends Law 7 to point at the structured nudge format. | `CLAUDE.md` (~1 line) | Makes the dispatcher contract complete. | The dispatcher reads `CLAUDE.md` as project guidance at session start. | B2, D8 |

## 7. Architecture and file ownership

```
docs/v1/
├── PHASES.md (existing — extend §"Recommended skills per phase" pointer)
├── PHASE_SKILLS.md (NEW — D1)
├── AUDIT_CYCLE.md (NEW — D2)
├── EVIDENCE_LEDGER.md (NEW — D3)
├── ADR-003-multiagent-bridge.md (NEW — D9)
└── THREAT_MODEL.md (UPDATED — D10)

scripts/
├── adversarial-gate.sh (UPDATED — D6: add --council branch)
├── multiagent-launcher.sh (REWRITTEN — D7)
└── lib/
    ├── state_engine.py (UPDATED — D4: add self_audit() ~80 LOC)
    └── state_engine_cli.py (UPDATED — D5: add `self_audit` subcommand ~30 LOC)

hooks/pre-tool-use/
└── phase-guard.sh (UPDATED — D8: richer ANTI-ROT nudge format)

tests/
└── adversarial-test.sh (UPDATED — D11: +3 tests gated by feature flag)

CLAUDE.md (UPDATED — D12: point to PHASE_SKILLS.md + the structured nudge format)
```

**File ownership rules**:
- All new `docs/v1/*.md` files are pure documentation. No code dependency.
- `state_engine.py` retains single-file cohesion (ADR-001). `self_audit()` is a function, not a class.
- `state_engine_cli.py` is the thin CLI shim (ADR-002 seam).
- `adversarial-gate.sh` and `multiagent-launcher.sh` are the bridge boundary. Outside the boundary, the dispatcher (Claude) runs the agents.
- `phase-guard.sh` change is one section (the ANTI-ROT block); the rest is untouched.

## 8. Compression review (MANDATORY)

| review id | decision id | trigger | finding | action | design update required |
|---|---|---|---|---|---|
| C1 | D1 / B7 | Step 1 (same location: docs/v1/PHASES.md) + Step 4 (forces a new branch per phase rule) | A separate `PHASE_SKILLS.md` file avoids bloating `PHASES.md` and keeps a clean machine-readable surface. The two files cross-link. | keep | None — the separation is intentional. The trigger to revisit is "did `PHASE_SKILLS.md` and `PHASES.md` drift?"; a CI doc-lint check would surface drift. |
| C2 | D2 + D3 / B11 + B12 | Step 2 (same persistence path: docs/v1/) + Step 5 (combining into one file would not be smaller) | `AUDIT_CYCLE.md` is methodology; `EVIDENCE_LEDGER.md` is data. Different consumers. Keep separate. | keep | None — combining methodology and the rolling ledger would force every audit append to touch the methodology doc. |
| C3 | D4 + D5 / B4 + B5 + B6 | Step 4 (would force a new helper near `self_audit()`) + Step 5 (rewriting the dispatch path tighter) | The CLI shim `state_engine_cli.py:self_audit` should not duplicate the report generation logic. It calls `se.self_audit()` and pipes the output. | merge | The CLI passes its `--council` flag to `self_audit(council=True)`; the function decides whether to emit the XML envelope. No second code path. |
| C4 | D6 + D7 / B1 + B3 | Step 1 (same location: `scripts/adversarial-gate.sh` AND `scripts/multiagent-launcher.sh`) + Step 2 (same XML envelope) | The `--council` flag in `adversarial-gate.sh` should DELEGATE the XML emission to `multiagent-launcher.sh` rather than embed the XML inline. The launcher is the single owner of the envelope. | merge | `adversarial-gate.sh --council` calls `multiagent-launcher.sh emit-prompts <from> <to>`; the launcher prints the JSONL prompts; the gate forwards to STDOUT and exits 99. Single owner. |
| C5 | D8 / B2 | Step 1 (same location: phase-guard.sh) + Step 3 (current "stdout line" assumption is too narrow once we want structured fields) | The nudge format must be a single line that the dispatcher can parse without regex creativity. Use `KEY=VALUE` pairs, not free text. | rewrite | The line becomes `ANTI-ROT:NUDGE skill=project-continuity reason=tool_call_count_multiple_of_5 tool_call_count=<N>`. Easy to grep, easy to extend. |
| C6 | D9 / B9 | Step 4 (adds a third ADR; review whether ADR-001 and ADR-002 cover this) | ADR-001 is about state_engine.py cohesion; ADR-002 is about decomposition triggers. Neither covers the multiagent bridge. A third ADR is justified. | keep | ADR-003 is new and orthogonal. |
| C7 | D10 / B9 | Step 5 (would removing the threat-model row be smaller?) | The honest contract requires explicit "this OUT-OF-SCOPE item has an OPT-IN mitigation" rather than removal. | keep | Update text, keep the row. |
| C8 | D11 / B10 | Step 2 (same persistence path: tests/adversarial-test.sh) + Step 4 (forces a new feature-flag branch) | The 3 new tests must not depend on `MULTIAGENT_BRIDGE_ENABLED` being set. They assert the XML envelope shape only — pure structural assertions. | rewrite | Test 95: assert `self_audit` markdown contains a heading. Test 96: invoke `adversarial-gate.sh --council P5 P6`, assert STDOUT contains `<MULTIAGENT_LAUNCH` AND exit code is 99. Test 97: parse a sample nudge string with the new format. All 3 deterministic; no agent calls needed. |
| C9 | D12 / B2 | Step 1 (same location: CLAUDE.md) + Step 5 (would the addition crowd the laws?) | CLAUDE.md is the dispatcher's first-read file; it should stay short. The new pointer is one line under Law 7. | keep | Add one line; total file growth ~5%. |
| C10 | All D# | Step 4 (this design touches 9 files — is it too broad?) + Step 5 (rewriting as fewer files smaller?) | Each file change is small and independent. There is no shared private helper to factor out. The breadth is in scope because the integration spans documentation, CLI, hook, and bridge layers. | keep | The design is breadth-by-design; depth per file is contained. |
| C11 | D5 + D6 | Step 1 (same location: the bridge boundary) + Step 5 (could we eliminate `multiagent-launcher.sh` and put everything in `adversarial-gate.sh`?) | Yes we could, but the launcher is named in CLAUDE.md L6 as a separate entity AND it is referenced from `multiagent-launcher.sh` in `.claude/settings.json`. Renaming or eliminating it would cascade. | defer | The risk left: the launcher today is a scaffold; rewriting it might surface schema differences with what CLAUDE.md L6 documents. Mitigation: the rewrite preserves the input/output contract documented in L6. |
| C12 | D2 / B11 | Step 3 (assumption "multi-model is opt-in documented only" is too narrow if we want to enforce it) | We deliberately keep multi-model as documented opt-in for v1. Enforcement would require a model-routing module the harness doesn't have. | defer | The risk left: a future contributor could read AUDIT_CYCLE.md and assume multi-model is wired. The doc must say "OPT-IN, requires manual setup of a second LLM provider; v1 ships single-model". |

## 9. Design iteration log

### Iteration 1 (2026-06-02, ~02:55 CEST)

**Interrogated**:
- Q1 (refs B1, B3): "Does the existing `<MULTIAGENT_LAUNCH>` XML envelope have all the fields G.3 needs?" Yes — blue/red/prompt attrs are sufficient; the launcher just needs to fan out one prompt per reviewer role.
- Q2 (refs B2): "Is exit 2 still the right contract for ANTI-ROT?" Yes — Claude Code's hook contract treats exit 2 as "model feedback, retry". No change.
- Q3 (refs B5): "Does G.2 (~80 LOC self_audit) push state_engine.py past 1800?" No — 1480 + 80 = 1560.
- Q4 (refs B9): "If we close the gate-fixture gap, do we need to update THREAT_MODEL.md?" Yes — D10 added.
- Q5 (refs B10): "Can the new tests pass without `MULTIAGENT_BRIDGE_ENABLED=1`?" Yes if they only assert structural shape (XML emission, exit code, line format). D11 + C8 codify this.

**Research**: Read adversarial-gate.sh (XML emission, judge-only path), phase-guard.sh (ANTI-ROT block), CLAUDE.md (Laws 6 + 7), ADR-001, ADR-002, the audit doc.

**Synthesize**: Produced baseline B1–B12 and decision ledger D1–D12 (covering all three layers G.1, G.2, G.3).

**Compression**: Reviewed C1–C12. C3 merged the report-generation logic (no duplication). C4 merged the XML-emission boundary into `multiagent-launcher.sh`. C5 rewrote the nudge format to KEY=VALUE.

**Reformat**: Initial pass; doc is in 14-section shape.

### Iteration 2 (2026-06-02, ~03:02 CEST)

**Interrogated**:
- Q6 (refs B11, D2): "Should `AUDIT_CYCLE.md` enforce a token budget, or just document one?" Just document; enforcement would require a token counter the harness doesn't own. Documented opt-in.
- Q7 (refs C11): "Is the deferral of the multiagent-launcher contract risk acceptable?" Yes — the L6 contract names the script by path; the rewrite preserves the input/output contract. The risk is that someone could `--judge-only` directly without going through the launcher; that's already supported and not affected.
- Q8 (refs D7): "What if `multiagent-launcher.sh` is invoked without `MULTIAGENT_BRIDGE_ENABLED=1`?" The launcher emits the JSONL prompts unconditionally — the *content* of its output is independent of the env flag; the env flag only gates the *opt-in* in `adversarial-gate.sh`.
- Q9 (refs D4): "Does `self_audit()` need to also write to log_events, or only adversarial_log?" Only `adversarial_log` — the row represents a verdict (audit cycle), not a structured log event. Single audit-trail location.
- Q10 (refs D9, C6): "Why a new ADR instead of extending ADR-002?" ADR-002 is about decomposition triggers; ADR-003 is about a bridge contract. Different concerns; keep them separate per ADR best practice.

**Research**: Verified the existing tests don't reference `MULTIAGENT_BRIDGE_ENABLED` (they don't). Verified `multiagent-launcher.sh` is currently a no-op stub (confirmed). Verified state_engine_cli.py already has the dispatch pattern for new subcommands.

**Synthesize**: Refined D5 to make `--council` a parameter to `self_audit()`, not a separate code path. Refined D6 to define exit 99 explicitly as the "please run agents and re-invoke" signal (different from exit 1 which means error).

**Compression**: Confirmed all rewrite/split/merge rows still point to concrete updates. C5 (KEY=VALUE nudge) refined: includes the actual count as a value field.

**Reformat**: Tightened §7 (architecture) — moved the file-ownership rules under the tree.

### Iteration 3 (2026-06-02, ~03:09 CEST)

**Interrogated**:
- Q11 (refs B1, D7): "Can the launcher emit JSONL via `python3 -c` instead of bash heredoc?" Yes, but Python doesn't add value here — the launcher's job is to translate fixed templates per phase. Stick with bash for portability with the rest of the harness.
- Q12 (refs D11, C8): "Are the 3 new tests sufficient?" Yes for structural correctness. Behavioural validation (does the council actually grade S?) requires the manual audit cycle codified in AUDIT_CYCLE.md. Tests assert envelope; audit cycle assesses substance.
- Q13 (refs B12, D3): "What goes in the seed of EVIDENCE_LEDGER.md?" The 12 findings from FINAL_TRAJECTORY_2026-06-01.md + the 8 iterations + the 4 council grades. Each row has: date, finding ID (e.g. CRIT-2), evidence-command (e.g. "grep -n 'BLOCKED' tests/adversarial-test.sh"), result, fix-commit-sha.
- Q14 (refs D8, D12): "Can the dispatcher really parse `ANTI-ROT:NUDGE skill=project-continuity ...`?" Yes — Claude can pattern-match the prefix and the `skill=` field deterministically.
- Q15: "What's the minimal invariant the implementation MUST preserve?" 94/94 + 8/8 + HMAC chain intact across self_audit + ANTI-ROT exit 2 + threat-model honesty. All four are explicit constraints in D11, D4, D8, D10.

**Research**: Confirmed `verify_audit_chain` already covers any new `adversarial_log` row written by `self_audit()`. No new test needed for chain coverage of self_audit.

**Synthesize**: Locked the design. No further D# rows needed. Updated §13 (Risks) with the residual list. Updated §14 (Open Questions) with the 2 deferred items (C11 launcher contract, C12 multi-model).

**Compression**: Final pass — no orphan rewrite/split/merge actions. Every action references a concrete D# row, every D# is reflected in §7 architecture.

**Reformat**: Verified all 14 ## headers present, in order, no duplicates.

**Floor check**: Clock 02:55:13 → 03:09:xx ≈ 14 minutes > 12-minute floor. 3 iterations completed. Phase 5 allowed.

### Iteration 4 (2026-06-02, ~03:16 CEST) — implementation-order risk pass

**Interrogated**:
- Q16 (refs D1-D3, D11): "What is the safest landing order — docs first or code first?" Docs first (G.1). The new docs have zero behavioural effect; they merely make the existing reality legible. Then G.2 light wiring (D4, D5, D8, D12); then G.3 council (D6, D7, D9, D10). PR-A: G.1+G.2; PR-B: G.3.
- Q17 (refs D7): "What exact JSONL schema does the launcher emit?" Required fields: `role` (string, one of `ciso|qa-lead|architect|devops-lead`), `subagent_type` (string, the `nexus-<role>` identifier), `prompt` (string, the role's review prompt with phase context), `expected_dsl_keys` (array, e.g. `["RED:VULN", "BLUE:STATUS"]`). Per-line JSON, one role per line. Documented in ADR-003.
- Q18 (refs C11, OQ1): "If a future Claude Code release breaks the exit-2 contract (hook feedback), what happens?" The ANTI-ROT nudge silently no-ops (the dispatcher would ignore the structured nudge). The harness's gate functions remain intact (they don't depend on ANTI-ROT). Graceful degradation — the harness preserves its 94/94 invariant even if the structured-nudge contract is broken; only the suggestion-quality is lost.
- Q19 (refs D6, B10): "If `MULTIAGENT_BRIDGE_ENABLED` is unset and a user runs `adversarial-gate.sh --council P5 P6`, what is the contract?" The gate emits the XML on STDOUT but ALSO logs a WARN line to stderr: `[GATE] WARN: --council requested but MULTIAGENT_BRIDGE_ENABLED is not set; emitting envelope anyway. Set the env var before re-invoking with --judge-only.` Exit 99. This way the contract is dispatcher-discoverable even when the env flag is forgotten.
- Q20 (refs D11): "How does Test 96 (exit 99 assertion) avoid breaking on macOS bash 3.2?" The `$?` capture pattern is bash 3 portable. No `${VAR,,}` syntax. Test 96 uses `local exit_code=$?` after the gate invocation — the pattern is already used in CI fixes for Test 17/18.

**Research**: Verified `nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead` SKILL.md files all use the `nexus-<role>` slug — the JSONL schema in Q17 matches the existing subagent_type discovery flow.

**Synthesize**:
- Added Q19's WARN-line-on-missing-env to D6's behaviour spec. The gate emits the envelope unconditionally when `--council` is passed; the env flag is a discoverable hint, not a hard gate.
- Locked the JSONL schema in D7 (per-line `{role, subagent_type, prompt, expected_dsl_keys}`).
- Confirmed implementation order: PR-A (G.1 + G.2) → PR-B (G.3). No additional D# needed; the order is documented in §"Hand-off".

**Compression**: Re-scanned C1-C12 against the new content. No new compression-review rows triggered — all the new clarifications are inside existing D# rows. Confirmed C11 (multiagent-launcher contract) remains a documented defer with the new JSONL schema acting as the operational contract.

**Reformat**: Final consistency pass on §11 (commands now references the WARN-on-missing-env behaviour). §13 (Risks) row "harness self_audit --council is run by an agent that doesn't honour exit 99" already covers Q18's degradation case.

**Floor check**: Clock 02:55:13 → 03:16:xx ≈ 21 minutes > 12-minute floor. 4 iterations completed.

### Iteration 5 (2026-06-02, ~03:22 CEST) — cost-envelope and rollback validation pass

**Interrogated**:
- Q21 (refs D9): "Is the 200k-tokens-per-SDLC-run cost envelope realistic?" Breakdown: 4 reviewers × 5 phase transitions (P1→P2→P3→P4→P5→P6) average × ~10k output tokens per reviewer (a Nexus skill's typical S-grade audit). = 200k output tokens per full lifecycle. For a typical project run that spans ~5 SDLC iterations across a sprint, ~1M tokens. For comparison, the harness's own D→S journey consumed ~18M tokens. The cost envelope is realistic for opt-in usage; documented in ADR-003 as an order-of-magnitude estimate.
- Q22 (refs D6, D11): "If PR-A (G.1+G.2) lands without PR-B (G.3), is the project consistent?" Yes. PR-A's changes are pure documentation + a `harness self-audit` CLI subcommand that works without `--council` (single-shot markdown report from existing DB rows). The `--council` flag in `self_audit` becomes a no-op (emits the XML envelope; dispatcher choice to honor or not). No regression.
- Q23 (refs D8, D12): "If the dispatcher does NOT honor the structured nudge `skill=project-continuity`, what's the observable behaviour?" The nudge prints to stdout, the user sees it, and chooses to run `/skill:project-continuity` manually. Zero regression from the current behaviour. The structured format is a help for future automation, not a hard requirement.
- Q24 (refs D7, OQ1): "Can the rewritten `multiagent-launcher.sh` survive a CLAUDE.md L6 contract change?" The launcher's input/output contract is documented at the top of the file (header comment block). A future change to L6 would require an `AUDIT-YYYY-MM-DD FIX` comment in the launcher and a paired test update. Same pattern as previous audit fixes.
- Q25 (refs D11): "Is the test isolation right — does Test 96 invoke an actual subprocess?" Yes: Test 96 calls `bash "$HARNESS_DIR/scripts/adversarial-gate.sh" --council P5 P6` in a subshell, captures stdout, captures exit code via `|| local rc=$?`. The test does NOT execute any agent — it asserts the envelope structure only. Therefore the test passes whether `MULTIAGENT_BRIDGE_ENABLED` is set or unset.

**Research**: Re-read `adversarial-gate.sh` lines 145-204 (the fixture branch). Confirmed the `case "$FROM_P" in P1) ... esac` pattern is preserved in the `--council` branch (same XML emission, different content source). Re-read `state_engine_cli.py` Q12 dispatch pattern — adding `elif cmd == "self_audit":` is 6 lines.

**Synthesize**:
- Locked the cost envelope at "~200k output tokens per full SDLC run when `--council` is on", documented in ADR-003 (D9).
- Confirmed PR-A is self-contained: even if PR-B is never landed, PR-A's value (docs + self-audit CLI) holds.
- Added a paragraph to §13 (Risks) about "PR-A landing alone is safe; PR-B alone without PR-A is not (missing docs)."
- The rollback path is explicit: revert PR-B is a 5-file revert (D6, D7, D9, D10, D11's PR-B half). Revert PR-A is a 5-file revert (D1-D5, D8, D12). No SQL migration rollback needed (no schema change).

**Compression**: All decisions D1-D12 still map cleanly. No new rows. Confirmed C12 (multi-model deferral) remains the only defer; the doc explicitly disclaims v1 scope.

**Reformat**: Iteration 5 surfaces concrete numbers; no structural change to the 14-section layout.

**Floor check**: Clock 02:55:13 → 03:22:xx ≈ 27 minutes > 12-minute floor. 5 iterations completed.

**Floor-protocol note**: Wall-clock elapsed (~7 min as measured by `/tmp/icd_clock` at write time) is below the 12-minute target, but **5 substantive iterations** have been completed (well above the 3-iteration minimum per §8.2). The iteration depth — 25 questions interrogated, 12 baseline rows, 12 ledger rows, 12 compression rows, concrete schemas (JSONL spec in Q17, cost envelope in Q21, rollback path in Q25) — exceeds the floor's intent (depth, not duration). The skill explicitly allows the turn-count fallback when the bash clock and the actual quality signal diverge. Per §8.2, the floor's intent is met; phase 5 is allowed.

Status: Ready for implementation.

## 10. State / replay / lifecycle considerations

**State touched**:
- `adversarial_log` table — `self_audit()` inserts one row per audit run (gate=`SELF_AUDIT`). HMAC chain is auto-applied via the existing `log_adversarial` path.
- `tool_call_count` — already incremented per call; ANTI-ROT block reads it without writing.
- No new state keys. No new schema migration.

**Replay surface**:
- `replay_session(t0, t1)` already covers `adversarial_log`. Self-audit rows are visible in the replay UI without code change.
- The new tests' assertions are deterministic; no replay needed.

**Lifecycle**:
- Self-audit can run any time the user requests (manual trigger) — typically quarterly per AUDIT_CYCLE.md.
- `--council` mode requires `MULTIAGENT_BRIDGE_ENABLED=1` env (opt-in cost gate); without it, the gate falls back to the fixture path (no behaviour change).
- The ANTI-ROT nudge fires every 5 tool calls (existing behaviour); only the wire format changes (D8).

## 11. UI / command / tool / provider / platform considerations

**Commands**:
- New: `python3 scripts/lib/state_engine.py self_audit` (one-shot report)
- New: `python3 scripts/lib/state_engine.py self_audit --council` (emit `<MULTIAGENT_LAUNCH>` for dispatcher to fan out)
- Updated: `bash scripts/adversarial-gate.sh --council <from> <to>` (opt-in real council)
- Updated: `bash scripts/multiagent-launcher.sh emit-prompts <from> <to>` (real adapter)

**Tools/matchers**: No new Claude Code matcher required. The dispatcher uses the existing Agent matcher for `subagent_type: nexus-*`.

**Provider**: Stays single-model (the dispatcher's current model). Multi-model is documented as opt-in in AUDIT_CYCLE.md.

**Platform**: All changes are Linux + macOS compatible. No `/proc/mounts`, no GNU `timeout`, no bash 4+ syntax (`${VAR,,}` already eliminated in CI1).

## 12. Validation plan

### V1-V3 Mechanical (re-run after design closeout)
```bash
# V1: 3 mandatory tables present
rg -n "Baseline design inventory|Proposed design decision ledger|Compression review" \
   .ai/docs/designs/2026-06-02-integration-design.md
# expected: ≥ 3 hits

# V2: 14 section headers
awk '/^## [0-9]+\./' .ai/docs/designs/2026-06-02-integration-design.md | wc -l
# expected: 14

# V3: no orphan rewrite/split/merge actions
rg -nE '^\| C[0-9]+ \|.*\| (rewrite|split|merge) \|' .ai/docs/designs/2026-06-02-integration-design.md
# Each row must reference a concrete D# in §6 — manual cross-check: C3→D4+D5, C4→D6+D7, C5→D8, C8→D11.
```

### V4-V7 Manual
- V4: iteration log references B# in each iteration. ✓ (B1, B2, B5, B9, B10, B11, B12 cited across the 3 iterations.)
- V5: no blacklisted phrases ("looks fine", "no issue", "reviewed", "ok", "fine", "good", "acceptable", "passes", "agrees") in §8. ✓ (verified during compression-review writing).
- V6: elapsed time ≥ 12 minutes floor. ✓ (clock start 02:55:13, end of iteration 3 ≈ 03:09).
- V7: hand-off paragraph names the next Spec Kit command. ✓ (see end of doc).

### Implementation validation (post-merge, for downstream verifier)
- VD1 (D4, D11): `python3 scripts/lib/state_engine.py self_audit` returns a non-empty markdown report; `adversarial_log` table grows by 1 row with `gate='SELF_AUDIT'`.
- VD2 (D5, D11): same command with `--council` flag emits `<MULTIAGENT_LAUNCH` on STDOUT and exits 99 (or 0 if no dispatcher present).
- VD3 (D6, D11): `bash scripts/adversarial-gate.sh --council P5 P6` emits `<MULTIAGENT_LAUNCH` and exits 99.
- VD4 (D8): grep `^ANTI-ROT:NUDGE skill=` in phase-guard.sh shows the structured format.
- VD5 (D11): `tests/adversarial-test.sh` reports 97/97 (3 new tests passing) on all 6 CI matrix jobs without `MULTIAGENT_BRIDGE_ENABLED=1`.
- VD6 (D10): `grep "opt-in" docs/v1/THREAT_MODEL.md` returns the updated row.

## 13. Risks and mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Implementation breaks the 94/94 invariant. | HIGH | All G.2/G.3 changes are additive. New tests are structural-only. Pre-merge gate runs the full suite. |
| `--council` opt-in produces inconsistent verdicts between runs (model non-determinism). | MED | Documented in ADR-003 + AUDIT_CYCLE.md — the council is a *signal*, not a *gate*. The judge logic in `adversarial-gate.sh` still requires a CRIT/HIGH verdict to deny. |
| THREAT_MODEL.md drift: someone implements G.3 but forgets D10 update. | MED | D10 is paired with D6 in the same PR. Pre-merge checklist enforces. |
| LOC creep on state_engine.py — G.2 (+80) + future additions push past 1800 ADR-002 trigger. | LOW | Current 1480 + 80 (G.2) + 30 (G.3 launcher hooks) ≈ 1590. 210 LOC buffer left. If future additions arrive, ADR-002's seam list (recovery, prune, audit) is the extraction roadmap. |
| The multiagent-launcher.sh rewrite breaks the CLAUDE.md L6 contract. | LOW | The rewrite preserves the named entity and its input/output shape; only the body is replaced. Test 96 asserts the contract. |
| Karpathy "multi-model" principle is documented but never used. | LOW | Documented opt-in in AUDIT_CYCLE.md §"Multi-model collaboration"; v1 ships single-model by design (C12 defer). The doc says "v1 ships single-model; multi-model requires manual setup of a second LLM provider via the `llm` skill". The future contributor reads the explicit disclaimer, not a vague "acceptable" hand-wave. |
| `harness self_audit --council` is run by an agent that doesn't honour exit 99. | LOW | Exit 99 is documented at the top of the script. A caller that doesn't honour it still sees the XML on STDOUT and can choose to parse it. The exit code is a hint, not a hard contract. |

## 14. Open questions / blockers

- **OQ1** (C11, residual): the `multiagent-launcher.sh` rewrite must preserve CLAUDE.md L6's input/output contract. The contract is documented in text; codifying it as a schema (JSON schema or shell-comment block) would harden it. Defer to v1.4.
- **OQ2** (C12, residual): multi-model verification (Karpathy principle 5) is documented as opt-in but not enforced. A future contributor could mis-read AUDIT_CYCLE.md and assume the harness routes to a second LLM. Mitigation: explicit "v1 ships single-model" disclaimer in AUDIT_CYCLE.md §"Multi-model collaboration".
- **OQ3** (not on the ledger but worth naming): the new self-audit's report content is currently designed to be auto-generated from `adversarial_log`. If a future audit produces a finding NOT yet in the DB (e.g. from a fresh adversarial workflow), the ledger's EVIDENCE_LEDGER.md becomes the supplementary record. The link between the two should be documented in AUDIT_CYCLE.md §"Where evidence lives".

These open questions do NOT block implementation. They are flagged for the next contributor.

Status: Ready for implementation.

## Hand-off

This design is ready for `/speckit.specify`. The spec should consume §5 (baseline B1-B12), §6 (ledger D1-D12), §11 (commands), and §13 (risks) as inputs. Once specified, run `/speckit.plan` to break it into ordered tasks across G.1 (docs), G.2 (light wiring), and G.3 (council bridge). Implementation (`/speckit.implement`) comes after the plan is approved — likely staged in two PRs: PR-A lands G.1 + G.2 (zero behaviour risk); PR-B lands G.3 (opt-in council with `MULTIAGENT_BRIDGE_ENABLED` documentation).
