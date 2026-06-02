---
timestamp: 2026-05-30T23:50:00Z
trigger: anti-rot-every-5-calls
project: swebok-v4-harness
---

# MEMORY COMPACTION

## Project
- **Name**: SWEBOK v4 Harness
- **Main objective**: Production-ready SDLC enforcement via state machine + hooks + adversarial gates
- **Current phase**: P4_DESIGN (bootstrapped legacy codebase)

## Session context
- **Trigger**: Anti-ROT mandate (every 5 tool calls)
- **Delta**: Implemented M1–M6: CLAUDE.md compressed (5212→759 bytes), `.claude/settings.json` created, all scripts validated
- **Files read**: EXHAUSTIVE-HARNESS-SPEC.md, DSL.md, all core scripts
- **Files written**: CLAUDE.md (compressed), `.claude/settings.json` (new), `.claude/context/project-state.md`, `.claude/context/latest-handoff.md`

## What is already done
- CLAUDE.md compressed to 759 bytes (~150 tokens, under200-token mandate)
- `.claude/settings.json` created with PreToolUse + PostToolUse hook bindings
- M1 bootstrap: `swebok-bootstrap.sh` auto-detects P4_DESIGN for this project
- M2 DSL parser: `scripts/lib/dsl_parser.sh` handles GATE=PASS, GATE:PASS, missing pipes
- M3 hooks: `phase-guard.sh` blocks .py in P1 (EXIT:1), circuit breaker at 3 blocks
- M4 adversarial: `adversarial-gate.sh` P1→P2 PASS, outputs DSL-parseable Judge output
- M5 AOV: `act-observe-verify.sh`, `self-heal.sh`, `browser-use-orchestrator.sh` all have MCP graceful degradation (SKIP vs crash)
- M6 dry-run: All milestones validated

## Current state
- **All 6 milestones**: PASS ✓
- **Hook system**: fully wired via `.claude/settings.json`
- **Token budget**: under control (CLAUDE.md 759 bytes)
- **Ready for**: real codebase deployment (not the harness itself)

## Environment status
- **No services** running (framework, not runtime)
- **No DB**: `knowledge/swebok.db` not yet generated (run `python3 scripts/generate-kg.py --lite`)
- **No tests**: no test suite for harness itself (QA applies to target projects)

## Important files

| Path | Purpose | Notes |
|------|---------|-------|
| `.swebok_state` | Phase-locked state machine | P4_DESIGN, gates [P1,P2,P3]_EXIT |
| `CLAUDE.md` | Dispatcher (≤200 tokens) | Compressed from 5212 to 759 bytes |
| `.claude/settings.json` | Native hook integration | PreToolUse + PostToolUse wired |
| `scripts/lib/dsl_parser.sh` | Fuzzy DSL parser | GATE=PASS, GATE:PASS, auto-correct |
| `hooks/pre-tool-use/phase-guard.sh` | Phase enforcement + circuit breaker | blocks code in P1/P2 |
| `hooks/post-tool-use/auto-verify.sh` | Lint + syntax check | --lite flag for hot path |
| `scripts/adversarial-gate.sh` | Blue/Red/Judge | DSL output parseable by dsl_parser.sh |
| `scripts/multiagent-launcher.sh` | Parallel Agent calls | outputs Agent tool syntax |
| `scripts/act-observe-verify.sh` | E2E surveillance loop | MCP graceful degradation |
| `scripts/self-heal.sh` | Browser Use self-healing | MCP graceful degradation |
| `scripts/browser-use-orchestrator.sh` | BDD scenario orchestrator | MCP graceful degradation |
| `scripts/validate-qa-gates.sh` | P6_EXIT gate validation | chained QA1/QA2/QA3 |
| `scripts/swebok-query.py` | RAG query | SQLite FTS5, --lite fallback |
| `scripts/generate-kg.py` | KG indexer | --lite mode available |

## Decisions and rationale
- **CLAUDE.md compression**: original 5212 bytes →759 bytes to meet ≤200-token mandate
- **Graceful MCP degradation**: all MCP-wired scripts output `MCP_*:FAILED` + SKIP (not exit 1) when zai-mcp-server unreachable
- **Circuit breaker**:3 blocked attempts → override active (DEADLOCK_WARNING), prevents infinite blocking
- **Hot path --lite**: `auto-verify.sh --lite` skips heavy linting for micro-tasks (typo, comment, config tweak)

## Known failures / technical debt
- **None** in harness itself
- `knowledge/swebok.db` not generated: run `python3 scripts/generate-kg.py --lite` to populate
- QA triptych (QA1/QA2/QA3) not yet exercised on real codebase

## Open tasks
1. Run `python3 scripts/generate-kg.py --lite` to populate RAG knowledge base
2. Apply harness to a real project (not the harness) to exercise full P1→P9 flow
3. Wire QA triptych to CI/CD pipeline

## Risks and watchouts
- MCP tools (`zai-mcp-server`) may be unreachable in some environments → graceful degradation kicks in
- Screenshot tools (`scrot`, `gnome-screenshot`) may be absent → placeholder created
- Circuit breaker override is a break-glass mechanism — use only when certain action is correct

## Resume plan
1. Run `python3 scripts/generate-kg.py --lite` to build RAG index
2. Run `bash scripts/swebok-bootstrap.sh --force-phase P1` on a new project to start fresh SDLC
3. Run `bash scripts/adversarial-gate.sh P1 P2` to validate P1→P2 transition
