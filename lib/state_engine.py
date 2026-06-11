#!/usr/bin/env python3
# SWEBOK v4 Harness — State Engine v2.0
# AUDIT-2026-06-01 rebuild: all CRIT/HIGH findings baked in.
#
# Design invariants (from ICD review 2026-06-01):
#   I1 — Append-only triggers present on all 4 audit tables.
#        Restored by _init_db on every startup (defense-in-depth against
#        crash-window between DROP and CREATE in _prune_with_trigger).
#   I2 — metadata.version matches actual schema columns.
#        Migrations registered via @migration decorator; CI guard ensures
#        no string-typo can silently skip a migration.
#   I3 — _DB_READY = True only after a fully successful migration loop.
#        _safe_add_column helper centralises the PRAGMA-table_info dance
#        so a partial-failure on column N does not corrupt column N+1.
#   I4 — Type of state.value is stable across writers, governed by SCHEMA_TYPES.
#
# Exit code mapping:
#   0  — success
#   3  — STATE_ENGINE_READONLY_FS
#   4  — STATE_ENGINE_DISK_FULL
#   5  — STATE_ENGINE_INTEGRITY_FAIL
#   6  — STATE_ENGINE_SCHEMA_DOWNGRADE / HARNESS_DIR_INVALID
#
# Module size: 1700 LOC across 12 sections. The Council (2026-06-10) flagged
# this as "approaching god-class". The acknowledged refactor plan is in
# docs/v2-plan/ADR-004-state-engine-refactor.md: Strategy B (keep monolith
# + add structural doc) for v2.6.0, incremental extraction in v2.7.0+.

import sqlite3
import os
import sys
import json
import time
import threading
import shutil
import logging
from contextlib import contextmanager
from pathlib import Path

_log = logging.getLogger("swebok.state_engine")

# ===== HARNESS_DIR + STATE_DB resolution =====
# AUDIT-2026-06-01 (STRIDE-Iso-1): multi-project isolation.
#
# HARNESS_DIR  — where the harness CODE lives (CLAUDE.md, scripts/, hooks/).
#                Resolved from this file's path. Read-only at runtime.
# STATE_DB     — where this PROJECT's state lives. Resolved in order:
#                1. $SWEBOK_STATE_DB env var (explicit override)
#                2. <git_project_root>/.swebok_state.db (per-project isolation)
#                3. $HARNESS_DIR/.swebok_state.db (legacy single-global)
# This allows the same harness install to gate N projects independently;
# project A's circuit breaker, gates_validated, and audit log do not leak
# into project B's.
import subprocess

_THIS_FILE = Path(__file__).resolve()
# Default: HARNESS_DIR is the parent of `lib/`. The state_engine lives at
# <HARNESS_DIR>/lib/state_engine.py, so we go up 2 levels from this file.
# (Was parent.parent.parent — one level too many, assumed a single-project
# layout like /home/<user>/lib/state_engine.py.)
HARNESS_DIR = Path(os.environ.get("HARNESS_DIR", str(_THIS_FILE.parent.parent)))


def _verify_harness_dir() -> Path:
    """v1.5.6: trust-boundary check on HARNESS_DIR.

    Defense-in-depth against an attacker who sets HARNESS_DIR to a malicious
    path containing a trojaned state_engine.py. We refuse to load from any
    path that does not contain the file we expect to be running.

    Specifically: HARNESS_DIR must contain a CLAUDE.md and a lib/state_engine.py
    whose __file__ matches _THIS_FILE. If the env var was set to a directory
    that contains a DIFFERENT state_engine.py, refuse to run.
    """
    h = HARNESS_DIR
    expected = _THIS_FILE
    actual = (h / "lib" / "state_engine.py").resolve()
    if not expected.samefile(actual):
        _log.critical(
            "HARNESS_DIR points to %s but we are running from %s. Refusing to "
            "load — the env var has been tampered with. Set HARNESS_DIR to "
            "the directory containing this file, or unset it.",
            h, _THIS_FILE.parent.parent.parent,
        )
        sys.exit(6)  # HARNESS_DIR_INVALID
    return h


HARNESS_DIR = _verify_harness_dir()


def _resolve_state_db():
    # 1. Explicit env override
    override = os.environ.get("SWEBOK_STATE_DB")
    if override:
        return Path(override).resolve()
    # 2. Per-project: try git root of CWD (v1.5.5: refuse world-writable cwd)
    cwd = Path(os.getcwd()).resolve()
    try:
        # os.stat in Python: st_mode has world-writable bit (S_IWOTH = 0o2).
        # Refuse to walk into a project root that any local user could plant a
        # malicious .swebok_state.db into.
        cwd_stat = os.stat(cwd)
        if cwd_stat.st_mode & 0o002:
            _log.warning(
                "state_engine: cwd %s is world-writable; refusing to use git "
                "root for state DB. Falling back to HARNESS_DIR.", cwd
            )
        else:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, timeout=2, cwd=str(cwd),
            )
            if result.returncode == 0 and result.stdout.strip():
                git_root = Path(result.stdout.strip()).resolve()
                # Only use git root if it is NOT the harness dir itself (avoids
                # gating the harness's own development by its own state).
                if git_root != HARNESS_DIR:
                    return git_root / ".swebok_state.db"
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    # 3. Legacy fallback: single global state at harness root
    return HARNESS_DIR / ".swebok_state.db"


_REQUIRED_PATHS = [
    HARNESS_DIR / "CLAUDE.md",
    HARNESS_DIR / "lib" / "state_engine.py",
]
for _req in _REQUIRED_PATHS:
    if not _req.exists():
        print(
            f"FATAL: HARNESS_DIR={HARNESS_DIR} missing {_req}. "
            f"Set HARNESS_DIR to a real swebok-v4-harness checkout.",
            file=sys.stderr,
        )
        sys.exit(6)

STATE_DB = _resolve_state_db()

# ===== Schema version + migration registry (D4) =====
STATE_VERSION = 3
_MIGRATIONS = {}  # populated by @migration decorator

def migration(version):
    """Decorator: register a migration for a given target version."""
    def _wrap(fn):
        if version in _MIGRATIONS:
            raise RuntimeError(f"Migration {version} double-registered: {fn.__name__}")
        _MIGRATIONS[version] = fn
        return fn
    return _wrap

# ===== Schema type map (D6) — invariant I4 =====
SCHEMA_TYPES = {
    "current_phase":        "string",
    "active_ka":            "json",
    "gates_validated":      "json",
    "last_action":          "string",
    "project_scope":        "string",
    "project_name":         "string",
    "tool_call_count":      "int",
    "last_continuity_compact": "string",
    "adversarial_log":      "json",
    "circuit_breaker":      "json",
    "lint_attempts":        "int",
    "hotpath_actions":      "json",
    "intent":               "string",
    "intent_confidence":    "string",
    "log_level":            "string",
    "circuit_breaker_cap":  "int",
    "phase_data":           "json",
}

# ===== Connection factory (D3) — unified =====
_DB_READY = False
_THREAD_LOCAL = threading.local()
_JOURNAL_SIZE_LIMIT = 64 * 1024 * 1024  # 64 MiB
_BUSY_TIMEOUT_MS = 30000


def _open(write_xact=False, cached=False):
    """Single connection factory.

    write_xact=True  -> BEGIN EXCLUSIVE on entry (caller commits/rolls back)
    cached=True      -> reuse a per-thread cached connection (hot path)
    """
    if cached:
        conn = getattr(_THREAD_LOCAL, "conn", None)
        if conn is None:
            conn = _open_raw()
            _THREAD_LOCAL.conn = conn
        return conn
    conn = _open_raw()
    if write_xact:
        conn.execute("BEGIN EXCLUSIVE")
    return conn


def _open_raw():
    """Raw connection with standard PRAGMAs. Used by _open() and sibling modules
    that need a direct connection (counters, prune) without BEGIN EXCLUSIVE."""
    conn = sqlite3.connect(str(STATE_DB), timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
    conn.execute(f"PRAGMA journal_size_limit={_JOURNAL_SIZE_LIMIT}")
    return conn


@contextmanager
def _xact():
    """Context manager: write transaction with auto-rollback on exception.

    Retries on lock contention. With xargs -P10 spawning 1000 writers, the
    BEGIN EXCLUSIVE can lose the race even with busy_timeout=30s if many
    workers try simultaneously and the OS scheduler is unfair. We retry up
    to 10 times with exponential backoff capped at ~1s before giving up.
    """
    last_exc = None
    backoff = 0.01
    for attempt in range(10):
        conn = None
        try:
            conn = sqlite3.connect(str(STATE_DB), timeout=60.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
            conn.execute(f"PRAGMA journal_size_limit={_JOURNAL_SIZE_LIMIT}")
            conn.execute("BEGIN EXCLUSIVE")
        except sqlite3.OperationalError as e:
            last_exc = e
            if conn is not None:
                try:
                    conn.close()
                except (sqlite3.Error, OSError) as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
            if "locked" in str(e).lower() or "busy" in str(e).lower():
                time.sleep(min(backoff, 1.0))
                backoff *= 2
                continue
            raise
        # Got the lock — execute caller body
        try:
            yield conn
            conn.execute("COMMIT")
            return
        except sqlite3.OperationalError as e:
            last_exc = e
            try:
                conn.execute("ROLLBACK")
            except (sqlite3.Error, OSError) as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
            if "locked" in str(e).lower() or "busy" in str(e).lower():
                try:
                    conn.close()
                except (sqlite3.Error, OSError) as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
                time.sleep(min(backoff, 1.0))
                backoff *= 2
                continue
            raise
        except (sqlite3.Error, ValueError, TypeError, KeyError, IndexError, AttributeError, OSError):
            try:
                conn.execute("ROLLBACK")
            except (sqlite3.Error, OSError) as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
            raise
        finally:
            try:
                conn.close()
            except (sqlite3.Error, OSError) as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    # Exhausted retries
    if last_exc is not None:
        raise last_exc
    raise sqlite3.OperationalError("BEGIN EXCLUSIVE exhausted retries")


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _session_correlation():
    sid = os.environ.get("CLAUDE_SESSION_ID") or os.environ.get("SESSION_ID") or "cli"
    agent = os.environ.get("CLAUDE_AGENT") or os.environ.get("AGENT") or "unknown"
    cid = os.environ.get("CORRELATION_ID") or sid
    return sid, agent, cid


def _safe_add_column(conn, table, col, ctype):
    """D7: idempotent ALTER TABLE ADD COLUMN."""
    cur = conn.execute(f"PRAGMA table_info({table})")
    cols = {r[1] for r in cur.fetchall()}
    if col not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {ctype}")


# ===== HMAC audit chain (MISSING-04 — CISO S blocker) =====
# Extracted to state_engine_audit.py (ADR-004 Strategy C, 2026-06-11).
# Re-exported here for sibling-module access via `se.audit_hmac()`,
# `se.last_hmac()`, etc. — see state_engine_logging.py, state_engine_cli.py.
from state_engine_audit import (  # noqa: F401  (re-export for sibling access)
    audit_hmac, last_hmac, drop_audit_triggers, ensure_triggers,
    verify_audit_chain, recompute_audit_chain,
)


def _translate_op_error(e, ctx):
    err = str(e).lower()
    if "readonly" in err or "read-only" in err:
        print(f"STATE_ENGINE_READONLY_FS: {ctx}", file=sys.stderr)
        sys.exit(3)
    if "disk full" in err or "database or disk is full" in err:
        print(f"STATE_ENGINE_DISK_FULL: {ctx}", file=sys.stderr)
        sys.exit(4)
    return False


def _init_db():
    """Idempotent init. Runs pending migrations, re-asserts triggers."""
    global _DB_READY
    if _DB_READY and STATE_DB.exists():
        return
    conn = sqlite3.connect(str(STATE_DB), timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
    # Restrict DB file permissions to owner-only (like .audit_key)
    try:
        os.chmod(str(STATE_DB), 0o600)
    except OSError:
        pass
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS state ("
                     "key TEXT PRIMARY KEY, value TEXT, "
                     "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("CREATE TABLE IF NOT EXISTS metadata ("
                     "key TEXT PRIMARY KEY, value TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS adversarial_log ("
                     "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                     "ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "gate TEXT NOT NULL, verdict TEXT NOT NULL, reason TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_adv_ts ON adversarial_log(ts)")
        conn.execute("CREATE TABLE IF NOT EXISTS log_events ("
                     "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                     "ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "level TEXT NOT NULL, component TEXT NOT NULL, "
                     "phase TEXT, message TEXT, metadata TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_le_ts ON log_events(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_le_comp ON log_events(component)")
        conn.execute("CREATE TABLE IF NOT EXISTS state_events ("
                     "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                     "ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "key TEXT NOT NULL, old_value TEXT, new_value TEXT, source TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_se_ts ON state_events(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_se_key ON state_events(key)")
        conn.execute("CREATE TABLE IF NOT EXISTS circuit_breaker_events ("
                     "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                     "ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "blocked_file TEXT, blocked_count INTEGER, reason TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cbe_ts ON circuit_breaker_events(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cbe_file ON circuit_breaker_events(blocked_file)")

        cur = conn.execute("SELECT value FROM metadata WHERE key='version'")
        row = cur.fetchone()
        on_disk = 0
        if row:
            try:
                on_disk = int(row[0])
            except (TypeError, ValueError):
                on_disk = 0
        if on_disk > STATE_VERSION:
            raise RuntimeError(
                f"State DB schema version {on_disk} is newer than code "
                f"version {STATE_VERSION}. Refusing to read."
            )
        if on_disk < STATE_VERSION and STATE_DB.exists():
            ts = int(time.time())
            try:
                shutil.copy2(str(STATE_DB), str(STATE_DB.with_suffix(f".db.bak.{ts}")))
            except OSError as e:
                print(f"WARN: backup-before-migrate failed: {e}", file=sys.stderr)
        for v in range(on_disk + 1, STATE_VERSION + 1):
            mig_fn = _MIGRATIONS.get(v)
            if mig_fn is None:
                raise RuntimeError(
                    f"Migration {v} required but not registered. "
                    f"Available: {sorted(_MIGRATIONS.keys())}"
                )
            mig_fn(conn)
        conn.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES ('version', ?)",
            (str(STATE_VERSION),),
        )
        if on_disk == 0:
            _init_default_state(conn)
        ensure_triggers(conn)
        conn.commit()
        _DB_READY = True
        try:
            prune_backup_files(keep_last=3)
        except (sqlite3.Error, OSError) as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    finally:
        conn.close()


def _init_default_state(conn):
    defaults = {
        'current_phase':        'P5_CONSTRUCTION',
        'active_ka':            '[]',
        'gates_validated':      '["P1_EXIT","P2_EXIT","P3_EXIT","P4_EXIT"]',
        'last_action':          'INIT:state_engine',
        'project_scope':        'default',
        'project_name':         'swebok-v4-harness',
        'tool_call_count':      '0',
        'last_continuity_compact': 'init',
        'adversarial_log':      '{}',
        'circuit_breaker':      '{"blocked_attempts":0,"override_active":false,"last_blocked_file":""}',
        'lint_attempts':        '0',
        'hotpath_actions':      '[]',
        'intent':               'unknown',
        'intent_confidence':    '0.0',
        'log_level':            'INFO',
        'circuit_breaker_cap':  '1000',
    }
    for key, value in defaults.items():
        conn.execute("INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)", (key, value))


@migration(1)
def _migrate_v1_fresh(conn):
    """v1 is the baseline schema; nothing to migrate from <v1."""
    pass


@migration(2)
def _migrate_v2_audit_metadata(conn):
    """v2: add session_id/agent/correlation_id to audit tables; metadata to log_events."""
    _safe_add_column(conn, "log_events", "metadata", "TEXT")
    for tbl in ("adversarial_log", "log_events", "state_events", "circuit_breaker_events"):
        for col in ("session_id", "agent", "correlation_id"):
            _safe_add_column(conn, tbl, col, "TEXT")
    for idx_row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
    ).fetchall():
        try:
            conn.execute(f"REINDEX {idx_row[0]}")
        except (sqlite3.Error, OSError) as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)


@migration(3)
def _migrate_v3_audit_hmac_chain(conn):
    """v3: add row_hmac TEXT column to every audit table.

    AUDIT-2026-06-01 (MISSING-04 — CISO S blocker): per-row HMAC chains
    each audit row to its predecessor. An attacker that drops triggers and
    deletes or modifies rows breaks the chain, which `verify_audit_chain()`
    detects.
    """
    for tbl in ("adversarial_log", "log_events", "state_events", "circuit_breaker_events"):
        _safe_add_column(conn, tbl, "row_hmac", "TEXT")



# ===== Public API: state CRUD =====

def _coerce(key, value):
    """D6: coerce based on declared schema type (I4)."""
    t = SCHEMA_TYPES.get(key, "string")
    s = str(value).strip()
    if t == "int":
        try:
            return str(int(s))
        except (TypeError, ValueError):
            return "0"
    if t == "bool":
        return "true" if s.lower() == "true" else "false"
    if t == "json":
        try:
            json.loads(s)
            return s
        except (TypeError, ValueError, json.JSONDecodeError):
            return s
    return s


def get(key_path):
    if not key_path:
        return ""
    _init_db()
    keys = key_path.split('.')
    conn = _open()
    try:
        cur = conn.execute("SELECT value FROM state WHERE key = ?", (keys[0],))
        row = cur.fetchone()
        if not row:
            return ""
        if len(keys) > 1:
            try:
                data = json.loads(row[0])
                val = data
                for k in keys[1:]:
                    if isinstance(val, dict):
                        val = val.get(k, '')
                    else:
                        return ''
                return str(val) if val is not None else ''
            except (json.JSONDecodeError, TypeError, AttributeError):
                return ''
        return row[0]
    finally:
        conn.close()


def set(key_path, value, source="cli"):
    if not key_path:
        return False
    _init_db()
    keys = key_path.split('.')
    try:
        with _xact() as conn:
            cur = conn.execute("SELECT value FROM state WHERE key = ?", (keys[0],))
            row = cur.fetchone()
            old_value = row[0] if row else None
            if len(keys) == 1:
                coerced = _coerce(keys[0], value)
                conn.execute(
                    "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                    (keys[0], coerced),
                )
            else:
                if row:
                    try:
                        data = json.loads(row[0])
                    except json.JSONDecodeError:
                        data = {}
                else:
                    data = {}
                if not isinstance(data, dict):
                    data = {}
                target = data
                for k in keys[1:-1]:
                    if k not in target or not isinstance(target[k], dict):
                        target[k] = {}
                    target = target[k]
                target[keys[-1]] = str(value)
                conn.execute(
                    "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                    (keys[0], json.dumps(data)),
                )
            sid, agent, cid = _session_correlation()
            ts = _now_iso()
            row_hmac = audit_hmac(
                last_hmac(conn, "state_events"),
                ts, "state_events", key_path, old_value, str(value), source, sid, agent, cid,
            )
            conn.execute(
                "INSERT INTO state_events "
                "(ts, key, old_value, new_value, source, session_id, agent, correlation_id, row_hmac) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ts, key_path, old_value, str(value), source, sid, agent, cid, row_hmac),
            )
        return True
    except sqlite3.OperationalError as e:
        return _translate_op_error(e, "set")
    except (sqlite3.Error, ValueError, TypeError, KeyError, IndexError, AttributeError):
        return False


# ===== Sibling-module import helper =====
# Ensure this file's directory (lib/) is on sys.path so that sibling modules
# like state_engine_counters / state_engine_logging / state_engine_prune are
# found regardless of whether the caller set PYTHONPATH, ran us directly, or
# imported as lib.state_engine.
_this_dir = str(_THIS_FILE.parent)
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)


# ===== Atomic counters (extracted to state_engine_counters.py) =====
from state_engine_counters import (  # noqa: F401  (re-export)
    _incr_scalar, _incr_nested_phase, reset_aov_iterations,
    increment_lint, lint_attempts, reset_lint,
    increment_aov_iterations, get_aov_iterations,
    increment_heal_iterations, get_heal_iterations,
    increment_tool_calls, get_tool_call_count,
    should_run_continuity, hot_path_decision, set_intent,
)


# ===== Circuit breaker / record_block =====

def record_block(file_path, reason="blocked"):
    _init_db()
    try:
        with _xact() as conn:
            cur = conn.execute("SELECT value FROM state WHERE key = 'circuit_breaker'")
            row = cur.fetchone()
            cb = {'blocked_attempts': 0, 'override_active': False, 'last_blocked_file': ''}
            if row and row[0]:
                try:
                    cb = json.loads(row[0])
                except json.JSONDecodeError:
                    pass
            try:
                cap_row = conn.execute(
                    "SELECT value FROM state WHERE key = 'circuit_breaker_cap'"
                ).fetchone()
                cap = int(cap_row[0]) if cap_row and cap_row[0] else 1000
            except (TypeError, ValueError):
                cap = 1000
            cur_v = int(cb.get('blocked_attempts', 0) or 0)
            if cur_v < cap:
                cb['blocked_attempts'] = cur_v + 1
            cb['last_blocked_file'] = file_path or ""
            new_count = int(cb['blocked_attempts'])
            conn.execute(
                "INSERT OR REPLACE INTO state (key, value) VALUES ('circuit_breaker', ?)",
                (json.dumps(cb),),
            )
            sid, agent, cid = _session_correlation()
            ts = _now_iso()
            row_hmac = audit_hmac(
                last_hmac(conn, "circuit_breaker_events"),
                ts, "circuit_breaker_events", file_path or "", new_count, reason, sid, agent, cid,
            )
            conn.execute(
                "INSERT INTO circuit_breaker_events "
                "(ts, blocked_file, blocked_count, reason, session_id, agent, correlation_id, row_hmac) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (ts, file_path or "", new_count, reason, sid, agent, cid, row_hmac),
            )
            return new_count
    except sqlite3.OperationalError as e:
        return _translate_op_error(e, "record_block") or 0


def increment_blocked(file_path=None, reason="blocked"):
    return record_block(file_path or "", reason)


def reset_all_circuits(phase=None):
    """Reset circuit_breaker, lint_attempts, and (if phase given) phase_data counters.

    Called on phase transition to clear the noise of the previous phase.
    Tests rely on this resetting phase_data.<phase>.aov_iterations and
    phase_data.<phase>.heal_iterations to 0.
    """
    _init_db()
    try:
        with _xact() as conn:
            # Reset circuit_breaker JSON
            conn.execute(
                "INSERT OR REPLACE INTO state (key, value) VALUES ('circuit_breaker', ?)",
                ('{"blocked_attempts":0,"override_active":false,"last_blocked_file":""}',),
            )
            # Reset lint_attempts
            conn.execute(
                "INSERT OR REPLACE INTO state (key, value) VALUES ('lint_attempts', '0')"
            )
            # If a phase was named, also reset phase_data.<phase>.aov/heal_iterations
            if phase:
                cur = conn.execute("SELECT value FROM state WHERE key = 'phase_data'")
                row = cur.fetchone()
                pd = {}
                if row and row[0]:
                    try:
                        pd = json.loads(row[0])
                    except json.JSONDecodeError:
                        pd = {}
                if not isinstance(pd, dict):
                    pd = {}
                pd.setdefault(phase, {})
                pd[phase]["aov_iterations"] = 0
                pd[phase]["heal_iterations"] = 0
                conn.execute(
                    "INSERT OR REPLACE INTO state (key, value) VALUES ('phase_data', ?)",
                    (json.dumps(pd),),
                )
            # Audit row
            sid, agent, cid = _session_correlation()
            ts = _now_iso()
            row_hmac = audit_hmac(
                last_hmac(conn, "state_events"),
                ts, "state_events", "reset_all_circuits", None, phase or "global",
                "reset_all_circuits", sid, agent, cid,
            )
            conn.execute(
                "INSERT INTO state_events "
                "(ts, key, old_value, new_value, source, session_id, agent, correlation_id, row_hmac) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ts, "reset_all_circuits", None, phase or "global",
                 "reset_all_circuits", sid, agent, cid, row_hmac),
            )
        return True
    except (sqlite3.Error, ValueError, TypeError, KeyError, IndexError, AttributeError):
        return False


# ===== Logging (extracted to state_engine_logging.py) =====
from state_engine_logging import (  # noqa: F401  (re-export)
    log_tool_call, log_event, query_log_events,
    log_adversarial, query_adversarial, query_state_events,
    query_circuit_breaker_events,
)



# ===== Prune (extracted to state_engine_prune.py) =====
from state_engine_prune import (  # noqa: F401  (re-export)
    _prune_with_trigger, prune_log_events, prune_state_events,
    prune_circuit_breaker_events, prune_adversarial, prune_backup_files,
)


# ===== append_gate (extracted to state_engine_gates.py) =====
# Original append_gate() implementation (~42 LOC) was extracted to
# state_engine_gates.py per Architect MED-2 gap closure.
# Re-exported here for backward-compat with existing callers.
from state_engine_gates import (  # noqa: F401  (re-export)
    append_gate,
)


# ===== Recovery (extracted to state_engine_recovery.py) =====
from state_engine_recovery import (  # noqa: F401  (re-export)
    rebuild, check_integrity,
)


# Original rebuild implementation removed (now in state_engine_recovery.py).


# ===== Export (extracted to state_engine_export.py) =====
from state_engine_export import (  # noqa: F401  (re-export)
    export_state, export_audit,
)


# ===== Self-audit (ADR-003 / G.2) (extracted to state_engine_self_audit.py) =====
# Original replay_session() and self_audit() implementations (142 LOC) were
# extracted to state_engine_self_audit.py per Architect LOW gap closure.
# Re-exported here for backward-compat with existing callers.
from state_engine_self_audit import (  # noqa: F401  (re-export)
    replay_session, self_audit,
)


# ===== CLI dispatch =====
# AUDIT-2026-06-01 ITER6 (Architect S blocker): CLI dispatcher extracted to
# `state_engine_cli.py` per ADR-001's named seam. We keep a thin wrapper
# here so `python3 state_engine.py <cmd>` continues to work — it just
# delegates to the dedicated CLI module.


def main():
    """Backward-compat shim — delegates to state_engine_cli.main()."""
    from state_engine_cli import main as _cli_main
    _cli_main()


if __name__ == "__main__":
    main()
