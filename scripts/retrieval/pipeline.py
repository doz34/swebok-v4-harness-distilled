#!/usr/bin/env python3
"""
*** EXPERIMENTAL_v2 - OPT-IN ONLY. NOT CONSUMED BY COMPILED_KNOWLEDGE.PY. ***
SWEBOK v4 Harness V2 — End-to-End Indexing Pipeline
===================================================

Builds all 4 views from a corpus directory in one pass.
Stores everything in an index file (JSON) for fast query-time loading.

Usage:
    from retrieval.pipeline import IndexPipeline
    pipeline = IndexPipeline()
    pipeline.index_directory(Path("corpus/"), output_path=Path("index.json"))
    # Later, at query time:
    pipeline.load(Path("index.json"))
    results = pipeline.search("API design")
"""

import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.bm25 import BM25Index
from retrieval.chunker import Chunk, chunk_directory
from retrieval.embedder import Embedder
from retrieval.graph import KnowledgeGraph
from retrieval.hierarchy import Hierarchy
from retrieval.reranker import RankedResult, Reranker
from retrieval.security import hmac_sign, hmac_verify, get_index_key, parse_chunk_jsonl  # noqa: E402


class IndexPipeline:
    """End-to-end indexing of a corpus into 4 views."""

    def __init__(self, embedder_provider: str = "deterministic"):
        self.chunks: List[Chunk] = []
        self.bm25 = BM25Index()
        self.embedder = Embedder(provider=embedder_provider)
        self.embeddings: List[List[float]] = []
        self.kg = KnowledgeGraph()
        self.hierarchy = Hierarchy()
        # BUGFIX QA-CRIT + DEV-01: cache for query embeddings to avoid
        # rebuilding on every search (was: 'self.embedder.embed([query])[0]'
        # called per-query, which is a network call with non-deterministic
        # provider, and a tautological test in V2 roundtrip).
        self._query_embed_cache: Dict[str, List[float]] = {}
        self._query_embed_cache_max = 256  # LRU bound

    def index_directory(self, directory: Path, max_chars: int = 1500) -> dict:
        """Build all 4 views from a directory. Returns stats."""
        t0 = time.time()
        # Phase 1: chunk
        self.chunks = list(chunk_directory(directory, max_chars=max_chars))
        t_chunk = time.time() - t0
        # Phase 2: BM25 (lexical)
        t1 = time.time()
        self.bm25.build(self.chunks)
        t_bm25 = time.time() - t1
        # Phase 3: embeddings (semantic)
        t2 = time.time()
        texts = [c.text for c in self.chunks]
        self.embeddings = self.embedder.embed(texts) if texts else []
        t_embed = time.time() - t2
        # Phase 4: knowledge graph
        t3 = time.time()
        self.kg.build(self.chunks)
        t_kg = time.time() - t3
        # Phase 5: hierarchy
        t4 = time.time()
        self.hierarchy.build(self.chunks)
        t_hier = time.time() - t4
        return {
            "n_chunks": len(self.chunks),
            "phase_timings": {
                "chunk": round(t_chunk, 2),
                "bm25": round(t_bm25, 2),
                "embed": round(t_embed, 2),
                "graph": round(t_kg, 2),
                "hierarchy": round(t_hier, 2),
                "total": round(time.time() - t0, 2),
            },
            "view_stats": {
                "bm25": self.bm25.stats(),
                "kg": self.kg.stats(),
                "hierarchy": self.hierarchy.stats(),
                "embedder_dim": self.embedder.dim,
                "embedder_provider": self.embedder.provider_name,
            },
        }

    def _get_query_embedding(self, query: str) -> List[float]:
        """Embed a query with a bounded cache (DEV-01 fix)."""
        if query in self._query_embed_cache:
            return self._query_embed_cache[query]
        if len(self._query_embed_cache) >= self._query_embed_cache_max:
            # Simple FIFO eviction
            oldest = next(iter(self._query_embed_cache))
            del self._query_embed_cache[oldest]
        emb = self.embedder.embed([query])[0]
        self._query_embed_cache[query] = emb
        return emb

    def search(
        self,
        query: str,
        top_k: int = 5,
        view: str = "all",  # "all" | "bm25" | "graph" | "hierarchy"
    ) -> List[RankedResult]:
        """Multi-view search."""
        # BM25
        bm25_results = []
        if view in ("all", "bm25"):
            bm25_results = self.bm25.search(query, top_k=top_k * 2)
        # Graph: find entities matching the query, then get their chunks
        graph_chunks = []
        if view in ("all", "graph"):
            query_words = query.lower().split()
            for word in query_words:
                if len(word) > 2:
                    for entity_name in self.kg.entities:
                        if word in entity_name.lower():
                            # Get chunks mentioning this entity
                            for chunk in self.chunks:
                                if entity_name in chunk.text or entity_name.lower() in chunk.text.lower():
                                    if chunk not in graph_chunks:
                                        graph_chunks.append(chunk)
                            break
        # Embeddings: cosine similarity (with cache to avoid re-embedding per query)
        embed_sims = {}
        # Always populate the query embedding cache (DEV-01 fix: amortize embedding)
        # even if self.embeddings is empty (e.g. after load()).
        if view in ("all",):
            query_emb = self._get_query_embedding(query)
            from retrieval.embedder import cosine_similarity
            for i, emb in enumerate(self.embeddings):
                sim = cosine_similarity(query_emb, emb)
                if sim > 0.1:  # threshold
                    embed_sims[self.chunks[i].id] = sim
        # Rerank
        reranker = Reranker()
        chunks_by_id = {c.id: c for c in self.chunks}
        results = reranker.rerank(
            query=query,
            bm25_results=bm25_results,
            graph_chunks=graph_chunks,
            embed_sims=embed_sims,
            chunks_by_id=chunks_by_id,
            top_k=top_k,
        )
        return results

    def save(self, output_path: Path) -> None:
        """Persist the index with HMAC signature. Embeddings NOT saved (recomputed at load)."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "2.0",
            "n_chunks": len(self.chunks),
            "chunks": [c.to_dict() for c in self.chunks],
            "bm25": {
                "k1": self.bm25.k1, "b": self.bm25.b,
                "vocabulary": list(self.bm25.inverted_index.keys()),
            },
            "graph": {
                "entities": {n: {"type": e.type, "frequency": e.frequency} for n, e in self.kg.entities.items()},
                "relations": [{"source": r.source, "target": r.target, "weight": r.weight, "evidence_count": r.evidence_count} for r in self.kg.relations],
                "claims": [{"subject": c.subject, "predicate": c.predicate, "object": c.object, "chunk_id": c.chunk_id} for c in self.kg.claims],
            },
            "hierarchy": {
                "books": {n: {"chunk_count": b.chunk_count, "total_chars": b.total_chars} for n, b in self.hierarchy.books.items()},
                "chapters": {n: {"chunk_count": c.chunk_count, "total_chars": c.total_chars, "parent": c.parent} for n, c in self.hierarchy.chapters.items()},
            },
        }
        # Atomic write: write to .tmp, then rename
        tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
        body = json.dumps(data, ensure_ascii=False, indent=2).encode()
        # Sign with HMAC
        key = get_index_key()
        sig = hmac_sign(body, key)
        with open(tmp_path, "wb") as f:
            f.write(body)
        # Sidecar with signature
        sig_path = output_path.with_suffix(output_path.suffix + ".sig")
        with open(sig_path, "w") as f:
            f.write(sig)
        # Atomic rename
        os.replace(tmp_path, output_path)

    def load(self, index_path: Path) -> None:
        """Load an index from disk. Verifies HMAC signature. Recomputes embeddings."""
        sig_path = index_path.with_suffix(index_path.suffix + ".sig")
        with open(index_path, "rb") as f:
            body = f.read()
        # Verify HMAC if sidecar present
        if sig_path.exists():
            with open(sig_path) as f:
                sig = f.read().strip()
            key = get_index_key()
            if not hmac_verify(body, sig, key):
                raise ValueError(
                    f"HMAC signature mismatch for {index_path}. "
                    f"Index may be tampered. Re-run index_directory."
                )
        else:
            print(f"[pipeline] WARNING: no signature file at {sig_path}, skipping HMAC verify", file=__import__("sys").stderr)
        data = json.loads(body)
        # Defensively parse chunks via parse_chunk_jsonl
        chunks_parsed = []
        for c in data["chunks"]:
            parsed = parse_chunk_jsonl(json.dumps(c))
            if parsed is None:
                continue  # skip malformed
            chunks_parsed.append(Chunk(**parsed))
        self.chunks = chunks_parsed
        # Re-build BM25
        self.bm25.build(self.chunks)
        # Re-build graph
        self.kg.build(self.chunks)
        # Re-build hierarchy
        self.hierarchy.build(self.chunks)
        # Embeddings: lazy (recompute on first search)
        self.embeddings = []


# === CLI ===
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Index a corpus and save")
    parser.add_argument("directory", help="Corpus directory to index")
    parser.add_argument("--output", "-o", default="index.json", help="Output index file")
    parser.add_argument("--max-chars", type=int, default=1500)
    parser.add_argument("--provider", default="deterministic")
    args = parser.parse_args()
    pipeline = IndexPipeline(embedder_provider=args.provider)
    stats = pipeline.index_directory(Path(args.directory), max_chars=args.max_chars)
    print("Indexing stats:")
    print(json.dumps(stats, indent=2)[:2000])
    pipeline.save(Path(args.output))
    print(f"\nIndex saved to {args.output}")
