# Audit — Phase 2 : Requirements

> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 2
- Nom : Requirements
- Équivalent SWEBOK v4 : P1 SWEBOK (Requirements Engineering KA)
- Spec existante : `specs/workflows/by-phase/phase-2-requirements.md`
- Date de l'audit : 04/06/2026 (révisé 2026-06-06 post-corpus)
- Auditeur : mainteneur
- Corpus-aligned : OUI — voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`
  - Couverture corpus : **78%** (post-vague 8, 2026-06-09) — cf. §39 du corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md
- Verdict global : 🟡 À ajuster (spec v2 validée, reste utilité à mesurer en pratique)

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
**Suggestions** :
- [x] A. *« Elicit, analyze, specify, and validate software requirements »* (spec actuelle)
- [ ] B. *« Transformer une intention validée en spécification testable, traçable, et signée par les stakeholders »*
- [x] C. *« Produire un SRS (IEEE 830) avec acceptance criteria, RTM 100%, backlog priorisé »*
- [x] D. *« Produire ce qu'il faut pour que la phase 3 puisse designer sans ambiguïté »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
**Suggestions** :
- [x] A. Elicitation + Analysis + Specification + Validation (spec, 4 activités)
- [x] B. + Priorisation (P0-P4)
- [x] C. + Traceability matrix
- [x] D. + Acceptance criteria
- [ ] E. **+ Tests d'acceptance (côté QA)** pour valider la testabilité — déjà inclus dans XG-2.6
- [ ] Autre : ____________________________________________

### 1.3 Hors-périmètre
**Suggestions** :
- [x] A. Architecture détaillée (phase-3)
- [x] B. Estimation effort (P4 SWEBOK, absente ici — voir point suivant)
- [x] C. Code (P5+)
- [x] D. **+ Plan de test d'acceptance détaillé** (phase-5)
- [x] E. **+ Décision de stack technique** (phase-3)
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK
- [ ] 🟡 À ajuster
- [ ] 🔴 À repenser

**Justification** : mission recentrée sur "ce qu'il faut pour que P3 puisse designer sans ambiguïté" (option D). Périmètre explicite (4 items cochés), hors-périmètre explicite (5 items). Cible universelle couverte.

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
**Suggestions** :
- [x] A. Phase 0 discovery report approuvé (spec EG-2.1)
- [x] B. Project charter ratifié (spec EG-2.2)
- [ ] C. Intent utilisateur post-découverte = "ok on y va"
- [ ] Autre : ____________________________________________

### 2.2 Critères de complétion
**Suggestions** (cocher les plus importants) :
- [x] A. SRS ≥95% IEEE 830 (XG-2.1)
- [ ] B. Peer review par ≥3 reviewers (XG-2.2)
- [x] C. RTM 100% (XG-2.3)
- [x] D. Backlog 100% priorisé P0-P4 (XG-2.4)
- [ ] E. Sign-off stakeholders primaires (XG-2.5)
- [x] F. Acceptance criteria pour chaque requirement (XG-2.6)
- [x] G. **+ Le mainteneur peut écrire le smoke test** = testabilité confirmée
- [x] H. **+ Aucun requirement "ambigu" non résolu**
- [ ] Autre : ____________________________________________

### 2.3 Conditions d'échec → escalade
**Suggestions** :
- [x] A. Stakeholder principal refuse de signer
- [x] B. Conflit de requirements non résolvable
- [x] C. RTM < 100% après 2 itérations
- [x] D. Le designer (phase 3) revient avec "ce n'est pas implémentable"
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟢 OK

**Justification** : XG-2.5 "sign-off stakeholders formels" remplacé par "moi seul + checklist 100%" (10 critères, R1-Q4). Conditions d'échec explicites. Trigger activation clair (P0 outputs validés).

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
**Suggestions** :
- [x] A. Phase 0 outputs (charter, stakeholders, scope, risks)
- [x] B. Phase 0 risk landscape (pour informer la priorisation)
- [ ] C. **Mode consultation envelope** : ne charger que la slice pertinente, pas tout
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
**Suggestions** :
- [x] A. Sign-off explicite sur chaque requirement
- [x] B. Décisions sur les conflits (priorisation, scope)
- [x] C. **+ Validation des acceptance criteria avant figeage**
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **40%** (████░░░░░░).**Sources externes disponibles localement (post-corpus) :****New Books (achats locaux)** (6 livres) — chemin `/home/doz/Bureau/New Books/` :- **Domain-Driven Design: A Pragmatic Approach (preview)** (Eduard Ghergu, 2025) — formats: PDF, EPUB- **The Agile Guide to Business Analysis and Planning** (Howard Podeswa, 2021) — formats: PDF- **Rapid Story Development** (—, 2020) — formats: PDF- **CBAP Certification and BABOK Study Guide** (Hans Jonasson, 2018) — formats: PDF- **Domain-Driven Design Distilled** (Vaughn Vernon, 2016) — formats: PDF- **BABOK v2 (2009)** (IIBA, 2009) — formats: PDF**Standards NIST/OWASP téléchargés (open access)** (1) :- OWASP ASVS 5.0**Lacunes critiques restantes (à acquérir)** (8) :- Domain-Driven Design (Evans) (2003)  -- 🔴 Le livre fondateur. Implementing DDD est acquis, mais l'original man- User Stories Applied (Cohn) (2004)  -- User stories fondateur. Acquérir.- Agile Software Requirements (Leffingwell) (2010)  -- Lean requirements. Toujours référence.- Software Requirements 3rd (Wiegers/Beatty) (2013)  -- 🔴 SRS + IEEE 830/29148. Acquérir.- Visual Models for Software Requirements (Beatty/Chen) (2012)  -- Modèles UML/BPMN. Acquérir.- ... et 3 autres. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20.
### 3.4 Verdict
- [x] 🟢 OK

**Justification** : pre-hydrate P0 obligatoire (F7 recherche 2026). Mode consultation envelope strict (3.1.C spec v2). Pas d'injection complète des 7 livrables P0, seulement la slice pertinente.

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
**Suggestions** (cocher) :
- [x] A. `requirements-spec.md` (spec)
- [x] B. `use-case-model.md` (spec)
- [x] C. `requirements-traceability-matrix.md` (spec)
- [x] D. `prioritized-backlog.md` (spec)
- [x] E. `acceptance-criteria.md` (spec)
- [x] F. `requirements-validation-report.md` (spec)
- [x] G. **+ ADR (Architecture Decision Record) si des choix structurants sont faits pendant l'elicitation**
- [ ] Autre : ____________________________________________

### 4.2 Format de stockage
**Suggestions** :
- [ ] A. Markdown
- [ ] B. JSON pour le RTM (machine-parse)
- [x] C. Les deux
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
**Suggestions** :
- [x] A. SRS complet + résumé 1 page
- [x] B. Backlog priorisé en vue tableau
- [x] C. RTM consultable via tool
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
**Suggestions** :
- [x] A. Oui — chaque requirement tracé vers source + acceptance criteria
- [x] B. Manque le "pourquoi on a écarté les alternatives"
- [x] C. Manque l'historique des décisions
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟢 OK

**Justification** : 7 livrables (6 spec + ADR, R2-Q3), format md+json partout (R2-Q4), traçabilité max + UDL (R4-Q14), résumé 1 page en tête (R4-Q13).

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
**Suggestions** (cocher) :
- [x] A. Hyperagent-Orchestrator (spec)
- [x] B. Nexus-PM (spec)
- [x] C. Nexus-Architect pour les NFR (spec)
- [x] D. Nexus-QA pour la testabilité (spec)
- [x] E. Discovery-Orchestrator pour l'elicitation (spec, required skills)
- [x] F. speckit-qa (spec, QA assurance)
- [x] G. **+ T3 Consequentialist** pour prédire les impacts phase-3
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
**Suggestions** :
- [x] A. `nexus-pm`, `nexus-architect`, `nexus-qa` (spec)
- [x] B. `discovery-orchestrator` (spec)
- [x] C. `speckit-qa` (spec)
- [x] D. **+ Outil RTM (création/maintenance)**
- [x] E. **+ Outil de questionnement structuré (interview stakeholders)**
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

**Livres canoniques disponibles localement pour cette phase** (6 livres corpus-aligned sur ~15 recommandés = **40%**) :

- **New Books** : 6 livres — voir détail §3.3 ci-dessus
- **Standards** : 1 NIST/OWASP

**Lacunes critiques (§20)** : 8 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
**Suggestions** (cocher) :
- [x] A. T1 (producteur vs casseur) — utile : un agent propose, l'autre essaie de trouver ambiguïtés
- [x] B. T2 (spec-compliance) — critique : vérification contre IEEE 830
- [x] C. T3 (conséquentialiste) — utile : prédire ce qui va pécher en phase-3/4
- [x] D. Conseil (4 reviewers : CISO, QA, Architect, DevOps) — utile pour les NFR
- [ ] Autre : ____________________________________________

### 5.5 Points de décision utilisateur (B threshold)
**Décisions tranchées par le mainteneur (2026-06-05) — 7 questions max, seuil B appliqué** :

1. **Existence d'un stakeholder manquant** vs P0 register
2. **Conflit requirement vs existant** (cas maintenance)
3. **NFR conflictuels** (perf vs cost, sécurité vs UX)
4. **Acceptance criterion contesté** (arbitrage mainteneur)
5. **Compliance spécifique** (RGPD, HIPAA, sectoriel)
6. **Scope additionnel tardif** (scope creep détecté en P2)
7. **Rejet d'un finding T1/T2 casseur** (le mainteneur maintient sa position)

L'agent peut choisir de ne pas poser les 7 si le contexte est déjà clair. Min 0, max 7. Au-delà, le système choisit en autonomie et logge dans l'UDL. (Aligné décision R2-Q4.)

### 5.6 Verdict
- [x] 🟢 OK (5.5 comblé en spec v2, 5.4 T1+T2+T3 explicités, 4 agents séquentiel + Nexus-Critic + Council NFR)

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques
**Suggestions** :
- [x] A. Pas d'architecture dans cette phase
- [x] B. Pas d'estimation effort (à moins de l'intégrer — c'est absent du modèle)
- [x] C. Pas de figeage avant sign-off stakeholder
- [x] D. Pas de NFR inventés (chaque NFR doit venir d'un besoin explicite ou d'une contrainte documentée)
- [ ] Autre : ____________________________________________

### 6.2 Modes d'échec connus
**Suggestions** :
- [x] A. Requirements gonflés (gold-plating)
- [x] B. Acceptance criteria non testables
- [x] C. Ambiguïté sémantique (le même mot, deux sens)
- [x] D. NFR oubliés (perf, security, scalabilité)
- [x] E. Scope creep (ajout de requirements en cours de phase)
- [x] F. **P4 SWEBOK manquant** : pas d'estimation, on reporte le problème
- [ ] Autre : ____________________________________________

### 6.3 Cas limites
**Suggestions** :
- [x] A. Maintenance (requirements = user stories de bugfix)
- [x] B. Exploration R&D (requirements = hypothèses à valider)
- [x] C. Compliance-driven (RGPD, HIPAA — requirements externes imposés)
- [x] D. Projet interne vs client
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
**Suggestions** :
- [ ] A. Stakeholder refuse de signer → remonte au sponsor
- [x] B. 3 ambiguïtés non résolues en 24h → escalade
- [x] C. NFR conflictuels (ex: perf vs cost) → décision mainteneur
- [ ] Autre : ____________________________________________

### 6.5 Verdict
- [x] 🟢 OK

**Justification** : 4 refus statut quo (R5-Q17), 5 critères abandon (R5-Q18), 6 cas limite universel explicite (R5-Q19), escalade documentée (3 ambiguïtés / 24h, NFR conflictuels → mainteneur).

---

## Section 7 — Adéquation aux besoins (utilité)

### 7.1 Usage réel
> ____________________________________________________________________________

### 7.2 Friction observée
> ____________________________________________________________________________

### 7.3 Pattern de contournement probable
> ____________________________________________________________________________

### 7.4 Valeur ajoutée perçue
> ____________________________________________________________________________

### 7.5 Dette d'orchestration
> ____________________________________________________________________________

### 7.6 Verdict
- [x] 🟡 À ajuster (la spec v2 est validée mais le mainteneur n'a pas encore utilisé P2 en pratique — dette d'orchestration à mesurer après 1-2 projets réels)

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. Token budget proposé : 3k base / 5k soft / 8k hard.

### 8.1 Token budget alloué
**Suggestion** : 8k. Ajuster si : __________

### 8.2 Compaction checkpoint
- [ ] A. Tous les 5 tool calls
- [ ] B. À 70% du soft cap
- [x] C. Les deux
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
- [x] A. Phase 0 outputs (charter, risks) en cache
- [x] B. RTM comme source cross-phase (réutilisable phase-3, 4, 5)
- [x] C. **Mode consultation envelope strict** (jamais injecter tout le SRS)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret
- [x] A. T1 : prod (SRS) vs breaker (trouve ambiguïtés)
- [x] B. T2 : auditeur vérifie conformité IEEE 830
- [x] C. T3 : consequentialist prédit ce qui pète en phase-3
- [x] D. Council : CISO + QA + Architect + DevOps sur les NFR
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger
**7 éléments P2-spécifiques confirmés par le mainteneur (2026-06-05, décision R3-Q4)** :

1. **Requirement ajouté ou refusé** — tout REQ accepté ou rejeté en P2, avec rationale
2. **Ambiguïté levée** — cas où 2 interprétations étaient possibles, arbitrage
3. **NFR ajouté ou refusé** — NFR (perf, scalabilité, sécurité) ajouté au SRS ou refusé
4. **Acceptance criterion contesté** — AC où Nexus-QA et mainteneur ont divergé
5. **Sign-off partiel ou refus** — sign-off obtenu avec réserve, ou refusé sur un livrable
6. **Rejet du T1/T2 casseur** — quand Nexus-Critic a trouvé un problème et comment c'est résolu
7. **Décisions "pas de décision"** — cas où on a choisi de NE PAS trancher, et pourquoi (escalade P3)

Stockés dans `.swebok_state.db` (table `udl_p2`) et consultables via Consultation Envelope (A1) par les phases suivantes. (Aligné avec P0 v2 6 éléments, étendu à 7 avec les spécificités P2.)

### 8.6 Verdict
- [x] 🟢 OK (section 8.7 findings intégrés, 8.5 UDL 7 éléments comblé en spec v2, budget 4k/7k/10k aligné, 8.2 compaction 60-70% retenu, 8.3 consultation envelope strict)

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md`.

#### Findings les plus pertinents pour cette phase
- **F13** : Single-agent ≥ multi-agent à budget tokens égal → **confirme single Nexus-PM + Discovery-Orchestrator** pour le SRS, pas de fan-out
- **F5** : Lost-in-the-middle = -30% accuracy en positions 5-15 → le SRS a beaucoup de sections, **structure pyramidale obligatoire** (acceptance criteria en tête, RTM en queue)
- **F8** : Compaction Claude Code à 95% = trop tard → ANTI-ROT trigger à 60-70% du soft cap
- **F3** : Subagent brief = OBJECT/FORMAT/TOOLS/BOUND → auditer chaque spawn (rare en P2 mais possible pour T3 Consequentialist)

#### Anti-patterns à éviter dans cette phase
- **AP7** : Contexte "flood" — ne pas injecter tout le corpus `distilled/` dans le contexte
- **AP2** : Brief vague "research X" — si T3 spawn, brief structuré obligatoire

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : un requirement mal interprété qui contamine le SRS ?
- [x] **Distraction** : trop de NFRs qui éloignent du core ?
- [x] **Confusion** : ambiguïtés sémantiques (le même mot, deux sens) ?
- [x] **Clash** : requirements contradictoires (perf vs cost, scope vs délai) ?

#### Recommandation budget (mise à jour 2026)
- **Base 4k / Soft 7k / Hard 10k** (4 agents séquentiel + Nexus-Critic + Council NFR, structure pyramidale SRS, compaction 60-70% du soft cap = 4.2k tokens, compaction checkpoint toutes les 5 actions)
- ⚠️ **Révision 2026-06-05** : budget relevé de 3k/5k/8k à 4k/7k/10k. Justification : mainteneur assume 4 agents en séquentiel (Discovery→PM→Archi→QA) + 1 Nexus-Critic + 4 council reviewers (R1-Q1). Séquentiel strict = pas de fan-out ×15 (F2 recherche 2026), surcoût = re-chargement contexte. Vigilance : 9 invocations d'agents potentielles = saturation possible, à mesurer en pratique.
- ⚠️ **Action P3-1** : token-counter.sh P2 hardcodé à mettre à jour de 3000/5000/8000 à 4000/7000/10000.

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 0 |
| New Books achetés (§19) | 6 |
| Standards NIST/OWASP (§13) | 1 |
| Open-access téléchargés | 0 |
| **TOTAL corpus-aligned local** | **7** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~15 livres
- **Disponible localement** : 6 corpus-aligned
- **Couverture effective** : **40%** ████░░░░░░

### Lacunes (§20)

- **8** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **partielles** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel


## Verdict global de la phase
- [ ] 🟢 OK — conforme, rien à changer
- [x] 🟡 À ajuster — fonctionne mais perfectible
- [ ] 🔴 À repenser — design ou utilité à revoir fondamentalement

**Justification verdict global 🟡** : la spec v2 est validée par 20 décisions tranchées (R1→R5), tous les manques de la grille sont comblés (5.5, 8.5), tous les verdicts par section sont tracés, le budget est aligné. **Mais** la section 7 (utilité) reste 🟡 car le mainteneur n'a pas encore utilisé P2 en pratique. C'est honnête : la spec est solide, sa valeur réelle reste à mesurer sur 1-2 projets.

## Liste d'actions
**🔴 P1 — bloquants (fermés le 2026-06-05 par la spec v2)** :
1. ✅ Section 5.5 comblée (7 questions utilisateur, aligné décision B seuil fort impact)
2. ✅ Section 8.5 comblée (7 éléments UDL P2-spécifiques)
3. ✅ Verdicts tranchés (sections 1-8 + global = 🟢 partout sauf 7 = 🟡)
4. ✅ Spec v2 réécrite (`specs/workflows/by-phase/phase-2-requirements.md`, 295 lignes)
5. ✅ Budget P2 mis à jour dans strategy (3k/5k/8k → 4k/7k/10k)
6. ✅ Token counter P2 hardcodé à mettre à jour (action P3-1)

**🟡 P2 — qualité (fermés par la spec v2)** :
7. ✅ T1+T2+T3 tous activés (vs spec v1 = T1 implicite seulement)
8. ✅ Nexus-Critic introduit comme 5e agent dédié (séparation des rôles)
9. ✅ Council 4 reviewers sur NFR conflictuels (vs spec v1 = absent)
10. ✅ 7 livrables (6 spec + ADR) en format md+json (vs spec v1 = 6 md uniquement)
11. ✅ Couverture universelle adaptative explicite (6 cas : greenfield, maintenance, interne, externe, compliance, R&D)
12. ✅ Traçabilité max + alternatives documentées par décision structurante

**🟢 P3 — nice-to-have (à fermer post-v2)** :
13. ⬜ Token counter P2 hardcodé à 4k/7k/10k dans `pre-tool-use/token-counter.sh` ligne 57 (P3-1)
14. ⬜ Mesurer l'usage réel de P2 sur 1-2 projets pour fermer la section 7 (utilité)
15. ⬜ Vérifier la saturation des 9 agents potentiels (mesurer hard cap atteint)
16. ⬜ Étendre la même méthode d'audit 4 failure modes Drew Breunig à P3-P9 (référence : P0 v2 + P2 v2)

## Notes libres
> Phase 2 Requirements = v2 validée 2026-06-05. 20 décisions tranchées (cf. spec v2).
> 12 actions P1+P2 fermées par la spec v2. 4 actions P3 restantes (token counter, mesure réelle, saturation agents, méthode reproductible).
> Verdict global 🟡 (à ajuster — spec solide, utilité à mesurer).
> Cible universelle adaptative (6 cas). Budget 4k/7k/10k tokens, cap 35 min, 4 agents séquentiel + Nexus-Critic + Council NFR.
> 7 livrables (6 spec + ADR) en md+json. T1+T2+T3 + Council. Traçabilité max + UDL 7 éléments.
> Tension notée : 9 invocations d'agents potentielles (4+1+4) à 4k/7k/10k = saturation possible. Action P3-15.
> Méthode d'audit reproductible : 5 rounds × 4 questions = 20 décisions tranchées (cf. P0 v2 et P2 v2).
> Prochaine phase d'audit suggérée : P3 (Design) ou P4 (Implementation), selon la priorité du mainteneur.