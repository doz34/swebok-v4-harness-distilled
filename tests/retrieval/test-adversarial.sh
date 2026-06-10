#!/usr/bin/env bash
# SWEBOK v4 Harness V2 — Adversarial Test Suite
# Tests that the security fixes actually hold.
# Run: bash tests/retrieval/test-adversarial.sh
#
# Self-contained: each test inlines its Python fixture as a heredoc, so no
# external /tmp/test_adv*.py files are required. All tests return a single
# status word on stdout (REJECTED, SANITIZED, DETECTED, BLOCKED, CACHED, "7/7").

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

PASSED=0
FAILED=0
log_test() { echo ""; echo "[TEST] $1"; }
log_pass() { echo "[PASS] $1"; PASSED=$((PASSED+1)); }
log_fail() { echo "[FAIL] $1"; FAILED=$((FAILED+1)); }

# === ADV-1: Path traversal rejected ===
test_path_traversal() {
    log_test "ADV-1: chunk_file rejects paths outside allowed root (NEW-02 fix)"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
from pathlib import Path
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.chunker import chunk_file
# Try to chunk /etc/passwd with allowed_roots=distilled — should be REJECTED
try:
    chunks = list(chunk_file(
        Path('/etc/passwd'),
        allowed_roots={Path('/home/doz/swebok-v4-harness-distilled/distilled')}
    ))
    if len(chunks) == 0:
        print('REJECTED')
    else:
        print('NOT_REJECTED')
except (ValueError, PermissionError) as e:
    print('REJECTED')
PYEOF
)
    if [[ "$out" == "REJECTED" ]]; then
        log_pass "chunk_file rejects /etc/passwd (allowed_roots enforced)"
    else
        log_fail "chunk_file result: $out"
    fi
}

# === ADV-2: Prompt injection sanitized ===
test_prompt_injection() {
    log_test "ADV-2: sanitize_for_prompt neutralizes triple-backtick fences (prompt injection)"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.security import sanitize_for_prompt
# Triple backticks are the main prompt-injection vector (markdown code-fence escape)
TRIPLE = chr(96) * 3  # avoid bash interpretation
test_input = "harmless text " + TRIPLE + "\nrm -rf /\n" + TRIPLE + " more text"
sanitized = sanitize_for_prompt(test_input)
# Pass condition: triple backticks (3 consecutive raw) are not present
# Sanitizer inserts zero-width-space U+200B between backticks, breaking the fence
if TRIPLE not in sanitized:
    print('SANITIZED')
else:
    print('NOT_SANITIZED')
PYEOF
)
    if [[ "$out" == "SANITIZED" ]]; then
        log_pass "sanitize_for_prompt neutralizes triple-backtick fences"
    else
        log_fail "sanitizer output: $out"
    fi
}

# === ADV-3: HMAC tampering detected ===
test_hmac_tampering() {
    log_test "ADV-3: HMAC signature detects index tampering"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.security import hmac_sign, hmac_verify, get_index_key
# Sign some data
key = get_index_key()
data = b'test payload'
sig = hmac_sign(data, key)
# Tamper: change one byte
tampered = b'test PAYLOAD'
valid = hmac_verify(tampered, sig, key)
if valid:
    print('NOT_DETECTED')
else:
    print('DETECTED')
PYEOF
)
    if [[ "$out" == "DETECTED" ]]; then
        log_pass "HMAC detects tampering"
    else
        log_fail "HMAC result: $out"
    fi
}

# === ADV-4: Malicious JSONL rejected ===
test_malicious_jsonl() {
    log_test "ADV-4: parse_chunk_jsonl rejects malicious payloads"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.security import parse_chunk_jsonl
tests = [
    ('{"text": "valid", "file": "f.md"}', 'ACCEPT'),
    ('{"text": "x", "file": "f.md", "__init_subclass__": 1}', 'REJECT'),
    ('not json', 'REJECT'),
    ('{"text": 123, "file": "f.md"}', 'REJECT'),
    ('{}', 'REJECT'),
    ('{"text": ""}', 'REJECT'),
    ('{"text": "x", "file": "f.md", "file": "duplicate"}', 'ACCEPT'),
]
ok = 0
total = 0
for line, expected in tests:
    total += 1
    result = parse_chunk_jsonl(line)
    if (result is not None and expected == 'ACCEPT') or (result is None and expected == 'REJECT'):
        ok += 1
print(f'{ok}/{total}')
PYEOF
)
    if [[ "$out" == "7/7" ]]; then
        log_pass "parse_chunk_jsonl handles all 7 cases correctly"
    else
        log_fail "parse_chunk_jsonl: $out"
    fi
}

# === ADV-5: SSRF on Ollama blocked ===
test_ollama_ssrf() {
    log_test "ADV-5: OllamaProvider rejects SSRF (private IPs require opt-in)"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
import os
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.providers import OllamaProvider
# Default: private IPs blocked
os.environ.pop('SWEBOK_OLLAMA_ALLOW_PRIVATE', None)
try:
    p = OllamaProvider(host='http://169.254.169.254:80')
    print('NOT_BLOCKED')
except ValueError as e:
    if 'private' in str(e).lower() or 'allow_private' in str(e):
        print('BLOCKED')
    else:
        print(f'OTHER: {e}')
PYEOF
)
    if [[ "$out" == "BLOCKED" ]]; then
        log_pass "Ollama SSRF blocked (private IPs require opt-in)"
    else
        log_fail "Ollama SSRF: $out"
    fi
}

# === ADV-6: Symlink rejection ===
test_symlink_rejection() {
    log_test "ADV-6: chunk_file rejects symlinks (default)"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.chunker import chunk_file
tmpdir = Path(tempfile.mkdtemp())
try:
    real = tmpdir / 'real.md'
    real.write_text('# Real\n\nContent here.')
    link = tmpdir / 'link.md'
    link.symlink_to(real)
    # Default allow_symlinks=False should REJECT the symlink
    try:
        chunks = list(chunk_file(link))
        if len(chunks) == 0:
            print('REJECTED')
        else:
            print('NOT_REJECTED')
    except (ValueError, OSError):
        print('REJECTED')
finally:
    import shutil
    shutil.rmtree(tmpdir)
PYEOF
)
    if [[ "$out" == "REJECTED" ]]; then
        log_pass "chunk_file rejects symlinks by default"
    else
        log_fail "chunk_file: $out"
    fi
}

# === ADV-7: Resource limit (max file size) ===
test_max_file_size() {
    log_test "ADV-7: safe_read_text enforces max file size"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.security import safe_read_text
tmpdir = Path(tempfile.mkdtemp())
try:
    big = tmpdir / 'big.md'
    big.write_text('x' * (2 * 1024 * 1024))  # 2MB
    try:
        text = safe_read_text(big, max_bytes=1024)  # limit 1KB
        if len(text) <= 1024:
            print('REJECTED')
        else:
            print('NOT_REJECTED')
    except (ValueError, OSError):
        print('REJECTED')
finally:
    import shutil
    shutil.rmtree(tmpdir)
PYEOF
)
    if [[ "$out" == "REJECTED" ]]; then
        log_pass "safe_read_text rejects oversized files"
    else
        log_fail "safe_read_text: $out"
    fi
}

# === ADV-8: Embedding cache works (not a tautology) ===
test_embedding_cache_not_tautological() {
    log_test "ADV-8: Embedding cache returns SAME vector (not new embedding each call)"
    local out
    out=$(python3 <<'PYEOF' 2>&1 | tail -1
import sys
from pathlib import Path
import tempfile
sys.path.insert(0, '/home/doz/swebok-v4-harness-distilled/scripts')
from retrieval.pipeline import IndexPipeline

tmpdir = Path(tempfile.mkdtemp())
try:
    idx_path = tmpdir / 'idx.json'
    p = IndexPipeline()
    p.index_directory(Path('/home/doz/swebok-v4-harness-distilled/distilled/'), max_chars=1500)
    p.save(idx_path)
    p.load(idx_path)
    r1 = p.search('SOLID')
    cache_size_1 = len(p._query_embed_cache)
    r2 = p.search('SOLID')
    cache_size_2 = len(p._query_embed_cache)
    print(f'{cache_size_1} {cache_size_2} {r1[0].score == r2[0].score}')
finally:
    import shutil
    shutil.rmtree(tmpdir)
PYEOF
)
    read -r c1 c2 same <<< "$out"
    if [[ "$c1" -ge 1 && "$c2" -eq "$c1" && "$same" == "True" ]]; then
        log_pass "cache works (size=$c1 after 1st, $c2 after 2nd, scores match)"
    else
        log_fail "cache: $out"
    fi
}

# === CALL ALL ADVERSARIAL TESTS ===
test_path_traversal
test_prompt_injection
test_hmac_tampering
test_malicious_jsonl
test_ollama_ssrf
test_symlink_rejection
test_max_file_size
test_embedding_cache_not_tautological

echo ""
echo "============================================"
echo "  ADVERSARIAL TESTS: $PASSED passed, $FAILED failed"
echo "============================================"
exit $FAILED
