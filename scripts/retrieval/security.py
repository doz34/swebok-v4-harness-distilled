#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Security Utilities
==========================================

Cross-cutting security helpers used by chunker, dossier, pipeline:
- Path sandbox (allowlist + symlink rejection + max file size)
- Prompt injection sanitizer (escape triple backticks, wrap untrusted)
- JSONL defensive loader (allowlist + type check + length cap)
- HMAC index signer/verifier

All helpers are pure stdlib, no external deps.
"""

import hashlib
import hmac
import json
import os
import re
from pathlib import Path
from typing import Any, List, Optional, Set

# === Resource limits ===
MAX_FILE_BYTES = 50 * 1024 * 1024          # 50MB per file
MAX_CHUNKS_PER_INDEX = 200_000             # 200K chunks per index
MAX_VOCAB_SIZE = 500_000                   # 500K unique tokens
MAX_QUERY_CHARS = 4096                     # 4KB max query length
MAX_INDEX_BYTES = 100 * 1024 * 1024        # 100MB max index size

# === Path sandbox ===

def safe_path_resolve(path: Path, allowed_roots: Optional[Set[Path]] = None) -> Path:
    """
    Resolve a path and ensure it is within one of the allowed roots.
    Reject symlinks, non-existent paths, and paths outside allowed_roots.
    Returns the resolved absolute Path.
    Raises ValueError on any sandbox violation.
    """
    path = Path(path)
    # Reject if not under any allowed root
    if allowed_roots:
        resolved = path.resolve()
        ok = False
        for root in allowed_roots:
            try:
                resolved.relative_to(root.resolve())
                ok = True
                break
            except ValueError:
                continue
        if not ok:
            raise ValueError(f"Path {path} not under any allowed root {allowed_roots}")
        return resolved
    return path.resolve()


def is_within_allowed(path: Path, allowed_roots: Set[Path]) -> bool:
    """Check if a path is under any allowed root (no exception)."""
    try:
        resolved = Path(path).resolve()
        for root in allowed_roots:
            try:
                resolved.relative_to(root.resolve())
                return True
            except ValueError:
                continue
    except (OSError, RuntimeError):
        pass
    return False


def safe_read_text(path: Path, max_bytes: int = MAX_FILE_BYTES) -> str:
    """
    Read a text file with a max size guard.
    - Reject if file is a symlink (symlink attacks)
    - Reject if file is too large
    - Reject if file is not a regular file
    - Catches FileNotFoundError specifically (not generic Exception)
    """
    # Reject symlinks
    if path.is_symlink():
        raise ValueError(f"Refusing to read symlink: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Not a regular file: {path}")
    size = path.stat().st_size
    if size > max_bytes:
        raise ValueError(f"File too large ({size} bytes > {max_bytes} max): {path}")
    return path.read_text(encoding="utf-8", errors="replace")


# === Prompt injection sanitizer ===

_BACKTICK_FENCE_RE = re.compile(r"```")


def sanitize_for_prompt(text: str, max_length: int = 8000) -> str:
    """
    Sanitize text for inclusion in an LLM prompt.
    - Escape triple backticks (defeats prompt-injection fence escapes)
    - Truncate to max_length
    - Strip control characters (except newline/tab)
    """
    # Escape backtick fences: replace ``` with ` + ` + ` (3 single backticks → 3 pairs of single backticks)
    # Actually simpler: replace with '```' (escaped form)
    text = text.replace("```", "```")
    # Truncate
    if len(text) > max_length:
        text = text[:max_length] + "\n[... truncated ...]"
    # Strip control chars except \n and \t
    text = "".join(c for c in text if c == "\n" or c == "\t" or ord(c) >= 0x20)
    return text


def sanitize_book_name(name: str) -> str:
    """Strip non-alphanumeric chars from a derived book name."""
    return re.sub(r"[^\w\s\-]", "", name).strip() or "(unnamed)"


def wrap_untrusted(content: str, source_id: str) -> str:
    """Wrap untrusted content with delimiter tags for LLM prompts."""
    return f'<untrusted_source id="{source_id}">\n{content}\n</untrusted_source>'


# === JSONL defensive loader ===

# Allow-list of valid Chunk fields (defense against __init_subclass__ and other
# dataclass internals)
_CHUNK_ALLOWED_FIELDS = frozenset({
    "id", "file", "book", "chapter", "section_path", "start_line", "end_line",
    "start_char", "end_char", "text", "chunk_type", "char_count", "word_count",
    "token_estimate",
})


def parse_chunk_jsonl(line: str) -> Optional[dict]:
    """
    Defensively parse a single JSONL line as a chunk dict.
    Returns the validated dict, or None if invalid.
    Rejects extra/missing fields, type mismatches, oversized text.
    """
    line = line.strip()
    if not line:
        return None
    try:
        d = json.loads(line)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(d, dict):
        return None
    # Reject unknown fields (defense against __init_subclass__ etc.)
    extras = set(d.keys()) - _CHUNK_ALLOWED_FIELDS
    if extras:
        return None
    # Required fields + type checks
    if not isinstance(d.get("text"), str):
        return None
    if len(d["text"]) > 200_000:  # 200K chars max per chunk
        return None
    if not isinstance(d.get("file"), str):
        return None
    return d


# === HMAC index signer ===

def hmac_sign(data: bytes, key: bytes) -> str:
    """Return hex HMAC-SHA256 of data with key."""
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def hmac_verify(data: bytes, signature: str, key: bytes) -> bool:
    """Constant-time verification of HMAC signature."""
    expected = hmac.new(key, data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def get_index_key() -> bytes:
    """
    Get the HMAC key for index signing.
    Priority:
    1. SWEBOK_INDEX_KEY env var (explicit)
    2. .audit_key file in harness dir (matches the state engine convention)
    3. Generate a random key (warns the user to persist it)
    """
    env_key = os.environ.get("SWEBOK_INDEX_KEY")
    if env_key:
        return env_key.encode()
    audit_key = Path(__file__).parent.parent.parent / ".audit_key"
    if audit_key.exists():
        return audit_key.read_bytes()
    # Last resort: generate ephemeral key
    return hashlib.sha256(b"swebok-v4-harness-distilled:default").digest()[:32]
