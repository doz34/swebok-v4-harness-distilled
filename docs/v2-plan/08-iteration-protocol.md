# Iteration Protocol — Continue in fresh Claude Code sessions

> **Date** : 2026-06-10
> **Goal** : allow continuation in fresh Claude Code sessions with new context
> **Status** : ⏳ TODO

## 1. Problem statement

The swebok v2 plan is large (8 sprints, ~14h of work). A single Claude Code session:
- Has limited context window
- Gets fatigued on long sessions
- Loses nuance on complex multi-step plans

**Solution** : structured hand-off protocol so each fresh session:
1. Reads the current state
2. Picks up exactly where the last left off
3. Updates the state
4. Hands off to the next session

## 2. Protocol

### 2.1 State management (3 files)

**File 1: `docs/v2-plan/STATE.md`** (single source of truth)
```markdown
# swebok v2 plan state

**Last update** : 2026-06-10 18h30
**Current sprint** : S1
**Status** : ⏳ TODO

## Done
- ✅ S0 (Sprint 0) : adversarial loop MVP, 3 patterns (P0, P5, P7)
- ✅ S1 (Sprint 1) : inventory + gap analysis

## In progress
- 🚧 S2 (Sprint 2) : auto-trigger harness
  - ⏳ 02-feature-1-auto-trigger.md — not started

## TODO
- ⏳ S3, S4, S5

## Open questions
- Q1: How to handle the 50+ "nexus-*" agents? (Some are subagents_type, some are skills)

## Last 5 commits (relevant)
- abc1234 (S1) : docs/v2-plan/01-inventory-and-gap-analysis.md
- def5678 (S0) : lib/adv-loop/* + bin/adv-loop
- ghi9012 (S0) : specs/adversarial-patterns/{phase-0,phase-5,phase-7}-*.sh
```

**File 2: `docs/v2-plan/00-INDEX.md`** (navigation, see this first)
**File 3: `docs/v2-plan/HANDOFF-<date>-<sprint>.md`** (per-session handoff)

### 2.2 Session start protocol

When starting a new Claude Code session to work on swebok v2:

```
1. Read docs/v2-plan/00-INDEX.md (orientation)
2. Read docs/v2-plan/STATE.md (current state)
3. Read the latest HANDOFF-*.md (last session's notes)
4. Read the latest sprint's plan (e.g. docs/v2-plan/02-feature-1-auto-trigger.md)
5. Execute the tasks
6. Update docs/v2-plan/STATE.md
7. Create new HANDOFF-<date>-<sprint>.md
8. Commit
```

### 2.3 Session end protocol

When ending a Claude Code session on swebok v2:

```
1. Update docs/v2-plan/STATE.md
   - Mark done/in-progress/TODO
   - Note any open questions
2. Create docs/v2-plan/HANDOFF-<date>-<sprint>.md
3. Commit
4. (optional) Tag as WIP-<sprint>
```

### 2.4 HANDOFF template

`docs/v2-plan/HANDOFF-<date>-<sprint>.md`:

```markdown
# Handoff — 2026-06-10 (Sprint 2)

## Session
- Date : 2026-06-10
- Time : 18h30 → 20h15
- Focus : Auto-trigger harness (S2)

## Done
- ✅ Created `lib/auto trigger.py` (200 lines)
- ✅ Created `bin/auto-trigger` (50 lines)
- ✅ Created `pre-tool-use/auto-trigger-hook.sh` (30 lines)
- ✅ Tests 1-5 pass

## In progress
- 🚧 Test 6 (latency benchmark)

## TODO
- ⏳ Test 7 (offline mode)
- ⏳ Update `intent-map.json` with manual override patterns
- ⏳ Update `CLAUDE.md` to reference `bin/auto-trigger`

## Open questions
- Q1: How to handle the 50+ "nexus-*" agents?

## Files modified
- `lib/auto trigger.py` (created, 200 lines)
- `bin/auto-trigger` (created, 50 lines)
- `pre-tool-use/auto-trigger-hook.sh` (created, 30 lines)
- `tests/test_auto_trigger.py` (created, 80 lines)

## Commit
- abc1234 (S2) : lib/auto trigger.py + bin/auto-trigger + tests
```

## 3. Implementation

### 3.1 Files to create

- [ ] `docs/v2-plan/STATE.md` (new)
- [ ] `docs/v2-plan/HANDOFF-2026-06-10-S1.md` (new, example)
- [ ] `scripts/state_update.sh` (new) — helper to update STATE.md

### 3.2 Update CLAUDE.md to reference the protocol

Add to CLAUDE.md:
```markdown
## v2 Plan State
- Read docs/v2-plan/00-INDEX.md
- Update docs/v2-plan/STATE.md at end of session
- Create HANDOFF-<date>-<sprint>.md
```

## 4. Tests (acceptance criteria)

- [ ] Test 1: STATE.md exists and is up-to-date
- [ ] Test 2: 00-INDEX.md is the entry point
- [ ] Test 3: HANDOFF-*.md pattern works
- [ ] Test 4: scripts/state_update.sh works
- [ ] Test 5: CLAUDE.md references v2 plan
- [ ] Test 6: cross-session continuity verified
- [ ] Test 7: no context loss between sessions
- [ ] Test 8: easy to resume from any state
- [ ] Test 9: git history of STATE.md shows clear progression
- [ ] Test 10: works for new maintainer (not just me)

## 5. Status

- ⏳ TODO
- Next: create STATE.md and HANDOFF-2026-06-10-S1.md
- Effort: 1h

## 6. Implementation log

(Each iteration adds a line here)
