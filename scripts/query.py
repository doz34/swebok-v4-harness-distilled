#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Main Entry Point with L0/L1 Router
==========================================================

Combines:
- L0: V1 compiled knowledge (compiled_knowledge.py) — fast path, <5ms
- L1: V2 multi-view retrieval (4 views) — slow path, ~500ms

The router decides which to use per query.

Usage:
    python3 scripts/query.py "should I use SQL or NoSQL?"
    python3 scripts/query.py --l1 "API versioning best practices"
    python3 scripts/query.py --dossier "Compare TDD vs BDD"
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).parent.parent
DISTILLED_DIR = HARNESS_DIR / "distilled"

sys.path.insert(0, str(HARNESS_DIR / "scripts"))

from compiled_knowledge import CompiledKnowledge, format_result  # noqa: E402
from retrieval.pipeline import IndexPipeline  # noqa: E402


# Heuristic intent classifier (no LLM)
L0_PATTERNS = [
    "what is", "define", "principle", "principles", "kiss", "yagni", "dry", "solid",
    "antipattern", "anti-pattern", "checklist", "p1", "p2", "p3", "p4", "p5",
    "p6", "p7", "p8", "p9", "phase", "compare", "vs", "versus",
    "risk", "security risk", "performance risk",
]

L1_PATTERNS = [
    "where does", "in book", "which book", "page", "chapter",
    "combine", "connect", "across", "synthesize", "all books",
    "global view", "summary of", "summarize", "compare across", "holistic",
    "according to", "author says", "writes about",
]

INDEX_FILE = HARNESS_DIR / "index.json"


class Router:
    """Routes queries to L0 (compiled) or L1 (retrieval) or both."""

    def __init__(self):
        self.ck = CompiledKnowledge()
        self.l1 = None  # lazy-load

    def _load_l1(self):
        if self.l1 is None:
            self.l1 = IndexPipeline()
            if INDEX_FILE.exists():
                self.l1.load(INDEX_FILE)
            else:
                print(f"[router] No index found at {INDEX_FILE}, L1 disabled", file=sys.stderr)
                self.l1 = False
        return self.l1

    def classify(self, query: str) -> dict:
        """Classify query intent. Returns {'mode': 'l0'|'l1'|'hybrid', 'reasons': [...]}."""
        q = query.lower()
        reasons = []
        scores = {"l0": 0, "l1": 0}
        for p in L0_PATTERNS:
            if p in q:
                scores["l0"] += 1
                reasons.append(f"L0: matched '{p}'")
        for p in L1_PATTERNS:
            if p in q:
                scores["l1"] += 1
                reasons.append(f"L1: matched '{p}'")
        # If L0 has compiled match for the ID, prefer L0
        # Check if query contains a known principle/antipattern ID
        tokens = q.upper().replace("-", "_").split()
        for tok in tokens:
            if self.ck.principle_by_id.get(tok):
                scores["l0"] += 5
                reasons.append(f"L0: matched principle ID '{tok}'")
            if self.ck.antipattern_by_id.get(tok):
                scores["l0"] += 5
                reasons.append(f"L0: matched antipattern ID '{tok}'")
        # Decision
        # "How to" / "how do I" pattern → L1 (need examples from the corpus)
        q_lower = q
        how_pattern = ("how to" in q_lower or "how do" in q_lower or "how can" in q_lower or "how should" in q_lower)
        if how_pattern and scores["l1"] == 0:
            scores["l1"] += 2
            reasons.append("L1: 'how to/how do' pattern (needs examples from corpus)")
        if scores["l1"] > scores["l0"] and scores["l1"] >= 1:
            return {"mode": "l1", "reasons": reasons}
        elif scores["l0"] > 0 and scores["l1"] == 0:
            return {"mode": "l0", "reasons": reasons}
        elif scores["l0"] > 0 and scores["l1"] > 0:
            return {"mode": "hybrid", "reasons": reasons}
        return {"mode": "l0", "reasons": ["default to L0 (canonical patterns)"]}

    def query(self, q: str, mode: str = None, top_k: int = 5) -> dict:
        """Run the query, combining L0 and L1 as appropriate."""
        if mode is None:
            intent = self.classify(q)
            mode = intent["mode"]
            reasons = intent["reasons"]
        else:
            reasons = [f"forced mode: {mode}"]
        t0 = time.time()
        result = {"query": q, "mode": mode, "reasons": reasons, "l0": [], "l1": []}
        # L0 path (always run if available — fast)
        if mode in ("l0", "hybrid"):
            l0_results = self.ck.query(q, top_k=top_k)
            result["l0"] = l0_results
        # L1 path
        if mode in ("l1", "hybrid"):
            l1 = self._load_l1()
            if l1 and l1 is not False:
                l1_results = l1.search(q, top_k=top_k)
                result["l1"] = l1_results
        result["latency_ms"] = round((time.time() - t0) * 1000, 1)
        return result

    def dossier(self, q: str, top_k: int = 5) -> dict:
        """Build a working dossier combining L0 summary + L1 chunks + LLM prompt."""
        from retrieval.dossier import DossierAssembler
        result = self.query(q, mode="hybrid", top_k=top_k)
        assembler = DossierAssembler()
        l0_summary = ""
        if result["l0"]:
            parts = []
            for r in result["l0"][:5]:
                d = r["data"]
                text = d.get("synthesis") or d.get("snippet") or d.get("description") or ""
                parts.append(f"- {d.get('id', d.get('name', '?'))}: {text[:300]}")
            l0_summary = "\n".join(parts)
        return assembler.assemble(
            query=q,
            ranked_results=result["l1"],
            compiled_summary=l0_summary,
        )


def format_response(result: dict) -> str:
    """Format a router result for terminal display."""
    out = []
    out.append(f"Query: {result['query']}")
    out.append(f"Mode: {result['mode']} (latency: {result['latency_ms']}ms)")
    out.append(f"Reasons: {'; '.join(result['reasons'])}")
    if result.get("l0"):
        out.append(f"\n--- L0 (compiled, {len(result['l0'])} results) ---")
        for r in result["l0"][:3]:
            out.append(format_result(r))
    if result.get("l1"):
        out.append(f"\n--- L1 (retrieval, {len(result['l1'])} results) ---")
        for r in result["l1"][:3]:
            out.append(f"\n  Score: {r.score:.3f} | sources: {','.join(r.sources)}")
            out.append(f"  {r.chunk.context_header}")
            out.append(f"  Text: {r.chunk.text[:200]}{'...' if len(r.chunk.text) > 200 else ''}")
    if not result.get("l0") and not result.get("l1"):
        out.append("\n(no results)")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="V2 Router: L0 compiled + L1 retrieval")
    parser.add_argument("query", nargs="?", help="Query string")
    parser.add_argument("--l0", action="store_const", const="l0", dest="mode", help="Force L0 only")
    parser.add_argument("--l1", action="store_const", const="l1", dest="mode", help="Force L1 only")
    parser.add_argument("--hybrid", action="store_const", const="hybrid", dest="mode", help="Force hybrid")
    parser.add_argument("--dossier", action="store_true", help="Build a working dossier (for LLM prompt)")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--stats", action="store_true", help="Show router stats")
    parser.add_argument("--health", action="store_true", help="JSON health probe (for k8s/Docker)")
    args = parser.parse_args()
    if args.health:
        import json as _json
        from pathlib import Path as _P
        ck = CompiledKnowledge()
        idx_path = INDEX_FILE
        idx_exists = idx_path.exists()
        idx_chunks = 0
        if idx_exists:
            try:
                r = Router()
                r._load_l1()
                if r.l1 and r.l1 is not False:
                    idx_chunks = len(r.l1.chunks)
            except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError, ImportError, json.JSONDecodeError) as e:
                idx_exists = f"error: {e}"
        report = {
            "status": "ok" if (ck.principles and (idx_exists is True or idx_exists != "error")) else "degraded",
            "l0_principles": len(ck.principles),
            "l0_antipatterns": len(ck.antipatterns),
            "l0_decision_trees": len(ck.decision_trees),
            "l0_recipes": len(ck.recipes),
            "l1_index_present": idx_exists is True,
            "l1_index_path": str(idx_path),
            "l1_index_chunks": idx_chunks,
            "provider": os.environ.get("SWEBOK_PROVIDER", "deterministic"),
            "version": "2.0.0",
        }
        print(_json.dumps(report, indent=2))
        return 0 if report["status"] == "ok" else 1
    if args.stats:
        ck = CompiledKnowledge()
        print("L0 stats:", json.dumps(ck.stats(), indent=2))
        if INDEX_FILE.exists():
            print(f"\nL1 index: {INDEX_FILE} ({INDEX_FILE.stat().st_size // 1024} KB)")
        return 0
    if not args.query:
        parser.print_help()
        return 1
    router = Router()
    result = router.query(args.query, mode=args.mode, top_k=args.top_k)
    if args.dossier:
        # Build a working dossier
        router_obj = Router()
        dossier = router_obj.dossier(args.query, top_k=args.top_k)
        print(f"Dossier stats: {dossier.stats()}")
        print()
        print(dossier.to_prompt(max_tokens=4000))
    else:
        print(format_response(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
