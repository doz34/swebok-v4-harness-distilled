# SWEBOK v4 Harness

> A discipline layer for software projects that guides you through the full
> development lifecycle — from the first conversation about what to build, all
> the way to shipping and supporting it in production. It watches your work,
> reminds you of what comes next, and stops you from skipping important steps.

[![Tests](https://img.shields.io/badge/tests-52%2F52%20PASS-brightgreen)](tests/)
[![Knowledge](https://img.shields.io/badge/knowledge-227%20compiled%20items-blue)](distilled/)
[![Corpus](https://img.shields.io/badge/corpus-145%2C963%20concepts%20searchable-orange)](scripts/corpus_browser.py)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## What is it, in plain English?

When you sit down to build something, you usually know roughly what to do:
gather requirements, sketch an architecture, write code, test it, ship it, fix
bugs, eventually retire the project. Most teams skip steps when they're
tired, rushed, or just don't remember. **The SWEBOK v4 Harness is a
discipline layer that holds you to the process.**

It does three things at the same time:

1. **It watches your commands.** When you ask your AI coding assistant to
   write a file or run a shell command, the harness checks whether that
   action makes sense for the current phase. Want to delete files in
   production? Blocked. Want to skip writing tests? Blocked.

2. **It remembers what you've done.** Every action is logged to a tamper-
   evident audit chain. If something goes wrong six months from now, you
   can replay exactly what happened and when.

3. **It carries the collective wisdom of 870+ reference books.** Ask it about
   API design, database choice, security patterns, machine learning
   operations, prompt engineering — and it answers with citations.

The result: you build more carefully, with fewer skipped steps, and you
have a clear record of what you did and why.

---

## Who is this for?

- **Solo developers** who want a "second pair of eyes" on every command.
- **Small teams** that need a consistent SDLC without formal process overhead.
- **AI-assisted workflows** (Claude Code, etc.) where you want guardrails on
  what the assistant can and cannot do without your explicit consent.
- **Anyone** who has shipped software, regretted skipping a step, and wants
  to never do that again.

You do **not** need to be an expert. The harness is opinionated — it makes
choices for you, and you can override them when needed.

---

## Quick start

### What you need

- Linux or macOS
- Python 3.10 or newer
- A Bash shell (Git Bash on Windows is fine)
- 5 minutes

### Install

```bash
git clone https://github.com/doz34/swebok-v4-harness.git
cd swebok-v4-harness
bash install-harness.sh
```

The installer will:

1. Verify the harness is intact (no missing files).
2. Back up your existing Claude Code settings (if any).
3. Merge the harness's hook entries into your `~/.claude/settings.json`.
4. Generate a fresh cryptographic key for the audit chain.
5. Tell you it's done.

### Verify it works

```bash
# Knowledge engine: ask a question
python3 scripts/compiled_knowledge.py "should I use SQL or NoSQL?"

# Knowledge engine: list all 24 universal principles
python3 scripts/compiled_knowledge.py --principle KISS

# Knowledge engine: get a recipe (step-by-step procedure)
python3 scripts/compiled_knowledge.py --recipe api-design

# Knowledge engine: get a phase checklist
python3 scripts/compiled_knowledge.py --checklist P5

# Test suite (should report 32/32 PASS)
bash tests/distilled-test.sh
```

### Use it day-to-day

Once installed, the harness runs automatically when you use Claude Code.
You don't need to invoke it manually. It will:

- **Block** destructive commands at the wrong phase (e.g. `rm -rf` during
  requirements gathering).
- **Remind you** of the current phase's deliverables (e.g. "you should write
  tests before claiming P5 is done").
- **Suggest** the next phase when you've completed the current one.
- **Answer** questions about design, patterns, decisions, and best practices.

---

## What does it actually do?

### Phase gating

Software has phases. The harness enforces them.

| Phase | Name | What you should be doing |
|---|---|---|
| **P1** | Requirements | Talking to stakeholders, writing specs. No code. |
| **P2** | Architecture | Sketching boxes and arrows. Still no code. |
| **P3** | Design | Interface contracts, decision diagrams. |
| **P4** | Estimation | Time, cost, risk. |
| **P5** | Construction | Writing the actual code. |
| **P6** | Verification | Tests, integration, acceptance. |
| **P7** | Deployment | Release artifacts, rollout. |
| **P8** | Maintenance | Bug fixes, patches. |
| **P9** | Retirement | Decommissioning, end-of-life. |

When you try to do something inappropriate for the current phase, the
harness blocks it and tells you why. For example:

- **In P1-P4 (before construction)**: trying to write `.py` files is
  blocked. You should still be thinking, not coding.
- **In P6 (verification)**: modifying `src/` (non-test code) is blocked.
  You should be writing tests, not changing the implementation.
- **In any phase**: `rm -rf /`, `mkfs`, `dd of=/dev/...`, dropping tables,
  and other destructive commands are blocked. Period.

### Safety net for the unexpected

Even outside the phase rules, the harness has your back:

- **`BASH_ENV` injection** is detected and blocked unless the env file is
  a system one (`/etc/profile`, `/etc/bashrc`, etc.).
- **`eval` with base64** is decoded before scanning — `eval "$(echo
  cm0gLXJmIC8= | base64 -d)"` (which decodes to `rm -rf /`) is caught.
- **Three strikes rule**: three blocked operations on the same file
  hard-locks that operation. You have to explicitly override with
  `state_engine.py set circuit_breaker.override_active true`.
- **Audit chain**: every decision (block, allow, override) is logged with
  a cryptographic signature. If anything tries to rewrite history, you'll
  know.

### The compiled knowledge engine

The harness ships with a curated database of 227 items distilled from 870+
software engineering reference books, organized into 7 layers:

1. **Principles** (24) — universal rules like "Keep It Simple", "You
   Aren't Gonna Need It", "Don't Repeat Yourself". Each principle tells
   you when to apply it, when it fails, and which antipatterns it
   protects against.
2. **Antipatterns** (46) — concrete failure modes with symptom, cause,
   and fix.
3. **Ontologies** (6) — taxonomies for software engineering, data
   engineering, machine learning systems, web frontend, Python
   ecosystem, and security.
4. **Decision trees** (5) — "if your data is X, choose Y" with
   concrete answers at each leaf.
5. **Recipes** (5) — step-by-step procedures for common tasks (API
   design, authentication, database schema, error handling, refactoring).
6. **Comparisons** (3) — head-to-head matrices (SQL vs NoSQL, REST vs
   GraphQL, monolith vs microservices).
7. **Checklists** (9) — one per phase, with deliverables and "done"
   criteria.
8. **Risk catalogs** (4) — security, performance, maintainability,
   operational risks with mitigations.
9. **Risk enrichments** (144) — adversarially-accepted concepts from the
   870-book corpus, grouped into 17 themes (Git, React, LLMs, ML, DB,
   patterns, etc.).

You query this database from the command line:

```bash
# Free-text question, returns top-5 ranked results
python3 scripts/compiled_knowledge.py "API design REST versioning"

# Look up a specific item by ID
python3 scripts/compiled_knowledge.py --principle KISS
python3 scripts/compiled_knowledge.py --antipattern god-class
python3 scripts/compiled_knowledge.py --decision-tree choose-database
python3 scripts/compiled_knowledge.py --recipe api-design
python3 scripts/compiled_knowledge.py --checklist P5

# Compare two options
python3 scripts/compiled_knowledge.py --comparison "sql vs nosql"
```

Every result is **deterministic**: same question, same answer, no LLM, no
network, no hallucination.

### The corpus browser

If you want to go deeper than the 227 curated items, the harness also ships
a 145,963-concept index of the 870-book corpus. You can search any
concept from any book by line number:

```bash
# How many books and concepts are indexed?
python3 scripts/corpus_browser.py --stats

# Find every mention of "yield from generator" in the corpus
python3 scripts/corpus_browser.py --search "yield from generator" --top 10

# All concepts from a specific book
python3 scripts/corpus_browser.py --book "Fluent Python"

# Concepts in a specific line range (closest equivalent to a chapter)
python3 scripts/corpus_browser.py --book "Fluent Python" --lines 1-500

# By concept layer
python3 scripts/corpus_browser.py --layer recipe --top 5

# With prompt-injection sanitization (default ON when piping to another command)
python3 scripts/corpus_browser.py --safe --search "ignore previous"
```

Every result includes the source book and line number, so you can verify
anything against the original source.

---

## Architecture, in 30 seconds

```
┌────────────────────────────────────────────────────────────┐
│  Claude Code  (or any AI tool that calls Bash/Edit/Write) │
└──────────────────────────┬─────────────────────────────────┘
                           │  every tool call
                           ▼
┌────────────────────────────────────────────────────────────┐
│  Pre-tool-use hook  (reads settings.json)                  │
│  ┌──────────────────────┐  ┌────────────────────────────┐ │
│  │  phase-guard.sh      │  │  bash-guard.sh             │ │
│  │  (Write/Edit/Skill)  │  │  (Bash only)               │ │
│  └──────────┬───────────┘  └──────────┬─────────────────┘ │
│             │                         │                    │
│             ▼                         ▼                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  state engine  (atomic SQLite, audit chain)          │  │
│  │  • current_phase: P5                                 │  │
│  │  • gates_validated: [P1, P2, P3, P4]                 │  │
│  │  • circuit_breaker: 0/3                              │  │
│  │  • audit_log: 1,247 events, all HMAC-signed         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘

                       (separate, manual)
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│  compiled_knowledge.py  (the brain)                       │
│  "should I use SQL or NoSQL?" → ranked, cited answers     │
└────────────────────────────────────────────────────────────┘
```

The **hooks** are the gatekeepers. They run on every tool call and ask
the state engine "is this allowed right now?". If the answer is no, the
hook returns a structured reason and Claude Code refuses the action.

The **state engine** is the single source of truth. It uses SQLite with
write-ahead logging for atomicity, and every state change is HMAC-signed
to detect tampering.

The **compiled knowledge engine** is the brain. You don't need to use it
in your day-to-day work, but it's there when you have a design question
and want a quick, sourced answer.

---

## Use cases

### "I want to start a new project with this"

1. Install the harness (above).
2. Open Claude Code in your project directory.
3. Tell Claude what you want to build. The harness will keep you in
   `P1_REQUIREMENTS` until you've actually written requirements.
4. When you're ready, tell Claude: "advance to P2". The harness will
   verify your P1 deliverables before letting you move on.

### "I want to add it to an existing project"

1. Install the harness. The hooks activate immediately for new commands.
2. Run `python3 lib/state_engine.py set current_phase P5` to set the
   current phase to whatever you're actually doing.
3. Run `python3 lib/state_engine.py set gates_validated '["P1","P2","P3","P4"]'`
   to mark the earlier phases as already done.
4. The harness will then enforce P5+ rules on your ongoing work.

### "I want to use only the knowledge engine, no phase gating"

```bash
# Skip the install, just clone and use directly
git clone https://github.com/doz34/swebok-v4-harness.git
cd swebok-v4-harness
python3 scripts/compiled_knowledge.py "your question"
```

The knowledge engine has no dependencies on the hooks or the state engine.
You can use it as a standalone CLI in any workflow.

### "I want to inspect the audit log after an incident"

```bash
# Replay a time range
python3 lib/state_engine.py replay_session 2026-06-01 2026-06-02

# Check the audit chain integrity
python3 lib/state_engine.py check_integrity

# Export everything for forensics
python3 lib/state_engine.py export_state > incident-export.json
```

### "I want to bypass the harness for a specific command"

```bash
# Override the circuit breaker for the next operation
python3 lib/state_engine.py set circuit_breaker.override_active true

# Run your dangerous command (logged with reason)
rm -rf /tmp/stale-data

# Re-engage the harness
python3 lib/state_engine.py set circuit_breaker.override_active false
```

Every override is logged with a reason. The audit chain doesn't lie.

---

## Customization

### Add a custom principle

Edit `distilled/principles.json` and add a new entry. The schema:

```json
{
  "id": "MY_PRINCIPLE",
  "name": "My Custom Principle",
  "domains": ["my-domain"],
  "phases": ["P3", "P5"],
  "category": "universal",
  "citation_density": "high",
  "books_endorsing": ["My Favorite Book"],
  "synthesis": "One-paragraph explanation of the principle.",
  "applies_when": "Conditions under which the principle is relevant.",
  "violations_signal": "What a violation looks like in code.",
  "antipatterns": ["linked_antipattern_id"]
}
```

Reload by re-running `python3 scripts/compiled_knowledge.py --principle MY_PRINCIPLE`.

### Add a custom phase rule

Edit `lib/bash_scanner.py` to add a per-phase rule. Each rule is a regex
that triggers a block. The existing rules are in the `_phase_rules`
dict at the top of the file.

### Add a custom recipe

Create a new file in `distilled/recipes/` (markdown format) and reload.
The recipe is automatically picked up by the engine.

---

## Security and trust

- **The audit chain is tamper-evident.** Every row has an HMAC signature
  computed over the previous row's HMAC, the timestamp, and the content.
  Modifying any row breaks the chain.
- **The HMAC key is per-installation.** A fresh random 32-byte key is
  generated on first install. The key never leaves your machine.
- **The knowledge engine is offline.** It does not call any network
  resource. It is safe to use on air-gapped machines.
- **The state DB is per-project.** Each project gets its own
  `.swebok_state.db`. The harness's own state and your project's state
  are isolated.

If you find a security issue, please open a GitHub issue with the
`security` label.

---

## Limitations and honest scope

- **It is not a sandbox.** The harness blocks dangerous commands but
  does not prevent the assistant from doing anything else. It is one
  layer of defense, not the only one.
- **It is not an authentication boundary.** Anyone with access to your
  terminal can bypass the harness by editing the state DB or removing
  the hooks. It is designed to catch accidents, not adversaries.
- **The knowledge engine is curated, not generative.** The 227 items
  represent what the maintainers consider the consensus of the field.
  Newer practices may not be in there yet. Contributions welcome.

See `SECURITY.md` for the full threat model and `AUDIT_REPORT.md` for
the quarterly audit findings.

---

## Development and contributing

- **Run the tests:** `bash tests/distilled-test.sh` (32 tests) and
  `bash tests/retrieval/test-v2.sh` (20 tests). All should pass.
- **Add a knowledge item:** edit the relevant JSON file in `distilled/`,
  add a test in `tests/distilled-test.sh`, run the tests.
- **Add a phase rule:** edit `lib/bash_scanner.py`, add a test in
  `tests/`, run the tests.
- **Audit the project:** see `AUDIT_REPORT.md` for the methodology.

---

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

The compiled knowledge was distilled from 870+ software engineering
reference books across 16 domains, applying the SWEBOK v4 (Software
Engineering Body of Knowledge) taxonomy. The corpus browser exposes
the full 145,963 concepts of these books, line-by-line, for any reader
who wants to go deeper than the curated 227 items.
