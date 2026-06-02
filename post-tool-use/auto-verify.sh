#!/usr/bin/env bash
# SWEBOK v4 Harness - PostToolUse Auto-Verify + LINT CIRCUIT BREAKER
# Auto-lint + syntax check after Write/Edit
# FAIL-SECURE: trap 'exit 1' ERR
#
# AUDIT-2026-06-01 FIX (DevOps-Gap2): previously crashed on every invocation
# because $2/$3 were unbound when Claude Code invoked this hook (stdin JSON,
# not positional args). Now reads stdin JSON like phase-guard.sh; positional
# args still work as a fallback for direct CLI invocation.

set -euo pipefail
# FAIL-SECURE: block on any internal error (lint failures alone do not trigger this)
trap 'echo "WARN:HOOK_INTERNAL_ERROR: Blocking action due to script crash"; exit 1' ERR

HARNESS_DIR="${HARNESS_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
STATE_ENGINE="$HARNESS_DIR/scripts/lib/state_engine.py"
# State of truth: .swebok_state.db. STATE_FILE is NOT read.

# === ARG PARSING: stdin JSON (Claude Code contract) OR positional args (CLI test) ===
TOOL="${1:-}"
FILE="${2:-}"
LITE_FLAG="${3:-}"

# If no positional args, try stdin JSON (Claude Code's standard hook contract).
if [[ -z "$TOOL" && -z "$FILE" ]]; then
    # Read up to 1 MB of stdin with a short timeout; missing stdin = quiet no-op
    # (PostToolUse with no payload is a normal Claude Code invocation pattern).
    json_input=""
    if read -r -t 1 -d '' json_input < /dev/stdin 2>/dev/null || true; then
        :
    fi
    if [[ -n "$json_input" ]]; then
        parsed=$(python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
except Exception:
    sys.exit(0)
ti = d.get('tool_input', d.get('params', {})) or {}
file_path = ti.get('file_path','') or ti.get('notebook_path','') or ''
tool_name = d.get('tool_name','') or ''
print(tool_name + '\x1f' + file_path)
" <<< "$json_input" 2>/dev/null || echo "")
        if [[ -n "$parsed" ]]; then
            TOOL="${parsed%%$'\x1f'*}"
            FILE="${parsed#*$'\x1f'}"
        fi
    fi
fi

LITE_MODE=false
if [[ "$LITE_FLAG" == "--lite" ]]; then
    LITE_MODE=true
fi

# No file to verify → quiet no-op (Read/Skill/Task/Agent/WebFetch tools land here).
if [[ -z "$FILE" ]] || [[ ! -f "$FILE" ]]; then
    exit 0
fi

# Get current phase from state_engine.py
get_phase() {
    local phase
    phase=$(python3 "$STATE_ENGINE" get "current_phase" 2>/dev/null || echo "UNKNOWN")
    echo "${phase:-UNKNOWN}"
}

CURRENT=$(get_phase)
PHASE_NUM="${CURRENT:1:1}"

echo "[AUTO-VERIFY] File: $FILE | Phase: $CURRENT | Lite: $LITE_MODE"

# === LITE MODE: Skip heavy linting ===
if [[ "$LITE_MODE" == "true" ]]; then
    echo "[AUTO-VERIFY] Lite mode: syntax check only"
    case "$FILE" in
        *.py)
            python3 -m py_compile "$FILE" 2>&1 || echo "[AUTO-VERIFY] SYNTAX ERROR in $FILE"
            ;;
        *.js)
            node --check "$FILE" 2>&1 || echo "[AUTO-VERIFY] SYNTAX ERROR in $FILE"
            ;;
        *.ts)
            npx tsc --noEmit "$FILE" 2>&1 || echo "[AUTO-VERIFY] SYNTAX ERROR in $FILE"
            ;;
        *.go)
            go build -o /dev/null "$FILE" 2>&1 || echo "[AUTO-VERIFY] BUILD ERROR in $FILE"
            ;;
    esac
    exit 0
fi

# === FULL MODE: Language-specific linting ===
LINT_FAILED=0
case "$FILE" in
    *.py)
        echo "[AUTO-VERIFY] Python: Running lint checks..."
        if command -v ruff &>/dev/null; then
            if ! ruff check "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] WARN: ruff issues on $FILE"
                LINT_FAILED=1
            fi
        elif command -v pyflakes &>/dev/null; then
            if ! pyflakes "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] WARN: pyflakes issues on $FILE"
                LINT_FAILED=1
            fi
        fi
        ;;
    *.ts|*.js)
        echo "[AUTO-VERIFY] JS/TS: Running lint checks..."
        if command -v npx &>/dev/null && [[ -f "package.json" ]]; then
            if ! npx eslint "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] WARN: eslint issues on $FILE"
                LINT_FAILED=1
            fi
        fi
        ;;
    *.go)
        echo "[AUTO-VERIFY] Go: Running lint checks..."
        if command -v golangci-lint &>/dev/null; then
            if ! golangci-lint run "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] WARN: golangci issues on $FILE"
                LINT_FAILED=1
            fi
        elif command -v gofmt &>/dev/null; then
            if ! gofmt -l "$FILE" >/dev/null 2>&1; then
                echo "[AUTO-VERIFY] WARN: gofmt issues on $FILE"
                LINT_FAILED=1
            fi
        fi
        ;;
    *.java)
        echo "[AUTO-VERIFY] Java: Running checkstyle..."
        if command -v checkstyle &>/dev/null; then
            if ! checkstyle "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] WARN: checkstyle issues on $FILE"
                LINT_FAILED=1
            fi
        fi
        ;;
    *.rs)
        echo "[AUTO-VERIFY] Rust: Running clippy..."
        if command -v cargo &>/dev/null; then
            if ! cargo check --quiet 2>&1; then
                echo "[AUTO-VERIFY] WARN: clippy issues"
                LINT_FAILED=1
            fi
        fi
        ;;
esac

# === LINT CIRCUIT BREAKER LOGIC ===
if [[ "$LINT_FAILED" -eq 1 ]]; then
    echo "[AUTO-VERIFY] Lint failed - incrementing lint_attempts..."

    # Call Python state_engine to increment lint counter
    lint_attempts=$(python3 "$STATE_ENGINE" increment_lint 2>/dev/null || echo "0")

    echo "[AUTO-VERIFY] lint_attempts: $lint_attempts"

    if [[ "$lint_attempts" -ge 3 ]]; then
        echo "LINT_DEADLOCK_WARNING: 3 attempts failed. Requires human review."
        echo "[AUTO-VERIFY] Circuit breaker triggered at $lint_attempts attempts - breaking loop"
        exit 0  # EXIT 0 to break the loop per M2 mandate
    fi
else
    # Lint passed - reset counter
    python3 "$STATE_ENGINE" reset_lint 2>/dev/null || true
fi

# === P5+ syntax validation ===
if [[ "$PHASE_NUM" =~ ^[56789]$ ]]; then
    echo "[AUTO-VERIFY] Phase $PHASE_NUM: Running syntax validation..."
    case "$FILE" in
        *.py)
            if ! python3 -m py_compile "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] ERROR: Python syntax error in $FILE"
                exit 1
            fi
            ;;
        *.js)
            if ! node --check "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] ERROR: JavaScript syntax error in $FILE"
                exit 1
            fi
            ;;
        *.ts)
            if command -v npx &>/dev/null; then
                if ! npx tsc --noEmit "$FILE" 2>&1; then
                    echo "[AUTO-VERIFY] ERROR: TypeScript syntax error in $FILE"
                    exit 1
                fi
            fi
            ;;
        *.go)
            if ! go build -o /dev/null "$FILE" 2>&1; then
                echo "[AUTO-VERIFY] ERROR: Go build error in $FILE"
                exit 1
            fi
            ;;
        *.java)
            if command -v javac &>/dev/null; then
                if ! javac -d /tmp "$FILE" 2>&1; then
                    echo "[AUTO-VERIFY] ERROR: Java compile error in $FILE"
                    exit 1
                fi
            fi
            ;;
    esac
fi

echo "[AUTO-VERIFY] PASSED: $FILE"
exit 0