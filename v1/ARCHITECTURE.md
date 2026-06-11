# SWEBOK v4 Harness — Architecture (Distilled)

> **Version**: v2.6.2 (2026-06-11)
> **Scope**: The distilled (`swebok-v4-harness-distilled`) fork's current module
> decomposition, security model, and data flow. Replaces the v1.4.1-era single-file
> `state_engine.py` description that this document previously contained.

---

## 1. System diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Claude Code (AI Assistant)                   │
│                                                                     │
│  When you type: "Create a login API endpoint"                       │
│  Claude wants to: Write → src/auth.py, Bash → python3 manage.py    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                  settings.json routes tool calls to hooks
                             │
         ┌───────────────────┼───────────────────────────────┐
         ▼                   ▼                               ▼
  ┌──────────────┐   ┌──────────────┐   ┌───────────────────────────┐
  │  PHASE-GUARD │   │  BASH-GUARD  │   │  POST-TOOL-USE HOOKS     │
  │              │   │              │   │                           │
  │ Triggers on: │   │ Triggers on: │   │ • auto-verify.sh         │
  │ • Write      │   │ • Bash       │   │   (syntax check P5+)     │
  │ • Edit       │   │              │   │ • council-scheduler-hook │
  │ • Skill      │   │ Scans for:   │   │   (schedule reviews)     │
  │              │   │ • rm -rf     │   │ • mini-council-hook      │
  │ Checks:      │   │ • DROP TABLE │   │   (quick heuristic)      │
  │ • Current    │   │ • eval(base64│   │                           │
  │   phase      │   │ • sudo       │   │ • auto-trigger-hook.sh   │
  │ • File type  │   │ • curl|sh    │   │   (UserPromptSubmit)     │
  │ • Phase rules│   │ • mkfs, dd   │   │                           │
  └──────┬───────┘   └──────┬───────┘   └───────────────────────────┘
         │                  │
         ▼                  ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     STATE ENGINE                             │
  │                                                              │
  │  .swebok_state.db (SQLite WAL, per-project isolation)       │
  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
  │  │ state table │ │ 4 audit      │ │ circuit_breaker      │ │
  │  │ (key/value) │ │ tables       │ │ (3-strike lock)      │ │
  │  │             │ │ (HMAC chain) │ │                      │ │
  │  │ phase: P5   │ │              │ │ file X: 2/3 blocks   │ │
  │  │ gates: [..] │ │ append-only  │ │                      │ │
  │  │ tools: 152  │ │ triggers     │ │ override: false      │ │
  │  └─────────────┘ └──────────────┘ └──────────────────────┘ │
  │                                                              │
  │  Security: HMAC key per install, mode 0600, gitignored      │
  │  Integrity: verify_audit_chain, export_state, rebuild        │
  └──────────────────────────────────────────────────────────────┘
```

## 2. State Engine — module decomposition (v2.6.2)

The `state_engine.py` god-class has been progressively decomposed into 7
sibling modules plus 1 compat helper, all importable as a flat namespace
(e.g. `from state_engine import verify_audit_chain` works because the
parent re-exports). Total: **~2,600 LOC** spread across the cluster.

| Module | LOC | Owns |
|---|---|---|
| `state_engine.py` (core) | ~900 | DB connection, schema, `_init_db`, `_xact`, `get`/`set`/`increment`, public re-exports |
| `state_engine_audit.py` | 294 | HMAC chain (`audit_hmac`, `last_hmac`, `verify_audit_chain`, `recompute_audit_chain`), trigger management (`drop_audit_triggers`, `ensure_triggers`) |
| `state_engine_counters.py` | 219 | Atomic scalar + nested JSON phase counters (`increment_lint`, etc.) |
| `state_engine_logging.py` | 177 | Logging API (`log_event`, `log_tool_call`, `log_adversarial`, `query_*`) |
| `state_engine_prune.py` | 152 | Crash-safe prune (`prune_log_events`, `prune_state_events`, …) |
| `state_engine_recovery.py` | 174 | DB recovery (`rebuild`, `check_integrity`) |
| `state_engine_self_audit.py` | 197 | Quarterly self-audit (`self_audit`, `replay_session`) |
| `state_engine_gates.py` | 73 | Gate lifecycle (`append_gate`) |
| `state_engine_export.py` | 73 | JSON export (`export_state`, `export_audit`) |
| `state_engine_cli.py` | 296 | `main()` CLI dispatcher + subcommand handlers |
| `state_engine_compat.py` | 50 | Shared `_se()` lazy accessor for sibling modules |
| **Total** | **~2,600** | 11 sibling modules + 1 compat helper |

**Sibling module pattern**: every child module exposes its public API at
the top level, and `state_engine.py` re-exports them via
`from state_engine_audit import (audit_hmac, last_hmac, …)  # noqa: F401`.
Children never import `state_engine` at module-load time (would create a
circular import); instead they use the shared `from state_engine_compat
import _se` accessor to resolve sibling privates lazily.

**Public surface vs implementation details**: post-v2.6.2 the audit chain
primitives (`audit_hmac`, `last_hmac`, `drop_audit_triggers`,
`ensure_triggers`) are public (no leading underscore) — they're called
from 5+ sibling modules and form the documented public surface for the
audit chain.

## 3. Compiled knowledge engine (7 layers, 1,139 books distilled)

| Layer | Count | Examples |
|---|---|---|
| Principles | 24 | KISS, YAGNI, DRY, Fail Fast |
| Antipatterns | 46 | God Class, Spaghetti Code, Magic Numbers |
| Ontologies | 6 | SWEBOK taxonomy, Python ecosystem, ML systems |
| Decision trees | 5 | choose-database, choose-protocol |
| Recipes | 5 | api-design, authentication, error-handling |
| Comparisons | 3 | SQL vs NoSQL, REST vs GraphQL, monolith vs microservices |
| Checklists | 9 | one per phase P0–P9 (deliverables + done criteria) |
| Risks | 4 | security, performance, maintainability, operational |
| Corpus enrichment | 144 | adversarial-accepted concepts from 1,139 books |

Query: `<5ms`, deterministic, $0, offline, no LLM. See
`scripts/compiled_knowledge.py` for the CLI.

## 4. Security model

### What we protect against

| Threat | Defense |
|---|---|
| External attacker (different UID) | HMAC key chmod 0600, audit chain tamper-evident |
| Accidental developer mistake (rm -rf in wrong dir, eval base64) | Phase guard + bash guard + circuit breaker |
| Prompt injection via malicious input | 3-layer detection (outer marker, inner phase, scoper) |
| Supply chain compromise | pip hash-pinned, HARNESS_DIR validated, state DB per-project |

### What we do NOT protect against

- **Same-user privilege escalation**: any process running as your user
  can read the HMAC key. Audit chain defends against different-user
  tampering, not same-user attacks.
- **Physical access**: someone with your machine can edit the state DB.
- **Social engineering**: the harness cannot prevent you from manually
  overriding it.

### Security features checklist

| Feature | How | Tested |
|---|---|---|
| HMAC audit chain | SHA-256, per-row, chained | `verify_audit_chain` (4 tables) |
| Append-only audit | BEFORE DELETE/UPDATE triggers | `test_health.py::test_hooks_wired_count` |
| State DB isolation | Per-project, world-writable CWD refused | unit tests |
| HARNESS_DIR validation | Trust boundary check, `samefile()` | `state_engine.py:78-85` |
| Bash command scanning | Phase-aware, 30+ dangerous patterns | `bash_scanner.py` |
| SQL injection protection | Allowlist table names, parameterized queries | CLI + counters |
| Path traversal detection | Symlink rejection, path sandboxing | `test-adversarial.sh` |
| SSRF protection | Private IP rejection (Ollama provider) | `test-adversarial.sh` |
| Kill switch | 1 env var disables all auto-triggers | `HARNESS_AUTO_TRIGGER=0` |

## 5. Data flow: what happens when you type a command

```
 User types: "Create a REST API for user authentication"
                           │
                           ▼
              ┌────────────────────────┐
              │  Claude Code parses    │
              │  and plans actions:    │
              │                        │
              │  1. Write → auth.py    │
              │  2. Write → test_auth  │
              │  3. Bash → pytest      │
              └───────────┬────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
   Action 1: Write   Action 2: Write   Action 3: Bash
   auth.py            test_auth.py      pytest
         │                │                │
         ▼                ▼                ▼
   ┌───────────┐   ┌───────────┐   ┌───────────┐
   │phase-guard│   │phase-guard│   │bash-guard │
   │           │   │           │   │           │
   │ Phase P5? │   │ Phase P5? │   │ Safe cmd? │
   │ .py file? │   │ test/ OK? │   │ pytest OK │
   │           │   │           │   │           │
   │ ✅ ALLOW  │   │ ✅ ALLOW  │   │ ✅ ALLOW  │
   └───────────┘   └───────────┘   └───────────┘
         │                │                │
         └────────────────┼────────────────┘
                          ▼
              ┌────────────────────────┐
              │  State Engine updates: │
              │  • tool_call_count +=3 │
              │  • audit log: 3 events │
              │  • HMAC chain updated  │
              └────────────────────────┘
```

If the phase were P2 (Requirements) instead of P5, the phase-guard would
**block** the Write actions with a clear message (see
`hooks/pre-tool-use/phase-guard.sh`).

## 6. Multi-session support

SQLite with WAL mode natively handles concurrent access:
- **Readers**: don't block each other
- **Writers**: `BEGIN EXCLUSIVE` serializes writes (10-attempt retry in `_xact()`)
- **No explicit `fcntl.flock`** — SQLite WAL handles it
- **No stale lock recovery** — `.swebok_state.db-wal` and `.shm` are managed by SQLite

## 7. File structure (distilled fork)

```
swebok-v4-harness-distilled/
├── CLAUDE.md                  # Laws and routing rules (the "constitution")
├── README.md                  # User-facing docs (15 sections, ASCII diagrams)
├── CHANGELOG.md               # Version history
├── LICENSE                    # MIT
├── settings.json              # Hook wiring (merged into ~/.claude/)
│
├── lib/                       # Python core (canonical location)
│   ├── state_engine.py        #   State machine + re-exports (~900 LOC)
│   ├── state_engine_audit.py  #   HMAC chain + triggers (294 LOC)
│   ├── state_engine_counters.py
│   ├── state_engine_logging.py
│   ├── state_engine_prune.py
│   ├── state_engine_recovery.py
│   ├── state_engine_self_audit.py
│   ├── state_engine_gates.py
│   ├── state_engine_export.py
│   ├── state_engine_cli.py
│   ├── state_engine_compat.py #   Shared _se() lazy accessor
│   ├── bash_scanner.py        #   Phase-aware command filtering
│   ├── dsl_engine.py          #   DSL parser (KEY:VALUE;; delimiter)
│   ├── auto_trigger.py        #   Intent detection (4-layer)
│   └── adv-loop/              #   Adversarial loop (S0–S5)
│
├── pre-tool-use/              # Hooks that run BEFORE each tool call
│   ├── phase-guard.sh
│   ├── bash-guard.sh
│   ├── token-counter.sh
│   ├── auto-trigger-hook.sh
│   └── phase-change-detector.sh
│
├── post-tool-use/             # Hooks that run AFTER each tool call
│   ├── auto-verify.sh
│   ├── council-scheduler-hook.sh
│   └── mini-council-hook.sh
│
├── distilled/                 # The curated knowledge base (7 layers)
├── distilled_corpus/          # Raw distillation (1,139 books, gitignored)
├── scripts/                   # CLI tools (symlinks → ../lib/ for bash)
├── bin/                       # Adversarial loop runner
├── tests/                     # Test suites (152 tests total)
├── specs/adversarial-patterns/ # Per-phase adversarial patterns (P0–P10)
├── audit/                     # Phase audit reports (P0–P10, all 🟢)
├── docs/                      # Architecture docs, ADRs
├── adversarial-gate.sh        # Red/Blue/Judge gate with DSL
├── multiagent-launcher.sh     # Council bridge (4 LLM judges)
├── health-check.sh            # Readiness probe (7 checks)
├── pre-commit-hook.sh         # Git pre-commit gate (152 tests + HMAC)
└── install-harness.sh         # One-command installer
```

## 8. Version history

- **v2.6.2** (2026-06-11) — 11 sibling modules, 1,139 books, 152 tests, 94.5% Council #9
- **v2.6.0** (2026-06-10) — Anti-Drift Auto-Trigger (G1 + G3 + G5 + G6)
- **v2.5.0** (2026-06-10) — Adversarial loop S0–S5 (44 property tests)
- **v2.0.0** (2026-06-03) — Multi-view retrieval (L0 + L1 + router)
- **v1.5.x** (2026-06-03) — Production hardening batch (CRIT-8 + STRIDE)
- **v1.4.1** (2026-06-01) — *This document's last accurate version* (single-file state engine)

See `CHANGELOG.md` for the full diff history and `audit/` for the per-phase
audit reports (all 10 phases closed at 🟢).
