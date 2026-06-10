# Audit — Phase 4 : Design

> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 4
- Nom : Design
- Équivalent SWEBOK v4 : P3 SWEBOK (Software Design KA) — **uniquement**
- Spec existante : `specs/workflows/by-phase/phase-4-design.md` (v2 — validé 2026-06-07)
- Date de l'audit : 2026-06-07 (post-fix structurel, vague 1)
- Auditeur : Mainteneur (grille offline) + Claude (analyse + 4 questions + rédaction v2)
- Couverture corpus : **97%** (post-vague 8, 2026-06-09) — cf. §39 du corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md
- Verdict global : 🟢 OK — toutes les sections comblées (7 par projection + cohérence P0/P1/P2/P3 v2, 5.5 transformée en 7 questions précises)

---

## ⚠️ Findings pré-identifiés (post-fix structurel)

1. **Phase 4 = Design SEUL** (créée le 2026-06-05 lors du fix structurel). Avant : P3 fusionnait P2 (Architecture) + P3 (Design) SWEBOK. Après : P3 Architecture (séparé) + P4 Design (ce fichier).
2. **L'Architecture est déjà faite en P3** : la phase 4 consomme les ADRs de P3 et descend au niveau module (interfaces, structures de données, algorithmes, error handling, logging).
3. **3 activités, 7 livrables** : Detailed Design + Design Specification + Design Validation. Pas de redondance avec P3.
4. **Budget 5k/8k/15k (validé 2026-06-07)** : Nexus-Critic T1+T2+T3 obligatoire, hard cap 15k comme P3 v2. 3-5 agents max.
5. **Format contracts différencié aligné P3 v2** : md+json pour modules internes, +OpenAPI 3.0 pour API REST, +AsyncAPI 3.0 pour événements async (option).
6. **Critère de démarcation P3↔P4 explicite** : inscrit dans P3 ET P4 (action P3-3 du mainteneur 2026-06-06, exécutée pour P4 le 2026-06-07).

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
- [x] A. *« Consommer les ADRs P3 et descendre au niveau module : interfaces, structures de données, algorithmes, error handling, logging — pour que P5 Implementation puisse coder sans re-conception ni ré-décision architecturale »* (spec v2)
- [x] B. *« Produire ce qu'il faut pour que la phase 5 (Implémentation) puisse coder sans re-conception »*
- [x] C. *« Consommer les ADRs de P3 Architecture et descendre au niveau module »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
- [x] A. Detailed design (interfaces modules, data structures, algos, error handling, logging)
- [x] B. Design specification (DDS par module)
- [x] C. Design validation (revues + traceability DTAM + DRTM + matrice conformité ADRs P3)
- [x] D. Module interface contracts (signatures, types, comportements — format md+json modules internes, +OpenAPI API REST, +AsyncAPI events)
- [x] E. Testability hooks (test seams, mocks, fixtures)
- [x] F. **+ Consommation des ADRs P3** (pas de re-décision architecturale, matrice ADR → module obligatoire XG-4.7)

### 1.3 Hors-périmètre
- [x] A. Architecture (P3, déjà fait)
- [x] B. Code d'implémentation (P5)
- [x] C. Tests d'implémentation (P6)
- [x] D. **+ Re-décision architecturale** (escalade P3 si nécessaire — règle de démarcation)
- [x] E. **+ Estimation effort** (P5 fait ses propres estimations)
- [x] F. **+ Choix de stack** (déjà ratifiée en P1)

### 1.4 Verdict
- [x] 🟢 OK (mission claire, périmètre explicite, hors-périmètre explicite, démarcation P3↔P4 inscrite dans la spec v2)

### 1.5 Critère de démarcation P3 vs P4 (Design) — **validé 2026-06-07**
- [x] A. **P3 = QUOI + POURQUOI** : bounded contexts, style archi, sécurité patterns, intégration patterns, ADRs, contrats externes
- [x] B. **P4 = COMMENT** : algos détaillés, classes/fonctions, error handling, signatures internes, schémas de données internes
- [x] C. **Règle simple** : si la décision impacte ≥2 bounded contexts / équipes = P3. Si elle impacte un module / classe = P4
- [x] D. **Cas limite type** : "monolith modulaire avec 3 bounded contexts" = P3. "Module Billing = Repository pattern + factory pour les stratégies de pricing" = P4
- [x] E. **Critère inscrit explicitement dans P3 ET P4** (action P3-3 du mainteneur 2026-06-06, exécutée pour P4 le 2026-06-07)
- [x] F. **Conséquence opérationnelle** : si P4 détecte qu'une décision descendante impacte ≥2 bounded contexts, **elle escalade P3** (refus catégorique 5)

### 1.6 Verdict global section 1
- [x] 🟢 OK (mission + périmètre + hors-périmètre + démarcation P3↔P4 explicites et inscrits dans la spec v2)

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] A. Phase 3 architecture approved (spec EG-4.1)
- [x] B. ADRs signés (P3, spec EG-4.2)
- [x] C. Architectural interface contracts v1 (spec EG-4.3)
- [x] D. Design environment prepared (spec EG-4.4)
- [x] E. Module assignment matrix defined (spec EG-4.5)

### 2.2 Critères de complétion
- [x] A. DDS 100% modules (spec XG-4.1)
- [x] B. Design review approved (spec XG-4.2)
- [x] C. Module interface contracts finalisés 100% (spec XG-4.3 — format différencié md+json modules, +OpenAPI REST, +AsyncAPI events)
- [x] D. Design-to-Architecture traceability DTAM 100% (spec XG-4.4)
- [x] E. Design-to-Requirements traceability DRTM 100% (spec XG-4.5)
- [x] F. **+ UDL 7 éléments P4-spécifiques loggés** (spec XG-4.6)
- [x] G. **+ Conformité aux ADRs P3 vérifiée** (matrice ADR → module, XG-4.7 — pas de déviation architecturale)

### 2.3 Conditions d'échec → escalade
- [x] A. ADR P3 non respecté (déviation architecturale) → escalade P3
- [x] B. NFR conflictuels (perf vs cost) non résolus
- [x] C. Interface contract module impossible à implémenter (côté P5)
- [x] D. Security design détaillé rejeté par Nexus-Security

### 2.4 Verdict
- [x] 🟢 OK (trigger + complétion + échec explicites, matrice ADR P3 ajoutée, UDL 7 éléments ajoutés)

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. P3 Architecture outputs (architectural-design.md, ADRs, architectural interface contracts) — **consommés en mode lecture seule via Consultation Envelope A1**
- [x] B. P2 Requirements outputs (SRS, NFR, RTM, AC)
- [x] C. P1 Concept/Feasibility outputs (stack candidate, business case, constraints)
- [x] D. P0 risk landscape
- [x] E. **+ NFR extraits du SRS** (souvent oubliés, ici obligatoires pour T2 Nexus-Critic)
- [x] F. **+ Use case model** (de P2)

### 3.2 Depuis l'utilisateur
- [x] A. Décision de stack technique (si pas déjà ratifiée en P1)
- [x] B. Trade-offs design à valider (pattern par module, algo complexity vs readability)
- [x] C. **+ Acceptation des contraintes de dette technique**
- [x] D. **+ Validation conformité aux ADRs P3** (si déviation proposée)

### 3.3 Depuis sources externes

> **Validé 2026-06-07** : couverture corpus à **40%** (████░░░░░░). 8 livres corpus-aligned (Mac Studio) + 1 open-access (Ousterhout) = 9 total.

**Sources externes disponibles localement (post-corpus)** :

**Mac Studio** (8 livres) — chemin `/Users/dorianciet/Desktop/Test PDF books` et `/Volumes/External/Obsidian KB/Knowledge Base/raw/pdfs` :
- **Head First Design Patterns** (Eric Freeman;Elisabeth Robson;) — 47.6 MB, 672 pages
- **Tidy First?** (Kent Beck;) — 3.5 MB, 125 pages
- **Generative AI Design Patterns** (Valliappa Lakshmanan;Hannes Ha) — 19.7 MB, 509 pages
- **Fundamentals of Software Engineering** (Nathaniel Schutta;Dan Vega;) — 11.6 MB, 405 pages
- **Data Engineering Design Patterns** (Bartosz Konieczny;) — 7.1 MB, 375 pages
- **Machine Learning Design Patterns** (Lakshmanan, Valliappa; Robinso) — 15.9 MB, 408 pages
- **Software Design Patterns: The Ultimate Guide** (Sufyan bin Uzayr) — 8.4 MB, 454 pages
- **The easiest way to learn design patterns** (Fiodar Sazanavets) — 6.2 MB, 324 pages

**Livres open-access téléchargés** (1) :
- A Philosophy of Software Design (Ousterhout 2e, 14 MB)

**Lacunes critiques restantes (à acquérir)** (4) :
- Refactoring, 2nd ed. (Fowler) (2018)  -- 🔴 Le plus important refactoring book. Acheter si budget le permet.
- Refactoring (Fowler) - 1st ed. (1999)  -- Ancien mais fondateur. 2e ed préférable.
- Refactoring to Patterns (Kerievsky) (2004)  -- Pont refactoring ↔ patterns. Toujours valide.
- Code Complete, 2nd ed. (McConnell) (2004)  -- L'encyclopédie du code. Toujours la référence.

### 3.4 Verdict
- [x] 🟢 OK (P0+P1+P2+P3 + sources externes + NFR extraits + matrice ADR P3 obligatoire)

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
- [x] A. `detailed-design.md` (DDS par module)
- [x] B. `module-interfaces.md` (signatures, types, comportements — format md+json modules internes, +OpenAPI 3.0 API REST, +AsyncAPI 3.0 events option)
- [x] C. `data-structures.md` (structures et algorithmes par module)
- [x] D. `error-handling-design.md` (stratégie d'erreurs et exceptions par module)
- [x] E. `logging-design.md` (logging et monitoring spécifications par module)
- [x] F. `design-traceability-matrix.md` (DTAM 100% + DRTM 100%)
- [x] G. `design-review-report.md` (revues détaillées + sign-offs + T1+T2+T3 Nexus-Critic)
- [x] H. **+ Conformité aux ADRs P3 documentée** (matrice ADR → module — XG-4.7 obligatoire)
- [x] I. **+ Diagrammes (UML, sequence, state machines)** par module (optionnels mais recommandés)

### 4.2 Format de stockage (différencié par type — aligné P3 v2 — décision mainteneur 2026-06-07)
- [x] A. **Markdown** pour tous les livrables (lisibles par mainteneur)
- [x] B. **JSON** pour les module interface contracts (machine-parse pour P5)
- [x] C. **+ OpenAPI 3.0** pour les API contracts modules REST (subset de module-interfaces.md)
- [x] D. **+ AsyncAPI 3.0** (option) pour les événements async (subset, si applicable)
- [x] E. **Format différencié** : md+json pour modules internes, md+json+OpenAPI pour API REST, md+json+AsyncAPI pour events
- [x] F. **Validation par lint** : `openapi-lint` pour OpenAPI, `asyncapi-lint` pour AsyncAPI

### 4.3 Format de présentation à l'utilisateur
- [x] A. Design overview + liens vers le détail par module
- [x] B. Diagrammes clés en premier (UML, sequence, state machines par module)
- [x] C. **+ Matrice de conformité ADR P3** (chaque module → ADR respecté ou déviation documentée) — en évidence
- [x] D. **+ Matrice de couverture des patterns** (mapping module → pattern, UDL 3)

### 4.4 Auditabilité
- [x] A. Oui — chaque module tracé + ADRs respectés (matrice XG-4.7)
- [x] B. Manque le "pourquoi on a écarté tel pattern" → couvert par DDS section "Alternatives considered" + UDL 3
- [x] C. Manque la justification des trade-offs → couvert par UDL 4 ("trade-off design arbitrée")
- [x] D. **+ Pas de déviation architecturale silencieuse** → matrice ADR P3 obligatoire, UDL 1 ("déviation proposée")

### 4.5 Verdict
- [x] 🟢 OK (7 livrables principaux + matrice ADR P3 + diagrammes optionnels, format différencié md+json pour modules / md+json+OpenAPI pour API REST, auditabilité max)

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
- [x] A. Hyperagent-Orchestrator (spec, coordination)
- [x] B. Nexus-Architect (lead, synthèse, consommation ADRs P3)
- [x] C. Nexus-Backend (design modules backend)
- [x] D. Nexus-Frontend (design components frontend)
- [x] E. Nexus-DevOps (design infra détaillée, CI/CD scripts)
- [x] F. Nexus-Security (security controls design détaillé)
- [x] G. **+ Limiter à 3-5 sub-agents max** (F13 recherche 2026)
- [x] H. **+ Nexus-Critic (5e agent OBLIGATOIRE — décision mainteneur 2026-06-07)** : T1 casseur + T2 conformité NFR P2 + T3 prédiction aval P5 — **3 invocations systématiques** (comme P3 v2)

### 5.2 Tools disponibles
- [x] A. `nexus-architect`, `nexus-backend`, `nexus-frontend`, `nexus-devops`, `nexus-security`
- [x] B. `nexus-critic` (**OBLIGATOIRE**, 3 invocations T1+T2+T3 — décision 2026-06-07)
- [x] C. `speckit-qa` (design quality)
- [x] D. **+ Outil de génération de diagrammes (Mermaid, PlantUML)**
- [x] E. **+ Outil de validation de contrats : OpenAPI 3.0 lint (obligatoire REST), AsyncAPI 3.0 lint (option événements)**
- [x] F. **+ Outil de lint design patterns** (respect des patterns documentés en P3)

### 5.3 Knowledge items consultés

> **Validé 2026-06-07** : Knowledge items alignés sur le nouveau corpus.

**Référentiel principal** : `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` (2 269 lignes, 18 sections, 480 ressources recommandées).

**Sections clés du référentiel à consulter** :
- **§18** : Sources locales — Mac Studio (117 livres corpus-matching identifiés)
- **§19** : Nouveaux livres acquis (Bureau/New Books/, 87 livres)
- **§20** : Lacunes restantes (43 livres non encore acquis, alternatives ≥ 2017)
- **§7** : Classics (Brooks, Fowler, Martin, Evans, Hunt/Thomas, etc.)

**Livres canoniques disponibles localement pour cette phase** (8 livres corpus-aligned sur ~20 recommandés = **40%**) :

- **Mac Studio** : 8 livres — voir détail §3.3 ci-dessus
- **Open-access** : 1 livre (Ousterhout, A Philosophy of Software Design)

**Lacunes critiques (§20)** : 4 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.

### 5.4 Pattern adversarial applicable
- [x] A. T1 (producteur vs breaker) — **OBLIGATOIRE** : un dev propose DDS, Nexus-Critic casse (3 invocations systématiques, décision 2026-06-07)
- [x] B. T2 (spec-compliance) — **OBLIGATOIRE** : Nexus-Critic vérifie conformité NFR P2 + ADRs P3
- [x] C. T3 (conséquentialiste) — **OBLIGATOIRE** : Nexus-Critic prédit les difficultés P5 Implementation
- [x] D. **+ Pas de Council en standard** (escalade mainteneur sur conflit ADR P3)

### 5.5 Points de décision utilisateur (B threshold)
**7 questions précises avec options (transformation 2026-06-07 vague 1 — était liste de 5 catégories, devient questions actionnables comme P3 v2 finale)** :

1. **Déviation d'ADR P3 proposée** : si P4 propose de dévier d'un ADR P3, l'agent doit-il (a) escalader systématiquement au mainteneur, (b) trancher par défaut avec rationale + alternatives écartées dans l'UDL, (c) refuser systématiquement et escalader P3, (d) autre ?
2. **Trade-off design module** (algo complexity vs lisibilité, perf vs mémoire) : l'agent doit-il (a) escalader systématiquement, (b) trancher par défaut avec rationale documentée dans UDL 4, (c) poser 1-2 questions ciblées avant de trancher, (d) autre ?
3. **Acceptation dette technique** (si module P4 doit supporter dette pour livraison rapide) : l'agent doit-il (a) refuser systématiquement et escalader, (b) accepter et logger dette + rationale dans l'UDL, (c) demander confirmation explicite au mainteneur avant acceptation, (d) autre ?
4. **Pattern contre-patterns** (si un pattern commun est écarté pour ce module) : l'agent doit-il (a) justifier systématiquement l'écartement dans le DDS, (b) le faire uniquement si impacte ≥2 modules, (c) escalader au mainteneur, (d) autre ?
5. **Rejet d'un finding T1 casseur** (le mainteneur maintient sa position après que Nexus-Critic ait trouvé un problème) : l'agent doit-il (a) accepter le rejet et logger dans l'UDL 5, (b) escalader au mainteneur pour arbitrage, (c) accepter avec proposition de mitigation, (d) autre ?
6. **Conformité ADR P3 vs Design Pattern mieux-adapté** (le design pattern "idéal" dévie légèrement d'un ADR P3 tactique) : l'agent doit-il (a) suivre l'ADR P3 par défaut, (b) dévier et documenter dans UDL 1 (escalade mainteneur), (c) demander confirmation explicite, (d) autre ?
7. **Pas de décision sur un trade-off** (on n'arbitre pas entre 2 options équivalentes) : l'agent doit-il (a) reporter à P5 Implementation, (b) trancher par défaut et logger dans UDL 7, (c) escalader au mainteneur pour décision finale, (d) autre ?

**Règle d'usage** : l'agent peut choisir de ne pas poser les 7 si le contexte est déjà clair. Min 0, max 7. Au-delà, le système choisit en autonomie et logge dans l'UDL. Les 7 questions sont **prêtes à l'emploi** dans le format AskUserQuestion (header + 2-4 options mutuellement exclusives par question).

### 5.6 Verdict
- [x] 🟢 OK (5.5 comblé en 7 questions précises avec options AskUserQuestion — transformation 2026-06-07, 5.4 T1+T2+T3 explicités et obligatoires, 3-5 agents max + Nexus-Critic OBLIGATOIRE)

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques (5)
- [x] A. Pas de code d'implémentation (uniquement pseudo-code et signatures — P5 s'en charge)
- [x] B. Pas de tests d'implémentation (P6)
- [x] C. **+ Pas de re-décision architecturale** (escalade P3 si nécessaire — règle de démarcation)
- [x] D. **+ Pas de design qui ne respecte pas les NFR P2** (sécurité, perf, scalabilité)
- [x] E. **+ Pas de design qui dévie des ADRs P3 sans escalade** (matrice ADR → module obligatoire, XG-4.7)

### 6.2 Modes d'échec connus
- [x] A. Over-engineering (trop de patterns, trop d'abstractions)
- [x] B. Design-by-committee (trop d'inputs, pas de décision)
- [x] C. God object / spaghetti code (pas de séparation module)
- [x] D. **+ Déviation silencieuse des ADRs P3** (module conçu hors archi) → matrice XG-4.7 obligatoire
- [x] E. **+ Specs trop denses post-split** (P4 a moins de place qu'avant, surcharge possible)
- [x] F. **+ Pas d'estimation** → on découvre en P5 que c'est 10× plus gros

### 6.3 Cas limites
- [x] A. Greenfield vs refonte
- [x] B. Criticalité forte (medical, avionique) vs CRUD interne
- [x] C. Solo dev vs équipe distribuée
- [x] D. Contraintes infra fortes (serverless, edge, on-prem)
- [x] E. **+ Code existant avec patterns imposés** (refonte : respecter l'existant)
- [x] F. **+ Compliance-driven** (design security-heavy, conformité ADRs P3 renforcée)
- [x] G. **+ R&D / exploration** (design = POC, DDS minimaux, matrice ADR P3 simplifiée)

### 6.4 Règles d'escalade
- [x] A. Déviation ADR P3 détectée → escalade P3
- [x] B. 3 reviewers en désaccord → escalade mainteneur
- [x] C. NFR impossible à respecter → escalade (remonter aux requirements P2)
- [x] D. Security design détaillé rejeté par Nexus-Security → bloquer la transition
- [x] E. **+ Interface contract module impossible à implémenter (côté P5)** → escalade P5 ou P3 (ajout 2026-06-07)

### 6.5 Verdict
- [x] 🟢 OK (5 refus, 6 modes échec, 7 cas limite, 5 escalades)

---

## Section 7 — Adéquation aux besoins (utilité)

### 7.1 Usage réel
> **Projection (par cohérence P0/P1/P2/P3 v2 + benchmarks corpus 2026, validée 2026-06-07)** :
> - **Greenfield from-scratch** : 5-10 modules typiques × DDS complet (interfaces, structures de données, algos, error handling, logging) + 5-10 contrats d'interface (md+json modules internes + OpenAPI API REST si applicable) + 1 matrice ADR P3 (100% ADRs tracés par module) + 1 DTAM/DRTM 100%. Effort estimé : 1-2 sessions de 35 min.
> - **Maintenance legacy** : DDS = "que doit-on modifier pour respecter le design existant", 1-3 modules touchés × DDS partiel + matrice ADR P3 mise à jour (pas créée ex nihilo). Effort estimé : 0.5-1 session de 35 min.
> - **R&D / exploration** : 1-2 modules POC × DDS minimal (signatures + 1-2 algos), matrice ADR P3 simplifiée, pas de DTAM/DRTM complet. Effort estimé : 0.5 session de 35 min.
> - **Compliance-driven** : 5-10 modules × DDS security-heavy + matrice ADR P3 renforcée (chaque ADR sécurité tracé) + validation Nexus-Security explicite. Effort estimé : 1.5-2.5 sessions de 35 min.
> - **Projet interne / équipe légère** : 3-5 modules × DDS standard + matrice ADR P3 standard. Effort estimé : 1 session de 35 min.
> - **Projet externe client** : 5-10 modules × DDS + revue architecte client (sign-off formel) + matrice ADR P3 validée par client. Effort estimé : 2 sessions de 35 min (révision incluse).
>
> **Cohérence P0/P1/P2/P3 v2** : les phases P0/P1/P2/P3 utilisent les mêmes patterns (séquentiel strict ou multi-agent justifié, format md+json + différencié, UDL 6-7 éléments, 4 failure modes Drew Breunig). P4 applique les patterns multi-agent justifié de P3 (3-5 sub-agents + Nexus-Critic T1+T2+T3 obligatoire) avec budget 5k/8k/15k. Le passage de P3 (5k/8k/15k) à P4 (5k/8k/15k) est aligné et justifié par la consommation des ADRs P3 + contrats critiques pour P5. Aucun contournement ni friction majeure remonté à date sur P0/P1/P2/P3 v2.

### 7.2 Friction observée
> **Projection (par cohérence P0/P1/P2/P3 v2 + analyse 4 failure modes Drew Breunig, validée 2026-06-07)** :
> - **F1 — Coordination multi-agent** : 3-5 sub-agents en parallèle + Nexus-Critic T1+T2+T3 obligatoire = 5-7 invocations potentielles. Mitigation = Nexus-Architect lead synthèse, F10 recherche 2026 (subagent output → filesystem, pas de dump). Pattern hérité de P3 v2, friction connue et gérée.
> - **F2 — Budget tokens** : hard cap 15k = 3e phase la plus large (après P3 et P5, ex-aequo avec P5). Mitigation = token counter live (pre-tool-use/token-counter.sh mis à jour 2026-06-07 : P4 = 5k/8k/15k), compaction 60-70% (F8), budget prévisible.
> - **F3 — Consultation envelope strict** : P4 doit consommer les ADRs P3 + NFR P2 en mode lecture seule via Consultation Envelope (A1). Mitigation = format double md+json (P2) + format différencié md+json/OpenAPI (P3) = slicing trivial. La règle de démarcation P3↔P4 explicite (inscrite dans P3 ET P4) clarifie ce qui est lecture seule vs re-décision.
> - **F4 — Densité post-split** : P4 a moins de place qu'avant (le split P3 Architecture + P4 Design a redistribué l'espace). Mitigation = 7 livrables principaux + matrice ADR P3 + diagrammes optionnels = volume maîtrisé. Format différencié évite la surcharge (json pour machine, md pour humain).
> - **F5 — Nexus-Critic T1+T2+T3 obligatoire** : 3 invocations × ~1.5k tokens = ~4.5k tokens additionnels, comme P3. Mitigation = hard cap 15k absorbe, F13 recherche 2026 valide le pattern.
> - **F6 — Matrice ADR P3 obligatoire** : chaque module doit tracer quels ADRs P3 il consomme. Mitigation = template matrice pré-rempli (module → ADR → status : consommé / dévié / nouveau), UDL 1 logge les déviations, XG-4.7 vérifie 100% avant transition.
> - **F7 — Format contracts différencié** : md+json pour modules internes, OpenAPI pour API REST, AsyncAPI pour événements = 3 formats à gérer. Mitigation = `openapi-lint` + `asyncapi-lint` (validation automatique), spec v2 section "Format des fichiers" explicite, pattern hérité de P3 v2.
>
> **Cohérence P0/P1/P2/P3 v2** : aucune friction majeure remontée à date (audits clos sans friction bloquante). Les patterns (consultation envelope, UDL, 4 failure modes) sont stables depuis P0 v2 (2026-06-04). La friction principale = gestion du multi-agent (3-5 sub-agents en parallèle) qui est alignée sur P3 v2, friction connue et documentée.

### 7.3 Pattern de contournement probable
> **Projection (par cohérence P0/P1/P2/P3 v2 + analyse 4 failure modes Drew Breunig, validée 2026-06-07)** :
> - **Contournement C1 — Court-circuit P3 → P4 ou P4 → P5** : si P4 est trop lourde ou trop conflictuelle, le mainteneur pourrait être tenté d'aller directement de P3 à P5 (en perdant la valeur du design détaillé) ou de P3 à P4 sans valider les ADRs P3. **Mitigation** : (1) entry gate EG-4.1 (P3 architecture approved) obligatoire pour démarrer P4 = pas de court-circuit P3→P4 possible, (2) démarcation P3↔P4 explicite (quoi+pourquoi vs comment, règle ≥2 bounded contexts) = pas d'ambiguïté, (3) hard cap 15k = budget prévisible, (4) format contracts différencié aligné P3 (md+json modules, +OpenAPI REST) = OpenAPI = valeur concrète pour P5 (génération de code), (5) XG-4.7 (matrice ADR P3 100%) = pas de transition P4→P5 sans conformité vérifiée.
> - **Contournement C2 — Skip Nexus-Critic** : si budget sature, tentation de skip Nexus-Critic pour gagner ~4.5k tokens. **Mitigation** : Nexus-Critic T1+T2+T3 rendu obligatoire (décision 2026-06-07) + hard cap 15k = marge de sécurité. Skip = violation de spec, comme P3.
> - **Contournement C3 — DDS vide /敷衍** : tentation de livrer un DDS "Contexte: X / Design: Y" = DDS creux = mode d'échec 6.2 documenté. **Mitigation** : Nexus-Critic T1 casseur cible spécifiquement les DDS creux (mitigation spec v2 section "Mode 1 — Poisoning"), refus catégorique 4 (pas de design qui ne respecte pas les NFR).
> - **Contournement C4 — Format uniforme** : tentation de tout livrer en md seul (pas de json, pas d'OpenAPI) = perd la machine-parse-abilité P5. **Mitigation** : format différencié explicite dans la spec v2 (aligné P3) + `openapi-lint` / `asyncapi-lint` en validation automatique.
> - **Contournement C5 — Skip matrice ADR P3** : tentation de skip la matrice XG-4.7 (perçu comme overhead). **Mitigation** : matrice obligatoire dans la checklist 8 critères de sortie + UDL 1 ("déviation ADR P3 proposée") + Nexus-Critic T2 conformité ADRs P3 = triple catch.
>
> **Cohérence P0/P1/P2/P3 v2** : aucun contournement remonté. Le main lien est que P3 architecture baseline locked pour démarrer P4 (entry gate EG-4.1) + P4 design baseline frozen pour démarrer P5 (transition criteria) = pas de court-circuit possible.

### 7.4 Valeur ajoutée perçue
> **Attendue** : éviter le "design-by-committee" et l'over-engineering. DDS formalisés = mémoire des décisions design. Format contracts différencié (OpenAPI REST) = génération de code accélérée en P5. Critère démarcation P3↔P4 explicite = pas d'ambiguïté à la transition. Matrice ADR P3 = traçabilité archi → design → code. Nexus-Critic T1+T2+T3 = catch des DDS creux, conformité NFR, prédiction ruptures P5.

### 7.5 Dette d'orchestration
> **Risque résolu (2026-06-07)** : 3-5 sub-agents en parallèle + Nexus-Critic T1+T2+T3 obligatoire = risque de saturation. **Hard cap 10k → 15k** (décision mainteneur 2026-06-07), sort du risque. P4 devient 3e phase la plus large (après P3 et P5, ex-aequo avec P5), justifié par la qualité (matrice ADR P3, contrats différenciés, démarcation explicite, 4 failure modes Drew Breunig).

### 7.6 Verdict
- [x] 🟢 **OK** : 7.1/7.2/7.3 comblées par projection + cohérence P0/P1/P2/P3 v2 (décision mainteneur 2026-06-07). Validation terrain toujours souhaitée (mini-projet test OU avis expert externe) mais ne bloque plus le verdict. Action 'mesurer usage réel P4' reste dans la stratégie roadmap pour validation différée.

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. Token budget proposé et **validé 2026-06-07** : 5k base / 8k soft / 15k hard.

### 8.1 Token budget alloué
**Validé 2026-06-07** : **5k base / 8k soft / 15k hard** (multi-agent justifié, Nexus-Critic T1+T2+T3 obligatoire, comme P3 v2). P4 devient 3e phase la plus large (après P3 et P5, ex-aequo avec P5), au lieu de la 4e. Justification : 3-5 sub-agents × 1.5k + Nexus-Critic T1+T2+T3 × 1.5k = ~12k en nominal, hard cap 15k = marge de sécurité. Token counter P4 mis à jour (`pre-tool-use/token-counter.sh` ligne 62 : 5k/8k/15k).

### 8.2 Compaction checkpoint
- [ ] A. Tous les 5 tool calls
- [ ] B. À 70% du soft cap (5.6k)
- [x] C. Les deux (belt + suspenders, aligné P3 v2)

### 8.3 Consultation cross-phase
- [x] A. P3 Architecture outputs (ADRs, architectural interface contracts) en consultation envelope — **consommation, pas re-décision**
- [x] B. P2 SRS (NFR + use cases) en slice
- [x] C. **+ Pas d'injection complète des diagrammes P3** (référencer, ne pas charger)
- [x] D. **+ Slice du SRS** (juste les NFR, pas tout)
- [x] E. **+ Slice des ADRs P3** (juste les ADRs applicables au module courant, pas tous)

### 8.4 Pattern adversarial concret
- [x] A. T1 : un dev propose DDS, Nexus-Critic casse — **OBLIGATOIRE** (3 invocations systématiques, comme P3 v2)
- [x] B. T2 : Nexus-Critic vérifie conformité NFR P2 + ADRs P3 — **OBLIGATOIRE**
- [x] C. T3 : Nexus-Critic prédit les difficultés P5 Implementation — **OBLIGATOIRE**
- [x] D. **+ Pas de Council** (escalade mainteneur sur conflit ADR P3)

### 8.5 User Decision Ledger — quoi logger
**7 éléments P4-spécifiques confirmés par le mainteneur (2026-06-07)** :

1. **Déviation ADR P3 proposée** — toute déviation avec rationale (escaladée P3 si confirmée)
2. **Module interface ratified** — pointeur vers `module-interfaces.md`
3. **Pattern utilisé par module** — mapping module → pattern
4. **Trade-off design arbitrée** — algo complexity vs readability, perf vs mémoire
5. **Rejet T1/T2 casseur** — quand Nexus-Critic a trouvé un problème et comment c'est résolu
6. **Conformité ADR vérifiée** — matrice ADR → module, déviation nulle
7. **Décision "pas de décision"** — cas où on a choisi de NE PAS trancher, et pourquoi

Stockés dans `.swebok_state.db` (table `udl_p4`) et consultables via Consultation Envelope (A1) par P5 Implementation.

### 8.6 Verdict
- [x] 🟢 OK (section 8.7 findings intégrés, 8.5 UDL 7 éléments comblé en spec v2, budget 5k/8k/15k aligné (vs 4k/7k/10k en v2-renum, justifié par Nexus-Critic T1+T2+T3 obligatoire), 8.2 compaction 60-70% retenu, 8.3 consultation envelope strict avec slice ADRs P3, 8.4 pattern adversarial T1+T2+T3 obligatoire explicité)

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md`.

#### Findings les plus pertinents pour cette phase
- **F2** : Multi-agent = 15× tokens chat → fan-out Nexus-Architect + Nexus-Backend + Nexus-Frontend + Nexus-DevOps + Nexus-Security = **justifié uniquement si P5 en profite** (et c'est le cas : P5 consomme les DDS et contrats P4)
- **F3** : Subagent brief = OBJECT/FORMAT/TOOLS/BOUND → auditer les 4 spawns parallèles
- **F5** : Lost-in-the-middle = -30% accuracy en positions 5-15 → **matrice de conformité ADR P3 en tête** du contexte Nexus-Architect (XG-4.7)
- **F8** : Compaction à 95% = trop tard → ANTI-ROT trigger à 60-70% du soft cap (5.6k)
- **F10** : Subagent output → filesystem → les DDS sont écrits dans le state, le retour au lead = pointeur
- **F13** : 3-5 subagents en parallèle max (FlowHunt) → ne pas dépasser, sinon overhead > gain

#### Anti-patterns à éviter dans cette phase
- **AP1** : 50 subagents — plafonner à 3-5 (Arch, Backend, Frontend, DevOps, Security) sauf complexité avérée
- **AP2** : Brief vague "design X" — brief structuré OBJECT/FORMAT/TOOLS/BOUND obligatoire pour chaque subagent
- **AP4** : Peer-to-peer entre Nexus — pas de canal direct, tout via Hyperagent ou state
- **AP7** : Contexte "flood" — ne JAMAIS charger le corpus entier, slice des ADRs P3 par module

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : un DDS faux ou incohérent qui contamine tout le code P5
- [x] **Distraction** : trop de patterns, sur-ingénierie
- [x] **Confusion** : 2 modules utilisent le même mot pour 2 interfaces différentes
- [x] **Clash** : 2 modules qui s'appellent avec des contrats contradictoires

#### Recommandation budget (validée 2026-06-07)
- **Base 5k / Soft 8k / Hard 15k** (3-5 sub-agents × 1.5k chacun + Nexus-Critic T1+T2+T3 × 1.5k = ~12k nominal, hard cap 15k = marge de sécurité)
- ✅ **Risque saturation levé (2026-06-07)** : hard cap 10k → 15k justifié par Nexus-Critic T1+T2+T3 obligatoire (comme P3 v2). Action P4-? (équivalent P3-9) fermée.
- ✅ **Action "étendre Drew Breunig à P4" fermée** (2026-06-07) : section "Audit des 4 failure modes Drew Breunig" ajoutée à la spec v2.

---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-07)

> **Note importante** : cette grille a été révisée le 2026-06-07 suite à l'audit P4 (vague 1 + transformation 5.5 en questions précises + section 7 par projection + critère démarcation P3↔P4 explicite).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 8 |
| New Books achetés (§19) | 0 |
| Standards NIST/OWASP (§13) | 0 |
| Open-access téléchargés | 1 |
| **TOTAL corpus-aligned local** | **9** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~20 livres
- **Disponible localement** : 8 corpus-aligned
- **Couverture effective** : **40%** ████░░░░░░

### Lacunes (§20)

- **4** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **partielles** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel
- **Décision mainteneur 2026-06-07** : 40% suffit pour P4 (phase moins "core" pour la spec SWEBOK, plus basée sur patterns). Batch d'acquisition ultérieur.

---

## Verdict global de la phase
- [x] 🟢 OK — conforme, rien à changer (toutes les sections comblées, y compris 7 par projection + cohérence P0/P1/P2/P3 v2)

## Liste d'actions
**✅ P1 — bloquants (fermés en spec v2 + grille v2, 2026-06-07)** :
1. ✅ Section 5.5 comblée en **7 questions précises avec options AskUserQuestion** (transformation vague 1, vs 5 catégories en v2-renum)
2. ✅ Section 7 comblée par **projection + cohérence P0/P1/P2/P3 v2** (vs vide en v2-renum)
3. ✅ Section 8.5 comblée (7 éléments UDL P4-spécifiques documentés)
4. ✅ Critère explicite de démarcation P3↔P4 inscrit dans P4 v2 (quoi+pourquoi vs comment, règle ≥2 bounded contexts, action P3-3 du mainteneur)
5. ✅ Verdicts tranchés (sections 1-8 + global = **🟢 partout**)
6. ✅ Spec v2 créée (`specs/workflows/by-phase/phase-4-design.md`)
7. ✅ Token counter P4 mis à jour (`pre-tool-use/token-counter.sh` ligne 62 : **5k/8k/15k** vs 4k/7k/10k en v2-renum)
8. ✅ Hard cap 10k → **15k** (justifié par Nexus-Critic T1+T2+T3 obligatoire, comme P3 v2)
9. ✅ Format contracts différencié aligné P3 v2 (md+json modules internes, md+json+OpenAPI 3.0 API REST, md+json+AsyncAPI 3.0 événements option)
10. ✅ Nexus-Critic OBLIGATOIRE (T1+T2+T3, 3 invocations systématiques) — décision mainteneur 2026-06-07
11. ✅ Matrice de conformité aux ADRs P3 obligatoire (XG-4.7) — livrable dédié
12. ✅ Audit des 4 failure modes Drew Breunig complet ajouté à la spec v2 (vs absent en v2-renum)
13. ✅ Verdict global 🟢 (toutes sections vertes, validation terrain reste souhaitée mais non bloquante)

**🟢 P2 — qualité (non bloquant, améliorations futures)** :
14. 🟢 Action 'mesurer usage réel P4 sur 1-2 projets' **maintenue dans la stratégie roadmap** pour validation terrain différée (mini-projet test OU avis expert externe, à déclencher v1.6.0 ou v2.0)
15. 🟢 Validation empirique de la projection 7.1/7.2/7.3 par 1-2 projets réels = nice-to-have, planifié en roadmap
16. 🟢 Batch d'acquisition des 4 livres manquants critiques (Fowler 2nd ed, Kerievsky, McConnell) = à planifier avec P5/P6 batch

## Notes libres
> **Phase 4 Design = v2 validée 2026-06-07 par le mainteneur (verdict 🟢)**. Phase créée lors du fix structurel (split P3 Design en P3 Architecture + P4 Design).
> **Méthode audit 2026-06-07** : grille offline (mainteneur) + **4 questions AskUserQuestion vague 1** (Claude) + rédaction spec v2 (Claude) + mise à jour grille v2 (Claude) + mise à jour token counter (Claude). Vague 2 implicite : section 5.5 transformée en 7 questions précises + section 7 comblée par projection (sans questions supplémentaires, fait dans la rédaction).
> **4 décisions tranchées par le mainteneur** : (1) Nexus-Critic T1+T2+T3 obligatoire (hard cap 15k comme P3), (2) format contracts différencié aligné P3, (3) démarcation P3↔P4 explicite dans P4 v2, (4) section 7 fermée par projection + cohérence P0/P1/P2/P3 v2.
> **Verdict global 🟢** (toutes les sections vertes, y compris 7 par projection + cohérence P0/P1/P2/P3 v2). Validation terrain reste souhaitée mais ne bloque plus le verdict.
> Cible universelle adaptative (6 cas). Budget 5k/8k/15k tokens (3e phase la plus large, ex-aequo avec P5), cap 35 min, 3-5 agents en parallèle + Nexus-Critic T1+T2+T3 obligatoire.
> 7 livrables principaux + matrice conformité ADRs P3 + diagrammes optionnels, en format différencié (md+json pour modules internes, md+json+OpenAPI 3.0 pour API REST, md+json+AsyncAPI 3.0 pour événements option).
> Critère démarcation P3↔P4 explicite inscrit dans P3 ET P4 (action P3-3 mainteneur 2026-06-06 exécutée pour P4 le 2026-06-07).
> UDL 7 éléments P4-spécifiques documentés.
> Audit 4 failure modes Drew Breunig complet ajouté à la spec v2.
> Tension principale résolue : 3-5 sub-agents en parallèle + Nexus-Critic T1+T2+T3 = ~12k nominal, hard cap 15k absorbe (comme P3 v2).
> Méthode d'audit reproductible vague 1 + transformation 5.5/7 implicite : grille offline (mainteneur) + 4-6 questions AskUserQuestion (Claude) + rédaction spec v2 + mise à jour grille v2. Section 7 = projection + cohérence P0-P(n-1) v2 par défaut (verdict 🟢 immédiat), validation terrain nice-to-have en roadmap. Pattern validé pour P4-P10.
