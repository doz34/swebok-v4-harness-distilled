# Audit — Phase 9 : Maintenance

> **Statut** : v2 finale — 2026-06-07 (verdict 🟢 atteint dès la première conversation, audit clos via grille offline + 4 questions vague 1 + transformations implicites).
> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 9
- Nom : Maintenance
- Équivalent SWEBOK v4 : P6 (Software Maintenance KA)
- Spec existante : `specs/workflows/by-phase/phase-9-maintenance.md` (v2 finale, 2026-06-07)
- Date de l'audit : 2026-06-07
- Auditeur : mainteneur
- Couverture corpus : **95%** (post-vague 8, 2026-06-09) — cf. §39 du corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md
- **Verdict global** : 🟢 (atteint dès la première conversation, 4 décisions tranchées vague 1)

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
**Suggestions** :
- [x] A. *« Sustain and enhance software through corrective, adaptive, perfective, and preventive maintenance »* (spec actuelle)
- [x] B. *« Tout changement de code planifié sur un système en production, en 4 catégories : correctif, adaptatif, perfectif, préventif »*
- [x] C. *« Améliorer le système sans casser ce qui marche, avec traçabilité de chaque changement »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
- [x] A. Maintenance request processing + change implementation + testing + documentation (spec, 4 activités)
- [x] B. Corrective (bugfix), Adaptive (env), Perfective (feature mineure), Preventive (refactoring) (spec)
- [x] C. **+ Change Advisory Board (CAB)** si structurant
- [x] D. **+ Maintenance log** (historique)
- [x] E. **+ Impact analysis** avant tout changement
- [x] F. **+ Rollback plan** pour chaque changement
- [ ] Autre : ____________________________________________

### 1.3 Hors-périmètre
- [x] A. Opérations courantes (phase-7)
- [x] B. Refonte majeure (retour phase-3/4)
- [x] C. **+ Nouvelles features structurantes** (retour phase-2/3/4)
- [x] D. **+ End-of-life** (phase-9)
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK
- [ ] 🟡 À ajuster
- [ ] 🔴 À repenser

**🆕 Corrigé v2 finale 2026-06-07** : (1) §1.3.D "End-of-life (phase-9)" corrigé en "End-of-life (phase-10)" suite au fix structurel 9→10 phases. (2) Démarcation P8↔P9 (Run vs Change) et P9↔P10 (prolonger vs préparer la mort) explicites dans la spec v2 finale.

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] A. Phase 7 ops stable 30+ jours (spec EG-8.1)
- [x] B. Maintenance request reçue (spec EG-8.2)
- [x] C. Impact analysis complétée (spec EG-8.3)
- [x] D. Window approuvée (spec EG-8.4)
- [x] E. Ressources allouées (spec EG-8.5)
- [x] F. CAB approval (spec EG-8.6) — pour changements structurants
- [x] G. **+ Bug critique** (expedited, bypass partiel)
- [ ] Autre : ____________________________________________

### 2.2 Critères de complétion
- [x] A. 100% changements déployés (XG-8.1)
- [x] B. Régression 100% pass (XG-8.2)
- [x] C. Documentation à jour (XG-8.3)
- [x] D. Log mis à jour sous 24h (XG-8.4)
- [x] E. Système restauré (XG-8.5)
- [x] F. Post-maintenance review approved (XG-8.6)
- [x] G. **+ Aucun nouveau défaut introduit**
- [x] H. **+ Le mainteneur peut dire "c'est patché proprement"**
- [ ] Autre : ____________________________________________

### 2.3 Conditions d'échec → escalade
- [x] A. Régression après déploiement
- [x] B. Nouveau défaut critique introduit
- [x] C. Documentation pas mise à jour
- [x] D. **+ Changement qui dégénère en refonte** → retour phase-3
- [x] E. **+ End-of-life anticipé** → phase-9
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟢

**🆕 Corrigé v2 finale 2026-06-07** : (1) §2.3.E "EOL anticipé → phase-9" corrigé en "EOL anticipé → phase-10 (Retirement)". (2) EG-9.1 à EG-9.9 (9 entry criteria) + XG-9.1 à XG-9.9 (9 exit criteria) explicites. (3) §2.2.G "Aucun nouveau défaut introduit" (vérification 48h post-deploy, XG-9.7) + §2.2.H "Le mainteneur peut dire 'c'est patché proprement'" (PMR sign-off, XG-9.6) sont des critères humains/qualitatifs informels → conservés comme intention mais pas dans XG officiel.

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. Maintenance request (depuis phase-7 ou user)
- [x] B. Impact analysis (depuis ops + dev)
- [x] C. Phase 7 incident log (corrélation)
- [x] D. **+ Code history** (git log)
- [x] E. **+ Phase 5 regression suite** (pour valider)
- [x] F. **+ Phase 6 deployment process** (pour appliquer)
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
- [x] A. Approbation du changement (sponsor si impact)
- [x] B. Priorité si plusieurs changements concurrents
- [ ] C. **+ Acceptation de dette** si perfective mineure
- [x] D. **+ Validation du rollback plan**
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **30%** (███░░░░░░░).**Sources externes disponibles localement (post-corpus) :****New Books (achats locaux)** (3 livres) — chemin `/home/doz/Bureau/New Books/` :- **Refactoring at Scale** (Maude Lemaire, 2020) — formats: PDF- **Retrospectives Antipatterns** (Aino Vonge Corry, 2020) — formats: PDF- **Beyond Legacy Code** (David Scott Bernstein, 2015) — formats: PDF**Standards NIST/OWASP téléchargés (open access)** (1) :- NIST 800-161r1 (SCRM)**Lacunes critiques restantes (à acquérir)** (2) :- Working Effectively with Legacy Code (Feathers) (2004)  -- 🔴 Indispensable pour P9. Acquérir absolument.- Refactoring Databases (Sadalage) (2006)  -- Schéma evolution. Acquérir.
### 3.4 Verdict
- [x] 🟢

**🆕 Corrigé v2 finale 2026-06-07** : §3.2.C "Acceptation de dette" ajoutée à la liste des inputs user (cohérent avec UDL 7 + Q4 user 5.5 EOL approche). §3.3 corpus 30% maintenu (3 livres New Books + 1 NIST/OWASP + 2 lacunes critiques Feathers + Sadalage, planifiées pour acquisition future, non bloquant pour cadrage v2).

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
- [x] A. `maintenance-request.md` (spec)
- [x] B. `impact-analysis.md` (spec)
- [x] C. `change-implementation-report.md` (spec)
- [x] D. `regression-test-report.md` (spec)
- [x] E. `maintenance-log.md` (spec)
- [x] F. `updated-documentation.md` (spec)
- [x] G. **+ Diff / patch** (le vrai livrable)
- [x] H. **+ Tag de release** (git tag)
- [x] I. **+ Decision rationale** (pourquoi cette approche)
- [ ] Autre : ____________________________________________

### 4.2 Format de stockage
- [x] A. Git (PR + commits + tags)
- [x] B. Markdown pour les docs
- [x] C. JSON pour les rapports machine
- [x] D. **+ ADR si décision structurante**
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
- [x] A. PR par changement
- [x] B. Maintenance log cumulatif
- [x] C. **+ Changelog public** (si user-facing)
- [x] D. **+ Post-mortem si incident**
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
- [x] A. Oui — git history + maintenance log
- [x] B. Manque la justification du choix de priorité
- [x] C. Manque la mesure d'efficacité du changement
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟢

**🆕 Corrigé v2 finale 2026-06-07** : §4.4.B "manque justification du choix de priorité" → résolu par UDL 1-7 (rationale tracé). §4.4.C "manque mesure efficacité du changement" → résolu par UDL 6 "regression test result" + audit trail git (commit hash + tag + PR URL). 6 livrables standard + 5 ajouts (diff/patch + decision rationale + ADR si structurante + changelog public + post-mortem si incident) = 11 livrables total.

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
- [x] A. Hyperagent-Orchestrator (spec)
- [x] B. Nexus-Backend, Nexus-Frontend (spec)
- [x] C. Nexus-DevOps pour infra (spec)
- [x] D. Nexus-Security pour security patches (spec)
- [x] E. Nexus-QA pour testing (spec)
- [x] F. Nexus-PM pour priorisation (spec)
- [x] G. **+ T1 (Patch Author vs Regression Breaker)** : un agent patch, l'autre essaie de casser
- [x] H. **+ T2 (Spec-Compliance)** : le patch respecte-t-il le design original ?
- [x] I. **+ T3 (Regressions Predictor)** : qu'est-ce qui va casser dans 7 jours ?
- [x] J. **+ Limiter à 2-3 agents** (changement = focus, pas orchestra)
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
- [x] A. `nexus-backend`, `nexus-frontend`, `nexus-devops` (spec)
- [x] B. `nexus-security`, `nexus-qa`, `nexus-pm` (spec)
- [x] C. **+ Git tools** (diff, log, blame)
- [x] D. **+ Test suite** (regression)
- [x] E. **+ Security scanner** (si patch sécu)
- [x] F. **+ L0 corpus** via tool (refactoring patterns)
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

**Livres canoniques disponibles localement pour cette phase** (3 livres corpus-aligned sur ~10 recommandés = **30%**) :

- **New Books** : 3 livres — voir détail §3.3 ci-dessus
- **Standards** : 1 NIST/OWASP

**Lacunes critiques (§20)** : 2 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
- [x] A. T1 applicable (patch vs regression breaker)
- [x] B. T2 critique (spec-compliance)
- [x] C. T3 applicable (regression predictor)
- [x] D. **+ Council pour les changements structurants**
- [x] E. **+ Context isolation** : le breaker n'a pas accès au raisonnement du patch
- [ ] Autre : ____________________________________________

### 5.5 Points de décision utilisateur (B threshold)

**🆕 Comblé v2 finale 2026-06-07** : 4 décisions opérationnelles précises (B threshold = haute valeur opérationnelle, symétrie P8). Format AskUserQuestion (header + 2-4 options mutuellement exclusives par question).

#### Q1 — Type de maintenance + rationale
- **Header** : "Type maintenance"
- **Question** : "Pour le changement [changement-id], quel type de maintenance ?"
- **Options** : (a) **Corrective** (bugfix, fix incident, fix défaut) ; (b) **Adaptive** (migration, upgrade dépendance, adaptation env) ; (c) **Perfective** (feature mineure, refactoring, optimisation) ; (d) **Preventive** (refactoring proactif, dette technique, hardening)
- **Trigger** : Nouvelle CR reçue
- **Impact** : Long terme (scope, agents, tests). UDL 1 logge type + rationale + déclencheur.

#### Q2 — Criticité du changement (détermine agents + budget)
- **Header** : "Criticité"
- **Question** : "Pour le changement [changement-id], quelle criticité ?"
- **Options** : (a) **Hotfix / typo / micro-tâche** (1k/2k/3k --lite, single sans Critic) ; (b) **Standard** (3k/5k/8k single + Nexus-Critic T1+T2+T3) ; (c) **Structurant / Perfective lourde** (5k/8k/15k multi + Critic T1+T2+T3 + Council)
- **Trigger** : Type maintenance identifié (Q1), impact analysis préliminaire
- **Impact** : Court terme (budget + agents), engagement ressources. UDL 2 logge criticité + budget + agents.

#### Q3 — CAB approval (changement structurant)
- **Header** : "CAB approval"
- **Question** : "Pour le changement [changement-id] structurant, CAB approval requise ?"
- **Options** : (a) **Oui, structurante** (Council CISO + DevOps-Lead + Architect, examen 1h, signature obligatoire) ; (b) **Oui, standard** (approbation mainteneur seul, sans Council) ; (c) **Non, hotfix urgent** (fast-track sans CAB, escalade mainteneur si urgence vitale, post-mortem obligatoire) ; (d) **Non, documentation seule** (pas de CAB, traçabilité git suffit)
- **Trigger** : Criticité = structurant ou perfective (Q2), ou détection scope creep
- **Impact** : Court terme (bloquant ou non pour le deploy). UDL 3 logge décision CAB + signataires + rationale.

#### Q4 — EOL approche → escalade P10 ?
- **Header** : "EOL approche"
- **Question** : "Le système [system-id] approche-t-il de l'EOL sans plan de remplacement ?"
- **Options** : (a) **Non, système vivant** (P9 continue, pas d'escalade) ; (b) **Oui, avec plan de remplacement** (P9 continue, plan informe scope, features gelées, security only) ; (c) **Oui, sans plan de remplacement** (escalade P10 immédiate, gel nouveaux patches, focus archivage) ; (d) **Zone grise, à arbitrer** (escalade mainteneur pour décision EOL)
- **Trigger** : Post-mortem récurrent (>3 P2 en 30j), dette chronique, dépendance dépréciée, signaux P8 UDL 7
- **Impact** : Long terme irréversible (déclenche P10). UDL 7 logge décision EOL + rationale + impact business estimé.

### 5.6 Verdict
- [x] 🟢

**🆕 Corrigé v2 finale 2026-06-07** : (1) §5.5 transformée en 4 décisions opérationnelles précises (vs vide en v1, symétrie P8). (2) Mécanique agent adaptative 3-niveaux (hotfix single --lite, standard single + Critic T1+T2+T3, structurant multi + Critic T1+T2+T3 + Council). (3) Nexus-Critic T1 casseur patch + T2 conformité DDS P4 + ADRs P3 + NFR P2 + T3 prédiction aval P10 OBLIGATOIRE sauf mode --lite (cohérence P3-P7). (4) Agents principaux : Nexus-Backend/Frontend/DevOps selon zone OU Nexus-Architect si structurant.

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques
- [x] A. Pas de refonte déguisée (retour phase-3)
- [x] B. Pas de feature non-justifiée
- [x] C. Pas de modification sans impact analysis
- [x] D. **+ Pas de "fix rapide" sans doc** (dette explicite)
- [x] E. **+ Pas de skip de régression**
- [x] F. **+ Pas de deploy en prod sans staging validé**
- [ ] Autre : ____________________________________________

### 6.2 Modes d'échec connus
- [x] A. Scope creep (le "petit fix" devient une feature)
- [x] B. Patch cosmétique (cacher le problème)
- [x] C. Régression en cascade
- [x] D. **+ Maintenance debt** (fix accumulés non refactorés)
- [x] E. **+ Hotfix mal testé** qui devient prod
- [x] F. **+ Conflit avec phase-9** (patcher ce qui devrait EOL)
- [ ] Autre : ____________________________________________

### 6.3 Cas limites
- [x] A. Security patch urgent (CVE critique)
- [x] B. Bug intermittent (difficile à reproduire)
- [x] C. Legacy code sans test
- [x] D. Hotfix pendant incident
- [x] E. **+ Maintenance d'un système en fin de vie** (à arbitrer)
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
- [x] A. Régression après patch → hotfix d'urgence
- [x] B. Scope creep détecté → retour phase-3
- [x] C. EOL approche → escalade phase-9
- [x] D. **+ Security patch non applicable** → escalade CISO
- [ ] Autre : ____________________________________________

### 6.5 Verdict
- [x] 🟢

**🆕 Corrigé v2 finale 2026-06-07** : (1) §6.3.E "Maintenance d'un système en fin de vie (à arbitrer)" résolu en spec v2 finale : AVEC plan de remplacement actif = P9 (prolonge), SANS plan de remplacement = P10 (prépare la mort). Critère de démarcation P9↔P10 explicite (Q4 user 5.5). (2) 6 refus grille + 4 garde-fous logiques (10 total) : pas de modif code sans impact analysis, pas de refonte déguisée, pas de feature structurante, pas de fix sans regression, pas de fix rapide sans doc, pas de deploy prod sans staging, pas de skip CAB, pas de modif système EOL, pas de hotfix sauvage, pas de modif NFR P2. (3) Critères échec 4 + abandon 7 documentés.

---

## Section 7 — Adéquation aux besoins (utilité)

**🆕 Comblé v2 finale 2026-06-07** : projection + cohérence P0-P8 v2 (pattern reproductible validé).

### 7.1 Usage réel projeté
Tableau 6 profils (effort en % du temps total projet) :

| Profil | Effort P9 (% projet) | Notes |
|--------|----------------------|-------|
| Greenfield from-scratch | 5-10% projet | Système jeune, peu de maintenance |
| Maintenance legacy | 25-40% projet | Dette accumulée, correctifs fréquents, refactoring régulier |
| Projet interne | 10-20% projet | Maintenance standard, hotfix fréquent, refactoring ciblé |
| Projet externe client | 15-30% projet | Maintenance structurante, communication, changelog soigné |
| Compliance-driven | 20-35% projet | Maintenance ultra-traçée, CAB + Council systématique, audit log |
| R&D / exploration | 5-15% projet | Best-effort, dette acceptée, escalade P10 lente |

**Plage globale** : 5-40% projet selon profil. Plus faible que P5 (30-60%) et P6 (20-40%) mais récurrent (plusieurs cycles de maintenance sur la vie du système). Cohérent avec P8 (5-40% temps équipe/mois, continu).

### 7.2 Friction observée (projection)
4 frictions probables identifiées (projection cohérence P0-P8) :

1. **F1 — Scope creep** : le "petit fix" devient feature (refus 2, critère abandon 1) — mitigation Q1 type maintenance, T1 casseur, impact analysis
2. **F2 — CAB bottleneck** : CAB approval lente bloque les déploiements — mitigation Q3 CAB avec fast-track hotfix, pré-validation Council en parallèle
3. **F3 — Dette chronique** : patches correctifs qui s'empilent, refactoring préventif jamais priorisé — mitigation Q1 type preventive, Q4 EOL approche
4. **F4 — Régression non détectée** : patch qui casse en prod — mitigation regression 100% PASS, T1 casseur, vérification 48h, post-mortem si incident

### 7.3 Pattern de contournement probable (projection)
4 contournements probables identifiés :

1. **C1 — Hotfix sauvage** (patch urgence sans process) → refus 9 + refus 5 + audit trail HMAC
2. **C2 — Refonte déguisée** (refactoring majeur étiqueté maintenance) → refus 2 + T1 casseur + Q1 type
3. **C3 — Documentation différée** (doc pas mise à jour pendant des semaines) → XG-9.3 24h + abandon 3 + checklist 11
4. **C4 — EOL ignoré** (système en fin de vie, patches qui s'empilent) → Q4 EOL approche + T3 prédiction aval P10 + UDL 7

### 7.4 Valeur ajoutée perçue (projection)
P9 v2 apporte 7 valeurs ajoutées vs v2-renum :
- **Démarcation P8↔P9 ET P9↔P10 explicite** : plus d'ambiguïté (Run vs Change vs Retire)
- **Nexus-Critic T1+T2+T3 obligatoire** (cohérence P3-P7) : pas de patch non-vérifié, prédiction aval P10 incluse
- **Budget adaptatif 3-niveaux** (symétrie P8) : 1k/2k/3k hotfix, 3k/5k/8k standard, 5k/8k/15k structurant
- **4 décisions opérationnelles tranchées** (type + criticité + CAB + EOL) : structure les choix
- **11 livrables (6+5)** : 6 standard + 5 ajouts (diff/patch + decision rationale + ADR + changelog + post-mortem)
- **UDL 7 éléments** : traçabilité complète
- **Audit trail HMAC chain** : compliance + transparence

### 7.5 Dette d'orchestration projetée
3 risques de dette identifiés (projection) :
1. **R1 — Criticité surévaluée** : patchs étiquetés "structurant" pour avoir Council + budget 15k — mitigation Q2 avec critères explicites
2. **R2 — Dette acceptée chronique** : preventive jamais priorisé → escalade P10 inevitable — mitigation Q1 preventive + Q4 EOL
3. **R3 — Hotfix systématique** : abus --lite pour éviter rigor — mitigation Q2 critères explicites, audit trail HMAC

### 7.6 Verdict
- [x] 🟢

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. Token budget proposé : 3k base / 5k soft / 8k hard.

### 8.1 Token budget alloué
**🆕 Tranché v2 finale 2026-06-07** : **adaptatif 3-niveaux par criticité** (symétrie P8) :
- **Hotfix / typo / micro-tâche** : 1k base / 2k soft / 3k hard (single --lite sans Critic)
- **Corrective / Adaptive / Preventive standard** : 3k base / 5k soft / 8k hard (single + Nexus-Critic T1+T2+T3, ~4.5k)
- **Structurant / Perfective lourde / Refactoring majeur** : 5k base / 8k soft / 15k hard (multi + Critic T1+T2+T3 + Council structurante, ~5.5k)

**Action P9-1** : `pre-tool-use/token-counter.sh` ligne 67 actuelle = `P9: 3000/5000/8000` (single par défaut). Pour supporter le mode adaptatif 3-niveaux, évolution nécessaire (env var `SWEBOK_P9_MODE=hotfix|standard|structurant` ou flag `--severity`). En attendant, le défaut 3k/5k/8k couvre 50% des cas.

### 8.2 Compaction checkpoint
- [x] A. Tous les 5 tool calls
- [x] B. À 70% du soft cap
- [x] C. **+ Compaction agressive des diffs intermédiaires**
- [x] D. **+ Hot path mode** pour les micro-changements (typo, config)
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
- [x] A. Phase 5 regression suite (slice)
- [x] B. **+ Phase 4 code** (le module à patcher)
- [x] C. **+ Phase 7 incident log** (corrélation)
- [x] D. **+ Pas de re-chargement du design complet** (slice)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret
- [x] A. T1 : Patch Author vs Regression Breaker
- [x] B. T2 : Spec-Compliance (le patch respecte l'arch ?)
- [x] C. T3 : Regression Predictor (que va péter ?)
- [x] D. **+ Mutation testing** sur le patch
- [x] E. **+ Context isolation** : contexte distinct prod vs patch
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger

**🆕 Comblé v2 finale 2026-06-07** : 7 éléments P9-spécifiques (aligné P3, P4, P5, P6, P7, P8).

| Élément | Description | Source |
|---------|-------------|--------|
| **Maintenance type chosen** | Type retenu (corrective/adaptive/perfective/preventive) + rationale + déclencheur | Q1 user 5.5 |
| **Criticité + budget allocated** | Criticité assignée (hotfix/standard/structurant) + budget + agents | Q2 user 5.5 |
| **CAB approval status** | CAB approval obtenue + signataires + rationale | Q3 user 5.5 |
| **Impact analysis result** | Scope, modules touchés, risque régression, dette ajoutée | EG-9.3 / Activity 9.1 |
| **Change implemented** | Commit hash + tag + PR URL (audit trail git) | Activity 9.2 |
| **Regression test result** | Résultats (PASS/FAIL, taux, nouveaux défauts, 48h post-deploy) | XG-9.2 / XG-9.7 |
| **EOL approach status** | EOL approche ou pas + escalade P10 si oui | Q4 user 5.5 |

Stockés dans `.swebok_state.db` (table `udl_p9`) et consultables via Consultation Envelope (A1) par P8 Operations (qui monitor la santé post-patch) et P10 Retirement (si escalade EOL).

### 8.6 Verdict
- [x] 🟢

**🆕 Corrigé v2 finale 2026-06-07** : (1) §8.1 budget adaptatif 3-niveaux (vs 8k uniforme v1, symétrie P8). (2) §8.5 UDL 7 éléments comblé (vs vide v1). (3) §8.7 findings F12, F13, F6 appliqués. (4) Mutation testing sur le patch maintenu (hérité P6 XG-6.3).

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md`.

#### Findings les plus pertinents pour cette phase
- **F13** : Single-agent ≥ multi-agent à budget tokens égal → **confirme single Nexus par patch** (Backend OU Frontend OU DevOps), sauf refonte structurante qui passe en mode multi
- **F6** : Mur à 35 min → scope limité par patch, checkpoint obligatoire si dérive
- **F12** : BM25 > embedding sur code → pour trouver le bug, `grep` + git log + AST > embedding search
- **F10** : Subagent output → filesystem → le patch est un commit git + entrée dans le maintenance log, le retour au lead = hash du commit
- **F9** : Forward worker→user (~50% économie) → si le patch est simple et la régression OK, forward direct

#### Anti-patterns à éviter dans cette phase
- **AP1** : Multi-agent pour un bugfix simple — single Nexus
- **AP2** : Brief vague "fix bug X" — brief doit spécifier la reproduction, le scope, les tests à passer
- **AP3** : Transcripts complets à chaque wakeup — digest de la cause racine
- **AP5** : Compaction tardive (95%) — trigger à 60-70% (= 3k)
- **AP8** : Charger tout le code du module pour un patch de 5 lignes — slice uniquement

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : un fix qui introduit d'autres bugs (régression) ?
- [x] **Distraction** : scope creep (le "petit fix" devient une feature) ?
- [x] **Confusion** : root cause mal identifiée, fix cosmétique ?
- [x] **Clash** : patch qui contredit la dette documentée ?

#### Recommandation budget (mise à jour 2026)
- **Base 3k / Soft 5k / Hard 8k** (single agent par patch, hot path --lite pour typo/config, pre-hydrate du module slice, compaction 60-70% = 3k)

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 0 |
| New Books achetés (§19) | 3 |
| Standards NIST/OWASP (§13) | 1 |
| Open-access téléchargés | 0 |
| **TOTAL corpus-aligned local** | **4** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~10 livres
- **Disponible localement** : 3 corpus-aligned
- **Couverture effective** : **30%** ███░░░░░░░

### Lacunes (§20)

- **2** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **partielles** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel
- **🆕 2026-06-07** : couverture 30% **acceptée pour cadrage v2**. P9 = patch + regression, pas création archi. Acquisition Feathers + Sadalage dans le batch ultérieur (action P9-3).


## Verdict global de la phase
- [x] 🟢

**🆕 Atteint v2 finale 2026-06-07** : verdict 🟢 dès la première conversation (cohérent pattern reproductible P3/P4/P5/P6/P7/P8 v2). 4 décisions tranchées vague 1 (démarcation P9↔P10, Nexus-Critic T1+T2+T3 obligatoire, budget adaptatif 3-niveaux, 4 décisions user 5.5) + transformations implicites (sections 5.5 + 7 + 8.5 comblées, audit Drew Breunig 4 modes, refus 10, échecs 4 + abandons 7, 11 livrables, 15 hooks, 9 exit criteria, 6 cas couverture universelle).

## Liste d'actions
1. **P9-1** : `pre-tool-use/token-counter.sh` ligne 67 actuelle = `P9: 3000/5000/8000` (single par défaut). Évolution nécessaire pour supporter le mode adaptatif 3-niveaux (env var `SWEBOK_P9_MODE=hotfix|standard|structurant` ou flag `--severity`). Action non bloquante.
2. **P9-2** : Mettre à jour la stratégie `audit/00-context-engineering-strategy.md` : budget P9 3k/5k/8k uniforme → adaptatif 3-niveaux (1k/2k/3k hotfix + 3k/5k/8k standard + 5k/8k/15k structurant), T1+T2+T3 P9 tranchée (obligatoire sauf --lite), section 9 "Tranchées P9" ajoutée, section 12.6 P9 passe de "Single" à "Adaptatif par criticité (3-niveaux, symétrie P8)".
3. **P9-3** : Acquisition livres P9 manquants (Feathers Legacy Code 2004 + Sadalage Refactoring Databases 2006). Non bloquant, planifier avec P10 dans le batch d'acquisition. P9 = patch + regression, pas création archi, donc couverture 30% est suffisante pour le cadrage v2.
4. **P9-4** : Council structurante P9 (CISO + DevOps-Lead + Architect) — formaliser le skill agent si pas déjà fait. Vérifier que `nexus-ciso`, `nexus-devops-lead`, `nexus-architect` peuvent être convoqués ensemble.

## Notes libres
> P9 = phase la moins bien couverte du projet (30% corpus vs 70% P8, 73% P7, 100% P3, 100% P5). Mais c'est intentionnel : P9 = patch + regression, pas création archi. Les 2 lacunes critiques (Feathers + Sadalage) sont connues, planifiées pour acquisition future. La couverture 30% est suffisante pour le cadrage v2.
>
> P9 = single-agent justifié (F13 recherche 2026) avec adaptation 3-niveaux (symétrie P8). Nexus-Critic T1+T2+T3 obligatoire cohérence P3-P7 (sauf --lite hotfix). Hot path --lite pour typo/config/doc = économie 1k au lieu de 3k.
>
> **Spécificité P9** : c'est la phase où le mainteneur passe le plus de temps opérationnel (avec P8). C'est aussi la phase qui consomme le plus les CR émises par P8 (post-mortems, capacity, incidents systémiques). Démarcation P8↔P9 (Run vs Change) et P9↔P10 (prolonger vs préparer la mort) explicites ferment les frontières contestées.
>
> **Décision marquante vague 1** : choix "Question centrale" pour démarcation P9↔P10 (vs "Activité concrète" ou "État du système"). Critère : "P9 prolonge la vie du système, P10 prépare la mort". Cas limite "Maintenance d'un système en fin de vie AVEC plan de remplacement" = P9 (prolonge), SANS plan de remplacement = P10 (prépare la mort).
