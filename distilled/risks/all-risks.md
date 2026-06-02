# Risk Catalogs
> Threats and mitigations distilled from 30+ security references (OWASP, NIST, CIS, MITRE ATT&CK, web security books)

## Security Risks (OWASP Top 10 + extensions)

### A01 — Broken Access Control
- **Threat**: User accesses resources they shouldn't (IDOR, privilege escalation, missing auth checks)
- **Detection**: Authorization tests, penetration testing, log analysis
- **Mitigation**:
  - Default deny, explicit allow
  - Centralized authorization middleware
  - Test every endpoint with non-privileged user
  - Log all access decisions
  - Apply principle of least privilege

### A02 — Cryptographic Failures
- **Threat**: Weak/old crypto, no encryption, poor key management
- **Detection**: Dependency scan, code review, penetration testing
- **Mitigation**:
  - TLS everywhere (no HTTP)
  - AES-256 for symmetric, RSA-2048+ or EC-256+ for asymmetric
  - Use established libraries (don't roll your own)
  - Key rotation policy
  - Hash passwords with Argon2id (see `recipes/authentication.md`)

### A03 — Injection (SQL, NoSQL, LDAP, OS command, etc.)
- **Threat**: Untrusted input executed as code
- **Detection**: SAST, DAST, fuzzing
- **Mitigation**:
  - Parameterized queries (never string concatenation)
  - ORMs with proper escaping
  - Input validation (whitelist > blacklist)
  - Output encoding
  - Principle: input is guilty until proven innocent

### A04 — Insecure Design
- **Threat**: Architectural flaws that no code review can fix
- **Detection**: Threat modeling, design review, security architecture review
- **Mitigation**:
  - Threat model every new feature (STRIDE, PASTA)
  - Reference architectures for common patterns
  - Security in the design phase, not bolted on
  - Use secure-by-default frameworks (Django, Rails, Spring Security)

### A05 — Security Misconfiguration
- **Threat**: Default settings, debug mode in prod, open S3 buckets, exposed admin panels
- **Detection**: Configuration scanners, manual review
- **Mitigation**:
  - Hardened base images
  - Configuration as code (Terraform, Ansible, etc.)
  - Disable unused features
  - Principle of least privilege (services, users, networks)
  - Automated config scanning in CI

### A06 — Vulnerable & Outdated Components
- **Threat**: Known CVEs in libraries
- **Detection**: SCA tools (Snyk, Dependabot, npm audit, pip-audit, OWASP Dependency-Check)
- **Mitigation**:
  - Automated dependency updates (Dependabot, Renovate)
  - Pin versions, lock files
  - Subscribe to security advisories
  - Remove unused dependencies
  - Use LTS versions of major dependencies

### A07 — Identification & Authentication Failures
- **Threat**: Weak passwords, no MFA, session fixation, credential stuffing
- **Detection**: Auth testing, log analysis
- **Mitigation**:
  - See `recipes/authentication.md`
  - MFA everywhere
  - Rate limit on auth endpoints
  - Session regeneration on login
  - Account lockout
  - Use established auth (don't roll your own)

### A08 — Software & Data Integrity Failures
- **Threat**: Untrusted updates, CI/CD pipeline compromise, insecure deserialization
- **Detection**: Code review, supply chain analysis
- **Mitigation**:
  - Signed updates
  - Reproducible builds
  - Pinned dependencies with hashes
  - Secure CI/CD (isolated runners, secret management)
  - Use safe deserialization (JSON, not pickle for untrusted data)

### A09 — Logging & Monitoring Failures
- **Threat**: Breaches go unnoticed, can't investigate, can't respond
- **Detection**: Tabletop exercises, log audits
- **Mitigation**:
  - Comprehensive logging (auth, access, errors)
  - Centralized log aggregation
  - Real-time alerting on suspicious activity
  - Incident response plan and runbooks
  - Log retention policy

### A10 — Server-Side Request Forgery (SSRF)
- **Threat**: Attacker makes server fetch internal resources
- **Detection**: Network monitoring, log analysis
- **Mitigation**:
  - Whitelist allowed domains/IPs
  - Block private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8)
  - DNS resolution validation
  - Network segmentation

---

## Performance Risks

### Hot Path Code in Critical Section
- **Symptom**: Slow response, high CPU, timeout errors
- **Cause**: Algorithm in hot path not optimized, N+1 queries, sync I/O in async path
- **Mitigation**:
  - Profile before optimizing
  - Cache common queries
  - Use connection pooling
  - Async I/O for I/O-bound work
  - Lazy loading where appropriate

### Memory Leaks
- **Symptom**: OOM errors, growing memory usage
- **Cause**: Unclosed resources, accumulating collections, event listener leaks
- **Mitigation**:
  - Use context managers (`with` statements)
  - Weak references for caches
  - Monitor memory in production
  - Load testing with realistic durations

### Database Connection Exhaustion
- **Symptom**: "Too many connections" errors
- **Cause**: Connection leak, bursty load, oversized connection pool
- **Mitigation**:
  - Connection pooling with appropriate size
  - Statement timeouts
  - Transaction timeouts
  - Monitor active connection count

### Cache Stampede
- **Symptom**: Latency spike when cache expires, repeated backend load
- **Cause**: Many concurrent requests for the same uncached key
- **Mitigation**:
  - Cache pre-warming
  - Lock-based refresh (only one process refreshes)
  - Stale-while-revalidate pattern
  - Background refresh

---

## Maintainability Risks

### High Coupling
- **Symptom**: One change requires changes in many places
- **Cause**: No module boundaries, shared mutable state, no abstractions
- **Mitigation**:
  - Apply SOLID principles
  - Dependency injection
  - Module boundaries enforced by tests
  - Architecture fitness functions

### Low Cohesion
- **Symptom**: Class/module does many unrelated things
- **Cause**: Speculative inclusion, "kitchen sink" classes
- **Mitigation**:
  - SRP (Single Responsibility Principle)
  - Extract Class refactoring
  - Define what the class IS NOT

### Missing Tests
- **Symptom**: Fear of changing code, regressions
- **Cause**: No testing culture, time pressure, hard-to-test code
- **Mitigation**:
  - Test-first development
  - Quality gates in CI
  - Coverage requirements
  - Refactor for testability

### Outdated Dependencies
- **Symptom**: Security vulnerabilities, missing features, compatibility issues
- **Cause**: "Don't touch what works"
- **Mitigation**:
  - Automated updates (Dependabot, Renovate)
  - Quarterly dependency review
  - Deprecation policy
  - Migration plan for major version bumps

### Knowledge Silos (Bus Factor 1)
- **Symptom**: Only one person knows critical code
- **Cause**: No rotation, no documentation, no pair programming
- **Mitigation**:
  - Architecture Decision Records
  - Runbooks
  - Pair programming
  - Code review (every change reviewed by another)
  - "Lunch and learn" sessions

---

## Operational Risks

### Cascade Failures
- **Symptom**: One slow service makes everything slow
- **Cause**: Synchronous calls, no timeouts, no circuit breakers
- **Mitigation**:
  - Timeouts on every external call
  - Circuit breakers
  - Bulkheads (separate thread pools)
  - Graceful degradation
  - Fallback responses

### Runaway Resource Consumption
- **Symptom**: OOM, CPU spike, disk full
- **Cause**: Memory leak, unbounded queue, log explosion
- **Mitigation**:
  - Resource limits (ulimit, cgroups, K8s limits)
  - Rate limiting per user/IP
  - Bounded queues with backpressure
  - Log sampling

### Data Loss
- **Symptom**: Corrupted data, missing rows, lost files
- **Cause**: No backups, failed migration, hardware failure
- **Mitigation**:
  - Regular backups (automated, tested)
  - Backup verification (restore test)
  - 3-2-1 rule (3 copies, 2 media, 1 offsite)
  - PITR (Point-In-Time Recovery)
  - Soft delete + audit log

### Deployment Failures
- **Symptom**: Bad deploy, service down, rollback needed
- **Cause**: Manual steps, insufficient testing, race conditions
- **Mitigation**:
  - Automated deployment
  - Canary / blue-green / rolling
  - Feature flags for gradual rollout
  - Health checks + auto-rollback
  - Post-deploy verification

### Configuration Drift
- **Symptom**: Dev works, prod doesn't (or vice versa)
- **Cause**: Manual config changes, undocumented env vars
- **Mitigation**:
  - Infrastructure as code
  - Environment parity (Docker, K8s)
  - Config validation at startup
  - Config audit logs

### Insufficient Observability
- **Symptom**: "Is it broken? How broken? When did it break?"
- **Cause**: No metrics, no logs, no traces
- **Mitigation**:
  - RED metrics (Rate, Errors, Duration)
  - USE metrics (Utilization, Saturation, Errors) for resources
  - Distributed tracing
  - Structured logging
  - Dashboards
  - Alerts with actionable runbooks

### Alert Fatigue
- **Symptom**: Alerts ignored, real incidents missed
- **Cause**: Too many alerts, noisy alerts, alerts without context
- **Mitigation**:
  - Alert on SLO violations, not symptoms
  - Actionable alerts (link to runbook)
  - Severity levels
  - Review and prune quarterly
  - "Who wakes up for this?" rule

---

## Compliance Risks

### GDPR
- **Risk**: PII exposure, no consent, no right-to-be-forgotten
- **Mitigation**:
  - Data inventory
  - Consent management
  - Right-to-be-forgotten endpoint
  - Data Processing Agreement (DPA)
  - Data Protection Officer (DPO)
  - Privacy by design

### HIPAA (healthcare)
- **Risk**: PHI exposure, no audit log, no BAA
- **Mitigation**:
  - Encryption at rest and in transit
  - Access controls + audit logs
  - BAA with all vendors
  - Security risk assessment
  - Breach notification plan

### PCI-DSS (payments)
- **Risk**: Cardholder data exposure, no tokenization
- **Mitigation**:
  - Never store CVV
  - Tokenize card numbers (use Stripe, Adyen, etc.)
  - Network segmentation
  - Quarterly scans
  - Annual audit (SAQ or ROC)

### SOC 2
- **Risk**: No security controls documentation
- **Mitigation**:
  - Document all security policies
  - Implement access controls + monitoring
  - Annual audit
  - Continuous compliance monitoring
