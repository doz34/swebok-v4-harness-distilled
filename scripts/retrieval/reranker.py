#!/usr/bin/env python3
"""
*** EXPERIMENTAL_v2 - OPT-IN ONLY. NOT CONSUMED BY COMPILED_KNOWLEDGE.PY. ***
SWEBOK v4 Harness V2 — Reranker
================================

Re-scores top-k retrieval results. Without a cross-encoder LLM,
we use a deterministic fusion of multiple signals:
- Original retrieval score
- Title/heading match bonus
- Entity overlap with query
- Position in source (earlier = more relevant? configurable)
- Recency (we don't have it, but reserved for future)

Pluggable: swap in a real cross-encoder for production.

Usage:
    from retrieval.reranker import Reranker
    reranker = Reranker()
    reranked = reranker.rerank(query, bm25_results, graph_results, embedder_sims)
"""

import os
import sys
from dataclasses import dataclass, field
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.bm25 import BM25Result
from retrieval.chunker import Chunk


@dataclass
class RankedResult:
    chunk: Chunk
    score: float
    sources: List[str] = field(default_factory=list)  # which views contributed
    matched_terms: List[str] = field(default_factory=list)


class Reranker:
    """Deterministic score fusion. No LLM required."""

    # Weights for each signal
    W_BM25 = 1.0
    W_GRAPH = 0.5
    W_EMBED = 0.7
    W_HEADING = 0.3
    W_POSITION = 0.05  # mild preference for earlier chunks in a book

    def rerank(
        self,
        query: str,
        bm25_results: List[BM25Result] = None,
        graph_chunks: List[Chunk] = None,
        embed_sims: dict = None,  # chunk_id -> similarity
        chunks_by_id: dict = None,  # chunk_id -> Chunk
        top_k: int = 10,
    ) -> List[RankedResult]:
        """Fuse multiple signals into final ranking."""
        bm25_results = bm25_results or []
        graph_chunks = graph_chunks or []
        embed_sims = embed_sims or {}
        chunks_by_id = chunks_by_id or {}

        scores: dict = {}  # chunk_id -> (score, sources, terms)
        for r in bm25_results:
            cid = r.chunk.id
            prev = scores.get(cid, (0.0, [], []))
            new_score = prev[0] + self.W_BM25 * r.score
            scores[cid] = (new_score, prev[1] + ["bm25"], list(set(prev[2] + r.matched_terms)))
        for chunk in graph_chunks:
            cid = chunk.id
            prev = scores.get(cid, (0.0, [], []))
            # Constant boost for graph presence (assume weight 1.0)
            new_score = prev[0] + self.W_GRAPH * 1.0
            scores[cid] = (new_score, prev[1] + ["graph"], prev[2])
        for cid, sim in embed_sims.items():
            prev = scores.get(cid, (0.0, [], []))
            new_score = prev[0] + self.W_EMBED * sim
            scores[cid] = (new_score, prev[1] + ["embed"], prev[2])
        # Heading bonus: if chunk's section matches query terms
        for cid, (score, sources, terms) in scores.items():
            chunk = chunks_by_id.get(cid)
            if not chunk:
                continue
            heading = " ".join(chunk.section_path).lower()
            q_lower = query.lower()
            if any(t in heading for t in q_lower.split() if len(t) > 2):
                scores[cid] = (score + self.W_HEADING, sources, terms)
        # Position bonus: earlier chunks in book mildly preferred
        for cid, (score, sources, terms) in scores.items():
            chunk = chunks_by_id.get(cid)
            if not chunk:
                continue
            # Inverse: earlier start_line = small position bonus
            pos_bonus = self.W_POSITION / (1 + chunk.start_line / 1000.0)
            scores[cid] = (score + pos_bonus, sources, terms)
        # Sort
        ranked = sorted(scores.items(), key=lambda x: -x[1][0])
        results = []
        for cid, (score, sources, terms) in ranked[:top_k]:
            chunk = chunks_by_id.get(cid)
            if chunk:
                results.append(RankedResult(
                    chunk=chunk, score=score, sources=sources, matched_terms=terms,
                ))
        return results


# === CLI ===
if __name__ == "__main__":
    import argparse
    import json
    from retrieval.bm25 import BM25Index
    parser = argparse.ArgumentParser(description="Test reranker with BM25 + graph")
    parser.add_argument("chunks_jsonl")
    parser.add_argument("query")
    args = parser.parse_args()
    chunks = []
    with open(args.chunks_jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(Chunk(**json.loads(line)))
    bm25 = BM25Index()
    bm25.build(chunks)
    bm25_res = bm25.search(args.query, top_k=20)
    reranker = Reranker()
    chunks_by_id = {c.id: c for c in chunks}
    results = reranker.rerank(args.query, bm25_results=bm25_res, chunks_by_id=chunks_by_id, top_k=5)
    print(f"Reranked for: {args.query}")
    for r in results:
        print(f"\n  Score: {r.score:.3f} | sources: {','.join(r.sources)} | matched: {','.join(r.matched_terms[:3])}")
        print(f"  {r.chunk.context_header}")
        print(f"  Text: {r.chunk.text[:200]}{'...' if len(r.chunk.text) > 200 else ''}")
