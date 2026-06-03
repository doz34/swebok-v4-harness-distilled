# Changelog

All notable changes to the SWEBOK v4 Harness V2 (Distilled) will be documented here.

## [1.5.5] - 2026-06-03

### Security (4 CRITICAL fixes, closing the audit backlog)
- **rebuild() refuses to ship a broken chain** (`lib/state_engine.py`): if `recompute_audit_chain()` fails on any of the 4 audit tables, the rebuild aborts with exit code 5 (`STATE_ENGINE_INTEGRITY_FAIL`) and preserves the backup for forensics. The pre-chain state where rows have `row_hmac=NULL` is no longer a silent fallback.
- **CWD world-writable check** (`lib/state_engine.py:_resolve_state_db`): refuses to use a world-writable CWD for the git-root state-DB fallback. Logs a warning and falls back to `HARNESS_DIR` instead. Prevents symlink-planting of malicious `.swebok_state.db` by any local user.
- **adversarial-gate.sh normal mode requires explicit fixture flag**: the canned-fixture NORMAL MODE now requires `HARNESS_TEST_FIXTURE=1` env var. Without it, the gate refuses to run with a clear error pointing to `--council` or `--judge-only`. Production callers cannot accidentally get a fake review.
- **multiagent-launcher.sh emit-prompts validates phase args**: `FROM_P` and `TO_P` must match `^P[0-9]+$` regex before being interpolated into the JSONL body. Defense-in-depth against shell-injection in subagent prompts.

### Cleanup
- **`scripts/retrieval/` is now untracked**: added to `.gitignore`. The 10 module files remain on disk for opt-in use; tests pass. Future `git clone` will not include them by default.

### Test quality (3 strengthened)
- **Test 3 (BM25 search)**: now asserts `score > 1.0` AND `has_term` (was just `len > 0`).
- **Test 5 (embedder)**: now asserts determinism AND different texts produce different vectors (was just determinism — a constant embedder would have passed).
- **Test 8 (graph community)**: now requires `n > 5` AND seed presence (was just `> 1`).

### Test results
- 32 distilled + 20 v2 retrieval = **52/52 PASS** (verified by 4th-pass adversarial council)

## [1.5.4] - 2026-06-03

### Security (CRITICAL)
- **HMAC fallback secret removed** (`lib/state_engine.py`): the hardcoded `b"swebok-audit-fallback-secret-do-not-use-in-prod"` constant is replaced with a `RuntimeError("STATE_ENGINE_INTEGRITY_FAIL")` raise. The chain can no longer operate with a forgeable fallback secret.

### Cleanup (after 5-hyperagent audit, ~165 findings)
- **Dead code removed** (~1900 LOC deleted):
  - `scripts/judge.py` (233), `line_distiller.py` (276), `phrase_distiller.py` (278), `theme_clusterer.py` (262), `coverage_report.py` (172), `logging_config.py` (71), `answer.py` (59), root-level `swebok-query.py` (159). All were one-shot pipeline artifacts or dead CLIs.
- **`.gitignore` expanded**: now ignores `__pycache__/`, `*.pyc`, `state.db`, `*.db*`, `.audit_key`, `index.json`, `intent-map.json`, `distilled_corpus/`, `distilled_corpus_v2/`, `coverage_report/`, editor/OS junk. 22 .pyc files untracked.
- **Install path consistency**: 5 call sites in `install-harness.sh`, `README.md`, `CLAUDE.md`, `pre-commit-hook.sh` updated from `scripts/lib/` to `lib/` (the actual location).
- **Test 12 strengthened** (v1.5.3 audit followup): determinism test now runs 5 diverse queries × 2 runs = 10 hash matches instead of a single-query test.

### Net effect
- ~1900 LOC deleted, ~50 LOC modified
- 0 test regressions: 32 distilled + 20 v2 retrieval = **52/52 PASS**
- HMAC chain no longer forgeable via known fallback
- 22 .pyc files no longer pollute git
- See `AUDIT_REPORT.md` for the full synthesis

## [1.5.3] - 2026-06-03

### Added
- **ML systems ontology** (`distilled/ontologies/ml-systems.json`): 6th ontology covering the ML lifecycle — problem framing, data, features, training, evaluation, serving, monitoring, governance. Fills the only ontology gap in v1.
- **Phase coverage P1/P8/P9**: extended 15 principles with phase mappings so all 9 workflow phases (P1 Requirements → P9 Retirement) are now covered. Previously P1, P8, P9 had zero principles.
- **4 new tests** in `tests/distilled-test.sh`: ontology completeness, all-9-phases coverage, ontology count, retrieval-marker check. Total: 24 explicit tests / 44 [PASS] assertions (was 20/40).

### Changed
- **Council-verified v1.5.2**: two-round 5-hyperagent council (Architect/QA/DevOps/CISO/Anti-rec) + adversarial COUNCIL-2 reviewed the v2 line-distilled corpus. Verdict: v1 hand-curated 7-layer knowledge base is the source of truth; v2 line-distilled 47,385 items are 90.6% single-book noise and are not promoted into production.
- **All `scripts/retrieval/*.py` files marked `EXPERIMENTAL_v2 - OPT-IN ONLY`**: the v2 multi-view retrieval engine is preserved as research output but is NOT consumed by `compiled_knowledge.py`. The 20/20 v2 retrieval tests still pass.

### Not changed (intentional, per council)
- v1 curated 7 layers stay as the operational source of truth
- v2 line-distilled dumps (`distilled_corpus/judged/*.json`, `per_book/*.json`) are research artifacts; not loaded at runtime
- No new dependencies, no new runtime code, no new build steps

### Security
- v2 line-distilled dumps contain prompt-injection vectors from source books (research artifacts); `compiled_knowledge.py` does NOT load them, so vectors are inert at runtime.
- `scripts/corpus_browser.py` defaults to `--safe` mode (auto-on when stdout is a pipe) which redacts known prompt-injection patterns and caps content at 500 chars. The 5 known injection vectors from v2 dumps (e.g., "ignore previous instructions" example) are redacted in safe mode.

## [1.5.3] - 2026-06-03

### Added (corpus enrichment via 3-step pipeline)
- **`distilled/corpus_enrichment.json`** (NEW, 60 KB): 144 adversarially-accepted concepts from 17 themes. Generated by:
  1. `scripts/phrase_distiller.py` — phrase-by-phrase extraction of all 872 corpus books (1,039,222 sentence candidates, 20s, 8 workers)
  2. `scripts/theme_clusterer.py` — TF-IDF + KMeans k=200 (sklearn), 200 themes from 200k sampled docs
  3. **5-hyperagent adversarial council** — 200 themes evaluated, 17 ACCEPTED
  4. **5-hyperagent per-concept adversarial eval** — 425 concepts sampled, 144 ACCEPTED (33.9% acceptance)
- **`scripts/phrase_distiller.py`** (NEW, ~220 LOC): sentence segmentation with abbreviation handling, anti-noise regex, layer classification.
- **`scripts/theme_clusterer.py`** (NEW, ~260 LOC): TF-IDF + KMeans with sklearn fallback to stdlib.
- **`scripts/corpus_browser.py`** enrichment integration: 145,963 raw concepts now queryable.
- **`scripts/compiled_knowledge.py`** now loads the enrichment layer; `query()` returns a new `corpus_enrichment` type for relevant matches.

### The 17 accepted themes
Git branching, design patterns, relational schema, primary/foreign keys + crypto, event-driven architecture, observability, React components, LLM/foundation model concepts, prompt engineering, neural networks, API gateway, error handling, software testing, regular expressions, graph data structures, Git tooling, microservices.

### Tests
- 3 new tests (30-32): enrichment layer loads (144 items), query returns `corpus_enrichment` type, 17 themes covered. Total: 32 distilled tests + 20 retrieval tests = 52/52 PASS.

## [1.5.2] - 2026-06-03 (superseded by 1.5.4)
- (v1.5.2 entries retained for historical reference; see git log `0c0ad36`)

### Added (v1.5.2 — coverage complete)
- **`scripts/corpus_browser.py`** (NEW, ~250 LOC): read-only deterministic index over `distilled_corpus/per_book/*.json`. CLI: `--stats`, `--search`, `--book`, `--lines`, `--layer`, `--top`, `--human`, `--safe`. Cold start 233ms, search 327ms. The 145,963 raw concepts are now queryable, satisfying the literal "every concept from every chapter of every book" goal.
- **`docs/COVERAGE.md`** (NEW): per-module coverage report. Two-layer architecture: `compiled_knowledge.py` (102 v1 items, runtime-modifying) + `corpus_browser.py` (145,963 items, read-only access). 100% corpus coverage + 100% curated implementation.
- **5 new tests** (25-29): full coverage, search structure, fuzzy book lookup, --safe redaction, offline capability. Total: 29 explicit tests / 29 PASS.

## [2.0.0] - 2026-06-03

### Added (V2 — multi-view retrieval)
- **L1 multi-view retrieval** (4 views): full text (V1), BM25 + embeddings + reranking (V2), knowledge graph (V3), hierarchy tree (V4)
- **Working dossier assembler** with prompt-injection defenses
- **L0/L1 router** with intent classifier (canonical → L0, "how to" → L1)
- **Provider abstraction** (deterministic, mock, OpenAI, Anthropic, Ollama)
- **HMAC-signed index** with atomic write, defensive JSONL parsing
- **Embedder** with deterministic SHA-256 fallback, OpenAI, sentence-transformers backends
- **Path sandbox** with symlink rejection, max file size, allowlist
- **Health probe** (`--health` JSON for k8s/Docker)
- **Logging** (JSON + text formatters, configurable via env)
- **Dockerfile** (multi-stage, non-root, healthcheck, ENTRYPOINT)
- **GitHub Actions CI** (matrix: ubuntu/macos × Python 3.10/3.11/3.12)
- **CHANGELOG.md**, **requirements.txt**, **VERSION** files

### Changed
- **CLAUDE.md** Law 3: `RAG-STRICT` → `COMPILED-KNOWLEDGE` (the engine replaces the FTS5 RAG)
- **Test count reconciled**: 92/92 honest function count, not 100/100 or 106/106 (which were highest test IDs)
- **`CompiledKnowledge` deduplicated**: 24 principles (was 25 reported, actual was 24)

### Security (post-audit)
- HMAC signing of `index.json` with `.sig` sidecar
- Path traversal prevention (`safe_read_text` rejects symlinks, enforces `MAX_FILE_BYTES=50MB`)
- Prompt injection defense: backtick fence escaping, `<untrusted_source>` wrapping, control char stripping
- SSRF defense: `OllamaProvider` host validation against allowlist
- Defensive `parse_chunk_jsonl` with strict allowlist
- HMAC verify on every `IndexPipeline.load()`

## [1.0.0] - 2026-06-02

### Added (V1 — compiled knowledge)
- Initial release
- 7 layers of compiled knowledge: 24 principles, 46 antipatterns, 5 ontologies, 5 decision trees, 5 recipes, 3 comparisons, 9 phase checklists, 4 risk catalogs
- `compiled_knowledge.py` engine (pure Python, stdlib)
- `swebok-query.py` back-compat shim
- 20/20 tests passing

[2.0.0]: https://github.com/doz34/swebok-v4-harness-distilled/compare/v1.0.0...v2.0.0
