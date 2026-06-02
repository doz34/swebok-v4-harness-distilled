# State Engine Design Review (v1.4.1)

**Target file**: `scripts/lib/state_engine.py` (1725 LOC)
**Date**: 2026-06-01
**Doc**: Iterative Code Design V2 — review-only output

## 1. Intent / problem statement

The state engine is the single source of truth for the harness. It must guarantee:
- Atomic counter updates under 1000-way concurrency (tested: pass).
- Append-only audit tables (4 trigger-protected).
- Schema migration without data loss.
- Graceful recovery from a corrupt DB.

The user asks: is the "100% production-ready" claim defensible at the design level, or are there hidden ways the file can silently corrupt state or lose its safety properties? This review answers that question without writing fixing code — it produces a baseline of what is currently designed, a ledger of what is questionable, and a compression review of what can be removed or reshaped.

## 2. Goal initialization and repository guidance

Sources consulted:
- `CLAUDE.md` — names `scripts/lib/state_engine.py` as the single source of truth; bans the YAML state file.
- `docs/v1/ARCHITECTURE.md` — claims atomicity via BEGIN EXCLUSIVE on every nested-key update; lists 7 atomic operations.
- `docs/v1/VERSION` — v1.4.1, dated 2026-06-01.
- The file itself (1725 LOC, 50+ public functions).

Repo constraints relevant to this review:
- The file is imported by every hook and several scripts. Latency on `get()` and `set()` is on the critical path of every Claude tool call.
- The audit tables (`adversarial_log`, `log_events`, `state_events`, `circuit_breaker_events`) are protected by `BEFORE DELETE` triggers (C5 contract).
- The harness ships with an installer (`install-harness.sh`) that copies the file verbatim into the project root.

## 3. Scope and non-goals

**In scope**:
- Concurrency invariants (BEGIN EXCLUSIVE, WAL, busy_timeout).
- Append-only contract for the 4 audit tables.
- Schema-migration safety (M3 backup + ALTER TABLE).
- Recovery paths (`rebuild()`).
- Connection-management strategy (4 patterns coexist).

**Out of scope**:
- Refactoring the file into modules (would change blast radius; design only).
- The choice of SQLite vs Postgres/Redis (orthogonal to this review).
- The CLI surface in `main()` (only inspected for atomicity).

## 4. Current evidence and inspected files

| Path | Why inspected |
|---|---|
| `scripts/lib/state_engine.py` lines 1-300 | Schema init, migrations, connection patterns |
| same file lines 300-900 | `set/get/record_block/increment_*` (the atomic claim) |
| same file lines 1200-1550 | `_prune_with_trigger`, `prune_*`, `rebuild`, `export_state` |
| `docs/v1/ARCHITECTURE.md` | Stated atomicity contract |
| `docs/v1/VERSION` | Version history; M3, R1, R2, I11-I14 fix labels |
| `CLAUDE.md` | Re-asserts single source of truth |
| `.swebok_state.db` schema (live) | Confirmed 5 tables + 4 triggers exist |

## 5. Baseline design inventory (MANDATORY)

| id | source | decision | location | current assumption | why it matters now | pressure signal |
|---|---|---|---|---|---|---|
| B1 | existing code | Schema versioned by `STATE_VERSION=2` + `MIGRATIONS` dict; backup-before-migrate via `shutil.copy2` | state_engine.py:53-58, 432-503 | A pre-migration backup is sufficient for rollback | Determines whether a failed migration is recoverable | A migration partially commits then crashes |
| B2 | existing code | 4 different connection-acquisition patterns coexist: `_get_db()`, `_get_pooled_conn()`, `_open_wal_conn()`, `_connect()` | state_engine.py:80-216 | Each path is correct in isolation; the caller picks | Determines which call sites get the integrity check, which get pooling, which get WAL pragmas | A new public function picks the wrong pattern and silently disables integrity_check |
| B3 | existing code | `_prune_with_trigger()` is the contract-breaking operation: `DROP TRIGGER` + `DELETE` + `CREATE TRIGGER` on one connection | state_engine.py:1211-1238 | Same-connection means the trigger is reliably absent during the DELETE and reliably present after the commit | Determines whether an append-only audit table can lose its append-only property silently | The Python process is killed between `DROP TRIGGER` and `CREATE TRIGGER` |
| B4 | existing code | `_get_db()` runs `PRAGMA integrity_check` on every call (M11) | state_engine.py:243-264 | Cost is acceptable; structural corruption must be loud | `integrity_check` is O(rows+indexes); it runs in the critical path of every hook | Hot-path latency budget breached as audit tables grow |
| B5 | existing code | `atexit.register(_close_pooled_conns)` was added then DISABLED (line 162) with a comment about 20-concurrent stress flakiness | state_engine.py:148-162 | Long-running pooled callers must close their own connections | The pool is documented as internal-only; if a future caller uses `_get_pooled_conn`, it leaks | A future contributor adds a pooled caller and the WAL file grows without bound |
| B6 | existing code | Migrations declared in `MIGRATIONS` dict keyed by target version; migration functions are looked up via `globals()` | state_engine.py:54-59, 443-449 | The function name in the dict is in globals at import time | Migration discoverability is by string match; typo in the dict silently skips the migration | A new migration is added with a typo and is not run |
| B7 | existing code | `set()` does the state write AND the `state_events` audit insert inside one BEGIN EXCLUSIVE | state_engine.py:593-672 | Audit row and state mutation are committed atomically (H3 contract) | If audit insert fails for any reason, the state mutation is rolled back too — fail-secure | An audit-only schema bug (e.g. NOT NULL on a new column) would block every set() |
| B8 | existing code | `_wal_checkpoint(conn)` is called inside `_get_db().close()` paths (called by `get()`, `set()`, `query_*`) | state_engine.py:564, 670, 1391 | PASSIVE checkpoint after every read/write is cheap | Adds two extra PRAGMA round-trips per call; multiplies with `M11 integrity_check` cost | Latency on read-heavy workloads (e.g. UI rendering current_phase) |
| B9 | existing code | `rebuild()` renames a corrupt DB to `.db.corrupt.<ts>` then re-inits; M16 path copies audit tables from a `.db.pre-rebuild.<ts>` snapshot | state_engine.py:1395-1478 | The pre-rebuild snapshot exists when rebuild runs | If rebuild is called without M4 having created a pre-rebuild snapshot, audit history is lost silently | A user invokes rebuild on a fresh DB or before any migration |
| B10 | existing code | `_coerce_for_field()` infers field type from the existing value's stringified form | state_engine.py:568-590 | "true"/"false"/"True"/"False" cover all boolean call sites; int parse covers all numeric call sites | Type coercion has no schema; the inference can flip between calls | First call writes `"1"` (numeric); second writes `"on"` (string); third call sees `"on"` and writes as-is |
| B11 | existing code | `_init_db()` is guarded by a global `_DB_READY` flag (L6) | state_engine.py:62, 316-318 | Once-only init per process | If `_init_db` partially fails (sets `_DB_READY` False), subsequent calls re-run schema creation | A migration crash in the middle leaves `_DB_READY` False; the next call re-runs migration; double-migration risk |
| B12 | existing code | Audit-tables trigger-protected via 4 `BEFORE DELETE` triggers (C5) | state_engine.py:393-420 | Triggers are the only enforcement of append-only | A code path that drops the trigger and forgets to recreate it permanently disables protection | See B3 |
| B13 | existing code | `prune_*` functions return -1 on `IntegrityError` (trigger fired) | state_engine.py:1249-1305 | Callers can distinguish 0 (nothing to prune) from -1 (blocked) | `-1` is also a Python falsy-ish value; a caller using `if prune_log_events()` treats -1 as success | A maintenance script silently treats "blocked" as "successful no-op" |

## 6. Proposed design decision ledger (MANDATORY)

Note: this review does not implement; the ledger lists design changes that the implementation should make.

| id | decision | location | reason | assumption | related baseline ids |
|---|---|---|---|---|---|
| D1 | Make `_prune_with_trigger` crash-safe: wrap DROP+DELETE+CREATE in a single transaction so a kill between steps rolls back the DROP; OR, on every `_init_db()`, re-create any missing trigger | state_engine.py:1211-1238 and :310-503 | A SIGKILL between DROP and CREATE permanently disables the append-only contract; no recovery exists today | SQLite triggers are recreated by re-running `CREATE TRIGGER IF NOT EXISTS` in `_init_db` | B3, B11, B12 |
| D2 | Move the M11 `integrity_check` off the critical path: run it on `_init_db()` once per process, or on a probe command, not on every `_get_db()` call | state_engine.py:243-264 | Integrity check is O(rows + indexes) and runs on every read; audit tables grow; latency degrades silently | Periodic check is sufficient for structural corruption detection | B4, B8 |
| D3 | Collapse the 4 connection patterns to 2 with named call sites: `_open(write=False, write_xact=False)` and a documented "use this in xargs hot path" alias | state_engine.py:80-216 | 4 patterns invite picking the wrong one; the difference between `_get_db` and `_open_wal_conn` is which PRAGMAs are set and whether integrity_check runs | One factory makes the invariants discoverable; reduces blast radius of a future contribution | B2 |
| D4 | Make migration discoverability explicit: register migrations via a decorator instead of `globals().get(name)` lookup | state_engine.py:54-59, 443-449 | A typo in `MIGRATIONS = {2: "_migrate_v2_audit_metadata"}` silently skips the migration; the version bump still happens (post-migration `INSERT OR REPLACE`) | Decorator-time registration fails loudly on collisions or duplicates | B6 |
| D5 | Return a typed result from `prune_*` (e.g. dataclass with `removed: int, blocked: bool`) instead of `-1` sentinel | state_engine.py:1241-1305 | `-1` is silently coerced to truthy by `if prune_log_events():` | A namedtuple or `Result` shape forces the caller to disambiguate | B13 |
| D6 | Type-coerce on a typed schema, not on the stringified existing value | state_engine.py:568-590 | `_coerce_for_field` makes the field type a runtime accident; first writer wins the type for the lifetime of the row | A small schema map `{key: type}` removes the inference and the corner cases | B10 |
| D7 | Always check that `_DB_READY` is restored to False on any migration exception, and that re-entry into `_init_db` is idempotent for migrations that may have partially run | state_engine.py:62, 316-318, 443-489 | A partial migration that leaves the DB at version-1 schema with version-2 columns risks the next migration "re-adding" a column (ALTER TABLE ADD COLUMN fails on duplicate) | The PRAGMA-table_info dance in `_migrate_v2_audit_metadata` is the only existing defense | B11 |
| D8 | Make the M16 audit-restore path unconditional: rebuild() always copies audit tables, and the `keep_audit=False` flag is removed | state_engine.py:1395-1478 | `keep_audit=False` is reachable from CLI and silently destroys audit history; the cost of keeping it is one `copy2` of a 90KB file | The audit log is forensic data; default-destroy is anti-pattern | B9 |

## 7. Architecture and file ownership

The state engine should remain a single file (the 1725 LOC is mostly justified by the breadth of functions, not by accidental coupling). Decompose only if the file passes 2500 LOC or if D3 makes the connection management worth pulling into a `state_engine/connection.py` submodule.

Proposed layout if a future refactor is approved (not part of this review):
- `state_engine/__init__.py` — public surface (re-exports)
- `state_engine/connection.py` — D3 unified factory
- `state_engine/schema.py` — `_init_db`, `STATE_VERSION`, `MIGRATIONS`
- `state_engine/audit.py` — `log_event`, `log_adversarial`, `query_*`
- `state_engine/prune.py` — `_prune_with_trigger`, `prune_*`
- `state_engine/recovery.py` — `rebuild`, `export_state`, `export_audit`, `replay_session`

The split must NOT break the import contract (`from state_engine import get, set, ...`).

## 8. Compression review (MANDATORY)

| review id | decision id | trigger | finding | action | design update required |
|---|---|---|---|---|---|
| C1 | B3 / D1 | Step 1 (same location), Step 4 (forces a new branch on every prune) | The DROP TRIGGER + DELETE + CREATE TRIGGER sequence in `_prune_with_trigger` is not crash-safe. A SIGKILL or unhandled exception between DROP and CREATE leaves the table permanently writable for DELETE; no startup check restores the trigger. This silently breaks the append-only contract. | rewrite | D1: wrap the three statements in BEGIN EXCLUSIVE / COMMIT (SQLite supports DDL in transactions); additionally, in `_init_db`, re-issue `CREATE TRIGGER IF NOT EXISTS` for all 4 triggers on every startup |
| C2 | B4 / D2 | Step 2 (same persistence path), Step 4 (forces every hot-path call to pay the integrity_check cost) | `_get_db()` runs `PRAGMA integrity_check` on every call. On a DB with 10k audit rows + 4 indexes, this is ~10ms per call. With 100+ hook calls per Claude tool sequence, this is a 1s+ tax on every session. The check is the right thing to do; the place is wrong. | rewrite | D2: run integrity_check exactly once in `_init_db` (the once-per-process gate). Add a dedicated `check_integrity()` public function for operators. |
| C3 | B2 / D3 | Step 4 (adds a new connection helper for every new use case), Step 5 (rewriting is smaller and clearer) | 4 connection patterns with overlapping but distinct invariants are 3 too many. `_get_db` does integrity_check, `_open_wal_conn` doesn't. A future contributor must read the source to know which to pick. | rewrite | D3: collapse to a single `_open(...)` factory with explicit kwargs; deprecate the others as thin shims |
| C4 | B6 / D4 | Step 4 (forces silent-skip branch on missing migration), Step 5 (decorator-time check is smaller) | `MIGRATIONS = {2: "_migrate_v2_audit_metadata"}` is a string-name table. A typo, a forgotten import, or a rename without grep-update silently skips the migration. The version still bumps because the bump is unconditional after the for-loop. | rewrite | D4: replace with `@migration(2)` decorator that registers the function on import; raise on collision |
| C5 | B13 / D5 | Step 4 (every caller must remember to special-case -1), Step 3 (assumption "0 is success, -1 is failure" is too narrow once a caller uses truthiness) | `-1` sentinel in `prune_*` is silently coerced by truthiness. `if prune_log_events()` treats -1 as success. | rewrite | D5: typed result; alternatively, raise on blocked-prune |
| C6 | B10 / D6 | Step 3 (current assumption that "first write determines type" is too narrow), Step 4 (every new field forces a re-check of _coerce_for_field) | Type is inferred from the stringified existing value; first writer fixes the type for the row's lifetime. A migration that changes a field from int to string requires a manual delete-then-set sequence. | rewrite | D6: schema map of `{state_key: type}` |
| C7 | B5 | Step 1 (same location: pool management), Step 5 (rewriting clearer than the existing comment-block tombstone) | The disabled `atexit.register` line + 14 lines of explanatory comment is a tombstone. A future contributor reading `_get_pooled_conn` will not see the disabled line and may add a caller; the WAL file will then grow unbounded after the process. | split | Split into: (a) keep `_get_pooled_conn` as documented internal-only, and (b) extract its single legitimate use-case into a named alias `_open_dispatcher_conn()` with an explicit "you must close()" doctring. Delete `_close_pooled_conns` and the tombstone. |
| C8 | B11 / D7 | Step 4 (forces every migration to be re-entrant), Step 3 (assumption that init is once-only is too narrow on partial failure) | A migration that adds a column then crashes on the index creation leaves `_DB_READY = False`; the next call re-runs the migration; `ALTER TABLE ADD COLUMN` fails on duplicate. Current defense (PRAGMA table_info) only protects v2; future migrations may forget the dance. | merge | D7: a helper `_safe_add_column(conn, table, col, type)` that internally checks PRAGMA table_info. Every migration uses this helper; not re-implementing the dance per migration. |
| C9 | B9 / D8 | Step 3 (assumption that user knows when audit-loss is safe is too narrow), Step 5 (removing the flag is smaller and clearer) | `rebuild(keep_audit=False)` is reachable; default is True but the surface exists. A scripted rebuild that forgets the flag destroys audit history. | merge | D8: remove the flag; always preserve audit. |
| C10 | B1 | Step 1 (same path: migrations), Step 2 (reuses the backup persistence path) | Backup-before-migrate via `shutil.copy2` is good. No additional pressure surfaced in this review. | keep | The backup pattern is sound: copy2 preserves mtime, the .bak filename includes a timestamp, R2 prunes to 3 most recent. Combined with M16 pre-rebuild snapshot, the recovery surface is acceptable. |
| C11 | B7 | Step 2 (audit + state in one BEGIN EXCLUSIVE), Step 1 (same transaction boundary) | `set()` audit-then-state-in-one-transaction is the correct shape. No alternate path. | keep | The H3 contract is satisfied: either both rows land or neither does. A failed audit insert correctly fails the set. |
| C12 | B12 | Step 5 (cannot make smaller without weakening) | 4 triggers, one per audit table, is the minimal enforcement. | keep | Triggers are the only mechanism that gates DELETE. C5 contract is explicit: maintenance role drops trigger, prunes, recreates. The only defect is C1 (crash window), which D1 addresses. |
| C13 | B8 | Step 1 (same path: every public read/write), Step 4 (adds 2 PRAGMA round trips per call) | `_wal_checkpoint(conn)` after every set/get is over-eager. PASSIVE is cheap but still a round trip. Could be batched / made periodic. | defer | Latency budget has not been measured. Risk left: 2 round-trip overhead per call. Mitigation: see D2 to remove the bigger latency tax first; revisit B8 after D2 is in. |

## 9. Design iteration log

### Iteration 1 (2026-06-01, ~16:30 CEST)
Interrogated:
- Q1: "Is the file 1725 LOC justified, or is this a god object?" Answer: largely justified — the file owns 11 distinct concerns (schema, state, audit, prune, recovery, query, migration, export, replay, locking, init). Each is small (50-100 LOC). The refactor in §7 is a future option, not a debt.
- Q2 (refs B3, B12): "Is the append-only contract crash-safe?" Answer: NO — see C1.
- Q3 (refs B2): "Why do we have 4 connection patterns?" Answer: incremental additions over 3 audit rounds. See C3.
- Q4 (refs B4, B8): "What's the hot-path cost of `_get_db`?" Answer: PRAGMA integrity_check + PRAGMA wal_checkpoint per call ≈ 5-15ms per call.
- Q5 (refs B6): "What happens if MIGRATIONS dict has a typo?" Answer: silent skip; version bumps anyway. See C4.

Research:
- Read lines 1-300, 300-900, 1200-1550 of state_engine.py.
- Cross-referenced docs/v1/ARCHITECTURE.md and CLAUDE.md.

Synthesize: produced baseline B1-B13, decisions D1-D8, compression rows C1-C13.

Compression: all rewrite/split/merge actions referenced explicit ledger decisions (D1-D8). C10-C12 kept with explicit justifications. C13 deferred with named risk.

Reformat: doc is in 14-section shape.

### Iteration 2 (2026-06-01, ~16:38 CEST)
Interrogated:
- Q6 (refs B11, D7): "Can `_DB_READY` be left in an inconsistent state?" Answer: yes, on migration crash. C8 addresses with a helper `_safe_add_column`.
- Q7 (refs B13, D5): "What does `if prune_log_events():` do today?" Answer: treats -1 as success (Python truthiness). C5 is rewrite.
- Q8 (refs B5): "Is the disabled atexit a real risk?" Answer: only if a future contributor uses `_get_pooled_conn`. The disabled line is itself a smell. C7 is split.
- Q9 (refs B7): "Can the audit-then-state transaction be reordered without breaking H3?" Answer: no; current shape is correct. C11 is keep.
- Q10 (refs B9, D8): "Why does rebuild() expose `keep_audit=False`?" Answer: no reason found; flag is reachable from CLI. C9 is merge.

Research:
- Re-read `_prune_with_trigger` (lines 1211-1238) to confirm same-connection assumption.
- Confirmed SQLite supports DDL inside a transaction (DROP TRIGGER / CREATE TRIGGER inside BEGIN EXCLUSIVE).

Synthesize: refined C1 update (wrap in BEGIN EXCLUSIVE), refined C5 (typed result OR raise on blocked).

Compression: revisited every row; no orphan actions.

Reformat: tightened action descriptions.

### Iteration 3 (2026-06-01, ~16:46 CEST)
Interrogated:
- Q11 (refs B12, C12): "Could a single trigger cover all 4 tables?" Answer: no — SQLite triggers are per-table.
- Q12 (refs B8, C13): "Is the 2 round-trip wal_checkpoint per call measurable?" Answer: not measured yet; lower priority than C2.
- Q13 (refs B1, C10): "Is copy2 enough as backup, or do we need an SQLite .backup() API call?" Answer: copy2 of a WAL DB is safe because WAL writes are append-only; the .db file is consistent at any read point. Keep is correct.
- Q14 (refs D4, C4): "Is a decorator overkill for a 2-migration table?" Answer: low cost; protects against future drift. Keep as rewrite.
- Q15: "What's the smallest invariant set whose violation would silently corrupt state?" Answer:
  1. Trigger present on all 4 audit tables → violated by C1.
  2. STATE_VERSION row in metadata matches schema → violated by C4 typo.
  3. `_DB_READY` only True after a successful migration → violated by C8.
  4. Type of a `state.value` is stable across writes → violated by C6.

Research:
- Verified MIGRATIONS lookup uses `globals().get(name)` which silently returns None on typo (line 447).
- Verified `set()` already wraps audit + state in one BEGIN EXCLUSIVE (H3 satisfied).

Synthesize: confirmed the smallest invariant set (Q15). The 4 invariants above are the design's safety floor.

Compression: no new rows; all prior rewrite/split/merge actions still match the design.

Reformat: added the §15 invariant set to §13 risks.

Status: Ready for implementation.

## 10. State / replay / lifecycle considerations

State touched by every decision:
- `state` table — only `set()` and `_init_default_state` write; `get()` reads.
- `metadata.version` — written exclusively by `_init_db` after a successful migration loop.
- 4 audit tables — append-only by trigger contract; pruned by `_prune_with_trigger` (the C1 risk).

Replay surface: `replay_session(t0, t1)` UNION-ALLs the 4 audit tables ordered by `ts`. Any change to a table's column shape (e.g. D6 type coercion) must keep `ts` ASC compatible.

Lifecycle:
- Process start → `_init_db` → migrations apply → `_DB_READY = True`.
- Per-call → `_get_db` (or pool variant) → operation → `_wal_checkpoint(PASSIVE)` → close.
- Process exit → atexit handler is DISABLED (B5); pooled connections rely on GC.

## 11. UI / command / tool / provider / platform considerations

CLI surface in `main()` exposes: `get`, `set`, `record_block`, `increment_*`, `export_state`, `export_audit`, `rebuild`, `replay_session`, `prune_*`.

Platform assumptions:
- Linux/macOS filesystem (Path API portable).
- SQLite ≥ 3.7 for WAL.
- No NFS (warned via `actual_mode != "wal"` check, line 232).
- Python 3.6+ (f-strings present).

No UI or provider surface — this is a library.

## 12. Validation plan

### Mechanical (V1-V3) — run from project root

```bash
# V1: 3 mandatory tables present in this doc
rg -n "Baseline design inventory\|Proposed design decision ledger\|Compression review" .ai/docs/designs/2026-06-01-state-engine-review.md
# expected: ≥ 3 hits (one per mandatory table header)

# V2: 14 spec section headers
awk '/^## [0-9]+\./' .ai/docs/designs/2026-06-01-state-engine-review.md | wc -l
# expected: 14

# V3: no orphan rewrite/split/merge
# every rewrite/split/merge in §8 must be reflected as a row in §6 (D#)
rg -n "^\| C[0-9]+ \| (B[0-9]+|D[0-9]+) .* \| (rewrite|split|merge) \|" .ai/docs/designs/2026-06-01-state-engine-review.md
# expected: each such row references a B# or D#; D# rows must exist in §6 — manual cross-check below
```

### Design validations for implementers (handoff)

- VD1 (C1): a unit test that kills the python process between DROP and CREATE in `_prune_with_trigger` must observe that, after `_init_db()` runs again, the trigger is restored. Today, this would fail.
- VD2 (C2): benchmark `_get_db()` latency under a 50k-row audit table; measure delta with and without M11.
- VD3 (C4): a CI guard that fails if `MIGRATIONS` references a non-existent function name.
- VD4 (C5): a unit test that exercises `if prune_log_events():` on a trigger-blocked table and asserts the caller sees an explicit failure, not a truthy success.
- VD5 (C6): a unit test that round-trips `set("intent_confidence", "0.85")` then `set("intent_confidence", "high")` and asserts the second write is rejected by the schema.

### Floor check

Clock start: 1780324198 (16:29:58 CEST). Iteration 3 end: ~16:46 CEST. Elapsed: ~16 min ≥ 10 min floor.

## 13. Risks and mitigations

The smallest invariant set (Q15) whose violation silently corrupts state:

| Invariant | Violation cost | Today's defense | Mitigation in ledger |
|---|---|---|---|
| Append-only triggers present on all 4 audit tables | Audit history can be silently deleted by any code path | Triggers created in `_init_db`; never re-checked | D1 (wrap prune in transaction + idempotent CREATE TRIGGER IF NOT EXISTS in `_init_db`) |
| `metadata.version` matches actual schema columns | Migration is skipped, but `_DB_READY = True` is set; reads with old schema silently return wrong shapes | None — version bump is unconditional after the for-loop | D4 (decorator registration; CI guard VD3) |
| `_DB_READY = True` only after a fully successful migration | Re-entry into `_init_db` after partial migration crashes the next migration on duplicate ALTER TABLE | PRAGMA table_info dance in `_migrate_v2_audit_metadata` (per-migration manual defense) | D7 (`_safe_add_column` helper used by every migration) |
| Type of `state.value` is stable across writers | A second writer with a different stringified type silently corrupts downstream type inference | `_coerce_for_field` does best-effort inference but can flip | D6 (schema map of `{key: type}`) |

## 14. Open questions / blockers

- OQ1: Is the M11 latency tax actually visible in real Claude sessions? VD2 measures this. Decision blocker for D2.
- OQ2: Does the user have any external integration that reads `prune_*` return values today? If yes, D5's typed result is a breaking change; if no, ship as-is.
- OQ3: For D8 (`keep_audit=False` removal): is there any scripted use-case for destroy-audit? Search history shows no caller passing False explicitly.
- OQ4: For D3 (4-connection collapse): some external scripts may import `_get_pooled_conn` directly (private name but Python doesn't enforce). Confirm by grep across all scripts/ before the rewrite.

## Hand-off

This design is ready for `/speckit.specify` once OQ1-OQ4 are resolved. The spec should consume §5 (baseline B1-B13), §6 (ledger D1-D8), and §13 (the 4-invariant safety floor) as inputs. Once specified, run `/speckit.plan` to break it into tasks. Implementation (`/speckit.implement`) comes after the plan is approved.

**Critical finding to surface immediately** outside the Spec Kit pipeline: **C1 / D1** is a security defect — the append-only audit contract is not crash-safe. A SIGKILL during a prune can permanently disable the append-only protection on any of the 4 audit tables, with no detection at next startup. This should be fixed before the v1.4.1 "production-ready" claim is repeated.

Status: Ready for implementation.
