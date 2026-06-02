# Threat Model — SWEBOK v4 Harness

**Last updated**: 2026-06-01 (post-audit rebuild)
**Status**: Living document. Update on every CRIT/HIGH finding.

## Assets

| ID | Asset | Why it matters |
|---|---|---|
| A1 | `.swebok_state.db` SQLite file | Single source of truth for current phase, gates validated, circuit breaker counter, audit tables |
| A2 | 4 audit tables (`adversarial_log`, `log_events`, `state_events`, `circuit_breaker_events`) | Forensic trail; chain of custody for gate decisions |
| A3 | `phase-guard.sh` + `bash-guard.sh` hooks | Gate logic; runs on every relevant tool call |
| A4 | `state_engine.py` | All read/write to A1/A2; ~600 LOC |
| A5 | `bash_scanner.py` | String-pattern scanner; phase-rule database |
| A6 | `.claude/settings.json` | Hook wiring + permission allowlist + env vars |
| A7 | `~/.claude/settings.json` | User's global Claude Code config; carries `ANTHROPIC_AUTH_TOKEN` |
| A8 | `install-harness.sh` | Installer; touches A6, A7 |
| A9 | The Claude session itself (model + sub-agents) | Trust assumption — see "Trust model" below |

## Trust model

The harness assumes Claude is **cooperative-but-fallible**. It will attempt to follow the SDLC discipline but may inadvertently:
- Try to write to `src/` during P1 specification (mistake, not malice)
- Spawn a sub-agent without remembering it's in P3 (forgetfulness)
- Get prompt-injected by external content fetched via WebFetch

The harness does NOT assume Claude is **adversarial**. An adversarial model with Python access can:
- Read `.swebok_state.db` directly and INSERT current_phase = P9
- Drop the audit-table triggers and rewrite history
- Spawn a sub-agent with a custom prompt that bypasses the matcher patterns

If the threat model includes adversarial-model, the harness is insufficient. Add OS-level isolation (LSM, seccomp, container).

## Per-asset attack tree

### A1 — `.swebok_state.db`

| Vector | Mitigation | Status |
|---|---|---|
| Direct INSERT current_phase via `sqlite3` CLI | None — file is mode 0644, owned by user | OUT OF SCOPE (STRIDE-Tamper-1, documented) |
| Concurrent-writer corruption | WAL + `BEGIN EXCLUSIVE` + 10-attempt retry loop in `_xact()` | IN SCOPE, verified at 1000-concurrent (live, 5/5 runs) |
| Schema migration failure | `shutil.copy2` backup + decorator-based migration registry that raises on missing version | IN SCOPE |
| Disk full | `_translate_op_error` exits with code 4 | IN SCOPE |
| Read-only FS | exits with code 3 | IN SCOPE |

### A2 — audit tables

| Vector | Mitigation | Status |
|---|---|---|
| `DELETE FROM adversarial_log` | `BEFORE DELETE` trigger raises | IN SCOPE |
| `UPDATE adversarial_log SET verdict='PASS'` | NOT mitigated — BEFORE UPDATE trigger was attempted 2026-06-01 but caused regression under WAL+high-frequency writes; reverted. Row-content tampering remains an open gap. | OUT OF SCOPE (TBD) |
| `DROP TRIGGER` + DELETE + `CREATE TRIGGER` | Defense-in-depth: `_ensure_triggers()` re-asserts on every `_init_db()`; maintenance role uses this intentionally (C5 contract) | IN SCOPE (PARTIAL — see C5) |
| `DROP TABLE` | Not blocked — caller has full DDL access | OUT OF SCOPE; mitigation = file ACL |
| Process killed mid-prune (between DROP and CREATE) | `_ensure_triggers()` restores on next startup | IN SCOPE |

### A3/A4/A5 — hook scripts and Python libs

| Vector | Mitigation | Status |
|---|---|---|
| Hook crash → fail-OPEN | `set -euo pipefail` + ERR trap = fail-CLOSED | IN SCOPE |
| Hook hung 30s+ on locked DB | `busy_timeout=30000ms` + 10-retry loop | IN SCOPE |
| `python -c "..."` injection in phase-guard JSON parser | `json.loads` is the only Python call; no `eval` | IN SCOPE |
| Tool input >1 MB DoS | H7 1 MiB cap | IN SCOPE |
| Path traversal `../../src/x.py` | M29 `realpath -m` canonicalisation | IN SCOPE |
| Unicode/Cyrillic homoglyph `сrc` (Cyrillic с-r-c vs Latin src) | NOT mitigated; scanner is byte-level | OUT OF SCOPE (F-BYPASS-013, documented) |

### A6/A7 — settings.json

| Vector | Mitigation | Status |
|---|---|---|
| `install-harness.sh` overwrites `~/.claude/settings.json` wiping user env | NOT mitigated; installer is destructive | OUT OF SCOPE (DevOps-Gap1, roadmap) |
| `mcp__*`, `Glob`, `Grep`, `LS`, `TodoWrite`, `NotebookRead`, `ExitPlanMode` matchers absent | NOT mitigated; tools run without harness gate | OUT OF SCOPE (STRIDE-Iso-1, roadmap) |
| `skipDangerousModePermissionPrompt:true` in install | NOT mitigated | OUT OF SCOPE |
| Adversarial gate is a hardcoded RED/BLUE fixture per phase (CRIT-2 from 2026-06-01 audit) | OPT-IN via `adversarial-gate.sh --council` with `MULTIAGENT_BRIDGE_ENABLED=1` — spawns 4 Nexus reviewers (`nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead`) through the dispatcher. Default behaviour stays fixture-based for deterministic CI. | OPT-IN MITIGATED (see `ADR-003-multiagent-bridge.md`) |

### A8 — `install-harness.sh`

| Vector | Mitigation | Status |
|---|---|---|
| Unsigned installer | NOT mitigated | OUT OF SCOPE |
| Hardcoded harness path | Mitigated — all runtime scripts self-resolve via `dirname` (zero hardcoded paths) | RESOLVED |

## STRIDE matrix

| Category | In scope | Out of scope |
|---|---|---|
| **S**poofing | session_id/agent/correlation_id are env-derived audit fields. Cooperative-model assumption. | Cryptographic identity binding (STRIDE-Spoof-1) |
| **T**ampering | Audit-table triggers (DELETE+UPDATE); WAL atomicity; M16 backup. | Direct SQLite write to A1/A2 outside the harness (STRIDE-Tamper-1, 2, 3, 4) |
| **R**epudiation | `state_events` records every `set()`; `circuit_breaker_events` records every block; `adversarial_log` records every gate verdict. BEFORE DELETE triggers block silent purge. | BEFORE UPDATE protection NOT installed (regression). Row-content tampering OUT OF SCOPE. Off-host sink, HMAC chain (STRIDE-Rep-1 partial) |
| **I**nformation disclosure | Phase logs do not contain secrets. | `ANTHROPIC_AUTH_TOKEN` in `~/.claude/settings.json` plaintext; installer touches this file (STRIDE-Info-1) |
| **D**enial of service | 1 MiB stdin cap; circuit breaker hard-locks after 3 to prevent loops; backups pruned to keep_last=3. | Adversarial xargs flood; single global state can be locked for all projects (STRIDE-DoS-1, partial) |
| **E**levation | Phase transitions require gates; `record_block` is atomic. | Direct `set current_phase P9` bypasses the gate (STRIDE-EoP-1, 2 out of scope without auth) |

## Verification: how to confirm the harness still meets the model

1. Run `tests/adversarial-test.sh` — must be 92/92 PASS, exit 0, 5 consecutive runs.
2. Run `tests/attack-payloads-test.sh` — STRIDE-lite, must be 8/8 PASS.
3. Run independent council audit (CISO, QA, Architect, DevOps) every release.
4. Run an 8-finder adversarial workflow at least once per major version.
5. Maintain the `[X]` Status column above per release.

## Out-of-scope items on roadmap (path to "S" grade in all categories)

- Multi-project isolation via per-project `HARNESS_DIR` resolved from `git rev-parse`
- HMAC chain for audit rows + off-host sink
- Signed installer + checksum manifest
- `mcp__*` / `Glob` / `Grep` / `LS` matchers added
- Privilege drop into a `harness` UID after startup
- Unicode/homoglyph normalisation in the scanner pre-pass
- LSM/seccomp sandbox for hook execution
