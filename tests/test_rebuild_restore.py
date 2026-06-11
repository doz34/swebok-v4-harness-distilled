#!/usr/bin/env python3
"""Test: rebuild() preserves audit data across a full rebuild cycle.

This regression test prevents re-introduction of the CRIT D1 bug
(d[0] vs d[1] in PRAGMA table_info) that silently lost all audit data.

Run: python3 tests/test_rebuild_restore.py
"""
import json
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

# Ensure lib/ is on path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
import state_engine

PASSED = 0
FAILED = 0

def log_pass(name):
    global PASSED
    PASSED += 1
    print(f"✓ {name}")

def log_fail(name, detail=""):
    global FAILED
    FAILED += 1
    print(f"✗ {name}" + (f" — {detail}" if detail else ""))

def test_rebuild_preserves_log_events():
    """Insert log events, rebuild, verify they survive."""
    state_engine._init_db()
    # Insert known rows
    state_engine.log_event("INFO", "rebuild_test", "row_alpha", "P5")
    state_engine.log_event("WARN", "rebuild_test", "row_beta", "P6")
    state_engine.log_event("ERROR", "rebuild_test", "row_gamma", "P7")

    count_before = len(state_engine.query_log_events(limit=1000))
    assert count_before >= 3, f"Expected ≥3 rows, got {count_before}"

    # Run rebuild
    state_engine.rebuild()

    count_after = len(state_engine.query_log_events(limit=1000))
    rows = state_engine.query_log_events(limit=100)
    messages = [str(r) for r in rows]

    if count_after >= 3 and any("row_alpha" in m for m in messages):
        log_pass("rebuild preserves log_events data")
    else:
        log_fail("rebuild preserves log_events", f"before={count_before} after={count_after}")

def test_rebuild_preserves_adversarial_log():
    """Insert adversarial entries, rebuild, verify they survive."""
    state_engine._init_db()
    state_engine.log_adversarial("test_gate", "PASS", "rebuild regression test")

    count_before = len(state_engine.query_adversarial(limit=1000))

    state_engine.rebuild()

    count_after = len(state_engine.query_adversarial(limit=1000))
    if count_after >= count_before:
        log_pass("rebuild preserves adversarial_log data")
    else:
        log_fail("rebuild preserves adversarial_log", f"before={count_before} after={count_after}")

def test_rebuild_hmac_chain_intact():
    """After rebuild, verify HMAC chains on all 4 tables."""
    state_engine._init_db()
    state_engine.log_event("INFO", "chain_test", "chain verify", "P5")
    state_engine.rebuild()

    all_ok = True
    for tbl in ("adversarial_log", "log_events", "state_events", "circuit_breaker_events"):
        ok, broken_at = state_engine.verify_audit_chain(tbl)
        if not ok:
            all_ok = False
            log_fail(f"HMAC chain on {tbl}", f"broken at row {broken_at}")

    if all_ok:
        log_pass("HMAC chains intact after rebuild on all 4 tables")

def test_rebuild_triggers_restored():
    """After rebuild, verify audit triggers are restored."""
    state_engine._init_db()
    state_engine.log_event("INFO", "trigger_test", "trigger verify", "P5")
    state_engine.rebuild()

    conn = state_engine._open()
    try:
        triggers = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'trg_%'"
        ).fetchall()
        trigger_names = {t[0] for t in triggers}
    finally:
        conn.close()

    # Expect 8 triggers: 4 tables × (no_delete + no_update_v2)
    expected = 8
    if len(trigger_names) == expected:
        log_pass(f"all {expected} audit triggers restored after rebuild")
    else:
        log_fail("audit triggers restored", f"expected {expected}, found {len(trigger_names)}: {trigger_names}")

def test_prune_then_rebuild():
    """Prune rows, rebuild, verify surviving rows intact."""
    state_engine._init_db()
    for i in range(10):
        state_engine.log_event("INFO", "prune_rebuild_test", f"row {i}", "P5")

    # Prune to keep last 5
    deleted = state_engine.prune_log_events(keep_last=5)
    count_after_prune = len(state_engine.query_log_events(limit=100))

    # Rebuild
    state_engine.rebuild()
    count_after_rebuild = len(state_engine.query_log_events(limit=100))

    if count_after_rebuild >= count_after_prune:
        log_pass("rebuild preserves data after prune")
    else:
        log_fail("rebuild after prune", f"prune_left={count_after_prune} rebuild_left={count_after_rebuild}")


if __name__ == "__main__":
    print("=== Rebuild-Restore Regression Tests ===\n")
    test_rebuild_preserves_log_events()
    test_rebuild_preserves_adversarial_log()
    test_rebuild_hmac_chain_intact()
    test_rebuild_triggers_restored()
    test_prune_then_rebuild()
    print(f"\n{'='*40}")
    print(f"  REBUILD-RESTORE: {PASSED} passed, {FAILED} failed")
    if FAILED > 0:
        sys.exit(1)
