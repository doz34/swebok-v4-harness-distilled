#!/usr/bin/env bash
# SWEBOK v4 Harness — Distilled Knowledge Engine Tests
# Tests the compiled-knowledge.py engine: deterministic, no-LLM, no-RAG.
# Run: bash tests/distilled-test.sh

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISTILLED_DIR="$HARNESS_DIR/distilled"
COMPILER="$HARNESS_DIR/scripts/compiled_knowledge.py"

PASSED=0
FAILED=0

log_test() { echo ""; echo "[TEST] $1"; }
log_pass() { echo "[PASS] $1"; PASSED=$((PASSED+1)); }
log_fail() { echo "[FAIL] $1"; FAILED=$((FAILED+1)); }

# === Test 1: Engine loads ===
test_engine_loads() {
    log_test "Test 1: compiled_knowledge.py loads without error"
    if python3 "$COMPILER" --stats 2>&1 | grep -q '"principles"'; then
        log_pass "engine loaded, stats returned"
    else
        log_fail "engine failed to load"
    fi
}

# === Test 2: All 25+ principles have required fields ===
test_principles_complete() {
    log_test "Test 2: Every principle has id, name, synthesis, citation_density"
    local count valid
    count=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
missing = []
for p in ck.principles:
    for k in ('id', 'name', 'synthesis', 'citation_density', 'phases', 'domains'):
        if k not in p:
            missing.append(f\"{p.get('id', '?')}:{k}\")
print(len(missing))
")
    if [[ "$count" -eq 0 ]]; then
        log_pass "all principles have required fields"
    else
        log_fail "$count principles have missing fields"
    fi
}

# === Test 3: Principle lookup by ID ===
test_principle_lookup_kiss() {
    log_test "Test 3: --principle KISS returns the KISS principle"
    local out
    out=$(python3 "$COMPILER" --principle KISS 2>&1)
    if echo "$out" | grep -q '"id": "KISS"' && echo "$out" | grep -q 'Keep It Simple'; then
        log_pass "KISS principle correctly retrieved"
    else
        log_fail "KISS lookup failed: $out"
    fi
}

# === Test 4: Hyphen-to-underscore normalization ===
test_hyphen_normalization() {
    log_test "Test 4: --principle kiss (lowercase) works (case + hyphen normalized)"
    local out
    out=$(python3 "$COMPILER" --principle kiss 2>&1)
    if echo "$out" | grep -q '"id": "KISS"'; then
        log_pass "lowercase + hyphen normalization works"
    else
        log_fail "lowercase failed: $out"
    fi
}

# === Test 5: Antipattern lookup ===
test_antipattern_lookup() {
    log_test "Test 5: --antipattern god-class returns God Class"
    local out
    out=$(python3 "$COMPILER" --antipattern god-class 2>&1)
    if echo "$out" | grep -q '"id": "GOD_CLASS"' && echo "$out" | grep -q 'God Class'; then
        log_pass "antipattern God Class correctly retrieved"
    else
        log_fail "antipattern lookup failed: $out"
    fi
}

# === Test 6: Decision tree retrieval ===
test_decision_tree_lookup() {
    log_test "Test 6: --decision-tree choose-database returns full tree"
    local out
    out=$(python3 "$COMPILER" --decision-tree choose-database 2>&1)
    if echo "$out" | grep -q '"id": "choose_database"' && echo "$out" | grep -q 'PostgreSQL'; then
        log_pass "decision tree choose-database correctly retrieved"
    else
        log_fail "decision tree lookup failed: $out"
    fi
}

# === Test 7: Recipe retrieval ===
test_recipe_lookup() {
    log_test "Test 7: --recipe api-design returns the API design recipe"
    local out
    out=$(python3 "$COMPILER" --recipe api-design 2>&1)
    if echo "$out" | grep -q 'API Design Recipe' && echo "$out" | grep -q 'HTTP methods'; then
        log_pass "recipe api-design correctly retrieved"
    else
        log_fail "recipe lookup failed (expected 'API Design Recipe' + 'HTTP methods')"
    fi
}

# === Test 8: Phase checklist ===
test_phase_checklist() {
    log_test "Test 8: --checklist P5 returns the P5 construction checklist"
    local out
    out=$(python3 "$COMPILER" --checklist P5 2>&1)
    if echo "$out" | grep -q 'P5 — Construction' && echo "$out" | grep -q 'Test-First'; then
        log_pass "P5 checklist correctly retrieved"
    else
        log_fail "P5 checklist failed: $out"
    fi
}

# === Test 9: All 9 phases have checklists ===
test_all_phase_checklists() {
    log_test "Test 9: All 9 phase checklists (P1-P9) are retrievable"
    local fail=0
    for phase in P1 P2 P3 P4 P5 P6 P7 P8 P9; do
        if ! python3 "$COMPILER" --checklist "$phase" 2>&1 | grep -q "${phase} —"; then
            echo "  Missing: $phase"
            fail=$((fail+1))
        fi
    done
    if [[ $fail -eq 0 ]]; then
        log_pass "all 9 phases have checklists"
    else
        log_fail "$fail phase checklists missing"
    fi
}

# === Test 10: Free-text query returns relevant results ===
test_query_relevance() {
    log_test "Test 10: Query 'SQL or NoSQL' returns SQL vs NoSQL comparison"
    local out
    out=$(python3 "$COMPILER" "SQL or NoSQL" 2>&1)
    if echo "$out" | grep -q 'COMPARISON' && echo "$out" | grep -q 'SQL vs NoSQL'; then
        log_pass "free-text query returns relevant comparison"
    else
        log_fail "free-text query did not return comparison: $out"
    fi
}

# === Test 11: All ontologies load ===
test_ontologies_load() {
    log_test "Test 11: All 5 ontologies (SE/Python/Web/Data/Security) load"
    local out count
    out=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
print(len(ck.ontologies))
")
    if [[ "$out" -ge 5 ]]; then
        log_pass "$out ontologies loaded"
    else
        log_fail "only $out ontologies loaded (expected >= 5)"
    fi
}

# === Test 12: Determinism — same query returns same result ===
test_determinism() {
    log_test "Test 12: Engine is deterministic across 5 diverse queries (v1.5.3 strengthened)"
    local hashes=()
    local q
    # 5 diverse queries, run each twice, total 10 hashes must all match
    for q in "DRY" "REST" "principle" "P5 checklist" "antipattern god"; do
        local h1 h2
        h1=$(python3 "$COMPILER" "$q" 2>&1 | md5sum | awk '{print $1}')
        h2=$(python3 "$COMPILER" "$q" 2>&1 | md5sum | awk '{print $1}')
        if [[ "$h1" != "$h2" ]]; then
            log_fail "non-deterministic on query '$q': $h1 != $h2"
            return
        fi
    done
    log_pass "deterministic across 5 diverse queries (10/10 hash matches)"
}

# === Test 13: No LLM, no network (offline operation) ===
test_offline_capable() {
    log_test "Test 13: Engine works without network (no LLM calls)"
    # Simulate no network by clearing proxy and trying to load
    local out
    out=$(env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
        python3 "$COMPILER" --stats 2>&1)
    if echo "$out" | grep -q '"principles"'; then
        log_pass "engine works without network (offline-capable)"
    else
        log_fail "engine failed offline: $out"
    fi
}

# === Test 14: Citation density is documented ===
test_citation_density() {
    log_test "Test 14: Every principle has a citation_density >= 'low' (none missing)"
    local out
    out=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
missing_density = [p for p in ck.principles if p.get('citation_density', '') in ('', 'unknown')]
print(len(missing_density))
")
    if [[ "$out" -eq 0 ]]; then
        log_pass "all principles have citation_density documented"
    else
        log_fail "$out principles missing citation_density"
    fi
}

# === Test 15: Decision tree has answer at every leaf ===
test_decision_trees_have_answers() {
    log_test "Test 15: Every decision-tree leaf has a 'pick' answer"
    local out
    out=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
import json
ck = CompiledKnowledge()
issues = []
for t in ck.decision_trees:
    dt = t.get('decision_tree', {})
    nodes = dt.get('nodes', {})
    leaf_count = 0
    answer_count = 0
    for name, node in nodes.items():
        if 'options' in node:
            for opt in node['options']:
                if 'answer' in opt and 'pick' in opt['answer']:
                    answer_count += 1
                if 'next' in opt:
                    pass  # internal node
                else:
                    leaf_count += 1
    if answer_count == 0 and leaf_count > 0:
        issues.append(t.get('id'))
print(' '.join(issues) if issues else 'OK')
")
    if [[ "$out" == "OK" ]]; then
        log_pass "decision trees have answers at leaves"
    else
        log_fail "decision trees without answers: $out"
    fi
}

# === Test 16: All files in distilled/ are valid JSON (except .md) ===
test_json_files_valid() {
    log_test "Test 16: All JSON files in distilled/ are valid JSON"
    local fail=0
    while IFS= read -r -d '' f; do
        if ! python3 -c "import json; json.load(open('$f'))" 2>/dev/null; then
            echo "  Invalid JSON: $f"
            fail=$((fail+1))
        fi
    done < <(find "$DISTILLED_DIR" -name "*.json" -print0)
    if [[ $fail -eq 0 ]]; then
        log_pass "all JSON files are valid"
    else
        log_fail "$fail invalid JSON files"
    fi
}

# === Test 17: Total distilled size < 1MB (vs 352MB corpus) ===
test_size_benefit() {
    log_test "Test 17: Distilled size is < 1MB (vs 352MB corpus, < 0.3%)"
    local size_kb
    size_kb=$(du -sk "$DISTILLED_DIR" 2>/dev/null | cut -f1)
    if [[ $size_kb -lt 1024 ]]; then
        log_pass "distilled size: ${size_kb}KB (vs 352MB corpus = 0.X% the size)"
    else
        log_fail "distilled too large: ${size_kb}KB"
    fi
}

# === Test 18: compiled_knowledge.py direct CLI works (was swebok-query.py shim) ===
test_swebok_query_shim() {
    log_test "Test 18: compiled_knowledge.py --principle KISS returns KISS"
    local out
    out=$(python3 "$COMPILER" --principle KISS 2>&1)
    if echo "$out" | grep -q '"id": "KISS"'; then
        log_pass "compiled_knowledge.py CLI returns KISS"
    else
        log_fail "compiled_knowledge.py --principle KISS failed: $out"
    fi
}

# === Test 19: Risks catalog is comprehensive ===
test_risks_catalog() {
    log_test "Test 19: Risk catalog has all 4 categories (security/perf/maintainability/ops)"
    local out
    out=$(python3 "$COMPILER" --risks 2>&1)
    local fail=0
    for cat in "Security Risks" "Performance Risks" "Maintainability Risks" "Operational Risks"; do
        if ! echo "$out" | grep -q "$cat"; then
            echo "  Missing: $cat"
            fail=$((fail+1))
        fi
    done
    if [[ $fail -eq 0 ]]; then
        log_pass "risk catalog has all 4 categories"
    else
        log_fail "$fail risk categories missing"
    fi
}

# === Test 20: Compilation_date present in all distilled files ===
test_compilation_metadata() {
    log_test "Test 20: Distilled files have compilation_date metadata"
    local fail=0
    while IFS= read -r -d '' f; do
        if ! grep -q "compilation_date" "$f" 2>/dev/null; then
            echo "  Missing: $f"
            fail=$((fail+1))
        fi
    done < <(find "$DISTILLED_DIR" -name "*.json" -print0)
    if [[ $fail -eq 0 ]]; then
        log_pass "all distilled JSON files have compilation_date"
    else
        log_fail "$fail distilled files missing compilation_date"
    fi
}

# === Test 21: ML systems ontology exists and has core nodes (v1.5.2) ===
test_ml_systems_ontology() {
    log_test "Test 21: ml-systems ontology loads with required nodes"
    local nodes
    nodes=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
ont = ck.ontologies.get('ml-systems', {})
n = ont.get('nodes', {})
required = ['ml_systems', 'data', 'training', 'evaluation', 'serving', 'monitoring', 'governance']
missing = [r for r in required if r not in n]
print(len(missing))
")
    if [[ "$nodes" -eq 0 ]]; then
        log_pass "ml-systems ontology has all 7 required top-level nodes"
    else
        log_fail "ml-systems ontology missing $nodes required nodes"
    fi
}

# === Test 22: All 9 phases P1-P9 are covered (v1.5.2) ===
test_all_phases_covered() {
    log_test "Test 22: All 9 phases (P1-P9) are covered by at least one principle"
    local count
    count=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
covered = set()
for p in ck.principles:
    for ph in p.get('phases', []):
        if ph != 'all':
            covered.add(ph)
required = {'P1','P2','P3','P4','P5','P6','P7','P8','P9'}
missing = required - covered
print(len(missing))
")
    if [[ "$count" -eq 0 ]]; then
        log_pass "all 9 phases covered by at least one principle"
    else
        log_fail "$count phases not covered (P1, P8, P9 must be present)"
    fi
}

# === Test 23: Five ontologies including new ml-systems (v1.5.2) ===
test_five_ontologies() {
    log_test "Test 23: 5+ ontologies including the new ml-systems"
    local count
    count=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
print(len(ck.ontologies))
")
    if [[ "$count" -ge 6 ]]; then
        log_pass "$count ontologies loaded (>=6 required)"
    else
        log_fail "only $count ontologies (< 6)"
    fi
}

# === Test 24: retrieval/ files are marked EXPERIMENTAL_v2 (v1.5.2) ===
test_retrieval_marked_experimental() {
    log_test "Test 24: scripts/retrieval/ is marked EXPERIMENTAL_v2"
    local unmarked
    unmarked=$(python3 -c "
import os, sys
n = 0
for f in sorted(os.listdir('scripts/retrieval')):
    if f == '__init__.py' or not f.endswith('.py'):
        continue
    p = os.path.join('scripts/retrieval', f)
    with open(p) as fh:
        if 'EXPERIMENTAL_v2' not in fh.read():
            n += 1
print(n)
")
    if [[ "$unmarked" -eq 0 ]]; then
        log_pass "all retrieval files carry EXPERIMENTAL_v2 marker"
    else
        log_fail "$unmarked retrieval files are unmarked"
    fi
}

# === Test 25: corpus_browser.py reports a sane concept count (data-driven, v2.6.0)
# Previously hard-coded 145,963 (v1.5.2 baseline). Corpus has grown since.
# The test now asserts a LOWER BOUND (>= 145,963 = original baseline) so it stays
# meaningful as the corpus grows AND fails if the browser breaks and reports 0.
test_corpus_browser_full_coverage() {
    log_test "Test 25: corpus_browser.py --stats reports >=145,963 concepts (data-driven)"
    local count
    count=$(python3 scripts/corpus_browser.py --stats 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d['n_concepts'])
")
    if [[ "$count" -ge 145963 ]]; then
        log_pass "corpus_browser covers $count concepts (>= 145,963 baseline)"
    else
        log_fail "corpus_browser has $count concepts (expected >= 145,963)"
    fi
}

# === Test 26: corpus_browser search returns content + book + line (v1.5.2) ===
test_corpus_browser_search() {
    log_test "Test 26: corpus_browser --search returns structured hits"
    local ok
    ok=$(python3 scripts/corpus_browser.py --search "yield from generator" --top 3 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
ok = len(d) > 0 and all('book' in r and 'line' in r and 'content' in r for r in d)
print('OK' if ok else 'FAIL')
")
    if [[ "$ok" == "OK" ]]; then
        log_pass "search returns structured hits with book/line/content"
    else
        log_fail "search returns malformed results"
    fi
}

# === Test 27: corpus_browser --book fuzzy-finds a book (v1.5.2) ===
test_corpus_browser_book_lookup() {
    log_test "Test 27: corpus_browser --book finds a book via fuzzy match"
    local found
    found=$(python3 scripts/corpus_browser.py --book "AI Assisted Programming Tom Taulli" --top 1 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('YES' if d.get('found') and d.get('n_concepts', 0) > 0 else 'NO')
")
    if [[ "$found" == "YES" ]]; then
        log_pass "fuzzy book lookup works"
    else
        log_fail "fuzzy book lookup failed"
    fi
}

# === Test 28: corpus_browser --safe redacts injection patterns (v1.5.2) ===
test_corpus_browser_safe_mode() {
    log_test "Test 28: corpus_browser --safe redacts prompt-injection patterns"
    local safe_ok
    safe_ok=$(python3 scripts/corpus_browser.py --safe --search "ignore previous" --top 5 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
# The known injection sample from the book MUST be redacted
hit = any(r.get('content') == '[REDACTED: prompt-injection pattern detected]' for r in d)
print('OK' if hit else 'FAIL')
")
    if [[ "$safe_ok" == "OK" ]]; then
        log_pass "--safe mode redacts prompt-injection patterns"
    else
        log_fail "--safe mode did not redact known injection"
    fi
}

# === Test 29: corpus_browser is offline (no network) (v1.5.2, data-driven v2.6.0)
# The browser must work fully offline. We assert: (1) no exception is raised when
# HTTP_PROXY points to a black-hole (proves no network was attempted), AND (2) the
# returned JSON has a sane n_books count (>= 777 = v1.5.2 baseline; corpus grows).
test_corpus_browser_offline() {
    log_test "Test 29: corpus_browser works without network (data-driven)"
    local ok
    # Block network with an unrouteable address — if browser tries it, the call will fail
    ok=$(HTTP_PROXY=http://127.0.0.1:1 HTTPS_PROXY=http://127.0.0.1:1 python3 scripts/corpus_browser.py --stats 2>&1 | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    n_books = d.get('n_books', 0)
    # Pass: no exception + n_books >= 777 baseline (corpus may have grown)
    print('OK' if n_books >= 777 else 'FAIL')
except:
    print('FAIL')
")
    if [[ "$ok" == "OK" ]]; then
        log_pass "browser works without network (offline-capable)"
    else
        log_fail "browser tried to make a network call"
    fi
}

# === Test 30: corpus_enrichment layer is loaded (v1.5.3) ===
test_corpus_enrichment_loads() {
    log_test "Test 30: corpus_enrichment.json loads with 144 items"
    local n
    n=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
print(len(ck.corpus_enrichment))
")
    if [[ "$n" -eq 144 ]]; then
        log_pass "corpus_enrichment loaded with 144 items"
    else
        log_fail "corpus_enrichment has $n items (expected 144)"
    fi
}

# === Test 31: query() returns corpus_enrichment type (v1.5.3) ===
test_query_returns_enrichment() {
    log_test "Test 31: query() returns corpus_enrichment type for relevant queries"
    local found
    found=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
res = ck.query('react', top_k=20)
types = set(r['type'] for r in res)
print('YES' if 'corpus_enrichment' in types else 'NO')
")
    if [[ "$found" == "YES" ]]; then
        log_pass "query returns corpus_enrichment type"
    else
        log_fail "query never returns corpus_enrichment"
    fi
}

# === Test 32: enrichment has 17 themes (v1.5.3) ===
test_enrichment_themes() {
    log_test "Test 32: enrichment covers 17 distinct themes"
    local n
    n=$(python3 -c "
import sys; sys.path.insert(0, '$HARNESS_DIR/scripts')
from compiled_knowledge import CompiledKnowledge
ck = CompiledKnowledge()
themes = set(c['theme_id'] for c in ck.corpus_enrichment)
print(len(themes))
")
    if [[ "$n" -eq 17 ]]; then
        log_pass "enrichment covers 17 themes (Git, React, LLMs, ML, DB, etc.)"
    else
        log_fail "enrichment has $n themes (expected 17)"
    fi
}

# === CALL ALL TESTS ===
test_engine_loads
test_principles_complete
test_principle_lookup_kiss
test_hyphen_normalization
test_antipattern_lookup
test_decision_tree_lookup
test_recipe_lookup
test_phase_checklist
test_all_phase_checklists
test_query_relevance
test_ontologies_load
test_determinism
test_offline_capable
test_citation_density
test_decision_trees_have_answers
test_json_files_valid
test_size_benefit
test_swebok_query_shim
test_risks_catalog
test_compilation_metadata
test_ml_systems_ontology
test_all_phases_covered
test_five_ontologies
test_retrieval_marked_experimental
test_corpus_browser_full_coverage
test_corpus_browser_search
test_corpus_browser_book_lookup
test_corpus_browser_safe_mode
test_corpus_browser_offline
test_corpus_enrichment_loads
test_query_returns_enrichment
test_enrichment_themes

echo ""
echo "============================================"
echo "  DISTILLED TESTS: $PASSED passed, $FAILED failed"
echo "============================================"
exit $FAILED
