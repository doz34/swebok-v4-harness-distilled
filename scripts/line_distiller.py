#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Line-by-Line Concept Distiller
======================================================

Streams over the entire corpus line by line. At each line:
1. Detects structural elements (headings, lists, code, bold)
2. Classifies if the line contains a concept
3. Decides which distilled layer to incorporate it into
4. Maintains provenance (book, line, context)

Classification rules (deterministic, no LLM):
- "X is a/an..." → principle
- "X should/shouldn't/must/mustn't..." → principle
- "Don't X", "Avoid X", "Never X" → antipattern
- "When to use X" / "X is best for" → decision tree node
- Numbered list (1. 2. 3.) → recipe step
- Checkbox [ ] / - [x] → checklist item
- Bold term in heading → graph entity
- Question with "?" → FAQ entry

Each extracted concept carries:
- id (sha256 of book+line+content)
- book (derived from path)
- line (1-indexed)
- layer (principle|antipattern|decision|recipe|checklist|entity|faq)
- content (the extracted text)
- citations (book, line range, file path)

Usage:
    python3 scripts/line_distiller.py /path/to/corpus/ --output distilled_incremental/
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HARNESS_DIR = Path(__file__).parent.parent


def make_id(book: str, line: int, content: str) -> str:
    return f"ld_{hashlib.sha256(f'{book}:{line}:{content}'.encode()).hexdigest()[:12]}"


def derive_book(path: Path) -> str:
    """Same algorithm as chunker.py: clean book name from file path."""
    name = path.stem
    name = re.sub(r"^\d+_?", "", name)
    name = re.sub(r"_\d+_?", " ", name)
    name = re.sub(r"[\(\[]\d{10,}[\)\]]", "", name)
    name = name.replace("_", " ").replace("-", " ").strip()
    parts = []
    upper = {"SQL", "API", "REST", "HTTP", "CSS", "HTML", "JSON", "XML", "AI", "ML",
             "UI", "UX", "OOP", "MVC", "MVP", "CLI", "K8S", "AWS", "GCP", "CI", "CD",
             "JS", "TS", "GO", "CRDT", "OLAP", "OLTP", "OAuth", "JWT", "TLS", "SSL",
             "DDD", "TDD", "BDD", "OAuth", "SQLite", "NoSQL", "ORM", "RPC", "gRPC",
             "GraphQL", "OpenAPI", "SOAP", "CSRF", "XSS", "DDoS", "SSRF", "ACID",
             "CAP", "BASE", "JWT", "SAML", "OAuth", "SSO", "MFA", "RBAC", "ABAC"}
    for w in name.split():
        if w.upper() in upper:
            parts.append(w.upper())
        else:
            parts.append(w.capitalize())
    return " ".join(parts) if parts else path.stem


# === Classification patterns ===

_PRINCIPLE_PATTERNS = [
    re.compile(r"^(?:the\s+)?(\w[\w\s\-]{2,40}?)\s+(?:is|are)\s+(?:a|an|the)\s+([a-z][^.!?\n]{10,200})", re.IGNORECASE),
    re.compile(r"^(\w[\w\s\-]{2,40}?)\s+(?:should|must|needs? to|have to|requires?)\s+([a-z][^.!?\n]{10,200})", re.IGNORECASE),
    re.compile(r"^(?:always|never|avoid|do not|don't|do)\s+([a-z][^.!?\n]{10,200})", re.IGNORECASE),
    re.compile(r"^(?:principle|rule|guideline)\s*:\s*([a-z][^.!?\n]{20,300})", re.IGNORECASE),
    re.compile(r"^([A-Z][A-Za-z0-9_\-]+(?:\s+[A-Z][A-Za-z0-9_\-]+){0,4})\s+(?:is|are|means|denotes)\s+([a-z][^.!?\n]{10,200})"),
]

_ANTIPATTERN_PATTERNS = [
    re.compile(r"^(?:don't|do not|never|avoid)\s+([a-z][^.!?\n]{10,200})", re.IGNORECASE),
    re.compile(r"^(?:anti-?pattern|smell|warning|caution)\s*:\s*([a-z][^.!?\n]{20,300})", re.IGNORECASE),
    re.compile(r"^(?:pitfall|trap|gotcha)\s*:\s*([a-z][^.!?\n]{20,300})", re.IGNORECASE),
    re.compile(r"^(\w[\w\s\-]{2,40}?)\s+(?:is|are)\s+(?:an?\s+)?(?:anti-?pattern|smell|bad practice)", re.IGNORECASE),
]

_DECISION_PATTERNS = [
    re.compile(r"^(?:when to use|when not to use|use)\s+([a-z][^:?!\n]{5,80})", re.IGNORECASE),
    re.compile(r"^([\w\s]+)\s+is\s+(?:best|ideal|recommended|suitable)\s+for\s+([a-z][^.\n]{5,100})", re.IGNORECASE),
    re.compile(r"^([\w\s]+)\s+is\s+(?:not\s+)?(?:recommended|advisable)\s+for\s+([a-z][^.\n]{5,100})", re.IGNORECASE),
    re.compile(r"^use\s+([\w\s]+)\s+when\s+([a-z][^.\n]{5,100})", re.IGNORECASE),
    re.compile(r"^choose\s+([\w\s]+)\s+(?:when|if|for)\s+([a-z][^.\n]{5,100})", re.IGNORECASE),
]

_RECIPE_PATTERNS = [
    re.compile(r"^(?:step\s+(\d+)[:.]\s+|(\d+)[.)]\s+)([a-z][^.!?\n]{10,200})", re.IGNORECASE),
    re.compile(r"^(?:to\s+(\w+)\s+,?\s+(?:you\s+)?(?:should|need to|can)\s+)([a-z][^.!?\n]{10,200})", re.IGNORECASE),
    re.compile(r"^(?:how to\s+)([a-z][^:?!\n]{5,80})", re.IGNORECASE),
    re.compile(r"^(?:first|then|next|finally)[,.\s]+([a-z][^.!?\n]{10,200})", re.IGNORECASE),
]

_CHECKLIST_PATTERNS = [
    re.compile(r"^[\s]*-\s*\[\s*[xX ]\s*\]\s+(.+)$"),
    re.compile(r"^[\s]*\*\s*\[\s*[xX ]\s*\]\s+(.+)$"),
    re.compile(r"^[\s]*\d+\.\s*\[\s*[xX ]\s*\]\s+(.+)$"),
    re.compile(r"^(?:check|verify|ensure|confirm|make sure)\s+(?:that\s+)?([a-z][^.!?\n]{10,200})", re.IGNORECASE),
]

_FAQ_PATTERNS = [
    re.compile(r"^(?:what is|what are|how does|why|when should|how can|is it)\s+([^.!?\n]{5,150})\?$", re.IGNORECASE),
    re.compile(r"^(?:Q|Question)\s*:\s*([^.!?\n]{5,150})", re.IGNORECASE),
]

_BOLD_TERM_RE = re.compile(r"\*\*([A-Z][A-Za-z0-9_\-]+(?:\s+[A-Z][A-Za-z0-9_\-]+){0,4})\*\*")


def classify_line(line: str) -> Optional[Tuple[str, str, str]]:
    """
    Classify a single line. Returns (layer, id_type, content) or None.
    layer ∈ {principle, antipattern, decision, recipe, checklist, faq, entity}
    """
    line = line.strip()
    if len(line) < 10 or len(line) > 500:
        return None
    # Try each pattern in priority order
    for pattern in _ANTIPATTERN_PATTERNS:
        m = pattern.match(line)
        if m:
            return ("antipattern", "ap_text", m.group(0))
    for pattern in _PRINCIPLE_PATTERNS:
        m = pattern.match(line)
        if m:
            return ("principle", "pr_text", m.group(0))
    for pattern in _DECISION_PATTERNS:
        m = pattern.match(line)
        if m:
            return ("decision", "dec_text", m.group(0))
    for pattern in _RECIPE_PATTERNS:
        m = pattern.match(line)
        if m:
            return ("recipe", "rec_text", m.group(0))
    for pattern in _CHECKLIST_PATTERNS:
        m = pattern.match(line)
        if m:
            return ("checklist", "cl_text", m.group(1).strip() if m.lastindex and m.lastindex >= 1 else m.group(0))
    for pattern in _FAQ_PATTERNS:
        m = pattern.match(line)
        if m:
            return ("faq", "faq_text", m.group(0))
    # Bold terms are candidate entities
    bold = _BOLD_TERM_RE.search(line)
    if bold:
        return ("entity", "ent_text", bold.group(1))
    return None


def distill_file(path: Path, layers: dict) -> int:
    """
    Distill concepts from a single file, line by line.
    Appends to layers dict. Returns number of lines processed.
    """
    book = derive_book(path)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, start=1):
                classification = classify_line(line)
                if classification is None:
                    continue
                layer, id_type, content = classification
                cid = make_id(book, line_num, content)
                layers[layer][cid] = {
                    "id": cid,
                    "book": book,
                    "file": str(path),
                    "line": line_num,
                    "content": content,
                    "type": id_type,
                }
    except Exception as e:
        print(f"  [warn] {path}: {e}", file=sys.stderr)
    return 0


def distill_directory(directory: Path, output_dir: Path, min_books: int = 1) -> dict:
    """
    Distill concepts from every file in a directory.
    Writes per-book concept files AND an aggregate.

    min_books: minimum number of books a concept must appear in to be kept
    in the aggregate. Default 1 = keep everything. Use a higher value to
    filter for cross-book consensus.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    per_book_dir = output_dir / "per_book"
    per_book_dir.mkdir(exist_ok=True)
    # First pass: extract per-book
    per_book_layers: Dict[str, Dict[str, Dict]] = {}
    files = sorted(directory.rglob("*.md"))
    files += sorted(directory.rglob("*.txt"))
    files = list(set(files))
    t0 = time.time()
    n_files = 0
    for path in files:
        n_files += 1
        if n_files % 50 == 0:
            elapsed = time.time() - t0
            rate = n_files / max(elapsed, 0.1)
            print(f"  [{n_files}/{len(files)}] {rate:.1f} files/sec")
        book = derive_book(path)
        book_layers: Dict[str, Dict[str, Dict]] = defaultdict(dict)
        distill_file(path, book_layers)
        per_book_layers[book] = book_layers
        # Write per-book file
        book_total = sum(len(v) for v in book_layers.values())
        if book_total > 0:
            per_book_file = per_book_dir / f"{book[:100].replace('/', '_').replace(' ', '_')}.json"
            with open(per_book_file, "w") as f:
                json.dump({
                    "book": book,
                    "file": str(path),
                    "n_concepts": book_total,
                    "by_layer": {k: len(v) for k, v in book_layers.items()},
                    "concepts": [
                        {"layer": layer, "line": item["line"], "content": item["content"]}
                        for layer, items in book_layers.items()
                        for item in items.values()
                    ],
                }, f, indent=2, ensure_ascii=False)
    # Second pass: aggregate by content, keeping items that appear in min_books+ books
    content_groups: Dict[Tuple[str, str], List[Dict]] = defaultdict(list)
    for book, book_layers in per_book_layers.items():
        for layer, items in book_layers.items():
            for cid, item in items.items():
                norm = re.sub(r"\s+", " ", item["content"].lower()).strip()[:200]
                key = (layer, norm)
                content_groups[key].append({**item, "book": book})
    final_layers: Dict[str, List[Dict]] = defaultdict(list)
    for (layer, norm), items in content_groups.items():
        if len(items) >= min_books:
            rep = items[0]
            rep["n_books"] = len(items)
            rep["books"] = sorted(set(it["book"] for it in items))[:20]
            final_layers[layer].append(rep)
    for layer_name, items in final_layers.items():
        out_file = output_dir / f"distilled_{layer_name}.json"
        with open(out_file, "w") as f:
            json.dump({
                "layer": layer_name,
                "n_items": len(items),
                "min_books_threshold": min_books,
                "items": sorted(items, key=lambda x: -x["n_books"]),
            }, f, indent=2, ensure_ascii=False)
    total_items = sum(len(v) for v in final_layers.values())
    return {
        "n_files": n_files,
        "n_books": len(per_book_layers),
        "n_raw_items": sum(len(it) for bl in per_book_layers.values() for it in bl.values()),
        "n_items": total_items,
        "per_layer": {k: len(v) for k, v in final_layers.items()},
        "elapsed_sec": round(time.time() - t0, 2),
        "min_books": min_books,
    }


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Line-by-line concept distiller")
    parser.add_argument("directory", help="Corpus directory to distill")
    parser.add_argument("--output", "-o", default="distilled_incremental", help="Output dir")
    args = parser.parse_args()
    result = distill_directory(Path(args.directory), Path(args.output))
    print(json.dumps(result, indent=2))
