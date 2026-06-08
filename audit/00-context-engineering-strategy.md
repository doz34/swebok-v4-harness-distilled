# Stratégie Context Engineering — SWEBOK v4 Harness

> **Statut** : draft v0.1 — 2026-06-04
> **Préparé par** : discovery-orchestrator
> **Sources** : synthèse interne basée sur l'état de l'art 2025-2026 (Anthropic Context Engineering guide, OpenAI Agents SDK, Google ADK, RAG papers, hierarchical memory research). *Note : WebSearch étant indisponible côté API au moment de la rédaction, les références sont issues du corpus de connaissance général, pas d'une recherche temps-réel.*

---

## 1. Pourquoi c'est critique pour ce projet

Le SWEBOK v4 Harness a **trois propriétés structurelles** qui rendent le context engineering non-négociable :

1. **Multi-agent par design** — plusieurs agents Nexus-*, un orchestrateur, un adversarial gate avec Red+Blue+Judge+Council(×4 reviewers). Chaque agent = un contexte.
2. **Phase-séquentiel sur projet long** — un projet passe par **10 phases** (modèle canonique 2026-06-05, 1-par-1 SWEBOK v4 KAs). Chaque phase peut accumuler des artefacts volumineux (specs, designs, code, tests, logs d'incidents).
3. **Audit chain exhaustive** — chaque décision est loggée. Le replay = un volume potentiellement infini.

**Conséquences sans stratégie** :
- 💸 Coût token qui explose (le test rapide devient une facture à 4 chiffres)
- 🧠 Dégradation LLM (lost-in-the-middle, attention dilution, hallucinations)
- 🐌 Latence croissante (chaque tour = compilation d'un contexte de plus en plus gros)
- 🔁 Biais de récence (le LLM oublie les décisions du début de la phase)

---

## 2. Les 4 lois du context engineering (synthèse)

1. **Ne mets dans le contexte que ce qui va être utilisé** — RAG et just-in-time retrieval > stuffing
2. **Compresse tôt, décompresse tard** — un checkpoint de compaction à 70% du budget est plus efficace qu'un résume d'urgence à 95%
3. **Isole les contextes adversariaux** — T1 (producteur/casseur), T2 (spec-compliance), T3 (conséquentialiste) doivent avoir des contextes disjoints sinon l'attaque perd son sens
4. **Le contexte est une ressource à durée de vie limitée** — traiter chaque fenêtre comme précieuse, pas comme un disque dur gratuit

---

## 3. Architecture en 4 couches (L0 → L3)

```
┌────────────────────────────────────────────────────────────┐
│ L0 — Long-term corpus (offline, jamais dans le contexte)  │
│   • 227 items distilled (principles, antipatterns, etc.)  │
│   • 145k concepts corpus_v2                              │
│   • Accès : tool call uniquement                          │
├────────────────────────────────────────────────────────────┤
│ L1 — Phase outputs cache (structuré, requêtable)          │
│   • Chaque phase écrit dans un format standardisé         │
│   • Lecture cross-phase = query structurée, slice         │
│   • Pas de "lis tout P3" → "lis-moi juste les contrats"  │
├────────────────────────────────────────────────────────────┤
│ L2 — Phase working memory (volatile, token-budgeted)      │
│   • Le contexte de la phase active                       │
│   • Auto-summarized à chaque step boundary                │
│   • Compaction checkpoint à 70% du soft cap              │
├────────────────────────────────────────────────────────────┤
│ L3 — Immediate context (ce que le LLM "voit" maintenant)  │
│   • Tâche courante (1-2 phrases)                         │
│   • Slice pertinent de L2                                 │
│   • Tool results (post-compression)                       │
│   • Dernier message utilisateur                          │
└────────────────────────────────────────────────────────────┘
```

**Application directe au projet** :
- L0 existe déjà (`distilled/`, `distilled_corpus_v2/`) — il faut s'assurer qu'il n'est **jamais** injecté en bloc, uniquement via tool calls
- L1 est partiellement en place (`specs/workflows/by-phase/`, `context/project-state.md`) — il faut standardiser le format de sortie de chaque phase
- L2 est à formaliser (working memory par phase, avec budget)
- L3 est le seul contexte "live" du LLM

---

## 4. Techniques spécifiques à implémenter

### 4.1 Le Compaction Checkpoint (CC)

À chaque N tool calls (N=5 actuellement via ANTI-ROT), un checkpoint de compaction :
- Résume ce qui s'est passé depuis le dernier CC
- Drop les résultats de tools volumineux (garder la décision, pas la donnée brute)
- Garde un pointeur vers la donnée si elle est re-nécessaire
- Token counter + warning à 70/85/95% du budget

### 4.2 Le Consultation Envelope (A1)

Quand la phase X a besoin de la phase Y :
```
PHASE_X → CONSULTER(phase=Y, query="contrats d'interface REST", 
                    scope="interfaces/contracts", format="summary")
                ↓
PHASE_Y_CACHE → SCOPE_FILTER → RESPONSE_SLICE
                ↓
PHASE_X reçoit UNIQUEMENT la slice demandée
```

**Clé** : le contexte de X ne contient jamais la totalité de Y. X reçoit un objet structuré minimal.

### 4.3 Le User Decision Ledger (UDL)

Chaque décision utilisateur est loggée avec :
- Timestamp
- Phase + step en cours
- Snapshot du contexte (token count, top-3 éléments)
- Options présentées (avec rationale)
- Décision prise
- Reversibility flag
- Impact prédit (court terme)

Ce ledger est :
- une source de contexte future (le LLM peut le consulter)
- une source d'audit (replay des décisions)
- une source d'amélioration (analyse des patterns de décision)

### 4.4 Le Hot Path Optimization (HPO)

Pour les micro-tâches (typo, config tweak, comment update) :
- Skip full pre-tool-use phase check (utiliser --lite)
- Token budget = 2k pour toute la tâche
- Pas d'adversarial gate sauf demande explicite
- Auto-compaction à chaque tool call

Le `--lite` flag existe déjà dans `auto-verify.sh`. Il faut l'étendre systématiquement.

### 4.5 L'Adversarial Context Isolation (ACI)

Pour T1, T2, T3 :
- **T1 (producteur vs casseur)** : le casseur reçoit l'artefact + la spec. Il ne voit pas le prompt système du producteur.
- **T2 (spec-compliance)** : l'auditeur reçoit UNIQUEMENT la spec et l'artefact. Il ne voit pas les délibérations T1.
- **T3 (conséquentialiste)** : l'agent aval reçoit les contrats d'interface de P+1, P+2, pas leur implémentation. Il prédit les ruptures.

**Clé** : chaque rôle adversarial a un contexte distinct, sinon les "adversaires" se laissent influencer par le contexte partagé.

### 4.6 Le Decision Threshold Mechanism (DTM) — modèle B

Implémentation du seuil utilisateur :
- **Décision à fort impact / irréversible** : query obligatoire, options classées, timeout 5min, après = décision par défaut
- **Décision réversible à faible coût** : notification a posteriori (summary log), validation à la demande
- **Décision triviale** : silencieuse, pas de log

Le système doit classifier la décision au moment où elle se présente (avant de demander).

---

## 5. Token budgets par phase (proposition)

> **Mise à jour 2026-06-05** : Fix structurel. 10 phases (vs 9 avant). P1 ajouté (Concept/Feasibility). P3 et P4 créés par split. P5-P10 = renommage cascade P4-P9. Budgets mis à jour.

| Phase | Base | Soft cap (CC) | Hard cap (abort) | Justification |
|-------|------|---------------|------------------|---------------|
| phase-0 Discovery | 4k | 7k | 10k | Cadrage exhaustif validé 2026-06-04, aligné phase Design (spec v2) |
| **phase-1 Concept/Feasibility** | **3k** | **5k** | **8k** | **Filtre go/no-go rapide. Phase la plus serrée du projet.** |
| phase-2 Requirements | 4k | 7k | 10k | Spec SRS IEEE 830 validée 2026-06-05 (spec v2), 4 agents séquentiel + Nexus-Critic + Council NFR, séquentiel strict donc pas ×15 |
| **phase-3 Architecture** | **5k** | **8k** | **15k** | **Multi-agent justifié (F13) : 3-5 sub-agents parallèles + Nexus-Critic T1+T2+T3 obligatoire. ADRs obligatoires, threat model STRIDE si security-sensitive. Hard cap 15k justifié par coût additionnel Nexus-Critic T1+T2+T3 (~4.5k).** |
| phase-4 Design | 5k | 8k | 15k | Design détaillé (consomme ADRs P3, consomme ADRs = pas de re-décision archi). 3-5 agents max + Nexus-Critic T1+T2+T3 obligatoire (3 invocations systématiques, comme P3 v2). Format contracts différencié aligné P3 (md+json modules internes, +OpenAPI 3.0 API REST, +AsyncAPI 3.0 events option). Matrice de conformité aux ADRs P3 obligatoire (XG-4.7). |
| phase-5 Implementation | 5k | 10k | 15k | Code, intégration, CI/CD. Budget large (activité 1 du projet). |
| **phase-6 Testing** | **5k** | **8k** | **15k** | **Suites, défauts, rapports + NFR perf+security + mutation testing. Multi-agent justifié (F13) : 4 niveaux de test + 2 transverses (perf, security) + mutation en parallèle + Nexus-Critic T1+T2+T3 obligatoire (3 invocations systématiques, comme P3/P4/P5, décision mainteneur 2026-06-07). Hard cap 15k justifié par Nexus-Critic (~4.5k additionnel). P6 = 2e phase la plus coûteuse en effort (20-40% projet) après P5 Implementation. Bascule coverage/mutation de P5 vers P6 (P5 = unit seul, P6 = coverage + mutation + reste).** |
| **phase-7 Deployment** | **5k** | **8k** | **15k** | **Multi-agent justifié (F13) : 5 sub-agents en parallèle (Nexus-DevOps-Lead lead + Nexus-DevOps + Nexus-Backend + Nexus-Frontend + Nexus-SM) + Nexus-Critic T1 casseur plan + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 OBLIGATOIRE (3 invocations systématiques, comme P3/P4/P5/P6, décision mainteneur 2026-06-07). Hard cap 15k justifié par Nexus-Critic T1+T2+T3 (~4.5k additionnel). Démarcation P6↔P7 explicite (P6=code-va-passer-en-prod, P7=prod-tourne-après-deploy). Stratégie rollout défaut = big-bang (DTM par projet). Hotfix = pas de bypass. 7+4 livrables (11). XG-7.1-XG-7.10 (10 exit criteria).** |
| phase-8 Operations | 2k (courant) / 5k (P0-P1) | 4k (courant) / 8k (P0-P1) | 6k (courant) / 15k (P0-P1) | **Adaptatif par sévérité incident** (décision 2026-06-07) : monitoring courant 1k/2k/3k (single Nexus-SM), incident standard P2/P3 2k/4k/6k (single + Nexus-Critic T2), incident critique P0/P1 5k/8k/15k (multi-agent + Nexus-Critic T1+T2+T3 + Council post-incident, cohérent P3-P7). Phase vivante (longue durée), pas projet. Compaction par incident (AP5). |
| **phase-9 Maintenance** | **1k (hotfix) / 3k (standard) / 5k (structurant)** | **2k (hotfix) / 5k (standard) / 8k (structurant)** | **3k (hotfix) / 8k (standard) / 15k (structurant)** | **Adaptatif 3-niveaux par criticité (symétrie P8)** : hotfix/typo 1k/2k/3k --lite single sans Critic ; corrective/adaptive/preventive standard 3k/5k/8k single + Nexus-Critic T1+T2+T3 ; structurant/perfective lourde 5k/8k/15k multi + Nexus-Critic T1+T2+T3 + Council structurante. Nexus-Critic T1 casseur patch + T2 conformité DDS P4 + ADRs P3 + NFR P2 + T3 prédiction aval P10 OBLIGATOIRE (3 invocations systématiques sauf mode --lite, cohérence P3-P7). Démarcation P8↔P9 (Run vs Change) et P9↔P10 (prolonger vs préparer la mort) explicites. Q1-Q4 user 5.5 (type maintenance + criticité + CAB + EOL). |
| **phase-10 Retirement** | **1k (simple) / 3k (RGPD) / 5k (regulated)** | **2k (simple) / 5k (RGPD) / 8k (regulated)** | **3k (simple) / 8k (RGPD) / 15k (regulated)** | **Adaptatif 3-niveaux par criticité conformité (symétrie P8/P9)** : archivage simple/donnée standard = single + T2 (1k/2k/3k, pas de Council) ; RGPD/standard métier = single + T1 casseur + T2 (3k/5k/8k) ; Finance/Santé/Défense = multi + T1+T2+T3 + Council de clôture obligatoire (5k/8k/15k). P10 = dernière phase du cycle de vie (one-shot, pas projet). Nexus-Critic adaptatif (T2 seul / T1+T2 / T1+T2+T3+Council). Hard cap 15k justifié par coût additionnel Council Finance/Santé/Défense (~2k). Démarcation P9↔P10 (prolonger vs préparer la mort, tranchée vague 1 P9) ET P10↔P0 (fin de vie ancien vs début nouveau système, tranchée vague 1 P10) explicites. Council de clôture conditionnel par criticité (signature Nexus-DevOps-Lead simple / CISO+Legal RGPD / Council complet regulated). 9+3 livrables (eol-decision-memo + archive-procedure + data-migration-plan + compliance-closure-report + ownership-transfer + stakeholder-notification + final-archive-snapshot + post-retirement-monitoring-stop + post-retirement-review + legal/compliance sign-off + communication-sent-log). UDL 7. Réversibilité hybride par criticité (30j/90j/180j+ read-only). |

**Note** : ces chiffres sont des ordres de grandeur. Le tuning doit être empirique, basé sur la mesure réelle.

---

## 6. Failure modes à prévenir

| Mode | Description | Détection | Mitigation |
|------|-------------|-----------|------------|
| **Context drift** | Accumulation silencieuse de bruit | CC à 70% du soft cap | Compaction forcée |
| **Decision amnesia** | Oubli des choix utilisateur antérieurs | Hash UDL vs state attendu | UDL injecté en L3 si pertinent |
| **Cross-phase contamination** | Phase X lit ce que Y a écrit en secret | Manifeste de permissions | Consultation Envelope strict |
| **Adversarial leakage** | T1/T2/T3 partagent trop de contexte | Audit des contextes injectés par rôle | ACI strict |
| **Token explosion** | Coût qui dérape sans warning | Token counter live | CC + abort au hard cap |
| **Recency bias** | Décisions du début de phase oubliées | Dissonance entre UDL et comportement | Rappel UDL en début de chaque step |
| **Lost-in-the-middle** | LLM "perd" le milieu du contexte | Métriques de recall (T2 échoue sur des éléments du milieu) | Structure pyramidale (décisions en haut, bas, jamais au milieu) |

---

## 7. Anti-patterns à NE PAS faire

- ❌ **Stuffing du corpus** : charger les 227 items "au cas où" → mort du contexte
- ❌ **Re-lecture intégrale** : relire toute la sortie d'une phase à chaque step → gaspillage
- ❌ **Summarisation trop agressive** : résumer trop tôt = perte de précision critique
- ❌ **Summarisation trop tardive** : résumer à 95% = coût déjà explosé
- ❌ **Contexte partagé T1/T2/T3** : tue la dynamique adversariale
- ❌ **Contexte global du projet** dans chaque phase : viole A1
- ❌ **Logs d'audit dans le contexte** : le HMAC chain est rejouable, pas besoin d'être en L3
- ❌ **Décisions sans timestamp** : impossible de trancher en cas d'ambiguïté

---

## 8. Roadmap d'implémentation

| Étape | Quoi | Quand | Effort | Impact |
|-------|------|-------|--------|--------|
| E1 | Token counter live dans chaque phase spec | Sprint 1 | XS | S (visibilité) |
| E2 | Compaction checkpoint à 70% du soft cap | Sprint 1 | S | L (économie) |
| E3 | Format standardisé L1 (chaque phase écrit dans le même schéma) | Sprint 1 | M | XL (interop) |
| E4 | Consultation Envelope (A1) implémenté | Sprint 2 | L | XL (isolation) |
| E5 | User Decision Ledger (UDL) | Sprint 2 | M | L (audit + traçabilité) |
| E6 | Decision Threshold Mechanism (DTM) | Sprint 2 | S | L (UX) |
| E7 | Adversarial Context Isolation (ACI) | Sprint 3 | M | L (qualité des gates) |
| E8 | Dashboards par phase (tokens, décisions, CC) | Sprint 3 | M | M (observabilité) |
| E9 | Hot Path Optimization étendu (--lite partout) | Sprint 3 | S | M (micro-tâches) |
| E10 | Memory decay (résumer l'épisode précédent à chaque début de phase) | Sprint 4 | M | M (long-term projects) |

---

## 9. Questions ouvertes (à arbitrer par le mainteneur)

**🆕 Tranchées par l'audit P3 (2026-06-06)** :
- ✅ **Token budget P3** : 5k/8k/15k (vs 5k/8k/12k en v1), justifié par Nexus-Critic T1+T2+T3 obligatoire. P3 = 2e phase la plus large (ex-aequo avec P4 et P5).
- ✅ **Nexus-Critic en P3** : T1 casseur + T2 conformité + T3 aval **TOUS OBLIGATOIRES** (3 invocations systématiques, ~4.5k tokens additionnels).
- ✅ **Format contracts en P3** : différencié par type — md+json pour modules internes, md+json+OpenAPI pour API REST, md+json+AsyncAPI pour événements async (option).
- ✅ **Token budget P4** : 5k/8k/15k, justifié par Nexus-Critic T1+T2+T3 obligatoire. P4 = 3e phase la plus large.
- ✅ **Token budget P5** : 5k/10k/15k (le plus large), justifié par Nexus-Critic T1+T2+T3 obligatoire + effort-report.md (livrable formel, T-shirt vs réel). P5 = phase la plus chère en tokens (15× multi-agent vs chat).
- ✅ **Nexus-Critic en P4** : T1 casseur + T2 conformité NFR P2/ADRs P3 + T3 aval **TOUS OBLIGATOIRES** (3 invocations systématiques, ~4.5k tokens additionnels).
- ✅ **Nexus-Critic en P5** : T1 casseur code + T2 conformité DDS P4/ADRs P3 + T3 prédiction aval P6 **TOUS OBLIGATOIRES** (3 invocations systématiques, ~4.5k tokens additionnels).

**🆕 Tranchées par l'audit P7 (2026-06-07)** :
- ✅ **Token budget P7** : 3k/5k/8k → **5k/8k/15k** (cohérence P3/P4/P5/P6, justifié par Nexus-Critic T1+T2+T3 obligatoire, ~4.5k additionnel). P7 = 5e phase la plus large.
- ✅ **Nexus-Critic en P7** : T1 casseur plan déploiement + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 **TOUS OBLIGATOIRES** (3 invocations systématiques, ~4.5k tokens additionnels). **P7 passe de "Single-agent justifié" à "Multi justifié"** (cohérence P3-P6 prime sur économie tokens, décision mainteneur 2026-06-07).
- ✅ **Démarcation P6↔P7 explicite** (décision 2026-06-07) : P6 = "code va-t-il passer en prod sans casser" (staging iso-prod + tests + go/no-go) ; P7 = "prod tourne-t-elle correctement après le deploy" (release + monitoring + handoff). Symétrique à démarcation P5↔P6.
- ✅ **Stratégie rollout par défaut** : big-bang (DTM par projet pour canary/blue-green). Hotfix = pas de bypass (process complet obligatoire, escalade mainteneur si urgence vitale).
- ✅ **7+4 livrables** (vs 7 v2-renum) : 7 standard + 4 ajouts (changelog + runbook + monitoring dashboard + audit trail). 11 exit criteria XG-7.1-XG-7.10.

**🆕 Tranchées par l'audit P8 (2026-06-07)** :
- ✅ **Token budget P8** : **adaptatif par sévérité incident** (vs 2k/4k/6k uniforme v2-renum). Monitoring courant 1k/2k/3k, incident standard P2/P3 2k/4k/6k, incident critique P0/P1 5k/8k/15k. Phase vivante (longue durée, pas projet), spécificité unique.
- ✅ **Nexus-Critic en P8** : **adaptatif par sévérité incident**. Monitoring courant = aucun Nexus-Critic (P8 = exécution, pas création, gaspillage tokens). Incident standard P2/P3 = T2 seul (spec-compliance vs runbook P7, 1 invocation). Incident critique P0/P1 = T1+T2+T3 obligatoires (3 invocations systématiques comme P3/P4/P5/P6/P7) + Council post-incident (CISO + DevOps-Lead + SM).
- ✅ **Démarcation P7↔P8 ET P8↔P9 explicites** (Setup vs Run vs Change) : P7 = release + monitoring SETUP avant deploy ; P8 = monitoring CONTINU post-release + alertes + escalade + capacity + post-mortems (sans modification code) ; P9 = CHANGEMENT de code planifié (corrective/adaptive/perfective/preventive). Cas limites tranchés : "calibrer un seuil d'alerte" = P8 (config monitoring), "configurer alerts initiales" = P7 (setup), "modifier le code pour réduire les alertes" = P9 (fix).
- ✅ **4 décisions opérationnelles user (B threshold)** : Q1 calibration seuils SLO/SLI, Q2 priorisation incidents P0-P3 + escalade, Q3 profondeur post-mortem (1-page vs full RCA), Q4 acceptation incidents deferred (acceptable risk vs escalade P9).
- ✅ **P8 passe de "Single"** (suggestion initiale §12.6) **à "Adaptatif par sévérité"** : Single par défaut (monitoring courant + incident standard), Multi justifié pour incidents critiques P0/P1. Spécificité P8 unique (aucune autre phase n'a cette structure adaptative).

**🆕 Tranchées par l'audit P10 (2026-06-07)** :
- ✅ **Token budget P10** : **adaptatif 3-niveaux par criticité conformité** (vs 2k/3k/5k uniforme v2-renum). Archivage simple/donnée standard 1k/2k/3k, RGPD/standard métier 3k/5k/8k, Finance/Santé/Défense/donnée sensible 5k/8k/15k. Symétrie P8 (sévérité) et P9 (criticité). P10 = archivage séquentiel, pas création archi, donc 3-niveaux adapté à la criticité conformité.
- ✅ **Nexus-Critic en P10** : **ADAPTATIF par criticité conformité** (vs T1+T2+T3 obligatoire P3-P7 ou adaptatif P8/P9). Archivage simple = T2 seul (1 invocation ~1.5k, vérification conformité procédure + réversibilité). RGPD/standard = T1 casseur archivage (Data Loss Hunter) + T2 conformité réglementaire (2 invocations ~3k). Finance/Santé/Défense = T1+T2+T3 (3 invocations ~4.5k) + Council de clôture obligatoire (CISO+Legal+PM+DevOps-Lead, examen 1h, ~2k). Coût additionnel jusqu'à 6.5k sur mode regulated, justifié par hard cap 15k.
- ✅ **Démarcation P10↔P0 explicite** (Question centrale, symétrie P9) : P10 = fin de vie d'un système EXISTANT (archivage, conformité, transfert ownership, notification). P0 = début d'un NOUVEAU système (exploration, intake, JTBD, cadrage). Cas limites tranchés : "réutilisation de composants archivés pour un nouveau système" = P0 du nouveau (pas P10, on parle du nouveau). "Lessons learned d'un EOL" = P10 (post-retirement review, attaché au système archivé). "Re-démarrage d'un système archivé (annulation EOL)" = P10 (re-archivage, traçabilité décisions EOL). Triple démarcation P8↔P9↔P10 (Run vs Change vs Retire) + P10↔P0 ferment toutes les frontières contestées.
- ✅ **Council de clôture conditionnel par criticité** (vs obligatoire pour Finance/Santé/Défense) : Archivage simple = signature Nexus-DevOps-Lead suffit. RGPD/standard = signature Nexus-DevOps-Lead + CISO + Legal. Finance/Santé/Défense = Council CISO+Legal+PM+DevOps-Lead obligatoire (examen 1h, signature collective avant `PROJECT_RETIRED`). Symétrie P8 (Council post-incident P0/P1) et P9 (Council structurante).
- ✅ **Réversibilité hybride par criticité** : Archivage simple = 30j read-only, RGPD/standard = 90j read-only (cohérent P9 hotfix window), Finance/Santé/Défense = 180j+ read-only. Restaurable sur demande stakeholder, pas automatique. Refus catégorique 6 : "Pas de suppression définitive avant période de réversibilité (Q3 user 5.5)".
- ✅ **4 décisions opérationnelles user (B threshold)** : Q1 type retirement (archivage simple / RGPD / Finance-Santé-Défense / transfert ownership), Q2 criticité conformité (simple / standard / élevée), Q3 réversibilité (30j / 90j / 180j+ / indéfini), Q4 lien P0 (aucun / parallèle / lessons learned / après). Symétrie P8 (4 décisions) et P9 (4 décisions).
- ✅ **P10 passe de "Single"** (suggestion initiale §12.6) **à "Adaptatif par criticité conformité (3-niveaux, symétrie P8/P9)"** : single + T2 archivage simple, single + T1+T2 RGPD, multi + T1+T2+T3 + Council Finance/Santé/Défense. Démarcation P9↔P10 (prolonger vs préparer la mort, déjà tranchée vague 1 P9) ET P10↔P0 (fin ancien vs début nouveau) explicites, ferment toutes les frontières de phase contestées du projet.

**🔴 Encore ouvertes (à arbitrer)** :
1. **Format L1** : JSON structuré, Markdown structuré, ou les deux ? (impacte tous les consumers)
2. **Token budgets P0-P10** : les chiffres sont-ils réalistes après mesure sur projets réels ? (à ajuster empiriquement, cible v2.1)
3. **T3 par défaut sur P6 Testing** : ✅ **TRANCHÉE pour P3, P4, P5, P6** — T1+T2+T3 **OBLIGATOIRE** (3 invocations systématiques, décision mainteneur 2026-06-07). P6 = multi-agent justifié (4 niveaux + 2 transverses + mutation), Nexus-Critic obligatoire comme P3/P4/P5. Hard cap 15k justifié sur les 4 phases multi-agent.
4. **DTM timeout** : 5min acceptable ? Plus ? Avec notif progressive ?
5. **UDL privacy** : qui peut voir le ledger ? (mainteneur only ? phase courante ? audit post-mortem ?)
6. **--lite pour P5-P7** : où s'arrête le hot path ? Quelle complexité déclenche le full check ?
7. **🆕 2026-06-06** : **Avis expert externe pour fermer la section 7 des grilles** : qui ? (architecte senior indépendant ? consultancy ? ancien collègue ?). Coût estimé ? Timing (avant v2.0 ? avant v1.6.0 ?).

---

## 10. Métriques de succès (à mesurer)

- **Coût moyen par projet complet** (P0→P9) — doit chuter de X% après implémentation
- **% de CC déclenchés à 70%** (signe d'un tuning correct)
- **% de hard cap atteint** (cible : < 2% des phases)
- **% de décisions user-répétées** (signe que le contexte oublie)
- **Taux de faux positifs des gates** (T2 échoue à tort) — signe de leakage adversarial
- **Latence moyenne par phase** (cible : ne pas augmenter)

---

## 12. Validation empirique 2026 (recherche complémentaire)

> Section ajoutée le 2026-06-04 suite à la recherche `01-context-engineering-research-2026.md` (15 requêtes search, 5 URLs fetched, 30+ sources primaires, 15 findings, 15 benchmarks, 8 anti-patterns).

### 12.1 Findings clés validant ou affinant la stratégie

| # | Finding | Source | Implication stratégie |
|---|---------|--------|------------------------|
| **F1** | 80% de la variance perf = token usage (BrowseComp) | Anthropic multi-agent research (2025-06) | Le budget phase est un **proxy de qualité**, pas qu'un cost-control |
| **F2** | Multi-agent = 15× tokens chat ; single-agent = 4× | idem | **Justifier chaque fan-out** Nexus comme "high-value" |
| **F3** | Subagent brief doit porter 4 champs : OBJECT/FORMAT/TOOLS/BOUND | idem | Le DSL `KEY:VALUE;;KEY:VALUE` mappe naturellement — auditer chaque spawn |
| **F4** | Context rot : 18/18 modèles se dégradent à TOUT incrément | Chroma study via Morph (2026-03) | "Plus de contexte" n'est pas une solution. Gating par phase obligatoire |
| **F5** | Lost-in-the-middle = -30% accuracy en position 5-15 (sur 20 docs) | Liu et al. Stanford/TACL 2024 | **Éléments critiques en tête/queue**, jamais au milieu |
| **F6** | Mur à 35 min : failure rate × 4 quand durée × 2 | Morph (2026-03) | Budget temps par phase ; checkpoint obligatoire au-delà |
| **F7** | 60% du 1er tour agent = retrieval (Cognition/Devin) | Morph (2026-03) | **Pre-hydrate obligatoire** en début de phase |
| **F8** | Compaction Claude Code = 95% de la fenêtre (référence) | Claude Cookbook | Notre ANTI-ROT toutes les 5 calls = trop agressif ou mal mesuré. Viser 60-70% en tokens |
| **F9** | 50% économie : forward worker→user (vs swarm supervisor) | LangChain 2025 via FlowHunt | Court-circuiter Hyperagent quand il ne fait que relayer |
| **F10** | Subagent output → filesystem (artefact persistant), pas transcript | Anthropic Appendix | `.swebok_state.db` = ce filesystem. Subagent écrit, lead reçoit un pointeur |
| **F11** | Prompt caching : stable prefix en tête uniquement | Anthropic docs | Si appel Claude API : system + phase_rules + DSL schema en tête, jamais de tool result dynamique avant |
| **F12** | RAG embedding = plafond mathématique pour le code (DeepMind) | Morph (2026-03) | Préférer grep/AST/keyword + rerank LLM sur `distilled_corpus_v2/` |
| **F13** | Single-agent ≥ multi-agent à budget tokens égal (Tran & Kiela, avril 2026) | arXiv 2604.02460 via FlowHunt | Phases P0/P2/P6 = single Nexus suffit. Multi-agent justifié si (a) read-heavy parallèle ou (b) disjoint tools |
| **F14** | Adversarial Red→Blue→Judge = pattern production | Farzulla 2025 | Valide `adversarial-gate.sh` Red/Blue/Judge + Council Bridge |
| **F15** | Tamper-evident log = HMAC chain | Cossack Labs 2025 | Étendre HMAC à TOUS les events DSL, pas seulement transitions de phase |

### 12.2 4 failure modes de Drew Breunig (NOUVEAU)

LangChain blog (2025-07) cite Drew Breunig qui identifie 4 failure modes systémiques :

1. **Poisoning** : hallucination ou erreur qui contamine tout le raisonnement aval
2. **Distraction** : le contexte surchargé fait diverger l'attention du LLM
3. **Confusion** : informations superflues qui diluent les signaux importants
4. **Clash** : informations contradictoires dans le contexte qui bloquent la décision

**Implication SWEBOK v4** : chaque grille de phase doit auditer ces 4 modes dans sa section 6 (Bornes & modes d'échec). Suggestion : ajouter une sous-section "6.6 Failure modes Drew Breunig" à chaque grille.

### 12.3 Benchmarks opérationnels intégrés

| Métrique | Valeur | Application budget SWEBOK |
|----------|--------|------------------------------|
| Single-agent tokens / chat | 4× | Baseline P0, P2, P6 : un seul Nexus |
| Multi-agent tokens / chat | 15× | P3, P4, P5 : budget × 15, justifier le fan-out |
| Multi-agent gain (recherche) | +90.2% | Valide Hyperagent+Nexus sur recherche/archi, **pas** sur code |
| 3-5 subagents parallèles | -90% durée | Budget durée phase = durée_single / 3-5 |
| Lost-in-the-middle (5-15/20) | -30% accuracy | Structure pyramidale obligatoire |
| Mur des 35 min | ×4 failure | Checkpoint obligatoire au-delà |
| 1er tour = 60% retrieval | — | Pre-hydrate = gain × 2.5 sur 1er tour |
| Variance tokens entre runs | × 10 | Mesurer pour détecter drift |
| Compaction trigger | 60-70% (vs 95% Claude Code) | Rejustifier ANTI-ROT |
| Subagent retour au lead | 1-2K tokens max | Pas de dump, juste un pointeur |

### 12.4 Anti-patterns confirmés (8) avec mitigation SWEBOK

- **AP1** : 50 subagents pour une question simple → règles d'effort-scaling dans `phase_rules.json` (1 agent / 3-10 calls, 2-4 subagents comparaison, 10+ recherche complexe)
- **AP2** : Brief vague "research X" → brief structuré OBJECT/FORMAT/TOOLS/BOUND obligatoire
- **AP3** : Rejouer le transcript complet à chaque wakeup → digest structuré via modèle cheap, forward direct
- **AP4** : Peer-to-peer entre subagents → tout passe par Hyperagent ou `.swebok_state.db`, pas de canal Nexus↔Nexus
- **AP5** : Compaction à 95% = trop tard → trigger à 60-70% du budget phase
- **AP6** : Tool result clearing absent → vider les tool results après consommation
- **AP7** : Contexte "flood" pour tâches courtes → hot_context sélectif, ne JAMAIS charger `distilled_corpus_v2/` entier
- **AP8** : Confondre taille fenêtre et capacité attention → mesurer qualité par outcome (gate), pas par volume chargé

### 12.5 Roadmap mise à jour (12 recommandations priorisées)

**P1 — Implémenter immédiatement (haute valeur, effort S/M)** :
1. Reformuler ANTI-ROT en seuil relatif (tokens ou % budget phase), pas compteur calls. Trigger cible 60-70%.
2. Documenter "subagent contract" (OBJECT/FORMAT/TOOLS/BOUND) dans `phase_rules.json`. Auditer Nexus existants.
3. Placer éléments critiques en tête/queue du contexte Nexus (gate, contraintes, findings adversariaux).
4. **🆕 2026-06-06** : **Étendre la méthode d'audit 4 failure modes Drew Breunig à P4-P10** (déplacée depuis grille P3 action P3-10). Référence : P0 v2 + P2 v2 + P3 v2. La méthode est déjà documentée, l'extension est mécanique.

**P2 — Implémenter au sprint prochain (haute valeur, effort M)** :
5. Budget temps par phase : 35 min cible, checkpoint obligatoire au-delà.
6. Pre-hydrate obligatoire en début de phase (charger hot_context dans `.swebok_state.db`).
7. Forward direct worker→user quand Hyperagent ne synthétise rien (~50% économie).
8. Étendre HMAC chain à tous les events DSL (pas seulement transitions).
9. **🆕 2026-06-06** : **Fermer la section 7 (utilité réelle) des grilles P1, P3, et futures P4-P10 par avis expert externe OU par 1-2 projets réels** (déplacée depuis grilles P1 et P3 actions P1-8 et P3-8). Effort : XS par phase (un projet test suffit, ou 1 avis expert par phase).

**P3 — À planifier (moyenne valeur ou effort L)** :
10. Distinguer explicitement phases "single-agent OK" (P0, P2, P6) vs "multi-agent justifié" (P3, P4, P5).
11. Préférer grep/AST/rerank à embedding search sur `distilled_corpus_v2/`.
12. Si appel Claude API : structurer payload avec cache stable prefix en tête.
13. Documenter la 4-failure-mode grid (Drew Breunig) dans chaque phase spec.
14. Préparer migration long-running (quand Anthropic publiera "Effective Harnesses for Long-Running Agents", ingérer en V2.1).

### 12.6 Phases "single-agent OK" vs "multi-agent justifié" (recommandation P3-8)

> **Mise à jour 2026-06-05** : Fix structurel. Modèle 10 phases.

| Phase | Type | Justification |
|-------|------|---------------|
| **P0 Discovery** | Single | Séquentiel, exploration, peu d'état |
| **P1 Concept/Feasibility** | Single | Filtre go/no-go rapide, 4 agents en standard (5e Nexus-DevOps si PoC infra complexe), budget serré |
| **P2 Requirements** | Single | SRS, IEEE 830, single Nexus-PM suffit (4 séquentiel + 1 Nexus-Critic + 4 Council NFR) |
| **P3 Architecture** | **Multi justifié** | 3-5 sub-agents parallèles (Arch, Sec, Backend, Frontend, DevOps) + **Nexus-Critic T1+T2+T3 obligatoire (3 invocations systématiques, ~4.5k tokens)**. Read-heavy parallèle. Hard cap 15k. |
| **P4 Design** | **Multi justifié** | 3-5 sub-agents parallèles (Arch, Backend, Frontend, DevOps, Security) + **Nexus-Critic T1+T2+T3 obligatoire (3 invocations systématiques, comme P3 v2)**. Consomme les ADRs P3 (pas de re-décision = matrice ADR → module obligatoire XG-4.7). Format contracts différencié aligné P3 (md+json modules internes, +OpenAPI 3.0 API REST, +AsyncAPI 3.0 events option). Hard cap 15k justifié par Nexus-Critic T1+T2+T3 (~4.5k additionnel). |
| **P5 Implementation** | **Multi justifié** | 3-5 sub-agents parallèles (Backend, Frontend, DevOps, Security) + **Nexus-Critic T1 casseur + T2 conformité DDS P4/ADRs P3 + T3 prédiction aval P6 OBLIGATOIRE (3 invocations systématiques, comme P3 et P4, décision mainteneur 2026-06-07)**. Consomme les DDS P4 (pas de re-décision design = matrice DDS → code obligatoire XG-5.7). Livrable `effort-report.md` comble P4 SWEBOK absente. Hard cap 15k justifié par Nexus-Critic T1+T2+T3 (~4.5k additionnel). |
| **P6 Testing** | **Multi justifié** | **4 niveaux de test (intégration, système, acceptance, régression) + 2 transverses (perf, security) + mutation en parallèle + Nexus-Critic T1 casseur tests + T2 conformité acceptance criteria P2 + T3 prédiction aval P7 OBLIGATOIRE (3 invocations systématiques, comme P3/P4/P5, décision mainteneur 2026-06-07). Consomme le code P5 + acceptance criteria P2 + NFR P2 (pas de re-décision code = escalade P5, pas de re-définition NFR = escalade P2). Bascule coverage/mutation de P5 vers P6 (P5 = unit seul). 11+1 livrables (test plan + 4 résultats par niveau + defect + TTM + closure + 3 transverses + go/no-go). Hard cap 15k justifié par Nexus-Critic T1+T2+T3 (~4.5k additionnel).** |
| **P7 Deployment** | **Multi justifié** | **5 sub-agents en parallèle (DevOps-Lead + DevOps + Backend + Frontend + SM) + Nexus-Critic T1 casseur plan + T2 conformité go/no-go P6 + NFR P2 + ADRs P3 + T3 prédiction aval P8 OBLIGATOIRE (3 invocations systématiques, comme P3/P4/P5/P6, décision mainteneur 2026-06-07). Consomme le go/no-go memo P6 + closure report + test plan validé pour amener le code de production-ready à production-running. Hard cap 15k justifié par Nexus-Critic T1+T2+T3 (~4.5k additionnel). Démarcation P6↔P7 explicite (P6=code-va-passer-en-prod, P7=prod-tourne-après-deploy). Stratégie rollout défaut = big-bang (DTM par projet).** |
| **P8 Operations** | **Adaptatif par sévérité incident** | **Monitoring courant** = single Nexus-SM (sans Critic, 1k/2k/3k). **Incident standard P2/P3** = single Nexus-SM + Nexus-Critic T2 spec-compliance vs runbook (2k/4k/6k, 1 invocation). **Incident critique P0/P1** = multi-agent (Hyperagent + SM + DevOps + Security + Backend + Frontend) + Nexus-Critic T1+T2+T3 obligatoire (3 invocations, cohérent P3-P7) + Council post-incident (CISO + DevOps-Lead + SM, 5k/8k/15k). **Spécificité P8** : phase vivante (longue durée, pas projet), budget par incident pas par session. Compaction immédiate après RCA (AP5). Démarcations P7↔P8 (Setup vs Run) et P8↔P9 (Run vs Change) explicites. 4 décisions opérationnelles user (calibration seuils, priorisation incidents, post-mortem profondeur, deferred). |
| **P9 Maintenance** | **Adaptatif par criticité (3-niveaux, symétrie P8)** | **Hotfix/typo/micro-tâche** = single --lite sans Critic (1k/2k/3k, hot path, gaspillage tokens évité). **Corrective/Adaptive/Preventive standard** = single + Nexus-Critic T1+T2+T3 obligatoire (3k/5k/8k, 3 invocations systématiques, cohérence P3-P7). **Structurant/Perfective lourde/Refactoring majeur** = multi-agent (Hyperagent + Lead + Architect + Security + QA + PM) + Nexus-Critic T1+T2+T3 obligatoire (3 invocations) + Council structurante (CISO + DevOps-Lead + Architect, examen 1h avant deploy, 5k/8k/15k cohérent P3-P7). P9 = patch + regression, pas création archi, donc budget 3-niveaux adapté à la nature de la tâche. Démarcation P8↔P9 (Run vs Change) et P9↔P10 (prolonger vs préparer la mort) explicites. 4 décisions user 5.5 (type + criticité + CAB + EOL). 11 livrables (6 standard + 5 ajouts : diff/patch + decision rationale + ADR + changelog public + post-mortem si incident). UDL 7 éléments. Spécificité P9 : consommation des CR émises par P8 + escalade vers P10 si EOL approche. |
| **P10 Retirement** | **Adaptatif par criticité conformité (3-niveaux, symétrie P8/P9)** | **Archivage simple** = single Nexus-DevOps-Lead + T2 seul (1k/2k/3k, pas de Council). **RGPD/standard** = single + T1 casseur archivage (Data Loss Hunter) + T2 conformité réglementaire (3k/5k/8k, signature CISO+Legal). **Finance/Santé/Défense** = multi + T1+T2+T3 + Council de clôture obligatoire (5k/8k/15k, signature collective CISO+Legal+PM+DevOps-Lead). **Spécificité P10** : dernière phase du cycle de vie (one-shot, pas projet, pas phase vivante). Démarcation P9↔P10 (prolonger vs préparer la mort, déjà tranchée vague 1 P9) ET P10↔P0 (fin de vie ancien vs début d'un NOUVEAU système, tranchée vague 1 P10) explicites. Compaction immédiate après `PROJECT_RETIRED` (phase one-shot). Council de clôture conditionnel par criticité (symétrie P8 Council post-incident P0/P1 et P9 Council structurante). Réversibilité hybride par criticité (30j/90j/180j+ read-only). 9+3 livrables (9 standard + legal/compliance sign-off + communication-sent-log). UDL 7 éléments P10-spécifiques. Nexus-Critic adaptatif (T2 seul / T1+T2 / T1+T2+T3+Council). 4 décisions user 5.5 (Q1 type retirement, Q2 criticité, Q3 réversibilité, Q4 lien P0). |

**Note** : "Multi-agent justifié" ne veut pas dire "toujours multi-agent". Le trigger est : (a) read-heavy parallèle ou (b) disjoint tools. Sinon, single.

### 12.7 Sources complémentaires récupérées (non couvertes par sections 1-11)

- **LangChain — Context Engineering for Agents** (2025-07-02) : taxonomie Write/Select/Compress/Isolate
- **Morph — Context Rot** (2026-03-13) : synthèse Chroma + benchmarks
- **FlowHunt — Multi-Agent AI Systems in 2026** (2026-04-28) : consensus orchestrator + isolated subagents
- **VILA-Lab — Dive into Claude Code** (arXiv 2604.14228, 2026-04) : design space des coding agents
- **Cognition Labs** : pivot single-threaded → coordinator + managed Devins (juin 2025 → mars 2026)
- **AORCHESTRA** (arXiv 2602.03786) : +16.28% sur GAIA/SWE-Bench
- **Drammeh** (arXiv 2511.15755) : narrow-domain multi-agent = 100% vs 1.7% actionable
- **Tran & Kiela** (arXiv 2604.02460, avril 2026) : single-agent ≥ multi-agent à budget tokens égal
- **Farzulla 2025** : Autonomous Red/Blue Team AI pattern
- **Cossack Labs 2025** : HMAC chain audit logs
- **Towards AI — Long Context Compaction Part 1** : STM + summarization 2-tiers
- **Emotion Machine — Three Memory Architectures** : pre-hydrate + structured note-taking + periodic eviction
- **Zylos Research — AI Agent Context Compression Strategies** (2026-02-28) : anchored iterative summarization

### 12.8 Sources non récupérées (à creuser en V2)

- **Anthropic — Effective Harnesses for Long-Running Agents** (jan 2026) : référencé mais URL non confirmé
- **Cognition Labs blogs primaires** : paywall probable, synthèse FlowHunt retenue
- **arXiv 2603.09619 (Context Engineering paper)** : ID à reconfirmer
- **arXiv 2604.11978v1 (HORIZON benchmark long-horizon)** : à ouvrir si stratégie creuse long-horizon

---

*Section 12 rédigée par Claude le 2026-06-04 à partir de `01-context-engineering-research-2026.md`.*

---

## 11. Sources de référence (état de l'art 2025-2026)

### Sources primaires récupérées via WebFetch (2026-06-04)

- **Anthropic — Effective Context Engineering for AI Agents** (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 7 principes fondateurs récupérés :
  1. System prompts à la bonne altitude (ni trop rigide, ni trop vague)
  2. Token-efficient tools (self-contained, minimal overlap)
  3. Curated few-shot examples (diverses, canoniques)
  4. Just-in-time context retrieval (pointeurs + tools, pas stuffing)
  5. Hybrid retrieval (pre-retrieval + exploration)
  6. 3 techniques long-horizon : **compaction** + structured note-taking + sub-agent architectures
  7. Tool result clearing (raw result rarement re-nécessaire)

- **Anthropic — Building Effective Multi-Agent Research Systems** (https://www.anthropic.com/engineering/built-multi-agent-research-system) — insights clés pour SWEBOK v4 :
  - **Coût token** : multi-agent = **4× chat, 15× multi-agent vs chat** (per Anthropic BrowseComp eval)
  - **80% de la variance** de performance = tokens utilisés
  - **Multi-agent justifié seulement** si "value of task is high enough"
  - **Effort scaling** : 1 agent 3-10 calls (simple), 2-4 subagents 10-15 calls (comparison), 10+ subagents (complex)
  - **Context isolation** = separate context windows per subagent
  - **Lead agent** = seul à avoir la vue complète ; subagents = narrow scopes
  - **Plan persistant en mémoire** (sinon tronqué à 200k tokens)
  - **Artifact/file output** pour les gros résultats (subagent → fichier, lead → référence légère)
  - **Anti-pattern** : subagent instructions vagues → travail dupliqué
  - **Anti-pattern** : 50 subagents pour rien
  - **Anti-pattern** : agents qui continuent de chercher alors qu'ils ont assez
  - **Bottleneck actuel** : synchronous execution (lead ne peut pas steer les subagents)

### Sources complémentaires (corpus de connaissance général)

- Anthropic — *Prompt Caching* documentation
- OpenAI — *Agents SDK* context management patterns
- Google — *Agent Development Kit* memory hierarchy
- LangChain — *LangGraph* state management & checkpointing
- MemGPT / Letta — virtual context management
- RAG papers (Lewis et al. original, dense retrieval, hybrid search)
- Hierarchical memory research (SummScreen, multi-level summarization)

### Application directe à SWEBOK v4 (synthèse)

L'architecture du projet **est déjà partiellement alignée** avec ces best practices :
- ✅ Hyperagent-Orchestrator + Nexus-* = pattern Lead/Subagent
- ✅ Adversarial-gate (Red/Blue/Judge) = adversarial pattern
- ✅ COUNCIL BRIDGE (4 reviewers) = council pattern
- ✅ .swebok_state (SQLite) = state persistant
- ✅ DSL format `KEY:VALUE;;KEY:VALUE` = structured output
- ⚠️ **À formaliser** : consultation envelope (A1) — les phases ne sont pas explicitement read-only cache
- ⚠️ **À formaliser** : context isolation entre T1/T2/T3 — pas explicite actuellement
- ⚠️ **À formaliser** : token budget live par phase
- ⚠️ **À formaliser** : compaction checkpoint explicite
- ⚠️ **À formaliser** : user decision ledger (UDL)

*WebSearch est resté indisponible pendant cette session (erreur 400 API systématique). WebFetch a permis de récupérer 2 sources primaires Anthropic. Les sources secondaires sont issues de la connaissance générale du modèle.*
