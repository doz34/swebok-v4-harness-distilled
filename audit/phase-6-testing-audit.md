# Audit — Phase 6 : Testing

> **Statut** : v2 — validé 2026-06-07 par le mainteneur (audit P6 clos via grille offline + 4 questions vague 1 + 3 questions section 7, verdict 🟢 dès la première conversation)
> **Changement vs v1** : (1) critère explicite de démarcation P5↔P6 inscrit (P5 = unit tests seuls, P6 = coverage + mutation + reste), (2) Nexus-Critic T1+T2+T3 OBLIGATOIRE (3 invocations systématiques, comme P3/P4/P5), (3) budget 4k/7k/10k → 5k/8k/15k (cohérence P3/P4/P5), (4) section 5.5 transformée en 7 questions précises avec options AskUserQuestion, (5) section 7 comblée par 3 questions de projection + cohérence P0/P1/P2/P3/P4/P5 v2 (effort 20-40% projet, 4 frictions + 4 contournements, 3 risques dette orchestration), (6) section 8.5 UDL 7 éléments P6-spécifiques documentée, (7) 4 décisions tranchées vague 1 + 3 décisions projection section 7, (8) verdict global 🟢.

## Métadonnées
- Phase : 6
- Nom : Testing
- Équivalent SWEBOK v4 : P5 SWEBOK (Testing KA)
- Spec existante : `specs/workflows/by-phase/phase-6-testing.md` (v2)
- Date de l'audit : 2026-06-07
- Auditeur : mainteneur

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
> « Consommer le code P5 (source + coverage) et les acceptance criteria P2, exécuter les 4 niveaux de test (intégration, système, acceptance, régression) + les 2 transverses (perf, security) + mutation testing, tracker les défauts, et produire un test closure report + go/no-go memo pour P7 Deployment — sans modifier le code (escalade P5) ni redéfinir les NFR (escalade P2). »

### 1.2 Périmètre
- [x] A. Test planning + execution + defect management + reporting (4 activités)
- [x] B. Intégration, système, acceptance, régression (4 niveaux)
- [x] C. **Performance testing** (NFR perf P2)
- [x] D. **Security testing** (DAST, pentest OWASP ASVS 5.0)
- [x] E. **Mutation testing** (mesure qualité des tests, XG-6.3 ≥70% par défaut)
- [x] F. **Couverture globale** (line + branch, validation finale XG-6.2)
- [x] G. **Observabilité** (vérifier que le système est debuggable en prod)

### 1.3 Hors-périmètre
- [x] A. Pas de modification du code de production (escalade P5)
- [x] B. Pas de redéfinition des NFR (escalade P2)
- [x] C. Pas de modification des tests unitaires P5 (escalade P5)
- [x] D. Pas de déploiement (P7 Deployment)
- [x] E. Pas de monitoring/alerting en continu (P8 Operations)

### 1.4 Verdict
- [x] 🟢 OK

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] EG-6.1 : Phase 5 implementation complete (≥95% modules, XG-5.1 P5)
- [x] EG-6.2 : Unit test suite available (tests unitaires présents P5)
- [x] EG-6.3 : Build coverage gate passed (≥80% line + ≥70% branch, lint gate P5 XG-5.3)
- [x] EG-6.4 : Acceptance criteria P2 définis (100% requirements avec AC)
- [x] EG-6.5 : NFR P2 ratified (100% NFR perf + security + observability validés P2)
- [x] EG-6.6 : Test environments prepared (4 envs : intégration, système, acceptance, perf + 1 security iso-prod)
- [x] EG-6.7 : Test data defined (synthétiques / anonymisées / prod-like)
- [x] EG-6.8 : Test harnesses ready (4 harnesses fonctionnels)
- [x] EG-6.9 : Test plan approved (plan de test formellement approuvé)
- [x] EG-6.10 : Conformité DDS P4 vérifiée (matrice DDS → code XG-5.7, hérité de P5)

### 2.2 Critères de complétion (XG-6.1 à XG-6.10)
- [x] XG-6.1 : 100% test plans executed (4 niveaux + 2 transverses)
- [x] XG-6.2 : Coverage validée (≥80% line + ≥70% branch en contexte d'exécution réelle)
- [x] XG-6.3 : Mutation score achieved (≥70% par défaut, adaptatif par profil)
- [x] XG-6.4 : Defect backlog stabilized (≤1 critical ouvert, ≤5 high, ≤20 medium)
- [x] XG-6.5 : Test traceability verified (TTM 100% tests tracés AC + NFR + DDS)
- [x] XG-6.6 : NFR perf validés (100% NFR perf P2, latence p95 + throughput + scalabilité)
- [x] XG-6.7 : NFR security validés (0 critical security finding, 0 high non résolu)
- [x] XG-6.8 : Release readiness confirmed (tous critères green + sign-off mainteneur)
- [x] XG-6.9 : UDL 7 éléments P6-spécifiques loggés (`.swebok_state.db` table `udl_p6`)
- [x] XG-6.10 : Conformité acceptance criteria P2 vérifiée (matrice AC → test)

### 2.3 Conditions d'échec → escalade
- [x] A. Défaut critique non résolvable après 3 itérations → escalade mainteneur
- [x] B. Couverture < cible après 2 itérations → escalade P5
- [x] C. Mutation score < seuil sans dette acceptable → escalade P5 ou décision mainteneur
- [x] D. Performance non-conforme aux NFR P2 → escalade P3 (design sous-jacent)
- [x] E. Security finding critique non patchable rapidement → escalade mainteneur
- [x] F. Test data manquante ou non représentative → escalade Nexus-DevOps ou décision mainteneur

### 2.4 Verdict
- [x] 🟢 OK

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. Phase 5 code + unit tests (P5 source-code/, unit-test-suite.md)
- [x] B. Phase 2 acceptance criteria (P2 SRS IEEE 830)
- [x] C. Phase 2 NFR (perf, security, observability)
- [x] D. Phase 5 coverage report (lint gate build, P5 XG-5.3)
- [x] E. Phase 4 DDS (detailed design, contrats d'interface modules)
- [x] F. Phase 3 ADRs (architectural decisions)
- [x] G. Phase 5 conformité DDS (matrice DDS → code, XG-5.7)

### 3.2 Depuis l'utilisateur
- [x] A. Go/no-go pour le déploiement (décision documentée, sign-off)
- [x] B. Décision sur les défauts "acceptés" (workaround vs fix vs defer)
- [x] C. Acceptation des défauts de basse priorité (dette de test documentée)

### 3.3 Depuis sources externes
- **Couverture corpus** : 13% (4 ressources corpus-aligned, 2e phase la moins couverte)
  - Mac Studio (2 livres : Full Stack Testing Mohan, Introduction to Software Testing)
  - Standards NIST/OWASP (1 : NIST 800-22r1a)
  - Open-access (1 : Lessons Learned in Software Testing Kaner, OWASP ASVS 5.0)
- **Lacunes critiques** : Testing KA SWEBOK (Beizer, Kaner, Bach, etc.) — non acquis
- **Décision mainteneur 2026-06-06** : 13% suffit pour cadrage, batch d'acquisition ultérieur (action P1-N roadmap)

### 3.4 Verdict
- [x] 🟢 OK

---

## Section 4 — Outputs

### 4.1 Deliverables concrets (11 livrables, grille mainteneur maintenue)
- [x] A. `test-plan.md` (stratégie par niveau + transverses, outils, séquencement)
- [x] B. `integration-test-results.md` (résultats inter-modules)
- [x] C. `system-test-results.md` (résultats bout-en-bout)
- [x] D. `acceptance-test-results.md` (vs acceptance criteria P2)
- [x] E. `defect-report.md` (log + disposition fix/wontfix/defer)
- [x] F. `test-traceability-matrix.md` (TTM, test → AC + NFR + DDS)
- [x] G. `test-closure-report.md` (résumé exécutif, 1 page vue exécutive + détails)
- [x] H. `performance-test-report.md` (NFR perf, k6/JMeter)
- [x] I. `security-test-report.md` (DAST + pentest, OWASP ASVS 5.0)
- [x] J. `mutation-testing-report.md` (mutation score, mutants survivants)
- [x] K. `go-no-go-decision-memo.md` (1 page, décision, sign-off)
- [x] L. `regression-test-results.md` (résultats régression, ajouté pour complétude)

### 4.2 Format de stockage (triple différencié aligné P3/P4/P5 v2)
- [x] A. Markdown pour les rapports humains
- [x] B. JSON pour les résultats machine-parse (perf, mutation, defect log)
- [x] C. SARIF pour les security findings (standard OWASP)
- [x] D. HTML pour les graphiques de perf
- [x] E. md+table pour TTM (matrice lisible)

### 4.3 Format de présentation à l'utilisateur
- [x] A. Test closure report en vue exécutive (1 page synthèse)
- [x] B. Dashboard temps réel pendant l'exécution (optionnel)
- [x] C. Go/no-go memo en 1 page (décision + rationale + sign-off)

### 4.4 Auditabilité
- [x] A. Oui — TTM 100% + results stockés (md+json+SARIF)
- [x] B. Justification des défauts acceptés (workaround vs fix vs defer) documentée dans defect-report.md

### 4.5 Verdict
- [x] 🟢 OK

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés (5 obligatoires + transverses)
- [x] A. Hyperagent-Orchestrator (coordination)
- [x] B. **Nexus-QA-Lead** (lead, sign-off closure + go/no-go)
- [x] C. Nexus-Backend, Nexus-Frontend (résolution défauts)
- [x] D. Nexus-DevOps (env management, isolation, observabilité)
- [x] E. **Nexus-Performance** (tests de charge, NFR perf)
- [x] F. **Nexus-Security** (pentest, DAST, OWASP ASVS 5.0)
- [x] G. speckit-qa (QA framework, automated tests)
- [x] H. **Nexus-Critic (5e agent obligatoire — décision mainteneur 2026-06-07)** : **T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 — TOUS OBLIGATOIRES** (3 invocations systématiques, comme P3/P4/P5)
- [x] I. **+ T1 (Test Designer vs Test Adversary)** : un agent conçoit les tests, l'autre essaie de trouver des trous
- [x] J. **+ T2 (Acceptance Compliance)** : chaque acceptance criteria P2 a son test ?
- [x] K. **+ T3 (Production Predictor)** : prédire quels défauts vont se manifester en prod/P7

### 5.2 Tools disponibles
- [x] A. `nexus-qa`, `nexus-qa-lead` (spec)
- [x] B. `speckit-qa` (spec)
- [x] C. `nexus-devops`, `nexus-backend`, `nexus-frontend`, `nexus-security`, `nexus-performance` (spec)
- [x] D. Test runners (pytest, jest, etc.)
- [x] E. Coverage tools (coverage.py, c8, etc.) — lint gate P5, validation finale P6
- [x] F. **Mutation testing** (mutmut, stryker, PIT, etc.)
- [x] G. Performance tools (k6, JMeter, etc.)
- [x] H. Security tools (OWASP ZAP, Burp, etc.)
- [x] I. Consult L0 corpus via tool (test-strategy principles, test-design techniques)

### 5.3 Knowledge items consultés

**Référentiel principal** : `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`

**Sections clés du référentiel à consulter** :
- **§18** : Sources locales — Mac Studio (117 livres corpus-matching identifiés)
- **§20** : Lacunes restantes (43 livres non encore acquis, alternatives ≥ 2017)
- **§13** : Standards NIST/OWASP (44 documents, open access)

**Livres canoniques disponibles localement pour cette phase** (4 ressources corpus-aligned sur ~15 recommandées = **13%**) :
- **Mac Studio** : 2 livres (Full Stack Testing Mohan, Introduction to Software Testing)
- **Standards** : 1 NIST/OWASP (NIST 800-22r1a)
- **Open-access** : 1 livre (Lessons Learned in Software Testing Kaner) + OWASP ASVS 5.0

**Lacunes critiques (§20)** : Testing KA SWEBOK (Beizer, Kaner, Bach, etc.) — non bloquants pour cadrage.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.

### 5.4 Pattern adversarial applicable
- [x] A. T1 critique (Test Designer vs Test Adversary)
- [x] B. T2 critique (Acceptance Compliance — chaque AC P2 a son test ?)
- [x] C. T3 applicable (Production Predictor — ruptures P7)
- [x] D. Council pour les go/no-go structurants
- [x] E. **T1 casseur tests + T2 conformité AC P2 + T3 prédiction aval P7 — TOUS OBLIGATOIRES** (Nexus-Critic 3 invocations systématiques, comme P3/P4/P5)

### 5.5 Points de décision utilisateur (7 questions précises avec options AskUserQuestion)

> **Validation 2026-06-07** : section 5.5 transformée de "catégories" en 7 questions précises, aligné P3/P4/P5 v2 finale.

**Q1 — Stratégie de test par niveau**
- A) **Bottom-up** : unit → intégration → système → acceptance (recommandé pour greenfield)
- B) **Top-down** : acceptance → système → intégration (recommandé pour maintenance legacy)
- C) **Big-bang** : tout en parallèle (risqué, non recommandé sauf POC)

**Q2 — Stratégie de test data**
- A) **Synthétique** : données générées à la demande (rapide, peu représentatif)
- B) **Anonymisée** : données prod anonymisées (équilibre réalisme/risque, recommandé)
- C) **Prod-like** : données ressemblant à la prod (réaliste, effort de génération élevé)
- D) **Prod réelle (subset)** : sous-ensemble prod non anonymisé (fort réalisme, fort risque RGPD)

**Q3 — Stratégie de test environment**
- A) **Docker local** (rapide, peu iso-prod, recommandé pour intégration)
- B) **Cloud staging iso-prod** (recommandé pour système, acceptance, perf, security)
- C) **On-prem iso-prod** (pour compliance, finance, santé, défense)

**Q4 — Outils de test prioritaires**
- A) **Framework + coverage + mutation + perf + security** (recommandé, pile complète)
- B) **Framework + coverage + perf + security** (sans mutation, économie)
- C) **Framework + coverage seul** (minimal, R&D POC)

**Q5 — Gestion des défauts — modèle de sévérité**
- A) **Critical/High/Medium/Low** (4 niveaux, standard IEEE 829, recommandé)
- B) **Blocker/Critical/Major/Minor/Trivial** (5 niveaux, plus granulaire)
- C) **S0/S1/S2/S3** (numérique, Google-style)

**Q6 — Stratégie de go/no-go**
- A) **Criteria-based + Project Sponsor sign-off** (recommandé, criteria objectifs + sign-off humain)
- B) **Voting multi-stakeholders** (QA + Dev + PO + Security, consensus)
- C) **Unilateral Project Sponsor** (rapide, moins robuste)

**Q7 — Stratégie de régression**
- A) **Full regression par nuit + selective sur commit** (recommandé, équilibre temps/couverture)
- B) **Full regression par commit** (coûteux, très robuste)
- C) **Selective regression uniquement** (rapide, risque de régression non détectée)

### 5.6 Verdict
- [x] 🟢 OK (100%, 7 questions précises actionnables)

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques (7)
1. Pas de modification du code de production (escalade P5)
2. Pas de redéfinition des NFR (escalade P2)
3. Pas de modification des tests unitaires P5 (escalade P5)
4. Pas de go avec défauts critiques ouverts (XG-6.4 : ≤1 critical ouvert)
5. Pas de skip de tests sans justification (chaque skip documenté)
6. Pas de "test passed" sur tests flaky (le flaky = 0 jusqu'à preuve de stabilité)
7. Pas de mutation score < seuil accepté sans dette documentée (XG-6.3 = ≥70% par défaut)

### 6.2 Modes d'échec connus (4 frictions + 2 complémentaires)
1. **Test theater** (100% coverage, 0% utile) — mitigated par mutation testing
2. **Flaky tests** (les devs apprennent à les ignorer) — mitigated par refus catégorique 6
3. **Env drift** ("ça marche sur ma machine") — mitigated par EG-6.6 envs iso-prod
4. **Mutation score gaming** (muter des lignes triviales) — mitigated par UDL 4 + T1 casseur
5. **Integration hell** (env pas iso-prod) — mitigated par EG-6.6
6. **Defect backlog qui grossit sans triage** — mitigated par Activity 6.4 (defect management)

### 6.3 Cas limites (5 + 1 adaptatif)
- A. Criticalité forte (test d'aviation, medical) — coverage + mutation relevés
- B. Non-determinism (ML, random algorithms) — tests property-based
- C. State-dependent (BDD, time-based) — mock time, fixtures
- D. External dependencies (third-party APIs) — mocking + contract testing
- E. Pas d'env de test iso-prod (par budget ou contrainte) — escalade mainteneur

### 6.4 Règles d'escalade (6 + 1)
1. Défaut critique non résolvable après 3 itérations → escalade mainteneur
2. Performance non-conforme aux NFR P2 → escalade P3 (design)
3. Couverture < cible après 2 itérations → escalade P5
4. Security finding critique non patchable rapidement → escalade mainteneur
5. Mutation score < seuil sans dette acceptable → escalade P5 ou décision mainteneur
6. Test data manquante ou non représentative → escalade Nexus-DevOps

### 6.5 Verdict
- [x] 🟢 OK

---

## Section 7 — Adéquation aux besoins (utilité)

> **Validation 2026-06-07** : section 7 comblée par 3 questions de projection + cohérence P0/P1/P2/P3/P4/P5 v2 (vs vide en v1). Décisions mainteneur : (1) effort P6 = 20-40% projet, valeur = NFR, (2) 4 frictions + 4 contournements typiques, (3) 3 risques de dette orchestration.

### 7.1 Usage réel
P6 = phase lourde, **effort = 20-40% de l'effort total projet** (décision mainteneur 2026-06-07). C'est la 2e phase la plus coûteuse après P5 Implementation. Profil d'usage typique par projet (le profil P0 + détection auto adapte le déroulé) :

| Profil projet | Effort P6 | Couverture cible | Mutation | Perf+Security | Valeur typique |
|---------------|-----------|-------------------|----------|----------------|-----------------|
| **Greenfield from-scratch** | 30% | ≥85% line, ≥75% branch | ≥75% | Baselines perf+sec établies | Confiance prod dès V1, 0 régression critique en prod sur 90 jours |
| **Maintenance legacy** | 25% | ≥80% line, ≥70% branch | ≥60% | Tests régression renforcis | Zéro régression sur périmètre modifié, dette de test documentée |
| **Projet interne** | 15% | ≥75% line, ≥65% branch | ≥50% (option) | Smoke perf+sec | Smoke test + acceptance criteria validés, go/no-go rapide |
| **Projet externe client** | 35% | ≥90% line, ≥80% branch | ≥80% | Sign-off client perf+sec | NFR + acceptance criteria signés par client, go/no-go contractuel |
| **Compliance-driven** (finance, santé, défense) | 40% | ≥95% line, ≥90% branch | ≥85% | OWASP ASVS 5.0 niveau 3, pentest externe | Conformité auditable, certification possible (ISO 27001, SOC2, HDS) |
| **R&D / exploration** | 20% | ≥70% line, ≥60% branch | ≥50% (justifié) | Smoke perf+sec | Smoke + acceptance, dette de test acceptée explicitement |

### 7.2 Friction observée (4 frictions + 4 contournements, décision mainteneur 2026-06-07)
| Friction | Description | Mitigation spec v2 |
|----------|-------------|---------------------|
| **F1 Test theater** | 100% coverage, 0% utile (tests qui ne testent rien) | Mutation testing obligatoire (XG-6.3) détecte les mutants survivants = tests faibles. UDL 4 ("coverage achieved") expose la granularité par module. T1 casseur tests casse les faux tests. |
| **F2 Flaky tests** | Les devs apprennent à les ignorer → tests skippés | Refus catégorique 6 (pas de "test passed" sur flaky) + flaky = 0 jusqu'à preuve de stabilité (3 runs consécutifs). Documentation des skips dans test-closure-report.md. |
| **F3 Env drift** | "Ça marche sur ma machine" → env pas iso-prod | EG-6.6 envs iso-prod (docker ou cloud) + test data définie et versionnée (EG-6.7). Critère d'abandon 6 (test data non représentative) = escalade. |
| **F4 Mutation score gaming** | Muter des lignes triviales (getters, setters) pour gonfler le score | UDL 4 ("coverage achieved") expose la couverture réelle par module. T1 casseur tests détecte les mutations triviales. Mutation score seuil ≥70% (XG-6.3) + score par catégorie (lignes critiques vs triviales). |

### 7.3 Pattern de contournement probable (4 contournements)
| Contournement | Description | Mitigation spec v2 |
|---------------|-------------|---------------------|
| **C1 Skip tests sans justification** | Skip = 0 dans la TTM, mais tests skippés en pratique | Refus catégorique 5 (chaque skip documenté dans test-closure-report.md avec rationale). TTM 100% force à tracer chaque test skippé. |
| **C2 Coverage inflation** | Tester des getters/setters pour gonfler la couverture | Mutation testing détecte les lignes non-couvertes utiles. UDL 4 expose la granularité par module (pas juste un %). |
| **C3 Mutation gaming** | Muter des lignes triviales (getters) pour augmenter le score | T1 casseur tests détecte les mutations triviales. Mutation score par catégorie (critical lines vs trivial lines). |
| **C4 Copy-paste de tests d'intégration** | Tests copiés d'un module à l'autre sans adaptation | TTM 100% (XG-6.5) — chaque test pointe vers un AC unique, pas de duplication. T2 conformité acceptance criteria P2 détecte les tests dupliqués. |

### 7.4 Valeur ajoutée perçue
P6 = **valeur NFR + go/no-go documenté** (décision mainteneur 2026-06-07). Valeur typique :
- **NFR perf validés** : latence p95, throughput, scalabilité mesurés et documentés
- **NFR security validés** : 0 critical security finding, OWASP ASVS 5.0 audité
- **Mutation score attestant la qualité des tests** : les tests testent vraiment
- **TTM complète** : 100% acceptance criteria P2 tracés par test (preuve d'exhaustivité)
- **Go/no-go documenté** : décision traçable, sign-off formel, rationale explicite
- **Confiance pour P7 Deployment** : "le mainteneur a confiance pour déployer" (vs anxiété pré-P6)
- **Réduction des incidents prod** : 0 régression critique en prod sur 90 jours (cible greenfield)

**Métrique roi** : taux d'incidents prod post-déploiement attribuables à un défaut non détecté en P6 (cible = 0 sur 90 jours).

### 7.5 Dette d'orchestration (3 risques, décision mainteneur 2026-06-07)
| Risque | Description | Mitigation spec v2 |
|--------|-------------|---------------------|
| **R1 Sync failure des 4 niveaux + 2 transverses** | 4 niveaux + 2 transverses en parallèle peuvent dériver (résultats incohérents, défauts pas synchronisés) | Checkpoint par niveau (XG-6.1) + defect-report.md versionné + TTM temps réel. Hyperagent-Orchestrator impose un ordre de réduction. |
| **R2 Context drift dans le TTM** | TTM se désynchronise des acceptance criteria P2 modifiés en cours de P6 (rare mais possible) | TTM = single source of truth, regénérée à chaque exécution. T2 conformité acceptance criteria P2 (matrice AC → test, XG-6.10) détecte les dérives. Snapshot TTM dans `.swebok_state.db`. |
| **R3 Overhead des 11+1 livrables** | Formalisme (12 livrables) qui ralentit sans valeur (overhead documentation) | Vue exécutive 1 page (closure report + go/no-go memo) pour le mainteneur. Détails dans les rapports annexes. Templates imposés pour éviter la sur-ingénierie documentaire. |

**Validation terrain** (nice-to-have) : 1 mini-projet test ou 1 avis expert externe pour valider les hypothèses de projection. Maintenu dans roadmap stratégie (P2-9), ne bloque plus le verdict.

### 7.6 Verdict
- [x] 🟢 OK (100%, projection + 3 questions de validation)

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. Token budget validé : **5k/8k/15k** (cohérent P3/P4/P5, justifié par Nexus-Critic T1+T2+T3 obligatoire).

### 8.1 Token budget alloué
**Validé 2026-06-07** : **5k base / 8k soft cap / 15k hard cap** (cohérence P3/P4/P5 v2 finale).
- Justification : Nexus-Critic T1+T2+T3 obligatoire = 3 invocations × ~1.5k = 4.5k additionnel, ce qui sature le budget 10k en nominal. 15k = marge de sécurité.

### 8.2 Compaction checkpoint
- [x] A. Tous les 5 tool calls (toutes les 5 actions, F8 recherche 2026)
- [x] B. À 60-70% du soft cap (5.6k tokens, aligné P3/P4/P5)
- [x] C. **Compaction agressive des résultats de test** (résumer les passes, garder les échecs en détail, AP7 recherche 2026)
- [x] D. Drop les tool results volumineux (garder la décision, pas la donnée brute)

### 8.3 Consultation cross-phase
- [x] A. Phase 5 code en slice (le module testé)
- [x] B. Phase 2 acceptance criteria (slice)
- [x] C. TTM comme source de cohérence (ne pas re-lire tout, structure incrémentale)
- [x] D. Ne pas charger tous les résultats de test (résumé + pointeurs)
- [x] E. **Pre-hydrate obligatoire** : au début de P6, charger dans `.swebok_state.db` la liste des modules + AC P2 + NFR P2 + TTM initiale + envs + harnesses (F7 recherche 2026)

### 8.4 Pattern adversarial concret
- [x] A. T1 : Test Designer vs Test Adversary (Nexus-Critic casse les tests)
- [x] B. T2 : Acceptance Compliance (chaque AC P2 a son test ?)
- [x] C. T3 : Production Predictor (quels défauts vont émerger en P7/prod ?)
- [x] D. **Mutation testing** comme T1 automatisé (mesure qualité des tests)
- [x] E. **Context isolation** : Nexus-Critic n'a pas accès aux délibérations du designer
- [x] F. **3 invocations systématiques** : Nexus-Critic = T1 casseur + T2 conformité AC P2 + T3 prédiction P7 (comme P3/P4/P5)

### 8.5 User Decision Ledger — 7 éléments P6-spécifiques

> **Validation 2026-06-07** : UDL 7 éléments P6-spécifiques (aligné P3, P4, P5).

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

### 8.6 Verdict
- [x] 🟢 OK

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md`.

#### Findings les plus pertinents pour cette phase
- **F2** : Multi-agent = 15× tokens → **3-5 subagents test par niveau** (4 niveaux + 2 transverses + mutation = 7 tâches, mais 3-5 subagents en parallèle MAX, F13 recherche 2026). Hard cap 15k justifié.
- **F3** : Subagent brief = OBJECT/FORMAT/TOOLS/BOUND → auditer les briefs de chaque subagent test (Nexus-QA, Nexus-Performance, Nexus-Security, Nexus-Critic)
- **F12** : BM25 > embedding sur code → pour trouver les tests existants à exécuter, `grep` > embedding search
- **F9** : Forward worker→user (~50% économie) → si un subagent test (ex: perf) produit un go/no-go clair, forward direct à l'utilisateur sans re-synthèse
- **F6** : Mur à 35 min → segmentation par niveau de test (intégration, système, acceptance, régression, perf, security, mutation), pas une seule phase longue
- **F13** : Single-agent ≥ multi-agent à budget tokens égal → P6 = multi-agent justifié car (a) 7 tâches parallèles disjointes (4 niveaux + 2 transverses + mutation), (b) outils disjoints (perf vs security vs mutation), (c) read-heavy parallèle (AC P2 + DDS P4 + coverage P5)

#### Anti-patterns à éviter dans cette phase
- **AP1** : 50 subagents test pour 10 tests à écrire — calibrer au besoin réel (3-5 par niveau)
- **AP3** : Transcripts complets à chaque wakeup test — digest des échecs uniquement (AP7)
- **AP7** : Contexte "flood" avec tous les résultats de test — résumer les passes, garder les échecs en détail
- **AP5** : Compaction à 95% — trigger à 60-70% (= 5.6k tokens pour P6)

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : un faux positif qui contamine la suite de tests ? → Mitiigé par mutation testing (XG-6.3) + T1 casseur + UDL 7
- [x] **Distraction** : trop de tests "nice to have" qui éloignent des acceptance criteria ? → Mitiigé par TTM 100% + UDL 3 (NFR P2 validé)
- [x] **Confusion** : tests ambigus (quoi tester exactement) ? → Mitiigé par TTM 100% + UDL 1 (test case executed unique)
- [x] **Clash** : tests contradictoires (mock vs intégration) ? → Mitiigé par envs iso-prod (EG-6.6) + test data versionnée (EG-6.7)

#### Recommandation budget (mise à jour 2026)
- **Hard 15k** (3-5 subagents test par niveau, 7 tâches parallèles max, compaction agressive des passes = 60-70% trigger)
- **Justification Nexus-Critic T1+T2+T3** : 3 invocations × ~1.5k = 4.5k additionnel, sature le budget 10k → 15k justifié (cohérence P3/P4/P5)

---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-07 lors de l'audit P6 v2 pour intégrer la bascule coverage/mutation de P5 vers P6, la démarcation P5↔P6 explicite, le Nexus-Critic T1+T2+T3 obligatoire, et la section 7 comblée par projection.

### Couverture effective

| Source | Ressources disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 2 livres |
| New Books achetés (§19) | 0 |
| Standards NIST/OWASP (§13) | 1 |
| Open-access téléchargés | 1 |
| **TOTAL corpus-aligned local** | **4** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~15 livres
- **Disponible localement** : 4 corpus-aligned
- **Couverture effective** : **13%** █░░░░░░░░░

### Lacunes (§20)

- **Testing KA SWEBOK** (Beizer, Kaner, Bach, etc.) — non acquis
- **0 livres manquants critiques bloquants** pour le cadrage (action P1-N roadmap)

### Verdict révisé

- Les ressources sont **insuffisantes** pour la phase (13%), mais **suffisantes pour le cadrage**
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel

---

## Verdict global de la phase
- [x] 🟢 OK (atteint dès la première conversation, pattern reproductible P3/P4/P5)

## Liste d'actions
1. **Mettre à jour P5 v2 finale** : (a) coverage reste en P5 comme lint gate build (XG-5.3 inchangé) mais validation finale migrée en P6 (XG-6.2), (b) mutation testing retiré de P5 UDL 6 et basculé en P6.
2. **Mettre à jour `pre-tool-use/token-counter.sh`** ligne 64 : P6 hard 15000 (vs 10000 v2-renum).
3. **Mettre à jour la stratégie** `audit/00-context-engineering-strategy.md` §5 (budget P6) + §9.3 (T3 par défaut sur P6 = TRANCHÉE : T1+T2+T3 OBLIGATOIRE).
4. **Créer mémoire P6 spec v2** : `swebok-v4-p6-spec-v2-vert-2026-06-07.md` dans le dossier memory.
5. **P7 Deployment** : prochaine phase à auditer (cf. user prompt exhaustif fourni).

## Notes libres
> P6 = 2e phase la plus coûteuse en effort (20-40% projet) après P5 Implementation. La bascule coverage/mutation de P5 vers P6 est un changement structurel qui allège P5 (focus unit seul) et muscle P6 (focus qualité + NFR).
> La cohérence Nexus-Critic T1+T2+T3 obligatoire est maintenue sur les 4 phases multi-agent (P3, P4, P5, P6), justifiant le hard cap 15k partout.
> L'audit Drew Breunig 4 modes est complet (7 mécanismes par mode), pattern reproductible validé.
