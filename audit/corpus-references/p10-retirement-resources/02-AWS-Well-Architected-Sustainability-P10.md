# AWS Well-Architected Framework — Sustainability Pillar (Application Retirement)

> **Source** : AWS Well-Architected Framework, Sustainability Pillar, whitepaper (2024)
> **URL** : https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html
> **Version synthétisée** : 2026-06-09 pour SWEBOK v4 P10

## 1. Les 6 design principles (Sustainability Pillar)

### Principle 1 — Understand your impact
- **P10 application** : Mesurer l'impact environnemental et financier de chaque système AVANT de décider de retirement
- **Metrics** : kWh consommés, CO2 produit, $ maintenance annuel, $ infrastructure
- **Outils AWS** : AWS Cost Explorer, AWS Carbon Footprint Tool, AWS Sustainability Insights

### Principle 2 — Establish sustainability goals
- **P10 application** : Définir des KPIs de retirement (data archived %, users migrated %, time-to-shutdown)
- **Targets** : 100% data archived, 100% users notifié, <12 mois pour retirement simple
- **Reporting** : dashboards CloudWatch, tableaux de bord stakeholders

### Principle 3 — Maximize utilization
- **P10 application** : Avant retirement, consolider les workloads sur les ressources restantes
- **Pratique** : "Harvest" des compute/storage inutilisés vers d'autres systèmes AVANT shutdown
- **Outils** : AWS Compute Optimizer, AWS Trusted Advisor

### Principle 4 — Anticipate and adopt new, more efficient offerings
- **P10 application** : Si replacement system existe, migrer vers les services cloud-native modernes
- **Pratique** : Ne pas faire de "lift and shift" vers le replacement — moderniser pendant la transition
- **Exemple** : On-prem Oracle → AWS RDS PostgreSQL (managed) au lieu de EC2 self-managed

### Principle 5 — Use managed services
- **P10 application** : Pour les services qui restent (replacement), préférer managed services
- **Pratique** : RDS au lieu de self-managed DB, Lambda au lieu de EC2, S3 au lieu de self-hosted storage
- **Bénéfice** : Réduit l'operational overhead pendant la transition P9→P10

### Principle 6 — Reduce the downstream impact of your cloud workloads
- **P10 application** : Réduire l'impact des "downstream consumers" (autres apps qui dépendent de ce système)
- **Pratique** : Documenter tous les downstreams, leur donner un replacement ou un EOL accepté
- **Communication** : 6-3-1 mois aux downstreams avant shutdown

## 2. Les 6 best practice areas (Sustainability Pillar)

### Region selection (pour data archival)
- **Recommandation** : Utiliser les régions AWS avec meilleure empreinte carbone (e.g., eu-north-1 Stockholm alimenté hydroélectricité)
- **Service** : S3 Glacier Flexible Retrieval / Deep Archive dans les régions "vertes"
- **Coût** : ~$1/TB/mois en Deep Archive

### Software and architecture (P10)
- **Patterns** : Event-driven architectures pour faciliter le decoupling avant retirement
- **Anti-patterns** : Tight coupling, distributed monolith (DISTL)
- **Refactoring** : Avant retirement, "decompose" les monolithes pour permettre un graceful shutdown

### Data management (P10 critique)
- **Stratégie** : Identifier la "data dormante" (>90 jours sans accès) → archiver
- **Format** : Parquet (columar, compressé), ORC (Hadoop), ou formats natifs
- **Storage classes S3** : S3 Standard → S3 Standard-IA → S3 Glacier Instant → S3 Glacier Flexible → S3 Glacier Deep Archive
- **Lifecycle policies** : Automatiser la transition data dormante → archival

### Hardware and services (P10)
- **EC2** : Right-size avant retirement, utiliser Spot pour les workloads restants
- **Lambda** : Préférer Lambda pour les fonctions ponctuelles pendant la transition
- **Containers (ECS/EKS)** : Right-size, supprimer les tasks idle

### Process and culture (P10)
- **Sustainable retirement** : Intégrer la sustainability dans le decision-making
- **Documentation** : Sustainability impact report avant retirement
- **Training** : Former les équipes aux "green" patterns

### Data deletion (P10 critique pour RGPD)
- **Outils** : AWS S3 Object Lock pour retention, S3 Lifecycle pour expiration, AWS Macie pour identification PII
- **Process** : Cryptographic erasure (supprimer les clés KMS), physical destruction (decommission hardware)
- **Compliance** : RGPD Art. 17, HIPAA, PCI-DSS

## 3. Service-specific P10 patterns

### S3 (storage) — retirement pattern
1. Identify all S3 buckets for the system
2. Snapshot data to Glacier (cold storage)
3. Set lifecycle policy: Glacier → Deep Archive after 90 days
4. Disable bucket access (bucket policy: deny all except audit role)
5. After retention period: delete bucket + audit log
6. Verify deletion via S3 Inventory + Macie scan

### RDS (database) — retirement pattern
1. Final snapshot of database
2. Export to Parquet on S3 Glacier (long-term archival)
3. Delete DB instance
4. Delete automated backups
5. Delete transaction logs
6. Verify via RDS console + CloudTrail

### Lambda (compute) — retirement pattern
1. Disable all triggers (EventBridge, S3 events, etc.)
2. Delete function code
3. Delete function (keeps CloudWatch logs for retention)
4. Delete CloudWatch log group after retention period

### EC2 (compute) — retirement pattern
1. Stop instance (not terminate) — preserve EBS volumes
2. Final snapshot of EBS volumes
3. Export snapshot to S3 Glacier
4. Delete EBS volumes
5. Terminate instance
6. Delete associated Elastic IPs, Security Groups, etc.

## 4. Migration patterns (P9 → P10)

### Strangler pattern
- Remplacer progressivement l'ancien système par le nouveau
- Strangler fig : nouveau système "entoure" l'ancien, prend des parts de charge
- Final step : ancien système = 0% traffic, peut être shutdown

### Parallel run
- Ancien et nouveau systèmes tournent en parallèle 1-3 mois
- Validation croisée des outputs
- Switch DNS when validated

### Big-bang cutover
- Rare, risqué, pour les cas où parallel run impossible
- Nécessite : excellent testing, excellent rollback plan, fenêtre maintenance courte

## 5. Compliance et sustainability reporting

| Report | Frequency | Audience | Tool |
|---|---|---|---|
| Sustainability impact | Per retirement | Engineering + Sustainability team | AWS Sustainability Insights |
| Cost savings | Per retirement | Finance + Management | AWS Cost Explorer |
| Data archival compliance | Per retirement | Legal + Compliance | AWS Audit Manager |
| Carbon footprint reduction | Per retirement | Sustainability team | AWS Carbon Footprint Tool |

## 6. Conclusion

AWS Well-Architected Sustainability Pillar fournit un cadre actionnable pour P10 Retirement. Les 6 design principles + 6 best practice areas + service-specific patterns couvrent tous les aspects de la méthodologie P10 : décision, data archival, user migration, dependency shutdown, knowledge archival, compliance, post-retirement review.
