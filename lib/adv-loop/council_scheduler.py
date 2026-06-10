#!/usr/bin/env python3
"""
council_scheduler.py — Council auto-fire on edit counter.
SPRINT-2026-06-10 G5.

Logic:
  - On each non-whitelist edit, increment edits.counter
  - If edits.counter >= threshold AND now - council.last_at >= cooldown → fire Council
  - Whitelist: *.md, *.json (config), tests/*
  - Threshold default: 5, configurable via HARNESS_COUNCIL_THRESHOLD env var
  - Cooldown default: 3600s (1h), configurable via HARNESS_COUNCIL_COOLDOWN env var
  - On fire: reset edits.counter, set council.last_at = now, emit <MULTIAGENT_LAUNCH>
"""
import os
import sys
import time
import subprocess
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent.parent.parent
STATE_CLI = HARNESS_DIR / "lib" / "state_engine_cli.py"

THRESHOLD = int(os.environ.get("HARNESS_COUNCIL_THRESHOLD", "5"))
COOLDOWN = int(os.environ.get("HARNESS_COUNCIL_COOLDOWN", "3600"))


def is_whitelisted(file_path: str) -> bool:
    """Skip counter for docs, config, tests."""
    p = file_path.lower()
    if p.endswith(".md"):
        return True
    if p.endswith(".json"):
        return True
    if "/tests/" in p or "/test/" in p or p.startswith("tests/") or p.startswith("test/"):
        return True
    if "/.git/" in p:
        return True
    return False


def state_get(key: str, default: str = "0") -> str:
    """Read a state key, return default on error."""
    try:
        env = os.environ.copy()
        env["HARNESS_DIR"] = str(HARNESS_DIR)
        r = subprocess.run(
            ["python3", str(STATE_CLI), "get_nested", key],
            capture_output=True, text=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        val = r.stdout.strip()
        return val if val else default
    except (subprocess.TimeoutExpired, OSError):
        return default


def state_set(key: str, value: str) -> bool:
    """Set a state key."""
    try:
        env = os.environ.copy()
        env["HARNESS_DIR"] = str(HARNESS_DIR)
        r = subprocess.run(
            ["python3", str(STATE_CLI), "set_nested", key, value],
            capture_output=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        return r.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def state_set_nested(parent: str, sub: str, value: str) -> bool:
    """Set a nested state key like edits.counter."""
    try:
        env = os.environ.copy()
        env["HARNESS_DIR"] = str(HARNESS_DIR)
        # We have to use the existing set command, but it's a flat key
        # So we use a sub-key pattern: set_nested <parent>.<sub> <value>
        r = subprocess.run(
            ["python3", str(STATE_CLI), "set_nested", f"{parent}.{sub}", value],
            capture_output=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        return r.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def should_fire(edits_count: int, last_at: int, threshold: int = THRESHOLD, cooldown: int = COOLDOWN) -> bool:
    """Return True if Council should fire."""
    if edits_count < threshold:
        return False
    now = int(time.time())
    if now - last_at < cooldown:
        return False
    return True


def on_edit(file_path: str) -> str:
    """
    Called from post-tool-use/auto-verify hook on each Write/Edit.
    Returns DSL line. Outputs envelope to stderr if Council fires.
    """
    if is_whitelisted(file_path):
        return (
            f"council_scheduler:action=skipped;;"
            f"council_scheduler:reason=whitelisted;;"
            f"council_scheduler:file={file_path};;"
            f"council_scheduler:verdict=🟢 OK"
        )

    # Read current state
    counter = int(state_get("edits.counter", "0"))
    last_at = int(state_get("council.last_at", "0"))

    # Increment counter
    new_counter = counter + 1
    state_set_nested("edits", "counter", str(new_counter))

    if should_fire(new_counter, last_at):
        # FIRE
        now = int(time.time())
        state_set_nested("council", "last_at", str(now))
        state_set_nested("edits", "counter", "0")

        # Emit envelope to stderr
        import sys as _sys
        print(
            f"## <MULTIAGENT_LAUNCH reason=\"edits_threshold\" threshold=\"{THRESHOLD}\" edits=\"{new_counter}\">\n"
            f"\n"
            f"SPRINT-2026-06-10 G5: {new_counter} edits since last Council (threshold={THRESHOLD}).\n"
            f"Spawn 4 LLM-judges via Agent tool (subagent_type: nexus-ciso, nexus-qa-lead, nexus-architect, nexus-devops-lead).\n"
            f"After collecting 4 DSL lines, run:\n"
            f"  bash scripts/adversarial-gate.sh --judge-only --red \"<aggregated RED>\" --blue \"<aggregated BLUE>\"\n",
            file=_sys.stderr,
        )

        return (
            f"council_scheduler:action=fired;;"
            f"council_scheduler:edits={new_counter};;"
            f"council_scheduler:threshold={THRESHOLD};;"
            f"council_scheduler:verdict=🟢 OK"
        )
    else:
        return (
            f"council_scheduler:action=counted;;"
            f"council_scheduler:edits={new_counter};;"
            f"council_scheduler:threshold={THRESHOLD};;"
            f"council_scheduler:remaining_to_fire={max(0, THRESHOLD - new_counter)};;"
            f"council_scheduler:verdict=🟢 OK"
        )


def emit_status() -> str:
    """Return human-readable council status (for `adv-loop council-status`)."""
    counter = int(state_get("edits.counter", "0"))
    last_at = int(state_get("council.last_at", "0"))
    return f"counter={counter}/{THRESHOLD};;last_at={last_at};;cooldown={COOLDOWN}s"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: council_scheduler.py <on-edit <file_path>> | <should-fire <count> <last_at>> | <status>", file=sys.stderr)
        return 0

    cmd = sys.argv[1]
    try:
        if cmd == "on-edit":
            file_path = sys.argv[2] if len(sys.argv) > 2 else ""
            print(on_edit(file_path))
        elif cmd == "should-fire":
            count = int(sys.argv[2])
            last_at = int(sys.argv[3])
            threshold = int(sys.argv[4]) if len(sys.argv) > 4 else THRESHOLD
            cooldown = int(sys.argv[5]) if len(sys.argv) > 5 else COOLDOWN
            print("true" if should_fire(count, last_at, threshold, cooldown) else "false")
        elif cmd == "status":
            print(emit_status())
        else:
            print(f"unknown cmd: {cmd}", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"council_scheduler:error={type(e).__name__};;council_scheduler:verdict=🟡 DEGRADED")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
