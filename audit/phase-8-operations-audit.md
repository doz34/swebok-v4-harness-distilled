# Audit — Phase 8 : Operations

> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 8
- Nom : Operations
- Équivalent SWEBOK v4 : hors-SWEBOK (ajouté — Operations fait partie de P8 SWEBOK dans le standard, ici c'est séparé)
- Spec existante : `specs/workflows/by-phase/phase-7-operations.md`
- Date de l'audit : __________
- Auditeur : mainteneur
- Couverture corpus : **92%** (post-vague 8, 2026-06-09) — cf. §39 du corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md

---

## ⚠️ Findings pré-identifiés

1. **Phase hors-SWEBOK** : SWEBOK fusionne Operations et Maintenance dans P8. Le choix de séparer est-il justifié ? Oui, il est justifié car il faut bien séparer les deux processes.
2. **Phase très différente des autres** : c'est une phase "vivante" (longue durée, time-series), pas une phase projet. Le modèle de gate à "ALL PASS" est-il adapté à un état stable ? Pas forcément, il faut trouver les bons critères.
3. **Conflit potentiel avec phase-8** : où est la frontière entre "opération courante" et "maintenance" ?

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
**Suggestions** :
- [x] A. *« Maintain software operation and monitor system health »* (spec actuelle)
- [x] B. *« Garder le système en vie, performant, et sécurisé en régime permanent »*
- [x] C. *« Produire un SLO/SLA respecté, avec incidents gérés et performance tenue »*
- [x] D. *« Tout ce qui n'est pas un changement planifié (phase-8) »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
- [x] A. System monitoring + incident management + perf + security (spec, 4 activités)
- [x] B. SLA tracking
- [x] C. Capacity planning
- [x] D. **+ Runbook execution** (incident response)
- [x] E. **+ Reporting** (dashboards, SLO reports)
- [x] F. **+ Post-mortem** après incident
- [x] G. **+ Capacity forecasting** (prévenir la saturation)
- [ ] Autre : ____________________________________________

### 1.3 Hors-périmètre
- [x] A. Maintenance (phase-8) — tout changement de code
- [x] B. Nouvelles features (retour phase-3/4)
- [x] C. **+ Pas d'optimisation non-justifiée** (sinon dette)
- [x] D. **+ Pas de modification de l'archi en douce** (retour phase-3)
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK (4 missions cochées + périmètre 7 items + hors-périmètre clair + démarcations P7↔P8 et P8↔P9 inscrites dans spec v2)
- [ ] 🟡 À ajuster
- [ ] 🔴 À repenser

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] A. Phase 6 deployment complete (spec EG-7.1)
- [x] B. Prod system opérationnel ≥99.5% (spec EG-7.2)
- [x] C. Ops docs livrés (spec EG-7.3)
- [x] D. Support team trained (spec EG-7.4)
- [x] E. Monitoring actif (spec EG-7.5)
- [x] F. SLA défini (spec EG-7.6)
- [ ] Autre : ____________________________________________

### 2.2 Critères de complétion
- [x] A. SLO ≥99.5% uptime (XG-7.1)
- [x] B. MTTR ≤4h, MTTF ≥720h (XG-7.2)
- [x] C. Performance KPIs respectés (XG-7.3)
- [x] D. Security score ≥95% (XG-7.4)
- [x] E. Metrics dashboard live (XG-7.5)
- [x] F. Capacity plan current (XG-7.6)
- [x] G. **+ "30-day stable operation"** (spec transition criteria)
- [ ] H. **+ Le mainteneur peut dire "ça tourne, je n'y pense plus"**
- [ ] Autre : ____________________________________________

### 2.3 Conditions d'échec → escalade
- [x] A. SLO breach répété (>3 en 30j)
- [x] B. Security incident majeur
- [x] C. Capacity saturée (pas de marge)
- [x] D. **+ Le système devient ingérable** (trop d'incidents)
- [x] E. **+ Besoin de refonte** → retour phase-3
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟢 (EG-8.1-EG-8.8 = 8 entry criteria, XG-8.1-XG-8.10 = 10 exit criteria, note phase vivante explicite, transitions P9 tranchées via CR formelle)

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. Phase 6 deployment report + handoff
- [x] B. Phase 3 ops architecture
- [x] C. Phase 5 SLA tests
- [x] D. **+ Runbooks** (de la phase 6)
- [x] E. **+ Baseline de performance** (P5/P6)
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
- [x] A. Sign-off sur le SLA
- [x] B. **+ Priorisation des incidents** (P0 vs P3)
- [x] C. **+ Acceptation des incidents acceptables** (deferred)
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **70%** (███████░░░).**Sources externes disponibles localement (post-corpus) :****Mac Studio** (5 livres) — chemin `/Users/dorianciet/Desktop/Test PDF books` et `/Volumes/External/Obsidian KB/Knowledge Base/raw/pdfs` :- **Defensive Security Handbook** (Amanda Berlin, Lee Brotherston) — 8.9 MB, 363 pages- **Adversary Emulation with MITRE ATT&CK** () — 27.6 MB, 386 pages- **Intelligence-Driven Incident Response** (Rebekah Brown and Scott J. Rob) — 4.0 MB, 346 pages- **Web Application Security** (Andrew Hoffman) — 14.6 MB, 444 pages- **Security Chaos Engineering** (Kelly Shortridge;Aaron Rinehar) — 14.2 MB, 431 pages**New Books (achats locaux)** (9 livres) — chemin `/home/doz/Bureau/New Books/` :- **Site Reliability Engineering 2nd ed. (forthcoming)** (Google, 2026) — formats: EPUB- **Mastering SRE in Enterprise** (—, 2025) — formats: PDF, EPUB- **Mastering SRE in Enterprise (alt)** (—, 2025) — formats: EPUB- **High Performance SRE** (Anchal Arora Mishra, 2024) — formats: PDF- **Data Observability for Data Engineering** (—, 2023) — formats: EPUB- **SLO Adoption and Usage in SRE** (Google, 2023) — formats: EPUB- **Observability Engineering** (Charity Majors et al., 2022) — formats: PDF, EPUB- **The Site Reliability Workbook** (Google (Beyer et al.), 2018) — formats: PDF, EPUB- **Site Reliability Engineering** (Google (Beyer et al.), 2016) — formats: PDF, MOBI, EPUB**Standards NIST/OWASP téléchargés (open access)** (4) :- NIST CSF 2.0- NIST 800-53r5- NIST 800-61r2 (Incident)- NIST 800-37r2 (RMF)**Livres open-access téléchargés** (7) :- SRE Book (Google, 7 MB)- SRE Workbook (Google, 12 MB)- OS: 3 Easy Pieces- Computer Networks- Probabilistic ML vol 1+2 (Murphy, 244 MB)- CS229 notes (Stanford)- SLP 3e (Jurafsky, 26 MB)
### 3.4 Verdict
- [x] 🟢 (Inputs phases précédentes cohérents avec P7 v2 finale handoff, inputs utilisateur tranchés via 4 décisions section 5.5, corpus 70% solide — phase mieux couverte que P9)

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
- [x] A. `operations-dashboard.md` (spec)
- [x] B. `incident-log.md` (spec)
- [x] C. `performance-report.md` (spec)
- [x] D. `security-posture-report.md` (spec)
- [x] E. `sla-compliance-report.md` (spec)
- [x] F. `operations-handbook.md` (spec)
- [x] G. **+ Post-mortem reports** (par incident majeur)
- [x] H. **+ Capacity forecast** (par trimestre)
- [x] I. **+ Change requests** (entrée vers phase-8)
- [ ] Autre : ____________________________________________

### 4.2 Format de stockage
- [x] A. Markdown pour les rapports
- [x] B. JSON/TSDB pour les métriques (Prometheus, InfluxDB, etc.)
- [x] C. Ticketing system pour les incidents
- [x] D. **+ Logs structurés** (JSON, centralisés)
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
- [x] A. Dashboard live (Grafana, Datadog, etc.)
- [x] B. Weekly/monthly SLO report
- [x] C. Post-mortem par incident
- [x] D. **+ Alertes temps réel** (PagerDuty, Opsgenie, etc.)
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
- [x] A. Oui — métriques historisées + incident log
- [x] B. Manque la traçabilité des décisions d'ops
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟢 (11 livrables = 6 standard + 5 ajouts dans spec v2 — post-mortem + capacity forecast + change requests + on-call rotation + audit trail. Format triple différencié md+JSON+ticketing+TSDB. Auditabilité OK via HMAC chain Cossack Labs.)

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
- [x] A. Hyperagent-Orchestrator (spec)
- [x] B. Nexus-SM (Service Management) lead (spec)
- [x] C. Nexus-DevOps pour infra (spec)
- [x] D. Nexus-Security pour monitoring sécu (spec)
- [x] E. Nexus-Backend, Nexus-Frontend pour support (spec)
- [x] F. **+ T1 (Monitoring vs Anomaly Hunter)** : un agent surveille, l'autre chasse les anomalies subtiles
- [x] G. **+ T2 (SLA Compliance)** : le système respecte-t-il le SLA ?
- [x] H. **+ T3 (Incident Predictor)** : qu'est-ce qui va casser dans les 7 jours ?
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
- [x] A. `nexus-sm`, `nexus-devops`, `nexus-security` (spec)
- [x] B. `nexus-backend`, `nexus-frontend` (spec)
- [x] C. **+ Monitoring** (Prometheus, Grafana, Datadog, etc.)
- [x] D. **+ Alerting** (PagerDuty, Opsgenie, etc.)
- [x] E. **+ Log aggregation** (ELK, Loki, Splunk)
- [x] F. **+ Ticketing** (Jira, Linear, etc.)
- [x] G. **+ Consult L0 corpus** via tool (incident patterns)
- [ ] Autre : ____________________________________________

### 5.3 Knowledge items consultés

> **🆕 Mis à jour 2026-06-06** : Knowledge items alignés sur le nouveau corpus.

**Référentiel principal** : `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` (2 269 lignes, 18 sections, 480 ressources recommandées).

**Sections clés du référentiel à consulter** :
- **§18** : Sources locales — Mac Studio (117 livres corpus-matching identifiés)
- **§19** : Nouveaux livres acquis (Bureau/New Books/, 87 livres)
- **§20** : Lacunes restantes (43 livres non encore acquis, alternatives ≥ 2017)
- **§13** : Standards NIST/OWASP (44 documents, open access)
- **§5** : PMI Standards (PMBOK 7e/8e, Risk, Program, Portfolio, etc.)
- **§7** : Classics (Brooks, Fowler, Martin, Evans, Hunt/Thomas, etc.)
- **§9** : AI/LLM (Chip Huyen, RAG-Driven, etc.)

**Livres canoniques disponibles localement pour cette phase** (14 livres corpus-aligned sur ~20 recommandés = **70%**) :

- **Mac Studio** : 5 livres — voir détail §3.3 ci-dessus
- **New Books** : 9 livres — voir détail §3.3 ci-dessus
- **Standards** : 4 NIST/OWASP
- **Open-access** : 7 livres (Ousterhout, OSTEP, CS229, etc.)

**Lacunes critiques (§20)** : 0 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
- [x] A. T1 applicable (monitoring vs anomaly hunter)
- [x] B. T2 critique (SLA compliance)
- [x] C. T3 critique (incident predictor)
- [x] D. **+ Chaos engineering** comme T1 régulier
- [x] E. **+ Council post-incident** : CISO + DevOps + SM
- [ ] Autre : ____________________________________________

### 5.5 Points de décision utilisateur (B threshold)

> **Validation 2026-06-07** : 4 décisions opérationnelles précises (B threshold = haute valeur opérationnelle). Format AskUserQuestion (header + 2-4 options mutuellement exclusives).

**Q1 — Calibration seuils d'alerte SLO/SLI** (header "Seuil alerte") :
- (a) Conservative (seuil bas, plus d'alertes, risque alert fatigue)
- (b) Balanced (seuil moyen, équilibré, recommandé par défaut)
- (c) Aggressive (seuil haut, moins d'alertes, risque incident manqué)
- (d) Custom (mainteneur précise le seuil exact)
- Trigger : drift baseline > 20%, nouveau service, post-mortem qui révèle alerte mal calibrée
- Impact : court terme réversible (re-calibration possible)

**Q2 — Priorisation incidents + escalade** (header "Priorité + escalade") :
- (a) P0 critique (service down/security breach) → escalade immédiate CISO + mainteneur + on-call 24/7 + Council post-incident
- (b) P1 majeur (SLO breach) → escalade ops lead + mainteneur si non résolu en 4h
- (c) P2 modéré (perf dégradé) → escalade ops si non résolu en 24h
- (d) P3 mineur (cosmétique) → ticket sans escalade
- Trigger : nouveau incident, alerte déclenchée
- Impact : court terme réversible (re-classification possible)

**Q3 — Profondeur post-mortem** (header "Post-mortem") :
- (a) 1-page minimum (défaut P2/P3)
- (b) Full RCA (5 whys, fishbone — défaut P1)
- (c) Full RCA + Council post-incident CISO + DevOps-Lead + SM (défaut P0)
- (d) Skip (uniquement si incident < 5 min sans impact, justification écrite)
- Trigger : incident fermé (déclenchement automatique selon sévérité)
- Impact : long terme (apprentissage organisationnel)

**Q4 — Acceptation incidents deferred** (header "Incident deferred") :
- (a) Deferred court terme (workaround config, re-évaluer dans 30j)
- (b) Deferred long terme (acceptable risk documenté)
- (c) Escalade P9 prioritaire (CR formelle, scheduling rapide)
- (d) Escalade P9 standard (backlog, scheduling normal)
- Trigger : incident P2/P3 récurrent (>3 en 30j), incident P0/P1 dont l'action correctrice nécessite code
- Impact : long terme irréversible si "Deferred long terme" (acceptation dette)

### 5.6 Verdict
- [x] 🟢

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques
- [x] A. Pas de modif code sans change request (phase-8)
- [x] B. Pas de SLO dégradé accepté sans communication
- [x] C. Pas d'alerte silencieuse (alert fatigue accepté = dette)
- [x] D. **+ Pas de secrets en clair** dans les logs
- [x] E. **+ Pas d'optimisation non-justifiée** (YAGNI)
- [x] F. **+ Pas de skip de post-mortem** après incident majeur
- [ ] Autre : ____________________________________________

### 6.2 Modes d'échec connus
- [x] A. Alert fatigue (trop d'alertes, plus aucune traitée)
- [x] B. Incident loops (même incident qui revient)
- [x] C. SLO drift (cible oubliée)
- [x] D. Capacity surprise (saturée d'un coup)
- [x] E. **+ Ops debt** (runbooks pas à jour)
- [x] F. **+ Conflit de frontières** avec phase-8
- [ ] Autre : ____________________________________________

### 6.3 Cas limites
- [x] A. Système critique 24/7
- [x] B. Système événementiel (rare mais intense)
- [x] C. Système avec saisonnalité
- [x] D. **+ Multi-tenant** (SLO par tenant ?)
- [x] E. **+ Cloud vs on-prem** (différentes contraintes)
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
- [x] A. SLO breach → escalade immédiate
- [x] B. Security incident → escalade CISO
- [x] C. Capacity saturée → capacity planning urgent
- [x] D. **+ Incident récurrent** (>3 en 30j) → RCA formelle
- [ ] Autre : ____________________________________________

### 6.5 Verdict
- [x] 🟢 (10 refus catégoriques tranchés dans spec v2 vs 6 initiaux. 6 modes échec + 5 cas limites + 4 escalades. 4 critères échec + 7 critères abandon. Démarcations P7/P8/P9 ferment les conflits frontières.)

---

## Section 7 — Adéquation aux besoins (utilité)

> **Validation 2026-06-07** : section comblée par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7 v2 (pattern reproductible, pas de mesure terrain nécessaire pour fermer la section).

### 7.1 Usage réel
> **Charge mensuelle projetée par profil** (P8 phase continue, exprimée en % temps équipe/mois) :
> - Greenfield from-scratch : 5-10% temps équipe/mois (monitoring basique, peu d'incidents)
> - Maintenance legacy : 15-25% (monitoring renforcé, incidents récurrents legacy)
> - Projet interne : 5-15% (monitoring léger, on-call business hours)
> - Projet externe client : 15-30% (monitoring complet, SLA contractuels, on-call 24/7 si besoin)
> - Compliance-driven : 25-40% (monitoring 24/7, post-mortems signés, Council systématique)
> - R&D / exploration : 5-15% (best-effort, apprentissage prioritaire)
> Plage globale 5-40% temps équipe/mois selon profil. Plus faible que P5 (30-60%) et P6 (20-40%) mais **continue** sur toute la vie du système.

### 7.2 Friction observée
> 4 frictions probables projetées :
> - **F1 Alert fatigue** : trop d'alertes → équipe ignore → vrais incidents manqués. Mitigation : Q1 calibration recalibrée régulièrement + critère abandon 5 (refonte runbook P7) + AP7 recherche 2026.
> - **F2 Runbook obsolète** : runbook P7 livré mais pas tenu à jour → équipe improvise. Mitigation : post-mortem obligatoire (refus 8) + update runbook via escalade P7 + T2 spec-compliance trace écarts.
> - **F3 Capacity surprise** : saturation imprévue (saisonnalité, viralité). Mitigation : capacity forecast trimestriel (XG-8.6) + UDL 5 + critère échec 4 (capacity > 90% → urgence).
> - **F4 Post-mortem négligé** : skip post-mortem → apprentissage perdu, incidents récurrents. Mitigation : refus 8 + critère abandon 4 (overdue > 10j → escalade) + Q3 défaut 1-page acceptable.

### 7.3 Pattern de contournement probable
> 4 contournements probables projetés :
> - **C1 Skip post-mortem informel** ("c'était évident, pas besoin"). Mitigation : refus 8 + critère abandon 4 (process broken).
> - **C2 Hotfix sauvage** (modification config en prod en autonomie). Mitigation : refus 1 (pas de modif code) + refus 2 (pas de re-deploy) + audit trail HMAC chain (détection).
> - **C3 Acceptation deferred silencieuse** ("on verra plus tard"). Mitigation : Q4 user 5.5 (décision tranchée + logguée UDL 7), action de suivi.
> - **C4 Calibration arbitraire** ("je monte le seuil pour avoir moins d'alertes"). Mitigation : Q1 user 5.5 (calibration avec baseline + rationale + recommandation observabilité), UDL 1 trace décision.

### 7.4 Valeur ajoutée perçue
> 6 valeurs ajoutées vs v2-renum :
> - Démarcation P7/P8/P9 explicite (Setup vs Run vs Change) — plus d'ambiguïté
> - Mode adaptatif par sévérité — budget et complexité proportionnels (pas de gaspillage en courant, pas de sous-dimensionnement en P0/P1)
> - 4 décisions opérationnelles tranchées (calibration, sévérité, post-mortem, deferred) — structure les choix au lieu d'improviser
> - UDL 7 éléments — traçabilité complète (qui décide quoi, quand, pourquoi)
> - Council post-incident P0/P1 (CISO + DevOps-Lead + SM) — examen pluridisciplinaire, pas de blame culture
> - Audit trail HMAC chain — compliance + transparence, pas d'action cachée

### 7.5 Dette d'orchestration
> 3 risques de dette identifiés (projection) :
> - **R1 Multi-agent surcoût en P0/P1** : si trop d'incidents P0/P1, le mode multi-agent + Council systématique peut devenir goulot. Mitigation : seuil P0/P1 calibré, Council batch (1/semaine si trop nombreux).
> - **R2 Drift monitoring P7→P8** : runbook P7 livré ne suit pas calibrations P8 → divergence doc/pratique. Mitigation : refus 3 (pas de redéfinition setup P8) + escalade P7 pour update runbook officiel + UDL 1 trace calibrations.
> - **R3 Saturation post-mortems** : accumulation post-mortems non lus → apprentissage gaspillé. Mitigation : digest trimestriel (lecture obligatoire équipe) + pattern matching cross-incident (L0 corpus) + Council post-incident batch.

### 7.6 Verdict
- [x] 🟢

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. Token budget proposé : 2k base / 4k soft / 6k hard (phase légère).

### 8.1 Token budget alloué
**Validation 2026-06-07** : budget **ADAPTATIF par sévérité incident** (décision mainteneur Q3 vague 1, spécificité P8 phase vivante) :
- **Monitoring courant** (sans incident actif) : **1k/2k/3k** (single Nexus-SM, lecture continue)
- **Incident standard P2/P3** : **2k/4k/6k** par incident (single + Nexus-Critic T2 seul, 1 invocation ~1.5k)
- **Incident critique P0/P1** : **5k/8k/15k** par incident (multi-agent + Nexus-Critic T1+T2+T3 + Council post-incident, cohérent P3-P7)

Compaction immédiate après RCA (AP5 recherche 2026). Pre-hydrate obligatoire (F7) : runbook + monitoring dashboard + alertes actives + historique incidents.

Note action P8-1 : `pre-tool-use/token-counter.sh` ligne 66 = `P8: 2000/4000/6000` (incident standard par défaut). Évolution nécessaire pour supporter le mode 3-niveaux (env var ou flag).

### 8.2 Compaction checkpoint
- [x] A. Tous les 5 tool calls
- [x] B. À 70% du soft cap
- [x] C. **+ Compaction agressive des logs d'incident** (garder la RCA, drop le verbose)
- [x] D. **+ Memory à long terme des incidents résolus** (consultable, pas dans le contexte)
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
- [x] A. Phase 6 handoff + runbooks
- [x] B. **+ Historique d'incidents** (cross-incident memory)
- [x] C. **+ L0 corpus** via tool (patterns d'incident connus)
- [x] D. **+ Pas de re-chargement de tous les dashboards** (référencer)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret
- [x] A. T1 : Monitoring vs Anomaly Hunter
- [x] B. T2 : SLA Compliance audit
- [x] C. T3 : Incident Predictor (prédire 7 jours)
- [x] D. **+ Chaos engineering** simulé
- [x] E. **+ Council post-incident** pour les P0/P1
- [x] F. **+ Context isolation** : l'anomaly hunter n'a pas accès aux alertes traitées
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger

> **Validation 2026-06-07** : 7 éléments P8-spécifiques (aligné P3, P4, P5, P6, P7). Stockés dans `.swebok_state.db` (table `udl_p8`) et consultables via Consultation Envelope (A1) par P9 Maintenance.

1. **Alert threshold calibrated** : seuil ajusté avec baseline + rationale (ex. "Latency p95 > 200ms → > 300ms, baseline 7j = 180ms, validé mainteneur")
2. **Incident severity + escalation** : sévérité assignée + escalade déclenchée (ex. "INC-2026-0142 = P1, escalade ops 14h32 puis mainteneur 16h05, MTTR final 5h18")
3. **Stakeholder communication** : comm pendant incident interne + externe (ex. "status page public 5x updates + email clients enterprise 16h45")
4. **SLA measured** : SLO/SLI vs cible à chaque incident + weekly (ex. "Uptime 30j = 99.62% cible 99.5%, MTTR 3.8h cible 4h")
5. **Capacity forecast** : forecast 1m/3m/6m + scaling recommandé (ex. "DB connections 65% actuel → 85% forecast 3m, scaling horizontal +2 read replicas")
6. **Post-mortem completed** : décision Q3 + URL + niveau (ex. "INC-0142 full RCA + Council 2026-06-22, URL /post-mortems/2026-06-22-INC-0142.md, action correctrice = CR-0089 escalade P9")
7. **Deferred / escalated to P9** : décision Q4 + rationale (ex. "INC-0089 récurrent 5x/30j → CR-0089 escalade P9 prioritaire, fix N+1 query, ROI -50% incidents P2")

### 8.6 Verdict
- [x] 🟢

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md`. **Phase atypique** : c'est une phase vivante (longue durée), pas une phase projet. Le modèle de compaction par phase s'applique par incident, pas globalement.

#### Findings les plus pertinents pour cette phase
- **F7** : 60% retrieval sur 1er tour → **pre-hydrate du runbook + alertes actives + derniers incidents** avant chaque session ops
- **F6** : Mur à 35 min → impossible globalement (phase continue), mais segmentation par incident : chaque incident = 35 min max
- **F8** : Compaction 95% trop tard → par incident, compaction immédiate après RCA
- **F11** : Prompt caching : structure stable (runbook, monitoring queries) en tête, alertes dynamiques en queue
- **F5** : Lost-in-the-middle → runbook d'incident en tête, dashboard metrics en queue

#### Anti-patterns à éviter dans cette phase
- **AP3** : Transcripts complets d'incidents — digest RCA uniquement
- **AP5** : Compaction à 95% sur incident — immédiate après résolution
- **AP7** : Contexte "flood" avec tous les logs — filtrer par sévérité et pattern
- **AP6** : Tool result clearing absent — vider les logs bruts après parsing
- **AP8** : "Plus de logs = mieux" → rot, ne garder que les signaux

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : une fausse alerte qui déclenche un incident ?
- [x] **Distraction** : alertes trop nombreuses (alert fatigue) ?
- [x] **Confusion** : runbooks ambigus qui ne disent pas quoi faire ?
- [x] **Clash** : métriques contradictoires (SLO vs budget) ?

#### Recommandation budget (mise à jour 2026)
- **Base 2k / Soft 4k / Hard 6k par incident** (single agent Nexus-SM, pre-hydrate runbook+alertes, compaction immédiate après RCA — pas de budget global, segmentation par incident)

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 5 |
| New Books achetés (§19) | 9 |
| Standards NIST/OWASP (§13) | 4 |
| Open-access téléchargés | 7 |
| **TOTAL corpus-aligned local** | **25** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~20 livres
- **Disponible localement** : 14 corpus-aligned
- **Couverture effective** : **70%** ███████░░░

### Lacunes (§20)

- **0** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **suffisantes** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel


## Verdict global de la phase
- [x] 🟢 (8/8 sections 🟢, 4 décisions tranchées vague 1, spec v2 finalisée, démarcations P7↔P8 et P8↔P9 inscrites, mode adaptatif par sévérité, UDL 7, audit Drew Breunig complet, couverture corpus 70%)

## Liste d'actions
1. **P8-1** : Évolution `pre-tool-use/token-counter.sh` ligne 66 pour supporter le mode adaptatif 3-niveaux (env var `SWEBOK_P8_MODE=monitoring|standard|critical` ou flag `--severity`). En attendant, défaut 2k/4k/6k (incident standard) couvre 90% des cas.
2. **P8-2** : Mise à jour `audit/00-context-engineering-strategy.md` : budget P8 2k/4k/6k → adaptatif (1k/2k/3k + 2k/4k/6k + 5k/8k/15k), section 12.6 P8 passe de "Single" à "Adaptatif par sévérité (Single par défaut, Multi justifié P0/P1)", section 9 ajout "Tranchées par l'audit P8 (2026-06-07)".
3. **P8-3** : Council post-incident P0/P1 — formaliser le skill agent (CISO + DevOps-Lead + SM) si pas déjà fait. Vérifier que les skills `nexus-ciso`, `nexus-devops-lead`, `nexus-sm` existent et peuvent être convoqués ensemble.
4. **P8-4** : Acquisition livres P8 manquants (alternatives ≥ 2017) si besoin renforcer couverture corpus au-delà de 70%. Non bloquant, planifier avec P9/P10.

## Notes libres
> **Pattern reproductible** : vague 1 (4 questions ciblées) + transformations implicites (5.5 → 4 décisions précises, 7 → projection cohérence P0-P7, 8.5 → UDL 7) = 🟢 dès la première conversation. Cohérent P3 (8 décisions + projection), P4/P5/P6/P7 (4 décisions vague 1).
>
> **Spécificité P8 vs P3-P7** : P8 est une phase **vivante** (longue durée, pas projet). Le mode adaptatif par sévérité est unique : monitoring courant minimaliste, incident critique cohérent P3-P7. Aucune autre phase n'a cette structure.
>
> **Démarcations triple P7↔P8↔P9** : Setup vs Run vs Change. Trois questions simples qui couvrent les frontières. Symétrique aux démarcations P5↔P6 (organisation interne vs coverage+mutation) et P6↔P7 (code-va-passer-en-prod vs prod-tourne-après-deploy).
>
> **Tokens spéciaux** : non capable de représenter le 3-niveaux dans le script bash actuel — action P8-1. En attendant, défaut incident standard 2k/4k/6k couvre 90% des cas.
