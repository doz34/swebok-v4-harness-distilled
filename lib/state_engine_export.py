#!/usr/bin/env python3
"""state_engine_export.py — JSON export of state + audit tables.

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_export import export_state, export_audit

Public API:
  - export_state() -> str  (JSON dump of the state table, parsed)
  - export_audit(limit=10000) -> str  (JSON dump of all 4 audit tables)

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or use sys.modules lookup for sibling privates.
"""
import json
import logging
import sys
from state_engine_compat import _se

_log = logging.getLogger("swebok.state_engine")



# ===== Export =====

def export_state():
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        cur = conn.execute("SELECT key, value FROM state")
        out = {}
        for row in cur.fetchall():
            try:
                out[row[0]] = json.loads(row[1])
            except (json.JSONDecodeError, TypeError):
                out[row[0]] = row[1]
        return json.dumps(out, indent=2, sort_keys=True, default=str)
    finally:
        conn.close()


def export_audit(limit=10000):
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        out = {}
        for tbl in ("adversarial_log", "log_events",
                    "state_events", "circuit_breaker_events"):
            cur = conn.execute(
                f"SELECT * FROM {tbl} ORDER BY id ASC LIMIT ?",
                (limit,),
            )
            cols = [d[0] for d in cur.description]
            out[tbl] = [dict(zip(cols, row)) for row in cur.fetchall()]
        return json.dumps(out, indent=2, sort_keys=True, default=str)
    finally:
        conn.close()
