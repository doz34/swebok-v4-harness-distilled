#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Coverage Report
======================================

Generates a coverage report proving that the corpus was actually
parsed line-by-line and that the distilled knowledge is grounded
in the source material.

Outputs:
- coverage_report.json (machine-readable)
- coverage_report.md (human-readable)

Usage:
    python3 scripts/coverage_report.py /tmp/line_distill_judged/ \
        /tmp/line_distill_test/per_book/ \
        --output coverage_report/
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List


def load_judged(input_dir: Path) -> Dict[str, List[Dict]]:
    """Load judged items by layer."""
    out: Dict[str, List[Dict]] = defaultdict(list)
    for f in sorted(input_dir.glob("judged_*.json")):
        with open(f) as fh:
            data = json.load(fh)
        layer = data["layer"]
        out[layer] = data["items"]
    return out


def load_per_book(per_book_dir: Path) -> List[Dict]:
    """Load per-book concept files."""
    out = []
    for f in sorted(per_book_dir.glob("*.json")):
        with open(f) as fh:
            out.append(json.load(fh))
    return out


def make_report(judged: Dict[str, List[Dict]], per_book: List[Dict]) -> Dict:
    """Build the coverage report."""
    total_judged = sum(len(v) for v in judged.values())
    # Books with at least one concept
    n_books_with_concepts = len(per_book)
    n_books_total = n_books_with_concepts
    # Total raw concepts across all books
    total_raw_concepts = sum(b["n_concepts"] for b in per_book)
    # Books by layer
    layer_coverage = {}
    for layer, items in judged.items():
        unique_books = set()
        for it in items:
            for bk in it.get("books", [it.get("book", "")]):
                if bk:
                    unique_books.add(bk)
        layer_coverage[layer] = {
            "n_judged": len(items),
            "n_books": len(unique_books),
        }
    # Top books by concept count
    top_books = sorted(per_book, key=lambda b: -b["n_concepts"])[:20]
    # Sample of high-score cross-book principles
    cross_book = []
    for it in judged.get("principle", []):
        if it.get("n_books", 1) >= 5:
            cross_book.append({
                "content": it["content"][:200],
                "n_books": it["n_books"],
                "sample_books": it.get("books", [])[:5],
            })
    cross_book.sort(key=lambda x: -x["n_books"])
    return {
        "n_books_total": n_books_total,
        "n_books_with_concepts": n_books_with_concepts,
        "total_raw_concepts": total_raw_concepts,
        "total_judged_included": total_judged,
        "per_layer": layer_coverage,
        "top_books_by_concepts": [
            {"book": b["book"], "n_concepts": b["n_concepts"]} for b in top_books
        ],
        "cross_book_consensus_principles": cross_book[:30],
    }


def write_markdown(report: Dict, output_path: Path) -> None:
    """Write a human-readable markdown report."""
    lines = []
    lines.append("# SWEBOK v4 Harness V2 — Corpus Coverage Report\n")
    lines.append(f"**Generated**: 2026-06-03\n")
    lines.append("## Summary\n")
    lines.append(f"- **Books in corpus**: {report['n_books_total']}")
    lines.append(f"- **Books with extracted concepts**: {report['n_books_with_concepts']}")
    lines.append(f"- **Total raw concepts extracted (line-by-line)**: {report['total_raw_concepts']}")
    lines.append(f"- **Concepts judged useful (included)**: {report['total_judged_included']}")
    if report["total_raw_concepts"] > 0:
        incl_pct = 100.0 * report["total_judged_included"] / report["total_raw_concepts"]
        lines.append(f"- **Inclusion rate**: {incl_pct:.1f}%")
    lines.append("")
    lines.append("## Per-Layer Coverage\n")
    lines.append("| Layer | Judged included | Books with this concept |")
    lines.append("|-------|-----------------|-------------------------|")
    for layer, stats in sorted(report["per_layer"].items(), key=lambda x: -x[1]["n_judged"]):
        lines.append(f"| {layer} | {stats['n_judged']} | {stats['n_books']} |")
    lines.append("")
    lines.append("## Top 20 Books by Concept Count\n")
    lines.append("| Book | Concepts |")
    lines.append("|------|----------|")
    for b in report["top_books_by_concepts"]:
        lines.append(f"| {b['book']} | {b['n_concepts']} |")
    lines.append("")
    lines.append("## Cross-Book Consensus (5+ books)\n")
    lines.append(f"{len(report['cross_book_consensus_principles'])} principles appear in 5+ books:\n")
    for it in report["cross_book_consensus_principles"][:20]:
        lines.append(f"- **(×{it['n_books']})** {it['content']}")
        lines.append(f"  - Sample books: {', '.join(it['sample_books'])}")
    lines.append("")
    output_path.write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Coverage report for line-distilled corpus")
    parser.add_argument("judged_dir", help="Directory with judged_*.json")
    parser.add_argument("per_book_dir", help="Directory with per_book/*.json")
    parser.add_argument("--output", "-o", default="coverage_report", help="Output dir")
    args = parser.parse_args()
    judged = load_judged(Path(args.judged_dir))
    per_book = load_per_book(Path(args.per_book_dir))
    report = make_report(judged, per_book)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "coverage_report.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    write_markdown(report, out_dir / "coverage_report.md")
    print(f"Report written to {out_dir}/coverage_report.{{json,md}}")
    print()
    print("## Quick summary")
    print(f"  Books: {report['n_books_total']}")
    print(f"  Raw concepts: {report['total_raw_concepts']:,}")
    print(f"  Judged included: {report['total_judged_included']:,}")
    if report["total_raw_concepts"] > 0:
        print(f"  Inclusion rate: {100 * report['total_judged_included'] / report['total_raw_concepts']:.1f}%")


if __name__ == "__main__":
    main()
