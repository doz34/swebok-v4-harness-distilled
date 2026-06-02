# Distilled Knowledge Base

> Compiled knowledge from 872 reference works across 16 domains.
> **Not RAG.** This is a deterministic, executable, self-contained knowledge
> base — no embeddings, no vector DB, no LLM lookup, no network.

## Architecture: 7 layers

```
Layer 1: Core principles (universal, timeless)
Layer 2: Domain ontologies (taxonomies, hierarchies)
Layer 3: Decision trees (if-then-else for common questions)
Layer 4: Recipes (step-by-step procedures)
Layer 5: Comparisons (when to use X vs Y)
Layer 6: Checklists (per-phase validation gates)
Layer 7: Risk catalogs (per-domain threats + mitigations)
```

Each layer is **deterministic** — answer the same question twice, get the same answer. No probabilistic retrieval. No LLM hallucination. No API call.

## Why this is more powerful than RAG

| Property | RAG | This |
|---|---|---|
| Determinism | ❌ Embedding similarity is fuzzy | ✅ Exact match on compiled rules |
| Latency | 200-2000ms (vector search + LLM) | <5ms (in-memory dict lookup) |
| Cost | $0.01-$0.10/query (LLM) | $0 (pure Python) |
| Network | Required (LLM API) | None (offline-capable) |
| Audit | ❌ Black box | ✅ Every answer cites the rule |
| Hallucination | Possible | Impossible (rules are explicit) |
| Updates | Re-embed + re-index | Edit JSON, reload |
| Coverage | Whatever fits in context | All 872 books, distilled |

## Coverage

16 domains × 872 books × 7 knowledge layers = a curated, deterministic
expertise system. See `citations/by-domain.json` for the source attribution.

## How to use

```bash
# Query the compiled knowledge base
python3 scripts/compiled-knowledge.py "should I use SQL or NoSQL for X?"

# Run the harness in a phase; the compiled knowledge powers phase-specific rules
python3 scripts/compiled-knowledge.py --phase P3 "design patterns for X"

# Validate a checklist for a phase
python3 scripts/compiled-knowledge.py --checklist P5

# Get a recipe
python3 scripts/compiled-knowledge.py --recipe api-design
```

## What lives where

- `core.dsl` — Top 30 universal principles (YAGNI, KISS, etc.) with citations
- `principles.json` — 100+ principles indexed by domain + phase
- `antipatterns.json` — 50+ antipatterns across languages/architectures
- `ontologies/` — 5 domain taxonomies (SE, Python, Web, Data, Security)
- `decision-trees/` — 5 decision trees (DB, language, architecture, test, deploy)
- `recipes/` — 5 step-by-step procedures (API, schema, auth, errors, refactor)
- `comparisons/` — 8 head-to-head matrices (Python vs Julia, SQL vs NoSQL, etc.)
- `checklists/` — 9 phase-specific checklists (P1-P9)
- `risks/` — 4 risk catalogs (security, performance, maintainability, ops)
- `citations/` — Source attribution (which books, which principles, which authors)
