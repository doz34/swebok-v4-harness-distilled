# V2 Architecture — Multi-view Retrieval with L0 Compiled Cache

> Inspired by Dorian CIET's critique of the V1 compiled-only approach.
> See email "Re: cognitif externe multi-couches" for the original.

## The shift from V1 → V2

**V1 (compiled-only)** has a fundamental coverage limit: the 7 layers in `distilled/` only contain what we pre-distilled. Novel questions about books we didn't deeply read get no answer. GraphRAG-style questions ("connect the dots across 5 books") are impossible because the LLM did the connecting at compile time, not query time.

**V2 (this architecture)** keeps the V1 compiled knowledge as a **fast L0 cache** but layers a **multi-view retrieval engine (L1)** on top, with a **router** that picks the right layer per query, and a **working dossier** that assembles context dynamically.

## 4 views of the same corpus (L1)

```
                              ┌──────────────────────────┐
                              │        CORPUS            │
                              │ (872 books, ~3.5M tokens) │
                              └────────────┬─────────────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
   ┌──────────────────┐      ┌──────────────────────┐      ┌────────────────────┐
   │  V1: TEXT VIEW   │      │  V2: CONTEXTUAL RETRIEVAL │  │  V3: KNOWLEDGE GRAPH│
   │  Faithful full   │      │  BM25 + embeddings +   │      │  Entities, relations,│
   │  text per chunk  │      │  contextual chunks +   │      │  claims, communities│
   │                  │      │  reranking             │      │                    │
   └────────┬─────────┘      └─────────┬────────────┘      └─────────┬──────────┘
            │                           │                             │
            └───────────────────────────┼─────────────────────────────┘
                                        │
                                        ▼
                          ┌──────────────────────────┐
                          │  V4: HIERARCHICAL        │
                          │  book > chapter > section│
                          │  > paragraph + summaries│
                          └──────────────┬───────────┘
                                         │
                                         ▼
                          ┌──────────────────────────┐
                          │   WORKING DOSSIER       │
                          │  (assembled per query)  │
                          └──────────────┬───────────┘
                                         │
                                         ▼
                            ┌────────────────────────┐
                            │   LLM ANSWER (optional)│
                            │ with citations         │
                            └────────────────────────┘
```

### V1: Faithful text view
- Every chunk = exact text from the source
- Source: `corpus/pdfs/*.md` (or user-provided corpus)
- Indexed by: file path, line range, char offset
- Use case: "show me what the book actually says, verbatim"

### V2: Contextual retrieval view (Anthropic-style)
- Each chunk gets a short LLM-generated context (1-2 sentences) at index time
- Indexed in TWO ways:
  - **BM25** (lexical, exact terms) — pure Python
  - **Embeddings** (semantic, similar meaning) — pluggable backend
- **Reranking** at query time: cross-encoder (or mock) re-scores top-k
- Solves: "destroyed context from naive chunking" (Microsoft critique)
- Use case: "find the chunk that talks about contract testing limits"

### V3: Knowledge graph (GraphRAG-style)
- Extracted at index time:
  - **Entities**: capitalized noun phrases, technical terms
  - **Relations**: co-occurrence + syntactic patterns
  - **Claims**: `subject predicate object` extractions
- Communities detected (Louvain or simple clustering)
- Per-community summary
- Use case: "connect TDD, BDD and snapshot testing across all books"

### V4: Hierarchical view
- Tree: book > chapter > section > paragraph
- Bottom-up summaries (one per level, LLM-generated)
- Top-down search: start from root, drill into relevant branches
- Use case: "give me a global view of testing strategies across the corpus"

### Working dossier (assembled per query)
- Composed of: top chunks from V2, entities/relations from V3, relevant branch from V4
- Size: 5k-20k tokens (fits in any LLM context)
- Generated WHEN the query is asked, not at index time
- Cites every source (file, chapter, page if available)

## L0 cache (V1 compiled knowledge, kept as fast path)

```
Query → L0 router → compiled knowledge match? → YES → return in <5ms
                                          ↓ NO
                                          → L1 multi-view → dossier → LLM answer
```

L0 is the **fast path** for:
- Canonical patterns (YAGNI, KISS, SOLID, ACID, etc.)
- Decision trees (DB choice, architecture choice)
- Phase checklists (P1-P9)
- Common antipatterns

L0 stays the SAME compiled knowledge from V1 (no rebuild needed).
L1 is NEW and ADDS retrieval on top.

## Query router (intent classifier)

The router decides **which view to query** based on intent:

| Query type | Mode | Views used |
|---|---|---|
| "What is YAGNI?" | L0 (compiled) | L0 only |
| "How do I design a REST API?" | L0+recipe | L0 + recipe + V1 text |
| "Where does book X discuss Y?" | L1 retrieval | V2 (BM25+embed) |
| "Compare A vs B across all books" | L1 graph | V3 (graph) + V2 (sources) |
| "Summarize testing strategies" | L1 hierarchy | V4 (top-down) + V2 (sources) |
| "Plan a migration strategy" | L1 dossier | All views → working dossier |
| "What does chapter Z of book W say?" | L1 retrieval | V2 + V4 (drill into tree) |

The classifier itself is **heuristic + keyword-based** (no LLM). For 90% of queries, the right mode is obvious from the question. For the 10% ambiguous, we try L0 first, fall through to L1.

## Provider abstraction (LLM-agnostic)

The system supports **multiple LLM providers** via a clean interface:

```python
class Provider(Protocol):
    def embed(self, texts: List[str]) -> List[List[float]]: ...
    def complete(self, prompt: str, max_tokens: int = 1024) -> str: ...
    def chat(self, messages: List[Dict], **kwargs) -> str: ...
```

Built-in providers:
- **`DeterministicProvider`** (default, offline): hash-based embeddings, no LLM. Returns canned answers from compiled knowledge.
- **`OpenAIProvider`**: gpt-4o, gpt-4o-mini embeddings
- **`AnthropicProvider`**: claude-sonnet, claude-haiku
- **`OllamaProvider`**: local models (mistral, llama3, etc.)
- **`MockProvider`**: returns deterministic placeholder for testing

The user picks via env var: `SWEBOK_PROVIDER=openai|anthropic|ollama|deterministic`

## Cost & performance envelope

| Mode | Latency | Cost | When used |
|---|---|---|---|
| L0 (compiled) | <5ms | $0 | 70% of queries (canonical patterns) |
| L1 + DeterministicProvider | <100ms | $0 | Offline mode |
| L1 + OpenAI (embed + chat) | 1-3s | $0.02-0.10 | Online with budget |
| L1 + Anthropic (embed + chat) | 1-3s | $0.03-0.15 | Online, complex queries |
| L1 + Local (Ollama) | 2-10s | $0 | Privacy-first |

## What's in this repo (V2)

```
distilled/                     # L0 — V1 compiled knowledge (UNCHANGED)
scripts/
  compiled_knowledge.py        # L0 engine (V1, unchanged)
  retrieval/                   # L1 — V2 NEW
    __init__.py
    chunker.py                 # V2a: contextual chunker
    bm25.py                    # V2b: BM25 index
    embedder.py                # V2c: embedding interface + providers
    graph.py                   # V2d: knowledge graph extractor
    hierarchy.py               # V2e: book/chapter tree
    reranker.py                # V2f: reranking interface
    dossier.py                 # V2g: working dossier assembler
    providers.py               # V2h: LLM provider abstraction
    pipeline.py                # V2i: end-to-end indexing pipeline
  query.py                     # V2j: router + main entry point
tests/
  retrieval/                   # V2 tests
    test_chunker.sh
    test_bm25.sh
    test_graph.sh
    test_hierarchy.sh
    test_router.sh
    test_e2e.sh
```

## What's deterministic vs LLM-required

| Component | Deterministic? | LLM required? | Default behavior |
|---|---|---|---|
| Chunker (V2a) | ✅ | No | Splits by headings/paragraphs |
| BM25 (V2b) | ✅ | No | Pure-Python |
| Embedder (V2c) | Mock | Yes (for real embeddings) | DeterministicProvider (hash-based) |
| Graph (V2d) | ✅ | No | Heuristic entity/relation extraction |
| Hierarchy (V2e) | ✅ | No | Markdown heading detection |
| Reranker (V2f) | Mock | Yes (for real reranking) | DeterministicProvider (score fusion) |
| Dossier (V2g) | ✅ | Optional | Assembles from L1 results |
| Answer (V2h) | Stub | Yes (for real answers) | Returns "see dossier for sources" |

**In the default `deterministic` mode, the whole system works offline with $0 cost.**
**In `openai` or `anthropic` mode, the LLM-required parts use real embeddings + real generation.**

## How V2 fixes V1's gaps

| V1 gap | V2 fix |
|---|---|
| Coverage limited to distilled content | V1 text view = full corpus, every chunk retrievable |
| "Connect the dots" impossible | V3 graph + working dossier |
| No page-level citation | V1 text view + chunk metadata (file, line, char) |
| Single view (compiled rules) | 4 views + router |
| No novel-question handling | L1 retrieval + LLM generation |
| Static synthesis | Dynamic retrieval per query |

## Honest disclosure

V2's **deterministic parts** (chunker, BM25, graph, hierarchy) are **fully built** and **work offline**.
V2's **LLM parts** (real embeddings, real reranking, real answer generation) are **interfaces** with mock implementations.
To use real LLMs, install the relevant provider SDK and set `SWEBOK_PROVIDER=openai` etc.

The repo is **corpus-agnostic**: point it at any directory of `.md` or `.txt` files and it builds the indices.
