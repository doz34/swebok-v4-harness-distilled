#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Concept Judge
====================================

For every concept extracted by line_distiller.py, score utility and decide
INCLUDE / EXCLUDE. The output is the "judged" distilled knowledge base
that augments or replaces V1's hand-curated content.

Scoring rubric (0-100, no LLM, all heuristics):

- SPECIFICITY (0-30): is there a concrete subject (noun phrase) or just
  a code-output statement? "X is a Y" scores high; "the output is..." low.

- ACTIONABILITY (0-30): is it prescriptive? "Always X", "Avoid X",
  "Never X" score high; "the code outputs" low.

- LENGTH (0-15): sweet spot 30-500 chars. Too short = noise; too long = prose.

- ARTIFACT FILTER (-100 to 0): reject if it contains "should output",
  "should return", "see figure", "see table", "the code", "the output",
  "page X" — these are book artifacts, not concepts.

- CROSS-BOOK (0-15): n_books it appears in. More = more consensus.

- SPECIFICITY_VS_GENERICITY (0-10): does it have proper capitalization
  of the subject? Does it have a verb? Or is it a fragment?

INCLUSION THRESHOLD: total >= 50 (out of 100).

Usage:
    python3 scripts/judge.py /tmp/line_distill_test --output distilled_judged/
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

HARNESS_DIR = Path(__file__).parent.parent


# === Artifact patterns (negative signal) ===

_ARTIFACT_PATTERNS = [
    re.compile(r"\b(?:should\s+output|should\s+return|will\s+output|will\s+return|the\s+output|the\s+return|returns?\s+the\s+following)\b", re.IGNORECASE),
    re.compile(r"\b(?:see\s+figure|see\s+table|see\s+chapter|see\s+page|see\s+appendix|see\s+listing)\b", re.IGNORECASE),
    re.compile(r"^(?:\d+\s+|[a-z]\s+|\s*$)"),  # starts with number, lowercase, or whitespace
    re.compile(r"^\s*the\s+code\b", re.IGNORECASE),
    re.compile(r"^(?:#+\s*)?(chapter|section|part)\s+\d+", re.IGNORECASE),
    re.compile(r"^[\s\W]*$"),  # only whitespace or punctuation
    re.compile(r"\b(?:TODO|FIXME|XXX|HACK)\b"),
    re.compile(r"^[\[\(\{].*[\]\)\}]\s*$"),  # only bracketed content
    re.compile(r"^[\-\=\*]{3,}\s*$"),  # separator lines
    re.compile(r"^>.*$", re.MULTILINE | re.DOTALL),  # blockquote lines
    re.compile(r"^```.*$", re.MULTILINE),  # code-fence lines
    re.compile(r"^!\[\]\(.*\)$"),  # image links
    re.compile(r"^\|.*\|$"),  # table rows
    re.compile(r"^\s*\d+\s*$"),  # lone numbers
    re.compile(r"^(?:table|figure)\s+\d+", re.IGNORECASE),
]


# === Quality scoring patterns ===

_PRINCIPLE_INDICATORS = [
    re.compile(r"\b(?:is|are|means?|denotes?|refers?\s+to)\b"),
    re.compile(r"\b(?:principle|rule|guideline|law|axiom)\b", re.IGNORECASE),
    re.compile(r"^(?:the\s+)?[A-Z]"),  # starts with capital (proper noun)
    re.compile(r"\b(?:should|must|always|never|avoid|don't|do\s+not)\b", re.IGNORECASE),
]

_ACTIONABILITY_INDICATORS = [
    re.compile(r"^(?:always|never|avoid|don't|do\s+not|ensure|make\s+sure|use|prefer|consider|enable|disable)", re.IGNORECASE),
    re.compile(r"\b(?:should|must|need\s+to|have\s+to|required\s+to|recommended|best\s+practice)\b", re.IGNORECASE),
    re.compile(r"^(?:if|when|after|before)\b.*\b(?:then|you\s+should|consider|try)\b", re.IGNORECASE),
]


def score_concept(item: Dict) -> Tuple[int, str]:
    """
    Score a single concept 0-100. Return (score, reason_for_score).
    INCLUDE if score >= 50.
    """
    content = item.get("content", "").strip()
    score = 0
    reasons = []

    # 1. Artifact filter (immediate reject)
    for pat in _ARTIFACT_PATTERNS:
        if pat.search(content):
            return (0, "artifact: matches " + pat.pattern[:30])

    # 2. Length sweet spot (0-15)
    if 30 <= len(content) <= 500:
        score += 15
        reasons.append("len")
    elif 10 <= len(content) < 30:
        score += 5
        reasons.append("short")
    elif len(content) > 500:
        score += 5
        reasons.append("long")
    # < 10 chars = 0

    # 3. SPECIFICITY (0-30): has a proper subject + verb + object
    if re.match(r"^[A-Z]", content):
        score += 10
        reasons.append("cap-start")
    if re.search(r"\b\w+ing\b|\b\w+ed\b|\b\w+s\b", content):  # has verbs
        score += 5
        reasons.append("verb")
    # Has both a capitalized noun phrase AND a verb-like pattern
    if re.search(r"\bis\b|\bare\b|\bmeans?\b|\bdenotes?\b", content, re.IGNORECASE):
        score += 10
        reasons.append("copula")
    # Has a defined term (X is a Y, X is defined as Y)
    if re.search(r"\bis\s+(?:a|an|the)\s+[a-z]", content, re.IGNORECASE):
        score += 5
        reasons.append("definitional")

    # 4. ACTIONABILITY (0-30): prescriptive
    for pat in _ACTIONABILITY_INDICATORS:
        if pat.search(content):
            score += 10
            reasons.append("action")
            break
    # Imperative form (verb at start, no subject)
    if re.match(r"^(?:Use|Avoid|Always|Never|Don't|Do\s+not|Make|Ensure|Consider|Prefer|Enable|Disable|Start|Stop|Keep|Add|Remove|Delete|Create|Update|Refactor|Rewrite|Test|Verify|Validate|Check)\b", content):
        score += 15
        reasons.append("imperative")
    # Anti-pattern signal
    if re.match(r"^(?:Don't|Do\s+not|Never|Avoid|Stop)", content, re.IGNORECASE):
        score += 5
        reasons.append("anti")

    # 5. CROSS-BOOK CONSENSUS (0-15)
    n_books = item.get("n_books", 1)
    if n_books >= 10:
        score += 15
        reasons.append("consensus-strong")
    elif n_books >= 5:
        score += 10
        reasons.append("consensus-med")
    elif n_books >= 2:
        score += 5
        reasons.append("consensus-low")
    # Single-book items still get a small bonus for being captured
    else:
        score += 1
        reasons.append("single-book")

    # 6. Source provenance
    if item.get("books"):
        score += 5
        reasons.append("cited")

    # 7. Layer-appropriate bonus
    layer = item.get("layer", "")
    if layer in ("principle", "antipattern"):
        score += 5  # principles/antipatterns are highest-value
    elif layer == "decision":
        score += 3
    # recipes and checklists get base score only

    return (min(score, 100), ",".join(reasons))


def judge_directory(input_dir: Path, output_dir: Path, threshold: int = 50) -> dict:
    """
    Judge all items in input_dir/distilled_*.json. Output to output_dir/.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    # Load all items
    all_items: List[Dict] = []
    for in_file in sorted(input_dir.glob("distilled_*.json")):
        with open(in_file) as f:
            data = json.load(f)
        layer = data.get("layer", in_file.stem.replace("distilled_", ""))
        for item in data.get("items", []):
            item["layer"] = layer
            all_items.append(item)
    # Judge
    included: Dict[str, List[Dict]] = defaultdict(list)
    excluded: List[Tuple[Dict, int, str]] = []
    for item in all_items:
        score, reason = score_concept(item)
        if score >= threshold:
            included[item["layer"]].append({**item, "_score": score, "_reason": reason})
        else:
            excluded.append((item, score, reason))
    # Sort included by score
    for layer in included:
        included[layer].sort(key=lambda x: -x["_score"])
    # Write
    for layer, items in included.items():
        out_file = output_dir / f"judged_{layer}.json"
        with open(out_file, "w") as f:
            json.dump({
                "layer": layer,
                "threshold": threshold,
                "n_judged": len(items),
                "items": items,
            }, f, indent=2, ensure_ascii=False)
    # Write excluded report
    with open(output_dir / "excluded.json", "w") as f:
        json.dump({
            "threshold": threshold,
            "n_excluded": len(excluded),
            "items": [{"content": it[0]["content"], "score": it[1], "reason": it[2]} for it in excluded[:200]],
        }, f, indent=2, ensure_ascii=False)
    return {
        "n_total": len(all_items),
        "n_included": sum(len(v) for v in included.values()),
        "n_excluded": len(excluded),
        "per_layer_included": {k: len(v) for k, v in included.items()},
        "threshold": threshold,
    }


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Judge distilled concepts by utility")
    parser.add_argument("input_dir", help="Directory with distilled_*.json files")
    parser.add_argument("--output", "-o", default="distilled_judged", help="Output dir")
    parser.add_argument("--threshold", type=int, default=50, help="Min score to include (0-100)")
    args = parser.parse_args()
    result = judge_directory(Path(args.input_dir), Path(args.output), threshold=args.threshold)
    print(json.dumps(result, indent=2))
