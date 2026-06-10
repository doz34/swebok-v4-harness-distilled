"""
Adversarial loop orchestrator.
Per Fowler "Harness engineering" + dev.to "Adversarial Planning":
- 3 phases per phase boundary: entry → in-loop → exit
- Each phase has feedforward (guides) + feedback (sensors)
- Stop conditions are mechanical (time, tokens, value)
- DSL output for swebok audit trail
- No Docker, no external deps — pure Python stdlib

Output: KEY:VALUE;;KEY:VALUE (swebok DSL)
"""
from pathlib import Path
from typing import List, Optional
import sys

# Make adv_loop importable
_ADV_DIR = Path(__file__).parent
if str(_ADV_DIR) not in sys.path:
    sys.path.insert(0, str(_ADV_DIR))

from stop_conditions import (
    StopState, AdversarialFinding
)
from feedback import (
    FeedforwardResult, check_phase_feedforwards, check_demarcation,
    PHASE_FEEDFORWARDS,
)
from feedback import (
    FeedbackFinding, lint_spec_vagueness, lint_required_sections,
    lint_cross_phase_consistency, lint_dsl_format,
    run_all_feedback_sensors,
)


def severity_from_findings(findings: List) -> str:
    """Map a list of findings (Feedforward or Feedback) to highest severity."""
    rank = {"LOW": 1, "MED": 2, "HIGH": 3, "CRIT": 4}
    if not findings:
        return "LOW"
    return max(findings, key=lambda f: rank.get(f.severity, 0)).severity


def run_phase_adversarial_loop(
    phase: int,
    spec_content: str,
    work_content: str = "",
    work_dir: str = ".",
    max_iterations: int = 3,
    verbose: bool = False,
) -> str:
    """Run the full adversarial loop for a phase.
    Returns swebok DSL output (KEY:VALUE;;KEY:VALUE).

    Algorithm:
    1. Run feedforward controls (guides) — pre-check spec & work
    2. Run feedback sensors (sensors) — post-check content
    3. Aggregate findings, apply stop conditions
    4. If stop condition met, exit; else iterate (with bounded pressure)
    """
    if phase not in PHASE_FEEDFORWARDS:
        return f"adv_loop:error=unknown_phase_{phase};;adv_loop:verdict=🔴"

    stop = StopState(max_iterations=max_iterations)
    all_findings: List[AdversarialFinding] = []

    # 1. Feedforward (guides) — pre-phase
    ff_results = check_phase_feedforwards(phase, work_dir)
    if work_content:
        demarcation = check_demarcation(phase, work_content)
        ff_results.extend(demarcation)
    ff_severity = severity_from_findings(ff_results)
    if verbose:
        for r in ff_results:
            print(f"[feedforward] {r.severity}: {r.control_name} — {r.message}")

    # 2. Feedback (sensors) — post-phase
    fb_findings = run_all_feedback_sensors(phase, spec_content)
    fb_severity = severity_from_findings(fb_findings)
    if verbose:
        for f in fb_findings:
            print(f"[feedback] {f.severity}: {f.sensor_name} — {f.message}")

    # 3. Combine into AdversarialFinding list (normalized)
    for r in ff_results:
        all_findings.append(AdversarialFinding(
            severity=r.severity,
            category=f"feedforward:{r.control_name}",
            message=r.message,
            fix_suggestion=r.fix_suggestion,
        ))
    for f in fb_findings:
        all_findings.append(AdversarialFinding(
            severity=f.severity,
            category=f"feedback:{f.sensor_name}",
            message=f.message,
            fix_suggestion=f.fix_suggestion,
        ))

    # 4. Add findings to stop state and check stop
    for finding in all_findings:
        stop.add_finding(finding)
        stop_reason = stop.check_stop()
        if stop_reason:
            if verbose:
                print(f"[stop] {stop_reason}")
            break

    # 5. Emit DSL
    return stop.to_dsl() + f";;adv_loop:verdict={stop.verdict()}"


def run_phase_adversarial_loop_from_files(
    phase: int,
    spec_path: str,
    work_path: Optional[str] = None,
    work_dir: str = ".",
) -> str:
    """Convenience: read files, run loop."""
    spec_content = Path(spec_path).read_text(encoding="utf-8", errors="ignore")
    work_content = ""
    if work_path:
        work_content = Path(work_path).read_text(encoding="utf-8", errors="ignore")
    return run_phase_adversarial_loop(
        phase=phase,
        spec_content=spec_content,
        work_content=work_content,
        work_dir=work_dir,
    )


if __name__ == "__main__":
    # CLI: python3 -m adv-loop.loop_orchestrator <phase> <spec_path> [work_path]
    if len(sys.argv) < 3:
        print("Usage: python3 -m adv-loop.loop_orchestrator <phase> <spec_path> [work_path]")
        sys.exit(1)
    phase = int(sys.argv[1])
    spec = sys.argv[2]
    work = sys.argv[3] if len(sys.argv) > 3 else None
    result = run_phase_adversarial_loop_from_files(phase, spec, work)
    print(result)
