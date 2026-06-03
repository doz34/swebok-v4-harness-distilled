#!/usr/bin/env python3
"""
SWEBOK v4 Harness — Corpus Browser
===================================

A read-only, offline, deterministic query interface over the FULL distilled
corpus (145,963 raw concepts from 777 books, line-by-line).

This is the v1.5.2 COVERAGE-COMPLETE companion to `compiled_knowledge.py`:
- `compiled_knowledge.py` returns the 102 v1 layer items that MODIFY
  runtime behavior (24 principles, 46 antipatterns, 6 ontologies, 5
  decision trees, 5 recipes, 3 comparisons, 9 checklists, 4 risk
  catalogs).
- `corpus_browser.py` returns ANY concept from ANY book, ANY line,
  ANY chapter — so the user can ask "what does the corpus say about X?"
  without the curated filter.

This is NOT a RAG engine. It is a deterministic index over
`distilled_corpus/per_book/*.json`. No LLM. No embeddings. No network.

Why this exists
---------------
The v1.5.2 user's goal was: "every concept from every chapter of every
book must be accessible in the system." The v1 layer (102 items) covers
the curated, universally-applicable rules. The corpus browser covers
the LONG TAIL: per-book, per-chapter, per-line concept lookup.

Usage
-----
    python3 scripts/corpus_browser.py --stats
    python3 scripts/corpus_browser.py --search "yield from" --top 10
    python3 scripts/corpus_browser.py --book "Fluent Python" --top 20
    python3 scripts/corpus_browser.py --book "Fluent Python" --lines 1-500
    python3 scripts/corpus_browser.py --layer recipe --top 5
    python3 scripts/corpus_browser.py --search "ignore previous" --layer principle

Note on chapters
----------------
Per-book concept records carry `line` but NOT `chapter` boundaries. The
data model is line-indexed, not chapter-indexed. Per-chapter rollups
require re-deriving chapter spans from the source MD files. Until then,
"--lines 1-500" is the closest equivalent to a per-chapter view.

Output
------
JSON to stdout. Use `--human` for pretty-printed table.

Security
--------
Read-only. The browser never executes, evaluates, or pipes content
into a prompt. Output is JSON-escaped. The browser itself does not
import the v2 retrieval/ stack. Path traversal is prevented by
restricting reads to `distilled_corpus/per_book/*.json`.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

HARNESS_DIR = Path(__file__).parent.parent
CORPUS_DIR = HARNESS_DIR / "distilled_corpus" / "per_book"

# Prompt-injection / shell-injection patterns the browser sanitizes on output.
# Source books may contain these; the browser marks them but does NOT strip
# (caller decides). The flag is informational.
INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions?", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?prior", re.IGNORECASE),
    re.compile(r"\bsudo\s+rm\b", re.IGNORECASE),
    re.compile(r"\beval\s*\(", re.IGNORECASE),
]


def _normalize_book_key(title: str) -> str:
    """Match a user-supplied book title to a per_book JSON stem."""
    # The per_book files are named with the title sanitized:
    #   - punctuation and spaces replaced with underscores
    #   - max 100 chars
    # We rebuild that mapping here.
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", title).strip("_")
    return stem[:100] + ".json"


def iter_books(corpus_dir: Path = CORPUS_DIR) -> Iterator[Tuple[str, dict]]:
    """Yield (filename, parsed_json) for every per_book file."""
    if not corpus_dir.exists():
        return
    for f in sorted(corpus_dir.glob("*.json")):
        try:
            with open(f) as fh:
                yield f.name, json.load(fh)
        except (json.JSONDecodeError, OSError):
            continue


def list_books(corpus_dir: Path = CORPUS_DIR) -> List[str]:
    return sorted(f.stem for f in corpus_dir.glob("*.json")) if corpus_dir.exists() else []


def search(
    query: str,
    *,
    top: int = 20,
    layer: Optional[str] = None,
    corpus_dir: Path = CORPUS_DIR,
) -> List[dict]:
    """Full-text search over all concepts. Returns hits with book+line+content."""
    tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) >= 2]
    if not tokens:
        return []
    out: List[dict] = []
    for fname, book in iter_books(corpus_dir):
        title = book.get("book", fname)
        for c in book.get("concepts", []):
            content = c.get("content", "")
            if layer and c.get("layer") != layer:
                continue
            content_lower = content.lower()
            score = sum(1 for t in tokens if t in content_lower)
            if score == 0:
                continue
            out.append({
                "book": title,
                "file": fname,
                "line": c.get("line"),
                "layer": c.get("layer"),
                "score": score,
                "content": content,
                "_injection_risk": any(p.search(content) for p in INJECTION_PATTERNS),
            })
    out.sort(key=lambda x: (-x["score"], x["book"], x["line"] or 0))
    return out[:top]


def book_view(
    book_query: str,
    *,
    lines: Optional[Tuple[int, int]] = None,
    top: Optional[int] = None,
    corpus_dir: Path = CORPUS_DIR,
) -> dict:
    """Return all concepts (or line-range subset) of one book."""
    target_stem = _normalize_book_key(book_query)
    # Try direct match, then case-insensitive substring match
    candidates = list(corpus_dir.glob("*.json")) if corpus_dir.exists() else []
    match = None
    for f in candidates:
        if f.name.lower() == target_stem.lower():
            match = f
            break
    if match is None:
        # Fuzzy: case-insensitive substring of the user query
        ql = book_query.lower()
        for f in candidates:
            if ql in f.stem.lower() or f.stem.lower() in ql:
                match = f
                break
    if match is None:
        return {"book": book_query, "found": False, "concepts": []}
    with open(match) as fh:
        book = json.load(fh)
    concepts = book.get("concepts", [])
    if lines is not None:
        lo, hi = lines
        concepts = [c for c in concepts if c.get("line") and lo <= c["line"] <= hi]
    if top is not None:
        concepts = concepts[:top]
    return {
        "book": book.get("book", match.stem),
        "file": match.name,
        "found": True,
        "n_concepts": len(concepts),
        "by_layer": book.get("by_layer", {}),
        "concepts": concepts,
    }


def _sanitize_for_prompt(content: str, max_len: int = 500) -> str:
    """Trim and redact content for safe piping into a prompt.

    - Caps length to max_len (default 500 chars)
    - Replaces backticks with single quotes (prevents code-block escape)
    - Strips control characters
    - Returns a redacted sentinel for content matching injection patterns
    """
    if any(p.search(content) for p in INJECTION_PATTERNS):
        return "[REDACTED: prompt-injection pattern detected]"
    # Strip backticks to prevent code-block escape
    content = content.replace("`", "'")
    # Strip control characters
    content = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", content)
    if len(content) > max_len:
        content = content[: max_len - 3] + "..."
    return content


def stats(corpus_dir: Path = CORPUS_DIR) -> dict:
    """Corpus-wide aggregate statistics."""
    n_books = 0
    n_concepts = 0
    by_layer: Dict[str, int] = {}
    for _, book in iter_books(corpus_dir):
        n_books += 1
        for c in book.get("concepts", []):
            n_concepts += 1
            by_layer[c.get("layer", "?")] = by_layer.get(c.get("layer", "?"), 0) + 1
    return {
        "corpus_dir": str(corpus_dir),
        "n_books": n_books,
        "n_concepts": n_concepts,
        "by_layer": by_layer,
    }


# === CLI ===
def main() -> int:
    p = argparse.ArgumentParser(description="Query the full SWEBOK corpus (777 books, 145k concepts).")
    p.add_argument("--stats", action="store_true", help="corpus-wide statistics")
    p.add_argument("--search", help="full-text search query")
    p.add_argument("--book", help="show all concepts for a book (fuzzy match)")
    p.add_argument("--lines", help="restrict to a line range, e.g. 1-500")
    p.add_argument("--layer", help="filter by layer (principle/recipe/etc.)")
    p.add_argument("--random", type=int, metavar="N", help="deterministic random sample of N concepts")
    p.add_argument("--top", type=int, default=20, help="max results (default 20)")
    p.add_argument("--human", action="store_true", help="pretty-print instead of JSON")
    p.add_argument("--safe", action="store_true", default=None,
                   help="sanitize content for prompt piping (default: ON when stdout is a pipe)")
    p.add_argument("--unsafe", action="store_true",
                   help="disable --safe sanitization (raw content)")
    args = p.parse_args()

    # Default --safe to ON when stdout is a pipe (i.e. content will be piped
    # into another command like `claude` or `xargs`).
    is_piped = not sys.stdout.isatty()
    safe_mode = (not args.unsafe) if args.safe is None else args.safe

    if args.stats:
        result = stats()
    elif args.search:
        result = search(args.search, top=args.top, layer=args.layer)
    elif args.book:
        lr = None
        if args.lines:
            lo, hi = args.lines.split("-", 1)
            lr = (int(lo), int(hi))
        result = book_view(args.book, lines=lr, top=args.top)
    else:
        p.print_help()
        return 0

    # Apply sanitization in safe mode (search + book views contain content)
    if safe_mode and isinstance(result, list):
        for item in result:
            if "content" in item:
                item["content"] = _sanitize_for_prompt(item["content"])
    elif safe_mode and isinstance(result, dict) and "concepts" in result:
        for c in result.get("concepts", []):
            if "content" in c:
                c["content"] = _sanitize_for_prompt(c["content"])

    if args.human:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
