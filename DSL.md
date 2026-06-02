# SWEBOK v4 Harness - DSL Specification

## Overview
The Domain Specific Language uses `;;` as delimiter to separate fields. Pipe `|` is preserved inside values.

## DSL Format

### 1. GATE (Phase Transition)
```
GATE:<PASS|DENY>;;FIX_REQ:<action>;;REASON:<string>
```
Example:
```
GATE:PASS;;FIX_REQ:NONE;;REASON:NO_CRITICAL_FLAWS
```

### 2. RED (Attack/Vulnerability)
```
RED: VULN:<severity>;;LOC:<location>;;TYPE:<vulnerability_type>;;FIX_REQ:<fix>
```
Example:
```
RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION;;FIX_REQ:SANITIZE_ALL_INPUTS
```

### 3. BLUE (Defense/Verification)
```
BLUE: DEFENDED;;NORMS:<ka_numbers>;;STATUS:<ok|failed>
```
Example:
```
BLUE: DEFENDED;;NORMS:KA-1+KA-13;;STATUS:OK
```

### 4. JUDGE (Gate Decision)
```
JUDGE: GATE:<PASS|DENY>;;FIX_REQ:<action>;;REASON:<string>
```
Example:
```
JUDGE: GATE:DENY;;FIX_REQ:SANITIZE;;REASON:CRITICAL_FLAW_FOUND
```

## Delimiter Rules
- **Field separator**: `;;` (double-semicolon)
- **Space handling**: Spaces around `;;` are stripped during normalization
- **Pipe preservation**: Pipe `|` inside values is NOT treated as delimiter
  - Example: `FIX_REQ:Add WAF | CORS` → fix = "Add WAF | CORS"

## Severity Levels
| Level | Gate |
|-------|------|
| CRIT | DENY |
| HIGH | DENY |
| MED | PASS |
| LOW | PASS |

## DSL Engine API

```python
from lib.dsl_engine import normalize, parse_gate, parse_fix_req, parse, validate

# Normalize: strip spaces around ;;
normalized = normalize("GATE:PASS ;; FIX_REQ:NONE")

# Parse gate status
gate = parse_gate("GATE:PASS;;FIX_REQ:NONE")
# Returns: "PASS"

# Parse fix requirement (preserves pipe)
fix = parse_fix_req("FIX_REQ:Add WAF | CORS")
# Returns: "Add WAF | CORS"

# Full parse
result = parse("RED: VULN:CRIT;;LOC:USER_INPUT;;TYPE:INJECTION")
# Returns: {"TYPE": "INJECTION", "LOC": "USER_INPUT", "VULN": "CRIT", "FIX": "NONE"}
```

## Anti-Patterns (DSL)
- ❌ Using `|` instead of `;;` (pipe is data, not separator)
- ❌ Natural language in GATE output (use DSL dict only)
- ❌ Missing GATE keyword (validation fails)

## Version
- Current: 1.4.1 (2026-06-01)
- See: docs/v1/VERSION
