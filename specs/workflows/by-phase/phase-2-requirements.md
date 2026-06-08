# Phase 2: Requirements — Spécification v2

> **Statut** : v2 — validé 2026-06-05 par le mainteneur
> **Changement vs v1** : 4 agents en séquentiel strict + Nexus-Critic + Council NFR, T1+T2+T3 activés, 7 livrables (6+ADR), format md+json, budget 4k/7k/10k, cap 35 min, validation mainteneur seul, 7 questions max, 7 UDL items, traçabilité max, couverture universelle adaptative, 4 refus, 5 critères abandon, 6 cas, 10 critères sortie.

## Métadonnées

- **Phase** : 2
- **Nom** : Requirements
- **Mission** : Transformer l'intention cadrée en P0 en spécification testable, traçable, et sans ambiguïté, pour que P3 (Design) puisse designer sans ambiguïté
- **Budget temps** : 35 minutes max
- **Budget contexte** : base 4k / soft cap 7k / hard cap 10k tokens
- **Concurrency mode** : séquentiel strict (5 agents : 4 fonctionnels + 1 critique, 1 à la fois)
- **Équivalent SWEBOK v4** : P1 SWEBOK (Requirements Engineering KA)
- **Référentiels** : IEEE 830-1998, ISO/IEC/IEEE 29148:2018

---

## Démarrage

**Démarrage automatique** : après que la phase 0 (Discovery) ait livré les 7 livrables et passé la checklist 100%.

**Démarrage manuel** : sur commande explicite du mainteneur (`/speckit-requirements` ou équivalent).

**Pré-hydrate obligatoire** (F7 recherche 2026) : charger dans `.swebok_state.db` les 7 livrables P0 (charter, stakeholders, scope, risks, problem-statement, success-criteria, discovery-report). Ces éléments sont le **point de départ obligatoire** de P2.

---

## Profil utilisateur (hérité de P0)

Le profil (vibecodeur / junior / senior / équipe) est lu depuis `.swebok_state.db` (saisi en P0). L'agent adapte sa communication, son niveau de guidage, et la densité des livrables. Pas de re-questionnement en P2.

---

## 7 questions au mainteneur (max)

Le seuil de questionnement = décision à fort impact / irréversible (décision B cadrage stratégique). 7 questions max pour P2 (vs 5 en P0) car la phase est plus dense et le mainteneur veut plus de contrôle. Au-delà de 7, le système choisit en autonomie et logge dans l'UDL.

**Catégories de questions** (non exhaustif) :
1. **Existence d'un stakeholder manquant** (vs P0 register)
2. **Conflit requirement vs existant** (maintenance)
3. **NFR conflictuels** (perf vs cost, sécurité vs UX)
4. **Acceptance criterion contesté** (le mainteneur arbitre)
5. **Compliance spécifique** (RGPD, HIPAA, sectoriel)
6. **Scope additionnel tardif** (scope creep)
7. **Rejet d'un finding T1/T2 casseur** (le mainteneur maintient sa position)

L'agent peut choisir de ne pas poser les 7 si le contexte est déjà clair. Min 0, max 7.

---

## 7 activités (= 7 livrables), en séquence

| # | Activité | Agent | Livrable (md) | Livrable (json) |
|---|----------|-------|---------------|-----------------|
| 1 | Elicitation | Discovery-Orchestrator | `requirements-elicitation.md` | `requirements-elicitation.json` |
| 2 | Specification | Nexus-PM | `requirements-spec.md` | `requirements-spec.json` |
| 3 | Use Case Modeling | Nexus-PM | `use-case-model.md` | `use-case-model.json` |
| 4 | Acceptance Criteria | Nexus-QA | `acceptance-criteria.md` | `acceptance-criteria.json` |
| 5 | Prioritization + RTM | Nexus-Architect | `prioritized-backlog.md` + `requirements-traceability-matrix.md` | `prioritized-backlog.json` + `requirements-traceability-matrix.json` |
| 6 | NFR + ADR | Nexus-Architect + Council 4 reviewers | `nfr-and-adr.md` | `nfr-and-adr.json` |
| 7 | Validation + Adversarial | Nexus-Critic (T1+T2+T3) | `requirements-validation-report.md` | `requirements-validation-report.json` |

**Travail des agents** : séquentiel strict. L'agent N+1 hérite du contexte consolidé de N. Chaque agent écrit son livrable (md + json) puis passe le relais.

**Format des livrables** : double (md + json) — md pour lecture humaine, json pour tooling et consultation inter-phase (A1).

**Council NFR** (activité 6) : 4 reviewers (CISO / QA / Architect / DevOps) en parallèle pour valider les NFR conflictuels. Sortie : un verdict unifié pour chaque NFR contesté.

---

## 3 patterns adversariaux + 1 council

| Pattern | Acteur | Cible | Sortie |
|---------|--------|-------|--------|
| **T1 casseur** | Nexus-Critic | SRS + AC | Liste d'ambiguïtés, contradictions, zones floues |
| **T2 conformité spec** | Nexus-Critic | SRS vs IEEE 830 / ISO 29148 | Score de conformité (cible ≥95%) |
| **T3 conséquentialiste** | Nexus-Critic | Prédiction impacts P3 (Design) et P4 (Implé) | Top-3 zones à risque en aval |
| **Council NFR** | CISO + QA + Architect + DevOps | NFR conflictuels (perf vs cost, etc.) | Verdict unifié par NFR contesté |

**Nexus-Critic** : 5e agent dédié, activé en activité 7. Lit le SRS, le casse, vérifie la conformité, prédit les impacts aval. Son rapport est inclus tel quel dans `requirements-validation-report.md`.

**Isolation des contextes** (ACI stratégie §4.5) : Nexus-Critic ne voit pas le prompt système des producteurs. Council NFR ne voit que les NFR (pas le SRS complet).

---

## 7 éléments loggés dans le User Decision Ledger (UDL)

| Élément | Description | Exemple |
|---------|-------------|---------|
| Requirement ajouté ou refusé | Tout requirement accepté ou rejeté en P2, avec rationale | "Ajout REQ-23 (audit log) car compliance" |
| Ambiguïté levée | Cas où 2 interprétations étaient possibles, arbitrage | "REQ-15 'rapide' → '≤200ms p95' (arbitrage mainteneur)" |
| NFR ajouté ou refusé | NFR (perf, scalabilité, sécurité) ajouté au SRS ou refusé | "NFR-SEC-2 (chiffrement at-rest) ajouté car RGPD" |
| Acceptance criterion contesté | AC où Nexus-QA et mainteneur ont divergé | "AC-REQ-08 'fonctionne offline' → assoupli à 'gracieux fail'" |
| Sign-off partiel ou refus | Sign-off obtenu avec réserve, ou refusé sur un livrable | "Validation report signé sous réserve de clarification AC-12" |
| Rejet du T1/T2 casseur | Quand Nexus-Critic a trouvé un problème et comment c'est résolu | "T1 a trouvé ambiguïté REQ-31, levée via question 4 mainteneur" |
| Décisions "pas de décision" | Cas où on a choisi de NE PAS trancher, et pourquoi | "Pas d'arbitrage perf vs cost : escaladé en P3 Design" |

Stockés dans `.swebok_state.db` (table `udl_p2`) et consultables via Consultation Envelope (A1) par les phases suivantes.

---

## Alternatives écartées (rejouabilité enrichie)

Pour chaque décision structurante (requirement ajouté, NFR ajouté, AC contesté), on documente dans le livrable concerné, section "Alternatives considered" :
- Les options non choisies
- Pourquoi on ne les a pas choisies
- Dans quelles conditions on les reconsidérerait

La phase est **rejouable** : mêmes inputs (livrables P0 + 7 questions) = même SRS déterministe (modulo ajustements adaptatifs si contexte a changé).

---

## Format des fichiers (double)

- **Markdown** : lecture humaine, structuré par sections
- **JSON** : machine-parse, utilisé par les outils de traçabilité et la consultation inter-phase
- **Base interne** : `.swebok_state.db` pour le UDL et la consultation inter-phase (A1)

**Convention de nommage** : `${livrable}.md` + `${livrable}.json` dans `specs/workflows/by-phase/phase-2-requirements/`.

---

## Critères d'abandon (5 max)

L'agent abandonne et prévient le mainteneur si :
1. Conflit de scope non résolvable après 2 tentatives
2. Risque bloquant non mitigable identifié pendant l'elicitation
3. RTM < 100% après 2 itérations
4. Conflit stakeholder non résolvable en 24h
5. Dépassement de 35 min sans avancée claire

---

## Conditions de sortie (passage à P3)

Le mainteneur valide avec une **checklist à 100%** (10 critères max) :
- [ ] `requirements-spec.md` existe (≥95% IEEE 830)
- [ ] `use-case-model.md` existe
- [ ] `requirements-traceability-matrix.md` existe (100% coverage)
- [ ] `prioritized-backlog.md` existe (100% P0-P4)
- [ ] `acceptance-criteria.md` existe (≥1 AC par requirement)
- [ ] `requirements-validation-report.md` existe (T1+T2+T3 + Council passés)
- [ ] `nfr-and-adr.md` existe (ADR signé pour choix structurants)
- [ ] Alternatives écartées documentées par décision structurante
- [ ] UDL 7 éléments loggés
- [ ] Aucune ambiguïté non résolue (vérifié par Nexus-Critic)

Pas de feu vert séparé — les documents font foi. Le mainteneur signe en cochant les 10 critères.

---

## Budget contexte

- **Base** : 4k tokens
- **Soft cap** : 7k tokens (alerte)
- **Hard cap** : 10k tokens (compactage forcé + abort si insuffisant)

**Justification du budget large** : 4 agents en séquentiel + 1 Nexus-Critic + 4 council reviewers = potentiel de 9 invocations d'agents, mais séquentiel strict = pas de fan-out ×15 (F2 recherche 2026). Le coût additionnel vs P2 single-agent est re-chargement contexte, pas ×15. 4k/7k/10k est cohérent avec P0 (4 agents aussi).

### Token counter live (implémenté 2026-06-04)

Le hook `pre-tool-use/token-counter.sh` mesure le coût tokens de chaque appel d'outil et le cumule dans `${PHASE}.tokens.used` du `.swebok_state.db`. Budget P2 hardcodé à `4000/7000/10000` (mis à jour v2). Trois seuils :
- **Soft cap (7k)** : `WARN` non-bloquant
- **85% hard (8.5k)** : `WARN` non-bloquant
- **Hard cap (10k)** : `BLOCK` (exit 1) + reset obligatoire

⚠️ **Vigilance P3** : 9 agents potentiels dans la phase (4 + 1 + 4) = saturation possible. À mesurer en pratique, ajuster si hard cap atteint >2% des phases.

---

## Pauses

Toutes les 5 actions : compaction checkpoint (nettoyage du contexte de travail). Compaction à 60-70% du soft cap (F8 recherche 2026), pas 95% (trop tardif).

---

## Couverture cas (universelle adaptative)

6 cas explicites (le profil P0 + détection auto adapte le déroulé) :
1. **Greenfield from-scratch** : nouveau projet, pas d'existant
2. **Maintenance legacy** : requirements = user stories de bugfix/évolution
3. **Projet interne** (équipe, gouvernance légère)
4. **Projet externe client** (sign-off formel, change management)
5. **Compliance-driven** (RGPD, HIPAA, sectoriel — requirements externes imposés)
6. **R&D / exploration** (requirements = hypothèses à valider, pas de spec stricte)

---

## Projets passés

L'agent consulte automatiquement le `.swebok_state.db` et le dossier `audit/` pour s'inspirer des SRS similaires. Les patterns récurrents (NFR, AC, structure) sont remontés en suggestion au mainteneur.

---

## Refus catégoriques (4)

La phase P2 **refuse** de :
1. **Pas d'architecture détaillée** (forcé en P3 Design)
2. **Pas d'estimation effort** (forcé en P4 Implementation, absent du modèle)
3. **Pas de figeage avant validation** (checklist 100% mainteneur)
4. **Pas de NFR inventés** (chaque NFR doit venir d'un besoin explicite ou d'une contrainte documentée)

---

## Agents

| Agent | Activités | Rôle |
|-------|-----------|------|
| Discovery-Orchestrator | 1 | Elicitation structurée, interviews, pré-hydrate P0 |
| Nexus-PM | 2, 3 | Specification SRS + use case model |
| Nexus-Architect | 5, 6 | RTM, priorisation, NFR, ADR |
| Nexus-QA | 4 | Acceptance criteria, testabilité |
| Nexus-Critic (5e agent) | 7 | T1 casseur + T2 conformité + T3 conséquentialiste |
| Council 4 reviewers | 6 (NFR) | CISO + QA + Architect + DevOps sur NFR conflictuels |

**Concurrency** : séquentiel strict. 1 agent actif à la fois. Council NFR = exception (4 reviewers en parallèle uniquement pour cette activité 6 sur les NFR contestés).

---

## Skills requises

- `discovery-orchestrator` : elicitation, cadrage besoin
- `nexus-pm` : specification SRS, use case modeling
- `nexus-architect` : RTM, priorisation, NFR
- `nexus-qa` : acceptance criteria, testabilité
- `nexus-critic` : T1 casseur + T2 conformité + T3 prédiction aval
- `speckit-qa` : requirements quality assurance
- `council-bridge` : aggregation 4 reviewers NFR

---

## Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-requirements-approved` | 10 critères checklist validés | Triggers Phase 3 (Design) |
| `requirements-frozen` | Spec complète | Locks requirements baseline |
| `prioritized-backlog-created` | Backlog P0-P4 fait | Updates product backlog |
| `traceability-matrix-established` | RTM complet | Enables change impact analysis |
| `udl-p2-logged` | 7 éléments UDL loggés | Snapshot pour phases suivantes |
| `abandon-triggered` | 1 des 5 critères atteint | Prévient mainteneur |

---

## Présentation finale

SRS complet (7 livrables md + 7 livrables json) + **résumé 1 page** en tête qui donne l'essentiel (scope, top-3 NFR, top-5 requirements, ADR résumés, verdict Council, rejets T1/T2/T3 arbitrés, alternatives écartées top-3, décision finale). Le mainteneur peut ne lire que le résumé s'il est pressé.

---

## Notes de version

- **v2 (2026-06-05)** : refonte complète basée sur 20 décisions tranchées par le mainteneur. 4 agents séquentiel + Nexus-Critic + Council NFR, T1+T2+T3, 7 livrables (6+ADR), format md+json, budget 4k/7k/10k, cap 35 min, validation mainteneur seul, 7 questions max, 7 UDL items, traçabilité max, couverture universelle adaptative, 4 refus, 5 critères abandon, 6 cas, 10 critères sortie, audit 4 failure modes Drew Breunig.
- **v1** : spec originale avec Hyperagent enabled, 4 parallel_tasks sync:false, 6 artifacts md uniquement, XG-2.5 sign-off stakeholders (incompatible avec cible universelle solo), 0 budget token, 0 cap durée.

Voir `audit/phase-2-requirements-audit.md` pour la traçabilité des 20 décisions.

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-05

### Mode 1 — Poisoning (Empoisonnement)

**Risque en P2** : un requirement mal interprété qui contamine tout le SRS et contamine P3/P4 en aval (ex: "rapide" sans seuil numérique qui devient tout et n'importe quoi en P3).

**Mitigations spec v2** :
1. Acceptance criteria **chiffrés** pour chaque requirement (Nexus-QA, activité 4) — pas d'ambiguïté sémantique
2. UDL item 1 ("requirement ajouté ou refusé") logge tout ajout avec rationale
3. T1 casseur (Nexus-Critic) cherche activement les interprétations multiples
4. 7 questions max pour les cas ambigus (le mainteneur arbitre)

**Status** : ✅ Validé (4 mécanismes)

### Mode 2 — Distraction (Distraction)

**Risque en P2** : trop de NFR ou de requirements périphériques qui éloignent du core (gold-plating).

**Mitigations spec v2** :
1. Backlog **priorisé P0-P4** avec 100% coverage — le P3/P4 ne lit que P0-P1
2. Refus catégorique 4 (NFR inventés interdits)
3. 4 refus (pas d'archi, pas d'estimation, pas de figeage, pas de NFR inventés) — focus forcé
4. Council NFR ne s'active **que** sur les NFR conflictuels, pas sur tous les NFR

**Status** : ✅ Validé (4 mécanismes)

### Mode 3 — Confusion (Confusion)

**Risque en P2** : 2 stakeholders utilisent le même mot pour 2 choses différentes (ex: "user" = client final ou admin ?).

**Mitigations spec v2** :
1. UDL item 2 ("ambiguïté levée") logge explicitement les cas arbitrés
2. Format double (md + json) — le json force la structure, pas de place pour le flou
3. Use case model avec acteurs **nommés explicitement** (pas de pronoms)
4. T1 casseur cible spécifiquement les ambiguïtés sémantiques

**Status** : ✅ Validé (4 mécanismes)

### Mode 4 — Clash (Conflit)

**Risque en P2** : requirements contradictoires (perf vs cost, sécurité vs UX, scope vs délai).

**Mitigations spec v2** :
1. Council NFR (4 reviewers) tranche les NFR conflictuels
2. UDL item 7 ("décisions 'pas de décision'") documente les clashes non arbitrés, escalade P3
3. T2 conformité spec (Nexus-Critic) détecte les clashes entre requirements
4. 5 critères d'abandon incluant "RTM < 100% après 2 itérations" = sortie propre si clash irréductible

**Status** : ✅ Validé (4 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | Requirement mal interprété contamine SRS | 4 mécanismes | ✅ |
| Distraction | Gold-plating éloigne du core | 4 mécanismes | ✅ |
| Confusion | Même mot, 2 sens | 4 mécanismes | ✅ |
| Clash | Requirements contradictoires | 4 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Aucune mitigation supplémentaire requise pour P2.

**À étendre** : les phases P3-P9 devront justifier leurs propres mitigations aux 4 modes (méthode reproductible).
