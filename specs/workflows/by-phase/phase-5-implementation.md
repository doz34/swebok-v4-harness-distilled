# Phase 5: Implementation Workflow Spec

> **Statut** : v2.1 — ajusté 2026-06-07 (conséquence de l'audit P6 : bascule coverage finale + mutation testing vers P6 ; P5 = unit tests seuls)
> **Changement v2.1 vs v2** : (1) P5 = **unit tests seuls** (plus de coverage finale ni mutation testing en P5, ces deux activités sont en P6 Testing), (2) XG-5.3 reste valide comme **lint gate au build** (build fail si <80% line), mais la **validation finale** de la couverture et le **mutation testing** sont en P6, (3) UDL P5 6 ("Rejet T1/T2 casseur") reste, l'UDL "Mutation testing" qui était implicite en P5 v2 finale n'est plus là (mutation = P6).
> **Statut v2 antérieure** : v2 — validé 2026-06-07 par le mainteneur (audit P5 clos via grille offline + 4 questions ciblées, vague 1)
> **Changement vs v2-renum** : (1) **critère explicite de démarcation P4↔P5** inscrit dans P5 (organisation interne du code vs signatures externes/algorithmes, règle ≥1 module), (2) **Nexus-Critic T1 casseur + T2 conformité DDS P4/ADRs P3 + T3 prédiction aval P6 OBLIGATOIRE** (3 invocations systématiques, comme P3 et P4), (3) **effort-report.md = livrable formel** (comble P4 SWEBOK absente, estimation T-shirt S/M/L/XL par module vs temps réel passé), (4) **XG-5.1 = ≥95% partout** (compromis mainteneur entre rigueur grille ≥99% et pragmatisme spec v2-renum ≥80%), (5) section 5.5 transformée en **7 questions précises avec options AskUserQuestion** (vs vide en v2-renum), (6) section 7 comblée par **projection + cohérence P0/P1/P2/P3/P4 v2** (vs vide en v2-renum), (7) UDL 7 éléments P5-spécifiques documentés (vs absent en v2-renum), (8) audit des 4 failure modes Drew Breunig complet (vs absent en v2-renum), (9) XG-5.7 = matrice de conformité aux DDS P4 (équivalent XG-4.7), (10) Couverture cas universelle adaptative (6 cas alignés P3/P4), (11) Tokens budget explicite 5k/10k/15k (vs implicite), (12) Pauses (compaction 60-70% du soft cap), (13) Conditions de sortie (checklist 8 critères). 4 décisions tranchées par le mainteneur.
> **Changement vs structure antérieure** : P3 (Design) splitté en P3 (Architecture) + P4 (Design) le 2026-06-05 (fix structurel). P5 Implementation = ex-P4 Implementation renommée. Pas de changement de fond vs v2-renum, refonte ciblée pour aligner sur P3/P4 v2.
> **But** : transformer les DDS P4 et contrats d'interface en code production-ready, traçable jusqu'au design, couvert par des tests unitaires et un SAST clean, avec dette technique documentée — pour que P6 Testing puisse tester sans ambiguïté.

## Metadata

- **Phase**: 5
- **Name**: Implementation
- **Purpose**: Consume P4 detailed design (DDS + module interface contracts) and P3 architecture (ADRs) to produce production-ready code (modules implémentés, tests unitaires, CI/CD, dette technique trackée)
- **Parallel Mode**: Hyperagent enabled (multi-agent justifié, F13 recherche 2026 — read-heavy parallèle + disjoint tools : DDS P4 par module, code disjoint par Nexus)
- **Équivalent SWEBOK v4** : P4 SWEBOK (Software Construction KA — Code construction, Integration, Reuse, Technical debt tracking)
- **Référentiels** : IEEE 1028-2008 (Software Reviews), ISO/IEC/IEEE 12207:2017, NIST SSDF 800-218 (Secure Software Development Framework)

---

## Mission (1 phrase)

> « Consommer les DDS P4 + ADRs P3 et descendre au niveau code : organisation fichiers, naming, classes, dépendances, tests unitaires, CI/CD — pour que P6 Testing puisse tester sans ambiguïté et P7 Deployment puisse packager sans re-implémentation. »

---

## Critère de démarcation P4 (Design) vs P5 (Implementation) vs P6 (Testing)

> **Validation 2026-06-07** : le mainteneur a tranché pour deux critères explicites : (1) P4↔P5 symétrique à P3↔P4 (inscrit dans P4 ET P5), (2) P5↔P6 = **P5 = unit tests seuls, P6 = coverage + mutation + reste** (inscrit dans P5 ET P6 — action P6-N du mainteneur 2026-06-07).

| Dimension | P4 Design (déjà tranché) | P5 Implementation (cette spec) | P6 Testing (cf. spec dédiée) |
|-----------|--------------------------|--------------------------------|------------------------------|
| **Question centrale** | **QUOI** (signatures, interfaces, algorithmes) | **COMMENT** (organisation interne du code) | **Est-ce que le système complet fait ce qu'il dit et respecte les NFR ?** |
| **Périmètre** | Contrats d'interface modules + API REST + événements + DDS par module (signatures externes, structures de données, algos, error handling strategy, logging strategy) | Structure fichiers/répertoires, naming interne, classes abstraites, dépendances in-module, **unit tests seuls** (pas de coverage finale, pas de mutation), CI/CD config, build artifacts | **Couverture globale** (line + branch) + **Mutation testing** + Intégration + Système + Acceptance + Régression + Perf + Security + Observabilité |
| **Niveau d'abstraction** | Interfaces, signatures, comportements (vue externe du module) | Code concret, implémentation réelle + tests isolés (vue interne) | Tests inter-modules, bout-en-bout, NFR transverses (vue système) |
| **Livrables typiques** | `detailed-design.md` (DDS), `module-interfaces.md` (md+json modules internes, +OpenAPI REST, +AsyncAPI events), `data-structures.md`, `error-handling-design.md`, `logging-design.md`, `design-traceability-matrix.md` (DTAM + DRTM), `design-review-report.md`, matrice de conformité aux ADRs P3 (XG-4.7) | `source-code/`, `unit-test-suite.md` (unit tests seuls), `code-review-reports.md`, `coverage-report.md` (lint gate build), `ci-cd-pipeline.md`, `implementation-traceability.md` (matrice code → DDS P4), `technical-debt-register.md`, `effort-report.md` (T-shirt vs réel), `implementation-report.md` | `test-plan.md`, `integration-test-results.md`, `system-test-results.md`, `acceptance-test-results.md`, `regression-test-results.md`, `defect-report.md`, `test-traceability-matrix.md` (TTM), `test-closure-report.md`, `performance-test-report.md`, `security-test-report.md`, `mutation-testing-report.md`, `go-no-go-decision-memo.md` |
| **Décisions** | Tactiques (algorithme, structure de données, library au niveau interface) | Internes au code (organisation fichiers, naming, classes abstraites, dépendances in-module) | Externes au code (stratégie de test, choix outils, plan d'exécution, critères go/no-go) |
| **Agents typiques** | Nexus-Architect (lead), Nexus-Backend, Nexus-Frontend, Nexus-DevOps, Nexus-Security, Nexus-Critic | Nexus-Backend (lead code), Nexus-Frontend, Nexus-DevOps, Nexus-Security, Nexus-Critic | Nexus-QA-Lead (lead), Nexus-Backend/Frontend (résolution défauts), Nexus-DevOps (env), Nexus-Security (pentest), Nexus-Performance (perf), Nexus-Critic |
| **Adversarial** | T1 casseur DDS + T2 conformité NFR P2 + ADRs P3 + T3 prédiction aval P5 | T1 casseur code (pas de mutation testing) + T2 conformité DDS P4 + ADRs P3 + T3 prédiction aval P6 | T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 |

**Règle simple P4↔P5** : si la décision impacte **un module ou une classe** (organisation fichiers, naming interne, factorisation interne, choix de lib in-module, classes abstraites) = P5. Si elle impacte **l'interface externe du module** (signature, type de retour, contrat asynchrone, structure de données publique) = P4.

**Règle simple P5↔P6 (validation 2026-06-07)** : si la décision teste **une fonction ou classe isolément** (unit test) = P5. Si elle teste **plusieurs modules ensemble** (intégration/système/acceptance) ou **une NFR transverse** (perf, security, observabilité) ou **la qualité des tests** (mutation testing) = P6.

**Cas limite type P4↔P5** : "Module Billing = Repository pattern" (choix tactique) = **P4** (déjà dans le DDS P4). "Module Billing = `src/billing/{domain,infrastructure,interfaces}/` avec naming kebab-case pour les fichiers" = **P5**. "Module Billing = ajoute une dépendance à `pydantic` pour la validation" = **P5** (lib in-module).

**Cas limite type P5↔P6** : "Module billing = tester que la fonction `calculateTotal()` retourne 42" = **P5** (unit). "Module billing + Module payment = tester que le total calcule puis déclenche le paiement sans race condition" = **P6** (intégration). "Mutation testing sur `calculateTotal`" = **P6** (qualité des tests). "Tester que le système complet répond en < 200ms pour 95% des requêtes" = **P6** (perf NFR).

**Conséquence opérationnelle P4↔P5** : si P5 détecte qu'une décision descendante impacte l'interface externe du module (signature, comportement, structure publique), **elle escalade P4** (refus catégorique 1 — pas de re-décision design silencieuse). Si la décision impacte l'architecture (≥2 bounded contexts), escalade P3.

**Conséquence opérationnelle P5↔P6** : si P5 détecte qu'une décision touche à un test d'intégration/système/acceptance/perf/security ou à la qualité globale des tests (mutation), **elle escalade P6**. Si P5 détecte qu'un défaut émerge en cours d'implémentation qui demande une correction post-unit-test, **elle consigne dans `effort-report.md` et signale à P6** (P6 validera la résolution en intégration/système).

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-5.1 | Phase 4 design approved | Design baseline version | Approved version locked |
| EG-5.2 | Detailed design specifications complete | DDS coverage per module | 100% modules avec DDS |
| EG-5.3 | Module interface contracts finalized | Contract documents | 100% modules avec contrats (md+json modules internes, +OpenAPI REST, +AsyncAPI events) |
| EG-5.4 | Design traceability matrix established | DTAM + DRTM coverage | 100% éléments design tracés (archi P3 + reqs P2) |
| EG-5.5 | Matrice de conformité aux ADRs P3 validée | Matrice ADR → module | 100% ADRs P3 tracés par module (XG-4.7) |
| EG-5.6 | Development environment configured | Environment health check | All tools operational (compilateur, linter, test runner, SAST, coverage) |
| EG-5.7 | Module assignments defined | Assignment document | 100% modules assigned (qui code quoi) |
| EG-5.8 | CI/CD pipeline stages defined | Pipeline config | All stages configured (build, test, lint, SAST, coverage) |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers Phase 4 (Design) or Phase 3 (Architecture) remediation.

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-5.1 | All modules implemented | Implementation status | **≥95% modules** complétés (compromis mainteneur 2026-06-07) |
| XG-5.2 | Code review passed (T1 casseur) | Review findings | No critical/unresolved issues, T1 Nexus-Critic passé |
| XG-5.3 | Unit test coverage lint gate met (build) | Coverage report | ≥80% line coverage, ≥70% branch au **build** (lint gate, le build fail si <80% line). **La validation finale de la couverture + mutation testing sont en P6** (XG-6.2 + XG-6.3 P6 Testing). |
| XG-5.4 | Integration points implemented | Integration status | 100% interfaces DDS P4 connectées (tous les modules compilent ensemble) |
| XG-5.5 | Implementation traceability verified | ITM coverage | 100% code tracé au DDS P4 + ADR P3 + NFR P2 (chaque ligne de code → requirement) |
| XG-5.6 | Static analysis clean | SAST report | 0 critical security findings (semgrep, snyk, etc.) |
| XG-5.7 | **Conformité aux DDS P4 vérifiée** | **Matrice DDS → code** | **100% DDS P4 tracés par fichier de code (pas de déviation design silencieuse)** |
| XG-5.8 | UDL 7 éléments P5-spécifiques loggés | UDL set | 100% loggés dans `.swebok_state.db` (table `udl_p5`) |
| XG-5.9 | Effort report signé | effort-report.md | T-shirt estimé vs temps réel passé par module, signé par mainteneur |
| XG-5.10 | Technical debt register à jour | technical-debt-register.md | Toute dette introduite documentée avec rationale et plan de remédiation |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` requires implementation remediation.

**XG-5.1 — Adaptativité par profil projet (note)** : pour les projets compliance/sécurité (ex: finance, santé, défense), le seuil peut être relevé à ≥99% via décision mainteneur documentée dans `effort-report.md`. Pour les projets R&D/POC, il peut être abaissé à ≥80% avec justification. Décision par défaut = 95% (cette spec).

---

## Transition Criteria to Phase 6 (Testing)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Implementation freeze declared | Nexus-Backend/Frontend | Phase 6 Lead (Nexus-QA) | Feature freeze memo |
| Code complete status verified | Nexus-Critic (T2 conformité DDS P4) | QA Lead | Completeness report |
| Test environment readiness confirmed | Nexus-DevOps | Nexus-QA | Environment health check |
| Test data availability confirmed | Nexus-QA | Test Lead | Data set validation |
| Integration build successful | CI/CD | Nexus-QA | Build artifact verified |
| Effort report transmitted | Nexus-Backend/Frontend | Project Lead | effort-report.md signé |
| Technical debt register transmitted | Nexus-Architect | Project Lead | technical-debt-register.md à jour |
| Conformité DDS P4 vérifiée | Nexus-Architect (T2) | Phase 6 Lead | Matrice DDS → code (XG-5.7) |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_5_COMPLETE` only when all transition criteria verified with formal evidence.

---

## Key Activities

### Activity 5.1: Module Implementation
- Implémenter les modules backend selon les DDS P4 (signatures, comportements, structures de données)
- Implémenter les composants frontend selon les specs design
- Implémenter l'infrastructure-as-code (Terraform, Ansible, etc.)
- Implémenter les contrôles sécurité selon `security-architecture.md` (P3)
- Implémenter le logging et monitoring selon `logging-design.md` (P4)

### Activity 5.2: Code Quality
- Conduire des peer code reviews (pair programming simulé)
- Exécuter linters (ruff, eslint, etc.) — 0 erreur, 0 warning
- Atteindre les seuils de complexité cyclomatique (par module)
- Appliquer les conventions de naming (kebab-case fichiers, snake_case variables, etc.)
- Adresser la dette technique introduite (documentation dans `technical-debt-register.md`)

### Activity 5.3: Unit Testing (lint gate)
- Écrire les **unit tests seuls** pour chaque fonction/classe publique (P5 = unit seul, P6 = reste)
- Atteindre les seuils de coverage au **build** (XG-5.3, lint gate : le build fail si <80% line)
- Fixer les tests qui échouent
- Documenter les cas de test (en markdown + en code)
- **Note v2.1** : la **validation finale** de la couverture + le **mutation testing** sont en P6 (XG-6.2 + XG-6.3 P6 Testing), pas en P5.

### Activity 5.4: Integration Preparation
- Implémenter les interfaces d'intégration (consommateurs des contrats P3/P4)
- Préparer les test harnesses (pour P6)
- Configurer les stages CI/CD (build, test, lint, SAST, coverage, package)

### Activity 5.5: Adversarial Validation (Nexus-Critic — OBLIGATOIRE)
- **T1 casseur** : Nexus-Critic relit le code, cherche des cas limites, propose des mutations (mutation testing simulé). Cible : fichiers source par module.
- **T2 conformité** : Nexus-Critic vérifie la conformité aux DDS P4 (matrice DDS → code, XG-5.7) + ADRs P3 (consommation des décisions archi, pas de déviation). Cible : implémentation vs design.
- **T3 prédiction aval** : Nexus-Critic prédit ce qui va être dur à tester en P6 (casses potentiels, zones d'ambiguïté, dépendances cachées, dette technique introduite). Cible : interfaces d'intégration + complexité des modules.

### Activity 5.6: Effort Tracking
- Estimer chaque module en T-shirt size (S/M/L/XL) basé sur la complexité du DDS P4
- Mesurer le temps réel passé par module (par Nexus-Backend/Frontend)
- Comparer estimation vs réel dans `effort-report.md`
- Identifier les modules sous-estimés (>2× réel vs estimé) → escalade P3/P4 si design sous-estimé

---

## Responsible Agents

| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordonne les tâches d'implémentation parallèles (3-5 sub-agents) |
| Nexus-Backend | Lead code backend, implémentation des modules serveur |
| Nexus-Frontend | Implémentation des composants UI |
| Nexus-DevOps | Infrastructure-as-code, CI/CD config, observabilité |
| Nexus-Security | Secure coding, secrets management, rotation clés |
| **Nexus-Critic (5e agent obligatoire — décision mainteneur 2026-06-07)** | **T1 casseur + T2 conformité DDS P4 + ADRs P3 + T3 prédiction aval P6 — TOUS OBLIGATOIRES** (3 invocations systématiques, comme P3 et P4) |

**Concurrency** : multi-agent justifié (F13 recherche 2026 — read-heavy parallèle : DDS P4 par module, code disjoint par Nexus). 3-5 sub-agents en parallèle, jamais plus. **Nexus-Critic = 3 invocations systématiques** (T1 casse le code, T2 vérifie conformité DDS P4 + ADRs P3, T3 prédit les ruptures P6). Coût additionnel ~4.5k tokens, justifié par le hard cap 15k.

**Patterns adversariaux T1/T2/T3 (rappel)** :
- **T1 (casseur)** : un dev propose du code, Nexus-Critic casse. Cible : fichiers source, edge cases, mutation testing simulé.
- **T2 (spec-compliance)** : Nexus-Critic vérifie la conformité aux DDS P4 (matrice DDS → code, XG-5.7) + ADRs P3. Cible : implémentation vs design.
- **T3 (conséquentialiste)** : Nexus-Critic prédit ce qui va être dur à tester en P6. Cible : interfaces d'intégration + complexité + dette technique.

**Isolation des contextes (ACI stratégie §4.5)** : Nexus-Critic ne voit pas le prompt système des producteurs. Chaque rôle adversarial a un contexte distinct, sinon les "adversaires" se laissent influencer par le contexte partagé.

---

## Required Skills

- `nexus-backend`: Backend development (implémentation modules serveur)
- `nexus-frontend`: Frontend development (composants UI)
- `nexus-devops`: CI/CD et infrastructure-as-code
- `nexus-security`: Secure coding, SAST, secrets management
- `nexus-critic`: Adversarial validation (T1 casseur + T2 conformité + T3 aval) — **OBLIGATOIRE** (3 invocations)
- `speckit-qa`: Test implementation et coverage

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-implementation-complete` | Exit criteria met | Triggers Phase 6 (Testing) initiation |
| `module-implementation-complete` | Module done | Updates progress tracking |
| `code-review-passed` | Review approved | Enables merge to integration |
| `coverage-targets-met` | Coverage verified | Unblocks integration |
| `t1-casseur-passed` | T1 Nexus-Critic passé | Confirme robustesse du code |
| `t2-dds-conformity-verified` | Matrice DDS → code | Confirme conformité design (XG-5.7) |
| `t3-p6-prediction-logged` | T3 prédiction faite | Snapshot pour P6 |
| `udl-p5-logged` | 7 éléments UDL loggés | Snapshot pour phases suivantes |
| `effort-report-signed` | Effort report signé | Confirme estimation vs réel |

---

## Artifacts Produced

| Artifact | Description | Location | Format |
|----------|-------------|----------|--------|
| `source-code/` | Code source par module (généré depuis DDS P4) | `specs/workflows/by-phase/phase-5-implementation/source-code/` | Code (langage natif) |
| `unit-test-suite.md` | Documentation des suites de tests unitaires | `specs/workflows/by-phase/phase-5-implementation/` | md |
| `code-review-reports.md` | Revue pair-à-pair + T1 Nexus-Critic | `specs/workflows/by-phase/phase-5-implementation/` | md |
| `coverage-report.md` + `coverage.json` | Rapport de couverture | `specs/workflows/by-phase/phase-5-implementation/` | md + JSON+HTML |
| `implementation-traceability.md` | Matrice code → DDS P4 (XG-5.7) + ADR P3 + NFR P2 | `specs/workflows/by-phase/phase-5-implementation/` | md |
| `ci-cd-pipeline.md` | Configuration CI/CD (GitHub Actions, etc.) | `specs/workflows/by-phase/phase-5-implementation/` | md + YAML |
| `technical-debt-register.md` | Dette technique introduite (rationale + plan remédiation) | `specs/workflows/by-phase/phase-5-implementation/` | md |
| `effort-report.md` (NOUVEAU vs v2-renum) | Estimation T-shirt S/M/L/XL par module vs temps réel passé | `specs/workflows/by-phase/phase-5-implementation/` | md |
| `implementation-report.md` | Résumé 1 page (modules livrés, dette, estimations, sign-off) | `specs/workflows/by-phase/phase-5-implementation/` | md |

**Format de stockage du code** (transformation implicite — défaut) : **mono-repo avec sous-dossiers par module** (`source-code/${module}/`), adaptatif selon profil P0 (multi-repo si microservices détecté en P1).

**Format de la matrice de conformité (XG-5.7)** : matrice DDS P4 → fichier de code, avec pointeur unique. Chaque DDS du P4 a au moins un fichier de code qui l'implémente. Chaque fichier de code référence au moins un DDS P4. Pas de code orphelin (sans DDS), pas de DDS orphelin (sans code). Symétrique à la matrice ADR → module de P4 (XG-4.7).

---

## Format des fichiers

| Type de livrable | Format primaire | Format secondaire | Standard |
|------------------|------------------|-------------------|----------|
| **Code source** | Code natif (Python, TS, etc.) | — | Conventions du langage |
| **Specs narratives** (unit-test-suite, code-review-reports, implementation-traceability, ci-cd-pipeline, technical-debt-register, effort-report, implementation-report) | md (lecture humaine) | — | — |
| **Coverage report** | md (résumé) | JSON (machine-parse) + HTML (visualisation) | Istanbul/c8/coverage.py |
| **SAST report** | md (résumé) | SARIF/JSON (machine-parse) | semgrep, snyk |
| **Matrice de conformité DDS P4** (implementation-traceability.md) | md (lecture humaine) | table en markdown | — |

**Convention de nommage** :
- Code : conventions du langage (snake_case Python, camelCase JS, etc.)
- Specs narratives : `${livrable}.md`
- Coverage : `coverage.json` + `coverage.html`
- SAST : `sast.sarif` (si applicable)
- Tests : `test_${module}.py` ou `${module}.test.ts` (convention du framework)

**Localisation** : tous dans `specs/workflows/by-phase/phase-5-implementation/` (specs narratives) ou `specs/workflows/by-phase/phase-5-implementation/source-code/` (code).

---

## Hyperagent Parallel Processing

```
parallel_tasks:
  - task: backend_implementation
    agents: [Nexus-Backend, Nexus-Security]
    sync: false

  - task: frontend_implementation
    agents: [Nexus-Frontend, Nexus-Backend]
    sync: false

  - task: infrastructure_implementation
    agents: [Nexus-DevOps]
    sync: false

  - task: security_implementation
    agents: [Nexus-Security, Nexus-Backend]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après parallel):
  - task: t1_casseur
    agents: [Nexus-Critic]
    target: source-code/ par module
    sync: true

  - task: t2_conformite
    agents: [Nexus-Critic]
    target: implémentation vs DDS P4 + ADRs P3 (matrice XG-5.7)
    sync: true

  - task: t3_prediction_p6
    agents: [Nexus-Critic]
    target: interfaces d'intégration + dette technique introduite
    sync: true

reduction: "Hyperagent-Orchestrator aggregates status into implementation-report.md + effort-report.md + technical-debt-register.md"
```

---

## Refus catégoriques (7)

La phase P5 **refuse** de :
1. **Pas de re-décision design** (escalade P4 si déviation DDS détectée — règle de démarcation)
2. **Pas de re-décision architecturale** (escalade P3 si décision impacte ≥2 bounded contexts)
3. **Pas de feature non-spec** (refus du gold-plating / YAGNI)
4. **Pas de dette technique non documentée** (toute dette introduite → `technical-debt-register.md`)
5. **Pas de dépendance non-justifiée** (vendor lock-in check, rationale documenté)
6. **Pas de merge sans review** (T1 casseur Nexus-Critic obligatoire)
7. **Pas de SAST critique accepté** (XG-5.6 = 0 critical)

---

## Critères d'abandon (5 + temps)

L'agent abandonne et prévient le mainteneur si :
1. DDS P4 non respecté et déviation non escaladée (escalade P4)
2. Effort réel > 2× estimation pour >30% des modules (signaling: design sous-estimé, escalade P3/P4)
3. Conflit de contrats d'interface DDS P4 (signaling: design incomplet, escalade P4)
4. Coverage < cible après 2 itérations (escalade P4 pour DDS incomplets, ou P5 pour tests incomplets)
5. SAST critique non résolvable (décision mainteneur : accepter dette ou bloquer)
6. Dépassement de 35 min sans avancée claire

---

## Tokens budget

- **Base** : 5k tokens
- **Soft cap** : 10k tokens (alerte, compaction 60-70% = 6-7k)
- **Hard cap** : 15k tokens (compactage forcé + abort)

Multi-agent justifié (F13 recherche 2026) : 3-5 sub-agents en parallèle × 1.5k chacun = 4.5-7.5k base. Cap 15k hard pour absorber les validations adversariales T1+T2+T3 obligatoires (Nexus-Critic en mode rotation sur les 3 patterns, comme P3 et P4 — décision mainteneur 2026-06-07). **Justification du maintien 15k** : Nexus-Critic T1+T2+T3 obligatoire = 3 invocations × ~1.5k = 4.5k additionnel, ce qui sature le budget 10k en nominal. 15k = marge de sécurité pour absorber les validations adversariales complètes, en cohérence avec P3 Architecture et P4 Design (5k/8k/15k).

**Note** : P5 reste 2e phase la plus large (ex-aequo avec P3, P4), au lieu de 1re. Acceptable car le code = l'activité 1 du projet et le sur-coût est compensé par la qualité (matrice DDS → code, tests unitaires, dette technique trackée, effort report).

---

## Pauses

Toutes les 5 actions : compaction checkpoint à 60-70% du soft cap (6-7k tokens, F8 recherche 2026). Compaction sélective : garder les décisions et les diffs, drop les résultats d'outils intermédiaires (lint output, test results, coverage raw).

**Pre-hydrate obligatoire** (F7 recherche 2026 — 60% du 1er tour = retrieval) : au début de P5, charger dans le hot_context (`.swebok_state.db`) la slice suivante :
- Liste des modules à implémenter (pointeurs vers DDS P4)
- Matrice de conformité ADR P3 (héritée de P4, XG-4.7)
- Conventions de naming et d'organisation fichiers (décision P5 par défaut)
- Seuils de coverage (XG-5.3)

Sans ce pre-hydrate, 60% du budget du 1er tour est consommé en retrieval, ce qui sature le soft cap en nominal.

---

## Couverture corpus (état 2026-06-06)

- **100% de couverture** — P5 = phase la mieux couverte (68 livres corpus-aligned sur ~30 recommandés)
- **68 livres corpus-aligned** : Mac Studio (63) + New Books (5) + Standards NIST/OWASP (4) + Open-access (5)
- **3 livres manquants critiques** (non bloquants) : Effective Java 3rd ed. (Bloch 2018), An Elegant Puzzle (Larson 2024)
- **Décision mainteneur 2026-06-06** : 100% suffit pour P5. Batch d'acquisition ultérieur (action P2-N roadmap).

**Livres canoniques P5** (extrait, voir grille §5.3 pour la liste complète) :
- Pragmatic Programmer (Hunt & Thomas 2019, 20th ed.)
- Clean Coder (Martin 2011)
- Clean Code (Martin 2008)
- Code Complete 2nd ed. (McConnell 2004)
- Mythical Man-Month (Brooks 1975/1995)
- NIST SSDF 800-218 (Secure Software Development Framework)

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :

1. **Greenfield from-scratch** : implémentation from scratch, 5-10 modules typiques, dette technique minimale, effort report = baseline de référence
2. **Maintenance legacy** : P5 = "que doit-on modifier pour respecter le DDS P4", dette technique P9 pré-existante à inventorier
3. **Projet interne** (équipe, gouvernance légère) : implémentation rapide, peer review suffisant, T1 casseur optionnel (T2+T3 obligatoires)
4. **Projet externe client** : implémentation revue par architecte client, sign-off formel, T1+T2+T3 tous obligatoires + revue externe
5. **Compliance-driven** (finance, santé, défense) : implémentation security-heavy, SAST + tests + coverage + traçabilité renforcés, XG-5.1 relevé à ≥99% par décision mainteneur
6. **R&D / exploration** : implémentation POC, XG-5.1 abaissé à ≥80% avec justification dans effort-report.md, dette technique acceptée explicitement

---

## UDL — 7 éléments P5-spécifiques

> **Validation 2026-06-07** : 7 éléments P5-spécifiques (aligné P2, P3, P4). **Note v2.1** : mutation testing retiré de P5 (basculé en P6).

| Élément | Description | Exemple |
|---------|-------------|---------|
| **Module code completed** | Pointeur vers `source-code/${module}/` + hash du commit | "Module billing = `source-code/billing/` commit `a3f9d2`" |
| **Library / dependency added** | Rationale + vendor lock-in check | "Ajout de `pydantic` v2 pour validation, alternative `marshmallow` écartée (perf), lock-in faible (open source)" |
| **Estimation réelle vs estimée** | T-shirt size S/M/L/XL estimé vs heures réelles passées | "Module billing estimé M (4-8h), réel 12h (sous-estimé 50%), raison = DDS incomplet sur les cas d'erreur" |
| **Reuse vs create-from-scratch** | Décision documentée (import lib externe vs code interne vs from scratch) | "Module auth = reuse `authlib` (battle-tested) vs from scratch (réinventer la roue, risque sécurité)" |
| **Dette technique introduite** | Pointeur vers `technical-debt-register.md` avec rationale | "Module reporting = utilise `eval()` pour parser les formules dynamiques, dette TD-005 avec plan migration vers AST en P9" |
| **Rejet T1/T2 casseur** | Quand Nexus-Critic a trouvé un problème et comment c'est résolu | "T1 a trouvé injection SQL dans module X via concaténation, corrigé via parameterized queries + review" |
| **Décision "pas de décision"** | Cas où on a choisi de NE PAS trancher, et pourquoi | "Pas d'arbitrage perf vs memory pour cache LRU : escaladé P6 (P5 ne mesure pas la perf, c'est P6+P8)" |

**Note v2.1** : la mutation testing n'est plus un UDL P5 (c'est un livrable P6 : `mutation-testing-report.md`). Le coverage est tracké au build (lint gate, XG-5.3) et validé en P6 (XG-6.2).

Stockés dans `.swebok_state.db` (table `udl_p5`) et consultables via Consultation Envelope (A1) par P6 Testing.

---

## Conditions de sortie (passage à P6)

Le mainteneur valide avec une **checklist à 100%** (10 critères) :
- [ ] `source-code/` existe (≥95% modules, XG-5.1)
- [ ] `unit-test-suite.md` existe (coverage ≥80% line, ≥70% branch, XG-5.3)
- [ ] `code-review-reports.md` existe (T1 casseur Nexus-Critic passé)
- [ ] `coverage-report.md` + `coverage.json` + `coverage.html` existent
- [ ] `implementation-traceability.md` existe (matrice DDS → code, XG-5.7)
- [ ] `ci-cd-pipeline.md` existe (build + test + lint + SAST + coverage stages)
- [ ] `technical-debt-register.md` existe (toute dette introduite documentée)
- [ ] `effort-report.md` existe (T-shirt vs réel signé par mainteneur)
- [ ] `implementation-report.md` existe (résumé 1 page)
- [ ] UDL 7 éléments loggés dans `.swebok_state.db`

Pas de feu vert séparé — les documents font foi.

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-07

### Mode 1 — Poisoning (Empoisonnement)
**Risque en P5** : un module mal implémenté qui contamine tous les modules dépendants (effet papillon module par module, propagation de l'erreur dans tout le code).

**Mitigations spec v2** :
1. Chaque module challengé par Nexus-Critic T1 casseur (3 invocations systématiques, comme P3 et P4)
2. Conformité aux DDS P4 vérifiée par matrice DDS → code (XG-5.7) — pas de déviation design silencieuse
3. Conformité aux ADRs P3 vérifiée par héritage de la matrice P4 (XG-4.7)
4. Validation mainteneur finale (checklist 10 critères) = catch du poison
5. UDL 6 ("rejet T1/T2 casseur") logge les modules rejetés et comment c'est résolu
6. SAST 0 critical obligatoire (XG-5.6) = filet sur les vulnérabilités classiques (injection, XSS, etc.)

**Status** : ✅ Validé (6 mécanismes)

### Mode 2 — Distraction (Distraction)
**Risque en P5** : scope creep (gold-plating), features non-spec ajoutées "tant qu'on y est".

**Mitigations spec v2** :
1. Refus catégorique 3 (pas de feature non-spec) + 1 (pas de re-décision design) = focus forcé
2. Budget 5k/10k/15k (large mais pas infini, force à prioriser)
3. 3-5 sub-agents max (vs 50 subagents, F2 recherche 2026)
4. UDL 1 ("module code completed") force à pointer vers le DDS P4 d'origine (pas de scope libre)
5. UDL 7 ("décision 'pas de décision'") force à documenter les arbitrages
6. Couverture cas universelle adaptative (6 cas) cadre le périmètre

**Status** : ✅ Validé (6 mécanismes)

### Mode 3 — Confusion (Confusion)
**Risque en P5** : 2 modules utilisent le même nom pour 2 fonctions différentes, ou tests unitaires qui ne testent rien (test theater).

**Mitigations spec v2** :
1. Conventions de naming imposées par module (kebab-case fichiers, snake_case variables) + lint 0 erreur
2. UDL 1 ("module code completed") trace chaque module par pointeur unique
3. Nexus-Critic T2 conformité DDS P4 + ADRs P3 détecte les clashes de nommage
4. UDL 3 ("estimation réelle vs estimée") force à mesurer le temps passé par module (signal de complexité)
5. Coverage ≥80% line + ≥70% branch (XG-5.3) + T1 casseur sur les tests (mutation testing simulé)
6. Code review pair-à-pair obligatoire avant merge (refus catégorique 6)

**Status** : ✅ Validé (6 mécanismes)

### Mode 4 — Clash (Conflit)
**Risque en P5** : 2 modules qui s'appellent avec des signatures différentes (modification silencieuse des contrats P3/P4), ou merge conflicts en cascade.

**Mitigations spec v2** :
1. Module interface contracts figés en P3/P4 (pas de modification en P5, escalade P4 si déviation)
2. Nexus-Critic T2 conformité DDS P4 catch les clashes de signature
3. UDL 2 ("library / dependency added") documente les versions de chaque lib (évite les conflits de version)
4. UDL 4 ("reuse vs create-from-scratch") force à documenter les décisions d'import
5. Critère d'abandon 3 (conflit de contrats d'interface DDS P4) = escalade P4
6. Critère d'abandon 1 (DDS P4 non respecté et déviation non escaladée) = sortie propre
7. CI/CD pipeline avec tests d'intégration obligatoires (XG-5.4) détecte les clashes au build

**Status** : ✅ Validé (7 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | Module mal implémenté contamine tout | 6 mécanismes | ✅ |
| Distraction | Scope creep, gold-plating | 6 mécanismes | ✅ |
| Confusion | Nommage ambigu, test theater | 6 mécanismes | ✅ |
| Clash | Contrats modifiés silencieusement, merge conflicts | 7 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Pattern reproductible de P0/P2/P3/P4 v2 étendu à P5.

---

## Notes de version

- **v2 (2026-06-07)** : refonte ciblée via audit (grille offline + 4 questions ciblées vague 1). Changements : (1) critère explicite de démarcation P4↔P5 inscrit dans P5 (organisation interne du code vs signatures externes/algorithmes, règle ≥1 module), (2) Nexus-Critic T1 casseur + T2 conformité DDS P4 + ADRs P3 + T3 prédiction aval P6 OBLIGATOIRE (3 invocations systématiques, comme P3 et P4), (3) effort-report.md = livrable formel (comble P4 SWEBOK absente, estimation T-shirt S/M/L/XL par module vs temps réel passé), (4) XG-5.1 = ≥95% partout (compromis mainteneur entre rigueur grille ≥99% et pragmatisme spec v2-renum ≥80%), (5) section 5.5 transformée en 7 questions précises avec options AskUserQuestion (vs vide en v2-renum), (6) section 7 comblée par projection + cohérence P0/P1/P2/P3/P4 v2 (vs vide en v2-renum), (7) UDL 7 éléments P5-spécifiques documentés (vs absent en v2-renum), (8) audit des 4 failure modes Drew Breunig complet (vs absent en v2-renum), (9) XG-5.7 = matrice de conformité aux DDS P4 (équivalent XG-4.7), (10) Couverture cas universelle adaptative (6 cas alignés P3/P4), (11) Tokens budget explicite 5k/10k/15k (vs implicite), (12) Pauses (compaction 60-70% du soft cap), (13) Conditions de sortie (checklist 10 critères). 4 décisions tranchées par le mainteneur.
- **v2-renum (2026-06-05)** : créé suite au fix structurel (renommage cascade P4→P5 après split P3). 4 activités, 6 livrables, 5 agents en parallèle (pas de Nexus-Critic), 5k/10k/15k tokens, cap 35 min, pas de UDL documenté, pas d'audit Drew Breunig, pas de démarcation P4↔P5, pas de matrice de conformité DDS P4.

Voir `audit/phase-5-implementation-audit.md` pour la traçabilité des 4 décisions.
