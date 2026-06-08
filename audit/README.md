# SWEBOK v4 Harness — Audit des Phases

> Grilles d'audit à compléter hors-ligne. Chaque fichier est autonome.
> **Note 2026-06-05** : fix structurel majeur. L'ancien modèle 9-phases fusionnait SWEBOK P2 (Architecture) et P3 (Design). Le modèle canonique est désormais **10 phases**, 1-par-1 avec les KAs SWEBOK v4.

## Comment utiliser ce dossier

### Étape 1 — Lis la stratégie context engineering d'abord
Ouvre `00-context-engineering-strategy.md` en premier. C'est la référence transverse qui informe toutes les grilles. Tu y trouveras le modèle L0-L3, les budgets par phase, et les anti-patterns à éviter.

### Étape 2 — Audite les phases une par une
L'ordre recommandé est l'ordre du cycle de vie (du discovery au retirement), mais tu peux commencer par la phase qui te préoccupe le plus.

Pour chaque phase, le fichier te fournit :
- Une **grille pré-remplie** avec plusieurs suggestions par question (coche ou reformule)
- Des **espaces vides** pour tes réponses libres
- Des **sections contextuelles** (spec existante, hooks, agents)
- Un **verdict final** 🟢 / 🟡 / 🔴

### Étape 3 — Édite directement les fichiers
Tu peux éditer chaque fichier .md avec n'importe quel éditeur (VSCode, vim, nano, même un éditeur web). Les formats Markdown sont standard.

### Étape 4 — Livre tous les fichiers remplis à Claude en une fois
Quand tu as fini, dis simplement à Claude "j'ai rempli les grilles, lis-les". Il lira les fichiers et continuera le cadrage.

---

## Liste des fichiers (modèle 10 phases, 2026-06-05)

| Fichier | Phase | Équivalent SWEBOK v4 | Statut |
|---------|-------|----------------------|--------|
| `00-context-engineering-strategy.md` | (transverse) | — | 📖 Référence |
| `01-context-engineering-research-2026.md` | (transverse) | — | 📖 Référence |
| `phase-0-discovery-audit.md` | Discovery | (hors SWEBOK, ajouté) | ✅ FERMÉ (v2) |
| `phase-1-concept-feasibility-audit.md` | Concept/Feasibility | Software Engineering Management KA | ✅ FERMÉ (v2) |
| `phase-2-requirements-audit.md` | Requirements | P1 SWEBOK (Requirements Engineering) | ✅ FERMÉ (v2) |
| `phase-3-architecture-audit.md` | Architecture | P2 SWEBOK (Software Architecture) | ✅ FERMÉ (v2 finale 🟢) |
| `phase-4-design-audit.md` | Design | P3 SWEBOK (Software Design) | ✅ FERMÉ (v2 finale 🟢) |
| `phase-5-implementation-audit.md` | Implementation | P4 SWEBOK (Software Construction) | ✅ FERMÉ (v2 finale 🟢) |
| `phase-6-testing-audit.md` | Testing | P5 SWEBOK (Software Testing) | ⬜ À remplir |
| `phase-7-deployment-audit.md` | Deployment | Software Configuration Management | ⬜ À remplir |
| `phase-8-operations-audit.md` | Operations | (hors SWEBOK core, justifié) | ⬜ À remplir |
| `phase-9-maintenance-audit.md` | Maintenance | P6 SWEBOK (Software Maintenance) | ⬜ À remplir |
| `phase-10-retirement-audit.md` | Retirement | Software Engineering Process | ⬜ À remplir |

---

## Fix structurel 2026-06-05 : 9 phases → 10 phases

### Problème identifié

L'ancien modèle 9-phases avait **3 anomalies structurelles** :
1. **P3 (harness) = SWEBOK P2 (Architecture) + P3 (Design) FUSIONNÉS** — perte de détail
2. **Phase 1 (harness) MANQUANTE** entre Discovery et Requirements
3. **9 phases harness vs 10+ KAs SWEBOK** — désalignement

### Solution appliquée

**Split propre + renommage cascade** :
- **NOUVEAU P1** = Concept/Feasibility (filtre go/no-go entre Discovery et Requirements)
- **NOUVEAU P3** = Architecture (split d'avec l'ancien P3 Design)
- **P4 Design** = Design seul (l'ancien P3 Design sans Architecture)
- **P5-P10** = renommage cascade de l'ancien P4-P9

### Mapping avant/après

| Ancien (9 phases) | Nouveau (10 phases) | Équivalent SWEBOK v4 |
|---|---|---|
| P0 Discovery | P0 Discovery | (hors SWEBOK) |
| — | **P1 Concept/Feasibility** | Software Engineering Management |
| P2 Requirements | P2 Requirements | P1 SWEBOK |
| P3 Design (fused) | **P3 Architecture** | P2 SWEBOK |
| (P3 Design) | **P4 Design** | P3 SWEBOK |
| P4 Implementation | P5 Implementation | P4 SWEBOK |
| P5 Testing | P6 Testing | P5 SWEBOK |
| P6 Deployment | P7 Deployment | Software Configuration Management |
| P7 Operations | P8 Operations | (hors SWEBOK core) |
| P8 Maintenance | P9 Maintenance | P6 SWEBOK |
| P9 Retirement | P10 Retirement | Software Engineering Process |

### Justification

- **P1 Concept/Feasibility** : comble le gap entre "intention cadrée" (P0) et "specs testables" (P2). Permet une décision go/no-go documentée. Économise du temps de specs sur projets infaisables.
- **Split P3 (Archi) + P4 (Design)** : sépare les KAs SWEBOK P2 et P3 qui étaient fusionnés. Évite la perte de détail (l'un des deux était sacrifié dans l'ancien modèle).
- **Renommage P4-P9 → P5-P10** : cascade mécanique pour aligner le numbering harness sur le numbering SWEBOK.

### Impact sur l'outillage

- `pre-tool-use/token-counter.sh` : mis à jour avec les nouvelles phases P1, P3, P10 et les nouveaux budgets.
- `audit/00-context-engineering-strategy.md` : à mettre à jour avec la nouvelle table de budgets.
- Tous les fichiers specs renommés (phase-3-design.md → phase-4-design.md, etc.) et leurs références croisées mises à jour.

---

## Findings pré-identifiés (à confirmer pendant l'audit)

Ces points ont été détectés pendant la préparation et seront à valider dans les grilles :

1. ✅ **Phase 1 manquante** : **RÉSOLU 2026-06-05** (P1 Concept/Feasibility créé)
2. ✅ **P2 Architecture fusionné dans P3 Design** : **RÉSOLU 2026-06-05** (split en P3 Architecture + P4 Design)
3. ✅ **P4 SWEBOK (Estimation) absente** : **RÉSOLU 2026-06-05** (P5 Implementation inclut ses propres estimations)
4. **Phase 0 (Discovery) et Phase 8 (Operations) ajoutées** : ces phases hors-SWEBOK sont-elles justifiées par un besoin réel ? — À valider
5. ✅ **9 phases au lieu de 10** : **RÉSOLU 2026-06-05** (10 phases maintenant, alignement 1-pour-1 SWEBOK)
6. **Context engineering déjà partiellement en place** (CLAUDE.md 759 bytes, .swebok_state machine, ANTI-ROT) mais pas formalisé.

### Findings post-corpus (2026-06-06)

7. ✅ **Grilles d'audit actualisées** : les 11 grilles (P0-P10) ont été révisées le 2026-06-06 pour intégrer le nouveau référentiel corpus. Sections §3.3, §5.3, verdict global mis à jour.
8. ✅ **Mac Studio scan intégré** : 117 livres corpus-matching identifiés (§18). Phase P5 (Impl) à 100% de couverture, P0 (Discovery) à 53%, P1 (Feasib) à 20%, P6 (Testing) à 13%, P10 (Retirement) à 0% (critique).
9. ✅ **New Books acquis** : 87 livres uniques acquis (110 fichiers, ~2.5 GB) (§19). PMBOK 8e, Mythical Man-Month, Clean Code, Pragmatic Programmer, SRE Book, Observability Engineering, etc.
10. ✅ **Standards téléchargés** : 44 documents NIST/OWASP open-access (§13). NIST CSF 2.0, SSDF 800-218, 800-53r5, OWASP ASVS 5.0.
11. **Couverture cumulée** : ~40% du corpus recommandé (cf. §20 du référentiel pour les ~43 livres encore manquants).

### Statut de couverture par phase (post-acquisition 2026-06-06)

| Phase | Couverture | Verdict |
|---|---:|---|
| P0 Discovery | 53% | 🟡 Suffisant |
| P1 Feasibility | 20% | 🟠 Faible |
| P2 Requirements | 40% | 🟡 Suffisant |
| P3 Architecture | 65% | 🟢 Bon |
| P4 Design | 40% | 🟡 Suffisant |
| P5 Implementation | **100%** | 🟢 Très bon |
| P6 Testing | 13% | 🟠 Faible |
| P7 Deployment | 73% | 🟢 Bon |
| P8 Operations | 70% | 🟢 Bon |
| P9 Maintenance | 30% | 🟠 Faible |
| P10 Retirement | **0%** | 🔴 Critique |

**Top 5 acquisitions prioritaires** (§20.6) :
1. **Clean Architecture** (Martin, 2017) — ~$30
2. **Software Architecture in Practice 4th** (Bass, 2021) — ~$60
3. **Continuous Delivery** (Humble/Farley, 2010) — ~$45
4. **The DevOps Handbook 2nd** (Kim, 2021) — ~$30
5. **Working Effectively with Legacy Code** (Feathers, 2004) — ~$50

**Budget pour atteindre 75% du corpus** : ~$1 200.

---

## Workflow d'audit recommandé

```
Par phase :
1. Lire la spec existante (specs/workflows/by-phase/phase-X-xxx.md)
2. Lire le code qui l'implémente (lib/, scripts/, hooks/)
3. Remplir la grille section par section
4. Statuer le verdict
5. Lister les actions
6. Répéter pour la phase suivante
```

Une fois toutes les grilles remplies, on aura :
- Un **inventaire** de ce qui est bien, perfectible, ou à revoir
- Une **liste d'actions** priorisée
- Un **nouveau design de référence** pour chaque phase (si verdict 🔴)
- Une **trajectoire** pour itérer le projet
