# SWEBOK v4 Harness v2 — Plan Index

> **Date** : 2026-06-10
> **Status** : DRAFT (in progress)
> **Owner** : maintainer
> **Goal** : build the v2 harness that satisfies the 7 user requirements

## User Requirements (from goal hook)

1. **Auto-trigger** of swebok v4 harness distilled based on user prompt → must be **extremely reliable and efficient**
2. **Modular phases** — each phase independently usable per user needs
3. **Elaborate adversarial harness** per phase — serene and reliable validation of each phase's assertions
4. **No document mentions** (except swebok + scientific papers) — book sources = **black box** for users
5. **GitHub publish** — delete obsolete v1.5.x tags, document **in English**, replace with v2
6. **Exhaustive listing of local Claude Code skills/tools** — done (see §1)
7. **Structured plan** in .md documents for iterative work — **this file**
8. **Each concept must be implemented** and functional in the project

## Plan Documents

| # | Document | Purpose | Status |
|---|---|---|---|
| 00 | **00-INDEX.md** (this) | Overview, navigation, status | ✅ |
| 01 | [01-inventory-and-gap-analysis.md](./01-inventory-and-gap-analysis.md) | Exhaustive list of local skills/tools + gap analysis | ⏳ TODO |
| 02 | [02-feature-1-auto-trigger.md](./02-feature-1-auto-trigger.md) | Auto-trigger harness from user prompt | ⏳ TODO |
| 03 | [03-feature-2-modular-phases.md](./03-feature-2-modular-phases.md) | Each phase as standalone module | ⏳ TODO |
| 04 | [04-feature-3-adversarial-harness.md](./04-feature-3-adversarial-harness.md) | Per-phase adversarial validation | ⏳ TODO |
| 05 | [05-feature-4-black-box-principle.md](./05-feature-4-black-box-principle.md) | Remove book/document references from user-facing | ⏳ TODO |
| 06 | [06-feature-5-github-publish.md](./06-feature-5-github-publish.md) | Delete obsolete tags, publish v2, English docs | ⏳ TODO |
| 07 | [07-feature-6-skills-mapping.md](./07-feature-6-skills-mapping.md) | Map local skills to phases (one per phase) | ⏳ TODO |
| 08 | [08-iteration-protocol.md](./08-iteration-protocol.md) | How to continue in fresh Claude Code sessions | ⏳ TODO |

## Execution Order

| Sprint | Tasks | Effort | Blocks |
|---|---|---|---|
| **S1** | 01 (inventory + gap) | 30 min | All others |
| **S2** | 02 (auto-trigger) + 07 (skills mapping) | 4 h | Core |
| **S3** | 03 (modular phases) + 04 (adversarial) | 6 h | Quality |
| **S4** | 05 (black-box) + 06 (GitHub publish) | 2 h | Ship |
| **S5** | 08 (iteration protocol) | 1 h | Continuity |

**Total** : ~14 h over 2-3 working days

## Quick Start (for new Claude Code session)

If you are a **fresh Claude Code session** and want to continue this work:

1. Read this file (`docs/v2-plan/00-INDEX.md`)
2. Read `08-iteration-protocol.md` for state continuity
3. Read the latest sprint's plan (e.g. `02-feature-1-auto-trigger.md`)
4. Execute the tasks in that document
5. Update the status at the bottom of the document
6. Commit

## Status Legend

- ✅ Done
- ⏳ TODO (in plan)
- 🚧 In progress
- ❌ Blocked
