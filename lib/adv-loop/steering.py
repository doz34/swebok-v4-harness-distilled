"""
Steering loop persistence for adv-loop.

Per Fowler (2026): "the human's job is to steer the agent by iterating
on the harness. Whenever an issue happens multiple times, the feedforward
and feedback controls should be improved."

S3 (2026-06-10) — Persistence:
- Store every adv-loop run in a dedicated SQLite DB at .swebok_steering_state.db
- Fingerprint each finding (category + message[:80] hash) to detect recurrence
- Track per-pattern history: first_seen, last_seen, count
- Generate steering action suggestions: "this finding recurred N times,
  consider improving <pattern_script> with <check>"

Why a separate DB: keeps the main .swebok_state.db schema untouched
(no migration on the existing state_engine), gives the maintainer a
single file to inspect/clear for steering-loop-specific data.

DSL fields emitted (per run):
- steering:run_id=<N>
- steering:patterns_detected=<M>
- steering:recurring_categories=<top3>
- steering:top_finding=<message>
"""
import sqlite3
import hashlib
import json
import os
import time
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict, Optional, Iterable
from dataclasses import dataclass


# Default path: alongside .swebok_state.db but in a separate file
def default_db_path(project_root: str = ".") -> str:
    return str(Path(project_root) / ".swebok_steering_state.db")


# === Schema ===

SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phase INTEGER NOT NULL,
    spec_path TEXT NOT NULL,
    work_path TEXT,
    verdict TEXT NOT NULL,
    findings_crit INTEGER DEFAULT 0,
    findings_high INTEGER DEFAULT 0,
    findings_med INTEGER DEFAULT 0,
    findings_low INTEGER DEFAULT 0,
    council_severity TEXT,
    total_findings INTEGER NOT NULL,
    dsl TEXT
);

CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    severity TEXT NOT NULL,
    category TEXT NOT NULL,
    message TEXT NOT NULL,
    line_ref TEXT,
    fix_suggestion TEXT,
    fingerprint TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_findings_fingerprint
    ON findings(fingerprint);
CREATE INDEX IF NOT EXISTS idx_findings_run
    ON findings(run_id);
CREATE INDEX IF NOT EXISTS idx_runs_phase
    ON runs(phase, ts);

CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint TEXT UNIQUE NOT NULL,
    severity TEXT NOT NULL,
    category TEXT NOT NULL,
    sample_message TEXT NOT NULL,
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    occurrences INTEGER NOT NULL DEFAULT 1,
    suggested_action TEXT,
    acknowledged BOOLEAN DEFAULT 0
);
"""


# === Connection helper ===

@contextmanager
def _connect(db_path: str, write: bool = False):
    """Open a SQLite connection with WAL + foreign keys + row factory."""
    conn = sqlite3.connect(db_path, isolation_level=None)  # autocommit
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    # Restrict DB file permissions to owner-only
    try:
        os.chmod(db_path, 0o600)
    except OSError:
        pass
    if write:
        conn.execute("PRAGMA synchronous = NORMAL")
    try:
        yield conn
    finally:
        conn.close()


def _init_db(db_path: str) -> None:
    """Idempotent schema init."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with _connect(db_path, write=True) as conn:
        conn.executescript(SCHEMA_V1)


# === Fingerprinting ===

def fingerprint_finding(severity: str, category: str, message: str) -> str:
    """Stable hash for a finding, used to detect recurrence.

    Uses severity + category + first 80 chars of message (case-folded,
    whitespace-collapsed). Same finding across runs → same fingerprint.
    """
    msg_norm = " ".join(message.lower().split())[:80]
    key = f"{severity.upper()}|{category.lower()}|{msg_norm}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


# === Public API ===

@dataclass(frozen=True)
class FindingRecord:
    severity: str
    category: str
    message: str
    line_ref: Optional[str] = None
    fix_suggestion: Optional[str] = None


@dataclass(frozen=True)
class RunRecord:
    phase: int
    spec_path: str
    work_path: Optional[str]
    verdict: str
    findings: List[FindingRecord]
    council_severity: Optional[str] = None
    dsl: Optional[str] = None


@dataclass
class PatternInfo:
    fingerprint: str
    severity: str
    category: str
    sample_message: str
    occurrences: int
    first_seen: str
    last_seen: str
    suggested_action: Optional[str]
    acknowledged: bool


def log_run(db_path: str, run: RunRecord) -> int:
    """Log a single adv-loop run + all its findings. Returns run_id."""
    _init_db(db_path)
    with _connect(db_path, write=True) as conn:
        cur = conn.execute(
            """INSERT INTO runs
            (phase, spec_path, work_path, verdict,
             findings_crit, findings_high, findings_med, findings_low,
             council_severity, total_findings, dsl)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (run.phase, run.spec_path, run.work_path, run.verdict,
             sum(1 for f in run.findings if f.severity == "CRIT"),
             sum(1 for f in run.findings if f.severity == "HIGH"),
             sum(1 for f in run.findings if f.severity == "MED"),
             sum(1 for f in run.findings if f.severity == "LOW"),
             run.council_severity,
             len(run.findings),
             run.dsl)
        )
        run_id = cur.lastrowid
        for f in run.findings:
            fp = fingerprint_finding(f.severity, f.category, f.message)
            conn.execute(
                """INSERT INTO findings
                (run_id, severity, category, message, line_ref,
                 fix_suggestion, fingerprint)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (run_id, f.severity, f.category, f.message, f.line_ref,
                 f.fix_suggestion, fp)
            )
        # Update patterns table
        fps_in_run = set()
        for f in run.findings:
            fp = fingerprint_finding(f.severity, f.category, f.message)
            fps_in_run.add((fp, f))
        for fp, f in fps_in_run:
            existing = conn.execute(
                "SELECT id, occurrences FROM patterns WHERE fingerprint = ?",
                (fp,)
            ).fetchone()
            if existing is None:
                conn.execute(
                    """INSERT INTO patterns
                    (fingerprint, severity, category, sample_message,
                     first_seen, last_seen, occurrences, suggested_action)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
                            1, ?)""",
                    (fp, f.severity, f.category, f.message[:200],
                     _suggest_action(f.severity, f.category))
                )
            else:
                conn.execute(
                    """UPDATE patterns
                    SET last_seen = CURRENT_TIMESTAMP,
                        occurrences = occurrences + 1,
                        sample_message = ?
                    WHERE fingerprint = ?""",
                    (f.message[:200], fp)
                )
    return run_id


def get_history(db_path: str, phase: int, last_n: int = 10) -> List[Dict]:
    """Return the N most recent runs for a phase, newest first."""
    if not Path(db_path).exists():
        return []
    with _connect(db_path) as conn:
        rows = conn.execute(
            """SELECT id, ts, phase, spec_path, work_path, verdict,
                      findings_crit, findings_high, findings_med, findings_low,
                      council_severity, total_findings
            FROM runs
            WHERE phase = ?
            ORDER BY id DESC
            LIMIT ?""",
            (phase, last_n)
        ).fetchall()
        return [dict(r) for r in rows]


def detect_repeating_findings(
    db_path: str, threshold: int = 3, since_run_id: Optional[int] = None
) -> List[PatternInfo]:
    """Return all patterns that have occurred >= threshold times.

    If since_run_id is set, only count occurrences in runs after that ID
    (useful for "patterns introduced since my last commit").
    """
    if not Path(db_path).exists():
        return []
    with _connect(db_path) as conn:
        if since_run_id is not None:
            rows = conn.execute(
                """SELECT p.fingerprint, p.severity, p.category, p.sample_message,
                          p.first_seen, p.last_seen, p.occurrences,
                          p.suggested_action, p.acknowledged,
                          COALESCE((
                              SELECT COUNT(*) FROM findings f
                              WHERE f.fingerprint = p.fingerprint
                                AND f.run_id > ?
                          ), 0) AS recent_count
                FROM patterns p
                HAVING recent_count >= ?
                ORDER BY recent_count DESC, p.occurrences DESC""",
                (since_run_id, threshold)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT fingerprint, severity, category, sample_message,
                          first_seen, last_seen, occurrences,
                          suggested_action, acknowledged
                FROM patterns
                WHERE occurrences >= ?
                ORDER BY occurrences DESC""",
                (threshold,)
            ).fetchall()
        return [
            PatternInfo(
                fingerprint=r["fingerprint"],
                severity=r["severity"],
                category=r["category"],
                sample_message=r["sample_message"],
                occurrences=r["occurrences"],
                first_seen=r["first_seen"],
                last_seen=r["last_seen"],
                suggested_action=r["suggested_action"],
                acknowledged=bool(r["acknowledged"]),
            )
            for r in rows
        ]


def acknowledge_pattern(db_path: str, fingerprint: str) -> bool:
    """Mark a pattern as acknowledged (the maintainer has fixed it)."""
    if not Path(db_path).exists():
        return False
    with _connect(db_path, write=True) as conn:
        cur = conn.execute(
            "UPDATE patterns SET acknowledged = 1 WHERE fingerprint = ?",
            (fingerprint,)
        )
        return cur.rowcount > 0


def clear_history(db_path: str, phase: Optional[int] = None) -> int:
    """Clear steering history. If phase is set, only that phase's runs.

    Returns number of runs deleted.
    """
    if not Path(db_path).exists():
        return 0
    with _connect(db_path, write=True) as conn:
        if phase is None:
            cur = conn.execute("DELETE FROM runs")
        else:
            cur = conn.execute("DELETE FROM runs WHERE phase = ?", (phase,))
        return cur.rowcount


# === Steering action suggestion ===

# Map (severity, category) → actionable suggestion. Generic when no match.
_STEERING_ACTIONS = {
    ("HIGH", "feedback:spec_vague"): (
        "Add a non-vague-language check to the per-phase pattern script "
        "(e.g. grep for 'should/might' and require measurable criterion)"
    ),
    ("MED", "feedback:spec_vague"): (
        "Strengthen the pattern script's vague-language filter"
    ),
    ("HIGH", "feedforward:demarcation"): (
        "The phase spec allows content from adjacent phases. Tighten the "
        "PHASE_FEEDFORWARDS demarcation list in lib/adv-loop/feedback.py"
    ),
    ("HIGH", "feedforward:required_deliverable"): (
        "Update specs/workflows/by-phase/phase-{n}.md to clarify the "
        "deliverable list (check the 'required_deliverables' array)"
    ),
    ("HIGH", "feedback:required_section"): (
        "Add the missing section to the phase spec (universal sections: "
        "Statut, Métadonnées, Mission)"
    ),
    ("MED", "feedback:required_section"): (
        "Add the optional section (Entry Gate, Exit Gate) to the phase spec"
    ),
    ("HIGH", "feedback:cross_phase"): (
        "Add a back-reference from this phase spec to the prior phase's "
        "deliverables (per PHASE_CHAIN in lib/adv-loop/feedback.py)"
    ),
    ("LOW", "feedback:spec_vague"): (
        "Tolerable: LOW spec_vague findings are common in prose. "
        "Consider if the recurred pattern warrants a new check."
    ),
}


def _suggest_action(severity: str, category: str) -> str:
    """Map a finding to a steering action suggestion."""
    return _STEERING_ACTIONS.get(
        (severity, category),
        f"Review this {severity} finding in category '{category}' and decide "
        f"whether to add a dedicated check in the per-phase pattern script."
    )


def get_steering_summary(
    db_path: str, phase: int, threshold: int = 3, last_n: int = 10
) -> Dict:
    """Return a summary of steering state for a phase:
    - total runs
    - verdict trend
    - recurring patterns (>= threshold)
    - top recurring categories
    """
    history = get_history(db_path, phase, last_n)
    patterns = detect_repeating_findings(db_path, threshold)
    # Filter patterns to those that appeared in the last N runs of this phase
    run_ids = {r["id"] for r in history}
    relevant_patterns = []
    if Path(db_path).exists():
        with _connect(db_path) as conn:
            for p in patterns:
                recent = conn.execute(
                    """SELECT COUNT(*) FROM findings
                    WHERE fingerprint = ? AND run_id IN ({})""".format(
                        ",".join("?" * len(run_ids)) if run_ids else "0"
                    ),
                    (p.fingerprint, *run_ids) if run_ids else (p.fingerprint,)
                ).fetchone()[0]
                if recent > 0:
                    relevant_patterns.append({
                        "fingerprint": p.fingerprint,
                        "category": p.category,
                        "severity": p.severity,
                        "sample_message": p.sample_message[:100],
                        "occurrences": p.occurrences,
                        "suggested_action": p.suggested_action,
                    })
    # Verdict trend
    verdicts = [r["verdict"] for r in history]
    verdict_counts = {v: verdicts.count(v) for v in set(verdicts)}
    return {
        "phase": phase,
        "total_runs_in_window": len(history),
        "verdict_trend": verdict_counts,
        "patterns_count": len(relevant_patterns),
        "patterns": relevant_patterns,
    }


# === DSL output ===

def steering_dsl(summary: Dict) -> str:
    """Format steering summary as swebok DSL fragment."""
    top_categories = [p["category"] for p in summary["patterns"][:3]]
    top_finding = summary["patterns"][0]["sample_message"] if summary["patterns"] else "none"
    return (
        f"steering:run_total={summary['total_runs_in_window']};;"
        f"steering:patterns_detected={summary['patterns_count']};;"
        f"steering:recurring_categories={','.join(top_categories) or 'none'};;"
        f"steering:top_finding={top_finding[:60]}"
    )


if __name__ == "__main__":
    # CLI: python3 -m adv-loop.steering <db_path> <command> [args]
    if len(sys.argv) < 3:
        print("Usage: python3 -m adv-loop.steering <db_path> <log|history|patterns|steer> [args]")
        sys.exit(1)
    db_path = sys.argv[1]
    cmd = sys.argv[2]
    if cmd == "history":
        phase = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        for r in get_history(db_path, phase):
            print(f"  P{phase} | {r['ts']} | {r['verdict']} | "
                  f"C={r['findings_crit']} H={r['findings_high']} "
                  f"M={r['findings_med']} L={r['findings_low']}")
    elif cmd == "patterns":
        threshold = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        for p in detect_repeating_findings(db_path, threshold):
            print(f"  [{p.occurrences}x] {p.severity} {p.category} | "
                  f"{p.sample_message[:80]}")
            print(f"    → {p.suggested_action}")
    elif cmd == "steer":
        phase = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        s = get_steering_summary(db_path, phase)
        print(f"Phase {phase}: {s['total_runs_in_window']} runs, "
              f"{s['patterns_count']} recurring patterns")
        for p in s["patterns"]:
            print(f"  [{p['occurrences']}x] {p['severity']} {p['category']}")
            print(f"    sample: {p['sample_message'][:80]}")
            print(f"    action: {p['suggested_action']}")
    elif cmd == "clear":
        phase = int(sys.argv[3]) if len(sys.argv) > 3 else None
        n = clear_history(db_path, phase)
        print(f"Cleared {n} runs")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
