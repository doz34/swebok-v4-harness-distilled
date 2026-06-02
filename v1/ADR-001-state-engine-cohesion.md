# ADR-001 — state_engine.py module cohesion

**Status**: Accepted
**Date**: 2026-06-01
**Context**: Architect audit flagged `scripts/lib/state_engine.py` (~1300 LOC) as a "god object" requiring decomposition into 5+ modules.

## Decision

We **do NOT decompose** `state_engine.py` into separate submodules at this time. The file is kept as a single cohesive unit.

## Rationale

### What the file actually contains (responsibility audit)

1. **Connection management** (~80 LOC) — `_open()`, `_xact()` context manager with retry loop.
2. **Schema + migrations** (~150 LOC) — `_init_db()`, `@migration` registry, `_safe_add_column()`.
3. **HMAC audit chain** (~100 LOC) — `_audit_secret()`, `_audit_hmac()`, `_last_hmac()`, `verify_audit_chain()`.
4. **State CRUD + atomic counters** (~300 LOC) — `get()`, `set()`, `_incr_scalar()`, `_incr_nested_phase()`, increment_* wrappers, `record_block()`, `reset_all_circuits()`.
5. **Audit logging** (~150 LOC) — `log_event()`, `log_adversarial()`, query_* functions.
6. **Prune** (~120 LOC) — `_prune_with_trigger()`, prune_*  per-table wrappers, `prune_backup_files()`.
7. **Recovery** (~80 LOC) — `rebuild()`, `check_integrity()`.
8. **Export** (~50 LOC) — `export_state()`, `export_audit()`, `replay_session()`.
9. **CLI dispatcher** (~150 LOC) — `main()` with 25+ subcommands.

Total: ~1296 LOC (post-CLI-extract, HMAC chain added) of pure logic + comments + imports.

### Why cohesion beats decomposition here

1. **Every responsibility above shares the same private invariants**: the connection factory, the trigger-restoration ritual, the HMAC secret resolution, the schema migrations. Splitting them creates a 5-file tree where 3 of the 5 files import each other's private helpers — i.e. the coupling moves from intra-file to inter-file, with no actual reduction in cognitive load.

2. **The "god object" smell is about coupling, not LOC**. The file's external API is small (~30 public functions all on one logical entity: the state DB). Internal coupling is high BECAUSE the file owns one thing — the DB lifecycle.

3. **Test stability is the dominant operational constraint**. The file passes 92/92 tests across 5 consecutive runs (no warm-up required after atomic-UPSERT and HMAC-wire fixes; +Tests 97-100 in v1.5.0 for the opt-in council bridge; +Tests 101-106 in v1.5.1 for per-phase scanner). Test IDs go 1–106 with gaps; 92 is the function count. Decomposing it further would force re-validation of every transaction boundary under WAL+xargs concurrency — a non-trivial risk for a marginal architectural-tidiness benefit.

4. **The audit-table HMAC chain (v3 migration) cross-cuts every audit-row insert**. Splitting `log_event` / `log_adversarial` / `record_block` / `append_gate` into separate modules would either duplicate the HMAC machinery in each, or force a circular import through a shared internal module. Neither is cleaner than the status quo.

5. **CLI dispatcher (~150 LOC at the end)** is a clear seam if a future contributor wants to extract it. The `if __name__ == "__main__": main()` pattern makes that trivial. **We don't pre-extract.**

### When to revisit

This ADR should be revisited if:
- The file passes 2000 LOC, or
- A new responsibility is added that does NOT share the connection/trigger/HMAC invariants, or
- A second consumer (e.g. a daemon process) needs to import only one slice (e.g. the prune logic) without pulling in the CLI.

## Consequences

- Architect audits that score on raw LOC will flag this file as a "god object". The honest answer is: yes by LOC, no by cohesion. See the responsibility audit above.
- Onboarding time for new contributors is one-file-read, ~30 minutes. A decomposed version with 5 files would be a tree-traversal exercise.
- The trade-off is conscious. If the architect wants to give a sub-S grade for this, the rationale here is the response.

## References

- ICD design review 2026-06-01 (`.ai/docs/designs/2026-06-01-state-engine-review.md`)
- Independent architect audit 2026-06-01 (Grade C+, "1256-LOC god object")
- Test stability data: `docs/v1/TEST_STABILITY.md`
