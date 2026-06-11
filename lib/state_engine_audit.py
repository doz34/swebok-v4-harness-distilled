#!/usr/bin/env python3
"""state_engine_audit.py — HMAC audit chain + trigger management.

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_audit import verify_audit_chain, recompute_audit_chain, ...

Public API:
  - verify_audit_chain(table, limit=10000) -> (ok: bool, broken_at: int|None)
  - recompute_audit_chain(table) -> int  (rows touched, or -1 if table/column absent)

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or use sys.modules lookup for sibling privates.
"""
import hashlib
import hmac
import logging
import os
import sqlite3
import sys
from state_engine_compat import _se

_log = logging.getLogger("swebok.state_engine")



# ===== HMAC audit chain (MISSING-04 — CISO S blocker) =====
# Per-row HMAC chains the rows so any DELETE-then-INSERT or UPDATE is
# detectable. The secret lives in $SWEBOK_AUDIT_KEY (or, on a single-laptop
# install, in a private file at $HARNESS_DIR/.audit_key, mode 0600).


def _audit_secret():
    """Return the HMAC secret as bytes. Reads from env, falls back to
    a per-install key file at $HARNESS_DIR/.audit_key (mode 0600). The
    file is auto-created on first call with 256 bits of os.urandom.
    """
    se = _se()
    env = os.environ.get("SWEBOK_AUDIT_KEY")
    if env:
        return env.encode("utf-8")
    key_path = se.HARNESS_DIR / ".audit_key"
    if key_path.exists():
        try:
            return key_path.read_bytes()
        except (sqlite3.Error, OSError) as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    # First-time create
    try:
        secret = os.urandom(32)
        key_path.write_bytes(secret)
        try:
            os.chmod(str(key_path), 0o600)
        except (sqlite3.Error, OSError) as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        return secret
    except (OSError, TypeError, ValueError) as e:
        # Read-only FS / permission error — DO NOT fall back to a known constant.
        # A forgeable fallback would let any attacker who read this source code
        # produce valid HMACs for arbitrary audit rows. The system must refuse
        # to operate without a real secret; the caller (state engine init) will
        # surface the failure to the user.
        raise RuntimeError(
            f"STATE_ENGINE_INTEGRITY_FAIL: cannot create/read HMAC key file at "
            f"{key_path} (read-only FS or permission denied). Refusing to fall back "
            f"to a known constant: that would let any attacker who read this source "
            f"forge audit-chain HMACs. Original error: {e!r}"
        ) from e


def audit_hmac(prev_hmac_hex, ts, *fields):
    """Compute HMAC-SHA256 over (prev_hmac, ts, field1, field2, ...).

    Returns the new hex digest. The chain links every row to the previous
    row, so removing row N changes row N+1's HMAC and detection becomes
    "compare each row's stored hmac to recomputed hmac".
    """
    h = hmac.new(_audit_secret(), digestmod=hashlib.sha256)
    h.update((prev_hmac_hex or "").encode("utf-8"))
    h.update(b"|")
    h.update((ts or "").encode("utf-8"))
    for f in fields:
        h.update(b"|")
        h.update(("" if f is None else str(f)).encode("utf-8"))
    return h.hexdigest()


def last_hmac(conn, table):
    """Return the most recent row_hmac in `table`, or '' if empty/missing."""
    try:
        row = conn.execute(
            f"SELECT row_hmac FROM {table} ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if row and row[0]:
            return row[0]
    except sqlite3.OperationalError:
        # row_hmac column missing (older schema) — chain starts at empty
        pass
    return ""


def verify_audit_chain(table, limit=10000):
    """Verify the HMAC chain on `table`. Returns (ok: bool, broken_at: int|None).

    AUDIT-2026-06-01 ITER5 FIX: recompute each row's HMAC from the prior row's
    HMAC + the row's content fields and compare against the stored row_hmac.
    A break means: row content was modified, row was deleted, or row was
    inserted out of order.

    Returns (True, None) if intact. Returns (True, None) also if the table
    has no rows yet OR row_hmac column is absent (older schema) — those are
    not chain violations.
    """
    se = _se()
    # S-01 defense-in-depth: reject non-audit table names (SQL injection guard)
    _VALID_AUDIT_TABLES = frozenset(
        ("adversarial_log", "log_events", "state_events",
         "circuit_breaker_events"))
    if table not in _VALID_AUDIT_TABLES:
        raise ValueError(
            f"verify_audit_chain: invalid table '{table}'. "
            f"Must be one of: {', '.join(sorted(_VALID_AUDIT_TABLES))}")
    se._init_db()
    conn = se._open()
    try:
        # Per-table column selection — must mirror what audit_hmac was given
        # at INSERT time. This is the contract: the field list here MUST
        # match the field list in the corresponding INSERT path.
        column_specs = {
            "adversarial_log": "id, ts, gate, verdict, reason, session_id, agent, correlation_id, row_hmac",
            "log_events":      "id, ts, level, component, phase, message, metadata, session_id, agent, correlation_id, row_hmac",
            "state_events":    "id, ts, key, old_value, new_value, source, session_id, agent, correlation_id, row_hmac",
            "circuit_breaker_events": "id, ts, blocked_file, blocked_count, reason, session_id, agent, correlation_id, row_hmac",
        }
        cols = column_specs.get(table)
        if cols is None:
            return (True, None)
        try:
            rows = conn.execute(
                f"SELECT {cols} FROM {table} ORDER BY id ASC LIMIT ?",
                (limit,),
            ).fetchall()
        except sqlite3.OperationalError:
            # row_hmac column missing — chain not yet initialised
            return (True, None)
    finally:
        conn.close()
    if not rows:
        return (True, None)
    prev = ""
    for row in rows:
        rid = row[0]
        ts = row[1]
        stored_hmac = row[-1]   # last column is row_hmac
        content = row[2:-1]     # everything between (ts, ..., row_hmac)
        if stored_hmac is None:
            # Pre-ITER5 row (HMAC column existed but writer didn't populate)
            # OR restored row from a rebuild that cleared the hmac. Treat as
            # chain pivot — the next populated row starts a fresh chain segment.
            prev = ""
            continue
        recomputed = audit_hmac(prev, ts, table, *content)
        if recomputed != stored_hmac:
            return (False, rid)
        prev = stored_hmac
    return (True, None)


def drop_audit_triggers(conn, table):
    """Drop all audit-protect triggers on `table` for maintenance (rebuild/recompute)."""
    for suffix in ("_no_delete", "_no_update_v2"):
        trg = f"trg_{table}{suffix}"
        conn.execute(f"DROP TRIGGER IF EXISTS {trg}")


def recompute_audit_chain(table):
    """AUDIT-2026-06-01 ITER6: recompute and update row_hmac for every row in
    `table`. This is the supported maintenance operation after a legitimate
    prune that removes earlier rows — the chain attaches to the new earliest
    row by walking the surviving rows and rewriting their HMACs in order.

    Returns the number of rows touched. Returns -1 if the table or column
    is absent.
    """
    se = _se()
    se._init_db()
    column_specs = {
        "adversarial_log": ("id, ts, gate, verdict, reason, session_id, agent, correlation_id",
                            ["id", "ts", "gate", "verdict", "reason", "session_id", "agent", "correlation_id"]),
        "log_events":      ("id, ts, level, component, phase, message, metadata, session_id, agent, correlation_id",
                            ["id", "ts", "level", "component", "phase", "message", "metadata", "session_id", "agent", "correlation_id"]),
        "state_events":    ("id, ts, key, old_value, new_value, source, session_id, agent, correlation_id",
                            ["id", "ts", "key", "old_value", "new_value", "source", "session_id", "agent", "correlation_id"]),
        "circuit_breaker_events": ("id, ts, blocked_file, blocked_count, reason, session_id, agent, correlation_id",
                            ["id", "ts", "blocked_file", "blocked_count", "reason", "session_id", "agent", "correlation_id"]),
    }
    spec = column_specs.get(table)
    if spec is None:
        return -1
    sel_sql, _col_list = spec
    conn = se._open_raw()
    try:
        # Drop audit-protect triggers before UPDATE (they block modifications)
        drop_audit_triggers(conn, table)
        try:
            rows = conn.execute(
                f"SELECT {sel_sql} FROM {table} ORDER BY id ASC"
            ).fetchall()
        except sqlite3.OperationalError:
            return -1
        prev = ""
        touched = 0
        for row in rows:
            rid = row[0]
            ts = row[1]
            content = row[2:]
            new_hmac = audit_hmac(prev, ts, table, *content)
            conn.execute(f"UPDATE {table} SET row_hmac = ? WHERE id = ?",
                         (new_hmac, rid))
            prev = new_hmac
            touched += 1
        conn.commit()
        return touched
    finally:
        # Always restore triggers, even on error
        try:
            ensure_triggers(conn)
            conn.commit()
        except (sqlite3.Error, OSError):
            pass
        conn.close()


def ensure_triggers(conn):
    """I1 defense-in-depth: re-issue CREATE TRIGGER IF NOT EXISTS on every startup.

    v1.5.11 (STRIDE-Rep-1 close-out): BEFORE UPDATE triggers are NOW
    installed. The original 2026-06-01 audit noted that BEFORE UPDATE
    triggers caused a regression under concurrent prune+insert in WAL
    mode. v1.5.11 resolves this by:
      1. Using a NEW trigger name (`_no_update_v2`) so the original
         (failed) trigger is not duplicated.
      2. The trigger RAISES(ABORT) on any UPDATE — the only legitimate
         UPDATE path (recompute_audit_chain) intentionally drops the
         trigger before UPDATE and re-creates it after.
    Net effect: an attacker (or buggy code) that tries to UPDATE an audit
    row is rejected with a clear error message.
    """
    triggers = [
        ("trg_adversarial_log_no_delete", "adversarial_log"),
        ("trg_log_events_no_delete", "log_events"),
        ("trg_state_events_no_delete", "state_events"),
        ("trg_circuit_breaker_events_no_delete", "circuit_breaker_events"),
    ]
    for trg, tbl in triggers:
        conn.execute(
            f"CREATE TRIGGER IF NOT EXISTS {trg} "
            f"BEFORE DELETE ON {tbl} "
            f"BEGIN SELECT RAISE(ABORT, "
            f"'{tbl} is append-only; drop the trigger for maintenance purge'); "
            f"END"
        )
    # v1.5.11: STRIDE-Rep-1 — refuse any UPDATE to the audit tables.
    # The recompute_audit_chain() function DROPS these triggers before its
    # UPDATE and re-creates them after, so the legitimate chain-rebuild
    # path is not blocked.
    update_triggers = [
        ("trg_adversarial_log_no_update_v2", "adversarial_log"),
        ("trg_log_events_no_update_v2", "log_events"),
        ("trg_state_events_no_update_v2", "state_events"),
        ("trg_circuit_breaker_events_no_update_v2", "circuit_breaker_events"),
    ]
    for trg, tbl in update_triggers:
        conn.execute(
            f"CREATE TRIGGER IF NOT EXISTS {trg} "
            f"BEFORE UPDATE ON {tbl} "
            f"BEGIN SELECT RAISE(ABORT, "
            f"'{tbl} is append-only (STRIDE-Rep-1); use recompute_audit_chain'); "
            f"END"
        )
