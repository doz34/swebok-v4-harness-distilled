# Feature 5 — GitHub Publish (delete obsolete, English docs)

> **Date** : 2026-06-10
> **Goal** : delete obsolete v1.5.x tags, publish v2.0 with English docs
> **Status** : ⏳ TODO

## 1. Problem statement

Current published tags on GitHub:
- `v1.5.4`, `v1.5.5`, `v1.5.6`, `v1.5.7`, `v1.5.8`, `v1.5.9`, `v1.5.10`, `v1.5.11`
- `v2.0.0-audit-complete` (only audit, not full v2.0)

**User requirements**:
1. **Delete obsolete versions** (v1.5.x) — replace with v2.0
2. **All docs in English** — currently `docs/v1/ARCHITECTURE.md` and others are FR-mixed
3. **Extremely well documented** — README + per-feature docs + CHANGELOG + examples

## 2. Plan

### 2.1 Phase A: Documentation audit (English-first)

Audit and translate to English:
- [ ] `README.md` (already EN — verify)
- [ ] `docs/v1/ARCHITECTURE.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/PHASES.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/HOOKS.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/OPERATIONS.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/AUDIT_CYCLE.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/EVIDENCE_LEDGER.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/THREAT_MODEL.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/ADVERSARIAL.md` (FR-mixed) → translate to EN
- [ ] `docs/v1/ADR-*.md` (FR-mixed) → translate to EN
- [ ] `audit/phase-*-audit.md` (FR-mixed) → translate to EN
- [ ] `audit/00-context-engineering-strategy.md` (FR-mixed) → translate to EN
- [ ] `audit/01-context-engineering-research-2026.md` (FR-mixed) → translate to EN
- [ ] `CLAUDE.md` (FR-mixed) → translate to EN
- [ ] `workflows/WORKFLOWS-SPEC.md` (FR-mixed) → translate to EN
- [ ] `CHANGELOG.md` (already EN) → verify
- [ ] `SECURITY.md` (already EN) → verify
- [ ] `UNINSTALL.md` (verify EN)
- [ ] `LICENSE` (verify EN)

### 2.2 Phase B: Black-box scrub (per Feature 4)

Per `05-feature-4-black-box-principle.md`:
- Remove all book/author references from user-facing docs
- Move private files to `audit-private/`
- Sanitize per_book filenames

### 2.3 Phase C: Git operations

```bash
# 1. Create v2 branch
git checkout -b v2.0

# 2. Move old tags (don't delete, mark superseded)
git tag v1.5.4-archived v1.5.4
git tag v1.5.5-archived v1.5.5
# ... (etc for v1.5.6 through v1.5.11)
git push origin --tags

# 3. Update README with v2 badge
# (modify README.md)

# 4. Commit v2
git add .
git commit -m "v2.0: per-phase modular, black-box, adversarial harness, English docs"
git tag v2.0
git push origin v2.0
git push origin v2.0

# 5. Create GitHub release
gh release create v2.0 --title "v2.0: Modular Phase Harness" --notes-file RELEASE-NOTES-v2.0.md
```

### 2.4 Phase D: Release notes

`RELEASE-NOTES-v2.0.md`:
```markdown
# v2.0 — Modular Phase Harness

## New in v2.0
- Per-phase modular CLI (`bin/phase N`)
- Auto-trigger from user prompt (`bin/auto-trigger`)
- Per-phase adversarial harness (11 patterns, all phases)
- Black-box principle (no book references in public docs)
- English-only documentation
- 467k concepts, 95% coverage

## Breaking changes from v1.5.x
- Old audit/ folder moved to audit-private/
- Per-book filenames are now numeric (concept_NNNN.json)
- State DB is per-phase (.swebok_state_pN.db)

## Migration
$ bin/phase migrate --from v1.5.11
```

### 2.5 Phase E: README rewrite (English, comprehensive)

`README.md` new structure:
1. **What is it?** (one paragraph)
2. **Quick start** (5 steps)
3. **Modular phases** (table of 11 phases)
4. **Auto-trigger** (example)
5. **Adversarial harness** (example)
6. **Compiling** (how to add your own compiled knowledge)
7. **Testing** (`bin/adv-loop test`)
8. **MCP integration** (zai, zread, web-reader)
9. **Contributing** (how to add a phase)
10. **License** (MIT)

## 3. Tests (acceptance criteria)

- [ ] Test 1: `git tag -l` shows v1.5.x-archived + v2.0
- [ ] Test 2: README is 100% English
- [ ] Test 3: All `docs/v1/` files are 100% English
- [ ] Test 4: All `audit/phase-*-audit.md` files are 100% English
- [ ] Test 5: GitHub release v2.0 created
- [ ] Test 6: All book references scrubbed from public docs
- [ ] Test 7: per_book filenames are numeric
- [ ] Test 8: `audit-private/` is gitignored
- [ ] Test 9: GitHub Actions CI passes on v2.0
- [ ] Test 10: Clone + install + run works on fresh machine

## 4. Status

- ⏳ TODO
- Next: Phase A (English audit)
- Effort: 2h
- Blocker: depends on S4 (black-box)

## 5. Implementation log

(Each iteration adds a line here)
