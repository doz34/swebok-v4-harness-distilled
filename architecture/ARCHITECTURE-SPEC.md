# SWEBOK v4 Harness — Architecture Specification

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER PROMPT                              │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HOOK: pre-prompt                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │Intent Detect │ │Context Inject│ │Skill Router  │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR LAYER                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │Discovery     │ │Spec          │ │Project       │            │
│  │Orchestrator  │ │Generator     │ │Architect     │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT LAYER (Specialists)                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │Requirements  │ │Architecture  │ │Test          │            │
│  │Analyst       │ │Designer      │ │Strategist    │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │Security      │ │Quality       │ │Maintenance   │            │
│  │Engineer      │ │Assurance     │ │Specialist     │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTOR LAYER                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │Code          │ │Test          │ │Doc           │            │
│  │Generator     │ │Writer        │ │Writer        │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HOOK: post-task / post-prompt                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │Validation    │ │Quality       │ │Handoff       │            │
│  │              │ │Check         │ │Completion    │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        USER RESPONSE                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Intent Detection Engine

**Purpose**: Classifier l'intent du prompt utilisateur et déterminer les skills/agents à invoquer

**Algorithm**:
```
1. Parse prompt → tokens
2. Match against intent_patterns (regex + semantic)
3. Score each potential intent (0.0 - 1.0)
4. Select top-k intents above threshold
5. Output: List<(intent, confidence, relevant_skills)>
```

**Intent Taxonomy** (based on SWEBOK KAs):
- `requirement_gathering` → KA-1
- `architecture_planning` → KA-2
- `software_design` → KA-3
- `code_construction` → KA-4
- `test_planning` → KA-5
- `maintenance_analysis` → KA-6
- `config_management` → KA-7
- `project_planning` → KA-8
- `process_improvement` → KA-9
- `method_selection` → KA-10
- `quality_assurance` → KA-11
- `safety_analysis` → KA-12
- `security_engineering` → KA-13
- `system_integration` → KA-14

---

### 2.2 Skill Router

**Purpose**: Router vers les skills appropriés basés sur les intents détectés

**Routing Rules**:
```yaml
routing:
  requirement_gathering:
    primary_skill: requirements-elicitation
    fallback: general-elicitation
    dependencies: []
    
  architecture_planning:
    primary_skill: architecture-design
    fallback: general-architecture
    dependencies: [requirements-specification]
    
  test_planning:
    primary_skill: testing-strategies
    fallback: general-testing
    dependencies: [requirements-validation]
```

---

### 2.3 Knowledge Base Interface

**Purpose**: Accéder au corpus SWEBOK v4 (742 sections) pour contextualiser les réponses

**Index Structure**:
```yaml
index:
  by_ka:
    1: [sections 1-73]
    2: [sections 74-156]
    ...
  by_topic:
    "sql-injection": [section_451, section_452]
    "design-patterns": [section_201-210]
  by_keyword:
    "requirements": [all sections containing "requirement"]
```

**Query Interface**:
```
search(query, filters) → List<Section>
get_section(section_id) → Section
get_ka_overview(ka_id) → Summary + TOC
get_topic_detail(topic) → Detailed explanation + examples
```

---

### 2.4 Orchestrator Agents

#### Discovery Orchestrator
- **Role**: Clarifie les besoins, structure l'ambiguïté
- **Inputs**: Raw user request
- **Outputs**: Structured requirement brief, identified gaps
- **Protocol**: `discovery-orchestrator` skill

#### Spec Generator
- **Role**: Transforme les briefs en spécifications exécutables
- **Inputs**: Structured brief, SWEBOK references
- **Outputs**: SPEC.md, acceptance criteria, traceability

#### Project Architect
- **Role**: Définit l'architecture technique globale
- **Inputs**: Requirements specification, constraints
- **Outputs**: Architecture decision record, component map

---

### 2.5 Specialist Agents

Chaque KA du SWEBOK a un agent spécialiste correspondant:

| KA | Agent | Responsibilities |
|----|-------|------------------|
| 1 | requirements-analyst | Elicitation, analysis, specification, validation |
| 2 | architecture-designer | Architecture design, pattern selection, evaluation |
| 3 | design-specialist | Detailed design, pattern application |
| 4 | construction-lead | Coding standards, verification, integration |
| 5 | test-strategist | Test planning, technique selection, automation |
| 6 | maintenance-specialist | Change analysis, migration, retirement |
| 7 | config-manager | Version control, change management |
| 8 | project-manager | Planning, estimation, risk, stakeholder |
| 9 | process-engineer | Process definition, assessment, improvement |
| 10 | method-consultant | Methodology selection, tailoring |
| 11 | quality-assurance | QA, metrics, verification |
| 12 | safety-engineer | Hazard analysis, risk management |
| 13 | security-engineer | Security design, testing, vulnerability |
| 14 | systems-engineer | Whole system, HW/SW integration |
| 15 | foundation-specialist | Data structures, algorithms |

---

### 2.6 Executor Agents

**Code Generator**
- Génère du code à partir de spécifications
- Applique les standards du langage cible
- Auto-invoqué après architecture/design approval

**Test Writer**
- Génère des tests unitaires, integration, E2E
- S'appuie sur les acceptance criteria
- Applique les pratiques de testing du KA-5

**Doc Writer**
- Génère documentation technique
- Maintient la documentation au fil du code
- Synchronise avec les changements

---

## 3. Data Flow

### 3.1 Requirement → Implementation Flow

```
User: "I need a REST API for user management"

→ HOOK(pre-prompt): intent_detect("REST API development")
  → Injects: requirements-elicitation context
  → Routes to: requirements-analyst agent

→ REQUIREMENTS_ANALYST: Elicitation
  → Questions stakeholder
  → Produces: UserStories.md

→ REQUIREMENTS_ANALYST: Analysis & Specification  
  → Produces: RequirementsSpec.md
  → Handoff: to architecture-designer

→ ARCHITECTURE_DESIGNER: Architecture Design
  → Produces: ArchitectureDecision.md
  → Pattern: RESTful API, Layered Architecture
  → Handoff: to design-specialist

→ DESIGN_SPECIALIST: Detailed Design
  → Produces: DesignSpec.md
  → Handoff: to code-generator

→ CODE_GENERATOR: Implementation
  → Produces: user-management-api/
  → Includes: unit tests
  → Includes: OpenAPI spec

→ HOOK(post-task): Quality validation
  → Code review checklist
  → Test coverage check
  → Security scan

→ HOOK(post-prompt): Final response to user
```

---

### 3.2 Skill Auto-Invocation Flow

```
User Prompt
    │
    ▼
┌─────────────────┐
│ Intent Detection│
│ (pre-prompt)    │
└─────────────────┘
    │
    ▼
┌─────────────────┐     ┌─────────────────┐
│ Intent: testing │────▶│ Test Strategist │
│ score: 0.92    │     │ Skill: injected │
└─────────────────┘     └─────────────────┘
    │
    ▼
┌─────────────────┐     ┌─────────────────┐
│ Intent: reqs    │────▶│ Requirements    │
│ score: 0.87     │     │ Skill: injected │
└─────────────────┘     └─────────────────┘
    │
    ▼
┌─────────────────┐
│ Orchestration   │
│ (parallel       │
│ processing)     │
└─────────────────┘
```

---

## 4. Communication Protocols

### 4.1 Inter-Agent Protocol

```yaml
protocol: agent_communication_v1

messages:
  - type: task_request
    fields:
      - task_id
      - task_type
      - context
      - inputs
      - expected_outputs
      - constraints
  
  - type: task_response
    fields:
      - task_id
      - status (success|partial|failure)
      - outputs
      - issues
      - handoff_ready
  
  - type: handoff_notification
    fields:
      - from_agent
      - to_agent
      - content_summary
      - dependencies_met
  
  - type: clarification_request
    fields:
      - question
      - context
      - priority
```

---

### 4.2 Skill Invocation Protocol

```yaml
protocol: skill_invocation_v1

invocation:
  trigger:
    - intent_match
    - explicit_request
    - hook_injection
    - dependency_resolution
  
  lifecycle:
    1. skill_identified(skill_id)
    2. context_prepared(context, relevant_files)
    3. skill_executed(input)
    4. output_validated(output_spec)
    5. handoff_or_complete(result)
```

---

## 5. Quality Assurance

### 5.1 Output Quality Gates

| Gate | Check | Action on Failure |
|------|-------|-------------------|
| Completeness | All required sections present | Block, request completion |
| Traceability | Requirements → Code mapping exists | Warn, require mapping |
| Consistency | No conflicting outputs | Mediate conflict |
| Format | Output matches spec format | Reformat or block |
| Security | No vulnerabilities introduced | Block, require fix |

---

### 5.2 Performance Targets

| Metric | Target |
|--------|--------|
| Hook execution (pre-prompt) | < 50ms |
| Intent detection | < 100ms |
| Skill injection | < 200ms |
| Agent handoff | < 500ms |
| Full flow (simple task) | < 5s |

---

## 6. Extensibility

### Adding a New Skill

1. Create `skills/specializations/<domain>/SKILL.md`
2. Define triggers, entrypoint, outputs
3. Register in `config/skills-registry.yaml`
4. Add to routing rules in `config/routing.yaml`

### Adding a New Agent

1. Create `agents/specialists/<agent-name>/AGENT.md`
2. Define capabilities, protocols, handoffs
3. Register in `config/agents-registry.yaml`
4. Add to orchestrator's agent pool

### Adding a New Hook

1. Create `hooks/<type>/<hook-name>.yaml`
2. Define trigger, conditions, actions
3. Register in `config/hooks.yaml`
4. Enable in hook execution chain

---

## 7. Configuration

```yaml
# config/harness.yaml
harness:
  version: 1.0.0
  mode: standard  # standard | minimal | maximum
  
  intent_detection:
    enabled: true
    threshold: 0.7
    max_intents: 3
    
  skills:
    auto_invoke: true
    allow_cascading: true
    max_depth: 5
    
  agents:
    enabled: true
    parallel_execution: true
    max_concurrent: 3
    
  hooks:
    enabled: true
    execution_order: [security, requirements, architecture, testing, quality]
    
  knowledge_base:
    enabled: true
    cache_index: true
    preload_ka: [1, 2, 3]  # First 3 KAs preloaded
```
