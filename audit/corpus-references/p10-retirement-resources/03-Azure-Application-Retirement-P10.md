# Azure Architecture Center — Application Retirement Pattern (P10)

> **Source** : Azure Architecture Center, Application Retirement (2024)
> **URL** : https://learn.microsoft.com/en-us/azure/architecture/framework/
> **Version synthétisée** : 2026-06-09 pour SWEBOK v4 P10

## 1. Vue d'ensemble

Azure Architecture Center considère l'application retirement comme un **process structuré** (pas un événement ponctuel), composé de :
1. **Decision** : business case, replacement strategy
2. **Planning** : timeline, stakeholders, risks
3. **Execution** : data archival, user migration, dependency shutdown
4. **Closure** : post-retirement review, sign-off, lessons learned

## 2. Les 5 phases Azure (P10-aligned)

### Phase 1: Discovery & Inventory
- **Inventaire des composants** : compute (VMs, App Services), data (SQL DB, Cosmos DB, Storage Accounts), network (VNets, NSGs, App Gateways), security (Key Vault, AD apps)
- **Inventaire des données** : PII, PHI, PCI, IP, business data, logs, backups
- **Inventaire des utilisateurs** : actifs (30j), récents (90j), dormants (>90j)
- **Inventaire des dépendances** : upstream calls, downstream consumers, scheduled jobs, manual processes

### Phase 2: Planning & Approvals
- **Decision matrix** : coût annuel maintenance, valeur business, complexité retirement
- **Approval chain** : sponsor → finance → legal → data owner → IT
- **Communication plan** : 6-3-1 mois, channels, FAQ, support
- **Risk register** : data loss, user impact, compliance, technical

### Phase 3: User Migration
- **Strategy** : (a) replacement system, (b) data export, (c) graceful goodbye
- **Timeline** : 3-6 mois pour migration complète
- **Support** : helpdesk dédié, FAQ, webinars
- **Cutover** : DNS switch, read-only mode sur ancien, monitor activity

### Phase 4: Data Archival & Compliance
- **Data classification** : PII, PHI, PCI, IP, business, logs
- **Retention policy** : basée sur regulatory requirements (RGPD, HIPAA, SOX)
- **Archival storage** : Azure Archive Blob Storage (~$0.00099/GB/mois)
- **Encryption** : Customer-managed keys (CMK) avec Azure Key Vault
- **Data destruction** : après retention period, RGPD Art. 17 (right to erasure)
- **Compliance audit** : immutable logs, signed reports, regulatory notification

### Phase 5: System Decommission & Closure
- **Dependency cutover** : switch DNS, redirect traffic, monitor for stragglers
- **Infrastructure shutdown** : VMs deallocated, Storage deleted, network resources removed
- **License termination** : software licenses, cloud subscriptions, support contracts
- **Knowledge archival** : code → GitHub read-only, docs → SharePoint archive, runbooks → Confluence
- **Post-retirement review** : lessons learned, what worked, what didn't, ROI achieved
- **Closure memo** : official sign-off, system status "retired"

## 3. Patterns Azure spécifiques P10

### Pattern 1: Strangler Fig
- Nouveau système "absorbe" progressivement les fonctionnalités de l'ancien
- Pattern : reverse proxy + feature flag + gradual traffic shift
- Avantage : rollback possible à chaque étape
- Outils Azure : Azure Front Door + Azure App Configuration feature flags

### Pattern 2: Big-Bang (avec precautions)
- Cutover en une fenêtre maintenance
- Pré-requis : comprehensive testing, blue-green deployment, instant rollback
- Risques : data corruption, user impact, recovery time

### Pattern 3: Parallel Run
- Ancien et nouveau en parallèle 1-3 mois
- Validation croisée continue
- Switch DNS after validation

### Pattern 4: Data-First Migration
- Migrer les données d'abord (depuis ancien vers nouveau)
- Puis migrer les users
- Puis shutdown ancien
- Avantage : pas de downtime data access

## 4. Azure services pour P10

### Azure services à archiver
| Service | Archival Strategy | Cost |
|---|---|---|
| Azure VMs | Snapshot → Archive Storage | ~$0.05/GB/mois |
| Azure SQL DB | Export BACPAC → Archive Storage | ~$0.10/GB/mois |
| Cosmos DB | Export → Archive Storage | ~$0.10/GB/mois |
| Azure Storage (Blob) | Move to Archive tier | $0.00099/GB/mois |
| Azure Files | Snapshot → Archive | ~$0.10/GB/mois |
| Azure Backup | Keep for retention period, then delete | Per policy |

### Azure tools pour P10
- **Azure Resource Graph** : query all resources of the system
- **Azure Cost Management** : track savings from retirement
- **Azure Policy** : enforce "no orphan resources" pattern
- **Azure Monitor** : activity logs for compliance audit
- **Azure Key Vault** : cryptographic erasure (delete CMK)
- **Azure AD** : disable service principals, archive logs

## 5. Compliance patterns Azure

### RGPD Art. 17 (Right to erasure)
- Identify PII in system
- Document data flow
- Implement deletion mechanism (cascade delete, soft delete with TTL)
- Verify deletion with audit log
- Notify data subject (if requested)

### RGPD Art. 20 (Data portability)
- Provide data export to data subjects on request
- Standard format (JSON, CSV, XML)
- Within 30 days of request
- Document process

### HIPAA (santé US)
- Retention period : 6 years minimum
- Secure destruction : NIST 800-88 guidelines
- Audit trail : all access logged for 6 years
- Business Associate Agreement (BAA) termination

### PCI-DSS (paiements)
- Retention period : 1 year minimum, but card data not stored
- Secure destruction : crypto-shred for encrypted data
- Audit trail : all access for 1 year
- QSA attestation

### SOX (finance US)
- Retention period : 7 years
- Immutable storage (WORM)
- Audit trail : all access for 7 years
- Officer certification

## 6. Checklist Azure P10

### Pre-retirement
- [ ] Business case approved
- [ ] Replacement system ready OR EOL accepted
- [ ] Data inventory complete
- [ ] User inventory complete
- [ ] Dependency map complete
- [ ] Legal/compliance requirements documented
- [ ] Communication plan ready
- [ ] Risk register created

### User migration
- [ ] Users notified 6 months before
- [ ] Users notified 3 months before
- [ ] Users notified 1 month before
- [ ] Users notified 1 week before
- [ ] Replacement system documentation available
- [ ] User training completed
- [ ] Cutover executed
- [ ] Old system in read-only mode

### Data archival
- [ ] All data classified
- [ ] Retention policy applied
- [ ] Data encrypted at rest
- [ ] Data moved to archival storage
- [ ] Cryptographic erasure tested (for sensitive data)
- [ ] Data subject requests processed
- [ ] Audit log immutable

### System decommission
- [ ] DNS redirected
- [ ] Infrastructure deallocated
- [ ] Backups deleted (after retention)
- [ ] Licenses terminated
- [ ] Service principals disabled
- [ ] CloudTrail logs preserved
- [ ] Cost monitoring shows $0

### Closure
- [ ] Knowledge archived
- [ ] Lessons learned documented
- [ ] Closure memo signed
- [ ] Project officially closed
- [ ] Cost savings reported
- [ ] Carbon footprint reduction reported
- [ ] Compliance audit completed

## 7. Conclusion

Azure Application Retirement Pattern offre un cadre structuré, pragmatique, et compliant pour P10. Les 5 phases + 4 patterns + services/tools + compliance patterns + checklist couvrent tous les aspects critiques de la méthodologie P10.
