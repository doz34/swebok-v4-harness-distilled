# swebok v2 Plan State

**Last update** : 2026-06-10 (session S1)
**Current sprint** : S2 (auto-trigger harness)
**Status** : 🚧 In progress

## Done

- ✅ **S0 (Sprint 0, 2026-06-09)** : Adversarial loop MVP
  - `lib/adv-loop/stop_conditions.py` (95 lines)
  - `lib/adv-loop/feedback.py` (306 lines)
  - `lib/adv-loop/loop_orchestrator.py` (140 lines)
  - `bin/adv-loop` (130 lines)
  - 3 useful patterns: P0, P5, P7
  - 8 stub patterns: P1, P2, P3, P4, P6, P8, P9, P10
  - 11 specs validated to 🟢 OK
  - 5 self-tests pass
- ✅ **S1 (Sprint 1, 2026-06-10)** : Inventory + Gap analysis
  - Local skills/tools inventoried (57 skills, 13 commands, 4 MCPs)
  - Gap analysis vs user requirements done
  - Plan documents created (8 docs in `docs/v2-plan/`)
  - Skills-to-phases mapping drafted

## In progress

- 🚧 **S2 (Sprint 2)** : Auto-trigger harness
  - ⏳ `02-feature-1-auto-trigger.md` — not started

## TODO

- ⏳ **S3 (Sprint 3)** : Modular phases + Adversarial patterns
  - ⏳ `03-feature-2-modular-phases.md`
  - ⏳ `04-feature-3-adversarial-harness.md` (8 remaining patterns)
- ⏳ **S4 (Sprint 4)** : Black-box + GitHub publish
  - ⏳ `05-feature-4-black-box-principle.md`
  - ⏳ `06-feature-5-github-publish.md`
- ⏳ **S5 (Sprint 5)** : Skills mapping + Iteration protocol
  - ⏳ `07-feature-6-skills-mapping.md`
  - ⏳ `08-iteration-protocol.md` (this doc)

## Open questions

- Q1: How to handle the 50+ "nexus-*" agents? (Some are subagent_type, some are skills, some are slash commands — overlap is unclear)
- Q2: Where to put the v2 in the existing `v1/` documentation structure? (v2/ is empty)
- Q3: Should `intent-detector.py` be replaced or extended? (Current implementation works but not tested)
- Q4: How to handle the 1 170 per_book files in a "black box" way without losing queryability?

## Last 5 commits (relevant to v2 plan)

```
[TBD - will be filled at end of S2]
```

## Files modified (S0-S1)

- `lib/adv-loop/stop_conditions.py` (new, 95 lines)
- `lib/adv-loop/feedback.py` (new, 306 lines)
- `lib/adv-loop/loop_orchestrator.py` (new, 140 lines)
- `bin/adv-loop` (new, 130 lines)
- `specs/adversarial-patterns/phase-0-discovery.sh` (new)
- `specs/adversarial-patterns/phase-5-implementation.sh` (new)
- `specs/adversarial-patterns/phase-7-deployment.sh` (new)
- `specs/adversarial-patterns/README.md` (new)
- `docs/v2-plan/00-INDEX.md` (new)
- `docs/v2-plan/01-inventory-and-gap-analysis.md` (new)
- `docs/v2-plan/02-feature-1-auto-trigger.md` (new)
- `docs/v2-plan/03-feature-2-modular-phases.md` (new)
- `docs/v2-plan/04-feature-3-adversarial-harness.md` (new)
- `docs/v2-plan/05-feature-4-black-box-principle.md` (new)
- `docs/v2-plan/06-feature-5-github-publish.md` (new)
- `docs/v2-plan/07-feature-6-skills-mapping.md` (new)
- `docs/v2-plan/08-iteration-protocol.md` (new)
- `docs/v2-plan/STATE.md` (this file)

## Next session

If you are a **fresh Claude Code session** starting work on swebok v2:

1. Read `docs/v2-plan/00-INDEX.md` (orientation)
2. Read this file (`docs/v2-plan/STATE.md`) — current state
3. Read the latest HANDOFF-*.md (last session's notes)
4. Read the latest sprint's plan (e.g. `02-feature-1-auto-trigger.md`)
5. Execute the tasks
6. Update this file (`STATE.md`)
7. Create new HANDOFF-*.md
8. Commit
