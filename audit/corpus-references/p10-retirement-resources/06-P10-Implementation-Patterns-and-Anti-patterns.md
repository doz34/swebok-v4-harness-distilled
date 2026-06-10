# P10 Retirement — Implementation Patterns & Anti-patterns

> **But** : Catalogue de patterns/anti-patterns P10 basés sur Li 2015, Sneed 2010, Khan 2018, AWS, Azure, GCP
> **Version synthétisée** : 2026-06-09 pour SWEBOK v4 P10

## 1. Les 4 patterns de migration (consensus)

### Pattern 1: Big-Bang Cutover
- **Description** : Cutover complet en une seule fenêtre maintenance (typiquement week-end ou nuit)
- **Quand** : Systèmes simples, peu d'utilisateurs, données faciles à migrer
- **Durée** : 4-48 heures
- **Avantages** : Rapide, clair, "one shot"
- **Risques** : Data corruption, user impact, recovery time
- **Critique** : Khan 2018 — 88 % dépassent budget, 25 % abandonnés

### Pattern 2: Phased / Incremental
- **Description** : Decommission par sous-système, par feature, ou par data
- **Quand** : Systèmes complexes, dépendances multiples
- **Durée** : 6-18 mois
- **Avantages** : Rollback possible à chaque étape, validation continue
- **Risques** : "Partial retirement" (système reste vivant trop longtemps)
- **Sous-patterns** :
  - By feature (par feature)
  - By data (par type de data)
  - By user (par segment d'utilisateurs)
  - By geography (par région)

### Pattern 3: Strangler Fig
- **Description** : Nouveau système "absorbe" progressivement l'ancien, jusqu'à 0% traffic
- **Quand** : Replacement system existe, peut être développé en parallèle
- **Durée** : 6-12 mois
- **Avantages** : Rollback facile, transition continue
- **Patterns associés** :
  - **Anti-Corruption Layer** : intercepte les calls, redirige vers nouveau
  - **Branch by Abstraction** : abstraction qui permet switch
  - **Feature Toggles** : switch on/off de features
- **Risques** : "Long-running strangler" (jamais fini)

### Pattern 4: Parallel Run
- **Description** : Ancien et nouveau systèmes en parallèle 1-3 mois
- **Quand** : Critique, regulator présent, zero-downtime requis
- **Durée** : 1-3 mois
- **Avantages** : Validation croisée continue, zero-risk switch
- **Risques** : Coût doublé pendant la transition, divergence des données
- **Stratégie** : "Dark launch" (nouveau tourne mais ne sert pas encore), "canary" (10% traffic, puis 50%, puis 100%)

## 2. Les 7 piliers P10 — Détaillé

### Pillar 1 — Decision & Planning
- **Decision matrix** : 5 critères pondérés
  - ROI maintenance annuel (coût)
  - Valeur business (revenu, satisfaction)
  - Complexité retirement (1-10)
  - Risque compliance (1-10)
  - Risque utilisateur (1-10)
- **Decision criteria** : retirement si (complexité + risque) ≤ 2 × valeur business
- **Stakeholders** : sponsor, finance, legal, data owner, IT, security
- **Communication** : executive memo, decision rationale documenté

### Pillar 2 — Data Retention & Archival
- **Data inventory** : Toutes les DB, files, logs, configs
- **Classification** : Public, Internal, Confidential, PII
- **Retention policy** : Basée sur cadre réglementaire
- **Archival strategy** :
  - **Format** : Parquet (columar, compressé), JSON (lisible), CSV (simple)
  - **Storage** : S3 Glacier ($1/TB/mois), Azure Archive ($0.99/TB/mois), GCP Coldline ($1/TB/mois)
  - **Encryption** : AES-256 at rest, TLS 1.3 in transit
  - **Compression** : Gzip, Zstd (ratio 5-10x)
- **Data destruction** : Pour PII, après retention period
  - **Cryptographic erasure** : Supprimer les clés KMS
  - **Physical destruction** : Pour backup tapes (NIST 800-88)

### Pillar 3 — User Migration
- **User inventory** : Tous les users actifs (30j), récents (90j), dormants (>90j)
- **Migration path** :
  - (a) Replacement system : users migrent vers nouveau système
  - (b) Data export : users récupèrent leurs données et trouvent un autre système
  - (c) Graceful goodbye : users notifiés, données archivées, système fermé
- **Communication timeline** :
  - **6 mois avant** : Announcement, FAQ, support hotline
  - **3 mois avant** : Migration instructions, replacement system preview
  - **1 mois avant** : Final reminder, support hotline renforcé
  - **1 semaine avant** : Last chance
  - **Jour J** : Cutover
- **Training** : Replacement system user guides, workshops, webinars
- **Support** : Helpdesk dédié pendant 3 mois post-cutover

### Pillar 4 — Dependency Map & Shutdown
- **Dependency inventory** :
  - Upstream : Qui appelle ce système ?
  - Downstream : Qui est appelé par ce système ?
  - Scheduled jobs : Cron, Airflow, etc.
  - Manual processes : Scripts, runbooks
- **Cascade plan** :
  - Étape 1 : Désactiver les triggers upstream
  - Étape 2 : Migrer les downstreams
  - Étape 3 : Shutdown des compute
  - Étape 4 : Delete des storage
  - Étape 5 : Delete des network resources
- **DNS cutover** : Redirect to 410 Gone ou maintenance page
- **License termination** : Software, cloud, support contracts

### Pillar 5 — Knowledge Archival
- **Code** : Git repo (read-only), final commit hash, build artifacts
- **Documentation** : Architecture, runbooks, post-mortems, ADRs
- **Operational knowledge** : On-call history, incident reports, performance baselines
- **Tribal knowledge** : Interviews with key engineers (avant départ !)
- **Format** : Versioned, signed, immutable (WORM storage if compliance)
- **Storage** : Same as data archival (S3 Glacier, Azure Archive, GCP Coldline)

### Pillar 6 — Compliance & Legal Sign-off
- **Sign-off chain** : Sponsor, finance, legal, data owner, security, CISO
- **Compliance sign-off** : RGPD DPO, HIPAA Compliance Officer, PCI QSA, SOX Auditor
- **Audit trail** : Immutable, signed, archived for legal duration
- **Legal review** : Contracts terminés, SLAs fermés, licenses terminés
- **Notification** : Regulators if applicable (HHS for HIPAA, ICO for RGPD)

### Pillar 7 — Post-Retirement Review
- **Review meeting** : Lessons learned, what worked, what didn't
- **Metrics review** :
  - Time to migrate (vs plan)
  - Data archived (vs plan)
  - User satisfaction (survey)
  - Cost savings (vs budget)
  - Incidents post-retirement (count)
- **Documentation** : Post-retirement report (20-50 pages)
- **Closure memo** : Official sign-off, system status "retired"
- **Decommission ceremony** : Optional, but valuable for team morale
  - Cake
  - Retrospective
  - Knowledge transfer celebration
  - Lessons shared

## 3. Anti-patterns P10 (catalogue)

### Anti-pattern 1: Silent Retirement
- **Description** : Users découvrent la fermeture par hasard
- **Symptômes** : Tickets "site is down" sans contexte, support overwhelmed
- **Causes** : Pas de communication plan, équipe partie avant communication
- **Mitigation** : Communication 6-3-1 mois obligatoire, FAQ, support hotline

### Anti-pattern 2: Data Graveyard
- **Description** : Données archivées mais inaccessibles
- **Symptômes** : Data sujet demande ses données, personne ne sait comment les récupérer
- **Causes** : Pas d'access pattern défini, format propriétaire, encryption keys perdues
- **Mitigation** : Archival policy avec access patterns, format standard (Parquet, JSON), keys archivées

### Anti-pattern 3: Knowledge Loss
- **Description** : Experts démissionnent avant archivage, knowledge perdu
- **Symptômes** : Plus personne ne sait pourquoi décisions ont été prises, plus personne ne peut répondre aux questions
- **Causes** : Pas d'interviews, pas de documentation, pas de "exit interview" pour knowledge
- **Mitigation** : Interviews obligatoires avant départ, runbooks obligatoires, ADR pour chaque décision

### Anti-pattern 4: Compliance Afterthought
- **Description** : RGPD/HIPAA traité à la fin
- **Symptômes** : Amendes RGPD (jusqu'à 4% CA mondial), violations HIPAA
- **Causes** : Pas de DPO impliqué, pas de risk assessment
- **Mitigation** : Compliance dès Pillar 1, DPO sign-off obligatoire

### Anti-pattern 5: Orphan Services
- **Description** : Downstreams non informés, services dépendent d'un système disparu
- **Symptômes** : Services en prod qui crashent soudainement
- **Causes** : Dependency map incomplete, pas de cascade plan
- **Mitigation** : Dependency map obligatoire Pillar 4, communication 6-3-1 mois

### Anti-pattern 6: No Closure Memo
- **Description** : Projet "informellement clos", pas de trace officielle
- **Symptômes** : Confusion 2 ans après, personne ne sait si le projet est "officiellement" clos
- **Causes** : Pas de sponsor engagé, pas de post-retirement review
- **Mitigation** : Closure memo obligatoire Pillar 7, sponsor sign-off

### Anti-pattern 7: Big-Bang Cowboy
- **Description** : Cutover en une fenêtre sans dual-run, sans testing extensif
- **Symptômes** : Data corruption, user impact severe, recovery time élevé
- **Causes** : Pression management, sous-estimation complexité
- **Mitigation** : Parallel run obligatoire pour critique, Strangler pour complexe, Big-bang uniquement pour simple

### Anti-pattern 8: Decommission Deconstructor
- **Description** : Pas de plan, pas de sponsor, pas de budget
- **Symptômes** : Projet abandonné en cours de route (25% des cas Khan 2018)
- **Causes** : Pas d'executive sponsorship, pas de dedicated team
- **Mitigation** : Sponsor obligatoire, dedicated team (pas兼任), budget 30% buffer

## 4. Checklist P10 — 100 critères de succès

### Pre-retirement (15 critères)
- [ ] Business case approved
- [ ] Decision matrix documented
- [ ] Stakeholders identified
- [ ] Replacement system ready OR EOL accepted
- [ ] Data inventory complete
- [ ] User inventory complete
- [ ] Dependency map complete
- [ ] Legal/compliance requirements documented
- [ ] Communication plan ready
- [ ] Risk register created
- [ ] Budget approved (with 30% buffer)
- [ ] Timeline approved (with 30% buffer)
- [ ] Executive sponsor identified
- [ ] Dedicated team identified
- [ ] Compliance officer (DPO) involved

### User migration (10 critères)
- [ ] Users notified 6 months before
- [ ] Users notified 3 months before
- [ ] Users notified 1 month before
- [ ] Users notified 1 week before
- [ ] Replacement system documentation available
- [ ] User training completed
- [ ] Cutover executed
- [ ] Old system in read-only mode
- [ ] Support hotline available
- [ ] User satisfaction survey sent

### Data archival (15 critères)
- [ ] All data classified
- [ ] Retention policy applied
- [ ] Data encrypted at rest
- [ ] Data encrypted in transit
- [ ] Data moved to archival storage
- [ ] Cryptographic erasure tested
- [ ] Data subject requests processed
- [ ] Audit log immutable
- [ ] Backup tapes destroyed
- [ ] KMS keys archived or destroyed
- [ ] DPO sign-off
- [ ] Compliance officer sign-off
- [ ] Legal sign-off
- [ ] Audit trail preserved
- [ ] Regulator notified (if applicable)

### System decommission (15 critères)
- [ ] DNS redirected
- [ ] Infrastructure deallocated
- [ ] Backups deleted (after retention)
- [ ] Licenses terminated
- [ ] Service principals disabled
- [ ] CloudTrail logs preserved
- [ ] Cost monitoring shows $0
- [ ] No production traffic
- [ ] No scheduled jobs
- [ ] No alerts fired
- [ ] All dependencies migrated
- [ ] All downstreams informed
- [ ] Replacement system validated
- [ ] Rollback plan tested
- [ ] Cutover team disbanded

### Closure (15 critères)
- [ ] Knowledge archived
- [ ] Code archived (git read-only)
- [ ] Documentation archived
- [ ] Runbooks archived
- [ ] Post-mortems archived
- [ ] Interviews conducted
- [ ] Lessons learned documented
- [ ] Closure memo signed
- [ ] Project officially closed
- [ ] Cost savings reported
- [ ] Carbon footprint reduction reported
- [ ] Compliance audit completed
- [ ] Sponsor sign-off
- [ ] Decommission ceremony held
- [ ] Final status: "retired"

### Post-retirement (15 critères)
- [ ] No production traffic after 30 days
- [ ] No new incidents
- [ ] Cost savings verified
- [ ] User satisfaction survey received
- [ ] Lessons learned shared with organization
- [ ] Post-retirement report distributed
- [ ] Best practices documented
- [ ] Anti-patterns documented
- [ ] Recommendations for future retirements
- [ ] Templates updated
- [ ] Training updated
- [ ] Architecture patterns updated
- [ ] Compliance patterns updated
- [ ] Cost model updated
- [ ] Risk model updated

## 5. Conclusion

P10 Retirement nécessite :
- **Méthodologie** : 7 piliers, 4 patterns, 3 niveaux
- **Compliance** : 4+ cadres réglementaires (RGPD, HIPAA, PCI, SOX)
- **Discipline** : Pas de big-bang cowboy, communication obligatoire, archival obligatoire
- **Gouvernance** : Sponsor, dedicated team, post-retirement review

**C'est un marathon, pas un sprint**.
