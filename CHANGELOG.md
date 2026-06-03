# Changelog

All notable changes to the SWEBOK v4 Harness V2 (Distilled) will be documented here.

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
