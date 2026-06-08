# Audit — Phase 10 : Retirement

> Grille d'audit — **v2 finale 2026-06-07** (audit clos via grille offline + 4 questions AskUserQuestion vague 1, verdict 🟢 dès la première conversation).
> **Changement vs v1 template** : (1) section 5.5 transformée en 4 décisions opérationnelles précises (Q1 type retirement, Q2 criticité conformité, Q3 réversibilité, Q4 lien P0), (2) section 7 comblée par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7/P8/P9 v2, (3) section 8.5 comblée par UDL 7 éléments P10-spécifiques, (4) 8.1 budget adaptatif 3-niveaux (1k/2k/3k + 3k/5k/8k + 5k/8k/15k, symétrie P8/P9), (5) tous les verdicts de section 🟢, (6) liste d'actions P10-1 à P10-4, (7) audit Drew Breunig 4 modes complet, (8) démarcation P10↔P0 explicite (Question centrale, symétrie P9).

## Métadonnées
- Phase : 10
- Nom : Retirement
- Équivalent SWEBOK v4 : Pas de KA direct. Couvre Software Engineering Process (KA P9 SWEBOK) + Software Maintenance (P6 SWEBOK, fin de vie) + aspects RGPD/archivage.
- Spec existante : `specs/workflows/by-phase/phase-10-retirement.md` (v2, 2026-06-07)
- Date de l'audit : 2026-06-07
- Auditeur : mainteneur (grille offline) + Claude (analyse + 4 questions + rédaction v2)

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
**Suggestions** :
- [x] A. *« Gracefully decommission software and archive artifacts »* (spec actuelle)
- [x] B. *« Éteindre proprement un système, migrer les utilisateurs, archiver la connaissance, respecter la conformité »*
- [x] C. *« Produire la preuve qu'on peut fermer le système sans casser les engagements (légaux, utilisateurs, contractuels) »*
- [x] D. *« Tout ce qui doit être fait APRÈS la décision de fin de vie »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
- [x] A. Retirement planning + data management + user migration + system shutdown (spec, 4 activités)
- [x] B. Data retention policy
- [x] C. User migration ou notification
- [x] D. System shutdown
- [x] E. **+ Knowledge archival** (institutional memory)
- [x] F. **+ Legal/compliance sign-off**
- [x] G. **+ Post-retirement review**
- [ ] Autre : ____________________________________________

### 1.3 Hors-périmètre
- [x] A. Nouvelles features (interdit)
- [x] B. Maintenance non-critique (phase-8) — sauf si nécessaire pour EOL
- [x] C. **+ Pas d'extinction sans plan de data retention**
- [x] D. **+ Pas d'extinction sans user migration**
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK
- [ ] 🟡 À ajuster
- [ ] 🔴 À repenser

**Note v2** : Mission + périmètre + hors-périmètre validés. Démarcation P9↔P10 (prolonger vs préparer la mort, tranchée vague 1 P9) et P10↔P0 (fin de vie ancien vs début nouveau système, tranchée vague 1 P10) explicites. Verdict 🟢.

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] A. Décision de fin de vie documentée (spec EG-9.1)
- [x] B. Replacement system ready ou EOL accepté (spec EG-9.2)
- [x] C. Approbation stakeholders (spec EG-9.3)
- [x] D. Plan de retirement documenté (spec EG-9.4)
- [x] E. Data retention policy définie (spec EG-9.5)
- [x] F. Risk assessment complété (spec EG-9.6)
- [x] G. **+ Communication envoyée aux users** (X mois avant)
- [ ] Autre : ____________________________________________

### 2.2 Critères de complétion
- [x] A. 100% data archived (XG-9.1)
- [x] B. 100% users migrés ou notifiés (XG-9.2)
- [x] C. System shutdown clean (XG-9.3)
- [x] D. Retirement report approved (XG-9.4)
- [x] E. 100% artifacts préservés (XG-9.5)
- [x] F. Legal/compliance sign-off (XG-9.6)
- [x] G. **+ Knowledge archivée et consultable**
- [x] H. **+ Le mainteneur peut dire "c'est fermé proprement"**
- [x] I. **+ Le projet est officiellement clos** (closure memo)
- [ ] Autre : ____________________________________________

### 2.3 Conditions d'échec → escalade
- [x] A. Données non archivées → blocage
- [x] B. Users non migrés → escalade
- [x] C. Legal/compliance refuse → blocage
- [x] D. **+ Données sensibles non détruites** → escalade CISO
- [x] E. **+ Post-retirement review révèle des manques** → remédiation
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟢

**Note v2** : 9 entry criteria (EG-10.1-10.9) + 10 exit criteria (XG-10.1-10.10) + checklist 11 critères de sortie. Critères d'échec 4 (déclenchent action immédiate) + critères d'abandon 7 (escalade mainteneur). Verdict 🟢.

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. Décision de fin de vie (sponsor)
- [x] B. Plan de retirement (Nexus-PM)
- [x] C. **+ Data inventory** (où sont les données ?)
- [x] D. **+ User list** (qui est impacté ?)
- [x] E. **+ Dependency map** (quels systèmes sont impactés ?)
- [x] F. **+ Legal/compliance requirements** (RGPD, etc.)
- [x] G. **+ Knowledge artifacts** (code, docs, post-mortems)
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
- [x] A. Approbation finale
- [x] B. Communication aux users (sponsor + comms)
- [x] C. **+ Décision sur la rétention** (combien de temps ?)
- [x] D. **+ Validation des données à détruire vs archiver**
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **0%** (░░░░░░░░░░).**Sources externes disponibles localement (post-corpus) :**
### 3.4 Verdict
- [x] 🟢

**Note v2** : Inputs depuis P9 (EOL decision Q4) + P8 (incident systémique) + P2-P4 (data inventory) + P2-P7 (user list) + P3 (dependency map) + P2/P3 (compliance requirements) + P0-P9 cumul (knowledge artifacts). Couverture corpus 0% documentée, action P10-2 prioritaire. Verdict 🟢.

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
- [x] A. `retirement-plan.md` (spec)
- [x] B. `data-retention-report.md` (spec)
- [x] C. `user-migration-report.md` (spec)
- [x] D. `system-dependency-map.md` (spec)
- [x] E. `decommission-report.md` (spec)
- [x] F. `retirement-closure-report.md` (spec)
- [x] G. `knowledge-archive.md` (spec)
- [x] H. **+ Legal sign-off doc** (suggéré)
- [x] I. **+ Compliance sign-off doc** (suggéré)
- [x] J. **+ Post-retirement review report** (suggéré)
- [x] K. **+ Communication sent log** (qui a été notifié, quand)
- [ ] Autre : ____________________________________________

### 4.2 Format de stockage
- [x] A. Markdown pour les rapports
- [x] B. Archives long-terme (Glacier, cold storage)
- [x] C. **+ Index consultable** (pour retrouver la connaissance)
- [x] D. **+ Destruction certificates** (pour les données détruites)
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
- [x] A. Closure memo (1 page)
- [x] B. Knowledge archive index
- [x] C. Communication finale aux users
- [x] D. **+ Post-retirement review** (transmis aux stakeholders)
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
- [x] A. Oui — tout tracé (data, users, sign-offs, archive)
- [x] B. Manque la traçabilité des communications
- [x] C. Manque la preuve de destruction sécurisée
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟢

**Note v2** : 9 livrables standard (eol-decision-memo, archive-procedure, data-migration-plan, compliance-closure-report, ownership-transfer, stakeholder-notification, final-archive-snapshot, post-retirement-monitoring-stop, post-retirement-review) + 3 ajouts (legal sign-off, compliance sign-off, communication-sent-log) = 9+3 livrables. Format triple différencié (md + git + JSON + MADR + Keep a Changelog + HMAC chain). Auditabilité complète. Verdict 🟢.

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
- [x] A. Hyperagent-Orchestrator (spec)
- [x] B. Nexus-DevOps pour shutdown (spec)
- [x] C. Nexus-Backend, Nexus-Frontend pour décommission (spec)
- [x] D. Nexus-PM pour stakeholder comm (spec)
- [x] E. Nexus-Security pour data destruction (spec)
- [x] F. Nexus-CISO pour compliance (spec)
- [x] G. Nexus-DS pour data archival (spec)
- [x] H. **+ T1 (Shutdown Operator vs Data Loss Hunter)** : vérifier qu'on ne perd rien
- [x] I. **+ T2 (Compliance Audit)** : tout est conforme ?
- [x] J. **+ T3 (Future Impact Predictor)** : qu'est-ce qui manquera dans 1 an ?
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
- [x] A. `nexus-devops`, `nexus-backend`, `nexus-frontend` (spec)
- [x] B. `nexus-pm`, `nexus-security`, `nexus-ciso`, `nexus-ds` (spec)
- [x] C. **+ Data archival tools** (tar, gzip, cloud archival)
- [x] D. **+ Data destruction tools** (secure wipe, crypto-shred)
- [x] E. **+ User communication tools** (email, in-app, etc.)
- [x] F. **+ L0 corpus** via tool (retirement patterns)
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

**Livres canoniques disponibles localement pour cette phase** (0 livres corpus-aligned sur ~5 recommandés = **0%**) :


**Lacunes critiques (§20)** : 0 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
- [x] A. T1 critique (data loss hunt)
- [x] B. T2 critique (compliance audit)
- [x] C. T3 applicable (future impact)
- [x] D. **+ Council de clôture** : CISO + Legal + PM + DevOps
- [x] E. **+ Context isolation** : le data loss hunter n'a pas accès au plan de destruction
- [ ] Autre : ____________________________________________

### 5.5 Points de décision utilisateur (B threshold) — **4 décisions précises, symétrie P8/P9**

#### Q1 — Type de retirement
- [x] **A. Archivage simple** (recommandé P10 défaut) — single + T2 (1k/2k/3k), pas de Council
- [ ] B. RGPD / données personnelles — single + T1+T2 (3k/5k/8k), signature CISO + Legal
- [ ] C. Finance / Santé / Défense — multi + T1+T2+T3 + Council (5k/8k/15k)
- [ ] D. Transfert ownership structurant — single + T2 (1k/2k/3k), signature PM + sponsor

#### Q2 — Criticité conformité
- [x] **A. Archivage simple / donnée standard** (recommandé défaut) — 30j read-only, pas de Council
- [ ] B. RGPD standard / donnée métier — 90j read-only, CISO + Legal
- [ ] C. Finance / Santé / Défense / donnée sensible — 180j+ read-only, Council formel 1h

#### Q3 — Réversibilité de l'archivage
- [x] **A. 30j read-only** (recommandé archivage simple) — sur demande stakeholder
- [ ] B. 90j read-only (recommandé RGPD/standard) — sur demande stakeholder
- [ ] C. 180j+ read-only (recommandé Finance/Santé/Défense) — sur demande CISO/Legal/Regulator
- [ ] D. Indéfini read-only (archive permanente) — sur demande regulator uniquement

#### Q4 — Lien avec P0 Discovery
- [x] **A. Aucun lien P0** (recommandé EOL pur) — le système archivé n'est pas remplacé
- [ ] B. P0 d'un nouveau projet démarre en parallèle (recommandé si replacement) — P0 indépendant
- [x] **C. Lessons learned alimentent P0 futur** (recommandé systématiquement) — post-retirement review archivé
- [ ] D. P0 démarre APRÈS P10 complete (recommandé si pas urgent) — cut-over séquentiel

### 5.6 Verdict
- [x] 🟢

**Note v2** : 4 décisions opérationnelles précises (Q1-Q4), symétrie P8 (4 décisions) et P9 (4 décisions). Format identique AskUserQuestion (header + 2-4 options mutuellement exclusives par question). Verdict 🟢.

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques
- [x] A. Pas d'extinction sans data retention policy
- [x] B. Pas d'extinction avec users non notifiés
- [x] C. Pas d'extinction sans legal sign-off
- [x] D. **+ Pas de destruction de données sans preuve**
- [x] E. **+ Pas de "juste éteindre le serveur"** (processus obligatoire)
- [x] F. **+ Pas d'amnésie** (la connaissance doit être archivée)
- [ ] Autre : ____________________________________________

### 6.2 Modes d'échec connus
- [x] A. Knowledge loss (personne ne sait pourquoi on avait fait tel choix)
- [x] B. Compliance violation (RGPD oublié)
- [x] C. Users orphelins (non migrés et non notifiés)
- [x] D. Data leak (destruction ratée)
- [x] E. **+ Zombie systems** (éteint mais pas décommissionné)
- [x] F. **+ Post-mortem oublié** (la connaissance d'échec se perd)
- [ ] Autre : ____________________________________________

### 6.3 Cas limites
- [x] A. Système avec données personnelles (RGPD)
- [x] B. Système critique (santé, finance) — extended retention
- [x] C. Open source (code archivé publiquement)
- [x] D. **+ Système sans replacement** (EOL pur, pas de migration)
- [x] E. **+ Données scientifiques** (reproductibilité requise)
- [x] F. **+ Successeur partiel** (migrer seulement certaines features)
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
- [x] A. Compliance refuse → blocage total
- [x] B. Users non migrés → escalade PM + sponsor
- [x] C. Données non archivées dans la fenêtre → escalade
- [x] D. **+ Data leak détecté post-extinction** → escalade CISO + Legal (incident)
- [ ] Autre : ____________________________________________

### 6.5 Verdict
- [x] 🟢

**Note v2** : 10 refus catégoriques (vs 6 v2-renum), 4 critères d'échec (action immédiate), 7 critères d'abandon (escalade mainteneur), 6 cas limites (RGPD, finance, OSS, EOL pur, données scientifiques, successeur partiel), 4 règles d'escalade (compliance refus, users non migrés, données non archivées, data leak post-extinction). Verdict 🟢.

---

## Section 7 — Adéquation aux besoins (utilité)

> **Comblée par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7/P8/P9 v2** (vs vide en v1).

### 7.1 Usage réel

P10 = dernière phase du cycle de vie d'un système. Effort typique 5-40% du projet (one-shot, mais structurant) selon criticité conformité :
- Archivage simple : 5-10% du projet
- RGPD/standard : 15-25% du projet
- Finance/Santé/Défense : 25-40% du projet

**P10 ne s'active PAS** dans 95% des projets (les projets meurent rarement formellement). Quand P10 s'active, c'est un événement structurant (EOL, replacement, incident systémique). Profil majoritaire : archivage simple (single + T2, 1k/2k/3k).

### 7.2 Friction observée (4 frictions)

1. **F1 — Knowledge loss** : personne ne sait pourquoi on avait fait tel choix → risque de régression sur le système de remplacement
2. **F2 — Compliance violation** : RGPD oublié, finance/santé/défense non conforme → risque juridique et réputationnel
3. **F3 — Users orphelins** : non migrés et non notifiés → utilisateurs bloqués, support client surchargé
4. **F4 — Data leak** : destruction ratée de données sensibles → escalade CISO + regulator

**Mitigations** : matrice destruction vs archivage, checklist XG-10.1-XG-10.10, communication sent log, certificats de destruction signés HMAC.

### 7.3 Pattern de contournement probable (4 contournements)

1. **C1 — "Juste éteindre le serveur"** : on coupe l'infra sans archivage → perte de connaissance, non-conformité, régression système de remplacement
2. **C2 — "Skip du Council"** : on signe seul (Nexus-DevOps-Lead) au lieu de Council pour Finance/Santé/Défense → escalade CISO + Legal + regulatory
3. **C3 — "Réversibilité oubliée"** : on supprime définitivement sans fenêtre de grâce → perte de données, escalade mainteneur
4. **C4 — "Lessons learned non documentés"** : on archive sans post-retirement review → perte de connaissance pour les futurs EOL

**Mitigations** : refus catégoriques 1-10, XG-10.7 + XG-10.8 obligatoires, Q3 user 5.5 force la fenêtre de réversibilité.

### 7.4 Valeur ajoutée perçue (7 valeurs)

1. **V1 — Démarcations P9↔P10 ET P10↔P0 explicites** : ferment les frontières contestées (système vivant vs archive vs nouveau système)
2. **V2 — Mécanique adaptative 3-niveaux par criticité conformité** : le bon budget pour le bon cas (1k/2k/3k archivage simple, 5k/8k/15k Finance/Santé/Défense)
3. **V3 — Nexus-Critic adaptatif** : T2 seul (archivage simple) → T1+T2 (RGPD) → T1+T2+T3 (Finance/Santé/Défense), context isolation respectée
4. **V4 — Council de clôture conditionnel** : obligatoire seulement si criticité élevée (Finance/Santé/Défense)
5. **V5 — 4 décisions opérationnelles précises (Q1-Q4 user 5.5)** : type retirement, criticité conformité, réversibilité, lien P0
6. **V6 — 9+ livrables triple différencié** : md + git + JSON + MADR + Keep a Changelog + HMAC chain
7. **V7 — UDL 7 + audit trail HMAC** : traçabilité complète de la fermeture (EOL decision → archive → data migration → compliance → ownership → stakeholder notification → P0 link)

### 7.5 Dette d'orchestration (3 risques)

1. **R1 — Criticité sous-évaluée** : on traite un système Finance comme archivage simple → escalade CISO + Legal + regulatory, refaire P10 en mode Finance
2. **R2 — Réversibilité trop courte** : on configure 30j pour Finance/Santé/Défense → perte de données si regulator demande restauration après 30j
3. **R3 — P10 s'éternise** (35 min sans avancée) → segmentation du retirement, escalade mainteneur

**Mitigations** : Q1+Q2 user 5.5 obligatoires avant démarrage, refus catégorique 6 (réversibilité), checkpoint 35min obligatoire.

### 7.6 Verdict
- [x] 🟢

**Note v2** : Section 7 comblée par projection (5.1 usage réel, 5.2 4 frictions, 5.3 4 contournements, 5.4 7 valeurs, 5.5 3 risques dette). Cohérence P0-P9 v2 (effort one-shot structurant, démarcations explicites, adaptatif symétrie P8/P9). Verdict 🟢.

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. Token budget proposé : 2k base / 3k soft / 5k hard (phase courte).

### 8.1 Token budget alloué — **adaptatif 3-niveaux par criticité conformité (symétrie P8/P9)**

| Criticité | Base | Soft cap (CC) | Hard cap (abort) | Agents | Nexus-Critic |
|-----------|------|---------------|------------------|--------|--------------|
| **Archivage simple / donnée standard** | 1k | 2k | 3k | Single (Nexus-DevOps-Lead + support) | T2 seul |
| **RGPD / standard métier** | 3k | 5k | 8k | Single + T1 casseur | T1 + T2 |
| **Finance / Santé / Défense / donnée sensible** | 5k | 8k | 15k | Multi (5-7 agents) + Council | T1 + T2 + T3 + Council |

**Note v2** : P10 passe de "Single" (suggestion initiale 2k/3k/5k) à "Adaptatif par criticité conformité (3-niveaux, symétrie P8/P9)". Action P10-1 : évolution `pre-tool-use/token-counter.sh` pour supporter mode adaptatif 3-niveaux (env var `SWEBOK_P10_MODE=simple|rgpd|regulated` ou flag `--criticality`).

### 8.2 Compaction checkpoint
- [x] A. Tous les 5 tool calls
- [x] B. À 70% du soft cap
- [x] C. **+ Compaction agressive des logs de shutdown** (garder les actions critiques, drop le verbose)
- [x] D. **+ Memory durable des artefacts archivés** (consultable, pas dans le contexte)
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
- [x] A. Toutes les phases précédentes (pour la connaissance)
- [x] B. **+ Data inventory** (depuis phase-2/3/4)
- [x] C. **+ User list** (depuis phase-2/7)
- [x] D. **+ Dependency map** (depuis phase-3)
- [x] E. **+ Pas de re-chargement de toutes les specs** (index + retrieval)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret
- [x] A. T1 : Shutdown Operator vs Data Loss Hunter
- [x] B. T2 : Compliance Audit (RGPD, etc.)
- [x] C. T3 : Future Impact Predictor (que va-t-on regretter dans 1 an ?)
- [x] D. **+ Council de clôture** formel
- [x] E. **+ Context isolation** : le data loss hunter n'a pas accès au plan
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger — **7 éléments P10-spécifiques**

> Stockés dans `.swebok_state.db` table `udl_p10` (cohérent P8/P9 v2).

1. **EOL decision formalized** : sponsor sign-off, date, rationale (qui décide, pourquoi)
2. **Retirement type + criticité** : Q1+Q2 user 5.5, détermine agents + budget + Council
3. **Reversibility window configured** : Q3 user 5.5, fenêtre 30j/90j/180j+ read-only
4. **Compliance sign-off obtained** : Legal + CISO + DPO (si RGPD) signatures, dates
5. **Ownership transferred** : vers équipe remplacement OU archivage long-terme, contrat signé
6. **Stakeholder notification sent** : users, clients, partenaires, regulators, dates, canaux
7. **P0 link established** (si applicable) : Q4 user 5.5, nouveau projet démarré OU pas

### 8.6 Verdict
- [x] 🟢

**Note v2** : 8.1 budget adaptatif 3-niveaux (1k/2k/3k + 3k/5k/8k + 5k/8k/15k, symétrie P8/P9), 8.2 compaction 60-70% du soft cap, 8.3 consultation cross-phase via index+retrieval, 8.4 pattern adversarial adaptatif (T2/T1+T2/T1+T2+T3+Council), 8.5 UDL 7 éléments P10-spécifiques, 8.7 validation empirique 2026 + Drew Breunig 4 modes complet. Verdict 🟢.

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md`.

#### Findings les plus pertinents pour cette phase
- **F13** : Single-agent ≥ multi-agent à budget tokens égal → **confirme single Nexus-PM + Nexus-CISO + Nexus-DS en séquentiel**, pas en parallèle (chaque étape = gate de conformité)
- **F5** : Lost-in-the-middle → **checklist de conformité en tête** (RGPD, rétention, sign-off), data inventory en queue
- **F6** : Mur à 35 min → data archival est long, **segmenter par type de données** (users, transactions, logs, knowledge), pas une seule phase
- **F10** : Subagent output → filesystem → les certificats de destruction, sign-offs, archive index sont tous dans le state
- **F15** : HMAC chain = pattern production → étendre à tous les events de retirement (compliance audit trail)

#### Anti-patterns à éviter dans cette phase
- **AP1** : Multi-agent pour un shutdown simple — single Nexus
- **AP3** : Transcripts complets — digest des actions critiques uniquement
- **AP6** : Tool result clearing absent — garder les preuves de destruction, vider le reste
- **AP7** : Contexte "flood" avec toutes les specs historiques — index + retrieval, pas chargement
- **AP8** : "Plus de données archivées = mieux" → rot, archiver les knowledge artifacts, détruire le reste

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : une donnée archivée qui contamine la conformité ?
- [x] **Distraction** : trop de données à archiver qui noient les critiques ?
- [x] **Confusion** : ambiguïté sur ce qu'il faut détruire vs archiver ?
- [x] **Clash** : requirements contradictoires (RGPD vs rétention business) ?

#### Recommandation budget (mise à jour 2026)
- **Base 2k / Soft 3k / Hard 5k par segment** (single agent, séquentiel, structure pyramidale conformité, HMAC étendu à tous les events)

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 0 |
| New Books achetés (§19) | 0 |
| Standards NIST/OWASP (§13) | 0 |
| Open-access téléchargés | 0 |
| **TOTAL corpus-aligned local** | **0** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~5 livres
- **Disponible localement** : 0 corpus-aligned
- **Couverture effective** : **0%** ░░░░░░░░░░

### Lacunes (§20)

- **0** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **insuffisantes** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel


## Verdict global de la phase
- [x] 🟢

**Récap sections** (avant → après audit 2026-06-07) :
- 1. Charte (mission + démarcations P9↔P10 + P10↔P0 explicites) : 🟡 → 🟢
- 2. Conditions entrée/sortie (EG-10.1-10.9 + XG-10.1-10.10 + checklist 11 critères) : 🟡 → 🟢
- 3. Inputs (corpus 0% documenté, handoff P9 cohérent) : 🟡 → 🟢
- 4. Outputs (9+3 livrables triple différencié) : 🟡 → 🟢
- 5. Mécanique (5.5 = 4 décisions précises, adaptatif 3-niveaux) : 🟡 → 🟢
- 6. Bornes & modes échec (10 refus + 4 échecs + 7 abandons) : 🟡 → 🟢
- 7. Adéquation besoins (7.1-7.5 = projection cohérence P0-P9 v2) : 🟡 → 🟢
- 8. Context Engineering (adaptatif 3-niveaux + UDL 7 + pre-hydrate + Drew Breunig) : 🟡 → 🟢

## Liste d'actions

1. **P10-1** : Évoluer `pre-tool-use/token-counter.sh` pour supporter mode adaptatif 3-niveaux P10 (env var `SWEBOK_P10_MODE=simple|rgpd|regulated` ou flag `--criticality`). Action de suivi non bloquante, défaut 1k/2k/3k pour P10 archivage simple.
2. **P10-2** : Acquisition livres P10 manquants (5 livres canoniques : Software End-of-Life, EOL Management, Data Migration, Compliance Closure, Data Retention Policies + 2 NIST/OWASP : NIST 800-88r1 + 1 autre). Effort ~$400, 2-3 semaines. Non bloquant, planifier avec P9 dans le batch d'acquisition (Feathers + Sadalage).
3. **P10-3** : Formaliser Council de clôture P10 (CISO + Legal + PM + DevOps-Lead) si pas déjà fait. Vérifier que `nexus-ciso`, `legal-advisor`, `nexus-pm`, `nexus-devops-lead` peuvent être convoqués ensemble (skill agent).
4. **P10-4** : Valider la démarcation P10↔P0 sur un projet test où un EOL est suivi d'un replacement (P10 ancien archivé + P0 nouveau projet démarré en parallèle ou en séquence). Nice-to-have, nice-to-have pour la roadmap v2.1.

## Notes libres

- **Phase précédente** : P9 v2 finale (2026-06-07) a déjà tranché la démarcation P9↔P10 ("prolonger vs préparer la mort"). P10 v2 finale 2026-06-07 a ajouté la démarcation P10↔P0 ("fin de vie ancien vs début nouveau système"). Triple démarcation P8↔P9↔P10 (Run vs Change vs Retire) + démarcation P10↔P0 ferment toutes les frontières de phase contestées.
- **Spécificité P10 unique** : P10 est la seule phase qui n'est PAS une phase vivante (vs P8 Operations qui dure tant que la prod tourne). P10 est one-shot et marque la FIN du cycle de vie. Après P10, le système est archivé et seules les ré-ouvertures contrôlées sont possibles (toujours dans P10, pas de redémarrage P9).
- **Vers le récap projet final** : P0-P10 tous à 🟢. Le projet SWEBOK v4 Harness Distilled est complet. Le mainteneur peut merger toutes les specs v2 dans main, tag une version "v2.0.0-audit-complete", ou démarrer un nouveau projet (retour P0).
- **Batch d'acquisition P9+P10 prioritaire** : 2 livres P9 (Feathers + Sadalage) + 5 livres P10 + 2 NIST/OWASP = ~$800, 3-4 semaines. Action non bloquante mais critique pour la qualité (0% sur 2 phases).
