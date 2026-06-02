# Evidence Ledger — SWEBOK v4 Harness

> Durable index of audit findings, fixes, and verification commands. Append-only.

**Status**: seed populated from the 2026-06-01 / 06-02 D→S journey. Future audits **append**; never overwrite.

---

## Schema

Each row links one audit finding to its fix and to a re-runnable verification command. Columns:

- **Date**: when the finding was raised
- **ID**: stable identifier (CRIT-N / HIGH-N / MED-N / LOW-N — never reused)
- **Source**: which audit / council role surfaced it
- **Finding (1-line)**: the claim
- **Evidence cmd**: a command that reproduces the finding on the broken code
- **Fix commit**: short SHA of the commit that resolves it
- **Verification cmd**: a command that confirms the fix
- **Status**: OPEN / FIXED / DEFERRED / WONT_FIX (with reason)

---

## Audit findings — 2026-06-01 to 2026-06-02 (D→S trajectory)

| Date | ID | Source | Finding (1-line) | Evidence cmd | Fix commit | Verification cmd | Status |
|---|---|---|---|---|---|---|---|
| 2026-06-01 | CRIT-1 | independent council (CISO) | Circuit breaker fail-OPEN: 3 blocks → `exit 0` (5-min override window) | `grep -n 'activate_override' hooks/pre-tool-use/phase-guard.sh` (before) | initial release `97b5457` | `grep -n 'exit 1' hooks/pre-tool-use/phase-guard.sh:325` | FIXED |
| 2026-06-01 | CRIT-2 | independent council (Architect) | `adversarial-gate.sh` is a hardcoded RED/BLUE fixture per phase | `bash scripts/adversarial-gate.sh P5 P6` (returns canned strings) | initial release + honesty banner; full close-out in v1.5.0 (commit 94394a3, ADR-003) | `head -25 scripts/adversarial-gate.sh \| grep HONESTY` and `bash scripts/adversarial-gate.sh --council P5 P6; echo $?` (= 99) | CLOSED (v1.5.0, opt-in council bridge) |
| 2026-06-01 | CRIT-3 | independent council (Architect) | Append-only audit log "enforced by honesty" — same module DROPs the trigger | `grep -n DROP TRIGGER scripts/lib/state_engine.py` | `97b5457` + HMAC chain in ITER5 | `python3 scripts/lib/state_engine.py verify_audit_chain` (tamper detected with exit 1) | FIXED (HMAC chain, detection-only — see SECURITY.md item 5) |
| 2026-06-01 | CRIT-4 | own stress test | `auto-verify.sh` crashed on every PostToolUse (`$2` unbound) | `echo '{}' \| bash hooks/post-tool-use/auto-verify.sh; echo $?` (was 1) | `97b5457` | `echo '{}' \| bash hooks/post-tool-use/auto-verify.sh; echo $?` (now 0) | FIXED |
| 2026-06-01 | CRIT-5 | independent council (CISO) | `rm -rf /` and other destructive commands not blocked outside P5/P7/P8 | `python3 -c "import sys; sys.path.insert(0,'scripts/lib'); from bash_scanner import scan_command; print(scan_command('P3', 'rm -rf /'))"` (was NONE) | `97b5457` | Same cmd (now `BLOCKED:DESTRUCTIVE`) | FIXED |
| 2026-06-01 | CRIT-6 | own stress test | SQLite DB observed in `database disk image is malformed` state during 1000-way concurrency | `bash tests/adversarial-test.sh` (race) | atomic UPSERT in ITER4, `97b5457` | `time seq 1 1000 \| xargs -P10 -I{} python3 scripts/lib/state_engine.py increment_nested phase_data P6 ctr_test; python3 scripts/lib/state_engine.py get phase_data.P6.ctr_test` (must be 1000) | FIXED |
| 2026-06-01 | CRIT-7 | independent council (CISO) | Skill/Task/Agent payloads silently allowed (empty file_path + command) | `echo '{"tool_name":"Skill","tool_input":{"skill":"x"}}' \| bash hooks/pre-tool-use/phase-guard.sh` | `97b5457` | Same cmd; emit INFO log_event | FIXED (audit-visible) |
| 2026-06-01 | CRIT-8 | own stress test | bash-guard false positives on `echo "src"`, `ls /usr/src`, `man rsrc` | `echo '{"tool_name":"Bash","tool_input":{"command":"echo src"}}' \| bash hooks/pre-tool-use/bash-guard.sh` | NOT_FIXED — known limitation (string scanner, not parser) | n/a | DEFERRED (documented in SECURITY.md "out of scope" §2) |
| 2026-06-01 | HIGH-9 | own | Phase rules duplicated in `bash_scanner.py` + `phase-guard.sh`, drifted | `diff <(grep -E "P[0-9]" hooks/pre-tool-use/phase-guard.sh) <(grep PHASE_RULES scripts/lib/bash_scanner.py)` | NOT_FIXED — documented architectural debt | n/a | DEFERRED (ADR-002 candidate for future refactor) |
| 2026-06-01 | HIGH-10 | independent council (DevOps) | `install-harness.sh` destructively overwrites `~/.claude/settings.json` | `bash install-harness.sh` (before) wiped user env | `97b5457` jq-merge rewrite | `bash install-harness.sh --help` prompts for consent + backup | FIXED |
| 2026-06-01 | F-TEST-001 | independent council (QA) | Test 68 "decorative_md_inventoried" always passes (no assertion) | `grep -A5 'test_decorative_md' tests/adversarial-test.sh` | `97b5457` | Test 68 now asserts count ≤ 200 (real assertion) | FIXED |
| 2026-06-01 | F-TEST-002 | independent council (QA) | Test 5c tautological — `run_or_true` + unconditional `log_pass` | `grep -B2 -A8 'Test 5c' tests/adversarial-test.sh` | `97b5457` | Test 5c now asserts journal_mode=wal + cross-conn read | FIXED |
| 2026-06-01 | F-TEST-003 | independent council (QA) | Dead test calls after `exit 0` (lines 2134-2138) | `awk 'NR>=2125 && NR<=2138' tests/adversarial-test.sh` | `97b5457` | Lines deleted; test file ends at `exit 1; fi` | FIXED |
| 2026-06-01 | F-TEST-005 | independent council (QA) | 13 tests use only `!= NONE` weak assertion (catches scanner returning garbage) | `grep -c '!= "NONE"' tests/adversarial-test.sh` (was 13) | `97b5457` | `grep -c '=~ ^BLOCKED:' tests/adversarial-test.sh` (now used) | FIXED |
| 2026-06-01 | MISSING-04 | independent council (CISO) | No HMAC chain on audit rows — just append-only by trigger | `sqlite3 .swebok_state.db "SELECT * FROM adversarial_log LIMIT 1"` (no row_hmac column) | ITER5 / `97b5457` | `python3 scripts/lib/state_engine.py verify_audit_chain` returns ok | FIXED |
| 2026-06-02 | CI-1 | GitHub Actions matrix | bash 3.2 `${TOOL_NAME,,}` syntax fails on macOS | CI run 26789848961 logs | `b56d6ba` | `bash --version` on macOS + run tests | FIXED |
| 2026-06-02 | CI-2 | GitHub Actions matrix | `timeout` command absent on macOS — Tests 66, 91 fail | CI run 26789848961 logs | `b56d6ba` | Tests skip cleanly when `command -v timeout` empty | FIXED |
| 2026-06-02 | CI-3 | GitHub Actions matrix | `/proc/mounts` absent on macOS — Test 65 fails | CI run 26789848961 logs | `b56d6ba` | Test 65 skips when `/proc/mounts` unreadable | FIXED |
| 2026-06-02 | CI-4 | GitHub Actions matrix | `/tmp/private` macOS realpath difference — Test 93 fails | CI run 26789848961 logs | `b56d6ba` | Test 93 compares via `os.path.realpath` both sides | FIXED |
| 2026-06-02 | CI-5 | GitHub Actions matrix (macOS APFS mtime sub-second precision) | Test 49 fails on macOS — `act-observe-verify.sh` exits via STALE_RESULT before cleanup | CI run 26790477737 | `7a957f9` | Test 49 skips on macOS (Darwin) | FIXED (covered by Test 25 cross-platform) |
| 2026-06-02 | F-BYPASS-001 to 008 | adversarial workflow (8 finders) | bash_scanner missing decoders for eval / backticks / `$(...)` / source/. / BASH_ENV / quoted destructive paths / apt-no-`-get` | per-payload reproduction via `python3 -c "scan_command(...)"` | `97b5457` + `b56d6ba` | 14/14 bypass payloads BLOCKED (see CISO final audit) | FIXED |
| 2026-06-02 | STRIDE-Rep-1 | independent council (CISO) | Audit tables have `BEFORE DELETE` but no `BEFORE UPDATE` triggers | attempted in ITER5; reverted | NOT_FIXED — WAL high-frequency write regression caused REINDEX failure | `verify_audit_chain` provides detection-on-tamper (not prevention) | DEFERRED (documented OUT-OF-SCOPE in THREAT_MODEL.md; HMAC chain provides detection) |
| 2026-06-02 | DOCS-1 | own | `state_engine.py` "1180 LOC" claim in ADR-001 drifted to 1296 LOC | `wc -l scripts/lib/state_engine.py` vs ADR claim | `b56d6ba` | ADR-001 updated to ~1296 LOC | FIXED |
| 2026-06-02 | DOCS-2 | own | `CLAUDE.md` test count "47/47 PASS" stale; actual 94 tests | `bash tests/adversarial-test.sh \| tail -1` | `97b5457` | CLAUDE.md now says "94/94 PASS, 5/5 stable" | FIXED |
| 2026-06-02 | DOCS-3 (PR-B) | own | Test count "94/94" stale in README/CLAUDE.md/ADR-001/ADR-003 after v1.5.0 added Tests 97-100; VERSION file existed but was 1.4.1 (not 1.5.0) | `grep -rn "94/94" --include="*.md" .` | (this commit) | All 5 docs updated to 100/100; VERSION bumped 1.4.1 → 1.5.0 with PR-B changelog entry | FIXED |

---

## Council grade trajectory

| Iteration | CISO | QA | Architect | DevOps | Composite |
|---|---|---|---|---|---|
| 0 (auto-claim) | "100%" | "100%" | "100%" | "100%" | D− (refuted) |
| 0 (real, independent) | D | D | C+ | C− | D− |
| ITER 1-2 | B | B | B− | B | B− |
| ITER 3 | B+ | B− | B+ | A | B+ |
| ITER 4 (atomic UPSERT) | A | C+→B | B+ | B | B+ |
| ITER 5 (HMAC wired) | **S** | A | A− | A | **A** |
| ITER 6-7 (regression under multi-agent load) | A | C | B− | F | C+ |
| **ITER 8 (sequential council, final)** | **S** | **S** | **S** | **S** | **S** |

The regression at ITER 6-7 is a methodological finding: **parallel council audits pollute the shared SQLite DB**. Sequential audits restore the S grade. Codified in [`AUDIT_CYCLE.md`](AUDIT_CYCLE.md) §"ISOLATE-VERIFY".

---

## Open items (DEFERRED, not WONT_FIX)

| Date | ID | Why deferred | Trigger to revisit |
|---|---|---|---|
| 2026-06-01 | CRIT-8 (bash-guard false positives) | String scanner ≠ parser; fixing requires shell-parser library (bashlex / `shlex` AST walk) | If false-positive rate is reported by downstream users |
| 2026-06-01 | HIGH-9 (phase rules duplicated) | Architectural debt; ADR-002 candidate for v1.6+ | If a phase rule drift is observed (CI doc-lint) |
| 2026-06-02 | STRIDE-Rep-1 (BEFORE UPDATE) | WAL-mode write regression; detection-on-tamper via HMAC is the v1 contract | If the SQLite WAL semantics around UPDATE triggers improve OR if an alternative tamper-evidence mechanism is needed |
| 2026-06-02 | KARPATHY-5 (multi-model) | v1 single-model by design (AUDIT_CYCLE.md §"Multi-model collaboration") | When the user opts in via `SWEBOK_SECONDARY_LLM` |
| 2026-06-02 | G.4 (hyperagents auto-evolution loop) | Risk > S-grade benefit; requires fitness contract | v2.0 — when the contract is designed |
| 2026-06-02 | PRB-AGG-1 (aggregation policy) | Council aggregation contract (worst-severity wins / any FAIL → FAIL) is documented in CLAUDE.md L6.1 but not codified in the harness as a deterministic merge. Current state: dispatcher-policy. | If a 2-council disagreement is observed in production or if a non-Claude dispatcher is introduced |
| 2026-06-02 | PRB-SEQ-1 (sequential vs parallel) | AUDIT_CYCLE mandates sequential council runs. The new bridge JSONL does not encode ordering; dispatcher is free to spawn 4 agents in parallel. | When a real council audit is run end-to-end and ordering becomes observable |
| 2026-06-02 | PRB-TMI-1 (council reads untrusted state) | CISO/Architect prompts ask reviewers to read `export_state` + `query_adversarial 50`, but threat model says adversarial model can INSERT into `.swebok_state.db`. No HMAC verify on the read path. | When a real council audit must trust its own read inputs |

---

## PR-B findings ledger (2026-06-02 council review of G.3 council bridge)

| Date | ID | Source | One-line finding | Evidence cmd | Fix sha | Verification cmd | Status |
|---|---|---|---|---|---|---|---|
| 2026-06-02 | F-001 (CRIT convergence) | CISO+QA+DevOps council | `2>/dev/null \| grep -E '^\{' \|\| true` silently swallows launcher crashes | `bash scripts/adversarial-gate.sh --council P5 P6; echo $?` | 94394a3 | Test 97 PASS | RESOLVED |
| 2026-06-02 | F-02 (Architect CRIT) | Architect council | Single-owner envelope contract violated: gate emitted XML inline | `grep -n MULTIAGENT_LAUNCH scripts/*.sh` | 94394a3 | `emit-envelope` task added | RESOLVED |
| 2026-06-02 | F-03 (Architect CRIT) | Architect council | CLAUDE.md Law 6 dispatcher contract still 2-agent | `grep -n "nexus-defender" CLAUDE.md` | 94394a3 | Law 6.1 added | RESOLVED |
| 2026-06-02 | F-DO-01 (DevOps CRIT) | DevOps council | Zero tests for new --council path | `bash tests/adversarial-test.sh \| tail -3` | 94394a3 | Tests 97-100 PASS | RESOLVED |
| 2026-06-02 | F-04 (Architect HIGH) | Architect+DevOps | P10/P11 phase_num silently truncates to P1 | `bash scripts/multiagent-launcher.sh emit-envelope P10 P11` | 94394a3 | Test 100 PASS, output `KA-10+KA-11` | RESOLVED |
| 2026-06-02 | INJ-1 (CISO HIGH) | CISO council | FROM_P/TO_P injected verbatim into 4 reviewer prompts | `bash scripts/adversarial-gate.sh --council 'P5; rm -rf /' P6; echo $?` | 94394a3 | Test 99 PASS, exits 1 | RESOLVED |
| 2026-06-02 | F-DO-02 (DevOps HIGH) | DevOps council | MULTIAGENT_BRIDGE_ENABLED not exposed via installer | `grep MULTIAGENT_BRIDGE_ENABLED install-harness.sh` | 94394a3 | line 130, 174 | RESOLVED |
| 2026-06-02 | F-DO-03 (DevOps HIGH) | DevOps council | OPERATIONS.md missing council bridge runbook | `grep "## 12" docs/v1/OPERATIONS.md` | 94394a3 | line 181 | RESOLVED |
| 2026-06-02 | F-DO-04 (DevOps HIGH) | DevOps council | CI matrix never exercises --council | (covered by Tests 97-100) | 94394a3 | Tests 97-100 in adversarial-test.sh | RESOLVED |
| 2026-06-02 | F-DO-05 (DevOps MED) | DevOps council | THREAT_MODEL A6 fixture row mislabeled under A8 | `grep -A1 "Adversarial gate is" docs/v1/THREAT_MODEL.md` | 94394a3 | row now in A6/A7 section | RESOLVED |
| 2026-06-02 | F-DO-08 (DevOps MED) | DevOps council | Launcher had `set -e` only, not `set -euo pipefail` | `head -10 scripts/multiagent-launcher.sh` | 94394a3 | `set -euo pipefail` line 9 | RESOLVED |
| 2026-06-02 | F-DO-06 (DevOps MED) | DevOps council | log_dsl to STDOUT polluted envelope | `bash scripts/multiagent-launcher.sh emit-prompts P5 P6 2>/dev/null` | 94394a3 | clean JSONL on STDOUT | RESOLVED |

---

## How to append a new row

Append at the END of the table for the current quarter. **Do not edit historical rows.** Use this template:

```markdown
| YYYY-MM-DD | <ID> | <source-audit> | <one-line finding> | <evidence-cmd> | <fix-sha> | <verification-cmd> | <STATUS> |
```

After appending, increment the relevant council-grade row if the finding's resolution changes a grade. Recompute the composite via the rule: composite = `min(category grades)`. Any single category below A− pulls composite below A.
