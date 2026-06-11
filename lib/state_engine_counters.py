#!/usr/bin/env python3
"""state_engine_counters.py — Atomic counters (scalar + nested JSON phase).

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_counters import increment_lint, ...

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or use sys.modules lookup for sibling privates.
"""
import json
import re
import sqlite3
import sys
from state_engine_compat import _se

# JSON path SQLi protection: only allow alphanumeric + underscore
_SAFE_JSON_PATH_RE = re.compile(r'^[A-Za-z0-9_]+$')



# ===== Atomic counters =====

def _incr_scalar(key, delta=1, cap=None):
    """Atomic integer increment for a top-level state key.

    AUDIT-2026-06-01 FIX (CONC-XX): use SQLite UPSERT with a single SQL
    statement (`INSERT ... ON CONFLICT DO UPDATE`) instead of SELECT-then-
    UPDATE. SQLite guarantees this is atomic at the statement level — no
    BEGIN EXCLUSIVE retry loop needed for this path. This eliminates the
    race we saw under high external load (xargs -P10 with system contention).
    """
    se = _se()
    se._init_db()
    conn = None
    try:
        conn = se._open_raw()
        if cap is not None:
            sql = (
                "INSERT INTO state(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET "
                "value = CAST(MIN(CAST(value AS INTEGER) + ?, ?) AS TEXT)"
            )
            conn.execute(sql, (key, str(delta), delta, cap))
        else:
            sql = (
                "INSERT INTO state(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET "
                "value = CAST(CAST(value AS INTEGER) + ? AS TEXT)"
            )
            conn.execute(sql, (key, str(delta), delta))
        conn.commit()
        # Read back the new value
        row = conn.execute("SELECT value FROM state WHERE key = ?", (key,)).fetchone()
        return int(row[0]) if row and row[0] else 0
    except sqlite3.OperationalError as e:
        return se._translate_op_error(e, f"incr {key}") or 0
    finally:
        if conn is not None:
            try:
                conn.close()
            except (sqlite3.Error, OSError) as _e:
                se._log.debug("state_engine: secondary error during cleanup", exc_info=_e)


def _incr_nested_phase(key, subkey, phase="P6", delta=1):
    """Atomic increment of a counter nested inside the phase_data JSON.

    AUDIT-2026-06-01 FIX: uses SQLite's json_set + json_extract for atomic
    single-statement update on the JSON value. Falls back to SELECT-then-
    UPDATE inside _xact() retry loop if JSON1 is unavailable.
    """
    se = _se()
    se._init_db()
    # Validate phase and subkey to prevent JSON path SQLi
    if not _SAFE_JSON_PATH_RE.match(phase):
        raise ValueError(f"Invalid phase: {phase!r} (must match ^[A-Za-z0-9_]+$)")
    if not _SAFE_JSON_PATH_RE.match(subkey):
        raise ValueError(f"Invalid subkey: {subkey!r} (must match ^[A-Za-z0-9_]+$)")
    conn = None
    try:
        conn = se._open_raw()
        # Ensure the row exists with a sane default
        conn.execute(
            "INSERT OR IGNORE INTO state(key, value) VALUES(?, ?)",
            (key, '{}'),
        )
        # Atomic single-statement UPDATE using JSON1 functions
        path = f"$.{phase}.{subkey}"
        sql = (
            f"UPDATE state SET value = json_set("
            f"  CASE WHEN json_type(value, '{path}') IS NULL "
            f"       THEN json_set(value, '{path}', 0) "
            f"       ELSE value END, "
            f"  '{path}', "
            f"  COALESCE(CAST(json_extract(value, '{path}') AS INTEGER), 0) + ?) "
            f"WHERE key = ?"
        )
        conn.execute(sql, (delta, key))
        conn.commit()
        # Read back
        row = conn.execute(
            f"SELECT json_extract(value, '{path}') FROM state WHERE key = ?",
            (key,)
        ).fetchone()
        return int(row[0]) if row and row[0] is not None else 0
    except sqlite3.OperationalError as e:
        return se._translate_op_error(e, f"incr {key}.{phase}.{subkey}") or 0
    finally:
        if conn is not None:
            try:
                conn.close()
            except (sqlite3.Error, OSError) as _e:
                se._log.debug("state_engine: secondary error during cleanup", exc_info=_e)


def reset_aov_iterations():
    """Reset the P6 aov_iterations counter to 0."""
    se = _se()
    se._init_db()
    try:
        with se._xact() as conn:
            cur = conn.execute("SELECT value FROM state WHERE key = 'phase_data'")
            row = cur.fetchone()
            if row:
                try:
                    pd = json.loads(row[0])
                except json.JSONDecodeError:
                    pd = {}
            else:
                pd = {}
            if not isinstance(pd, dict):
                pd = {}
            pd.setdefault("P6", {})
            pd["P6"]["aov_iterations"] = 0
            conn.execute(
                "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                ("phase_data", json.dumps(pd)),
            )
        return True
    except (sqlite3.Error, ValueError, TypeError, KeyError, IndexError, AttributeError):
        return False


def increment_lint():
    return _incr_scalar("lint_attempts", 1)

def lint_attempts():
    se = _se()
    v = se.get("lint_attempts")
    return int(v) if v else 0

def reset_lint():
    se = _se()
    return se.set("lint_attempts", "0")

def increment_aov_iterations():
    return _incr_nested_phase("phase_data", "aov_iterations", "P6", 1)

def get_aov_iterations():
    se = _se()
    v = se.get("phase_data.P6.aov_iterations")
    try:
        return int(v) if v else 0
    except (TypeError, ValueError):
        return 0

def increment_heal_iterations():
    return _incr_nested_phase("phase_data", "heal_iterations", "P6", 1)

def get_heal_iterations():
    se = _se()
    v = se.get("phase_data.P6.heal_iterations")
    try:
        return int(v) if v else 0
    except (TypeError, ValueError):
        return 0

def increment_tool_calls():
    return _incr_scalar("tool_call_count", 1)

def get_tool_call_count():
    se = _se()
    v = se.get("tool_call_count")
    return int(v) if v else 0

def should_run_continuity():
    n = get_tool_call_count()
    return n > 0 and n % 5 == 0

def hot_path_decision():
    """Return FULL or LITE based on the current intent.

    LITE → intent=micro_task (skip heavy validation, fast path).
    FULL → anything else (normal path).
    """
    se = _se()
    intent = se.get("intent")
    return "LITE" if intent == "micro_task" else "FULL"

def set_intent(intent, confidence=0.0):
    se = _se()
    a = se.set("intent", str(intent))
    b = se.set("intent_confidence", str(confidence))
    return a and b
