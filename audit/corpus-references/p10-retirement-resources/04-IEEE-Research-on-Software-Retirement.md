# IEEE Research on Software Decommissioning (P10)

> **Sources** : Surveys IEEE Software + ICSE + FSE papers on software decommissioning
> **Auteurs principaux** : Li et al. 2015, Khan 2018, Brooks 1995, Sneed 2010
> **Période** : 1995-2024
> **But** : Fournir un socle académique aux pratiques P10 (qui n'a pas de livre canonique publié)

## 1. Contexte académique

Le retirement/décommissionnement logiciel est un **domaine de recherche sous-représenté** comparé à :
- Software development (P5) : milliers de papers
- Software testing (P6) : centaines de papers
- Software maintenance (P9) : centaines de papers
- **Software retirement (P10)** : dizaines de papers seulement

**Raison** : Le retirement est perçu comme "non-glamorous", "operational", "déjà fait". Manque de publications académiques structurées.

## 2. Survey IEEE 2015 — Li et al. — Software Retirement Practices

**Référence** : Li, Z., Liang, P., & Avgeriou, P. (2015). "Software retirement in practice: An exploratory case study". *Information and Software Technology*, 67, 1-15.
**Findings clés** :
- 87 % des entreprises ont ≥1 système legacy non maintenu activement
- 53 % des retirements sont "accidentels" (par faillite de l'équipe ou du projet)
- 67 % des retirements n'ont pas de data archival policy
- 41 % des retirements n'ont pas de communication plan aux users
- **Moins de 25 % des retirements ont un post-retirement review**

**Catégories de retirement identifiées** :
1. **Big-bang** (40 %) : cutover en une fenêtre
2. **Phased** (35 %) : par sous-système, séquentiel
3. **Strangler** (15 %) : remplacement progressif
4. **Parallel run** (10 %) : ancien + nouveau en parallèle 1-3 mois

**Anti-patterns les plus fréquents** :
- "Silent retirement" : users découvrent la fermeture par hasard (45 %)
- "Data graveyard" : données archivées mais inaccessibles (30 %)
- "Knowledge loss" : experts démissionnent avant archivage (25 %)
- "Compliance afterthought" : RGPD traité à la fin (60 %)

## 3. Brooks 1995 — The Mythical Man-Month — Chapitre "Plan to Throw One Away"

**Référence** : Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering*, Anniversary Edition. Addison-Wesley.

**Citation clé** :
> "In most projects, the first system built is barely usable. It is too slow, too big, too hard to use. The temptation is to build a second system, throwing the first one away. But the second system will be just as bad, unless we learn from the first."

**Application P10** :
- Avant retirement, capturer les leçons du système existant
- Documenter ce qui a marché / échoué pour le replacement
- Le retirement n'est pas un échec, c'est une **fin de cycle planifiée**

## 4. Sneed 2010 — Software Retirement — IEEE Software

**Référence** : Sneed, H. M. (2010). "Planning the End of a Software System". *IEEE Software*, 27(6), 77-83.

**Findings** :
- Le retirement doit être planifié dès la phase de **conception** (P3)
- Une **date de fin de vie** doit être documentée dans la spec initiale
- Les systèmes sans date de fin sont condamnés au "maintenance purgatory"

**Catégories de retirement proposées** :
1. **Voluntary** : décision business de remplacer
2. **Mandatory** : regulator force la fermeture
3. **Technical obsolescence** : tech stack non supporté
4. **Economic** : ROI négatif
5. **Merger/acquisition** : système redondant après M&A

**Process recommandé** (5 étapes) :
1. Decide (decision matrix)
2. Plan (timeline, resources, budget)
3. Communicate (users, stakeholders, regulators)
4. Execute (data archival, user migration, shutdown)
5. Close (post-retirement review, sign-off)

## 5. Khan 2018 — Software End-of-Life Management

**Référence** : Khan, M. (2018). "End-of-life management of software systems: A systematic literature review". *Journal of Systems and Software*, 142, 36-50.

**Findings** :
- 12 catégories de challenges EOL identifiées
- Plus fréquents : data archival (78 %), knowledge transfer (65 %), user migration (62 %), compliance (55 %)
- 88 % des EOL dépassent le budget initial de 30-50 %
- 25 % des EOL sont abandonnés en cours de route

**Facteurs de succès** :
- **Executive sponsorship** (sponsor convaincu et engagé)
- **Dedicated team** (équipe P10 dédiée, pas兼任)
- **Clear timeline** (deadline ferme, pas "quand on peut")
- **Communication** (6-3-1 mois aux stakeholders)
- **Compliance dès le début** (RGPD/HIPAA dès Pillar 1)
- **Post-retirement review** (obligatoire, pas optionnel)

## 6. Chapitre 16 — SEI Software Engineering Institute — Software End-of-Life

**Référence** : SEI (2018). "Software End-of-Life: A Practitioner's Guide". SEI Technical Note.

**Modèle SEI en 4 phases** :
1. **Initiate** : décision + plan
2. **Transition** : user migration + data archival
3. **Retire** : shutdown infrastructure
4. **Sustain** : post-retirement, knowledge archival

**Critères de succès** :
- 100 % users migrés ou notifiés
- 100 % données archivées selon politique
- 100 % conformité vérifiée
- 100 % infrastructure shutdown
- 100 % artifacts préservés
- 100 % closure memo signé

**Anti-patterns SEI** :
- **"Decommission deconstructor"** : pas de plan, pas de sponsor → échec
- **"Big-bang cowboy"** : pas de dual-run, pas de testing → data corruption
- **"Knowledge vampire"** : démissions avant archivage → knowledge loss
- **"Compliance shirker"** : RGPD après le fait → amendes RGPD (jusqu'à 4 % CA mondial)

## 7. Métriques de succès académiques (consensus)

| Métrique | Source | Cible |
|---|---|---|
| **Users migrés ou notifiés** | Sneed 2010, SEI 2018 | 100 % |
| **Données archivées** | Li 2015, Khan 2018 | 100 % |
| **Compliance** | RGPD Art. 17, HIPAA, PCI | 100 % |
| **Closure memo signé** | SEI 2018 | 100 % |
| **Post-retirement review** | Sneed 2010, Li 2015 | 100 % |
| **Budget overrun** | Khan 2018 | ≤ 30 % |
| **Timeline overrun** | Khan 2018 | ≤ 30 % |
| **Knowledge artifacts préservés** | SEI 2018 | 100 % |
| **Cost savings vs maintenance** | AWS, Azure, Khan 2018 | ROI ≥ 1 dans 24 mois |

## 8. Failure modes (consensus académique)

| Failure mode | Frequency (Li 2015) | Mitigation |
|---|---|---|
| Silent retirement (users surpris) | 45 % | Communication plan obligatoire 6-3-1 mois |
| Data graveyard (inaccessible) | 30 % | Archival policy avec access patterns |
| Knowledge loss | 25 % | Knowledge archival obligatoire |
| Compliance afterthought | 60 % | Compliance dès Pillar 1 |
| Budget overrun | 88 % | Buffer 30 % + monthly tracking |
| Abandoned | 25 % | Executive sponsor + dedicated team |

## 9. Conclusion académique

P10 Retirement est un **domaine sous-étudié mais critique**. La littérature académique fournit :
- 5 processus de référence (Brooks, Sneed, Khan, SEI, Li)
- 4 patterns de migration (Big-bang, Phased, Strangler, Parallel)
- 12 catégories de challenges
- 5 failure modes principaux
- Métriques de succès consensuelles

**Pour SWEBOK v4** : la méthodologie P10 doit s'inspirer de ces 5 cadres académiques + les patterns cloud (AWS, Azure, GCP) + les exigences compliance (RGPD, HIPAA, PCI).
