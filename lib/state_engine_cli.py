#!/usr/bin/env python3
# SWEBOK v4 Harness — State Engine CLI
#
# AUDIT-2026-06-01 ITER6 (Architect S blocker): extracted from state_engine.py
# per ADR-001's named seam (the CLI dispatcher was identified as a clean
# extraction point). This brings the state engine logic module under the
# 1100-LOC threshold and keeps the CLI as a thin argv-to-API translator.

import sys
import sqlite3
from pathlib import Path

# Ensure sibling modules are importable regardless of invocation method
_this_dir = str(Path(__file__).resolve().parent)
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

import state_engine as se


def main():
    if len(sys.argv) < 2:
        print("usage: state_engine.py <cmd> [args...]", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    try:
        if cmd == "get":
            print(se.get(sys.argv[2]))
        elif cmd == "set":
            ok = se.set(sys.argv[2], sys.argv[3],
                        sys.argv[4] if len(sys.argv) > 4 else "cli")
            sys.exit(0 if ok else 1)
        elif cmd == "increment_lint":
            print(se.increment_lint())
        elif cmd == "lint_attempts":
            print(se.lint_attempts())
        elif cmd == "reset_lint":
            se.reset_lint()
        elif cmd == "increment_aov_iterations":
            print(se.increment_aov_iterations())
        elif cmd == "get_aov_iterations":
            print(se.get_aov_iterations())
        elif cmd == "reset_aov_iterations":
            ok = se.reset_aov_iterations()
            sys.exit(0 if ok else 1)
        elif cmd == "increment_nested":
            # ITER7: generic nested-counter increment for test isolation.
            # CLI: increment_nested <key> <phase> <subkey> [delta]
            key = sys.argv[2]
            phase = sys.argv[3]
            subkey = sys.argv[4]
            delta = int(sys.argv[5]) if len(sys.argv) > 5 else 1
            print(se._incr_nested_phase(key, subkey, phase, delta))
        elif cmd == "get_nested":
            # CLI: get_nested <key.path.dot.notation>
            print(se.get(sys.argv[2]))
        elif cmd == "set_nested":
            # CLI: set_nested <key.path> <value>
            ok = se.set(sys.argv[2], sys.argv[3], "test_iso")
            sys.exit(0 if ok else 1)
        elif cmd == "increment_heal_iterations":
            print(se.increment_heal_iterations())
        elif cmd == "get_heal_iterations":
            print(se.get_heal_iterations())
        elif cmd == "increment_tool_calls":
            print(se.increment_tool_calls())
        elif cmd == "get_tool_call_count":
            print(se.get_tool_call_count())
        elif cmd == "hot_path_decision":
            print(se.hot_path_decision())
        elif cmd == "set_intent":
            ok = se.set_intent(sys.argv[2],
                               float(sys.argv[3]) if len(sys.argv) > 3 else 0.0)
            sys.exit(0 if ok else 1)
        elif cmd == "increment_blocked":
            print(se.increment_blocked(sys.argv[2] if len(sys.argv) > 2 else "",
                                       sys.argv[3] if len(sys.argv) > 3 else "blocked"))
        elif cmd == "record_block":
            print(se.record_block(sys.argv[2] if len(sys.argv) > 2 else "",
                                  sys.argv[3] if len(sys.argv) > 3 else "blocked"))
        elif cmd == "reset_all_circuits":
            ok = se.reset_all_circuits(sys.argv[2] if len(sys.argv) > 2 else None)
            sys.exit(0 if ok else 1)
        elif cmd == "log_event":
            ok = se.log_event(sys.argv[2], sys.argv[3], sys.argv[4],
                              sys.argv[5] if len(sys.argv) > 5 else None)
            sys.exit(0 if ok else 1)
        elif cmd == "log_adversarial":
            ok = se.log_adversarial(sys.argv[2], sys.argv[3], sys.argv[4])
            sys.exit(0 if ok else 1)
        elif cmd == "append_gate":
            ok = se.append_gate(sys.argv[2])
            sys.exit(0 if ok else 1)
        elif cmd == "prune_log_events":
            print(se.prune_log_events(int(sys.argv[2]) if len(sys.argv) > 2 else 10000))
        elif cmd == "prune_state_events":
            print(se.prune_state_events(int(sys.argv[2]) if len(sys.argv) > 2 else 10000))
        elif cmd == "prune_circuit_breaker_events":
            print(se.prune_circuit_breaker_events(int(sys.argv[2]) if len(sys.argv) > 2 else 1000))
        elif cmd == "prune_adversarial":
            print(se.prune_adversarial(int(sys.argv[2]) if len(sys.argv) > 2 else 10000))
        elif cmd == "prune_backup_files":
            print(se.prune_backup_files(int(sys.argv[2]) if len(sys.argv) > 2 else 3))
        elif cmd == "rebuild":
            ok = se.rebuild(keep_audit=(sys.argv[2] != "no") if len(sys.argv) > 2 else True)
            sys.exit(0 if ok else 1)
        elif cmd == "check_integrity":
            print(se.check_integrity())
        elif cmd == "verify_audit_chain":
            _AUDIT_TABLES = frozenset(
                ["adversarial_log", "log_events",
                 "state_events", "circuit_breaker_events"])
            if len(sys.argv) > 2:
                t = sys.argv[2]
                if t not in _AUDIT_TABLES:
                    print(f"ERROR: invalid table '{t}'. "
                          f"Must be one of: {', '.join(sorted(_AUDIT_TABLES))}",
                          file=sys.stderr)
                    sys.exit(1)
                tables = [t]
            else:
                tables = sorted(_AUDIT_TABLES)
            any_broken = False
            for t in tables:
                ok, broken_at = se.verify_audit_chain(t)
                if ok:
                    print(f"{t}: ok")
                else:
                    print(f"{t}: BROKEN at row {broken_at}")
                    any_broken = True
            sys.exit(1 if any_broken else 0)
        elif cmd == "self_audit":
            # G.2 (ADR-003): one-shot self-audit; optional --council flag emits
            # the multiagent bridge envelope so the dispatcher can spawn the
            # 4 Nexus reviewers. Honors --since-days N for the window.
            council = "--council" in sys.argv[2:]
            since_days = 30
            for i, a in enumerate(sys.argv[2:], start=2):
                if a == "--since-days" and i + 1 < len(sys.argv):
                    try:
                        since_days = int(sys.argv[i + 1])
                    except ValueError:
                        pass
            report = se.self_audit(council=council, since_days=since_days)
            print(report)
        elif cmd == "export_state":
            print(se.export_state())
        elif cmd == "export_audit":
            print(se.export_audit(int(sys.argv[2]) if len(sys.argv) > 2 else 10000))
        elif cmd == "should_run_continuity":
            print("YES" if se.should_run_continuity() else "NO")
        elif cmd == "query_adversarial":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            since = sys.argv[3] if len(sys.argv) > 3 else None
            for r in se.query_adversarial(limit, since):
                print("\t".join(str(c) if c is not None else "" for c in r))
        elif cmd == "query_state_events":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            key = sys.argv[3] if len(sys.argv) > 3 else None
            since = sys.argv[4] if len(sys.argv) > 4 else None
            for r in se.query_state_events(limit, key, since):
                print("\t".join(str(c) if c is not None else "" for c in r))
        elif cmd == "query_circuit_breaker_events":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            since = sys.argv[3] if len(sys.argv) > 3 else None
            for r in se.query_circuit_breaker_events(limit, since):
                print("\t".join(str(c) if c is not None else "" for c in r))
        elif cmd == "query_log_events":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            level = sys.argv[3] if len(sys.argv) > 3 else None
            since = sys.argv[4] if len(sys.argv) > 4 else None
            for r in se.query_log_events(limit, level, since):
                print("\t".join(str(c) if c is not None else "" for c in r))
        elif cmd == "metrics":
            # ITER6 DevOps S: cheap metrics view
            se._init_db()
            conn = se._open()
            try:
                rows = {}
                for tbl in ("adversarial_log", "log_events",
                            "state_events", "circuit_breaker_events"):
                    rows[tbl] = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
                cb = conn.execute("SELECT value FROM state WHERE key='circuit_breaker'").fetchone()
                phase = conn.execute("SELECT value FROM state WHERE key='current_phase'").fetchone()
                tc = conn.execute("SELECT value FROM state WHERE key='tool_call_count'").fetchone()
                print(f"current_phase: {phase[0] if phase else 'unset'}")
                print(f"tool_call_count: {tc[0] if tc else 0}")
                print(f"circuit_breaker: {cb[0] if cb else 'unset'}")
                for tbl, n in rows.items():
                    print(f"{tbl}_rows: {n}")
            finally:
                conn.close()
        elif cmd == "list_append":
            # SPRINT-2026-06-10 G3: append to a JSON-list state key with FIFO max.
            # CLI: list_append <key> <value> [max_len=10]
            import json
            key = sys.argv[2]
            value = sys.argv[3]
            max_len = int(sys.argv[4]) if len(sys.argv) > 4 else 10
            se._init_db()
            with se._xact() as conn:
                cur = conn.execute("SELECT value FROM state WHERE key = ?", (key,))
                row = cur.fetchone()
                items = []
                if row and row[0]:
                    try:
                        items = json.loads(row[0])
                    except (json.JSONDecodeError, TypeError):
                        items = []
                if not isinstance(items, list):
                    items = []
                items.append(value)
                # FIFO eviction
                if len(items) > max_len:
                    items = items[-max_len:]
                new_val = json.dumps(items)
                conn.execute(
                    "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                    (key, new_val),
                )
                # Audit
                sid, agent, cid = se._session_correlation()
                ts = se._now_iso()
                old_val = row[0] if row else None
                row_hmac = se._audit_hmac(
                    se._last_hmac(conn, "state_events"),
                    ts, "state_events", key, old_val, new_val,
                    "list_append", sid, agent, cid,
                )
                conn.execute(
                    "INSERT INTO state_events "
                    "(ts, key, old_value, new_value, source, session_id, agent, correlation_id, row_hmac) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (ts, key, old_val, new_val,
                     "list_append", sid, agent, cid, row_hmac),
                )
            print(new_val)
        elif cmd == "list_get":
            # SPRINT-2026-06-10 G3: read a JSON-list state key.
            # CLI: list_get <key>
            import json
            key = sys.argv[2]
            se._init_db()
            conn = se._open()
            try:
                cur = conn.execute("SELECT value FROM state WHERE key = ?", (key,))
                row = cur.fetchone()
                if not row or not row[0]:
                    print("[]")
                else:
                    try:
                        items = json.loads(row[0])
                        print(json.dumps(items if isinstance(items, list) else []))
                    except (json.JSONDecodeError, TypeError):
                        print("[]")
            finally:
                conn.close()
        elif cmd == "list_clear":
            # SPRINT-2026-06-10: clear a JSON-list state key.
            # CLI: list_clear <key>
            import json
            key = sys.argv[2]
            se._init_db()
            with se._xact() as conn:
                cur = conn.execute("SELECT value FROM state WHERE key = ?", (key,))
                row = cur.fetchone()
                old_val = row[0] if row else None
                conn.execute(
                    "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                    (key, json.dumps([])),
                )
                sid, agent, cid = se._session_correlation()
                ts = se._now_iso()
                row_hmac = se._audit_hmac(
                    se._last_hmac(conn, "state_events"),
                    ts, "state_events", key, old_val, "[]",
                    "list_clear", sid, agent, cid,
                )
                conn.execute(
                    "INSERT INTO state_events "
                    "(ts, key, old_value, new_value, source, session_id, agent, correlation_id, row_hmac) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (ts, key, old_val, "[]",
                     "list_clear", sid, agent, cid, row_hmac),
                )
            print("[]")
        else:
            print(f"unknown cmd: {cmd}", file=sys.stderr)
            sys.exit(1)
    except sqlite3.OperationalError as e:
        se._translate_op_error(e, f"cmd:{cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
