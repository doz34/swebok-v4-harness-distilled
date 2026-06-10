#!/usr/bin/env python3
"""
auto_trigger.py — UserPromptSubmit intent detection for SWEBOK v4 harness.

SPRINT-2026-06-10 G1: Detect the user's intent from a free-form prompt
and assign the right SDLC phase. Wired in pre-tool-use/auto-trigger-hook.sh.

Architecture (4 layers, deterministic-first, LLM-last):
  Layer 1: Manual override   — prompt contains "phase=N" → force
  Layer 2: Exact-pattern     — regex match against intent-map.json
  Layer 3: Keyword scoring   — TF-style word overlap with phase descriptions
  Layer 4: Fallback          — return "P0" with confidence=0.0, log

Per Fowler (harness engineering) + CE-Harness practice:
  - Latency budget: 50ms p50 / 100ms p95 / 500ms p99
  - Cache hit > 80% (in-memory dict, TTL 1h)
  - Fail-open: never block legitimate work
  - DSL output: `auto_trigger:phase=N;confidence=0.X;intent=foo;fallback=bar`

Usage:
  python3 lib/auto_trigger.py "Write tests for the user model"
  python3 lib/auto_trigger.py --json "Refactor the auth module"

Exit code: always 0 (fail-open per CLAUDE.md L1, L4).
"""
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, Dict, List

HARNESS_DIR = Path(__file__).resolve().parent.parent
INTENT_MAP = HARNESS_DIR / "intent-map.json"
INTENT_DETECTOR = HARNESS_DIR / "intent-detector.py"

# Per-phase keywords (lightweight, hand-tuned for fast path).
# Order matters: P0..P10. First match wins on tie.
PHASE_KEYWORDS: Dict[str, List[str]] = {
    "P0":  ["discover", "stakeholder", "charter", "context map", "discovery", "explore needs"],
    "P1":  ["feasibility", "go no-go", "go/no-go", "roi", "payback", "concept", "feasible", "viable"],
    "P2":  ["requirement", "user story", "acceptance criteria", "spec", "nfr", "rtm", "srs", "use case"],
    "P3":  ["architecture", "adr", "c4", "madr", "container", "component", "archi", "tech choice"],
    "P4":  ["design", "api contract", "openapi", "swagger", "data model", "sequence diagram", "interface"],
    "P5":  ["implement", "refactor", "code", "module", "function", "class", "method", "antipattern"],
    "P6":  ["test", "coverage", "mutation", "integration test", "e2e", "qa", "regression", "smoke"],
    "P7":  ["deploy", "release", "rollback", "canary", "blue green", "smoke test", "production deploy"],
    "P8":  ["incident", "on-call", "runbook", "slo", "sli", "postmortem", "outage", "alert", "monitoring"],
    "P9":  ["maintain", "tech debt", "refactor plan", "perfective", "corrective", "adaptive", "preventive"],
    "P10": ["retire", "decommission", "archival", "rgpd", "closure", "eol", "end of life", "data migration"],
}

# In-memory cache: prompt-hash -> (phase, confidence, ts)
_CACHE: Dict[str, Tuple[str, float, float]] = {}
_CACHE_TTL = 3600  # 1 hour


def _normalize(prompt: str) -> str:
    """Normalize prompt for cache key + pattern match."""
    return re.sub(r"\s+", " ", prompt.strip().lower())


def _cache_key(prompt: str) -> str:
    return _normalize(prompt)[:500]


def _cache_get(key: str) -> Optional[Tuple[str, float]]:
    """Get cached (phase, confidence) if not expired."""
    if key in _CACHE:
        phase, conf, ts = _CACHE[key]
        if time.time() - ts < _CACHE_TTL:
            return phase, conf
        del _CACHE[key]
    return None


def _cache_put(key: str, phase: str, conf: float) -> None:
    """Cache (phase, confidence, timestamp). Cap at 256 entries to avoid mem bloat."""
    if len(_CACHE) > 256:
        # FIFO evict oldest 64
        sorted_keys = sorted(_CACHE, key=lambda k: _CACHE[k][2])
        for k in sorted_keys[:64]:
            del _CACHE[k]
    _CACHE[key] = (phase, conf, time.time())


def layer1_manual_override(prompt: str) -> Optional[Tuple[str, float]]:
    """Layer 1: manual override via 'phase=N' in prompt."""
    m = re.search(r"\bphase\s*=\s*(P?\d{1,2})\b", prompt, re.IGNORECASE)
    if m:
        n = m.group(1).upper()
        if not n.startswith("P"):
            n = "P" + n
        return n, 1.0
    return None


def layer2_pattern_match(prompt: str) -> Optional[Tuple[str, float]]:
    """Layer 2: regex pattern match against intent-map.json (if present)."""
    if not INTENT_MAP.exists():
        return None
    try:
        data = json.loads(INTENT_MAP.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict) or "intents" not in data:
        return None
    p_norm = _normalize(prompt)
    best_phase = None
    best_score = 0
    for intent in data["intents"]:
        if not isinstance(intent, dict):
            continue
        phase = intent.get("phase", "")
        patterns = intent.get("patterns", [])
        if not isinstance(patterns, list):
            continue
        for pat in patterns:
            if not isinstance(pat, str):
                continue
            try:
                if re.search(pat, p_norm, re.IGNORECASE):
                    return phase, 0.9
            except re.error:
                continue
    return None


def layer3_keyword_scoring(prompt: str) -> Optional[Tuple[str, float]]:
    """Layer 3: keyword overlap scoring per phase.

    Score = sqrt(matching_keywords) / sqrt(total_kws_in_phase + 1)
    - 1 match in phase with 5 kws: sqrt(1)/sqrt(6) = 0.408
    - 2 matches in phase with 5 kws: sqrt(2)/sqrt(6) = 0.577
    - Threshold for conf: max(0.6, score + 0.4) → 1 match = 0.6+, 2 matches = 0.85
    """
    p_norm = _normalize(prompt)
    if not p_norm:
        return None
    # Tokenize
    words = set(w for w in re.findall(r"\b\w{3,}\b", p_norm))
    if not words:
        return None
    import math
    scores: Dict[str, float] = {}
    for phase, kws in PHASE_KEYWORDS.items():
        hits = 0
        for kw in kws:
            kw_words_in_kw = [w for w in re.findall(r"\b\w{3,}\b", kw.lower())]
            if not kw_words_in_kw:
                continue
            # Multi-word kw: ALL kw words must match a prompt word (substring).
            # Single-word kw: substring match (handles test/tests morphology).
            if len(kw_words_in_kw) == 1:
                kw_lower = kw_words_in_kw[0]
                if any(kw_lower in w or w in kw_lower for w in words if len(w) >= 3):
                    hits += 1
            else:
                if all(
                    any(kw_w in w or w in kw_w for w in words if len(w) >= 3)
                    for kw_w in kw_words_in_kw
                ):
                    hits += 1
        if hits > 0:
            score = math.sqrt(hits) / math.sqrt(len(kws) + 1)
            scores[phase] = score
    if not scores:
        return None
    # Prefer later phases (P5+) over P0-P4 when scores tie — P5+ are more specific.
    # Sort by score desc, then phase number desc.
    best = max(scores.items(), key=lambda x: (x[1], int(x[0][1:]) if x[0][1:].isdigit() else 0))
    phase = best[0]
    score = best[1]
    conf = min(0.85, max(0.6, score + 0.4))
    if conf < 0.5:
        return None
    return phase, round(conf, 3)


def layer4_fallback(prompt: str) -> Tuple[str, float]:
    """Layer 4: fallback — no detection possible."""
    return "P0", 0.0


def detect_intent(prompt: str) -> Tuple[str, float, str, str]:
    """
    Detect intent from prompt. Returns (phase, confidence, intent_label, fallback_layer).

    4-layer pipeline with caching. Always returns a phase (never raises).
    """
    t0 = time.time()
    if not prompt or not prompt.strip():
        return "P0", 0.0, "empty", "L4"

    # Cache check
    key = _cache_key(prompt)
    cached = _cache_get(key)
    if cached is not None:
        elapsed_ms = (time.time() - t0) * 1000
        if elapsed_ms > 50:
            # Log slow cache hit for diagnosis
            pass
        return cached[0], cached[1], "cache", f"elapsed_ms={elapsed_ms:.1f}"

    # Layer 1: manual override
    r = layer1_manual_override(prompt)
    if r is not None:
        _cache_put(key, r[0], r[1])
        return r[0], r[1], "manual_override", "L1"

    # Layer 2: pattern match (intent-map.json)
    r = layer2_pattern_match(prompt)
    if r is not None:
        _cache_put(key, r[0], r[1])
        return r[0], r[1], "pattern", "L2"

    # Layer 3: keyword scoring
    r = layer3_keyword_scoring(prompt)
    if r is not None:
        _cache_put(key, r[0], r[1])
        return r[0], r[1], "keywords", "L3"

    # Layer 4: fallback
    phase, conf = layer4_fallback(prompt)
    _cache_put(key, phase, conf)
    return phase, conf, "fallback", "L4"


def emit_dsl(phase: str, conf: float, intent: str, fallback: str) -> str:
    """Emit swebok DSL (KEY=VALUE;;KEY=VALUE)."""
    return (
        f"auto_trigger:phase={phase};;"
        f"auto_trigger:confidence={conf:.3f};;"
        f"auto_trigger:intent={intent};;"
        f"auto_trigger:fallback={fallback};;"
        f"auto_trigger:verdict=🟢 OK"
    )


def write_intent_to_state(phase: str, conf: float) -> bool:
    """
    Write intent.phase, intent.confidence, intent.timestamp to state DB.
    Only writes if confidence >= threshold (0.5).
    Returns True if written, False otherwise.
    """
    if conf < 0.5:
        return False
    state_cli = HARNESS_DIR / "lib" / "state_engine_cli.py"
    if not state_cli.exists():
        return False
    import subprocess
    try:
        ts = int(time.time())
        env = os.environ.copy()
        env["HARNESS_DIR"] = str(HARNESS_DIR)
        # set_nested key.subkey value
        r1 = subprocess.run(
            ["python3", str(state_cli), "set_nested", "intent.phase", phase],
            capture_output=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        r2 = subprocess.run(
            ["python3", str(state_cli), "set_nested", "intent.confidence", f"{conf:.3f}"],
            capture_output=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        r3 = subprocess.run(
            ["python3", str(state_cli), "set_nested", "intent.timestamp", str(ts)],
            capture_output=True, timeout=5, env=env, cwd=str(HARNESS_DIR),
        )
        return all(r.returncode == 0 for r in (r1, r2, r3))
    except (subprocess.TimeoutExpired, OSError):
        return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: auto_trigger.py [--json] <prompt>", file=sys.stderr)
        return 0  # fail-open

    args = sys.argv[1:]
    json_mode = False
    if "--json" in args:
        json_mode = True
        args.remove("--json")

    if not args:
        return 0

    prompt = " ".join(args)
    try:
        phase, conf, intent, layer = detect_intent(prompt)
    except Exception as e:
        # Catastrophic fail-open
        print(f"auto_trigger:error={type(e).__name__};;auto_trigger:verdict=🟡 DEGRADED")
        return 0

    dsl = emit_dsl(phase, conf, intent, layer)

    if json_mode:
        result = {
            "phase": phase,
            "confidence": conf,
            "intent": intent,
            "fallback": layer,
            "prompt": prompt[:200],
        }
        print(json.dumps(result))
    else:
        print(dsl)

    # Write to state DB if confidence sufficient
    if conf >= 0.5:
        write_intent_to_state(phase, conf)

    return 0


if __name__ == "__main__":
    sys.exit(main())
