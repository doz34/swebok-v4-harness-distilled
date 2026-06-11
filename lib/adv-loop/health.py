#!/usr/bin/env python3
"""health.py — Aggregated harness health check.

Single entry point for "is the SWEBOK v4 harness OK right now?".
Returns a single DSL line (key=value;;key=value) on stdout.
Exit codes: 0 healthy, 1 degraded (one SLO at MED), 2 broken (CRIT/HMAC).

Used by `bin/adv-loop health` (this module is the canonical implementation;
the bash subcommand is a thin wrapper).

SLO doc: docs/v2-plan/10-devops-slo.md §6.
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

# HARNESS_DIR is the project root (parent of lib/).
HARNESS_DIR = Path(os.environ.get("HARNESS_DIR", "."))
DB_PATH = HARNESS_DIR / ".swebok_state.db"
SETTINGS_PATH = HARNESS_DIR / "settings.json"

# Audit tables that must be HMAC-chained.
AUDIT_TABLES = ("adversarial_log", "log_events", "state_events", "circuit_breaker_events")


def _load_state_engine():
    """Import state_engine lazily; returns (module, ok)."""
    # Try the canonical location first (HARNESS_DIR/lib/state_engine.py).
    sys.path.insert(0, str(HARNESS_DIR / "lib"))
    try:
        import state_engine  # noqa: WPS433
        return state_engine, True
    except (ImportError, ModuleNotFoundError, SyntaxError):  # noqa: BLE001
        pass
    # Fallback: search upward for a lib/ dir that contains state_engine.py.
    # This lets the module work from any subdirectory (e.g. tests).
    p = HARNESS_DIR.resolve()
    for _ in range(4):
        candidate = p / "lib" / "state_engine.py"
        if candidate.exists():
            sys.path.insert(0, str(p / "lib"))
            try:
                import state_engine  # noqa: WPS433
                return state_engine, True
            except (ImportError, ModuleNotFoundError, SyntaxError):  # noqa: BLE001
                return None, False
        p = p.parent
    return None, False


def check_state_db() -> tuple[str, int]:
    """Returns (state, exit_code_delta). state ∈ {ok, missing}."""
    if not DB_PATH.exists():
        return "missing", 2  # CRIT: state DB missing
    return "ok", 0


def check_hmac_chain() -> tuple[str, int]:
    """Returns (state, exit_code_delta). state ∈ {ok, BROKEN, error:<class>}.
    Walks all 4 audit tables; any failure flips state to BROKEN.
    """
    se, ok = _load_state_engine()
    if not ok:
        return "error:ImportError", 2
    try:
        for tbl in AUDIT_TABLES:
            chain_ok, _ = se.verify_audit_chain(tbl)
            if not chain_ok:
                return "BROKEN", 2  # CRIT: any broken chain = broken
    except (sqlite3.Error, OSError, ValueError, TypeError, KeyError, IndexError, AttributeError) as e:  # noqa: BLE001
        return f"error:{type(e).__name__}", 2
    return "ok", 0


def check_hooks_wired() -> int:
    """Counts hook entries in settings.json. Returns count (0 if read fails)."""
    try:
        s = json.loads(SETTINGS_PATH.read_text())
        n = 0
        for phase in s.get("hooks", {}).values():
            for h in phase:
                n += len(h.get("hooks", []))
        return n
    except (OSError, json.JSONDecodeError, KeyError, TypeError, AttributeError):  # noqa: BLE001
        return 0


def check_circuit_breaker() -> tuple[str, int]:
    """Returns (state, exit_code_delta). state ∈ {clean, tripped, override, unknown}.
    tripped (>100 blocked) and override (active override flag) are MED = degraded.
    """
    if not DB_PATH.exists():
        return "unknown", 0
    try:
        con = sqlite3.connect(str(DB_PATH))
        con.row_factory = sqlite3.Row
        row = con.execute("SELECT value FROM state WHERE key='circuit_breaker'").fetchone()
        con.close()
        if not row:
            return "unknown", 0
        cb = json.loads(row["value"])
        if cb.get("blocked_attempts", 0) > 100:
            return "tripped", 1  # MED: degraded
        if cb.get("override_active"):
            return "override", 1  # MED: degraded
        return "clean", 0
    except (sqlite3.Error, json.JSONDecodeError, OSError, KeyError, TypeError):  # noqa: BLE001
        return "unknown", 0


def check_edits_counter() -> str:
    """Returns the edits counter formatted as 'N/5'."""
    if not DB_PATH.exists():
        return "0/5"
    try:
        con = sqlite3.connect(str(DB_PATH))
        row = con.execute("SELECT value FROM state WHERE key='edits.counter'").fetchone()
        con.close()
        if row:
            return f"{row[0]}/5"
    except (sqlite3.Error, OSError, TypeError):  # noqa: BLE001
        pass
    return "0/5"


def check_intent_phase() -> str:
    """Returns the current intent.phase string (e.g. 'P5' or 'unknown')."""
    if not DB_PATH.exists():
        return "unknown"
    try:
        con = sqlite3.connect(str(DB_PATH))
        row = con.execute("SELECT value FROM state WHERE key='intent'").fetchone()
        con.close()
        if row:
            v = json.loads(row[0])
            if isinstance(v, dict):
                return str(v.get("phase", "unknown"))
            return str(v)
    except (sqlite3.Error, json.JSONDecodeError, OSError, KeyError, TypeError):  # noqa: BLE001
        pass
    return "unknown"


def check_gates_validated() -> str:
    """Returns comma-separated list of validated gates (e.g. 'P1_EXIT,P2_EXIT')."""
    if not DB_PATH.exists():
        return "none"
    try:
        con = sqlite3.connect(str(DB_PATH))
        row = con.execute("SELECT value FROM state WHERE key='gates_validated'").fetchone()
        con.close()
        if row:
            v = json.loads(row[0])
            if v:
                return ",".join(v)
    except (sqlite3.Error, json.JSONDecodeError, OSError, KeyError, TypeError):  # noqa: BLE001
        pass
    return "none"


def aggregate() -> dict:
    """Run all checks and return aggregated verdict.
    Returns dict with keys: state_db, hmac_chain, circuit_breaker, edits_since_council,
    intent_phase, gates_validated, hooks_wired, degraded, broken, verdict, exit_code.
    """
    checks = {
        "state_db": check_state_db(),
        "hmac_chain": check_hmac_chain(),
        "circuit_breaker": check_circuit_breaker(),
    }

    degraded = 0
    broken = 0
    exit_code = 0
    for _name, (_state, code_delta) in checks.items():
        if code_delta == 1:
            degraded += 1
            exit_code = max(exit_code, 1)
        elif code_delta == 2:
            broken += 1
            exit_code = max(exit_code, 2)

    # Verdict
    if broken > 0:
        verdict = "🔴 BROKEN"
    elif degraded > 0:
        verdict = "🟡 DEGRADED"
    else:
        verdict = "🟢 OK"

    return {
        "state_db": checks["state_db"][0],
        "hmac_chain": checks["hmac_chain"][0],
        "circuit_breaker": checks["circuit_breaker"][0],
        "edits_since_council": check_edits_counter(),
        "intent_phase": check_intent_phase(),
        "gates_validated": check_gates_validated(),
        "hooks_wired": check_hooks_wired(),
        "degraded": degraded,
        "broken": broken,
        "verdict": verdict,
        "exit_code": exit_code,
    }


def to_dsl(agg: dict) -> str:
    """Format the aggregated verdict as a single DSL line."""
    return (
        f"health:state_db={agg['state_db']};;"
        f"health:hmac_chain={agg['hmac_chain']};;"
        f"health:circuit_breaker={agg['circuit_breaker']};;"
        f"health:edits_since_council={agg['edits_since_council']};;"
        f"health:intent_phase={agg['intent_phase']};;"
        f"health:gates_validated={agg['gates_validated']};;"
        f"health:hooks_wired={agg['hooks_wired']};;"
        f"health:degraded={agg['degraded']};;"
        f"health:broken={agg['broken']};;"
        f"health:verdict={agg['verdict']}"
    )


def main() -> int:
    """CLI entry point: prints DSL line, returns exit code."""
    agg = aggregate()
    print(to_dsl(agg))
    return agg["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
