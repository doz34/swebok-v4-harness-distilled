# SWEBOK v4 Harness - Hooks Integration Guide

## Overview

Hooks are executable scripts that Claude Code invokes at specific lifecycle points to enforce phase-gated development and safety constraints.

## Hook Types

### Pre-Tool-Use Hooks (`hooks/pre-tool-use/`)

Invoked BEFORE a tool is executed. Can block the action or modify behavior.

| Hook | Purpose | Fail-Secure |
|------|---------|-------------|
| `phase-guard.sh` | Block Write/Edit based on current phase | Exit 1 on any error |
| `bash-guard.sh` | Scan Bash commands for forbidden patterns | Exit 1 on any error |

### Post-Tool-Use Hooks (`hooks/post-tool-use/`)

Invoked AFTER a tool executes. Used for auto-verification and linting.

| Hook | Purpose | Fail-Secure |
|------|---------|-------------|
| `auto-verify.sh` | Auto-lint + syntax check after Write/Edit | Exit 0 (allow action) |

### Event Hooks (`hooks/event/`)

Invoked on specific events.

| Hook | Purpose |
|------|--------|
| (event hooks) | Reserved for future use |

## Phase Guard (`phase-guard.sh`)

**Purpose**: Block Write/Edit operations based on current SDLC phase.

**Auto-Bootstrap (FAIL-SECURE)**: At script start, if `.swebok_state.db` is missing, the hook automatically executes `bash scripts/swebok-bootstrap.sh` to create it. This ensures the hook never fails on a fresh clone. If the bootstrap script is absent or fails, the hook blocks with `BOOTSTRAP_FAILED` and exits 1.

**Logic**:
- P1/P2: No code files (.py, .ts, .js, etc.) allowed - requirements only
- P3/P4: No implementation paths (src/, impl/, implementations/) allowed
- P5: NEW src/ creation (mkdir src, touch src/x.py) blocked
- P6: ALL /src access except test-related paths blocked

**Circuit Breaker**: After 3 blocks, override activates for 5 minutes.

**Usage**:
```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"/path/to/file.py"}}' | bash hooks/pre-tool-use/phase-guard.sh __JSON__
```

## Bash Guard (`bash-guard.sh`)

**Purpose**: Phase-aware command scanning for Bash tool.

**Method**: Calls `bash_scanner.py` for pattern matching per phase.

**Phase Rules**:
| Phase | Blocked |
|-------|---------|
| P1/P2 | Code files (.py, .ts, .js) and src/ paths |
| P3/P4 | Implementation paths (src/, impl/, implementations/) |
| P5 | NEW src/ creation (mkdir src, touch src/x.py) |
| P6 | ALL /src access except test-related |
| P7/P8 | Destructive commands (rm -rf, DROP TABLE) |

**Usage**:
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /src"}}' | bash hooks/pre-tool-use/bash-guard.sh __JSON__
```

## Auto-Verify (`auto-verify.sh`)

**Purpose**: Auto-lint and syntax check after Write/Edit operations.

**Features**:
- Language-specific linting (Python, JavaScript, TypeScript, Go, Java, Rust)
- Syntax validation for P5+ phases
- Lint circuit breaker: 3 failures → requires human review

**Usage**:
```bash
bash hooks/post-tool-use/auto-verify.sh Write "/path/to/file.py"
bash hooks/post-tool-use/auto-verify.sh Edit "/path/to/file.py" --lite
```

## Hook Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HARNESS_DIR` | `$HARNESS_DIR (auto-resolved)` | Harness root directory |
| `STATE_FILE` | `.swebok_state` | State file path (deprecated, use .swebok_state.db) |
| `STATE_DB` | `.swebok_state.db` | SQLite state database |

### Integration with Claude Code

Place hooks in the correct directory structure:
```
hooks/
├── pre-tool-use/
│   ├── phase-guard.sh
│   └── bash-guard.sh
├── post-tool-use/
│   └── auto-verify.sh
└── event/
```

Claude Code will automatically invoke these hooks based on tool usage.

## Error Handling

All hooks use `trap '...' ERR` for FAIL-SECURE behavior:
- phase-guard.sh: `trap 'echo "WARN:HOOK_INTERNAL_ERROR: Blocking action due to script crash"; exit 1' ERR`
- bash-guard.sh: `trap 'echo "WARN:HOOK_INTERNAL_ERROR: Blocking action due to script crash"; exit 1' ERR`
- auto-verify.sh: `trap 'echo "WARN:HOOK_INTERNAL_ERROR: Allowing action due to script crash"; exit 0' ERR` (allows action on internal errors)

## Testing Hooks

```bash
# Test phase-guard
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/test/src/main.py"}}' | bash hooks/pre-tool-use/phase-guard.sh __JSON__

# Test bash-guard
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /src"}}' | bash hooks/pre-tool-use/bash-guard.sh __JSON__

# Test auto-verify
bash hooks/post-tool-use/auto-verify.sh Write "/tmp/test.py"
```

## Version

- Current: 1.1.0 (2026-06-01)
- Changed: Simplified architecture (YAML+flock → SQLite WAL)