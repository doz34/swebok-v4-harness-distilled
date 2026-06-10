# P10 Compliance & Legal Framework (RGPD, HIPAA, PCI, SOX)

> **But** : Cadre complet des exigences compliance P10 Retirement
> **Sources** : RGPD (EU 2016/679), HIPAA (US 1996), PCI-DSS (PCI SSC 4.0), SOX (US 2002)
> **Version synthétisée** : 2026-06-09 pour SWEBOK v4 P10

## 1. Vue d'ensemble

P10 Retirement doit naviguer **4+ cadres réglementaires majeurs** selon le secteur :

| Secteur | Cadre | Pénalité max |
|---|---|---|
| **EU (toutes données personnelles)** | RGPD | 4 % CA mondial ou 20M€ |
| **Santé US** | HIPAA | $1.9M / violation |
| **Paiements** | PCI-DSS | $5K-100K / mois + perte license |
| **Finance US (coté)** | SOX | $1M + 10 ans prison |
| **Finance EU** | MiFID II / DORA | Variable |
| **Énergie US** | NERC CIP | $1M / jour |
| **Télécom** | FCC + local | Variable |

## 2. RGPD (General Data Protection Regulation)

### Articles clés pour P10
- **Art. 5(1)(e)** : Storage limitation — data ne doit pas être conservée plus longtemps que nécessaire
- **Art. 5(1)(f)** : Integrity & confidentiality — security of processing
- **Art. 17** : Right to erasure ("right to be forgotten")
- **Art. 20** : Right to data portability
- **Art. 25** : Data protection by design and by default
- **Art. 30** : Records of processing activities
- **Art. 32** : Security of processing
- **Art. 33** : Breach notification (within 72h)
- **Art. 35** : Data Protection Impact Assessment (DPIA)

### Implications P10
1. **Data inventory** : Identifier toutes les données personnelles (PII) du système
2. **Data classification** : Public / Internal / Confidential / PII
3. **Retention policy** : Définir combien de temps chaque catégorie est conservée
4. **Data subject rights** : Processus pour Art. 17 (erasure) et Art. 20 (portability)
5. **Cryptographic erasure** : Pour PII, supprimer les clés KMS = "destroy" data
6. **DPO notification** : Informer le DPO avant retirement
7. **Records update** : Mettre à jour Art. 30 records (registry of processing activities)
8. **Audit trail** : Immatriculé, signé, conservé 3 ans minimum

### Data retention par catégorie (RGPD-compliant)
| Catégorie | Retention | Justification |
|---|---|---|
| PII (identifiants, contacts) | ≤ 3 ans après dernier contact | Art. 5(1)(e) |
| Données de transaction (achats) | 10 ans | Obligations comptables |
| Logs techniques | 1 an | Sécurité |
| Logs d'audit sécurité | 3 ans | Investigation |
| Données de santé (PII sensible) | 20 ans | Médical |
| Données financières | 10 ans | SOX + MiFID |

## 3. HIPAA (Health Insurance Portability and Accountability Act)

### Règles clés pour P10
- **Privacy Rule** : Protection des PHI (Protected Health Information)
- **Security Rule** : Administrative, physical, technical safeguards
- **Breach Notification Rule** : Notification within 60 days
- **Enforcement Rule** : Pénalités $100-$50K par violation, max $1.9M/an

### Implications P10
1. **PHI inventory** : Identifier toutes les données de santé protégées
2. **Minimum necessary** : Limiter l'accès au minimum nécessaire
3. **Encryption** : PHI encrypted at rest + in transit
4. **Audit trail** : 6 ans minimum, immuable
5. **BAA termination** : Business Associate Agreements terminés avec tous les sous-traitants
6. **Risk Assessment** : HIPAA Risk Analysis obligatoire avant retirement
7. **Notification** : HHS notification si breach (60j), patients si >500 affectés
8. **Data destruction** : NIST 800-88 guidelines (clear, purge, destroy)

### HIPAA-compliant retirement checklist
- [ ] PHI inventory complete
- [ ] Encryption verified (AES-256 minimum)
- [ ] Audit trail preserved (6 years)
- [ ] Backup tapes securely destroyed
- [ ] BAA terminated with all processors
- [ ] Risk Assessment completed
- [ ] HHS notification prepared
- [ ] Patient notification mechanism in place

## 4. PCI-DSS (Payment Card Industry Data Security Standard)

### Règles clés pour P10
- **Req 3** : Protect stored cardholder data
- **Req 9** : Restrict physical access
- **Req 10** : Track and monitor all access
- **Req 11** : Test security regularly
- **Req 12** : Maintain information security policy

### Implications P10
1. **PAN (Primary Account Number) inventory** : Trouver tous les PAN stockés
2. **Tokenization ou truncation** : PAN jamais stocké en clair
3. **Card data NOT retained** : Au-delà de authorization, PAN doit être unreadable
4. **Audit trail** : 1 an minimum, 3 mois online
5. **QSA attestation** : Qualified Security Assessor sign-off si applicable
6. **Cryptographic erasure** : Supprimer les clés = data unreadable
7. **Network diagrams** : Updated post-retirement
8. **Penetration testing** : Post-retirement verification

### PCI-DSS-compliant retirement
- [ ] PAN inventory complete
- [ ] All PAN tokenized or truncated
- [ ] Cryptographic keys destroyed
- [ ] Audit trail preserved (1 year)
- [ ] QSA sign-off
- [ ] Network diagrams updated
- [ ] Penetration test report
- [ ] Compliance certificate archived

## 5. SOX (Sarbanes-Oxley Act)

### Sections clés pour P10
- **Section 302** : Corporate responsibility for financial reports
- **Section 404** : Management assessment of internal controls
- **Section 409** : Real-time issuer disclosures
- **Section 802** : Retention of audit records (7 years)

### Implications P10
1. **Audit trail preservation** : 7 years minimum, WORM (Write Once Read Many)
2. **Officer certification** : CFO + CEO certifient les controls
3. **Internal controls** : Documentation des controls IT (ITGC)
4. **Audit firm attestation** : Big 4 firms sign-off on retirement
5. **Fraud prevention** : Vérifier que personne n'a volé de data avant retirement

### SOX-compliant retirement
- [ ] Audit trail preserved (7 years, WORM)
- [ ] Officer certification obtained
- [ ] Internal controls documented
- [ ] Audit firm sign-off
- [ ] Fraud assessment completed
- [ ] Financial reports reconciled
- [ ] ITGC (IT General Controls) updated

## 6. EU sectoriels (MiFID II, DORA, NIS2)

### MiFID II (finance EU)
- **Article 16(7)** : Records of all services, activities, transactions
- **Retention** : 5-7 years minimum
- **Format** : Readable, accessible, machine-readable
- **Sanction** : Up to 10 % CA annuel

### DORA (Digital Operational Resilience Act, EU finance)
- **Article 12** : ICT risk management
- **Article 17** : ICT-related incident management
- **Article 28** : Third-party ICT risk management
- **Implication P10** : Documentation des third-party providers terminés

### NIS2 (Network and Information Security Directive 2, EU)
- **Article 21** : Cybersecurity risk management measures
- **Article 23** : Incident reporting (24h early warning, 72h notification)
- **Implication P10** : Documentation de la fin du service ICT

## 7. Process P10 unifié (Compliance-by-design)

### Phase 1: Compliance discovery (Semaine 1-2)
- Identifier tous les cadres réglementaires applicables
- Documenter les exigences spécifiques à chaque cadre
- Désigner un DPO/Compliance officer pour le projet
- Risk register initial

### Phase 2: Compliance plan (Semaine 3-4)
- Data inventory + classification (PII/PHI/PCI/SOX)
- Retention policy par catégorie
- Compliance checkpoints (où on vérifie le compliance)
- Sign-off chain (qui signe quoi)

### Phase 3: Compliance execution (Pendant migration)
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Audit trail immutable (WORM storage)
- DPIA si nécessaire (RGPD)
- Risk Assessment (HIPAA)
- QSA attestation (PCI)

### Phase 4: Compliance closure (Post-retirement)
- Sign-off final (officer certification)
- Audit trail archivé (durée légale)
- Regulator notification (si applicable)
- Compliance certificate émis
- Lessons learned (compliance)

## 8. Anti-patterns compliance P10

| Anti-pattern | Description | Mitigation |
|---|---|---|
| **"Compliance afterthought"** | RGPD/HIPAA traité à la fin | Compliance dès Pillar 1 |
| **"Data subject forgotten"** | Data subjects pas notifiés de l'erasure | Process Art. 17 RGPD |
| **"Key not destroyed"** | Clés KMS conservées après data "deleted" | Cryptographic erasure vérifié |
| **"Audit trail lost"** | Logs supprimés avec le système | Archive immutable séparée |
| **"Officer no sign-off"** | Pas de certification | Officer sign-off obligatoire |
| **"Regulator unnotified"** | Regulator pas informé | Notification process défini |

## 9. Conclusion

Le compliance P10 est un **patchwork complexe** de cadres réglementaires. La méthodologie doit :
1. Identifier **tous** les cadres applicables (pas juste RGPD)
2. Intégrer compliance **dès la planification** (pas en fin)
3. Avoir des **checkpoints** pendant l'exécution
4. Obtenir **sign-off** formel avant shutdown
5. Archiver **audit trail** pour la durée légale (5-7 ans)
6. **Notifier** les regulators si applicable
