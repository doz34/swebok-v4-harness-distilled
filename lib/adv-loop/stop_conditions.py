"""
Stop conditions for adversarial loop.
Per dev.to "Adversarial Planning for Spec Driven Development":
> "You need stop conditions that are not emotional. You need boundaries that are mechanical."

Stop signals prevent infinite loops. Three orthogonal stop conditions:
1. Time — hard timeout per phase (swebok spec has 35min cap for P0, varies)
2. Token budget — soft/hard cap (swebok spec has 4k/7k/10k for P0)
3. Value — diminishing returns: if last N critiques were LOW-severity, stop

Design choice: stop conditions are checked AFTER each adversarial iteration.
If any stop condition is met, return stop_reason for audit trail.
"""
from dataclasses import dataclass, field
from typing import List, Optional
import time


@dataclass
class AdversarialFinding:
    """A single critique from the adversarial loop."""
    severity: str  # "CRIT" | "HIGH" | "MED" | "LOW"
    category: str  # "completeness" | "survivability" | "ambiguity" | "coupling" | "testability" | ...
    message: str
    line_ref: Optional[str] = None  # e.g. "P2/Section3/EG-2.1"
    fix_suggestion: Optional[str] = None


@dataclass
class StopState:
    """Tracks the adversarial loop state and decides when to stop."""
    start_time: float = field(default_factory=time.time)
    max_seconds: int = 1800  # 30min default per phase
    token_soft_cap: int = 7000
    token_hard_cap: int = 10000
    tokens_consumed: int = 0
    findings: List[AdversarialFinding] = field(default_factory=list)
    iterations: int = 0
    max_iterations: int = 5
    low_severity_streak: int = 0
    low_severity_threshold: int = 3  # 3 LOW in a row = stop (value criterion)
    force_stop: bool = False

    def check_stop(self) -> Optional[str]:
        """Return None if loop should continue, else stop_reason."""
        if self.force_stop:
            return "force_stop"
        elapsed = time.time() - self.start_time
        if elapsed > self.max_seconds:
            return f"time_cap ({elapsed:.0f}s > {self.max_seconds}s)"
        if self.tokens_consumed > self.token_hard_cap:
            return f"token_hard_cap ({self.tokens_consumed} > {self.token_hard_cap})"
        if self.iterations >= self.max_iterations:
            return f"max_iterations ({self.iterations})"
        if self.low_severity_streak >= self.low_severity_threshold:
            return f"value_diminishing ({self.low_severity_streak} LOW in row)"
        return None

    def add_finding(self, finding: AdversarialFinding) -> None:
        self.findings.append(finding)
        self.iterations += 1
        if finding.severity == "LOW":
            self.low_severity_streak += 1
        else:
            self.low_severity_streak = 0  # reset on any non-LOW

    def to_dsl(self) -> str:
        """Export as swebok DSL (KEY:VALUE;;KEY:VALUE)."""
        crits = sum(1 for f in self.findings if f.severity == "CRIT")
        highs = sum(1 for f in self.findings if f.severity == "HIGH")
        meds = sum(1 for f in self.findings if f.severity == "MED")
        lows = sum(1 for f in self.findings if f.severity == "LOW")
        return (
            f"phase_loop:iterations={self.iterations};;"
            f"phase_loop:findings_crit={crits};;"
            f"phase_loop:findings_high={highs};;"
            f"phase_loop:findings_med={meds};;"
            f"phase_loop:findings_low={lows};;"
            f"phase_loop:tokens={self.tokens_consumed};;"
            f"phase_loop:elapsed_s={int(time.time() - self.start_time)};;"
            f"phase_loop:low_streak={self.low_severity_streak}"
        )

    def verdict(self) -> str:
        """Return overall verdict (mirroring swebok Council verdicts)."""
        crits = sum(1 for f in self.findings if f.severity == "CRIT")
        highs = sum(1 for f in self.findings if f.severity == "HIGH")
        meds = sum(1 for f in self.findings if f.severity == "MED")
        if crits > 0:
            return "🔴 CRIT"
        if highs > 0:
            return "🟠 HIGH"
        if meds > 0:
            return "🟡 MED"
        return "🟢 OK"
