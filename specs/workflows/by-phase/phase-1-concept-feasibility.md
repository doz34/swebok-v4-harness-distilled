# Phase 1: Concept/Feasibility Workflow Spec

> **Statut** : v2 — validé 2026-06-06 par le mainteneur (audit P1 clos via grille offline + 7 questions ciblées)
> **Changement vs v1** : T1/T2/T3 explicités (T2 = Discovery-Orch, T1/T3 = rotation entre Nexus-Archi/PM/Security), Nexus-DevOps gardé en option (5e agent si PoC infra complexe, à arbitrage mainteneur), format `go-no-go-decision` = md+json (vs md seul en v1), cap 35 min strict, couverture corpus 20% acceptée (pas d'achat Cohn 2005 maintenant, batch ultérieur).
> **Changement vs structure antérieure** : nouvelle phase. Avant : P0 Discovery → P2 Requirements (manque la phase de faisabilité). Après : P0 → P1 Concept/Feasibility → P2 Requirements.
> **But** : combler le gap entre "intention cadrée" (P0) et "specs testables" (P2). P1 valide la faisabilité technique, économique, organisationnelle AVANT d'investir dans une spec détaillée.

## Metadata
- **Phase**: 1
- **Name**: Concept/Feasibility
- **Purpose**: Valider la faisabilité d'un projet cadré (P0) sous ses dimensions techniques, économiques, organisationnelles, et réglementaires. Produire une décision go/no-go documentée pour P2.
- **Parallel Mode**: séquentiel strict (analyse mono-agent ou 2-3 agents max)
- **Équivalent SWEBOK v4** : Software Engineering Management KA (P8) — concepts de feasibility, alternatives analysis, business case
- **Référentiels** : IEEE 1059 (feasibility studies), BABOK (business case)

---

## Mission (1 phrase)

> « Transformer un cadrage P0 validé en décision go/no-go documentée, avec analyse de faisabilité technique, économique, organisationnelle, et réglementaire — pour que P2 specs ne parte pas sur un projet infaisable. »

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-1.1 | P0 Discovery validé | Charter + 7 livrables P0 | 100% checklist P0 |
| EG-1.2 | Intent clairement exprimée | Discovery-report "intent" | Pas d'ambiguïté sur le POURQUOI |
| EG-1.3 | Top-3 risques identifiés | risk-preliminary.md P0 | ≥3 risques nommés avec rating |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers P0 remediation.

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-1.1 | Feasibility study complete | feasibility-study.md | 4 dimensions couvertes (technique, économique, organisationnelle, réglementaire) |
| XG-1.2 | Alternatives analysis done | alternatives-analysis.md | ≥2 options comparées (incluant "build vs buy vs nothing") |
| XG-1.3 | Business case approved | business-case.md | ROI estimé + payback period |
| XG-1.4 | Go/no-go decision documented | go-no-go-decision.md | Décision signée par le mainteneur |
| XG-1.5 | Stack technique candidate identifiée | tech-stack-candidate.md | Top-1 stack recommandée + rationale |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed to P2. Any `FAIL` requires more analysis or P0 re-cadrage.

---

## Transition Criteria to Phase 2 (Requirements)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Go-decision signed | Mainteneur | Phase 2 Lead | Go/no-go memo |
| Feasibility study locked | Nexus-Architect | Phase 2 Lead | Study baseline version |
| Stack candidate ratified | Mainteneur | Phase 2 Lead | Tech-stack memo |
| Business case approved | Mainteneur | Project Sponsor | Business case signature |
| Constraints propagés to P2 | Discovery-Orchestrator | Phase 2 Lead | Constraints list in UDL |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_1_COMPLETE` only when go-decision signed and all artifacts validated.

---

## Key Activities

### Activity 1.1: Technical Feasibility
- Identifier les contraintes techniques dures (performance, scalabilité, intégration legacy)
- Tester des PoC (proof of concept) sur les zones à risque technique
- Identifier les dépendances externes critiques (API tierces, vendors)
- Valider que la stack candidate tient la charge attendue

### Activity 1.2: Economic Feasibility
- Estimer le coût total (TCO) sur 3 ans
- Calculer le ROI et le payback period
- Comparer avec les alternatives (buy, SaaS, nothing)
- Identifier les coûts cachés (formation, migration, dette technique)

### Activity 1.3: Organizational Feasibility
- Valider la disponibilité des compétences (interne vs recrutement vs sous-traitance)
- Évaluer la résistance au changement
- Identifier les stakeholders "anti" et leurs arguments
- Valider le sponsorship (un sponsor identifié et engagé)

### Activity 1.4: Regulatory Feasibility
- Identifier les contraintes réglementaires (RGPD, HIPAA, sectoriel)
- Vérifier les contraintes juridiques (propriété intellectuelle, contrats)
- Anticiper les obligations d'audit/compliance
- Valider la conformité du data residency (si Cloud)

---

## Responsible Agents
| Agent | Role |
|-------|------|
| Discovery-Orchestrator | Lead coordination + animation go/no-go + **T2 (conformité IEEE 1059 / BABOK)** |
| Nexus-Architect | Faisabilité technique + stack candidate + **T1 ou T3 (rotation)** |
| Nexus-PM | Faisabilité économique + business case + alternatives + **T1 ou T3 (rotation)** |
| Nexus-Security | Faisabilité réglementaire (compliance) + **T1 ou T3 (rotation)** |
| (optionnel, **5e agent**) Nexus-DevOps | PoC infra si zone à risque technique complexe. Standard = 4 agents, ce 5e agent = exception justifiée par PoC infra lourd. |

**Concurrency** : séquentiel strict, **4 agents en standard**. **5e agent (Nexus-DevOps) autorisé UNIQUEMENT si PoC infra complexe**, à l'arbitrage du mainteneur (décision loggée dans UDL). Budget serré (3k/5k/8k tokens).

**Patterns adversariaux (T1/T2/T3)** :
- **T1 (producteur vs casseur)** : rotation entre Nexus-Architect, Nexus-PM, Nexus-Security. Chacun casse le livrable d'un autre (ex: Nexus-Security casse le business case de Nexus-PM).
- **T2 (spec-compliance IEEE 1059 / BABOK)** : Discovery-Orchestrator vérifie la conformité de la feasibility study et du business case.
- **T3 (conséquentialiste)** : rotation entre les 3 Nexus. Chacun prédit ce qui pète en P2-P5.
- **Pas de Council** : budget serré, max 4-5 agents. Pas de 4 reviewers en parallèle (vs P2).

---

## Required Skills
- `discovery-orchestrator` : cadrage + animation décisionnelle
- `nexus-architect` : analyse technique, PoC léger
- `nexus-pm` : business case, alternatives analysis
- `nexus-security` : compliance check

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-feasibility-approved` | Exit criteria met | Triggers Phase 2 (Requirements) initiation |
| `poc-completed` | Activity 1.1 done | PoC results integrated |
| `go-decision-signed` | Activity go-decision | Unblocks Phase 2 |
| `no-go-decision` | Go-decision = NO | Closes project, archives P0+P1 |

---

## Artifacts Produced

| Artifact | Description | Location |
|----------|-------------|----------|
| `feasibility-study.md` | 4-dimension feasibility report (technical, economic, organizational, regulatory) | `specs/workflows/by-phase/phase-1-concept-feasibility/` |
| `alternatives-analysis.md` | ≥2 options comparées (build vs buy vs nothing + autres stacks) | `specs/workflows/by-phase/phase-1-concept-feasibility/` |
| `business-case.md` | ROI, payback, TCO 3 ans | `specs/workflows/by-phase/phase-1-concept-feasibility/` |
| `tech-stack-candidate.md` | Top-1 stack recommandée + rationale | `specs/workflows/by-phase/phase-1-concept-feasibility/` |
| `poc-results.md` | Résultats PoC techniques (si applicable) | `specs/workflows/by-phase/phase-1-concept-feasibility/` |
| `go-no-go-decision.md` + `go-no-go-decision.json` | Décision finale signée par le mainteneur (md pour humain, json pour state engine) | `specs/workflows/by-phase/phase-1-concept-feasibility/` |

---

## Refus catégoriques (4)

La phase P1 **refuse** de :
1. **Pas de specs détaillées** (forcé en P2)
2. **Pas d'architecture** (forcé en P3)
3. **Pas de code** (jamais)
4. **Pas de figeage de stack** (P1 propose, P3 peut challenger, P5 confirme)

---

## Critères d'abandon (3 + temps)

L'agent abandonne et prévient le mainteneur si :
1. Faisabilité technique impossible (PoC échoue, contrainte physique)
2. ROI négatif et pas d'alternative (revenir à P0 ou clôturer)
3. Sponsor manquant ou opposition forte non résolvable
4. Dépassement de 35 min sans avancée claire

---

## Tokens budget

- **Base** : 3k tokens
- **Soft cap** : 5k tokens (alerte)
- **Hard cap** : 8k tokens (compactage forcé + abort)

Séquentiel strict + 4 agents max = pas de ×15 tokens. Budget serré car P1 doit être rapide (c'est un filtre, pas une exploration).

---

## Format des fichiers

- **Markdown** : pour tous les livrables (lecture humaine, structuré par sections)
- **JSON** : pour `go-no-go-decision.json` UNIQUEMENT (machine-parse pour state engine)
- **Pas de triple format** comme P0/P2 (pas d'entrée `.swebok_state.db` pour les livrables, seulement pour l'UDL)
- **UDL** : 6 éléments P1-spécifiques stockés dans `.swebok_state.db` table `udl_p1`, consultables via Consultation Envelope (A1) par P2

**Convention de nommage** : `${livrable}.md` + `${livrable}.json` (uniquement go-no-go) dans `specs/workflows/by-phase/phase-1-concept-feasibility/`.

---

## Couverture corpus (état 2026-06-06)

- **3 livres corpus-aligned** sur ~15 recommandés = **20%** de couverture
- **Lacune critique** : Agile Estimating and Planning (Cohn 2005) — pas acquis
- **Décision mainteneur 2026-06-06** : ne pas acquérir maintenant, batch ultérieur avec P2 (Cohn est utile aussi pour Requirements)
- **Impact** : 20% suffit pour P1 (filtre rapide, ne dépend pas tant du corpus). Le mainteneur compense par expérience.

---

## Pauses

Toutes les 5 actions : compaction checkpoint.

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :
1. **Greenfield from-scratch** : faisabilité riche, PoC technique critique
2. **Maintenance legacy** : faisabilité = "peut-on moderniser ?", dette technique
3. **Projet interne** (équipe, gouvernance légère)
4. **Projet externe client** (business case critique, sign-off formel)
5. **Compliance-driven** (réglementaire en première position)
6. **R&D / exploration** (faisabilité = "peut-on faire de la recherche ?", peu de ROI formel)

---

## UDL — 6 éléments P1-spécifiques

| Élément | Description | Exemple |
|---------|-------------|---------|
| Décision go/no-go | La décision finale + rationale | "GO car ROI 18 mois, stack candidate validée par PoC" |
| Stack candidate recommandée | Top-1 stack + alternatives écartées | "PostgreSQL + FastAPI + React (vs MongoDB+Express écarté pour X)" |
| Contraintes propagées vers P2 | Ce que P2 doit savoir | "Pas de Cloud public, on-prem imposé" |
| Risques de faisabilité identifiés | Risques qui peuvent bloquer P2-P5 | "Dépendance API tierce non-garantie SLA" |
| Alternatives écartées | Pourquoi on n'a pas choisi les autres options | "Buy (SaaS) écarté car data residency incompatible" |
| Sign-off et rejets | Qui a signé quoi, qui a refusé | "Sponsor X a signé business case, stakeholder Y a contesté" |

Stockés dans `.swebok_state.db` (table `udl_p1`) et consultables via Consultation Envelope (A1) par P2.

---

## Conditions de sortie (passage à P2)

Le mainteneur valide avec une **checklist à 100%** (6 critères) :
- [ ] `feasibility-study.md` existe (4 dimensions)
- [ ] `alternatives-analysis.md` existe (≥2 options)
- [ ] `business-case.md` existe (ROI + payback)
- [ ] `tech-stack-candidate.md` existe (Top-1)
- [ ] `go-no-go-decision.md` signé
- [ ] UDL 6 éléments loggés

Pas de feu vert séparé — les documents font foi.

---

## Audit des 4 failure modes Drew Breunig

### Mode 1 — Poisoning (Empoisonnement)
**Risque** : un PoC "presque réussi" qui cache un défaut bloquant.
**Mitigations** :
1. PoC = critères d'échec explicites (pas de "ça marche à peu près")
2. Faisabilité technique challengée par Nexus-Security (pas l'architecte qui l'a faite)
3. Business case challengé par Nexus-PM (pas le même qui l'a fait)
4. Go/no-go signé par le mainteneur = catch final

### Mode 2 — Distraction (Distraction)
**Risque** : PoC infini, on optimise la faisabilité au lieu de décider.
**Mitigations** :
1. Budget serré 3k/5k/8k (vs 4k/7k/10k ailleurs)
2. Cap 35 min
3. "Build vs buy vs nothing" : 3 options max, pas 10
4. Pas de PoC sans hypothèse de succès explicite

### Mode 3 — Confusion (Confusion)
**Risque** : faisabilité technique OK mais économique KO (ou inverse).
**Mitigations** :
1. 4 dimensions explicites (tech / eco / org / reg)
2. UDL 1 ("décision go/no-go") synthétise les 4
3. Business case = artefact dédié (pas noyé dans feasibility-study)
4. UDL 2 ("stack candidate") est un POINTER, pas un dump

### Mode 4 — Clash (Conflit)
**Risque** : faisabilité technique OK mais sponsor refuse le business case.
**Mitigations** :
1. UDL 5 ("alternatives écartées") documente les options non choisies
2. UDL 6 ("sign-off et rejets") logge les oppositions
3. Critère d'abandon 3 (sponsor manquant / opposition non résolvable)
4. Go/no-go signé = sortie propre si clash irréductible

---

## Notes de version

- **v2 (2026-06-06)** : T1/T2/T3 explicités (T2 = Discovery-Orch, T1/T3 = rotation entre Nexus-Archi/PM/Security), Nexus-DevOps 5e agent optionnel (PoC infra complexe), format `go-no-go-decision` = md+json, cap 35 min strict, couverture corpus 20% acceptée. 7 décisions tranchées via grille offline (`audit/phase-1-concept-feasibility-audit.md`).
- **v1 (2026-06-05)** : créé suite au fix structurel (split P3 + ajout P1). 4 activités, 6 livrables, 4 agents séquentiel max, 3k/5k/8k tokens, cap 35 min, 6 questions max, 6 UDL items, 4 refus, 3 critères abandon, 6 cas limite.
