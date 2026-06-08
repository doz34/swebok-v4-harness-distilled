# Audit — Phase 3 : Architecture

> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 3
- Nom : Architecture
- Équivalent SWEBOK v4 : P2 SWEBOK (Software Architecture KA)
- Spec existante : `specs/workflows/by-phase/phase-3-architecture.md` (v2 — validé 2026-06-06)
- Date de l'audit : 2026-06-06
- Auditeur : Mainteneur (grille offline) + Claude (analyse + 8 questions + rédaction v2)
- Verdict global : 🟢 OK — toutes les sections comblées (7 par projection + cohérence P0/P1/P2 v2)

---

## ⚠️ Findings pré-identifiés

1. **Phase 3 NOUVELLE** : créée le 2026-06-05 lors du fix structurel (split P3 Design en P3 Architecture + P4 Design). Avant : P3 = Archi+Design fusionnés (perte de détail). Après : P3 = Architecture seule, P4 = Design seul.
2. **Multi-agent justifié** : 3-5 sub-agents en parallèle (Nexus-Architect, Nexus-Security, Nexus-Backend, Nexus-Frontend, Nexus-DevOps) + Nexus-Critic. Justifié par F13 recherche 2026 (read-heavy parallèle, disjoint tools).
3. **ADRs formalisés** : chaque décision structurante = un ADR (Architecture Decision Record). Avant : les ADR étaient mentionnés comme suggestion dans P3 Design, pas obligatoires. Après : obligatoires.

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
- [x] A. *« Produire l'architecture système validée par ≥3 architectes, avec ADRs signés pour chaque choix structurant, et contrats d'interface au niveau archi — pour que P4 Design puisse designer sans ambiguïté »* (spec actuelle)
- [ ] B. *« Décider l'architecture en un seul cycle, avec contrats d'interface signés »*
- [ ] C. *« Produire ce qu'il faut pour que P4 Design et P5 Implementation n'aient pas à re-concevoir »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
- [x] A. System decomposition (subsystems, Bounded Contexts)
- [x] B. Architectural patterns and styles (monolith, microservices, etc.)
- [x] C. Data architecture (storage, partitioning, consistency)
- [x] D. Security architecture (auth/authz, threat model STRIDE)
- [x] E. Integration architecture (API gateway, event bus, versioning)
- [x] F. Architectural interface contracts (API contracts, module contracts — archi level)
- [x] G. **+ ADRs (Architecture Decision Records) formels par décision structurante**
- [x] H. **+ Threat model si security-sensitive (STRIDE)**
- [ ] Autre : ____________________________________________

### 1.3 Hors-périmètre
- [x] A. Detailed design (P4 Design)
- [x] B. Code (P5+)
- [x] C. Tests d'implémentation (P6 Testing)
- [x] D. **+ Choix tactique** (la tactique est pour P4 Design)
- [x] E. **+ Estimation effort détaillée** (P5 Implementation inclut ses propres estimations)
- [x] F. **+ Choix de stack si déjà ratifiée en P1** (sinon ratifier ici)
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK (mission claire, périmètre explicite, hors-périmètre explicite)

### 1.5 Critère de démarcation P3 vs P4 (Design)
- [x] A. **P3 = QUOI + POURQUOI** : bounded contexts, style archi, sécurité patterns, intégration patterns, ADRs, contrats externes
- [x] B. **P4 = COMMENT** : algos détaillés, classes/fonctions, error handling, signatures internes, schémas de données internes
- [x] C. **Règle simple** : si la décision impacte ≥2 bounded contexts / équipes = P3. Si elle impacte un module / classe = P4
- [x] D. **Cas limite type** : "monolith modulaire avec 3 bounded contexts" = P3. "Module Billing = Repository pattern" = P4
- [x] E. **Critère inscrit explicitement dans P3 ET P4** (décision mainteneur 2026-06-06, validé pour les 2 specs)

### 1.6 Verdict global section 1
- [x] 🟢 OK (mission + périmètre + hors-périmètre + démarcation P3/P4 explicites)

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] A. Phase 2 requirements approved (SRS baseline locked)
- [x] B. Prioritized backlog ≥90% priorisé
- [x] C. RTM accessible et current
- [x] D. Acceptance criteria définis (chaque req a un AC)
- [x] E. Tech stack ratified (P1) — éviter le chicken-and-egg avec P1
- [x] F. Architecture environment prepared (write access pour tous les architectes)
- [ ] Autre : ____________________________________________

### 2.2 Critères de complétion
- [x] A. Architectural design complete (≥95% ISO 42010)
- [x] B. Architectural design reviewed (peer review par ≥3 architectes)
- [x] C. Architectural interface contracts finalisés (100% interfaces archi)
- [x] D. ADRs signés (100% structurants)
- [x] E. Security architecture approved (Nexus-Security + CISO)
- [x] F. Architecture-to-Requirements traceability (ART 100%)
- [x] G. UDL 7 éléments loggés
- [ ] Autre : ____________________________________________

### 2.3 Conditions d'échec → escalade
- [x] A. Conflit entre architectes non résolvable (3 reviewers en désaccord)
- [x] B. NFR conflictuels (perf vs cost) non résolus par mainteneur
- [x] C. Interface contract impossible à designer en P4
- [x] D. Security architecture rejeté par Nexus-CISO
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟢 OK (trigger + complétion + échec explicites, ADRs obligatoires)

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. Phase 2 outputs (SRS, use case model, AC, RTM, prioritized backlog, NFR-and-ADR)
- [x] B. Phase 1 (Concept/Feasibility) outputs (stack candidate, business case, constraints)
- [x] C. Phase 0 risk landscape
- [x] D. Phase 0 stakeholder register
- [x] E. **+ NFR extraits du SRS** (souvent oubliés, ici obligatoires)
- [x] F. **+ Use case model** (de la phase 2)
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
- [x] A. Décision sur NFR conflictuels (perf vs cost, sécurité vs UX)
- [x] B. Validation des trade-offs architecturaux (monolith vs microservices, SQL vs NoSQL)
- [x] C. **+ Acceptation des contraintes de dette technique** (si P5 doit supporter de la dette)
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **65%** (██████░░░░).**Sources externes disponibles localement (post-corpus) :****Mac Studio** (10 livres) — chemin `/Users/dorianciet/Desktop/Test PDF books` et `/Volumes/External/Obsidian KB/Knowledge Base/raw/pdfs` :- **Head First Software Architecture** (Raju Gandhi, Mark Richards, Ne) — 50.7 MB, 486 pages- **Building Evolutionary Architectures** (Neal Ford, Rebecca Parsons, Pa) — 8.2 MB, 265 pages- **Software Architecture: The Hard Parts** (Neal Ford, Mark Richards, Pram) — 15.2 MB, 462 pages- **Building Micro-Frontends** (Luca Mezzalira) — 8.6 MB, 337 pages- **The Software Architect Elevator** (Gregor Hohpe) — 21.3 MB, 367 pages- **Building Microservices** (Sam Newman) — 15.4 MB, 615 pages- **Software Architecture Metrics** (Christian Ciceri, Dave Farley,) — 7.9 MB, 218 pages- **Fundamentals of Software Architecture** (Mark Richards and Neal Ford) — 21.6 MB, 422 pages- **Building Event-Driven Microservices** (Adam Bellemare) — 10.4 MB, 324 pages- **Learning Domain-Driven Design** (Vlad Khononov) — 15.9 MB, 342 pages**New Books (achats locaux)** (3 livres) — chemin `/home/doz/Bureau/New Books/` :- **Architecture for Flow** (Susanne Kaiser, 2024) — formats: PDF- **Fundamentals of Software Architecture** (Mark Richards, Neal Ford, 2020) — formats: PDF- **Design It!** (Michael Keeling, 2017) — formats: PDF**Standards NIST/OWASP téléchargés (open access)** (3) :- NIST 800-145 (Cloud)- NIST 800-204 series (Microservices)- NIST 800-207 (Zero Trust)**Livres open-access téléchargés** (2) :- Computer Networks (Peterson, 22 MB)- A Philosophy of Software Design (Ousterhout 2e, 14 MB)**Lacunes critiques restantes (à acquérir)** (9) :- Patterns of Enterprise Application Architecture (Fowler) (2002)  -- Catalogue de patterns fondateur. Toujours référence.- Clean Architecture (Martin) (2017)  -- 🔴 Manque encore. Très haute valeur.- Software Architecture in Practice 4th ed. (Bass) (2021)  -- 🔴 Référence académique #1. Critique.- Designing Software Architectures 2nd ed. (Cervantes/Kazman) (2024)  -- Méthode ADD. Très récent et pertinent.- Effective Software Architecture (Ford) (2024)  -- Pragmatique. Très récent.- ... et 4 autres. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20.
### 3.4 Verdict
- [x] 🟢 OK (P0+P1+P2 + sources externes + NFR extraits)

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
- [x] A. `architectural-design.md` (C4 model + key views)
- [x] B. `system-decomposition.md` (subsystems, modules, Bounded Contexts)
- [x] C. `data-architecture.md`
- [x] D. `security-architecture.md` (avec threat model STRIDE)
- [x] E. `integration-architecture.md`
- [x] F. `architectural-interface-contracts.md` (100% interfaces archi — modules internes + API REST)
- [x] G. `adrs/` (répertoire avec **minimum 1 ADR par décision structurante, pas de max** — décision mainteneur 2026-06-06)
- [x] H. `architecture-traceability-matrix.md` (ART)
- [x] I. `architecture-review-report.md` (sign-off ≥3 architectes)
- [ ] Autre : ____________________________________________

### 4.2 Format de stockage (différencié par type — décision mainteneur 2026-06-06)
- [x] A. **Markdown** pour tous les livrables (lisibles par mainteneur)
- [x] B. **JSON** pour les interface contracts (machine-parse pour génération de code en P5)
- [x] C. **+ OpenAPI 3.0** pour les API REST (subset de architectural-interface-contracts.md)
- [x] D. **+ AsyncAPI 3.0** (option) pour les événements async (subset, si applicable)
- [x] E. **Format différencié** : md+json pour modules internes, md+json+OpenAPI pour API REST
- [x] F. **Validation par lint** : `openapi-lint` pour OpenAPI, `asyncapi-lint` pour AsyncAPI
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
- [x] A. Architecture overview (C4 model) en première page
- [x] B. Diagrammes clés (C4, sequence, ER) en premier
- [x] C. ADR explicite pour chaque choix structurant
- [x] D. Threat model summary en annexe
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
- [x] A. Oui — chaque décision tracée + ADR
- [x] B. "Pourquoi on a écarté X" couvert par section "Alternatives considered" dans chaque ADR
- [x] C. Justification des trade-offs couverte par ADR + UDL 3
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟢 OK (9 livrables clairs, format différencié md+json pour modules / md+json+OpenAPI pour API REST, auditabilité max)

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
- [x] A. Hyperagent-Orchestrator (lead, coordination)
- [x] B. Nexus-Architect (synthèse, ADR writing)
- [x] C. Nexus-Security (security architecture + threat model)
- [x] D. Nexus-Backend (backend subsystems)
- [x] E. Nexus-Frontend (frontend architecture)
- [x] F. Nexus-DevOps (infrastructure architecture)
- [x] G. **+ Nexus-Critic (5e agent)** : **T1 casseur + T2 conformité ISO 42010 + T3 prédiction aval — TOUS OBLIGATOIRES** (décision mainteneur 2026-06-06)
- [x] H. **+ Limiter à 3-5 sub-agents en parallèle** (F13 recherche 2026)
- [x] I. **+ Pas de Council** en standard (F13 single-agent suffisant, sauf NFR conflictuels où on escalade au mainteneur)
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
- [x] A. `nexus-architect`, `nexus-security`, `nexus-backend`, `nexus-frontend`, `nexus-devops`
- [x] B. `nexus-critic` (**T1+T2+T3 obligatoires**, 3 invocations systématiques)
- [x] C. `speckit-qa` (architecture quality)
- [x] D. **+ Outil de génération de diagrammes (Mermaid, PlantUML, C4 model)**
- [x] E. **+ Outil de validation de contrats : OpenAPI 3.0 lint (obligatoire REST), AsyncAPI 3.0 lint (option événements)**
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

**Livres canoniques disponibles localement pour cette phase** (13 livres corpus-aligned sur ~20 recommandés = **65%**) :

- **Mac Studio** : 10 livres — voir détail §3.3 ci-dessus
- **New Books** : 3 livres — voir détail §3.3 ci-dessus
- **Standards** : 3 NIST/OWASP
- **Open-access** : 2 livres (Ousterhout, OSTEP, CS229, etc.)

**Lacunes critiques (§20)** : 9 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
- [x] A. T1 (producteur vs casseur) — **OBLIGATOIRE** : un architecte propose, Nexus-Critic casse
- [x] B. T2 (spec-compliance) — **OBLIGATOIRE** : Nexus-Critic vérifie conformité ISO 42010 + NFR
- [x] C. T3 (conséquentialiste) — **OBLIGATOIRE** : Nexus-Critic prédit les difficultés P4 Design
- [x] D. **+ Pas de Council en standard** (escalade mainteneur sur NFR conflictuels)
- [x] E. **+ Coût additionnel ~4.5k tokens** (3 invocations Nexus-Critic), justifié par hard cap 15k (vs 12k en v1)
- [ ] Autre : ____________________________________________

### 5.5 Points de décision utilisateur (B threshold)
**7 questions précises avec options (transformation 2026-06-06 — était liste de catégories, devient questions actionnables comme P1 v2)** :

1. **NFR conflictuels** (perf vs cost, sécurité vs UX) : l'agent doit-il (a) escalader systématiquement au mainteneur, (b) proposer une solution trade-off documentée, (c) appliquer la règle par défaut `sécurité > perf > coût > UX` et logguer dans l'UDL, (d) autre ?
2. **Trade-off architectural structurant** (style monolith vs microservices, SQL vs NoSQL, REST vs GraphQL, etc.) : l'agent doit-il (a) escalader systématiquement, (b) trancher par défaut avec rationale + alternatives écartées dans l'ADR, (c) poser 1-2 questions ciblées avant de trancher, (d) autre ?
3. **Acceptation dette technique** (si P5 doit supporter de la dette pour livraison rapide) : l'agent doit-il (a) refuser systématiquement et escalader, (b) accepter et logger dette + rationale dans l'UDL, (c) demander confirmation explicite au mainteneur avant acceptation, (d) autre ?
4. **Rejet d'un finding T1 casseur** (Nexus-Critic trouve un problème, l'architecte proposeur maintient sa position) : l'agent doit-il (a) accepter le rejet et logger dans l'UDL, (b) escalader au mainteneur pour arbitrage, (c) accepter avec proposition de mitigation, (d) autre ?
5. **Contraintes réglementaires incompatibles avec stack** (RGPD, HIPAA, sectoriel vs stack candidate P1) : l'agent doit-il (a) escalader P1 pour re-cadrage de la stack, (b) proposer une alternative stack conforme avec rationale, (c) accepter la stack et documenter le risque dans l'ADR, (d) autre ?
6. **Sponsor absent sur décision structurante** (pas de sponsor identifié pour trancher) : l'agent doit-il (a) escalader au mainteneur (toi), (b) reporter la décision à une session ultérieure, (c) trancher par défaut et logger dans l'UDL, (d) autre ?
7. **Go/no-go "no" sur une alternative** (l'alternative est définitivement écartée, pas juste "pas choisie pour ce projet") : l'agent doit-il (a) marquer "écarté définitivement" dans l'UDL (non ré-évaluable), (b) laisser en "non choisie" (ré-évaluable dans un autre contexte), (c) demander confirmation explicite avant de marquer définitif, (d) autre ?

**Règle d'usage** : l'agent peut choisir de ne pas poser les 7 si le contexte est déjà clair. Min 0, max 7. Au-delà, le système choisit en autonomie et logge dans l'UDL. Les 7 questions sont **prêtes à l'emploi** dans le format AskUserQuestion (header + 2-4 options mutuellement exclusives par question).

### 5.6 Verdict
- [x] 🟢 OK (5.5 comblé en 7 questions précises avec options AskUserQuestion — transformation 2026-06-06, 5.4 T1+T2+T3 explicités et obligatoires, 3-5 agents max + Nexus-Critic)

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques
- [x] A. Pas de design détaillé module (P4)
- [x] B. Pas de code d'implémentation (jamais)
- [x] C. Pas d'estimation effort détaillée
- [x] D. **+ Pas de choix "tactique"** (la tactique est pour P4)
- [x] E. **+ Pas de design qui ne respecte pas les NFR** (sécurité, perf, scalabilité)
- [ ] Autre : ____________________________________________

### 6.2 Modes d'échec connus
- [x] A. Architecture astronaut (over-engineering)
- [x] B. Design-by-committee (trop d'inputs, pas de décision)
- [x] C. Big ball of mud (pas de séparation)
- [x] D. Vendor lock-in non documenté
- [x] E. **+ ADRs creux** (formalisme sans substance) → exigence : alternatives + conséquences dans chaque ADR
- [x] F. **+ Pas de threat model** → exigence : STRIDE obligatoire si security-sensitive
- [x] G. **+ Architecture isolée des requirements** → exigence : ART 100%
- [ ] Autre : ____________________________________________

### 6.3 Cas limites
- [x] A. Greenfield vs refonte (code existant = contrainte forte)
- [x] B. Criticalité forte (medical, avionique) vs CRUD interne
- [x] C. Solo dev vs équipe distribuée
- [x] D. Contraintes infra fortes (serverless, edge, on-prem)
- [x] E. **+ Compliance-driven** (sécurité archi en première position)
- [x] F. **+ R&D / exploration** (architecture = POC, ADRs minimaux)
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
- [x] A. 3 reviewers en désaccord → escalade mainteneur
- [x] B. NFR impossible à respecter → escalade (remonter aux requirements P2)
- [x] C. Security design rejeté par Nexus-CISO → bloquer la transition
- [x] D. Interface contract impossible à designer en P4 → escalade P2
- [ ] Autre : ____________________________________________

### 6.5 Verdict
- [x] 🟢 OK (5 refus, 7 modes échec, 6 cas limite, escalade documentée)

---

## Section 7 — Adéquation aux besoins (utilité)

### 7.1 Usage réel
> **Projection (par cohérence P0/P1/P2 v2 + benchmarks corpus 2026, validée 2026-06-06)** :
> - **Greenfield from-scratch** : 5-10 ADRs (style archi, DB, frontend, backend, sécurité, intégration, etc.), 3-5 contrats d'interface (modules internes + API REST), 1 threat model STRIDE (si security-sensitive), 1 ART 100%. Effort estimé : 1-2 sessions de 35 min.
> - **Maintenance legacy** : 1-3 ADRs (nouveaux choix uniquement, l'existant est tracé), peu de contrats modifiés, ART mis à jour (pas créé ex nihilo). Effort estimé : 0.5-1 session de 35 min.
> - **R&D / exploration** : 1-2 ADRs (POC uniquement, justifications minimales), pas de threat model formel, ART simplifié. Effort estimé : 0.5 session de 35 min.
> - **Compliance-driven** : 5-10 ADRs + threat model STRIDE complet + 1 NFR-and-ADR dédié. Effort estimé : 1.5-2.5 sessions de 35 min.
> - **Projet interne / équipe légère** : 3-5 ADRs, threat model léger, ART 100%. Effort estimé : 1 session de 35 min.
> - **Projet externe client** : 5-10 ADRs + revue architecte client (sign-off formel). Effort estimé : 2 sessions de 35 min (révision incluse).
>
> **Cohérence P0/P1/P2 v2** : les phases P0/P1/P2 utilisent les mêmes patterns (4 agents séquentiel, format md+json, UDL 7 éléments, 4 failure modes Drew Breunig). P3 les applique en mode multi-agent justifié (F13 recherche 2026). Le passage de single-agent (P0/P1/P2) à multi-agent (P3) est documenté et justifié. Aucun contournement ni friction majeure remonté à date sur P0/P1/P2 v2.

### 7.2 Friction observée
> **Projection (par cohérence P0/P1/P2 v2 + analyse 4 failure modes Drew Breunig, validée 2026-06-06)** :
> - **F1 — Coordination multi-agent** : 3-5 sub-agents en parallèle + Nexus-Critic T1+T2+T3 obligatoire = 5-7 invocations potentielles. Mitigation = Nexus-Architect lead synthèse, F10 recherche 2026 (subagent output → filesystem, pas de dump).
> - **F2 — Budget tokens** : hard cap 15k = 2e phase la plus large (ex-aequo avec P5). Mitigation = token counter live (pre-tool-use/token-counter.sh), compaction 60-70% (F8), budget prévisible.
> - **F3 — Consultation envelope strict** : slicing manuel des NFR P2 + ADRs P3 en cross-phase = discipline à tenir. Mitigation = format double md+json (P2) + format différencié md+json/OpenAPI (P3) = slicing trivial.
> - **F4 — ADRs formalisés** : sur-coût rédaction vs simple "on a choisi X". Mitigation = minimum 1 par décision structurante (pas de max) = pas de sur-coût pour les projets simples, template ADR Nygard (Contexte/Décision/Alternatives/Conséquences) = structure pré-remplie.
> - **F5 — Threat model STRIDE** : si security-sensitive = obligatoire. Mitigation = template STRIDE pré-rempli, validation par Nexus-Security + CISO.
> - **F6 — Format contracts différencié** : md+json pour modules internes, OpenAPI pour API REST, AsyncAPI pour événements = 3 formats à gérer. Mitigation = `openapi-lint` + `asyncapi-lint` (validation automatique), spec v2 section "Format des fichiers" explicite.
>
> **Cohérence P0/P1/P2 v2** : aucune friction majeure remontée à date (audits clos sans friction bloquante). Les patterns (consultation envelope, UDL, 4 failure modes) sont stables depuis P0 v2 (2026-06-04). La friction principale = gestion du multi-agent (3-5 sub-agents en parallèle) qui n'existe PAS en P0/P1/P2 (single-agent ou séquentiel strict). C'est une friction nouvelle, attendue, et documentée.

### 7.3 Pattern de contournement probable
> **Projection (par cohérence P0/P1/P2 v2 + analyse 4 failure modes Drew Breunig, validée 2026-06-06)** :
> - **Contournement C1 — Court-circuit P3 → P4** : si P3 est trop lourde ou trop conflictuelle (3 reviewers en désaccord), le mainteneur pourrait être tenté d'aller directement de P2 à P4 en perdant la valeur des ADRs. **Mitigation** : (1) ADRs = minimum 1 par décision structurante (pas de max) = pas de sur-coût pour les projets simples, (2) critère démarcation P3/P4 explicite (quoi+pourquoi vs comment) = pas d'ambiguïté sur ce qui est P3 vs P4, (3) hard cap 15k = budget prévisible, (4) format contracts différencié (md+json modules, OpenAPI REST) = OpenAPI = valeur concrète pour P5 (génération de code), (5) entry gate EG-3.1 (P2 SRS approuvé) obligatoire pour démarrer P3 = pas de court-circuit possible.
> - **Contournement C2 — Skip Nexus-Critic** : si budget sature, tentation de skip Nexus-Critic pour gagner ~4.5k tokens. **Mitigation** : Nexus-Critic T1+T2+T3 rendu obligatoire (décision 2026-06-06) + hard cap 15k = marge de sécurité. Skip = violation de spec.
> - **Contournement C3 — ADR vide** : tentation de livrer un ADR "Contexte: X / Décision: Y / Alternatives: aucune" = ADR creux = mode d'échec 6.2.E documenté. **Mitigation** : Nexus-Critic T1 casseur cible spécifiquement les ADRs creux (mitigation spec v2 section "Mode 1 — Poisoning").
> - **Contournement C4 — Format uniforme** : tentation de tout livrer en md seul (pas de json, pas d'OpenAPI) = perd la machine-parse-abilité P5. **Mitigation** : format différencié explicite dans la spec v2 + `openapi-lint` / `asyncapi-lint` en validation automatique.
>
> **Cohérence P0/P1/P2 v2** : aucun contournement remonté. Le main lien est que P2 SRS est obligatoire pour démarrer P3 (entry gate EG-3.1) = pas de court-circuit P2→P4 possible. P3 hérite du même principe (P3 architecture baseline locked pour démarrer P4).

### 7.4 Valeur ajoutée perçue
> **Attendue** : éviter le "design-by-committee" et l'over-engineering architectural. ADRs formalisés = mémoire des décisions. Threat model = sécurité dès l'archi (pas après l'implémentation). Format contracts différencié (OpenAPI REST) = génération de code accélérée en P5. Critère démarcation P3/P4 explicite = pas d'ambiguïté à la transition.

### 7.5 Dette d'orchestration
> **Risque résolu (2026-06-06)** : 3-5 sub-agents en parallèle + Nexus-Critic T1+T2+T3 obligatoire = risque de saturation. **Hard cap 12k → 15k** (décision mainteneur 2026-06-06), sort du risque. P3 devient 2e phase la plus large (ex-aequo avec P5), justifié par la qualité (ADRs + threat model + contrats propres).

### 7.6 Verdict
- [x] 🟢 **OK** : 7.1/7.2/7.3 comblées par projection + cohérence P0/P1/P2 v2 (décision mainteneur 2026-06-06). Validation terrain toujours souhaitée (mini-projet test OU avis expert externe) mais ne bloque plus le verdict. Action P3-8 ('mesurer usage réel') reste dans la stratégie roadmap pour validation différée.

---

## Section 8 — Context Engineering (transverse)

### 8.1 Token budget alloué
**Validé 2026-06-06** : **5k base / 8k soft / 15k hard** (multi-agent justifié, Nexus-Critic T1+T2+T3 obligatoire). P3 devient 2e phase la plus large (ex-aequo avec P5 Implementation), 3e plus large (P5) et 1er budget (P5) restent inchangés. Justification : 3-5 sub-agents × 1.5k + Nexus-Critic T1+T2+T3 × 1.5k = ~12k en nominal, hard cap 15k = marge de sécurité.

### 8.2 Compaction checkpoint
- [ ] A. Tous les 5 tool calls
- [ ] B. À 70% du soft cap (5.6k)
- [x] C. Les deux (belt + suspenders)
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
- [x] A. Phase 2 outputs (SRS, NFR) en consultation envelope
- [x] B. Phase 1 outputs (stack candidate, business case) en consultation envelope
- [x] C. **Mode consultation envelope strict** (jamais injecter tout P0-P2)
- [x] D. **+ Slice du SRS** (juste les NFR et use case, pas tout)
- [x] E. **+ Pas d'injection complète des diagrams des phases précédentes** (référencer, ne pas charger)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret
- [x] A. T1 : architecte A propose, architecte B casse
- [x] B. T2 : Nexus-Critic vérifie ISO 42010 + conformité NFR
- [x] C. T3 : Nexus-Critic prédit les difficultés P4 Design
- [x] D. **+ Pas de Council en standard** (escalade mainteneur sur NFR conflictuels)
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger
**7 éléments P3-spécifiques confirmés par le mainteneur (2026-06-05)** :

1. **Décision architecturale** — choix structurant (monolith vs microservices, SQL vs NoSQL, etc.)
2. **ADR signé** — pointeur vers l'ADR (adr-001, adr-002, ...)
3. **Alternative écartée** — option non choisie + pourquoi
4. **Threat identifié** — menace architecturale + mitigation
5. **Interface contract architectural** — pointeur vers le contrat d'interface
6. **Rejet T1/T2 casseur** — quand Nexus-Critic a trouvé un problème et comment c'est résolu
7. **Décision "pas de décision"** — cas où on a choisi de NE PAS trancher, et pourquoi

Stockés dans `.swebok_state.db` (table `udl_p3`) et consultables via Consultation Envelope (A1) par P4 Design.

### 8.6 Verdict
- [x] 🟢 OK (section 8.7 findings intégrés, 8.5 UDL 7 éléments comblé en spec v2, budget 5k/8k/15k aligné (vs 5k/8k/12k en v1, justifié par Nexus-Critic T1+T2+T3 obligatoire), 8.2 compaction 60-70% retenu, 8.3 consultation envelope strict, 8.4 pattern adversarial T1+T2+T3 obligatoire explicité)

### 8.7 Validation empirique 2026 (recherche complémentaire)

#### Findings les plus pertinents pour cette phase
- **F2** : Multi-agent = 15× tokens chat → fan-out Nexus-Architect + Nexus-Security + Nexus-Backend + Nexus-Frontend + Nexus-DevOps = **justifié uniquement si P+1/P+2 en profitent** (et c'est le cas : alimente P4 Design)
- **F3** : Subagent brief = OBJECT/FORMAT/TOOLS/BOUND → auditer les 4 spawns parallèles
- **F5** : Lost-in-the-middle = -30% accuracy en positions 5-15 → **diagrammes clés (C4, sequence) en tête/queue** du contexte Nexus-Architect, pas au milieu
- **F13** : 3-5 subagents en parallèle max (FlowHunt) → ne pas dépasser, sinon overhead > gain
- **F10** : Subagent output → filesystem → les ADRs et contrats d'interface sont écrits dans le state, le retour au lead = pointeur

#### Anti-patterns à éviter dans cette phase
- **AP1** : 50 subagents — plafonner à 3-5 (Arch, Sec, Data) sauf complexité avérée
- **AP4** : Peer-to-peer entre Nexus — pas de canal direct, tout via Hyperagent ou state
- **AP2** : Brief vague — chaque subagent a un scope écrit dans le DSL
- **AP7** : Contexte "flood" — ne JAMAIS charger le corpus entier

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : un ADR faux qui contamine les contrats d'interface aval
- [x] **Distraction** : trop d'options architecturales (over-engineering)
- [x] **Confusion** : trop de patterns candidats sans hiérarchie
- [x] **Clash** : ADRs contradictoires (monolith vs microservices, REST vs GraphQL)

#### Recommandation budget (mise à jour 2026-06-06)
- **Base 5k / Soft 8k / Hard 15k** (multi-agent 3-5 subagents × 1.5k chacun + Nexus-Critic T1+T2+T3 × 1.5k = ~12k nominal, hard cap 15k = marge de sécurité)
- ✅ **Risque saturation levé (2026-06-06)** : hard cap 12k → 15k justifié par Nexus-Critic T1+T2+T3 obligatoire. Action P3-9 ('vérifier saturation') fermée.
- ✅ **Action P3-10 (étendre Drew Breunig à P4-P10) déplacée dans la stratégie roadmap** (`00-context-engineering-strategy.md`).

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 10 |
| New Books achetés (§19) | 3 |
| Standards NIST/OWASP (§13) | 3 |
| Open-access téléchargés | 2 |
| **TOTAL corpus-aligned local** | **18** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~20 livres
- **Disponible localement** : 13 corpus-aligned
- **Couverture effective** : **65%** ██████░░░░

### Lacunes (§20)

- **9** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **suffisantes** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel


## Verdict global de la phase
- [x] 🟢 OK — conforme, rien à changer (toutes les sections comblées, y compris 7 par projection + cohérence P0/P1/P2 v2)
- [ ] 🟡 À fermer en pratique par avis expert externe OU 1-2 projets réels
- [ ] 🔴 À repenser — design ou utilité à revoir fondamentalement

## Liste d'actions
**✅ P1 — bloquants (fermés en spec v2 + grille v2 finale)** :
1. ✅ Section 5.5 comblée en **7 questions précises avec options AskUserQuestion** (transformation 2026-06-06, vs catégories en v1)
2. ✅ Section 8.5 comblée (7 éléments UDL P3-spécifiques)
3. ✅ Verdicts tranchés (sections 1-8 + global = **🟢 partout**)
4. ✅ Spec v2 créée (`specs/workflows/by-phase/phase-3-architecture.md`)
5. ✅ Token counter P3 mis à jour (`pre-tool-use/token-counter.sh` ligne 61 : **5k/8k/15k** vs 5k/8k/12k en v1)
6. ✅ ADRs formalisés comme livrables obligatoires (vs suggestion dans ancienne P3 Design)
7. ✅ Threat model STRIDE rendu obligatoire si security-sensitive
8. ✅ Hard cap 12k → **15k** (justifié par Nexus-Critic T1+T2+T3 obligatoire)
9. ✅ Format contracts différencié (md+json modules internes, md+json+OpenAPI API REST, md+json+AsyncAPI événements option)
10. ✅ Critère explicite de démarcation P3/P4 (quoi+pourquoi vs comment, inscrit dans P3 et P4)
11. ✅ ADRs = minimum 1 par décision structurante, pas de max (pas de fourchette indicative fixe par cas)
12. ✅ Action P3-9 (saturation Nexus-Critic) **fermée** (hard cap 15k absorbe)
13. ✅ Action P3-10 (étendre Drew Breunig à P4-P10) **déplacée dans la stratégie** (`00-context-engineering-strategy.md` roadmap)
14. ✅ **Section 7 comblée par projection + cohérence P0/P1/P2 v2** (décision mainteneur 2026-06-06, 7.1/7.2/7.3 remplies)
15. ✅ Verdict global 🟢 (toutes sections vertes, validation terrain reste souhaitée mais non bloquante)

**🟢 P2 — qualité (non bloquant, améliorations futures)** :
16. 🟢 Action P3-8 (mesurer usage réel P3) **maintenue dans la stratégie roadmap** pour validation terrain différée (mini-projet test OU avis expert externe, à déclencher v1.6.0 ou v2.0)
17. 🟢 Validation empirique de la projection 7.1/7.2/7.3 par 1-2 projets réels = nice-to-have, planifié en roadmap P2-9 de la stratégie

## Notes libres
> **Phase 3 Architecture = v2 finale validée 2026-06-06 (verdict 🟢)**. Phase créée lors du fix structurel (split P3 Design en P3 Architecture + P4 Design).
> **Méthode audit 2026-06-06** : grille offline (mainteneur) + **6 questions AskUserQuestion** (Claude) + rédaction spec v2 (Claude) + mise à jour grille v2 (Claude) + mise à jour stratégie (Claude) + **deuxième vague 2 questions** (Claude) pour fermer section 7 + transformer 5.5 en questions précises.
> **8 décisions tranchées par le mainteneur** : (1) hard cap 15k (Nexus-Critic T1+T2+T3 obligatoire), (2) format contracts différencié, (3) démarcation P3/P4 explicite dans P3 ET P4, (4) section 7 fermée par projection + cohérence P0/P1/P2 v2, (5) action P3-10 déplacée dans la stratégie, (6) ADRs = minimum 1 par décision structurante, pas de max, (7) section 5.5 transformée en 7 questions précises avec options, (8) verdict global 🟢 validé.
> **Verdict global 🟢** (toutes les sections vertes, y compris 7 par projection + cohérence P0/P1/P2 v2). Validation terrain reste souhaitée mais ne bloque plus le verdict.
> Cible universelle adaptative (6 cas). Budget 5k/8k/15k tokens (P3 = 2e plus large, ex-aequo avec P5), cap 35 min, 3-5 agents en parallèle + Nexus-Critic T1+T2+T3 obligatoire.
> 9 livrables (8 md + répertoire adrs/) en format différencié (md+json pour modules internes, md+json+OpenAPI pour API REST, md+json+AsyncAPI pour événements option). ADRs minimum 1 par décision structurante.
> ADRs formalisés = amélioration majeure vs ancienne P3 Design (qui les suggérait seulement).
> Tension principale résolue : 3-5 sub-agents en parallèle + Nexus-Critic T1+T2+T3 = ~12k nominal, hard cap 15k absorbe.
> Méthode d'audit reproductible pour P4-P10 : grille offline (mainteneur) + 4-6 questions AskUserQuestion (Claude) + rédaction spec v2 + mise à jour grille v2. Section 7 = projection + cohérence P0/P1/P2 v2 par défaut (verdict 🟢 immédiat), validation terrain nice-to-have en roadmap.
