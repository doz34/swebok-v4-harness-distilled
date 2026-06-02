# SWEBOK Phase Checklists

> Compiled from 60+ software engineering references. Each phase has a focused checklist of what must be true before moving to the next phase.

---

## P1 — Requirements

**Goal**: Specify WHAT, not HOW. Validate the problem before solving it.

### Discovery
- [ ] Stakeholders identified and accessible
- [ ] User personas defined (or stakeholder equivalents)
- [ ] Problem statement written in user terms
- [ ] Out-of-scope explicitly stated
- [ ] Success criteria defined (measurable)

### Requirements
- [ ] Functional requirements documented (what the system does)
- [ ] Non-functional requirements documented (perf, security, compliance, scalability)
- [ ] Constraints documented (budget, time, technology)
- [ ] Assumptions documented
- [ ] Risks identified and rated (likelihood × impact)

### Validation
- [ ] Stakeholders have signed off on requirements
- [ ] Conflicts / contradictions resolved
- [ ] Traceability matrix: requirement → design → code → test

### Anti-patterns
- ❌ Solution-first ("we'll use X") instead of problem-first
- ❌ "Just build it and they'll come"
- ❌ Requirements that prescribe implementation
- ❌ Unmeasurable success criteria ("fast", "user-friendly")

---

## P2 — Architecture

**Goal**: Define structure that supports all requirements without over-engineering.

### Decisions
- [ ] Architecture style chosen (monolith, microservices, serverless, etc.) — see `decision-trees/choose-architecture.json`
- [ ] Major components identified with clear responsibilities
- [ ] Interfaces defined between components
- [ ] Data flow documented (where data lives, how it moves)
- [ ] Cross-cutting concerns addressed: auth, logging, error handling, monitoring

### Quality attributes
- [ ] Performance budget (latency, throughput, payload size)
- [ ] Availability target (99.9%? 99.99%? 99.999%?)
- [ ] Scalability plan (vertical, horizontal, sharding)
- [ ] Security model (authn, authz, threat model)
- [ ] Compliance requirements (GDPR, HIPAA, SOC2, PCI-DSS)

### Documentation
- [ ] Architecture diagram (C4: context, container, component, code)
- [ ] ADRs for major decisions (Architecture Decision Records)
- [ ] Tech stack with rationale
- [ ] Data model sketch

### Anti-patterns
- ❌ Big Design Up Front (BDUF) for unknown future requirements
- ❌ Resume-Driven Development (RDD)
- ❌ Distributed Monolith (microservices without boundaries)
- ❌ Architecture astronaut (over-abstracted, no concrete plan)

---

## P3 — Design

**Goal**: Detail enough to start coding, abstract enough to allow change.

### Modules
- [ ] Each module has a single responsibility (SRP)
- [ ] Module interfaces are minimal and stable
- [ ] Dependencies are explicit (no hidden coupling)
- [ ] Cohesion is high; coupling is low

### Patterns
- [ ] Design patterns used where they fit, not because "experts use them"
- [ ] Antipatterns checked (see `antipatterns.json`)
- [ ] No reinvention of standard solutions (use libraries)

### Data
- [ ] Schema designed — see `recipes/database-schema.md`
- [ ] Data ownership clear (which module owns which data)
- [ ] Migrations planned (forward AND backward)

### API
- [ ] API design — see `recipes/api-design.md`
- [ ] Versioning strategy decided
- [ ] Error response format defined
- [ ] Authentication / authorization designed

### Anti-patterns
- ❌ Big Ball of Mud (no discernible structure)
- ❌ Anemic Domain Model (entities with no behavior)
- ❌ Speculative Generality (built for hypothetical needs)
- ❌ Design by Committee (Frankenstein)

---

## P4 — Estimation

**Goal**: Honest estimate of effort, risk, and dependencies.

### Scope
- [ ] Scope is well-defined (what's in, what's out)
- [ ] Dependencies identified (internal, external, third-party)
- [ ] Risks identified with mitigation plans
- [ ] Unknowns called out as spikes

### Estimate
- [ ] Estimate is range, not point (3-5 days, not 4 days)
- [ ] Estimate includes: design, code, test, review, deploy, monitor
- [ ] Estimate is from the people who'll do the work
- [ ] Confidence level stated

### Plan
- [ ] Milestones defined
- [ ] Critical path identified
- [ ] Buffer added (10-30% depending on novelty)
- [ ] Tracking in place (Jira, GitHub Projects, etc.)

### Anti-patterns
- ❌ Parkison's Law (work expands to fill time)
- ❌ "Just one more feature" (scope creep)
- ❌ Optimism bias ("we'll definitely hit the deadline")
- ❌ PERT syndrome (90% done, forever)

---

## P5 — Construction

**Goal**: Working code that meets requirements, with tests.

### Code
- [ ] Style guide followed (PEP 8, Google, Airbnb, etc.)
- [ ] No dead code (delete unused, comment-out is not a thing)
- [ ] No commented-out code (git remembers)
- [ ] No magic numbers / strings (use named constants)
- [ ] No deep nesting (early return, guard clauses)
- [ ] Functions are small (<20 lines typically)
- [ ] Names are meaningful (no `tmp`, `data`, `x`)

### Testing (Test-First or Test-Soon)
- [ ] Unit tests for business logic
- [ ] Integration tests for adapters
- [ ] Tests run fast (<5 min for the full suite)
- [ ] Tests are deterministic (no flake)
- [ ] Coverage tracked (target 80%+ for new code)
- [ ] Edge cases covered (empty, null, very large, unicode)

### Security
- [ ] Input validation at every boundary
- [ ] Output encoding (no XSS)
- [ ] No SQL string concatenation
- [ ] No secrets in code
- [ ] Dependencies scanned for vulnerabilities
- [ ] OWASP Top 10 reviewed

### Performance
- [ ] No obvious N+1 queries
- [ ] No obvious N² algorithms
- [ ] No unnecessary network calls
- [ ] No unnecessary allocations in hot paths

### Version control
- [ ] Small, atomic commits
- [ ] Clear commit messages (why, not what)
- [ ] Feature branches or trunk-based
- [ ] PR reviews required

### Anti-patterns
- ❌ Premature Optimization
- ❌ Copy-Paste Programming
- ❌ Magic Numbers
- ❌ Spaghetti Code
- ❌ God Class

---

## P6 — Verification

**Goal**: Prove the system works as specified.

### Test pyramid
- [ ] Many unit tests (70%)
- [ ] Some integration tests (20%)
- [ ] Few E2E tests (10%)
- [ ] Test strategy: see `decision-trees/choose-testing-strategy.json`

### Coverage
- [ ] Line/branch coverage tracked
- [ ] New code: >80% coverage
- [ ] Critical paths: 100% coverage
- [ ] Mutation testing for critical code

### Non-functional
- [ ] Load testing (does it meet perf budget?)
- [ ] Stress testing (what breaks at 10x load?)
- [ ] Security testing (OWASP ZAP, Burp)
- [ ] Chaos testing (kill a service, does it degrade gracefully?)
- [ ] Accessibility testing (WCAG)

### Quality gates
- [ ] All tests pass (zero flake)
- [ ] Linter passes
- [ ] Type checker passes
- [ ] No new warnings
- [ ] Coverage not decreased
- [ ] Security scan clean
- [ ] Performance budget met

### Anti-patterns
- ❌ Flaky tests (just re-run)
- ❌ Testing Through a Pinhole (only public API)
- ❌ Ice Cream Cone (too many E2E)
- ❌ Coverage theater (lines covered ≠ behavior tested)

---

## P7 — Deployment

**Goal**: Get the system to production safely and reliably.

### Pre-deploy
- [ ] All P6 quality gates passed
- [ ] Staging environment tested
- [ ] Rollback plan documented
- [ ] Feature flags in place (if applicable)
- [ ] Migrations are backward-compatible (expand-contract)
- [ ] Monitoring and alerting ready
- [ ] Runbook updated

### Deploy
- [ ] Deployment strategy chosen — see `decision-trees/choose-deployment.json`
- [ ] Canary / blue-green / rolling (depending on risk)
- [ ] Database migrations applied first
- [ ] Health checks pass
- [ ] Smoke tests pass

### Post-deploy
- [ ] Error rate within SLO
- [ ] Latency within budget
- [ ] No new alerts firing
- [ ] Logs flowing
- [ ] Metrics flowing

### Anti-patterns
- ❌ Big Bang Deploy (no rollout)
- ❌ Friday afternoon deploy
- ❌ Manual deploy steps (always automate)
- ❌ No rollback plan

---

## P8 — Maintenance

**Goal**: Keep the system running, fix bugs, evolve gracefully.

### Monitoring
- [ ] Metrics dashboarded
- [ ] Alerts on SLO violations
- [ ] Error tracking (Sentry, Rollbar, etc.)
- [ ] Distributed tracing (if distributed)
- [ ] Log aggregation

### Incident response
- [ ] On-call rotation
- [ ] Incident playbook
- [ ] Blameless postmortems
- [ ] Action items tracked
- [ ] Runbooks for common issues

### Bug fixes
- [ ] Regression test added BEFORE fix
- [ ] Root cause identified
- [ ] Fix is minimal and targeted
- [ ] Follow-up refactoring planned if the bug signals design issues

### Deprecation
- [ ] Old versions supported for a defined window
- [ ] Migration path provided
- [ ] Users notified in advance
- [ ] End-of-life date communicated

### Anti-patterns
- ❌ Fire Drill (reactive only, no preventive)
- ❌ "Just patch it" without root cause
- ❌ Squelching alerts (turning off noisy alerts)
- ❌ Living in P8 forever (no investment in P3 to reduce maintenance burden)

---

## P9 — Retirement

**Goal**: End the system's life cleanly, capturing lessons learned.

### Pre-retirement
- [ ] Users notified well in advance
- [ ] Migration path provided (or replacement identified)
- [ ] Data export available
- [ ] All data backed up (in case of late migrations)

### Retirement
- [ ] Read-only mode first
- [ ] Then shutdown
- [ ] Data retained per policy
- [ ] DNS / load balancer / monitoring removed
- [ ] Code archived (for forensic purposes)

### Post-retirement
- [ ] Postmortem / lessons learned
- [ ] Patterns identified for future projects
- [ ] Reusable code extracted
- [ ] Documentation updated (e.g. "this system no longer exists")

### Anti-patterns
- ❌ Zombie systems (no one knows who's responsible)
- ❌ Data loss during retirement
- ❌ Quiet retirement (users find out when it breaks)
