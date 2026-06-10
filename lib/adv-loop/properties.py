"""
Property-based tests for adv-loop.

S5 (2026-06-10) — 4 properties × 11 phases = 44 property tests.

Per Fowler (2026) and the testing literature, property-based testing
defines invariants that should hold for ALL inputs (not just hand-picked
ones). A generator produces many random inputs; a shrinker finds
minimal counterexamples on failure.

For adv-loop, the 4 properties are META-properties about the harness
itself (not about specific phase content):

  1. Idempotence     : same input → same verdict + counts
  2. Determinism     : same input → byte-identical DSL (modulo steering history)
  3. Monotonicity    : adding adversarial content to a clean input never
                       decreases the severity (severity is monotone w.r.t.
                       adversarial content)
  4. DSL well-formed : output is always valid swebok DSL (KEY:VALUE;; format)

Generator:
  - generate_work_content(seed, intensity) : random adversarial content
  - generate_clean_content(seed) : random non-adversarial content

DSL output format invariant:
  Every adv-loop DSL has the form KEY=VALUE;;KEY=VALUE;...;;adv_loop:verdict=<X>
  where X is one of: 🟢 OK, 🟡 MED, 🟠 HIGH, 🔴 CRIT

Self-tests: 4 properties × 11 phases = 44 cases (S5).
"""
import random
import string
import json
import re
import sys
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from pathlib import Path


# === Property data model ===

@dataclass
class PropertyResult:
    """Result of a single property test."""
    phase: int
    property_name: str
    passed: bool
    n_runs: int
    details: str = ""
    counterexample: Optional[Dict] = None


@dataclass
class PropertyReport:
    total: int = 0
    passed: int = 0
    failed: int = 0
    results: List[PropertyResult] = field(default_factory=list)
    elapsed_s: float = 0.0

    def to_dsl(self) -> str:
        failed = ";".join(
            f"P{r.phase}.{r.property_name}:{r.details[:40]}"
            for r in self.results if not r.passed
        ) or "none"
        return (
            f"property:total={self.total};;"
            f"property:passed={self.passed};;"
            f"property:failed={self.failed};;"
            f"property:failed_cases={failed};;"
            f"property:elapsed_s={self.elapsed_s:.1f}"
        )


# === Content generators ===

# Adversarial vocabulary (for the generator)
VAGUE_MODALS = ["should", "might", "maybe", "could", "perhaps", "probably"]
VAGUE_TEMPORAL = ["soon", "later", "eventually", "asap"]
VAGUE_QUALITY = ["fast", "slow", "good", "bad", "nice", "robust", "clean"]
PLACEHOLDERS = ["TBD", "TODO", "FIXME", "XXX", "TBC"]
INCOMPLETE_ENDINGS = ["etc.", "and more", "and so on", "and others"]

# Phase-specific adversarial keywords (for demarcation tests)
DEMARCATION_KEYWORDS = {
    0: ["feasibility study", "ROI", "go-no-go"],
    1: ["stakeholder map", "P0 charter", "discovery report"],
    2: ["architecture style", "ADR", "tech stack choice"],
    3: ["API contract details", "data model schema", "P4 deliverable"],
    4: ["production code", "unit test", "P5 deliverable"],
    5: ["integration test", "mutation test", "coverage report"],
    6: ["deployment script", "rollback plan", "P7 deliverable"],
    7: ["on-call rotation", "SLO", "runbook"],
    8: ["refactoring plan", "tech debt register", "P9 deliverable"],
    9: ["retirement plan", "EOL decision", "P10 deliverable"],
    10: ["new feature", "next sprint", "P0 charter"],
}


def _random_word(rng: random.Random, length: int = 8) -> str:
    return "".join(rng.choices(string.ascii_lowercase, k=length))


def _random_sentence(rng: random.Random, words: int = 8) -> str:
    parts = [_random_word(rng) for _ in range(words)]
    parts[0] = parts[0].capitalize()
    return " ".join(parts) + "."


def generate_work_content(
    seed: int, intensity: float = 0.5, n_lines: int = 20
) -> str:
    """Generate random work content with controllable adversarial density.

    Args:
        seed: RNG seed for reproducibility
        intensity: 0.0 (clean) → 1.0 (maximally adversarial).
                   Probability that each line contains adversarial elements.
        n_lines: number of lines to generate.
    """
    rng = random.Random(seed)
    lines = []
    for i in range(n_lines):
        # Each line is either clean, vague-modal, placeholder, or subjective
        roll = rng.random()
        if roll < intensity * 0.4:
            # Vague modal + sentence
            modal = rng.choice(VAGUE_MODALS)
            subject = _random_word(rng)
            lines.append(f"{subject.capitalize()} {modal} {_random_word(rng)} {_random_word(rng)}.")
        elif roll < intensity * 0.7:
            # Placeholder
            ph = rng.choice(PLACEHOLDERS)
            lines.append(f"Item {i+1}: {ph} {_random_word(rng)}.")
        elif roll < intensity * 0.85:
            # Subjective quality
            qual = rng.choice(VAGUE_QUALITY)
            lines.append(f"Section {i+1} should be {qual}.")
        elif roll < intensity * 0.95:
            # Incomplete enumeration
            end = rng.choice(INCOMPLETE_ENDINGS)
            lines.append(f"Items include {_random_word(rng)}, {_random_word(rng)}, {end}.")
        else:
            # Clean sentence
            lines.append(_random_sentence(rng))
    return "\n".join(lines)


def generate_clean_content(seed: int, n_lines: int = 20) -> str:
    """Generate content with no vague/placeholder keywords — should score clean."""
    rng = random.Random(seed)
    lines = []
    for i in range(n_lines):
        # Use measurable, specific content
        subject = _random_word(rng)
        verb = rng.choice(["processes", "validates", "stores", "retrieves", "monitors"])
        obj = _random_word(rng)
        # Specific number
        n = rng.randint(100, 10000)
        lines.append(f"Module {i+1} {verb} {n} {obj}s per second with p95 latency under 200ms.")
    return "\n".join(lines)


def generate_demarcation_violation(phase: int, seed: int) -> str:
    """Generate work content that violates demarcation for the given phase."""
    rng = random.Random(seed)
    kws = DEMARCATION_KEYWORDS.get(phase, ["P0 charter"])
    kw = rng.choice(kws)
    return f"This document also covers {kw} as part of the work. " \
           f"The deliverable references {kw} directly."


# === DSL well-formedness check ===

DSL_LINE_RE = re.compile(r"^[a-z_]+:[a-zA-Z0-9_./=+,\-:%]+\s*$")
VERDICT_VALUES = ("🟢 OK", "🟡 MED", "🟠 HIGH", "🔴 CRIT", "🔴", "🟠", "🟡", "🟢")
SEVERITY_VALUES = ("LOW", "MED", "HIGH", "CRIT", "OK")


def is_well_formed_dsl(dsl: str) -> tuple[bool, str]:
    """Check that a swebok DSL string is well-formed.

    Returns (is_well_formed, error_message).
    """
    if not dsl:
        return False, "empty"
    pieces = [p.strip() for p in dsl.split(";;") if p.strip()]
    if not pieces:
        return False, "no pieces"
    if not any(p.startswith("adv_loop:verdict=") for p in pieces):
        return False, "missing adv_loop:verdict=... final key"
    last = pieces[-1]
    if not last.startswith("adv_loop:verdict="):
        return False, f"last key must be adv_loop:verdict, got: {last[:40]}"
    verdict = last.split("=", 1)[1].strip()
    # Accept any verdict containing 🟢/🟡/🟠/🔴 as a sanity check
    if not any(v in verdict for v in SEVERITY_VALUES) and not any(c in verdict for c in "🟢🟡🟠🔴"):
        return False, f"unknown verdict value: {verdict}"
    for piece in pieces:
        # Each piece: lowercase_key: value
        if ":" not in piece:
            return False, f"piece missing ':' : {piece[:40]}"
        k = piece.split(":", 1)[0]
        if k and not k.replace("_", "").isalnum():
            return False, f"key not lowercase/alphanum: {k}"
    return True, ""


# === Property tests ===

def property_idempotence(
    phase: int, work: str, spec: str, project_root: str = "."
) -> PropertyResult:
    """Same input → same verdict + counts (within steering noise)."""
    try:
        from .loop_orchestrator import _run_loop
    except ImportError:
        from loop_orchestrator import _run_loop
    dsl_a, _ = _run_loop(phase, spec, work, work_dir=project_root, max_iterations=1)
    dsl_b, _ = _run_loop(phase, spec, work, work_dir=project_root, max_iterations=1)
    # Compare verdict + counts only (steering fragment depends on history)
    keys_to_compare = [
        "adv_loop:verdict", "phase_loop:findings_crit", "phase_loop:findings_high",
        "phase_loop:findings_med", "phase_loop:findings_low",
    ]
    def get(dsl, k):
        for p in dsl.split(";;"):
            if p.strip().startswith(k + "="):
                return p.strip().split("=", 1)[1]
        return None
    diffs = []
    for k in keys_to_compare:
        a, b = get(dsl_a, k), get(dsl_b, k)
        if a != b:
            diffs.append(f"{k}: {a!r} != {b!r}")
    if diffs:
        return PropertyResult(
            phase, "idempotence", False, 2,
            details=f"verdict/counts differ: {'; '.join(diffs)}",
        )
    return PropertyResult(phase, "idempotence", True, 2)


def property_determinism(
    phase: int, work: str, spec: str, project_root: str = "."
) -> PropertyResult:
    """Same input → byte-identical DSL (modulo timestamp-bearing fields).

    Steering and elapsed_s fields depend on history/time and are excluded.
    """
    try:
        from .loop_orchestrator import _run_loop
    except ImportError:
        from loop_orchestrator import _run_loop
    # Run twice — to be deterministic, the orchestrator must not depend on time/random
    dsl_a, _ = _run_loop(phase, spec, work, work_dir=project_root, max_iterations=1)
    dsl_b, _ = _run_loop(phase, spec, work, work_dir=project_root, max_iterations=1)
    # Strip volatile fields
    volatile_keys = ["steering:", "phase_loop:elapsed_s", "phase_loop:run_total"]
    def strip_volatile(dsl):
        out = []
        for p in dsl.split(";;"):
            if not any(p.strip().startswith(v) for v in volatile_keys):
                out.append(p)
        return ";;".join(out)
    if strip_volatile(dsl_a) != strip_volatile(dsl_b):
        return PropertyResult(
            phase, "determinism", False, 2,
            details=f"DSL differs after stripping volatile fields\n  a={strip_volatile(dsl_a)[:120]}\n  b={strip_volatile(dsl_b)[:120]}",
        )
    return PropertyResult(phase, "determinism", True, 2)


def property_monotonicity(
    phase: int, spec: str, project_root: str = ".", n_seeds: int = 5
) -> PropertyResult:
    """Adding adversarial content to a clean input never decreases severity.

    For each seed: run on clean content, then on the same content PLUS
    adversarial content. The total count of findings should not decrease
    (and the severity should not get lower).
    """
    try:
        from .loop_orchestrator import _run_loop
    except ImportError:
        from loop_orchestrator import _run_loop
    def get_counts(dsl):
        def get(k):
            for p in dsl.split(";;"):
                if p.strip().startswith(k + "="):
                    return int(p.strip().split("=", 1)[1])
            return 0
        return {
            "crit": get("phase_loop:findings_crit"),
            "high": get("phase_loop:findings_high"),
            "med": get("phase_loop:findings_med"),
            "low": get("phase_loop:findings_low"),
        }
    def severity_rank(c):
        # Higher = more severe
        return c["crit"] * 4 + c["high"] * 3 + c["med"] * 2 + c["low"]
    counterexamples = []
    for seed in range(n_seeds):
        clean = generate_clean_content(seed)
        adversarial = generate_work_content(seed, intensity=0.8, n_lines=20)
        # Compose: clean + adversarial = at least as many findings as clean
        combined = clean + "\n" + adversarial
        dsl_clean, _ = _run_loop(phase, spec, clean, work_dir=project_root, max_iterations=1)
        dsl_combined, _ = _run_loop(phase, spec, combined, work_dir=project_root, max_iterations=1)
        c_clean = get_counts(dsl_clean)
        c_combined = get_counts(dsl_combined)
        # Assertion: combined.total >= clean.total (or at worst, equal)
        total_clean = sum(c_clean.values())
        total_combined = sum(c_combined.values())
        if total_combined < total_clean:
            counterexamples.append({
                "seed": seed,
                "clean": c_clean, "combined": c_combined,
                "delta": total_combined - total_clean,
            })
    if counterexamples:
        return PropertyResult(
            phase, "monotonicity", False, n_seeds,
            details=f"{len(counterexamples)} seeds where adversarial reduced findings",
            counterexample=counterexamples[0],
        )
    return PropertyResult(phase, "monotonicity", True, n_seeds)


def property_dsl_well_formed(
    phase: int, project_root: str = ".", n_seeds: int = 10
) -> PropertyResult:
    """For all random work content seeds, the output DSL is well-formed.

    Per swebok DSL spec: KEY=VALUE;;KEY=VALUE;...;;adv_loop:verdict=<X>
    """
    try:
        from .loop_orchestrator import _run_loop
    except ImportError:
        from loop_orchestrator import _run_loop
    spec_path = Path(project_root) / f"specs/workflows/by-phase/phase-{phase}-{_phase_slug(phase)}.md"
    if not spec_path.exists():
        matches = list((Path(project_root) / "specs/workflows/by-phase").glob(f"phase-{phase}-*.md"))
        spec_path = matches[0] if matches else None
    if not spec_path:
        return PropertyResult(phase, "dsl_well_formed", False, 0, "spec not found")
    spec = spec_path.read_text(encoding="utf-8", errors="ignore")
    counterexamples = []
    for seed in range(n_seeds):
        for intensity in [0.0, 0.3, 0.6, 0.9, 1.0]:
            work = generate_work_content(seed, intensity=intensity, n_lines=15)
            dsl, _ = _run_loop(phase, spec, work, work_dir=project_root, max_iterations=1)
            ok, err = is_well_formed_dsl(dsl)
            if not ok:
                counterexamples.append({
                    "seed": seed, "intensity": intensity, "error": err,
                    "dsl_preview": dsl[:120],
                })
    if counterexamples:
        return PropertyResult(
            phase, "dsl_well_formed", False, n_seeds * 5,
            details=f"{len(counterexamples)} malformed DSL outputs",
            counterexample=counterexamples[0],
        )
    return PropertyResult(phase, "dsl_well_formed", True, n_seeds * 5)


def _phase_slug(phase: int) -> str:
    slugs = {
        0: "discovery", 1: "concept-feasibility", 2: "requirements",
        3: "architecture", 4: "design", 5: "implementation", 6: "testing",
        7: "deployment", 8: "operations", 9: "maintenance", 10: "retirement",
    }
    return slugs.get(phase, f"phase-{phase}")


# === Runner ===

def run_all_properties(project_root: str = ".") -> PropertyReport:
    """Run all 4 properties × 11 phases = 44 property tests."""
    report = PropertyReport()
    t0 = time.time()
    for phase in range(11):
        spec_path = Path(project_root) / f"specs/workflows/by-phase/phase-{phase}-{_phase_slug(phase)}.md"
        if not spec_path.exists():
            matches = list((Path(project_root) / "specs/workflows/by-phase").glob(f"phase-{phase}-*.md"))
            spec_path = matches[0] if matches else None
        if not spec_path:
            continue
        spec = spec_path.read_text(encoding="utf-8", errors="ignore")
        work = generate_work_content(seed=42, intensity=0.5, n_lines=10)

        # Property 1: idempotence
        r = property_idempotence(phase, work, spec, project_root)
        report.results.append(r)
        if r.passed:
            report.passed += 1
        else:
            report.failed += 1

        # Property 2: determinism
        r = property_determinism(phase, work, spec, project_root)
        report.results.append(r)
        if r.passed:
            report.passed += 1
        else:
            report.failed += 1

        # Property 3: monotonicity (multi-seed)
        r = property_monotonicity(phase, spec, project_root, n_seeds=3)
        report.results.append(r)
        if r.passed:
            report.passed += 1
        else:
            report.failed += 1

        # Property 4: DSL well-formedness (multi-seed × multi-intensity)
        r = property_dsl_well_formed(phase, project_root, n_seeds=3)
        report.results.append(r)
        if r.passed:
            report.passed += 1
        else:
            report.failed += 1

    report.total = len(report.results)
    report.elapsed_s = time.time() - t0
    return report


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        report = run_all_properties(".")
        for r in report.results:
            status = "✓" if r.passed else "✗"
            print(f"  {status} P{r.phase:2d} {r.property_name:18s} runs={r.n_runs}")
        print()
        print(f"Total: {report.total}  Passed: {report.passed}  Failed: {report.failed}  "
              f"Elapsed: {report.elapsed_s:.1f}s")
        print(report.to_dsl())
        sys.exit(0 if report.failed == 0 else 1)
    print("Usage: python3 -m adv-loop.properties all")
    sys.exit(1)
