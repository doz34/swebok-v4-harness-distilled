# SWEBOK v4 Harness - Architecture

## Overview

The SWEBOK v4 Harness is an SDLC enforcement framework that enforces phase-gated development through Claude Code hooks and scripts.

## Simplified Architecture

**Key Principle**: "Smaller delta" - SQLite replaces YAML+flock, handles mono AND multi-session natively.

## Core Components

### 1. State Engine (`scripts/lib/state_engine.py`)
- **Purpose**: Centralized state management
- **Backend**: SQLite with WAL mode (handles concurrent access)
- **Multi-session**: SQLite WAL allows multiple readers while writing
- **Mono-session**: Works without modification
- **Atomic Operations**: Counters use single-statement atomic UPSERT (`INSERT...ON CONFLICT DO UPDATE`) and JSON1 `json_set`/`json_extract` for nested keys (no read-modify-write race). State+audit writes that need a combined transaction (e.g. `set()` writes both `state` and `state_events` atomically) use `BEGIN EXCLUSIVE` with a 10-attempt retry loop in `_xact()`. Audit rows carry an HMAC-SHA256 chain (`row_hmac`); `verify_audit_chain` detects tampering and `recompute_audit_chain` re-attaches the chain after a legitimate prune.

**Key Functions**:
- `get(key_path)` - Read state using dot notation
- `set(key_path, value)` - Write state with dot notation (ATOMIC for nested keys)
- `increment_blocked()` - Atomic via single-statement UPSERT
- `increment_aov_iterations()` - Atomic via `json_set` + `json_extract`
- `increment_heal_iterations()` - Atomic via `json_set` + `json_extract`
- `log_adversarial(gate, verdict, reason)` - Audit logging
- `reset_all_circuits(phase)` - Reset counters on phase transition

**State Storage**:
```
.state.db (SQLite)
├── state (key-value table)
│   ├── current_phase: "P5_CONSTRUCTION"
│   ├── circuit_breaker: '{"blocked_attempts":0,"override_active":false}'
│   └── phase_data: '{"P6":{"aov_iterations":0}}'
└── metadata (version info)
```

### 2. Bash Scanner (`scripts/lib/bash_scanner.py`)
- **Purpose**: Phase-aware command filtering for Bash tool
- **Method**: Pattern matching per phase
- **FAIL-SECURE**: Blocks on any parse error

**Phase Rules**:
| Phase | Blocked |
|-------|---------|
| P1/P2 | Code files (.py, .ts, .js) and src/ paths |
| P3/P4 | Implementation paths (src/, impl/, implementations/) |
| P5 | NEW src/ creation (mkdir src, touch src/x.py) |
| P6 | ALL /src access except test-related |
| P7/P8 | Destructive commands (rm -rf, DROP TABLE) |

### 3. DSL Engine (`scripts/lib/dsl_engine.py`)
- **Purpose**: Parse the strict DSL format with `;;` delimiter
- **Delimiter**: `;;` (pipe `|` preserved in values)

**Format**:
```
GATE:PASS;;FIX_REQ:NONE;;REASON:NO_CRITICAL_FLAWS
RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION;;FIX_REQ:SANITIZE
BLUE: DEFENDED;;NORMS:KA-1+KA-13;;STATUS:OK
```

### 4. Phase Guard (`hooks/pre-tool-use/phase-guard.sh`)
- **Purpose**: Block Write/Edit operations based on current phase
- **Circuit Breaker**: 3 blocks → override for 5 minutes

### 5. Bash Guard (`hooks/pre-tool-use/bash-guard.sh`)
- **Purpose**: Scan Bash tool commands for forbidden patterns
- **Method**: Calls bash_scanner.py for phase-aware filtering

### 6. MCP Bridge (`scripts/act-observe-verify.sh`, `scripts/self-heal.sh`)
- **Purpose**: Bridge to MCP tools via XML tags
- **Format**: `<MCP_CALL><tool>...</tool><args>{...}</args></MCP_CALL>`
- **Anti-Loop**: aov_iterations >= 2 blocks further attempts

## File Structure

```
swebok-v4-harness/
├── hooks/
│   ├── pre-tool-use/
│   │   ├── phase-guard.sh      # Phase enforcement
│   │   └── bash-guard.sh     # Bash command scanning
│   └── post-tool-use/
│       └── auto-verify.sh
├── scripts/
│   ├── lib/
│   │   ├── state_engine.py     # SQLite-based state (SIMPLIFIED)
│   │   ├── bash_scanner.py     # Command filtering
│   │   └── dsl_engine.py       # DSL parsing
│   ├── adversarial-gate.sh
│   ├── act-observe-verify.sh
│   ├── self-heal.sh
│   ├── bdd-generator.sh        # BDD scenario generation (P6)
│   └── browser-use-orchestrator.sh  # Browser Use automation (P6)
├── tests/
│   └── adversarial-test.sh      # 47/47 PASS
└── docs/v1/                    # Versioned documentation
```

## Data Flow

```
User Prompt → Claude Code → Intent Detection
                                 ↓
                   Phase Guard (hooks/pre-tool-use/)
                                 ↓
                   Bash Guard (if Bash tool)
                                 ↓
                   State Engine (SQLite - no locking code!)
                                 ↓
                   Action Allowed/Blocked
```

## Security Model

1. **FAIL-SECURE**: Any error → block action
2. **Defense in Depth**: phase-guard + bash-guard
3. **Circuit Breaker**: 3 blocks → override with 5min TTL
4. **Anti-Loop**: aov_iterations >= 2, heal_iterations >= 3
5. **Audit Trail**: adversarial_log in SQLite

## Multi-Session Support

SQLite with WAL mode natively handles concurrent access:
- **Readers**: Don't block each other
- **Writers**: BEGIN EXCLUSIVE serializes writes
- **No explicit fcntl.flock code needed**
- **No stale lock recovery hack needed**

## Version

- Current: 1.4.1 (2026-06-01)
- Changes: Audit fixes - atomicity, P9 path blocking, MCP XML format, docs consistency
- See: `docs/v1/VERSION`
