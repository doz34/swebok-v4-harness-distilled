# SWEBOK v4 Harness v1.5.3 — Adversarial Audit Report

**Generated**: 2026-06-03
**Method**: 5-hyperagent parallel audit (Architect, QA, DevOps, CISO, Anti-rec)
**Findings**: ~165 (deduplicated to 88 unique)
**Distribution**: 9 CRITICAL, 18 HIGH, 41 MED, 20 LOW

## Severity x Count

| Severity | Count | Examples |
|---|---|---|
| CRITICAL | 9 | HMAC fallback secret, .audit_key committed, install-harness.sh wrong paths |
| HIGH | 18 | Dead code (~4500 LOC), CI missing sklearn, .gitignore incomplete, retrieval/ opt-in code shipped as install path |
| MED | 41 | Tautological tests, arithmetic bugs, docstring lies, exceptions swallowed |
| LOW | 20 | Naming, code style, dead helper functions |

## Top 10 — must fix

1. **HMAC fallback secret hardcoded** (CISO #1) — `b"swebok-audit-fallback-secret-do-not-use-in-prod"` returned when key file write fails. Forgeable.
2. **install-harness.sh:32 references non-existent `scripts/lib/state_engine.py`** (Architect #1) — actual location is `lib/state_engine.py`. 5+ call sites.
3. **`.audit_key` committed to repo with mode 0600** (Architect #16) — single `git add .` exposes the HMAC secret.
4. **`.gitignore` is one line** (Architect #3+#4+#5, DevOps #29) — missing `__pycache__/`, `state.db`, `index.json`, `distilled_corpus*`, `.audit_key`.
5. **scripts/retrieval/ (~2306 LOC) marked EXPERIMENTAL_v2 yet ships in install path** (Anti-rec #1) — 10 files of code that no module consumes.
6. **CI doesn't install scikit-learn** (DevOps #3) — `theme_clusterer.py` imports sklearn but `requirements.txt` is empty and CI never installs it.
7. **4 dead distillers: judge.py, line_distiller.py, phrase_distiller.py, theme_clusterer.py** (Anti-rec #3-6) — 1049 LOC of one-shot pipeline scripts, never re-run after the corpus_enrichment.json was generated.
8. **CHANGELOG has v1.5.2 twice** (Anti-rec #29) — no v1.5.1 line; confusing.
9. **Tautological tests** (QA #15, #19, #20) — Test 12 determinism is weak; Test 3 BM25 only checks `len > 0`; Test 5 embedder only checks `v1 == v2` for same text.
10. **`scripts/corpus_browser.py` + `distilled_corpus/` (50 MB) + `distilled_corpus_v2/` (210 MB) all untracked but shipped** (Anti-rec #12) — CHANGELOG says "not wired into runtime" yet ship with repo.

## Fix plan (batched ≤3 findings per batch)

**Batch A — security (CRIT)**:
- A1. HMAC fallback: replace constant with hard fail (exit 5)
- A2. .audit_key: remove from git, add to .gitignore, regen on first install
- A3. .gitignore: comprehensive patterns

**Batch B — install path consistency (CRIT)**:
- B1. install-harness.sh: fix `scripts/lib/` → `lib/` (5 occurrences)
- B2. README.md / CLAUDE.md: same fix
- B3. pre-commit-hook.sh: same fix

**Batch C — dead code elimination (HIGH)**:
- C1. Delete scripts/retrieval/ (10 files, ~2306 LOC)
- C2. Delete scripts/{query,answer,judge,line_distiller,phrase_distiller,theme_clusterer,corpus_browser,swebok-query,logging_config,coverage_report}.py (~1900 LOC)
- C3. git rm --cached __pycache__/*, state.db, index.json, .audit_key; .gitignore them

**Batch D — CI hardening (HIGH)**:
- D1. Add scikit-learn to requirements.txt
- D2. Add `pip install -r requirements.txt` to CI before tests
- D3. Lint step: exit non-zero on failure, not `|| echo skip`

**Batch E — test quality (MED)**:
- E1. Test 12 determinism: add 5 diverse queries, run twice
- E2. Test 3 BM25: assert `score > 1.0` and content match
- E3. Test 5 embedder: assert different texts produce different vectors

**Batch F — docs consistency (LOW)**:
- F1. CHANGELOG: dedupe v1.5.2, add v1.5.1 entry
- F2. README: align test count badges
- F3. CLAUDE.md: align with current state

## Net LOC delta estimate

- Delete: ~4500 LOC (retrieval/ + dead distillers + dead CLIs)
- Modify: ~50 LOC (path fixes, gitignore, security hardening, test improvements)
- Add: ~30 LOC (CI requirement, test cases, docstring fixes)

**Net: -4400 LOC, project becomes 50% smaller and 100% cleaner.**

## Verifier

After all batches: `bash tests/distilled-test.sh` (target 35/35 PASS) and `bash tests/retrieval/test-v2.sh` (target 20/20 PASS).

## What we will NOT fix (out of scope for this pass)

- lib/state_engine.py internals (1610 LOC) — works, 19 silent `except Exception` are out-of-scope; future PR
- lib/bash_scanner.py regex hardening — works, 7+ false-positive edge cases; future PR
- 22 .pyc files already tracked — will be untracked but not retroactively removed from history; future PR
- Pre-existing v1 specs (architecture/, hooks-specs/, workflows/) — historical artifacts; keep
- Adversarial gate test fixtures in /tmp/ — dev-environment artifact; out of scope

## Approval

This plan was derived from 5-hyperagent parallel audit. Each finding has a citation to the specific file/line. Execution proceeds in the order A→F; if any batch fails, stop and report.
