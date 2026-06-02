# Workflow Specifications — SWEBOK v4 Harness

## Workflow Catalog

### 1. Requirements Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 REQUIREMENTS WORKFLOW (KA-1)                    │
└─────────────────────────────────────────────────────────────────┘

[Start] → Identify Stakeholders → Plan Elicitation → Conduct Elicitation
    ↓
Document Raw Requirements → Analyze Requirements → Classify & Prioritize
    ↓
Resolve Conflicts → Specify Requirements → Validate with Stakeholders
    ↓
[Output: Requirements Specification + Acceptance Criteria]
    ↓
[Next: Architecture Workflow]
```

**Sub-Workflows**:
- `elicitation-subworkflow` — Stakeholder interviews, workshops
- `analysis-subworkflow` — Classification, conflict resolution
- `specification-subworkflow` — Document drafting
- `validation-subworkflow` — Review, prototyping, testing

---

### 2. Architecture Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 ARCHITECTURE WORKFLOW (KA-2)                     │
└─────────────────────────────────────────────────────────────────┘

[From: Requirements] → Understand Requirements → Define Architecture Views
    ↓
Select Architecture Pattern → Design Component Structure
    ↓
Define Interfaces → Document Architectural Decisions
    ↓
Evaluate Against Quality Attributes → Review with Stakeholders
    ↓
[Output: Architecture Description + ADRs]
    ↓
[Next: Design Workflow + Test Strategy]
```

---

### 3. Design Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 DESIGN WORKFLOW (KA-3)                         │
└─────────────────────────────────────────────────────────────────┘

[From: Architecture] → High-Level Design → Detailed Design
    ↓
Select Design Strategies → Apply Patterns → Create Design Descriptions
    ↓
Review Design → Analyze Quality Attributes
    ↓
[Output: Detailed Design Specification]
    ↓
[Next: Construction Workflow]
```

---

### 4. Construction Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 CONSTRUCTION WORKFLOW (KA-4)                     │
└─────────────────────────────────────────────────────────────────┘

[From: Design] → Setup Environment → Implement Components
    ↓
Apply Coding Standards → Write Unit Tests → Verify Build
    ↓
Static Analysis → Code Review → Integrate Components
    ↓
System Integration → [Output: Implemented System]
    ↓
[Next: Testing Workflow]
```

---

### 5. Testing Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 TESTING WORKFLOW (KA-5)                          │
└─────────────────────────────────────────────────────────────────┘

[Planning] → Strategy → Test Plan → Test Case Design
    ↓
[Execution] → Unit Tests → Integration Tests → System Tests
    ↓
[Evaluation] → Defect Reporting → Root Cause Analysis
    ↓
[Completion] → Test Report → Lessons Learned
```

**Test Levels**:
1. **Unit Testing** (KA-5.2.1)
2. **Integration Testing** (KA-5.2.2)
3. **System Testing** (KA-5.2.3)
4. **Acceptance Testing** (KA-5.2.4)

---

### 6. Maintenance Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 MAINTENANCE WORKFLOW (KA-6)                      │
└─────────────────────────────────────────────────────────────────┘

[Change Request] → Impact Analysis → Plan Modification
    ↓
Implement Change → Re-test → Deploy
    ↓
Update Documentation → [Output: Modified System]
```

---

## Cross-Cutting Workflows

### 7. Code Review Workflow

```
[Commit/PR] → Pre-Review Hook → Automated Checks (lint, format, secrets)
    ↓
[Notification] → Review Assignment → Review Execution
    ↓
[Feedback] → Author Updates → Re-review (if needed)
    ↓
[Approval] → Merge → Post-Review Hook
```

---

### 8. Spec-Driven Development Workflow

```
[User Need] → /speckit.specify → Create SPEC.md
    ↓
[speckit.plan] → Implementation Plan → Task Breakdown
    ↓
[Implementation] → /speckit.implement → Code + Tests
    ↓
[speckit.analyze] → Verification → Quality Gates
    ↓
[speckit.checklist] → Acceptance → Delivery
```

---

### 9. Quality Assurance Workflow

```
[Continuous] → Quality Monitoring → Metrics Collection
    ↓
[Analysis] → Quality Trends → Issues Identified
    ↓
[Action] → Process Improvement → Verification
```

---

### 10. Security Workflow

```
[Threat Modeling] → Identify Assets → Analyze Threats
    ↓
[Security Design] → Security Requirements → Security Architecture
    ↓
[Secure Implementation] → Secure Coding → Security Testing
    ↓
[Verification] → Penetration Testing → Vulnerability Assessment
```

---

## Workflow Triggers

| Trigger | Workflow |
|---------|----------|
| User describes new feature | Requirements → Architecture → Design → Construction |
| User submits code | Code Review → Testing |
| User requests change | Maintenance Workflow |
| Security concern raised | Security Workflow |
| Quality metrics degrade | Quality Assurance Workflow |
| /speckit.specify command | Spec-Driven Development |

---

## Workflow Selection Algorithm

```
1. Parse user intent
2. Match to workflow trigger
3. If multiple matches:
   - Check for explicit workflow naming
   - Use most specific match
   - Apply parallel execution if dependencies allow
4. Return workflow chain
```

---

## Workflow State Management

```yaml
state:
  requirements_workflow:
    current_step: specify_requirements
    steps_completed:
      - identify_stakeholders
      - plan_elicitation
      - conduct_elicitation
    steps_pending:
      - validate_requirements
      - baseline_requirements
    artifacts:
      - stakeholder_matrix.md
      - requirements_spec.md
      
  architecture_workflow:
    current_step: pattern_selection
    blocked_by:
      - requirements_workflow (not_baselined)
```

---

## Parallel Execution

Some workflows can execute in parallel:

```
Requirements Analysis (KA-1) ──────────────────┐
                                                │
Architecture Design (KA-2) ← Requirements ─────┤ (dependency)
                                                │
Test Strategy (KA-5) ← Architecture ────────────┼ (dependency)
                                                │
Security Design (KA-13) ← Requirements ─────────┤ (can be parallel)

Construction (KA-4) ← Design ← Architecture ────┘
Testing (KA-5) ← Construction ──────────────────┘
```
