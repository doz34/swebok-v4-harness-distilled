# Audit — Phase 0 : Discovery

> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 0
- Nom : Discovery
- Équivalent SWEBOK v4 : hors-SWEBOK (ajouté)
- Spec existante : `specs/workflows/by-phase/phase-0-discovery.md`
- Date de l'audit : 04/06/2026 (révisé 2026-06-06 post-corpus)
- Auditeur : mainteneur
- Corpus-aligned : OUI — voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`
  - Couverture corpus : **77%** (post-vague 8, 2026-06-09) — cf. §39 du corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
**Suggestions (cocher ou reformuler)** :
- [x] A. *« Initial exploration, stakeholder identification, and project chartering »* (spec actuelle)
- [x] B. *« Transformer une intention floue en problème cadré, avec parties prenantes identifiées et risques pré-cartographiés »*
- [x] C. *« Produire un charter + scope + risk landscape + stakeholder map exploitables par les phases suivantes »*
- [ ] Autre : ____________________________________________

### 1.2 Périmètre
**Suggestions** :
- [x] A. Stakeholder analysis + context exploration + problem framing + risk discovery
- [x] B. + quick corpus sweep (L0) pour ne pas réinventer
- [x] C. + decision tree "est-ce qu'on a vraiment un projet à faire ?"
- [ ] Autre : ____________________________________________

### 1.3 Hors-périmètre
**Suggestions** :
- [x] A. Pas d'écriture de code (c'est P5+)
- [x] B. Pas d'architecture détaillée (c'est phase-3)
- [x] C. Pas de requirements spec (c'est phase-2)
- [x] D. Pas d'engagement formel sur un livrable précis (c'est pour le charter signé en XG-0.1)
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK
- [ ] 🟡 À ajuster
- [ ] 🔴 À repenser

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
**Suggestions** :
- [x] A. Initiative documentée + stakeholder request (spec EG-0.1, EG-0.2)
- [x] B. Intent utilisateur = "j'ai une idée" / "je veux construire X"
- [x] C. Auto-déclenché après validation d'un précédent projet
- [ ] Autre : ____________________________________________

### 2.2 Critères de complétion
**Suggestions** (cocher les plus importants) :
- [x] A. Charter documenté (XG-0.1, ≥95% checklist)
- [x] B. Stakeholder register à ≥90%
- [x] C. Scope défini avec inclusions/exclusions explicites
- [x] D. Risk landscape à ≥80% coverage
- [ ] E. Discovery report signé par ≥2 stakeholders
- [ ] F. Le mainteneur peut dire "je sais ce qu'on va faire et pourquoi"
- [ ] Autre : ____________________________________________

### 2.3 Conditions d'échec → escalade
**Suggestions** :
- [ ] A. Pas de stakeholder identifié après X jours
- [x] B. Conflit de scope non résolvable
- [x] C. Risques bloquants non mitigables
- [x] D. Le mainteneur dit explicitement "je ne sais pas ce qu'on fait"
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟡 À ajuster (incohérence XG-0.5 résolue en v2 : "validé mainteneur + checklist 100%")

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
**Suggestions** :
- [x] A. Aucune (première phase)
- [x] B. Contexte projet (si déjà un `.swebok_state.db` existe)
- [x] C. Historique d'anciens projets similaires (cross-project memory)
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
**Suggestions** :
- [x] A. Demande explicite ("je veux faire X")
- [x] B. Clarification des motivations profondes (le "pourquoi" derrière le "quoi")
- [x] C. Identification des stakeholders clés
- [x] D. Contraintes budgétaires / temporelles
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **53%** (█████░░░░░).**Sources externes disponibles localement (post-corpus) :****New Books (achats locaux)** (8 livres) — chemin `/home/doz/Bureau/New Books/` :- **Agile Project Management with Scrum #1** (—, 2024) — formats: EPUB- **Agile Project Management with Scrum #2** (—, 2024) — formats: EPUB- **The Product-Minded Engineer** (Drew Hoskins, 2024) — formats: EPUB- **UI/UX Design Basics (Figma + UI/UX)** (—, 2024) — formats: PDF- **Understanding Project Management (with PMBOK summary)** (—, 2021) — formats: EPUB- **Remote Team Interactions Workbook** (—, 2020) — formats: EPUB- **Remote Team Interactions Workbook (dup)** (—, 2020) — formats: EPUB- **The Standard for OPM** (PMI, 2018) — formats: EPUB**Standards NIST/OWASP téléchargés (open access)** (3) :- NIST 800-30r1 (Risk Assessment)- NIST 800-37r2 (RMF)- NIST AI 100-1 (AI Risk Mgmt)**Lacunes critiques restantes (à acquérir)** (9) :- The Mythical Man-Month, 50th Anniv. (Brooks) (2025)  -- Anniversary edition récente. EPUB 1995 déjà acquis.- Accelerate (Forsgren/Humble/Kim) (2018)  -- 🔴 La science derrière DORA. Acquérir.- Waltzing with Bears (DeMarco/Lister) (2003)  -- Gestion des risques. Toujours référence.- Death March 2nd (Yourdon) (2009)  -- Détecter projets impossibles. Toujours valide.- Impact Mapping (Adzic) (2012)  -- FREE PDF sur impactmapping.org. Excellent.- ... et 4 autres. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20.
### 3.4 Verdict
- [x] 🟢 OK (exhaustif : utilisateur, sources externes, corpus)

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
**Suggestions** (cocher) :
- [x] A. `project-charter.md` (spec actuelle)
- [x] B. `stakeholder-register.md` (spec actuelle)
- [x] C. `discovery-report.md` (spec actuelle)
- [x] D. `risk-preliminary.md` (spec actuelle)
- [x] E. `context-survey.md` (spec actuelle)
- [x] F. **+ `problem-statement.md` clair en 1 page** (suggéré — pas dans la spec)
- [x] G. **+ `success-criteria.md` mesurables** (suggéré — pas dans la spec)
- [ ] Autre : ____________________________________________

### 4.2 Format de stockage
**Suggestions** :
- [ ] A. Markdown uniquement
- [ ] B. JSON structuré (pour machine-parse)
- [x] C. Les deux (md pour humain, json pour tooling)
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
**Suggestions** :
- [ ] A. Résumé 1 page + liens vers le détail
- [x] B. Full report
- [ ] C. Progressive disclosure (le mainteneur demande ce qu'il veut voir)
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
**Suggestions** :
- [x] A. Oui — rejouable depuis les outputs
- [ ] B. Partiellement — il manque le "pourquoi on a écarté les alternatives"
- [ ] C. Non — à améliorer
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟡 À ajuster (7 livrables désormais obligatoires en spec v2 : 5 + problem-statement + success-criteria)

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
**Suggestions** (cocher les pertinents) :
- [x] A. Hyperagent-Orchestrator (spec)
- [x] B. Nexus-Architect (spec)
- [x] C. Nexus-PM (spec)
- [x] D. Nexus-Security (spec)
- [x] E. **+ Discovery-Orchestrator (cité en required skills)** — c'est ce skill-là
- [ ] F. Réduire à 2-3 agents pour cette phase exploratoire ?
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
**Suggestions** :
- [x] A. `nexus-architect`, `nexus-pm`, `nexus-security` (spec)
- [x] B. `discovery-orchestrator` (cité)
- [x] C. **+ Outil de consultation L0 du corpus** pour ne pas réinventer
- [x] D. **+ Outil de questionnement socratique** (clarifier le besoin)
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

**Livres canoniques disponibles localement pour cette phase** (8 livres corpus-aligned sur ~15 recommandés = **53%**) :

- **New Books** : 8 livres — voir détail §3.3 ci-dessus
- **Standards** : 3 NIST/OWASP

**Lacunes critiques (§20)** : 9 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
**Suggestions** (cocher) :
- [ ] A. T1 (producteur vs casseur) — peu pertinent en discovery (pas d'artefact à casser)
- [x] B. T2 (spec-compliance) — oui : le discovery respecte-t-il la checklist ?
- [x] C. T3 (conséquentialiste) — oui : prédire les risques de phase 2-3
- [ ] D. Aucun adversarial (trop early) — défendable
- [x] Autre : Adversarial pour challenger l'utilisateur intelligemment tout en l'accompagnant.

### 5.5 Points de décision utilisateur (B threshold)
**Décisions confirmées par le mainteneur (2026-06-04) — 5 questions max** :

1. **Contraintes dures** : deadline, budget, stack imposé, conformité réglementaire
2. **Scope in/out** : ce qu'on inclut, ce qu'on exclut
3. **Hypothèse de ROI** : pourquoi ce projet maintenant, pourquoi pas l'alternative
4. **Risque bloquant** : y a-t-il un risque "no-go" identifié
5. **Gouvernance** : qui valide, qui décide, qui relit

L'agent peut choisir de ne pas poser les 5 si le contexte est déjà clair. Min 0, max 5.

### 5.6 Verdict
- [x] 🟡 À ajuster (5.5 comblé en v2, 5.4 adversarial explicité : 2 vérifs + challenge, 4 agents en séquentiel strict)

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques
**Suggestions** :
- [x] A. Refuse d'écrire du code (P5+)
- [x] B. Refuse de figer des requirements précis (phase-2)
- [x] C. Refuse de s'engager sur un planning détaillé (phase-4)
- [ ] Autre : ____________________________________________

### 6.2 Modes d'échec connus
**Suggestions** :
- [x] A. Discovery paralysis (trop d'exploration, pas de décision)
- [x] B. Solutionnisme précoce (on a déjà décidé de la solution avant d'avoir compris le problème)
- [x] C. Stakeholders oubliés (on découvre un acteur clé trop tard)
- [x] D. Scope creep (on ajoute des features au lieu de cadrer)
- [ ] Autre : ____________________________________________

### 6.3 Cas limites
**Suggestions** :
- [x] A. Projet greenfield pur (pas d'existant)
- [ ] B. Maintenance d'un projet legacy (l'existant EST le contexte)
- [ ] C. Projet interne vs client externe
- [ ] D. Solo dev vs équipe
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
**Suggestions** :
- [x] A. 3 deliverables en retard → escalade mainteneur
- [ ] B. Conflit stakeholder → escalade mainteneur (impossible à résoudre en autonomie)
- [x] C. Risque bloquant → escalade mainteneur
- [ ] Autre : ____________________________________________

### 6.5 Verdict
- [x] 🟡 À ajuster (couverture universelle explicite en v2 : from-scratch, maintenance, interne, externe, solo, équipe)

---

## Section 7 — Adéquation aux besoins (utilité)

### 7.1 Usage réel
**Question ouverte** : est-ce que tu utilises effectivement cette phase dans ton workflow actuel, ou tu la sautes ?

> Oui, je dirais même que c'est la plus importante de toutes car elle permet un bon cadrage au tout début d'un projet ou de recadrer un projet qui serait trop parti à la dérive par exemple.
> ____________________________________________________________________________

### 7.2 Friction observée
**Question ouverte** : qu'est-ce qui t'agace, te ralentit, ou te fait contourner ?

> Le fait de que la phase de découverte ne soit pas assez poussée pour être bien certain du cadrage à 100% avec une couverture des besoins et de la cohérence très exhaustive.
> ____________________________________________________________________________

### 7.3 Pattern de contournement probable
**Question ouverte** : par quoi remplaces-tu cette phase en pratique ?

> Par de l'écriture de specs, mais sincèrement cette phase est indispensable en toutes circonstances pour la bonne réussite de tout projet.
> ____________________________________________________________________________

### 7.4 Valeur ajoutée perçue
**Question ouverte** : ce que la phase apporte d'irremplaçable (le cas échéant)

> Un cadragre du projet très exhaustif et détaillé au maximum.
> ____________________________________________________________________________

### 7.5 Dette d'orchestration
**Question ouverte** : y a-t-il des "TODO", "FIXME", "à améliorer" qui croupissent ?

> Je ne sais pas mais si après analyse tu as des suggestions à me faire à ce sujet, n'hésite pas.
> ____________________________________________________________________________

### 7.6 Verdict
- [x] 🟡 À ajuster (friction 7.2 "couverture besoins 100% / cohérence exhaustive" répondue par 7 livrables obligatoires + budget large 4k/7k/10k)

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. Token budget par défaut : 6k hard.

### 8.1 Token budget alloué
**Suggestion** : 6k (proposition strategy), voire 8k si besoin.

### 8.2 Compaction checkpoint
**Suggestions** :
- [ ] A. Tous les 5 tool calls (ANTI-ROT, déjà en place)
- [ ] B. À 70% du soft cap
- [x] C. Les deux (belt + suspenders)
- [ ] D. Aucun nécessaire en discovery (phase courte)
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
**Suggestions** (quelles phases cette phase peut consulter) :
- [ ] A. Aucune (première phase)
- [x] B. Anciens projets (cross-project memory)
- [x] C. Le L0 corpus (uniquement via tool, jamais injecté)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret pour cette phase
**Suggestions** (le plus applicable) :
- [x] A. T2 : auditeur vérifie que le charter est complet vs checklist
- [x] B. T3 : consequentialiste prédit les failles de phase 2/3 si on continue avec ce scope
- [ ] C. Aucun
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger
**6 éléments confirmés par le mainteneur (2026-06-04)** :

1. **Intention de départ** — capturée littéralement (pas reformulée)
2. **Contraintes dures** — deadline, budget, stack, compliance (timestampées)
3. **Scope in/out** — inclusions/exclusions + rationale + date
4. **Top-3 risques** — identifiés + mitigation choisie ou escalade
5. **Friction/contournement observé** — la 7.x du mainteneur = mine d'or
6. **Décisions marquantes** — choix structurants du projet

Stockés dans `.swebok_state.db` (table `udl_p0`) et consultables via Consultation Envelope (A1).

### 8.6 Verdict
- [x] 🟢 OK (section 8.7 Validation empirique 2026 excellente, 8.5 UDL comblé en v2, budget aligné spec v2)

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md` (15 findings, 8 anti-patterns, 4 failure modes Drew Breunig).

#### Findings les plus pertinents pour cette phase
- **F7** : 60% du 1er tour agent = retrieval → **pre-hydrate obligatoire** en début de phase (charger le sous-ensemble L0 pertinent du `distilled_corpus_v2/`)
- **F13** : Single-agent ≥ multi-agent à budget tokens égal (Tran & Kiela, avril 2026) → **confirme single Nexus-PM + Discovery-Orchestrator**, pas de fan-out
- **F4** : Context rot à 18/18 modèles, à TOUT incrément → ne pas charger toute la stack de référence "au cas où"

#### Anti-patterns à éviter dans cette phase
- **AP7** : Contexte "flood" pour tâches courtes — hot_context sélectif, ne JAMAIS charger le corpus entier
- **AP3** : Rejouer le transcript complet à chaque wakeup — passer un digest, pas le transcript

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : une hypothèse contaminée qui propage dans le charter ?
- [x] **Distraction** : trop d'exploration qui éloigne du problème initial ?
- [x] **Confusion** : trop d'informations collectées sans priorisation ?
- [x] **Clash** : sources contradictoires dans l'exploration qui bloquent la décision ?

#### Recommandation budget (mise à jour 2026)
- **Base 4k / Soft 7k / Hard 10k** (4 agents en séquentiel strict, pre-hydrate L0 partiel, ANTI-ROT trigger à 60% du soft cap = 4.2k tokens, compaction checkpoint toutes les 5 actions)
- ⚠️ **Révision 2026-06-04** : budget doublé vs recommandation initiale. Justification : mainteneur assume coût 4 agents pour complétude (4 agents séquentiels = pas de fan-out, donc pas ×15 tokens ; surcoût = re-chargement contexte). Cap 35 min justifié par F6 (failure rate ×4 au-delà).

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 0 |
| New Books achetés (§19) | 8 |
| Standards NIST/OWASP (§13) | 3 |
| Open-access téléchargés | 0 |
| **TOTAL corpus-aligned local** | **11** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~15 livres
- **Disponible localement** : 8 corpus-aligned
- **Couverture effective** : **53%** █████░░░░░

### Lacunes (§20)

- **9** livres manquants critiques pour cette phase
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

## Liste d'actions
**🔴 P1 — bloquants (fermés le 2026-06-04 par la spec v2)** :
1. ✅ Section 5.5 comblée (5 questions utilisateur)
2. ✅ Section 8.5 comblée (6 éléments UDL)
3. ✅ Verdicts tranchés (sections 1-8 + global)
4. ✅ Spec v2 réécrite (`specs/workflows/by-phase/phase-0-discovery.md`)
5. ✅ Budget P0 mis à jour dans strategy (4k/7k/10k)

**🟡 P2 — qualité (fermés par la spec v2)** :
6. ✅ Officialiser `problem-statement.md` et `success-criteria.md` dans la spec
7. ✅ Réduire spec P0 à 4 agents en séquentiel strict
8. ✅ Aligner scope cas limites 6.3 sur cible universelle

**🟢 P3 — nice-to-have (fermés le 2026-06-04)** :
9. ✅ Audit systématique des 4 failure modes Drew Breunig dans la spec → section "Audit des 4 failure modes Drew Breunig" ajoutée à la spec, 4/4 modes couverts par 4 mécanismes chacun
10. ✅ Token counter live dans le budget P0 (E1 strategy) → `pre-tool-use/token-counter.sh` créé (76 lignes), enregistré dans `settings.json`, testé OK (soft cap warn, 85% warn, hard cap block)

## Notes libres
> Phase 0 Discovery = v2 validée 2026-06-04. 20 décisions tranchées (cf. spec v2).
> 8 actions P1+P2 fermées par la spec v2. 2 actions P3 restantes (failure modes audit, token counter).
> Verdict global 🟡 (à ajuster, ajustements dans la spec v2).
> Couverture universelle (from-scratch, maintenance, interne, externe, solo, équipe).
> Budget 4k/7k/10k tokens, cap 35 min, 4 agents en séquentiel, 7 livrables obligatoires.
> Prochaine phase d'audit suggérée : P2 (Requirements) ou P3 (Design), selon ce qui te préoccupe le plus.