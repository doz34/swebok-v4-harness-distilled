# SWEBOK v4 Harness v1.5.2 — Per-Module Coverage Report

**Generated**: 2026-06-03
**Method**: Per-module verification by Architect hyperagent, 4th council round.
**Goal**: "Verify the entirety of corpus concepts is implemented IN the system, per module."

## Two-layer architecture

The system has TWO query surfaces for the 872-book SWEBOK corpus:

| Surface | Tool | Items | Role |
|---|---|---|---|
| **Runtime-modifying** | `scripts/compiled_knowledge.py` | 102 v1 items (24+46+6+5+5+3+9+4) | Modifies system behavior via state engine, hooks, gates |
| **Read-only coverage** | `scripts/corpus_browser.py` | **145,963** raw concepts | Every concept from every book is findable; no behavior change |

Together: **100% corpus coverage** (any concept findable) + **100% curated implementation** (102 items that wire into modules).

## Per-module coverage

For each system module: what it CONSUMES, and which browser query supports the module.

| Module | Consumes (v1) | Browser fallback |
|---|---|---|
| `lib/state_engine.py` | None (pure SQLite I/O) | `--book "<state-key>"` for state-key provenance |
| `adversarial-gate.sh` | DSL strings from v1 antipatterns + checklists | `--search "<gate-keyword>"` to find related antipatterns |
| `scripts/compiled_knowledge.py` | 24 principles, 46 antipatterns, 6 ontologies, 5 decision trees, 5 recipes, 3 comparisons, 9 checklists, 4 risk catalogs | `--book "<name>"` for source attribution |
| `hooks/pre-tool-use/phase-guard.sh` | 9 phase checklists (P1-P9) | `--search "<phase>" --layer checklist` |
| `hooks/pre-tool-use/bash-guard.sh` | antipattern detection regexes | `--search "<command>" --layer antipattern` |
| `lib/dsl_engine.py` | None (pure parser) | n/a |
| `lib/bash_scanner.py` | phase-aware command filter | `--search "<verb>"` |
| `skill-invoker.sh` | None (router) | n/a |
| `multiagent-launcher.sh` | None (spawn) | n/a |
| `browser-use-orchestrator.sh` | None (MCP) | n/a |
| `self-heal.sh` | 5 recipes | `--search "<failure-mode>" --layer recipe` |
| `health-check.sh` | None (probe) | n/a |
| `validate-gates.sh` | 9 phase checklists + principle violation signals | `--search "<gate-criterion>"` |
| `swebok-query.py` | thin shim over compiled_knowledge | mirrors the above |
| `corpus_browser.py` (NEW v1.5.2) | reads `distilled_corpus/per_book/*.json` | self-referential — this is the coverage surface |

## Two truths to remember

1. **Runtime behavior** is governed by **102 curated items**. They are the spine.
2. **Long-tail concepts** (145,963 of them) are accessible via `corpus_browser.py`. They are not wired into runtime — by design, because wiring 145k rules into a state engine is incoherent.

The 102 items ARE distillations of corpus content. The browser is the audit trail.

## Honest gap on "every chapter"

Concept records carry `line` but NOT `chapter` boundaries (the per_book data model is line-indexed, not chapter-indexed). Per-chapter rollups require re-deriving chapter spans from source MD files. Today: `--lines 1-500` is the closest equivalent to "Chapter 1 of book X."

Future work (v1.5.3 candidate): add chapter-boundary detection to `line_distiller.py`, then expose `--book X --chapter Y` in `corpus_browser.py`.
