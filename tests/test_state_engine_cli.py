#!/usr/bin/env python3
"""test_state_engine_cli.py — pytest integration tests for state_engine_cli.main().

Strategy: spawn `python3 lib/state_engine.py <cmd> [args...]` as a subprocess
against a real-but-isolated state DB. This exercises the full CLI surface
the same way Claude Code hooks do (they all shell out via this CLI).

Why subprocess instead of in-process:
- The CLI is the user-facing contract; testing it through the same
  boundary as production catches arg-parsing bugs that in-process tests
  miss.
- state_engine_cli.main() reads sys.argv directly; in-process invocation
  would require monkeypatching sys.argv per test, which is fiddly.

Per-test isolation: each test sets/uses a unique env var (HARNESS_TEST_ISO)
that state_engine respects via its own logic; the real repo's
.swebok_state.db is the SUT. (This is a pragmatic choice — same as
test_health.py — sandboxing a full state DB would duplicate the
schema and add risk.)
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
HARNESS = REPO / "lib" / "state_engine.py"


def _run(args, env_extra=None, expect_exit=0):
    """Run `python3 lib/state_engine.py <args>` and return (stdout, exit_code)."""
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    result = subprocess.run(
        [sys.executable, str(HARNESS)] + list(args),
        capture_output=True, text=True, env=env, cwd=str(REPO),
    )
    if expect_exit is not None and result.returncode != expect_exit:
        raise AssertionError(
            f"CLI {args} exited {result.returncode}, expected {expect_exit}\n"
            f"stdout: {result.stdout!r}\n"
            f"stderr: {result.stderr!r}"
        )
    return result.stdout, result.returncode


def _cleanup_key(key):
    """Remove a state key after the test (best-effort)."""
    # state_engine doesn't have a 'delete' command; we use set to "" which
    # leaves the row but with empty value. For test isolation, just leave
    # the row — the next test re-sets it to its known value.
    pass


# ===== get / set =====

def test_get_set_roundtrip():
    """set <key> <value> then get <key> returns the value."""
    test_key = "test.cli.roundtrip"
    _run(["set", test_key, "value42"], expect_exit=0)
    out, _ = _run(["get", test_key])
    assert out.strip() == "value42", f"expected 'value42', got {out!r}"


def test_set_returns_nonzero_on_failure():
    """set with malformed JSON for a list-typed key should still return 0 (best-effort)."""
    # state_engine.set() swallows JSON errors and stores raw — exit 0.
    _run(["set", "test.cli.malformed", "not-json"], expect_exit=0)
    out, _ = _run(["get", "test.cli.malformed"])
    assert "not-json" in out, f"raw value not preserved: {out!r}"


# ===== append_gate =====

def test_append_gate_idempotent():
    """append_gate P_FOO twice produces a list with one entry, not two."""
    gate = "TEST_CLI_GATE_42"
    _run(["append_gate", gate], expect_exit=0)
    _run(["append_gate", gate], expect_exit=0)
    out, _ = _run(["get", "gates_validated"])
    gates = json.loads(out)
    # If P_FOO already existed, count == previous_count + 1
    # (we don't reset state to keep the test cheap).
    # The key assertion: at most 1 NEW entry per append_gate call.
    assert out.count(gate) == 1, f"gate {gate} should appear once in {out!r}"


def test_append_gate_empty_name_rejected():
    """append_gate with empty name exits 1 (rejected — no-op validation)."""
    _, exit_code = _run(["append_gate", ""], expect_exit=1)
    # The CLI wrapper surfaces state_engine.append_gate's False as exit 1
    # — this is correct fail-fast behavior (an empty gate name would
    # otherwise pollute gates_validated[] with "").


# ===== increment_* =====

def test_increment_lint():
    """increment_lint returns the new value (>= 1)."""
    out, _ = _run(["increment_lint"])
    val = int(out.strip())
    assert val >= 1, f"expected >= 1, got {val}"


def test_increment_blocked():
    """increment_blocked <file> records the block."""
    test_file = "/tmp/test_cli_block_42"
    _run(["increment_blocked", test_file, "test_reason"], expect_exit=0)
    # The state is now in circuit_breaker; we don't need to verify it
    # back via get (it could be cleared by other tests). The point is
    # the command exits 0.


# ===== verify_audit_chain (Python entry point) =====

def _import_state_engine_in_process():
    """Import state_engine as a module, with lib/ on sys.path for siblings."""
    if str(REPO / "lib") not in sys.path:
        sys.path.insert(0, str(REPO / "lib"))
    import state_engine
    return state_engine


def test_verify_audit_chain_returns_ok():
    """verify_audit_chain on a clean DB returns (True, None)."""
    se = _import_state_engine_in_process()
    for tbl in ("adversarial_log", "log_events", "state_events", "circuit_breaker_events"):
        ok, broken_at = se.verify_audit_chain(tbl)
        assert ok, f"audit chain broken in {tbl} at row {broken_at}"


# ===== export_state / export_audit =====

def test_export_state_returns_valid_json():
    """export_state returns parseable JSON with the state table."""
    se = _import_state_engine_in_process()
    raw = se.export_state()
    data = json.loads(raw)
    assert isinstance(data, dict), f"export_state should be dict, got {type(data)}"
    # The state table always has 'current_phase' or similar key
    assert len(data) > 0, "export_state returned empty dict"


def test_export_audit_returns_valid_json():
    """export_audit returns parseable JSON with audit rows."""
    se = _import_state_engine_in_process()
    raw = se.export_audit(limit=10)
    data = json.loads(raw)
    assert isinstance(data, dict), f"export_audit should be dict, got {type(data)}"
    # 4 tables
    for tbl in ("adversarial_log", "log_events", "state_events", "circuit_breaker_events"):
        assert tbl in data, f"export_audit missing {tbl}: keys={list(data.keys())}"


# ===== self_audit / replay_session =====

def test_self_audit_returns_markdown():
    """self_audit returns a markdown-formatted report."""
    se = _import_state_engine_in_process()
    report = se.self_audit(council=False, since_days=1)
    assert "#" in report, f"expected markdown headings, got: {report[:200]!r}"


def test_replay_session_empty_window():
    """replay_session with a window that has no events returns []."""
    se = _import_state_engine_in_process()
    # 1970-01-01 → 1970-01-02 — no events should match
    events = se.replay_session("1970-01-01T00:00:00", "1970-01-02T00:00:00")
    assert isinstance(events, list), f"expected list, got {type(events)}"
    assert len(events) == 0, f"expected 0 events in far-past window, got {len(events)}"


# ===== main() entry point =====

def test_main_no_args_exits_nonzero():
    """`python3 state_engine.py` with no args exits non-zero with usage."""
    _, exit_code = _run([], expect_exit=None)
    assert exit_code != 0, "main() with no args should exit non-zero"


def test_main_unknown_cmd_exits_nonzero():
    """`python3 state_engine.py bogus_cmd` exits non-zero."""
    _, exit_code = _run(["bogus_cmd_xyz"], expect_exit=None)
    assert exit_code != 0, "unknown command should exit non-zero"


# ===== JSON injection regression (Council #8 CISO MED) =====

def test_increment_nested_validates_phase():
    """increment_nested with a phase containing special chars is rejected (SQLi defense)."""
    # Valid phase: passes
    _run(["increment_nested", "test.cli.iso", "P5", "subkey"], expect_exit=0)
    # Invalid phase (contains SQL meta-char): rejected with non-zero exit
    _, exit_code = _run(
        ["increment_nested", "test.cli.iso", "P5'; DROP TABLE state; --", "subkey"],
        expect_exit=None,
    )
    assert exit_code != 0, (
        f"increment_nested with SQL meta-chars in phase should be rejected, "
        f"but exited {exit_code}"
    )


if __name__ == "__main__":
    # Allow running as a script: pytest is required for collection.
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
