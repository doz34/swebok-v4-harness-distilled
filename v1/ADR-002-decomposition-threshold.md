# ADR-002 — state_engine.py decomposition threshold rule

**Status**: Accepted
**Date**: 2026-06-02
**Context**: ADR-001 defended `scripts/lib/state_engine.py` as a single cohesive module despite its size (currently ~1480 LOC). Architect ITER8 audit (Grade A+) noted that "1480 LOC for a single cohesive unit sits at the edge of what most style guides accept" and asked for an explicit threshold rule so future contributors inherit a clear policy.

## Decision

**Decomposition trigger** — when ANY of the following conditions is true, file MUST be split into focused modules:

1. **LOC ceiling**: file exceeds **1800 LOC** of pure logic (comments and imports excluded).
2. **Responsibility creep**: file gains a new top-level responsibility that does NOT share the connection factory, the `_xact()` retry semantic, the audit-trigger contract, or the HMAC chain. (Today the 9 responsibility buckets all share these invariants; adding e.g. a "GitHub API client" or a "report generator" would be a new bucket.)
3. **External dependency creep**: file gains a third unrelated external-dependency group (current groups: stdlib only, with sqlite3 and hmac being the boundaries). Adding e.g. `requests` + `pyyaml` + `boto3` would trip this.
4. **Test-cycle creep**: ≥ 2 successive iterations show transaction-boundary regressions traceable to the file's growth (not to a specific function bug).

If NONE of the four triggers, the cohesion-over-decomposition argument from ADR-001 stands.

## Decomposition shape (when triggered)

The CLI dispatcher is the documented seam (already extracted to `state_engine_cli.py` in ITER6). The next seams, in order of safety:

| Seam | LOC saved | Risk | Notes |
|---|---|---|---|
| `recovery.py` (rebuild, check_integrity, export_*, replay_session) | ~150 | Low | Pure read paths + one renaming write; no audit-write invariants |
| `prune.py` (`_prune_with_trigger`, prune_*) | ~120 | Low-Med | Calls `recompute_audit_chain` — keep that import explicit |
| `audit.py` (`log_event`, `log_adversarial`, `record_block`, query_*) | ~250 | Med | Cross-cuts HMAC chain — must import `_audit_hmac`/`_last_hmac` |
| `counters.py` (`_incr_scalar`, `_incr_nested_phase`, increment_*) | ~150 | Med | Touches `set_intent`, `should_run_continuity` — keep tight |
| `schema.py` (`_init_db`, migrations, `_ensure_triggers`) | ~200 | High | Bootstrap order matters; extract last |

State CRUD (`get`, `set`) and the connection factory (`_open`, `_xact`) stay in the entry-point module — they are the shared invariants.

## Consequences

- Future contributors have a measurable trigger ("did I cross 1800 LOC?") rather than a subjective "this feels too big".
- The named seams are pre-prioritised by safety, so extraction can land incrementally without a big-bang refactor.
- This ADR is a forward contract — until a trigger fires, file remains intact; when one fires, the next seam in the order above is the first to extract.

## References

- ADR-001 (cohesion-vs-decomposition; LOC drift acknowledged)
- Architect ITER8 audit (Grade A+; noted threshold rule was missing)
- ICD design review 2026-06-01 (`.ai/docs/designs/2026-06-01-state-engine-review.md`)
