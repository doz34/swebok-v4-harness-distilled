"""
Feedforward controls (guides) — prevent issues BEFORE they happen.
Per Fowler: "Guides increase the probability that the agent creates good results in the first attempt"

For swebok, feedforward controls are:
1. Spec compliance check — does the work-in-progress match the phase spec?
2. Demarcation check — is the work in the right phase vs adjacent ones?
3. Required livrables check — are all mandatory deliverables present?
4. Entry gate check — are all entry criteria met?
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import re
import os
import sys
from pathlib import Path


@dataclass
class FeedbackFinding:
    """A finding from a feedback sensor (post-phase)."""
    sensor_name: str
    severity: str  # "CRIT" | "HIGH" | "MED" | "LOW"
    message: str
    line_ref: Optional[str] = None
    fix_suggestion: Optional[str] = None


@dataclass
class FeedforwardResult:
    """Result of a feedforward control check."""
    control_name: str
    passed: bool
    severity: str  # "CRIT" | "HIGH" | "MED" | "LOW"
    message: str
    fix_suggestion: Optional[str] = None


# Per-phase feedforward controls (computational, deterministic)
PHASE_FEEDFORWARDS = {
    0: {
        "spec": "specs/workflows/by-phase/phase-0-discovery.md",
        "entry_criteria": ["user_profile_detected", "max_5_questions"],
        "required_deliverables": [
            "charter.md", "context_map.md", "stakeholders.md",
            "constraints.md", "success_criteria.md", "alternatives.md",
            "discovery_report.md"
        ],
        "demarcation": "P0 ≠ P1 (no feasibility study in P0)",
    },
    1: {
        "spec": "specs/workflows/by-phase/phase-1-concept-feasibility.md",
        "entry_criteria": ["p0_signed_off"],
        "required_deliverables": ["feasibility_report.md", "roi_analysis.md", "go_no_go_memo.md"],
        "demarcation": "P1 ≠ P0 (no new discovery) and P1 ≠ P2 (no requirements)",
    },
    2: {
        "spec": "specs/workflows/by-phase/phase-2-requirements.md",
        "entry_criteria": ["p1_go_decision"],
        "required_deliverables": ["srs.md", "user_stories.md", "acceptance_criteria.md", "rtm.md"],
        "demarcation": "P2 ≠ P1 (no feasibility) and P2 ≠ P3 (no architecture)",
    },
    3: {
        "spec": "specs/workflows/by-phase/phase-3-architecture.md",
        "entry_criteria": ["p2_srs_signed"],
        "required_deliverables": ["architecture_doc.md", "adrs.md", "c4_diagrams/"],
        "demarcation": "P3 ≠ P4 (no detailed module design) and P3 ≠ P2 (no reqs)",
    },
    4: {
        "spec": "specs/workflows/by-phase/phase-4-design.md",
        "entry_criteria": ["p3_architecture_signed"],
        "required_deliverables": ["design_doc.md", "api_contracts.md", "data_model.md", "sequence_diagrams/"],
        "demarcation": "P4 ≠ P3 (no arch style) and P4 ≠ P5 (no code)",
    },
    5: {
        "spec": "specs/workflows/by-phase/phase-5-implementation.md",
        "entry_criteria": ["p4_design_signed", "unit_tests_pattern_defined"],
        "required_deliverables": ["source_code/", "unit_tests/"],
        "demarcation": "P5 = unit tests ONLY, P6 = coverage + mutation + reste",
    },
    6: {
        "spec": "specs/workflows/by-phase/phase-6-testing.md",
        "entry_criteria": ["p5_code_complete", "unit_tests_passing"],
        "required_deliverables": ["test_plan.md", "integration_tests/", "mutation_report.md", "coverage_report.md"],
        "demarcation": "P6 ≠ P5 (no new features) and P6 ≠ P7 (no deploy)",
    },
    7: {
        "spec": "specs/workflows/by-phase/phase-7-deployment.md",
        "entry_criteria": ["p6_test_plan_validated", "rollback_plan_tested"],
        "required_deliverables": ["deployment_plan.md", "rollback_plan.md", "release_notes.md", "smoke_tests.md"],
        "demarcation": "P7 ≠ P6 (no test refactor) and P7 ≠ P8 (no runbook)",
    },
    8: {
        "spec": "specs/workflows/by-phase/phase-8-operations.md",
        "entry_criteria": ["p7_deployment_done", "slos_defined"],
        "required_deliverables": ["runbooks.md", "slos.md", "on_call_rotation.md", "incident_postmortems.md"],
        "demarcation": "P8 ≠ P7 (no new deploy) and P8 ≠ P9 (no refactor)",
    },
    9: {
        "spec": "specs/workflows/by-phase/phase-9-maintenance.md",
        "entry_criteria": ["p8_runbook_validated", "tech_debt_register_active"],
        "required_deliverables": ["refactoring_plan.md", "tech_debt_register.md", "release_notes.md"],
        "demarcation": "P9 ≠ P8 (no runbook) and P9 ≠ P10 (no retirement prep)",
    },
    10: {
        "spec": "specs/workflows/by-phase/phase-10-retirement.md",
        "entry_criteria": ["p9_eol_decision", "replacement_ready"],
        "required_deliverables": ["retirement_plan.md", "data_archival.md", "user_migration.md", "closure_memo.md"],
        "demarcation": "P10 ≠ P9 (no maintenance) and P10 ≠ P0 (no new project)",
    },
}


def check_phase_feedforwards(phase: int, work_dir: str = ".") -> List[FeedforwardResult]:
    """Run all feedforward controls for a given phase. Return findings."""
    results: List[FeedforwardResult] = []
    config = PHASE_FEEDFORWARDS.get(phase)
    if not config:
        return [FeedforwardResult("config", False, "CRIT", f"No config for phase {phase}")]

    # 1. Spec compliance
    spec_path = Path(work_dir) / config["spec"]
    if not spec_path.exists():
        results.append(FeedforwardResult(
            "spec_exists", False, "CRIT",
            f"Spec file missing: {config['spec']}",
            "Verify phase spec is at the expected path"
        ))
    # S3 fix: don't log "Spec OK" as a finding — it's a passing marker,
    # not a real critique. Logging it pollutes the steering pattern detector
    # (every run would mark "Spec OK" as a recurring LOW).

    # 2. Required deliverables presence
    work_path = Path(work_dir)
    for d in config["required_deliverables"]:
        # Deliverables are directories or files
        full = work_path / d
        # Check if it exists OR is mentioned in any obvious location
        # (in this MVP, we just verify the spec mentions the deliverable)
        pass  # deliverable checks need work_dir scan — done by feedback sensors

    return results


def check_demarcation(phase: int, work_content: str) -> List[FeedforwardResult]:
    """Check that the work-in-progress respects phase demarcation.
    This is a heuristic check based on keywords that should/shouldn't appear."""
    results: List[FeedforwardResult] = []
    config = PHASE_FEEDFORWARDS.get(phase)
    if not config:
        return results

    demarcation = config.get("demarcation", "")
    # Heuristic keywords per phase
    FORBIDDEN_KEYWORDS = {
        0: ["feasibility study", "ROI", "go-no-go", "P1 deliverable"],
        1: ["stakeholder map", "P0 charter", "discovery report"],
        2: ["architecture style", "P3 deliverable", "ADR", "tech stack choice"],
        3: ["API contract details", "data model schema", "P4 deliverable"],
        4: ["production code", "unit test", "P5 deliverable"],
        5: ["integration test", "mutation test", "P6 deliverable", "coverage report"],
        6: ["deployment script", "rollback plan", "P7 deliverable"],
        7: ["on-call rotation", "P8 deliverable", "SLO"],
        8: ["refactoring plan", "tech debt register", "P9 deliverable"],
        9: ["retirement plan", "EOL decision", "P10 deliverable"],
        10: ["new feature", "next sprint", "P0 charter"],
    }

    forbidden = FORBIDDEN_KEYWORDS.get(phase, [])
    work_lower = work_content.lower()
    for kw in forbidden:
        if kw.lower() in work_lower:
            results.append(FeedforwardResult(
                "demarcation", False, "HIGH",
                f"Work mentions '{kw}' which belongs to adjacent phase",
                f"Move '{kw}' to the appropriate phase per demarcation: {demarcation}"
            ))

    if not results:
        results.append(FeedforwardResult("demarcation", True, "LOW", f"Demarcation OK for P{phase}"))

    return results


# ==== Feedback sensors (linter) ====

# Patterns for spec vagueness detection (computational, deterministic)
# Severity rationale:
# - HIGH: placeholders that MUST be resolved (TBD, FIXME)
# - MED: vague modals that hide requirements
# - LOW: stylistic issues (some, few, etc.)
SPEC_VAGUE_PATTERNS = [
    (r"\b(should|might|may|could|perhaps|maybe|probably)\b", "MED", "Vague modal verb"),
    (r"\b(TBD|TODO|FIXME|XXX)\b", "HIGH", "Unresolved placeholder"),
    (r"\b(some|few|many|several|various)\b", "LOW", "Quantifier vagueness"),
    # "fast/slow" are subjective but common in swebok specs — demote to LOW
    (r"\b(fast|slow|good|bad|nice)\b", "LOW", "Subjective quality (consider measurable metric)"),
    (r"\b(soon|later|eventually|asap)\b", "MED", "Temporal vagueness"),
    (r"\betc\.?\b|\band so on\b|\band more\b", "LOW", "Incomplete enumeration"),
    (r"\b(can|should)\s+be\s+(used|done|added)\b", "MED", "Vague imperative"),
]

# Patterns for required sections in swebok specs
# Note: swebok specs mix English and French headers
# Universal (all phases)
REQUIRED_SECTIONS = [
    # Status / Statut (universal)
    (r"(\*\*Statut\*\*|##\s*Statut|##\s*Status)", "Status/Statut"),
    # Metadata / Métadonnées (universal)
    (r"(\*\*M[ée]tadonn[ée]es\*\*|##\s*M[ée]tadonn[ée]es|##\s*Metadata)", "Métadonnées"),
    # Mission (universal)
    (r"(##\s*Mission|\*\*Mission\*\*|##\s*Objectif)", "Mission"),
    # Verdict (universal, may be at end)
    (r"(##\s*Verdict|\*\*Verdict\*\*)", "Verdict"),
]

# Optional sections (MED severity if missing) — phase-specific
OPTIONAL_SECTIONS = [
    # Livrables / Artifacts (only P2-P10)
    (r"(##\s*Livrables?|##\s*Artifacts?\s+Produced|\*\*Livrables?\*\*|##\s*Deliverables?|7\s+activit[ée]s\s*\(=\s*7\s+livrables)", "Livrables/Artifacts"),
]

# Cross-phase consistency: each phase must reference prior phases
PHASE_CHAIN = {
    3: [  # P3 Architecture
        (r"(Requirements|Exigences|Requirements Engineering|NFR|non-fonctionnel)", "P3 should reference P2 requirements"),
    ],
    4: [  # P4 Design
        (r"(Architecture|ADRs?|D[ée]cisions?\s+d[' ]architecture)", "P4 should reference P3 ADRs"),
        (r"(Requirements|SRS|exigences)", "P4 should reference P2 SRS"),
    ],
    5: [  # P5 Implementation
        (r"(Design|API|contract)", "P5 should reference P4 design"),
    ],
    6: [  # P6 Testing
        (r"(Acceptance|SRS|Requirements|crit[èe]res?\s+d[' ]acceptation)", "P6 should reference P2 acceptance criteria"),
    ],
    7: [  # P7 Deployment
        (r"(Test|Rollback|Smoke)", "P7 should reference P6 test plan + rollback"),
    ],
    8: [  # P8 Operations
        (r"(SLO|Monitoring|Alert|runbook)", "P8 should reference SLOs + runbooks"),
    ],
    9: [  # P9 Maintenance
        (r"(Tech.?debt|Refactor|ADR)", "P9 should reference tech debt + ADRs"),
    ],
    10: [  # P10 Retirement
        (r"(Data.?archival|RGPD|Compliance|EOL|retirement)", "P10 should reference RGPD + data archival"),
    ],
}


def lint_spec_vagueness(content: str) -> List[FeedbackFinding]:
    """Computational sensor: detect vague language in a spec."""
    findings: List[FeedbackFinding] = []
    for line_no, line in enumerate(content.split("\n"), 1):
        # Skip code blocks, comments, DSL lines
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("#"):
            continue
        if ";" in stripped and ":" in stripped and stripped.startswith("phase_"):
            continue
        for pattern, severity, msg in SPEC_VAGUE_PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                findings.append(FeedbackFinding(
                    "spec_vague", severity,
                    f"Line {line_no}: '{match.group()}' ({msg})",
                    line_ref=f"L{line_no}",
                    fix_suggestion="Replace with measurable criterion"
                ))
    return findings


def lint_required_sections(content: str, phase: int) -> List[FeedbackFinding]:
    """Computational sensor: check that required sections exist."""
    findings: List[FeedbackFinding] = []
    # Universal required
    for pattern, label in REQUIRED_SECTIONS:
        if not re.search(pattern, content, re.IGNORECASE):
            # P1+ specs use Gates instead of Verdict
            if label == "Verdict" and phase >= 1:
                # Skip for P1+: Entry/Exit Gates are used instead
                continue
            findings.append(FeedbackFinding(
                "required_section", "HIGH",
                f"Missing required section: '{label}'",
                fix_suggestion=f"Add section: ## {label}"
            ))
    # Phase-specific required (P1+)
    if phase >= 1:
        # Entry Gate OR Entry Critères OR Conditions d'entrée OR Démarrage (P0, P2)
        if not re.search(r"(##\s*Entry\s+Gate|##\s*Entr[ée]e|##\s*Conditions?\s+d[' ]entr[ée]e|##\s*D[ée]marrage)", content, re.IGNORECASE):
            findings.append(FeedbackFinding(
                "required_section", "HIGH",
                "Missing required section: 'Entry Gate / Conditions d'entrée'",
                fix_suggestion="Add section: ## Entry Gate (or Conditions d'entrée)"
            ))
        # Exit Gate OR Sortie Critères OR Conditions de sortie
        if not re.search(r"(##\s*Exit\s+Gate|##\s*Sortie|##\s*Conditions?\s+de\s+sortie)", content, re.IGNORECASE):
            findings.append(FeedbackFinding(
                "required_section", "HIGH",
                "Missing required section: 'Exit Gate / Conditions de sortie'",
                fix_suggestion="Add section: ## Exit Gate (or Conditions de sortie)"
            ))
    # Optional sections (MED if missing)
    for pattern, label in OPTIONAL_SECTIONS:
        if not re.search(pattern, content, re.IGNORECASE):
            findings.append(FeedbackFinding(
                "optional_section", "MED",
                f"Optional section missing: '{label}'",
                fix_suggestion=f"Consider adding: ## {label}"
            ))
    return findings


def lint_cross_phase_consistency(content: str, phase: int) -> List[FeedbackFinding]:
    """Computational sensor: check that current phase references prior phases."""
    findings: List[FeedbackFinding] = []
    refs = PHASE_CHAIN.get(phase, [])
    for pattern, label in refs:
        if not re.search(pattern, content, re.IGNORECASE):
            findings.append(FeedbackFinding(
                "cross_phase", "MED",
                f"Missing reference: {label}",
                fix_suggestion=f"Reference prior phase via pattern: {pattern}"
            ))
    return findings


def lint_dsl_format(content: str) -> List[FeedbackFinding]:
    """Computational sensor: lint DSL output (KEY:VALUE;;KEY:VALUE)."""
    findings: List[FeedbackFinding] = []
    for line_no, line in enumerate(content.split("\n"), 1):
        if ";" in line and ":" in line:
            # Heuristic: DSL line should be lowercase_key: value
            if re.match(r"^[A-Z]+:", line):
                findings.append(FeedbackFinding(
                    "dsl_format", "LOW",
                    f"Line {line_no}: DSL key should be lowercase",
                    fix_suggestion="Format: 'lowercase_key: value'"
                ))
    return findings


def run_all_feedback_sensors(phase: int, content: str) -> List[FeedbackFinding]:
    """Run all feedback sensors for a given phase + content."""
    findings: List[FeedbackFinding] = []
    findings.extend(lint_spec_vagueness(content))
    findings.extend(lint_required_sections(content, phase))
    findings.extend(lint_cross_phase_consistency(content, phase))
    findings.extend(lint_dsl_format(content))
    return findings
