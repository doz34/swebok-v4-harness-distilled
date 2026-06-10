#!/usr/bin/env python3
"""state_engine_logging.py — Logging API (log_event, log_tool_call, log_adversarial, query_*).

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_logging import log_event, log_tool_call, ...
"""
import json
import sqlite3
import time

import state_engine  # sibling module, shares _open, _log, _audit_hmac
# Pull in private helpers that the logging functions need.
_init_db = state_engine._init_db
_open = state_engine._open
_log = state_engine._log
_audit_hmac = state_engine._audit_hmac
_translate_op_error = state_engine._translate_op_error
# ===== Logging =====

def log_tool_call(component, tool_name, phase=None, metadata=None):
    return log_event("INFO", component, f"tool_call:{tool_name}", phase, metadata)


def log_event(level, component, message, phase=None, metadata=None):
    _init_db()
    try:
        with _xact() as conn:
            md = json.dumps(metadata) if isinstance(metadata, dict) else (metadata or "")
            sid, agent, cid = _session_correlation()
            ts = _now_iso()
            row_hmac = _audit_hmac(
                _last_hmac(conn, "log_events"),
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
    _init_db()
    conn = _open()
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
    _init_db()
    try:
        with _xact() as conn:
            sid, agent, cid = _session_correlation()
            ts = _now_iso()
            row_hmac = _audit_hmac(
                _last_hmac(conn, "adversarial_log"),
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
    _init_db()
    conn = _open()
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
    _init_db()
    conn = _open()
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
    _init_db()
    conn = _open()
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
