#!/usr/bin/env python3
"""state_engine_prune.py — Crash-safe prune (per I1).

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_prune import prune_log_events, ...

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or use sys.modules lookup for sibling privates.
"""
import os
import sqlite3
import sys
import time


def _se():
    """Lazy accessor: returns the state_engine module without triggering a
    circular import at our module-load time."""
    return sys.modules.get('state_engine') or __import__('state_engine')


def _prune_with_trigger(table, trigger_name, keep_last):
    """Crash-safe prune. Uses autocommit DDL semantics for DROP/CREATE
    (so the DROP propagates before the DELETE). If killed mid-sequence,
    _init_db restores the trigger via _ensure_triggers on next startup (I1).
    """
    se = _se()
    conn = sqlite3.connect(str(se.STATE_DB), timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"PRAGMA busy_timeout={se._BUSY_TIMEOUT_MS}")
    try:
        conn.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
        try:
            cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
            total = cur.fetchone()[0]
            deleted = 0
            if total > keep_last:
                cur = conn.execute(
                    f"DELETE FROM {table} WHERE id IN "
                    f"(SELECT id FROM {table} ORDER BY id ASC LIMIT ?)",
                    (total - keep_last,)
                )
                deleted = cur.rowcount
            conn.commit()
            return deleted
        finally:
            try:
                conn.execute(
                    f"CREATE TRIGGER IF NOT EXISTS {trigger_name} "
                    f"BEFORE DELETE ON {table} "
                    f"BEGIN SELECT RAISE(ABORT, "
                    f"'{table} is append-only; drop the trigger for maintenance purge'); "
                    f"END"
                )
                conn.commit()
            except (sqlite3.Error, OSError) as _e:
                se._log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    finally:
        conn.close()


def prune_log_events(keep_last=10000):
    se = _se()
    se._init_db()
    try:
        n = _prune_with_trigger("log_events", "trg_log_events_no_delete", keep_last)
        if n > 0:
            se.recompute_audit_chain("log_events")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_log_events blocked: {e}", file=sys.stderr)
        return -1


def prune_state_events(keep_last=10000):
    se = _se()
    se._init_db()
    try:
        n = _prune_with_trigger("state_events", "trg_state_events_no_delete", keep_last)
        if n > 0:
            se.recompute_audit_chain("state_events")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_state_events blocked: {e}", file=sys.stderr)
        return -1


def prune_circuit_breaker_events(keep_last=1000):
    se = _se()
    se._init_db()
    try:
        n = _prune_with_trigger(
            "circuit_breaker_events",
            "trg_circuit_breaker_events_no_delete",
            keep_last,
        )
        if n > 0:
            se.recompute_audit_chain("circuit_breaker_events")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_cb_events blocked: {e}", file=sys.stderr)
        return -1


def prune_adversarial(keep_last=10000):
    se = _se()
    se._init_db()
    try:
        n = _prune_with_trigger(
            "adversarial_log",
            "trg_adversarial_log_no_delete",
            keep_last,
        )
        if n > 0:
            se.recompute_audit_chain("adversarial_log")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_adversarial blocked: {e}", file=sys.stderr)
        return -1


def prune_backup_files(keep_last=3):
    """R2: keep only the N most recent .swebok_state.db.bak.* files."""
    se = _se()
    try:
        backups = sorted(
            se.HARNESS_DIR.glob(".swebok_state.db.bak.*"),
            key=lambda p: int(p.name.rsplit(".", 1)[-1])
                          if p.name.rsplit(".", 1)[-1].isdigit() else 0,
        )
        if len(backups) <= keep_last:
            return 0
        to_remove = backups[:-keep_last] if keep_last > 0 else backups
        removed = 0
        for old in to_remove:
            try:
                old.unlink()
                removed += 1
            except (sqlite3.Error, OSError) as _e:
                se._log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        return removed
    except Exception:
        return 0
