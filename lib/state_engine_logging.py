#!/usr/bin/env python3
"""state_engine_logging.py — Logging API (log_event, log_tool_call, log_adversarial, query_*).

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_logging import log_event, log_tool_call, ...

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or use sys.modules lookup for sibling privates.
"""
import json
import sqlite3
import sys
import time


def _se():
    """Lazy accessor: returns the state_engine module without triggering a
    circular import at our module-load time."""
    return sys.modules.get('state_engine') or __import__('state_engine')


# ===== Logging =====

def log_tool_call(component, tool_name, phase=None, metadata=None):
    return log_event("INFO", component, f"tool_call:{tool_name}", phase, metadata)


def log_event(level, component, message, phase=None, metadata=None):
    se = _se()
    se._init_db()
    try:
        with se._xact() as conn:
            md = json.dumps(metadata) if isinstance(metadata, dict) else (metadata or "")
            sid, agent, cid = se._session_correlation()
            ts = se._now_iso()
            row_hmac = se._audit_hmac(
                se._last_hmac(conn, "log_events"),
                ts, "log_events", level, component, phase, message, md, sid, agent, cid,
            )
            conn.execute(
                "INSERT INTO log_events "
                "(ts, level, component, phase, message, metadata, session_id, agent, correlation_id, row_hmac) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ts, level, component, phase, message, md, sid, agent, cid, row_hmac),
            )
        return True
    except Exception:
        return False


def query_log_events(limit=100, level=None, since_date=None, component=None):
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        conds, params = [], []
        if level:
            conds.append("level = ?")
            params.append(level)
        if component:
            conds.append("component = ?")
            params.append(component)
        if since_date:
            conds.append("ts >= ?")
            params.append(since_date)
        where = ("WHERE " + " AND ".join(conds)) if conds else ""
        params.append(limit)
        cur = conn.execute(
            f"SELECT id, ts, level, component, phase, message, metadata "
            f"FROM log_events {where} ORDER BY id DESC LIMIT ?",
            params,
        )
        return cur.fetchall()
    finally:
        conn.close()


def log_adversarial(gate, verdict, reason):
    se = _se()
    se._init_db()
    try:
        with se._xact() as conn:
            sid, agent, cid = se._session_correlation()
            ts = se._now_iso()
            row_hmac = se._audit_hmac(
                se._last_hmac(conn, "adversarial_log"),
                ts, "adversarial_log", gate, verdict, reason, sid, agent, cid,
            )
            conn.execute(
                "INSERT INTO adversarial_log "
                "(ts, gate, verdict, reason, session_id, agent, correlation_id, row_hmac) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (ts, gate, verdict, reason, sid, agent, cid, row_hmac),
            )
        return True
    except Exception:
        return False


def query_adversarial(limit=100, since_date=None):
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        if since_date:
            cur = conn.execute(
                "SELECT id, ts, gate, verdict, reason FROM adversarial_log "
                "WHERE ts >= ? ORDER BY id DESC LIMIT ?",
                (since_date, limit),
            )
        else:
            cur = conn.execute(
                "SELECT id, ts, gate, verdict, reason FROM adversarial_log "
                "ORDER BY id DESC LIMIT ?",
                (limit,),
            )
        return cur.fetchall()
    finally:
        conn.close()


def query_state_events(limit=100, key_filter=None, since_date=None):
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        conds, params = [], []
        if key_filter:
            conds.append("key = ?")
            params.append(key_filter)
        if since_date:
            conds.append("ts >= ?")
            params.append(since_date)
        where = ("WHERE " + " AND ".join(conds)) if conds else ""
        params.append(limit)
        cur = conn.execute(
            f"SELECT id, ts, key, old_value, new_value, source FROM state_events "
            f"{where} ORDER BY id DESC LIMIT ?",
            params,
        )
        return cur.fetchall()
    finally:
        conn.close()


def query_circuit_breaker_events(limit=100, since_date=None):
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        if since_date:
            cur = conn.execute(
                "SELECT id, ts, blocked_file, blocked_count, reason "
                "FROM circuit_breaker_events WHERE ts >= ? "
                "ORDER BY id DESC LIMIT ?",
                (since_date, limit),
            )
        else:
            cur = conn.execute(
                "SELECT id, ts, blocked_file, blocked_count, reason "
                "FROM circuit_breaker_events ORDER BY id DESC LIMIT ?",
                (limit,),
            )
        return cur.fetchall()
    finally:
        conn.close()
