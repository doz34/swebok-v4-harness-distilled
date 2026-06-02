# SWEBOK v4 Harness - DSL Specification

## Overview

The SWEBOK v4 Harness uses a strict Domain Specific Language (DSL) with `;;` (double-semicolon) delimiter for all structured output. This ensures parseable, machine-readable logs and gate decisions.

## Delimiter Rule

**CRITICAL**: Use `;;` as delimiter. NEVER use `|` as delimiter. Pipe `|` is preserved WITHIN values (e.g., `FIX_REQ:Add WAF | CORS`).

## DSL Format

### Attack (RED Team)

```
RED: VULN:<severity>;;LOC:<location>;;TYPE:<vulnerability_type>;;FIX_REQ:<fix_requirement>
```

**Example**:
```
RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION;;FIX_REQ:SANITIZE_ALL_INPUTS
```

### Defense (BLUE Team)

```
BLUE: DEFENDED;;NORMS:<ka_numbers>;;STATUS:<ok|failed>
```

**Example**:
```
BLUE: DEFENDED;;NORMS:KA-1+KA-13;;STATUS:OK
```

### Judge (Decision)

```
JUDGE: GATE:<PASS|DENY>;;FIX_REQ:<action>;;REASON:<string>
```

**Example**:
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

## DSL Keywords (Authoritative Set)

The full keyword vocabulary used across the harness. The parser accepts
only keys from this set; unknown keys produce a `DSL_FORMAT_ERROR`.

| Keyword | Type | Used in | Example |
|---------|------|---------|---------|
| `RED` | role prefix | attack verdict | `RED: VULN:CRIT` |
| `BLUE` | role prefix | defense verdict | `BLUE: DEFENDED` |
| `JUDGE` | role prefix | gate decision | `JUDGE: GATE:PASS` |
| `AOV` | role prefix | act-observe-verify | `AOV:PASS` |
| `HEAL` | role prefix | self-heal | `HEAL:PASS` |
| `VULN` | field | attack severity | `VULN:HIGH` |
| `LOC` | field | attack location | `LOC:USER_INPUT` |
| `TYPE` | field | attack category | `TYPE:INJECTION` |
| `FIX_REQ` | field | required fix | `FIX_REQ:SANITIZE` |
| `NORMS` | field | SWEBOK KA refs | `NORMS:KA-1+KA-13` |
| `STATUS` | field | defense status | `STATUS:OK` |
| `GATE` | field | gate decision (PASS\|DENY) | `GATE:PASS` |
| `REASON` | field | rationale | `REASON:CRITICAL_FLAW_FOUND` |
| `ITERATIONS` | field | anti-loop counter | `ITERATIONS:2` |

## DSL Engine (`scripts/lib/dsl_engine.py`)

### Normalization

```python
def normalize(dsl: str) -> str:
    """Normalize DSL: strip spaces around ;; delimiter."""
    result = re.sub(r' *;; *', ';;', dsl)
    return result
```

### Parsing

```python
def parse(normalized: str) -> dict:
    """Parse normalized DSL and return dict with TYPE, LOC, VULN, FIX fields."""
```

### Validation

```python
def validate(normalized: str) -> bool:
    """Validate DSL format. Returns True if valid."""
    if not re.search(r'GATE', normalized, re.IGNORECASE):
        return False
    return True
```

## Anti-Loop DSL

### Act-Observe-Verify (AOV)

```
AOV:PASS;;ITERATIONS:1
AOV:FAIL;;REASON:MAX_MCP_RETRIES
```

### Self-Heal

```
HEAL:PASS;;ITERATIONS:2
HEAL:FAIL;;REASON:INFINITE_LOOP_DETECTED
```

## Pipe Preservation

**CRITICAL**: Pipe `|` within values must be preserved, not treated as delimiter.

**Correct**:
```
RED: VULN:HIGH;;LOC:API_SURFACE;;TYPE:BROKEN_AUTH;;FIX_REQ:Add JWT | OAuth2
```

**Wrong** (using pipe as delimiter):
```
RED: VULN:HIGH | LOC:API_SURFACE | TYPE:BROKEN_AUTH | FIX_REQ:Add JWT
```

## Usage in Scripts

### Python
```python
from scripts.lib.dsl_engine import parse, normalize

dsl_input = "RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION"
normalized = normalize(dsl_input)
result = parse(normalized)
print(result)  # {'TYPE': 'INJECTION', 'LOC': 'USER_INPUT', 'VULN': 'CRIT', 'FIX': 'NONE'}
```

### Bash
```bash
# Use state_engine.py for DSL operations in bash
python3 scripts/lib/state_engine.py get phase_data
```
normalized=$(normalize_dsl "$dsl_input")
gate=$(parse_gate "$normalized")
echo "Gate: $gate"  # Gate: OK
```

## Version

- Current: 1.4.1 (2026-06-01)
- Changed: Audit fixes - added AOV/HEAL formats, removed dead dsl_parser.sh reference