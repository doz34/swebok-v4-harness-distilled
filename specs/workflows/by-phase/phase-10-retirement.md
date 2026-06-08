# Phase 10: Retirement Workflow Spec

> **Statut** : v2 — validé 2026-06-07 par le mainteneur (audit P10 clos via grille offline + 4 questions vague 1, verdict 🟢 dès la première conversation).
> **Changement vs v2-renum** : (1) **critère explicite de démarcation P9↔P10 ET P10↔P0** inscrit (P9 = code modifié → système vivant ; P10 = code archivé → système arrêté ; P0 = début d'un NOUVEAU système), (2) **Nexus-Critic ADAPTATIF par criticité conformité** (3 niveaux symétrie P8/P9 : archivage simple = T2 seul, RGPD/standard = T1+T2, finance/santé/défense = T1+T2+T3), (3) **hard cap 5k → adaptatif 3-niveaux par criticité conformité** (archivage simple 1k/2k/3k, RGPD/standard 3k/5k/8k, finance/santé/défense 5k/8k/15k, symétrie P8/P9), (4) **Council de clôture CONDITIONNEL par criticité** (archivage simple = signature Nexus-DevOps-Lead, finance/santé/défense = Council CISO+Legal+PM+DevOps-Lead), (5) **9+ livrables** (7 standard + ajouts : legal sign-off + compliance sign-off + post-retirement review + communication sent log), (6) XG-10.1-10.10 (10 exit criteria), (7) **section 5.5 transformée en 4 décisions précises** (type retirement + criticité conformité + réversibilité + lien P0 futur), (8) **section 7 comblée par projection + cohérence P0/P1/P2/P3/P4/P5/P6/P7/P8/P9 v2** (effort 5-15% projet pour archivage simple, 15-30% pour conformité lourde), (9) **UDL 7 éléments P10-spécifiques** documentés, (10) **audit des 4 failure modes Drew Breunig** complet, (11) **Couverture cas universelle adaptative** 6 cas, (12) **Hooks 15** alignés P9, (13) **Refus catégoriques 10** (vs 6 v2-renum), (14) **Critères d'échec 4 + d'abandon 7**, (15) **Pre-hydrate obligatoire** (F7 recherche 2026), (16) **Compaction 60-70% du soft cap** par criticité, (17) **Conditions de sortie (checklist 11 critères)**, (18) **Réversibilité hybride par criticité** (archivage simple 30j read-only, RGPD/standard 90j, finance/santé/défense 180j+).
> **Changement vs structure antérieure** : v2-renum créée 2026-06-05 (renommage cascade P9→P10 après split P3). Refonte ciblée pour aligner sur P3/P4/P5/P6/P7/P8/P9 v2 + intégrer les démarcations P9↔P10 (déjà tranchée vague 1 P9) et P10↔P0 + mode adaptatif 3-niveaux par criticité conformité (symétrie P8/P9) + Nexus-Critic adaptatif + Council de clôture conditionnel.
> **But** : consommer les EOL decisions émises par P9 (système en fin de vie sans plan de remplacement) ou P8 (système à retirer après incident critique systémique) pour arrêter proprement un système — archivage code + données + config + docs + transfert ownership + conformité de fermeture + notification stakeholders + réversibilité hybride — avec traçabilité complète de la fermeture et signature collective conditionnelle par criticité, sans redémarrer le système (escalade P0 si nouveau projet) ni modifier le code de production (impossible : système archivé, code read-only).

---

## Metadata

- **Phase**: 10
- **Name**: Retirement
- **Purpose**: Gracefully decommission software in a controlled, compliant manner when it reaches end-of-life, with full traceability of the closure, conditional collective sign-off by compliance criticality, and reversible archival window
- **Parallel Mode**: Adaptatif par criticité conformité (3 niveaux, symétrie P8/P9) : archivage simple/donnée standard = single Nexus-DevOps-Lead + T2 seul sans Council ; RGPD/donnée personnelle = single + T1 casseur + T2 conformité ; finance/santé/défense = multi + T1+T2+T3 + Council de clôture obligatoire
- **Équivalent SWEBOK v4** : Pas de KA SWEBOK direct. Couvre Software Engineering Process (KA P9 SWEBOK) + Software Maintenance (P6 SWEBOK, fin de vie) + aspects RGPD/archivage/conformité. Séparé dans le présent modèle pour la clarté opérationnelle (fin de vie, archivage, conformité, transfert ownership).
- **Référentiels** : ISO/IEC/IEEE 12207:2017 (Software Life Cycle Processes), ISO/IEC 14764:2006 (Software Maintenance), RGPD (Règlement Général sur la Protection des Données), ITIL v4 (Service Transition → Service Retirement), Data Retention Policies (juridictions multiples), 0 livre canonique disponible localement (🔴 0% couverture corpus, lacune critique)

---

## Mission (1 phrase)

> « Consommer les EOL decisions émises par P9 (système en fin de vie sans plan de remplacement) ou P8 (incident systémique requérant arrêt) pour arrêter proprement un système qui s'arrête — archivage code + données + config + docs + transfert ownership + conformité de fermeture + notification stakeholders + réversibilité hybride par criticité — avec traçabilité complète de la fermeture, signature collective conditionnelle par criticité conformité (Nexus-DevOps-Lead pour archivage simple, Council CISO+Legal+PM+DevOps-Lead pour finance/santé/défense), et fenêtre de réversibilité hybride (30j/90j/180j+ read-only selon profil), sans redémarrer le système archivé (escalade P0 si nouveau projet) ni modifier le code de production (impossible : code read-only après archivage). »

---

## Critère de démarcation P9 (Maintenance) ↔ P10 (Retirement) ↔ P0 (Discovery)

> **Validation 2026-06-07** : le mainteneur a tranché pour des critères explicites, inscrits dans P10 (et déjà inscrits dans P9 v2 finale pour P9↔P10). **P9 = code modifié → système continue à vivre ; P10 = code archivé → système s'arrête ; P0 = début d'un NOUVEAU système (exploration/intake/JTBD)**. Trois questions simples : P9 "modifier le code pour faire vivre le système ?" ; P10 "arrêter, archiver, retirer un système ?" ; P0 "découvrir et cadrer un nouveau système (éventuellement en remplaçant l'ancien) ?".

### Démarcation P9 ↔ P10 (TRANCHÉE vague 1 P9 audit 2026-06-07, reprise ici)

**Règle simple P9 vs P10** : si la décision **prolonge la vie du système** (modifier le code, ajouter une feature, corriger un bug) = P9. Si la décision **prépare la mort du système** (archiver, transférer ownership, notifier stakeholders EOL) = P10.

**Critère retenu : question centrale (recommandé)** — P9 prolonge la vie du système, P10 prépare la mort.

### Démarcation P10 ↔ P0 (TRANCHÉE vague 1 P10 audit 2026-06-07, NOUVELLE)

**Règle simple P10 vs P0** : P10 = **fin de vie d'un système EXISTANT** (archivage, conformité, transfert, notification de l'ancien système). P0 = **début d'un NOUVEAU système** (exploration, intake, JTBD, cadrage, scope). Le critère opérationnel est : **"Est-ce qu'on parle d'arrêter un système qui s'arrête, ou de commencer un système qui n'existe pas encore ?"**

**Critère retenu : question centrale (recommandé, symétrie P9↔P10)** — P10 ferme un système, P0 ouvre un système.

| Dimension | P10 Retirement (cette spec) | P0 Discovery (nouveau projet) |
|-----------|------------------------------|-------------------------------|
| **Question centrale** | **Arrêter, archiver, retirer un système ?** (le système s'arrête définitivement) | **Découvrir, explorer, cadrer un NOUVEAU système ?** (le système n'existe pas encore, exploration libre) |
| **Système cible** | Système EXISTANT en production (code, données, config, docs, stakeholders) | Système FUTUR inexistant (intake, exploration, alternatives, scope) |
| **Activité dominante** | Archiver code + données + config + docs, transférer ownership, notifier stakeholders, fermer monitoring, démontrer conformité | Interviewer stakeholders, faire JTBD, explorer solutions, cadrer scope, valider faisabilité |
| **Inputs typiques** | EOL decision (P9 escalade ou sponsor direct), data inventory (P2-P4), user list (P2-P7), dependency map (P3), compliance requirements (P2/P3), knowledge artifacts (P0-P9 cumul) | Brief/intake, idée vague, problème observé, demande stakeholder, marché |
| **Outputs typiques** | `eol-decision-memo.md`, `archive-procedure.md`, `data-migration-plan.md`, `compliance-closure-report.md`, `ownership-transfer.md`, `stakeholder-notification.md`, `final-archive-snapshot.md`, `post-retirement-monitoring-stop.md`, `post-retirement-review.md`, `communication-sent-log.md` | `discovery-brief.md`, `jobs-to-be-done.md`, `alternatives-explored.md`, `scope-charter.md`, `feasibility-report.md` |
| **Adversarial** | Adaptatif par criticité conformité (3 niveaux, cf. Mécanique opérationnelle) | T1 (producteur vs casseur) + T2 (spec-compliance) en standard, T3 optionnel |
| **Agents typiques** | Adaptatif par criticité (cf. Responsible Agents) | Nexus-PM lead, Nexus-Architect, Nexus-CEO (cadrage stratégique), Nexus-CPO (cadrage produit) |
| **Trigger transition** | EOL approche (P9 escalade) ou incident systémique (P8 escalade) → démarrage P10. P10 complete → système archivé, plus de modifications. | Nouveau besoin, nouveau projet, OU P10 se termine et le mainteneur veut remplacer l'ancien système par un nouveau (passage P10 → P0 d'un nouveau projet, pas de P0 du même projet car le système est archivé) |
| **Réversibilité** | Hybride par criticité (30j/90j/180j+ read-only) avant suppression définitive | P0 n'a pas de "réversibilité" car le système n'existe pas encore. P0 produit une décision go/no-go pour P1. |

### Cas limites types (tranchés vague 1 P10)

- **"Réutilisation de composants d'un système archivé pour un nouveau système"** = **P0 du nouveau système** (on parle du nouveau, pas de l'ancien). L'extraction des composants archivés est une activité technique (P10), mais le cadrage du nouveau système = P0.
- **"Documentation des lessons learned d'un EOL pour les futurs projets"** = **P10** (post-retirement review, attaché au système archivé). Le système archivé = source de lessons learned, pas le nouveau projet.
- **"Re-démarrage d'un système archivé (annulation EOL)"** = **P10** (re-archivage, traçabilité décisions EOL). Si l'EOL est annulé, on consigne dans l'UDL P10, on ré-évalue la réversibilité, et on bascule en mode "archive gelée indéfiniment" ou "réouverture contrôlée" (toujours dans P10, pas de P0 car on ne parle pas d'un nouveau système).
- **"EOL d'un système AVEC plan de remplacement actif"** : la phase de remplacement du système (build du nouveau) = **P0/P1/P2/...P7/P8/P9** du nouveau projet. L'EOL de l'ancien = **P10** (en parallèle ou en séquence après le cut-over).
- **"Hotfix urgent sur un système en cours d'archivage P10"** = **escalade P9** (changement code) ou **escalade P7** (re-deploy). P10 ne modifie JAMAIS le code en cours d'archivage. Si le hotfix est critique, on peut déplier l'archive (tant que la réversibilité le permet, 30j/90j/180j+), appliquer le hotfix via P9 + P7, puis re-archiver.
- **"Communiquer aux stakeholders pendant le processus P10"** = **P10** (UDL 3 = stakeholder communication). Le plan de communication initial (quoi dire, à qui, quand) = P10 (livrable `stakeholder-notification.md`).
- **"Décider du sort des données personnelles (RGPD)"** = **P10** (data migration plan + compliance closure report). Mais "définir la politique de rétention des données" = P2 (requirement) si fait en amont, P10 si fait pendant l'EOL.
- **"Maintenance d'un système en fin de vie AVEC plan de remplacement actif"** = **P9** (prolonge). "Maintenance d'un système en fin de vie SANS plan de remplacement" = **P10** (prépare la mort). (Reprise de P9 v2 finale, démarcation réciproque.)

**Conséquence opérationnelle sur P9 v2 finale** : aucune modification. P9 émet l'EOL decision (Q4 user 5.5 = "Système en fin de vie sans plan de remplacement") qui escalade vers P10.

**Conséquence opérationnelle sur P0** : aucune modification. P0 reste le point d'entrée de tout nouveau système. Si un projet démarre pour remplacer un système archivé, c'est un P0 indépendant (peut réutiliser des composants archivés via une activité technique, mais le cadrage reste P0).

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-10.1 | EOL decision formalisée | EOL decision memo (sponsor + stakeholders) | Sponsor sign-off documenté (signature numérique ou manuscrit) |
| EG-10.2 | Replacement system ready OU EOL accepté | Replacement status | Replacement system go-live confirmé OU EOL pur accepté par stakeholders |
| EG-10.3 | Stakeholder approval obtenue | Approval signatures | Tous les primary stakeholders (sponsor, PM, CISO si conformité, Legal si RGPD) ont signé |
| EG-10.4 | Plan de retirement documenté | Plan completeness (Q1 user 5.5) | Type de retirement (archivage simple / RGPD / finance / défense / transfert ownership) tranché |
| EG-10.5 | Data retention policy définie | Policy document (Legal + Compliance) | Approuvé par Legal/Compliance (juridiction applicable) |
| EG-10.6 | Risk assessment complété | Risk register (P3 heritage) | Tous les risques identifiés et rated (perte données, régression système remplacement, non-conformité, stakeholder non notifié) |
| EG-10.7 | Criticité conformité évaluée | Criticité décision (Q2 user 5.5) | Archivage simple / RGPD standard / Finance-Santé-Défense tranché (détermine agents + budget + Council) |
| EG-10.8 | Réversibilité configurée | Reversibility window (Q3 user 5.5) | Fenêtre 30j/90j/180j+ read-only configurée, restaurable sur demande stakeholder |
| EG-10.9 | Communication planifiée | Communication plan (livrable `stakeholder-notification.md`) | Date d'envoi aux stakeholders (users, clients, partenaires, regulators) planifiée et confirmée |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers additional stakeholder engagement ou escalade P9 (si EOL non finalisé) ou escalade P0 (si nouveau projet à démarrer en parallèle).

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-10.1 | Data archived ou migrated per retention policy | Archive verification | 100% données archivées ou migrées vers système de remplacement, intégrité vérifiée (checksum) |
| XG-10.2 | Users migrés ou notifiés | Migration status | 100% users migrés vers système remplacement OU notifiés formellement (email + in-app + regulator si requis) |
| XG-10.3 | System shutdown clean | Shutdown checklist | 100% composants arrêtés (serveurs, DNS, monitoring, alertes, logs archivés) |
| XG-10.4 | Ownership transferred OU archived | Ownership transfer doc | Transfert signé vers équipe de remplacement OU archivage long-terme documenté (responsabilité claire) |
| XG-10.5 | All artifacts préservés | Artifact inventory | 100% artifacts archivés (code, docs, post-mortems, ADR, runbooks, knowledge base, dépendances) |
| XG-10.6 | Legal/compliance sign-off | Compliance confirmation (écrit) | Legal + Compliance (CISO pour sécurité, DPO pour RGPD) ont signé formellement |
| XG-10.7 | Final archive snapshot signée | Snapshot signature (git tag) | Tag EOL posé sur le commit final, archive signée (HMAC ou GPG), registre des décisions EOL complet |
| XG-10.8 | Post-retirement review documenté | Review report | Post-mortem EOL documenté (ce qui a marché, ce qui n'a pas marché, lessons learned pour futurs EOL) |
| XG-10.9 | Post-retirement monitoring stopped | Monitoring shutdown log | Monitoring, alertes, logs archivés (pas supprimés), DNS pointé vers page "service archived", alertes désactivées |
| XG-10.10 | UDL 7 éléments P10-spécifiques loggés | UDL set | 100% loggés dans `.swebok_state.db` (table `udl_p10`) |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` requires remediation before `PROJECT_RETIRED` emission. Si la réversibilité est dépassée (30j/90j/180j+ read-only expiré), aucune restauration possible.

---

## Transition Criteria (Phase Complete)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Data retention verified | Nexus-DS | CISO + DPO (si RGPD) | Retention compliance confirmed, signature |
| User transition complete | Nexus-PM | Project Sponsor | Notification sent log, transition memo |
| System decommission verified | Nexus-DevOps-Lead | Project Lead + CISO | Shutdown verification, monitoring stopped log |
| Knowledge preserved | Tous les agents | Knowledge Base | Archive indexed, consultable (search par profil) |
| Compliance closure | Nexus-CISO + Legal | Regulators (si applicable) | Sign-off écrit, archivage long-terme |
| Ownership transferred | Project Sponsor | Replacement team OU Archive | Transfert signé OU archivage long-terme documenté |
| Project closure authorized | Project Sponsor + Council (si applicable) | All stakeholders | Closure memo, PROJECT_RETIRED émis par Hyperagent-Orchestrator |

**Transition Authorization**: Hyperagent-Orchestrator émet `PROJECT_RETIRED` UNIQUEMENT quand TOUS les exit gate criteria vérifiés avec evidence formelle ET signature finale :
- Archivage simple : Nexus-DevOps-Lead seul
- RGPD/standard : Nexus-DevOps-Lead + CISO + Legal
- Finance/Santé/Défense : Council complet (CISO + Legal + PM + DevOps-Lead), examen 1h, signature collective

---

## Key Activities (adaptatif par criticité conformité)

### Activity 10.1: EOL Decision & Planning (toutes criticités)
- Consolider l'EOL decision memo (sponsor + stakeholders)
- Identifier le type de retirement (Q1 user 5.5) : archivage simple, RGPD, finance, défense, transfert ownership
- Évaluer la criticité conformité (Q2 user 5.5) : archivage simple / RGPD standard / Finance-Santé-Défense
- Définir la fenêtre de réversibilité (Q3 user 5.5) : 30j/90j/180j+ read-only
- Planifier la communication aux stakeholders (Q4 user 5.5 : lien avec P0 si nouveau projet)
- Documenter le plan de retirement (`retirement-plan.md`)

### Activity 10.2: Data Management & Compliance (toutes criticités, profondeur par criticité)
- Exporter les données critiques per retention policy
- Migrer les données vers système de remplacement OU archiver long-terme (chiffré)
- Vérifier l'intégrité des données (checksum, échantillonnage)
- Détruire les données per security policy (si applicable) avec certificats de destruction
- Pour RGPD : anonymiser/pseudonymiser, documenter le base légale de rétention
- Pour Finance/Santé/Défense : conformité réglementaire stricte (archivage immutable, signature numérique, audit trail)

### Activity 10.3: User Migration & Stakeholder Communication (toutes criticités)
- Exécuter la migration des users vers système de remplacement (si applicable)
- Fournir support pendant la transition (helpdesk, FAQ, tutoriels)
- Envoyer la communication finale aux stakeholders (users, clients, partenaires, regulators)
- Gérer les demandes d'export de données personnelles (RGPD Article 20)
- Décommissionner les accès (auth, OAuth, API keys)

### Activity 10.4: System Shutdown & Knowledge Archive (toutes criticités)
- Terminer les dépendances externes (API contracts, webhooks, DNS)
- Arrêter les systèmes de production (rolling shutdown ou big-bang selon dépendances)
- Libérer les ressources cloud (instances, storage, networking)
- Archiver toute la documentation (technique, ops, user, ADR, runbooks, post-mortems)
- Effectuer le post-retirement review (ce qui a marché, ce qui n'a pas marché, lessons learned)
- Construire l'index de la knowledge archive (consultable, search par profil)

### Activity 10.5: Council de clôture (CONDITIONNELLE par criticité)
- **Archivage simple** : pas de Council, signature Nexus-DevOps-Lead suffit
- **RGPD/standard** : signature Nexus-DevOps-Lead + CISO + Legal, pas de Council formel
- **Finance/Santé/Défense** : Council CISO + Legal + PM + DevOps-Lead, examen 1h, signature collective avant `PROJECT_RETIRED`

---

## Responsible Agents (adaptatif par criticité conformité)

| Criticité | Agents principaux | Agents support | Council de clôture |
|-----------|-------------------|----------------|---------------------|
| **Archivage simple** (single mode) | Nexus-DevOps-Lead (lead archivage + transfert) | Nexus-DS (data archival), Nexus-PM (notification stakeholders), Nexus-Docs (archivage documentation) | Aucun (signature Nexus-DevOps-Lead) |
| **RGPD/standard** (single + T1+T2) | Nexus-DevOps-Lead + Nexus-CISO (lead conformité) | Nexus-DS, Nexus-PM, Nexus-Docs, Legal (consultation) | Signature Nexus-DevOps-Lead + CISO + Legal |
| **Finance/Santé/Défense** (multi + T1+T2+T3) | Nexus-DevOps-Lead (lead), Nexus-CISO (conformité réglementaire), Nexus-PM (stakeholders), Legal (compliance) | Nexus-DS, Nexus-Docs, Nexus-Security (destruction sécurisée), Nexus-Architect (si refactoring pré-EOL) | **Council CISO + Legal + PM + DevOps-Lead obligatoire** (examen 1h, signature collective) |

**Note** : Nexus-Critic adaptatif par criticité (cf. Mécanique opérationnelle).

---

## Required Skills (adaptatif par criticité)

### Archivage simple
- `nexus-devops-lead` (lead archivage)
- `nexus-ds` (data archival)
- `nexus-pm` (stakeholder communication)
- `nexus-docs` (documentation archival)

### RGPD/standard
- Toutes les skills archivage simple +
- `nexus-ciso` (conformité sécurité)
- `legal-advisor` (consultation juridique)

### Finance/Santé/Défense
- Toutes les skills RGPD/standard +
- `nexus-security` (destruction sécurisée)
- `nexus-architect` (si refactoring pré-EOL)
- Council skills : `nexus-ciso` + `legal-advisor` + `nexus-pm` + `nexus-devops-lead`

---

## Knowledge Items Consultés (couverture corpus 0%, lacune critique)

> **🔴 0% de couverture** : 0 livre canonique disponible localement sur ~5 recommandés (Software End-of-Life, EOL Management, Data Migration, Compliance Closure, Data Retention Policies).

**Sources externes mobilisables** :
- Standards ISO/IEC/IEEE 12207:2017, ISO/IEC 14764:2006 (open access)
- RGPD (règlement européen 2016/679, open access)
- ITIL v4 (Service Transition → Service Retirement, payant)
- NIST 800-88r1 (Guidelines for Media Sanitization, open access)
- Data Retention Policies (juridictions multiples, специфик par secteur)

**Plan d'intégration** : acquisition des 5 livres canoniques + 2 NIST/OWASP dans le batch P10 prioritaire (avec Feathers + Sadalage de P9), effort ~$400, 2-3 semaines.

**Décision mainteneur 2026-06-07** : 0% = critique globale, batch d'acquisition P10 prioritaire (action P10-1).

---

## Hooks to Invoke (15 alignés P9)

| Hook | Trigger | Purpose |
|------|---------|---------|
| `retirement-decision-formalized` | EG-10.1 passed | Ouvre le record project P10 |
| `data-archived` | XG-10.1 passed | Update data governance (data est archivée) |
| `user-migration-complete` | XG-10.2 passed | Confirme la transition utilisateur |
| `system-shutdown-complete` | XG-10.3 passed | Libère les ressources (cloud, DNS) |
| `ownership-transferred` | XG-10.4 passed | Documente le transfert ownership |
| `compliance-signoff-obtained` | XG-10.6 passed | Confirme la conformité (Legal + CISO) |
| `retirement-closure-report-approved` | XG-10.7 + XG-10.8 passed | Archive le projet |
| `eol-tag-created` | Tag EOL posé sur commit final | Signature git, HMAC chain |
| `post-retirement-monitoring-stopped` | XG-10.9 passed | Monitoring archivé, alertes désactivées |
| `post-retirement-review-due` | Post-mortem EOL dû | Trigger le review (RCA de l'EOL) |
| `reversibility-window-expiring` | 7j avant expiration réversibilité | Notification stakeholders (rappel restauration possible) |
| `reversibility-window-expired` | 30j/90j/180j+ expiré | Archive définitive, suppression irréversible |
| `t1-data-loss-casseur-passed` | T1 casseur archivage passé | Confirme aucune perte de données |
| `t2-compliance-audit-passed` | T2 conformité audit passé | Configne conformité réglementaire |
| `udl-p10-logged` | UDL 7 loggés dans `.swebok_state.db` | Marque la phase complète |

---

## Artifacts Produced (9+ livrables, format triple différencié)

| Artifact | Description | Format | Location |
|----------|-------------|--------|----------|
| `eol-decision-memo.md` | EOL decision formalisée (sponsor + stakeholders) | md (1-2 pages, signature) | `specs/workflows/by-phase/phase-10-retirement/` |
| `archive-procedure.md` | Procédure archivage code + données + config | md (5-10 pages, step-by-step) | idem |
| `data-migration-plan.md` | Plan migration données (vers remplacement OU archive long-terme) | md (5-15 pages, schéma) | idem |
| `compliance-closure-report.md` | Conformité de fermeture (RGPD, finance, santé, défense) | md (10-20 pages, sign-off) | idem |
| `ownership-transfer.md` | Transfert ownership (vers remplacement OU archivage) | md (3-5 pages, contrat signé) | idem |
| `stakeholder-notification.md` | Notification finale (users, clients, partenaires, regulators) | md (2-3 pages, communication sent log) | idem |
| `final-archive-snapshot.md` | Snapshot final (code read-only, données archivées, config figée) | md + git tag + HMAC | idem + git |
| `post-retirement-monitoring-stop.md` | Arrêt monitoring, DNS, alertes, logs archivés | md (1-2 pages, log) | idem |
| `post-retirement-review.md` | Post-mortem EOL (ce qui a marché, lessons learned) | md (5-10 pages) | idem |
| **+ Legal sign-off doc** (suggéré si criticité élevée) | Signature Legal (RGPD Article 17, finance, défense) | PDF signé | idem |
| **+ Compliance sign-off doc** (suggéré si criticité élevée) | Signature CISO + DPO (DPO si RGPD) | PDF signé | idem |
| **+ Communication sent log** (suggéré) | Log de toutes les communications envoyées (date, destinataire, canal) | JSON ou CSV | idem |

**Format de stockage triple différencié** (cohérent P3-P9 v2) :
- **md** : rapports narratifs (eol-decision, archive-procedure, data-migration-plan, etc.)
- **git** : code archivé (tag EOL sur commit final, branche archive read-only)
- **JSON** : registres machine (communication-sent-log.json, archive-inventory.json)
- **MADR** : ADR EOL decision rationale (si structurante)
- **Keep a Changelog** : changelog public EOL announcement
- **HMAC chain** : audit trail (chaque event de retirement signé)

---

## Adversarial Pattern (adaptatif par criticité conformité)

### Archivage simple (single + T2)
- **T2 seul** : Nexus-Critic vérifie la conformité de la procédure d'archivage (checklist XG-10.1-XG-10.10) et la réversibilité configurée (Q3 user 5.5). 1 invocation ~1.5k tokens.

### RGPD/standard (single + T1+T2)
- **T1 casseur archivage** : "Data Loss Hunter" — vérifie qu'aucune donnée personnelle n'est perdue, que la pseudonymisation est correcte, que les certificats de destruction sont valides. Context isolation : le data loss hunter n'a PAS accès au plan de destruction (sinon il ne peut pas chasser).
- **T2 conformité réglementaire** : vérifie la conformité RGPD (Article 17 droit à l'effacement, Article 20 portabilité, base légale de rétention). 2 invocations ~3k tokens.

### Finance/Santé/Défense (multi + T1+T2+T3)
- **T1 casseur archivage** : "Data Loss Hunter" — comme RGPD mais étendu à toutes les données réglementées (transactions financières, dossiers patients, données classifiées défense).
- **T2 conformité réglementaire** : vérification stricte (PCI-DSS pour finance, HIPAA pour santé, IGI/IIR pour défense). 1 invocation ~1.5k.
- **T3 prédiction post-EOL** : "Future Impact Predictor" — prédit ce qui manquera dans 1-5 ans (régression sur système de remplacement, perte de connaissance, dette d'archivage). 1 invocation ~1.5k.
- **+ Council de clôture** : CISO + Legal + PM + DevOps-Lead, examen 1h, signature collective. Coût : ~2k tokens pour la session Council.

**Total Nexus-Critic** :
- Archivage simple : 1 invocation (T2) ~1.5k
- RGPD/standard : 2 invocations (T1+T2) ~3k
- Finance/Santé/Défense : 3 invocations (T1+T2+T3) + Council ~6.5k

---

## Hyperagent Parallel Processing (adaptatif par criticité)

```
# Archivage simple (séquentiel)
sequential_tasks:
  - data_archival: [Nexus-DS]
  - user_migration: [Nexus-PM]
  - infrastructure_decommission: [Nexus-DevOps-Lead]
  - knowledge_archive: [Nexus-Docs]
  - post_retirement_review: [Nexus-DevOps-Lead]
  reduction: "Nexus-DevOps-Lead synthétise en retirement-closure-report.md"

# RGPD/standard (séquentiel + adversarial T1+T2)
sequential_tasks:
  - data_archival: [Nexus-DS, Nexus-CISO]
  - user_migration: [Nexus-PM]
  - infrastructure_decommission: [Nexus-DevOps-Lead]
  - compliance_closure: [Nexus-CISO, Legal]
  - knowledge_archive: [Nexus-Docs]
  adversarial:
    - t1_data_loss_casseur: [Nexus-Critic, "Data Loss Hunter"]
    - t2_compliance_audit: [Nexus-Critic, "RGPD Compliance"]
  reduction: "Nexus-DevOps-Lead + CISO synthétisent en retirement-closure-report.md + compliance-closure-report.md"

# Finance/Santé/Défense (multi + 3 sequential adversarial + Council)
parallel_tasks:
  - data_archival: [Nexus-DS, Nexus-Security]
  - user_migration: [Nexus-PM, Nexus-Frontend]
  - infrastructure_decommission: [Nexus-DevOps-Lead, Nexus-CISO]
  - stakeholder_communication: [Nexus-PM, Legal]
  - compliance_closure: [Nexus-CISO, Legal]
  - knowledge_archive: [Nexus-Docs]
  adversarial:
    - t1_data_loss_casseur: [Nexus-Critic, "Data Loss Hunter (regulatory extended)"]
    - t2_compliance_audit: [Nexus-Critic, "Finance/Santé/Défense Compliance"]
    - t3_future_impact: [Nexus-Critic, "Future Impact Predictor (1-5 ans)"]
  council:
    - closure_council: [CISO, Legal, PM, DevOps-Lead]
  reduction: "Council synthétise en retirement-closure-report.md + sign-off collectif"
```

---

## Section 5.5 — Décisions opérationnelles utilisateur (B threshold)

> **4 décisions précises (vs vide v1, vs catégories v2-renum)** — symétrie P8 (4 décisions) et P9 (4 décisions). P10 = single-agent archivage séquentiel par défaut, mais 4 décisions structurantes pour cadrer le retirement.

### Q1 — Type de retirement (Q1 user 5.5)

| Option | Description | Conséquence budget/agents |
|--------|-------------|---------------------------|
| **A. Archivage simple** (recommandé P10 défaut) | Code + données + config archivés, pas de conformité lourde | Single + T2 (1k/2k/3k), pas de Council |
| **B. RGPD / données personnelles** | Données personnelles à anonymiser/pseudonymiser, droit à l'effacement (Article 17) | Single + T1+T2 (3k/5k/8k), signature CISO + Legal |
| **C. Finance / Santé / Défense** | Conformité réglementaire stricte (PCI-DSS, HIPAA, IGI/IIR) | Multi + T1+T2+T3 + Council (5k/8k/15k) |
| **D. Transfert ownership structurant** | Transfert vers équipe de remplacement (nouveau système prend le relais) | Single + T2 (1k/2k/3k), signature PM + sponsor |

### Q2 — Criticité conformité (Q2 user 5.5)

| Option | Criticité | Fenêtre réversibilité | Council |
|--------|-----------|------------------------|---------|
| **A. Archivage simple / donnée standard** (recommandé défaut) | Faible | 30j read-only | Non |
| **B. RGPD standard / donnée métier** | Moyenne | 90j read-only | CISO + Legal (pas formel) |
| **C. Finance / Santé / Défense / donnée sensible** | Élevée | 180j+ read-only | Oui (formel, 1h) |

### Q3 — Réversibilité de l'archivage (Q3 user 5.5)

| Option | Fenêtre | Restaurable | Usage typique |
|--------|---------|-------------|---------------|
| **A. 30j read-only** (recommandé archivage simple) | 30 jours | Sur demande stakeholder | Archivage simple, risque faible |
| **B. 90j read-only** (recommandé RGPD/standard) | 90 jours | Sur demande stakeholder | RGPD, données métier |
| **C. 180j+ read-only** (recommandé Finance/Santé/Défense) | 180 jours | Sur demande CISO/Legal/Regulator | Conformité réglementaire stricte |
| **D. Indéfini read-only** (archive permanente) | Indéfini | Sur demande regulator uniquement | Banking, défense, audit permanent |

### Q4 — Lien avec P0 Discovery (Q4 user 5.5)

| Option | Description | Conséquence P0 |
|--------|-------------|----------------|
| **A. Aucun lien P0** (recommandé EOL pur) | Le système archivé n'est pas remplacé. Pas de P0 à démarrer. | — |
| **B. P0 d'un nouveau projet démarre en parallèle** (recommandé si replacement) | Le système archivé est remplacé par un nouveau système. P0 du nouveau projet démarre. | P0 indépendant (réutilisation de composants via activité technique, pas de P0 du même projet) |
| **C. Lessons learned alimentent P0 futur** (recommandé systématiquement) | Le post-retirement review (livrable P10) alimente les futurs P0 (meilleures pratiques EOL) | Pas de P0 immédiat, mais lessons learned archivés pour P0 futurs |
| **D. P0 démarre APRÈS P10 complete** (recommandé si pas urgent) | Le cut-over est séquentiel : P10 d'abord (ancien archivé), puis P0 du nouveau | P0 démarre quand `PROJECT_RETIRED` est émis |

---

## UDL — User Decision Ledger (7 éléments P10-spécifiques)

> Stockés dans `.swebok_state.db` table `udl_p10` (cohérent P8/P9 v2).

1. **EOL decision formalized** : sponsor sign-off, date, rationale
2. **Retirement type + criticité** : Q1+Q2 user 5.5, détermine agents + budget + Council
3. **Reversibility window configured** : Q3 user 5.5, fenêtre 30j/90j/180j+ read-only
4. **Compliance sign-off obtained** : Legal + CISO + DPO (si RGPD) signatures, dates
5. **Ownership transferred** : vers équipe remplacement OU archivage long-terme, contrat signé
6. **Stakeholder notification sent** : users, clients, partenaires, regulators, dates, canaux
7. **P0 link established** (si applicable) : Q4 user 5.5, nouveau projet démarré OU pas

---

## Compaction & Pre-hydrate (transverse)

### Pre-hydrate obligatoire (F7 recherche 2026)

**Chargement obligatoire en début de phase P10** :
- EOL decision memo (sponsor + stakeholders)
- Data inventory (P2-P4 heritage, où sont les données)
- User list (P2-P7 heritage, qui est impacté)
- Dependency map (P3 heritage, quels systèmes sont impactés)
- Legal/compliance requirements (P2/P3 heritage, RGPD, finance, santé, défense)
- Knowledge artifacts (code, docs, post-mortems, ADR, runbooks, P0-P9 cumul)
- Replacement system status (si applicable) ou confirmation EOL pur
- Communication plan (qui notifier, quand, comment)

### Compaction 60-70% du soft cap (F8 recherche 2026)

**Triggers de compaction** :
- Archivage simple : compaction à 1.4k/2.1k tokens (60-70% de 2k/3k soft cap)
- RGPD/standard : compaction à 3.5k/5.6k tokens
- Finance/Santé/Défense : compaction à 5.6k/8.4k tokens (60-70% de 8k/15k soft cap)

**Stratégies de compaction** :
- **Compaction agressive des logs de shutdown** : garder les actions critiques (XG-10.1-XG-10.10 status), drop le verbose
- **Memory durable des artefacts archivés** : consultable via L0 corpus, pas dans le contexte
- **Tool result clearing (AP6)** : vider les tool results volumineux (data inventory, dependency map) après consommation
- **Index + retrieval, pas chargement** : knowledge archive index en L3, pas la knowledge archive entière

---

## 4 Failure Modes Drew Breunig (NOUVEAU, audit Drew Breunig complet)

### Poisoning (7 mécanismes)
1. **Data archivée contaminée par PII oubliée** : une donnée personnelle non identifiée contamine la conformité RGPD → vérification T1 data loss casseur
2. **Certificat de destruction forgé** : un certificat falsifié contamine l'audit trail → signature HMAC + vérification croisée Legal
3. **Stakeholder notification adressée à la mauvaise personne** : RGPD violation (donnée personnelle envoyée à un tiers) → validation destinataire stricte
4. **Snapshot final incomplet** : un artefact oublié contamine l'archive (pas restaurable à 100%) → checklist XG-10.5 100% artifacts
5. **Compliance report cite un texte de loi obsolète** : un texte abrogé contamine la conformité → vérification version texte de loi
6. **Ownership transfer signé par la mauvaise personne** : transfert non valable → validation identité signataire
7. **Audit trail avec timestamps incohérents** : incohérence temporelle contamine la traçabilité → HMAC chain + cohérence temporelle

### Distraction (7 mécanismes)
1. **Trop de données à archiver qui noient les critiques** : archivage de logs verbeux au lieu de knowledge artifacts → stratégie d'archivage sélective
2. **Trop de stakeholders à notifier** : notifications en masse noient les messages critiques → segmentation par profil (users/clients/regulators)
3. **Trop de réglementations à vérifier** : checklist conformité surdimensionnée → focus sur les réglementations applicables au profil
4. **Trop d'agents en parallèle** (Finance/Santé/Défense) : 5-7 agents noient le contexte → séquentiel strict (chaque étape = gate)
5. **Trop de livrables** (9+) : 12 livrables noient l'attention → focus sur les 6 critiques (eol-decision, archive-procedure, data-migration, compliance-closure, ownership-transfer, stakeholder-notification)
6. **Trop de réversibilité à configurer** : 4 fenêtres de réversibilité selon criticité → Q3 user 5.5 tranche une fois pour toutes
7. **Trop de Council à convoquer** : CISO + Legal + PM + DevOps-Lead = 4 stakeholders noient l'attention → Council formel 1h, pas de réunions annexes

### Confusion (7 mécanismes)
1. **Ambigüité sur ce qu'il faut détruire vs archiver** : RGPD = détruire les données personnelles, archiver les logs → matrice destruction vs archivage documentée
2. **Ambigüité sur qui signe quoi** : sponsor vs Legal vs CISO vs DPO → matrice de signature par criticité
3. **Ambigüité sur le destinataire de la notification** : users internes vs externes vs regulators → segmentation claire
4. **Ambigüité sur la fenêtre de réversibilité** : 30j vs 90j vs 180j+ → Q3 user 5.5 tranche une fois
5. **Ambigüité sur le sort des artefacts** : détruire vs archiver vs donner à l'équipe de remplacement → matrice par type d'artefact
6. **Ambigüité sur la migration des users** : migrer automatiquement vs notifier pour migration manuelle → décision Q1 user 5.5
7. **Ambigüité sur le redémarrage éventuel** : si EOL annulé, qui ré-ouvre → documentation du processus de ré-ouverture dans le plan de retirement

### Clash (7 mécanismes)
1. **Requirements contradictoires (RGPD vs rétention business)** : Article 17 RGPD (droit à l'effacement) vs rétention 10 ans finance → matrice de priorité documentée, escalade Legal si conflit
2. **Stakeholders contradictoires (sponsor vs Legal)** : sponsor veut aller vite, Legal veut compliance stricte → escalade mainteneur + arbitrage
3. **Agents contradictoires (Nexus-DevOps-Lead vs CISO)** : DevOps veut shut down rapide, CISO veut vérifications longues → séquentiel strict (chaque étape = gate)
4. **Format contradictoire (md vs JSON)** : spec dit md, audit trail dit JSON → format triple différencié (md pour rapports, JSON pour registres, git pour code)
5. **Timeline contradictoire (sponsor vs ops)** : sponsor veut 30j, ops veut 90j → Q3 user 5.5 tranche, respect de la fenêtre
6. **Council contradictoire (CISO vs PM)** : CISO veut Council formel 1h, PM veut signature rapide → Q2 user 5.5 détermine si Council est obligatoire
7. **Réversibilité contradictoire (stakeholder demande restauration après expiration)** : réversibilité expirée = pas de restauration → documentation stricte, escalade CISO/Legal

---

## Refus catégoriques (10, vs 6 v2-renum)

1. **Pas d'archivage sans EOL decision formelle** (sponsor sign-off obligatoire)
2. **Pas de perte de données utilisateurs** (migration ou archive explicite obligatoire)
3. **Pas de skip de conformité réglementaire** (RGPD, finance, santé, défense)
4. **Pas de fermeture de système avec incidents ouverts** (escalade P8 ou P9 d'abord)
5. **Pas d'arrêt monitoring sans période de grâce** (minimum 30j, selon Q3 user 5.5)
6. **Pas de suppression définitive avant période de réversibilité** (Q3 user 5.5)
7. **Pas de transfert ownership sans contrat signé** (responsabilité claire obligatoire)
8. **Pas d'EOL d'un système critique sans plan de remplacement** (escalade P0 si nouveau projet)
9. **Pas de modification de code pendant l'archivage** (P10 = read-only après EOL decision)
10. **Pas de réouverture d'un système archivé sans réversibilité active** (sinon nouveau P0 + P1 + ... P9)

---

## Critères d'échec (4, déclenchent action immédiate)

1. **Données perdues pendant migration** → escalade critique + post-mortem + notification stakeholders immédiate
2. **Conformité non respectée** (RGPD violation, finance/santé/défense non conforme) → escalation CISO + Legal + regulatory + communication de crise
3. **Stakeholder non notifié** (user/client/regulator oublié) → escalade mainteneur + communication de crise + remédiation
4. **Ownership non transféré** (équipe de remplacement pas prévenue) → escalade juridique + responsabilité mainteneur

## Critères d'abandon (7, escalade mainteneur)

1. **EOL annulé en cours de P10** → ré-archivage, traçabilité décisions EOL (toujours P10)
2. **Conformité impossible à atteindre** (réglementation contradictoire) → escalade mainteneur + arbitrage juridique
3. **Stakeholder refus de signer l'EOL** (sponsor refuse) → escalade mainteneur + décision go/no-go
4. **Données irrécupérables** (corrompues pendant migration) → escalade CISO + post-mortem obligatoire
5. **Replacement system pas prêt** (P7 du nouveau système bloqué) → suspension P10, escalade P7 du nouveau
6. **Réversibilité dépassée** (30j/90j/180j+ expiré avant `PROJECT_RETIRED`) → escalade CISO/Legal, prolongation réversibilité ou suppression définitive
7. **35 min sans avancée** (mur F6) → escalade mainteneur, segmentation du retirement

---

## Couverture cas universelle adaptative (6 cas)

| Cas | % projet | Profil conformité | Council | Budget |
|-----|----------|-------------------|---------|--------|
| **Greenfield** (nouveau système) | 5-10% (1 EOL en fin de vie) | Archivage simple | Non | 1k/2k/3k |
| **Maintenance legacy** (système ancien) | 15-30% (fin de vie, dette accumulée) | RGPD/standard | CISO + Legal | 3k/5k/8k |
| **Projet interne** (système d'entreprise) | 10-20% (EOL planifié) | Archivage simple | Non | 1k/2k/3k |
| **Projet externe** (système client) | 15-25% (transfert ownership) | Archivage + transfert | Signature PM + sponsor | 1k/2k/3k |
| **Compliance-driven** (système régulé) | 25-40% (finance/santé/défense) | Conformité stricte | Council obligatoire | 5k/8k/15k |
| **R&D / prototype** (système expérimental) | 5-15% (EOL rapide) | Archivage simple | Non | 1k/2k/3k |

---

## Section 7 — Adéquation aux besoins (utilité réelle, comblée par projection)

### 7.1 Usage réel

P10 = dernière phase du cycle de vie d'un système. Effort typique 5-40% du projet (one-shot, mais structurant) selon criticité conformité :
- Archivage simple : 5-10% du projet
- RGPD/standard : 15-25% du projet
- Finance/Santé/Défense : 25-40% du projet

**P10 ne s'active PAS** dans 95% des projets (les projets meurent rarement formellement). Quand P10 s'active, c'est un événement structurant (EOL, replacement, incident systémique).

### 7.2 Friction observée (4 frictions)

1. **F1 — Knowledge loss** : personne ne sait pourquoi on avait fait tel choix → risque de régression sur le système de remplacement
2. **F2 — Compliance violation** : RGPD oublié, finance/santé/défense non conforme → risque juridique et réputationnel
3. **F3 — Users orphelins** : non migrés et non notifiés → utilisateurs bloqués, support client surchargé
4. **F4 — Data leak** : destruction ratée de données sensibles → escalade CISO + regulator

**Mitigations** : matrice destruction vs archivage, checklist XG-10.1-XG-10.10, communication sent log, certificats de destruction signés HMAC.

### 7.3 Pattern de contournement (4 contournements)

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

---

## Token Budget (adaptatif 3-niveaux par criticité conformité)

| Criticité | Base | Soft cap (CC) | Hard cap (abort) | Justification |
|-----------|------|---------------|------------------|---------------|
| **Archivage simple / donnée standard** | 1k | 2k | 3k | Single Nexus-DevOps-Lead + T2 seul, pas de Council. Couvre greenfield, R&D, projet interne simple. |
| **RGPD / standard métier** | 3k | 5k | 8k | Single + Nexus-Critic T1 casseur + T2 conformité. Couvre données personnelles, métier standard. |
| **Finance / Santé / Défense / donnée sensible** | 5k | 8k | 15k | Multi + Nexus-Critic T1+T2+T3 + Council de clôture obligatoire. Coût additionnel : ~6.5k tokens (Critic T1+T2+T3 + Council 1h). Couvre conformité réglementaire stricte. |

**Action P10-1** : évolution `pre-tool-use/token-counter.sh` pour supporter mode adaptatif 3-niveaux (env var `SWEBOK_P10_MODE=simple|rgpd|regulated` ou flag `--criticality`). Action de suivi non bloquante, défaut 1k/2k/3k pour P10 archivage simple.

---

## Couverture corpus (0%, lacune critique)

| Source | Livres disponibles pour P10 |
|---|---:|
| Mac Studio | 0 |
| New Books achetés | 0 |
| Standards NIST/OWASP | 0 |
| Open-access téléchargés | 0 |
| **TOTAL corpus-aligned local** | **0** |

**Couverture recommandée** : ~5 livres (Software End-of-Life, EOL Management, Data Migration, Compliance Closure, Data Retention Policies).
**Disponible localement** : 0 corpus-aligned.
**Couverture effective** : **0%** 🔴

**Lacunes critiques** : 5 livres non encore acquis.

**Décision mainteneur 2026-06-07** : 0% = critique globale, batch d'acquisition P10 prioritaire (avec Feathers + Sadalage de P9). Action P10-2 : acquisition des 5 livres canoniques + 2 NIST/OWASP, effort ~$400, 2-3 semaines.

---

## Alignment Reference

- **SWEBOK v4** : Pas de KA direct. Couvre Software Engineering Process (KA P9 SWEBOK) + Software Maintenance (P6 SWEBOK, fin de vie) + aspects RGPD/archivage.
- ISO/IEC/IEEE 12207:2017 (Software Life Cycle Processes)
- ISO/IEC 14764:2006 (Software Maintenance)
- RGPD (Règlement Général sur la Protection des Données, 2016/679)
- ITIL v4 (Service Transition → Service Retirement)
- NIST 800-88r1 (Guidelines for Media Sanitization)
- Data Retention Policies (juridictions multiples)

---

## Prochaines étapes

1. **Récap projet final** : P0-P10 tous à 🟢. Le projet SWEBOK v4 Harness Distilled est complet (10 phases validées). Le mainteneur peut maintenant :
   - Merger toutes les specs v2 dans main
   - Tag une version "v2.0.0-audit-complete"
   - Démarrer un nouveau projet (retour P0) si desired
   - Valider sur un projet test (P4 + P5 + P6 + P7 + P8 + P9 + P10) — nice-to-have
2. **Action P10-1** : évolution `pre-tool-use/token-counter.sh` pour supporter mode adaptatif 3-niveaux P10 (env var `SWEBOK_P10_MODE` ou flag `--criticality`).
3. **Action P10-2** : Acquisition livres P10 manquants (5 livres canoniques + 2 NIST/OWASP). Non bloquant, planifier avec P9 dans le batch d'acquisition.
4. **Action P10-3** : Formaliser Council de clôture P10 (CISO + Legal + PM + DevOps-Lead) si pas déjà fait. Vérifier que `nexus-ciso`, `legal-advisor`, `nexus-pm`, `nexus-devops-lead` peuvent être convoqués ensemble.
5. **Action P10-4** : Valider la démarcation P10↔P0 sur un projet test où un EOL est suivi d'un replacement (P10 ancien archivé + P0 nouveau projet démarré en parallèle).

---

*Section rédigée par Claude le 2026-06-07 suite à l'audit P10 vague 1 (4 questions AskUserQuestion) + transformations implicites (5.5 transformée en 4 décisions précises, 7 comblée par projection cohérence P0-P9 v2, 8.5 comblée par UDL 7).*
