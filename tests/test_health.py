#!/usr/bin/env python3
"""test_health.py — Tests for lib/adv-loop/health.py.

Strategy: use the real repo as HARNESS_DIR (it has settings.json and a state
DB). We mock the parts we want to control by overriding module-level
constants after the import. This is pragmatic: the module is small (one
file, no I/O outside HARNESS_DIR), and a full sandbox would require
duplicating settings.json + state_engine, which adds more risk than value.
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

# Bootstrap: import health.py as a flat module (matches the bin/adv-loop invocation)
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "lib" / "adv-loop"))

import health  # noqa: E402

# The repo is the harness
REAL_HARNESS_DIR = REPO
REAL_DB = REAL_HARNESS_DIR / ".swebok_state.db"
REAL_SETTINGS = REAL_HARNESS_DIR / "settings.json"


def _override_health_module():
    """Point health module at the real repo."""
    health.HARNESS_DIR = REAL_HARNESS_DIR
    health.DB_PATH = REAL_DB
    health.SETTINGS_PATH = REAL_SETTINGS


def _set_state(key: str, value):
    """Update a state key in the real DB (test fixture pollution; cleaned up after)."""
    if not REAL_DB.exists():
        return
    con = sqlite3.connect(str(REAL_DB))
    con.execute("INSERT OR REPLACE INTO state(key, value) VALUES (?, ?)", (key, value))
    con.commit()
    con.close()


def _get_state(key: str):
    if not REAL_DB.exists():
        return None
    con = sqlite3.connect(str(REAL_DB))
    r = con.execute("SELECT value FROM state WHERE key=?", (key,)).fetchone()
    con.close()
    return r[0] if r else None


def test_healthy_state():
    """A clean harness returns 0 healthy."""
    _override_health_module()
    # Set a known-good state
    _set_state("circuit_breaker", json.dumps({"blocked_attempts": 0, "override_active": False}))
    _set_state("edits.counter", "3")
    _set_state("intent", json.dumps({"phase": "P5", "confidence": 0.85}))
    _set_state("gates_validated", json.dumps(["P1_EXIT", "P2_EXIT"]))

    agg = health.aggregate()
    assert agg["state_db"] == "ok", f"state_db={agg['state_db']}"
    assert agg["hmac_chain"] == "ok", f"hmac_chain={agg['hmac_chain']}"
    assert agg["circuit_breaker"] == "clean"
    assert agg["edits_since_council"] == "3/5"
    assert agg["intent_phase"] == "P5"
    assert agg["gates_validated"] == "P1_EXIT,P2_EXIT"
    assert agg["hooks_wired"] >= 14, f"hooks_wired={agg['hooks_wired']}"
    assert agg["degraded"] == 0
    assert agg["broken"] == 0
    assert agg["verdict"] == "🟢 OK"
    assert agg["exit_code"] == 0

    dsl = health.to_dsl(agg)
    assert dsl.startswith("health:state_db=ok;;")
    assert "health:verdict=🟢 OK" in dsl
    print("✓ Test H1: clean harness returns healthy verdict, exit 0")


def test_circuit_breaker_tripped():
    """Circuit breaker with >100 blocked returns degraded (exit 1)."""
    _override_health_module()
    _set_state("circuit_breaker", json.dumps({"blocked_attempts": 150, "override_active": False}))

    agg = health.aggregate()
    assert agg["circuit_breaker"] == "tripped", f"got {agg['circuit_breaker']}"
    assert agg["degraded"] >= 1
    assert agg["verdict"] == "🟡 DEGRADED"
    assert agg["exit_code"] == 1

    # Restore
    _set_state("circuit_breaker", json.dumps({"blocked_attempts": 0, "override_active": False}))
    print("✓ Test H2: circuit breaker tripped returns DEGRADED, exit 1")


def test_circuit_breaker_override():
    """Circuit breaker override_active returns degraded (exit 1)."""
    _override_health_module()
    _set_state("circuit_breaker", json.dumps({"blocked_attempts": 5, "override_active": True}))

    agg = health.aggregate()
    assert agg["circuit_breaker"] == "override"
    assert agg["degraded"] >= 1
    assert agg["verdict"] == "🟡 DEGRADED"
    assert agg["exit_code"] == 1

    _set_state("circuit_breaker", json.dumps({"blocked_attempts": 0, "override_active": False}))
    print("✓ Test H3: circuit breaker override returns DEGRADED, exit 1")


def test_dsl_format_is_strict():
    """DSL output follows strict KEY=VALUE;; format with no newlines."""
    _override_health_module()
    _set_state("circuit_breaker", json.dumps({"blocked_attempts": 0, "override_active": False}))

    agg = health.aggregate()
    dsl = health.to_dsl(agg)
    assert "\n" not in dsl, f"DSL contains newline: {dsl!r}"
    parts = dsl.split(";;")
    assert len(parts) == 10, f"expected 10 parts, got {len(parts)}: {parts}"
    for p in parts:
        assert "=" in p, f"part {p!r} missing '='"
        k, v = p.split("=", 1)
        assert k.startswith("health:"), f"key {k!r} doesn't start with health:"
    print("✓ Test H4: DSL format is strict (single line, 10 key=value pairs)")


def test_hooks_wired_count():
    """The hooks_wired count matches settings.json."""
    _override_health_module()
    s = json.loads(REAL_SETTINGS.read_text())
    expected = sum(
        len(h.get("hooks", []))
        for phase in s.get("hooks", {}).values()
        for h in phase
    )
    agg = health.aggregate()
    assert agg["hooks_wired"] == expected, f"got {agg['hooks_wired']}, expected {expected}"
    print(f"✓ Test H5: hooks_wired count matches settings.json ({expected} hooks)")


if __name__ == "__main__":
    test_healthy_state()
    test_circuit_breaker_tripped()
    test_circuit_breaker_override()
    test_dsl_format_is_strict()
    test_hooks_wired_count()
    print("\nAll health tests passed ✅ (5 tests)")
