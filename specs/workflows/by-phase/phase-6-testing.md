# Phase 6: Testing Workflow Spec

> **Statut** : v2 — validé 2026-06-07 par le mainteneur (audit P6 clos via grille offline + 4 questions vague 1 + 3 questions section 7, verdict 🟢 dès la première conversation)
> **Changement vs v2-renum** : (1) **critère explicite de démarcation P5↔P6** inscrit dans P6 (P5 = unit tests seuls, P6 = coverage + mutation + intégration + système + acceptance + perf + security + observabilité), (2) **Nexus-Critic T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 OBLIGATOIRE** (3 invocations systématiques, comme P3/P4/P5), (3) **hard cap 10k → 15k** (cohérence P3/P4/P5, justifié par Nexus-Critic T1+T2+T3 obligatoire), (4) **11 livrables** maintenus (grille mainteneur, vs 7 suggérés v2-renum : ajout perf report + security report + mutation testing report + go/no-go memo formalisé), (5) XG-6.1-XG-6.10 (10 exit criteria, dont couverture et mutation score migrés depuis P5), (6) section 5.5 transformée en **7 questions précises avec options AskUserQuestion** (vs vide en v2-renum), (7) section 7 comblée par **3 questions de projection + cohérence P0/P1/P2/P3/P4/P5 v2** (effort 20-40% projet, 4 frictions + 4 contournements, 3 risques dette orchestration), (8) UDL 7 éléments P6-spécifiques documentés, (9) audit des 4 failure modes Drew Breunig complet, (10) XG-6.7 = matrice de conformité aux acceptance criteria P2 (équivalent XG-5.7 P5), (11) Couverture cas universelle adaptative (6 cas alignés P3/P4/P5), (12) Tokens budget explicite 5k/8k/15k, (13) Pauses (compaction 60-70% du soft cap), (14) Conditions de sortie (checklist 10 critères). 4 décisions tranchées vague 1 + 3 décisions projection vague 1+.
> **Changement vs structure antérieure** : v2-renum créée 2026-06-05 (renommage cascade P5→P6 après split P3). Pas de changement de fond vs v2-renum, refonte ciblée pour aligner sur P3/P4/P5 v2 + intégrer la bascule coverage/mutation de P5 vers P6.
> **But** : consommer le code P5 et les acceptance criteria P2 pour produire un test closure report qui justifie le go/no-go pour P7 Deployment, en validant que le code fait ce qu'il dit (NFR P2 + acceptance criteria) — sans modifier le code (escalade P5) ni redéfinir les NFR (escalade P2).

## Metadata

- **Phase**: 6
- **Name**: Testing
- **Purpose**: Verify and validate the P5 implementation against P2 requirements (acceptance criteria + NFR) and P4 design (DDS), execute test suites (integration/system/acceptance/regression + perf + security), track defects, produce go/no-go for P7 Deployment
- **Parallel Mode**: Hyperagent enabled (multi-agent justifié, F13 recherche 2026 — 4 niveaux de test en parallèle : intégration, système, acceptance, régression + 2 transverses : perf, security)
- **Équivalent SWEBOK v4** : P5 SWEBOK (Software Testing KA)
- **Référentiels** : IEEE 829-2008 (Software Test Documentation), ISO/IEC/IEEE 29119 (Software Testing), ISTQB Foundation, NIST 800-22r1a (perf), OWASP ASVS 5.0 (security)

---

## Mission (1 phrase)

> « Consommer le code P5 (source + coverage) et les acceptance criteria P2, exécuter les 4 niveaux de test (intégration, système, acceptance, régression) + les 2 transverses (perf, security) + mutation testing, tracker les défauts, et produire un test closure report + go/no-go memo pour P7 Deployment — sans modifier le code (escalade P5) ni redéfinir les NFR (escalade P2). »

---

## Critère de démarcation P5 (Implementation) vs P6 (Testing)

> **Validation 2026-06-07** : le mainteneur a tranché pour un critère explicite, inscrit dans P5 ET P6. **P5 = unit tests seuls. P6 = coverage + mutation + tout le reste.**

| Dimension | P5 Implementation (déjà tranché en v2 finale) | P6 Testing (cette spec) |
|-----------|----------------------------------------------|--------------------------|
| **Question centrale** | **Est-ce que ce module est correctement implémenté unitairement ?** | **Est-ce que le système complet fait ce qu'il dit et respecte les NFR ?** |
| **Périmètre tests** | **Unit tests seuls** (couverture et mutation ne sont PLUS en P5) | **Couverture globale** (line + branch) + **Mutation testing** + Intégration + Système + Acceptance + Régression + Perf + Security + Observabilité |
| **Type de test** | Tests isolés par fonction/classe (in-process, pas de réseau, pas de DB) | Tests inter-modules (intégration), bout-en-bout (système/acceptance), conformité NFR (perf/security), qualité des tests (mutation) |
| **Périmètre fonctionnel** | Une fonction ou classe à la fois | Modules ensembles, système complet, NFR transverses (perf, security, observabilité) |
| **Décisions** | Internes au code (organisation fichiers, naming, factorisation) | Externes au code (stratégie de test, choix outils, plan d'exécution, critères go/no-go) |
| **Agents typiques** | Nexus-Backend (lead code), Nexus-Frontend, Nexus-DevOps, Nexus-Security, Nexus-Critic | Nexus-QA-Lead (lead), Nexus-Backend/Frontend (résolution défauts), Nexus-DevOps (env), Nexus-Security (pentest), Nexus-Performance (perf), Nexus-Critic |
| **Adversarial** | T1 casseur code + T2 conformité DDS P4 + ADRs P3 + T3 prédiction aval P6 | T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 (ruptures prod) |
| **Livrables typiques** | `source-code/`, `unit-test-suite.md`, `coverage-report.md` (lint gate build), `code-review-reports.md`, `ci-cd-pipeline.md`, `effort-report.md`, `technical-debt-register.md` | `test-plan.md`, `integration-test-results.md`, `system-test-results.md`, `acceptance-test-results.md`, `regression-test-results.md`, `defect-report.md`, `test-traceability-matrix.md` (TTM), `test-closure-report.md`, `performance-test-report.md`, `security-test-report.md`, `mutation-testing-report.md`, `go-no-go-decision-memo.md` |

**Règle simple** : si la décision impacte **une fonction ou classe isolément** = P5. Si elle impacte **plusieurs modules ensemble**, **un niveau de test** (intégration/système/acceptance), ou **une NFR transverse** (perf, security, observabilité) = P6.

**Cas limite type** : "Module billing = tester que la fonction `calculateTotal()` retourne 42" = **P5** (unit). "Module billing + Module payment = tester que le total calcule puis déclenche le paiement sans race condition" = **P6** (intégration). "Tester que le système complet répond en < 200ms pour 95% des requêtes" = **P6** (perf NFR). "Mutation testing sur `calculateTotal`" = **P6** (qualité des tests, pas P5).

**Conséquence opérationnelle sur P5 v2 finale** : la couverture (XG-5.3 dans P5 v2 finale, ≥80% line + ≥70% branch) reste valide en P5 comme **lint gate au build** (le build fail si <80% line), mais la **validation finale de la couverture** + **mutation testing** sont en P6. La couverture au build est une condition nécessaire mais pas suffisante ; la qualité des tests est mesurée en P6 par mutation testing + acceptance criteria P2.

**Conséquence opérationnelle sur P5 v2 finale (mutation testing)** : la mutation testing mentionnée dans P5 v2 finale (UDL 6) est retirée de P5 (P5 = unit seul). Mutation testing est un livrable P6 (`mutation-testing-report.md`).

**Conséquence opérationnelle inverse** : si P6 détecte qu'une décision impacte l'organisation interne du code, **elle escalade P5**. Si P6 détecte qu'une décision impacte les NFR P2 (perf cible, security target), **elle escalade P2**. Si P6 détecte qu'une décision impacte l'interface externe du module (contrat DDS P4), **elle escalade P4**.

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-6.1 | Phase 5 implementation complete | Implementation status | ≥95% modules implemented (XG-5.1 P5) |
| EG-6.2 | Unit test suite available | Test suite existence | Tests unitaires présents (P5) |
| EG-6.3 | Build coverage gate passed | Coverage report | ≥80% line + ≥70% branch (lint gate P5 XG-5.3) |
| EG-6.4 | Acceptance criteria defined | AC document (P2) | 100% requirements avec acceptance criteria (P2 EG-2.4) |
| EG-6.5 | NFR P2 ratified | NFR document | 100% NFR (perf + security + observability) validés P2 |
| EG-6.6 | Test environments prepared | Environment status | 4 envs opérationnels (intégration, système, acceptance, perf) + 1 security (staging iso-prod) |
| EG-6.7 | Test data defined | Test data sets | Données de test définies (synthétiques / anonymisées / prod-like) pour chaque cas |
| EG-6.8 | Test harnesses ready | Harness status | 4 harnesses fonctionnels (intégration, système, acceptance, régression) |
| EG-6.9 | Test plan approved | TP document | Plan de test formellement approuvé (chef de projet) |
| EG-6.10 | Conformité DDS P4 vérifiée | Matrice DDS → code (XG-5.7) | 100% DDS P4 tracés par fichier de code (hérité de P5) |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers Phase 5 (Implementation) remediation (escalade pour couverture/harnais) or Phase 2 (Requirements) remediation (escalade pour NFR/AC).

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-6.1 | All test levels completed | Test execution status | 100% test plans executed (4 niveaux + 2 transverses) |
| XG-6.2 | Coverage validated | Coverage report | ≥80% line + ≥70% branch validés en contexte d'exécution réelle |
| XG-6.3 | Mutation score achieved | Mutation testing report | ≥70% mutation score (seuil ISTQB, adaptatif par profil) |
| XG-6.4 | Defect backlog stabilized | Defect count trend | ≤1 critical defect ouvert (grille mainteneur), ≤5 high, ≤20 medium |
| XG-6.5 | Test traceability verified | TTM coverage | 100% tests tracés aux acceptance criteria P2 + NFR P2 + DDS P4 |
| XG-6.6 | NFR perf validés | Performance test report | 100% NFR perf P2 validés (latence p95, throughput, scalabilité) |
| XG-6.7 | NFR security validés | Security test report | 0 critical security finding, 0 high security finding non résolu |
| XG-6.8 | Release readiness confirmed | Release readiness check | All go/no-go criteria green + sign-off mainteneur |
| XG-6.9 | UDL 7 éléments P6-spécifiques loggés | UDL set | 100% loggés dans `.swebok_state.db` (table `udl_p6`) |
| XG-6.10 | Conformité acceptance criteria P2 vérifiée | Matrice AC → test | 100% acceptance criteria P2 tracés par test (XG-6.7) |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` requires additional test cycle or escalade.

**XG-6.3 — Adaptativité par profil projet (note)** : pour les projets compliance/sécurité, le seuil peut être relevé à ≥85% via décision mainteneur documentée dans `test-closure-report.md`. Pour les projets R&D/POC, il peut être abaissé à ≥50% avec justification.

**XG-6.4 — Adaptativité par profil projet (note)** : ≤1 critical par défaut (grille mainteneur, plus strict que spec v2-renum qui disait ≤5). Pour les projets compliance : 0 critical obligatoire.

---

## Transition Criteria to Phase 7 (Deployment)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Test completion certified | Nexus-QA-Lead | Deployment Lead | Test completion certificate + closure report |
| Go/no-go decision signed | Project Sponsor | All stakeholders | go-no-go-decision-memo.md (sign-off formel) |
| Defect escape rate acceptable | Nexus-QA | Project Lead | Escape rate ≤2% (defects post-go) |
| Release criteria met | Nexus-QA-Lead | Deployment Lead | Release criteria checklist (XG-6.8) |
| Deployment environment ready | Nexus-DevOps | Deployment Lead | Env de déploiement validé (handoff P6 → P7) |
| Conformité AC P2 vérifiée | Nexus-QA (T2) | Phase 7 Lead | Matrice AC → test (XG-6.10) |
| Mutation testing report transmitted | Nexus-QA | Project Lead | mutation-testing-report.md signé |
| Defect disposition documented | Nexus-QA | Project Lead | defect-report.md avec décision (fix/wontfix/defer) par défaut |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_6_COMPLETE` only when all transition criteria verified with formal evidence (closure report + go/no-go memo signés).

---

## Key Activities

### Activity 6.1: Test Planning
- Définir la stratégie de test par niveau (intégration, système, acceptance, régression) + transverses (perf, security, mutation)
- Choisir les outils (framework test, coverage, mutation, perf, security)
- Définir le plan d'exécution (séquencement, parallélisme, durée cible)
- Identifier les environnements de test (docker, cloud, on-prem) et leur iso-prod
- Définir la stratégie de test data (synthétique, anonymisée, prod-like)
- Définir les critères d'entrée/sortie par niveau

### Activity 6.2: Test Execution (4 niveaux + 2 transverses)
- **Intégration** : tester les interactions inter-modules (contrats DDS P4, mocking ciblé)
- **Système** : tester le système complet bout-en-bout (scénarios utilisateurs)
- **Acceptance** : valider les acceptance criteria P2 + NFR P2 (criteria-by-criteria)
- **Régression** : re-jouer la suite complète après chaque fix
- **Perf (transverse)** : valider les NFR perf P2 (latence p95, throughput, scalabilité) avec k6/JMeter
- **Security (transverse)** : DAST + pentest (OWASP ASVS 5.0) avec ZAP/Burp

### Activity 6.3: Mutation Testing
- Exécuter un outil de mutation testing (mutmut, stryker, PIT, etc.)
- Mesurer le mutation score (% mutants tués / mutants总数)
- Identifier les mutants survivants (= tests qui ne testent rien)
- Prioriser la correction des mutants survivants critiques
- Documenter le score dans `mutation-testing-report.md`

### Activity 6.4: Defect Management
- Logger les défauts dans `defect-report.md` (sévérité, priorité, owner, SLA)
- Prioriser les défauts (critical = bloqueur, high = corrigeable rapidement, medium/low = dette)
- Tracker la résolution (status, fix, retest, close)
- Documenter la disposition (fix, wontfix avec rationale, defer vers P9 maintenance)
- Décider des défauts "acceptés" (workaround vs fix) en accord avec mainteneur

### Activity 6.5: Test Reporting
- Compiler les résultats par niveau dans `*-test-results.md`
- Générer la matrice de traçabilité `test-traceability-matrix.md` (TTM, test → AC + NFR + DDS)
- Générer les rapports transverses (perf, security, mutation)
- Synthétiser le `test-closure-report.md` (résumé exécutif, taux de réussite, défauts restants, NFR status)
- Produire le `go-no-go-decision-memo.md` (1 page, décision documentée, sign-off)

### Activity 6.6: Adversarial Validation (Nexus-Critic — OBLIGATOIRE)
- **T1 casseur tests** : Nexus-Critic relit les tests, cherche des trous de couverture, propose des cas limites, valide que les tests testent vraiment (mutation testing mindset). Cible : `*-test-results.md` + harnesses.
- **T2 conformité acceptance criteria P2** : Nexus-Critic vérifie que chaque acceptance criteria P2 a son test, et que chaque NFR P2 est validé (matrice AC → test, XG-6.10). Cible : TTM + acceptance-test-results.md.
- **T3 prédiction aval P7** : Nexus-Critic prédit ce qui va casser en P7 Deployment ou en prod (zones non testées, env drift, données non représentatives, dette de test). Cible : closure report + go/no-go memo.

### Activity 6.7: Continuous Improvement
- Documenter les leçons apprises (ce qui a bien marché, ce qui a coincé)
- Identifier les améliorations pour les futurs projets (outillage, processus, couverture)
- Aligner sur le plan d'amélioration continue (P9 Maintenance)

---

## Responsible Agents

| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordonne les tâches de test parallèles (4 niveaux + 2 transverses) |
| **Nexus-QA-Lead (lead)** | Coordination test globale, sign-off closure report, go/no-go memo |
| Nexus-Backend | Résolution défauts backend, support tests intégration |
| Nexus-Frontend | Résolution défauts frontend, support tests système |
| Nexus-DevOps | Gestion des env de test, isolation env, observabilité test |
| Nexus-Security | Pentest, DAST, validation security findings (OWASP ASVS 5.0) |
| Nexus-Performance | Tests de charge, validation NFR perf (k6, JMeter) |
| **Nexus-Critic (5e agent obligatoire — décision mainteneur 2026-06-07)** | **T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 — TOUS OBLIGATOIRES** (3 invocations systématiques, comme P3/P4/P5) |

**Concurrency** : multi-agent justifié (F13 recherche 2026 — 4 niveaux de test en parallèle : intégration, système, acceptance, régression + 2 transverses : perf, security). 3-5 sub-agents en parallèle par niveau, jamais plus. **Nexus-Critic = 3 invocations systématiques** (T1 casse les tests, T2 vérifie conformité acceptance criteria P2, T3 prédit les ruptures P7). Coût additionnel ~4.5k tokens, justifié par le hard cap 15k (cohérence P3/P4/P5).

**Patterns adversariaux T1/T2/T3 (rappel)** :
- **T1 (casseur tests)** : un dev propose des tests, Nexus-Critic casse. Cible : `*-test-results.md`, harnesses, mutation score.
- **T2 (spec-compliance)** : Nexus-Critic vérifie conformité acceptance criteria P2 + NFR P2 + DDS P4 (matrice AC → test, XG-6.10). Cible : TTM + acceptance-test-results.md.
- **T3 (conséquentialiste)** : Nexus-Critic prédit ce qui va casser en P7 Deployment ou en prod. Cible : closure report + go/no-go memo + dette de test.

**Isolation des contextes (ACI stratégie §4.5)** : Nexus-Critic ne voit pas le prompt système des producteurs. Chaque rôle adversarial a un contexte distinct, sinon les "adversaires" se laissent influencer par le contexte partagé.

---

## Required Skills

- `nexus-qa`: Test strategy, exécution, defect management
- `nexus-qa-lead`: Test leadership, go/no-go decision, closure report
- `speckit-qa`: QA testing framework, automated tests
- `nexus-backend`: Résolution défauts backend
- `nexus-frontend`: Résolution défauts frontend
- `nexus-devops`: Gestion env de test, isolation, observabilité
- `nexus-security`: Pentest, DAST, OWASP ASVS 5.0
- `nexus-performance`: Tests de charge, k6, JMeter
- `nexus-critic`: Adversarial validation (T1 casseur tests + T2 conformité AC P2 + T3 aval P7) — **OBLIGATOIRE** (3 invocations)

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-testing-complete` | Exit criteria met (XG-6.1-XG-6.10) | Triggers Phase 7 (Deployment) initiation |
| `test-plan-approved` | Test planning done (Activity 6.1) | Enables test execution |
| `defects-stabilized` | Defect rate acceptable (XG-6.4) | Confirms release readiness |
| `release-readiness-confirmed` | All criteria met (XG-6.8) | Unblocks deployment |
| `nfr-perf-validated` | NFR perf validés (XG-6.6) | Confirme conformité perf P2 |
| `nfr-security-validated` | NFR security validés (XG-6.7) | Confirme conformité security P2 |
| `mutation-score-achieved` | Mutation score validé (XG-6.3) | Confirme qualité des tests |
| `t1-temoin-casseur-passed` | T1 Nexus-Critic passé | Confirme robustesse des tests |
| `t2-ac-conformity-verified` | Matrice AC → test (XG-6.10) | Confime conformité acceptance criteria P2 |
| `t3-p7-prediction-logged` | T3 prédiction faite | Snapshot pour P7 |
| `udl-p6-logged` | 7 éléments UDL loggés | Snapshot pour phases suivantes |
| `go-no-go-decided` | go-no-go-decision-memo.md signé | Confirme autorisation déploiement |

---

## Artifacts Produced

| Artifact | Description | Location | Format |
|----------|-------------|----------|--------|
| `test-plan.md` | Stratégie de test par niveau + transverses, outils, séquencement | `specs/workflows/by-phase/phase-6-testing/` | md |
| `integration-test-results.md` | Résultats des tests d'intégration (inter-modules) | `specs/workflows/by-phase/phase-6-testing/` | md |
| `system-test-results.md` | Résultats des tests système (bout-en-bout) | `specs/workflows/by-phase/phase-6-testing/` | md |
| `acceptance-test-results.md` | Résultats des tests d'acceptance (vs acceptance criteria P2) | `specs/workflows/by-phase/phase-6-testing/` | md |
| `regression-test-results.md` | Résultats des tests de régression | `specs/workflows/by-phase/phase-6-testing/` | md |
| `defect-report.md` | Log des défauts + décision (fix/wontfix/defer) | `specs/workflows/by-phase/phase-6-testing/` | md + JSON (machine-parse) |
| `test-traceability-matrix.md` (TTM) | Matrice test → acceptance criteria P2 + NFR P2 + DDS P4 | `specs/workflows/by-phase/phase-6-testing/` | md (table) |
| `test-closure-report.md` | Résumé exécutif (taux réussite, défauts, NFR status) | `specs/workflows/by-phase/phase-6-testing/` | md (1 page vue exécutive + détails) |
| `performance-test-report.md` (NFR perf) | Validation NFR perf P2 (latence p95, throughput, scalabilité) | `specs/workflows/by-phase/phase-6-testing/` | md + JSON (résultats bruts) + HTML (graphiques) |
| `security-test-report.md` (NFR security) | Pentest + DAST (OWASP ASVS 5.0) | `specs/workflows/by-phase/phase-6-testing/` | md + SARIF (machine-parse) |
| `mutation-testing-report.md` | Mutation score + mutants survivants | `specs/workflows/by-phase/phase-6-testing/` | md + JSON (résultats bruts) |
| `go-no-go-decision-memo.md` | Décision go/no-go documentée, 1 page, sign-off | `specs/workflows/by-phase/phase-6-testing/` | md |

**Format de stockage** :
- Specs narratives : md (lecture humaine)
- Résultats de tests bruts : JSON (machine-parse)
- Performance : JSON (résultats) + HTML (graphiques)
- Security : SARIF (standard)
- Mutation testing : JSON (résultats bruts)
- Defect log : JSON (machine-parse) + md (synthèse)

**Format de la matrice de conformité (XG-6.10)** : matrice acceptance criteria P2 → test, avec pointeur unique. Chaque AC a ≥1 test, chaque test référence ≥1 AC. Pas d'AC orphelin (sans test), pas de test orphelin (sans AC). Symétrique à la matrice DDS → code de P5 (XG-5.7) et à la matrice ADR → module de P4 (XG-4.7).

---

## Format des fichiers (triple différencié, aligné P3/P4/P5 v2)

> **Validation 2026-06-07** : format triple différencié par type de livrable (aligné P3/P4/P5 v2).

| Type de livrable | Format primaire | Format secondaire | Standard |
|------------------|------------------|-------------------|----------|
| **Specs narratives** (test-plan, integration/system/acceptance/regression-test-results, defect-report, test-closure-report) | md (lecture humaine) | — | — |
| **Performance report** | md (résumé) | JSON (résultats bruts) + HTML (graphiques) | k6, JMeter |
| **Security report** | md (résumé) | SARIF (machine-parse) | OWASP ZAP, Burp, OWASP ASVS 5.0 |
| **Mutation testing report** | md (résumé) | JSON (résultats bruts) | mutmut, stryker, PIT |
| **Defect log** | md (synthèse) | JSON (machine-parse) | — |
| **TTM** (test-traceability-matrix.md) | md (table) | — | — |
| **Go/no-go memo** | md (1 page) | — | — |

**Convention de nommage** :
- Specs narratives : `${livrable}.md`
- Performance : `performance-test-report.md` + `perf-results.json` + `perf-results.html`
- Security : `security-test-report.md` + `security-findings.sarif`
- Mutation : `mutation-testing-report.md` + `mutation-results.json`
- Defect log : `defect-report.md` + `defect-log.json`

**Localisation** : tous dans `specs/workflows/by-phase/phase-6-testing/`.

---

## Hyperagent Parallel Processing

```
parallel_tasks:
  - task: integration_testing
    agents: [Nexus-BA, Nexus-Backend]
    sync: false

  - task: system_testing
    agents: [Nexus-QA, Nexus-Frontend]
    sync: false

  - task: acceptance_testing
    agents: [Nexus-QA, Nexus-PM]
    sync: false

  - task: regression_testing
    agents: [Nexus-QA, Nexus-DevOps]
    sync: false

  - task: performance_testing
    agents: [Nexus-Performance, Nexus-DevOps]
    sync: false

  - task: security_testing
    agents: [Nexus-Security, Nexus-DevOps]
    sync: false

  - task: mutation_testing
    agents: [Nexus-QA, Nexus-Critic]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après parallel):
  - task: t1_casseur_tests
    agents: [Nexus-Critic]
    target: *-test-results.md + harnesses + mutation score
    sync: true

  - task: t2_conformite_ac_p2
    agents: [Nexus-Critic]
    target: TTM + acceptance-test-results.md (matrice XG-6.10)
    sync: true

  - task: t3_prediction_p7
    agents: [Nexus-Critic]
    target: closure report + go/no-go memo + dette de test
    sync: true

reduction: "Nexus-QA-Lead synthesizes all into test-closure-report.md + go-no-go-decision-memo.md"
```

---

## Refus catégoriques (7)

La phase P6 **refuse** de :
1. **Pas de modification du code de production** (escalade P5 — règle de démarcation)
2. **Pas de redéfinition des NFR** (escalade P2 — toute déviation NFR P2 = escalade P2)
3. **Pas de modification des tests unitaires P5** (escalade P5 — P5 = owner des unit tests)
4. **Pas de go avec défauts critiques ouverts** (XG-6.4 : ≤1 critical ouvert)
5. **Pas de skip de tests sans justification** (chaque skip documenté dans test-closure-report.md)
6. **Pas de "test passed" sur tests flaky** (le flaky = 0 jusqu'à preuve de stabilité)
7. **Pas de mutation score < seuil accepté sans dette documentée** (XG-6.3 = ≥70% par défaut, adaptatif par profil)

---

## Critères d'abandon (6 + temps)

L'agent abandonne et prévient le mainteneur si :
1. Défaut critique non résolvable après 3 itérations (escalade mainteneur)
2. Performance non-conforme aux NFR P2 (escalade P3 si design sous-jacent en cause)
3. Security finding critique non patchable rapidement (escalade mainteneur)
4. Couverture < cible après 2 itérations (escalade P5 pour tests incomplets)
5. Mutation score < seuil sans dette acceptable (escalade P5 ou décision mainteneur)
6. Test data manquante ou non représentative (escalade Nexus-DevOps pour env, ou décision mainteneur)
7. Dépassement de 35 min sans avancée claire

---

## Tokens budget

- **Base** : 5k tokens
- **Soft cap** : 8k tokens (alerte, compaction 60-70% = 5.6k)
- **Hard cap** : 15k tokens (compactage forcé + abort)

Multi-agent justifié (F13 recherche 2026) : 4 niveaux de test + 2 transverses + 1 mutation en parallèle × 1.5k chacun = 10.5-15k base théorique. Cap 15k hard pour absorber les validations adversariales T1+T2+T3 obligatoires (Nexus-Critic en mode rotation sur les 3 patterns, comme P3/P4/P5 — décision mainteneur 2026-06-07). **Justification du passage 10k → 15k** : Nexus-Critic T1+T2+T3 obligatoire = 3 invocations × ~1.5k = 4.5k additionnel, ce qui sature le budget 10k en nominal. 15k = marge de sécurité pour absorber les validations adversariales complètes, en cohérence avec P3 Architecture, P4 Design et P5 Implementation (5k/8k/15k).

**Note** : P6 devient 4e phase la plus large (ex-aequo avec P3, P4, P5). Acceptable car P6 = 20-40% de l'effort total projet (décision mainteneur 2026-06-07) et le sur-coût est compensé par la qualité (TTM complète, mutation testing, NFR perf+security validés, go/no-go formalisé).

---

## Pauses

Toutes les 5 actions : compaction checkpoint à 60-70% du soft cap (5.6k tokens, F8 recherche 2026). Compaction sélective : garder les décisions et les diffs, drop les résultats de tests volumineux (résumer les passes, garder les échecs en détail, AP7 recherche 2026).

**Pre-hydrate obligatoire** (F7 recherche 2026 — 60% du 1er tour = retrieval) : au début de P6, charger dans le hot_context (`.swebok_state.db`) la slice suivante :
- Liste des modules à tester (pointeurs vers `source-code/` P5)
- Acceptance criteria P2 (pointeurs vers SRS P2)
- NFR P2 (perf + security + observability)
- TTM initiale (structure vide à remplir)
- Environnements de test disponibles
- 4 harnesses + 2 transverses

Sans ce pre-hydrate, 60% du budget du 1er tour est consommé en retrieval, ce qui sature le soft cap en nominal.

---

## Couverture corpus (état 2026-06-06)

- **13% de couverture** — P6 = 2e phase la moins couverte (juste devant P10 Retirement)
- **4 ressources corpus-aligned** : 2 livres Mac Studio (Full Stack Testing Mohan, Introduction to Software Testing) + 1 standard NIST (800-22r1a) + 1 OWASP ASVS 5.0
- **Lacunes critiques** : Testing KA SWEBOK (Beizer, Kaner, Bach, etc.) — non acquis
- **1 livre open-access** : Lessons Learned in Software Testing (Kaner)
- **Décision mainteneur 2026-06-06** : 13% suffit pour cadrage, batch d'acquisition ultérieur (action P1-N roadmap, P6 bénéficiera de l'enrichissement P1).

**Livres canoniques P6** (extrait) :
- Lessons Learned in Software Testing (Kaner, open-access)
- Full Stack Testing (Mohan, Gayathri)
- Introduction to Software Testing
- OWASP ASVS 5.0 (standard ouvert)
- NIST 800-22r1a (Random Number Generation, perf)

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :

1. **Greenfield from-scratch** : tests d'intégration/système/acceptance riches, mutation testing activé, perf+security baselines
2. **Maintenance legacy** : tests = "que doit-on tester pour ne pas régresser", dette de test héritée
3. **Projet interne** (équipe, gouvernance légère) : tests standards, mutation testing optionnel, perf+security légers
4. **Projet externe client** : tests sign-off client, mutation testing obligatoire, perf+security renforcée
5. **Compliance-driven** (finance, santé, défense) : mutation testing obligatoire (XG-6.3 relevé à ≥85%), pentest obligatoire (OWASP ASVS 5.0 niveau 3), perf+security = NFR bloquantes
6. **R&D / exploration** : tests smoke + acceptance, mutation testing abaissé à ≥50% avec justification, perf+security = nice-to-have

---

## UDL — 7 éléments P6-spécifiques

> **Validation 2026-06-07** : 7 éléments P6-spécifiques (aligné P3, P4, P5).

| Élément | Description | Exemple |
|---------|-------------|---------|
| **Test case executed** | Résultat par cas (pass/fail/skip avec justification) | "Test INT-003 = PASS en 2.3s, Test ACC-007 = FAIL (AC P2 'latence < 200ms' violée : 280ms mesuré)" |
| **Defect found** | Pointeur vers `defect-report.md` + sévérité + décision | "DEF-012 = critical, fix scheduled P5+P6 itération 2, see defect-report.md §3.2" |
| **NFR P2 validé** | Pointeur vers `acceptance-test-results.md` + status | "NFR P2 perf latence p95 < 200ms = VALIDÉ, voir acceptance-test-results.md §4.3" |
| **Coverage achieved** | Couverture par module (line + branch + mutation score) | "Module billing = 87% line, 75% branch, 72% mutation score" |
| **Performance benchmark** | Mesure vs NFR P2 perf | "Latence p95 = 180ms (cible 200ms), throughput = 1500 req/s (cible 1000 req/s)" |
| **Security finding** | Finding par sévérité vs NFR P2 security | "XSS dans /api/search = high, fixed avant go (OWASP ASVS 5.0 §5.3.3)" |
| **Go/no-go decision** | Décision documentée + sign-off + rationale | "GO pour P7 Deployment, signé mainteneur 2026-06-15, rationale = 0 critical defect, NFR perf+security validés, mutation score 78%" |

Stockés dans `.swebok_state.db` (table `udl_p6`) et consultables via Consultation Envelope (A1) par P7 Deployment.

---

## Conditions de sortie (passage à P7)

Le mainteneur valide avec une **checklist à 100%** (11 critères) :
- [ ] `test-plan.md` existe (4 niveaux + 2 transverses + mutation, sign-off)
- [ ] `integration-test-results.md` existe (100% tests exécutés, défauts tracés)
- [ ] `system-test-results.md` existe
- [ ] `acceptance-test-results.md` existe (100% AC P2 validés)
- [ ] `regression-test-results.md` existe
- [ ] `defect-report.md` existe (≤1 critical ouvert, disposition documentée)
- [ ] `test-traceability-matrix.md` (TTM) existe (100% tests tracés AC + NFR + DDS)
- [ ] `test-closure-report.md` existe (résumé exécutif 1 page + détails)
- [ ] `performance-test-report.md` existe (100% NFR perf P2 validés)
- [ ] `security-test-report.md` existe (0 critical security finding, OWASP ASVS 5.0)
- [ ] `mutation-testing-report.md` existe (mutation score ≥70% par défaut)
- [ ] `go-no-go-decision-memo.md` existe (1 page, décision, sign-off)
- [ ] UDL 7 éléments loggés dans `.swebok_state.db`

Pas de feu vert séparé — les documents font foi.

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-07

### Mode 1 — Poisoning (Empoisonnement)
**Risque en P6** : un faux test qui passe (test theater) qui contamine la confiance dans la suite de tests, ou un mutant survivant non détecté qui laisse une régression silencieuse en prod.

**Mitigations spec v2** :
1. Mutation testing obligatoire (XG-6.3) — détecte les tests qui ne testent rien (mutants survivants = tests faibles)
2. TTM 100% (XG-6.5) — chaque test tracé à un acceptance criteria P2 (pas de test orphelin)
3. Conformité acceptance criteria P2 vérifiée par matrice AC → test (XG-6.10) — pas de couverture fantôme
4. Nexus-Critic T1 casseur tests (3 invocations systématiques) — casse les faux tests
5. Validation mainteneur finale (checklist 11 critères) = catch du poison
6. UDL 4 ("coverage achieved") expose la couverture réelle par module (pas de gonflement)
7. UDL 7 ("go/no-go decision") logge le rationale (pas de go de complaisance)

**Status** : ✅ Validé (7 mécanismes)

### Mode 2 — Distraction (Distraction)
**Risque en P6** : trop de tests "nice to have" qui éloignent des acceptance criteria P2, ou scope creep (perf testing devient optimization, security testing devient audit complet).

**Mitigations spec v2** :
1. Refus catégorique 2 (pas de redéfinition NFR) + 1 (pas de modification code) = focus forcé sur les NFR P2
2. TTM 100% force à tracer chaque test à un AC P2 (pas de test libre)
3. Budget 5k/8k/15k (large mais pas infini, force à prioriser)
4. 3-5 sub-agents max en parallèle par niveau (vs 50 subagents, F2 recherche 2026)
5. UDL 3 ("NFR P2 validé") force à pointer vers le NFR d'origine
6. Couverture cas universelle adaptative (6 cas) cadre le périmètre
7. Critère d'abandon 7 (35 min sans avancée) = checkpoint

**Status** : ✅ Validé (7 mécanismes)

### Mode 3 — Confusion (Confusion)
**Risque en P6** : tests ambigus (quoi tester exactement), ou tests qui testent la même chose sous des noms différents (test duplication).

**Mitigations spec v2** :
1. TTM 100% (XG-6.5) — chaque test pointe vers un AC unique, pas de duplication
2. UDL 1 ("test case executed") trace chaque test par ID unique + résultat
3. Nexus-Critic T2 conformité acceptance criteria P2 détecte les tests dupliqués ou ambigus
4. UDL 4 ("coverage achieved") expose la granularité par module
5. Mutation testing détecte les tests qui ne testent rien (mutants survivants)
6. Conventions de nommage des tests imposées (test_${niveau}_${module}_${scenario})
7. Code review pair-à-pair sur les tests (Nexus-QA-Lead review)

**Status** : ✅ Validé (7 mécanismes)

### Mode 4 — Clash (Conflit)
**Risque en P6** : tests contradictoires (mock vs intégration), ou environnement de test non iso-prod (env drift) qui donnent des résultats incohérents.

**Mitigations spec v2** :
1. Environnements de test iso-prod (EG-6.6) — docker ou cloud identiques à la prod
2. Test data définie et versionnée (EG-6.7) — pas de données aléatoires
3. Nexus-Critic T3 prédit les ruptures aval P7 (env drift, données non représentatives)
4. UDL 5 ("performance benchmark") trace les conditions de mesure (env, charge, données)
5. Critère d'abandon 6 (test data manquante ou non représentative) = escalade
6. Critère d'abandon 4 (couverture < cible après 2 itérations) = escalade P5
7. Critère d'abandon 3 (security finding critique non patchable) = escalade mainteneur

**Status** : ✅ Validé (7 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | Test theater, mutants survivants | 7 mécanismes | ✅ |
| Distraction | Scope creep, tests nice-to-have | 7 mécanismes | ✅ |
| Confusion | Tests ambigus, duplication | 7 mécanismes | ✅ |
| Clash | Env drift, tests contradictoires | 7 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Pattern reproductible de P0/P2/P3/P4/P5 v2 étendu à P6.

---

## Notes de version

- **v2 (2026-06-07)** : refonte ciblée via audit (grille offline + 4 questions ciblées vague 1 + 3 questions section 7). Changements : (1) critère explicite de démarcation P5↔P6 inscrit dans P6 (P5 = unit tests seuls, P6 = coverage + mutation + intégration + système + acceptance + perf + security + observabilité), (2) Nexus-Critic T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 OBLIGATOIRE (3 invocations systématiques, comme P3/P4/P5), (3) hard cap 10k → 15k (cohérence P3/P4/P5), (4) 11 livrables maintenus (vs 7 v2-renum : ajout perf report + security report + mutation testing report + go/no-go memo formalisé), (5) XG-6.1-XG-6.10 (10 exit criteria dont couverture et mutation score migrés depuis P5), (6) section 5.5 transformée en 7 questions précises avec options AskUserQuestion, (7) section 7 comblée par 3 questions de projection + cohérence P0/P1/P2/P3/P4/P5 v2 (effort 20-40% projet, 4 frictions + 4 contournements, 3 risques dette orchestration), (8) UDL 7 éléments P6-spécifiques documentés, (9) audit des 4 failure modes Drew Breunig complet, (10) XG-6.10 = matrice AC → test (équivalent XG-5.7 P5), (11) Couverture cas universelle adaptative (6 cas alignés P3/P4/P5), (12) Tokens budget explicite 5k/8k/15k, (13) Pauses (compaction 60-70% du soft cap), (14) Conditions de sortie (checklist 11 critères). 4 décisions tranchées vague 1 + 3 décisions section 7 vague 1+.
- **v2-renum (2026-06-05)** : créé suite au fix structurel (renommage cascade P5→P6 après split P3). 4 activités, 7 livrables, 5 agents en parallèle (pas de Nexus-Critic), 4k/7k/10k tokens, cap 35 min, 5.5 vide, pas d'UDL documenté, pas d'audit Drew Breunig, pas de démarcation P5↔P6, pas de matrice de conformité AC P2.

**Actions de suivi** :
- Mettre à jour P5 v2 finale pour refléter : (a) coverage reste en P5 comme lint gate build (XG-5.3 inchangé) mais validation finale migrée en P6 (XG-6.2), (b) mutation testing retiré de P5 UDL 6 et basculé en P6.
- `pre-tool-use/token-counter.sh` ligne 64 : P6 hard 15000 (vs 10000 v2-renum).

Voir `audit/phase-6-testing-audit.md` pour la traçabilité des décisions.
