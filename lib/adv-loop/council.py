"""
Council Bridge for adv-loop — Inferential checks (LLM-judge).

Per swebok CLAUDE.md L6.1 (ADR-003 / G.3):
- 4 reviewer roles: ciso, qa-lead, architect, devops-lead
- Each role spawns a subagent via Agent tool
- Each subagent emits a SINGLE DSL line
- Aggregator: RED worst-severity wins, BLUE any-FAIL → DEFENDED:FAIL

Per swebok adversarial-gate.sh / multiagent-launcher.sh:
- The launcher emits a <MULTIAGENT_LAUNCH> envelope with JSONL body
- The dispatcher (Claude Code) intercepts the envelope
- For each JSON line: spawn Agent with subagent_type + prompt
- Collect DSL output, write to /tmp/adv-loop-council-result.json
- Re-invoke adv-loop with --verify-result to close the loop

DSL format (per role):
- CISO (RED):    RED: VULN:<CRIT|HIGH|MED|LOW>;;LOC:<location>;;TYPE:<vuln_type>;;FIX_REQ:<fix>
- QA-Lead (BLUE): BLUE: DEFENDED;;NORMS:KA-<n>+KA-11;;STATUS:<OK|FAIL>
- Architect (BLUE): BLUE: DEFENDED;;NORMS:KA-<n>+KA-2;;STATUS:<OK|FAIL>
- DevOps-Lead (RED/BLUE): RED: VULN:<sev>;;LOC:OPS;;TYPE:<rel>;;FIX_REQ:<fix>
                            OR BLUE: DEFENDED;;NORMS:KA-7;;STATUS:OK
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional


# Per-phase role-specific hooks. Generic prompts are fine for most phases;
# phase-specific anchors ensure reviewers focus on the right artefacts.
# (P0 = no precedent, P10 = closure — both need explicit "look at" guidance.)
PHASE_COUNCIL_ANCHORS = {
    0: "Focus on charter, context_map, stakeholders, success_criteria — does the discovery set the project up for a feasible P1?",
    1: "Focus on feasibility-study.md, roi_analysis.md, go_no_go_memo.md — is the go/no-go decision justified?",
    2: "Focus on srs.md, user_stories.md, acceptance_criteria.md, rtm.md — are ACs testable and traceable?",
    3: "Focus on architecture_doc.md, adrs.md, c4_diagrams/ — are ADRs (MADR template) and C4 levels (context/container/component) present?",
    4: "Focus on design_doc.md, api_contracts.md, data_model.md, sequence_diagrams/ — are interfaces (OpenAPI) and error handling explicit?",
    5: "Focus on source_code/, unit_tests/ — is unit-test ratio adequate and antipattern-free?",
    6: "Focus on test_plan.md, integration_tests/, mutation_report.md, coverage_report.md — do coverage (80/70%) and mutation (70%) meet XG-6.2-XG-6.3?",
    7: "Focus on deployment_plan.md, rollback_plan.md, release_notes.md, smoke_tests.md — is the rollback plan TESTED with safe patterns?",
    8: "Focus on runbooks.md, slos.md, on_call_rotation.md, incident_postmortems.md — are SLOs measurable and escalation paths defined?",
    9: "Focus on refactoring_plan.md, tech_debt_register.md, release_notes.md — is the maintenance type (corrective/adaptive/perfective/preventive) explicit per IEEE 1219?",
    10: "Focus on retirement_plan.md, data_archival.md, user_migration.md, closure_memo.md — is RGPD compliance and réversibilité window explicit?",
}

# SWEBOK v4 KA references per phase (for NORMS field in DSL)
# Note: swebok v4 has 15 KAs numbered KA-1 to KA-15.
PHASE_KA_NORMS = {
    0: "KA-8",  # Software Engineering Management
    1: "KA-8",  # Feasibility = part of management
    2: "KA-1",  # Software Requirements
    3: "KA-2",  # Software Architecture
    4: "KA-3",  # Software Design
    5: "KA-4",  # Software Construction
    6: "KA-5",  # Software Testing
    7: "KA-7",  # Software Engineering Operations (deployment)
    8: "KA-7",  # Software Engineering Operations
    9: "KA-6",  # Software Maintenance
    10: "KA-9",  # Software Engineering Process (lifecycle)
}


def build_council_roles(phase: int, spec_path: str, work_path: str = "") -> List[Dict]:
    """Build the 4-role council config for a given phase.

    Returns a list of dicts (one per role) with:
    - role: human-readable name
    - subagent_type: nexus-* subagent identifier
    - prompt: phase-aware review prompt
    - expected_dsl_keys: list of keys the DSL output must contain
    """
    phase_anchor = PHASE_COUNCIL_ANCHORS.get(phase, "Review the phase deliverables per swebok spec.")
    phase_ka = PHASE_KA_NORMS.get(phase, "KA-0")
    # 2nd KA for context: each phase pairs with its downstream NFR/ops
    secondary_ka = {
        0: "KA-1", 1: "KA-1", 2: "KA-1", 3: "KA-2", 4: "KA-3",
        5: "KA-4", 6: "KA-5", 7: "KA-7", 8: "KA-7", 9: "KA-6", 10: "KA-9",
    }.get(phase, phase_ka)

    work_clause = f" and the work artefact at `{work_path}`" if work_path else ""

    return [
        {
            "role": "ciso",
            "subagent_type": "nexus-ciso",
            "prompt": (
                f"You are an INDEPENDENT CISO performing a SEMANTIC review of swebok phase {phase}. "
                f"Read the spec at `{spec_path}`{work_clause}. "
                f"{phase_anchor} "
                f"Look for security gaps specific to this phase: "
                f"threat model coverage, secrets handling, auth/authz design, "
                f"data classification, RGPD implications, OWASP alignment, "
                f"compliance gaps (ISO 27001/SOC2/HIPAA/PCI-DSS as relevant). "
                f"Output a SINGLE DSL line: "
                f"RED: VULN:<CRIT|HIGH|MED|LOW>;;LOC:<file_or_section>;;TYPE:<vuln_type>;;FIX_REQ:<required_fix>. "
                f"Default to VULN:LOW if no findings. Be conservative — prefer LOW over false positives."
            ),
            "expected_dsl_keys": ["RED:VULN", "RED:LOC", "RED:TYPE", "RED:FIX_REQ"],
        },
        {
            "role": "qa-lead",
            "subagent_type": "nexus-qa-lead",
            "prompt": (
                f"You are an INDEPENDENT QA Lead performing a SEMANTIC review of swebok phase {phase}. "
                f"Read the spec at `{spec_path}`{work_clause}. "
                f"{phase_anchor} "
                f"Evaluate testability: are acceptance criteria measurable? "
                f"Is traceability (RTM) complete forward (to P5/P6) and backward (to P0/P2)? "
                f"Are edge cases, error paths, and NFR (perf/sec/usability) testable? "
                f"Is the test pyramid correct (unit > integration > e2e, in that order)? "
                f"Output a SINGLE DSL line: "
                f"BLUE: DEFENDED;;NORMS:{phase_ka}+{secondary_ka};;STATUS:<OK|FAIL>. "
                f"STATUS:OK if testability is sound, STATUS:FAIL if major gaps."
            ),
            "expected_dsl_keys": ["BLUE:DEFENDED", "BLUE:NORMS", "BLUE:STATUS"],
        },
        {
            "role": "architect",
            "subagent_type": "nexus-architect",
            "prompt": (
                f"You are an INDEPENDENT principal architect performing a SEMANTIC review of swebok phase {phase}. "
                f"Read the spec at `{spec_path}`{work_clause}. "
                f"{phase_anchor} "
                f"Check for: spec-vs-code drift, ADR coherence (if P3+), "
                f"separation of concerns, dependency cycles, coupling smells, "
                f"alignment with the 10-phase SDLC (P0→P10) and demarcation rules "
                f"(the work must NOT contain content from adjacent phases). "
                f"Output a SINGLE DSL line: "
                f"BLUE: DEFENDED;;NORMS:{phase_ka}+KA-2;;STATUS:<OK|FAIL>."
            ),
            "expected_dsl_keys": ["BLUE:DEFENDED", "BLUE:NORMS", "BLUE:STATUS"],
        },
        {
            "role": "devops-lead",
            "subagent_type": "nexus-devops-lead",
            "prompt": (
                f"You are an INDEPENDENT DevOps Lead performing a SEMANTIC review of swebok phase {phase}. "
                f"Read the spec at `{spec_path}`{work_clause}. "
                f"{phase_anchor} "
                f"Check operability: deployability, observability (logs/metrics/traces), "
                f"rollback safety, capacity planning, on-call ergonomics, "
                f"monitoring/alerting calibration, secret rotation, dependency freshness, "
                f"infra-as-code coverage. "
                f"Output a SINGLE DSL line — choose the format that matches your verdict: "
                f"IF issues found: RED: VULN:<CRIT|HIGH|MED|LOW>;;LOC:OPS;;TYPE:<reliability_issue>;;FIX_REQ:<fix>. "
                f"ELSE: BLUE: DEFENDED;;NORMS:{phase_ka};;STATUS:OK."
            ),
            "expected_dsl_keys": ["RED:VULN", "BLUE:STATUS"],
        },
    ]


def emit_council_envelope(phase: int, spec_path: str, work_path: str = "") -> str:
    """Emit a <MULTIAGENT_LAUNCH> envelope with JSONL body (4 roles).

    The dispatcher (Claude Code) reads the envelope, spawns agents,
    collects DSL, and re-invokes adv-loop with --verify-result.
    Exit signal: this function returns the envelope and the caller exits 99.
    """
    roles = build_council_roles(phase, spec_path, work_path)
    phase_label = f"P{phase}"
    lines = ["<MULTIAGENT_LAUNCH gate=\"ADV_LOOP\" target=\"P{phase}_COUNCIL\">".format(phase=phase_label)]
    for r in roles:
        lines.append(json.dumps(r, ensure_ascii=False))
    lines.append("</MULTIAGENT_LAUNCH>")
    return "\n".join(lines)


# === DSL line parsing & aggregation ===

SEVERITY_RANK = {"CRIT": 4, "HIGH": 3, "MED": 2, "LOW": 1, "OK": 0, "PASS": 0}


def parse_dsl_line(line: str) -> Optional[Dict[str, str]]:
    """Parse a DSL line of form 'RED: VULN:CRIT;;LOC:foo;;TYPE:x;;FIX_REQ:y'
    or 'BLUE: DEFENDED;;NORMS:KA-1+KA-2;;STATUS:OK'.

    The first segment is special: 'RED: VULN:CRIT' means the lane is RED
    and the sub-key VULN has value CRIT. We expand this into {'_lane': 'RED',
    'VULN': 'CRIT', ...} so the rest of the aggregator can use dot notation.

    Returns a dict {key: value, ...} or None on parse failure.
    """
    if not line or ";" not in line:
        return None
    parts = [p.strip() for p in line.split(";;") if p.strip()]
    if not parts:
        return None
    parsed = {}
    for idx, p in enumerate(parts):
        if ":" not in p:
            continue
        # First segment may be 'LANE: SUBKEY:VALUE' (e.g. 'RED: VULN:CRIT')
        # or 'LANE: PLAIN' (e.g. 'BLUE: DEFENDED')
        if idx == 0:
            sub_parts = p.split(":", 2)  # up to 3 parts
            if len(sub_parts) == 3:
                lane, sub_k, sub_v = sub_parts
                if lane.strip() in ("RED", "BLUE"):
                    parsed["_lane"] = lane.strip()
                    parsed[sub_k.strip()] = sub_v.strip()
                    continue
            # Fall through: 2-part first segment
            k, v = p.split(":", 1)
            parsed[k.strip()] = v.strip()
        else:
            k, v = p.split(":", 1)
            parsed[k.strip()] = v.strip()
    if not parsed:
        return None
    # Ensure _lane is set
    if "_lane" not in parsed:
        first_key = next(iter(parsed), "")
        if first_key in ("RED", "BLUE"):
            parsed["_lane"] = first_key
    return parsed


def aggregate_council_results(red_lines: List[str], blue_lines: List[str]) -> Dict:
    """Aggregate 4 council DSL outputs into a single verdict.

    Per swebok CLAUDE.md L6.1:
    - RED aggregation: worst-severity wins (CRIT > HIGH > MED > LOW)
    - BLUE aggregation: any FAIL → DEFENDED:FAIL; all OK → DEFENDED:OK
    - Overall verdict: per severity (CRIT > HIGH > MED > LOW > OK)
    """
    red_findings = [parse_dsl_line(l) for l in red_lines if l.strip()]
    blue_findings = [parse_dsl_line(l) for l in blue_lines if l.strip()]
    red_findings = [f for f in red_findings if f]  # drop Nones
    blue_findings = [f for f in blue_findings if f]

    # RED: pick worst severity (and capture its LOC/TYPE/FIX_REQ)
    red_aggregated = {"RED:VULN": "LOW", "RED:LOC": "n/a", "RED:TYPE": "n/a", "RED:FIX_REQ": "n/a"}
    worst_sev = "LOW"
    worst_finding = None
    for f in red_findings:
        sev = f.get("VULN", "LOW")
        if SEVERITY_RANK.get(sev, 0) > SEVERITY_RANK.get(worst_sev, 0):
            worst_sev = sev
            worst_finding = f
    # If we never found anything worse than LOW but we have findings,
    # fall back to the first one so its LOC/TYPE/FIX_REQ are captured.
    if worst_finding is None and red_findings:
        worst_finding = red_findings[0]
    if worst_finding is not None:
        for k in ("LOC", "TYPE", "FIX_REQ"):
            if k in worst_finding:
                red_aggregated[f"RED:{k}"] = worst_finding[k]
    red_aggregated["RED:VULN"] = worst_sev

    # BLUE: any FAIL → DEFENDED:FAIL
    blue_statuses = [f.get("STATUS", "OK") for f in blue_findings]
    blue_aggregated = {"BLUE:DEFENDED": "OK", "BLUE:NORMS": "n/a"}
    if any(s == "FAIL" for s in blue_statuses):
        blue_aggregated["BLUE:DEFENDED"] = "FAIL"
    # Pick the first NORMS found (they should all be the same)
    for f in blue_findings:
        if "NORMS" in f:
            blue_aggregated["BLUE:NORMS"] = f["NORMS"]
            break

    # Council verdict: combined severity
    # RED worst vs BLUE FAIL
    if blue_aggregated["BLUE:DEFENDED"] == "FAIL":
        # If at least one BLUE FAIL, that equals a HIGH (per swebok Council practice)
        council_severity = "HIGH" if SEVERITY_RANK.get(worst_sev, 0) < SEVERITY_RANK["HIGH"] else worst_sev
    else:
        council_severity = worst_sev

    return {
        "red": red_aggregated,
        "blue": blue_aggregated,
        "red_count": len(red_findings),
        "blue_count": len(blue_findings),
        "council_severity": council_severity,
    }


def load_verify_result(path: str) -> Tuple[List[str], List[str]]:
    """Load council result from /tmp file written by the dispatcher.

    Expected JSON schema:
    {
        "red_lines": ["RED: VULN:HIGH;;LOC:foo;;..."],
        "blue_lines": ["BLUE: DEFENDED;;NORMS:KA-1;;STATUS:OK", ...]
    }
    """
    p = Path(path)
    if not p.exists():
        return [], []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return [], []
    return data.get("red_lines", []), data.get("blue_lines", [])


def council_severity_to_dsl(agg: Dict) -> str:
    """Format the aggregated council verdict as swebok DSL fragment."""
    red = agg["red"]
    blue = agg["blue"]
    return (
        f"council:red_vuln={red['RED:VULN']};;"
        f"council:red_loc={red['RED:LOC']};;"
        f"council:red_type={red['RED:TYPE']};;"
        f"council:red_fix_req={red['RED:FIX_REQ']};;"
        f"council:blue_defended={blue['BLUE:DEFENDED']};;"
        f"council:blue_norms={blue['BLUE:NORMS']};;"
        f"council:severity={agg['council_severity']};;"
        f"council:agents_red={agg['red_count']};;"
        f"council:agents_blue={agg['blue_count']}"
    )


if __name__ == "__main__":
    # CLI: python3 -m adv-loop.council <phase> <spec_path> [work_path]
    if len(sys.argv) < 3:
        print("Usage: python3 -m adv-loop.council <phase> <spec_path> [work_path]", file=sys.stderr)
        sys.exit(1)
    phase = int(sys.argv[1])
    spec = sys.argv[2]
    work = sys.argv[3] if len(sys.argv) > 3 else ""
    print(emit_council_envelope(phase, spec, work))
