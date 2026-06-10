"""
Adversarial corpus runner for adv-loop.

S4 (2026-06-10) — Corpus-based regression testing for the harness.

The corpus is a JSON file containing attack payloads — inputs designed
to bypass or stress the adv-loop checks. Each case has:
  - id, name, category, phase
  - work_content (the attack payload) or spec_content
  - expected_findings: list of matchers that must be satisfied

The runner executes each case against adv-loop and verifies the
expected findings are detected. This is the harness's own regression
test suite: if a case stops finding what it should, either the
payload is no longer adversarial, or the check is broken.

DSL output (per run):
  corpus:total=60;;
  corpus:passed=58;;
  corpus:failed=2;;
  corpus:by_category=vague:10/10;demarcation:11/11;antipattern:9/10;...;;
  corpus:missed=vague-001:expected MED spec_vague, got LOW spec_vague

Categories covered (v1, 2026-06-10):
  - vague_language        : prose with should/maybe/soon/etc.
  - demarcation_violation : phase N mentions keywords from phase N±1
  - antipattern           : TODO/FIXME/console.log/secrets-in-code
  - missing_section       : required spec sections absent
  - traceability_gap      : RTM without back/forward references
  - nfr_gap               : srs without perf/sec/scalability
  - compliance_gap        : data archival without RGPD/consent
  - council_injection     : prompt-injection payloads
  - edge_case             : empty, unicode, very long lines
"""
import json
import sys
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any


# === Data model ===

@dataclass
class ExpectedFinding:
    """A condition that the adversarial loop output must satisfy."""
    severity_min: Optional[str] = None       # CRIT > HIGH > MED > LOW
    category_contains: Optional[str] = None
    message_contains: Optional[str] = None
    count_min: Optional[int] = None         # at least N findings matching

    def matches(self, finding: Dict) -> bool:
        """Does a single finding satisfy this matcher?"""
        if self.severity_min:
            rank = {"LOW": 1, "MED": 2, "HIGH": 3, "CRIT": 4}
            if rank.get(finding.get("severity", "LOW"), 0) < rank.get(self.severity_min, 0):
                return False
        if self.category_contains:
            if self.category_contains not in finding.get("category", ""):
                return False
        if self.message_contains:
            if self.message_contains not in finding.get("message", ""):
                return False
        return True


@dataclass
class CorpusCase:
    id: str
    name: str
    category: str
    phase: int
    work_content: Optional[str] = None       # work-in-progress file
    spec_content: Optional[str] = None        # spec text override
    expected_findings: List[ExpectedFinding] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class CaseResult:
    case_id: str
    passed: bool
    details: str
    actual_findings: List[Dict] = field(default_factory=list)


@dataclass
class CorpusReport:
    total: int = 0
    passed: int = 0
    failed: int = 0
    by_category: Dict[str, Dict[str, int]] = field(default_factory=dict)
    failures: List[CaseResult] = field(default_factory=list)
    elapsed_s: float = 0.0


# === Corpus loading ===

def load_corpus(corpus_path: str) -> List[CorpusCase]:
    """Load and validate a corpus JSON file."""
    raw = Path(corpus_path).read_text(encoding="utf-8")
    data = json.loads(raw)
    cases = []
    for entry in data.get("cases", []):
        expected = [
            ExpectedFinding(
                severity_min=ef.get("severity_min"),
                category_contains=ef.get("category_contains"),
                message_contains=ef.get("message_contains"),
                count_min=ef.get("count_min"),
            )
            for ef in entry.get("expected_findings", [])
        ]
        cases.append(CorpusCase(
            id=entry["id"],
            name=entry["name"],
            category=entry["category"],
            phase=entry["phase"],
            work_content=entry.get("work_content"),
            spec_content=entry.get("spec_content"),
            expected_findings=expected,
            description=entry.get("description"),
        ))
    return cases


# === DSL parsing — extract findings from adv-loop output ===

SEVERITY_RANK = {"LOW": 1, "MED": 2, "HIGH": 3, "CRIT": 4}
SEVERITY_FROM_KEYS = ["findings_crit", "findings_high", "findings_med", "findings_low"]


def parse_adv_loop_dsl(dsl: str) -> List[Dict]:
    """Extract individual findings from a swebok DSL adv-loop output.

    The DSL is KEY=VALUE;;KEY=VALUE;...;adv_loop:verdict=...
    Findings are aggregated in findings_crit/high/med/low counts.
    We don't have detail per finding from the DSL alone (it's lossy by design),
    so we return synthetic findings for category matching based on known keys.

    For full per-finding detail, run loop_orchestrator.run_phase_adversarial_loop
    in-process and inspect the result.
    """
    out = []
    for piece in dsl.split(";;"):
        if "=" not in piece:
            continue
        k, v = piece.split("=", 1)
        k, v = k.strip(), v.strip()
        if k in SEVERITY_FROM_KEYS:
            count = int(v) if v.isdigit() else 0
            sev = k.replace("findings_", "").upper()
            for i in range(count):
                out.append({"severity": sev, "category": "dsl_aggregate", "message": ""})
        elif k == "council:red_vuln":
            out.append({"severity": v, "category": "council", "message": ""})
        elif k == "council:blue_defended" and v == "FAIL":
            out.append({"severity": "HIGH", "category": "council", "message": "BLUE FAIL"})
    return out


# === Test execution ===

def run_case(case: CorpusCase, project_root: str = ".") -> CaseResult:
    """Run a single corpus case through adv-loop and check expectations."""
    # Import lazily to avoid circular deps and CLI startup cost
    # When run as a module (adv-loop.corpus), use relative import
    try:
        from .loop_orchestrator import _run_loop
    except ImportError:
        from loop_orchestrator import _run_loop
    try:
        from .feedback import FeedforwardResult, FeedbackFinding
    except ImportError:
        from feedback import FeedforwardResult, FeedbackFinding

    # Read the phase spec (from project_root)
    spec_path = Path(project_root) / f"specs/workflows/by-phase/phase-{case.phase}-{_phase_slug(case.phase)}.md"
    if not spec_path.exists():
        # Try a glob as fallback (filenames have varied over time)
        matches = list((Path(project_root) / "specs/workflows/by-phase").glob(f"phase-{case.phase}-*.md"))
        if matches:
            spec_path = matches[0]
        else:
            return CaseResult(case.id, False, f"spec file not found for phase {case.phase}")
    spec_content = case.spec_content or spec_path.read_text(encoding="utf-8", errors="ignore")

    # Run the loop, get BOTH dsl and structured findings
    dsl, findings = _run_loop(
        phase=case.phase,
        spec_content=spec_content,
        work_content=case.work_content or "",
        work_dir=project_root,
        max_iterations=1,
        verbose=False,
        council_dsl="",  # corpus tests use computational checks only
    )
    # Convert structured findings to matcher format
    actual = [
        {
            "severity": f.severity,
            "category": f.category,
            "message": f.message,
        }
        for f in findings
    ]

    # Check each expectation
    missing = []
    for ef in case.expected_findings:
        if ef.count_min is not None:
            matching = [f for f in actual if ef.matches(f)]
            if len(matching) < ef.count_min:
                missing.append(
                    f"count_min={ef.count_min} for category_contains={ef.category_contains}, "
                    f"got {len(matching)} matching"
                )
        else:
            # At least one matching finding
            if not any(ef.matches(f) for f in actual):
                missing.append(
                    f"no finding with severity_min={ef.severity_min} "
                    f"category_contains={ef.category_contains} "
                    f"message_contains={ef.message_contains}"
                )
    if missing:
        return CaseResult(
            case_id=case.id, passed=False,
            details="; ".join(missing),
            actual_findings=actual,
        )
    return CaseResult(case_id=case.id, passed=True, details="all expectations met", actual_findings=actual)


def _phase_slug(phase: int) -> str:
    """Best-effort phase slug for spec filename (varies across versions)."""
    slugs = {
        0: "discovery",
        1: "concept-feasibility",
        2: "requirements",
        3: "architecture",
        4: "design",
        5: "implementation",
        6: "testing",
        7: "deployment",
        8: "operations",
        9: "maintenance",
        10: "retirement",
    }
    return slugs.get(phase, f"phase-{phase}")


def run_corpus(corpus_path: str, project_root: str = ".") -> CorpusReport:
    """Run all cases in a corpus and return a report."""
    cases = load_corpus(corpus_path)
    report = CorpusReport(total=len(cases))
    t0 = time.time()
    for case in cases:
        result = run_case(case, project_root)
        if result.passed:
            report.passed += 1
        else:
            report.failed += 1
            report.failures.append(result)
        # Tally per category
        cat = report.by_category.setdefault(case.category, {"total": 0, "passed": 0})
        cat["total"] += 1
        if result.passed:
            cat["passed"] += 1
    report.elapsed_s = time.time() - t0
    return report


# === Reporting ===

def report_to_dsl(report: CorpusReport) -> str:
    """Format a corpus report as swebok DSL fragment."""
    by_cat = ";".join(
        f"{cat}:{stats['passed']}/{stats['total']}"
        for cat, stats in sorted(report.by_category.items())
    )
    missed = ";".join(
        f"{f.case_id}:{f.details[:80]}" for f in report.failures[:5]
    ) or "none"
    return (
        f"corpus:total={report.total};;"
        f"corpus:passed={report.passed};;"
        f"corpus:failed={report.failed};;"
        f"corpus:by_category={by_cat};;"
        f"corpus:missed={missed};;"
        f"corpus:elapsed_s={report.elapsed_s:.1f}"
    )


def report_to_text(report: CorpusReport) -> str:
    """Human-readable report (for bin/adv-loop corpus)."""
    lines = [
        f"=== Adversarial corpus ===",
        f"Total: {report.total}  Passed: {report.passed}  Failed: {report.failed}  "
        f"Elapsed: {report.elapsed_s:.1f}s",
        "",
        "By category:",
    ]
    for cat, stats in sorted(report.by_category.items()):
        marker = "✓" if stats["passed"] == stats["total"] else "✗"
        lines.append(f"  {marker} {cat:25s} {stats['passed']}/{stats['total']}")
    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for f in report.failures[:10]:
            lines.append(f"  ✗ {f.case_id}: {f.details[:120]}")
        if len(report.failures) > 10:
            lines.append(f"  ... and {len(report.failures) - 10} more")
    return "\n".join(lines)


if __name__ == "__main__":
    # CLI: python3 -m adv-loop.corpus <corpus.json>
    if len(sys.argv) < 2:
        print("Usage: python3 -m adv-loop.corpus <corpus.json>")
        sys.exit(1)
    report = run_corpus(sys.argv[1])
    print(report_to_text(report))
    print()
    print(report_to_dsl(report))
    sys.exit(0 if report.failed == 0 else 1)
