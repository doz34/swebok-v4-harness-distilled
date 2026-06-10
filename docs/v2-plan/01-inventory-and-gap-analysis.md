# Sprint 1 — Inventory & Gap Analysis

> **Date** : 2026-06-10
> **Goal** : exhaustive list of local Claude Code skills/tools + map to swebok phases + identify gaps

## 1. Local Claude Code inventory (2026-06-10)

### 1.1 Slash commands (13)

| Command | Purpose | Maps to phase |
|---|---|---|
| `/agents` | Multi-agent subagent launch | All phases |
| `/best` | Switch to Opus 4.5 (paid) | Quality boost (P6) |
| `/explore` | Codebase exploration | P0, P3, P4 |
| `/fast` | Switch to local GPT-OSS 20B (free) | P0-P1 (low cost) |
| `/free` | Switch to local Qwen 3 Coder 30B (free) | All phases |
| `/legacy` | Legacy mode (9-section system prompts) | Legacy code (P9) |
| `/llm` | Dual LLM manager (Claude + PDF Skill) | P5, P7 |
| `/local` | Switch to local Qwen 3 14B | All phases |
| `/multiagent` | Multi-agent workflow | All gates |
| `/plan` | Architecture plan | P3, P4 |
| `/pro` | Switch to Sonnet 4.5 (paid) | Default mode |
| `/skills` | Create reusable skills | All phases |
| `/status` | Show current version | Diagnostic |

### 1.2 Skills (57)

| Skill | Domain | Maps to phase |
|---|---|---|
| **agent_skills** | agent-transcript | All |
| **caveman** | ultra-compact output | DSL (all) |
| **continuity-council** | 5-expert review | P6 (testing) |
| **core** | code_review | P5, P6 |
| **discovery-orchestrator** | spec-driven | **P0** |
| **hyperagent** | hyperagent orchestration | All |
| **iterative-code-design** | iterative design | **P4, P5** |
| **karpathy-skills** | skills concept | All |
| **llm** | Dual LLM manager | P5, P7 |
| **nexus (coordinator)** | multi-nexus | All |
| **nexus-ai** | AI/LLM/RAG | **P0, P5** |
| **nexus-architect** | system design | **P3** |
| **nexus-backend** | backend dev | **P5** |
| **nexus-ceo** | strategic vision | **P0, P1** |
| **nexus-ciso** | security | **P7, P8** |
| **nexus-cpo** | product strategy | **P0, P1** |
| **nexus-cto** | technical architecture | **P3, P5** |
| **nexus-data-eng** | data pipelines | **P5** |
| **nexus-devops** | Docker/K8s/Terraform | **P7** |
| **nexus-devops-lead** | infra strategy | **P7, P8** |
| **nexus-docs** | technical writing | **All (deliverables)** |
| **nexus-ds** | data science | **P5 (data)** |
| **nexus-em** | tech coordination | All |
| **nexus-frontend** | frontend dev | **P4, P5** |
| **nexus-fullstack** | full-stack dev | **P5** |
| **nexus-pm** | project planning | **P0, P1, P2** |
| **nexus-product** | backlog/roadmap | **P0, P2** |
| **nexus-qa** | test writing | **P6** |
| **nexus-qa-lead** | QA strategy | **P6** |
| **nexus-security** | security impl | **P5, P7** |
| **nexus-sm** | agile/scrum | **P0, P9** |
| **project-continuity** | project persistence | All |
| **qa-feature-test-expert** | test expertise | **P6** |
| **skill-composer-test** | test skill | (testing) |
| **skill-invoker** | explicit skill invoke | All |
| **speckit-qa** | spec-kit QA | **P6** |
| **vitalite-coach** | personalized coaching | All |
| **zai-glm51-cost-opt** | cost optimization | P0, P1 |
| **langues / domains / specializations / examples** | supplementary | — |

### 1.3 MCP servers (4)

| MCP | Purpose | Maps to phase |
|---|---|---|
| **zai-mcp-server** | Z.AI GLM models | All (default LLM) |
| **zread** | GitHub repo analysis | P3, P4 (research) |
| **web-reader** | Web article reading | P0, P1, P8 |
| **web-search-prime** | Web search | P0, P1, P8 |

### 1.4 Current swebok components

- **77 lib modules** including `intent-detector.py`, `state_engine.py`, `dsl_engine.py`, etc.
- **11 phase specs** in `specs/workflows/by-phase/`
- **3 gates**: `adversarial-gate.sh`, `validate-gates.sh`, `validate-qa-gates.sh`
- **3 hooks**: `pre-tool-use/phase-guard.sh`, `pre-tool-use/bash-guard.sh`, `post-tool-use/auto-verify.sh`
- **11 adversarial patterns** in `specs/adversarial-patterns/` (newly added)
- **1 170 per_book files** with 467 156 concepts
- **2 state engines** (SQLite WAL): `.swebok_state.db`

## 2. Gap Analysis — features vs state

| User requirement | Current state | Gap |
|---|---|---|
| **Auto-trigger from prompt** | `intent-detector.py` exists, uses `intent-map.json` | **Incomplete** — need to test reliability + efficiency |
| **Modular phases** | Phases defined in specs, hooks enforce | **Partial** — need per-phase CLI entry points |
| **Elaborate adversarial harness** | `specs/adversarial-patterns/` has 3 useful + 8 stubs | **Partial** — need to implement 8 remaining |
| **No document mentions** | Many places reference books (e.g. "Booch", "Brooks", "Sadalage") | **CRITICAL** — need to scrub user-facing docs |
| **GitHub publish (EN docs)** | README is EN, but technical docs (`docs/v1/`, `audit/`) are FR/EN mixed | **MIXED** — need to standardize to EN |
| **Exhaustive skills listing** | 57 skills + 13 commands + 4 MCPs inventoried | ✅ Done (this document) |
| **Structured plan .md** | This file is S1 | ✅ In progress |
| **Each concept functional** | 467k concepts distilled, 1 170 per_book, 95 % coverage | **Verify** — need end-to-end test |

## 3. Priority actions (next sprints)

| Sprint | Action | Owner | Effort |
|---|---|---|---|
| **S2** | Implement auto-trigger (intent-detector v2) | maintainer | 4 h |
| **S3** | Complete 8 missing adversarial patterns | maintainer | 3 h |
| **S3** | Add per-phase CLI (`bin/phase N`) | maintainer | 1 h |
| **S3** | Add per-phase deep validation tests | maintainer | 2 h |
| **S4** | Scrub all book references (black box principle) | maintainer | 2 h |
| **S4** | Delete obsolete v1.5.x tags on GitHub | maintainer | 30 min |
| **S4** | Publish v2.0 with English docs | maintainer | 1 h |
| **S5** | Write iteration protocol | maintainer | 1 h |

## 4. Status

- ✅ Local skills inventory done
- ✅ Gap analysis done
- ⏳ Next: S2 (auto-trigger) — see `02-feature-1-auto-trigger.md`
