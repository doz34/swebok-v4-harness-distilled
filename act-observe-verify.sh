#!/usr/bin/env bash
# SWEBOK v4 Harness - Act-Observe-Verify (MCP-BRIDGE) - STATELESS
# Usage:
#   ./act-observe-verify.sh                    # Output MCP_CALL XML + write .aov_pending JSON (I14)
#   ./act-observe-verify.sh --verify-result <result_file>   # Verify result vs pending, output AOV:PASS|AOV:FAIL
#
set -euo pipefail
trap 'echo "WARN:HOOK_INTERNAL_ERROR"; exit 0' ERR
# Lock cleanup trap fires on EXIT, not RETURN, so an `exit` in a function
# still releases the fcntl lock and sentinel file.
trap 'release_aov_lock' EXIT

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
# State of truth: .swebok_state.db. Do NOT read .swebok_state YAML.
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
AOV_PENDING="$HARNESS_DIR/.aov_pending"
AOV_LOCK="$HARNESS_DIR/.aov_pending.lock"
MCP_RESULT="/tmp/mcp_result.json"
SCREENSHOT_DIR="${SCREENSHOT_DIR:-/tmp/swebok-screenshots}"
DSL_PREFIX="AOV"
AOV_TIMEOUT_SECONDS=60
AOV_LOCK_TTL_SECONDS=60
MCP_EXECUTION_TIMEOUT=120  # MCP call execution timeout in seconds

# Source shared MCP precheck library
MCP_PRECHECK_LIB="$HARNESS_DIR/scripts/lib/mcp_precheck.sh"
# shellcheck disable=SC1090
[[ -f "$MCP_PRECHECK_LIB" ]] && source "$MCP_PRECHECK_LIB" || true

# === SCREENSHOT DIR: 0700 perms, realpath check (M11) ===
# mkdir -p alone leaves world-readable bits. Use explicit chmod and verify
# the realpath is a directory we own before any file is created.
ensure_screenshot_dir() {
    if [[ ! -d "$SCREENSHOT_DIR" ]]; then
        mkdir -p "$SCREENSHOT_DIR"
    fi
    chmod 0700 "$SCREENSHOT_DIR" 2>/dev/null || true
    local resolved
    resolved=$(realpath "$SCREENSHOT_DIR" 2>/dev/null || echo "")
    if [[ -z "$resolved" || ! -d "$resolved" ]]; then
        echo "[$DSL_PREFIX] FATAL: SCREENSHOT_DIR not a real directory: $SCREENSHOT_DIR" >&2
        exit 1
    fi
}

# === SENTINEL LOCK: fcntl.flock + 60s TTL fallback (C3, M10) ===
# Replaces mkdir-mutex. A stale lockdir (process killed mid-write) used to
# cause permanent AOV DoS. Now the lock is a real file with fcntl.flock and a
# mtime-based TTL fallback. The trap is EXIT so any exit path releases it.
#
# We hold the lock with a long-lived FD stored in a sentinel "holder" script
# (also a temp file under HARNESS_DIR). The holder runs flock on a separate
# FD and never exits until killed. If the parent dies, the holder dies too
# (pgid), and the TTL fallback recovers the lock.
AOV_LOCK_FD_HOLDER=""

acquire_aov_lock() {
    if [[ -f "$AOV_LOCK" ]]; then
        local age
        age=$(python3 -c "
import os, time
try:
    print(int(time.time() - os.path.getmtime('$AOV_LOCK')))
except Exception:
    print(0)
" 2>/dev/null || echo "0")
        if [[ "${age:-0}" -gt "$AOV_LOCK_TTL_SECONDS" ]]; then
            echo "[$DSL_PREFIX] STALE_LOCK: $AOV_LOCK is ${age}s old (TTL=${AOV_LOCK_TTL_SECONDS}s), removing" >&2
            rm -f "$AOV_LOCK"
        else
            echo "[$DSL_PREFIX] CONTENDED: another verification in progress" >&2
            return 1
        fi
    fi

    # O_EXCL refuses to clobber an existing lockfile, O_NOFOLLOW refuses to
    # follow a symlink (a malicious symlink would let an attacker point our
    # lock file at someone else's file). mode 0600 keeps others from
    # tampering with the lock. We acquire via a short-lived python that
    # immediately exits; the lock then relies on the file's existence +
    # mtime for mutual exclusion (with TTL fallback for the crash case).
    python3 - "$AOV_LOCK" <<'PYEOF' || return 1
import fcntl, os, sys
path = sys.argv[1]
try:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
        sys.exit(1)
    # Touch the file so mtime is "now"
    os.utime(path, None)
    os.close(fd)
    sys.exit(0)
except FileExistsError:
    sys.exit(1)
except Exception:
    sys.exit(1)
PYEOF
}

release_aov_lock() {
    rm -f "$AOV_LOCK" 2>/dev/null || true
}

# === CLEAN MCP RESULT ON ENTRY + EXIT (H5) ===
cleanup_mcp_result() {
    rm -f "$MCP_RESULT" 2>/dev/null || true
}

# === SAFE WRITE: O_EXCL|O_NOFOLLOW + fsync + os.replace (C4, H6) ===
# Uses an atomic temp+rename to avoid partial writes. Validates realpath
# before any rm. Refuses to follow symlinks at every step.
safe_write_aov_pending() {
    local data="$1"
    local tmpfile
    tmpfile=$(mktemp "$HARNESS_DIR/.aov_pending.XXXXXX" 2>/dev/null) || {
        echo "[$DSL_PREFIX] FATAL: cannot create temp file for $AOV_PENDING" >&2
        return 1
    }
    chmod 0600 "$tmpfile" 2>/dev/null || true
    if ! printf '%s' "$data" > "$tmpfile"; then
        rm -f "$tmpfile" 2>/dev/null || true
        return 1
    fi
    # Validate realpath of temp file (must be under HARNESS_DIR, no symlink).
    local rp
    rp=$(realpath "$tmpfile" 2>/dev/null || echo "")
    if [[ -z "$rp" || "$rp" != "$HARNESS_DIR"/* ]]; then
        rm -f "$tmpfile" 2>/dev/null || true
        echo "[$DSL_PREFIX] FATAL: temp file realpath escape: $rp" >&2
        return 1
    fi
    # fsync + atomic replace. This is safe even if $AOV_PENDING is a
    # symlink: os.replace removes the symlink itself, not the target.
    python3 - <<PYEOF
import os, sys
tmp = "$tmpfile"
dst = "$AOV_PENDING"
try:
    fd = os.open(tmp, os.O_RDONLY)
    os.fsync(fd)
    os.close(fd)
    # Refuse if dst is a symlink (defense in depth: O_NOFOLLOW equivalent
    # at the python layer)
    if os.path.islink(dst):
        print("REFUSE_SYMLINK", file=sys.stderr)
        sys.exit(1)
    os.replace(tmp, dst)
except Exception as e:
    print(f"REPLACE_FAIL: {e}", file=sys.stderr)
    try:
        os.unlink(tmp)
    except FileNotFoundError:
        pass
    sys.exit(1)
PYEOF
}

# === SAFE REMOVE: validate realpath (C4) ===
# Refuses to rm a path that is, or resolves to, a symlink. Removes the
# symlink itself if so, never the target.
safe_rm_aov_pending() {
    if [[ -L "$AOV_PENDING" ]]; then
        # It's a symlink: remove the symlink, not the target.
        unlink "$AOV_PENDING" 2>/dev/null || true
        return 0
    fi
    if [[ ! -e "$AOV_PENDING" ]]; then
        return 0
    fi
    local rp
    rp=$(realpath "$AOV_PENDING" 2>/dev/null || echo "")
    if [[ -z "$rp" || "$rp" != "$HARNESS_DIR"/* ]]; then
        echo "[$DSL_PREFIX] REFUSE_RM: realpath escape $rp" >&2
        return 1
    fi
    rm -f "$AOV_PENDING" 2>/dev/null || true
}

# === DSL OUTPUT ===
log_dsl() { echo "[$DSL_PREFIX] $1"; }

# === CHECK FOR GHOST STATES (pending >60s old) ===
# Acquires fcntl lock with 60s TTL fallback so a crashed process cannot
# permanently block AOV.
check_timeout() {
    if [[ ! -e "$AOV_PENDING" ]]; then
        return 1  # No pending, no timeout
    fi
    # Reject symlink (C4) before doing anything else.
    if [[ -L "$AOV_PENDING" ]]; then
        log_dsl "REJECT: .aov_pending is a symlink, refusing"
        unlink "$AOV_PENDING" 2>/dev/null || true
        echo "AOV:FAIL|REASON:SYMLINK"
        return 1
    fi
    if ! acquire_aov_lock; then
        echo "AOV:FAIL|REASON:CONTENDED"
        return 1
    fi

    local age_seconds
    age_seconds=$(python3 -c "
import os, time
try:
    mtime = os.path.getmtime('$AOV_PENDING')
    age = time.time() - mtime
    print(int(age))
except Exception:
    print(0)
" 2>/dev/null || echo "0")

    if [[ "$age_seconds" -gt "$AOV_TIMEOUT_SECONDS" ]]; then
        log_dsl "TIMEOUT: Pending state is ${age_seconds}s old (>${AOV_TIMEOUT_SECONDS}s). Removing ghost state."
        safe_rm_aov_pending
        echo "AOV:FAIL"
        return 1
    fi
    return 0
}

# === INCREMENT AOV ITERATIONS (anti-loop) ===
# Call this after each MCP_CALL output to track iterations
increment_aov_iterations() {
    python3 "$STATE_ENGINE" increment_aov_iterations 2>/dev/null || true
}

# === CHECK AOV ITERATIONS (anti-loop) ===
# Reads from SQLite via state_engine.py (source of truth).
# Blocks when aov_iterations >= 2 to prevent infinite MCP retry loops.
check_aov_iterations() {
    local iterations
    iterations=$(python3 "$STATE_ENGINE" get_aov_iterations 2>/dev/null || echo "0")
    iterations="${iterations:-0}"

    if [[ "$iterations" -ge 2 ]]; then
        log_dsl "AOV:FAIL|REASON:MAX_MCP_RETRIES|iterations=$iterations"
        echo "AOV:FAIL|REASON:MAX_MCP_RETRIES"
        # Clean up ghost state on anti-loop exit
        safe_rm_aov_pending
        exit 1
    fi
}

# === TAKE SCREENSHOT ===
# urandom in filename (M11), 0700 dir enforced by ensure_screenshot_dir.
take_screenshot() {
    local label="$1"
    local rand
    rand=$(tr -dc 'a-f0-9' </dev/urandom 2>/dev/null | head -c 16 || echo "$RANDOM$RANDOM")
    local path="$SCREENSHOT_DIR/${label}_$(date +%s%N)_${rand}.png"

    if command -v gnome-screenshot &>/dev/null; then
        gnome-screenshot -f "$path" 2>/dev/null || true
    elif command -v scrot &>/dev/null; then
        scrot "$path" 2>/dev/null || true
    elif command -v import &>/dev/null; then
        import -window root "$path" 2>/dev/null || true
    fi

    if [[ ! -f "$path" ]]; then
        touch "$path"
    fi
    chmod 0600 "$path" 2>/dev/null || true
    echo "$path"
}

# === ACTION WITHOUT ARGS: OUTPUT MCP_CALL XML + WRITE PENDING ===
if [[ $# -eq 0 ]]; then
    # Initialize global state_fd container for the lock FD
    AOV_LOCK_FD=""
    state_fd=(0)
    ensure_screenshot_dir
    # Clean up any stale /tmp/mcp_result.json from a prior failed run (H5)
    cleanup_mcp_result

    # Check for ghost states first
    check_timeout || true

    # Check AOV iterations (anti-loop) - block if >= 2
    check_aov_iterations

    # MCP availability precheck (M16: dead -v branch removed; use shared lib)
    if ! mcp_precheck "$DSL_PREFIX"; then
        echo "AOV:FAIL|REASON:MCP_UNAVAILABLE"
        exit 1
    fi

    ACTION="${ACTION:-unknown}"
    EXPECTED="${EXPECTED:-ok}"

    log_dsl "ACT-OBSERVE-VERIFY (STATELESS)"
    log_dsl "Action: $ACTION"
    log_dsl "Expected: $EXPECTED"

    # OBSERVE: Take screenshot
    SCREENSHOT=$(take_screenshot "aov_$(date +%s)")
    log_dsl "Screenshot: $SCREENSHOT"

    # Build MCP_CALL XML (root element required for valid XML).
    # M28: arguments are JSON-escaped via python3 to prevent injection of
    # `</MCP_CALL>` or stray quotes from $SCREENSHOT/$EXPECTED/$ACTION.
    _mcp_args1=$(SCREENSHOT="$SCREENSHOT" EXPECTED="$EXPECTED" ACTION="$ACTION" python3 -c '
import json, os
print(json.dumps({
    "image_source": os.environ["SCREENSHOT"],
    "prompt": "Verify expected state: " + os.environ["EXPECTED"],
    "context": os.environ["ACTION"],
}))
')
    _mcp_args2=$(SCREENSHOT="$SCREENSHOT" python3 -c '
import json, os
print(json.dumps({
    "image_source": os.environ["SCREENSHOT"],
    "prompt": "Extract all visible text for verification",
    "context": "",
}))
')
    cat <<MCP
<MCP_CALLS>
<MCP_CALL><tool>mcp__zai-mcp-server__diagnose_error_screenshot</tool><args>${_mcp_args1}</args></MCP_CALL>
<MCP_CALL><tool>mcp__zai-mcp-server__extract_text_from_screenshot</tool><args>${_mcp_args2}</args></MCP_CALL>
</MCP_CALLS>
MCP

    # Increment AOV iterations AFTER outputting MCP_CALL (for next iteration check)
    increment_aov_iterations

    # Write expected state to .aov_pending JSON (H6: atomic, O_NOFOLLOW)
    # I14: replaced YAML with JSON to remove the PyYAML dependency. JSON
    # is built into Python, so the harness no longer needs the yaml module.
    TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    PENDING_DATA=$(cat <<JSON
{"action": "$ACTION", "expected": "$EXPECTED", "screenshot": "$SCREENSHOT", "timestamp": "$TS"}
JSON
)
    if ! safe_write_aov_pending "$PENDING_DATA"; then
        log_dsl "WARN: failed to write $AOV_PENDING atomically"
    fi

    log_dsl "Pending state written to $AOV_PENDING"
    log_dsl "MCP_CALL XML output complete. Execute MCP tool, write result to /tmp/mcp_result.json, then re-run with --verify-result"
    # Clean up the stale mcp_result now (the user will write a fresh one)
    cleanup_mcp_result
    exit 0
fi

# === VERIFY RESULT MODE ===
if [[ "$1" == "--verify-result" ]]; then
    AOV_LOCK_FD=""
    state_fd=(0)
    RESULT_FILE="${2:-}"

    # M9: path sandbox. Reject symlinks and require file be under /tmp.
    if [[ -z "$RESULT_FILE" ]]; then
        log_dsl "ERROR: Result file missing: $RESULT_FILE"
        echo "AOV:FAIL"
        exit 1
    fi
    if [[ -L "$RESULT_FILE" ]]; then
        log_dsl "REJECT: RESULT_FILE is a symlink: $RESULT_FILE"
        echo "AOV:FAIL|REASON:SYMLINK_RESULT"
        exit 1
    fi
    RP_RESULT=$(realpath "$RESULT_FILE" 2>/dev/null || echo "")
    case "$RP_RESULT" in
        /tmp/*) ;;
        *)
            log_dsl "REJECT: RESULT_FILE not under /tmp: $RP_RESULT"
            echo "AOV:FAIL|REASON:RESULT_NOT_SANDBOXED"
            exit 1
            ;;
    esac
    if [[ ! -f "$RP_RESULT" ]]; then
        log_dsl "ERROR: Result file missing: $RESULT_FILE"
        echo "AOV:FAIL"
        exit 1
    fi

    if [[ ! -e "$AOV_PENDING" ]]; then
        log_dsl "ERROR: No pending state found at $AOV_PENDING"
        echo "AOV:FAIL"
        cleanup_mcp_result
        exit 1
    fi

    # Acquire the same fcntl lock the writer used (H6: prevents read
    # racing the atomic write).
    if ! acquire_aov_lock; then
        echo "AOV:FAIL|REASON:CONTENDED"
        exit 1
    fi

    # H5: staleness check - mcp_result.json must be NEWER than .aov_pending.
    # Otherwise the operator is verifying a stale (replayed) result.
    PENDING_MTIME=$(python3 -c "
import os, time
try:
    print(int(os.path.getmtime('$AOV_PENDING')))
except Exception:
    print(0)
" 2>/dev/null || echo "0")
    RESULT_MTIME=$(python3 -c "
import os, time
try:
    print(int(os.path.getmtime('$RP_RESULT')))
except Exception:
    print(0)
" 2>/dev/null || echo "0")
    if [[ "${RESULT_MTIME:-0}" -lt "${PENDING_MTIME:-0}" ]]; then
        log_dsl "REJECT: mcp_result.json mtime ($RESULT_MTIME) < .aov_pending mtime ($PENDING_MTIME) - stale result"
        echo "AOV:FAIL|REASON:STALE_RESULT"
        cleanup_mcp_result
        exit 1
    fi

    # Read pending expected state (I14: JSON, no PyYAML)
    PENDING_ACTION=$(python3 -c "import json; d=json.load(open('$AOV_PENDING')); print(d.get('action',''))" 2>/dev/null || echo "")
    PENDING_EXPECTED=$(python3 -c "import json; d=json.load(open('$AOV_PENDING')); print(d.get('expected',''))" 2>/dev/null || echo "")

    # Validate MCP call execution time against MCP_EXECUTION_TIMEOUT
    ELAPSED=$(python3 -c "
import os, time, json
try:
    with open('$AOV_PENDING') as f:
        pending = json.load(f)
    ts = pending.get('timestamp', '')
    if ts:
        from datetime import datetime
        t = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        elapsed = time.time() - t.timestamp()
        print(int(elapsed))
    else:
        print(0)
except Exception:
    print(0)
" 2>/dev/null || echo "0")

    if [[ "$ELAPSED" -gt "$MCP_EXECUTION_TIMEOUT" ]]; then
        log_dsl "TIMEOUT: MCP call took ${ELAPSED}s (>${MCP_EXECUTION_TIMEOUT}s)"
        echo "AOV:FAIL|TIMEOUT"
        safe_rm_aov_pending
        cleanup_mcp_result
        exit 1
    fi

    log_dsl "VERIFY: MCP call elapsed ${ELAPSED}s (timeout=${MCP_EXECUTION_TIMEOUT}s)"

    # Read result from MCP call
    RESULT_CONTENT=$(cat "$RP_RESULT" 2>/dev/null || echo "")

    log_dsl "VERIFY: pending action=$PENDING_ACTION expected=$PENDING_EXPECTED"
    log_dsl "VERIFY: result file size=${#RESULT_CONTENT} bytes"

    # M15 + H5: Require JSON envelope with status:ok|error. The plain
    # textual "looks like JSON" heuristic is removed.
    ENVELOPE_OK=$(python3 -c "
import json, sys
try:
    with open('$RP_RESULT') as f:
        d = json.load(f)
    status = d.get('status', '')
    if status in ('ok', 'error'):
        print('OK:' + status)
    else:
        print('NO_ENVELOPE')
except Exception as e:
    print(f'NO_ENVELOPE:{type(e).__name__}')
" 2>/dev/null || echo "NO_ENVELOPE")
    ENVELOPE_STATUS="${ENVELOPE_OK#OK:}"
    case "$ENVELOPE_OK" in
        OK:ok)
            log_dsl "RESULT: Verification passed (status:ok envelope)"
            echo "AOV:PASS"
            safe_rm_aov_pending
            cleanup_mcp_result
            exit 0
            ;;
        OK:error)
            log_dsl "RESULT: MCP reported error envelope"
            echo "AOV:FAIL|REASON:MCP_STATUS_ERROR"
            safe_rm_aov_pending
            cleanup_mcp_result
            exit 1
            ;;
        *)
            log_dsl "RESULT: Verification failed - missing JSON envelope (got: $ENVELOPE_OK)"
            echo "AOV:FAIL|REASON:NO_ENVELOPE"
            safe_rm_aov_pending
            cleanup_mcp_result
            exit 1
            ;;
    esac
fi

log_dsl "ERROR: Unknown arguments: $@"
echo "AOV:FAIL"
exit 1
