# Phase 0: Discovery — Spécification v2

> **Statut** : v2 — validé 2026-06-04 par le mainteneur
> **Changement vs v1** : séquentiel strict, 7 activités, 7 livrables, budget 4k/7k/10k, profil adaptatif, cap 35 min, XG simplifié (validé mainteneur), 5 questions max, 6 UDL items, triple format, auto-démarrage, 3+1 critères d'abandon, 2 vérifs + challenge adversarial, projets passés auto, alternatives documentées.

## Métadonnées

- **Phase** : 0
- **Nom** : Discovery
- **Mission** : Cadrer un projet (nouveau ou à recadrer) en produisant 7 livrables actionnables pour les phases suivantes
- **Budget temps** : 35 minutes max
- **Budget contexte** : base 4k / soft cap 7k / hard cap 10k tokens
- **Concurrency mode** : séquentiel strict (4 agents, 1 à la fois)

---

## Démarrage

**Démarrage automatique** dans 2 cas :
- L'utilisateur exprime une nouvelle idée
- L'agent estime qu'un projet en cours n'est pas clair ou mal cadré

**Démarrage manuel** : sur commande explicite de l'utilisateur.

---

## Profil utilisateur (détection 1 question au démarrage)

- 🟢 Vibecodeur (non-développeur, max de guidage, pas de jargon)
- 🟡 Dev junior (équilibre, vocabulaire technique ok)
- 🟠 Dev senior (rapide, dense, pas de blabla)
- 🔵 Équipe (multi-personnes, gouvernance explicite)

L'agent adapte ensuite sa communication, son niveau de guidage, et la densité des livrables.

---

## 5 questions au mainteneur (max)

1. **Contraintes dures** : deadline, budget, stack imposé, conformité
2. **Scope in/out** : ce qu'on inclut, ce qu'on exclut
3. **Hypothèse de ROI** : pourquoi ce projet maintenant, pas l'alternative
4. **Risque bloquant** : y a-t-il un risque "no-go"
5. **Gouvernance** : qui valide, qui décide, qui relit

L'agent peut choisir de ne pas poser les 5 si le contexte est déjà clair. Min 0, max 5.

---

## 7 activités (= 7 livrables), en séquence

| # | Activité | Agent | Livrable |
|---|----------|-------|----------|
| 1 | Stakeholder Analysis | Nexus-PM | `stakeholder-register.md` |
| 2 | Context Exploration | Nexus-Architect | `context-survey.md` |
| 3 | Problem Framing | Discovery-Orchestrator | `problem-statement.md` (1 page) |
| 4 | Risk Discovery | Nexus-Security | `risk-preliminary.md` |
| 5 | Success Criteria Definition | Discovery-Orchestrator | `success-criteria.md` (mesurable) |
| 6 | Project Chartering | Discovery-Orchestrator | `project-charter.md` |
| 7 | Discovery Synthesis | Hyperagent-Orchestrator | `discovery-report.md` |

**Travail des agents** : séquentiel strict. L'agent N+1 hérite du contexte consolidé de N. Chaque agent écrit son livrable puis passe le relais.

**Format des livrables** : triple (md + json + entrée dans `.swebok_state.db`).

---

## 3 vérifications adversariales + challenge (pendant activité 7)

- **Vérif 1 (complétude)** : aucun stakeholder, scope, risque n'a été oublié ?
- **Vérif 2 (risque futur)** : qu'est-ce qui peut casser dans les phases 2-3 ?
- **Challenge intelligent** : l'agent pose des questions percutantes à l'utilisateur, au fil de l'eau

L'agent challenger est le Discovery-Orchestrator en mode "red team" temporaire.

---

## 6 éléments loggés dans la mémoire décisions (UDL)

| Élément | Exemple |
|---------|---------|
| Intention de départ | "Je veux un outil de monitoring de mes serveurs" |
| Contraintes dures | "Deadline : 31/12/2026. Budget : 5k€" |
| Scope in/out | "In : monitoring CPU/RAM. Out : alerting Slack" |
| Top-3 risques | "Dépendance API tierce, complexité infra, adoption utilisateur" |
| Friction/contournement | "Le mainteneur hésite, je propose 2 cadrages alternatifs" |
| Décisions marquantes | "Choix A而非 B parce que..." |

---

## Alternatives écartées (rejouabilité enrichie)

Pour chaque décision clé, on documente dans `discovery-report.md` section "Alternatives considered" :
- Les options non choisies
- Pourquoi on ne les a pas choisies
- Dans quelles conditions on les reconsidérerait

---

## Format des fichiers (triple)

- **Markdown** : lecture humaine
- **JSON** : tooling, machine-parse
- **Base interne** : `.swebok_state.db` pour les phases suivantes (consultation inter-phase)

---

## Critères d'abandon (3 + temps)

L'agent abandonne et prévient le mainteneur si :
- Conflit de scope non résolvable
- Risque bloquant non mitigable
- Mainteneur dit "je ne sais pas ce qu'on fait"
- Dépassement de 35 min sans avancée claire

---

## Conditions de sortie (passage à P1)

Les 7 livrables sont remplis, validés, sauvegardés en triple format, et loggés dans l'UDL. Pas de feu vert séparé — les documents font foi.

Le mainteneur valide avec une **checklist à 100%** :
- [ ] `stakeholder-register.md` existe
- [ ] `context-survey.md` existe
- [ ] `problem-statement.md` existe (1 page)
- [ ] `risk-preliminary.md` existe
- [ ] `success-criteria.md` existe (mesurable)
- [ ] `project-charter.md` existe
- [ ] `discovery-report.md` existe (rapport complet, alternatives documentées)
- [ ] UDL 6 éléments loggés
- [ ] Profil utilisateur détecté
- [ ] 5 questions (ou moins) traitées

---

## Budget contexte

- **Base** : 4k tokens
- **Soft cap** : 7k tokens (alerte)
- **Hard cap** : 10k tokens (compactage forcé + abort si insuffisant)

### Token counter live (implémenté 2026-06-04)

Le hook `pre-tool-use/token-counter.sh` mesure le coût tokens de chaque appel d'outil et le cumule dans `${PHASE}.tokens.used` du `.swebok_state.db`. Trois seuils :

- **Soft cap (7k)** : `WARN` non-bloquant, recommandation de compaction
- **85% hard (8.5k)** : `WARN` non-bloquant
- **Hard cap (10k)** : `BLOCK` (exit 1) + reset obligatoire via `state_engine set ${PHASE}.tokens.used 0`

**Heuristique** : `chars(payload JSON) / 4` (estimation grossière anglais/code, pas un vrai tokenizer). Suffisant pour gating de budget.

**Lecture en cours de phase** : `HARNESS_DIR=... python3 lib/state_engine.py get P0.tokens.used`

**Note** : le compteur est **fail-open** (un crash du compteur ne bloque jamais l'agent). Voir `00-context-engineering-strategy.md` §4.1 (Compaction Checkpoint) pour le couplage avec le checkpoint toutes les 5 actions.

## Pauses

Toutes les 5 actions : compaction checkpoint (nettoyage du contexte de travail).

## Couverture cas

Universel : from-scratch, maintenance, projet interne, projet externe, solo, équipe. La phase s'adapte au contexte détecté.

## Projets passés

L'agent consulte automatiquement le `.swebok_state.db` et le dossier `audit/` pour s'inspirer des projets similaires. Les patterns récurrents sont remontés en suggestion au mainteneur.

---

## Agents

| Agent | Activités |
|-------|-----------|
| Discovery-Orchestrator | 3, 5, 6 + challenge adversarial |
| Nexus-PM | 1 |
| Nexus-Architect | 2 |
| Nexus-Security | 4 |
| Hyperagent-Orchestrator | 7 (synthèse finale) |

**Concurrency** : séquentiel strict (1 agent actif à la fois).

---

## Skills requises

- `discovery-orchestrator` : coordination et cadrage
- `nexus-pm` : stakeholder analysis
- `nexus-architect` : context exploration
- `nexus-security` : risk discovery
- `nexus-cpo` (si profil équipe) : gouvernance

---

## Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `post-discovery-complete` | 7 livrables validés | Triggers Phase 1 |
| `stakeholder-map-generated` | Activité 1 terminée | Met à jour stakeholder register |
| `risk-landscape-surveyed` | Activité 4 terminée | Met à jour risk register |
| `abandon-triggered` | Critère d'abandon atteint | Prévient mainteneur |

---

## Notes de version

- v2 (2026-06-04) : refonte complète basée sur 20 décisions tranchées par le mainteneur. Voir `audit/phase-0-discovery-audit.md` pour la traçabilité.
- v2.1 (2026-06-04) : actions P3 closes — (1) audit systématique des 4 failure modes Drew Breunig (§ Audit des 4 failure modes), (2) token counter live implémenté (`pre-tool-use/token-counter.sh`, budget 4k/7k/10k enforced).
- v1 : spec originale avec 4 activités, parallélisme Hyperagent, XG-0.5 "≥2 stakeholders" (incompatible avec cible universelle solo).

---

## Audit des 4 failure modes Drew Breunig

> Référence : Drew Breunig, cité par LangChain "Context Engineering for Agents" (2025-07-02) — https://www.langchain.com/blog/context-engineering-for-agents
> Date audit : 2026-06-04

### Mode 1 — Poisoning (Empoisonnement)

**Risque en P0** : une info pourrie capturée tôt contamine tout le cadrage downstream (ex: profil deviné faussement qui biaise tout le ton).

**Mitigations spec v2** :
1. Profil utilisateur détecté en 1 question explicite (pas deviné)
2. Intention de départ capturée **littéralement** dans l'UDL (item 1) — pas de reformulation
3. 5 questions max bornées = pas d'interprétation longue qui dérive
4. Validation mainteneur finale (checklist 100%) = catch du poison avant propagation vers P2

**Status** : ✅ Validé (4 mécanismes)

### Mode 2 — Distraction (Distraction)

**Risque en P0** : trop d'info consultée (corpus, projets passés) fait perdre le focus.

**Mitigations spec v2** :
1. Budget contexte strict 4k/7k/10k enforced par `token-counter.sh` (action #10)
2. Pre-hydrate L0 partiel (jamais le corpus entier, recommandation F4 context rot)
3. 7 activités en séquentiel strict = pas de fan-out qui éparpille l'attention (vs F2 ×15 tokens)
4. 7 livrables ciblés = focus sur les artefacts utiles, pas exploration infinie

**Status** : ✅ Validé (4 mécanismes)

### Mode 3 — Confusion (Confusion)

**Risque en P0** : trop d'éléments contradictoires sans tri (ex: 5 hypothèses de ROI, 4 stakeholders avec avis divergents).

**Mitigations spec v2** :
1. 5 questions max structurées = top-5 des zones de clarification, pas 50
2. Format triple (md + json + DB) = parsing structuré, pas de re-interprétation
3. Alternatives documentées dans `discovery-report.md` (section "Alternatives considered") = explicite ce qui n'a pas été choisi
4. Compaction toutes les 5 actions = nettoyage du bruit accumulé

**Status** : ✅ Validé (4 mécanismes)

### Mode 4 — Clash (Conflit)

**Risque en P0** : 2 sources contradictoires (ex: contraintes dures "budget 5k" mais stakeholder "10k minimum").

**Mitigations spec v2** :
1. Question 1 dédiée aux "contraintes dures" = clarification explicite des sources de vérité
2. Question 4 dédiée aux "risques bloquants" = capture les contradictions comme risque
3. Adversarial vérif 1 (complétude) = détecte les éléments contradictoires manquants
4. Critère d'abandon "conflit de scope non résolvable" = sortie propre si clash irréductible

**Status** : ✅ Validé (4 mécanismes)

### Bilan

| Mode | Risque | Mitigations spec v2 | Status |
|------|--------|---------------------|--------|
| Poisoning | Info pourrie contamine | 4 mécanismes | ✅ |
| Distraction | Trop d'info noie | 4 mécanismes | ✅ |
| Confusion | Éléments contradictoires | 4 mécanismes | ✅ |
| Clash | Sources qui s'affrontent | 4 mécanismes | ✅ |

**Verdict** : spec v2 est **robuste** aux 4 failure modes Drew Breunig. Aucune mitigation supplémentaire requise pour P0.

**À étendre** : quand l'audit couvrira P2-P9, chaque phase devra justifier ses propres mitigations aux 4 modes.
