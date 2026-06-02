#!/usr/bin/env python3
"""
SWEBOK v4 Harness — Compiled Knowledge Query (v1.5.1+)
========================================================

This is a thin wrapper over compiled_knowledge.py. It exists for
backwards compatibility with the RAG-STRICT law in the dispatcher
(CLAUDE.md) which expects `swebok-query.py <query>`.

The new default: deterministic, compiled, no-LLM, no-embeddings.
For 872 books, this is faster, more accurate, and auditable.

Usage:
    python3 scripts/swebok-query.py "should I use SQL or NoSQL?"
    python3 scripts/swebok-query.py --principle KISS
    python3 scripts/swebok-query.py --checklist P5
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from compiled_knowledge import CompiledKnowledge, format_result  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Compiled Knowledge Query (back-compat shim)")
    parser.add_argument("query", nargs="?", help="Query string")
    parser.add_argument("--principle", help="Get principle by ID")
    parser.add_argument("--antipattern", help="Get antipattern by ID")
    parser.add_argument("--recipe", help="Get recipe by name")
    parser.add_argument("--decision-tree", help="Get decision tree by ID")
    parser.add_argument("--checklist", help="Get phase checklist (P1-P9)")
    parser.add_argument("--risks", action="store_true", help="Show risk catalog")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--max-sentences", type=int, default=3, help="(legacy) ignored")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    ck = CompiledKnowledge()
    if args.stats:
        import json
        print(json.dumps(ck.stats(), indent=2))
        return 0
    if args.principle:
        p = ck.get_principle(args.principle)
        if p:
            import json
            print(json.dumps(p, indent=2))
            return 0
        print(f"Principle not found: {args.principle}", file=sys.stderr)
        return 1
    if args.antipattern:
        a = ck.get_antipattern(args.antipattern)
        if a:
            import json
            print(json.dumps(a, indent=2))
            return 0
        print(f"Antipattern not found: {args.antipattern}", file=sys.stderr)
        return 1
    if args.recipe:
        r = ck.get_recipe(args.recipe)
        if r:
            print(r["content"])
            return 0
        print(f"Recipe not found: {args.recipe}", file=sys.stderr)
        return 1
    if args.decision_tree:
        t = ck.get_decision_tree(args.decision_tree)
        if t:
            import json
            print(json.dumps(t, indent=2))
            return 0
        print(f"Decision tree not found: {args.decision_tree}", file=sys.stderr)
        return 1
    if args.checklist:
        c = ck.get_phase_checklist(args.checklist)
        if c:
            print(c)
            return 0
        return 1
    if args.risks:
        print(ck.get_risks())
        return 0
    if args.query:
        results = ck.query(args.query, top_k=args.top_k)
        if not results:
            print(f"No results for: {args.query}")
            return 1
        for r in results:
            print(format_result(r))
            print()
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
