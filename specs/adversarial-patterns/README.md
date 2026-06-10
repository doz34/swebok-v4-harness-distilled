# Adversarial Patterns for swebok — Phase-by-Phase

> **Date** : 2026-06-10
> **Source** : Synthèse de [Martin Fowler (2026) "Harness engineering"](https://martinfowler.com/articles/harness-engineering.html) + [dev.to "Adversarial Planning for SDD"](https://dev.to/marcosomma/adversarial-planning-for-spec-driven-development-4c3n) + [nyosegawa "Harness Engineering Best Practices 2026"](https://nyosegawa.com/en/posts/harness-engineering-best-practices-2026/) + bonnes pratiques CE-Harness v1.0
> **Contrainte** : Claude Code uniquement, pas de Docker, pas de dépendances externes

## 1. Concept

**Adversarial loop** = un système qui **défie systématiquement** chaque livrable de chaque phase **AVANT** de la valider, pour détecter les gaps et auto-corriger.

Per Fowler : *feedforward controls (guides)* + *feedback controls (sensors)*, computational (rapide, déterministe) ou inferential (LLM-judge).

## 2. Architecture

```
adversarial-loop/
├── lib/adv-loop/                    # Bibliothèque Python (stdlib only)
│   ├── stop_conditions.py          # 3 stop conditions mécaniques
│   ├── feedback.py                  # Feedforward (guides) + Feedback (sensors)
│   └── loop_orchestrator.py         # Orchestrateur principal
├── bin/adv-loop                     # CLI bash wrapper
├── specs/adversarial-patterns/      # Patterns par phase
│   ├── phase-0-discovery.sh
│   ├── phase-1-feasibility.sh
│   ├── ...
│   └── phase-10-retirement.sh
├── specs/workflows/by-phase/        # Specs swebok (input)
└── tests/adv-loop/                  # Self-tests
```

## 3. Utilisation

```bash
# Run adversarial loop on one phase
bin/adv-loop 0

# Run on all 11 phases
bin/adv-loop all

# Run with work file
bin/adv-loop 0 path/to/work.md

# Run self-tests
bin/adv-loop test

# Run per-phase pattern script
specs/adversarial-patterns/phase-0-discovery.sh
```

## 4. Output format (swebok DSL)

```
phase_loop:iterations=3;;
phase_loop:findings_crit=0;;
phase_loop:findings_high=0;;
phase_loop:findings_med=0;;
phase_loop:findings_low=1;;
phase_loop:tokens=0;;
phase_loop:elapsed_s=0;;
phase_loop:low_streak=0;;
adv_loop:verdict=🟢 OK
```

## 5. Stop conditions (mécaniques, pas émotionnelles)

Per dev.to *"Adversarial Planning for SDD"* :
> "You need stop conditions that are not emotional. You need boundaries that are mechanical."

| Condition | Default | Override par phase |
|---|---|---|
| **Time** | 30 min | spec définit (ex: 35min pour P0) |
| **Tokens** | 4k/7k/10k (soft/hard) | spec définit par phase |
| **Iterations** | 5 max | configuré |
| **Value** | 3 LOW en row = stop | évite la "rumination infinie" |

## 6. Adversarial patterns — par phase

| Phase | Pattern file | Capteurs computationnels |
|---|---|---|
| P0 Discovery | `phase-0-discovery.sh` | 7 livrés requis, P1 keywords interdits, charter vague |
| P1 Feasibility | `phase-1-feasibility.sh` | 4 dimensions faisabilité, ROI quantifié, payback, go/no-go signé, P0/P2 demarcation |
| P2 Requirements | `phase-2-requirements.sh` | AC testable (mesurable, pas vague), RTM traçabilité P0+forward, NFR coverage (perf/sec/scal/avail/usab), P1/P3 demarcation |
| P3 Architecture | `phase-3-architecture.sh` | ADR count ≥1 avec MADR template (Context/Decision/Consequences), C4 levels (context/container/component), archi style + security archi, P2/P4 demarcation |
| P4 Design | `phase-4-design.sh` | API contracts OpenAPI/Swagger + error responses, data model DDD, sequence diagrams (auth/main/error), P3/P5 demarcation |
| **P5 Implementation** | `phase-5-implementation.sh` | **source_code + unit_tests présents, P6 keywords interdits, antipatterns** |
| P6 Testing | `phase-6-testing.sh` | Coverage threshold (XG-6.2 ≥80% line/70% branch), mutation score (XG-6.3 ≥70%), defect backlog (XG-6.4), AC traceability (XG-6.10), test antipatterns, P5/P7 demarcation |
| **P7 Deployment** | `phase-7-deployment.sh` | **rollback plan TESTED, safe patterns (canary/blue-green), P8 keywords interdits** |
| P8 Operations | `phase-8-operations.sh` | SLO mesurable (p95/p99/<Xms), runbook actionnable + escalation, on-call rotation (primary/secondary/schedule/contact), post-mortem blameless+root cause+action items, P7/P9 demarcation |
| P9 Maintenance | `phase-9-maintenance.sh` | Maintenance type explicite (corrective/adaptive/perfective/preventive IEEE 1219), tech debt register (severity/owner/effort/impact), impact analysis + regression test, release notes, P8/P10 demarcation |
| P10 Retirement | `phase-10-retirement.sh` | RGPD compliance (retention/consent/anonymization/DPO/checksum), user migration, ownership transfer, system shutdown completeness (server/DNS/monitoring/log/DB), réversibilité window, closure memo, P9/P0 demarcation |

## 7. Résultats sur les 11 specs swebok (validation initiale)

```
P0: verdict=🟢 OK  | crit=0 high=0 med=0 low=1
P1: verdict=🟢 OK  | crit=0 high=0 med=0 low=1
P2: verdict=🟢 OK  | crit=0 high=0 med=0 low=2
P3: verdict=🟢 OK  | crit=0 high=0 med=0 low=3
P4: verdict=🟢 OK  | crit=0 high=0 med=0 low=1
P5: verdict=🟢 OK  | crit=0 high=0 med=0 low=3
P6: verdict=🟢 OK  | crit=0 high=0 med=0 low=3
P7: verdict=🟢 OK  | crit=0 high=0 med=0 low=3
P8: verdict=🟢 OK  | crit=0 high=0 med=0 low=2
P9: verdict=🟢 OK  | crit=0 high=0 med=0 low=3
P10: verdict=🟢 OK | crit=0 high=0 med=0 low=3
```

**0 CRIT, 0 HIGH, 0 MED sur les 11 phases** = swebok specs sont **adversarialement matures** (au niveau feedforward + computational feedback).

## 8. Steering loop (Fowler) — comment le mainteneur itère

Per Fowler : *"the human's job is to steer the agent by iterating on the harness. Whenever an issue happens multiple times, the feedforward and feedback controls should be improved."*

**Cycle** :
1. Run `bin/adv-loop all` → identifie les findings
2. Si HIGH/CRIT → corriger le livrable + le pattern
3. Si LOW se répète → améliorer le pattern (ex: ajouter un check)
4. Re-run → vérifier que le finding LOW est résolu
5. Commit

**Exemple de steering loop appliqué** :
1. Vague : "we should do this" dans charter.md
2. Run P0 → détecte "should" (MED)
3. Replace par "must" + critère mesurable
4. Re-run → 0 MED
5. Commit + lessons learned → améliorer le linter

## 9. Limites assumées

1. **Pas d'inferential checks** : les checks LLM-judge sont différés vers Council Bridge (simulée).
2. **Pas d'OS-level sandbox** : les per-phase patterns sont bash-only, pas de Docker.
3. **Pas de memory blocks** : pas de persistance des findings entre runs (à ajouter).
4. **Pas de TOFU sur les specs** : si un fichier spec est modifié hors spec, on ne le détecte pas.

## 10. Roadmap

| Sprint | Cible | Effort |
|---|---|---|
| **S0 (maintenant)** | 3 patterns (P0, P5, P7) + self-tests | ✅ Done |
| **S1** | 11 patterns complets (un par phase) | ✅ Done (2026-06-10) |
| **S2** | Inferential checks (LLM-judge via Council Bridge) | ✅ Done (2026-06-10) |
| **S3** | Steering loop persistence (memory blocks) | ✅ Done (2026-06-10) |
| **S4** | Adversarial corpus (50+ attack payloads) | 2 jours |
| **S5** | Property-based tests (4 propriétés par phase) | 2 jours |

## 10.2. Steering loop (S3) — usage

```bash
# 1. Run adv-loop normally — chaque run est auto-loggé dans .swebok_steering_state.db
bash bin/adv-loop 2
# → DSL output inclut maintenant un fragment steering:run_total=N etc.

# 2. Inspecter l'historique
bash bin/adv-loop history 2 10      # 10 derniers runs de la phase 2
bash bin/adv-loop history 2 50      # 50 derniers

# 3. Détecter les patterns qui se répètent
bash bin/adv-loop steer 2           # threshold=3 par défaut
bash bin/adv-loop steer 2 5         # threshold=5 (plus conservateur)

# 4. Marquer un pattern comme fixé (après amélioration du script)
bash bin/adv-loop ack a3f9b2c1

# 5. Nettoyer l'historique
bash bin/adv-loop clear 2           # clear phase 2 only
bash bin/adv-loop clear             # clear ALL
```

**Architecture :**
- DB isolée : `.swebok_steering_state.db` (séparée de `.swebok_state.db` pour ne pas toucher au schema principal)
- Tables : `runs` (résumé par run), `findings` (détail), `patterns` (détection récurrence)
- Fingerprint : SHA256 tronqué à 16 chars de `severity|category|message[:80]` — stable cross-runs
- Auto-log : chaque invocation de `adv-loop` insère un run + findings + met à jour les patterns

**DSL fragment steering (KEY=VALUE;;) :**
- `steering:run_total=N` — nombre de runs dans la fenêtre (last_n=10)
- `steering:patterns_detected=M` — patterns au-dessus du threshold
- `steering:recurring_categories=<top3>` — catégories les plus fréquentes
- `steering:top_finding=<message[:60]>` — pattern le plus récurrent

**Actions suggérées par pattern :**
- HIGH `feedback:spec_vague` → ajouter un check non-vague-langage au script de pattern
- HIGH `feedforward:demarcation` → resserrer la liste `PHASE_FEEDFORWARDS` dans feedback.py
- HIGH `feedback:required_section` → ajouter la section manquante à la spec
- HIGH `feedback:cross_phase` → ajouter une back-reference vers la phase antérieure
- LOW `feedback:spec_vague` → tolérable (LOW vague en prose est normal)

**Fix inclus (S3+) :** le check `feedforward:spec_exists` ne log plus "Spec OK" comme un LOW finding (c'était un marqueur de succès, pas un finding — polluait le détecteur de patterns).

## 10.1. Council Bridge (S2) — usage

```bash
# 1. Émet l'enveloppe <MULTIAGENT_LAUNCH> avec 4 rôles (ciso/qa-lead/architect/devops-lead)
bash bin/adv-loop 5 --council
# → exit 99 (signal au dispatcher pour spawn les 4 agents)

# 2. Dispatcher (Claude Code) spawn 4 agents via Agent tool
#    Chaque agent retourne 1 ligne DSL :
#      CISO/DevOps-Lead: RED: VULN:<sev>;;LOC:..;;TYPE:..;;FIX_REQ:..
#      QA-Lead/Architect: BLUE: DEFENDED;;NORMS:..;;STATUS:<OK|FAIL>

# 3. Dispatcher écrit les DSL dans /tmp/adv-loop-council-result.json
#    Format: {"red_lines": [...], "blue_lines": [...]}

# 4. Ré-invoke adv-loop avec --verify-result pour intégrer le verdict
bash bin/adv-loop 5 --verify-result /tmp/adv-loop-council-result.json
# → verdict final = max(computational_severity, council_severity)
```

**DSL fragment council** (KEY=VALUE;;) :
- `council:red_vuln=<CRIT|HIGH|MED|LOW>` — sévérité RED agrégée
- `council:red_loc=<file>` — location du pire finding RED
- `council:red_type=<vuln_type>` — type de vulnérabilité
- `council:red_fix_req=<fix>` — fix requis
- `council:blue_defended=<OK|FAIL>` — statut BLUE agrégé
- `council:blue_norms=<KA-X+KA-Y>` — normes SWEBOK citées
- `council:severity=<sev>` — sévérité council finale
- `council:agents_red=N` / `council:agents_blue=M` — nombre d'agents par lane

**Règles d'agrégation** (per CLAUDE.md L6.1) :
- RED : worst-severity wins (CRIT > HIGH > MED > LOW)
- BLUE : any FAIL → DEFENDED:FAIL ; all OK → DEFENDED:OK
- Verdict council combiné : si BLUE FAIL → minimum HIGH, sinon RED worst
- Verdict final adv-loop = max(computational, council)

**Note sur les subagent_types** : les IDs `nexus-ciso`, `nexus-qa-lead`, `nexus-architect`, `nexus-devops-lead` sont les identifiants canoniques (per CLAUDE.md L6). Si l'environnement Claude Code n'a pas ces subagents enregistrés, utiliser `general-purpose` avec framing de rôle dans le prompt — c'est ce qui a été fait pour la validation end-to-end (P5) le 2026-06-10.

## 11. Liens

- **Martin Fowler** : https://martinfowler.com/articles/harness-engineering.html
- **Adversarial Planning for SDD** : https://dev.to/marcosomma/adversarial-planning-for-spec-driven-development-4c3n
- **Harness Engineering 2026** : https://nyosegawa.com/en/posts/harness-engineering-best-practices-2026/
- **CE-Harness LESSONS-LEARNED** : `/home/doz/context-engineering-harness/audit/08-LESSONS-LEARNED-FOR-SWEBOK-2026-06-09.md`
- **swebok CLAUDE.md** : instructions pour le mainteneur

---

> **Statut** : v1.2 (S3 complete) — 11 patterns + Council Bridge + Steering loop persistence, 20/20 self-tests
> **Auteur** : swebok maintainer + Claude (adversarial planning mode)
> **Date** : 2026-06-10
