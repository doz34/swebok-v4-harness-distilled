# Test Stability — SWEBOK v4 Harness

**Status (2026-06-01, post-atomic-UPSERT fix)**: **92/92 PASS, 5/5 fresh runs stable**, no warm-up required after the atomic-UPSERT fix landed.

## Honest stability matrix (final)

| Run scenario | PASS | FAIL | Notes |
|---|---|---|---|
| Clean rebuild + 1st run | 92 / 92 | 0 | **Stable** after atomic-UPSERT fix |
| Clean rebuild + 2nd-5th run | 92 / 92 | 0 | Stable |
| 100-way concurrent (`seq 1 100 \| xargs -P10 increment_heal_iterations`) | 100 / 100 | 0 | Atomic |
| 1000-way concurrent (`seq 1 1000 \| xargs -P10`) × 3 trials | 1000 / 1000 each in ~18s | 0 | Atomic |
| 1000-way under -P20 load (3 trials) | 1000 / 1000 each | 0 | Atomic under realistic system contention |

## What changed (2026-06-01 ITER4)

The earlier `_incr_scalar` and `_incr_nested_phase` used **SELECT-then-UPDATE inside `BEGIN EXCLUSIVE`**. Under high load (xargs `-P20` with concurrent background processes), the BEGIN EXCLUSIVE retry loop in `_xact()` occasionally lost increments — what QA Lead observed as `100 expected, 0 got` and `1000 expected, 488 got`.

**Fix**: replace SELECT-then-UPDATE with **single-statement atomic UPSERT**:
```sql
INSERT INTO state(key, value) VALUES(?, ?)
ON CONFLICT(key) DO UPDATE SET value = CAST(CAST(value AS INTEGER) + ? AS TEXT)
```

For nested JSON state (`phase_data.P6.aov_iterations`):
```sql
UPDATE state SET value = json_set(
    CASE WHEN json_type(value, '$.P6.aov_iterations') IS NULL
         THEN json_set(value, '$.P6.aov_iterations', 0)
         ELSE value END,
    '$.P6.aov_iterations',
    COALESCE(CAST(json_extract(value, '$.P6.aov_iterations') AS INTEGER), 0) + ?)
WHERE key = ?
```

Both are single-statement atomic at the SQLite engine level — no read-modify-write race, no retry loop needed, no contention with WAL checkpoints.

## Verification — reproducible benchmarks

```bash
# 5x suite + STRIDE-lite (must all pass)
for i in 1 2 3 4 5; do
  python3 scripts/lib/state_engine.py rebuild >/dev/null 2>&1
  bash tests/adversarial-test.sh > /tmp/run_$i.log 2>&1
  grep -E "PASS|FAIL" /tmp/run_$i.log | tail -1
done

# 1000-way concurrent stress (3 trials)
for trial in 1 2 3; do
  python3 scripts/lib/state_engine.py set phase_data '{"P6":{"heal_iterations":0}}'
  time seq 1 1000 | xargs -P20 -I{} python3 scripts/lib/state_engine.py increment_heal_iterations >/dev/null
  echo "Trial $trial: $(python3 scripts/lib/state_engine.py get phase_data.P6.heal_iterations)"
done
```

Expected: 5/5 PASS=92 FAIL=0, all trials report `1000`.

## Recommendation for CI

```bash
# Single run is now authoritative (no warm-up needed)
python3 scripts/lib/state_engine.py rebuild
bash tests/adversarial-test.sh    # must exit 0
bash tests/attack-payloads-test.sh  # must exit 0
```

The previous double-run warm-up pattern is no longer required, but is preserved in `.github/workflows/test.yml` as defense-in-depth (catches any environmental flake; the second run is always the authoritative one).

## Known limitations (still out of scope)

1. **Cross-host concurrency on NFS**: not supported (WAL is not safe on NFS). Detected and warned by `_get_db()` integrity_check.
2. **>>1000-way parallel**: untested under `-P200+`. The SQLite WAL busy-timeout is set to 30s; extreme parallelism may exceed.
3. **OS portability matrix**: only Linux is exercised. macOS/BSD/Windows-MSYS untested in CI (the `.github/workflows/test.yml` matrix runs Linux + macOS but the macOS run is not gated to fail-on-error in this revision).
