# Hooks System Specification

## Overview

Le système de hooks permet d'intercepter et de modifier le flux d'exécution de Claude Code à différents points du cycle de traitement d'un prompt.

---

## Hook Types

### 1. pre-prompt Hooks

**Timing**: Avant que le prompt ne soit traité par le modèle

**Use Cases**:
- Injection de contexte pertinent (fichiers, documentation)
- Détection d'intents et routing automatique
- Validation de sécurité (SQL injection, XSS patterns)
- Ajout de checklists spécifiques au domaine

**Example Structure**:
```yaml
hook:
  id: pre-prompt-domain-detector
  trigger:
    event: prompt_submitted
  actions:
    - type: intent_detection
      model: semantic_analysis
      output: detected_intents[]
    - type: context_injection
      condition: intent_matches("security")
      source: security-engineering/owasp-top-10
    - type: routing_decision
      based_on: detected_intents
      targets:
        - skill: requirements-elicitation
          condition: intent == "requirement_gathering"
        - skill: architecture-design
          condition: intent == "architecture_planning"
```

---

### 2. post-prompt Hooks

**Timing**: Après génération de la réponse, avant retour à l'utilisateur

**Use Cases**:
- Validation de la réponse (complétude, format)
- Ajout de disclaimers ou warnings
- Formatage de sortie
- Logging et métriques

---

### 3. pre-task Hooks

**Timing**: Avant exécution d'une tâche spécifique (Read, Edit, Write, Bash, etc.)

**Use Cases**:
- Validation de chemin de fichier
- Vérification de permissions
- Préparation d'environnement
- Confirmation utilisateur pour actions destructives

---

### 4. post-task Hooks

**Timing**: Après exécution d'une tâche

**Use Cases**:
- Validation du résultat
- Mise à jour d'index
- Notifications
- Rollback si erreur

---

### 5. event Hooks

**Timing**: Sur événements spéciaux (commit, branch, merge, etc.)

**Use Cases**:
- Pre-commit validation
- Post-commit quality checks
- Branch naming enforcement
- Changelog generation

---

## Core Hook Implementations

### Hook 1: security-injection

```yaml
hook:
  id: pre-prompt-security-scan
  name: Security Context Injector
  trigger:
    events: [prompt_submitted]
    conditions:
      - pattern_match:
          patterns:
            - "sql"
            - "query"
            - "database"
            - "input"
            - "form"
            - "api"
            - "endpoint"
            - "user.*data"
            - "password"
            - "auth"
  actions:
    - type: inject_knowledge
      source: security-engineering/owasp
      selection: relevant_subset
    - type: inject_checklist
      category: security_validation
      items:
        - "[ ] SQL injection: parameterized queries used"
        - "[ ] Input validation: all inputs sanitized"
        - "[ ] XSS: output encoding applied"
        - "[ ] Auth: secure credential handling"
        - "[ ] Data: PII properly protected"
  continue: true
```

---

### Hook 2: requirements-auto-trigger

```yaml
hook:
  id: pre-prompt-requirements-detector
  name: Requirements Intent Auto-Trigger
  trigger:
    events: [prompt_submitted]
    conditions:
      - intent_match:
          intents:
            - requirement_gathering
            - requirement_analysis
            - requirement_specification
  actions:
    - type: inject_skill
      skill: requirements-elicitation
      condition: intent == "requirement_gathering"
    - type: inject_context
      context: |
        ## Requirements Engineering Context
        
        Based on SWEBOK v4 KA-1:
        - Elicitation: Techniques include interviewing, brainstorming, 
          prototyping, use case analysis
        - Analysis: Classify, prioritize, resolve conflicts
        - Specification: Document in appropriate format
        - Validation: Reviews, prototyping, simulation
  continue: true
```

---

### Hook 3: architecture-awareness

```yaml
hook:
  id: pre-prompt-architecture-context
  name: Architecture Decision Context
  trigger:
    events: [prompt_submitted]
    conditions:
      - pattern_match:
          patterns:
            - "architecture"
            - "design pattern"
            - "system structure"
            - "microservices"
            - "monolith"
            - "layers"
  actions:
    - type: inject_knowledge
      source: software-architecture/patterns
      selection: pattern_matching_user_query
    - type: inject_checklist
      category: architecture_review
      items:
        - "[ ] Quality attributes explicitly considered"
        - "[ ] Trade-offs documented"
        - "[ ] Stakeholder concerns addressed"
        - "[ ] Architecture views appropriate for audience"
  continue: true
```

---

### Hook 4: pre-commit-validator

```yaml
hook:
  id: event-pre-commit
  name: Pre-Commit Validation
  trigger:
    events: [git_pre_commit]
  actions:
    - type: execute
      command: |
        # Run pre-commit checks
        - syntax_validation
        - import sorting
        - formatting (prettier/black)
        - secret detection
        - large file check
    - type: block_if
      condition: secrets_detected == true
      message: "Secrets detected in commit. Aborting."
    - type: warning_if
      condition: files > 10
      message: "Large commit: consider splitting"
  continue: true
```

---

### Hook 5: test-awareness

```yaml
hook:
  id: pre-prompt-testing-context
  name: Testing Context Injector
  trigger:
    events: [prompt_submitted]
    conditions:
      - pattern_match:
          patterns:
            - "test"
            - "spec"
            - "verify"
            - "validate functionality"
            - "regression"
  actions:
    - type: inject_skill
      skill: testing-strategies
    - type: inject_checklist
      category: test_quality
      items:
        - "[ ] Test cases traceable to requirements"
        - "[ ] Edge cases covered"
        - "[ ] Mocking strategy defined"
        - "[ ] Test isolation verified"
        - "[ ] Coverage target met (if defined)"
  continue: true
```

---

## Hook Configuration Schema

```yaml
# config/hooks.yaml
hooks:
  enabled: true
  execution_order: [security, requirements, architecture, testing, quality]
  
  pre_prompt:
    - id: security-injection
      enabled: true
      priority: 1
    - id: requirements-auto-trigger
      enabled: true
      priority: 2
    - id: architecture-awareness
      enabled: true
      priority: 3
    - id: testing-context
      enabled: true
      priority: 4

  post_prompt:
    - id: response-validator
      enabled: true
    - id: completeness-checker
      enabled: true

  event:
    - id: pre-commit-validator
      enabled: true
    - id: branch-naming-enforcer
      enabled: true
```

---

## Injection Knowledge Sources

| Source | Hook | Content |
|--------|------|---------|
| `security-engineering/owasp` | security-injection | OWASP Top 10, secure coding practices |
| `software-architecture/patterns` | architecture-awareness | Pattern descriptions, trade-offs |
| `testing-strategies/techniques` | testing-context | Test techniques per context |
| `requirements-engineering/methods` | requirements-detector | Elicitation, analysis methods |
| `code-review/checklists` | post-prompt | Review checklists by language |

---

## Hook Development Guidelines

1. **Fast Execution** — Hooks must complete < 100ms
2. **Non-Blocking** — Most hooks should `continue: true`
3. **Idempotent** — Safe to run multiple times
4. **Fail-Safe** — Errors should not break main flow (unless blocking hook)
5. **Documented** — Each hook needs clear trigger/condition/action/continue

---

## Future Hook Ideas

- `pre-prompt-architecture-pattern-match` — Recommend patterns based on problem description
- `post-task-test-generation` — Auto-generate unit tests for new code
- `event-pr-review` — Automated PR review checklist
- `post-prompt-documentation-checker` — Ensure new code is documented
- `pre-task-dependency-check` — Verify dependencies before changes
