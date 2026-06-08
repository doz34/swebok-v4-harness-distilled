# Phase 4: Design Workflow Spec

> **Statut** : v2 — validé 2026-06-07 par le mainteneur (audit P4 clos via grille offline + 4 questions ciblées, vague 1)
> **Changement vs v2-renum** : (1) hard cap 10k → **15k** (Nexus-Critic T1+T2+T3 obligatoire, justifié par saturation à 10k comme P3 v2), (2) format contracts différencié aligné P3 v2 (md+json pour modules internes, +OpenAPI 3.0 pour API REST, +AsyncAPI 3.0 pour événements option), (3) **critère explicite de démarcation P3↔P4** inscrit dans P4 (quoi+pourquoi vs comment, règle ≥2 bounded contexts), (4) section 5.5 transformée en **7 questions précises avec options AskUserQuestion** (vs 5 catégories en v2-renum), (5) section 7 comblée par **projection + cohérence P0/P1/P2/P3 v2**, (6) UDL 7 éléments P4-spécifiques documentés (vs absent en v2-renum), (7) audit des 4 failure modes Drew Breunig complet (vs absent en v2-renum). 4 décisions tranchées par le mainteneur.
> **Changement vs structure antérieure** : P3 (Design) splitté en P3 (Architecture) + P4 (Design) le 2026-06-05 (fix structurel).
> **But** : transformer l'architecture P3 validée en spécifications design détaillées (interfaces modules, structures de données, algorithmes, error handling, logging) au niveau module — pour que P5 Implementation puisse coder sans re-conception.

## Metadata

- **Phase**: 4
- **Name**: Design
- **Purpose**: Consume the P3 architecture baseline (ADRs + interface contracts) and produce implementation-ready detailed design specifications (module interfaces, data structures, algorithms, error handling, logging)
- **Parallel Mode**: Hyperagent enabled (multi-agent justifié, F13 recherche 2026 — read-heavy parallèle + disjoint tools)
- **Équivalent SWEBOK v4** : P3 SWEBOK (Software Design KA)
- **Référentiels** : IEEE 1016-2009 (Software Design Description), ISO/IEC/IEEE 42010:2011 (architecture description — utilisé pour la traçabilité)

---

## Mission (1 phrase)

> « Consommer les ADRs P3 et descendre au niveau module : interfaces, structures de données, algorithmes, error handling, logging — pour que P5 Implementation puisse coder sans re-conception ni ré-décision architecturale. »

---

## Critère de démarcation P3 (Architecture) vs P4 (Design)

> **Validation 2026-06-07** : le mainteneur a tranché pour un critère explicite, symétrique à la section équivalente de P3 v2 (inscrit dans P3 ET P4 — action P3-3 du mainteneur 2026-06-06).

| Dimension | P3 Architecture | P4 Design (cette spec) |
|-----------|-----------------|------------------------|
| **Question centrale** | **QUOI** + **POURQUOI** | **COMMENT** |
| **Décomposition** | Bounded contexts, subsystems, services, couches (vue macro) | Modules, classes, fonctions, signatures internes (vue micro) |
| **Style** | Monolith vs microservices vs serverless vs event-driven (choix structurant + ADR) | Patterns tactiques (Repository, Factory, Strategy) au sein des modules |
| **Données** | Schéma logique, stratégie de stockage, modèle de cohérence, stratégie de partitioning | Schéma physique, index, migrations, requêtes |
| **Sécurité** | Patterns (defense in depth, zero trust), authn/authz patterns, threat model STRIDE, chiffrement strategy | Détails d'implémentation (qui appelle quoi, gestion des tokens, rotation de clés) |
| **Intégration** | API gateway, event bus, protocoles (REST, gRPC, async), versioning strategy | Endpoints concrets, schémas de messages, retry/backoff, error handling |
| **Contrats d'interface** | Externes (APIs publiques, événements publiés) ET internes entre bounded contexts (modules) | Internes au module (signatures de fonctions, classes, interfaces in-process) |
| **ADRs** | Décisions structurantes (style archi, choix DB, choix sécurité) | Décisions tactiques (algorithme, structure de données, library) — **consommation des ADRs P3, pas de re-décision silencieuse** |
| **Livrables typiques** | `architectural-design.md`, `system-decomposition.md`, `data-architecture.md`, `security-architecture.md`, `integration-architecture.md`, `architectural-interface-contracts.md` (contrats externes + inter-contextes), `adrs/`, `architecture-traceability-matrix.md`, `architecture-review-report.md` | `detailed-design.md` (DDS par module), `module-interfaces.md`, `data-structures.md`, `error-handling-design.md`, `logging-design.md`, `design-traceability-matrix.md` (DTAM + DRTM), `design-review-report.md` |

**Règle simple** : si la décision impacte **plus d'un bounded context** ou **plus d'une équipe**, c'est P3. Si elle impacte **un module ou une classe**, c'est P4.

**Cas limite type** : "Monolith modulaire avec 3 bounded contexts" = P3 (style archi). "Module Billing = Repository pattern + factory pour les stratégies de pricing" = P4.

**Conséquence opérationnelle** : si P4 détecte qu'une décision descendante impacte ≥2 bounded contexts, **elle escalade P3** (refus catégorique 5 — pas de design qui dévie des ADRs P3 sans escalade).

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-4.1 | Phase 3 architecture approved | Architecture baseline version | Approved version locked |
| EG-4.2 | ADRs signed | ADR set completeness | 100% structurants ADRs signés |
| EG-4.3 | Architectural interfaces defined | Interface contracts v1 | API contracts figés au niveau archi |
| EG-4.4 | Design environment prepared | Tool access and permissions | All designers have write access |
| EG-4.5 | Module assignment matrix defined | Module-to-team mapping | 100% modules assigned |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers Phase 3 (Architecture) remediation.

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-4.1 | Detailed design specifications complete | DDS coverage per module | 100% modules with DDS |
| XG-4.2 | Design review approved | DR minutes and sign-off | Formal approval documented |
| XG-4.3 | Interface contracts finalized (module-level) | Contract documents | 100% modules with contracts (md+json modules, +OpenAPI REST, +AsyncAPI events) |
| XG-4.4 | Design-to-Architecture traceability established | DTAM coverage | 100% design elements traced to archi (consumption of P3 ADRs verified) |
| XG-4.5 | Design-to-Requirements traceability established | DRTM coverage | 100% design elements traced to reqs |
| XG-4.6 | UDL 7 éléments P4-spécifiques loggés | UDL set | 100% loggés dans `.swebok_state.db` |
| XG-4.7 | Conformité aux ADRs P3 vérifiée | Matrice ADR → module | 100% ADRs P3 tracés par module (pas de déviation silencieuse) |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` requires design rework cycle.

---

## Transition Criteria to Phase 5 (Implementation)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Design baseline frozen | Nexus-Architect | Phase 5 Lead (Nexus-Backend/Frontend) | Design baseline memo |
| Interface contracts ratified (module-level) | Nexus-Architect | Nexus-Backend/Frontend | Contract signatures |
| Detailed design sign-off | Nexus-Architect | Project Lead | DDS review minutes |
| Design traceability audit passed | Nexus-QA | Design Lead | DTAM + DRTM verification report |
| Technical debt assessment done (design level) | Nexus-Architect | Project Lead | Debt report approved |
| Conformité aux ADRs P3 vérifiée | Nexus-Architect | Phase 5 Lead | Matrice ADR → module |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_4_COMPLETE` only when all transition criteria verified with formal evidence.

---

## Key Activities

### Activity 4.1: Detailed Design
- Design module interfaces (signatures, types, comportements) — md+json modules internes
- Define data structures and algorithms per module
- Design error handling and exception management
- Specify logging and monitoring requirements
- Design testability hooks (test seams, mocks, fixtures)

### Activity 4.2: Design Specification
- Document detailed design decisions (DDS par module)
- Create design models (UML, sequence, state machines) par module
- Specify design patterns employed (par module, mapping module → pattern)
- Document component-level security controls
- Document conformity to P3 ADRs (matrice ADR → module)

### Activity 4.3: Design Validation
- Conduct design reviews (peer + archi)
- Validate detailed design against architecture AND requirements
- Verify traceability coverage (DTAM + DRTM, 100% chacun)
- Assess design quality metrics (cohesion, coupling, complexity)
- Predict P5 Implementation difficulties (T3 Nexus-Critic)

---

## Responsible Agents

| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordinates parallel detailed design tasks (3-5 sub-agents) |
| Nexus-Architect | Lead, synthesis, ADR P3 consumption verification, conformité archi |
| Nexus-Backend | Backend module detailed design (interfaces, structures de données, algos, error handling) |
| Nexus-Frontend | Frontend component detailed design (signatures, state management) |
| Nexus-DevOps | Infrastructure detailed design (CI/CD scripts, observabilité, runbooks P8) |
| Nexus-Security | Security controls detailed design (qui appelle quoi, gestion tokens, rotation clés) |
| **Nexus-Critic (5e agent obligatoire — décision mainteneur 2026-06-07)** | **T1 casseur + T2 conformité NFR P2 + T3 prédiction aval P5 — TOUS OBLIGATOIRES** (3 invocations systématiques, comme P3) |

**Concurrency** : multi-agent justifié (F13 recherche 2026 — read-heavy parallèle : ADRs P3 + NFR P2 + contracts archi). 3-5 sub-agents en parallèle, jamais plus. **Nexus-Critic = 3 invocations systématiques** (T1 casse le DDS, T2 vérifie conformité NFR P2 + ADRs P3, T3 prédit les ruptures P5). Coût additionnel ~4.5k tokens, justifié par le hard cap 15k.

**Patterns adversariaux T1/T2/T3 (rappel)** :
- **T1 (casseur)** : un dev propose DDS, Nexus-Critic casse. Cible : DDS, contrats d'interface module, design patterns choisis.
- **T2 (spec-compliance)** : Nexus-Critic vérifie conformité NFR P2 + ADRs P3 (matrice ADR → module obligatoire). Cible : detailed-design.md + tous les livrables structurants.
- **T3 (conséquentialiste)** : Nexus-Critic prédit ce qui va être dur à implémenter en P5 (casses potentiels, zones d'ambiguïté, dépendances cachées). Cible : DTAM + contrats d'interface + patterns tactiques.

**Isolation des contextes (ACI stratégie §4.5)** : Nexus-Critic ne voit pas le prompt système des producteurs. Chaque rôle adversarial a un contexte distinct, sinon les "adversaires" se laissent influencer par le contexte partagé.

---

## Required Skills

- `nexus-architect`: Design conformance to architecture (consumption of P3 ADRs)
- `nexus-backend`: Module detailed design
- `nexus-frontend`: Component detailed design
- `nexus-devops`: Infrastructure detailed design
- `nexus-security`: Security controls design
- `nexus-critic`: Adversarial validation (T1 casseur + T2 conformité + T3 aval) — **OBLIGATOIRE** (3 invocations)
- `speckit-qa`: Design quality assurance

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-design-approved` | Exit criteria met | Triggers Phase 5 (Implementation) initiation |
| `detailed-design-frozen` | Design complete | Locks detailed design baseline |
| `module-contracts-finalized` | Module interfaces defined | Enables parallel implementation |
| `design-review-approved` | Design review passed | Proceeds to implementation |
| `adr-p3-conformity-verified` | Matrice ADR → module done | Unblocks P5 |
| `udl-p4-logged` | 7 éléments UDL loggés | Snapshot pour phases suivantes |

---

## Artifacts Produced

| Artifact | Description | Location | Format |
|----------|-------------|----------|--------|
| `detailed-design.md` | Module-level design specifications (DDS par module) | `specs/workflows/by-phase/phase-4-design/` | md |
| `module-interfaces.md` | Module signatures, types, comportements | `specs/workflows/by-phase/phase-4-design/` | **md+json** (modules internes in-process) |
| `data-structures.md` | Data structures and algorithms per module | `specs/workflows/by-phase/phase-4-design/` | md |
| `error-handling-design.md` | Error handling and exception strategy (par module) | `specs/workflows/by-phase/phase-4-design/` | md |
| `logging-design.md` | Logging and monitoring specifications (par module) | `specs/workflows/by-phase/phase-4-design/` | md |
| `design-traceability-matrix.md` | Design-to-Architecture (DTAM) + Design-to-Requirements (DRTM) | `specs/workflows/by-phase/phase-4-design/` | md |
| `design-review-report.md` | Detailed design review findings + sign-offs | `specs/workflows/by-phase/phase-4-design/` | md |

**Format contracts différencié (aligné P3 v2 — décision mainteneur 2026-06-07)** :
- **Modules internes** (appels in-process entre bounded contexts, ex: `BillingService.Notify(userId)`) : **md+json**. Pas d'OpenAPI car pas de transport réseau, le tooling P5 génère les stubs directement à partir du json.
- **API REST** (HTTP endpoints exposés par un module, ex: `POST /api/v1/payments`) : **md+json+OpenAPI 3.0**. OpenAPI car le tooling P5 (génération de clients) consomme du standard. Validation par `openapi-lint`.
- **Événements async** (pub/sub sur event bus, ex: `PaymentConfirmed` event) : **md+json+AsyncAPI 3.0** (option, à valider au cas par cas).

**Matrice de conformité aux ADRs P3** : ajoutée comme livrable obligatoire (XG-4.7). Chaque module documente quels ADRs P3 il consomme et comment. Pas de déviation architecturale silencieuse.

**Diagrammes (UML, sequence, state machines)** par module : ajoutés comme livrables complémentaires (optionnels mais recommandés pour P5).

---

## Format des fichiers (triple différencié, aligné P3 v2)

> **Validation 2026-06-07** : format triple différencié par type de livrable (aligné P3 v2, vs format uniforme en v2-renum).

| Type de livrable | Format primaire | Format secondaire | Standard |
|------------------|------------------|-------------------|----------|
| **Specs narratives** (detailed-design, data-structures, error-handling, logging, DTAM, review-report) | md (lecture humaine) | — | — |
| **Contrats modules internes** (module-interfaces.md) | md (lecture humaine) | json (machine-parse) | — |
| **Contrats API REST** (subset de module-interfaces.md, si applicable) | md (lecture humaine) | json (machine-parse) | **OpenAPI 3.0** |
| **Événements async** (subset de module-interfaces.md, si applicable) | md (lecture humaine) | json (machine-parse) | **AsyncAPI 3.0** (option) |

**Convention de nommage** :
- Specs narratives : `${livrable}.md`
- Contrats modules internes : `${module}-contract.md` + `${module}-contract.json`
- Contrats API REST : `${api-name}.md` + `${api-name}.json` + `${api-name}.openapi.yaml`
- Événements async : `${event-name}.md` + `${event-name}.json` + `${event-name}.asyncapi.yaml` (si applicable)

**Localisation** : tous dans `specs/workflows/by-phase/phase-4-design/`.

---

## Hyperagent Parallel Processing

```
parallel_tasks:
  - task: detailed_design_backend
    agents: [Nexus-Backend, Nexus-Architect]
    sync: false

  - task: detailed_design_frontend
    agents: [Nexus-Frontend, Nexus-Architect]
    sync: false

  - task: detailed_design_infrastructure
    agents: [Nexus-DevOps, Nexus-Architect]
    sync: false

  - task: detailed_design_security
    agents: [Nexus-Security, Nexus-Architect]
    sync: false

adversarial_tasks (Nexus-Critic, sequential après parallel):
  - task: t1_casseur
    agents: [Nexus-Critic]
    target: detailed-design.md + module-interfaces.md
    sync: true

  - task: t2_conformite
    agents: [Nexus-Critic]
    target: detailed-design.md vs NFR P2 + ADRs P3
    sync: true

  - task: t3_prediction_p5
    agents: [Nexus-Critic]
    target: DTAM + contrats d'interface + patterns tactiques
    sync: true

reduction: "Nexus-Architect synthesizes all into detailed-design.md + matrice ADR P3"
```

---

## Refus catégoriques (5)

La phase P4 **refuse** de :
1. **Pas de code d'implémentation** (uniquement pseudo-code et signatures — P5 s'en charge)
2. **Pas de tests d'implémentation** (P6 Testing)
3. **Pas de re-décision architecturale** (escalade P3 si nécessaire — règle de démarcation)
4. **Pas de design qui ne respecte pas les NFR P2** (sécurité, perf, scalabilité)
5. **Pas de design qui dévie des ADRs P3 sans escalade** (matrice ADR → module obligatoire, XG-4.7)

---

## Critères d'abandon (4 + temps)

L'agent abandonne et prévient le mainteneur si :
1. ADR P3 non respecté et déviation non escaladée (escalade P3)
2. NFR conflictuels (perf vs cost) non résolus par mainteneur
3. Interface contract module impossible à implémenter (côté P5) — escalade P5 ou P3
4. Security design détaillé rejeté par Nexus-Security
5. Dépassement de 35 min sans avancée claire

---

## Tokens budget

- **Base** : 5k tokens
- **Soft cap** : 8k tokens (alerte, compaction 60-70%)
- **Hard cap** : 15k tokens (compactage forcé + abort)

Multi-agent justifié (F13 recherche 2026) : 3-5 sub-agents en parallèle × 1.5k chacun = 4.5-7.5k base. Cap 15k hard pour absorber les validations adversariales T1+T2+T3 obligatoires (Nexus-Critic en mode rotation sur les 3 patterns, comme P3 — décision mainteneur 2026-06-07). **Justification du passage 10k → 15k** : Nexus-Critic T1+T2+T3 obligatoire = 3 invocations × ~1.5k = 4.5k additionnel, ce qui sature le budget 10k en nominal. 15k = marge de sécurité, en cohérence avec P3 Architecture (5k/8k/15k) et P5 Implementation (5k/10k/15k).

**Note** : P4 devient 3e phase la plus large (après P3 et P5), au lieu de la 4e. Acceptable car le design détaillé est l'activité qui consomme les ADRs P3 et alimente P5. Le sur-coût est compensé par la qualité (matrice ADR → module, contrats différenciés, démarcation explicite, 4 failure modes Drew Breunig).

---

## Pauses

Toutes les 5 actions : compaction checkpoint à 60-70% du soft cap (5.6k tokens, F8 recherche 2026).

---

## Couverture corpus (état 2026-06-06)

- **8 livres corpus-aligned** sur ~20 recommandés = **40%** de couverture
- **1 livre open-access** (Ousterhout, A Philosophy of Software Design)
- **4 livres manquants critiques** : Refactoring 2nd ed. (Fowler 2018), Refactoring 1st ed. (Fowler 1999), Refactoring to Patterns (Kerievsky 2004), Code Complete 2nd ed. (McConnell 2004)
- **Décision mainteneur 2026-06-06** : 40% suffit pour P4 (phase moins "core" pour la spec SWEBOK, plus basée sur patterns). Batch d'acquisition ultérieur.

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :
1. **Greenfield from-scratch** : DDS riches par module, 5-10 modules typiques, matrice ADR P3 complète
2. **Maintenance legacy** : DDS = "que doit-on modifier pour respecter le design existant", dette technique
3. **Projet interne** (équipe, gouvernance légère) : DDS standard, matrice ADR P3 allégée
4. **Projet externe client** : DDS revus par architecte client, sign-off formel
5. **Compliance-driven** : DDS security-heavy, conformité ADRs P3 renforcée
6. **R&D / exploration** : DDS = POC, documentation minimale, matrice ADR P3 simplifiée

---

## UDL — 7 éléments P4-spécifiques

> **Validation 2026-06-07** : 7 éléments P4-spécifiques (vs 6 en P1, 7 en P2, 7 en P3 — alignement).

| Élément | Description | Exemple |
|---------|-------------|---------|
| Déviation ADR P3 proposée | Toute déviation avec rationale (escaladée P3 si confirmée) | "Module X propose d'utiliser SQL vs ADR-005 NoSQL, escaladé P3" |
| Module interface ratified | Pointeur vers `module-interfaces.md` | "Voir module-billing-contract.md § 2.3" |
| Pattern utilisé par module | Mapping module → pattern | "Module Billing = Repository + Factory pour stratégies de pricing" |
| Trade-off design arbitrée | Algo complexity vs readability, perf vs mémoire | "Tri en O(n log n) retenu vs O(n) hashing, plus lisible" |
| Rejet T1/T2 casseur | Quand Nexus-Critic a trouvé un problème et comment c'est résolu | "T1 a trouvé error swallowing dans module Y, corrigé via try/catch + log" |
| Conformité ADR vérifiée | Matrice ADR → module, déviation nulle | "Tous les modules consomment les ADRs P3 sans déviation (XG-4.7)" |
| Décision "pas de décision" | Cas où on a choisi de NE PAS trancher, et pourquoi | "Pas d'arbitrage perf vs memory pour cache : escaladé P5" |

Stockés dans `.swebok_state.db` (table `udl_p4`) et consultables via Consultation Envelope (A1) par P5 Implementation.

---

## Conditions de sortie (passage à P5)

Le mainteneur valide avec une **checklist à 100%** (8 critères) :
- [ ] `detailed-design.md` existe (DDS 100% modules)
- [ ] `module-interfaces.md` existe (100% modules, format différencié md+json modules internes, +OpenAPI API REST si applicable)
- [ ] `data-structures.md` existe
- [ ] `error-handling-design.md` existe
- [ ] `logging-design.md` existe
- [ ] `design-traceability-matrix.md` existe (DTAM 100% + DRTM 100%)
- [ ] `design-review-report.md` existe (sign-off + T1+T2+T3 Nexus-Critic passés)
- [ ] Matrice de conformité aux ADRs P3 documentée (XG-4.7)
- [ ] UDL 7 éléments loggés

Pas de feu vert séparé — les documents font foi.

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-07

### Mode 1 — Poisoning (Empoisonnement)
**Risque en P4** : un DDS faux ou incohérent qui contamine tout le code P5 (effet papillon module par module).

**Mitigations spec v2** :
1. Chaque DDS challengé par Nexus-Critic T1 casseur (3 invocations systématiques, comme P3)
2. Conformité aux ADRs P3 vérifiée par matrice ADR → module (XG-4.7) — pas de déviation architecturale silencieuse
3. Validation mainteneur finale (checklist 8 critères) = catch du poison
4. UDL 6 ("rejet T1/T2 casseur") logge les DDS rejetés et comment c'est résolu

**Status** : ✅ Validé (4 mécanismes)

### Mode 2 — Distraction (Distraction)
**Risque en P4** : trop de patterns, trop d'abstractions, design-by-committee.

**Mitigations spec v2** :
1. Refus catégorique 1 (pas de code d'implémentation) + 3 (pas de re-décision archi) = focus forcé
2. Budget 5k/8k/15k (large mais pas infini, force à prioriser)
3. 3-5 sub-agents max (vs 50 subagents, F2 recherche 2026)
4. UDL 3 ("pattern utilisé par module") force à documenter le mapping pattern → module
5. UDL 4 ("trade-off design arbitrée") force à documenter les compromis

**Status** : ✅ Validé (5 mécanismes)

### Mode 3 — Confusion (Confusion)
**Risque en P4** : 2 modules utilisent le même mot pour 2 interfaces différentes, ou DDS contradictoires entre modules.

**Mitigations spec v2** :
1. Format contracts différencié (md+json modules internes, +OpenAPI API REST) = parsing structuré, pas de place pour le flou
2. UDL 2 ("module interface ratified") trace chaque interface par pointeur unique
3. Nexus-Critic T2 conformité NFR P2 + ADRs P3 détecte les clashes
4. UDL 7 ("décision 'pas de décision'") logge les cas ambigus escaladés

**Status** : ✅ Validé (4 mécanismes)

### Mode 4 — Clash (Conflit)
**Risque en P4** : 2 modules qui s'appellent avec des contrats différents (A appelle B avec X, B appelle A avec Y).

**Mitigations spec v2** :
1. Module interface contracts en format machine-parse (json) = détectable automatiquement
2. Nexus-Critic T3 prédit les ruptures aval P5 (anti-pattern clash Breunig)
3. UDL 1 ("déviation ADR P3 proposée") documente les options non alignées
4. Critère d'abandon 3 (interface contract impossible à implémenter) = escalade P5 ou P3
5. Critère d'abandon 1 (ADR P3 non respecté sans escalade) = sortie propre

**Status** : ✅ Validé (5 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | DDS faux contamine P5 | 4 mécanismes | ✅ |
| Distraction | Over-engineering, design-by-committee | 5 mécanismes | ✅ |
| Confusion | Même mot, 2 interfaces | 4 mécanismes | ✅ |
| Clash | Contrats contradictoires entre modules | 5 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Pattern reproductible de P0/P2/P3 v2 étendu à P4.

---

## Notes de version

- **v2 (2026-06-07)** : refonte ciblée via audit (grille offline + 4 questions ciblées vague 1). Changements : (1) hard cap 10k → 15k (Nexus-Critic T1+T2+T3 obligatoire, comme P3 v2), (2) format contracts différencié aligné P3 v2 (md+json modules internes, +OpenAPI 3.0 API REST, +AsyncAPI 3.0 événements option), (3) critère explicite de démarcation P3↔P4 inscrit dans P4 (quoi+pourquoi vs comment, règle ≥2 bounded contexts), (4) section 5.5 transformée en 7 questions précises avec options AskUserQuestion (vs 5 catégories en v2-renum), (5) section 7 comblée par projection + cohérence P0/P1/P2/P3 v2 (vs vide en v2-renum), (6) UDL 7 éléments P4-spécifiques documentés (vs absent en v2-renum), (7) audit des 4 failure modes Drew Breunig complet (vs absent en v2-renum). 4 décisions tranchées par le mainteneur.
- **v2-renum (2026-06-05)** : créé suite au fix structurel (split P3 en P3 Architecture + P4 Design). 3 activités, 7 livrables, 5 agents en parallèle + Nexus-Critic OPTIONNEL, 4k/7k/10k tokens, cap 35 min, 5 catégories 5.5, pas d'UDL documenté, pas d'audit Drew Breunig.

Voir `audit/phase-4-design-audit.md` pour la traçabilité des 4 décisions.
