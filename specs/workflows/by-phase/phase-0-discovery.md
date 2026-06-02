# Phase 0: Discovery Workflow Spec

## Metadata
- **Phase**: 0
- **Name**: Discovery
- **Purpose**: Initial exploration, stakeholder identification, and project chartering
- **Parallel Mode**: Hyperagent enabled

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-0.1 | Project initiative documented | Initiative brief exists and is non-null | 100% completion |
| EG-0.2 | Stakeholder request or problem statement | Documented request with originator | Non-empty string, author identified |
| EG-0.3 | Knowledge base accessibility | Read access confirmed to corpus | Access verified within 24h |
| EG-0.4 | Resource availability | At least 2 agents available | Availability confirmed |
| EG-0.5 | Discovery scope defined | Initial scope boundary document | Contains at minimum: scope, constraints, timeline |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers escalation to project sponsor.

---

## Entry Criteria (Legacy Reference)
- Project initiative identified
- Stakeholder request or business problem statement
- Access to relevant knowledge bases and corpus

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-0.1 | Project charter documented | Charter completeness score | ≥95% per checklist |
| XG-0.2 | Stakeholder register populated | Stakeholder entries with contact info | ≥90% populated |
| XG-0.3 | Initial scope defined | Scope document with boundaries | Scope items ≥10, ambiguity <5% |
| XG-0.4 | Risk landscape surveyed | Risk entries in register | ≥80% coverage of identified risks |
| XG-0.5 | Discovery report approved | Review sign-off by ≥2 stakeholders | Formal approval documented |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` requires remediation before Phase 1.

---

## Exit Criteria (Legacy Reference)
- Project charter documented
- Stakeholders identified and mapped
- Initial scope defined
- Risk landscape surveyed
- Discovery report approved

---

## Transition Criteria to Phase 1

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Discovery artifacts complete | Phase 0 | Phase 1 | Artifact checklist 100% |
| Stakeholder alignment confirmed | Nexus-PM | Discovery-Orchestrator | Signed acknowledgment |
| Risk appetite documented | Nexus-Security | Project Sponsor | Risk tolerance letter |
| Resource commitment secured | Hyperagent-Orchestrator | Project Lead | Resource allocation memo |
| Charter ratified | All agents | Project Charter | Sponsor signature |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_0_COMPLETE` only when all transition criteria verified.

---

## Key Activities

### Activity 0.1: Stakeholder Analysis
- Identify primary, secondary, and tertiary stakeholders
- Map stakeholder interests and influence
- Establish communication protocols

### Activity 0.2: Context Exploration
- Survey existing knowledge bases
- Explore corpus for relevant prior art
- Identify constraints and assumptions

### Activity 0.3: Problem Framing
- Articulate business problem
- Define success criteria
- Establish non-functional requirements boundaries

### Activity 0.4: Risk Discovery
- Preliminary risk assessment
- Dependency identification
- Resource constraint analysis

---

## Responsible Agents
| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordinates parallel discovery tasks |
| Nexus-Architect | System context and boundaries |
| Nexus-PM | Stakeholder management |
| Nexus-Security | Security risk initial assessment |

---

## Required Skills
- `nexus-architect`: Context framing
- `nexus-pm`: Stakeholder analysis
- `nexus-security`: Risk discovery
- `discovery-orchestrator`: Multi-expert needfinding

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-discovery-complete` | Exit criteria met | Triggers Phase 1 initiation |
| `stakeholder-map-generated` | Stakeholder analysis done | Updates stakeholder register |
| `risk-landscape-surveyed` | Risk discovery complete | Updates risk register |

---

## Artifacts Produced

| Artifact | Description | Location |
|----------|-------------|----------|
| `project-charter.md` | Initial project definition | `specs/specs/workflows/by-phase/phase0/` |
| `stakeholder-register.md` | Stakeholder map | `specs/specs/workflows/by-phase/phase0/` |
| `discovery-report.md` | Findings and recommendations | `specs/specs/workflows/by-phase/phase0/` |
| `risk-preliminary.md` | Initial risk assessment | `specs/specs/workflows/by-phase/phase0/` |
| `context-survey.md` | Environmental context | `specs/specs/workflows/by-phase/phase0/` |

---

## Hyperagent Parallel Processing

```
parallel_tasks:
  - task: stakeholder_analysis
    agents: [Nexus-PM, Nexus-Security]
    sync: false
  
  - task: context_exploration
    agents: [Nexus-Architect, Discovery-Orchestrator]
    sync: false
  
  - task: problem_framing
    agents: [Nexus-PM, Nexus-Architect]
    sync: true
  
  - task: risk_discovery
    agents: [Nexus-Security, Nexus-DevOps]
    sync: false

reduction: "Nexus-Architect synthesizes findings into discovery-report.md"