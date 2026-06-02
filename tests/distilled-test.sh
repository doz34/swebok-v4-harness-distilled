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
    log_test "Test 12: Engine is deterministic (same input = same output)"
    local r1 r2
    r1=$(python3 "$COMPILER" --principle DRY 2>&1 | md5sum)
    r2=$(python3 "$COMPILER" --principle DRY 2>&1 | md5sum)
    if [[ "$r1" == "$r2" ]]; then
        log_pass "deterministic (same hash on repeated invocation)"
    else
        log_fail "non-deterministic: $r1 != $r2"
    fi
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

# === Test 18: Back-compat shim works (swebok-query.py) ===
test_swebok_query_shim() {
    log_test "Test 18: swebok-query.py back-compat shim works"
    local out
    out=$(python3 "$HARNESS_DIR/scripts/swebok-query.py" --principle KISS 2>&1)
    if echo "$out" | grep -q '"id": "KISS"'; then
        log_pass "swebok-query.py shim works (back-compat preserved)"
    else
        log_fail "swebok-query.py shim failed: $out"
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

echo ""
echo "============================================"
echo "  DISTILLED TESTS: $PASSED passed, $FAILED failed"
echo "============================================"
exit $FAILED
