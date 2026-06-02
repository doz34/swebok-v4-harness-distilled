---
timestamp: 2026-05-30T23:50:00Z
trigger: anti-rot-every-5-calls
project: swebok-v4-harness
---

# PROJECT STATE

## Identity
- **Project**: SWEBOK v4 Harness — production SDLC enforcement framework
- **Type**: Claude Code harness + hooks system
- **Current phase**: P4_DESIGN (bootstrapped from existing codebase)
- **Gates validated**: [P1_EXIT, P2_EXIT, P3_EXIT]

## Architecture (Implemented)
- State machine: `.swebok_state` (YAML, phase-locked)
- DSL parser: `scripts/lib/dsl_parser.sh` (fuzzy-tolerant, auto-corrects)
- Phase guard: `hooks/pre-tool-use/phase-guard.sh` (circuit breaker, 3-block override)
- Auto-verify: `hooks/post-tool-use/auto-verify.sh` (--lite flag for hot path)
- Adversarial gate: `scripts/adversarial-gate.sh` (Blue/Red/Judge, DSL output)
- Multiagent launcher: `scripts/multiagent-launcher.sh` (Agent tool syntax output)
- AOV loop: `scripts/act-observe-verify.sh` (MCP-wired, graceful degradation)
- Self-heal: `scripts/self-heal.sh` (MCP-wired error diagnosis)
- Browser orchestrator: `scripts/browser-use-orchestrator.sh` (MCP-wired E2E loop)
- QA gates: `scripts/validate-qa-gates.sh` (chained QA1/QA2/QA3)
- RAG query: `scripts/swebok-query.py` (SQLite FTS5, --lite fallback)
- KG generator: `scripts/generate-kg.py` (--lite mode available)
- Bootstrap: `scripts/swebok-bootstrap.sh` (auto-detect existing vs greenfield)
- Native integration: `.claude/settings.json` (PreToolUse + PostToolUse hooks wired)

## Token Budget
- CLAUDE.md: 759 bytes (~150 tokens) ✓
- DSL.md: ~500 tokens
- .swebok_state: ~100 tokens
- Phase context: 2000 tokens max
- RAG result: 100 tokens
- **Total base: ~3000 tokens** (vs 800k naive)

## Quality Gates
```
GATE[P5_EXIT]: COMPILE:0 | COV:>80 | SAST_CRIT:0
GATE[P6_EXIT]: QA1_PASS | QA2_PASS | QA3_PASS | E2E:100% | VDIFF:<2% | XSS:PASS
GATE[P7_EXIT]: DEPLOY_SUCCESS | MONITORING_ACTIVE
```

## Validated
- M1: Bootstrap → P4_DESIGN detected ✓
- M2: DSL parser handles GATE=PASS, GATE:PASS, missing pipes ✓
- M3: `.claude/settings.json` written with PreToolUse/PostToolUse bindings ✓
- M4: Adversarial gate outputs DSL, multiagent outputs Agent tool syntax ✓
- M5: AOV/self-heal/orchestrator have graceful MCP degradation ✓
- M6: P1 blocks .py Write (EXIT:1), circuit breaker at 3 blocks ✓

## Status
- **Fully operational**: core scripts + hooks + native integration complete
- **Pending**: real codebase (not harness itself) to exercise full P1→P9 flow
