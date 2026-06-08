# Phase 8: Operations Workflow Spec

> **Statut** : v2 — validé 2026-06-07 par le mainteneur (audit P8 clos via grille offline + 4 questions vague 1, verdict 🟢 dès la première conversation).
> **Changement vs v2-renum** : (1) **critère explicite de démarcation P7↔P8 ET P8↔P9** inscrit dans P8 (P7 = release + monitoring SETUP avant deploy ; P8 = monitoring CONTINU post-release + alertes + escalade + capacity planning + post-mortems ; P9 = CHANGEMENT de code planifié), (2) **mécanique agent ADAPTATIVE par sévérité incident** (monitoring courant = single Nexus-SM sans Critic, incident standard P2/P3 = single + Nexus-Critic T2 spec-compliance vs runbook, incident critique P0/P1 = multi-agent + Nexus-Critic T1+T2+T3 + Council post-incident), (3) **Budget tokens PAR INCIDENT adaptatif** (1k/2k/3k monitoring courant, 2k/4k/6k incident standard, 5k/8k/15k incident critique), (4) **Section 5.5 transformée en 4 décisions opérationnelles précises** (calibration seuils SLO/SLI, priorisation incidents P0-P3 + escalade, profondeur post-mortem 1-page vs full RCA, acceptation incidents deferred), (5) **Section 7 comblée par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7 v2**, (6) **UDL 7 éléments P8-spécifiques** documentés, (7) **audit des 4 failure modes Drew Breunig** complet, (8) **Couverture cas universelle adaptative** 6 cas, (9) **Hooks à invoquer** alignés P7 (15 hooks), (10) **Refus catégoriques 10** (vs 6 v2-renum), (11) **Critères d'échec 4 + d'abandon 7**.
> **Changement vs structure antérieure** : v2-renum créée 2026-06-05 (renommage cascade P7→P8 après split P3). Refonte ciblée pour aligner sur P3/P4/P5/P6/P7 v2 + intégrer les démarcations P7↔P8 et P8↔P9 + mode adaptatif par sévérité (spécificité P8 phase vivante).
> **But** : maintenir la production saine après le handoff P7 (monitoring continu + alertes calibrées + on-call + escalade + capacity planning + post-mortems), sans modifier le code (escalade P9) ni redéfinir le monitoring setup (escalade P7).

## Metadata

- **Phase**: 8
- **Name**: Operations
- **Purpose**: Maintain production system health through continuous monitoring, incident response, capacity planning, and post-mortem learning
- **Parallel Mode**: Adaptatif par sévérité (single par défaut, multi-agent justifié pour incidents critiques P0/P1)
- **Équivalent SWEBOK v4** : Hors core KA. SWEBOK v4 fusionne Operations et Maintenance dans P6 — le présent modèle sépare les deux : Operations (P8) = vivant/courant (monitoring + incidents sans modification code) ; Maintenance (P9) = projet/changement (modification code planifiée). Justification : nature temporelle ET activité différentes.
- **Référentiels** : ITIL v4 (Service Operation + Continual Improvement), ISO/IEC/IEEE 12207:2017 (operation process), Google SRE Book (Beyer et al. 2016 + Workbook 2018 + Enterprise Adoption 2023), NIST 800-61r2 (Computer Security Incident Handling Guide), DevOps Handbook (Kim 2021)

---

## Mission (1 phrase)

> « Maintenir la production saine après le handoff P7 (monitoring continu + alertes calibrées + on-call + escalade + capacity planning + post-mortems) en mode adaptatif par sévérité incident — sans redéfinir le monitoring setup (escalade P7) ni modifier le code de production (escalade P9 pour tout changement planifié, escalade P7 pour tout re-deploy). »

---

## Critère de démarcation P7 (Deployment) ↔ P8 (Operations) ↔ P9 (Maintenance)

> **Validation 2026-06-07** : le mainteneur a tranché pour des critères explicites, inscrits dans P8 ET P7 ET P9. **P7 = release + monitoring SETUP (configure AVANT deploy) ; P8 = monitoring CONTINU post-release + alertes + escalade + capacity planning + post-mortems (RUN après deploy, sans modification code) ; P9 = CHANGEMENT de code planifié (corrective/adaptive/perfective/preventive)**. Trois questions simples : P7 "je lance le deploy ?", P8 "la prod tourne ?", P9 "je modifie le code ?".

### Démarcation P7 ↔ P8

| Dimension | P7 Deployment (déjà tranché en v2 finale) | P8 Operations (cette spec) |
|-----------|--------------------------------------------|------------------------------|
| **Question centrale** | **Est-ce que la prod tourne correctement après le deploy ?** (court terme, fenêtre de deploy) | **Est-ce que la prod reste saine au fil du temps ?** (long terme, exécution continue) |
| **Activité dominante** | Déployer (release + smoke tests + handoff) | Monitorer (alertes + on-call + capacity + post-mortems) |
| **Lieu d'exécution** | Production (release, smoke tests post-deploy, monitoring SETUP) | Production (monitoring CONTINU, alertes RUN, incidents) |
| **Périmètre fonctionnel** | Release packaging, infrastructure prod, communication stakeholders, handoff ops | Monitoring exécution, alertes calibration, incident response, capacity planning, post-mortems |
| **Outputs typiques** | `deployment-plan.md`, `deployment-report.md`, `runbook.md` (livré), `monitoring-dashboard.md` (configuré) | `operations-dashboard.md`, `incident-log.md`, `post-mortem-*.md`, `capacity-forecast.md`, `sla-compliance-report.md` |
| **Adversarial** | T1 casseur plan + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 | **Adaptatif** : aucun en monitoring courant, T2 spec-compliance vs runbook en incident standard, T1+T2+T3 + Council en incident critique |
| **Agents typiques** | Nexus-DevOps-Lead, DevOps, Backend, Frontend, SM, Critic | **Adaptatif** : Nexus-SM seul (courant), Nexus-SM + Critic T2 (standard), Hyperagent + SM + DevOps + Security + Backend/Frontend + Critic T1+T2+T3 + Council (critique) |

**Règle simple P7 vs P8** : si la décision impacte **le release lui-même (scripts, schedule, rollback test) ou le monitoring SETUP (config initiale alertes, runbook livré, dashboard configuré)** = P7. Si elle impacte **le monitoring CONTINU (calibration alertes au fil du temps), une réponse incident (escalade, communication, résolution), un capacity forecast, ou un post-mortem** = P8.

### Démarcation P8 ↔ P9

| Dimension | P8 Operations (cette spec) | P9 Maintenance (à auditer) |
|-----------|------------------------------|------------------------------|
| **Question centrale** | **La prod tourne-t-elle (monitoring + incidents sans modif code) ?** | **Dois-je modifier le code (corrective/adaptive/perfective/preventive) ?** |
| **Activité dominante** | Monitorer + répondre aux incidents (sans code) | Modifier le code planifié + tester + redéployer |
| **Décisions** | Calibration alertes, priorisation incidents, escalade, post-mortem profondeur, acceptation deferred | Type de maintenance (corrective/adaptive/perfective/preventive), impact analysis, CAB approval, scope du patch |
| **Outputs typiques** | `incident-log.md`, `post-mortem-*.md`, `capacity-forecast.md` | `maintenance-request.md`, `impact-analysis.md`, `change-implementation-report.md`, `regression-test-report.md` |
| **Trigger transition** | Incident répété (>3 en 30j) OU SLA breach répété OU besoin refactoring = change request formelle → P9 | Maintenance complétée + system back to steady-state → retour P8 |
| **Agents typiques** | Adaptatif (cf. section Responsible Agents) | Nexus-Backend + Frontend + DevOps + Security + QA + PM |

**Règle simple P8 vs P9** : si la décision **ne modifie PAS le code** (calibrer un seuil, écrire un post-mortem, escalader un incident, forecaster la capacité) = P8. Si la décision **modifie le code de production** (bugfix, security patch, refactoring, feature mineure planifiée) = P9 (avec impact analysis + regression testing obligatoires).

### Cas limites types

- "Calibrer un seuil d'alerte (latence > 200ms → > 300ms)" = **P8** (config monitoring, pas de code). UDL 1 ("alert threshold calibrated") logge la décision + rationale.
- "Configurer alerts initiales" (avant deploy) = **P7** (setup, fait dans `monitoring-dashboard.md` P7).
- "Modifier le code pour réduire les alertes" (par exemple corriger une N+1 query qui sature le DB) = **P9** (fix corrective, avec impact analysis + regression).
- "Écrire un post-mortem après incident P0" = **P8** (analyse post-incident, livrable P8). Mais "Implémenter l'action correctrice du post-mortem (fix du code)" = **P9** (change implementation).
- "Décider de scaler horizontalement (passer de 4 à 8 instances)" = **P8** (capacity planning, config infra, pas de code applicatif). Mais "Refactorer le code pour réduire la consommation mémoire" = **P9** (fix perfective).
- "Hotfix urgent pendant incident" = **escalade P7** (re-deploy d'urgence) si la cause est une régression P7, sinon **escalade P9** (change urgent avec fast-track CAB). P8 ne fait JAMAIS de modification code en autonomie.
- "Communiquer aux stakeholders pendant un incident" = **P8** (decision 3 UDL, "stakeholder communication"). Mais "Définir le plan de communication initial" = **P2** (requirement).

**Conséquence opérationnelle sur P7 v2 finale** : aucune modification. P7 livre le runbook + monitoring dashboard + handoff signé, P8 les consomme et les fait vivre. Le monitoring setup P7 est **une entrée** de P8, pas un sujet de re-décision.

**Conséquence opérationnelle sur P9 v2-renum (à auditer)** : la spec P9 actuelle confirme la transition P8→P9 via `maintenance-request received` (EG-9.2). P8 émet la CR formelle quand un incident nécessite un changement code.

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-8.1 | Phase 7 deployment complete + handoff signé | Deployment report P7 + handoff memo (XG-7.6) | "PHASE_7_COMPLETE" signé + 100% checklist 11 critères P7 |
| EG-8.2 | Production system operational | System status (XG-7.1 + XG-7.2) | ≥99.5% availability + smoke tests post-deploy 100% pass |
| EG-8.3 | Operations documentation delivered (runbook + ops doc) | Ops docs completeness (P7 XG-7.6) | 100% required docs delivered (runbook, ops doc, user doc, escalation paths) |
| EG-8.4 | Support team trained | Training completion (P7 handoff) | 100% team trained + brief Nexus-SM 30 min |
| EG-8.5 | Monitoring systems active + alertes testées | Monitoring status (P7 XG-7.4) | All monitors reporting + alertes configurées et testées |
| EG-8.6 | Operations SLA defined | SLA document (P2 requirements) | SLO/SLI documentés + sign-off mainteneur + sponsor |
| EG-8.7 | Audit trail P7 transmis | Audit log P7 (XG-7.8) | HMAC chain vérifié, transmis à compliance lead |
| EG-8.8 | On-call rotation établie | On-call schedule | Rotation définie (24/7, business hours, ou best-effort selon profil) |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers Phase 7 (Deployment) remediation (escalade pour monitoring setup ou handoff incomplet).

---

## Exit Gate

> **Note phase vivante** : contrairement aux phases projet (P0-P7, P9, P10), P8 est une phase **continue** (longue durée). Les "exit criteria" P8 sont des **conditions de transition vers P9 (maintenance)** déclenchées par un événement (CR formelle, EOL, refonte). Le mode normal est "P8 continue", pas "P8 complete".

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-8.1 | System operational targets met | SLO compliance | ≥99.5% uptime sur fenêtre glissante 30 jours |
| XG-8.2 | Incident management process stable | MTTR/MTTF metrics | MTTR ≤4h, MTTF ≥720h |
| XG-8.3 | Performance KPIs respectés | Performance metrics | All KPIs within thresholds (NFR P2 toujours en cible) |
| XG-8.4 | Security posture maintained | Security score | ≥85% security score, 0 CVE critique non-patché |
| XG-8.5 | Operations metrics documented | Metrics dashboard live | Real-time dashboard + alertes calibrées + accessibles à l'équipe |
| XG-8.6 | Capacity plan current | Capacity forecast | Forecast trimestriel à jour + scaling recommandé documenté |
| XG-8.7 | "30-day stable operation" atteint (transition P9 ready) | Stability log | 30 jours sans incident P0/P1, ≤2 incidents P2 |
| XG-8.8 | UDL 7 éléments P8-spécifiques loggés | UDL set | 100% loggés dans `.swebok_state.db` (table `udl_p8`) |
| XG-8.9 | Audit trail P8 complet | Audit log P8 | Trace de tous les incidents + post-mortems + escalades + calibrations |
| XG-8.10 | Post-mortems publiés pour tous incidents P0/P1 | Post-mortem repository | 100% incidents P0/P1 ont un post-mortem signé (1-page minimum, full RCA si critique) |

**Gate Evaluation**: P8 reste active tant que (a) le système tourne sans changement code ET (b) aucun seuil d'escalade n'est franchi. Transition P9 déclenchée par : maintenance request formelle (EG-9.2) OU incident répété (>3 P2 en 30j) OU besoin refactoring justifié.

**XG-8.5 — Adaptativité par profil projet (note)** : pour les projets compliance/sécurité, monitoring 24/7 + alertes P0 sur SLO breach. Pour les projets R&D/POC, monitoring best-effort acceptable.

---

## Transition Criteria to Phase 9 (Maintenance)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Operations steady-state confirmed | Nexus-SM | Maintenance Lead | 30-day stable operation (XG-8.7) |
| Maintenance request received (CR formelle) | System/User/Post-mortem action | Maintenance Team | Ticket loggé (impact, type corrective/adaptive/perfective/preventive) |
| Impact analysis completed | Nexus-PM | Maintenance Lead | Impact assessment done (P9 EG-9.3) |
| Maintenance window approved | Operations | Maintenance Lead | Window scheduled (P9 EG-9.4) |
| Resources allocated | Project Lead | Maintenance | Resources confirmed (P9 EG-9.5) |
| CAB approval (si changement structurant) | Change Advisory Board | Maintenance Lead | CAB approval documented (P9 EG-9.6) |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_8_TO_P9_TRANSITION` only when maintenance transition criteria met and logged. P8 reste active en parallèle (monitoring continue pendant la maintenance P9).

---

## Key Activities

### Activity 8.1: Continuous System Monitoring
- Monitorer la santé système (CPU, RAM, disk, network) en temps réel
- Tracker les performance metrics (latency p50/p95/p99, throughput, error rate)
- Monitorer les événements de sécurité (failed auth, suspicious patterns, CVE alerts)
- Générer les rapports opérationnels périodiques (daily/weekly/monthly)
- **Calibrer les seuils d'alerte** au fil du temps (UDL 1, décision user 5.5.A)

### Activity 8.2: Incident Management (adaptatif par sévérité)
- Recevoir et logger les incidents (ticket system, auto-créé sur alerte)
- **Triage et catégorisation** : P0 critique (service down, security breach), P1 majeur (SLO breach), P2 modéré (perf dégradé), P3 mineur (cosmétique)
- Coordonner la résolution selon la sévérité (single Nexus-SM pour P2/P3, multi-agent + Council pour P0/P1)
- Communication stakeholders pendant incident (UDL 3, décision user 5.5.D)
- Mener les incident reviews systématiques (post-mortem 1-page minimum, full RCA pour P0/P1)
- **Escalader** selon les règles (UDL 2, décision user 5.5.B)

### Activity 8.3: Performance Management
- Monitorer la performance système en continu
- Identifier les opportunités d'optimisation (sans modifier le code = capacity scaling, config tuning)
- Si optimisation nécessite code = escalade P9 (corrective/perfective)
- Reporter les performance metrics (KPI dashboard, weekly review)

### Activity 8.4: Security Operations
- Monitorer les événements de sécurité (24/7 si profil compliance, business hours sinon)
- Répondre aux incidents de sécurité (escalade CISO si P0/P1 security)
- Maintenir les security controls (patches OS/dépendances, certificats TLS rotation)
- Conduire les security assessments périodiques (trimestriel)

### Activity 8.5: Capacity Planning + Forecasting
- Mesurer la croissance utilisation (CPU/RAM/disk/network/DB connections)
- Forecaster la capacité requise (1 mois, 3 mois, 6 mois)
- Recommander le scaling (vertical, horizontal, géographique) — config infra, pas code
- Si scaling nécessite refactoring code = escalade P9 (perfective)

### Activity 8.6: Post-Mortem Process
- Pour chaque incident P0/P1 : post-mortem obligatoire dans les 5 jours ouvrés
- Format : 1-page minimum (cause root, timeline, action correctrice, lessons learned), full RCA pour incidents critiques
- **Profondeur** = décision user 5.5.C (1-page vs full RCA selon sévérité + impact business)
- Action correctrice = soit calibration P8 (config), soit escalade P9 (code), soit escalade P7 (re-deploy)
- Publication : repository post-mortems versionné, partage équipe pour learning

### Activity 8.7: Adversarial Validation (adaptatif par sévérité incident)

**Monitoring courant** (pas d'incident actif) : **aucun Nexus-Critic** (gaspillage tokens, P8 = exécution).

**Incident standard P2/P3** : **Nexus-Critic T2 seul** (spec-compliance vs runbook) — vérifier que la procédure suivie respecte le runbook P7 livré. Cible : `incident-log.md` + procédure suivie vs `runbook.md` P7.

**Incident critique P0/P1** : **Nexus-Critic T1+T2+T3 OBLIGATOIRE + Council post-incident** :
- **T1 casseur réponse incident** : Nexus-Critic relit la réponse, cherche des failles (étapes manquantes, escalade tardive, communication insuffisante)
- **T2 conformité runbook + SLA** : Nexus-Critic vérifie que la réponse respecte le runbook P7 + les SLA définis P2
- **T3 prédiction récurrence** : Nexus-Critic prédit si l'incident peut récurrer (cause root systémique vs ponctuelle) → trigger escalade P9 si systémique
- **Council post-incident** : CISO + DevOps-Lead + SM examinent le post-mortem, valident l'action correctrice, signent la fermeture

---

## Responsible Agents

> **Mécanique adaptative par sévérité** (décision mainteneur 2026-06-07, vague 1) : P8 n'a pas une configuration fixe. Elle s'adapte à la situation opérationnelle.

### Mode "Monitoring courant" (sans incident actif)

| Agent | Role |
|-------|------|
| **Nexus-SM (seul)** | Surveillance dashboards, calibration seuils alerte, capacity forecast périodique |

**Concurrency** : **single-agent** (F13 recherche 2026 — monitoring courant = lecture continue, pas de création).
**Nexus-Critic** : **aucun** (P8 monitoring = exécution, pas création, gaspillage tokens).
**Budget** : **1k/2k/3k**.

### Mode "Incident standard P2/P3"

| Agent | Role |
|-------|------|
| Nexus-SM (lead) | Triage, response, communication interne, log incident |
| Nexus-DevOps (support) | Investigation infrastructure si besoin |
| **Nexus-Critic (T2 seul)** | Spec-compliance vs runbook P7 (vérifier procédure suivie) |

**Concurrency** : **single-agent + support ponctuel** (F13 recherche 2026).
**Nexus-Critic** : **T2 seul** (spec-compliance vs runbook) — 1 invocation.
**Budget** : **2k/4k/6k par incident**.

### Mode "Incident critique P0/P1"

| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordonne la réponse multi-agent |
| **Nexus-SM (lead)** | Triage, response, communication stakeholders, log incident |
| Nexus-DevOps | Investigation infrastructure + actions correctrices config |
| Nexus-Security | Si security incident (escalade CISO) |
| Nexus-Backend, Nexus-Frontend | Support investigation par couche applicative |
| **Nexus-Critic (T1+T2+T3 obligatoires)** | T1 casseur réponse + T2 conformité runbook + SLA + T3 prédiction récurrence |
| **Council post-incident (CISO + DevOps-Lead + SM)** | Examen post-mortem, validation action correctrice, sign-off fermeture |

**Concurrency** : **multi-agent justifié** (F13 recherche 2026 — incident critique = read-heavy parallèle sur logs + métriques + sécurité + comm, disjoint tools).
**Nexus-Critic** : **T1+T2+T3 obligatoires** (3 invocations systématiques, comme P3/P4/P5/P6/P7).
**Council post-incident** : **OBLIGATOIRE** pour P0/P1, examen 1h dans les 5 jours ouvrés.
**Budget** : **5k/8k/15k par incident critique** (cohérence P3-P7).

### Patterns adversariaux T1/T2/T3 (rappel, mode P0/P1 uniquement)

- **T1 (casseur réponse)** : Nexus-SM produit la réponse incident, Nexus-Critic la casse (cherche les failles). Cible : `incident-log.md`, `post-mortem-*.md`.
- **T2 (spec-compliance)** : Nexus-Critic vérifie conformité runbook P7 + SLA P2 + procédure suivie. Cible : `incident-log.md` vs `runbook.md` P7 + SLA P2.
- **T3 (conséquentialiste)** : Nexus-Critic prédit la récurrence de l'incident (cause root systémique → escalade P9, ponctuelle → action correctrice config P8). Cible : `post-mortem-*.md` → `change-request-*.md` (si systémique).

**Isolation des contextes (ACI stratégie §4.5)** : Nexus-Critic ne voit pas le prompt système du producteur. Chaque rôle adversarial a un contexte distinct.

---

## Required Skills

- `nexus-sm`: Service management, incident response, calibration alertes
- `nexus-devops`: Infrastructure monitoring, scaling config, investigation
- `nexus-security`: Security monitoring, response, escalade CISO
- `nexus-backend`, `nexus-frontend`: Support investigation par couche applicative
- `nexus-critic`: Adversarial validation (T2 seul pour P2/P3, T1+T2+T3 pour P0/P1) — **adaptatif par sévérité**
- `nexus-ciso`: Council post-incident P0/P1 (sécurité)
- `nexus-devops-lead`: Council post-incident P0/P1 (infra)

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-operations-stable` | 30-day stable operation (XG-8.7) | Signal transition P9 disponible |
| `incident-detected` | New incident (auto-créé sur alerte) | Triggers incident management adaptatif |
| `incident-triaged-p0p1` | Incident classé P0 ou P1 | Active mode multi-agent + Nexus-Critic T1+T2+T3 + Council |
| `incident-triaged-p2p3` | Incident classé P2 ou P3 | Active mode single + Nexus-Critic T2 |
| `sla-breach-warning` | SLA at risk (seuil > 80% budget erreur) | Alerts operations lead |
| `sla-breach-confirmed` | SLA violé | Escalade mainteneur + auto-trigger post-mortem |
| `security-event-detected` | Security event | Triggers security response + escalade CISO si P0/P1 |
| `maintenance-required` | Incident systémique ou refactoring nécessaire | Triggers Phase 9 (Maintenance) avec change request |
| `post-mortem-due` | Incident P0/P1 fermé depuis 5 jours sans post-mortem | Reminder + escalade si overdue |
| `capacity-saturation-warning` | Capacity > 80% sur ressource critique | Trigger capacity planning urgent |
| `capacity-saturation-critical` | Capacity > 90% sur ressource critique | Escalade mainteneur + auto-trigger scaling |
| `alert-threshold-calibrated` | UDL 1 loggé | Audit trail config monitoring |
| `incident-resolved` | Incident fermé | Update SLA tracking + check si post-mortem dû |
| `council-post-incident-convened` | P0/P1 incident, Council activé | Council examen 1h |
| `udl-p8-logged` | UDL 7 éléments loggés | Snapshot pour phases suivantes |

---

## Artifacts Produced

| Artifact | Description | Location | Format |
|----------|-------------|----------|--------|
| `operations-dashboard.md` | Dashboard santé système + métriques live | `specs/workflows/by-phase/phase-8-operations/` | md (résumé) + JSON (config Grafana/Datadog) |
| `incident-log.md` | Log de tous les incidents (auto-créé sur alerte) | `specs/workflows/by-phase/phase-8-operations/` | md (synthèse) + JSON (machine-parse) |
| `performance-report.md` | Performance metrics (KPI weekly/monthly) | `specs/workflows/by-phase/phase-8-operations/` | md |
| `security-posture-report.md` | Security status (CVE, patches, audits) | `specs/workflows/by-phase/phase-8-operations/` | md |
| `sla-compliance-report.md` | SLA achievement (SLO/SLI vs cible) | `specs/workflows/by-phase/phase-8-operations/` | md + JSON (machine-parse) |
| `operations-handbook.md` | Day-to-day operations guide (procédures courantes) | `specs/workflows/by-phase/phase-8-operations/` | md |
| `post-mortem-{incident-id}.md` (livrable ajouté) | Post-mortem par incident P0/P1 (1-page ou full RCA) | `specs/workflows/by-phase/phase-8-operations/post-mortems/` | md (template standard) |
| `capacity-forecast.md` (livrable ajouté) | Forecast capacité 1m/3m/6m + scaling recommandé | `specs/workflows/by-phase/phase-8-operations/` | md + JSON (machine-parse) |
| `change-request-{cr-id}.md` (livrable ajouté) | Change request formelle pour P9 (depuis post-mortem ou capacity planning) | `specs/workflows/by-phase/phase-8-operations/change-requests/` | md + JSON |
| `on-call-rotation.md` (livrable ajouté) | Schedule on-call (24/7, business hours, ou best-effort) | `specs/workflows/by-phase/phase-8-operations/` | md + JSON (machine-parse) |
| `audit-trail-p8.md` (livrable ajouté) | Trace de tous les incidents + post-mortems + escalades + calibrations | `specs/workflows/by-phase/phase-8-operations/` | md (synthèse) + JSON (HMAC chain) |

**Format de stockage** :
- Specs narratives : md (lecture humaine)
- Métriques : JSON/TSDB (Prometheus, InfluxDB, Datadog)
- Incidents : ticketing system (Jira, Linear, PagerDuty) + log md/JSON pour audit
- Audit trail : JSON (HMAC chain, Cossack Labs 2025) + md (synthèse)
- Logs structurés : JSON centralisés (ELK, Loki, Splunk)

**Convention de nommage** :
- Post-mortems : `post-mortem-{YYYY-MM-DD}-{incident-id}.md`
- Change requests : `change-request-{YYYY-MM-DD}-{cr-id}.md`
- Audit trail : `audit-trail-p8.md` + `audit-trail-p8.json`

**Localisation** : tous dans `specs/workflows/by-phase/phase-8-operations/`.

---

## Format des fichiers (triple différencié, aligné P3/P4/P5/P6/P7 v2)

| Type de livrable | Format primaire | Format secondaire | Standard |
|------------------|------------------|-------------------|----------|
| **Specs narratives** (dashboard, handbook, post-mortems, capacity, on-call) | md (lecture humaine) | — | Markdown CommonMark |
| **Métriques temps réel** | JSON/TSDB | md (résumé) | Prometheus, InfluxDB, Datadog |
| **Incidents** | Ticketing system | md (log) + JSON (machine-parse) | Jira, Linear, PagerDuty, Opsgenie |
| **Logs** | JSON structurés centralisés | — | ELK, Loki, Splunk |
| **Audit trail** | JSON (HMAC chain) | md (synthèse) | Cossack Labs 2025 |
| **Change requests** | md (description) | JSON (machine-parse) | ITIL CR standard |

---

## Hyperagent Parallel Processing (adaptatif par sévérité)

### Mode "Monitoring courant" (sans incident)

```
single_task:
  - task: continuous_monitoring
    agents: [Nexus-SM]
    sync: false
    cadence: continuous
```

### Mode "Incident standard P2/P3"

```
parallel_tasks:
  - task: incident_response
    agents: [Nexus-SM (lead), Nexus-DevOps (support si besoin)]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après response):
  - task: t2_runbook_compliance
    agents: [Nexus-Critic]
    target: incident-log.md vs runbook.md P7
    sync: true

reduction: "Nexus-SM clôt l'incident dans incident-log.md"
```

### Mode "Incident critique P0/P1"

```
parallel_tasks:
  - task: incident_triage_p0p1
    agents: [Nexus-SM (lead)]
    sync: true (premier triage avant fan-out)

  - task: infrastructure_investigation
    agents: [Nexus-DevOps]
    sync: false

  - task: security_investigation
    agents: [Nexus-Security]
    sync: false
    only_if: security_incident

  - task: backend_investigation
    agents: [Nexus-Backend]
    sync: false

  - task: frontend_investigation
    agents: [Nexus-Frontend]
    sync: false

  - task: stakeholder_communication
    agents: [Nexus-SM]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après parallel):
  - task: t1_casseur_response
    agents: [Nexus-Critic]
    target: incident-log.md + procédure suivie
    sync: true

  - task: t2_runbook_sla_compliance
    agents: [Nexus-Critic]
    target: incident-log.md vs runbook.md P7 + SLA P2
    sync: true

  - task: t3_recurrence_prediction
    agents: [Nexus-Critic]
    target: post-mortem-*.md → change-request-*.md (si systémique)
    sync: true

council_post_incident (sequential, dans les 5 jours):
  - task: council_examen
    agents: [Nexus-CISO, Nexus-DevOps-Lead, Nexus-SM]
    target: post-mortem-*.md, action correctrice
    sync: true

reduction: "Nexus-SM clôt l'incident + publie post-mortem signé"
```

---

## Refus catégoriques (10)

La phase P8 **refuse** de :
1. **Pas de modification du code de production** (escalade P9 — règle de démarcation ; P8 = monitoring + incidents sans code)
2. **Pas de re-deploy en autonomie** (escalade P7 — règle de démarcation ; P7 = release, pas P8)
3. **Pas de redéfinition du monitoring setup** (escalade P7 — alerts initiales, runbook livré, dashboard configuré)
4. **Pas de redéfinition des NFR P2** (escalade P2 — SLO/SLI définis en P2)
5. **Pas de SLO dégradé accepté sans communication** stakeholders (transparence obligatoire)
6. **Pas d'alerte silencieuse** (alert fatigue acceptée = dette explicite, audit obligatoire)
7. **Pas de secrets en clair dans les logs** (scan automatique pre-log, vault obligatoire)
8. **Pas de skip de post-mortem** après incident P0/P1 (1-page minimum dans les 5 jours)
9. **Pas de post-mortem sans action correctrice** (action = config P8, code P9, ou re-deploy P7 — pas juste documentation)
10. **Pas de skip d'escalade** (chaque incident suit la chaîne d'escalade définie selon sévérité)

---

## Critères d'échec (4) et d'abandon (7 + temps)

### Critères d'échec (déclenchent une action immédiate)

1. **SLA violé (SLO breach répété > 3 en 30j)** → escalade mainteneur + auto-trigger post-mortem + analyse cause root systémique
2. **Incident non résolu après escalation** → rotation P9 Maintenance (CR formelle avec impact analysis)
3. **Monitoring cassé (alertes perdues)** → escalade ops + investigation immédiate (perte de visibilité = critique)
4. **Capacité saturée (CPU/RAM/disk > 90%)** → capacity planning urgence + escalade mainteneur si scaling code nécessite refactoring (P9)

### Critères d'abandon (l'agent abandonne et prévient le mainteneur si)

1. SLA breach répété (>3 en 30j) après plusieurs cycles de calibration → escalade mainteneur pour décision (acceptation deferred ou refonte)
2. Incident P0/P1 non résolvable en autonomie (cause root inconnue) → escalade mainteneur + Council post-incident
3. Capacity saturée + scaling vertical maxed out + horizontal nécessite refactoring code → escalade P9 (perfective majeure)
4. Post-mortem overdue depuis 10 jours pour incident P0/P1 → escalade mainteneur (process broken)
5. Alert fatigue confirmée (> 50 alertes/jour ignorées) → escalade mainteneur + refonte runbook P7
6. Monitoring drift (alertes inutiles ou alertes manquantes) → recalibration majeure ou escalade P7 (re-setup)
7. Dépassement de 35 min sans avancée claire **sur un incident** → escalade mainteneur, redécoupage (F6 recherche 2026)

---

## Tokens budget (adaptatif par sévérité incident)

> **Validation 2026-06-07** : le mainteneur a tranché pour un **budget adaptatif par incident**, pas par session globale. Compaction immédiate après RCA (AP5 recherche 2026).

| Mode | Base | Soft cap (CC) | Hard cap (abort) | Justification |
|------|------|---------------|------------------|---------------|
| **Monitoring courant** (sans incident) | **1k** | **2k** | **3k** | Single Nexus-SM, lecture continue dashboards, pas de création |
| **Incident standard P2/P3** | **2k** | **4k** | **6k** | Single Nexus-SM (lead) + DevOps (support ponctuel) + Nexus-Critic T2 (1 invocation, ~1.5k). Compaction immédiate après RCA |
| **Incident critique P0/P1** | **5k** | **8k** | **15k** | Multi-agent (Hyperagent + SM + DevOps + Security + Backend + Frontend) + Nexus-Critic T1+T2+T3 (3 invocations, ~4.5k) + Council post-incident. Cohérent P3/P4/P5/P6/P7 |

**Pre-hydrate obligatoire** (F7 recherche 2026 — 60% du 1er tour = retrieval) : au début de chaque session ops (et à chaque incident), charger dans le hot_context (`.swebok_state.db`) la slice suivante :
- `runbook.md` (P7 livré)
- `monitoring-dashboard.md` (P7 configuré)
- Alertes actives (slice des 10 dernières)
- Historique incidents similaires (cross-incident memory, top 5 par pattern)
- SLA P2 (SLO/SLI cibles)
- Audit trail P7 (HMAC chain pour validation handoff)
- Pour incident P0/P1 : pré-fetcher aussi NFR P2 + ADRs P3 (si action correctrice impacte archi)

Sans ce pre-hydrate, 60% du budget du 1er tour est consommé en retrieval, ce qui sature le soft cap en nominal sur monitoring courant (qui a un budget serré 1k/2k/3k).

**Note importante (action de suivi)** : `pre-tool-use/token-counter.sh` ligne 66 actuelle = `P8: 2000/4000/6000` (incident standard par défaut). Pour supporter le mode adaptatif 3-niveaux, évolution du script nécessaire (env var ou flag `--severity` pour switcher entre `monitoring`, `standard`, `critical`). En attendant, le défaut 2k/4k/6k couvre 90% des cas (incidents standards). Action P8-1 dans la liste d'actions.

---

## Pauses

**Spécificité P8 phase vivante** : pas de compaction globale (P8 n'est jamais "complete"). Compaction **par incident** (chaque incident = unité de travail bornée).

- **Compaction checkpoint par incident** : à 60-70% du soft cap selon mode (1.4k monitoring courant, 2.8k incident standard, 5.6k incident critique)
- **Compaction immédiate après RCA** (AP5 recherche 2026) : dès que la cause root est identifiée, drop les logs verbeux d'investigation, garder uniquement (cause, timeline, action correctrice, lessons learned)
- **Memory à long terme des incidents résolus** : consultable via L0 corpus (pas dans le contexte), accessible par tool call pour pattern matching cross-incident
- **Compaction agressive logs** entre incidents : drop les logs bruts, garder uniquement les digests RCA (AP3 recherche 2026)
- **Tool result clearing** : vider les requêtes monitoring brutes après parsing (AP6 recherche 2026)

**Pas de transcript complet en wakeup** (AP3) : à chaque reprise de session ops, charger uniquement le digest des 10 derniers incidents + alertes actives. Pas de re-rejeu intégral de l'historique.

---

## Couverture corpus (état 2026-06-06)

- **70% de couverture** — P8 = phase très solide (14 livres canoniques disponibles localement sur ~20 recommandés)
- **5 livres Mac Studio** : Defensive Security Handbook, Adversary Emulation with MITRE ATT&CK, Intelligence-Driven Incident Response, Web Application Security, Security Chaos Engineering
- **9 New Books** : Site Reliability Engineering 2nd ed. (Google, 2026), Mastering SRE in Enterprise (2025), High Performance SRE (Mishra 2024), Data Observability for Data Engineering (2023), SLO Adoption and Usage in SRE (Google, 2023), Observability Engineering (Majors et al. 2022), The Site Reliability Workbook (Google 2018), Site Reliability Engineering (Google 2016)
- **4 Standards** : NIST CSF 2.0, NIST 800-53r5, NIST 800-61r2 (Incident Handling), NIST 800-37r2 (RMF)
- **7 Open-access** : SRE Book + SRE Workbook + OSTEP + Computer Networks + Probabilistic ML + CS229 + SLP3
- **Lacunes critiques** : 0 livre manquant bloquant. Quelques alternatives ≥ 2017 documentées dans §20 du référentiel.
- **Décision mainteneur 2026-06-06** : 70% suffit pour cadrage, batch d'acquisition ultérieur si besoin.

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :

1. **Greenfield from-scratch** : monitoring basique (1-2 dashboards), alertes minimales, on-call best-effort, post-mortems informels
2. **Maintenance legacy** : monitoring renforcé (régression visible), alertes calibrées sur baseline historique, on-call business hours, post-mortems systématiques pour P0/P1
3. **Projet interne** (équipe, gouvernance légère) : monitoring léger, alertes ciblées, on-call business hours, post-mortems internes uniquement
4. **Projet externe client** : monitoring renforcé, alertes complètes, on-call 24/7 si SLA contractuel, post-mortems partagés client si impact visible
5. **Compliance-driven** (finance, santé, défense) : monitoring 24/7 + alertes P0 sur SLO breach + audit log immutable + on-call obligatoire + post-mortems signés CISO + Council post-incident systématique pour P0/P1
6. **R&D / exploration** : monitoring best-effort, alertes minimales, on-call best-effort, post-mortems informels (apprentissage prioritaire)

---

## Points de décision utilisateur (4 décisions opérationnelles, section 5.5 grille)

> **Validation 2026-06-07** : 4 décisions opérationnelles précises (B threshold = haute valeur opérationnelle). Format AskUserQuestion (header + 2-4 options mutuellement exclusives).

### Q1 — Calibration seuils d'alerte SLO/SLI

| Header | "Seuil alerte" |
|--------|----------------|
| **Question** | "Pour [métrique X], quel seuil d'alerte calibrer ?" |
| **Options** | (a) Conservative (seuil bas, plus d'alertes, risque alert fatigue) ; (b) Balanced (seuil moyen, équilibré, recommandé par défaut) ; (c) Aggressive (seuil haut, moins d'alertes, risque incident manqué) ; (d) Custom (mainteneur précise le seuil exact) |
| **Trigger** | Drift baseline > 20% (calibration nécessaire), nouveau service déployé, post-mortem qui révèle alerte mal calibrée |
| **Impact** | Court terme réversible (re-calibration possible à tout moment). UDL 1 logge décision + rationale + baseline historique. |

### Q2 — Priorisation incidents + escalade

| Header | "Priorité + escalade" |
|--------|-----------------------|
| **Question** | "Incident [type X] : quelle sévérité et quelle escalade ?" |
| **Options** | (a) P0 critique (service down/security breach) → escalade immédiate CISO + mainteneur + on-call 24/7 + Council post-incident ; (b) P1 majeur (SLO breach) → escalade ops lead + mainteneur si non résolu en 4h ; (c) P2 modéré (perf dégradé, fonctionnalité partielle) → escalade ops si non résolu en 24h ; (d) P3 mineur (cosmétique, n'impacte pas SLA) → ticket sans escalade |
| **Trigger** | Nouveau incident, alerte déclenchée, signal détecté manuellement |
| **Impact** | Court terme réversible (re-classification possible). UDL 2 logge sévérité + escalade. |

### Q3 — Profondeur post-mortem

| Header | "Post-mortem" |
|--------|---------------|
| **Question** | "Incident [id] fermé. Quel niveau de post-mortem ?" |
| **Options** | (a) 1-page minimum (cause, timeline, action — défaut P2/P3) ; (b) Full RCA (cause root analysis détaillée, 5 whys, fishbone — défaut P1) ; (c) Full RCA + Council post-incident (CISO + DevOps-Lead + SM, 1h examen — défaut P0) ; (d) Skip (uniquement si incident < 5 min sans impact utilisateur, justification écrite) |
| **Trigger** | Incident fermé (déclenchement automatique selon sévérité) |
| **Impact** | Long terme (apprentissage organisationnel). UDL 6 logge décision + post-mortem URL. |

### Q4 — Acceptation incidents deferred (acceptable risk vs escalade P9)

| Header | "Incident deferred" |
|--------|---------------------|
| **Question** | "Incident [id] récurrent : accepter en deferred (acceptable risk) ou escalader P9 (fix code) ?" |
| **Options** | (a) Deferred court terme (workaround config, calibration alertes, re-évaluer dans 30j) ; (b) Deferred long terme (acceptable risk documenté, pas de fix prévu) ; (c) Escalade P9 prioritaire (CR formelle, impact analysis, scheduling rapide) ; (d) Escalade P9 standard (CR formelle, backlog, scheduling normal) |
| **Trigger** | Incident P2/P3 récurrent (>3 en 30j), incident P0/P1 dont l'action correctrice nécessite code |
| **Impact** | Long terme irréversible si "Deferred long terme" (acceptation dette). UDL 7 logge décision + rationale + impact business estimé. |

---

## UDL — 7 éléments P8-spécifiques

> **Validation 2026-06-07** : 7 éléments P8-spécifiques (aligné P3, P4, P5, P6, P7).

| Élément | Description | Exemple |
|---------|-------------|---------|
| **Alert threshold calibrated** | Décision Q1 user 5.5 : seuil ajusté avec baseline + rationale | "Latency p95 > 200ms → > 300ms (baseline 7j = 180ms, recommandé par observabilité Engineering Majors 2022, validé mainteneur 2026-06-15)" |
| **Incident severity + escalation** | Décision Q2 user 5.5 : sévérité assignée + escalade déclenchée | "INC-2026-0142 = P1 (SLO breach checkout), escalade ops lead (14h32) puis mainteneur (16h05, non résolu en 4h), MTTR final 5h18" |
| **Stakeholder communication** | Communication pendant incident (interne + externe) | "INC-2026-0142 : status page public mis à jour 5x (14h35, 14h50, 15h15, 15h45, 16h30), email clients enterprise envoyé 16h45 (~80 destinataires)" |
| **SLA measured** | Mesure SLO/SLI vs cible (à chaque incident + weekly) | "Uptime 30j glissants : 99.62% (cible 99.5%, marge +0.12), MTTR moyen 3.8h (cible ≤4h, marge OK), MTTF 720h (cible OK)" |
| **Capacity forecast** | Forecast capacité 1m/3m/6m + scaling recommandé | "DB connections : 65% saturation actuelle, forecast 3m = 85% (croissance +30%), scaling horizontal recommandé (+2 read replicas) ou vertical (+50% RAM)" |
| **Post-mortem completed** | Décision Q3 user 5.5 : post-mortem publié + URL + niveau | "INC-2026-0142 : full RCA + Council post-incident 2026-06-22 14h (CISO + DevOps-Lead + SM signed off), URL /post-mortems/2026-06-22-INC-0142.md, action correctrice = CR-2026-0089 (escalade P9 fix N+1 query)" |
| **Deferred / escalated to P9** | Décision Q4 user 5.5 : acceptation deferred ou escalade P9 + rationale | "INC-2026-0089 récurrent (5x en 30j) → CR-2026-0089 escalade P9 prioritaire (fix corrective N+1 query, impact estimé 8h dev + 4h test, ROI = -50% incidents P2)" |

Stockés dans `.swebok_state.db` (table `udl_p8`) et consultables via Consultation Envelope (A1) par P9 Maintenance (qui consomme les CR émises par P8).

---

## Conditions de sortie (transition vers P9 Maintenance)

> **Note phase vivante** : P8 n'a pas de "sortie" finale. La transition P9 est déclenchée par un événement (CR formelle, incident systémique, refonte planifiée). P8 reste active en parallèle pendant la maintenance P9 (monitoring continue).

Le mainteneur valide la transition avec une **checklist à 100%** (12 critères) :

- [ ] `operations-dashboard.md` existe (dashboard santé + métriques live)
- [ ] `incident-log.md` existe (log de tous les incidents)
- [ ] `performance-report.md` existe (KPI weekly/monthly)
- [ ] `security-posture-report.md` existe (CVE, patches, audits)
- [ ] `sla-compliance-report.md` existe (SLO/SLI vs cible)
- [ ] `operations-handbook.md` existe (procédures courantes)
- [ ] `post-mortem-*.md` existent (1 par incident P0/P1, 1-page min)
- [ ] `capacity-forecast.md` existe (forecast trimestriel à jour)
- [ ] `change-request-*.md` existent (CR formelles émises pour escalades P9)
- [ ] `on-call-rotation.md` existe (schedule défini)
- [ ] `audit-trail-p8.md` existe (HMAC chain vérifié)
- [ ] UDL 7 éléments loggés dans `.swebok_state.db` (table `udl_p8`)

Pas de feu vert séparé — les documents font foi.

**Trigger spécifique transition P9** : CR formelle émise (depuis post-mortem action correctrice OU capacity planning scaling code OU incident systémique).

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-07

### Mode 1 — Poisoning (Empoisonnement)

**Risque en P8** : une fausse alerte (false positive) qui déclenche un incident, ou des métriques corrompues qui faussent le diagnostic. Plus subtil : un post-mortem qui blâme la mauvaise cause root et contamine l'apprentissage organisationnel.

**Mitigations spec v2** :
1. T2 spec-compliance vs runbook (Nexus-Critic) en incident P2/P3, T1+T2+T3 en P0/P1 — casse les diagnostics hâtifs
2. Council post-incident P0/P1 (CISO + DevOps-Lead + SM) examine et valide la cause root
3. UDL 2 logge sévérité + escalade (traçabilité décision triage)
4. UDL 4 ("SLA measured") expose les métriques objectives vs perçues
5. Refus 6 (pas d'alerte silencieuse) — chaque alerte fait l'objet d'un triage
6. Audit trail HMAC chain (refus 7, secrets) — pas d'altération possible
7. Cross-incident memory (consultation L0 corpus) pour pattern matching — détecte les diagnostics récurrents douteux

**Status** : ✅ Validé (7 mécanismes)

### Mode 2 — Distraction (Distraction)

**Risque en P8** : alert fatigue (trop d'alertes mineures qui font ignorer les vraies), ou capacity planning chronophage qui détourne de la résolution d'incidents critiques. Plus subtil : le mode "monitoring courant" qui s'éternise sur des optimisations cosmétiques.

**Mitigations spec v2** :
1. Budget adaptatif par sévérité (1k/2k/3k monitoring courant, force focus minimal)
2. Refus 6 (pas d'alerte silencieuse) + critère abandon 5 (alert fatigue confirmée → escalade refonte runbook P7)
3. Q1 user 5.5 (calibration seuils) recalibrée régulièrement pour réduire false positives
4. Single-agent par défaut (mode courant), pas de fan-out multi-agent inutile
5. Compaction agressive logs entre incidents (AP3) — pas de noise persistante
6. Critère abandon 7 (35 min sans avancée sur incident → escalade)
7. Adaptativité par profil projet (compliance vs R&D) cadre le périmètre attendu

**Status** : ✅ Validé (7 mécanismes)

### Mode 3 — Confusion (Confusion)

**Risque en P8** : runbook ambigu (procédure pas claire pour un type d'incident), ou ambiguïté sur la sévérité (P1 vs P2), ou conflit d'escalade (qui décide ?). Plus subtil : nommage incohérent des incidents qui empêche le pattern matching.

**Mitigations spec v2** :
1. Q2 user 5.5 (sévérité + escalade) avec options explicites (P0/P1/P2/P3) — pas d'ambiguïté
2. Runbook P7 livré + testé (EG-8.3) — référence unique pour les procédures
3. UDL 2 ("incident severity + escalation") trace la décision et le raisonnement
4. UDL 6 ("post-mortem completed") trace le niveau de post-mortem + URL — traçabilité
5. Convention de nommage stricte (incidents `INC-YYYY-NNNN`, post-mortems `post-mortem-YYYY-MM-DD-INC-NNNN.md`)
6. T2 conformité runbook + SLA (Nexus-Critic) détecte les écarts runbook
7. Council post-incident P0/P1 examine et clarifie les ambiguïtés (CISO + DevOps-Lead + SM)

**Status** : ✅ Validé (7 mécanismes)

### Mode 4 — Clash (Conflit)

**Risque en P8** : SLO contradictoires (par exemple uptime vs perf), feature flag activé en P7 qui rentre en conflit avec une alerte calibrée en P8, ou actions correctrices contradictoires (config P8 vs code P9). Plus subtil : monitoring tools qui se contredisent (Prometheus vs Datadog).

**Mitigations spec v2** :
1. Pre-hydrate obligatoire (runbook P7 + monitoring config P7) — référence unique
2. T3 prédiction récurrence (Nexus-Critic en P0/P1) détecte les conflits cause-effet
3. UDL 7 ("deferred / escalated to P9") trace si une action correctrice nécessite code (escalade P9) ou config (P8 autonome) — pas de conflit
4. Démarcation P7/P8/P9 explicite (Setup vs Run vs Change) — pas de chevauchement décisionnel
5. Refus 4 (pas de redéfinition NFR P2) + refus 3 (pas de redéfinition monitoring setup) — pas de re-décision contradictoire
6. Critère abandon 6 (monitoring drift) — détecte les contradictions outils/alertes
7. Audit trail HMAC chain — toute action loggée, impossible de masquer un conflit

**Status** : ✅ Validé (7 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | False positive, post-mortem mauvaise cause | 7 mécanismes | ✅ |
| Distraction | Alert fatigue, capacity chronophage | 7 mécanismes | ✅ |
| Confusion | Runbook ambigu, sévérité floue, nommage | 7 mécanismes | ✅ |
| Clash | SLO contradictoires, conflits outils/actions | 7 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Pattern reproductible de P0/P2/P3/P4/P5/P6/P7 v2 étendu à P8.

---

## Adéquation aux besoins (section 7 grille comblée par projection + cohérence P0-P7 v2)

### 7.1 Usage réel projeté

Tableau 6 profils (effort en % du temps total projet — P8 est une phase **continue**, l'effort est exprimé en charge mensuelle moyenne) :

| Profil | Charge mensuelle P8 | Notes |
|--------|---------------------|-------|
| Greenfield from-scratch | 5-10% temps équipe/mois | Monitoring basique, peu d'incidents |
| Maintenance legacy | 15-25% temps équipe/mois | Monitoring renforcé, incidents récurrents legacy |
| Projet interne | 5-15% temps équipe/mois | Monitoring léger, on-call business hours |
| Projet externe client | 15-30% temps équipe/mois | Monitoring complet, SLA contractuels, on-call 24/7 si nécessaire |
| Compliance-driven | 25-40% temps équipe/mois | Monitoring 24/7, post-mortems signés, Council systématique |
| R&D / exploration | 5-15% temps équipe/mois | Monitoring best-effort, apprentissage prioritaire |

**Plage globale** : 5-40% temps équipe/mois selon profil. Plus faible que P5 (30-60% du projet en effort one-shot) et P6 (20-40%) mais **continue** (s'étale sur toute la vie du système).

### 7.2 Friction observée (projection)

4 frictions probables identifiées (projection cohérence P0/P2/P3/P4/P5/P6/P7) :

1. **F1 — Alert fatigue** : trop d'alertes → équipe ignore → vrais incidents manqués
   - **Mitigation** : Q1 user 5.5 (calibration seuils) recalibrée régulièrement, critère abandon 5 (fatigue confirmée → refonte runbook P7), AP7 recherche 2026 (pas de flood)
2. **F2 — Runbook obsolète** : runbook P7 livré mais pas tenu à jour → équipe improvise pendant incident
   - **Mitigation** : post-mortem obligatoire (refus 8) → action correctrice peut être update runbook (escalade P7 pour modification runbook livré), audit trail logge les écarts runbook (T2 spec-compliance)
3. **F3 — Capacity surprise** : saturation imprévue (saisonnalité non anticipée, viralité) → incident P0/P1
   - **Mitigation** : capacity forecast trimestriel (XG-8.6), UDL 5 ("capacity forecast") + critère échec 4 (capacity > 90% → urgence), escalade P9 si scaling code
4. **F4 — Post-mortem négligé** : équipe sous pression skip le post-mortem → apprentissage perdu, incidents récurrents
   - **Mitigation** : refus 8 (pas de skip post-mortem P0/P1), critère abandon 4 (overdue > 10j → escalade), Q3 user 5.5 (profondeur tranchée, défaut 1-page acceptable)

### 7.3 Pattern de contournement probable (projection)

4 contournements probables identifiés :

1. **C1 — Skip post-mortem informel** ("c'était évident, pas besoin de post-mortem") → mitigation refus 8 + critère abandon 4 (process broken)
2. **C2 — Hotfix sauvage** (modification config en prod en autonomie pour "résoudre vite") → mitigation refus 1 (pas de modif code) + refus 2 (pas de re-deploy) + audit trail HMAC chain (détection)
3. **C3 — Acceptation deferred silencieuse** ("on verra plus tard, c'est mineur") → mitigation Q4 user 5.5 (décision tranchée + logguée UDL 7), action de suivi
4. **C4 — Calibration arbitraire** ("je monte le seuil pour qu'on ait moins d'alertes") → mitigation Q1 user 5.5 (calibration avec baseline + rationale + recommandation observabilité), UDL 1 trace décision

### 7.4 Valeur ajoutée perçue (projection)

P8 v2 apporte 6 valeurs ajoutées vs v2-renum :
- **Démarcation P7/P8/P9 explicite** : plus d'ambiguïté sur "qui fait quoi" (Setup vs Run vs Change)
- **Mode adaptatif par sévérité** : budget et complexité proportionnels à l'urgence (pas de gaspillage en monitoring courant, pas de sous-dimensionnement en P0/P1)
- **4 décisions opérationnelles tranchées** (calibration, sévérité, post-mortem, deferred) : structure les choix au lieu d'improviser
- **UDL 7 éléments** : traçabilité complète des décisions ops (qui décide quoi, quand, pourquoi)
- **Council post-incident P0/P1** : examen pluridisciplinaire (CISO + DevOps-Lead + SM) — pas de blame culture, learning organisationnel
- **Audit trail HMAC chain** : compliance + transparence (pas d'action cachée, pas de modification rétroactive)

### 7.5 Dette d'orchestration projetée

3 risques de dette identifiés (projection) :

1. **R1 — Multi-agent surcoût en P0/P1** : si trop d'incidents P0/P1, le mode multi-agent + Council systématique peut devenir un goulot d'étranglement (overhead coordination)
   - **Mitigation** : seuil P0/P1 calibré (pas tout en P0), Council batch (1 Council par semaine pour tous les P0/P1 de la semaine si trop nombreux)
2. **R2 — Drift monitoring P7→P8** : le runbook livré P7 ne suit pas les calibrations P8 → divergence entre doc et pratique
   - **Mitigation** : refus 3 (pas de redéfinition monitoring setup P8) + escalade P7 pour mise à jour runbook officiel + UDL 1 trace calibrations
3. **R3 — Saturation post-mortems** : si beaucoup d'incidents, accumulation post-mortems non lus → apprentissage gaspillé
   - **Mitigation** : digest trimestriel des post-mortems (lecture obligatoire équipe), pattern matching cross-incident (L0 corpus), Council post-incident batch

---

## Notes de version

- **v2 (2026-06-07)** : refonte ciblée via audit (grille offline + 4 questions ciblées vague 1). Changements : (1) critère explicite de démarcation P7↔P8 ET P8↔P9 inscrit dans P8 (P7 = release + monitoring SETUP avant deploy ; P8 = monitoring CONTINU post-release + alertes + escalade + capacity planning + post-mortems ; P9 = CHANGEMENT de code planifié), (2) mécanique agent ADAPTATIVE par sévérité incident (monitoring courant = single Nexus-SM sans Critic, incident standard P2/P3 = single + Nexus-Critic T2, incident critique P0/P1 = multi-agent + Nexus-Critic T1+T2+T3 + Council post-incident), (3) Budget tokens PAR INCIDENT adaptatif (1k/2k/3k monitoring, 2k/4k/6k standard, 5k/8k/15k critique), (4) Section 5.5 transformée en 4 décisions opérationnelles précises (calibration seuils, priorisation incidents + escalade, post-mortem profondeur, acceptation deferred), (5) Section 7 comblée par projection + cohérence P0-P7 v2 (charge 5-40% temps équipe/mois, 4 frictions, 4 contournements, 6 valeurs, 3 risques dette), (6) UDL 7 éléments P8-spécifiques documentés, (7) audit des 4 failure modes Drew Breunig complet, (8) Couverture cas universelle adaptative 6 cas, (9) 15 hooks alignés P7, (10) Refus catégoriques 10 (vs 6 v2-renum), (11) Critères d'échec 4 + d'abandon 7, (12) XG-8.1-XG-8.10 (10 exit criteria, vs 6 v2-renum), (13) 11 livrables (vs 6 v2-renum, 5 ajouts : post-mortem + capacity forecast + change requests + on-call rotation + audit trail), (14) Pre-hydrate obligatoire (F7 recherche 2026), (15) Compaction par incident (AP5). 4 décisions tranchées vague 1.

- **v2-renum (2026-06-05)** : créé suite au fix structurel (renommage cascade P7→P8 après split P3). 4 activités, 6 livrables, agents en parallèle sans Nexus-Critic, 2k/4k/6k tokens, cap 35 min, 5.5 vide, pas d'UDL documenté, pas d'audit Drew Breunig, pas de démarcation P7↔P8 ni P8↔P9.

**Actions de suivi** :
- **P8-1** : `pre-tool-use/token-counter.sh` ligne 66 actuelle = `P8: 2000/4000/6000` (incident standard par défaut). Évolution nécessaire pour supporter le mode adaptatif 3-niveaux (env var `SWEBOK_P8_MODE=monitoring|standard|critical` ou flag `--severity`). En attendant, le défaut 2k/4k/6k couvre 90% des cas (incidents standards).
- **P8-2** : Mettre à jour la stratégie `audit/00-context-engineering-strategy.md` : budget P8 2k/4k/6k → budget adaptatif (1k/2k/3k monitoring, 2k/4k/6k standard, 5k/8k/15k critique), section 12.6 P8 passe de "Single" à "Adaptatif par sévérité (Single par défaut, Multi justifié pour P0/P1)".
- **P8-3** : Acquisition livres P8 manquants (alternatives ≥ 2017) : non bloquant, planifier avec P9/P10.
- **P8-4** : Council post-incident P0/P1 — formaliser le skill agent (CISO + DevOps-Lead + SM) si pas déjà fait.

Voir `audit/phase-8-operations-audit.md` pour la traçabilité des décisions.
