# SWEBOK v4 Harness

> **A discipline layer for AI-assisted software development.** It watches
> every command, enforces your SDLC phases, carries the wisdom of 1,139
> reference books, and keeps a tamper-evident audit trail of everything
> that happened and why.

[![Tests](https://img.shields.io/badge/tests-152%2F152%20PASS-brightgreen)](tests/)
[![Audit](https://img.shields.io/badge/audit-100%25%20production%20ready-success)](ANALYSE_INTEGRALE_2026-06-10.md)
[![Corpus](https://img.shields.io/badge/corpus-1%2C139%20books%20%7C%20471K%20concepts-blue)](scripts/corpus_browser.py)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## Table of Contents

1. [What Is This?](#what-is-this)
2. [How It Works (Big Picture)](#how-it-works-big-picture)
3. [The 10 SDLC Phases](#the-10-sdlc-phases)
4. [Quick Start](#quick-start)
5. [Architecture](#architecture)
6. [The Compiled Knowledge Engine](#the-compiled-knowledge-engine)
7. [The Adversarial Loop](#the-adversarial-loop)
8. [Anti-Drift Auto-Trigger](#anti-drift-auto-trigger)
9. [Security Model](#security-model)
10. [Use Cases](#use-cases)
11. [Customization](#customization)
12. [Testing](#testing)
13. [Limitations](#limitations)
14. [Contributing](#contributing)
15. [License](#license)

---

## What Is This?

You know how it goes: you sit down to build something, start coding
immediately, skip the requirements, forget to write tests, push straight
to production, and six months later you're debugging a 3 AM incident
wondering "who approved this?"

**The SWEBOK v4 Harness fixes this.** It is a set of hooks that sit
between you (or your AI coding assistant) and your terminal. Every time
you try to write a file, run a command, or advance to the next phase of
your project, the harness checks:

- **"Is this action appropriate for the current phase?"** (Don't code
  during requirements gathering. Don't deploy without tests.)
- **"Is this command safe?"** (Block `rm -rf /`, `DROP TABLE`, `eval`
  with base64 obfuscation, and other destructive operations.)
- **"What does the collective wisdom of 1,139 books say about this?"**
  (Instant, deterministic answers about architecture, security, testing,
  and more.)

Everything is logged to a **tamper-evident audit chain** so you can
always answer "what happened and when?"

### Key Numbers

| Metric | Value |
|---|---|
| Tests | **152/152 PASS** (pre-commit gated) |
| Production audit | **100% — 0 blockers** (4-consultant council) |
| Knowledge corpus | **1,139 books, 471,472 concepts** |
| Curated items | **227 principles, antipatterns, recipes, etc.** |
| SDLC phases covered | **10 (P0–P10)** |
| Adversarial loop | **5 sprints (S0–S5)**, 60 payloads, 44 property tests |
| Lines of code | **~21,000** (Python + Shell) |
| License | **MIT** |

---

## How It Works (Big Picture)

```
 You type a prompt ──► Claude Code (AI assistant)
                            │
                ┌───────────┴───────────┐
                │  Every tool call is    │
                │  intercepted by hooks  │
                └───────────┬───────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
     ┌────────────┐  ┌────────────┐  ┌────────────────┐
     │ phase-guard│  │ bash-guard │  │ anti-drift     │
     │            │  │            │  │ auto-trigger   │
     │ Is this    │  │ Is this    │  │                │
     │ right for  │  │ command    │  │ Detect intent, │
     │ the phase? │  │ safe?      │  │ schedule       │
     └─────┬──────┘  └─────┬──────┘  │ council review │
           │               │         └───────┬────────┘
           ▼               ▼                 │
     ┌─────────────────────────────────┐     │
     │         State Engine            │     │
     │   (SQLite WAL + HMAC chain)     │     │
     │                                 │     │
     │  current_phase: P5_CONSTRUCTION │     │
     │  gates_validated: [P1..P4]      │     │
     │  audit_log: 1,247 HMAC-signed   │     │
     │  circuit_breaker: 0/3           │     │
     └─────────────────────────────────┘     │
           │                                 │
           ▼                                 ▼
     ┌─────────────────────────────────────────────┐
     │         Compiled Knowledge Engine            │
     │                                              │
     │  24 principles · 46 antipatterns · 6 trees  │
     │  5 recipes · 3 comparisons · 9 checklists   │
     │  4 risk catalogs · 144 enrichment concepts   │
     │                                              │
     │  "Should I use SQL or NoSQL?" → instant,    │
     │   deterministic, cited answer. No LLM.      │
     └─────────────────────────────────────────────┘
```

**Three layers, one purpose:**

1. **Hooks** (the gatekeepers) — run on every tool call, check the state
   engine, block or allow.
2. **State Engine** (the memory) — SQLite with HMAC chain, remembers
   everything, tamper-evident.
3. **Knowledge Engine** (the brain) — 1,139 books distilled into a
   queryable database. No LLM, no network, no hallucination.

---

## The 10 SDLC Phases

The harness enforces a 10-phase lifecycle based on SWEBOK v4 (IEEE
Computer Society's Software Engineering Body of Knowledge). Each phase
has specific rules about what you can and cannot do.

```
  ┌─────────┐     ┌─────────┐     ┌──────────┐     ┌─────────┐
  │  P0     │     │  P1     │     │  P2      │     │  P3     │
  │Discovery│────►│Concept &│────►│Require-  │────►│Archi-   │
  │         │     │Feasib.  │     │ments     │     │tecture  │
  └─────────┘     └─────────┘     └──────────┘     └─────────┘
       │                                               │
  "What should    "Is it worth   "Exactly what   "How do we
   we build?"     building?"      must it do?"    structure it?"
  
  ┌─────────┐     ┌─────────┐     ┌──────────┐     ┌─────────┐
  │  P4     │     │  P5     │     │  P6      │     │  P7     │
  │Design   │────►│Construc-│────►│Testing & │────►│Deploy-  │
  │         │     │tion     │     │Verif.    │     │ment     │
  └─────────┘     └─────────┘     └──────────┘     └─────────┘
       │                                               │
  "Detailed       "Write the      "Does it         "Ship it
   contracts"      actual code"    work?"           safely"
  
  ┌─────────┐     ┌─────────┐
  │  P8     │     │  P9/P10 │
  │Opera-   │────►│Maintain │────► End of Life
  │tions    │     │& Retire │
  └─────────┘     └─────────┘
       │
  "Keep it        "Fix it, evolve
   running"        it, or retire it"
```

### What gets blocked in each phase

| Phase | Write code? | Run tests? | Deploy? | Delete files? |
|---|---|---|---|---|
| P0–P4 | ❌ Blocked | ❌ Blocked | ❌ Blocked | ❌ Blocked |
| P5 | ✅ Allowed | ✅ Unit tests | ❌ Blocked | ❌ Blocked |
| P6 | ❌ Src changes | ✅ Full testing | ❌ Blocked | ❌ Blocked |
| P7 | ✅ Config only | ✅ Smoke tests | ✅ Allowed | ❌ Blocked |
| P8 | ✅ Hotfixes | ✅ Regression | ✅ Rollback | ⚠️ With override |
| P9–P10 | ✅ Patches | ✅ Validation | ✅ Migration | ⚠️ With override |

**Every block is logged. Every override requires a reason. The audit
chain doesn't lie.**

---

## Quick Start

### Prerequisites

- Linux or macOS
- Python 3.10+
- Bash shell
- [Claude Code](https://claude.ai/code) (optional, but that's the
  primary use case)
- 5 minutes

### Install

```bash
git clone https://github.com/doz34/swebok-v4-harness-distilled.git
cd swebok-v4-harness-distilled
bash install-harness.sh
```

The installer will:

1. Verify the harness is intact (no missing files)
2. Back up your existing Claude Code settings
3. Merge hook entries into `~/.claude/settings.json`
4. Generate a fresh HMAC key for the audit chain (stored in `.audit_key`,
   mode 0600, gitignored)
5. Initialize the state database

### Verify it works

```bash
# Ask the knowledge engine a question
python3 scripts/compiled_knowledge.py "should I use SQL or NoSQL?"

# Run the full test suite
bash tests/distilled-test.sh        # 32 tests
bash tests/retrieval/test-v2.sh     # 20 tests
bash tests/retrieval/test-adversarial.sh  # 8 tests
bash tests/adv-loop/test-properties.sh    # 44 tests
bash bin/adv-loop test              # 38 tests
python3 tests/test_health.py        # 5 tests
python3 tests/test_rebuild_restore.py  # 5 tests
# Total: 152 tests, all should PASS
```

### Day-to-day usage

Once installed, the harness runs **automatically** inside Claude Code.
You don't need to invoke it manually. It will:

- **Block** destructive commands at the wrong phase
- **Remind you** of deliverables for the current phase
- **Suggest** the next phase when deliverables are met
- **Answer** design and architecture questions instantly

---

## Architecture

### System diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Claude Code (AI Assistant)                   │
│                                                                     │
│  When you type: "Create a login API endpoint"                       │
│  Claude wants to: Write → src/auth.py, Bash → python3 manage.py    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                  settings.json routes tool calls to hooks
                             │
         ┌───────────────────┼───────────────────────────────┐
         ▼                   ▼                               ▼
  ┌──────────────┐   ┌──────────────┐   ┌───────────────────────────┐
  │  PHASE-GUARD │   │  BASH-GUARD  │   │  POST-TOOL-USE HOOKS     │
  │              │   │              │   │                           │
  │ Triggers on: │   │ Triggers on: │   │ • auto-verify.sh         │
  │ • Write      │   │ • Bash       │   │   (syntax check P5+)     │
  │ • Edit       │   │              │   │ • council-scheduler-hook │
  │ • Skill      │   │ Scans for:   │   │   (schedule reviews)     │
  │              │   │ • rm -rf     │   │ • mini-council-hook      │
  │ Checks:      │   │ • DROP TABLE │   │   (quick heuristic)      │
  │ • Current    │   │ • eval(base64│   │                           │
  │   phase      │   │ • sudo       │   └───────────────────────────┘
  │ • File type  │   │ • curl|sh    │
  │ • Phase rules│   │ • mkfs, dd   │
  └──────┬───────┘   └──────┬───────┘
         │                  │
         ▼                  ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     STATE ENGINE                             │
  │                                                              │
  │  .swebok_state.db (SQLite WAL, per-project isolation)       │
  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
  │  │ state table │ │ 4 audit      │ │ circuit_breaker      │ │
  │  │ (key/value) │ │ tables       │ │ (3-strike lock)      │ │
  │  │             │ │ (HMAC chain) │ │                      │ │
  │  │ phase: P5   │ │              │ │ file X: 2/3 blocks  │ │
  │  │ gates: [..] │ │ append-only  │ │                      │ │
  │  │ tools: 142  │ │ triggers     │ │ override: false      │ │
  │  └─────────────┘ └──────────────┘ └──────────────────────┘ │
  │                                                              │
  │  Security: HMAC key per install, mode 0600, gitignored      │
  │  Integrity: verify_audit_chain, export_state, rebuild        │
  └──────────────────────────────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                 COMPILED KNOWLEDGE ENGINE                     │
  │                                                              │
  │  distilled/                                                  │
  │  ├── principles.json     (24 universal rules)                │
  │  ├── antipatterns.json   (46 failure modes)                 │
  │  ├── ontologies/         (6 domain taxonomies)               │
  │  ├── decision-trees/     (5 "if X then Y" guides)           │
  │  ├── recipes/            (5 step-by-step procedures)         │
  │  ├── comparisons/        (3 head-to-head matrices)          │
  │  ├── checklists/         (9 per-phase gate checklists)      │
  │  ├── risks/              (4 threat catalogs)                │
  │  └── corpus_enrichment.json (144 adversarially-accepted)    │
  │                                                              │
  │  Query: <5ms · Deterministic · $0 · Offline · No LLM        │
  └──────────────────────────────────────────────────────────────┘
```

### File structure

```
swebok-v4-harness-distilled/
├── CLAUDE.md                  # Laws and routing rules (the "constitution")
├── README.md                  # This file
├── CHANGELOG.md               # Version history
├── LICENSE                    # MIT
├── settings.json              # Hook wiring (merged into ~/.claude/)
│
├── lib/                       # Python core (canonical location)
│   ├── state_engine.py        #   State machine + HMAC audit chain (~1100 LOC)
│   ├── state_engine_cli.py    #   CLI dispatcher for state_engine
│   ├── state_engine_counters.py  # Atomic counters (extracted)
│   ├── state_engine_logging.py   # Logging API (extracted)
│   ├── state_engine_prune.py     # Crash-safe pruning (extracted)
│   ├── bash_scanner.py        #   Phase-aware command filtering
│   ├── dsl_engine.py          #   DSL parser (KEY:VALUE;; delimiter)
│   └── auto_trigger.py        #   Intent detection (4-layer)
│
├── pre-tool-use/              # Hooks that run BEFORE each tool call
│   ├── phase-guard.sh         #   Block Write/Edit/Skill in wrong phase
│   ├── bash-guard.sh          #   Block dangerous shell commands
│   ├── token-counter.sh       #   Track token usage per phase
│   ├── auto-trigger-hook.sh   #   Detect user intent, auto-classify phase
│   └── phase-change-detector.sh  # Fire gate on phase transition
│
├── post-tool-use/             # Hooks that run AFTER each tool call
│   ├── auto-verify.sh         #   Syntax-check Python/JSON/YAML in P5+
│   ├── council-scheduler-hook.sh  # Schedule full council every N edits
│   └── mini-council-hook.sh   #   Quick heuristic review per edit
│
├── distilled/                 # The curated knowledge base (7 layers)
│   ├── principles.json        #   24 universal principles
│   ├── antipatterns.json      #   46 antipatterns with fixes
│   ├── ontologies/            #   6 domain taxonomies
│   ├── decision-trees/        #   5 decision guides
│   ├── recipes/               #   5 procedural guides
│   ├── comparisons/           #   3 comparison matrices
│   ├── checklists/            #   9 phase checklists
│   ├── risks/                 #   4 risk catalogs
│   ├── corpus_enrichment.json #   144 enrichment concepts
│   └── citations/             #   Source attribution
│
├── distilled_corpus/          # Raw distillation (1,139 books, gitignored)
│   └── per_book/              #   1,139 JSON files, one per book
│
├── scripts/                   # CLI tools
│   ├── compiled_knowledge.py  #   Query the knowledge engine
│   ├── corpus_browser.py      #   Browse the 471K-concept corpus
│   ├── batch_distill.py       #   Distill new books into the corpus
│   └── (symlinks → ../lib/)   #   lib/ alias for bash scripts
│
├── bin/                       # Adversarial loop runner
│   └── adv-loop               #   CLI: test, corpus, health, steer
│
├── tests/                     # Test suites (152 tests total)
│   ├── distilled-test.sh      #   32 tests: knowledge engine
│   ├── test_health.py         #   5 tests: health checks
│   ├── test_rebuild_restore.py #  5 tests: rebuild regression
│   ├── retrieval/
│   │   ├── test-v2.sh         #   20 tests: v2 retrieval
│   │   └── test-adversarial.sh #  8 tests: adversarial patterns
│   └── adv-loop/
│       └── test-properties.sh #   44 tests: property-based (4 × 11 phases)
│
├── specs/adversarial-patterns/ # Per-phase adversarial patterns (P0–P10)
├── audit/                     # Phase audit reports (P0–P10, all 🟢)
├── docs/                      # Architecture docs, ADRs
├── adversarial-gate.sh        # Red/Blue/Judge gate with DSL
├── multiagent-launcher.sh     # Council bridge (4 LLM judges)
├── health-check.sh            # Readiness probe (7 checks)
├── pre-commit-hook.sh         # Git pre-commit gate (152 tests + HMAC)
└── install-harness.sh         # One-command installer
```

### Data flow: what happens when you type a command

```
 User types: "Create a REST API for user authentication"
                           │
                           ▼
              ┌────────────────────────┐
              │  Claude Code parses    │
              │  and plans actions:    │
              │                        │
              │  1. Write → auth.py    │
              │  2. Write → test_auth  │
              │  3. Bash → pytest      │
              └───────────┬────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
   Action 1: Write   Action 2: Write   Action 3: Bash
   auth.py            test_auth.py      pytest
         │                │                │
         ▼                ▼                ▼
   ┌───────────┐   ┌───────────┐   ┌───────────┐
   │phase-guard│   │phase-guard│   │bash-guard │
   │           │   │           │   │           │
   │ Phase P5? │   │ Phase P5? │   │ Safe cmd? │
   │ .py file? │   │ test/ OK? │   │ pytest OK │
   │           │   │           │   │           │
   │ ✅ ALLOW  │   │ ✅ ALLOW  │   │ ✅ ALLOW  │
   └───────────┘   └───────────┘   └───────────┘
         │                │                │
         └────────────────┼────────────────┘
                          ▼
              ┌────────────────────────┐
              │  State Engine updates: │
              │  • tool_call_count +=3 │
              │  • audit log: 3 events │
              │  • HMAC chain updated  │
              └────────────────────────┘
```

If the phase was P2 (Requirements) instead of P5, the phase-guard would
**block** the Write actions with a clear message:

```
[PHASE-GUARD] BLOCKED: Writing .py files is not allowed in P2_REQUIREMENTS.
Current phase: P2_REQUIREMENTS
Reason: Construction (code writing) begins at P5. During P2, focus on
requirements specifications and stakeholder validation.
To advance phases: complete P2 deliverables and request gate review.
```

---

## The Compiled Knowledge Engine

The harness ships with a curated, deterministic knowledge base distilled
from **1,139 software engineering reference books**. This is **not RAG** —
it is a compiled database of rules, patterns, and decisions.

### Why this beats RAG

| Property | RAG (vector search + LLM) | This Engine |
|---|---|---|
| Determinism | ❌ Fuzzy similarity | ✅ Exact match, same answer every time |
| Latency | 200–2000ms | **<5ms** (in-memory dict lookup) |
| Cost | $0.01–0.10/query | **$0** (pure Python) |
| Network | Required | **None** (works offline, air-gapped) |
| Hallucination | Possible | **Impossible** (rules are explicit) |
| Audit | ❌ Black box | ✅ Every answer cites its source |

### 7 knowledge layers

```
┌──────────────────────────────────────────────────┐
│ Layer 1: PRINCIPLES (24)                         │
│ "Keep It Simple", "You Aren't Gonna Need It",    │
│ "Don't Repeat Yourself", "Fail Fast", etc.       │
│ Each with: when to apply, when it fails,         │
│ linked antipatterns.                              │
├──────────────────────────────────────────────────┤
│ Layer 2: ANTIPATTERNS (46)                       │
│ God Class, Spaghetti Code, Magic Numbers,         │
│ Golden Hammer, etc. Each with: symptom, cause,   │
│ and concrete fix.                                 │
├──────────────────────────────────────────────────┤
│ Layer 3: ONTOLOGIES (6)                          │
│ Software Engineering, Python, Web Frontend,       │
│ Data Engineering, Security, ML Systems.           │
│ Hierarchical taxonomies for each domain.          │
├──────────────────────────────────────────────────┤
│ Layer 4: DECISION TREES (5)                      │
│ "If your data is relational → SQL"                │
│ "If you need real-time → WebSocket"               │
│ Concrete if/then guides with leaf answers.        │
├──────────────────────────────────────────────────┤
│ Layer 5: RECIPES (5)                             │
│ API Design, Authentication, Database Schema,      │
│ Error Handling, Refactoring. Step-by-step.        │
├──────────────────────────────────────────────────┤
│ Layer 6: COMPARISONS (3)                         │
│ SQL vs NoSQL, REST vs GraphQL,                    │
│ Monolith vs Microservices. Scored matrices.       │
├──────────────────────────────────────────────────┤
│ Layer 7: CHECKLISTS + RISKS (13)                 │
│ 9 per-phase checklists (P0–P9) with deliverables  │
│ 4 risk catalogs (security, perf, maintain, ops)   │
└──────────────────────────────────────────────────┘
```

### Usage examples

```bash
# Free-text question → top-5 ranked results
python3 scripts/compiled_knowledge.py "should I use SQL or NoSQL?"

# Look up a specific principle
python3 scripts/compiled_knowledge.py --principle KISS

# Look up an antipattern
python3 scripts/compiled_knowledge.py --antipattern god-class

# Get a decision tree
python3 scripts/compiled_knowledge.py --decision-tree choose-database

# Get a recipe
python3 scripts/compiled_knowledge.py --recipe api-design

# Get a phase checklist
python3 scripts/compiled_knowledge.py --checklist P5

# Compare options
python3 scripts/compiled_knowledge.py --comparison "sql vs nosql"

# Get all risk items
python3 scripts/compiled_knowledge.py --risks

# Get statistics
python3 scripts/compiled_knowledge.py --stats
```

### Adding new books

```bash
# Distill a single book
python3 scripts/batch_distill.py file \
  --input ~/my-book.pdf \
  --title "My Book" \
  --author "Author Name" \
  --year 2025

# Batch distill from a JSON manifest
python3 scripts/batch_distill.py manifest \
  --manifest my-manifest.json
```

---

## The Adversarial Loop

The harness includes a 5-sprint adversarial system that stress-tests every
phase gate.

```
  Sprint 0         Sprint 1          Sprint 2          Sprint 3          Sprint 4          Sprint 5
  ┌───────┐       ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
  │ BASE  │──────►│ PER-PHASE │───►│ COUNCIL   │───►│ STEERING  │───►│ CORPUS    │───►│ PROPERTIES│
  │ LOOP  │       │ PATTERNS  │    │ BRIDGE    │    │ PERSIST.  │    │ 60 PAYLOAD│    │ 44 TESTS  │
  │       │       │           │    │           │    │           │    │           │    │           │
  │11     │       │11 bash    │    │4 LLM      │    │SHA-256    │    │9          │    │4 props ×  │
  │phase  │       │patterns   │    │judges     │    │fingerprnt │    │categories │    │11 phases  │
  │checks │       │P0-P10     │    │ciso/qa/   │    │recurring  │    │11 phases  │    │           │
  │       │       │           │    │arch/devops│    │patterns   │    │           │    │idempotent │
  └───────┘       └───────────┘    └───────────┘    └───────────┘    └───────────┘    │determin.  │
                                                                                    │monotonic  │
                                                                                    │well-formed│
                                                                                    └───────────┘
```

**Results:**
- **38 self-tests** (S0–S5)
- **44 property-based tests** (4 properties × 11 phases: idempotence,
  determinism, monotonicity, DSL well-formedness)
- **60 adversarial payloads** across 9 categories
- **3 real bugs found** by the corpus that S0–S3 missed

### Adversarial gate modes

| Mode | Command | Trust Level | Use Case |
|---|---|---|---|
| **Fixture** | `HARNESS_TEST_FIXTURE=1 adversarial-gate.sh P3 P4` | ⚠️ Dev only | Smoke testing |
| **Judge-only** | `adversarial-gate.sh P3 P4 --judge-only --red "..." --blue "..."` | ✅ Production | Real agent output |
| **Council** | `adversarial-gate.sh P3 P4 --council` | ✅ Strongest | 4 LLM judges |

> **⚠️ Fixture Disclosure:** The default (fixture) mode returns canned
> DSL strings for development. It is NOT a real adversarial review.
> Production verdicts MUST use `--council` or `--judge-only`. See
> `adversarial-gate.sh` lines 6–23 for the full honesty contract.

---

## Anti-Drift Auto-Trigger

Version 2.6.0 adds an anti-drift system that automatically detects when
you're working on something and schedules adversarial reviews without you
having to remember.

```
  You type a prompt
         │
         ▼
  ┌──────────────────┐
  │ G1: AUTO-TRIGGER │  UserPromptSubmit hook fires on every prompt
  │                  │  4-layer intent detection:
  │  • Cache lookup  │    cache → pattern → semantic → fallback
  │  • Regex match   │  Confidence threshold: 0.5
  │  • Semantic      │  Stores intent.phase in state DB
  │  • Fallback      │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ G3: PHASE CHANGE │  Detects phase transitions
  │                  │  Emits <MULTIAGENT_LAUNCH> envelope
  │  FIFO history:10 │  Dispatcher spawns Red/Blue agents
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ G5: COUNCIL      │  Schedules full council review
  │    SCHEDULER     │  Every 5 edits (configurable)
  │                  │  1-hour cooldown between reviews
  │  Threshold: 5    │  Whitelist: *.md, *.json, tests/*
  │  Cooldown: 1h    │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ G6: MINI-COUNCIL │  Per-edit heuristic review
  │                  │  Detects: hardcoded secrets, SQL injection,
  │  Latency: <100ms │  eval/exec, bare except, TODO/FIXME
  │  Escalates VULN  │  Falls back to Haiku judge if available
  └──────────────────┘
```

**Kill switch:** Set `HARNESS_AUTO_TRIGGER=0` to disable all 4 hooks.

---

## Security Model

### What we protect against

```
  ┌──────────────────────────────────────────────────────────┐
  │                    THREAT MODEL                          │
  │                                                          │
  │  ┌─────────────────┐    ┌─────────────────────────────┐ │
  │  │ External        │    │ Accidental                  │ │
  │  │ attacker with   │    │ developer mistake           │ │
  │  │ different UID   │    │                             │ │
  │  │                 │    │ • rm -rf in wrong dir       │ │
  │  │ → HMAC key is   │    │ • Skipping test phase       │ │
  │  │   chmod 0600    │    │ • Deploying without review  │ │
  │  │ → Audit chain   │    │ • Running eval(base64(...)) │ │
  │  │   is tamper-    │    │                             │ │
  │  │   evident       │    │ → Phase guard blocks        │ │
  │  └─────────────────┘    │ → Bash guard catches        │ │
  │                          │ → Circuit breaker locks     │ │
  │                          └─────────────────────────────┘ │
  │                                                          │
  │  ┌─────────────────┐    ┌─────────────────────────────┐ │
  │  │ Prompt          │    │ Supply chain                │ │
  │  │ injection via   │    │ compromise                  │ │
  │  │ malicious input │    │                             │ │
  │  │                 │    │ → pip hash-pinned           │ │
  │  │ → 3-layer       │    │ → HARNESS_DIR validated     │ │
  │  │   detection:    │    │ → State DB per-project      │ │
  │  │   outer marker, │    │ → No PII in commits         │ │
  │  │   inner phase,  │    │                             │ │
  │  │   scoper        │    │                             │ │
  │  └─────────────────┘    └─────────────────────────────┘ │
  └──────────────────────────────────────────────────────────┘
```

### Security features checklist

| Feature | How | Tested |
|---|---|---|
| HMAC audit chain | SHA-256, per-row, chained | ✅ verify_audit_chain |
| Append-only audit | BEFORE DELETE/UPDATE triggers | ✅ 4 tables |
| State DB isolation | Per-project, world-writable CWD refused | ✅ unit tests |
| HARNESS_DIR validation | Trust boundary check, samefile() | ✅ state_engine |
| Bash command scanning | Phase-aware, 30+ dangerous patterns | ✅ bash_scanner |
| SQL injection protection | Allowlist table names, parameterized queries | ✅ CLI + counters |
| Path traversal detection | Symlink rejection, path sandboxing | ✅ adversarial tests |
| SSRF protection | Private IP rejection (Ollama provider) | ✅ test-adversarial |
| Kill switch | 1 env var disables all auto-triggers | ✅ documented |

### What we do NOT protect against

- **Same-user privilege escalation**: any process running as your user
  can read the HMAC key. The audit chain defends against different-user
  tampering, not same-user attacks.
- **Physical access**: someone with your machine can edit the state DB.
- **Social engineering**: the harness cannot prevent you from manually
  overriding it.

---

## Use Cases

### Starting a new project

```bash
# Install (one time)
bash install-harness.sh

# Open Claude Code in your project
cd my-project
claude

# Tell Claude: "I want to build a task management app"
# → Harness keeps you in P1 (Requirements) until specs are written
# → Phase guard blocks any .py/.js file creation

# When requirements are done:
"Advance to P3 (Architecture)"
# → Harness verifies P1+P2 deliverables
# → Adversarial gate runs before allowing the transition
```

### Adding to an existing project

```bash
# Install, then set your current phase
python3 lib/state_engine.py set current_phase P5_CONSTRUCTION

# Mark earlier phases as done
python3 lib/state_engine.py set gates_validated '["P1","P2","P3","P4"]'

# Now the harness enforces P5 rules going forward
```

### Knowledge engine only (no hooks)

```bash
# Just clone and query — no installation needed
git clone https://github.com/doz34/swebok-v4-harness-distilled.git
cd swebok-v4-harness-distilled
python3 scripts/compiled_knowledge.py "how to design a rate limiter?"
```

### Incident forensics

```bash
# Check audit chain integrity (all 4 tables)
python3 lib/state_engine.py check_integrity

# Verify specific table
python3 lib/state_engine.py verify_audit_chain

# Replay a time range
python3 lib/state_engine.py replay_session 2026-06-01 2026-06-02

# Full export for forensics
python3 lib/state_engine.py export_state > incident.json
```

### Bypass for a specific command

```bash
# Override the circuit breaker (logged with reason)
python3 lib/state_engine.py set circuit_breaker.override_active true
rm -rf /tmp/stale-data
python3 lib/state_engine.py set circuit_breaker.override_active false
```

### Health check

```bash
bash health-check.sh

# Output:
#   integrity: OK
#   phase: OK (P5_CONSTRUCTION)
#   chain: OK (all 4 tables intact)
#   latency: OK (3ms)
#   backups: OK (3 snapshots)
#   audit_key: OK (mode 0600)
#   hooks: OK (7 hook entries)
#   Status: HEALTHY
```

---

## Customization

### Add a custom principle

Edit `distilled/principles.json`:

```json
{
  "id": "MY_PRINCIPLE",
  "name": "My Custom Principle",
  "domains": ["my-domain"],
  "phases": ["P3", "P5"],
  "category": "universal",
  "citation_density": "high",
  "books_endorsing": ["My Favorite Book"],
  "synthesis": "One-paragraph explanation.",
  "applies_when": "When X happens.",
  "violations_signal": "You'll see Y in the code.",
  "antipatterns": ["linked_antipattern_id"]
}
```

### Add a custom phase rule

Edit `lib/bash_scanner.py` — add a regex to the `_phase_rules` dict:

```python
_phase_rules["P5"] = [
    # existing rules...
    re.compile(r'\bmy_dangerous_command\b'),
]
```

### Add a custom recipe

Create `distilled/recipes/my-recipe.md` — the engine picks it up
automatically.

---

## Testing

### Run all tests

```bash
# The pre-commit hook runs all 152 tests automatically
bash pre-commit-hook.sh

# Or run individual suites:
bash tests/distilled-test.sh              # 32 tests: knowledge engine
bash tests/retrieval/test-v2.sh           # 20 tests: v2 retrieval
bash tests/retrieval/test-adversarial.sh  #  8 tests: adversarial patterns
bash tests/adv-loop/test-properties.sh    # 44 tests: property-based
bash bin/adv-loop test                    # 38 tests: adversarial loop
python3 tests/test_health.py             #  5 tests: health checks
python3 tests/test_rebuild_restore.py    #  5 tests: rebuild regression
```

### Test breakdown

| Suite | Count | What it tests |
|---|---|---|
| `distilled-test.sh` | 32 | Knowledge engine (principles, antipatterns, ontologies, etc.) |
| `test-v2.sh` | 20 | V2 retrieval engine, query accuracy |
| `test-adversarial.sh` | 8 | SSRF protection, symlink rejection, size limits |
| `test-properties.sh` | 44 | 4 properties × 11 phases (idempotence, determinism, etc.) |
| `adv-loop test` | 38 | Adversarial loop self-tests (S0–S5) |
| `test_health.py` | 5 | Health check functions |
| `test_rebuild_restore.py` | 5 | State DB rebuild preserves data |
| **Total** | **152** | **All gated by pre-commit hook** |

---

## Limitations

- **Not a sandbox.** The harness blocks dangerous commands but does not
  prevent the AI assistant from doing everything. It is one layer of
  defense, not the only one.
- **Not an authentication boundary.** Anyone with terminal access can
  edit the state DB or remove hooks. It catches accidents, not
  adversaries.
- **Knowledge is curated, not generative.** The 227 items are what the
  maintainers consider field consensus. Newer practices may not be there
  yet. Contributions welcome.
- **Adversarial gate is fixture by default.** Production verdicts
  require `--council` or `--judge-only` mode. The fixture mode is
  explicitly labeled as such (see `adversarial-gate.sh` lines 6–23).
- **Same-user HMAC limitation.** The HMAC audit chain defends against
  tampering by different users, not by processes running as the same
  user.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for your change
4. Run `bash pre-commit-hook.sh` — all 152 tests must pass
5. Submit a pull request

For security issues, please use the GitHub `security` label rather than
public disclosure.

---

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

The compiled knowledge was distilled from **1,139 software engineering
reference books** across 16 domains, applying the SWEBOK v4 (IEEE
Computer Society's Software Engineering Body of Knowledge) taxonomy.

The adversarial loop methodology follows the 5-sprint pattern (S0=base,
S1=patterns, S2=council, S3=steering, S4=corpus, S5=properties) — a
reproducible framework for adversarial testing of discipline layers.

Production readiness was validated by a **4-consultant adversarial
council** (CISO, Architect, DevOps/QA Lead, Product) through 4
iterations (84% → 92% → 98.5% → 100%).

---

*Built with ❤️ and too many reference books.*
