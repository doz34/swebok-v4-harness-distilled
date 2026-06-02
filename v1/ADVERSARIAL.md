# SWEBOK v4 Harness - Adversarial Testing Framework

## Overview

The adversarial framework uses Red/Blue team analysis with strict DSL output to validate gate transitions between SDLC phases.

## Adversarial Gate Flow (`scripts/adversarial-gate.sh`)

```
1. Generate RED TEAM template (vulnerability analysis)
2. Generate BLUE TEAM template (defense verification)
3. Simulate outputs for internal testing (production: Claude agents write outputs)
4. Parse RED/BLUE with dsl_engine.py
5. Judge decision based on severity
6. Log result to state
7. Reset circuits on PASS
```

## DSL Format (STRICT)

### Attack (RED)
```
RED: VULN:<severity>;;LOC:<location>;;TYPE:<vulnerability_type>;;FIX_REQ:<fix>
```
Example:
```
RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION;;FIX_REQ:SANITIZE_ALL_INPUTS
```

### Defense (BLUE)
```
BLUE: DEFENDED;;NORMS:<ka_numbers>;;STATUS:<ok|failed>
```
Example:
```
BLUE: DEFENDED;;NORMS:KA-1+KA-13;;STATUS:OK
```

### Judge (JUDGE)
```
JUDGE: GATE:<PASS|DENY>;;FIX_REQ:<action>;;REASON:<string>
```
Example:
```
JUDGE: GATE:DENY;;FIX_REQ:SANITIZE;;REASON:CRITICAL_FLAW_FOUND
```

## Severity Rules

| Severity | Gate Decision | Action |
|----------|---------------|--------|
| CRIT | DENY | Block transition, require fix |
| HIGH | DENY | Block transition, require fix |
| MED | PASS | Log, continue |
| LOW | PASS | Log, continue |

## Phase-Specific Vulnerabilities

| Phase | Expected Vulnerability |
|-------|----------------------|
| P1 | REQ_AMBIGUITY |
| P2 | ARCH_FRAGILITY |
| P3 | DESIGN_COMPLEXITY |
| P4 | IMPL_FEASIBILITY |
| P5 | INJECTION_RISK |
| P6 | ENV_DIVERGENCE |
| P7 | OPS_READINESS |
| P8 | MAINTENANCE_GAPS |

## Anti-Loop Mechanism

### AOV (Act-Observe-Verify) Iterations
- **File**: `.aov_pending`
- **Threshold**: 2 iterations → FAIL
- **Timeout**: 60 seconds
- **Reset**: On successful verification

### Self-Heal Iterations
- **State Path**: `phase_data.P6.heal_iterations`
- **Threshold**: 3 iterations → FAIL
- **Reset**: On successful heal

## Testing

### Smoke Tests (`tests/adversarial-test.sh`)
47 tests covering:
1. phase-guard blocks .py in P1
2. bash-guard blocks printf redirect to src/
3. bash-guard blocks python -c open() to src/
4. dsl_engine preserves pipe in FIX_REQ
5. state_engine atomic lock
6. bash_scanner blocks echo with no-space >
7. adversarial gate denies CRIT
8. aov_iterations increment/reset

### Running Tests
```bash
bash tests/adversarial-test.sh
# Expected: ALL TESTS PASSED - 100% CONFIRMED
```

## DSL Engine Details

### Delimiter
- **Separator**: `;;` (double-semicolon)
- **Preserved**: Pipe `|` in values (e.g., `FIX_REQ:Add WAF | CORS`)

### Normalization
```python
# Strips spaces around ;;
result = re.sub(r' *;; *', ';;', dsl)
```

### Parsing
```python
def parse(normalized):
    # Handles RED:, BLUE:, VULN:, JUDGE: formats
    # Returns dict with keys: TYPE, LOC, VULN, FIX, GATE, etc.
```

## Version

- Current: 1.0.0 (2026-06-01)
