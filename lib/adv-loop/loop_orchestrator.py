"""
Adversarial loop orchestrator.
Per Fowler "Harness engineering" + dev.to "Adversarial Planning":
- 3 phases per phase boundary: entry → in-loop → exit
- Each phase has feedforward (guides) + feedback (sensors)
- Stop conditions are mechanical (time, tokens, value)
- DSL output for swebok audit trail
- No Docker, no external deps — pure Python stdlib

S2 (2026-06-10) — Council Bridge:
- Add --council flag to spawn 4 LLM-judge agents (ciso, qa-lead, architect, devops-lead)
- Add --verify-result <path> flag to ingest aggregated DSL and finalize verdict
- Output: KEY:VALUE;;KEY:VALUE (swebok DSL)
"""
from pathlib import Path
from typing import List, Optional, Tuple
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
from council import (
    emit_council_envelope,
    load_verify_result,
    aggregate_council_results,
    council_severity_to_dsl,
)
from steering import (
    log_run as steering_log_run,
    get_steering_summary,
    steering_dsl,
    FindingRecord,
    RunRecord,
    default_db_path as steering_db_path,
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
    council_dsl: str = "",
) -> str:
    """Run the full adversarial loop for a phase.
    Returns swebok DSL output (KEY:VALUE;;KEY:VALUE).
    """
    return _run_loop(phase, spec_content, work_content, work_dir,
                     max_iterations, verbose, council_dsl)[0]


def _run_loop(
    phase: int,
    spec_content: str,
    work_content: str = "",
    work_dir: str = ".",
    max_iterations: int = 3,
    verbose: bool = False,
    council_dsl: str = "",
) -> Tuple[str, List[AdversarialFinding]]:
    """Internal: returns (dsl_string, structured_findings) for downstream use.

    Algorithm:
    1. Run feedforward controls (guides) — pre-check spec & work
    2. Run feedback sensors (sensors) — post-check content
    3. Aggregate findings, apply stop conditions
    4. (Optional) If council_dsl is provided, integrate council verdict
    5. Emit DSL + return findings for the corpus / steering

    The S4 corpus needs structured findings (with category and message),
    which the DSL output cannot carry (lossy by design).
    """
    if phase not in PHASE_FEEDFORWARDS:
        return (
            f"adv_loop:error=unknown_phase_{phase};;adv_loop:verdict=🔴",
            [],
        )
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
    # S4 fix: lint BOTH spec_content and work_content. Previously only the
    # spec was checked — a work artefact full of "should/maybe/TBD" was
    # never caught. The corpus exposed this gap.
    fb_findings = run_all_feedback_sensors(phase, spec_content)
    if work_content:
        work_findings = run_all_feedback_sensors(phase, work_content)
        fb_findings.extend(work_findings)
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

    # 4. S4 fix: add all findings from this pass, then check stop ONCE
    # (per pass). Previously the loop broke on the first stop reason during
    # the pass, which truncated findings before the corpus / steering could
    # see them. Now: 1 run_phase_adversarial_loop = 1 pass = all findings.
    # Stop applies between passes (handled at call site, not here).
    for finding in all_findings:
        stop.add_finding(finding)
    if verbose and all_findings:
        print(f"[pass] collected {len(all_findings)} findings")

    # 5. Build base DSL
    base_dsl = stop.to_dsl()

    # 6. Integrate council verdict if provided (S2)
    council_fragment = ""
    if council_dsl:
        try:
            import json as _json
            payload = _json.loads(council_dsl)
            red_lines = payload.get("red_lines", [])
            blue_lines = payload.get("blue_lines", [])
            agg = aggregate_council_results(red_lines, blue_lines)
            council_fragment = council_severity_to_dsl(agg)
            # Council severity can raise the overall verdict
            stop.add_finding(AdversarialFinding(
                severity=agg["council_severity"],
                category="council",
                message=f"Council verdict: {agg['council_severity']} "
                        f"(RED={agg['red_count']}, BLUE={agg['blue_count']})",
                fix_suggestion=None,
            ))
        except (KeyError, AttributeError, TypeError, ValueError, IndexError, ImportError) as e:
            council_fragment = f"council:error={e};;council:severity=LOW"

    # 7. Steering loop persistence (S3) — log this run, detect patterns
    steering_fragment = ""
    try:
        # Build finding records
        finding_records = [
            FindingRecord(
                severity=f.severity,
                category=f.category,
                message=f.message,
                line_ref=getattr(f, "line_ref", None),
                fix_suggestion=f.fix_suggestion,
            )
            for f in all_findings
        ] + ([FindingRecord(
            severity=agg.get("council_severity", "LOW"),
            category="council",
            message=f"Council verdict: {agg.get('council_severity', 'LOW')}",
        )] if council_dsl and "agg" in locals() else [])

        run_rec = RunRecord(
            phase=phase,
            spec_path="(in-process)",  # not available here; CLI logs with real path
            work_path=work_dir,
            verdict=stop.verdict(),
            findings=finding_records,
            council_severity=agg.get("council_severity") if council_dsl and "agg" in locals() else None,
            dsl=base_dsl,
        )
        steering_log_run(steering_db_path(work_dir), run_rec)
        summary = get_steering_summary(steering_db_path(work_dir), phase, threshold=3, last_n=10)
        steering_fragment = steering_dsl(summary)
    except (KeyError, AttributeError, TypeError, ValueError, IndexError, OSError, ImportError) as e:
        steering_fragment = f"steering:error={e}"

    final_verdict = stop.verdict()
    out = base_dsl
    if council_fragment:
        out += ";;" + council_fragment
    if steering_fragment:
        out += ";;" + steering_fragment
    out += f";;adv_loop:verdict={final_verdict}"
    return out, all_findings


def emit_council_envelope_and_signal(phase: int, spec_path: str, work_path: str = "") -> str:
    """Emit the <MULTIAGENT_LAUNCH> envelope and return signal code 99.

    The orchestrator caller (bin/adv-loop) should print the envelope
    and exit 99 to signal the dispatcher to spawn agents and re-invoke.
    """
    return emit_council_envelope(phase, spec_path, work_path)


def run_phase_adversarial_loop_from_files(
    phase: int,
    spec_path: str,
    work_path: Optional[str] = None,
    work_dir: str = ".",
    council_dsl_path: Optional[str] = None,
) -> str:
    """Convenience: read files, run loop."""
    spec_content = Path(spec_path).read_text(encoding="utf-8", errors="ignore")
    work_content = ""
    if work_path:
        work_content = Path(work_path).read_text(encoding="utf-8", errors="ignore")
    council_dsl = ""
    if council_dsl_path:
        with open(council_dsl_path, encoding="utf-8") as f:
            council_dsl = f.read()
    return run_phase_adversarial_loop(
        phase=phase,
        spec_content=spec_content,
        work_content=work_content,
        work_dir=work_dir,
        council_dsl=council_dsl,
    )


if __name__ == "__main__":
    # CLI: python3 -m adv-loop.loop_orchestrator <phase> <spec_path> [work_path] [--council] [--verify-result <path>]
    if len(sys.argv) < 3:
        print("Usage: python3 -m adv-loop.loop_orchestrator <phase> <spec_path> [work_path] [--council] [--verify-result <path>]")
        sys.exit(1)
    phase = int(sys.argv[1])
    spec = sys.argv[2]
    work = None
    council_mode = False
    verify_result = None
    i = 3
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--council":
            council_mode = True
            i += 1
        elif a == "--verify-result":
            verify_result = sys.argv[i + 1]
            i += 2
        else:
            work = a
            i += 1

    if council_mode and not verify_result:
        # Emit envelope, dispatcher (Claude Code) must spawn agents and re-invoke
        envelope = emit_council_envelope_and_signal(phase, spec, work or "")
        print(envelope)
        sys.exit(99)
    else:
        result = run_phase_adversarial_loop_from_files(
            phase, spec, work, work_dir=".", council_dsl_path=verify_result,
        )
        print(result)
