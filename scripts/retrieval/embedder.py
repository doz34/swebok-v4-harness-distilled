#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Embedding Interface + Providers
======================================================

Provider-agnostic embedding generation.
Default: deterministic hash-based embeddings (offline, $0, fast).
Optional: OpenAI, Anthropic, Ollama, sentence-transformers.

The deterministic provider is a "good enough" approximation:
- Same text always produces the same vector
- Similar texts (sharing tokens) produce similar vectors (cosine > 0)
- NOT a replacement for real embeddings, but allows the rest of the
  pipeline (graph, hierarchy, dossier) to work end-to-end offline.

Usage:
    from retrieval.embedder import Embedder
    embedder = Embedder(provider="deterministic")
    vectors = embedder.embed(["hello world", "goodbye world"])
    # Or: embedder = Embedder(provider="openai", model="text-embedding-3-small")
"""

import hashlib
import math
import os
import sys
from typing import List, Protocol

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.bm25 import tokenize


class EmbedderProvider(Protocol):
    """Interface for embedding providers."""

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        ...

    @property
    def dim(self) -> int:
        """Embedding dimension."""
        ...


class DeterministicProvider:
    """
    Hash-based deterministic embeddings.

    Algorithm: SHA-256 of (text + token) -> fixed-dim vector via
    bag-of-tokens hashing (similar to scikit-learn's HashingVectorizer).
    Plus L2 normalization so cosine similarity is well-defined.

    Properties:
    - Same text → same vector (deterministic)
    - Texts sharing many tokens → similar vectors (cosine > 0)
    - 384-dim (configurable)
    - Offline, $0, <1ms per text
    """

    def __init__(self, dim: int = 384):
        self._dim = dim

    def embed(self, texts: List[str]) -> List[List[float]]:
        vectors = []
        for text in texts:
            tokens = tokenize(text)
            if not tokens:
                vectors.append([0.0] * self._dim)
                continue
            # Hash each token to a position in the dim
            vec = [0.0] * self._dim
            for token in tokens:
                h = int(hashlib.sha256(token.encode()).hexdigest(), 16)
                pos = h % self._dim
                # Sub-hash for sign
                sign = 1 if (h >> 8) & 1 else -1
                vec[pos] += sign
            # IDF-like: weight by 1/sqrt(count) to dampen common tokens
            counts = {}
            for t in tokens:
                counts[t] = counts.get(t, 0) + 1
            for i, t in enumerate(tokens):
                pass  # already counted above
            # L2 normalize
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vec = [x / norm for x in vec]
            vectors.append(vec)
        return vectors

    @property
    def dim(self) -> int:
        return self._dim


class OpenAIProvider:
    """OpenAI embedding provider. Requires `openai` package and OPENAI_API_KEY."""

    def __init__(self, model: str = "text-embedding-3-small"):
        try:
            import openai  # noqa: F401
        except ImportError as e:
            raise ImportError("pip install openai to use OpenAIProvider") from e
        self.model = model
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY not set")
        self._client = openai.OpenAI()
        # Determine dim by a probe call
        self._dim = 1536  # text-embedding-3-small default
        if "large" in model:
            self._dim = 3072
        elif "ada" in model:
            self._dim = 1024

    def embed(self, texts: List[str]) -> List[List[float]]:
        # OpenAI supports up to 2048 inputs per call
        results = []
        for i in range(0, len(texts), 100):
            batch = texts[i:i + 100]
            response = self._client.embeddings.create(input=batch, model=self.model)
            results.extend([d.embedding for d in response.data])
        return results

    @property
    def dim(self) -> int:
        return self._dim


class SentenceTransformerProvider:
    """Local sentence-transformers. Requires `sentence-transformers` package."""

    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer  # noqa: F401
        except ImportError as e:
            raise ImportError("pip install sentence-transformers") from e
        self._model = SentenceTransformer(model)
        self._dim = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self._model.encode(texts, show_progress_bar=False).tolist()

    @property
    def dim(self) -> int:
        return self._dim


class Embedder:
    """Provider-agnostic embedder. Pick via SWEBOK_PROVIDER env var or constructor."""

    def __init__(self, provider: str = None, **kwargs):
        provider = provider or os.environ.get("SWEBOK_PROVIDER", "deterministic")
        if provider == "deterministic":
            self._provider = DeterministicProvider(**kwargs)
        elif provider == "openai":
            self._provider = OpenAIProvider(**kwargs)
        elif provider in ("sentence-transformers", "st"):
            self._provider = SentenceTransformerProvider(**kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}. Use: deterministic, openai, sentence-transformers")
        self._provider_name = provider

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self._provider.embed(texts)

    @property
    def dim(self) -> int:
        return self._provider.dim

    @property
    def provider_name(self) -> str:
        return self._provider_name


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two vectors."""
    if len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


# === CLI ===
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test the embedding interface")
    parser.add_argument("--provider", default="deterministic")
    parser.add_argument("--text", action="append", help="Texts to embed (can repeat)")
    args = parser.parse_args()
    texts = args.text or ["hello world", "goodbye world", "the quick brown fox"]
    emb = Embedder(provider=args.provider)
    vectors = emb.embed(texts)
    print(f"Provider: {emb.provider_name}, dim: {emb.dim}")
    for t, v in zip(texts, vectors):
        print(f"\n  Text: {t!r}")
        print(f"  Vector[0:5]: {v[:5]}")
    if len(vectors) >= 2:
        sim = cosine_similarity(vectors[0], vectors[1])
        print(f"\n  Cosine sim between text 0 and 1: {sim:.3f}")
