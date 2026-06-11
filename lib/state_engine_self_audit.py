#!/usr/bin/env python3
"""state_engine_self_audit.py — Quarterly self-audit report (ADR-003 / G.2).

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_self_audit import self_audit, replay_session

Public API:
  - self_audit(council=False, since_days=30) -> str  (markdown report; council=True adds MULTIAGENT_LAUNCH envelope)
  - replay_session(t0, t1) -> list  (all events in [t0, t1] window, ordered by ts)

self_audit() generates a markdown report summarising the harness's own
audit state — verdict counts, recent state transitions, circuit-breaker
activity, HMAC chain integrity. With council=True it ALSO emits a
<MULTIAGENT_LAUNCH> envelope on stdout so the dispatcher can spawn a
4-role review (CISO / QA-lead / Architect / DevOps-lead). The function
inserts a SELF_AUDIT row into adversarial_log so the audit cycle itself
is part of the chained record.

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or use sys.modules lookup for sibling privates.
"""
import logging
import os
import sqlite3
import sys

_log = logging.getLogger("swebok.state_engine")


def _se():
    """Lazy accessor: returns the state_engine module without triggering a
    circular import at our module-load time."""
    mod = sys.modules.get('state_engine')
    if mod is None:
        try:
            mod = __import__('state_engine')
        except ImportError:
            raise ImportError(
                "state_engine module not found. This sibling module must be "
                "imported through state_engine.py (which re-exports our symbols), "
                "not directly."
            )
    return mod


def replay_session(t0, t1):
    """Replay all events in [t0, t1] window, ordered by timestamp.

    Returns a list of rows: (src, id, ts, key/field, value, reason, meta).
    """
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        cur = conn.execute(
            """
            SELECT 'adversarial_log' AS src, id, ts, gate AS key, verdict, reason, NULL AS meta
            FROM adversarial_log WHERE ts >= ? AND ts <= ?
            UNION ALL
            SELECT 'log_events', id, ts, component, level, message, metadata
            FROM log_events WHERE ts >= ? AND ts <= ?
            UNION ALL
            SELECT 'state_events', id, ts, key, source, new_value, old_value
            FROM state_events WHERE ts >= ? AND ts <= ?
            UNION ALL
            SELECT 'circuit_breaker_events', id, ts, blocked_file, reason, blocked_count, NULL
            FROM circuit_breaker_events WHERE ts >= ? AND ts <= ?
            ORDER BY ts ASC
            """,
            (t0, t1, t0, t1, t0, t1, t0, t1),
        )
        return cur.fetchall()
    finally:
        conn.close()


def self_audit(council=False, since_days=30):
    """Generate the quarterly self-audit report.

    Args:
        council: when True, also emit a <MULTIAGENT_LAUNCH> envelope on stdout.
        since_days: window for the verdict / transition / circuit-breaker counts.

    Returns the report as a markdown string. The caller may print it.
    """
    se = _se()
    se._init_db()
    import datetime
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=since_days)).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    conn = se._open()
    try:
        # Verdict counts in window
        verdict_rows = conn.execute(
            "SELECT verdict, COUNT(*) FROM adversarial_log WHERE ts >= ? GROUP BY verdict",
            (cutoff,),
        ).fetchall()
        # State transition count
        try:
            transition_count = conn.execute(
                "SELECT COUNT(*) FROM state_events WHERE ts >= ? AND key = 'current_phase'",
                (cutoff,),
            ).fetchone()[0]
        except sqlite3.OperationalError:
            transition_count = 0
        # Circuit-breaker activity
        try:
            cb_rows = conn.execute(
                "SELECT blocked_file, COUNT(*) FROM circuit_breaker_events "
                "WHERE ts >= ? GROUP BY blocked_file ORDER BY COUNT(*) DESC LIMIT 10",
                (cutoff,),
            ).fetchall()
        except sqlite3.OperationalError:
            cb_rows = []
        # Audit table row counts
        table_counts = {}
        for tbl in ("adversarial_log", "log_events", "state_events",
                    "circuit_breaker_events"):
            try:
                table_counts[tbl] = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            except sqlite3.OperationalError:
                table_counts[tbl] = -1
    finally:
        conn.close()
    # HMAC chain integrity (uses public verify_audit_chain — no inline dup)
    chain_status = {}
    for tbl in ("adversarial_log", "log_events", "state_events",
                "circuit_breaker_events"):
        ok, broken_at = se.verify_audit_chain(tbl)
        chain_status[tbl] = "ok" if ok else f"BROKEN at row {broken_at}"
    # Build markdown
    lines = [
        f"# Self-audit — {se._now_iso()}",
        "",
        f"Window: last {since_days} days (since {cutoff})",
        "",
        "## Verdict counts (adversarial_log)",
    ]
    if verdict_rows:
        for verdict, n in verdict_rows:
            lines.append(f"- `{verdict}`: {n}")
    else:
        lines.append("- (none in window)")
    lines.extend([
        "",
        f"## Phase transitions: {transition_count}",
        "",
        "## Top blocked files (circuit_breaker_events)",
    ])
    if cb_rows:
        for f, n in cb_rows:
            lines.append(f"- `{f}`: {n}")
    else:
        lines.append("- (none in window)")
    lines.extend([
        "",
        "## Audit table sizes",
    ])
    for tbl, n in table_counts.items():
        lines.append(f"- `{tbl}`: {n}")
    lines.extend([
        "",
        "## HMAC chain integrity",
    ])
    for tbl, status in chain_status.items():
        lines.append(f"- `{tbl}`: {status}")
    lines.append("")
    # Council envelope (opt-in)
    if council:
        env = os.environ.get("MULTIAGENT_BRIDGE_ENABLED", "")
        if env != "1":
            lines.append("> NOTE: --council requested but MULTIAGENT_BRIDGE_ENABLED is not set.")
            lines.append("> Emitting the bridge envelope anyway for the dispatcher to discover.")
            lines.append("")
        lines.extend([
            "## <MULTIAGENT_LAUNCH>",
            "",
            "Spawn each of the 4 Nexus reviewers via the Agent tool, then re-invoke:",
            "  bash scripts/multiagent-launcher.sh emit-prompts SELF_AUDIT",
            "",
            "Roles: nexus-ciso, nexus-qa-lead, nexus-architect, nexus-devops-lead.",
            "Expected DSL output keys: RED:VULN, RED:LOC, RED:TYPE, RED:FIX_REQ, BLUE:STATUS.",
            "",
        ])
    report = "\n".join(lines)
    # Persist the audit row through the chained-write path (preserves HMAC).
    try:
        se.log_adversarial(
            "SELF_AUDIT",
            "PASS",
            f"window={since_days}d verdicts={len(verdict_rows)} chains_ok={sum(1 for s in chain_status.values() if s == 'ok')}/4",
        )
    except (sqlite3.Error, OSError) as _e:
        _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    return report
