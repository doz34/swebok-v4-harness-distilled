# SWEBOK v4 Harness - Phase Management Specification

> **Per-phase recommended Claude Code skills**: see [`PHASE_SKILLS.md`](PHASE_SKILLS.md) for the catalogue mapping each phase (P1-P9) to recommended Speckit commands, Nexus specialists, and the Karpathy discipline doc. The harness emits structured ANTI-ROT nudges (see [`HOOKS.md`](HOOKS.md)) but does NOT auto-invoke any skill — the dispatcher decides whether to honor a suggestion.

## Overview

The SWEBOK v4 Harness enforces phase-gated development through strict phase transitions. Each phase has specific constraints that determine what actions are allowed.

## Phase Definitions

| Phase | Name | Description | Exit Gate |
|-------|------|-------------|-----------|
| P1 | Discovery | Stakeholder identification, scope definition | P1_EXIT |
| P2 | Requirements | Requirements gathering, approval, traceability matrix | P2_EXIT |
| P3 | Architecture | Architecture doc approval, C4 diagram | P3_EXIT |
| P4 | Design | Design doc complete, interfaces defined | P4_EXIT |
| P5 | Construction | Code implementation, compilation, testing | P5_EXIT |
| P6 | Testing/QA | QA verification, E2E testing, visual diff | P6_EXIT |
| P7 | Deployment | Deploy success, monitoring active, rollback validated | P7_EXIT |
| P8 | Maintenance | SLO achieved, maintenance documentation | P8_EXIT |
| P9 | Retirement | Archive, only /archived/ or /docs/ allowed | P9_EXIT |

## Phase Transition Rules

### Valid Transitions

```
P1 → P2: Requires P1_EXIT gate (stakeholders identified, scope defined)
P2 → P3: Requires P2_EXIT gate (requirements approved, traceability matrix)
P3 → P4: Requires P3_EXIT gate (architecture doc approved, C4 diagram)
P4 → P5: Requires P4_EXIT gate (design doc complete, interfaces defined)
P5 → P6: Requires P5_EXIT gate (compile errors resolved, test coverage met)
P6 → P7: Requires P6_EXIT gate (QA passed, E2E passed, visual diff < threshold)
P7 → P8: Requires P7_EXIT gate (deploy success, monitoring active)
P8 → P9: Requires P8_EXIT gate (maintenance complete, archive ready)
P9 → END: Project archived
```

### Invalid Transitions (Blocked)

- Skipping phases (e.g., P1 → P4)
- Going backwards (e.g., P5 → P3)
- Missing required gate validation

## Phase Constraints

### P1 (Discovery)
- **Allowed**: Requirements gathering, stakeholder identification, scope definition
- **Blocked**: Code files (.py, .ts, .js, .go, .java, etc.), src/ paths, mkdir src

### P2 (Requirements)
- **Allowed**: Requirements approval, traceability matrix, use cases
- **Blocked**: Code files, src/ paths, implementation

### P3 (Architecture)
- **Allowed**: Architecture design, component diagrams, C4 model
- **Blocked**: Implementation paths (src/, impl/, implementations/), .py files

### P4 (Design)
- **Allowed**: Design documents, interface definitions, maquettes
- **Blocked**: Implementation paths, .py files

### P5 (Construction)
- **Allowed**: Code implementation, compilation, unit tests
- **Blocked**: NEW src/ creation (mkdir src, touch src/x.py, mkdir /tmp/src)

### P6 (Testing/QA)
- **Allowed**: QA verification, E2E testing, test execution
- **Blocked**: Non-test src/ access, new implementation files

### P7 (Deployment)
- **Allowed**: Deployment operations, monitoring setup
- **Blocked**: Destructive commands (rm -rf, DROP TABLE, DELETE FROM)

### P8 (Maintenance)
- **Allowed**: Monitoring, SLO tracking, maintenance updates
- **Blocked**: Destructive commands

### P9 (Retirement)
- **Allowed**: Archive documentation, compliance reports
- **Blocked**: Package managers (except security/patch), new implementation, /src/, /lib/ (except /archived/, /docs/)

## State Management

### Phase State (`current_phase`)
- Stored in SQLite WAL database (`.swebok_state.db`)
- Key: `current_phase`
- Value: String like "P5_CONSTRUCTION"

### Gate Validation (`gates_validated`)
- Stored as JSON array: `["P1_EXIT","P2_EXIT","P3_EXIT","P4_EXIT"]`
- Check with: `python3 scripts/lib/state_engine.py get gates_validated`

### Phase Data (`phase_data`)
- JSON object storing per-phase counters and state
- P6 specific: `{"P6":{"aov_iterations":0,"heal_iterations":0,...}}`

## Phase Guard Implementation

`hooks/pre-tool-use/phase-guard.sh` blocks Write/Edit operations:

```bash
# P1/P2: Block code files
if [[ "$FILE_PATH" =~ \.(py|ts|js|go|java|c|cpp|rs|rb|php|swift|kt)$ ]]; then
    SHOULD_BLOCK="true"
fi

# P3/P4: Block implementation paths
if [[ "$FILE_PATH" =~ (/src/|/impl/|/implementations/) ]]; then
    SHOULD_BLOCK="true"
fi

# P6: Block non-test src/ access
if [[ "$FILE_PATH" =~ (/src/|^src/) ]] && [[ ! "$FILE_PATH" =~ (test|spec|__tests__|tests?/) ]]; then
    SHOULD_BLOCK="true"
fi

# P9: Block /src/ and /lib/ except /archived/ and /docs/
if [[ "$FILE_PATH" =~ (/src/|/lib/) ]] && [[ ! "$FILE_PATH" =~ (/archived/|/docs/) ]]; then
    SHOULD_BLOCK="true"
fi
```

## Bash Scanning Per Phase

`scripts/lib/bash_scanner.py` uses PHASE_RULES dict for Bash tool commands:

| Phase | Bash Blocked |
|-------|-------------|
| P1/P2 | mkdir src, python -c open(), src/ paths |
| P3/P4 | src/, impl/, implementations/, .py files |
| P5 | mkdir src, mkdir /tmp/src, mkdir /impl |
| P6 | /src/ (except test paths) |
| P7/P8 | rm -rf, DROP TABLE, DELETE FROM |
| P9 | npm install, pip install, apt-get install (except security/patch) |

## Circuit Breaker

After 3 blocks in any phase, an override activates for 5 minutes:
- `circuit_breaker.blocked_attempts`: Counter (resets on successful action)
- `circuit_breaker.override_active`: Boolean with 5-minute TTL
- `circuit_breaker.override_timestamp`: Unix timestamp of activation

## Version

- Current: 1.3.0 (2026-06-01)
- Changed: Added P9 Retirement phase, fixed duplicate P3/P4 headers