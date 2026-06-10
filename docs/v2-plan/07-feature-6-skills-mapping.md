# Feature 6 — Skills Mapping (Local → Phases)

> **Date** : 2026-06-10
> **Goal** : map each local Claude Code skill to a swebok phase (one per phase)
> **Status** : ⏳ TODO

## 1. Problem statement

57 local skills + 13 commands + 4 MCPs. Each could contribute to one or more phases. The current harness doesn't formally map them.

## 2. Mapping table (proposal)

| Phase | Primary skill(s) | Secondary skill(s) | Slash command | MCP |
|---|---|---|---|---|
| **P0 Discovery** | discovery-orchestrator | nexus-ceo, nexus-cpo, nexus-pm, nexus-product, zai-glm51-cost-opt | /plan, /free | web-search-prime, web-reader |
| **P1 Feasibility** | nexus-pm, nexus-cpo | zai-glm51-cost-opt, nexus-ceo | /plan, /free | — |
| **P2 Requirements** | nexus-pm, nexus-product | discovery-orchestrator | /plan | web-reader |
| **P3 Architecture** | nexus-architect, nexus-cto | iterative-code-design | /plan, /explore | zread |
| **P4 Design** | iterative-code-design | nexus-architect, nexus-frontend, nexus-backend | /plan, /explore | zread |
| **P5 Implementation** | nexus-fullstack, nexus-backend, nexus-frontend, nexus-ai, nexus-data-eng | nexus-architect, iterative-code-design | /skills, /multiagent | zai-mcp-server |
| **P6 Testing** | nexus-qa, nexus-qa-lead, qa-feature-test-expert, speckit-qa, continuity-council, core | /agents | — |
| **P7 Deployment** | nexus-devops, nexus-devops-lead, nexus-security, nexus-ciso | /legacy | zai-mcp-server |
| **P8 Operations** | nexus-sm, nexus-devops-lead | continuity-council, speckit-qa | — |
| **P9 Maintenance** | nexus-sm, iterative-code-design | /legacy | — |
| **P10 Retirement** | nexus-ceo, nexus-cpo | project-continuity, skill-invoker | — |

## 3. Implementation

### 3.1 New file: `bin/swebok-suggest`

```bash
$ bin/swebok-suggest
# Shows which skills/commands/MCPs are useful for current phase
# Based on .swebok_state.db (current_phase key)
$ bin/swebok-suggest --phase 5
# Shows for explicit phase P5
```

Output:
```
Phase 5 (Implementation)
Recommended skills: nexus-fullstack, nexus-backend, nexus-frontend
Recommended commands: /skills, /multiagent
Recommended MCPs: zai-mcp-server
Useful: 4 skills, 2 commands, 1 MCP
```

### 3.2 Per-phase skills config: `config/phase-skills.json`

```json
{
  "0": {
    "primary_skills": ["discovery-orchestrator"],
    "secondary_skills": ["nexus-ceo", "nexus-cpo", "nexus-pm"],
    "slash_commands": ["/plan", "/free"],
    "mcps": ["web-search-prime", "web-reader"]
  },
  "1": {
    "primary_skills": ["nexus-pm", "nexus-cpo"],
    ...
  }
}
```

## 4. Tests (acceptance criteria)

- [ ] Test 1: `bin/swebok-suggest` returns skills for current phase
- [ ] Test 2: `bin/swebok-suggest --phase N` works for all 11 phases
- [ ] Test 3: each phase has ≥3 primary skills + ≥1 slash command
- [ ] Test 4: `phase-skills.json` is valid JSON for all 11 phases
- [ ] Test 5: skills listed in `phase-skills.json` exist in `~/.claude/skills/`
- [ ] Test 6: integrates with `bin/phase N` and `bin/auto-trigger`
- [ ] Test 7: latency <100ms
- [ ] Test 8: works offline
- [ ] Test 9: no missing skills
- [ ] Test 10: no orphan skills (all skills mapped to ≥1 phase)

## 5. Status

- ⏳ TODO
- Next: create `config/phase-skills.json` and `bin/swebok-suggest`
- Effort: 2h

## 6. Implementation log

(Each iteration adds a line here)
