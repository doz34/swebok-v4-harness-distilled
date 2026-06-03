#!/usr/bin/env python3
# SWEBOK v4 Harness - DSL Engine
# Strict double-semicolon ;; delimiter parsing

import re
import sys


def normalize(dsl: str) -> str:
    """Normalize DSL: strip spaces around ;; delimiter and : key:value separator."""
    if not dsl:
        return ""
    # Replace " ;; " with ";;" (strip spaces around double-semicolon delimiter)
    result = re.sub(r' *;; *', ';;', dsl)
    # Normalize spaces around : in key:value pairs (but preserve | within values)
    # Match KEY followed by optional spaces, colon, optional spaces, then value
    # Be careful to not affect pipes within values
    result = re.sub(r'([A-Za-z_]+)\s*:\s*', r'\1:', result)
    return result


def parse_gate(normalized: str) -> str:
    """Extract GATE status from normalized DSL."""
    if not normalized:
        return ""

    # Try GATE: pattern
    match = re.search(r'GATE:?([A-Z]+)', normalized, re.IGNORECASE)
    if match:
        return match.group(1).upper()

    # Try PASS/DENY directly
    if re.search(r'\bPASS\b', normalized, re.IGNORECASE):
        return "PASS"
    if re.search(r'\bDENY\b', normalized, re.IGNORECASE):
        return "DENY"

    return ""


def parse_fix_req(normalized: str) -> str:
    """Extract FIX_REQ value - get value between FIX_REQ: and next ;; or end.

    Returns the cleaned value, or "" if absent or empty.
    v1.5.7: unified regex `[^;;]+` (1+ chars) across parse and validate.
    Previously validate() used `[^;;]*` which silently accepted empty values;
    a malicious DSL `FIX_REQ:;;LOC:foo` would pass validate and emit an
    empty FIX_REQ field. Now both paths require a non-empty value.
    """
    if not normalized:
        return ""

    # Match FIX_REQ: followed by 1+ chars up to next ;;
    match = re.search(r'FIX_REQ:([^;;]+)', normalized, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    # Also accept FIX: prefix
    match = re.search(r'FIX:([^;;]+)', normalized, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return ""


def validate(normalized: str) -> bool:
    """Validate DSL format. Returns True if valid.

    v1.4.1 hardening (H9): a bare 'GATE' keyword with no value is
    rejected — callers must emit GATE:PASS or GATE:DENY (case-insensitive).
    """
    if not normalized:
        return False

    # Check for required format elements
    if not re.search(r'GATE', normalized, re.IGNORECASE):
        return False

    # FAIL-SECURE (H9): a bare GATE (no colon, no value) is not a
    # valid verdict. Require GATE:(PASS|DENY) case-insensitive.
    bare_gate = re.search(r'(?<!:)\bGATE\b(?!:)', normalized, re.IGNORECASE)
    if bare_gate:
        # Make sure it's not part of GATE:PASS / GATE:DENY by checking
        # the next non-space char isn't ':'.
        idx = bare_gate.end()
        tail = normalized[idx:idx + 1]
        if tail != ':':
            return False

    # Validate GATE has proper value (PASS or DENY)
    gate_match = re.search(r'GATE:([A-Z]+)', normalized, re.IGNORECASE)
    if gate_match:
        gate_value = gate_match.group(1).upper()
        if gate_value not in ('PASS', 'DENY'):
            return False

    # Validate FIX_REQ is not empty when present.
    # v1.5.7: regex unified with parse_fix_req (both use `[^;;]+` — 1+ chars).
    # An empty value is impossible because `[^;;]+` requires 1+ chars; the
    # match itself is the presence test. We do NOT need a separate empty-
    # value check (which used to live in the `if fix_value == '': return False`
    # block before v1.5.7).
    if not re.search(r'FIX_REQ:([^;;]+)', normalized, re.IGNORECASE):
        return False

    # Validate REASON is not empty when present
    reason_match = re.search(r'REASON:([^;;]*)', normalized, re.IGNORECASE)
    if reason_match:
        reason_value = reason_match.group(1).strip()
        if reason_value == '':
            return False

    return True


def _is_empty_field(match) -> bool:
    """Check if a regex match group value is empty or whitespace-only."""
    return match is None or not match.group(1).strip()


def parse(normalized: str) -> dict:
    """Parse normalized DSL and return dict with TYPE, LOC, VULN, FIX fields.
    FAIL-SECURE: Returns error dict if critical fields are missing or empty."""

    # Handle RED: attack lines
    if normalized.upper().startswith('RED:'):
        vuln_match = re.search(r'VULN:([^;;]*)', normalized, re.IGNORECASE)
        loc_match = re.search(r'LOC:([^;;]*)', normalized, re.IGNORECASE)
        type_match = re.search(r'TYPE:([^;;]*)', normalized, re.IGNORECASE)
        fix_match = re.search(r'FIX_REQ:([^;;]+)', normalized, re.IGNORECASE)
        if not fix_match:
            fix_match = re.search(r'FIX:([^;;]+)', normalized, re.IGNORECASE)

        # FAIL-SECURE: VULN is critical and must not be empty
        if vuln_match is None or not vuln_match.group(1).strip():
            return {"error": "DSL_FORMAT_ERROR: VULN critical field missing or empty"}
        # FAIL-SECURE: LOC is critical and must not be empty
        if loc_match is None or not loc_match.group(1).strip():
            return {"error": "DSL_FORMAT_ERROR: LOC critical field missing or empty"}
        # FAIL-SECURE: TYPE is critical and must not be empty
        if type_match is None or not type_match.group(1).strip():
            return {"error": "DSL_FORMAT_ERROR: TYPE critical field missing or empty"}

        return {
            "TYPE": type_match.group(1).strip(),
            "LOC": loc_match.group(1).strip(),
            "VULN": vuln_match.group(1).strip(),
            "FIX": fix_match.group(1).strip() if fix_match else "NONE"
        }

    # Handle BLUE: defense lines
    if normalized.upper().startswith('BLUE:'):
        status_match = re.search(r'STATUS:([^;;]+)', normalized, re.IGNORECASE)
        norms_match = re.search(r'NORMS:([^;;]*)', normalized, re.IGNORECASE)

        # FAIL-SECURE: STATUS is critical
        if status_match is None or not status_match.group(1).strip():
            return {"error": "DSL_FORMAT_ERROR: STATUS critical field missing or empty"}

        return {
            "DEFENDED": "TRUE",
            "NORMS": norms_match.group(1).strip() if norms_match else "NONE",
            "STATUS": status_match.group(1).strip()
        }

    # Handle VULN: without RED: prefix
    if re.search(r'^VULN:', normalized, re.IGNORECASE):
        vuln_match = re.search(r'VULN:([^;;]*)', normalized, re.IGNORECASE)
        loc_match = re.search(r'LOC:([^;;]*)', normalized, re.IGNORECASE)
        type_match = re.search(r'TYPE:([^;;]*)', normalized, re.IGNORECASE)
        fix_match = re.search(r'FIX_REQ:([^;;]+)', normalized, re.IGNORECASE)

        # FAIL-SECURE: VULN critical field check
        if vuln_match is None or not vuln_match.group(1).strip():
            return {"error": "DSL_FORMAT_ERROR: VULN critical field missing or empty"}
        if loc_match is None or not loc_match.group(1).strip():
            return {"error": "DSL_FORMAT_ERROR: LOC critical field missing or empty"}
        if type_match is None or not type_match.group(1).strip():
            return {"error": "DSL_FORMAT_ERROR: TYPE critical field missing or empty"}

        return {
            "TYPE": type_match.group(1).strip(),
            "LOC": loc_match.group(1).strip(),
            "VULN": vuln_match.group(1).strip(),
            "FIX": fix_match.group(1).strip() if fix_match else "NONE"
        }

    # Handle JUDGE:GATE:PASS/DENY lines
    gate_status = parse_gate(normalized)
    fix_req = parse_fix_req(normalized)

    if not gate_status:
        return {"error": f"DSL_FORMAT_ERROR: GATE critical field missing or empty"}

    reason_match = re.search(r'REASON:([^;;]+)', normalized, re.IGNORECASE)
    reason = reason_match.group(1).strip() if reason_match else "NONE"

    return {
        "GATE": gate_status,
        "FIX_REQ": fix_req if fix_req else "NONE",
        "REASON": reason
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: dsl_engine.py <command> [args]")
        print("Commands: normalize <dsl> | parse_gate <dsl> | parse_fix_req <dsl> | validate <dsl> | parse <dsl>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "normalize":
        if len(sys.argv) < 3:
            print("Usage: dsl_engine.py normalize <dsl>")
            sys.exit(1)
        print(normalize(sys.argv[2]))
    elif cmd == "parse_gate":
        if len(sys.argv) < 3:
            print("Usage: dsl_engine.py parse_gate <dsl>")
            sys.exit(1)
        print(parse_gate(normalize(sys.argv[2])))
    elif cmd == "parse_fix_req":
        if len(sys.argv) < 3:
            print("Usage: dsl_engine.py parse_fix_req <dsl>")
            sys.exit(1)
        print(parse_fix_req(normalize(sys.argv[2])))
    elif cmd == "validate":
        if len(sys.argv) < 3:
            print("Usage: dsl_engine.py validate <dsl>")
            sys.exit(1)
        result = validate(normalize(sys.argv[2]))
        print("VALID" if result else "INVALID")
    elif cmd == "parse":
        if len(sys.argv) < 3:
            print("Usage: dsl_engine.py parse <dsl>")
            sys.exit(1)
        result = parse(normalize(sys.argv[2]))
        for k, v in result.items():
            print(f"{k}:{v}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()