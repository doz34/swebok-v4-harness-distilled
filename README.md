# SWEBOK v4 Harness

> **A structural SDLC enforcement layer for Claude Code.**
> Phase-gated development with atomic state, append-only audit, and an HMAC chain.
> Honest threat model, honest test stability, honest documentation.

[![Tests](https://img.shields.io/badge/tests-94%2F94%20PASS%2C%205%2F5%20stable-brightgreen)](docs/v1/TEST_STABILITY.md)
[![STRIDE-lite](https://img.shields.io/badge/STRIDE--lite-8%2F8-brightgreen)](tests/attack-payloads-test.sh)
[![Concurrent atomicity](https://img.shields.io/badge/atomicity-1000%2F1000-brightgreen)](docs/v1/TEST_STABILITY.md)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## What it is

The SWEBOK v4 Harness wires four things into a Claude Code session:

1. **Phase guard.** A `PreToolUse` hook that reads the current SDLC phase (`P1_REQUIREMENTS` → `P9_DEPLOYMENT`) from an atomic SQLite state DB and refuses `Write` / `Edit` / `Bash` / `Skill` / `Task` / `Agent` / `MCP` operations that violate the current phase's contract. Built fail‑secure: any internal error blocks the action.
2. **Bash scanner.** A pattern engine that decodes shell quoting (`eval`, `bash -c`, ANSI‑C `$'…'`, backticks, `$(…)`, `source` / `.`, `BASH_ENV`, base64) before running the per‑phase rule set, so common evasions surface to the same path-and-verb rules as a plain literal.
3. **Atomic state engine.** SQLite WAL with single‑statement UPSERT counters (`INSERT … ON CONFLICT DO UPDATE`), JSON1 `json_set`/`json_extract` for nested keys, `BEGIN EXCLUSIVE` + 10‑attempt retry for combined state + audit writes, and `BEFORE DELETE` triggers on every audit table restored on every `_init_db()` call.
4. **HMAC audit chain.** Every audit row carries `row_hmac = HMAC‑SHA256(prev_hmac, ts, table, content…)`. Any `UPDATE`, `DELETE`, or out‑of‑order `INSERT` breaks the chain and is detected by `verify_audit_chain`. Prune is supported via `recompute_audit_chain`, which re-attaches the chain after a legitimate maintenance purge.

It is **not** a sandbox. It is **not** an authentication boundary. The threat model in `docs/v1/THREAT_MODEL.md` names what is in scope, what is out, and where every remaining gap is documented.

## Quick start

### Requirements

- Linux or macOS (Bash 4+ — macOS users: `brew install bash` if you want the GNU version)
- Python 3.10 or newer
- `sqlite3` CLI
- `jq` (for the installer's safe settings merge)

### Install

```bash
git clone https://github.com/<your-org>/swebok-v4-harness.git
cd swebok-v4-harness
bash install-harness.sh
```

The installer **merges** the harness's hook entries into your existing `~/.claude/settings.json` (using `jq`), writes a timestamped backup before touching anything, prompts for consent, and refuses to overwrite your user environment variables.

### Verify

```bash
# Cold start
python3 scripts/lib/state_engine.py rebuild

# Authoritative test run (must report 92/92 PASS)
bash tests/adversarial-test.sh

# STRIDE-lite attack payloads (must report 8/8 PASS)
bash tests/attack-payloads-test.sh

# Operational readiness probe (must report HEALTHY)
bash scripts/health-check.sh

# Pre-commit gate (full pipeline: tests + HMAC + STRIDE + health)
bash scripts/pre-commit-hook.sh
```

### Uninstall

See [UNINSTALL.md](UNINSTALL.md). Briefly: restore the timestamped settings backup the installer wrote, then `rm -rf` the harness directory.

## What you get when you use it

Each Claude Code tool call goes through the gate. Concretely:

- A `Write` to `src/main.py` during a specification phase (`P1`, `P2`) is **blocked** with a structured reason.
- A `Bash` invocation of `rm -rf /` or `rm -rf "/quoted/path"` or `mkfs.ext4 /dev/sda` is **blocked** in every phase, not just construction.
- A `Bash` invocation of `eval "$(echo cm0gLXJmIC8= | base64 -d)"` is decoded by the pre-pass and **blocked** because the decoded payload matches the destructive rule.
- A `BASH_ENV=/tmp/attacker.sh bash -c id` is **blocked** as `BASH_ENV_INJECTION` unless `BASH_ENV` points to an entry on the small system allowlist (`/etc/profile`, `/etc/bashrc`, `/etc/bash.bashrc`).
- Three consecutive blocks on the same file **hard-lock** that operation (fail‑closed); only an explicit operator command (`state_engine.py set circuit_breaker.override_active true`) lifts it.
- Every gate decision is logged with `(ts, gate, verdict, reason, session_id, agent, correlation_id, row_hmac)` so post-incident replay is possible via `state_engine.py replay_session <t0> <t1>`.

## Architecture at a glance

```
User Prompt
   │
   ▼
Claude Code ─── (.claude/settings.json hooks) ───▶  PreToolUse
                                                       │
                          ┌────────────────────────────┤
                          ▼                            ▼
              phase-guard.sh                      bash-guard.sh
              (Write/Edit/Skill/                  (Bash only)
               Task/Agent/Web/MCP)                     │
                          │                            ▼
                          │                   scripts/lib/bash_scanner.py
                          ▼                       (regex + decode pre-pass)
              scripts/lib/state_engine.py
              (atomic SQLite WAL)
                          │
                          ▼
              .swebok_state.db
              ┌────────────────────────────────────────┐
              │ state              ← single source     │
              │ adversarial_log    ← BEFORE DELETE     │
              │ log_events         ← + row_hmac chain  │
              │ state_events       ← per-row           │
              │ circuit_breaker_   ← HMAC-SHA256       │
              │   events           ←                   │
              │ metadata (schema_version)              │
              └────────────────────────────────────────┘
```

For the detail, see [`docs/v1/ARCHITECTURE.md`](docs/v1/ARCHITECTURE.md) and the two ADRs:
[`ADR-001`](docs/v1/ADR-001-state-engine-cohesion.md) (cohesion vs decomposition) and
[`ADR-002`](docs/v1/ADR-002-decomposition-threshold.md) (decomposition trigger rules).

## Phase model

| Phase | Theme | Blocks |
|---|---|---|
| **P1** Requirements | Specs, no code | `.py/.ts/.js/...` extensions, `src/`, `lib/`, `impl/`, `mkdir src` |
| **P2** Architecture | Decision diagrams | Same as P1 |
| **P3** Design | Interface contracts | `src/`, `impl/`, `implementations/`, `.py` |
| **P4** Estimation | Feasibility | Same as P3 |
| **P5** Construction | First implementation | `mkdir src` (new tree only), all destructive commands |
| **P6** Verification | Tests only | Non-test access to `/src` |
| **P7** Deployment | Release artifacts | Destructive commands |
| **P8** Maintenance | Bug-fix patches | Destructive commands |
| **P9** Retirement | EOL | Package managers (except `security`/`patch`), implementation paths |

Every phase also enforces the **global destructive list** (`rm -rf /…`, `rm -rf ~`, `rm -rf .`, `rm --`, `find -delete`, `shred`, `srm`, `wipe`, `mkfs.*`, `dd of=/dev/*`, `DROP TABLE`, `DROP DATABASE`, `BASH_ENV` non-system targets).

Transitions are made via `state_engine.py set current_phase P<N>` and gated against `gates_validated` (the list of phase exits already crossed).

## Test stability contract

The headline number is **92/92 PASS, 5/5 stable on sequential cold rebuilds**. (Test IDs go 1–106 with gaps; 92 is the function count — each test can have multiple assertions. See `docs/v1/VERSION` for the test-numbering convention.) The contract is documented at the top of [`tests/adversarial-test.sh`](tests/adversarial-test.sh) and in [`docs/v1/TEST_STABILITY.md`](docs/v1/TEST_STABILITY.md). Key points:

- **Sequential** invocation is the supported execution model. Running multiple concurrent test runs against the same SQLite DB is **not** supported (and is honestly documented as such — see the CI workflow for the recommended pattern).
- **Concurrent counter tests** use PID-isolated subkeys (`phase_data.P6.iso100_$$`, `phase_data.P6.iso1000_$$`) so they exercise the atomic UPSERT path without contending with the production counters.
- **Per-project state DB**: `_resolve_state_db()` honors `$SWEBOK_STATE_DB` first, then `<git_project_root>/.swebok_state.db`, then a single-project fallback. Run the harness against multiple projects and the state is automatically isolated per project.

## Opt-in: real council bridge (v1.3)

By default, `adversarial-gate.sh` runs in **fixture mode** (canned RED/BLUE DSL per phase) so unit tests, CI, and local dev are deterministic. To run a **real** adversarial review that spawns 4 independent reviewer agents (`nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead`) through the dispatcher:

```bash
export MULTIAGENT_BRIDGE_ENABLED=1
bash scripts/adversarial-gate.sh --council P5 P6
# → exit 99, single <MULTIAGENT_LAUNCH gate="P5_EXIT" target="P6">…</MULTIAGENT_LAUNCH>
# → dispatcher reads each JSONL line, invokes the Agent tool with the named
#   subagent_type, collects each agent's DSL, re-invokes with --judge-only.
```

**Cost**: ~40k output tokens per gate transition (4 reviewers × ~10k each). A full SDLC run (5 transitions) is ~200k tokens. For comparison, the harness's D→S journey consumed ~18M tokens.

**Contract** (single-owner): `multiagent-launcher.sh emit-envelope` owns the WHOLE `<MULTIAGENT_LAUNCH>` envelope (wrapper + JSONL body + close tag). The gate just calls it. See `CLAUDE.md` Law 6.1 and [`docs/v1/ADR-003-multiagent-bridge.md`](docs/v1/ADR-003-multiagent-bridge.md).

**Runbook**: [`docs/v1/OPERATIONS.md`](docs/v1/OPERATIONS.md) §12 covers enable / invoke / what-happens / cost / WARN / rollback.

## Security posture

**In scope.** Phase-aware blocking of writes and shell commands, atomic state with WAL retry semantics, append-only audit log with `BEFORE DELETE` triggers restored on every startup, per-row HMAC chain with detection-on-tamper, fail-closed circuit breaker, decoded shell-quoting evasions, global destructive block.

**Out of scope.** Sandbox-grade process isolation, syscall filtering, cryptographic chain-of-custody with off-host sink, prevention of direct SQLite tampering by anyone who has write access to the DB file. See [`SECURITY.md`](SECURITY.md) and [`docs/v1/THREAT_MODEL.md`](docs/v1/THREAT_MODEL.md) for the full breakdown.

**Reporting issues.** Open a private issue, do not post bypasses to the public tracker. Include the payload, the phase, and the harness output.

## Operations

[`docs/v1/OPERATIONS.md`](docs/v1/OPERATIONS.md) is the SRE runbook. It covers:

- A frozen / unresponsive hook (with the `~3 ms p99 steady-state` baseline)
- A corrupt SQLite DB (recovery via `state_engine.py rebuild`)
- The hard-locked circuit breaker (with the explicit operator override sequence)
- Restoring from a `.swebok_state.db.bak.*` snapshot
- WAL bloat recovery
- Tailing the audit log via `query_log_events`, `query_state_events`, `query_circuit_breaker_events`, `query_adversarial`
- A `scripts/health-check.sh` exit-code contract (0 HEALTHY, 1 DEGRADED, 2 BROKEN)
- A `state_engine.py metrics` one-shot summary

## Documentation map

| File | What it covers |
|---|---|
| [`README.md`](README.md) | This file. |
| [`SECURITY.md`](SECURITY.md) | In-scope / out-of-scope security policy. Vulnerability reporting process. |
| [`UNINSTALL.md`](UNINSTALL.md) | Step-by-step removal and recovery. |
| [`docs/v1/ARCHITECTURE.md`](docs/v1/ARCHITECTURE.md) | Component diagram and data flow. |
| [`docs/v1/PHASES.md`](docs/v1/PHASES.md) | Phase rules and transition gates. |
| [`docs/v1/HOOKS.md`](docs/v1/HOOKS.md) | Hook contract and stdin JSON format. |
| [`docs/v1/THREAT_MODEL.md`](docs/v1/THREAT_MODEL.md) | Per-asset attack tree and STRIDE matrix. |
| [`docs/v1/OPERATIONS.md`](docs/v1/OPERATIONS.md) | SRE runbook. |
| [`docs/v1/TEST_STABILITY.md`](docs/v1/TEST_STABILITY.md) | Stability matrix and CI guidance. |
| [`docs/v1/ADR-001-state-engine-cohesion.md`](docs/v1/ADR-001-state-engine-cohesion.md) | Why the state engine stays monolithic. |
| [`docs/v1/ADR-002-decomposition-threshold.md`](docs/v1/ADR-002-decomposition-threshold.md) | When and how to decompose it. |
| [`docs/v1/DSL_SPEC.md`](docs/v1/DSL_SPEC.md) | The `;;` DSL parser used by the adversarial gate. |

## Continuous integration

The shipped GitHub Actions workflow (`.github/workflows/test.yml`) runs:

- A 2 × 3 matrix (Ubuntu × macOS × Python 3.10 / 3.11 / 3.12).
- A cold `state_engine.py rebuild`.
- A warm-up test pass (advisory, may flake on cold WAL).
- An authoritative test pass (gating).
- The STRIDE-lite suite.
- The HMAC chain verification on all four audit tables.
- A 1000-way concurrent atomicity smoke test.
- `ruff` and `shellcheck` (advisory, not gating in v1).

The `scripts/pre-commit-hook.sh` mirrors the gating subset locally. Symlink it into your project's `.git/hooks/pre-commit` to block commits that would break the harness.

## Provenance

The phase taxonomy and knowledge-area mapping align with **SWEBOK v4** (IEEE Software Engineering Body of Knowledge, 4th edition). All other references are deliberately abstracted — the harness is meant to be self-contained code, not an annotated bibliography.

## Versioning

Semantic versioning. `docs/v1/VERSION` carries the canonical version string and changelog. The schema in the SQLite DB also has a `STATE_VERSION` that the engine migrates forward automatically (`MIGRATIONS` registry in `state_engine.py`). The engine refuses to read a DB with a newer schema than the code.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

1. Read [`docs/v1/ARCHITECTURE.md`](docs/v1/ARCHITECTURE.md) and [`docs/v1/THREAT_MODEL.md`](docs/v1/THREAT_MODEL.md) first.
2. Run `bash scripts/health-check.sh` and `bash tests/adversarial-test.sh` on your branch — must report HEALTHY and 92/92.
3. If you add a new audit-table column or migration, bump `STATE_VERSION` and add a `@migration(N)` function. The HMAC chain field list lives in `verify_audit_chain` — update it in lockstep.
4. If you add a new hook or matcher, document it in `docs/v1/HOOKS.md` and add a corresponding test in `tests/adversarial-test.sh`. Use the `=~ ^BLOCKED:` exact-prefix assertion pattern.
5. CRIT / HIGH findings from independent audits should land as `AUDIT-YYYY-MM-DD FIX` comments in the file they touch, with the finding ID.

## Acknowledgements

Architecture, security model and test design were stress-tested by an iterative council of independent reviewers (CISO, QA Lead, Architect, DevOps roles). The iterative pattern that produced the current version is documented in `.ai/docs/designs/FINAL_TRAJECTORY_2026-06-01.md` for anyone who wants to apply the same anti-tautology methodology elsewhere: **the agent that verifies a fix is never the agent that applied it.**

---

*The harness is software-engineering scaffolding. Read the threat model before relying on it for anything safety-critical.*
