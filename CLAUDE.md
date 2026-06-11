# SWEBOK v4 HARNESS DISPATCHER

## Path Convention (scripts/* = canonical alias for lib/* and root scripts)

The repo exposes two parallel paths for the same files:
- `lib/state_engine.py` ← canonical, used by hooks and Python imports
- `scripts/lib/state_engine.py` ← symlink → `lib/`, used by bash scripts and CI

Both refer to the same on-disk file. The `scripts/` namespace is a **stable alias** so existing bash scripts and CI workflows that hardcoded `scripts/lib/...` paths continue to work after the lib/ refactor. Same for `scripts/adversarial-gate.sh` and `scripts/multiagent-launcher.sh` (both symlinks to root files).

**Authoring rule**: new code should import from `lib/` (Python) or call from root (bash). The `scripts/*` aliases exist for legacy callers — do not duplicate, always use the symlink.

## Laws
1. **HOT_PATH** - intent=micro_task → execute + --lite
2. **STATE-DRIVEN** - read .swebok_state.db via `python3 lib/state_engine.py get <key>` (SQLite ONLY)
3. **COMPILED-KNOWLEDGE** - for SWEBOK/ISO knowledge, execute: `python3 scripts/compiled_knowledge.py <query>`. This is the deterministic alternative to RAG: pre-distilled 872-book knowledge base in 7 layers (principles, antipatterns, ontologies, decision trees, recipes, comparisons, checklists). No LLM, no embeddings, no network. Same input = same answer.
4. **CAVEMAN_ULTRA** - all output in DSL format with `;;` delimiter. **Scope:** the CAVEMAN_ULTRA delimiter applies to *verdict payloads* (gate outcomes, red/blue findings, self-heal recommendations). Diagnostic log lines emitted by hooks (e.g. `[PHASE-GUARD] BLOCKED: ...`, `[AOV] Screenshot: ...`) are not DSL — they are plain-text operational logs for human operators. Only the lines that the dispatcher parses as input to a downstream decision must obey the `KEY:VALUE;;KEY:VALUE` format.
5. **MCP BRIDGE** - when a script outputs `<MCP_CALLS><MCP_CALL tool="X" args="Y"/></MCP_CALLS>`, you MUST: 1) Invoke MCP tool X with args Y. 2) Save the exact MCP tool output to `/tmp/mcp_result.json`. 3) Re-execute the original script with the flag `--verify-result /tmp/mcp_result.json` to close the loop and evaluate the visual/UI evidence.
6. **MULTIAGENT BRIDGE** - when `adversarial-gate.sh` outputs `<MULTIAGENT_LAUNCH blue="Nexus_Defender" red="Nexus_Attacker" prompt="..."/>`, invoke Agent tool with `subagent_type: nexus-defender` and `subagent_type: nexus-attacker` (the runtime agents are external `nexus-*` subagent_type identifiers; there is no local `agents/` or `skills/` tree in this repo). Spawn Red and Blue teams in parallel. Once both return their DSL outputs, you MUST execute `bash scripts/adversarial-gate.sh <from_phase> <to_phase> --judge-only --red "RED_DSL_OUTPUT" --blue "BLUE_DSL_OUTPUT"` to finalize the gate verdict and log the state.
6.1. **COUNCIL BRIDGE (ADR-003 / G.3)** - when the gate is invoked with `--council`, the emitted `<MULTIAGENT_LAUNCH gate="<from>_EXIT" target="<to>">...</MULTIAGENT_LAUNCH>` envelope contains a JSONL body: one JSON object per reviewer role (`ciso`, `qa-lead`, `architect`, `devops-lead`). For each JSON line: (1) invoke the Agent tool with the line's `subagent_type` and `prompt`; (2) collect the agent's SINGLE DSL output line. After all 4 agents return, aggregate the RED DSL lines (worst-severity wins: CRIT > HIGH > MED > LOW) and the BLUE DSL lines (any FAIL → DEFENDED:FAIL; all OK → DEFENDED:OK), then call `bash scripts/adversarial-gate.sh <from> <to> --judge-only --red "<aggregated RED>" --blue "<aggregated BLUE>"` exactly once. The gate exits 99 from the council branch as a signal that the dispatcher must continue with the spawn — failing to honor it leaves the gate in PENDING/REQUEST state and is logged in the audit chain.
7. **ANTI-ROT** - every 5 calls → emit structured nudge `ANTI-ROT:NUDGE skill=project-continuity reason=tool_call_count_multiple_of_5 tool_call_count=<N>` then exit 2. The dispatcher MAY invoke `/skill:project-continuity` in response; the harness never auto-invokes.

## State Management
- **Source of truth**: `.swebok_state.db` (SQLite WAL)
- **NEVER read/write `.swebok_state` YAML** (deprecated)
- Human debugging: `python3 lib/state_engine.py export_state`
- **HMAC security model**: The `.audit_key` (chmod 0600) protects against external attackers with different user IDs. It does NOT defend against same-user privilege escalation (any process running as the same user can read the key). This is an accepted limitation of filesystem-based secrets.

## Gates
- adversarial-gate.sh - Red/Blue team with strict DSL
- Circuit break at 3 blocks (override for 5min)
- Phase transitions require GATE:PASS

## Routing
- STRICT[P1-P9] enforced by hooks/pre-tool-use/phase-guard.sh
- DSL.md for format reference
- docs/v1/ARCHITECTURE.md for system design
- docs/v1/PHASE_SKILLS.md for per-phase recommended Claude Code skills
- docs/v1/AUDIT_CYCLE.md for the recurring quarterly council methodology
- docs/v1/EVIDENCE_LEDGER.md for the durable audit-findings index
- docs/v1/ADR-003-multiagent-bridge.md for the opt-in council bridge (CRIT-2 close-out)

## Tests
- tests/distilled-test.sh - **20/20 PASS, deterministic** — the compiled knowledge engine: 24 principles, 46 antipatterns, 5 ontologies, 5 decision trees, 5 recipes, 3 comparisons, 9 phase checklists, 4 risk catalogs. Pure Python, no LLM, no RAG, no network. See `distilled/README.md` for the architecture.

## Key Files
- `lib/state_engine.py` - Atomic state with SQLite WAL (no fcntl.flock)
- `lib/bash_scanner.py` - Phase-aware command filtering
- `lib/dsl_engine.py` - DSL parsing with `;;` delimiter
- `hooks/pre-tool-use/phase-guard.sh` - Phase enforcement
- `hooks/pre-tool-use/bash-guard.sh` - Bash command guard