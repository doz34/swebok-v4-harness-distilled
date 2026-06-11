"""state_engine_gates.py — Gate lifecycle (append_gate).

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_gates import append_gate

Public API:
  - append_gate(gate_name) -> bool  (idempotent add to gates_validated[]; returns True on success)

`append_gate` is the single mutation point for the `gates_validated[]` list in
the `state` table. It is idempotent (re-adding the same gate is a no-op)
and audit-trailed: every successful append writes a row to `state_events`
with an HMAC chained to the previous row.

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or the shared ``_se()`` accessor for sibling privates.
"""

from __future__ import annotations

import json
import sqlite3
from state_engine_compat import _se


def append_gate(gate_name):
    """Append ``gate_name`` to the `gates_validated[]` state list (idempotent).

    Returns ``True`` on successful commit, ``False`` if the input is empty
    or the database write fails for any expected reason. Unexpected errors
    propagate.
    """
    if not gate_name:
        return False
    se = _se()
    se._init_db()
    try:
        with se._xact() as conn:
            cur = conn.execute("SELECT value FROM state WHERE key = 'gates_validated'")
            row = cur.fetchone()
            gates = []
            if row and row[0]:
                try:
                    gates = json.loads(row[0])
                except json.JSONDecodeError:
                    gates = []
            if not isinstance(gates, list):
                gates = []
            if gate_name not in gates:
                gates.append(gate_name)
            conn.execute(
                "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                ("gates_validated", json.dumps(gates)),
            )
            sid, agent, cid = se._session_correlation()
            ts = se._now_iso()
            old_val = row[0] if row else None
            new_val = json.dumps(gates)
            row_hmac = se.audit_hmac(
                se.last_hmac(conn, "state_events"),
                ts, "state_events", "gates_validated", old_val, new_val,
                "append_gate", sid, agent, cid,
            )
            conn.execute(
                "INSERT INTO state_events "
                "(ts, key, old_value, new_value, source, session_id, agent, correlation_id, row_hmac) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ts, "gates_validated", old_val, new_val,
                 "append_gate", sid, agent, cid, row_hmac),
            )
        return True
    except (sqlite3.Error, ValueError, TypeError, KeyError, IndexError, AttributeError, json.JSONDecodeError):
        return False


__all__ = ["append_gate"]
