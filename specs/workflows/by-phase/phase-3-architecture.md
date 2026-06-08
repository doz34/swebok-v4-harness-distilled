# Phase 3: Architecture Workflow Spec

> **Statut** : v2 — validé 2026-06-06 (audit P3 clos via grille offline + 6 questions ciblées)
> **Changement vs v1** : hard cap 12k → 15k (Nexus-Critic T1+T2+T3 obligatoire, justifié par saturation à 12k), format contracts différencié (md+json pour modules internes, OpenAPI pour API REST), critère explicite de démarcation P3/P4, ADRs = minimum 1 par décision structurante (pas de max), section 7 maintenue 🟡 avec fermeture différée par avis expert externe.
> **Changement vs structure antérieure** : nouveau. Avant : "P3 Design" fusionnait SWEBOK P2 (Architecture) et P3 (Design). Après : P3 Architecture (ce fichier) = décomposition système, patterns/styles archi, sécurité archi, intégration. P4 Design = detailed design, modules, algos, error handling.
> **But** : produire une architecture système cohérente, validée par 3 architectes minimum, avec ADRs pour chaque choix structurant — pour que P4 Design puisse descendre au niveau module sans ambiguïté.

## Metadata
- **Phase**: 3
- **Name**: Architecture
- **Purpose**: Décider l'architecture système (décomposition, patterns, styles, sécurité archi, intégration) à un niveau stratégique — pour servir de référence à P4 Design détaillé
- **Parallel Mode**: Hyperagent enabled (multi-agent justifié, F13 recherche 2026)
- **Équivalent SWEBOK v4** : P2 SWEBOK (Software Architecture KA)
- **Référentiels** : ISO/IEC/IEEE 42010:2011 (architecture description), IEEE 1016-2009 (design description)

---

## Mission (1 phrase)

> « Produire l'architecture système validée par ≥3 architectes, avec ADRs signés pour chaque choix structurant, et contrats d'interface au niveau archi — pour que P4 Design puisse designer sans ambiguïté et P5 Implementation puisse coder sans re-conception. »

---

## Critère de démarcation P3 (Architecture) vs P4 (Design)

> **Validation 2026-06-06** : le mainteneur a tranché pour un critère explicite, inscrit dans les deux specs (P3 ici + P4).

| Dimension | P3 Architecture (cette spec) | P4 Design |
|-----------|------------------------------|-----------|
| **Question centrale** | **QUOI** + **POURQUOI** | **COMMENT** |
| **Décomposition** | Bounded contexts, subsystems, services, couches (vue macro) | Modules, classes, fonctions, signatures internes (vue micro) |
| **Style** | Monolith vs microservices vs serverless vs event-driven (choix structurant + ADR) | Patterns tactiques (Repository, Factory, Strategy) au sein des modules |
| **Données** | Schéma logique, stratégie de stockage, modèle de cohérence, stratégie de partitioning | Schéma physique, index, migrations, requêtes |
| **Sécurité** | Patterns (defense in depth, zero trust), authn/authz patterns, threat model STRIDE, chiffrement strategy | Détails d'implémentation (qui appelle quoi, gestion des tokens, rotation de clés) |
| **Intégration** | API gateway, event bus, protocoles (REST, gRPC, async), versioning strategy | Endpoints concrets, schémas de messages, retry/backoff, error handling |
| **Contrats d'interface** | **Externes** (APIs publiques, événements publiés) ET **internes** entre bounded contexts (modules) | **Internes** au module (signatures de fonctions, classes, interfaces in-process) |
| **ADRs** | Décisions structurantes (style archi, choix DB, choix sécurité) | Décisions tactiques (algorithme, structure de données, library) |
| **Livrables typiques** | `architectural-design.md`, `system-decomposition.md`, `data-architecture.md`, `security-architecture.md`, `integration-architecture.md`, `architectural-interface-contracts.md` (contrats externes + inter-contextes), `adrs/`, `architecture-traceability-matrix.md`, `architecture-review-report.md` | Design détaillé par module, algorithmes, schémas de données internes, signatures, error handling, logging strategy |

**Règle simple** : si la décision impacte **plus d'un bounded context** ou **plus d'une équipe**, c'est P3. Si elle impacte **un module ou une classe**, c'est P4.

**Cas limite type** : "Monolith modulaire avec 3 bounded contexts" = P3 (style archi). "Module Billing = Repository pattern + factory pour les stratégies de pricing" = P4.

---

## Entry Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| EG-3.1 | Phase 2 requirements approved | Requirements baseline version | Approved version locked |
| EG-3.2 | Prioritized backlog available | Backlog items with priorities | ≥90% items prioritized |
| EG-3.3 | Traceability matrix established | RTM tool access | RTM accessible and current |
| EG-3.4 | Acceptance criteria defined | AC document version | Each requirement has linked AC |
| EG-3.5 | Tech stack ratified (P1) | tech-stack-candidate.md | Stack figée par décision P1 |
| EG-3.6 | Architecture environment prepared | Tool access and permissions | All architects have write access |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` triggers Phase 2 (Requirements) remediation.

---

## Exit Gate

| ID | Criterion | Measure | Threshold |
|----|-----------|---------|-----------|
| XG-3.1 | Architectural design complete | AD document completeness | ≥95% architecture defined |
| XG-3.2 | Architectural design reviewed | Peer review sign-off | ≥3 architects approved |
| XG-3.3 | Architectural interface contracts finalized | Contract documents v1 | All architecture-level interfaces documented |
| XG-3.4 | ADRs (Architecture Decision Records) signed | ADR set | 100% structurants ADRs signés |
| XG-3.5 | Architecture-to-Requirements traceability established | ART coverage | 100% archi elements traced to reqs |
| XG-3.6 | Security architecture approved | Security-architecture sign-off | Nexus-Security + CISO approved |

**Gate Evaluation**: ALL criteria must be `PASS` to proceed. Any `FAIL` requires architecture rework cycle.

---

## Transition Criteria to Phase 4 (Design)

| Criterion | Source | Target | Verification Method |
|-----------|--------|--------|---------------------|
| Architecture baseline frozen | Nexus-Architect | Phase 4 Lead | Architecture baseline memo |
| ADRs ratified | Nexus-Architect | All architects | ADR set signature |
| Architectural interface contracts ratified | Nexus-Architect | Phase 4 Lead (Nexus-Backend/Frontend) | Contract signatures |
| Security architecture accepted | Nexus-Security + CISO | Phase 4 Lead | Security acceptance memo |
| Architecture-to-Req traceability audit passed | Nexus-QA | Architecture Lead | ART verification report |
| Technical debt assessment done (archi level) | Nexus-Architect | Project Lead | Debt report approved |

**Transition Authorization**: Hyperagent-Orchestrator issues `PHASE_3_COMPLETE` only when all transition criteria verified with formal evidence.

---

## Key Activities

### Activity 3.1: System Decomposition
- Define system decomposition (subsystems, modules, components)
- Establish module responsibilities (Bounded Contexts, services, layers)
- Identify cross-cutting concerns (logging, auth, error handling — au niveau archi)

### Activity 3.2: Architectural Patterns and Styles
- Choose architectural style (monolith, microservices, serverless, event-driven, layered)
- Document patterns (CQRS, Event Sourcing, Saga, etc.) avec rationale
- Define communication patterns (sync REST, async messaging, gRPC)
- Document data flow patterns (read/write split, caching layers)

### Activity 3.3: Data Architecture
- Choose data storage strategies (SQL vs NoSQL, polyglot persistence)
- Define data partitioning and sharding strategy
- Document data consistency model (strong, eventual, read-your-writes)
- Define backup, archival, and data lifecycle policies

### Activity 3.4: Security Architecture
- Define security patterns (defense in depth, zero trust, least privilege)
- Choose authentication and authorization patterns (OAuth2, OIDC, JWT, RBAC, ABAC)
- Document secrets management strategy
- Define threat model (STRIDE) and mitigations at archi level
- Document encryption strategy (at rest, in transit, key management)

### Activity 3.5: Integration Architecture
- Define API gateway / service mesh patterns
- Document external system integrations (third-party APIs, legacy systems)
- Define event bus / message broker strategy (if applicable)
- Document API versioning and deprecation strategy

### Activity 3.6: Architecture Validation
- Conduct architecture reviews (peer + 2 externes minimum)
- Validate architecture against requirements (especially NFRs)
- Verify architecture-to-requirements traceability (ART)
- Assess architecture quality attributes (modifiability, performance, security, scalability)

---

## Responsible Agents
| Agent | Role |
|-------|------|
| Hyperagent-Orchestrator | Coordinates parallel architecture tasks (3-4 sub-agents) |
| Nexus-Architect | Lead, synthesis, ADR writing |
| Nexus-Security | Security architecture + threat model |
| Nexus-Backend | Backend architecture (subsystems, services) |
| Nexus-Frontend | Frontend architecture (UI layers, state management) |
| Nexus-DevOps | Infrastructure architecture (deployment topology, observability) |
| Nexus-Critic (5e agent) | **T1 casseur + T2 conformité + T3 prédiction aval — TOUS OBLIGATOIRES** (décision mainteneur 2026-06-06) |

**Concurrency** : multi-agent justifié (F13 recherche 2026 — archi = read-heavy parallèle). 3-5 sub-agents en parallèle, jamais plus. **Nexus-Critic = 3 invocations systématiques** (T1 casse le livrable, T2 vérifie ISO 42010 + conformité NFR, T3 prédit les ruptures P4). Coût additionnel ~4.5k tokens, justifié par le hard cap 15k.

**Patterns adversariaux T1/T2/T3 (rappel)** :
- **T1 (casseur)** : un architecte propose, Nexus-Critic casse. Cible : ADRs, contrats d'interface, threat model.
- **T2 (spec-compliance)** : Nexus-Critic vérifie ISO/IEC/IEEE 42010:2011 + conformité NFR + conformité SRS P2. Cible : architectural-design.md + tous les livrables structurants.
- **T3 (conséquentialiste)** : Nexus-Critic prédit ce qui va être dur à designer en P4 (casses potentiels, zones d'ambiguïté, dépendances cachées). Cible : architecture-to-requirements traceability + interface contracts.

**Isolation des contextes (ACI stratégie §4.5)** : Nexus-Critic ne voit pas le prompt système des producteurs. Chaque rôle adversarial a un contexte distinct, sinon les "adversaires" se laissent influencer par le contexte partagé.

---

## Required Skills
- `nexus-architect`: Architecture design, ADRs
- `nexus-security`: Security architecture, threat model
- `nexus-backend`: Backend subsystems design
- `nexus-frontend`: Frontend architecture
- `nexus-devops`: Infrastructure architecture
- `nexus-critic`: Adversarial validation (T1 casseur + T2 conformité + T3 aval)
- `speckit-qa`: Architecture quality assurance

---

## Hooks to Invoke

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-architecture-approved` | Exit criteria met | Triggers Phase 4 (Design) initiation |
| `architectural-design-frozen` | Architecture complete | Locks architectural baseline |
| `adrs-signed` | All ADRs ratified | Locks architectural decisions |
| `architectural-interfaces-finalized` | Interfaces defined | Enables parallel detailed design |
| `security-architecture-approved` | Security archi signed | Unblocks P4 + P5 |
| `archi-review-approved` | Architecture review passed | Proceeds to detailed design |

---

## Artifacts Produced

| Artifact | Description | Location | Format |
|----------|-------------|----------|--------|
| `architectural-design.md` | System architecture specification (C4 model + key views) | `specs/workflows/by-phase/phase-3-architecture/` | md |
| `system-decomposition.md` | Subsystems, modules, Bounded Contexts | `specs/workflows/by-phase/phase-3-architecture/` | md |
| `data-architecture.md` | Data model, storage strategies, consistency model | `specs/workflows/by-phase/phase-3-architecture/` | md |
| `security-architecture.md` | Security patterns, auth/authz, threat model (STRIDE) | `specs/workflows/by-phase/phase-3-architecture/` | md |
| `integration-architecture.md` | API patterns, external integrations, event bus | `specs/workflows/by-phase/phase-3-architecture/` | md |
| `architectural-interface-contracts.md` | Interface contracts (modules internes + API REST externes) | `specs/workflows/by-phase/phase-3-architecture/` | **md+json modules internes + md+json+OpenAPI API REST** |
| `adrs/` (directory) | 1+ ADR per structurant decision (pas de max) | `specs/workflows/by-phase/phase-3-architecture/adrs/` | md (1 ADR par fichier) |
| `architecture-traceability-matrix.md` | Architecture-to-Req mapping | `specs/workflows/by-phase/phase-3-architecture/` | md |
| `architecture-review-report.md` | Architecture review findings + sign-offs (≥3 architectes) | `specs/workflows/by-phase/phase-3-architecture/` | md |

**Format contracts différencié (décision mainteneur 2026-06-06)** :
- **Modules internes** (appels in-process entre bounded contexts, ex: `BillingService.Notify(userId)`) : **md+json**. Pas d'OpenAPI car pas de transport réseau, le tooling P5 génère les stubs directement à partir du json.
- **API REST** (HTTP endpoints exposés, ex: `POST /api/v1/payments`) : **md+json+OpenAPI 3.0**. OpenAPI car le tooling P5 (génération de clients) consomme du standard. Validation par `openapi-lint` (cf. tools section 5.2).
- **Événements async** (pub/sub sur event bus, ex: `PaymentConfirmed` event) : **md+json+AsyncAPI 3.0** (extension naturelle de la règle REST, à valider au cas par cas).

---

## ADRs (Architecture Decision Records)

**Règle de quantité (décision mainteneur 2026-06-06)** : **minimum 1 ADR par décision structurante**, **pas de maximum**. Pas de fourchette indicative fixe par cas (greenfield, maintenance, R&D) — l'agent trace ce qui est structurant, pas ce qui rentre dans un quota.

**Définition d'une décision structurante** : impacte ≥2 modules / bounded contexts / équipes, OU est coûteuse à inverser, OU a des conséquences long-terme (vendor lock-in, dette technique, conformité).

Chaque ADR doit contenir :
- **Contexte** : quel problème, quelles contraintes
- **Décision** : ce qu'on a choisi
- **Alternatives considérées** : ce qu'on a écarté et pourquoi (minimum 1, idéal 2-3)
- **Conséquences** : positives, négatives, risques (incluant vendor lock-in, dette technique, impact perf/sécurité)
- **Statut** : Proposé / Accepté / Déprécié / Remplacé
- **Date + signataires** (≥3 architectes pour les décisions structurantes)

Format de nommage : `adr-NNN-titre-court.md` (ex: `adr-001-choix-monolith-vs-microservices.md`).

**Exemples de décisions structurantes typiques** (non exhaustif) : choix du style architectural (monolith vs microservices vs serverless), choix du data store principal (SQL vs NoSQL, polyglot), choix du pattern de communication (sync REST vs async events vs gRPC), choix de la stratégie d'authentification (OAuth2 vs OIDC vs custom), choix du cloud provider (vendor lock-in), choix du modèle de déploiement (Kubernetes vs serverless vs VM).

**Exemples de décisions NON structurantes** (pas d'ADR) : nommage des variables, choix de la structure de données locale, choix de l'IDE, choix de la convention de logging.

## Format des fichiers (triple différencié)

> **Validation 2026-06-06** : format triple différencié par type de livrable (vs format triple uniforme en P0/P2).

| Type de livrable | Format primaire | Format secondaire | Standard |
|------------------|------------------|-------------------|----------|
| **Specs narratives** (architectural-design, system-decomposition, data-architecture, security-architecture, integration-architecture, ART, review-report) | md (lecture humaine) | — | — |
| **Contrats modules internes** (architectural-interface-contracts.md) | md (lecture humaine) | json (machine-parse) | — |
| **Contrats API REST** (subset de architectural-interface-contracts.md) | md (lecture humaine) | json (machine-parse) | **OpenAPI 3.0** |
| **Événements async** (subset de architectural-interface-contracts.md, si applicable) | md (lecture humaine) | json (machine-parse) | **AsyncAPI 3.0** (option) |
| **ADRs** (1 fichier par décision structurante) | md | — | Format Michael Nygard |
| **Threat model** (inclus dans security-architecture.md) | md | — | STRIDE |

**Convention de nommage** :
- Specs narratives : `${livrable}.md`
- Contrats modules internes : `${module}-contract.md` + `${module}-contract.json`
- Contrats API REST : `${api-name}.md` + `${api-name}.json` + `${api-name}.openapi.yaml`
- Événements async : `${event-name}.md` + `${event-name}.json` + `${event-name}.asyncapi.yaml` (si applicable)
- ADRs : `adr-NNN-titre-court.md` (1 fichier par décision structurante)

**Localisation** : tous dans `specs/workflows/by-phase/phase-3-architecture/` (specs narratives) ou `specs/workflows/by-phase/phase-3-architecture/adrs/` (ADRs).

---

## Hyperagent Parallel Processing

```
parallel_tasks:
  - task: system_decomposition
    agents: [Nexus-Architect, Nexus-Backend]
    sync: false

  - task: data_architecture
    agents: [Nexus-Architect, Nexus-Backend, Nexus-DataEng]
    sync: false

  - task: security_architecture
    agents: [Nexus-Security, Nexus-Architect]
    sync: false

  - task: integration_architecture
    agents: [Nexus-Backend, Nexus-Architect, Nexus-DevOps]
    sync: false

  - task: threat_model
    agents: [Nexus-Security, Nexus-CISO]
    sync: false

reduction: "Nexus-Architect synthesizes all into architectural-design.md + adrs/"
```

---

## Refus catégoriques (5)

La phase P3 **refuse** de :
1. **Pas de design détaillé module** (forcé en P4)
2. **Pas de code d'implémentation** (jamais)
3. **Pas d'estimation effort** (absent du modèle, P5 Implementation inclut ses propres estimations)
4. **Pas de choix "tactique"** (la tactique est pour P4 Design)
5. **Pas de design qui ne respecte pas les NFR** (sécurité, perf, scalabilité)

---

## Critères d'abandon (4 + temps)

L'agent abandonne et prévient le mainteneur si :
1. Conflit entre architectes non résolvable (3 reviewers en désaccord)
2. NFR conflictuels (perf vs cost) non résolus par mainteneur
3. Interface contract impossible à designer en P4 (escalade P2 requirements)
4. Security design rejeté par Nexus-CISO
5. Dépassement de 35 min sans avancée claire

---

## Tokens budget

- **Base** : 5k tokens
- **Soft cap** : 8k tokens (alerte)
- **Hard cap** : 15k tokens (compactage forcé + abort)

Multi-agent justifié (F13 recherche 2026) : 3-5 sub-agents en parallèle × 1.5k chacun = 4.5-7.5k base. Cap 15k hard pour absorber les validations adversariales T1+T2+T3 obligatoires (Nexus-Critic en mode rotation sur les 3 patterns, pas un seul — décision mainteneur 2026-06-06). **Justification du passage 12k → 15k** : Nexus-Critic T1+T2+T3 obligatoire = 3 invocations × ~1.5k = 4.5k additionnel, ce qui sature le budget 12k en nominal. 15k = marge de sécurité pour absorber les validations adversariales complètes, en cohérence avec P5 Implementation (5k/10k/15k) qui était déjà le budget le plus large.

**Note** : P3 devient 2e phase la plus large (ex-aequo avec P5) au lieu de 3e. Acceptable car l'architecture est l'activité 2 du projet (après implémentation) et le sur-coût est compensé par la qualité (ADRs formalisés, threat model STRIDE, contrats d'interface propres).

---

## Pauses

Toutes les 5 actions : compaction checkpoint à 60-70% du soft cap (4.8k tokens, F8 recherche 2026).

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :
1. **Greenfield from-scratch** : architecture riche, ADRs multiples, threat model complet
2. **Maintenance legacy** : architecture = "doit-on moderniser ?", dette technique
3. **Projet interne** (équipe, gouvernance légère)
4. **Projet externe client** (architecture revue par architecte client, sign-off formel)
5. **Compliance-driven** (security architecture + threat model en première position)
6. **R&D / exploration** (architecture = POC, ADRs minimaux)

---

## UDL — 7 éléments P3-spécifiques

| Élément | Description | Exemple |
|---------|-------------|---------|
| Décision architecturale | Choix structurant (monolith vs microservices, SQL vs NoSQL, etc.) | "Monolith modulaire choisi pour limiter la complexité ops" |
| ADR signé | Pointeur vers l'ADR | "Voir adr-001-monolith-vs-microservices.md" |
| Alternative écartée | Option non choisie + pourquoi | "Microservices écartés : équipe de 3, ops pas prêt" |
| Threat identifié | Menace architecturale + mitigation | "DDoS sur API publique → Cloudflare + rate limiting" |
| Interface contract architectural | Pointeur vers le contrat d'interface | "Voir architectural-interface-contracts.md § 3.2" |
| Rejet T1/T2 casseur | Quand Nexus-Critic a trouvé un problème | "T1 a trouvé ACID manquant sur le payment service, corrigé via ADR-005" |
| Décision "pas de décision" | Cas où on a choisi de NE PAS trancher, et pourquoi | "Pas d'arbitrage perf vs cost : escaladé en P4 Design" |

Stockés dans `.swebok_state.db` (table `udl_p3`) et consultables via Consultation Envelope (A1) par P4.

---

## Conditions de sortie (passage à P4)

Le mainteneur valide avec une **checklist à 100%** (8 critères) :
- [ ] `architectural-design.md` existe (≥95% ISO 42010)
- [ ] `system-decomposition.md` existe
- [ ] `data-architecture.md` existe
- [ ] `security-architecture.md` existe (threat model inclus)
- [ ] `integration-architecture.md` existe
- [ ] `architectural-interface-contracts.md` existe (100% interfaces archi)
- [ ] `adrs/` contient les ADRs structurants (≥1 par décision majeure)
- [ ] `architecture-review-report.md` signé par ≥3 architectes
- [ ] UDL 7 éléments loggés

Pas de feu vert séparé — les documents font foi.

---

## Audit des 4 failure modes Drew Breunig

### Mode 1 — Poisoning (Empoisonnement)
**Risque** : un ADR faux qui contamine les contrats d'interface aval.
**Mitigations** :
1. Chaque ADR challengé par ≥1 autre architecte (pas l'auteur)
2. Nexus-Critic T1 casseur relit tous les ADRs
3. Validation mainteneur finale (checklist 100%) = catch du poison
4. UDL 6 ("rejet T1/T2") logge les ADR rejetés et comment c'est résolu

### Mode 2 — Distraction (Distraction)
**Risque** : trop d'options architecturales (over-engineering).
**Mitigations** :
1. Refus catégorique 4 (pas de choix tactique, tactique = P4)
2. Budget 5k/8k/12k (large mais pas infini, force à prioriser)
3. 3-5 sub-agents max (vs 50 subagents, F2 recherche 2026)
4. UDL 4 ("alternative écartée") force à documenter ce qu'on n'a pas choisi

### Mode 3 — Confusion (Confusion)
**Risque** : trop de patterns candidats sans hiérarchie.
**Mitigations** :
1. Architectural style = UN seul choix (pas "on fait un peu de tout")
2. ADRs numérotés (adr-001, adr-002, etc.) = ordre logique
3. UDL 7 ("pas de décision") logge les cas où on n'arbitre pas
4. Nexus-Architect lead = synthèse finale unique (pas de "trop de cuisiniers")

### Mode 4 — Clash (Conflit)
**Risque** : ADRs contradictoires (monolith vs microservices, REST vs GraphQL).
**Mitigations** :
1. Revue par ≥3 architectes détecte les contradictions
2. Nexus-Critic T2 conformité (ISO 42010) catch les clashes
3. UDL 3 ("alternative écartée") documente les options mutuellement exclusives
4. Critère d'abandon 1 (3 reviewers en désaccord) = escalade mainteneur

---

## Notes de version

- **v2 (2026-06-06)** : refonte ciblée via audit (grille offline + 6 questions). Changements : (1) hard cap 12k → 15k (Nexus-Critic T1+T2+T3 obligatoire), (2) format contracts différencié (md+json modules internes, OpenAPI API REST, AsyncAPI événements), (3) critère explicite de démarcation P3/P4 (quoi+pourquoi vs comment), (4) ADRs = minimum 1 par décision structurante (pas de max), (5) section 7 maintenue 🟡 avec fermeture différée par avis expert externe. 6 décisions tranchées par le mainteneur, 6 références P0/P1/P2 v2 + stratégie.
- **v1 (2026-06-05)** : créé suite au fix structurel (split P3 en P3 Architecture + P4 Design). 6 activités, 9 livrables (8 md + répertoire adrs/), 3-5 agents en parallèle + Nexus-Critic, 5k/8k/12k tokens, cap 35 min, 7 questions max, 7 UDL items, 5 refus, 4 critères abandon, 6 cas limite, audit 4 failure modes Drew Breunig complet.
