# Feature 2 — Modular Phases

> **Date** : 2026-06-10
> **Goal** : each phase independently usable per user needs
> **Status** : 🚧 In progress

## 1. Problem statement

The swebok v4 harness currently has **11 phases** in `specs/workflows/by-phase/phase-N-*.md`. The hook system enforces phase transitions via `pre-tool-use/phase-guard.sh`. But:

- **No CLI entry point per phase** — user can't say "I want to use P5 only"
- **No per-phase state isolation** — all phases share `.swebok_state.db`
- **No per-phase prompt template** — user must read full spec
- **No per-phase validation gate** — the only gate is `adversarial-gate.sh` (general)

## 2. Design (v2)

### 2.1 New CLI: `bin/phase N [subcommand]`

```bash
$ bin/phase 0                           # Enter P0 (Discovery)
$ bin/phase 0 start                    # Same as above
$ bin/phase 0 status                   # Show P0 status
$ bin/phase 0 validate                 # Run P0 adversarial loop
$ bin/phase 0 close                    # Mark P0 done, transition to P1
$ bin/phase list                        # List all 11 phases
```

### 2.2 Per-phase prompt template: `bin/phase N prompt`

```bash
$ bin/phase 0 prompt
=== Phase 0: Discovery ===
Mission: Cadrer un projet en produisant 7 livrables actionnables
Budget: 35 min | 4k/7k/10k tokens
Sequential mode, 4 agents, 1 at a time
Output: 7 deliverables (charter.md, context_map.md, ...)
```

### 2.3 Per-phase state isolation: `bin/phase N init`

```bash
$ bin/phase 0 init
# Creates .swebok_state_p0.db (per-phase)
# Symlinks to .swebok_state.db if single-phase mode
```

### 2.4 Per-phase validation gate: `bin/phase N validate`

```bash
$ bin/phase 0 validate
# Runs the adversarial pattern for P0
# Returns: P0: verdict=🟢 OK | findings=...
```

## 3. Implementation

### 3.1 Tests (acceptance criteria)

- [ ] Test 1: `bin/phase 0` enters P0 mode
- [ ] Test 2: `bin/phase 5` can be invoked without P0-P4 having been run
- [ ] Test 3: `bin/phase 0 validate` runs the adversarial pattern
- [ ] Test 4: `bin/phase list` shows all 11 phases
- [ ] Test 5: `bin/phase 0 prompt` shows the phase template
- [ ] Test 6: per-phase state is independent (no cross-contamination)
- [ ] Test 7: each phase has its own deliverables checklist
- [ ] Test 8: each phase's exit criteria are validated before close
- [ ] Test 9: works with `bin/adv-loop N` (the new adversarial loop from Sprint S0)
- [ ] Test 10: works offline (no network, no LLM)

### 3.2 Files to create/modify

- [ ] `bin/phase` (new) — main CLI dispatcher
- [ ] `bin/phase-0-discovery` (new) — symlink to `bin/phase 0`
- [ ] `bin/phase-1-feasibility` (new)
- [ ] ... (one per phase)
- [ ] `lib/phase_modular.py` (new) — per-phase state isolation logic
- [ ] `tests/test_phase_modular.sh` (new) — 10+ tests
- [ ] `specs/workflows/by-phase/phase-N-*.md` (modify) — add "Modular CLI" section

## 4. Per-phase deliverables (re-used from specs)

| Phase | Name | Key deliverables | CLI subcommand |
|---|---|---|---|
| 0 | Discovery | 7 (charter, context_map, stakeholders, ...) | `bin/phase 0` |
| 1 | Feasibility | 3 (feasibility_report, roi_analysis, go_no_go_memo) | `bin/phase 1` |
| 2 | Requirements | 4 (srs, user_stories, acceptance_criteria, rtm) | `bin/phase 2` |
| 3 | Architecture | 3 (architecture_doc, adrs, c4) | `bin/phase 3` |
| 4 | Design | 4 (design_doc, api_contracts, data_model, sequences) | `bin/phase 4` |
| 5 | Implementation | 2 (source_code, unit_tests) | `bin/phase 5` |
| 6 | Testing | 4 (test_plan, integration_tests, mutation_report, coverage_report) | `bin/phase 6` |
| 7 | Deployment | 4 (deployment_plan, rollback_plan, release_notes, smoke_tests) | `bin/phase 7` |
| 8 | Operations | 4 (runbooks, slos, on_call_rotation, incident_postmortems) | `bin/phase 8` |
| 9 | Maintenance | 3 (refactoring_plan, tech_debt_register, release_notes) | `bin/phase 9` |
| 10 | Retirement | 4 (retirement_plan, data_archival, user_migration, closure_memo) | `bin/phase 10` |

## 5. Status

- 🚧 In progress
- Next: implement `bin/phase` dispatcher
- Blocker: depends on S1 (inventory)

## 6. Implementation log

```
[2026-06-10] Sprint 3 START. Designing bin/phase dispatcher
[2026-06-10] Drafting per-phase state isolation logic
```

(Each iteration adds a line here)
