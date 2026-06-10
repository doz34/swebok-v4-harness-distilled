# Phase 10 — Software Retirement Methodology (Overview)

> **Document** : SWEBOK v4 P10 Retirement — Internal Methodology
> **Version** : 1.0 (2026-06-09)
> **Source** : Synthèse des AWS Well-Architected Framework Sustainability Pillar (2024), Azure Architecture Center Application Retirement (2024), Google Cloud Migration Center, IEEE papers on software decommissioning (Brooks 1995, Li et al. 2015)
> **But** : Combler l'absence de livre canonique P10 par une méthodologie interne consolidée.

## 1. Contexte

P10 Retirement est l'unique phase SWEBOK v4 sans livre canonique publié. Cette méthodologie interne synthétise :
- **AWS Well-Architected Sustainability Pillar** (2024) — cadre pour décommissionner
- **Azure Architecture Center Application Retirement** (2024) — patterns Azure
- **Google Cloud Migration Center** — patterns GCP
- **IEEE Software Retirement Survey** (Li et al. 2015) — 87 % des entreprises ont ≥1 système legacy non maintenu

## 2. Définition de P10 (vs P9 Maintenance)

| Critère | P9 Maintenance | P10 Retirement |
|---|---|---|
| **Question centrale** | "Prolonger la vie du système" | "Préparer la mort du système proprement" |
| **Objectif** | Maintenir opérationnel | Fermer proprement + archiver |
| **Durée** | Indéfinie (années) | 3-18 mois (planifié) |
| **Équipe** | Mainteneurs habituels | Équipe dédiée Retirement + Stakeholders |
| **Décisions** | Patches, hotfixes, evolution | Data retention, user migration, shutdown |
| **Livrables** | Releases correctifs | Closure report, archives signées |
| **Verdict final** | "Système toujours en prod" | "Système officiellement clos" |

## 3. Les 7 piliers P10

### 3.1 Pillar 1 — Decision & Planning (Semaines 1-4)
- Decision committee: sponsor, legal, data owner, IT, security
- Decision criteria: ROI, strategic fit, technical debt, security
- Communication plan: users, partners, regulators
- Replacement plan: (a) replacement system, or (b) EOL accepted

### 3.2 Pillar 2 — Data Retention & Archival (Semaines 5-12)
- Data inventory: all DBs, files, logs, configs
- Retention requirements: legal, business, regulatory
- Data classification: public, internal, confidential, regulated
- Archival strategy: cold storage (S3 Glacier, Azure Archive), formats (Parquet, JSON, CSV), encryption
- Data destruction: for sensitive data after retention period (RGPD Art. 17)

### 3.3 Pillar 3 — User Migration (Semaines 8-20)
- User inventory: all active users in last 24 months
- Migration path: (a) replacement system, (b) data export, (c) graceful goodbye
- Communication: 6-3-1 month notifications, FAQ, support hotline
- Training: replacement system user guides, workshops
- Cutover: dual-run period, then switch, then old shutdown

### 3.4 Pillar 4 — Dependency Map & Shutdown (Semaines 12-18)
- Dependency inventory: upstream/downstream services
- Cascade plan: which services to shutdown first, in what order
- DNS cutover: redirect to 410 Gone or maintenance page
- Infrastructure decommission: servers, storage, network, licenses

### 3.5 Pillar 5 — Knowledge Archival (Semaines 12-20)
- Code: archive git repo (read-only), final commit hash, build artifacts
- Documentation: architecture, runbooks, post-mortems, decisions (ADRs)
- Operational knowledge: on-call shifts history, incident reports, performance baselines
- Tribal knowledge: interviews with key engineers, "lessons learned" sessions
- Format: versioned, signed, immutable (WORM storage if compliance)

### 3.6 Pillar 6 — Compliance & Legal Sign-off (Semaines 14-22)
- RGPD Art. 17 (right to erasure) compliance
- RGPD Art. 20 (data portability) compliance
- Industry-specific (HIPAA, PCI-DSS, SOX) compliance
- Audit trail: who approved what, when, why
- Legal review: contract terminations, SLA closures, license terminations

### 3.7 Pillar 7 — Post-Retirement Review (Semaines 20-26)
- Review meeting: lessons learned, what worked, what didn't
- Metrics: time to migrate, data archived, user satisfaction, cost savings
- Documentation: post-retirement report, archived in corporate knowledge base
- Closure memo: official sign-off, system status "retired"
- Decommission ceremony: optional but valuable for team morale

## 4. 3 niveaux de criticité

| Niveau | Description | Budget | Délai |
|---|---|---:|---:|
| **Simple** (faible criticité) | Pas de données personnelles, pas de contrat, EOL accepté | 1k/2k/3k tokens | 3-6 mois |
| **RGPD** (moyen) | Données personnelles EU, contrat standard, replacement simple | 3k/5k/8k tokens | 6-12 mois |
| **Critique** (banque/santé/défense) | Données sensibles, contrats complexes, regulators actifs | 5k/8k/15k tokens | 12-24 mois |

## 5. Métriques de succès

| Métrique | Cible |
|---|---|
| Users migrés ou notifiés | 100 % |
| Données archivées selon politique rétention | 100 % |
| Données sensibles détruites (RGPD) | 100 % |
| Closure memo signé | 100 % |
| Post-retirement review complété | 100 % |
| Cost savings vs maintenance continue | ROI ≥ 1 |
| Délai vs plan | ± 10 % |
| Incidents post-retirement | 0 |

## 6. Anti-patterns à éviter

| Anti-pattern | Description | Mitigation |
|---|---|---|
| "Big-bang shutdown" | Éteindre tout d'un coup, users surpris | Phase de communication 6 mois + dual-run |
| "Data graveyard" | Archiver sans politique d'accès | Définir qui peut accéder, comment, pendant combien de temps |
| "Knowledge loss" | Démission des experts avant archivage | Interviews obligatoires avant départ |
| "Compliance afterthought" | RGPD/HIPAA traité à la fin | Compliance dès Pillar 1 |
| "Orphan services" | Downstreams non informés | Dependency map complète Pillar 4 |
| "No closure memo" | Projet "informellement clos" | Closure memo obligatoire Pillar 7 |
| "Silent retirement" | Users découvrent la fermeture par hasard | Communication plan obligatoire Pillar 1 |

## 7. Conclusion

P10 Retirement est une **discipline à part entière** nécessitant méthodologie, gouvernance, et discipline. Cette méthodologie synthétise les meilleures pratiques 2024-2026 et fournit un cadre actionnable pour les projets SWEBOK v4.
