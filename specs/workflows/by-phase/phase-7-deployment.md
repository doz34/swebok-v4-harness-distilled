# Phase 7: Deployment Workflow Spec

> **Statut** : v2 — validé 2026-06-07 par le mainteneur (audit P7 clos via grille offline + 4 questions vague 1, verdict 🟢 dès la première conversation).
> **Changement vs v2-renum** : (1) **critère explicite de démarcation P6↔P7** inscrit dans P7 (P6 = "code va-t-il passer en prod sans casser" = staging iso-prod + tests + go/no-go ; P7 = "la prod tourne-t-elle correctement après le deploy" = release + monitoring + handoff), (2) **Nexus-Critic T1 casseur plan déploiement + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 OBLIGATOIRE** (3 invocations systématiques, comme P3/P4/P5/P6), (3) **hard cap 8k → 15k** (cohérence P3/P4/P5/P6, justifié par Nexus-Critic T1+T2+T3 obligatoire), (4) **7+4 livrables** maintenus (7 standard + 4 ajouts : changelog + runbook incidents + monitoring dashboard + audit trail), (5) XG-7.1-XG-7.10 (10 exit criteria), (6) section 5.5 transformée en **7 questions précises avec options AskUserQuestion** (vs vide en v2-renum), (7) section 7 comblée par **projection + cohérence P0/P1/P2/P3/P4/P5/P6 v2** (effort 5-15% projet, 4 frictions + 4 contournements, 3 risques dette orchestration), (8) UDL 7 éléments P7-spécifiques documentés, (9) audit des 4 failure modes Drew Breunig complet, (10) Stratégie rollout par défaut = big-bang (DTM par projet pour canary/blue-green), (11) Hotfix = pas de bypass (process complet obligatoire, escalade mainteneur si vital), (12) Couverture cas universelle adaptative (6 cas alignés P3/P4/P5/P6), (13) Tokens budget explicite 5k/8k/15k, (14) Pauses (compaction 60-70% du soft cap), (15) Conditions de sortie (checklist 11 critères). 4 décisions tranchées vague 1.
> **Changement vs structure antérieure** : v2-renum créée 2026-06-05 (renommage cascade P6→P7 après split P3). Pas de changement de fond vs v2-renum, refonte ciblée pour aligner sur P3/P4/P5/P6 v2 + intégrer la démarcation P6↔P7.
> **But** : consommer le go/no-go memo P6 + le closure report + le test plan validé pour amener le code de production-ready à production-running, avec rollback testé, monitoring actif, et handoff complet à P8 Operations — sans re-décider le go/no-go (escalade P6) ni définir le monitoring de long terme (escalade P8).

## Metadata

- **Phase**: 7
- **Name**: Deployment
- **Purpose**: Release software to production environments with proper validation, monitoring, and rollback capability; communicate to stakeholders; handoff to P8 Operations
- **Parallel Mode**: Hyperagent enabled (multi-agent justifié, F13 recherche 2026 — Nexus-DevOps-Lead lead + Nexus-DevOps + Nexus-Backend + Nexus-Frontend + Nexus-SM + Nexus-Critic en parallèle contrôlée)
- **Équivalent SWEBOK v4** : Software Configuration Management KA (release packaging) + aspects opérationnels de Software Construction (mise en production). Hors core KA SWEBOK direct.
- **Référentiels** : ISO/IEC/IEEE 12207:2017 (implementation process), ISO/IEC 27001 (conformité), NIST 800-53 (audit log prod), DevOps Handbook (Kim 2021), Continuous Delivery (Humble/Farley 2010)

---

## Mission (1 phrase)

> « Consommer le go/no-go memo P6 + le closure report + le test plan validé pour amener le code de production-ready à production-running, avec rollback testé, monitoring actif, communication stakeholders et handoff complet à P8 Operations — sans re-décider le go/no-go (escalade P6), ni redéfinir les NFR P2 (escalade P2), ni définir le monitoring de long terme (escalade P8). »

---

## Critère de démarcation P6 (Testing) vs P7 (Deployment)

> **Validation 2026-06-07** : le mainteneur a tranché pour un critère explicite, inscrit dans P6 ET P7. **P6 = "est-ce que le code va passer en prod sans casser" (staging iso-prod, 4 niveaux de test + 2 transverses + mutation, go/no-go). P7 = "est-ce que la prod tourne correctement après le deploy" (release, smoke tests post-deploy, monitoring actif, handoff).**

| Dimension | P6 Testing (déjà tranché en v2 finale) | P7 Deployment (cette spec) |
|-----------|----------------------------------------|------------------------------|
| **Question centrale** | **Est-ce que le code va passer en prod sans casser ?** | **Est-ce que la prod tourne correctement après le deploy ?** |
| **Lieu d'exécution** | **Staging iso-prod** (4 niveaux : intégration, système, acceptance, régression) + 2 transverses (perf, security) + mutation | **Production** (release, smoke tests post-deploy, monitoring actif, handoff) |
| **Périmètre fonctionnel** | Tests inter-modules, bout-en-bout, conformité NFR (perf, security, mutation) | Release packaging, infrastructure prod, communication stakeholders, handoff ops |
| **Décisions** | Stratégie de test, choix outils, plan d'exécution, critères go/no-go | Stratégie de rollout, choix feature flags, plan d'exécution deploy, critères handoff |
| **Activité dominante** | Tester (exécuter des tests) | Déployer (release + monitorer) |
| **Outputs typiques** | `go-no-go-decision-memo.md`, `test-closure-report.md`, `*-test-results.md`, `mutation-testing-report.md` | `deployment-plan.md`, `deployment-report.md`, `changelog.md`, `runbook.md`, `monitoring-dashboard.md`, `audit-trail.md`, `operations-documentation.md` |
| **Adversarial** | T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 (ruptures prod) | T1 casseur plan déploiement + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 (incidents prod) |
| **Agents typiques** | Nexus-QA-Lead (lead), Nexus-Backend/Frontend, Nexus-DevOps (env), Nexus-Security, Nexus-Performance, Nexus-Critic | Nexus-DevOps-Lead (lead), Nexus-DevOps, Nexus-Backend, Nexus-Frontend, Nexus-SM, Nexus-Critic |

**Règle simple** : si la décision impacte **un test, un défaut, ou un NFR P2 validé en staging** = P6. Si elle impacte **le release en prod, le monitoring actif, ou le handoff ops** = P7.

**Cas limite type** :
- "Exécuter les smoke tests post-deploy en prod" = **P7** (vérifier que la prod tourne). Mais "Définir la stratégie de test (quels smoke tests, quelles assertions)" = **P6** (extension naturelle du test plan).
- "Configurer le feature flag pour le rollout canary" = **P7** (release). Mais "Le feature flag est documenté dans les acceptance criteria" = **P2** (requirement).
- "Décider de rollback suite à un smoke test échoué" = **P7** (réflexe d'exécution, critère 6.4.A "rollback IMMÉDIAT, pas d'escalade, exécution"). Mais "Analyser pourquoi le smoke test a échoué (root cause)" = **P6** (analyse de défaut) puis escalade P5 (correction) si c'est un bug.
- "Communiquer la release aux stakeholders (release notes)" = **P7** (release packaging). Mais "Définir quels stakeholders notifier" = **P2** (requirement de communication).

**Conséquence opérationnelle sur P6 v2 finale** : aucune modification. P6 produit le go/no-go memo + le closure report, P7 les consomme. Le go/no-go P6 est **une entrée** de P7, pas un sujet de re-décision.

**Conséquence opérationnelle inverse** : si P7 détecte qu'une décision impacte l'organisation interne du code, **elle escalade P5**. Si P7 détecte qu'une décision impacte les NFR P2 (perf cible, security target), **elle escalade P2**. Si P7 détecte qu'une décision impacte le go/no-go (par exemple un défaut non détecté en P6 émerge en prod), **elle escalade P6** (analyse) puis P5 (fix). Si P7 détecte qu'une décision impacte le monitoring de long terme (alerte, dashboard, runbook), **elle escalade P8** (operations).

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-7.1 | Phase 6 testing complete | Test closure report | Approved + signed (go-no-go-decision-memo.md P6) |
| EG-7.2 | Go/no-go decision signed | Go/no-go memo (P6 XG-6.8) | "GO" formel signé par mainteneur + sponsor |
| EG-7.3 | Defect escape rate acceptable | Defect report P6 | Escape rate ≤2% (defects post-go) |
| EG-7.4 | Test traceability complete | TTM (P6 XG-6.5) | 100% acceptance criteria P2 tracés par test PASS |
| EG-7.5 | NFR P2 validés | Performance + security test reports (P6 XG-6.6/6.7) | 100% NFR P2 validés |
| EG-7.6 | Mutation testing passed | Mutation report (P6 XG-6.3) | Mutation score ≥70% (adaptatif par profil, défaut grillé) |
| EG-7.7 | Deployment plan approved | DP document sign-off | ≥2 approvers signed (mainteneur + sponsor) |
| EG-7.8 | Production environment prepared | Env health check | All systems operational (CPU, RAM, réseau, DB, cache) |
| EG-7.9 | Rollback procedures documented + tested | RB procedures + test result | Reviewed, approved, AND test de rollback exécuté en staging |
| EG-7.10 | Deployment window scheduled | Schedule confirmation | Window confirmée avec ops + stakeholders |
| EG-7.11 | Conformité acceptance criteria P2 vérifiée | Matrice AC → test (P6 XG-6.10) | 100% AC P2 tracés et validés |
| EG-7.12 | Conformité ADRs P3 vérifiée | Matrice ADR → module (P4 XG-4.7) + impact déploiement | Chaque ADR P3 a une note d'impact déploiement (config requise, feature flag, migration) |
| EG-7.13 | Conformité DDS P4 vérifiée | Matrice DDS → code (P5 XG-5.7) | 100% DDS P4 tracés par fichier de code déployé |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers Phase 6 (Testing) remediation (escalade pour test/rework) or Phase 2 (Requirements) remediation (escalade pour NFR).

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-7.1 | All deployment components released | Deployment status | 100% composants déployés (services, config, migrations, assets) |
| XG-7.2 | Smoke tests post-deploy passed | Smoke test results | 100% smoke tests pass en prod (latence, fonctionnalité, intégrité DB) |
| XG-7.3 | Rollback test passed | Rollback test report | Rollback testé en staging ET exécutable en < 5 min en prod |
| XG-7.4 | Monitoring active | Monitoring dashboard | 100% alertes configurées et testées (P8 handoff interface) |
| XG-7.5 | User-facing communication published | Release notes + changelog | Publiés (internes + externes selon stakeholders P2) |
| XG-7.6 | Handoff documentation complete | Handoff checklist | 100% items complete (runbook, ops doc, user doc, escalation paths) |
| XG-7.7 | Deployment report approved | Report sign-off | Formal approval (mainteneur + sponsor + ops lead) |
| XG-7.8 | Audit trail complete | Audit log | Trace de toutes les actions de déploiement (who, what, when, why) |
| XG-7.9 | UDL 7 éléments P7-spécifiques loggés | UDL set | 100% loggés dans `.swebok_state.db` (table `udl_p7`) |
| XG-7.10 | Conformité NFR P2 vérifiée en prod | NFR check prod | 100% NFR P2 mesurables (perf p95, error rate, availability) toujours en cible |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed to P8 Operations. Any `FAIL` triggers immediate rollback (XG-7.3, critère 6.4.A "rollback IMMÉDIAT, pas d'escalade, exécution") ou escalation mainteneur.

**XG-7.4 — Adaptativité par profil projet (note)** : pour les projets compliance/sécurité, le monitoring peut être relevé (alertes P0 24/7, on-call obligatoire, audit log immutable). Pour les projets R&D/POC, il peut être allégé (alertes best-effort, pas d'on-call).

**XG-7.10 — Note** : les NFR P2 sont **re-vérifiés en prod** (et pas seulement staging iso-prod P6) car le déploiement peut introduire un drift (env drift, données prod différentes, charge prod).

---

## Transition Criteria to Phase 8 (Operations)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Deployment validated | Nexus-DevOps-Lead | Operations Lead | Health check prod passé (XG-7.2) |
| Handoff documented | Deployment Lead | Ops Lead | Handoff memo signé + checklist 100% (XG-7.6) |
| Monitoring active | Nexus-DevOps | Ops Lead | Monitoring dashboard accessible + alertes testées (XG-7.4) |
| Runbook delivered | Nexus-DevOps-Lead | Ops Lead | Runbook signé + testé en simulation d'incident |
| Support team confirmed | Nexus-SM | Operations | Team briefé et prêt (training handoff) |
| SLAs handed off | Project Lead | Ops Lead | SLA doc transféré (défini P2) |
| Audit trail transmitted | Nexus-DevOps-Lead | Compliance Lead | Audit log prod complet (XG-7.8) |
| User documentation delivered | Nexus-Docs (ou Nexus-SM) | End users | User doc publié (XG-7.5) |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_7_COMPLETE` only when all transition criteria verified with formal evidence (deployment report + handoff memo signés).

---

## Key Activities

### Activity 7.1: Deployment Planning
- Définir la stratégie de rollout (défaut = big-bang, DTM par projet pour canary/blue-green)
- Créer les scripts de déploiement (IaC : Terraform, Helm, Ansible, Kustomize)
- Préparer les procédures de rollback (testées en staging avant prod)
- Planifier la fenêtre de déploiement (impact business, équipe d'astreinte)
- Coordonner avec l'équipe ops (Nexus-SM brief)
- Documenter le feature flag rollout si stratégie progressive
- Vérifier la conformité ADRs P3 (chaque ADR a une note d'impact déploiement)
- Identifier les migrations de schéma DB (forward + rollback)
- Identifier les feature flags (kill switch opérationnel pour chaque feature majeure)

### Activity 7.2: Environment Preparation
- Provisionner l'infrastructure prod (si greenfield) ou vérifier l'existante
- Configurer l'env prod (vars d'env, secrets via vault, certificats TLS)
- Exécuter les pre-deployment checks (santé des services upstream, capacité DB, cache warmed)
- Valider les procédures de backup (snapshot DB avant deploy)
- Configurer le monitoring et les alertes (AVANT le deploy, pas après)
- Configurer le feature flag system (kill switch opérationnel)
- Tester le rollback en staging (critère EG-7.9)

### Activity 7.3: Deployment Execution
- Exécuter les scripts de déploiement (ordre : read-only first, then mutable, then critical)
- Effectuer les health checks (services up, DB connectée, cache warmed)
- Vérifier la fonctionnalité système (smoke tests post-deploy en prod, XG-7.2)
- Monitorer les métriques de déploiement (latence, error rate, throughput)
- Activer les feature flags selon la stratégie (progressive ou big-bang)
- Exécuter les migrations DB (forward, puis vérifier intégrité)
- Documenter toutes les actions dans l'audit trail (XG-7.8)

### Activity 7.4: Handoff and Documentation
- Compléter la documentation ops (runbook d'incidents probables, XG-7.6)
- Brief-er l'équipe ops (Nexus-SM training handoff, 30 min)
- Livrer la documentation utilisateur (release notes, changelog, FAQ)
- Mener la review post-deployment (leads + ops + sponsor, 1h)
- Activer le canal de communication post-deploy (Slack/Teams ops room)
- Vérifier que les SLAs sont en place et monitorés (P8 handoff)

### Activity 7.5: Adversarial Validation (Nexus-Critic — OBLIGATOIRE, comme P3/P4/P5/P6)
- **T1 casseur plan de déploiement** : Nexus-Critic relit le plan, cherche des failles (étapes manquantes, dépendances non documentées, scripts dangereux, manque de feature flag). Cible : `deployment-plan.md` + `deployment-scripts.md`.
- **T2 conformité go/no-go P6 + NFR P2 + ADRs P3** : Nexus-Critic vérifie que le déploiement respecte le go/no-go P6, les NFR P2, et les ADRs P3. Cible : `deployment-plan.md` vs `go-no-go-decision-memo.md` + NFR doc + ADR doc.
- **T3 prédiction aval P8** : Nexus-Critic prédit ce qui va casser en P8 Operations (monitoring insuffisant, alertes mal calibrées, runbook incomplet, dette de configuration). Cible : `runbook.md` + `monitoring-dashboard.md` + dette configuration.

---

## Responsible Agents

| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordonne les tâches de déploiement parallèles (scripts + monitoring + handoff) |
| **Nexus-DevOps-Lead (lead)** | Lead déploiement global, sign-off deployment report, handoff P8 |
| Nexus-DevOps | Exécution scripts, infrastructure prod, monitoring setup |
| Nexus-Backend | Support déploiement backend, migrations DB, résolution incidents post-deploy |
| Nexus-Frontend | Support déploiement frontend, CDN, assets statiques |
| Nexus-SM | Brief ops team, handoff, communication stakeholders |
| **Nexus-Critic (5e agent obligatoire — décision mainteneur 2026-06-07)** | **T1 casseur plan déploiement + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 — TOUS OBLIGATOIRES** (3 invocations systématiques, comme P3/P4/P5/P6) |

**Concurrency** : **multi-agent justifié** (F13 recherche 2026 — déploiement = read-heavy parallèle sur config + monitoring + handoff + communication, disjoint tools). 3-5 sub-agents en parallèle par activité, jamais plus. **Nexus-Critic = 3 invocations systématiques** (T1 casse le plan, T2 vérifie la conformité go/no-go + NFR + ADRs, T3 prédit les incidents P8). Coût additionnel ~4.5k tokens, justifié par le hard cap 15k (cohérence P3/P4/P5/P6). **Note : contrairement à la suggestion initiale "P7 single-agent justifié", le mainteneur a tranché T1+T2+T3 obligatoire le 2026-06-07, ce qui justifie le passage en multi-agent.**

**Patterns adversariaux T1/T2/T3 (rappel)** :
- **T1 (casseur plan)** : Nexus-DevOps-Lead propose le plan, Nexus-Critic casse (cherche les failles). Cible : `deployment-plan.md`, `deployment-scripts.md`.
- **T2 (spec-compliance)** : Nexus-Critic vérifie conformité go/no-go P6 + NFR P2 + ADRs P3 (matrice ADR → déploiement, symétrique à matrice ADR → module P4 XG-4.7). Cible : `deployment-plan.md` vs sources de vérité.
- **T3 (conséquentialiste)** : Nexus-Critic prédit ce qui va casser en P8 (monitoring insuffisant, alertes mal calibrées, dette de configuration, runbook incomplet). Cible : `runbook.md` + `monitoring-dashboard.md`.

**Isolation des contextes (ACI stratégie §4.5)** : Nexus-Critic ne voit pas le prompt système des producteurs. Chaque rôle adversarial a un contexte distinct, sinon les "adversaires" se laissent influencer par le contexte partagé.

---

## Required Skills

- `nexus-devops`: Déploiement, IaC, monitoring setup
- `nexus-devops-lead`: Lead déploiement, handoff P8, sign-off
- `nexus-backend`: Support déploiement backend, migrations DB
- `nexus-frontend`: Support déploiement frontend, CDN, assets
- `nexus-sm`: Brief ops team, handoff, communication stakeholders
- `nexus-docs`: Documentation ops + user (release notes, runbook)
- `speckit-qa`: Vérification post-deploy, smoke tests automatisés
- `nexus-critic`: Adversarial validation (T1 casseur plan + T2 conformité go/no-go + NFR + ADRs + T3 aval P8) — **OBLIGATOIRE** (3 invocations)

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-deployment-complete` | Exit criteria met (XG-7.1-XG-7.10) | Triggers Phase 8 (Operations) initiation |
| `deployment-plan-approved` | Deployment planning done (Activity 7.1) | Enables env preparation |
| `env-prepared` | Environment health check passed (EG-7.8) | Enables deployment execution |
| `rollback-tested` | Rollback test passed en staging (EG-7.9) | Confirme capacité de rollback |
| `deployment-executed` | Deployment done | Updates deployment status |
| `smoke-tests-post-deploy-passed` | Smoke tests 100% pass (XG-7.2) | Confirme prod fonctionnelle |
| `monitoring-active` | Monitoring + alertes configurés (XG-7.4) | Confirme handoff P8 possible |
| `runbook-delivered` | Runbook signé et testé (XG-7.6) | Confisme handoff ops |
| `deployment-verified` | Verification passed | Confirms production readiness |
| `operations-handoff-complete` | Handoff done (tous transition criteria) | Transitions to operations |
| `t1-plan-casseur-passed` | T1 Nexus-Critic passé | Confirme robustesse du plan |
| `t2-conformity-go-nfr-adr-verified` | T2 conformité vérifiée | Confime conformité go/no-go + NFR + ADRs |
| `t3-p8-prediction-logged` | T3 prédiction faite | Snapshot pour P8 |
| `udl-p7-logged` | 7 éléments UDL loggés | Snapshot pour phases suivantes |
| `audit-trail-complete` | Audit log complet (XG-7.8) | Conformité compliance |

---

## Artifacts Produced

| Artifact | Description | Location | Format |
|----------|-------------|----------|--------|
| `deployment-plan.md` | Stratégie de rollout (défaut big-bang), schedule, fenêtre, dépendances | `specs/workflows/by-phase/phase-7-deployment/` | md |
| `deployment-scripts.md` | Scripts automatisés (IaC : Terraform, Helm, Ansible) | `specs/workflows/by-phase/phase-7-deployment/` | md + scripts versionnés git |
| `rollback-procedures.md` | Procédures de rollback (testées en staging) | `specs/workflows/by-phase/phase-7-deployment/` | md |
| `environment-config.md` | Configuration prod (vars d'env, secrets, certificats) | `specs/workflows/by-phase/phase-7-deployment/` | md + IaC |
| `deployment-report.md` | Rapport d'exécution (étapes, métriques, incidents) | `specs/workflows/by-phase/phase-7-deployment/` | md |
| `operations-documentation.md` | Guide ops (procédures courantes, escalade) | `specs/workflows/by-phase/phase-7-deployment/` | md |
| `user-documentation.md` | Guide utilisateur (release notes, FAQ) | `specs/workflows/by-phase/phase-7-deployment/` | md |
| `changelog.md` (livrable ajouté) | Changelog versionné (semver, breaking changes) | `specs/workflows/by-phase/phase-7-deployment/` | md (Keep a Changelog) |
| `runbook.md` (livrable ajouté) | Runbook d'incidents probables (top 5) | `specs/workflows/by-phase/phase-7-deployment/` | md |
| `monitoring-dashboard.md` (livrable ajouté) | Dashboard de monitoring (métriques + alertes) | `specs/workflows/by-phase/phase-7-deployment/` | md + JSON (config alertes) |
| `audit-trail.md` (livrable ajouté) | Trace de toutes les actions de déploiement (compliance) | `specs/workflows/by-phase/phase-7-deployment/` | md + JSON (machine-parse) |

**Format de stockage** :
- Specs narratives : md (lecture humaine)
- Scripts : git versionné (exécutable, auditable)
- Config : IaC (Terraform, Helm, Kustomize)
- Audit trail : JSON (machine-parse) + md (synthèse)
- Monitoring : JSON (config alertes Prometheus/Datadog) + md (dashboard)

**Convention de nommage** :
- Specs narratives : `${livrable}.md`
- Scripts : `scripts/${phase}/${action}.sh` ou équivalent IaC
- Config : `infra/${env}/${component}.tf|yaml`
- Audit trail : `audit-trail.md` + `audit-trail.json`

**Localisation** : tous dans `specs/workflows/by-phase/phase-7-deployment/`.

---

## Format des fichiers (triple différencié, aligné P3/P4/P5/P6 v2)

| Type de livrable | Format primaire | Format secondaire | Standard |
|------------------|------------------|-------------------|----------|
| **Specs narratives** (deployment-plan, deployment-report, rollback-procedures, ops-doc, user-doc, changelog, runbook) | md (lecture humaine) | — | — |
| **Scripts de déploiement** | Scripts versionnés git | — | Terraform, Helm, Ansible, Kustomize |
| **Config prod** | IaC | — | Terraform, Helm, Kustomize |
| **Monitoring dashboard** | md (résumé) | JSON (config alertes) | Prometheus, Grafana, Datadog |
| **Audit trail** | md (synthèse) | JSON (machine-parse) | HMAC chain (Cossack Labs 2025) |

**Convention de nommage** :
- Specs narratives : `${livrable}.md`
- Scripts : `scripts/deploy/${action}.sh` ou IaC
- Config : `infra/prod/${component}.tf|yaml`
- Monitoring : `monitoring-dashboard.md` + `alerts-config.json`
- Audit trail : `audit-trail.md` + `audit-trail.json`

**Localisation** : tous dans `specs/workflows/by-phase/phase-7-deployment/`.

---

## Hyperagent Parallel Processing

```
parallel_tasks:
  - task: infrastructure_preparation
    agents: [Nexus-DevOps, Nexus-DevOps-Lead]
    sync: false

  - task: backend_deployment
    agents: [Nexus-Backend, Nexus-DevOps]
    sync: false

  - task: frontend_deployment
    agents: [Nexus-Frontend, Nexus-DevOps]
    sync: false

  - task: monitoring_setup
    agents: [Nexus-DevOps, Nexus-SM]
    sync: false

  - task: documentation_and_handoff
    agents: [Nexus-SM, Nexus-Docs]
    sync: false

  - task: audit_trail_recording
    agents: [Nexus-DevOps-Lead]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après parallel):
  - task: t1_casseur_plan_deploiement
    agents: [Nexus-Critic]
    target: deployment-plan.md + deployment-scripts.md
    sync: true

  - task: t2_conformite_go_nfr_adr
    agents: [Nexus-Critic]
    target: deployment-plan.md vs go-no-go-decision-memo.md P6 + NFR P2 + ADRs P3
    sync: true

  - task: t3_prediction_p8
    agents: [Nexus-Critic]
    target: runbook.md + monitoring-dashboard.md + dette configuration
    sync: true

reduction: "Nexus-DevOps-Lead synthesizes all into deployment-report.md + handoff P8"
```

---

## Refus catégoriques (7)

La phase P7 **refuse** de :
1. **Pas de re-décision du go/no-go** (escalade P6 — règle de démarcation ; P7 ne ré-ouvre pas le go/no-go P6)
2. **Pas de redéfinition des NFR P2** (escalade P2 — toute déviation NFR P2 = escalade P2)
3. **Pas de modification du code de production** (escalade P5 — règle de démarcation ; P7 = release, pas fix)
4. **Pas de déploiement sans rollback testé** (EG-7.9 obligatoire)
5. **Pas de déploiement avec défauts critiques ouverts** (P6 XG-6.4 = ≤1 critical ouvert)
6. **Pas de skip de monitoring** (XG-7.4 obligatoire — alertes en place AVANT le deploy)
7. **Pas de hotfix bypass** (process complet obligatoire, y compris pour hotfix urgent ; escalade mainteneur si urgence vitale)
8. **Pas de feature flags oubliés** (chaque feature majeure = kill switch opérationnel)
9. **Pas de secrets en clair dans la config** (vault obligatoire, scan pre-deploy)
10. **Pas de "Friday deploy"** (pas de déploiement vendredi 17h, sauf urgence avec escalade mainteneur + astreinte)

---

## Critères d'échec (4) et d'abandon (6 + temps)

### Critères d'échec (déclenchent une action immédiate)
1. **Smoke tests échouent en prod** → rollback IMMÉDIAT (pas d'escalade, exécution, XG-7.3 + refus 5)
2. **Handoff incomplet** → bloquer la transition vers P8 (XG-7.6 obligatoire)
3. **Incident post-deploy** → rotation P8 Operations (P8 = owner du monitoring et de la réponse incident)
4. **Health checks dégradés** → escalade ops (smoke tests partiels, latence > NFR P2)

### Critères d'abandon (l'agent abandonne et prévient le mainteneur si)
1. Rollback test échoue en staging (escalade mainteneur, redéfinir procédure)
2. Env prod non préparé après 3 itérations (escalade Nexus-DevOps + mainteneur)
3. Smoke tests post-deploy échouent + rollback échoue (escalade mainteneur, CRITIQUE)
4. Feature flag système non opérationnel (escalade mainteneur, kill switch indispensable)
5. Migration DB échoue (escalade Nexus-Backend, rollback schema)
6. Monitoring alertes non configurables (escalade Nexus-DevOps + P8)
7. Dépassement de 35 min sans avancée claire (escalade mainteneur, redécoupage)

---

## Tokens budget

- **Base** : 5k tokens
- **Soft cap** : 8k tokens (alerte, compaction 60-70% = 5.6k)
- **Hard cap** : 15k tokens (compactage forcé + abort)

Multi-agent justifié (F13 recherche 2026) : 5 sub-agents en parallèle (DevOps-Lead + DevOps + Backend + Frontend + SM) × ~1k chacun = 5k base théorique. Cap 15k hard pour absorber les validations adversariales T1+T2+T3 obligatoires (Nexus-Critic en mode rotation sur les 3 patterns, comme P3/P4/P5/P6 — décision mainteneur 2026-06-07). **Justification du passage 3k/5k/8k → 5k/8k/15k** : Nexus-Critic T1+T2+T3 obligatoire = 3 invocations × ~1.5k = 4.5k additionnel, ce qui sature le budget 8k en nominal. 15k = marge de sécurité pour absorber les validations adversariales complètes, en cohérence avec P3 Architecture, P4 Design, P5 Implementation, P6 Testing (5k/8k/15k). **Note : le mainteneur a tranché 2026-06-07 pour T1+T2+T3 obligatoire en P7, ce qui justifie ce budget plus large que la suggestion initiale "single-agent justifié 3k/5k/8k" — la cohérence P3-P6 prime sur l'économie de tokens.**

**Note** : P7 devient 5e phase la plus large (ex-aequo avec P3, P4, P5, P6). Acceptable car P7 = phase critique de mise en prod, où les erreurs sont visibles publiquement et où le sur-coût est compensé par la qualité (plan robuste, conformité go/no-go + NFR + ADRs vérifiée, monitoring actif, handoff complet).

---

## Pauses

Toutes les 5 actions : compaction checkpoint à 60-70% du soft cap (5.6k tokens, F8 recherche 2026). Compaction sélective : garder les décisions et les étapes de déploiement, drop les logs verbeux (résumer les étapes OK, garder les incidents en détail, AP7 recherche 2026).

**Pre-hydrate obligatoire** (F7 recherche 2026 — 60% du 1er tour = retrieval) : au début de P7, charger dans le hot_context (`.swebok_state.db`) la slice suivante :
- go-no-go-decision-memo.md (P6)
- test-closure-report.md (P6)
- defect-report.md (P6)
- Liste des modules à déployer (pointeurs vers `source-code/` P5)
- Acceptance criteria P2 (pointeurs vers SRS P2)
- NFR P2 (perf + security + observability)
- ADRs P3 (matrice ADR → module, XG-4.7) + impact déploiement
- DDS P4 (matrice DDS → code, XG-5.7)
- Environnements prod disponibles (vars, secrets, certificats)
- Historique des incidents similaires (cross-deploy memory)

Sans ce pre-hydrate, 60% du budget du 1er tour est consommé en retrieval, ce qui sature le soft cap en nominal.

---

## Couverture corpus (état 2026-06-06)

- **73% de couverture** — P7 = phase la mieux couverte des phases restantes (après P5 100% et P3 100%)
- **11 livres canoniques** (vs 17 totaux) sur ~15 recommandés = 73%
- **8 livres Mac Studio** : Security Architecture for Hybrid Cloud, Serverless Development on AWS, Security and Microservice Architecture on AWS, Continuous Deployment (Servile), Practical Cloud Security, Cloud Native Security Cookbook, etc.
- **3 New Books** : Continuous Integration vs Delivery vs Deployment 2e (2022), Beyond the Phoenix Project (Kim 2019), The Phoenix Project (Kim 2013)
- **5 Standards NIST/OWASP** : NIST 800-145, 800-190, 800-204, SSDF 800-218, 800-52r2
- **1 Open-access** : TLCL — The Linux Command Line
- **4 lacunes critiques** : Humble/Farley Continuous Delivery (2010), DevOps Handbook 2nd (Kim 2021), Phoenix Project Graphic Novel (2018), Duvall Continuous Integration (2007)
- **Décision mainteneur 2026-06-06** : 73% suffit pour cadrage, batch d'acquisition ultérieur (action P1-N roadmap).

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :

1. **Greenfield from-scratch** : premier déploiement, infrastructure à provisionner, big-bang acceptable (audience limitée), monitoring basique
2. **Maintenance legacy** : déploiement sur infra existante, canary ou blue-green recommandé, monitoring renforcé (régression visible)
3. **Projet interne** (équipe, gouvernance légère) : big-bang acceptable, monitoring léger, release notes internes
4. **Projet externe client** : canary ou blue-green recommandé, monitoring renforcé, release notes externes, communication clients
5. **Compliance-driven** (finance, santé, défense) : blue-green ou canary obligatoire, audit log immutable (XG-7.8 renforcé), release notes signées, monitoring 24/7
6. **R&D / exploration** : big-bang acceptable, monitoring best-effort, release notes internes uniquement

---

## UDL — 7 éléments P7-spécifiques

> **Validation 2026-06-07** : 7 éléments P7-spécifiques (aligné P3, P4, P5, P6).

| Élément | Description | Exemple |
|---------|-------------|---------|
| **Deployment strategy chosen** | Stratégie de rollout retenue (big-bang, canary, blue-green) + rationale | "Big-bang retenu (projet interne, audience 50 users, risque faible, escalade feature flag si incident)" |
| **Rollback tested** | Résultat du test de rollback en staging (durée, succès) | "Rollback testé en staging : 3min12s pour rollback complet, 100% services restaurés, dry-run OK" |
| **Smoke test passed** | Résultat des smoke tests post-deploy en prod (par smoke test) | "SMK-001 health check = PASS (200ms), SMK-002 login = PASS (180ms), SMK-003 checkout = PASS (320ms)" |
| **Monitoring active** | Alertes configurées et testées (P8 handoff interface) | "Alerte latency_p95 > 200ms = active, alerte error_rate > 1% = active, alerte disk_usage > 80% = active (toutes testées à 14h32)" |
| **Handoff documentation** | Ops handoff complet (checklist 100%) | "Handoff Nexus-SM → Ops Lead = signé 2026-06-15 16h, 100% checklist OK (runbook, ops doc, training, escalation paths)" |
| **User-facing communication** | Release notes publiées (internes + externes selon stakeholders) | "Release notes v2.3.0 publiées sur Confluence + envoyées à 250 clients (mailing list), changelog GitHub release créé" |
| **Audit trail** | Trace de toutes les actions de déploiement (who, what, when, why) | "Audit trail : 47 actions loggées (5 scripts, 12 health checks, 8 feature flags, 15 smoke tests, 7 handoffs), HMAC chain vérifié" |

Stockés dans `.swebok_state.db` (table `udl_p7`) et consultables via Consultation Envelope (A1) par P8 Operations.

---

## Conditions de sortie (passage à P8)

Le mainteneur valide avec une **checklist à 100%** (11 critères) :
- [ ] `deployment-plan.md` existe (stratégie + schedule, sign-off)
- [ ] `deployment-scripts.md` existe (scripts versionnés git, IaC)
- [ ] `rollback-procedures.md` existe (testé en staging, exécution < 5min)
- [ ] `environment-config.md` existe (config prod, vars, secrets, certificats)
- [ ] `deployment-report.md` existe (étapes, métriques, incidents, sign-off)
- [ ] `operations-documentation.md` existe (procédures ops, escalade)
- [ ] `user-documentation.md` existe (release notes, FAQ)
- [ ] `changelog.md` existe (semver, breaking changes, format Keep a Changelog)
- [ ] `runbook.md` existe (top 5 incidents probables, procédures de réponse)
- [ ] `monitoring-dashboard.md` existe (métriques + alertes configurées et testées)
- [ ] `audit-trail.md` existe (trace complète, HMAC chain vérifié)
- [ ] UDL 7 éléments loggés dans `.swebok_state.db`

Pas de feu vert séparé — les documents font foi.

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-07

### Mode 1 — Poisoning (Empoisonnement)
**Risque en P7** : un plan de déploiement qui semble complet mais omet une étape critique (par exemple, oublier la migration DB), ou un script malicieux/corrompu qui contamine l'env prod.

**Mitigations spec v2** :
1. Rollback testé en staging AVANT prod (EG-7.9) — détecte les omissions
2. T1 casseur plan de déploiement (Nexus-Critic, 3 invocations systématiques) — casse les plans incomplets
3. Validation mainteneur finale (checklist 11 critères) = catch du poison
4. UDL 2 ("rollback tested") expose le résultat réel du test de rollback
5. UDL 7 ("audit trail") trace toutes les actions (pas d'action cachée)
6. Conformité ADRs P3 vérifiée (EG-7.12) — chaque ADR a une note d'impact déploiement
7. Feature flags opérationnels (refus 8) — kill switch disponible si feature défectueuse

**Status** : ✅ Validé (7 mécanismes)

### Mode 2 — Distraction (Distraction)
**Risque en P7** : trop de tâches "nice to have" (refactoring de scripts, optimisations de config) qui éloignent du core (release + monitoring + handoff).

**Mitigations spec v2** :
1. Refus catégorique 3 (pas de modification du code de production) = focus forcé sur le release
2. Refus catégorique 2 (pas de redéfinition NFR P2) = focus forcé sur les NFR P2
3. Budget 5k/8k/15k (large mais pas infini, force à prioriser)
4. 3-5 sub-agents max en parallèle par activité (vs 50 subagents, F2 recherche 2026)
5. UDL 4 ("monitoring active") force à configurer le monitoring AVANT le deploy (pas après)
6. Couverture cas universelle adaptative (6 cas) cadre le périmètre
7. Critère d'abandon 7 (35 min sans avancée) = checkpoint

**Status** : ✅ Validé (7 mécanismes)

### Mode 3 — Confusion (Confusion)
**Risque en P7** : ambiguïté sur l'ordre des étapes (par exemple, activer feature flag avant migration DB), ou des noms de variables/env qui se contredisent.

**Mitigations spec v2** :
1. T2 conformité go/no-go P6 + NFR P2 + ADRs P3 (Nexus-Critic, 3 invocations) détecte les ambiguïtés
2. TTM 100% héritée de P6 (XG-6.5) — chaque test pointe vers un AC unique
3. UDL 1 ("deployment strategy chosen") documente la stratégie explicitement
4. UDL 7 ("audit trail") trace l'ordre réel des actions
5. Conventions de nommage imposées (vars d'env, secrets, feature flags)
6. Code review pair-à-pair sur les scripts (Nexus-DevOps review)
7. Checklist 11 critères (conditions de sortie) = catch de la confusion

**Status** : ✅ Validé (7 mécanismes)

### Mode 4 — Clash (Conflit)
**Risque en P7** : configs contradictoires (env prod ≠ staging, le classique env drift), ou feature flag qui rentre en conflit avec une autre feature, ou migration DB qui casse une autre migration.

**Mitigations spec v2** :
1. Environnements prod iso-staging (EG-7.8) — config identique ou explicitement différenciée
2. T3 prédiction aval P8 (Nexus-Critic) — prédit les conflits d'alertes, les drifts de monitoring
3. UDL 3 ("smoke test passed") trace les conditions de mesure (env, charge, données)
4. UDL 4 ("monitoring active") trace les alertes configurées (pas de conflit d'alertes)
5. Critère d'échec 1 (smoke tests échouent → rollback IMMÉDIAT) = catch du clash
6. Critère d'abandon 5 (migration DB échoue → escalade) = escalade
7. Critère d'abandon 3 (smoke tests + rollback échouent → escalade mainteneur CRITIQUE) = escalade

**Status** : ✅ Validé (7 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | Plan incomplet, script malicieux | 7 mécanismes | ✅ |
| Distraction | Scope creep, refactoring de scripts | 7 mécanismes | ✅ |
| Confusion | Ambiguïté étapes, noms contradictoires | 7 mécanismes | ✅ |
| Clash | Env drift, feature flag conflicts, migration conflicts | 7 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Pattern reproductible de P0/P2/P3/P4/P5/P6 v2 étendu à P7.

---

## Notes de version

- **v2 (2026-06-07)** : refonte ciblée via audit (grille offline + 4 questions ciblées vague 1). Changements : (1) critère explicite de démarcation P6↔P7 inscrit dans P7 (P6 = "code va-t-il passer en prod sans casser" = staging iso-prod + tests + go/no-go ; P7 = "la prod tourne-t-elle correctement après le deploy" = release + monitoring + handoff), (2) Nexus-Critic T1 casseur plan déploiement + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 OBLIGATOIRE (3 invocations systématiques, comme P3/P4/P5/P6), (3) hard cap 8k → 15k (cohérence P3/P4/P5/P6), (4) 7+4 livrables maintenus (7 standard + 4 ajouts : changelog + runbook + monitoring dashboard + audit trail), (5) XG-7.1-XG-7.10 (10 exit criteria), (6) section 5.5 transformée en 7 questions précises avec options AskUserQuestion, (7) section 7 comblée par projection + cohérence P0/P1/P2/P3/P4/P5/P6 v2 (effort 5-15% projet, 4 frictions + 4 contournements, 3 risques dette orchestration), (8) UDL 7 éléments P7-spécifiques documentés, (9) audit des 4 failure modes Drew Breunig complet, (10) Stratégie rollout par défaut = big-bang (DTM par projet pour canary/blue-green), (11) Hotfix = pas de bypass (process complet obligatoire, escalade mainteneur si vital), (12) Couverture cas universelle adaptative (6 cas alignés P3/P4/P5/P6), (13) Tokens budget explicite 5k/8k/15k, (14) Pauses (compaction 60-70% du soft cap), (15) Conditions de sortie (checklist 11 critères). 4 décisions tranchées vague 1.
- **v2-renum (2026-06-05)** : créé suite au fix structurel (renommage cascade P6→P7 après split P3). 4 activités, 7 livrables, 4 agents en parallèle (pas de Nexus-Critic), 3k/5k/8k tokens, cap 35 min, 5.5 vide, pas d'UDL documenté, pas d'audit Drew Breunig, pas de démarcation P6↔P7, pas de matrice de conformité ADR P3.

**Actions de suivi** :
- `pre-tool-use/token-counter.sh` ligne 64 : P7 hard 15000 (vs 8000 v2-renum).
- Mettre à jour la stratégie `audit/00-context-engineering-strategy.md` : budget P7 3k/5k/8k → 5k/8k/15k, T3 P7 tranchée (T1+T2+T3 obligatoire).

Voir `audit/phase-7-deployment-audit.md` pour la traçabilité des décisions.
