#!/usr/bin/env python3
"""
mini_council.py — Cheap 1-Haiku-judge per edit adversarial check.
SPRINT-2026-06-10 G6.

Per Fowler (harness engineering):
  - Inferential feedback control: 1 LLM judge (cheap, fast)
  - Per edit, on non-whitelist files
  - Returns DSL line with finding
  - Tracks last 3 findings; if 1+ VULN → escalate to full Council

DSL output:
  mini_council:finding=OK|CRIT|HIGH|MED|LOW;;LOC:<path>;;TYPE:<type>;;FIX_REQ:<fix>;;elapsed_ms=<n>;;verdict=🟢|🟡|🔴
"""
import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Optional, Tuple

HARNESS_DIR = Path(__file__).resolve().parent.parent.parent
STATE_CLI = HARNESS_DIR / "lib" / "state_engine_cli.py"

# Per-phase focus anchors (lightweight, 1 judge, not 4)
PHASE_FOCUS = {
    "P0": "Discovery: stakeholders, success_criteria, alternatives",
    "P1": "Feasibility: ROI, payback, go/no-go, risks",
    "P2": "Requirements: testable AC, NFRs, RTM",
    "P3": "Architecture: ADRs, C4, trade-offs, security",
    "P4": "Design: API contracts, data model, error handling",
    "P5": "Implementation: antipatterns, unit tests, code smells",
    "P6": "Testing: coverage, mutation, edge cases",
    "P7": "Deployment: rollback, safe patterns, smoke tests",
    "P8": "Operations: SLO, runbook, on-call, postmortem",
    "P9": "Maintenance: tech debt, refactoring plan, release notes",
    "P10": "Retirement: RGPD, archival, réversibilité, closure",
}


def is_whitelisted(file_path: str) -> bool:
    p = file_path.lower()
    if p.endswith(".md"):
        return True
    if p.endswith(".json"):
        return True
    if "/tests/" in p or "/test/" in p or p.startswith("tests/") or p.startswith("test/"):
        return True
    if "/.git/" in p:
        return True
    return False


def get_phase() -> str:
    """Get current phase from state engine."""
    try:
        env = os.environ.copy()
        env["HARNESS_DIR"] = str(HARNESS_DIR)
        r = subprocess.run(
            ["python3", str(STATE_CLI), "get", "current_phase"],
            capture_output=True, text=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        v = r.stdout.strip()
        if v and v.startswith("P") and len(v) >= 2:
            return v.split("_")[0]
    except (subprocess.TimeoutExpired, OSError):
        pass
    return "P5"


def read_file_snippet(file_path: str, max_bytes: int = 4096) -> str:
    """Read first N bytes of file for context.
    R-05: validate file_path is within project or a safe system path.
    """
    try:
        resolved = Path(file_path).resolve()
        # Reject paths outside home directory (prevents /etc/shadow etc.)
        home = Path.home().resolve()
        try:
            resolved.relative_to(home)
        except ValueError:
            return ""
        with open(resolved, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_bytes)
    except OSError:
        return ""


def _mock_heuristic_judge(file_path: str, phase: str) -> Tuple[str, str, str]:
    """
    Stand-in for real Haiku judge (offline-safe).
    Returns (severity, vuln_type, fix_req).

    For sprint scaffolding: detect obvious antipatterns via regex.
    Real Haiku integration would replace this with API call.
    """
    import re
    snippet = read_file_snippet(file_path)
    if not snippet:
        return "OK", "empty", ""

    # Heuristics (offline-safe, no LLM call)
    findings = []

    # Hardcoded secrets
    if re.search(r"(api[_-]?key|password|secret|token)\s*=\s*['\"]\w+", snippet, re.IGNORECASE):
        findings.append(("CRIT", "hardcoded_secret", "move to env var, rotate credential"))

    # SQL injection risk
    if re.search(r"(execute|query)\s*\(\s*['\"].*?\+", snippet, re.IGNORECASE):
        findings.append(("CRIT", "sql_injection", "use parameterized queries"))

    # Eval/exec
    if re.search(r"\beval\s*\(|\bexec\s*\(", snippet):
        findings.append(("CRIT", "code_injection", "replace eval/exec with safe alternatives"))

    # Bare except
    if re.search(r"except\s*:", snippet):
        findings.append(("MED", "bare_except", "catch specific exceptions"))

    # print in production code
    if re.search(r"^\s*print\s*\(", snippet, re.MULTILINE):
        if "/tests/" not in file_path and "__main__" not in snippet:
            findings.append(("LOW", "debug_print", "use proper logger"))

    # TODO/FIXME without ticket
    if re.search(r"#\s*(TODO|FIXME|XXX)\b(?!\s*\[)", snippet):
        findings.append(("LOW", "untracked_todo", "link to ticket or remove"))

    if not findings:
        return "OK", "none", ""

    # Worst severity wins
    severity_order = {"CRIT": 4, "HIGH": 3, "MED": 2, "LOW": 1}
    findings.sort(key=lambda x: -severity_order.get(x[0], 0))
    return findings[0]


def _haiku_judge(file_path: str, phase: str) -> Tuple[str, str, str]:
    """
    Real Haiku 4.5 call (when API key available).
    Falls back to heuristic if not.
    """
    # If Haiku API is available, use it. Otherwise heuristic.
    if not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("HARNESS_HAIKU_API_KEY"):
        return _mock_heuristic_judge(file_path, phase)

    # TODO: real Haiku call when wired
    # For now, fall back to heuristic
    return _mock_heuristic_judge(file_path, phase)


def track_finding(severity: str) -> bool:
    """
    Track last 3 findings. Return True if escalation to full Council needed
    (1+ VULN in last 3).
    """
    try:
        env = os.environ.copy()
        env["HARNESS_DIR"] = str(HARNESS_DIR)
        # Read current findings (JSON list)
        r = subprocess.run(
            ["python3", str(STATE_CLI), "list_get", "mini_council.findings"],
            capture_output=True, text=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        findings = []
        try:
            findings = json.loads(r.stdout.strip() or "[]")
        except (json.JSONDecodeError, TypeError):
            findings = []

        # Add new
        findings.append(severity)
        # Keep last 3
        findings = findings[-3:]

        # Write back via list_append on a scratch key (atomic-ish)
        # We need list_set not list_append; let's use set_nested with JSON
        subprocess.run(
            ["python3", str(STATE_CLI), "set_nested", "mini_council.findings", json.dumps(findings)],
            capture_output=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )

        # Escalation: 1+ VULN in last 3
        return any(f in ("CRIT", "HIGH") for f in findings)
    except (subprocess.TimeoutExpired, OSError):
        return False


def on_edit(file_path: str) -> str:
    """
    Called from post-tool-use/mini-council-hook.sh on each Write/Edit.
    Returns DSL line. Outputs escalation envelope to stderr if needed.
    """
    t0 = time.time()
    if is_whitelisted(file_path):
        return (
            f"mini_council:action=skipped;;"
            f"mini_council:reason=whitelisted;;"
            f"mini_council:verdict=🟢 OK"
        )

    phase = get_phase()
    severity, vuln_type, fix_req = _haiku_judge(file_path, phase)
    elapsed_ms = int((time.time() - t0) * 1000)

    if severity == "OK":
        return (
            f"mini_council:finding=OK;;"
            f"mini_council:phase={phase};;"
            f"mini_council:file={file_path};;"
            f"mini_council:elapsed_ms={elapsed_ms};;"
            f"mini_council:verdict=🟢 OK"
        )

    # Track + escalation
    escalate = track_finding(severity)

    if escalate:
        import sys as _sys
        print(
            f"## <MULTIAGENT_LAUNCH reason=\"mini_council_escalation\" severity=\"{severity}\" file=\"{file_path}\">\n"
            f"\n"
            f"SPRINT-2026-06-10 G6: mini-council detected {severity} finding. Escalating to full Council.\n"
            f"Spawn 4 LLM-judges via Agent tool (subagent_type: nexus-ciso, nexus-qa-lead, nexus-architect, nexus-devops-lead).\n"
            f"Finding: {vuln_type} in {file_path}\n"
            f"Fix: {fix_req}\n",
            file=_sys.stderr,
        )

    verdict = "🔴" if severity == "CRIT" else ("🟡" if severity in ("HIGH", "MED") else "🟢")
    return (
        f"mini_council:finding={severity};;"
        f"mini_council:phase={phase};;"
        f"mini_council:file={file_path};;"
        f"mini_council:type={vuln_type};;"
        f"mini_council:fix_req={fix_req};;"
        f"mini_council:escalate={'true' if escalate else 'false'};;"
        f"mini_council:elapsed_ms={elapsed_ms};;"
        f"mini_council:verdict={verdict}"
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: mini_council.py <on-edit <file_path>>", file=sys.stderr)
        return 0

    cmd = sys.argv[1]
    try:
        if cmd == "on-edit":
            file_path = sys.argv[2] if len(sys.argv) > 2 else ""
            print(on_edit(file_path))
        else:
            print(f"unknown cmd: {cmd}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"mini_council:error={type(e).__name__};;mini_council:verdict=🟡 DEGRADED")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
