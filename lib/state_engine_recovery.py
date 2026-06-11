#!/usr/bin/env python3
"""state_engine_recovery.py — DB recovery (rebuild, check_integrity).

Extracted from state_engine.py to reduce god-class LOC.
Importable as: from state_engine_recovery import rebuild, check_integrity

Public API:
  - rebuild(keep_audit=True) -> bool  (corruption recovery; preserves audit by default)
  - check_integrity() -> str  (PRAGMA integrity_check result: "ok" or "*** in database...")

CIRCULAR IMPORT NOTE: This module must NOT import from state_engine at
module load time (state_engine imports from us). Use lazy imports inside
functions, or use sys.modules lookup for sibling privates.
"""
import logging
import os
import shutil
import sqlite3
import sys
import time
from pathlib import Path
from state_engine_compat import _se

_log = logging.getLogger("swebok.state_engine")



# ===== Recovery =====

def rebuild(keep_audit=True):
    """Rebuild DB from scratch (corruption recovery). Always preserves audit
    when keep_audit=True (default)."""
    se = _se()
    if se.STATE_DB.exists():
        ts = int(time.time())
        backup = se.STATE_DB.with_suffix(f".db.corrupt.{ts}")
        try:
            if keep_audit:
                shutil.copy2(str(se.STATE_DB),
                             str(se.STATE_DB.with_suffix(f".db.pre-rebuild.{ts}")))
            se.STATE_DB.rename(backup)
            print(f"[REBUILD] Corrupt DB moved to {backup}")
        except OSError as e:
            print(f"[REBUILD] ERROR: {e}", file=sys.stderr)
            return False
        for ext in ("-wal", "-shm"):
            sidecar = Path(str(se.STATE_DB) + ext)
            if sidecar.exists():
                try:
                    sidecar.unlink()
                except (sqlite3.Error, OSError) as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        try:
            for old in sorted(se.HARNESS_DIR.glob(".swebok_state.db.corrupt.*"))[:-3]:
                try:
                    old.unlink()
                except (sqlite3.Error, OSError) as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        except (sqlite3.Error, OSError) as _e:
            _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
    se._DB_READY = False
    se._init_db()
    if keep_audit:
        try:
            pre_rebuild = sorted(se.STATE_DB.parent.glob(
                se.STATE_DB.name + ".pre-rebuild.*" if se.STATE_DB.parent == se.HARNESS_DIR
                else ".swebok_state.db.pre-rebuild.*"
            ))
            if pre_rebuild:
                src = pre_rebuild[-1]
                src_conn = sqlite3.connect(str(src))
                try:
                    dst_conn = sqlite3.connect(str(se.STATE_DB))
                    try:
                        # Drop audit-protect triggers before restore (they block INSERT OR IGNORE)
                        for tbl in ("adversarial_log", "log_events",
                                    "state_events", "circuit_breaker_events"):
                            se.drop_audit_triggers(dst_conn, tbl)
                        dst_conn.commit()
                        for tbl in ("adversarial_log", "log_events",
                                    "state_events", "circuit_breaker_events"):
                            try:
                                rows = src_conn.execute(f"SELECT * FROM {tbl}").fetchall()
                                if not rows:
                                    continue
                                cols = [d[1] for d in dst_conn.execute(
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
                            except (sqlite3.Error, IndexError, TypeError, KeyError):
                                continue
                        dst_conn.commit()
                        # Restore triggers after data restore, before recompute
                        for tbl in ("adversarial_log", "log_events",
                                    "state_events", "circuit_breaker_events"):
                            se.ensure_triggers(dst_conn)
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
                        se.recompute_audit_chain(tbl)
                    except (sqlite3.Error, ValueError, TypeError, KeyError, IndexError, AttributeError, OSError) as e:
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
                except (sqlite3.Error, OSError) as _e:
                    _log.debug("state_engine: secondary error during cleanup", exc_info=_e)
        except (OSError, sqlite3.Error, ValueError, TypeError, KeyError, IndexError, AttributeError) as e:
            print(f"[REBUILD] audit restore warning: {e}", file=sys.stderr)
    print("[REBUILD] Fresh DB initialized with defaults.")
    return True


def check_integrity():
    """D2: explicit integrity check (NOT on hot path)."""
    se = _se()
    se._init_db()
    conn = se._open()
    try:
        row = conn.execute("PRAGMA integrity_check").fetchone()
        return row[0] if row else "unknown"
    finally:
        conn.close()
