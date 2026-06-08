# Audit — Phase 1 : Concept/Feasibility

> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 1
- Nom : Concept/Feasibility
- Équivalent SWEBOK v4 : Software Engineering Management KA (P8) — feasibility, alternatives, business case
- Spec existante : `specs/workflows/by-phase/phase-1-concept-feasibility.md`
- Date de l'audit : 2026-06-05
- Auditeur : Claude (post-cadrage)
- Verdict global : 🟡 À valider (grille créée, à confirmer avec le mainteneur)

---

## ⚠️ Findings pré-identifiés

1. **Phase 1 (harness) NOUVELLE** : créée le 2026-06-05 lors du fix structurel pour combler le gap entre Discovery (P0) et Requirements (P2). À valider : la phase de faisabilité est-elle vraiment nécessaire, ou P0+P2 suffit ? Réponse attendue via ce round d'audit.
2. **Concurrence serrée** : la phase doit être rapide (cap 35 min, 3k/5k/8k tokens). Tension entre exhaustivité de la faisabilité et rapidité de la décision. Justification budget serré.
3. **Go/no-go = binaire** : la phase produit une décision, pas une exploration. Risque : sur-protection (faisabilité riche) vs sous-protection (go-decision trop rapide). À équilibrer.

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
- [x] A. *« Valider la faisabilité d'un projet cadré (P0) sous ses dimensions techniques, économiques, organisationnelles, et réglementaires — pour produire une décision go/no-go documentée »* (spec actuelle)
- [ ] B. *« Filtrer les projets infaisables AVANT d'investir dans les specs détaillées (P2) »*
- [ ] C. *« Produire un business case et une stack candidate — décision mainteneur seule »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
- [x] A. Faisabilité technique (PoC, contraintes dures, dépendances)
- [x] B. Faisabilité économique (TCO, ROI, payback)
- [x] C. Faisabilité organisationnelle (compétences, sponsor, résistance)
- [x] D. Faisabilité réglementaire (RGPD, sectoriel, juridique)
- [x] E. Alternatives analysis (build vs buy vs nothing)
- [x] F. Business case + tech stack candidate
- [x] G. Décision go/no-go
- [ ] Autre : ____________________________________________

### 1.3 Hors-périmètre
- [x] A. Specs détaillées (P2)
- [x] B. Architecture (P3)
- [x] C. Design détaillé (P4)
- [x] D. Code (P5+)
- [x] E. Estimation effort détaillée (absent du modèle, P5 fait ses propres estimations)
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK (mission claire, périmètre explicite)

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] A. P0 Discovery validé (7 livrables + checklist 100%)
- [x] B. Intent clairement exprimée
- [x] C. Top-3 risques identifiés (risk-preliminary.md)
- [ ] Autre : ____________________________________________

### 2.2 Critères de complétion
- [x] A. feasibility-study.md (4 dimensions couvertes)
- [x] B. alternatives-analysis.md (≥2 options comparées)
- [x] C. business-case.md (ROI + payback)
- [x] D. tech-stack-candidate.md (Top-1 recommandée)
- [x] E. poc-results.md si applicable
- [x] F. go-no-go-decision.md signé par le mainteneur
- [x] G. UDL 6 éléments loggés
- [ ] Autre : ____________________________________________

### 2.3 Conditions d'échec → escalade
- [x] A. Faisabilité technique impossible (PoC échoue)
- [x] B. ROI négatif et pas d'alternative
- [x] C. Sponsor manquant / opposition forte non résolvable
- [x] D. Contraintes réglementaires incompatibles (data residency, sectoriel)
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟢 OK (trigger + complétion + échec explicites)

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. P0 Discovery outputs (charter, scope, risks, problem-statement, success-criteria, discovery-report)
- [x] B. P0 risk landscape
- [x] C. P0 stakeholder register
- [x] D. P0 UDL (intention, contraintes dures, scope in/out)
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
- [x] A. Validation de la go/no-go decision
- [x] B. Décision sur la stack candidate (accepter ou challenger)
- [x] C. Sponsor identifié et engagé (sinon critère d'abandon)
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **20%** (██░░░░░░░░).**Sources externes disponibles localement (post-corpus) :****New Books (achats locaux)** (3 livres) — chemin `/home/doz/Bureau/New Books/` :- **Practical Software Project Estimation** (—, 2024) — formats: EPUB- **Software Project Estimation (Dimitrov)** (Dimitre Dimitrov, 2024) — formats: PDF, EPUB- **Software Project Estimation** (Alain Abran, 2015) — formats: EPUB**Lacunes critiques restantes (à acquérir)** (1) :- Agile Estimating and Planning (Cohn) (2005)  -- Estimation agile. Toujours référence.
### 3.4 Verdict
- [x] 🟢 OK (inputs P0 + sources externes + UDL)

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
- [x] A. `feasibility-study.md` (4 dimensions)
- [x] B. `alternatives-analysis.md` (≥2 options)
- [x] C. `business-case.md` (ROI, payback, TCO 3 ans)
- [x] D. `tech-stack-candidate.md` (Top-1 stack + rationale)
- [x] E. `poc-results.md` (si applicable)
- [x] F. `go-no-go-decision.md` (signature mainteneur)
- [ ] Autre : ____________________________________________

### 4.2 Format de stockage
- [x] A. Markdown pour tous les livrables (lisibles par mainteneur)
- [ ] B. JSON pour la go/no-go decision (machine-parse pour le state engine)
- [x] C. Les deux : md pour humain, JSON pour go/no-go (référence state)
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
- [x] A. Résumé 1 page (feasibility-study.md) en tête
- [x] B. Go/no-go decision en évidence (vert ou rouge)
- [x] C. Business case chiffré en annexe
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
- [x] A. Oui — alternatives documentées, sign-off maintenu
- [x] B. Manque le "pourquoi on a écarté X" → couvert par alternatives-analysis.md
- [x] C. Manque l'historique des décisions → couvert par UDL 6
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟢 OK (6 livrables clairs, format md+json partiel, auditabilité OK)

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
- [x] A. Discovery-Orchestrator (lead, animation)
- [x] B. Nexus-Architect (faisabilité technique + stack)
- [x] C. Nexus-PM (faisabilité économique + business case)
- [x] D. Nexus-Security (faisabilité réglementaire)
- [x] E. (optionnel) Nexus-DevOps pour PoC infra
- [ ] F. **+ Limiter à 4 agents max** (budget serré 3k/5k/8k)
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
- [x] A. `discovery-orchestrator` (lead)
- [x] B. `nexus-architect`, `nexus-pm`, `nexus-security`
- [x] C. **+ Outil de calcul ROI / TCO / payback**
- [x] D. **+ Outil de PoC léger (Docker, scripts, mocks)**
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

**Livres canoniques disponibles localement pour cette phase** (3 livres corpus-aligned sur ~15 recommandés = **20%**) :

- **New Books** : 3 livres — voir détail §3.3 ci-dessus

**Lacunes critiques (§20)** : 1 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
- [x] A. T1 (producteur vs casseur) — utile : Nexus-Security casse le business case de Nexus-PM
- [x] B. T2 (spec-compliance) — utile : vérification IEEE 1059 / BABOK
- [x] C. T3 (conséquentialiste) — utile : prédire ce qui pète en P2-P5
- [x] D. **+ Pas de Council** (budget serré, pas 4 reviewers en parallèle)
- [ ] Autre : ____________________________________________

### 5.5 Points de décision utilisateur (B threshold)
**Décisions tranchées par le mainteneur (2026-06-05) — 6 questions max, seuil B appliqué** :

1. **Go/no-go final** : décision binaire, signature mainteneur
2. **Stack candidate acceptée ou challengée** : si challengée, retour à P1 bis ou P0
3. **Sponsor identifié et engagé ?** : si non, critère d'abandon
4. **Opposition stakeholder forte** : si oui, escalade ou abandon
5. **Contraintes réglementaires incompatibles ?** : si oui, alternative obligatoire
6. **ROI insuffisant, alternative écartée ?** : si oui, retour P0 ou clôture projet

L'agent peut choisir de ne pas poser les 6 si le contexte est déjà clair. Min 0, max 6. Au-delà, le système choisit en autonomie et logge dans l'UDL.

### 5.6 Verdict
- [x] 🟢 OK (5.5 comblé, 5.4 T1+T2+T3 explicités, 4 agents max)

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques
- [x] A. Pas de specs détaillées
- [x] B. Pas d'architecture
- [x] C. Pas de code
- [x] D. Pas de figeage de stack (P1 propose, P3 peut challenger, P5 confirme)
- [ ] Autre : ____________________________________________

### 6.2 Modes d'échec connus
- [x] A. **PoC infini** (on optimise la faisabilité au lieu de décider) → budget serré 3k/5k/8k
- [x] B. **Go-decision trop rapide** (pas de PoC,ROI inventé) → checklist 6 critères
- [x] C. **Go-decision trop tardive** (over-engineering faisabilité) → cap 35 min
- [x] D. **Sponsor manquant non détecté** (on avance sans) → critère abandon 3
- [x] E. **Alternative écartée silencieusement** (pas documentée) → UDL 5
- [ ] Autre : ____________________________________________

### 6.3 Cas limites
- [x] A. Greenfield from-scratch (faisabilité riche)
- [x] B. Maintenance legacy (faisabilité = modernisation ?)
- [x] C. Projet interne vs externe (business case critique pour externe)
- [x] D. Compliance-driven (réglementaire en première position)
- [x] E. R&D / exploration (peu de ROI formel)
- [x] F. Solo dev (sponsor = mainteneur lui-même)
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
- [x] A. Faisabilité technique impossible → retour P0 (re-cadrage)
- [x] B. ROI négatif et pas d'alternative → clôture projet
- [x] C. Sponsor manquant / opposition non résolvable → escalade ou abandon
- [x] D. Contraintes réglementaires incompatibles → alternative obligatoire
- [ ] Autre : ____________________________________________

### 6.5 Verdict
- [x] 🟢 OK (4 refus, 5 modes échec, 6 cas limite, escalade documentée)

---

## Section 7 — Adéquation aux besoins (utilité)

### 7.1 Usage réel
> ⬜ À mesurer en pratique sur 1-2 projets réels. La phase est créée le 2026-06-05, pas encore utilisée.

### 7.2 Friction observée
> ⬜ Non mesurée.

### 7.3 Pattern de contournement probable
> ⬜ Si P1 est trop lourde, le mainteneur pourrait court-circuiter et aller directement de P0 à P2 (en perdant la valeur de la go/no-go). À surveiller.

### 7.4 Valeur ajoutée perçue
> **Attendue** : éviter d'investir dans des specs P2 sur des projets infaisables. ROI P1 (économie de specs inutiles) > coût P1. À valider en pratique.

### 7.5 Dette d'orchestration
> ⬜ Pas de dette identifiée à ce stade.

### 7.6 Verdict
- [x] 🟡 À ajuster (spec créée, utilité à mesurer en pratique — section 7 honnête)

---

## Section 8 — Context Engineering (transverse)

### 8.1 Token budget alloué
**Suggestion** : 3k base / 5k soft / 8k hard (le plus serré du projet, justifié par "phase = filtre rapide").

### 8.2 Compaction checkpoint
- [ ] A. Tous les 5 tool calls
- [ ] B. À 70% du soft cap (3.5k)
- [x] C. Les deux (belt + suspenders)
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
- [x] A. P0 outputs (charter, scope, risks, UDL) en consultation envelope
- [x] B. Anciens projets (cross-project memory) pour sanity check sur stack
- [x] C. **Mode consultation envelope strict** (jamais injecter tout P0)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret
- [x] A. T1 : Nexus-Security casse le business case de Nexus-PM
- [x] B. T2 : auditeur vérifie IEEE 1059 / BABOK compliance
- [x] C. T3 : consequentialist prédit ce qui pète en P2-P5
- [x] D. **Pas de Council** (budget serré, max 4 agents)
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger
**6 éléments P1-spécifiques confirmés par le mainteneur (2026-06-05)** :

1. **Décision go/no-go** — la décision finale + rationale
2. **Stack candidate recommandée** — Top-1 + alternatives écartées
3. **Contraintes propagées vers P2** — ce que P2 doit savoir
4. **Risques de faisabilité identifiés** — risques qui peuvent bloquer P2-P5
5. **Alternatives écartées** — pourquoi on n'a pas choisi les autres options
6. **Sign-off et rejets** — qui a signé quoi, qui a refusé

Stockés dans `.swebok_state.db` (table `udl_p1`) et consultables via Consultation Envelope (A1) par P2.

### 8.6 Verdict
- [x] 🟢 OK (section 8.7 findings intégrés, 8.5 UDL 6 éléments comblé en spec v1, budget 3k/5k/8k aligné, 8.2 compaction 60-70% retenu, 8.3 consultation envelope strict)

### 8.7 Validation empirique 2026 (recherche complémentaire)

#### Findings les plus pertinents pour cette phase
- **F13** : Single-agent ≥ multi-agent à budget tokens égal → confirme single Discovery-Orchestrator + 3-4 Nexus max pour P1, pas de fan-out massif
- **F4** : Context rot à 18/18 modèles → ne pas charger toute la stack "au cas où"
- **F6** : Mur à 35 min → checkpoint obligatoire au-delà
- **F7** : 60% du 1er tour agent = retrieval → pre-hydrate P0 obligatoire en début de P1

#### Anti-patterns à éviter dans cette phase
- **AP7** : Contexte "flood" — ne pas injecter tout le corpus `distilled/` dans le contexte
- **AP2** : Brief vague "research X" — si T3 spawn, brief structuré obligatoire
- **AP6** : Tool result clearing absent — vider les tool results PoC après consommation

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : un PoC "presque réussi" qui cache un défaut bloquant
- [x] **Distraction** : PoC infini, on optimise la faisabilité au lieu de décider
- [x] **Confusion** : faisabilité technique OK mais économique KO (ou inverse)
- [x] **Clash** : faisabilité technique OK mais sponsor refuse le business case

#### Recommandation budget (mise à jour 2026)
- **Base 3k / Soft 5k / Hard 8k** (4 agents séquentiel max, pre-hydrate P0 partiel, ANTI-ROT trigger à 60% du soft cap = 3k tokens, compaction checkpoint toutes les 5 actions)
- ⚠️ **Justification budget serré** : P1 est un FILTRE, pas une exploration. Si on ne peut pas décider en 8k tokens, c'est qu'on a un problème de cadrage P0 ou que le projet est trop flou.

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 0 |
| New Books achetés (§19) | 3 |
| Standards NIST/OWASP (§13) | 0 |
| Open-access téléchargés | 0 |
| **TOTAL corpus-aligned local** | **3** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~15 livres
- **Disponible localement** : 3 corpus-aligned
- **Couverture effective** : **20%** ██░░░░░░░░

### Lacunes (§20)

- **1** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **insuffisantes** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel


## Verdict global de la phase
- [ ] 🟢 OK — conforme, rien à changer
- [x] 🟡 À ajuster — fonctionne mais perfectible (utilité à mesurer en pratique)
- [ ] 🔴 À repenser — design ou utilité à revoir fondamentalement

## Liste d'actions
**🟡 P1 — bloquants (fermés en spec v1)** :
1. ✅ Section 5.5 comblée (6 questions utilisateur, seuil B)
2. ✅ Section 8.5 comblée (6 éléments UDL P1-spécifiques)
3. ✅ Verdicts tranchés (sections 1-8 + global = 🟢 partout sauf 7 = 🟡)
4. ✅ Spec v1 créée (`specs/workflows/by-phase/phase-1-concept-feasibility.md`)
5. ✅ Token counter P1 ajouté (`pre-tool-use/token-counter.sh` ligne 58)
6. ✅ Budget P1 = 3k/5k/8k (le plus serré du projet, justifié)

**🟡 P2 — qualité (fermés en spec v2, 2026-06-06)** :
7. ✅ T1/T2/T3 explicités (T2 = Discovery-Orch, T1/T3 = rotation entre 3 Nexus)
8. ✅ Nexus-DevOps 5e agent optionnel clarifié (PoC infra complexe, à arbitrage mainteneur)
9. ✅ Format go-no-go-decision = md+json (vs md seul en v1)
10. ✅ Cap 35 min strict (vs ajustable en v1)
11. ✅ Couverture corpus 20% acceptée explicitement (section "Couverture corpus" ajoutée à spec v2)
12. ✅ 7 décisions tranchées via grille offline (cf. "Décisions d'audit" ci-dessous)

**🟢 P3 — nice-to-have (à fermer post-v2)** :
13. ⬜ Mesurer l'usage réel de P1 sur 1-2 projets pour fermer la section 7 (utilité)
14. ⬜ Vérifier que la phase ne se transforme pas en "mini-Discovery bis" (mesure PoC)
15. ⬜ Étendre la même méthode d'audit (grille offline + questions ciblées) à P4-P10 (référence : P0 v2, P1 v2, P2 v2, P3 v1)

## Décisions d'audit (7 décisions tranchées, 2026-06-06)

1. **Existence de P1** : garder P1 complet (4 dimensions + 6 livrables + go/no-go). Pas de fusion avec P0 ou P2.
2. **T1/T2/T3 mécanique** : rotation des 4 agents. T2 (spec-compliance) = Discovery-Orch. T1 (casseur) et T3 (conséquentialiste) = rotation entre Nexus-Architect, Nexus-PM, Nexus-Security.
3. **Nexus-DevOps** : gardé en option (5e agent, autorisé UNIQUEMENT si PoC infra complexe, à arbitrage mainteneur). Standard = 4 agents.
4. **PoC technique** : reste conditionnel ("si applicable" comme spec v1). Pas systématique.
5. **Format go/no-go** : md + json (les deux). md pour humain, json pour state engine.
6. **Cap 35 min** : strict (spec v1). Si dépassé, critère d'abandon #4 s'applique. Action P2-9 fermée.
7. **Couverture corpus 20%** : laisser tel quel. Pas d'achat Cohn 2005 maintenant. Batch ultérieur avec P2.

## Notes libres
> Phase 1 Concept/Feasibility = v2 validée 2026-06-06 par le mainteneur. Spec v1 créée 2026-06-05, spec v2 créée 2026-06-06 post-audit.
> 12 actions P1+P2 fermées (6 par spec v1, 6 par spec v2). 3 actions P3 restantes (mesure réelle, pas de drift, méthode reproductible).
> Verdict global 🟡 (à ajuster — spec solide, utilité à mesurer en pratique).
> Cible universelle adaptative (6 cas). Budget 3k/5k/8k tokens (le plus serré), cap 35 min strict, 4 agents en standard (5 si PoC complexe).
> 6 livrables (5 + go-no-go-decision) en md + JSON pour go/no-go. T1+T2+T3 (T2=Discovery-Orch, T1/T3=rotation 3 Nexus). Pas de Council.
> Tension principale : phase rapide vs exhaustivité de la faisabilité. Justification : c'est un filtre, pas une exploration.
> Méthode d'audit appliquée : grille offline + 7 questions AskUserQuestion (vs 5 rounds × 4 = 20 décisions pour P0/P2). Plus léger car phase simple + budget serré. Référence pour P4-P10.
> Prochaine phase d'audit suggérée : P3 (Architecture) — la grille et la spec v1 existent déjà, à valider/amender par audit.
