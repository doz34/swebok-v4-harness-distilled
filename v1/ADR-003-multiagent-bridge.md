# ADR-003 — Multiagent council bridge

**Status**: Accepted (design); IMPLEMENTATION in two PRs (PR-A: docs + light wiring; PR-B: real council bridge).
**Date**: 2026-06-02
**Context**: The original 2026-06-01 audit's CRIT-2 finding flagged `scripts/adversarial-gate.sh` as "a hardcoded RED/BLUE fixture per phase, not a real adversarial gate". The harness shipped with an honesty banner declaring the fixture status, but the gap remained an open OUT-OF-SCOPE row in `THREAT_MODEL.md`. This ADR documents the decision to close that gap via an **opt-in multiagent council bridge**.

## Decision

Add a `--council` flag to `scripts/adversarial-gate.sh` that, when invoked together with `MULTIAGENT_BRIDGE_ENABLED=1`:

1. Emits `<MULTIAGENT_LAUNCH>` XML on STDOUT naming 4 reviewer roles (`nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead`).
2. Exits with code 99 (a new convention: "please spawn the named agents and re-invoke me with `--judge-only --red <RED_DSL> --blue <BLUE_DSL>`").
3. Delegates the XML emission to `scripts/multiagent-launcher.sh` (the single owner of the bridge envelope per CLAUDE.md Law 6).

The dispatcher (Claude Code) handles the agent invocation. The harness stays **passive**: it never runs an Agent tool call itself.

## Rationale

### Why opt-in (not default)

1. **Cost**: ~200k output tokens per full SDLC run (4 reviewers × 5 transitions × ~10k tokens). Downstream users opt in only when the audit cost is justified.
2. **Determinism**: the existing fixture path is fully deterministic (canned strings per phase). Unit tests, CI, and local development paths stay green without the council. Opt-in preserves the 92/92 + 8/8 invariant.
3. **Provider neutrality**: the council uses Nexus skills which are independent of the harness. A downstream user without those skills falls back to the fixture path with no error.

### Why a separate launcher script

`scripts/multiagent-launcher.sh` is named in CLAUDE.md Law 6 as the bridge entry point. Today the file is a scaffold. Rewriting it as the real adapter:
1. Preserves the CLAUDE.md L6 contract (the dispatcher's named entrypoint stays the same).
2. Keeps the XML envelope owned by exactly one file (avoids duplication between the gate and an inline emitter).
3. Lets the gate stay a thin orchestrator (validate → delegate emission → exit 99).

### Why exit code 99

The harness's existing exit code conventions:
- `0` = pass / continue
- `1` = error / generic failure
- `2` = soft-block with model feedback (per Claude Code hook contract)
- `3` = STATE_ENGINE_READONLY_FS
- `4` = STATE_ENGINE_DISK_FULL
- `5` = STATE_ENGINE_INTEGRITY_FAIL
- `6` = STATE_ENGINE_SCHEMA_DOWNGRADE

`99` is unused and conventionally signals "the script's work isn't finished — please continue via another invocation". It's a hint, not a hard contract: a caller that doesn't honor it still sees the XML envelope on STDOUT and can choose to parse it.

### Why `MULTIAGENT_BRIDGE_ENABLED` env var

Two reasons:
1. **Cost gating**: a user who runs `--council` without setting the env gets a clear WARN on stderr and an envelope on stdout; the dispatcher chooses whether to actually spawn agents. No accidental 200k-token burns.
2. **CI safety**: GitHub Actions runs the test suite. The `MULTIAGENT_BRIDGE_ENABLED` env is unset in CI; the council tests (Test 97, Test 98, Test 99, Test 100) assert envelope structure, env-var WARN, input validation, and P10+ phase_num preservation only — not agent behaviour. CI stays under 3 minutes per matrix job.

## JSONL contract — what `multiagent-launcher.sh emit-prompts` produces

Per-reviewer-per-line JSON on STDOUT. Schema:

```json
{
  "role": "ciso|qa-lead|architect|devops-lead",
  "subagent_type": "nexus-ciso|nexus-qa-lead|nexus-architect|nexus-devops-lead",
  "prompt": "<full-text prompt with phase context>",
  "expected_dsl_keys": ["RED:VULN", "BLUE:STATUS"]
}
```

Example output for `multiagent-launcher.sh emit-prompts P5 P6`:

```
{"role":"ciso","subagent_type":"nexus-ciso","prompt":"You are an independent CISO ... gate transition P5_CONSTRUCTION → P6_VERIFICATION. Produce a single DSL line: RED: VULN:<sev>;;LOC:<loc>;;TYPE:<type>;;FIX_REQ:<req>","expected_dsl_keys":["RED:VULN","RED:LOC","RED:TYPE","RED:FIX_REQ"]}
{"role":"qa-lead","subagent_type":"nexus-qa-lead","prompt":"You are an independent QA Lead ...","expected_dsl_keys":["RED:VULN","BLUE:STATUS"]}
{"role":"architect","subagent_type":"nexus-architect","prompt":"You are an independent principal architect ...","expected_dsl_keys":["BLUE:NORMS","BLUE:STATUS"]}
{"role":"devops-lead","subagent_type":"nexus-devops-lead","prompt":"You are an independent DevOps Lead ...","expected_dsl_keys":["RED:VULN","BLUE:STATUS"]}
```

The dispatcher reads each line, invokes the Agent tool with the named `subagent_type` and `prompt`, collects the DSL outputs, then calls back into the gate via `adversarial-gate.sh --judge-only --red "<aggregated RED DSL>" --blue "<aggregated BLUE DSL>"`.

## Cost envelope

| Workload | Token estimate |
|---|---|
| Single gate transition with `--council` | 4 × ~10k output tokens ≈ **40k tokens** |
| Full SDLC run (5 phase transitions) | 5 × 40k ≈ **200k tokens** |
| Quarterly audit (single SDLC run) | ≈ 200k tokens |
| Annual cost | ≈ 800k tokens |

For comparison, the harness's D→S journey consumed ~18M tokens across 8 iterations of council-driven design. The opt-in council cost is two orders of magnitude smaller per cycle.

The cost is **per output token**. Input tokens (prompts read by the agents) are negligible since each agent receives a fresh prompt with the phase context, no chat history.

## What this ADR does NOT do

- It does **NOT** make `--council` the default. The fixture path remains the default for unit tests, CI, and local dev.
- It does **NOT** mandate a specific model. The dispatcher picks (one model for all roles in v1; multi-model is documented opt-in in [`AUDIT_CYCLE.md`](AUDIT_CYCLE.md)).
- It does **NOT** auto-promote the council's verdict. The Judge logic in `adversarial-gate.sh --judge-only` still requires a CRIT/HIGH RED verdict to DENY; the council is a *signal*, not a *gate*.
- It does **NOT** change `THREAT_MODEL.md` items 1-7 (out-of-scope rows). Only item A6 (gate fixture) moves from OUT-OF-SCOPE to OPT-IN MITIGATED.

## Consequences

- The CRIT-2 finding from the original audit is **closed** in v1.3 (when PR-B lands).
- `THREAT_MODEL.md` A6 row updated to reflect the opt-in mitigation.
- A new failure mode is introduced: if `MULTIAGENT_BRIDGE_ENABLED=1` but the dispatcher doesn't honor exit 99 (or doesn't invoke the launcher), the gate output is the XML envelope without any verdict. The Judge path requires `--red` and `--blue`; without them, it errors out cleanly. Documented at the top of `multiagent-launcher.sh`.
- The 4 Nexus skills (`nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead`) become a **soft requirement** for full opt-in functionality. They are NOT vendored by the harness; downstream users without them get a clean error from the dispatcher.

## Rollback path

PR-B is a 5-file revert (`scripts/adversarial-gate.sh`, `scripts/multiagent-launcher.sh`, `tests/adversarial-test.sh` Tests 96/97, `docs/v1/THREAT_MODEL.md` A6 row, this ADR). No SQL migration. No schema change. The fixture path resumes immediately.

PR-A (docs + light wiring + `state_engine.py self_audit`) is independent and rolls back separately if needed.

## References

- `.ai/docs/designs/2026-06-02-integration-design.md` (the design)
- `.ai/docs/designs/2026-06-02-claude-code-integration-audit.md` (the prior adversarial audit)
- `docs/v1/AUDIT_CYCLE.md` (the recurring methodology this bridge supports)
- `CLAUDE.md` Law 6 (the contract this ADR codifies)
- Original 2026-06-01 audit CRIT-2 finding
