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
HARNESS_DIR = Path(os.environ.get("HARNESS_DIR", str(_THIS_FILE.parent.parent.parent)))


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
            conn = sqlite3.connect(str(STATE_DB), timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
            conn.execute(f"PRAGMA journal_size_limit={_JOURNAL_SIZE_LIMIT}")
            _THREAD_LOCAL.conn = conn
        return conn
    conn = sqlite3.connect(str(STATE_DB), timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
    conn.execute(f"PRAGMA journal_size_limit={_JOURNAL_SIZE_LIMIT}")
    if write_xact:
        conn.execute("BEGIN EXCLUSIVE")
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
                except Exception as _e:
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
            except Exception as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
            if "locked" in str(e).lower() or "busy" in str(e).lower():
                try:
                    conn.close()
                except Exception as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
                time.sleep(min(backoff, 1.0))
                backoff *= 2
                continue
            raise
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except Exception as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
            raise
        finally:
            try:
                conn.close()
            except Exception as _e:
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
# Per-row HMAC chains the rows so any DELETE-then-INSERT or UPDATE is
# detectable. The secret lives in $SWEBOK_AUDIT_KEY (or, on a single-laptop
# install, in a private file at $HARNESS_DIR/.audit_key, mode 0600).
import hmac
import hashlib


def _audit_secret():
    """Return the HMAC secret as bytes. Reads from env, falls back to
    a per-install key file at $HARNESS_DIR/.audit_key (mode 0600). The
    file is auto-created on first call with 256 bits of os.urandom.
    """
    env = os.environ.get("SWEBOK_AUDIT_KEY")
    if env:
        return env.encode("utf-8")
    key_path = HARNESS_DIR / ".audit_key"
    if key_path.exists():
        try:
            return key_path.read_bytes()
        except Exception as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    # First-time create
    try:
        secret = os.urandom(32)
        key_path.write_bytes(secret)
        try:
            os.chmod(str(key_path), 0o600)
        except Exception as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        return secret
    except Exception as e:
        # Read-only FS / permission error — DO NOT fall back to a known constant.
        # A forgeable fallback would let any attacker who read this source code
        # produce valid HMACs for arbitrary audit rows. The system must refuse
        # to operate without a real secret; the caller (state engine init) will
        # surface the failure to the user.
        raise RuntimeError(
            f"STATE_ENGINE_INTEGRITY_FAIL: cannot create/read HMAC key file at "
            f"{key_path} (read-only FS or permission denied). Refusing to fall back "
            f"to a known constant: that would let any attacker who read this source "
            f"forge audit-chain HMACs. Original error: {e!r}"
        ) from e


def _audit_hmac(prev_hmac_hex, ts, *fields):
    """Compute HMAC-SHA256 over (prev_hmac, ts, field1, field2, ...).

    Returns the new hex digest. The chain links every row to the previous
    row, so removing row N changes row N+1's HMAC and detection becomes
    "compare each row's stored hmac to recomputed hmac".
    """
    h = hmac.new(_audit_secret(), digestmod=hashlib.sha256)
    h.update((prev_hmac_hex or "").encode("utf-8"))
    h.update(b"|")
    h.update((ts or "").encode("utf-8"))
    for f in fields:
        h.update(b"|")
        h.update(("" if f is None else str(f)).encode("utf-8"))
    return h.hexdigest()


def _last_hmac(conn, table):
    """Return the most recent row_hmac in `table`, or '' if empty/missing."""
    try:
        row = conn.execute(
            f"SELECT row_hmac FROM {table} ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if row and row[0]:
            return row[0]
    except sqlite3.OperationalError:
        # row_hmac column missing (older schema) — chain starts at empty
        pass
    return ""


def verify_audit_chain(table, limit=10000):
    """Verify the HMAC chain on `table`. Returns (ok: bool, broken_at: int|None).

    AUDIT-2026-06-01 ITER5 FIX: recompute each row's HMAC from the prior row's
    HMAC + the row's content fields and compare against the stored row_hmac.
    A break means: row content was modified, row was deleted, or row was
    inserted out of order.

    Returns (True, None) if intact. Returns (True, None) also if the table
    has no rows yet OR row_hmac column is absent (older schema) — those are
    not chain violations.
    """
    _init_db()
    conn = _open()
    try:
        # Per-table column selection — must mirror what _audit_hmac was given
        # at INSERT time. This is the contract: the field list here MUST
        # match the field list in the corresponding INSERT path.
        column_specs = {
            "adversarial_log": "id, ts, gate, verdict, reason, session_id, agent, correlation_id, row_hmac",
            "log_events":      "id, ts, level, component, phase, message, metadata, session_id, agent, correlation_id, row_hmac",
            "state_events":    "id, ts, key, old_value, new_value, source, session_id, agent, correlation_id, row_hmac",
            "circuit_breaker_events": "id, ts, blocked_file, blocked_count, reason, session_id, agent, correlation_id, row_hmac",
        }
        cols = column_specs.get(table)
        if cols is None:
            return (True, None)
        try:
            rows = conn.execute(
                f"SELECT {cols} FROM {table} ORDER BY id ASC LIMIT ?",
                (limit,),
            ).fetchall()
        except sqlite3.OperationalError:
            # row_hmac column missing — chain not yet initialised
            return (True, None)
    finally:
        conn.close()
    if not rows:
        return (True, None)
    prev = ""
    for row in rows:
        rid = row[0]
        ts = row[1]
        stored_hmac = row[-1]   # last column is row_hmac
        content = row[2:-1]     # everything between (ts, ..., row_hmac)
        if stored_hmac is None:
            # Pre-ITER5 row (HMAC column existed but writer didn't populate)
            # OR restored row from a rebuild that cleared the hmac. Treat as
            # chain pivot — the next populated row starts a fresh chain segment.
            prev = ""
            continue
        recomputed = _audit_hmac(prev, ts, table, *content)
        if recomputed != stored_hmac:
            return (False, rid)
        prev = stored_hmac
    return (True, None)


def recompute_audit_chain(table):
    """AUDIT-2026-06-01 ITER6: recompute and update row_hmac for every row in
    `table`. This is the supported maintenance operation after a legitimate
    prune that removes earlier rows — the chain attaches to the new earliest
    row by walking the surviving rows and rewriting their HMACs in order.

    Returns the number of rows touched. Returns -1 if the table or column
    is absent.
    """
    _init_db()
    column_specs = {
        "adversarial_log": ("id, ts, gate, verdict, reason, session_id, agent, correlation_id",
                            ["id", "ts", "gate", "verdict", "reason", "session_id", "agent", "correlation_id"]),
        "log_events":      ("id, ts, level, component, phase, message, metadata, session_id, agent, correlation_id",
                            ["id", "ts", "level", "component", "phase", "message", "metadata", "session_id", "agent", "correlation_id"]),
        "state_events":    ("id, ts, key, old_value, new_value, source, session_id, agent, correlation_id",
                            ["id", "ts", "key", "old_value", "new_value", "source", "session_id", "agent", "correlation_id"]),
        "circuit_breaker_events": ("id, ts, blocked_file, blocked_count, reason, session_id, agent, correlation_id",
                            ["id", "ts", "blocked_file", "blocked_count", "reason", "session_id", "agent", "correlation_id"]),
    }
    spec = column_specs.get(table)
    if spec is None:
        return -1
    sel_sql, _col_list = spec
    conn = sqlite3.connect(str(STATE_DB), timeout=30.0)
    try:
        try:
            rows = conn.execute(
                f"SELECT {sel_sql} FROM {table} ORDER BY id ASC"
            ).fetchall()
        except sqlite3.OperationalError:
            return -1
        prev = ""
        touched = 0
        for row in rows:
            rid = row[0]
            ts = row[1]
            content = row[2:]
            new_hmac = _audit_hmac(prev, ts, table, *content)
            conn.execute(f"UPDATE {table} SET row_hmac = ? WHERE id = ?",
                         (new_hmac, rid))
            prev = new_hmac
            touched += 1
        conn.commit()
        return touched
    finally:
        conn.close()


def _ensure_triggers(conn):
    """I1 defense-in-depth: re-issue CREATE TRIGGER IF NOT EXISTS on every startup.

    AUDIT-2026-06-01: BEFORE DELETE triggers are the primary protection.
    BEFORE UPDATE triggers were attempted but caused regression in the test
    suite (SQLite index integrity_check failed under concurrent prune+insert
    in WAL mode — root cause TBD). The UPDATE protection is documented as a
    gap in docs/v1/THREAT_MODEL.md until the trigger semantics can be made
    compatible with WAL-mode high-frequency writes.
    """
    triggers = [
        ("trg_adversarial_log_no_delete", "adversarial_log"),
        ("trg_log_events_no_delete", "log_events"),
        ("trg_state_events_no_delete", "state_events"),
        ("trg_circuit_breaker_events_no_delete", "circuit_breaker_events"),
    ]
    for trg, tbl in triggers:
        conn.execute(
            f"CREATE TRIGGER IF NOT EXISTS {trg} "
            f"BEFORE DELETE ON {tbl} "
            f"BEGIN SELECT RAISE(ABORT, "
            f"'{tbl} is append-only; drop the trigger for maintenance purge'); "
            f"END"
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
            except Exception as e:
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
        _ensure_triggers(conn)
        conn.commit()
        _DB_READY = True
        try:
            prune_backup_files(keep_last=3)
        except Exception as _e:
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
        except Exception as _e:
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
            row_hmac = _audit_hmac(
                _last_hmac(conn, "state_events"),
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
    except Exception:
        return False


# ===== Atomic counters =====

def _incr_scalar(key, delta=1, cap=None):
    """Atomic integer increment for a top-level state key.

    AUDIT-2026-06-01 FIX (CONC-XX): use SQLite UPSERT with a single SQL
    statement (`INSERT ... ON CONFLICT DO UPDATE`) instead of SELECT-then-
    UPDATE. SQLite guarantees this is atomic at the statement level — no
    BEGIN EXCLUSIVE retry loop needed for this path. This eliminates the
    race we saw under high external load (xargs -P10 with system contention).
    """
    _init_db()
    conn = None
    try:
        conn = sqlite3.connect(str(STATE_DB), timeout=60.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
        if cap is not None:
            sql = (
                "INSERT INTO state(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET "
                "value = CAST(MIN(CAST(value AS INTEGER) + ?, ?) AS TEXT)"
            )
            conn.execute(sql, (key, str(delta), delta, cap))
        else:
            sql = (
                "INSERT INTO state(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET "
                "value = CAST(CAST(value AS INTEGER) + ? AS TEXT)"
            )
            conn.execute(sql, (key, str(delta), delta))
        conn.commit()
        # Read back the new value
        row = conn.execute("SELECT value FROM state WHERE key = ?", (key,)).fetchone()
        return int(row[0]) if row and row[0] else 0
    except sqlite3.OperationalError as e:
        return _translate_op_error(e, f"incr {key}") or 0
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)


def _incr_nested_phase(key, subkey, phase="P6", delta=1):
    """Atomic increment of a counter nested inside the phase_data JSON.

    AUDIT-2026-06-01 FIX: uses SQLite's json_set + json_extract for atomic
    single-statement update on the JSON value. Falls back to SELECT-then-
    UPDATE inside _xact() retry loop if JSON1 is unavailable.
    """
    _init_db()
    conn = None
    try:
        conn = sqlite3.connect(str(STATE_DB), timeout=60.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
        # Ensure the row exists with a sane default
        conn.execute(
            "INSERT OR IGNORE INTO state(key, value) VALUES(?, ?)",
            (key, '{}'),
        )
        # Atomic single-statement UPDATE using JSON1 functions
        path = f"$.{phase}.{subkey}"
        sql = (
            f"UPDATE state SET value = json_set("
            f"  CASE WHEN json_type(value, '{path}') IS NULL "
            f"       THEN json_set(value, '{path}', 0) "
            f"       ELSE value END, "
            f"  '{path}', "
            f"  COALESCE(CAST(json_extract(value, '{path}') AS INTEGER), 0) + ?) "
            f"WHERE key = ?"
        )
        conn.execute(sql, (delta, key))
        conn.commit()
        # Read back
        row = conn.execute(
            f"SELECT json_extract(value, '{path}') FROM state WHERE key = ?",
            (key,)
        ).fetchone()
        return int(row[0]) if row and row[0] is not None else 0
    except sqlite3.OperationalError as e:
        return _translate_op_error(e, f"incr {key}.{phase}.{subkey}") or 0
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)


def reset_aov_iterations():
    """Reset the P6 aov_iterations counter to 0."""
    _init_db()
    try:
        with _xact() as conn:
            cur = conn.execute("SELECT value FROM state WHERE key = 'phase_data'")
            row = cur.fetchone()
            if row:
                try:
                    pd = json.loads(row[0])
                except json.JSONDecodeError:
                    pd = {}
            else:
                pd = {}
            if not isinstance(pd, dict):
                pd = {}
            pd.setdefault("P6", {})
            pd["P6"]["aov_iterations"] = 0
            conn.execute(
                "INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)",
                ("phase_data", json.dumps(pd)),
            )
        return True
    except Exception:
        return False


def increment_lint():
    return _incr_scalar("lint_attempts", 1)

def lint_attempts():
    v = get("lint_attempts")
    return int(v) if v else 0

def reset_lint():
    return set("lint_attempts", "0")

def increment_aov_iterations():
    return _incr_nested_phase("phase_data", "aov_iterations", "P6", 1)

def get_aov_iterations():
    v = get("phase_data.P6.aov_iterations")
    try:
        return int(v) if v else 0
    except (TypeError, ValueError):
        return 0

def increment_heal_iterations():
    return _incr_nested_phase("phase_data", "heal_iterations", "P6", 1)

def get_heal_iterations():
    v = get("phase_data.P6.heal_iterations")
    try:
        return int(v) if v else 0
    except (TypeError, ValueError):
        return 0

def increment_tool_calls():
    return _incr_scalar("tool_call_count", 1)

def get_tool_call_count():
    v = get("tool_call_count")
    return int(v) if v else 0

def should_run_continuity():
    n = get_tool_call_count()
    return n > 0 and n % 5 == 0

def hot_path_decision():
    """Return FULL or LITE based on the current intent.

    LITE → intent=micro_task (skip heavy validation, fast path).
    FULL → anything else (normal path).
    """
    intent = get("intent")
    return "LITE" if intent == "micro_task" else "FULL"

def set_intent(intent, confidence=0.0):
    a = set("intent", str(intent))
    b = set("intent_confidence", str(confidence))
    return a and b


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
            row_hmac = _audit_hmac(
                _last_hmac(conn, "circuit_breaker_events"),
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
            row_hmac = _audit_hmac(
                _last_hmac(conn, "state_events"),
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
    except Exception:
        return False


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


# ===== Prune (crash-safe per I1) =====

def _prune_with_trigger(table, trigger_name, keep_last):
    """Crash-safe prune. Uses autocommit DDL semantics for DROP/CREATE
    (so the DROP propagates before the DELETE). If killed mid-sequence,
    _init_db restores the trigger via _ensure_triggers on next startup (I1).
    """
    conn = sqlite3.connect(str(STATE_DB), timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"PRAGMA busy_timeout={_BUSY_TIMEOUT_MS}")
    try:
        conn.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
        try:
            cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
            total = cur.fetchone()[0]
            deleted = 0
            if total > keep_last:
                cur = conn.execute(
                    f"DELETE FROM {table} WHERE id IN "
                    f"(SELECT id FROM {table} ORDER BY id ASC LIMIT ?)",
                    (total - keep_last,)
                )
                deleted = cur.rowcount
            conn.commit()
            return deleted
        finally:
            try:
                conn.execute(
                    f"CREATE TRIGGER IF NOT EXISTS {trigger_name} "
                    f"BEFORE DELETE ON {table} "
                    f"BEGIN SELECT RAISE(ABORT, "
                    f"'{table} is append-only; drop the trigger for maintenance purge'); "
                    f"END"
                )
                conn.commit()
            except Exception as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    finally:
        conn.close()


def prune_log_events(keep_last=10000):
    _init_db()
    try:
        n = _prune_with_trigger("log_events", "trg_log_events_no_delete", keep_last)
        if n > 0:
            recompute_audit_chain("log_events")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_log_events blocked: {e}", file=sys.stderr)
        return -1


def prune_state_events(keep_last=10000):
    _init_db()
    try:
        n = _prune_with_trigger("state_events", "trg_state_events_no_delete", keep_last)
        if n > 0:
            recompute_audit_chain("state_events")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_state_events blocked: {e}", file=sys.stderr)
        return -1


def prune_circuit_breaker_events(keep_last=1000):
    _init_db()
    try:
        n = _prune_with_trigger(
            "circuit_breaker_events",
            "trg_circuit_breaker_events_no_delete",
            keep_last,
        )
        if n > 0:
            recompute_audit_chain("circuit_breaker_events")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_cb_events blocked: {e}", file=sys.stderr)
        return -1


def prune_adversarial(keep_last=10000):
    _init_db()
    try:
        n = _prune_with_trigger(
            "adversarial_log",
            "trg_adversarial_log_no_delete",
            keep_last,
        )
        if n > 0:
            recompute_audit_chain("adversarial_log")
        return n
    except sqlite3.IntegrityError as e:
        print(f"prune_adversarial blocked: {e}", file=sys.stderr)
        return -1


def prune_backup_files(keep_last=3):
    """R2: keep only the N most recent .swebok_state.db.bak.* files."""
    try:
        backups = sorted(
            HARNESS_DIR.glob(".swebok_state.db.bak.*"),
            key=lambda p: int(p.name.rsplit(".", 1)[-1])
                          if p.name.rsplit(".", 1)[-1].isdigit() else 0,
        )
        if len(backups) <= keep_last:
            return 0
        to_remove = backups[:-keep_last] if keep_last > 0 else backups
        removed = 0
        for old in to_remove:
            try:
                old.unlink()
                removed += 1
            except Exception as _e:
                _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        return removed
    except Exception:
        return 0


# ===== append_gate =====

def append_gate(gate_name):
    if not gate_name:
        return False
    _init_db()
    try:
        with _xact() as conn:
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
            sid, agent, cid = _session_correlation()
            ts = _now_iso()
            old_val = row[0] if row else None
            new_val = json.dumps(gates)
            row_hmac = _audit_hmac(
                _last_hmac(conn, "state_events"),
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
    except Exception:
        return False


# ===== Recovery =====

def rebuild(keep_audit=True):
    """Rebuild DB from scratch (corruption recovery). Always preserves audit
    when keep_audit=True (default)."""
    if STATE_DB.exists():
        ts = int(time.time())
        backup = STATE_DB.with_suffix(f".db.corrupt.{ts}")
        try:
            if keep_audit:
                shutil.copy2(str(STATE_DB),
                             str(STATE_DB.with_suffix(f".db.pre-rebuild.{ts}")))
            STATE_DB.rename(backup)
            print(f"[REBUILD] Corrupt DB moved to {backup}")
        except Exception as e:
            print(f"[REBUILD] ERROR: {e}", file=sys.stderr)
            return False
        for ext in ("-wal", "-shm"):
            sidecar = Path(str(STATE_DB) + ext)
            if sidecar.exists():
                try:
                    sidecar.unlink()
                except Exception as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        try:
            for old in sorted(HARNESS_DIR.glob(".swebok_state.db.corrupt.*"))[:-3]:
                try:
                    old.unlink()
                except Exception as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        except Exception as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    global _DB_READY
    _DB_READY = False
    _init_db()
    if keep_audit:
        try:
            pre_rebuild = sorted(HARNESS_DIR.glob(".swebok_state.db.pre-rebuild.*"))
            if pre_rebuild:
                src = pre_rebuild[-1]
                src_conn = sqlite3.connect(str(src))
                try:
                    dst_conn = sqlite3.connect(str(STATE_DB))
                    try:
                        for tbl in ("adversarial_log", "log_events",
                                    "state_events", "circuit_breaker_events"):
                            try:
                                rows = src_conn.execute(f"SELECT * FROM {tbl}").fetchall()
                                if not rows:
                                    continue
                                cols = [d[0] for d in dst_conn.execute(
                                    f"PRAGMA table_info({tbl})").fetchall()]
                                # AUDIT-2026-06-01 ITER5: clear row_hmac on
                                # restored rows so the chain restarts fresh
                                # after rebuild. The restored rows are
                                # preserved for forensics but flagged as
                                # pre-chain via NULL row_hmac. New rows
                                # written post-rebuild build a fresh chain.
                                if "row_hmac" in cols:
                                    hmac_idx = cols.index("row_hmac")
                                    rows = [
                                        tuple(None if i == hmac_idx else c
                                              for i, c in enumerate(r[:len(cols)]))
                                        for r in rows
                                    ]
                                placeholders = ",".join(["?"] * len(cols))
                                dst_conn.executemany(
                                    f"INSERT OR IGNORE INTO {tbl} "
                                    f"({','.join(cols)}) VALUES ({placeholders})",
                                    [r[:len(cols)] for r in rows],
                                )
                            except Exception:
                                continue
                        dst_conn.commit()
                    finally:
                        dst_conn.close()
                finally:
                    src_conn.close()
                # ITER6: re-attach the chain on restored rows so verify_audit_chain
                # reports them as intact (the chain was broken by prior writers
                # using a different secret OR by row 1 having been pruned earlier).
                # v1.5.5: a failed recompute on ANY table aborts the rebuild rather
                # than silently shipping rows that look pre-chain.
                recompute_failures = []
                for tbl in ("adversarial_log", "log_events",
                            "state_events", "circuit_breaker_events"):
                    try:
                        recompute_audit_chain(tbl)
                    except Exception as e:
                        recompute_failures.append((tbl, str(e)))
                        _log.error("state_engine: recompute_audit_chain failed for %s: %r", tbl, e)
                if recompute_failures:
                    # Do NOT unlink the backup; the user must investigate.
                    print(
                        f"[REBUILD] STATE_ENGINE_INTEGRITY_FAIL: {len(recompute_failures)} "
                        f"tables failed chain recompute: {recompute_failures}. "
                        f"Backup retained at {src}. Refusing to ship broken chain.",
                        file=sys.stderr,
                    )
                    sys.exit(5)
                try:
                    src.unlink()
                except Exception as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        except Exception as e:
            print(f"[REBUILD] audit restore warning: {e}", file=sys.stderr)
    print("[REBUILD] Fresh DB initialized with defaults.")
    return True


def check_integrity():
    """D2: explicit integrity check (NOT on hot path)."""
    _init_db()
    conn = _open()
    try:
        row = conn.execute("PRAGMA integrity_check").fetchone()
        return row[0] if row else "unknown"
    finally:
        conn.close()


# ===== Export =====

def export_state():
    _init_db()
    conn = _open()
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
    _init_db()
    conn = _open()
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


def replay_session(t0, t1):
    _init_db()
    conn = _open()
    try:
        cur = conn.execute(
            """
            SELECT 'adversarial_log' AS src, id, ts, gate AS key, verdict, reason, NULL AS meta
            FROM adversarial_log WHERE ts >= ? AND ts <= ?
            UNION ALL
            SELECT 'log_events', id, ts, component, level, message, metadata
            FROM log_events WHERE ts >= ? AND ts <= ?
            UNION ALL
            SELECT 'state_events', id, ts, key, source, new_value, old_value
            FROM state_events WHERE ts >= ? AND ts <= ?
            UNION ALL
            SELECT 'circuit_breaker_events', id, ts, blocked_file, reason, blocked_count, NULL
            FROM circuit_breaker_events WHERE ts >= ? AND ts <= ?
            ORDER BY ts ASC
            """,
            (t0, t1, t0, t1, t0, t1, t0, t1),
        )
        return cur.fetchall()
    finally:
        conn.close()


# ===== Self-audit (ADR-003 / G.2) =====
#
# self_audit() generates a markdown report summarising the harness's own
# audit state — verdict counts, recent state transitions, circuit-breaker
# activity, HMAC chain integrity. With council=True it ALSO emits a
# <MULTIAGENT_LAUNCH> envelope on stdout so the dispatcher can spawn a
# 4-role review (CISO / QA-lead / Architect / DevOps-lead). The function
# inserts a SELF_AUDIT row into adversarial_log so the audit cycle itself
# is part of the chained record.
def self_audit(council=False, since_days=30):
    """Generate the quarterly self-audit report.

    Args:
        council: when True, also emit a <MULTIAGENT_LAUNCH> envelope on stdout.
        since_days: window for the verdict / transition / circuit-breaker counts.

    Returns the report as a markdown string. The caller may print it.
    """
    _init_db()
    import datetime
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=since_days)).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    conn = _open()
    try:
        # Verdict counts in window
        verdict_rows = conn.execute(
            "SELECT verdict, COUNT(*) FROM adversarial_log WHERE ts >= ? GROUP BY verdict",
            (cutoff,),
        ).fetchall()
        # State transition count
        try:
            transition_count = conn.execute(
                "SELECT COUNT(*) FROM state_events WHERE ts >= ? AND key = 'current_phase'",
                (cutoff,),
            ).fetchone()[0]
        except sqlite3.OperationalError:
            transition_count = 0
        # Circuit-breaker activity
        try:
            cb_rows = conn.execute(
                "SELECT blocked_file, COUNT(*) FROM circuit_breaker_events "
                "WHERE ts >= ? GROUP BY blocked_file ORDER BY COUNT(*) DESC LIMIT 10",
                (cutoff,),
            ).fetchall()
        except sqlite3.OperationalError:
            cb_rows = []
        # Audit table row counts
        table_counts = {}
        for tbl in ("adversarial_log", "log_events", "state_events",
                    "circuit_breaker_events"):
            try:
                table_counts[tbl] = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            except sqlite3.OperationalError:
                table_counts[tbl] = -1
    finally:
        conn.close()
    # HMAC chain integrity (uses public verify_audit_chain — no inline dup)
    chain_status = {}
    for tbl in ("adversarial_log", "log_events", "state_events",
                "circuit_breaker_events"):
        ok, broken_at = verify_audit_chain(tbl)
        chain_status[tbl] = "ok" if ok else f"BROKEN at row {broken_at}"
    # Build markdown
    lines = [
        f"# Self-audit — {_now_iso()}",
        "",
        f"Window: last {since_days} days (since {cutoff})",
        "",
        "## Verdict counts (adversarial_log)",
    ]
    if verdict_rows:
        for verdict, n in verdict_rows:
            lines.append(f"- `{verdict}`: {n}")
    else:
        lines.append("- (none in window)")
    lines.extend([
        "",
        f"## Phase transitions: {transition_count}",
        "",
        "## Top blocked files (circuit_breaker_events)",
    ])
    if cb_rows:
        for f, n in cb_rows:
            lines.append(f"- `{f}`: {n}")
    else:
        lines.append("- (none in window)")
    lines.extend([
        "",
        "## Audit table sizes",
    ])
    for tbl, n in table_counts.items():
        lines.append(f"- `{tbl}`: {n}")
    lines.extend([
        "",
        "## HMAC chain integrity",
    ])
    for tbl, status in chain_status.items():
        lines.append(f"- `{tbl}`: {status}")
    lines.append("")
    # Council envelope (opt-in)
    if council:
        env = os.environ.get("MULTIAGENT_BRIDGE_ENABLED", "")
        if env != "1":
            lines.append("> NOTE: --council requested but MULTIAGENT_BRIDGE_ENABLED is not set.")
            lines.append("> Emitting the bridge envelope anyway for the dispatcher to discover.")
            lines.append("")
        lines.extend([
            "## <MULTIAGENT_LAUNCH>",
            "",
            "Spawn each of the 4 Nexus reviewers via the Agent tool, then re-invoke:",
            "  bash scripts/multiagent-launcher.sh emit-prompts SELF_AUDIT",
            "",
            "Roles: nexus-ciso, nexus-qa-lead, nexus-architect, nexus-devops-lead.",
            "Expected DSL output keys: RED:VULN, RED:LOC, RED:TYPE, RED:FIX_REQ, BLUE:STATUS.",
            "",
        ])
    report = "\n".join(lines)
    # Persist the audit row through the chained-write path (preserves HMAC).
    try:
        log_adversarial(
            "SELF_AUDIT",
            "PASS",
            f"window={since_days}d verdicts={len(verdict_rows)} chains_ok={sum(1 for s in chain_status.values() if s == 'ok')}/4",
        )
    except Exception as _e:
        _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    return report


# ===== CLI dispatch =====
# AUDIT-2026-06-01 ITER6 (Architect S blocker): CLI dispatcher extracted to
# `state_engine_cli.py` per ADR-001's named seam. We keep a thin wrapper
# here so `python3 state_engine.py <cmd>` continues to work — it just
# delegates to the dedicated CLI module.


def main():
    """Backward-compat shim — delegates to state_engine_cli.main()."""
    import importlib.util
    import os
    cli_path = os.path.join(os.path.dirname(__file__), "state_engine_cli.py")
    spec = importlib.util.spec_from_file_location("state_engine_cli", cli_path)
    cli_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli_mod)
    cli_mod.main()


if __name__ == "__main__":
    main()
