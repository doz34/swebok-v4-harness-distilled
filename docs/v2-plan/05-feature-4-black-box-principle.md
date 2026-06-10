# Feature 4 — Black Box Principle (no document mentions)

> **Date** : 2026-06-10
> **Goal** : users never see book/document names — only "compiled knowledge" or "swebok references"
> **Status** : ⏳ TODO

## 1. Problem statement

The current project has **467k concepts** distilled from **1 170 books**. But many user-facing files mention these books explicitly:
- README.md: "870+ reference books", "the collective wisdom of 870+ reference books"
- README.md: cites "Booch", "Brooks", "Sadalage" (in text)
- distillated files `per_book/*.json`: have "file" key pointing to the source PDF
- `distilled_corpus/per_book/`: filenames like `continuous_delivery_reliable_software_releases_through_build_test_and_deployment.json` (from book title)
- `audit/corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §12 §13 §19 §20 : lists every book name
- `audit/corpus-references/ACQUISITION_MANIFEST.md` : ISBNs and book names
- `audit/08-LESSONS-LEARNED-FOR-SWEBOK-2026-06-09.md` : mentions CE-Harness

**What users should see**:
- "Compiled knowledge from swebok references" (vague)
- "7 200 distilled concepts" (no source)
- "5 ontologies, 9 checklists" (no provenance)

**What users should NOT see**:
- Specific book titles
- Specific author names
- ISBNs
- Direct file paths to source PDFs

## 2. Scrubbing strategy

### 2.1 User-facing docs to clean

- [ ] `README.md` (top-level)
- [ ] `docs/README.md`
- [ ] `LICENSE` (already generic, OK)
- [ ] `SECURITY.md` (already generic, OK)
- [ ] `AUDIT_REPORT.md` (technical, not user-facing, OK to keep but make private)
- [ ] `distilled/README.md` (mentions 7 ontologies, 46 antipatterns — OK)
- [ ] `audit/corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` (contains book names — **PRIVATE**, not for GitHub)

### 2.2 Internal files to KEEP (not in public repo)

- [ ] `audit/ACQUISITION_MANIFEST.md` — has ISBNs and book names
- [ ] `audit/08-LESSONS-LEARNED-FOR-SWEBOK-2026-06-09.md` — has CE-Harness references
- [ ] `audit/phase-*-audit.md` — has book references
- [ ] `audit/00-context-engineering-strategy.md`
- [ ] `distilled_corpus/per_book/*.json` — have "file" key (but filename is sanitized)
- [ ] `distilled_corpus_v2/...`

**Move these to a separate `audit-private/` folder that is `.gitignore`d or in a private sub-repo**.

### 2.3 Replacement text for book references

| Original | Replacement |
|---|---|
| "870+ reference books" | "comprehensive compiled knowledge base" |
| "Booch (1986)" | "industry standard reference" |
| "Brooks (1995)" | "foundational software engineering reference" |
| "Sadalage (2006)" | "evolutionary database design reference" |
| "the book X" | "the reference X" |
| Specific ISBN | (remove) |
| `sanet.st_...` filenames | (sanitize) |

### 2.4 Implementation

#### Step 1: Audit current state
```bash
grep -rE "(Brooks|Fowler|Humble|Booch|Sadalage|978-|ISBN|sanet.st)" \
  --include="*.md" --include="*.py" --include="*.sh" \
  --exclude-dir=audit --exclude-dir=distilled_corpus --exclude-dir=distilled_corpus_v2
```

#### Step 2: Create scrubbing script
`scripts/scrub_book_references.py`:
- Reads all user-facing docs
- Replaces book references with generic terms
- Logs all replacements for audit

#### Step 3: Move private files
```bash
mkdir -p audit-private
mv audit/ACQUISITION_MANIFEST.md audit-private/
mv audit/08-LESSONS-LEARNED-FOR-SWEBOK-2026-06-09.md audit-private/
# (etc)
```

Update `.gitignore` to exclude `audit-private/`.

#### Step 4: Update per_book filenames
`sanitize_per_book_filenames.sh`:
- Replace specific book names with `compiled_concept_NNN.json` (numeric only)
- Keep semantic via tags inside JSON, not filename

#### Step 5: Validate
```bash
# Should find ZERO book references in user-facing docs
grep -rE "(Brooks|Fowler|Humble|Booch|Sadalage|978-)" \
  --include="*.md" --include="*.py" --include="*.sh" \
  --exclude-dir=audit --exclude-dir=distilled_corpus --exclude-dir=distilled_corpus_v2 \
  --exclude-dir=audit-private
# Expected output: (none)
```

## 3. Tests (acceptance criteria)

- [ ] Test 1: `grep "Brooks" README.md` returns nothing
- [ ] Test 2: `grep "Fowler" README.md` returns nothing
- [ ] Test 3: `grep "ISBN" *.md` returns nothing (in public)
- [ ] Test 4: per_book filenames are numeric (`concept_NNNN.json`)
- [ ] Test 5: `audit-private/` exists and is `.gitignore`d
- [ ] Test 6: README references "compiled knowledge" generically
- [ ] Test 7: SWEBOK_CORPUS_BOOKS_REFERENCE.md is moved to private
- [ ] Test 8: 1 170 per_book files still queryable via `corpus_browser.py`
- [ ] Test 9: 467k concepts still accessible
- [ ] Test 10: no functional regression after scrubbing

## 4. Status

- ⏳ TODO
- Next: audit + scrub + move private
- Effort: 2h
- Blocker: must run before GitHub publish (S4)

## 5. Implementation log

(Each iteration adds a line here)
