# Phase 9: Maintenance Workflow Spec

> **Statut** : v2 — validé 2026-06-07 par le mainteneur (audit P9 clos via grille offline + 4 questions vague 1, verdict 🟢 dès la première conversation).
> **Changement vs v2-renum** : (1) **critère explicite de démarcation P8↔P9 ET P9↔P10** inscrit (P8 = monitoring + incidents sans code ; P9 = CHANGEMENT de code planifié ; P10 = retirement = archive/arrêt), (2) **Nexus-Critic T1 casseur patch + T2 conformité design original + T3 prédiction aval P10 OBLIGATOIRE** (3 invocations systématiques, cohérence P3-P7), (3) **hard cap 8k → adaptatif 3-niveaux** (hotfix/typo 1k/2k/3k --lite, corrective standard 3k/5k/8k single, structurant/perfective 5k/8k/15k multi justifié, symétrie P8), (4) **6+5 livrables** (6 standard + 5 ajouts : diff/patch concret + tag release + decision rationale + post-mortem si incident + ADR si structurante), (5) XG-9.1-XG-9.9 (9 exit criteria), (6) **section 5.5 transformée en 4 décisions précises** (type maintenance + criticité + CAB approval + EOL→P10), (7) **section 7 comblée par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7/P8 v2** (effort 10-30% projet, 4 frictions + 4 contournements, 3 risques dette), (8) **UDL 7 éléments P9-spécifiques** documentés, (9) **audit des 4 failure modes Drew Breunig** complet, (10) **Couverture cas universelle adaptative** 6 cas, (11) **Hooks 15** alignés P8, (12) **Refus catégoriques 10** (vs 6 v2-renum), (13) **Critères d'échec 4 + d'abandon 7**, (14) **Pre-hydrate obligatoire** (F7 recherche 2026), (15) **Compaction 60-70% du soft cap** par criticité, (16) **Conditions de sortie (checklist 11 critères)**.
> **Changement vs structure antérieure** : v2-renum créée 2026-06-05 (renommage cascade P8→P9 après split P3). Refonte ciblée pour aligner sur P3/P4/P5/P6/P7/P8 v2 + intégrer les démarcations P8↔P9 et P9↔P10 + mode adaptatif 3-niveaux (symétrie P8) + Nexus-Critic T1+T2+T3 obligatoire (cohérence P3-P7).
> **But** : consommer les change requests émises par P8 (post-mortems, capacity, incidents systémiques) pour modifier le code planifié d'un système en production — corrective (bugfix), adaptive (env/dépendances), perfective (feature mineure/refactoring), preventive (dette) — avec impact analysis + regression testing + CAB approval pour les changements structurants, sans archiver le système (escalade P10) ni modifier le monitoring (escalade P8).

---

## Metadata

- **Phase**: 9
- **Name**: Maintenance
- **Purpose**: Sustain and enhance software through planned, traceable code changes (corrective, adaptive, perfective, preventive) without retiring the system (escalade P10)
- **Parallel Mode**: Adaptatif par criticité (3 niveaux, symétrie P8) : hotfix/typo single --lite sans Critic, corrective/standard single + Nexus-Critic T1+T2+T3, structurant/perfective multi + Nexus-Critic T1+T2+T3 + Council structurante
- **Équivalent SWEBOK v4** : P6 (Software Maintenance KA) — corrective, adaptive, perfective, preventive maintenance
- **Référentiels** : IEEE 1219 (Standard for Maintenance), ISO/IEC 14764 (Software Maintenance), ITIL v4 (Change Management + Release Management), Refactoring at Scale (Lemaire 2020), Working Effectively with Legacy Code (Feathers 2004, lacune critique), Refactoring Databases (Sadalage 2006, lacune critique), Beyond Legacy Code (Bernstein 2015)

---

## Mission (1 phrase)

> « Consommer les change requests émises par P8 (post-mortems, capacity, incidents systémiques) pour modifier le code planifié d'un système en production — corrective, adaptive, perfective, preventive — avec impact analysis, regression testing, CAB approval pour les changements structurants et traçabilité complète de chaque changement, sans archiver le système (escalade P10) ni modifier le monitoring en place (escalade P8). »

---

## Critère de démarcation P8 (Operations) ↔ P9 (Maintenance) ↔ P10 (Retirement)

> **Validation 2026-06-07** : le mainteneur a tranché pour des critères explicites, inscrits dans P9 (et déjà inscrits dans P8 v2 finale). **P8 = monitoring + incidents sans modification code ; P9 = CHANGEMENT de code planifié (système continue à vivre) ; P10 = retirement (système archivé, s'arrête)**. Trois questions simples : P8 "la prod tourne-t-elle (sans modif code) ?", P9 "modifier le code pour faire vivre le système ?", P10 "arrêter, archiver, retirer le système ?".

### Démarcation P8 ↔ P9 (reprise de P8 v2 finale)

**Règle simple P8 vs P9** : si la décision **ne modifie PAS le code** (calibrer un seuil, écrire un post-mortem, escalader un incident, forecaster la capacité) = P8. Si la décision **modifie le code de production** (bugfix, security patch, refactoring, feature mineure planifiée) = P9 (avec impact analysis + regression testing obligatoires).

### Démarcation P9 ↔ P10 (TRANCHÉE vague 1 audit 2026-06-07)

> **Critère retenu : question centrale (recommandé)** — P9 prolonge la vie du système, P10 prépare la mort.

| Dimension | P9 Maintenance (cette spec) | P10 Retirement (à auditer) |
|-----------|------------------------------|------------------------------|
| **Question centrale** | **Modifier le code d'un système qui tourne ?** (le système continue à vivre) | **Arrêter, archiver, retirer un système ?** (le système s'arrête) |
| **Activité dominante** | Modifier le code planifié + tester + redéployer | Archiver le code + données + config + docs + transfert ownership |
| **Décisions** | Type de maintenance (corrective/adaptive/perfective/preventive), impact analysis, CAB approval, scope du patch | EOL decision, archivage données, conformité de fermeture, transfert stakeholders, plan de remplacement |
| **Outputs typiques** | `maintenance-request.md`, `impact-analysis.md`, `change-implementation-report.md`, `regression-test-report.md`, `maintenance-log.md` | `eol-decision-memo.md`, `archive-procedure.md`, `data-migration-plan.md`, `compliance-closure-report.md`, `ownership-transfer.md` |
| **Adversarial** | T1 casseur patch + T2 conformité design + T3 prédiction aval P10 (toujours obligatoire) | T1 casseur plan retirement + T2 conformité réglementaire + T3 prédiction aval post-EOL |
| **Agents typiques** | Adaptatif par criticité (cf. Responsible Agents) | Nexus-DevOps-Lead (lead archivage), Nexus-Docs, Nexus-SM (comm stakeholders), Nexus-CISO (conformité) |
| **Trigger transition** | EOL approche (système en fin de vie sans plan de remplacement) → escalade P10 | Maintenance complétée + system back to steady-state → retour P8 |

**Règle simple P9 vs P10** : si la décision **prolonge la vie du système** (modifier le code, ajouter une feature, corriger un bug) = P9. Si la décision **prépare la mort du système** (archiver, transférer ownership, notifier stakeholders EOL) = P10.

### Cas limites types (tranchés)

- **"Maintenance d'un système en fin de vie AVEC plan de remplacement actif"** = **P9** (prolonge). Le code est toujours modifié, le système continue à tourner, le plan de remplacement informe le scope des patches.
- **"Maintenance d'un système en fin de vie SANS plan de remplacement"** = **P10** (prépare la mort). L'attention se porte sur l'archivage, le transfert, la conformité, pas sur de nouvelles features.
- **"Refactoring lourd pré-migration vers nouvelle version du même système"** = **P9** (cible = même système, code modifié). Si cible = nouveau système, alors = **P10** (préparation EOL de l'ancien).
- **"Calibrer un seuil d'alerte"** = **P8** (config monitoring, pas de code). "Configurer alerts initiales" = **P7** (setup, fait dans `monitoring-dashboard.md` P7).
- **"Modifier le code pour réduire les alertes"** (par exemple corriger une N+1 query qui sature le DB) = **P9** (fix corrective, avec impact analysis + regression).
- **"Écrire un post-mortem après incident P0"** = **P8** (analyse post-incident, livrable P8). Mais "Implémenter l'action correctrice du post-mortem (fix du code)" = **P9** (change implementation).
- **"Décider de scaler horizontalement (passer de 4 à 8 instances)"** = **P8** (capacity planning, config infra, pas de code applicatif). Mais "Refactorer le code pour réduire la consommation mémoire" = **P9** (fix perfective).
- **"Hotfix urgent pendant incident"** = **escalade P7** (re-deploy d'urgence) si la cause est une régression P7, sinon **escalade P9** (change urgent avec fast-track CAB). P8 ne fait JAMAIS de modification code en autonomie.
- **"Communiquer aux stakeholders pendant un incident"** = **P8** (UDL 3). Mais "Définir le plan de communication initial" = **P2** (requirement).

**Conséquence opérationnelle sur P8 v2 finale** : aucune modification. P8 émet la CR formelle quand un incident nécessite un changement code (UDL 7 P8 = "deferred / escalated to P9").

**Conséquence opérationnelle sur P10 (à auditer)** : la spec P10 traitera l'archivage, la conformité de fermeture, le transfert d'ownership. P9 lui transmet les CR émises quand le mainteneur détecte un EOL approche sans plan de remplacement.

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-9.1 | Phase 8 operations stable | Operations stability report (XG-8.7) | 30-day stable operation OU CR formelle émise par P8 (UDL 7) |
| EG-9.2 | Maintenance request received | Ticket/change request | CR formelle loggée (depuis P8 post-mortem, P8 capacity, P8 incident systémique, OU user direct) |
| EG-9.3 | Impact analysis completed | Impact assessment (Activity 9.1) | Analysis approved par mainteneur (scope, modules touchés, risque régression) |
| EG-9.4 | Maintenance window approved | Window confirmation | Scheduled et confirmed avec ops (P8) + stakeholders |
| EG-9.5 | Resources allocated | Resource assignment | Agent(s) assignés (Backend/Frontend/DevOps/Security selon zone) |
| EG-9.6 | CAB approval (si structurant) | Change Advisory Board | CAB approval documenté (si criticité = structurant, Q3 user 5.5) |
| EG-9.7 | Type de maintenance identifié | Type decision (Q1 user 5.5) | Corrective / Adaptive / Perfective / Preventive tranché + rationale |
| EG-9.8 | Criticité du changement évaluée | Criticité decision (Q2 user 5.5) | Hotfix / Standard / Structurant tranché (détermine agents + budget) |
| EG-9.9 | Rollback plan documenté | RB procedures + test result | Reviewed, approved, ET test de rollback exécuté en staging (réutilise P7 RB procedures) |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` requires additional planning (re-EG, escalade P3 si refonte, escalade P10 si EOL détecté).

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-9.1 | Maintenance changes implemented | Change status | 100% changements déployés (P7 deployment pour le re-deploy) |
| XG-9.2 | Regression testing passed | Regression results | 100% regression suite PASS (héritée de P6) + nouveaux tests pour le patch |
| XG-9.3 | Documentation updated | Doc currency | Toutes les docs affectées mises à jour (technique, ops, user si feature) |
| XG-9.4 | Maintenance log updated | Log completeness | Entrée ajoutée sous 24h dans `maintenance-log.md` |
| XG-9.5 | System restored to operational status | System status | Back to steady-state (smoke tests P7 re-passés, monitoring P8 stable) |
| XG-9.6 | Post-maintenance review approved | PMR sign-off | Review documenté (leads + ops + mainteneur) |
| XG-9.7 | Aucun nouveau défaut introduit | Defect report | 0 nouveau défaut critique/majeur post-patch (vérifié 48h après deploy) |
| XG-9.8 | Audit trail P9 complet | Audit log | Trace de tous les changements (commit hash, tag, PR URL, impact, regression) |
| XG-9.9 | UDL 7 éléments P9-spécifiques loggés | UDL set | 100% loggés dans `.swebok_state.db` (table `udl_p9`) |

**Gate Evaluation**: ALL criteria must be `PASS` to return to P8 Operations. Any `FAIL` triggers remediation cycle (rollback, hotfix, re-EG, escalade P3 si refonte détectée, escalade P10 si EOL).

---

## Transition Criteria to Phase 8 (Operations)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Maintenance completed | Maintenance Lead | Operations Lead | Completion memo (XG-9.1 + XG-9.6) |
| System operational | Maintenance Lead | Operations Lead (Nexus-SM) | Health check passé (XG-9.5) |
| Monitoring updated | Maintenance | Operations (Nexus-SM) | Alertes recalibrées si nécessaire (escalade P8 si config, jamais P9) |
| Support handover done | Maintenance | Operations | Handover documenté (runbook mis à jour, formation ops) |
| Audit trail P9 transmitted | Maintenance | Compliance | HMAC chain vérifié, transmis à compliance lead |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_9_COMPLETE` only when all exit criteria verified with formal evidence (commit hash + tag + PR URL + regression report signés). **P8 reste active en parallèle** (monitoring continue pendant la maintenance P9, handoff dans les 2 sens).

---

## Transition Criteria to Phase 10 (Retirement)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| EOL decision made | Project Sponsor | Maintenance Lead + Retirement Lead | EOL decision memo signé |
| Replacement ready OR not | Product Owner | Project Lead | Plan de remplacement actif (P9 continue) ou absent (P10 déclenché) |
| Stakeholder approval | Project Sponsor | All stakeholders | Approbation documentée |
| EOL approach detected by P9 | Maintenance Lead | Retirement Lead | Trigger Q4 user 5.5 = "EOL approche → escalade P10" |
| Maintenance debt documenté | Maintenance Lead | Retirement Lead | Liste des patches en deferred et dette acceptée (UDL 6 P9) |

**Trigger spécifique transition P10** : (a) décision EOL explicite (sponsor + stakeholders) OU (b) P9 détecte qu'un système approche EOL sans plan de remplacement (via post-mortems récurrents, dette technique insurmontable, dépréciation dépendance critique) → escalade P10 systématique.

---

## Key Activities

### Activity 9.1: Maintenance Request Processing
- Recevoir et logger les maintenance requests (CR formelles émises par P8 OU user direct OU discovery ops)
- **Catégoriser le type de maintenance** : corrective (bugfix), adaptive (env/dépendances/migrations), perfective (feature mineure/refactoring/optimisation), preventive (refactoring proactif/dette technique) — **Décision Q1 user 5.5**
- **Évaluer la criticité** : hotfix/typo (1k/2k/3k --lite), standard (3k/5k/8k single), structurant/perfective (5k/8k/15k multi) — **Décision Q2 user 5.5**
- Effectuer l'**impact analysis** (scope, modules touchés, risque régression, dette technique ajoutée)
- **CAB approval** si criticité = structurant — **Décision Q3 user 5.5**
- Prioriser et scheduler la maintenance (window, ressources)
- **Vérifier EOL approche** — **Décision Q4 user 5.5** (escalade P10 si oui)
- Rollback plan documenté (réutilise procédures P7, re-test en staging si nécessaire)

### Activity 9.2: Change Implementation
- Implémenter les changements de code (selon type : fix, migration, feature, refactoring)
- Mettre à jour la configuration (si adaptive : env vars, secrets, dépendances)
- Appliquer les patches et updates
- Gérer les changements de configuration (feature flags si besoin, matrices de compatibilité)
- Gérer les migrations de schéma DB (forward + rollback, symétrique à P7)
- Documenter le commit hash + tag + PR URL (livrable essentiel pour audit trail)
- ADR créé si décision structurante (impact architectural)

### Activity 9.3: Change Testing and Verification
- **Exécuter la regression suite** (héritée de P6 P5 P5 — fast feedback)
- Vérifier le fix ou l'enhancement (test unitaire + intégration)
- Valider la stabilité système (smoke tests re-passés, latence inchangée)
- Confirmer **0 nouveau défaut** introduit (vérification 48h post-deploy, XG-9.7)
- Tests mutation si refactoring (hérités de P6, XG-6.3)

### Activity 9.4: Maintenance Documentation
- Mettre à jour la documentation technique (code comments, README, ADR si nouveau)
- Logger l'activité dans `maintenance-log.md` (sous 24h, XG-9.4)
- Mettre à jour la knowledge base (lessons learned, patterns de fix récurrents)
- Archiver les change records (commit, tag, PR, impact, regression, post-mortem si incident)
- Mettre à jour le runbook P8 si procédure changée (escalade P8 pour runbook officiel, ou merge request soumis)
- **Changelog public** si user-facing (semver, breaking changes documentés)
- **Post-mortem si incident causé par le patch** (le patch est le "changement", incident = conséquence)

### Activity 9.5: Adversarial Validation (Nexus-Critic — OBLIGATOIRE, cohérence P3-P7)

- **T1 casseur patch** : Nexus-Critic relit le patch, cherche des failles (introduit-il un bug, scope creep, dette cachée, code path dangereux). Cible : `change-implementation-report.md` + diff commit + `impact-analysis.md`.
- **T2 conformité design original** : Nexus-Critic vérifie que le patch respecte le design DDS P4 + les ADRs P3 + les NFR P2 (pas de régression architecturale, pas de NFR dégradé, pas d'ADR contourné). Cible : diff commit vs DDS P4 + ADRs P3 + NFR P2.
- **T3 prédiction aval P10** : Nexus-Critic prédit si le patch (a) peut récidiver dans 7-30 jours (régression potentielle), (b) approche d'un EOL (dette systémique, dépendance dépréciée, dette acceptée chronique), (c) escalade vers P10 (système en fin de vie sans plan de remplacement). Cible : `regression-test-report.md` + `maintenance-log.md` (historique) → `change-request-*.md` (si escalade P10).

**Isolation des contextes (ACI stratégie §4.5)** : Nexus-Critic ne voit pas le prompt système du producteur. Chaque rôle adversarial a un contexte distinct.

**Council structurante** (si criticité = structurant, Q3 user 5.5 = OUI) : CISO + DevOps-Lead + Architect examinent le patch, valident l'impact, signent l'approbation finale. Cohérent avec P7 Council post-deployment et P8 Council post-incident.

---

## Responsible Agents

> **Mécanique adaptative par criticité** (décision mainteneur 2026-06-07, vague 1) : P9 a 3 modes de criticité, symétrie P8 (monitoring courant / standard / critique). Nexus-Critic T1+T2+T3 obligatoire dans tous les modes non --lite (cohérence P3-P7).

### Mode "Hotfix / typo / micro-tâche"

| Agent | Role |
|-------|------|
| **Nexus-Backend OU Frontend OU DevOps** (seul, selon zone) | Patch + commit + test + doc |

**Concurrency** : **single-agent** (F13 recherche 2026 — micro-tâche = lecture + écriture locale, pas de création).
**Nexus-Critic** : **aucun** (micro-tâche = exécution, pas création, gaspillage tokens). Hot path --lite obligatoire.
**Budget** : **1k/2k/3k** (--lite).
**Déclencheur** : Q2 user 5.5 = "Hotfix/typo" (typo, config tweak, comment update, dépendance patch triviale, doc update).

### Mode "Corrective / Adaptive / Preventive standard"

| Agent | Role |
|-------|------|
| **Nexus-Backend OU Frontend OU DevOps** (lead, selon zone du patch) | Patch principal, impact analysis, regression |
| Nexus-Security (support) | Security patches, CVE, dependency upgrades |
| Nexus-QA (support) | Regression suite, mutation testing si refactoring |
| **Nexus-Critic (T1+T2+T3 obligatoires)** | T1 casseur patch + T2 conformité design + T3 prédiction aval P10 |

**Concurrency** : **single-agent + support ponctuel** (F13 recherche 2026 — read-heavy parallèle sur impact + regression, disjoint tools).
**Nexus-Critic** : **T1+T2+T3 obligatoires** (3 invocations systématiques, cohérence P3-P7).
**Budget** : **3k/5k/8k**.
**Déclencheur** : Q2 user 5.5 = "Standard" (bugfix typique, dependency upgrade, security patch, refactoring localisé, preventive dette ciblée).

### Mode "Structurant / Perfective lourde / Refactoring majeur"

| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordonne la réponse multi-agent |
| **Nexus-Backend OU Frontend OU DevOps OU Nexus-Architect** (lead, selon zone) | Patch principal, design update, migration |
| Nexus-Security (si security patch) | Security review, threat model update |
| Nexus-QA (test lead) | Regression complète, mutation testing, NFR re-validation |
| Nexus-PM (priorisation) | Coordination CAB, stakeholders, window |
| **Nexus-Critic (T1+T2+T3 obligatoires)** | T1 casseur patch + T2 conformité design/ADRs/NFR + T3 prédiction aval P10 |
| **Council structurante (CISO + DevOps-Lead + Architect)** | Examen pré-deploy, validation impact, sign-off |

**Concurrency** : **multi-agent justifié** (F13 recherche 2026 — refactoring majeur = read-heavy parallèle sur impact + design + test + stakeholders, disjoint tools).
**Nexus-Critic** : **T1+T2+T3 obligatoires** (3 invocations systématiques, cohérence P3-P7).
**Council structurante** : **OBLIGATOIRE** si Q3 user 5.5 = OUI (CAB approval requise), examen 1h avant deploy.
**Budget** : **5k/8k/15k** (cohérence P3-P7).
**Déclencheur** : Q2 user 5.5 = "Structurant/perfective" (feature mineure multi-module, refactoring > 1 sem, migration schéma majeure, dependency upgrade structurante, debt reduction structurante).

### Patterns adversariaux T1/T2/T3 (rappel)

- **T1 (casseur patch)** : le lead produit le patch, Nexus-Critic le casse (cherche les failles). Cible : `change-implementation-report.md` + diff commit + `impact-analysis.md`.
- **T2 (spec-compliance)** : Nexus-Critic vérifie conformité design DDS P4 + ADRs P3 + NFR P2 (matrice DDS → patch, symétrique à matrice DDS → code P5 XG-5.7). Cible : diff commit vs DDS P4 + ADRs P3 + NFR P2.
- **T3 (conséquentialiste aval P10)** : Nexus-Critic prédit la récurrence (régression 7-30j), l'approche EOL (dette systémique, dépendance dépréciée), l'escalade P10 (système en fin de vie sans plan de remplacement). Cible : `regression-test-report.md` + `maintenance-log.md` → `change-request-*.md` (si escalade P10).

---

## Required Skills

- `nexus-backend`, `nexus-frontend`, `nexus-devops`: Patch implémentation selon zone (Backend OU Frontend OU DevOps OU Architect)
- `nexus-architect`: Refactoring structurant, design update
- `nexus-security`: Security patches, CVE management, dependency upgrades sécurité
- `nexus-qa`: Regression testing, mutation testing, defect verification
- `nexus-pm`: Maintenance priorisation, CAB coordination, stakeholder comm
- `nexus-sm`: Handoff P8, stakeholder communication si impact business
- `nexus-critic`: Adversarial validation (T1 casseur patch + T2 conformité design + T3 aval P10) — **OBLIGATOIRE** (3 invocations) pour modes standard et structurant, absent en --lite
- `nexus-ciso`, `nexus-devops-lead`, `nexus-architect`: Council structurante (si Q3 user 5.5 = OUI)

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-maintenance-complete` | Exit criteria met (XG-9.1-XG-9.9) | Returns to Phase 8 (Operations) |
| `maintenance-request-received` | CR logged (EG-9.2) | Triggers maintenance processing |
| `impact-analysis-approved` | Impact analysis signed (EG-9.3) | Enables change implementation |
| `cab-approval-required` | Criticité = structurant (Q3 user 5.5 = OUI) | Triggers Council structurante |
| `cab-approval-obtained` | Council signed | Enables change implementation |
| `maintenance-window-confirmed` | Window scheduled (EG-9.4) | Enables execution |
| `change-implemented` | Patch committed + tested | Updates change status |
| `regression-tests-passed` | 100% regression PASS (XG-9.2) | Confirme patch viable |
| `rollback-tested` | Rollback test passed en staging (EG-9.9) | Confirme capacité de rollback |
| `maintenance-log-updated` | Log entry added sous 24h (XG-9.4) | Confirme traçabilité |
| `eol-approach-detected` | Q4 user 5.5 = OUI | Triggers Phase 10 (Retirement) escalation |
| `post-mortem-due` | Incident causé par patch | Reminder post-mortem sous 5j (cohérent P8) |
| `t1-patch-casseur-passed` | T1 Nexus-Critic passé | Confirme robustesse du patch |
| `t2-design-conformity-verified` | T2 conformité DDS/ADRs/NFR vérifiée | Confirme respect design |
| `udl-p9-logged` | 7 éléments UDL loggés | Snapshot pour phases suivantes |

---

## Artifacts Produced

| Artifact | Description | Location | Format |
|----------|-------------|----------|--------|
| `maintenance-request.md` | CR details (type, scope, impact, priorité) | `specs/workflows/by-phase/phase-9-maintenance/` | md |
| `impact-analysis.md` | Change impact assessment (scope, modules, risque régression, dette) | `specs/workflows/by-phase/phase-9-maintenance/` | md |
| `change-implementation-report.md` | Implementation details (diff, fichiers touchés, tests ajoutés) | `specs/workflows/by-phase/phase-9-maintenance/` | md |
| `regression-test-report.md` | Test results (regression suite, nouveaux tests, mutation) | `specs/workflows/by-phase/phase-9-maintenance/` | md + JSON (résultats machine-parse) |
| `maintenance-log.md` | Complete maintenance history (cumulatif) | `specs/workflows/by-phase/phase-9-maintenance/` | md |
| `updated-documentation.md` | Revised documentation (technique, ops, user si feature) | `specs/workflows/by-phase/phase-9-maintenance/` | md |
| **Diff / patch concret** (livrable ajouté) | Commit hash + tag + PR URL | git | git (commit + tag + PR) |
| **Decision rationale** (livrable ajouté) | Pourquoi cette approche (vs alternatives écartées) | `specs/workflows/by-phase/phase-9-maintenance/` | md |
| **ADR si structurante** (livrable ajouté) | Décision structurante documentée (impact archi) | `specs/workflows/by-phase/phase-9-maintenance/adr/` | md (MADR template) |
| **Changelog public** (livrable ajouté) | Changelog versionné (semver, breaking changes) | `specs/workflows/by-phase/phase-9-maintenance/` | md (Keep a Changelog) |
| **Post-mortem si incident** (livrable ajouté) | Post-mortem si patch cause incident (cohérent P8) | `specs/workflows/by-phase/phase-9-maintenance/post-mortems/` | md (template standard) |

**Format de stockage** :
- Specs narratives : md (lecture humaine)
- Diff/patch : git versionné (commit + tag + PR)
- Test results : JSON (machine-parse) + md (synthèse)
- ADR : md (MADR template)
- Changelog : md (Keep a Changelog standard)
- Audit trail : JSON (machine-parse) + md (synthèse)

**Convention de nommage** :
- Specs narratives : `${livrable}.md`
- Patch : `git tag v{major}.{minor}.{patch}` (semver)
- PR : `PR-{YYYY-MM-DD}-{short-desc}`
- Post-mortem : `post-mortem-{YYYY-MM-DD}-{incident-id}.md`
- ADR : `adr-{YYYY-MM-DD}-{short-title}.md`

**Localisation** : tous dans `specs/workflows/by-phase/phase-9-maintenance/`.

---

## Format des fichiers (triple différencié, aligné P3-P8 v2)

| Type de livrable | Format primaire | Format secondaire | Standard |
|------------------|------------------|-------------------|----------|
| **Specs narratives** (request, impact, implementation, regression, log, doc, changelog, post-mortem, decision rationale) | md (lecture humaine) | — | Markdown CommonMark |
| **Patch / diff** | git (commit + tag + PR) | — | semver (Keep a Changelog) |
| **Test results** | JSON (machine-parse) | md (résumé) | JUnit XML, pytest JSON, Jest JSON |
| **ADR** | md (MADR template) | — | MADR 3.0 |
| **Audit trail** | JSON (HMAC chain) | md (synthèse) | Cossack Labs 2025 |

---

## Hyperagent Parallel Processing (adaptatif par criticité)

### Mode "Hotfix / typo / micro-tâche"

```
single_task:
  - task: micro_change
    agents: [Nexus-Backend OU Frontend OU DevOps]
    sync: false
    lite: true
```

### Mode "Corrective / Adaptive / Preventive standard"

```
parallel_tasks:
  - task: impact_analysis
    agents: [Nexus-Backend OU Frontend OU DevOps (lead)]
    sync: false

  - task: change_implementation
    agents: [Nexus-Backend OU Frontend OU DevOps]
    sync: false

  - task: regression_testing
    agents: [Nexus-QA]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après parallel):
  - task: t1_casseur_patch
    agents: [Nexus-Critic]
    target: change-implementation-report.md + diff commit
    sync: true

  - task: t2_conformite_design
    agents: [Nexus-Critic]
    target: diff commit vs DDS P4 + ADRs P3 + NFR P2
    sync: true

  - task: t3_prediction_p10
    agents: [Nexus-Critic]
    target: regression-test-report.md + maintenance-log.md (historique)
    sync: true

reduction: "Nexus-Lead synthétise dans change-implementation-report.md"
```

### Mode "Structurant / Perfective lourde / Refactoring majeur"

```
parallel_tasks:
  - task: design_review
    agents: [Nexus-Architect (lead)]
    sync: false

  - task: change_implementation
    agents: [Nexus-Backend OU Frontend OU DevOps (lead), Nexus-Architect]
    sync: false

  - task: security_review
    agents: [Nexus-Security]
    sync: false
    only_if: security_patch

  - task: regression_testing
    agents: [Nexus-QA (lead), Nexus-Performance]
    sync: false

  - task: stakeholder_coordination
    agents: [Nexus-PM]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après parallel):
  - task: t1_casseur_patch
    agents: [Nexus-Critic]
    target: change-implementation-report.md + diff commit + impact-analysis.md
    sync: true

  - task: t2_conformite_design
    agents: [Nexus-Critic]
    target: diff commit vs DDS P4 + ADRs P3 + NFR P2
    sync: true

  - task: t3_prediction_p10
    agents: [Nexus-Critic]
    target: regression-test-report.md + maintenance-log.md (historique) → change-request-*.md (si EOL)
    sync: true

council_structurante (sequential, avant deploy):
  - task: council_examen
    agents: [Nexus-CISO, Nexus-DevOps-Lead, Nexus-Architect]
    target: change-implementation-report.md, impact, sign-off
    sync: true

reduction: "Nexus-Lead synthétise + signe avec Council avant deploy P7"
```

---

## Refus catégoriques (10)

La phase P9 **refuse** de :

1. **Pas de modification du code sans impact analysis** (impact obligatoire, EG-9.3 — règle de démarcation ; P9 = code modifié avec traçabilité)
2. **Pas de refonte déguisée en maintenance** (escalade P3 — règle de démarcation ; P3/P4 = archi/design, P9 = patch)
3. **Pas de nouvelle feature structurante** (escalade P2/P3 — règle de démarcation ; P2 = requirements, P9 = sustain + enhance mineur)
4. **Pas de fix sans regression test** (regression obligatoire, XG-9.2 — pas de patch aveugle)
5. **Pas de fix rapide sans doc** (dette explicite documentée si pressé, XG-9.3 sous 24h)
6. **Pas de deploy en prod sans staging validé** (escalade P7 — P7 = release, P9 ne fait pas de re-deploy en autonomie)
7. **Pas de skip de CAB approval** pour changement structurant (Q3 user 5.5 = OUI obligatoire, EG-9.6)
8. **Pas de modification d'un système EOL** (escalade P10 — règle de démarcation Q1 user 5.5 ; P9 = système vivant, P10 = archivage)
9. **Pas de hotfix sauvage sans re-test staging** (même urgence, process complet — cohérence P7 refus 7)
10. **Pas de modification des NFR P2 sans escalade** (toute déviation NFR = escalade P2, refus catégorique)

---

## Critères d'échec (4) et d'abandon (7 + temps)

### Critères d'échec (déclenchent une action immédiate)

1. **Régression après patch** → hotfix d'urgence + rollback (P7 déploiement) + post-mortem (cohérent P8)
2. **Nouveau défaut critique introduit** → rollback immédiat (XG-9.7) + post-mortem (cohérent P8) + escalade P3 si bug archi
3. **Documentation pas mise à jour 24h après** → escalade mainteneur (XG-9.3 obligatoire)
4. **CAB approval skipped pour changement structurant** → bloquer le deploy + escalade mainteneur (refus 7)

### Critères d'abandon (l'agent abandonne et prévient le mainteneur si)

1. Scope creep détecté (le "petit fix" devient feature) → retour P3 (refonte archi détectée)
2. Nouveau défaut critique introduit 3+ fois sur le même patch → escalade mainteneur + post-mortem profond
3. Documentation pas à jour 48h après → escalade mainteneur (process broken)
4. EOL approche détectée sans plan de remplacement → escalade P10 (Q4 user 5.5 = OUI)
5. Patch conflict avec dette acceptée chronique → escalade mainteneur (accepter dette refresh ou escalade P10)
6. Stakeholder refus multiple du patch → escalade mainteneur (alignment produit à refaire)
7. Dépassement de 35 min sans avancée claire → escalade mainteneur, redécoupage (F6 recherche 2026)

---

## Tokens budget (adaptatif par criticité)

> **Validation 2026-06-07** : le mainteneur a tranché pour un **budget adaptatif 3-niveaux par criticité**, symétrie P8 (3 niveaux par sévérité). Nexus-Critic T1+T2+T3 obligatoire sauf mode --lite (cohérence P3-P7).

| Mode | Base | Soft cap (CC) | Hard cap (abort) | Justification |
|------|------|---------------|------------------|---------------|
| **Hotfix / typo / micro-tâche** | **1k** | **2k** | **3k** | Single Nexus (Backend OU Frontend OU DevOps) en --lite, hot path (typo, config tweak, comment update, doc). Pas de Nexus-Critic. |
| **Corrective / Adaptive / Preventive standard** | **3k** | **5k** | **8k** | Single Nexus (lead) + support ponctuel (Security/QA) + Nexus-Critic T1+T2+T3 (3 invocations, ~4.5k). Compaction 60-70% du soft cap (3.5k) |
| **Structurant / Perfective lourde / Refactoring majeur** | **5k** | **8k** | **15k** | Multi-agent justifié (Hyperagent + Lead + Architect + Security + QA + PM) + Nexus-Critic T1+T2+T3 (3 invocations, ~4.5k) + Council structurante (CISO + DevOps-Lead + Architect, ~1k). Cohérent P3/P4/P5/P6/P7 |

**Pre-hydrate obligatoire** (F7 recherche 2026 — 60% du 1er tour = retrieval) : au début de chaque session P9 (et à chaque changement), charger dans le hot_context (`.swebok_state.db`) la slice suivante :
- `maintenance-request.md` (CR émise par P8)
- `impact-analysis.md` (si déjà fait en amont)
- Slice du code à patcher (zone du patch uniquement, pas tout le module)
- `regression-test-report.md` P6 (réutilisé pour validation)
- DDS P4 (matrice DDS → code, pour T2 conformité)
- ADRs P3 (matrice ADR → module, pour T2 conformité)
- NFR P2 (perf + security + observability cibles)
- `maintenance-log.md` historique (5 derniers patches pour pattern matching, F12 recherche 2026)
- Pour structurant : aussi `architecture.md` P3 + design.md P4 + go-no-go P6 historique

Sans ce pre-hydrate, 60% du budget du 1er tour est consommé en retrieval, ce qui sature le soft cap en nominal.

**Note (action de suivi P9-1)** : `pre-tool-use/token-counter.sh` ligne 67 actuelle = `P9: 3000/5000/8000` (single par défaut). Pour supporter le mode adaptatif 3-niveaux, évolution nécessaire (env var `SWEBOK_P9_MODE=hotfix|standard|structurant` ou flag `--severity`). En attendant, le défaut 3k/5k/8k couvre 50% des cas (corrective standard). Action P9-1 dans la liste d'actions.

---

## Pauses

**Spécificité P9** : pas de compaction globale (P9 alterne avec P8 en mode opérationnel). Compaction **par changement** (chaque patch = unité de travail bornée).

- **Compaction checkpoint par changement** : à 60-70% du soft cap selon mode (1.4k hotfix, 3.5k standard, 5.6k structurant)
- **Compaction immédiate après regression PASS** (AP5 recherche 2026) : dès que les tests sont verts, drop les logs verbeux d'investigation, garder uniquement (impact, diff résumé, tests passés, ADR si nouveau)
- **Compaction agressive des diffs intermédiaires** (F12 recherche 2026 — BM25 > embedding sur code) : grep + git log + AST > embedding search, ne charger que la slice du code touchée
- **Tool result clearing** : vider les résultats de regression test bruts après parsing (AP6 recherche 2026)
- **Hot path mode** pour les micro-changements (typo, config) : skip full pre-tool-use phase check, token budget 1k, pas d'adversarial gate sauf demande explicite

**Pas de transcript complet en wakeup** (AP3) : à chaque reprise de session P9, charger uniquement le digest des 5 derniers patches + la CR courante. Pas de re-rejeu intégral de l'historique.

---

## Couverture corpus (état 2026-06-06)

> **Note** : P9 = phase la moins bien couverte du projet (30%) — c'est intentionnel. P9 = patch + regression, pas création archi. Les 2 lacunes critiques (Feathers + Sadalage) sont connues, planifiées pour acquisition future.

- **30% de couverture** (3 livres canoniques disponibles localement sur ~10 recommandés)
- **3 New Books** : Refactoring at Scale (Lemaire 2020), Retrospectives Antipatterns (Corry 2020), Beyond Legacy Code (Bernstein 2015)
- **1 Standard NIST/OWASP** : NIST 800-161r1 (SCRM)
- **2 lacunes critiques** : Working Effectively with Legacy Code (Feathers 2004) — 🔴 indispensable pour P9, Refactoring Databases (Sadalage 2006) — schéma evolution
- **Décision mainteneur 2026-06-06** : 30% accepté pour cadrage, batch d'acquisition ultérieur (acquérir Feathers + Sadalage en priorité). P9 = patch + regression, pas création archi, donc couverture 30% est suffisante pour le cadrage v2.

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :

1. **Greenfield from-scratch** : maintenance rare (système jeune), perfective = nouvelles features (escalade P2/P3), preventive = quality codebase setup
2. **Maintenance legacy** : maintenance lourde (dette accumulée), preventive prioritaire, perfective rare (escalade P3 si structurante), corrective fréquente
3. **Projet interne** (équipe, gouvernance légère) : maintenance standard, CAB allégé, hotfix fréquent, doc informelle
4. **Projet externe client** : maintenance structurante, CAB obligatoire, communication stakeholders, changelog public soigné
5. **Compliance-driven** (finance, santé, défense) : maintenance ultra-traçée, CAB + Council systématique, audit log immutable, ADR obligatoire pour chaque décision structurante, post-mortem signé CISO
6. **R&D / exploration** : maintenance best-effort, hotfix only, doc minimale, dette acceptée par défaut (escalade P10 lent)

---

## Points de décision utilisateur (4 décisions opérationnelles, section 5.5 grille)

> **Validation 2026-06-07** : 4 décisions opérationnelles précises (B threshold = haute valeur opérationnelle, symétrie P8). Format AskUserQuestion (header + 2-4 options mutuellement exclusives).

### Q1 — Type de maintenance + rationale

| Header | "Type maintenance" |
|--------|-------------------|
| **Question** | "Pour le changement [changement-id], quel type de maintenance ?" |
| **Options** | (a) **Corrective** : bugfix, fix incident, fix défaut (cause = bug) ; (b) **Adaptive** : migration, upgrade dépendance, adaptation env (cause = environnement qui change) ; (c) **Perfective** : feature mineure, refactoring, optimisation (cause = amélioration) ; (d) **Preventive** : refactoring proactif, dette technique, hardening (cause = prévention) |
| **Trigger** | Nouvelle CR reçue (depuis P8 post-mortem, P8 capacity, P8 incident, user direct, ou discovery ops) |
| **Impact** | Long terme (détermine scope, agents, tests). UDL 1 logge type + rationale + déclencheur. |

### Q2 — Criticité du changement (détermine agents + budget)

| Header | "Criticité" |
|--------|-------------|
| **Question** | "Pour le changement [changement-id], quelle criticité ?" |
| **Options** | (a) **Hotfix / typo / micro-tâche** : 1k/2k/3k --lite, single sans Critic, fast-track (typo, config, doc, dépendance triviale) ; (b) **Corrective / Adaptive / Preventive standard** : 3k/5k/8k single + Nexus-Critic T1+T2+T3 (bugfix typique, dependency upgrade, security patch, refactoring localisé) ; (c) **Structurant / Perfective lourde** : 5k/8k/15k multi + Nexus-Critic T1+T2+T3 + Council structurante (feature mineure multi-module, refactoring > 1 sem, migration schéma majeure) |
| **Trigger** | Type maintenance identifié (Q1), impact analysis préliminaire |
| **Impact** | Court terme (détermine budget + agents), mais engagement ressources. UDL 2 logge criticité + budget + agents. |

### Q3 — CAB approval (changement structurant)

| Header | "CAB approval" |
|--------|----------------|
| **Question** | "Pour le changement [changement-id] structurant, CAB approval requise ?" |
| **Options** | (a) **Oui, structurante** : Council structurante (CISO + DevOps-Lead + Architect) examen 1h, signature obligatoire, déploiement bloqué tant que non signé ; (b) **Oui, standard** : approbation mainteneur seul (CAB léger, sans Council), déploiement après sign-off mainteneur ; (c) **Non, hotfix urgent** : fast-track sans CAB (escalade mainteneur si urgence vitale, post-mortem obligatoire) ; (d) **Non, documentation seule** : pas de CAB, traçabilité git suffit (typo, config, doc update, micro-tâche) |
| **Trigger** | Criticité = structurant ou perfective (Q2), ou détection scope creep |
| **Impact** | Court terme (bloquant ou non pour le deploy). UDL 3 logge décision CAB + signataires + rationale. |

### Q4 — EOL approche → escalade P10 ?

| Header | "EOL approche" |
|--------|----------------|
| **Question** | "Le système [system-id] approche-t-il de l'EOL sans plan de remplacement ?" |
| **Options** | (a) **Non, système vivant** : P9 continue (patch + regression), pas d'escalade P10 ; (b) **Oui, avec plan de remplacement** : P9 continue (le plan informe le scope des patches, e.g. features gelées, security only), traçabilité dans `maintenance-log.md` ; (c) **Oui, sans plan de remplacement** : escalade P10 immédiate (CR formelle vers Retirement Lead, gel des nouveaux patches, focus sur archivage progressif) ; (d) **Zone grise, à arbitrer** : escalade mainteneur pour décision EOL (dette systémique, dépendance dépréciée, post-mortems récurrents signalent un problème systémique) |
| **Trigger** | Post-mortem récurrent (>3 P2 en 30j), dette chronique, dépendance dépréciée, dépréciation upstream, signaux P8 UDL 7 |
| **Impact** | Long terme irréversible (déclenche P10). UDL 7 logge décision EOL + rationale + impact business estimé. |

---

## UDL — 7 éléments P9-spécifiques

> **Validation 2026-06-07** : 7 éléments P9-spécifiques (aligné P3, P4, P5, P6, P7, P8).

| Élément | Description | Exemple |
|---------|-------------|---------|
| **Maintenance type chosen** | Décision Q1 user 5.5 : type retenu + rationale + déclencheur | "CR-2026-0089 = Corrective (fix N+1 query checkout, cause = 5 incidents P2 en 30j depuis post-mortem INC-2026-0142, validé mainteneur 2026-06-15)" |
| **Criticité + budget allocated** | Décision Q2 user 5.5 : criticité assignée + budget + agents | "CR-2026-0089 = Standard (impact 3 fichiers, 8h dev + 4h test, budget 3k/5k/8k, single Nexus-Backend + Nexus-QA + Nexus-Critic T1+T2+T3)" |
| **CAB approval status** | Décision Q3 user 5.5 : CAB approval obtenue + signataires | "CR-2026-0089 = Standard CAB, approbation mainteneur (signature 2026-06-15 14h32, pas de Council car criticité = standard)" |
| **Impact analysis result** | Résultat impact analysis (scope, modules, risque régression) | "CR-2026-0089 : scope = module checkout (3 fichiers), risque régression = faible (couverture tests 92%, mutation 78%), dette ajoutée = 0" |
| **Change implemented** | Commit hash + tag + PR URL (audit trail git) | "CR-2026-0089 : commit a1b2c3d4 sur main, tag v2.4.1, PR #847 (merged 2026-06-15 16h), 142 insertions, 23 deletions" |
| **Regression test result** | Résultat regression suite (PASS/FAIL, taux, nouveaux défauts) | "CR-2026-0089 : 124/124 tests PASS (100%), 3 nouveaux tests ajoutés, mutation score 78% (cible 70% OK), 0 nouveau défaut 48h après deploy" |
| **EOL approach status** | Décision Q4 user 5.5 : EOL approche ou pas + escalade P10 si oui | "Système checkout : pas d'EOL (zone vivante, plan de remplacement actif v3.0 prévu Q4 2026, dette technique sous contrôle, pas d'escalade P10)" |

Stockés dans `.swebok_state.db` (table `udl_p9`) et consultables via Consultation Envelope (A1) par P8 Operations (qui monitor la santé post-patch) et P10 Retirement (si escalade EOL).

---

## Conditions de sortie (transition vers P8 Operations)

Le mainteneur valide la transition avec une **checklist à 100%** (11 critères) :

- [ ] `maintenance-request.md` existe (CR loggée avec type, scope, impact)
- [ ] `impact-analysis.md` existe (scope, modules, risque régression, dette)
- [ ] `change-implementation-report.md` existe (diff, fichiers touchés, tests ajoutés)
- [ ] `regression-test-report.md` existe (regression 100% PASS, mutation si refactoring)
- [ ] `maintenance-log.md` existe et à jour (entrée sous 24h)
- [ ] `updated-documentation.md` existe (technique, ops, user si feature)
- [ ] **Diff / patch concret** existe (commit hash + tag + PR URL, git)
- [ ] **Decision rationale** existe (pourquoi cette approche vs alternatives)
- [ ] **ADR** existe si structurante (impact archi documenté, MADR template)
- [ ] **Changelog public** existe si user-facing (semver, breaking changes)
- [ ] **Post-mortem** existe si incident causé par patch (cohérent P8)
- [ ] UDL 7 éléments loggés dans `.swebok_state.db` (table `udl_p9`)

Pas de feu vert séparé — les documents font foi.

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-07

### Mode 1 — Poisoning (Empoisonnement)

**Risque en P9** : un patch qui semble correct mais introduit un bug caché (régression), ou une "fix" qui ne fix pas la cause root (patch cosmétique), ou un impact analysis qui rate un module touché (diff insufficient). Plus subtil : un post-mortem qui blâme la mauvaise cause root et déclenche un patch sur le mauvais code.

**Mitigations spec v2** :
1. T1 casseur patch (Nexus-Critic, 3 invocations systématiques modes standard et structurant) — casse les patches incomplets/cosmétiques
2. Impact analysis obligatoire (EG-9.3) — détecte le scope avant implémentation
3. T2 conformité design DDS P4 + ADRs P3 + NFR P2 — vérifie que le patch respecte l'archi (pas de régression archi)
4. Regression testing 100% PASS (XG-9.2) — détecte les régressions directes
5. UDL 4 ("impact analysis result") expose le scope réel (vs scope annoncé)
6. Council structurante (Q3 user 5.5 = OUI) — examen pluridisciplinaire des patches structurants
7. Audit trail HMAC chain — traçabilité complète, pas d'action cachée

**Status** : ✅ Validé (7 mécanismes)

### Mode 2 — Distraction (Distraction)

**Risque en P9** : scope creep (le "petit fix" devient feature, "juste une petite migration" devient 2 semaines), ou accumulation de "quick wins" qui détournent de la dette technique, ou perfectionnisme sur le refactoring préventif au détriment des correctifs urgents.

**Mitigations spec v2** :
1. Q1 user 5.5 (type maintenance) cadre le scope dès le départ
2. Refus catégorique 2 (pas de refonte déguisée en maintenance) = escalade P3
3. Refus catégorique 3 (pas de nouvelle feature structurante) = escalade P2/P3
4. Budget adaptatif 3-niveaux (1k/2k/3k hotfix force focus minimal)
5. Impact analysis obligatoire (EG-9.3) — verrouille le scope
6. Critère d'abandon 1 (scope creep détecté → retour P3) = catch
7. Q4 user 5.5 (EOL approche) — distingue "investir dans le système" vs "préparer la mort" (pas de distraction sur dette si EOL approche)

**Status** : ✅ Validé (7 mécanismes)

### Mode 3 — Confusion (Confusion)

**Risque en P9** : type de maintenance ambigu (corrective vs preventive), ou criticité mal évaluée (hotfix traité comme standard), ou CAB approval floue (qui signe ?). Plus subtil : nommage incohérent des CR (INC-2026-0142 vs FIX-2026-0089, pas de pattern).

**Mitigations spec v2** :
1. Q1 user 5.5 (type maintenance) avec 4 options explicites — pas d'ambiguïté
2. Q2 user 5.5 (criticité) avec 3 options explicites (hotfix/standard/structurant) — pas d'ambiguïté
3. Q3 user 5.5 (CAB approval) avec 4 options explicites — pas d'ambiguïté
4. Q4 user 5.5 (EOL approche) avec 4 options explicites — pas d'ambiguïté
5. UDL 1-7 tracent toutes les décisions et leurs rationale — traçabilité
6. Convention de nommage stricte (CR-YYYY-NNNN, semver tags, PR-{date}-{short-desc})
7. T2 conformité design (Nexus-Critic) détecte les patches qui contredisent DDS/ADRs/NFR

**Status** : ✅ Validé (7 mécanismes)

### Mode 4 — Clash (Conflit)

**Risque en P9** : patch qui contredit la dette documentée, ou fix qui rentre en conflit avec un feature flag P7, ou migration qui casse un autre patch en cours. Plus subtil : 2 patches concurrents sur le même module qui se contredisent (deux PR ouvertes en parallèle).

**Mitigations spec v2** :
1. Pre-hydrate obligatoire (maintenance-log.md historique) — détecte les patches concurrents
2. T3 prédiction aval P10 (Nexus-Critic) — prédit les conflits aval (dette systémique, EOL approche)
3. UDL 4 ("impact analysis result") trace le scope — évite les conflits scope
4. Q3 user 5.5 (CAB approval) — examine les interactions cross-patches pour le structurant
5. Critère d'abandon 1 (scope creep → retour P3) — évite les dérives contradictoires
6. Q4 user 5.5 (EOL approche) — arbitre les conflits "investir vs préparer la mort"
7. Audit trail HMAC chain — toute action loggée, impossible de masquer un conflit

**Status** : ✅ Validé (7 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | Patch incomplet/cosmétique, impact analysis raté | 7 mécanismes | ✅ |
| Distraction | Scope creep, dette vs correctif | 7 mécanismes | ✅ |
| Confusion | Type/criticité/CAB/EOL flou | 7 mécanismes | ✅ |
| Clash | Patch contradictoire, dette conflict | 7 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Pattern reproductible de P0/P2/P3/P4/P5/P6/P7/P8 v2 étendu à P9.

---

## Adéquation aux besoins (section 7 grille comblée par projection + cohérence P0-P8 v2)

### 7.1 Usage réel projeté

Tableau 6 profils (effort en % du temps total projet) :

| Profil | Effort P9 (% projet) | Notes |
|--------|----------------------|-------|
| Greenfield from-scratch | 5-10% projet | Système jeune, peu de maintenance |
| Maintenance legacy | 25-40% projet | Dette accumulée, correctifs fréquents, refactoring régulier |
| Projet interne (équipe, gouvernance légère) | 10-20% projet | Maintenance standard, hotfix fréquent, refactoring ciblé |
| Projet externe client | 15-30% projet | Maintenance structurante, communication, changelog soigné |
| Compliance-driven (finance, santé, défense) | 20-35% projet | Maintenance ultra-traçée, CAB + Council systématique, audit log |
| R&D / exploration | 5-15% projet | Best-effort, dette acceptée, escalade P10 lente |

**Plage globale** : 5-40% projet selon profil. Plus faible que P5 (30-60%) et P6 (20-40%) mais récurrent (plusieurs cycles de maintenance sur la vie du système). Cohérent avec P8 (5-40% temps équipe/mois, continu).

### 7.2 Friction observée (projection)

4 frictions probables identifiées (projection cohérence P0-P8) :

1. **F1 — Scope creep** : le "petit fix" devient feature (refus 2, critère abandon 1)
   - **Mitigation** : Q1 user 5.5 (type maintenance) cadre le scope, T1 casseur patch détecte la dérive, impact analysis verrouille le scope
2. **F2 — CAB bottleneck** : CAB approval lente bloque les déploiements, perfectives attendues des semaines
   - **Mitigation** : Q3 user 5.5 (CAB approval) avec option "fast-track hotfix urgent" + "standard sans Council", pré-validation Council en parallèle
3. **F3 — Dette chronique** : patches correctifs qui s'empilent, refactoring préventif jamais priorisé
   - **Mitigation** : Q4 user 5.5 (EOL approche) distingue dette acceptable vs EOL imminent, Q1 user 5.5 (type) cadre preventive vs corrective (refactoring proactif peut être planifié en fenêtre dédiée)
4. **F4 — Régression non détectée** : patch qui casse en prod (régression non capturée par les tests)
   - **Mitigation** : regression suite 100% PASS obligatoire (XG-9.2), T1 casseur patch (Nexus-Critic), vérification 48h post-deploy (XG-9.7), post-mortem si incident (cohérent P8)

### 7.3 Pattern de contournement probable (projection)

4 contournements probables identifiés :

1. **C1 — Hotfix sauvage** (patch appliqué en urgence sans process) → mitigation refus 9 (hotfix sans re-test staging) + refus 5 (fix rapide sans doc) + audit trail HMAC (détection)
2. **C2 — Refonte déguisée** (refactoring majeur étiqueté "maintenance") → mitigation refus 2 (escalade P3) + T1 casseur détecte le scope creep + Q1 user 5.5 (type maintenance = perfective vs preventive vs feature)
3. **C3 — Documentation différée** (doc pas mise à jour pendant des semaines) → mitigation XG-9.3 sous 24h + critère abandon 3 (48h → escalade) + checklist 11 critères (validation finale)
4. **C4 — EOL ignoré** (système en fin de vie, patches qui s'empilent au lieu d'escalader P10) → mitigation Q4 user 5.5 (EOL approche explicite) + T3 prédiction aval P10 (Nexus-Critic) + UDL 7 trace la décision

### 7.4 Valeur ajoutée perçue (projection)

P9 v2 apporte 7 valeurs ajoutées vs v2-renum :

- **Démarcation P8↔P9 ET P9↔P10 explicite** : plus d'ambiguïté sur "qui fait quoi" (Run vs Change vs Retire)
- **Nexus-Critic T1+T2+T3 obligatoire** (cohérence P3-P7) : pas de patch non-vérifié, prédiction aval P10 incluse
- **Budget adaptatif 3-niveaux** (symétrie P8) : 1k/2k/3k hotfix, 3k/5k/8k standard, 5k/8k/15k structurant
- **4 décisions opérationnelles tranchées** (type + criticité + CAB + EOL) : structure les choix au lieu d'improviser
- **11 livrables (6+5)** : 6 standard + 5 ajouts (diff/patch concret + decision rationale + ADR + changelog public + post-mortem si incident)
- **UDL 7 éléments** : traçabilité complète (type, criticité, CAB, impact, change, regression, EOL)
- **Audit trail HMAC chain** : compliance + transparence (pas d'action cachée, pas de modification rétroactive)

### 7.5 Dette d'orchestration projetée

3 risques de dette identifiés (projection) :

1. **R1 — Criticité surévaluée** : patchs étiquetés "structurant" pour avoir Council + budget 15k
   - **Mitigation** : Q2 user 5.5 (criticité) avec critères explicites (impact > 5 fichiers, durée > 1 sem, migration schéma = structurant), UDL 2 logge la justification
2. **R2 — Dette acceptée chronique** : preventive jamais priorisé, dette s'accumule → escalade P10 inevitable
   - **Mitigation** : Q1 user 5.5 (preventive) peut être planifiée en fenêtre dédiée, Q4 user 5.5 (EOL approche) détecte la chronicité, UDL 7 trace les décisions
3. **R3 — Hotfix systématique** : abus du mode --lite (1k/2k/3k) pour éviter la rigor (pas de Council, pas de Critic)
   - **Mitigation** : Q2 user 5.5 avec critères explicites (typo, config, doc = hotfix, tout le reste = standard minimum), audit trail HMAC détecte les abus, refus 9 (hotfix sauvage)

---

## Notes de version

- **v2 (2026-06-07)** : refonte ciblée via audit (grille offline + 4 questions ciblées vague 1). Changements : (1) critère explicite de démarcation P8↔P9 ET P9↔P10 inscrit dans P9 (P8 = monitoring + incidents sans code ; P9 = CHANGEMENT de code planifié, système continue à vivre ; P10 = retirement, système archivé/s'arrête), (2) Nexus-Critic T1 casseur patch + T2 conformité design DDS P4 + ADRs P3 + NFR P2 + T3 prédiction aval P10 OBLIGATOIRE (3 invocations systématiques, comme P3/P4/P5/P6/P7), (3) hard cap 8k → adaptatif 3-niveaux (1k/2k/3k hotfix --lite, 3k/5k/8k standard single, 5k/8k/15k structurant multi, symétrie P8), (4) 6+5 livrables maintenus (6 standard + 5 ajouts : diff/patch concret + decision rationale + ADR + changelog public + post-mortem), (5) XG-9.1-XG-9.9 (9 exit criteria), (6) section 5.5 transformée en 4 décisions précises avec options AskUserQuestion (symétrie P8), (7) section 7 comblée par projection + cohérence P0-P8 v2 (effort 5-40% projet, 4 frictions + 4 contournements, 7 valeurs, 3 risques dette), (8) UDL 7 éléments P9-spécifiques documentés, (9) audit des 4 failure modes Drew Breunig complet, (10) Couverture cas universelle adaptative 6 cas, (11) 15 hooks alignés P8, (12) Refus catégoriques 10 (vs 6 v2-renum), (13) Critères d'échec 4 + d'abandon 7, (14) Pre-hydrate obligatoire (F7 recherche 2026), (15) Compaction par changement (AP5). 4 décisions tranchées vague 1.

- **v2-renum (2026-06-05)** : créé suite au fix structurel (renommage cascade P8→P9 après split P3). 4 activités, 6 livrables, agents en parallèle sans Nexus-Critic, 3k/5k/8k tokens uniforme, cap 35 min, 5.5 vide, pas d'UDL documenté, pas d'audit Drew Breunig, pas de démarcation P8↔P9 ni P9↔P10, pas de pre-hydrate, pas de 3-niveaux budget.

**Actions de suivi** :

- **P9-1** : `pre-tool-use/token-counter.sh` ligne 67 actuelle = `P9: 3000/5000/8000` (single par défaut). Évolution nécessaire pour supporter le mode adaptatif 3-niveaux (env var `SWEBOK_P9_MODE=hotfix|standard|structurant` ou flag `--severity`). En attendant, le défaut 3k/5k/8k couvre 50% des cas (corrective standard). Action non bloquante.
- **P9-2** : Mettre à jour la stratégie `audit/00-context-engineering-strategy.md` : budget P9 3k/5k/8k uniforme → adaptatif 3-niveaux (1k/2k/3k hotfix + 3k/5k/8k standard + 5k/8k/15k structurant), T1+T2+T3 P9 tranchée (obligatoire sauf --lite), section 9 "Tranchées P9" ajoutée, section 12.6 P9 passe de "Single" à "Adaptatif par criticité (3-niveaux, symétrie P8)".
- **P9-3** : Acquisition livres P9 manquants (Feathers Legacy Code 2004 + Sadalage Refactoring Databases 2006). Non bloquant, planifier avec P10 dans le batch d'acquisition.
- **P9-4** : Council structurante P9 (CISO + DevOps-Lead + Architect) — formaliser le skill agent si pas déjà fait. Vérifier que `nexus-ciso`, `nexus-devops-lead`, `nexus-architect` peuvent être convoqués ensemble.

Voir `audit/phase-9-maintenance-audit.md` pour la traçabilité des décisions.
