#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — BM25 Lexical Index
==========================================

Pure-Python BM25 (Best Matching 25) implementation.
No external deps. Indexes chunks from chunker.py for lexical retrieval.

BM25 formula:
    score(q, d) = Σ_{t in q} IDF(t) * (f(t,d) * (k1 + 1)) / (f(t,d) + k1 * (1 - b + b * |d|/avgdl))

where:
    IDF(t) = log((N - n(t) + 0.5) / (n(t) + 0.5) + 1)
    f(t,d) = frequency of term t in document d
    |d| = length of document d
    avgdl = average document length
    k1 = 1.5 (term saturation)
    b = 0.75 (length normalization)

Usage:
    from retrieval.bm25 import BM25Index
    index = BM25Index()
    index.build(chunks)
    results = index.search("contract testing", top_k=5)
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import List

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.chunker import Chunk
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# BM25 hyperparameters (standard Okapi defaults)
K1 = 1.5
B = 0.75

_TOKEN_RE = re.compile(r"\b\w+\b", re.UNICODE)

# Common stopwords (English, French, German — the corpus is multilingual)
_STOPWORDS = set("""
a an the of and or but if then else for on in at to from by with as is are was were be been being
have has had do does did this that these those it its their there here what when where why how
i you he she we they me him her us them my your his our their
""".split())


def tokenize(text: str) -> List[str]:
    """Lowercase, split on word boundaries, drop short tokens and stopwords."""
    tokens = _TOKEN_RE.findall(text.lower())
    return [t for t in tokens if len(t) > 1 and t not in _STOPWORDS]


@dataclass
class BM25Result:
    chunk: Chunk
    score: float
    matched_terms: List[str]


class BM25Index:
    """Pure-Python BM25 index over chunks."""

    def __init__(self, k1: float = K1, b: float = B):
        self.k1 = k1
        self.b = b
        self.chunks: List[Chunk] = []
        self.doc_freqs: List[Counter] = []  # term -> count per doc
        self.doc_lens: List[int] = []
        self.avgdl: float = 0.0
        self.n_docs: int = 0
        # Inverted index: term -> set of doc indices
        self.inverted_index: dict = {}
        # IDF cache
        self.idf_cache: dict = {}

    def build(self, chunks: List[Chunk]) -> None:
        """Build the index from a list of chunks."""
        self.chunks = list(chunks)
        self.n_docs = len(self.chunks)
        self.doc_lens = []
        self.doc_freqs = []
        self.inverted_index = {}
        for i, chunk in enumerate(self.chunks):
            tokens = tokenize(chunk.text)
            self.doc_lens.append(len(tokens))
            tf = Counter(tokens)
            self.doc_freqs.append(tf)
            for term in tf:
                self.inverted_index.setdefault(term, set()).add(i)
        self.avgdl = sum(self.doc_lens) / max(1, self.n_docs)
        # Pre-compute IDF
        self.idf_cache = {}
        for term in self.inverted_index:
            n_t = len(self.inverted_index[term])
            self.idf_cache[term] = math.log((self.n_docs - n_t + 0.5) / (n_t + 0.5) + 1)

    def _idf(self, term: str) -> float:
        if term in self.idf_cache:
            return self.idf_cache[term]
        return 0.0

    def _score_chunk(self, query_tokens: List[str], doc_idx: int) -> tuple:
        """BM25 score for a single document."""
        tf = self.doc_freqs[doc_idx]
        doc_len = self.doc_lens[doc_idx]
        score = 0.0
        matched = []
        for term in query_tokens:
            if term not in tf:
                continue
            f = tf[term]
            idf = self._idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * doc_len / max(1, self.avgdl))
            score += idf * (numerator / denominator)
            matched.append(term)
        return score, matched

    def search(self, query: str, top_k: int = 10) -> List[BM25Result]:
        """Return top-k chunks by BM25 score."""
        if self.n_docs == 0:
            return []
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        # Get candidate docs (union of postings)
        candidates = set()
        for term in query_tokens:
            if term in self.inverted_index:
                candidates.update(self.inverted_index[term])
        # Score candidates
        scored = []
        for doc_idx in candidates:
            score, matched = self._score_chunk(query_tokens, doc_idx)
            if score > 0:
                scored.append((score, matched, doc_idx))
        scored.sort(key=lambda x: -x[0])
        results = []
        for score, matched, doc_idx in scored[:top_k]:
            results.append(BM25Result(
                chunk=self.chunks[doc_idx],
                score=score,
                matched_terms=matched,
            ))
        return results

    def stats(self) -> dict:
        return {
            "n_docs": self.n_docs,
            "avgdl": self.avgdl,
            "vocabulary_size": len(self.inverted_index),
            "total_tokens": sum(self.doc_lens),
        }


# === CLI ===
if __name__ == "__main__":
    import sys
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Build and query a BM25 index over a JSONL chunks file")
    parser.add_argument("chunks_jsonl", help="JSONL chunks file (from chunker.py)")
    parser.add_argument("query", nargs="?", help="Query string (if not given, just print stats)")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()
    chunks = []
    with open(args.chunks_jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(Chunk(**json.loads(line)))
    index = BM25Index()
    index.build(chunks)
    print(f"Index: {index.stats()}")
    if args.query:
        print(f"\nQuery: {args.query}")
        for r in index.search(args.query, top_k=args.top_k):
            print(f"\n  Score: {r.score:.3f} | matched: {', '.join(r.matched_terms[:5])}")
            print(f"  {r.chunk.context_header}")
            print(f"  Text: {r.chunk.text[:200]}{'...' if len(r.chunk.text) > 200 else ''}")
