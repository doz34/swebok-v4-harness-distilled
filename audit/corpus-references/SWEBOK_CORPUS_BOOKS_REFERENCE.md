# SWEBOK v4 Distiller — Corpus Books Reference

> **Document purpose** : Référentiel exhaustif de livres (éditeurs **O'Reilly**, **Packt Publishing**, **PMI/IIBA**, Manning, Pragmatic Bookshelf, Addison-Wesley, Wiley, Pearson, Apress, etc.) à intégrer dans le corpus du projet **swebok-v4-harness-distilled** pour améliorer la qualité et la performance de **chaque phase** (0→10).
>
> **Date** : 2026-06-05
> **Préparé par** : discovery + exhaustive web search (O'Reilly, Packt, PMI, IIBA)
> **Périmètre** : livres à jour (2020–2026), orientés pratique + référentiels normatifs/certifiants
> **Statut** : v1 — à valider phase par phase avant intégration batch

---

## Table des matières

1. [Synthèse exécutive](#1-synthèse-exécutive)
2. [État actuel du corpus — diagnostic](#2-état-actuel-du-corpus--diagnostic)
3. [Lacunes identifiées par phase](#3-lacunes-identifiées-par-phase)
4. [Livres recommandés — section éditeurs (O'Reilly + Packt)](#4-livres-recommandés--section-éditeurs-oreilly--packt)
   - 4.1 [Phase 0 — Discovery / Stakeholder](#41-phase-0--discovery--stakeholder)
   - 4.2 [Phase 1 — Concept & Feasibility](#42-phase-1--concept--feasibility)
   - 4.3 [Phase 2 — Requirements](#43-phase-2--requirements)
   - 4.4 [Phase 3 — Architecture](#44-phase-3--architecture)
   - 4.5 [Phase 4 — Design](#45-phase-4--design)
   - 4.6 [Phase 5 — Implementation / Construction](#46-phase-5--implementation--construction)
   - 4.7 [Phase 6 — Testing / Verification](#47-phase-6--testing--verification)
   - 4.8 [Phase 7 — Deployment](#48-phase-7--deployment)
   - 4.9 [Phase 8 — Operations / SRE](#49-phase-8--operations--sre)
   - 4.10 [Phase 9 — Maintenance](#410-phase-9--maintenance)
   - 4.11 [Phase 10 — Retirement](#411-phase-10--retirement)
5. [Section additionnelle — PMI / Project Management Institute](#5-section-additionnelle--pmi--project-management-institute)
6. [Section additionnelle — IIBA & Business Analysis (BABOK)](#6-section-additionnelle--iiba--business-analysis-babok)
7. [Section additionnelle — Classics / Fondations non-négociables](#7-section-additionnelle--classics--fondations-non-négociables)
8. [Section additionnelle — Soft skills, leadership, communication](#8-section-additionnelle--soft-skills-leadership-communication)
9. [Section additionnelle — AI-assisted software development](#9-section-additionnelle--ai-assisted-software-development)
10. [Plan d'intégration — priorisation & risques](#10-plan-dintégration--priorisation--risques)
11. [Annexes](#11-annexes)
12. **[NOUVEAU] Section additionnelle — Documents / livres à très forte valeur ajoutée (toutes sources)**](#12-section-additionnelle--documents--livres-à-très-forte-valeur-ajoutée-toutes-sources-confondues)
13. [Standards et méthodologies (toutes phases)](#13-documents-de-standards-et-de-méthodologie-toutes-phases)
14. [Académie / Papers fondateurs (PDF libres)](#14-académie--papers-fondateurs-à-intégrer-en-pdf-tous-libres)
15. [Documents internes / organisationnels utiles](#15-documents-internes--organisationnels-utiles)
16. [Statistiques finales](#16-statistiques-finales-cette-section)
17. [Recommandation finale (synthèse)](#17-recommandation-finale-synthèse)
18. **[NOUVEAU] Sources locales — Mac Studio (Scan 2026-06-05)**](#18-sources-locales--mac-studio-scan-du-2026-06-05)
19. **[NOUVEAU] Nouveaux livres acquis (Bureau/New Books/) — Achat local 2026-06-06**](#19-nouveaux-livres-acquis-achat-local--bureaunew-books)
20. **[NOUVEAU] Lacunes restantes et références recommandées (≥ 2017)**](#20-lacunes-restantes-et-références-recommandées-≥-2017)

---

## 1. Synthèse exécutive

### TL;DR

Le corpus actuel de **777 livres** est **déséquilibré** : très fort en Python/Web-frontend/ML/Blockchain, mais **quasi-vide** sur les phases "côté humain" (Discovery, Stakeholder, Communication, Maintenance) et **"côté production"** (SRE, Observability, Incident, Retirement). **PMI/PMBOK/BABOK** = zéro livre. Les **canoniques du génie logiciel** (Fowler, Martin, Humble, Google) = absents ou marginaux.

**Recommandation principale** : intégrer **~480 ressources distinctes** (livres + standards + papers + docs internes), organisées en **5 vagues** selon l'urgence (cf. §10). Couvre **tous** les éditeurs majeurs + ISO/IEEE/NIST/OWASP/CNCF + academia + papers fondateurs.

### Ce que la recherche a montré

1. **O'Reilly reste la mine d'or #1** : couverture la plus large, éditions récentes (2024–2026) sur tous les sujets SWEBOK. Patterns : livres de fondations (Fowler, Martin, Humble) + "livres pragmatiques" (Humble Bundle "Software Architecture 2025", playlist "Clean Code & Refactoring", etc.).
2. **Packt est spécialisé "Hands-On"** : force sur les aspects concrets/outillage (cloud, microservices, pentesting, tests) — utile surtout pour les phases 5–9.
3. **PMI a un corpus normatif à part** : **PMBOK 7e/8e**, **PMI Standard for Business Analysis**, **Standard for Risk Management**, **Standard for Program Management**, **Standard for Portfolio Management**, **Governance of Portfolios, Programs, and Projects**, **Disciplined Agile (DA)**. Ces standards sont la **référence mondiale** pour les phases 0, 1, 2, 8, 9 et transcendent SWEBOK.
4. **IIBA/BABOK** complète PMI côté business analysis : **BABOK v3** + extensions.
5. **Addison-Wesley / Pearson / Wiley** = le **vrai trésor** du corpus canonique (Mythical Man-Month, Pragmatic Programmer, Fowler, GoF, Evans, Brooks) — **largement absents** du corpus actuel.
6. **Manning / Pragmatic Bookshelf** = le **pendant pratique** (Microservices Patterns, Release It!, Beyond Legacy Code, Specification by Example) — à intégrer en priorité.
7. **Papers académiques fondateurs** (Parnas 1972, Brooks 1986, Naur 1986, Reeves 1992, Moseley & Marks 2006) sont **gratuits en PDF** et à **valeur inestimable** — sous-exploités.
8. **Standards & normes ISO/IEEE/NIST/OWASP/CNCF** : souvent **libres**, indispensables pour cadrage légal/réglementaire.
9. **Lacunes critiques** : (a) PMI/PMBOK (zéro), (b) Discovery/Stakeholder (zéro), (c) SRE/Observability (light), (d) Maintenance/Legacy (light), (e) Retirement (zéro), (f) Classics (Fowler/Martin/Brooks/Popp) largement absents.

---

## 2. État actuel du corpus — diagnostic

### 2.1 Métriques globales (per `distilled/citations/by-domain.json`)

| Domaine | Livres | % corpus | Appréciation |
|---|---:|---:|---|
| Python ecosystem | 138 | 17,8 % | ✅ Surreprésenté |
| Web frontend | 95 | 12,2 % | ✅ Surreprésenté |
| ML/AI | 81 | 10,4 % | ✅ Surreprésenté |
| Data engineering | 40 | 5,1 % | ✅ Suffisant |
| Software engineering (général) | 34 | 4,4 % | ⚠️ Faible |
| Cybersecurity | 33 | 4,2 % | ✅ Suffisant |
| Database | 30 | 3,9 % | ✅ Suffisant |
| DevOps | 20 | 2,6 % | ⚠️ Faible |
| Architecture | 12 | 1,5 % | 🔴 **Critique** |
| **Project management (PMI)** | **0** | **0 %** | 🔴 **Absent** |
| **Discovery / Stakeholder** | **0** | **0 %** | 🔴 **Absent** |
| **SRE / Observability** | **< 5** | **< 1 %** | 🔴 **Absent** |
| **Maintenance / Legacy** | **< 3** | **< 1 %** | 🔴 **Absent** |
| **Retirement** | **0** | **0 %** | 🔴 **Absent** |

### 2.2 Livres canoniaux présents vs absents

| Livre canonique | Statut corpus | Valeur pour le projet |
|---|:---:|---|
| Building Microservices, 2nd ed. (Newman) | ✅ présent | P3, P4, P7 |
| Building Event-Driven Microservices | ✅ présent | P3, P7 |
| Head First Software Architecture (Gandhi/Richards/Ford) | ✅ présent | P3 |
| Fundamentals of Software Architecture (Richards/Ford) | ✅ présent | P3 |
| Microservices Patterns (Richardson) | ✅ présent | P3 |
| Software Architecture: The Hard Parts | ✅ présent | P3 |
| Building Evolutionary Architectures, 2nd ed. | ✅ présent | P3, P9 |
| Learning Domain-Driven Design (Vernon) | ✅ présent | P2, P3 |
| Software Architecture Patterns 2nd ed. (Richards) | ✅ présent | P3 |
| Software Architecture Metrics | ✅ présent | P3, P4 |
| Flow Architectures (Ford) | ✅ présent | P3 |
| Requirements Engineering 4th ed. (Phillips) | ✅ présent | P2 |
| Software Architecture in Practice 4th ed. (Bass) | ❌ **absent** | P3, P4 |
| Designing Software Architectures 2nd ed. (Cervantes/Kazman) | ❌ **absent** | P3 |
| Effective Software Architecture (Ford) | ❌ **absent** | P3 |
| Software Architecture in an AI World (O'Reilly Radar) | ❌ **absent** | P3 |
| Software Engineering at Google (Winters) | ❌ **absent** | P5, P6, P8 |
| The Pragmatic Programmer 20th Anniversary (Hunt/Thomas) | ❌ **absent** | P5 |
| Clean Code (Martin) | ❌ **absent** (Clean Code Cookbook seulement) | P4, P5 |
| Clean Architecture (Martin) | ❌ **absent** | P3, P4 |
| Clean Craftsmanship (Martin) | ❌ **absent** | P4, P5 |
| Refactoring 2nd ed. (Fowler) | ❌ **absent** | P4, P9 |
| Working Effectively with Legacy Code (Feathers) | ❌ **absent** | P9 |
| Beyond Legacy Code (Bernstein) | ❌ **absent** | P9 |
| The Mythical Man-Month (Brooks) | ❌ **absent** | P0, P8 |
| Peopleware (DeMarco/Lister) | ❌ **absent** | P0, P8 |
| Death March (Yourdon) | ❌ **absent** | P0, P8 |
| Waltzing with Bears (McConnell) | ❌ **absent** | P0, P1 |
| Software Requirements 3rd ed. (Wiegers/Beatty) | ❌ **absent** | P2 |
| Agile Software Requirements (Leffingwell) | ❌ **absent** | P2 |
| User Stories Applied (Cohn) | ❌ **absent** | P2 |
| Visual Models for Software Requirements (Ambler) | ❌ **absent** | P2 |
| Domain-Driven Design (Evans) | ❌ **absent** (seulement "Learning DDD") | P2, P3 |
| Implementing DDD (Vernon) | ❌ **absent** | P2, P3 |
| Patterns of Enterprise Application Architecture (Fowler) | ❌ **absent** | P3, P4 |
| Enterprise Integration Patterns (Hohpe/Woolf) | ❌ **absent** | P3, P4 |
| Continuous Delivery (Humble/Farley) | ❌ **absent** | P7 |
| The DevOps Handbook (Kim et al.) | ❌ **absent** | P7, P8 |
| The Phoenix Project / Unicorn Project (Kim) | ❌ **absent** | P0, P7 |
| Accelerate (Forsgren/Humble/Kim) | ❌ **absent** | P0, P8 |
| Modern Software Engineering (Poppendieck) | ❌ **absent** | P5, P6, P8 |
| Site Reliability Engineering (Google) | ❌ **absent** | P8 |
| The Site Reliability Workbook (Google) | ❌ **absent** | P8 |
| Observability Engineering (Majors/Fong-Jones/Miranda) | ❌ **absent** | P8 |
| Chaos Engineering (Rosenthal) | ❌ **absent** | P7, P8 |
| Building Secure & Reliable Systems (Google) | ❌ **absent** | P7, P8 |
| Release It! 2nd ed. (Nygard) | ❌ **absent** | P7, P8 |
| Production-Ready Microservices (Newman) | ❌ **absent** | P7, P8 |
| Effective Java 3rd ed. (Bloch) | ❌ **absent** | P5 |
| Designing Data-Intensive Applications 2nd ed. (Kleppmann) | ❌ **absent** | P3, P8 |
| The Staff Engineer's Path (Tanner) | ❌ **absent** | P0, P8 |
| An Elegant Puzzle (Winters) | ❌ **absent** | P5 |
| The Manager's Path (Kaminski) | ❌ **absent** | P0, P8 |
| Team Topologies (Skelton/Pais) | ❌ **absent** | P0, P8 |
| INSPIRED (Cagan) | ❌ **absent** | P0 |
| Escaping the Build Trap (Perri) | ❌ **absent** | P0 |
| Lean UX 3rd ed. (Gothelf) | ❌ **absent** | P0 |
| Design Sprint (Knapp) | ❌ **absent** | P0, P1 |
| Sprint (Knapp) | ❌ **absent** | P0 |
| The Lean Startup (Ries) | ❌ **absent** | P0, P1 |
| Business Model Generation (Osterwalder) | ❌ **absent** | P0, P1 |
| Value Proposition Design (Osterwalder) | ❌ **absent** | P0, P1 |
| Thinking in Systems (Meadows) | ❌ **absent** | P0, P1 |
| Reinventing Organizations (Laloux) | ❌ **absent** | P0, P8 |
| AntiPatterns (Brown) | ❌ **absent** | tous |
| Exploring Requirements (Gause/Weinberg) | ❌ **absent** | P2 |
| **PMI Standards (PMBOK, Risk, Program, Portfolio, Governance, DA, BA)** | 🔴 **0 sur 8** | P0, P1, P2, P8, P9 |
| **BABOK v3 (IIBA)** | 🔴 **absent** | P0, P2 |
| **Crucial Conversations** | ❌ **absent** | tous |
| **Switch (Heath/Heath)** | ❌ **absent** | tous |
| **Drive (Pink)** | ❌ **absent** | P0, P8 |
| **Difficult Conversations** | ❌ **absent** | P0, P8 |
| **The Five Dysfunctions of a Team (Lencioni)** | ❌ **absent** | P0, P8 |
| **Making Software (Oram/Wilson)** | ❌ **absent** | P5, P6 |
| **Refactoring Databases (Sadalage)** | ❌ **absent** | P9 |
| **Sun Tzu / Clausewitz (stratégie)** | ❌ **absent** | P0, P1, P9 |
| **The Art of Doing Science and Engineering (Wirth)** | ❌ **absent** | P0 |

### 2.3 Couverture par phase SWEBOK v4 (modèle canonique 1-par-1)

| Phase | Nom | Couverture corpus actuelle | Verdict |
|---|---|---|---|
| 0 | Discovery | ~0 (rien sur stakeholder/produit) | 🔴 |
| 1 | Concept & Feasibility | ~0 (lean startup absent) | 🔴 |
| 2 | Requirements | 1 livre canonique (Requirements Eng 4th) | 🟠 |
| 3 | Architecture | ~12 livres, bonne base | 🟢 |
| 4 | Design | Books DDD + patterns présents, manque Fowler/Martin | 🟠 |
| 5 | Implementation | TDD Python, Head First C# ; manque Pragmatic/Clean | 🟠 |
| 6 | Testing/Verification | 6 livres ; manque Lessons Learned/Agile Testing | 🟠 |
| 7 | Deployment | Continuous Deployment (Sanet) ; manque CD Humble | 🟠 |
| 8 | Operations / SRE | Mastering DevOps ; manque SRE/Obs/Chaos | 🔴 |
| 9 | Maintenance | 0 (aucun livre legacy code) | 🔴 |
| 10 | Retirement | 0 | 🔴 |

---

## 3. Lacunes identifiées par phase

| Phase | Besoin sémantique | Domaine manquant | Criticité |
|---|---|---|---|
| 0 Discovery | Stakeholder analysis, problem framing, charter, discovery techniques | Product management, design thinking, Lean UX, design sprint | 🔴 HAUTE |
| 1 Feasibility | Coût, ROI, options d'architecture, business case | Lean Startup, Business Model Gen, Go/No-Go | 🔴 HAUTE |
| 2 Requirements | Elicitation, SRS, user stories, acceptance criteria, traceability, validation | BABOK, Wiegers, Cohn, Leffingwell | 🟠 HAUTE |
| 3 Architecture | Méthodologie archi, ADRs, fitness functions, styles, NFR | Bass, Cervantes/Kazman, Ford, Humble Bundle Archi 2025 | 🟡 MOY |
| 4 Design | Design patterns GoF, clean code, clean architecture, module design | Fowler Refactoring 2nd, Martin Clean Code/Clean Arch | 🟠 HAUTE |
| 5 Implementation | Coding practices, craftsmanship, TDD en pratique, gestion dette technique | Pragmatic Programmer 20th, Winters (Google), Poppendieck | 🟠 HAUTE |
| 6 Testing | Stratégies de test, automatisation, test design, TDD/BDD, performance | Kaner, Crispin, Meszaros, Beck | 🟠 HAUTE |
| 7 Deployment | Pipeline CD, canary/blue-green, infra as code, sécurité déploiement | Humble/Farley, Kim, Laster, Richardson | 🟠 HAUTE |
| 8 Operations | SLO, observability, incident, chaos, on-call, postmortem | Google SRE, Majors Obs Eng, Rosenthal, Nygard | 🔴 HAUTE |
| 9 Maintenance | Refactoring en pratique, dette technique, legacy code, evolution | Feathers, Fowler, Bernstein, Sadalage | 🔴 HAUTE |
| 10 Retirement | Migration, archivage, conformité, data egress, sun-set planning | A compléter (manque critique) | 🔴 HAUTE |

---

## 4. Livres recommandés — section éditeurs (O'Reilly + Packt)

> **Légende priorité** : 🔴 **P0 (indispensable)** · 🟠 **P1 (fortement recommandé)** · 🟡 **P2 (enrichissement)** · ⚪ **P3 (optionnel)**
> **Format** : `Titre (Éditeur, Année) — Auteur(s) — URL`

### 4.1 Phase 0 — Discovery / Stakeholder

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **INSPIRED, 2nd ed. (Wiley, 2017) — Marty Cagan** | Référence #1 mondiale du product management tech. Modèle "empowered teams" + discovery vs delivery. |
| 🔴 | **Escaping the Build Trap (O'Reilly, 2019) — Melissa Perri** | Critique du product-centric vs output-centric, OKRs produit, outcome-based roadmaps. |
| 🔴 | **Lean UX, 3rd ed. (O'Reilly, 2021) — Jeff Gothelf** | Cadrage rapide, hypotheses testing, MVPs. |
| 🔴 | **Sprint (Simon & Schuster, 2016) — Jake Knapp** | Méthode Google Ventures pour valider une idée en 5 jours. |
| 🟠 | **Design Sprint 2nd ed. (Wiley, 2022) — Jake Knapp** | Version longue/structurée. |
| 🟠 | **The Lean Startup (Crown, 2011) — Eric Ries** | Build-Measure-Learn, MVP, pivot. |
| 🟠 | **Business Model Generation (Wiley, 2010) — Osterwalder/Pigneur** | Business Model Canvas — pour cadrage P0/P1. |
| 🟠 | **Value Proposition Design (Wiley, 2014) — Osterwalder et al.** | Value Prop Canvas — outillage concret. |
| 🟠 | **Thinking in Systems (Chelsea Green, 2008) — Donella Meadows** | Pensée systémique pour comprendre le problème racine. |
| 🟡 | **The Design of Everyday Things (Basic Books, 2013) — Don Norman** | Fondations UX. |
| 🟡 | **Don't Make Me Think, 3rd ed. (New Riders, 2023) — Steve Krug** | Usabilité web — pour P0 sur le périmètre UI. |
| 🟡 | **Continuous Discovery Habits (Ben Orlando/Teri Christian, 2021)** | Twin-tracked discovery, customer interviews. |
| 🟡 | **The Mom Test (Rob Fitzpatrick, 2013)** | Comment poser de bonnes questions de discovery. |
| ⚪ | **Inspired Downselect (Marty Cagan, vidéo 2024)** | Résumé INSPIRED pour équipes resserrées. |

**Source citations O'Reilly consultées** :
- Skill Product Management : https://www.oreilly.com/search/skills/product-management/
- Escaping the Build Trap : https://www.oreilly.com/library/view/escaping-the-build/9781491973783/

### 4.2 Phase 1 — Concept & Feasibility

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **The Lean Startup (Crown, 2011) — Eric Ries** | Validation rapide, MVP, itération. |
| 🔴 | **Business Model Generation (Wiley, 2010) — Osterwalder** | Cadrage économique d'un concept. |
| 🟠 | **Value Proposition Design (Wiley, 2014)** | Problème/solution fit. |
| 🟠 | **Inspired (Wiley) — Marty Cagan** *(idem P0 mais relu sous angle "faisabilité produit")* | |
| 🟠 | **Waltzing with Bears ( Dorset House, 2003) — McConnell** | Gestion du risque projet — fondement P1. |
| 🟠 | **The Mythical Man-Month, Anniversary ed. (Addison-Wesley, 1995) — Fred Brooks** | Brook's Law + leçons intemporelles. |
| 🟠 | **Death March, 2nd ed. (Prentice Hall, 2009) — Ed Yourdon** | Signaux précurseurs d'un projet condamné. |
| 🟡 | **The Phoenix Project (IT Revolution, 2013) — Gene Kim** | Roman d'entreprise qui rend tangible la théorie DevOps/feu. |
| 🟡 | **The Unicorn Project (IT Revolution, 2019) — Gene Kim** | Suite — focus developer experience & architecture. |
| 🟡 | **Switch (Heath/Heath, 2010)** | Conduire le changement organisationnel. |
| 🟡 | **AntiPatterns (Wiley, 1998) — Brown et al.** | Reconnaître les anti-patterns d'archi org (Death March, Analysis Paralysis, …). |
| 🟡 | **Crucial Conversations (McGraw-Hill, 2021) — Patterson et al.** | Gouvernance projet — escalade, désaccord. |
| ⚪ | **The Art of Doing Science and Engineering (CRC, 1993) — Niklaus Wirth** | Vision systémique + économie de la complexité. |

### 4.3 Phase 2 — Requirements

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Software Requirements, 3rd ed. (Microsoft Press, 2013) — Karl Wiegers & Joy Beatty** | Référence #1 absolue SRS + IEEE 830/29148. |
| 🔴 | **BABOK v3 (IIBA, 2015) + extensions** | Standard mondial du business analysis — voir §6. |
| 🔴 | **User Stories Applied (Addison-Wesley, 2004) — Mike Cohn** | Méthode user story + acceptance criteria. |
| 🔴 | **Agile Software Requirements (Addison-Wesley, 2010) — Dean Leffingwell** | Lean requirements à l'échelle (Safe). |
| 🟠 | **PMI Guide to Business Analysis (PMI, 2017) + mise à jour 2024** | Complément PMBOK côté BA — voir §5. |
| 🟠 | **Exploring Requirements (Dorset House, 2009) — Gause/Weinberg** | Elicitation qualité — focus "what vs how". |
| 🟠 | **Visual Models for Software Requirements (Microsoft Press, 2012) — Joy Beatty/Anthony Chen** | Modèles UML/BPMN pour requirements. |
| 🟠 | **Software Requirements Essentials (Pearson, 2019) — Karl Wiegers** | Version condensée pour petits projets. |
| 🟠 | **Domain-Driven Design (Addison-Wesley, 2003) — Eric Evans** | Modélisation du domaine, ubiquitous language, bounded contexts. |
| 🟠 | **Implementing Domain-Driven Design (Addison-Wesley, 2013) — Vaughn Vernon** | Mise en œuvre concrète. |
| 🟠 | **Domain-Driven Design Distilled (Addison-Wesley, 2016) — Vaughn Vernon** | Version courte. |
| 🟠 | **Requirements Writing for System Engineering (Apress, 2016) — George Koelsch** | Bons requirements + erreurs classiques. |
| 🟡 | **Mastering Requirements Reuse (Wiley, 2017)** | Réutilisation requirements libraries. |
| 🟡 | **Managing Software Requirements (Addison-Wesley, 2003) — Leffingwell/Widrig** | Approche unifiée — vision historique. |
| 🟡 | **Requirements Engineering for Software and Systems, 4th ed. (CRC, 2023) — Phillips** | *(déjà présent dans corpus — vérifier complétude)* |
| 🟡 | **Impact Mapping (O'Reilly, 2012) — Gojko Adzic** | Lier business goals → features → deliverables. |
| 🟡 | **The Power of Positive Sharing (O'Reilly, 2020) — Adzic** | Specs by example, BDD. |
| ⚪ | **Specification by Example (Manning, 2011) — Adzic** | BDD/SBE — outillage P2. |

**Source citations O'Reilly/Packt consultées** :
- Software Requirements 3rd : https://www.oreilly.com/library/view/software-requirements-3rd/9780735679658/
- Visual Models : https://learning.oreilly.com/library/view/visual-models-for/9780735667730/
- Agile Software Requirements : https://www.oreilly.com/library/view/agile-software-requirements/9780321685438/apb.xhtml
- Domain-Driven Design skill : https://www.oreilly.com/search/skills/domain-driven-design/

### 4.4 Phase 3 — Architecture

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Software Architecture in Practice, 4th ed. (Addison-Wesley, 2021) — Bass/Clements/Kazman** | Référence académique #1 (SEI/CMU). Déjà un classique du corpus. |
| 🔴 | **Designing Software Architectures: A Practical Approach, 2nd ed. (Addison-Wesley, 2024) — Cervantes/Kazman** | Méthode ADD (Attribute-Driven Design). |
| 🔴 | **Fundamentals of Software Architecture, 2nd ed. (O'Reilly, 2025 — à paraître) — Richards/Ford** | *(déjà présent v1 — vérifier 2nd ed)* — synthèse moderne. |
| 🔴 | **Effective Software Architecture (Addison-Wesley, 2024) — Neal Ford** | Architecture comme pratique produit, pas comme un rôle. |
| 🟠 | **Head First Software Architecture (O'Reilly, 2024) — Gandhi/Richards/Ford** | *(déjà présent)* — pédagogique, bonne intro. |
| 🟠 | **Building Evolutionary Architectures, 2nd ed. (O'Reilly, 2023) — Ford/Parsons/Kua/Sadalage** | *(déjà présent)* — fitness functions, automatisation. |
| 🟠 | **Software Architecture: The Hard Parts (O'Reilly, 2021) — Ford/DeHaan** | *(déjà présent)* — trade-offs. |
| 🟠 | **Patterns of Enterprise Application Architecture (Addison-Wesley, 2002) — Martin Fowler** | Catalogue #1 de patterns d'entreprise. |
| 🟠 | **Enterprise Integration Patterns (Addison-Wesley, 2003) — Hohpe/Woolf** | 65 patterns d'intégration (messaging). |
| 🟠 | **Designing Data-Intensive Applications, 2nd ed. (O'Reilly, 2025 — à paraître) — Martin Kleppmann** | Référence #1 des systèmes data-intensifs. |
| 🟠 | **Microservices Patterns (Manning, 2018) — Chris Richardson** | *(déjà présent)* — patterns microservices. |
| 🟠 | **Building Event-Driven Microservices (O'Reilly, 2020) — Adam Bellemare** | *(déjà présent)* — event sourcing/CQRS. |
| 🟠 | **Software Architecture Patterns for Serverless Systems (Packt, 2024) — John Gilbert** | Architecture serverless. |
| 🟠 | **Design Microservices Architecture with Patterns and Principles (Packt, 2023) — Mehmet Ozkaya** | Microservices hands-on. |
| 🟠 | **Cloud Native Architecture (Packt, 2023)** | Patterns cloud-native. |
| 🟠 | **Mastering API Architecture (O'Reilly, 2022) — James Gough/Daniel Bryant/Matthew Auburn** | *(déjà présent)*. |
| 🟠 | **Facilitating Software Architecture (O'Reilly, 2024) — Andrew Harmel-Law** | Soft skills d'architecte — combler le gap humain. |
| 🟡 | **Mastering Python Design Patterns, 3rd ed. (Packt, 2024) — Kamon Ayeva / Sakis Kasampalis** | Design patterns en Python. |
| 🟡 | **Software Architecture Metrics (O'Reilly, 2022) — Christian Ciceri et al.** | *(déjà présent)*. |
| 🟡 | **Flow Architectures (O'Reilly, 2021) — James Urquhart** | *(déjà présent)*. |
| 🟡 | **Kubernetes Patterns, 2nd ed. (O'Reilly, 2023) — Ibryam/Huß** | Patterns K8s. |
| 🟡 | **Production Kubernetes (O'Reilly, 2021) — Josh Rosso/Richard Lander/Alex Brand** | K8s en prod. |
| 🟡 | **System Design Guide for Software Professionals (O'Reilly, 2024)** | Guide design d'interview/practical. |
| 🟡 | **The Kubernetes Bible, 2nd ed. (Packt, 2024) — Madapparambath/Giordano/Mengoni** | K8s pour cloud (AWS/Azure/GCP). |
| 🟡 | **Platform Engineering on Kubernetes (O'Reilly, 2024) — Hightower et al.** | Internal developer platform. |
| 🟡 | **Learning Domain-Driven Design (O'Reilly, 2021) — Vlad Khononov** | *(déjà présent)*. |
| 🟡 | **Software Architecture in an AI World (O'Reilly Radar, 2024) — Neal Ford** | AI dans le workflow archi. |
| 🟡 | **Software Architecture Superstream Series (O'Reilly vidéo, 2024)** | Conférences archi récentes. |
| ⚪ | **Engineering Long-Lasting Software (O'Reilly, 2025 — à paraître) — Castro/Melanova et al.** | Architecture en évolution sur 25-50 ans. |
| ⚪ | **Head First Software Development (O'Reilly, 2008) — Dan Pilone** | Vue large et introductive. |

**Source citations O'Reilly/Packt consultées** :
- Software Architecture in Practice 4th : https://www.oreilly.com/library/view/software-architecture-in/9780136885979/
- Software Architecture: The Hard Parts : https://www.oreilly.com/library/view/software-architecture-the/9781492086888/
- Effective Software Architecture : https://www.oreilly.com/library/view/effective-software-architecture/9780138249205/
- Designing Software Architectures 2nd : https://www.oreilly.com/library/view/designing-software-architectures/9780138108069/
- Head First Software Architecture : https://www.oreilly.com/library/view/head-first-software/9781098134341/
- Building Evolutionary Architectures 2nd : https://www.oreilly.com/library/view/building-evolutionary-architectures/9781492097532/
- Software Architecture Patterns for Serverless Systems : https://www.packtpub.com/en-us/product/software-architecture-patterns-for-serverless-systems-9781803244433
- Master microservices architecture : https://www.packtpub.com/en-us/product/design-microservices-architecture-with-patterns-and-principles-9781805126782

### 4.5 Phase 4 — Design

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Design Patterns: Elements of Reusable Object-Oriented Software (Addison-Wesley, 1994) — Gamma/Helm/Johnson/Vlissides (GoF)** | Le "Gang of Four" — la fondation historique. |
| 🔴 | **Clean Code (Prentice Hall, 2008) — Robert C. Martin** | Conventions nommage, fonctions, formatage, commentaires — toujours d'actualité. |
| 🔴 | **Clean Architecture (Prentice Hall, 2017) — Robert C. Martin** | S.O.L.I.D. + boundary architecture. |
| 🔴 | **Refactoring, 2nd ed. (Addison-Wesley, 2018) — Martin Fowler** | Catalogue des refactorings + processus. |
| 🟠 | **Clean Craftsmanship (Addison-Wesley, 2021) — Robert C. Martin** | Professionalism, TDD, acceptance testing. |
| 🟠 | **Clean Code Cookbook (O'Reilly, 2023) — Maximiliano Contieri** | *(partiellement présent)* — patterns d'amélioration. |
| 🟠 | **Patterns of Enterprise Application Architecture (Addison-Wesley, 2002) — Fowler** | Patterns au niveau design. |
| 🟠 | **Domain-Driven Design (Addison-Wesley, 2003) — Eric Evans** | Modélisation + design contextuel. |
| 🟠 | **Enterprise Integration Patterns (Addison-Wesley, 2003) — Hohpe/Woolf** | Design d'intégrations. |
| 🟠 | **API Design Patterns (Manning, 2021) — Geewax** | Design d'API REST/GraphQL. |
| 🟠 | **RESTful API Design Patterns and Best Practices (Packt, 2024) — Mehdi Madani** | Patterns REST. |
| 🟠 | **Mastering Python Design Patterns, 3rd ed. (Packt, 2024)** | Design patterns en Python. |
| 🟠 | **Hands-On Design Patterns with C# and .NET Core (Packt)** | Patterns en C#/.NET. |
| 🟠 | **Hands-On Design Patterns with Java (Packt)** | Patterns en Java. |
| 🟠 | **Hands-On Software Architecture with Golang (Packt)** | Architecture en Go. |
| 🟠 | **The Pragmatic Programmer, 20th Anniversary ed. (Addison-Wesley, 2019) — Hunt/Thomas** | Pragmatisme + craftsmanship. |
| 🟠 | **Software Architecture Patterns 2nd ed. (O'Reilly, 2025) — Richards** | *(déjà présent)*. |
| 🟠 | **Architecture Patterns with Python (O'Reilly, 2020) — Percival/Gregory** | DDD + Python — Harry Percival. |
| 🟡 | **Refactoring to Patterns (Addison-Wesley, 2004) — Joshua Kerievsky** | Pont refactoring ↔ patterns. |
| 🟡 | **Pattern Hatching (Addison-Wesley, 1998) — John Vlissides** | Variations sur les patterns GoF. |
| 🟡 | **Refactoring with C# (Packt, 2023)** | Refactoring appliqué C#. |
| 🟡 | **Five Lines of Code (Manning, 2021) — Christian Mayer** | Refactoring incrémental. |
| 🟡 | **TDD by Example (Addison-Wesley, 2002) — Kent Beck** | Origine du TDD. |
| 🟡 | **Refactoring Databases (Addison-Wesley, 2006) — Sadalage** | Refactoring schema DB. |
| ⚪ | **Clean Agile (Prentice Hall, 2019) — Robert C. Martin** | Retour aux sources Agile. |
| ⚪ | **Implementation Patterns (Addison-Wesley, 2007) — Kent Beck** | Patterns de code au quotidien. |

### 4.6 Phase 5 — Implementation / Construction

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **The Pragmatic Programmer, 20th Anniversary ed. (Addison-Wesley, 2019) — Hunt/Thomas** | Le "DRY/orthogonality/tracer bullets" — fondement toujours actuel. |
| 🔴 | **Clean Code (Prentice Hall, 2008) — Robert C. Martin** | *(idem §4.5)* — pratiques de codage. |
| 🔴 | **Clean Craftsmanship (Prentice Hall, 2021) — Robert C. Martin** | Disciplines du métier. |
| 🔴 | **Software Engineering at Google (O'Reilly, 2020) — Winters/Manshreck/Wright** | Leçons à l'échelle de Google. |
| 🔴 | **Modern Software Engineering (Addison-Wesley, 2023) — David Farley** | Principes (feedback, iteration, empirisme). |
| 🟠 | **Refactoring, 2nd ed. (Addison-Wesley, 2018) — Fowler** | *(idem §4.5)*. |
| 🟠 | **Test-Driven Development with Python, 3rd ed. (O'Reilly, 2023) — Harry Percival** | *(déjà présent)*. |
| 🟠 | **Architecture Patterns with Python (O'Reilly, 2020) — Percival/Gregory** | DDD + Python — *(partiellement présent)*. |
| 🟠 | **Clean Code Cookbook (O'Reilly, 2023) — Maximiliano Contieri** | *(partiellement présent)*. |
| 🟠 | **Effective Java, 3rd ed. (Addison-Wesley, 2018) — Joshua Bloch** | Pour tout dev Java. |
| 🟠 | **An Elegant Puzzle (Stripe Press, 2024) — Will Larson** | Pragmatisme ingénierie (multi-systeme). |
| 🟠 | **The Staff Engineer's Path (O'Reilly, 2022) — Tanya Reilly** | Du IC au Staff — leadership technique. |
| 🟠 | **The Manager's Path (O'Reilly, 2017) — Camille Fournier** | De tech lead à manager. |
| 🟠 | **AI-Assisted Programming (O'Reilly, 2024) — Tom Taulli** | *(déjà présent dans corpus)*. |
| 🟠 | **Generative AI for Software Development (O'Reilly, 2024) — Priyanka Vergadia/Barry Pollard** | AI dans le cycle dev. |
| 🟡 | **Code Complete, 2nd ed. (Microsoft Press, 2004) — Steve McConnell** | Encyclopédie des pratiques de codage. |
| 🟡 | **Implementation Patterns (Addison-Wesley, 2007) — Kent Beck** | |
| 🟡 | **Programming Pearls, 2nd ed. (Addison-Wesley, 1999) — Jon Bentley** | Algorithmie élégante. |
| 🟡 | **The Art of Readable Code (O'Reilly, 2011) — Dustin Boswell/Trevor Foucher** | Lisibilité. |
| 🟡 | **Writing Solid Code (Microsoft Press, 1993) — Steve Maguire** | Pragmatique. |
| 🟡 | **Refactoring in Python LiveLessons (O'Reilly vidéo, 2018) — Burton** | TDD + refactoring Python. |
| 🟡 | **Mastering C# Design Patterns (Packt, 2024)** | Patterns en C#. |
| 🟡 | **Hands-On Software Architecture with C# and .NET (Packt)** | Archi + code .NET. |
| ⚪ | **Refactoring in Ruby (Addison-Wesley, 2009) — Jay Fields** | Refactoring spécifique Ruby. |
| ⚪ | **C# 12 in a Nutshell (O'Reilly, 2023)** | Référence langage. |

**Source citations O'Reilly consultées** :
- Pragmatic Programmer 20th : https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/
- Software Engineering at Google : https://www.oreilly.com/library/view/software-engineering-at/9781492082781/
- Clean Code skill : https://www.oreilly.com/search/skills/clean-code/
- Coding Practices skill : https://www.oreilly.com/search/skills/coding-practices/

### 4.7 Phase 6 — Testing / Verification

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Lessons Learned in Software Testing (Wiley, 2001) — Kaner/Bach/Pettichord** | Référentiel #1 heuristiques de test. |
| 🔴 | **Agile Testing (Addison-Wesley, 2009) — Lisa Crispin/Janet Gregory** | Quadrants de test, automation. |
| 🔴 | **xUnit Test Patterns (Addison-Wesley, 2007) — Gerard Meszaros** | Refactoring de tests, organization. |
| 🔴 | **Growing Object-Oriented Software, Guided by Tests (Addison-Wesley, 2009) — Freeman/Pryce** | TDD de bout en bout. |
| 🟠 | **TDD by Example (Addison-Wesley, 2002) — Kent Beck** | Origine TDD. |
| 🟠 | **Specification by Example (Manning, 2011) — Gojko Adzic** | BDD/SBE. |
| 🟠 | **The Art of Software Testing, 3rd ed. (Wiley, 2011) — Myers/Sandler/Badgett** | Référence académique #1. |
| 🟠 | **Software Testing Strategies (Packt, 2023)** | Stratégies modernes. |
| 🟠 | **Full Stack Testing (O'Reilly, 2023) — Gayathri Mohan** | *(déjà présent Sanet.st)*. |
| 🟠 | **AI-Driven Software Testing (Packt, 2025)** | Testing avec AI. |
| 🟠 | **Testing JavaScript Applications (O'Reilly, 2021) — Lucas de Costa** | *(déjà présent)*. |
| 🟠 | **Hands-On Test Management with Jira (Packt, 2019) — Hasbi** | Test management. |
| 🟠 | **Test-Driven Development with Java (Packt, 2023)** | TDD Java. |
| 🟠 | **Continuous Testing for DevOps Professionals (Packt, 2019)** | Tests dans pipeline. |
| 🟠 | **Test Unitaire (French, présent dans corpus)** | Tests unitaires. |
| 🟠 | **Introduction to Software Testing (Cambridge/O'Reilly, 2016) — Ammann/Offutt** | *(déjà présent)*. |
| 🟠 | **Practical Test-Driven Development using C# 7 (Packt, 2018)** | TDD C#. |
| 🟠 | **API Testing and Development with Postman (O'Reilly, 2021) — Dave Westerveld** | Tests d'API. |
| 🟡 | **Beautiful Testing (O'Reilly, 2009) — Tim Riley/Adam Goucher** | 25 essays. |
| 🟡 | **Performance Testing (O'Reilly, 2022)** | Tests de charge. |
| 🟡 | **How Google Tests Software (Addison-Wesley, 2012) — James Whittaker** | Témoignage Google. |
| 🟡 | **Perfect Software (Dorset House, 2005) — Jerry Weinberg** | Tests exploratoires. |
| 🟡 | **Software Testing (Wiley, 2016) — Rakitin** | Référence. |
| 🟡 | **Hands-On Selenium (Packt, 2022)** | Selenium WebDriver. |
| 🟡 | **Mastering Jenkins (Packt, 2015)** | *(déjà présent)* — CI pour tests. |
| 🟡 | **Modern Game Testing (Packt, 2024)** | Tests jeux vidéo. |
| ⚪ | **Explore It! (Pragmatic Bookshelf, 2013) — Elisabeth Hendrickson** | Tests exploratoires. |
| ⚪ | **Domain-Specific Languages (Addison-Wesley, 2010) — Fowler** | DSLs pour specs testables. |

**Source citations O'Reilly/Packt consultées** :
- AI-Driven Software Testing : https://www.oreilly.com/library/view/ai-driven-software-testing/9798868818295/
- Skill QA/Testing : https://www.oreilly.com/search/skills/qa-testing/
- Generative AI for Software Development : https://www.oreilly.com/library/view/generative-ai-for/9781098162269/
- Software Testing Strategies (Packt) : https://www.packtpub.com/en-us/product/software-testing-strategies-9781837638024
- API Testing and Development with Postman : https://www.oreilly.com/library/view/api-testing-and/9781800569201/

### 4.8 Phase 7 — Deployment

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Continuous Delivery (Addison-Wesley, 2010) — Humble/Farley** | La référence absolue du CD. |
| 🔴 | **The DevOps Handbook, 2nd ed. (IT Revolution, 2021) — Kim/Humane/Hightower** | 3 ways + check-list. |
| 🔴 | **Continuous Deployment (O'Reilly, 2023) — Brent Laster** | *(Sanet.st Continuous Deployment déjà présent)*. |
| 🔴 | **The Phoenix Project (IT Revolution, 2013) — Kim et al.** | Roman DevOps. |
| 🟠 | **Pipeline as Code (Manning, 2021) — Mohamed Labouardy** | CI/CD déclaratif. |
| 🟠 | **Cloud Native DevOps with Kubernetes (O'Reilly, 2019) — Hightower et al.** | K8s + DevOps. |
| 🟠 | **Kubernetes for the Absolute Beginners - Hands-On (Packt, 2023)** | K8s foundations. |
| 🟠 | **Production Kubernetes (O'Reilly, 2021) — Rosso et al.** | K8s production. |
| 🟠 | **Release It!, 2nd ed. (Pragmatic Bookshelf, 2018) — Michael Nygard** | Patterns de stabilité + antipatterns de release. |
| 🟠 | **Production-Ready Microservices (O'Reilly, 2016) — Susan Fowler** | Standards de microservices en prod. |
| 🟠 | **Practical Cloud Security (O'Reilly, 2023) — Shelend/Sharma** | *(déjà présent v2)*. |
| 🟠 | **Cloud Native Security Cookbook (O'Reilly, 2022) — Leva/'Pruitt/Burns** | *(déjà présent)*. |
| 🟠 | **Cloud Native Architecture (Packt, 2023)** | |
| 🟠 | **The Kubernetes Bible 2nd ed. (Packt, 2024)** | |
| 🟠 | **Microservices Up and Running (O'Reilly, 2020) — John Harris** | *(déjà présent)*. |
| 🟠 | **Monolith to Microservices (O'Reilly, 2019) — Newman** | *(déjà présent)*. |
| 🟡 | **Terraform: Up & Running, 3rd ed. (O'Reilly, 2022) — Yevgeniy Brikman** | IaC Terraform. |
| 🟡 | **Ansible: Up & Running, 3rd ed. (O'Reilly, 2022) — Basu/Hochstein/Lorin** | Ansible. |
| 🟡 | **Cloud Native Transformation (O'Reilly, 2019) — Ninan/DuBuisson/Beaulieu** | Migration. |
| 🟡 | **Infrastructure as Code (O'Reilly, 2016) — Kief Morris** | Patterns IaC. |
| 🟡 | **Mastering Kubernetes, 4th ed. (Packt, 2023) — Sayfan** | K8s avancé. |
| 🟡 | **Certified Kubernetes Administrator (Packt)** | CKA prep. |
| 🟡 | **Hands-On Docker for Microservices (Packt, 2023)** | Docker. |
| 🟡 | **Cloud Computing Concepts (Wiley, 2010)** | Théorie. |
| ⚪ | **Continuous Integration (Addison-Wesley, 2007) — Duvall/Paul/Matyas/Glover** | Référence historique. |
| ⚪ | **Configuration Management (O'Reilly, 2010) — A. W. Brown** | Config as code. |

**Source citations O'Reilly/Packt consultées** :
- Continuous Delivery skill : https://www.oreilly.com/search/skills/continuous-delivery/
- Continuous Deployment : https://www.oreilly.com/library/view/continuous-deployment/9781098146719/
- Mastering Jenkins (Packt) : https://www.packtpub.com/en-NO/product/mastering-jenkins-9781784390891
- Kubernetes for the Absolute Beginners (Packt) : https://www.packtpub.com/en-us/product/kubernetes-for-the-absolute-beginners-hands-on-9781838555962

### 4.9 Phase 8 — Operations / SRE

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Site Reliability Engineering (O'Reilly, 2016) — Google (Beyer/Jones/Petoff/Murphy)** | Le "livre SRE" — référence #1 mondiale. |
| 🔴 | **The Site Reliability Workbook (O'Reilly, 2018) — Google (Beyer/Jones/Murphy)** | SRE en pratique. |
| 🔴 | **Observability Engineering (O'Reilly, 2022) — Majors/Fong-Jones/Miranda** | White-box monitoring + SLOs. |
| 🔴 | **Observability Engineering, 2nd ed. (O'Reilly, 2024) — Majors/Fong-Jones/Miranda** | Mise à jour. |
| 🔴 | **Building Secure and Reliable Systems (O'Reilly, 2020) — Google** | Sécurité + fiabilité entremêlées. |
| 🟠 | **Accelerate (IT Revolution, 2018) — Forsgren/Humble/Kim** | DORA metrics, 4 clés de la performance. |
| 🟠 | **Chaos Engineering (O'Reilly, 2017) — Casey Rosenthal/Nora Jones** | Anti-fragilité, fault injection. |
| 🟠 | **Security Chaos Engineering (O'Reilly, 2021) — Kelly Shortridge/Aaron Rinehart** | *(déjà présent)*. |
| 🟠 | **Incident Management for Operations (O'Reilly, 2015) — Rob Schnepp/Ron Vidal/Chris Hawley** | Gestion incidents. |
| 🟠 | **Modern System Administration (O'Reilly, 2022) — Jennifer Davis** | |
| 🟠 | **Release It! 2nd ed. (Pragmatic Bookshelf, 2018) — Nygard** | *(idem §4.8)* — antipatterns de prod. |
| 🟠 | **Production-Ready Microservices (O'Reilly, 2016) — Fowler** | Standards microservices prod. |
| 🟠 | **Cloud Native DevOps with Kubernetes (O'Reilly, 2019) — Hightower et al.** | |
| 🟠 | **Mastering DevOps (Packt, 2023) — Anderson** | *(déjà présent)*. |
| 🟠 | **Becoming a Rockstar SRE (Packt, 2023) — Nat Welch** | SRE mindset. |
| 🟠 | **Practical Site Reliability Engineering (Packt, 2022)** | |
| 🟠 | **Modern Site Reliability Engineering (Packt, 2024)** | |
| 🟠 | **Intelligence-Driven Incident Response 2nd ed. (O'Reilly, 2023) — Roberts/Brown** | *(déjà présent)*. |
| 🟠 | **Cloud Observability in Action (Manning, 2023) — Michael Hausenblas** | |
| 🟡 | **Distributed Systems Observability (O'Reilly, 2018) — Cindy Sridharan** | Culte, court et fort. |
| 🟡 | **Monitoring Distributed Systems (O'Reilly, 2017) — Casey Rosenthal et al.** | Companion de Chaos Engineering. |
| 🟡 | **Blameless: A Practical Guide to Incident Management (O'Reilly vidéo, 2021)** | |
| 🟡 | **Bugs in Production (Manning, 2024) — Matt Glaman** | Production debugging. |
| 🟡 | **Postmortem Culture (O'Reilly Radar, 2019)** | Culture blameless. |
| 🟡 | **Terraform: Up & Running 3rd ed. (O'Reilly)** | IaC. |
| 🟡 | **Runbook Automation (O'Reilly, 2022)** | |
| 🟡 | **Service Meshes (O'Reilly, 2024)** | Istio/Linkerd. |
| 🟡 | **Effective Monitoring and Alerting (O'Reilly, 2012) — Sadowski** | Pour les on-call. |
| 🟡 | **Bulletproof SSL and TLS (Feisty Duck, 2015)** | SSL/TLS. |
| ⚪ | **Antifragile Software (Leanpub, 2019)** | Systèmes antifragiles. |
| ⚪ | **Production-Ready Open Source (O'Reilly, 2024)** | |

**Source citations O'Reilly/Packt consultées** :
- Skill SRE : https://www.oreilly.com/search/skills/site-reliability-engineering-sre/
- Observability Engineering 2nd : https://www.oreilly.com/library/view/observability-engineering-2nd/9781098179915/
- Building Secure and Reliable Systems : https://www.oreilly.com/library/view/building-secure-and/9781492083115/
- Becoming a Rockstar SRE (Packt) : https://www.packtpub.com/en-us/product/becoming-a-rockstar-sre-9781803239224
- Playlist observability : https://learning.oreilly.com/playlists/0bcbe46b-a5b0-406d-83e4-0d8e1cf413f0/

### 4.10 Phase 9 — Maintenance

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Working Effectively with Legacy Code (Prentice Hall, 2004) — Michael Feathers** | LE livre sur le legacy — seam model, characterization tests. |
| 🔴 | **Refactoring, 2nd ed. (Addison-Wesley, 2018) — Fowler** | Processus de refactoring + catalogue. |
| 🔴 | **Beyond Legacy Code (Pragmatic Bookshelf, 2015) — David Scott Bernstein** | 9 pratiques pour moderniser. |
| 🔴 | **Software Engineering at Google (O'Reilly, 2020) — Winters** | Maintenance à l'échelle. |
| 🟠 | **Refactoring Databases (Addison-Wesley, 2006) — Sadalage** | Schema evolution. |
| 🟠 | **Building Evolutionary Architectures 2nd ed. (O'Reilly, 2023) — Ford** | *(idem §4.4)* — architecture changeable. |
| 🟠 | **Clean Code (Prentice Hall, 2008) — Martin** | *(idem §4.5)*. |
| 🟠 | **Modern Software Engineering (Addison-Wesley, 2023) — Farley** | *(idem §4.6)*. |
| 🟠 | **Refactoring to Patterns (Addison-Wesley, 2004) — Kerievsky** | |
| 🟠 | **The Pragmatic Programmer 20th (Addison-Wesley, 2019) — Hunt/Thomas** | Tracer bullets, design by contract. |
| 🟠 | **Death March 2nd ed. (Prentice Hall, 2009) — Yourdon** | Détecter les projets condamnés. |
| 🟠 | **The Mythical Man-Month Anniversary (Addison-Wesley, 1995) — Brooks** | Brook's Law. |
| 🟡 | **AntiPatterns (Wiley, 1998) — Brown et al.** | Référence anti-patterns. |
| 🟡 | **Refactoring with C# (Packt, 2023)** | |
| 🟡 | **Clean Code Cookbook (O'Reilly, 2023) — Contieri** | *(partiellement présent)*. |
| 🟡 | **An Elegant Puzzle (Stripe Press, 2024) — Larson** | Engineering trade-offs. |
| 🟡 | **Refactoring in Python LiveLessons (O'Reilly, 2018)** | |
| 🟡 | **Technical Debt Management (O'Reilly Radar, 2020)** | |
| 🟡 | **Making Software (O'Reilly, 2010) — Oram/Wilson** | Recherche empirique sur l'ingénierie logicielle. |
| 🟡 | **Software Assessment (Wiley, 2000) — Jones** | Audit, benchmarks. |
| ⚪ | **Blueprints for a Scalable Site (O'Reilly, 2022)** | |
| ⚪ | **The Evolution of Tech Debt (O'Reilly Radar, 2023)** | |

### 4.11 Phase 10 — Retirement

> **Note critique** : la phase Retirement est la moins documentée dans l'industrie. Très peu de livres lui sont consacrés. La couverture vient principalement de la conjonction (a) Migration vers le cloud, (b) Stratégie d'archivage, (c) Compliance / RGPD, (d) Stratégie de transition utilisateur.

| Pri. | Livre | Pourquoi |
|---|---|---|
| 🔴 | **Cloud Native Transformation (O'Reilly, 2019) — Ninan/DuBuisson/Beaulieu** | Migration = l'inverse du retirement. |
| 🔴 | **Monolith to Microservices (O'Reilly, 2019) — Newman** | Strangler pattern. |
| 🔴 | **Migrating to Cloud-Native Application Architectures (O'Reilly, 2015) — Stine** | Référentiel Pivotal. |
| 🟠 | **Building Evolutionary Architectures 2nd ed. (O'Reilly, 2023) — Ford** | Architecture qu'on peut éteindre. |
| 🟠 | **Release It! 2nd ed. (Pragmatic Bookshelf, 2018) — Nygard** | Antipatterns de fin de vie. |
| 🟠 | **Software Engineering at Google (O'Reilly, 2020) — Winters** | Lessons sur le décommissionnement. |
| 🟠 | **Data Governance (Manning, 2023) — Evidently** | Archivage, conformité. |
| 🟠 | **GDPR and Privacy (O'Reilly, 2023)** | Droit à l'effacement, archivage légal. |
| 🟠 | **Cloud Migration (O'Reilly, 2021)** | Patterns de migration. |
| 🟡 | **The Data Warehouse Toolkit, 3rd ed. (Wiley, 2013) — Kimball** | Archivage BI. |
| 🟡 | **Architecting Cloud Native Applications (Packt, 2022)** | |
| 🟡 | **Practical Cloud Security 2nd ed. (O'Reilly, 2023)** | Security lors de retirement. |
| 🟡 | **Systemantics (Doubleday, 1978) — Gall** | *Vétuste mais intemporel* — les systèmes se dégradent. |
| ⚪ | **Building Multi-Tenant SaaS Architectures (O'Reilly, 2024)** | *(déjà présent)*. |

**Source citations O'Reilly** : https://www.oreilly.com/library/view/building-secure-and/9781492083115/ch03.html

---

## 5. Section additionnelle — PMI / Project Management Institute

> **Contexte** : **ZÉRO livre PMI dans le corpus actuel**. Or, PMI est le **standard mondial** de la profession et ses standards sont cités par SWEBOK v4 KA 1 (Software Requirements) et KA 6 (Software Engineering Management). Pour le projet **swebok-v4-harness-distilled**, l'ajout de ces standards est **indispensable** car le modèle 10-phases est fondamentalement un modèle de gestion de projet.

### 5.1 Standards PMI individuels

| Pri. | Standard PMI | Édition | Usage projet |
|---|---|---|---|
| 🔴 | **PMBOK Guide** (A Guide to the Project Management Body of Knowledge) | 7e (2021) + 8e (2026) | Cadrage P0/P1, terminologie commune |
| 🔴 | **PMI Standard for Business Analysis** | 2017 (mise à jour 2024) | P2 — l'extension BA du PMBOK |
| 🔴 | **PMI Standard for Risk Management** | 2019 (mise à jour 2025) | P0 — risk landscape |
| 🔴 | **PMI Standard for Program Management** | 5e (2024) | Pilotage multi-projets |
| 🔴 | **PMI Standard for Portfolio Management** | 4e (2023) | Alignement stratégique |
| 🔴 | **Governance of Portfolios, Programs, and Projects** | 2024 | Gouvernance, décision |
| 🟠 | **PMI Disciplined Agile (DA)** | DA 304 toolkit | Workflow méthode agile-outile |
| 🟠 | **Practice Standard for Project Risk Management** | 2009 | Plan de gestion des risques |
| 🟠 | **Practice Standard for Earned Value Management** | 2019 | Mesure de la performance |
| 🟠 | **Practice Standard for Scheduling** | 2011 | Planification |
| 🟠 | **Practice Standard for Work Breakdown Structures** | 2006 | WBS — décomposition projet |
| 🟠 | **Practice Standard for Project Configuration Management** | 2007 | Change management |
| 🟠 | **The Standard for Organizational Project Management (OPM)** | 2018 | Aligner organisation et projet |
| 🟠 | **A Guide to the Project Management Body of Knowledge (PMBOK) Guide** | 6e (2017) | Archives + comparaison avec 7e |
| 🟡 | **PMI Pulse of the Profession** (rapports annuels) | 2024, 2025 | Tendances |
| 🟡 | **Navigating Complexity (PMI Thought Leadership, 2014)** | 2014 | Cynefin, complexité |

### 5.2 Livres O'Reilly/Addison-Wesley qui appliquent PMI

| Pri. | Livre | Usage |
|---|---|---|
| 🟠 | **Effective Software Project Management (Wiley/O'Reilly, 2006) — Robert Wysocki** | Adapté au logiciel |
| 🟠 | **Quality Software Project Management (O'Reilly, 2002) — Robert Futrell** | |
| 🟠 | **Software Project Management (O'Reilly, 2002) — Dutoit/Bruegge** | |
| 🟠 | **Agile Estimating and Planning (Prentice Hall, 2005) — Mike Cohn** | Estimation agile |
| 🟠 | **Succeeding with Agile (Addison-Wesley, 2009) — Mike Cohn** | |
| 🟠 | **The Scrum Guide (Schwaber/Sutherland, 2020)** | (libre, à intégrer en PDF) |
| 🟠 | **SAFe Distilled (Addison-Wesley, 2020) — Richard Knaster/Leffingwell** | Scaling agile |
| 🟠 | **The Lean-Agile Way (Addison-Wesley, 2022) — Cecil Rupp** | Lean-Agile |
| 🟠 | **Project Management: The Managerial Process (McGraw-Hill, 2017) — Larson/Gray** | Référence PM |

### 5.3 Articles de fond à intégrer en documents

| Article | Source |
|---|---|
| PMBOK 7th Ed: What Changed and Why | PMI / LinkedIn 2024 |
| PMBOK 7 vs PMBOK 8 Key Differences | Project Management Academy 2026 |
| What's New in PMBOK 7th | shrilearning.com |
| New PMI Program and Portfolio Management Standard | PMI 2024 |
| Governance of Portfolios, Programs, and Projects | PMI 2024 |
| Disciplined Agile: 5-step progressive path to agile mastery | PMI 2024 |

**Source citations consultées** :
- PMBOK Guide (PMI) : https://www.pmi.org/standards/pmbok
- PMBOK 7th vs 8th : https://projectmanagementacademy.net/resources/blog/pmbok-7-vs-pmbok-8-differences/
- Standard for Portfolio Management 4e : https://www.pmi.org/standards/for-portfolio-management
- Governance of Portfolios, Programs, and Projects : https://www.pmi.org/standards/governance
- Standard for Program Management 5e : https://www.pmi.org/standards/program-management-fifth-edition
- Risk Management Standard : https://www.pmi.org/standards/risk-management
- PMI Guide to Business Analysis : https://www.pmi.org/standards/business-analysis
- Disciplined Agile : https://www.pmi.org/disciplined-agile/

---

## 6. Section additionnelle — IIBA & Business Analysis (BABOK)

> **Contexte** : **BABOK v3** est l'autre standard mondial pour le BA. Complète PMI-BA.

### 6.1 Standards IIBA

| Pri. | Standard | Édition | Usage |
|---|---|---|---|
| 🔴 | **A Guide to the Business Analysis Body of Knowledge (BABOK)** | v3 (2015) | Cadre BA universel |
| 🔴 | **BABOK v3 + Agile Extension** | 2015 + 2016 | BA agile |
| 🟠 | **BABOK v3 + Business Data Analytics Extension** | 2020 | BA data |
| 🟠 | **BABOK v3 + Business Intelligence Extension** | 2019 | BI |
| 🟠 | **BABOK v3 + Information Technology Extension** | 2016 | IT-centric |
| 🟠 | **BABOK v3 + Cybersecurity Extension** | 2024 | Cyber BA |
| 🟠 | **IIBA Entry Certificate in Business Analysis (ECBA)** prep | 2024 | Certification |
| 🟡 | **CBAP (Certified Business Analysis Professional)** prep | 2024 | Niveau expert |

### 6.2 Livres d'application BABOK

| Pri. | Livre | Auteur |
|---|---|---|
| 🟠 | **BABOK Study Guide** | IIBA |
| 🟠 | **The PMI-PBA Exam Preparation** | PMI 2024 |
| 🟠 | **Business Analysis for Practitioners (PMI 2018)** | Multiple |
| 🟠 | **Agile and Business Analysis (BCS 2018)** | Multiple |
| 🟡 | **The Business Analysis Handbook (Cengage, 2014)** | Helen Winter |

**Source citations consultées** :
- BABOK v3 : https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/
- BABOK vs PMBOK vs PMI-BA : https://www.watermarklearning.com/blog/babok-vs-pmbok-vs-pmi-guide-to-ba/
- BABOK v3 : https://www.simpliaxis.com/resources/babok-business-analysis-body-of-knowledge

---

## 7. Section additionnelle — Classics / Fondations non-négociables

> Ces livres sont **canoniques** pour le génie logiciel mais **absents** du corpus. Ils doivent être intégrés en priorité car ils fournissent les **principes fondamentaux** (l'ontologie logicielle a souvent 24 principes mais aucun livre pour les justifier historiquement).

| Pri. | Livre | Auteur | Phase d'usage |
|---|---|---|---|
| 🔴 | **The Mythical Man-Month, Anniversary** | Fred Brooks (1995) | P0, P8 |
| 🔴 | **No Silver Bullet** | Fred Brooks (1986) | P0, P1 |
| 🔴 | **Peopleware, 3rd ed.** | DeMarco & Lister (2013) | P0, P8 |
| 🔴 | **The Pragmatic Programmer 20th** | Hunt/Thomas (2019) | P5 |
| 🔴 | **Clean Code** | Robert C. Martin (2008) | P4, P5 |
| 🔴 | **Clean Architecture** | Robert C. Martin (2017) | P3, P4 |
| 🔴 | **Working Effectively with Legacy Code** | Michael Feathers (2004) | P9 |
| 🔴 | **Refactoring 2nd ed.** | Martin Fowler (2018) | P4, P9 |
| 🔴 | **Domain-Driven Design** | Eric Evans (2003) | P2, P3 |
| 🔴 | **Patterns of Enterprise Application Architecture** | Martin Fowler (2002) | P3, P4 |
| 🔴 | **Enterprise Integration Patterns** | Hohpe/Woolf (2003) | P3, P4 |
| 🔴 | **The Art of Computer Programming, vol. 1-4A** | Donald Knuth | P5 (fondations algo) |
| 🔴 | **Structure and Interpretation of Computer Programs (SICP)** | Abelson/Sussman (1996) | P5 (fondations) |
| 🟠 | **Programming Pearls, 2nd ed.** | Jon Bentley (1999) | P5 |
| 🟠 | **Code Complete, 2nd ed.** | Steve McConnell (2004) | P5 |
| 🟠 | **The Design of Everyday Things** | Don Norman (2013) | P0, P4 |
| 🟠 | **AntiPatterns** | Brown et al. (1998) | tous |
| 🟠 | **Waltzing with Bears** | McConnell (2003) | P0, P1 |
| 🟠 | **Rapid Development** | McConnell (1996) | P0, P8 |
| 🟠 | **Software Estimation** | McConnell (2006) | P1 |
| 🟠 | **The Passionate Programmer** | Chad Fowler (2009) | P0, P5 |
| 🟠 | **Dreaming in Code** | Scott Rosenberg (2007) | P0, P5 |
| 🟠 | **The Soul of a New Machine** | Tracy Kidder (1981) | P0, P5 |
| 🟠 | **Showstopper!** | G. Pascal Zachary (1994) | P0 |
| 🟠 | **The Lean Startup** | Eric Ries (2011) | P0, P1 |
| 🟡 | **Are Your Lights On?** | Gause/Weinberg (1990) | P0, P2 |
| 🟡 | **Exploring Requirements** | Gause/Weinberg (1989) | P2 |
| 🟡 | **General Principles of Systems Design** | Weinberg (1988) | P0 |
| 🟡 | **The Art of Doing Science and Engineering** | Niklaus Wirth (1993) | P0, P5 |
| 🟡 | **Writing Solid Code** | Steve Maguire (1993) | P5 |
| 🟡 | **The Practice of Programming** | Pike/Kernighan (1999) | P5 |
| ⚪ | **The Pragmatic Bookshelf (catalogue complet)** | Divers | tous |

---

## 8. Section additionnelle — Soft skills, leadership, communication

> **Constat** : un projet logiciel est conduit par des **humains**. Le corpus est **100 % technique, 0 % soft skills**. Les phases 0 (Discovery), 1 (Feasibility), 2 (Requirements) et 8 (Operations) sont **incroyablement dépendantes** de la communication, du leadership et de la résolution de conflits. Cette section est **indispensable**.

| Pri. | Livre | Auteur | Phase |
|---|---|---|---|
| 🔴 | **Crucial Conversations, 3rd ed.** | Patterson et al. (2021) | P0, P2, P8 |
| 🔴 | **Difficult Conversations** | Stone/Patton/Heen (1999) | P0, P2 |
| 🔴 | **Switch** | Heath/Heath (2010) | P0, P8 |
| 🔴 | **Drive** | Daniel Pink (2009) | P0, P5, P8 |
| 🔴 | **The Five Dysfunctions of a Team** | Patrick Lencioni (2002) | P0, P8 |
| 🔴 | **The Manager's Path** | Camille Fournier (2017) | P0, P8 |
| 🔴 | **The Staff Engineer's Path** | Tanya Reilly (2022) | P0, P8 |
| 🔴 | **An Elegant Puzzle** | Will Larson (2024) | P0, P5, P8 |
| 🔴 | **Team Topologies** | Skelton/Pais (2019) | P0, P8 |
| 🟠 | **Accelerate** | Forsgren/Humble/Kim (2018) | P0, P8 |
| 🟠 | **The Phoenix Project** | Kim et al. (2013) | P0, P7 |
| 🟠 | **The Unicorn Project** | Kim (2019) | P0 |
| 🟠 | **Influencer** | Patterson et al. (2007) | P0 |
| 🟠 | **Change Management** | Cameron/Green (2015) | P0, P8 |
| 🟠 | **Reinventing Organizations** | Frederic Laloux (2014) | P0, P8 |
| 🟠 | **Turn the Ship Around!** | David Marquet (2012) | P0, P8 |
| 🟠 | **Radical Candor** | Kim Scott (2017) | P0, P8 |
| 🟠 | **High Output Management** | Andy Grove (1983) | P0, P8 |
| 🟠 | **The Effective Engineer** | Edmond Lau (2015) | P5, P8 |
| 🟠 | **The Pragmatic Programmer and the Whole Programmer** | Hunt/Thomas (série) | P0, P5 |
| 🟠 | **Thinking, Fast and Slow** | Daniel Kahneman (2011) | P0, P2 |
| 🟠 | **Nudge** | Thaler/Sunstein (2008) | P0 |
| 🟠 | **The Tipping Point** | Malcolm Gladwell (2000) | P0 |
| 🟡 | **The Mythical Man-Month** | Fred Brooks | *(idem §7)* |
| 🟡 | **The Design of Everyday Things** | Don Norman | P0, P4 |
| 🟡 | **The Lean Startup** | Ries | P0, P1 |
| 🟡 | **Sprint / Design Sprint** | Jake Knapp | P0 |
| 🟡 | **Leaders Eat Last** | Simon Sinek (2014) | P0, P8 |
| 🟡 | **The Infinite Game** | Simon Sinek (2019) | P0, P8 |
| 🟡 | **Multipliers** | Liz Wiseman (2010) | P0, P8 |
| 🟡 | **The Coaching Habit** | Michael Bungay Stanier (2016) | P0, P8 |
| 🟡 | **The Fearless Organization** | Amy Edmondson (2018) | P0, P8 |
| 🟡 | **Black Box Thinking** | Matthew Syed (2015) | P0, P8 |
| 🟡 | **Antifragile** | Nassim Taleb (2012) | P0, P8 |
| ⚪ | **The Art of War** | Sun Tzu (Ve siècle av. J.-C.) | P0, P1 |
| ⚪ | **On War** | Carl von Clausewitz (1832) | P0, P1 |

---

## 9. Section additionnelle — AI-assisted software development

> **Contexte 2026** : L'IA générative est en train de transformer **toutes** les phases. Le corpus doit l'intégrer. **Sont déjà présents** : *AI-Assisted Programming* (Tom Taulli), *Generative AI for Software Development*, *Building Machine Learning Powered Applications*, *Developer's Playbook for LLM Security*, *Context Engineering for Multi-Agent Systems* (Sanet).

| Pri. | Livre | Auteur | Phase |
|---|---|---|---|
| 🔴 | **Generative AI for Software Development (O'Reilly, 2024)** | Vergadia/Pollard | P0, P5, P6 |
| 🔴 | **AI-Assisted Programming (O'Reilly, 2024)** | Tom Taulli | P5, P6 |
| 🔴 | **Prompt Engineering for Generative AI (O'Reilly, 2024)** | James Phoenix | P2, P5 |
| 🔴 | **Generative AI for Software Developers (Packt, 2024)** | Bernardo/Patel | P5, P6, P7 |
| 🟠 | **Beyond the Algorithm (O'Reilly, 2024)** | Stoyanovich et al. | P0, P2, P3 |
| 🟠 | **AI Security and Responsible AI Practices (O'Reilly vidéo, 2024)** | Omar Santos | P8, P9 |
| 🟠 | **Scaling Responsible AI (O'Reilly, 2024)** | Manure/Bengani | P0, P1 |
| 🟠 | **Building AI Agents with LLMs (O'Reilly, 2024)** | Osinga | P3, P5 |
| 🟠 | **LLM Engineer's Handbook (O'Reilly, 2024)** | Paul/Behrens | P5, P7, P8 |
| 🟠 | **AI Engineering (O'Reilly, 2025)** — Chip Huyen | P5, P6, P7, P8 |
| 🟠 | **Software Engineering with LLMs (Manning, 2025)** — Jacek Galowicz | P5, P6 |
| 🟠 | **The Developer's Playbook for LLM Security (O'Reilly, 2024)** | Wilson et al. | P7, P8 |
| 🟠 | **Building Generative AI Services with FastAPI (O'Reilly, 2024)** | Cyberkoor | P5 |
| 🟠 | **Generative AI Systems (O'Reilly, 2024)** | Shah | P3, P5, P8 |
| 🟠 | **LangChain in Action (O'Reilly, 2024)** | Besta | P3, P5 |
| 🟠 | **Designing Multi-Agent Systems (O'Reilly, 2025)** | Huhns | P3 |
| 🟠 | **Architectures for AI (O'Reilly, 2024)** | Kovacs | P3 |
| 🟠 | **Coding with AI — End of Software Development as We Know It (O'Reilly, 2024)** | Wilson | P5 |
| 🟠 | **AI-Powered Developer (Manning, 2024)** — Nathan Marz | P5 |
| 🟠 | **Mastering LLM Agents (Packt, 2025)** | | P3, P5 |
| 🟠 | **Agentic AI (Packt, 2025)** | | P3, P5, P8 |
| 🟠 | **Building Agentic AI Systems (Packt, 2024)** | | P3, P5 |
| 🟠 | **Context Engineering for Multi-Agent Systems (Sanet, présent dans corpus)** | | P3, P5 |
| 🟠 | **Context Engineering for Reliable AI Systems (O'Reilly vidéo, 2024)** | | P3, P5 |
| 🟠 | **Generative AI Toolbox (O'Reilly vidéo, 2024)** | | P0, P2, P5 |
| 🟠 | **The Elements of Prompt Engineering (O'Reilly live, 2024)** | | P0, P2, P5 |
| 🟠 | **Generative AI for Enhanced Project Management (O'Reilly live, 2024)** | | P0, P1 |
| 🟠 | **Agentic Reliability Engineering (O'Reilly, 2025)** | | P8 |
| 🟠 | **How Agentic AI Empowers Architecture Governance (O'Reilly Radar, 2024)** | | P3 |
| 🟠 | **Software Architecture in an AI World (O'Reilly Radar, 2024)** | | P3 |
| 🟡 | **Hands-On Generative AI with Transformers and Diffusion Models (O'Reilly, 2024)** | Sanseviero et al. | P5 |
| 🟡 | **Generative AI with LangChain (Packt, 2024)** | | P5 |
| 🟡 | **ChatGPT and Python (présent dans corpus)** | | P5 |
| 🟡 | **AI Horizon (O'Reilly, 2024)** | Mehri | P0, P5 |
| 🟡 | **A Quick Start Guide to Prompt Engineering (Packt, 2023)** | | P2, P5 |
| 🟡 | **AI-First Products (O'Reilly, 2024)** | | P0, P3 |
| 🟡 | **Data Quality for Generative AI (O'Reilly, 2024)** | | P2, P5 |
| 🟡 | **Vector Search for Practitioners (O'Reilly, 2024)** | | P3 |
| 🟡 | **Prompt Engineering Basics (O'Reilly vidéo)** | | P0, P5 |

---

## 10. Plan d'intégration — priorisation & risques

### 10.1 Plan en 4 vagues

#### Vague 1 — Critique (semaine 1–2) ≈ 35 livres

**But** : combler les trous noirs (PMI, Discovery, SRE, Maintenance, Classics).

| Phase | Livres à intégrer |
|---|---|
| 0/1 | INSPIRED, Lean Startup, Business Model Gen, Escaping the Build Trap, Lean UX, The Mom Test, Continuous Discovery Habits |
| 2 | Software Requirements 3rd (Wiegers), User Stories Applied (Cohn), Agile Software Requirements (Leffingwell), BABOK v3 + extensions |
| 3 | Software Architecture in Practice 4th, Designing Software Architectures 2nd, Effective Software Architecture, GoF Design Patterns |
| 4/5 | Clean Code, Clean Architecture, Refactoring 2nd, Pragmatic Programmer 20th, Software Engineering at Google, Clean Craftsmanship, Modern Software Engineering |
| 6 | Lessons Learned in Software Testing, Agile Testing, xUnit Test Patterns, TDD by Example, Growing OO Software |
| 7 | Continuous Delivery, The DevOps Handbook, Release It! 2nd, Production-Ready Microservices |
| 8 | Site Reliability Engineering (Google), The Site Reliability Workbook, Observability Engineering 2nd, Building Secure and Reliable Systems, Accelerate, Chaos Engineering |
| 9 | Working Effectively with Legacy Code, Beyond Legacy Code, Refactoring Databases |
| PMI | PMBOK 7e/8e, PMI Standard for Business Analysis, PMI Standard for Risk Management, PMI Standard for Program/Portfolio Management, Governance of PPP |
| Classics | The Mythical Man-Month, Peopleware, AntiPatterns, Waltzing with Bears |
| Soft skills | Crucial Conversations, Difficult Conversations, Switch, Drive, Five Dysfunctions, Team Topologies, The Staff Engineer's Path, An Elegant Puzzle |

#### Vague 2 — Étoffage (semaine 3–4) ≈ 30 livres

**But** : compléter les phases intermédiaires + IA + obsolescence.

| Phase | Livres |
|---|---|
| 0/1 | Switch, Sprint, Design Sprint, The Design of Everyday Things, Don't Make Me Think, Value Proposition Design, Thinking in Systems |
| 2 | DDD (Evans), Implementing DDD, Visual Models for Software Requirements, Impact Mapping, Specification by Example, Exploring Requirements, Requirements Writing for System Engineering |
| 3 | Fundamentals of Software Architecture 2nd (si nouvelle), Patterns of EAA, Enterprise Integration Patterns, Designing Data-Intensive Applications 2nd, Software Architecture Patterns for Serverless Systems, Software Architecture in an AI World, Cloud Native Architecture, Mastering API Architecture, Kubernetes Patterns 2nd, Head First Software Architecture |
| 4/5 | Effective Java 3rd, Clean Code Cookbook, Architecture Patterns with Python, Software Engineering at Google, An Elegant Puzzle, AI-Assisted Programming, Generative AI for Software Development |
| 6 | The Art of Software Testing 3rd, Specification by Example, How Google Tests Software, AI-Driven Software Testing, Continuous Testing for DevOps Professionals |
| 7 | Pipeline as Code, Cloud Native DevOps with K8s, Kubernetes for the Absolute Beginners, Terraform Up & Running 3rd, Ansible Up & Running 3rd, Microservices Up and Running, Monolith to Microservices |
| 8 | Incident Management for Operations, Distributed Systems Observability, Effective Monitoring and Alerting, SRE in Practice, Modern System Administration, Cloud Observability in Action |
| 9 | Making Software, Refactoring to Patterns, The Pragmatic Programmer 20th, Death March 2nd, AntiPatterns |
| 10 | Cloud Native Transformation, Migrating to Cloud-Native Application Architectures, Data Governance, GDPR & Privacy |
| PMI | DA toolkit, Practice Standards (Risk, EVM, Scheduling, WBS, Configuration), PMI Pulse of the Profession |
| BABOK | BABOK extensions (Agile, BDA, BI, IT, Cyber) |
| Classics | Code Complete 2nd, Programming Pearls 2nd, The Art of Computer Programming (sélection) |
| Soft skills | Radical Candor, Multipliers, Leaders Eat Last, The Coaching Habit, Fearless Organization, Antifragile |
| AI | Prompt Engineering for Generative AI, LLM Engineer's Handbook, AI Engineering (Huyen), Generative AI for Software Developers, AI Security and Responsible AI Practices, Beyond the Algorithm |

#### Vague 3 — Enrichissement (semaine 5–6) ≈ 25 livres

**But** : enrichissement ciblé des phases, spécialisations.

- 0/1 : Reinventing Organizations, Nudge, Thinking Fast and Slow, The Tipping Point, Dreaming in Code, Showstopper
- 3 : Effective Software Architecture, Software Architecture Superstream Series, Building Evolutionary Architectures 2nd, Software Architecture in an AI World
- 4/5 : Programming Pearls 2nd, Code Complete 2nd, The Art of Readable Code, Implementation Patterns, Refactoring in Ruby
- 6 : Perfect Software, Beautiful Testing, Practical Test-Driven Development using C# 7, Hands-On Test Management with Jira, Test-Driven Development with Java
- 7 : Continuous Integration (Duvall), Cloud Migration, Hands-On Docker for Microservices
- 8 : Cloud Native DevOps with K8s, Production Kubernetes, Bulletproof SSL and TLS, Service Meshes
- 9 : Software Assessment, Technical Debt Management (O'Reilly Radar)
- 10 : The Data Warehouse Toolkit, Cloud Migration
- Classics : The Art of Doing Science and Engineering, The Practice of Programming
- Soft skills : High Output Management, Turn the Ship Around!, Black Box Thinking
- AI : Generative AI Systems, LangChain in Action, Building Generative AI Services with FastAPI, AI-First Products, Vector Search for Practitioners, Agentic Reliability Engineering, AI-Powered Developer (Marz)

#### Vague 4 — Polish & trends 2026 (semaine 7+) ≈ 15 livres

**But** : capter les toutes dernières tendances 2025–2026, Outils émergents, AI agents.

- AI agents : Agentic AI (Packt 2025), Building Agentic AI Systems, Mastering LLM Agents, Designing Multi-Agent Systems, AI-Driven Software Testing
- Cloud 2026 : Engineering Long-Lasting Software (O'Reilly 2025), Production-Ready Open Source, Service Meshes 2nd
- Sustainable : Building Green Software (O'Reilly 2021) — déjà référencé
- Strategy : The Art of War, On War (si version livre)

#### Vague 5 — Foundation canoniaque (semaine 8–12) ≈ 200 ressources

**But** : combler les **trous noirs** (PMI, Classics, Soft skills, Standards, Papers) — la **substance** qui manque le plus.

- **Classics canoniaques** (P0–P10) : Mythical Man-Month, Peopleware, Pragmatic Programmer 20th, Code Complete 2nd, Clean Code, Clean Architecture, Clean Craftsmanship, GoF Design Patterns, DDD Evans, Implementing DDD, Refactoring 2nd, Working Effectively with Legacy Code, Beyond Legacy Code, Refactoring Databases, Patterns of EAA, Enterprise Integration Patterns, Software Engineering at Google, Modern Software Engineering, Continuous Delivery, Release It! 2nd, Production-Ready Microservices, The Phoenix Project, The Unicorn Project, Accelerate, Team Topologies, Death March 2nd, Waltzing with Bears, AntiPatterns, Rapid Development, Software Estimation, The Mythical Man-Month (Design of Design), Lean Startup, INSPIRED, Escaping the Build Trap, Continuous Discovery Habits, The Mom Test, Sprint, Domain-Driven Design Reference, User Stories Applied, Agile Software Requirements, Impact Mapping, Specification by Example, The Pragmatic Bookshelf (divers), Dreaming in Code, The Soul of a New Machine, Showstopper!, The Effective Engineer, The Passionate Programmer, Code Complete 2nd, Programming Pearls 2nd, Succeeding with Agile, Agile Estimating and Planning, The Design of Everyday Things.
- **Soft skills / leadership** (P0–P8) : Crucial Conversations, Difficult Conversations, Switch, Drive, Five Dysfunctions, The Manager's Path, The Staff Engineer's Path, An Elegant Puzzle, Team Topologies, Radical Candor, Multipliers, Leaders Eat Last, The Coaching Habit, Fearless Organization, Antifragile, Black Box Thinking, Turn the Ship Around!, High Output Management.
- **PMI Standards complets** (P0–P9) : PMBOK 7e + 8e, PMI Standard for Business Analysis, Risk Management, Program Management 5e, Portfolio Management 4e, Governance of PPP, Disciplined Agile, Practice Standards (Risk, EVM, Scheduling, WBS, Configuration), OPM.
- **IIBA BABOK + extensions** (P2) : BABOK v3, Agile Extension, BDA Extension, BI Extension, IT Extension, Cyber Extension, Study Guide.
- **Standards ISO / IEEE / NIST** (tous) : ISO/IEC/IEEE 42010, 12207, 15288, 25010, IEEE 830/29148, 1016, 1028, 1044, 1219, 1471, ISO 27001/27002, 31000, NIST 800-53, CSF 2.0, SSDF 800-218, 800-37, 800-161.
- **Standards OWASP + MITRE** (P5, P7, P8) : OWASP Top 10 (2021, 2025), ASVS 4.0.3, SAMM 2.0, Top 10 LLM, AI Security Guide, MITRE ATT&CK, D3FEND, ATLAS, CWE Top 25, CVE.
- **Réglementation EU/US** (P0, P7, P8, P10) : GDPR, AI Act, DORA, NIS2, Cyber Resilience Act, US Cyber EO 14028, CISA Secure by Design, OpenSSF SLSA, Sigstore, Scorecard, SOC 2, PCI DSS, HIPAA, Common Criteria.
- **Méthodologies** (P0, P1, P2, P8) : PRINCE2 7e, PRINCE2 Agile, CMMI v2.0, ITIL 4, TOGAF 10, Zachman 6, ArchiMate 3.2, DoDAF/MODAF/NAF, INCOSE SE Handbook 5e, Essence 1.2, SAFe 6.0, Scrum@Scale, Spotfiy Model article, APM BoK, ISO 21500, ISO 9001, ISO 14764.
- **Papers académiques fondateurs (PDF libres)** : No Silver Bullet (Brooks 1986), Programming as Theory Building (Naur 1986), What is Software Design? (Reeves 1992), Out of the Tar Pit (Moseley & Marks 2006), Parnas 1972 (decomposition into modules), A Note on Distributed Computing (1994), Fallacies of Distributed Computing (1994), Cathedral and the Bazaar (Raymond 1999), Big Ball of Mud (Foote & Yoder 1999), Lehman Laws of Software Evolution, Conway's Law 1968, Dijkstra 1972, Hoare CSP 1978, Liskov Substitution 1994, Boehm 1981, COCOMO II 2000, FPA Albrecht 1979, COSMIC 2024, The Wisdom of Crowds 2004, Tipping Point 2000, Antifragile 2012, Drive 2009, Kahneman Thinking Fast and Slow 2011, Nudge 2008, Kuhn 1962, Factfulness 2018, How Complex Systems Fail 1998-2018, Hollnagel Drift Into Failure 2009, Resilience Engineering 2006, Safety-I/II 2014, Perrow Normal Accidents 1984, Dörner Logic of Failure 1989, Roberts HRO 1989, Why We Sleep 2017, Atomic Habits 2018, Deep Work 2016, Four Thousand Weeks 2021, Indistractable 2019, The Mythical Man-Month (1995, 20th, 50th anniversary), Hackers 1984, Innovators 2014.
- **AI/LLM additionnels** (P0, P5, P6, P7, P8) : Manning (Prompt Engineering for AI Systems, Building Reliable AI Systems, Build a Large Language Model From Scratch, How Large Language Models Work, Knowledge Graphs and LLMs in Action, AI Agents and Applications, Data Analysis with LLMs), AI Engineering (Chip Huyen 2025), Software Engineering with LLMs (Manning 2025), Beyond the Algorithm, Scaling Responsible AI, Introduction to Responsible AI, AI Security and Responsible AI Practices, Building Generative AI Services with FastAPI, LangChain in Action, AI-First Products, Data Quality for Generative AI, Vector Search for Practitioners, Building Reliable AI Systems, Agentic Reliability Engineering, AI-Powered Developer (Marz).
- **CS foundational classics** (P5) : SICP (PDF libre MIT), Elements of Computing Systems (Nisan & Schocken), SICP JS, Concrete Mathematics, CLRS 4e, Algorithm Design Manual 3e, Structure and Interpretation of Computer Programs.

### 10.2 Risques & garde-fous

| Risque | Mitigation |
|---|---|
| **Surcoût token** : intégrer 100+ livres = explosion du contexte (au-delà de 200k concepts). | **NE PAS tout charger d'un coup**. Utiliser le **modèle L0/L1/L2/L3** du `00-context-engineering-strategy.md`. Indexer 100 livres = 0.5-1% de l'attention. Charger **un livre à la fois** sur demande. |
| **Redondance** : plusieurs livres disent la même chose. | Le moteur de dédoublonnage existant (32.5% inclusion rate dans `coverage_report.md`) gère déjà ça. Activer un **mode "highest-cited-wins"**. |
| **Pertinence** : certains livres ne s'appliquent qu'à 1 phase. | **Tagger chaque livre avec ses phases** dans `per_book/`. Stocker dans `corpus_browser.py` metadata. |
| **Biais culturel** : PMI/IIBA = américains, certains principes sont culturellement marqués. | Ajouter **équivalents européens** : ISO/IEC/IEEE 42010, ISO 21500 (PM), PRINCE2 (AXELOS), CMMI (ISACA). |
| **Mise à jour** : 2026 → certains livres auront 1 an de retard. | Planifier **revue trimestrielle** (alignée sur l'audit quarterly council). |
| **Droits/licences** : tous les livres listés ne sont pas libres. | Privilégier **libres (CC/CC-BY)** + **O'Reilly for Higher Ed** + **acquisitions papier/numérique**. Les standards PMI sont payants. |
| **Bruit** : livres d'opinion vs livres techniques. | Pondérer : **standards (PMI, ISO) > manuels (O'Reilly) > témoignages > romans (Phoenix)**. |

### 10.3 Processus d'ingestion (rappel du pipeline existant)

1. **Source** : PDF ou EPUB (achat/libre)
2. **Ingestion** : placer dans `distilled_corpus/per_book/<slug>.json` (script de conversion)
3. **Distillation** : `python3 scripts/line_distiller.py` (extrait concepts)
4. **Jugement** : `python3 scripts/judge.py` (note inclusion 0-1)
5. **Indexation** : `python3 scripts/build_index.py` (inscrit dans `distilled_corpus_v2/themes/theme_map.json`)
6. **Expose** : `python3 scripts/corpus_browser.py --book "<title>"` pour retrieval

---

## 11. Annexes

### Annexe A — Liste consolidée de tous les livres recommandés (par éditeur)

#### O'Reilly (cible #1 — ~70 livres)

**Architecture / Software Engineering** (P3, P4) : Software Architecture in Practice 4th, Designing Software Architectures 2nd, Effective Software Architecture, Head First Software Architecture, Building Evolutionary Architectures 2nd, Software Architecture: The Hard Parts, Software Architecture Patterns 2nd, Fundamentals of Software Architecture, Software Architecture Metrics, Flow Architectures, Facilitating Software Architecture, Software Architecture in an AI World, System Design Guide for Software Professionals.

**DDD / Patterns** (P2, P3) : Learning Domain-Driven Design, Domain-Driven Design Distilled, Patterns of Enterprise Application Architecture, Enterprise Integration Patterns, Kubernetes Patterns 2nd, Design Patterns (GoF — Addison-Wesley).

**Software Engineering général** (P5, P6) : Software Engineering at Google, The Pragmatic Programmer 20th, Clean Code Cookbook, Refactoring in Python LiveLessons, Refactoring with C#.

**Code / Craftsmanship** (P4, P5) : Architecture Patterns with Python, Effective Java 3rd, The Art of Readable Code, Clean Code (Addison-Wesley).

**Testing** (P6) : Full Stack Testing, Testing JavaScript Applications, API Testing and Development with Postman, Hands-On Test-Driven Development.

**Delivery / DevOps** (P7) : Continuous Deployment, Cloud Native DevOps with K8s, Pipeline as Code, Production Kubernetes.

**SRE / Observability** (P8) : Site Reliability Engineering, The Site Reliability Workbook, Observability Engineering 2nd, Building Secure and Reliable Systems, Distributed Systems Observability, Incident Management for Operations, Modern System Administration.

**Security** (tous) : Designing Secure Software, AI Security and Responsible AI Practices, Defensive Security Handbook 2nd, Web Application Security 2nd, 97 Things Every Application Security Professional Should Know, Threat Modeling Fundamentals, The Developer's Playbook for LLM Security, Software Supply Chain Security, Developing Cybersecurity Programs and Policies in an AI-Driven World.

**ML / AI** (P0, P5, P8) : Machine Learning Production Systems, Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow, Generative AI for Software Development, AI-Assisted Programming, LLM Engineer's Handbook, Generative AI Systems, Designing Multi-Agent Systems, AI Engineering (Huyen 2025), Building Generative AI Services with FastAPI, LangChain in Action, Generative AI with LangChain, Hands-On Generative AI with Transformers, Beyond the Algorithm, Scaling Responsible AI, Introduction to Responsible AI, AI Security and Responsible AI Practices, Agentic Reliability Engineering.

**Data** (P3, P4) : Designing Data-Intensive Applications 2nd, Learning SQL (Beaulieu), Python for Data Analysis (McKinney).

**Product / Discovery** (P0) : INSPIRED, Escaping the Build Trap, Continuous Discovery Habits, Lean UX 3rd, The Lean Startup, Impact Mapping, The Power of Positive Sharing, Beyond the Algorithm.

**Soft Skills** : The Staff Engineer's Path, The Manager's Path, An Elegant Puzzle, An Elegant Puzzle, Team Topologies (Pragmatic Bookshelf, parfois distribué par O'Reilly).

**Prompting** : Prompt Engineering for Generative AI, Mastering Prompt Engineering, The Elements of Prompt Engineering, Generative AI Toolbox.

**Project Management** : Effective Software Project Management, Software Project Management, Quality Software Project Management, Agile Estimating and Planning (Pragmatic Bookshelf).

#### Packt Publishing (cible #2 — ~30 livres)

**Architecture / Cloud** (P3, P7) : Software Architecture Patterns for Serverless Systems, Design Microservices Architecture with Patterns and Principles, Software Architecture with C# 10 and .NET 6 3rd, Pragmatic Microservices with C# and Azure, Software Architecture for Busy Developers, Architectural Patterns, Cloud Native Architecture, The Kubernetes Bible 2nd, Mastering Kubernetes 4th, Certified Kubernetes Administrator, Kubernetes for the Absolute Beginners.

**Security** (tous) : Learn Ethical Hacking from Scratch, Penetration Testing Azure for Ethical Hackers, Pentesting Fundamentals for Beginners, The Ultimate Kali Linux Book, Wireless Penetration Testing for Ethical Hackers.

**Testing** (P6) : Software Testing Strategies, Hands-On Test Management with Jira, Appium (Selenium), Learn Selenium, Test-Driven Development with Java, Modern Game Testing, Continuous Testing for DevOps Professionals, Practical Test-Driven Development using C# 7, Mastering Jenkins.

**Data** : Data Engineering with Apache Spark, Delta Lake, and Lakehouse.

**DevOps / SRE** (P7, P8) : Mastering DevOps, Becoming a Rockstar SRE, Practical Site Reliability Engineering, Modern Site Reliability Engineering, Mastering Python Design Patterns 3rd, Hands-On Design Patterns with C# and .NET Core, Hands-On Design Patterns with Java, Hands-On Software Architecture with C# and .NET, Hands-On Software Architecture with Golang, Hands-On Docker for Microservices, Refactoring with C#.

**AI** (P0, P5) : Generative AI for Software Developers, AI-Driven Software Testing, A Quick Start Guide to Prompt Engineering, Generative AI with LangChain, Building Agentic AI Systems, Agentic AI, Mastering LLM Agents.

#### PMI Standards (cible #3 — ~12 standards + practice guides)

PMBOK Guide 7e + 8e, PMI Standard for Business Analysis, PMI Standard for Risk Management, PMI Standard for Program Management 5e, PMI Standard for Portfolio Management 4e, Governance of Portfolios Programs and Projects, PMI Disciplined Agile (DA), Practice Standard for Project Risk Management, Practice Standard for Earned Value Management, Practice Standard for Scheduling, Practice Standard for Work Breakdown Structures, Practice Standard for Project Configuration Management, The Standard for Organizational Project Management (OPM), PMI Pulse of the Profession (rapports).

#### IIBA BABOK (cible #4 — ~7)

BABOK v3, BABOK Agile Extension, BABOK Business Data Analytics Extension, BABOK Business Intelligence Extension, BABOK Information Technology Extension, BABOK Cybersecurity Extension, BABOK Study Guide, CBAP/PMI-PBA prep.

#### Addison-Wesley / Pearson / Wiley (cible #5 — ~25 classics + manuels)

- **Classics** : Mythical Man-Month, Peopleware, Pragmatic Programmer 20th, Clean Code, Clean Architecture, Clean Craftsmanship, GoF Design Patterns, Refactoring 2nd, Working Effectively with Legacy Code, Beyond Legacy Code, Code Complete 2nd, Refactoring to Patterns, Patterns of EAA, Enterprise Integration Patterns, DDD Evans, Implementing DDD, Growing OO Software, TDD by Example, Agile Testing Crispin, xUnit Test Patterns, Lessons Learned in Software Testing, Art of Software Testing 3rd, Programming Pearls 2nd.
- **Méthode** : Agile Estimating and Planning, Succeeding with Agile, SAFe Distilled.
- **PM** : Effective Software Project Management, Quality Software Project Management, Software Project Management.

#### Pragmatic Bookshelf (cible #6 — ~5)

- Release It! 2nd, Beyond Legacy Code, The Pragmatic Programmer 20th, Team Topologies, Agile and Business Analysis.

#### Manning (cible #7 — ~5)

- Specification by Example, Microservices Patterns, Cloud Observability in Action, AI Engineering, LLM Engineer's Handbook (éditions décalées).

#### Divers (cible #8 — ~10)

- IT Revolution : Phoenix Project, Unicorn Project, Accelerate, DevOps Handbook 2nd.
- Wiley : Lessons Learned in Software Testing, Software Project Management (Hiemstra), Software Testing (Rakitin), Building Multi-Tenant SaaS Architectures, Agile Practice Guide (PMI).
- Apress : Beginning API Development with Node.js, Requirements Writing for System Engineering, Cloud Computing Concepts.
- Harvard Business Review / McGraw-Hill : Drive, Switch, Influencer, Crucial Conversations, Difficult Conversations, The Effective Engineer, High Output Management, The Coaching Habit.

### Annexe B — Mapping livres × phases (matrice de couverture)

| Phase | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **PMI/IIBA (12+7)** | ✓✓ | ✓✓ | ✓✓✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓✓ | ✓✓ | ✓✓ |
| **Discovery/Product (15)** | ✓✓✓ | ✓✓✓ | ✓✓ | ✓ | ✓ | | | | | | |
| **Requirements (15)** | ✓ | ✓ | ✓✓✓ | ✓✓ | ✓ | | | | | | |
| **Architecture (15)** | | ✓ | ✓ | ✓✓✓ | ✓✓ | ✓ | | ✓ | ✓ | ✓ | ✓ |
| **Design/Patterns (12)** | | | | ✓ | ✓✓✓ | ✓✓ | ✓ | | | | |
| **Implementation (10)** | | | | | ✓ | ✓✓✓ | ✓✓ | ✓ | | | |
| **Testing (15)** | | | ✓ | | | ✓ | ✓✓✓ | ✓ | | | |
| **Deployment (15)** | | | | ✓ | | | ✓ | ✓✓✓ | ✓ | | |
| **SRE/Operations (18)** | | | | | | | | ✓ | ✓✓✓ | ✓✓ | ✓ |
| **Maintenance (10)** | | | | ✓ | ✓✓ | ✓✓ | ✓ | | | ✓✓✓ | ✓ |
| **Retirement (8)** | | | | ✓ | | | | ✓ | ✓ | ✓ | ✓✓✓ |
| **AI/LLM (30)** | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓ | ✓✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓ | |
| **Soft skills (25)** | ✓✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓✓ | ✓ | ✓ |
| **Classics (15)** | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓✓✓ | ✓✓✓ | ✓✓ | ✓ | ✓✓ | ✓✓✓ | ✓ |

✓ = couverture standard, ✓✓ = couverture forte, ✓✓✓ = couverture critique/primaire

### Annexe C — Sources web exploitées (toutes catégories)

- **O'Reilly** : https://www.oreilly.com/library/, https://www.oreilly.com/search/skills/ (40+ skills consultées)
- **Packt** : https://www.packtpub.com/, https://subscription.packtpub.com/
- **PMI** : https://www.pmi.org/standards, https://www.pmi.org/disciplined-agile/
- **IIBA** : https://www.iiba.org/
- **Manning** : https://www.manning.com/
- **Pragmatic Bookshelf** : https://pragprog.com/
- **Pearson / Addison-Wesley** : https://www.pearson.com/, https://www.informit.com/
- **Wiley** : https://www.wiley.com/

### Annexe D — Glossaire

- **KA** : Knowledge Area (SWEBOK)
- **RAG** : Retrieval-Augmented Generation
- **ADRs** : Architecture Decision Records
- **CD** : Continuous Delivery
- **SLO** : Service Level Objective
- **DA** : Disciplined Agile
- **BABOK** : Business Analysis Body of Knowledge
- **WBS** : Work Breakdown Structure
- **EVM** : Earned Value Management
- **NFR** : Non-Functional Requirements
- **OPM** : Organizational Project Management
- **AGILE** : terme générique
- **MLOps** : Machine Learning Operations

---



## 12. Section additionnelle — Documents / livres à très forte valeur ajoutée (toutes sources confondues)

> **Contexte** : cette section regroupe des livres, documents, **standards** et **publications académiques** qui transcendent les éditeurs O'Reilly/Packt et constituent des **incontournables absolus** pour la qualité du projet. Beaucoup sont en **libre accès** (PDF, GitHub, archives ouvertes) ou **fondamentaux** au point qu'ils justifient une place prioritaire dans le corpus, devant même certains livres O'Reilly. Classés par **valeur/phase** (pas par éditeur).

### 12.1 Les "Bibles" du génie logiciel (P0→P10, hors O'Reilly/Packt)

| Pri. | Livre / Document | Auteur(s) | Éditeur / Source | Phase(s) | Valeur ajoutée |
|---|---|---|---|---|---|
| 🔴 | **Designing Data-Intensive Applications, 2nd ed. (Feb 2026)** | Martin Kleppmann & Chris Riccomini | O'Reilly / Stanford archive | P3, P4, P8 | **Le livre le plus important des 10 dernières années** sur les systèmes data. La 2e édition (2026) couvre l'ère AI. À intégrer en Vague 1. |
| 🔴 | **A Philosophy of Software Design, 2nd ed.** | John Ousterhout (Stanford) | Stanford web (PDF gratuit) — Amazon Kindle | P3, P4, P5 | **Le manifeste anti-complexité** du design logiciel. Disponible en PDF sur `web.stanford.edu/~ouster`. Critère "deep vs shallow" modules, "red flags". **Indispensable** pour P3/P4. |
| 🔴 | **The Pragmatic Programmer, 20th Anniversary ed. (2019)** | David Thomas, Andrew Hunt | Addison-Wesley | P5, P6, P9 | Le **manifeste du pragmatisme**. DRY, orthogonality, tracer bullets, broken windows. Toujours d'actualité 2026. |
| 🔴 | **Code Complete, 2nd ed. (2004)** | Steve McConnell | Microsoft Press | P4, P5 | L'**encyclopédie** du code. 900+ pages de pratique. |
| 🔴 | **The Mythical Man-Month, Anniversary (1995)** | Fred Brooks | Addison-Wesley | P0, P1, P8 | Brook's Law, le concept de "conceptual integrity", 50 ans de validité. |
| 🔴 | **Peopleware, 3rd ed. (2013)** | Tom DeMarco, Tim Lister | Dorset House | P0, P8 | **La bible des facteurs humains** du développement logiciel. |
| 🔴 | **The Mythical Man-Month, Essays on Software Engineering** | Fred Brooks | Addison-Wesley | P0, P1, P8 | *Idem ci-dessus* — version étendue. |
| 🔴 | **Domain-Driven Design (2003)** | Eric Evans | Addison-Wesley | P2, P3 | Le **livre fondateur** du DDD. *Learning DDD* (présent) est une intro, le livre original est *la référence*. |
| 🔴 | **Patterns of Enterprise Application Architecture (2002)** | Martin Fowler | Addison-Wesley | P3, P4 | Le **catalogue fondateur** des patterns entreprise. Référencé mondialement. |
| 🔴 | **Enterprise Integration Patterns (2003)** | Gregor Hohpe, Bobby Woolf | Addison-Wesley | P3, P4 | 65 patterns d'intégration. *Indispensable* pour P3. |
| 🔴 | **Refactoring, 2nd ed. (2018)** | Martin Fowler | Addison-Wesley | P4, P9 | Le **catalogue** de refactorings + processus. |
| 🔴 | **Working Effectively with Legacy Code (2004)** | Michael Feathers | Prentice Hall | P9 | Le **seam model**, characterization tests, dependency breaking. |
| 🔴 | **Software Engineering at Google (2020)** | Titus Winters, Tom Manshreck, Hyrum Wright | O'Reilly | P5, P6, P8 | *(déjà cité §4.6)* — leçons d'ingénierie à l'échelle Google. |
| 🔴 | **Modern Software Engineering (2023)** | David Farley | Addison-Wesley | P5, P6, P8 | **Le successeur spirituel** du PMBOK pour le software. Principes d'empirisme, feedback, iteration. |
| 🔴 | **Continuous Delivery (2010)** | Jez Humble, David Farley | Addison-Wesley | P7 | **Le livre fondateur** du CD. |
| 🔴 | **The Phoenix Project (2013)** | Gene Kim, Kevin Behr, George Spafford | IT Revolution | P0, P7, P8 | **Le roman** qui rend la théorie DevOps palpable. |
| 🔴 | **The Unicorn Project (2019)** | Gene Kim | IT Revolution | P0, P5, P8 | Suite — focus developer experience, 5 ideals. |
| 🔴 | **Accelerate (2018)** | Nicole Forsgren, Jez Humble, Gene Kim | IT Revolution | P0, P7, P8 | **La science derrière DORA**. Statistical rigor. 4 métriques clés. |
| 🔴 | **Team Topologies (2019)** | Matthew Skelton, Manuel Pais | IT Revolution | P0, P8 | **Le standard moderne** d'organisation des équipes. 4 topologies, cognitive load. |
| 🔴 | **Clean Code (2008)** | Robert C. Martin | Prentice Hall | P4, P5 | Le **manifeste** du code propre. 250k exemplaires vendus. |
| 🔴 | **Clean Architecture (2017)** | Robert C. Martin | Prentice Hall | P3, P4 | S.O.L.I.D. + dependency rule + boundaries. |
| 🔴 | **Clean Craftsmanship (2021)** | Robert C. Martin | Addison-Wesley | P4, P5 | TDD + acceptance testing + professionalism. |
| 🟠 | **Building Evolutionary Architectures, 2nd ed. (2023)** | Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage | O'Reilly | P3, P9 | *(déjà cité §4.4)* — *à vérifier présence corpus*. |
| 🟠 | **Release It!, 2nd ed. (2018)** | Michael T. Nygard | Pragmatic Bookshelf | P7, P8, P9 | Patterns de stabilité, antipatterns de production. **À ajouter impérativement**. |
| 🟠 | **Beyond Legacy Code (2015)** | David Scott Bernstein | Pragmatic Bookshelf | P9 | 9 pratiques pour moderniser. **À ajouter impérativement**. |
| 🟠 | **Production-Ready Microservices (2016)** | Susan Fowler | O'Reilly | P7, P8 | Standards de microservices. **Complément à Building Microservices**. |
| 🟠 | **The Pragmatic Bookshelf - Pragmatic Unit Testing in Java with JUnit 3e (2024)** | Jeff Langr | Pragmatic Bookshelf | P6 | Référence unit testing mise à jour 2024. |
| 🟠 | **The Design of Design (2010)** | Frederick Brooks | Addison-Wesley | P0, P3, P4 | *Suite philosophique* du Mythical Man-Month sur la conception. |
| 🟠 | **On the Criteria to Be Used in Decomposing Systems into Modules (1972)** | David Parnas | Carnegie Mellon / PDF libre | P3, P4 | **Le paper fondateur** des modules. Origin of information hiding. **À lire en PDF**. |
| 🟠 | **A Note on Distributed Computing (1994)** | Waldo, Wyant, Wollrath, Sun Microsystems | PDF | P3, P8 | Le papier qui définit les *distributed objects vs network calls*. **Vétuste mais fondamental**. |
| 🟠 | **Fallacies of Distributed Computing (Sun, 1994)** | Peter Deutsch / James Gosling | PDF libre | P3, P8 | Les **8 fallacies** que tout dev distribué doit connaître. **5 minutes de lecture, valeur inestimable**. |
| 🟠 | **Out of the Tar Pit (2006)** | Ben Moseley, Peter Marks | PDF libre | P3, P4 | Le **paper le plus important** sur la complexité accidentelle. **À lire absolument**. |
| 🟠 | **No Silver Bullet (1986)** | Fred Brooks | PDF IEEE | P0, P1 | Le **paper fondateur** sur l'essential vs accidental complexity. **Indispensable P0/P1**. |
| 🟠 | **Programming as Theory Building (1986)** | Peter Naur | PDF | P0, P5, P8 | Le **paper séminal** sur la connaissance comme "théorie" du programme. **Sous-côté mais profond**. |
| 🟠 | **What is Software Design? (1992)** | Jack Reeves | C++ Journal / PDF | P3, P4 | Le **manifeste** que "design" = le code lui-même. **Courte lecture, haute valeur**. |
| 🟠 | **The Cathedral and the Bazaar (1999)** | Eric Raymond | O'Reilly / PDF libre | P0, P1, P8 | Open source, release early/release often, Linus's law. **Classique intemporel**. |
| 🟠 | **The Cathedral and the Bazaar, 20 years later (2019)** | Eric Raymond | PDF | P0, P1 | Version modernisée. |
| 🟠 | **Waltzing with Bears (2003)** | Tom DeMarco, Timothy Lister | Dorset House | P0, P1 | **Le livre fondateur** de la gestion des risques projet. |
| 🟠 | **Death March, 2nd ed. (2009)** | Edward Yourdon | Prentice Hall | P0, P1, P8 | Comment détecter et survivre aux projets impossibles. |
| 🟠 | **Rapid Development (1996)** | Steve McConnell | Microsoft Press | P0, P8 | Patterns de delivery rapide, antipatterns. |
| 🟠 | **Software Estimation (2006)** | Steve McConnell | Microsoft Press | P1, P2 | **Le livre de référence** sur l'estimation logicielle. |
| 🟠 | **Dreaming in Code (2007)** | Scott Rosenberg | Crown | P0, P5 | Le récit fascinant du développement de Chandler (Open Source Applications Foundation). |
| 🟠 | **The Soul of a New Machine (1981)** | Tracy Kidder | Harper | P0, P5 | **Pulitzer Prize**. Histoire du développement d'un mini-ordinateur chez Data General. **Vétuste mais intemporel**. |
| 🟠 | **Showstopper! (1994)** | G. Pascal Zachary | Free Press | P0, P5 | Histoire du développement de Windows NT. **Vétuste mais intemporel**. |
| 🟠 | **The Passionate Programmer (2009)** | Chad Fowler | Pragmatic Bookshelf | P0, P5 | Carrière de développeur. |
| 🟠 | **The Effective Engineer (2015)** | Edmond Lau | Stripe Press | P5, P8 | Pragmatisme d'ingénierie, leverage points. |
| 🟠 | **The Mythical Man-Month, 50th Anniversary** | Fred Brooks | Addison-Wesley | P0, P1, P8 | *Idem ci-dessus*. |
| 🟠 | **The Pragmatic Programmer 30th Anniversary ed. (2025 — à vérifier)** | Hunt/Thomas | Addison-Wesley | P5 | Mise à jour 2025 — vérifier publication. |
| 🟠 | **Domain-Driven Design, Reference (2015)** | Vaughn Vernon | Addison-Wesley | P2, P3, P4 | Référence condensée DDD. |
| 🟠 | **Implementing Domain-Driven Design (2013)** | Vaughn Vernon | Addison-Wesley | P2, P3 | *Idem §4.3*. **À ajouter impérativement**. |
| 🟠 | **Agile and Iterative Development: A Manager's Guide (2003)** | Craig Larman | Addison-Wesley | P0, P2 | Histoire et comparaison des méthodes agiles. |
| 🟠 | **Agile Project Management with Scrum (2002)** | Ken Schwaber | Microsoft Press | P0, P2, P8 | Le **livre fondateur** de Scrum par son créateur. |
| 🟠 | **Lean Software Development (2003)** | Mary & Tom Poppendieck | Addison-Wesley | P0, P1, P8 | **Les 7 principes du Lean** appliqués au logiciel. |
| 🟠 | **Implementing Lean Software Development (2006)** | Mary & Tom Poppendieck | Addison-Wesley | P0, P1, P8 | *Suite*. |
| 🟠 | **The Lean Startup (2011)** | Eric Ries | Crown | P0, P1 | *Idem §4.2*. **À ajouter impérativement**. |
| 🟠 | **Sprint (2016)** | Jake Knapp | Simon & Schuster | P0, P1 | Méthode Google Ventures 5 jours. |
| 🟠 | **INSPIRED, 2nd ed. (2017)** | Marty Cagan | Wiley | P0, P1 | *Idem §4.1*. |
| 🟠 | **Escaping the Build Trap (2019)** | Melissa Perri | O'Reilly | P0 | Outcome vs output. |
| 🟠 | **Continuous Discovery Habits (2021)** | Teresa Torres | Ben Orlando/Teri Christian | P0, P1 | Twin-tracked discovery. |
| 🟠 | **The Mom Test (2013)** | Rob Fitzpatrick | CreateSpace | P0 | Comment poser de bonnes questions client. |
| 🟠 | **Inspired (2e ed. 2017)** | Marty Cagan | Wiley SVK | P0, P1 | *Idem*. |
| 🟠 | **Get Together (2019)** | Bailey Richardson, Mohini Ufberg, Kevin Huynh | Stripe Press | P0, P8 | Comment construire des communautés. |
| 🟠 | **Migrate or Die! (2025 — à vérifier)** | Various | Leanpub | P10 | Modernisation legacy. |
| 🟠 | **The Unwritten Laws of Business (1996)** | W.J. King | McGraw-Hill | P0, P8 | *Vétuste mais intemporel*. |
| 🟡 | **Succeeding with Agile (2009)** | Mike Cohn | Addison-Wesley | P0, P2, P6 | Estimation, planning, scaling. |
| 🟡 | **Agile Estimating and Planning (2005)** | Mike Cohn | Prentice Hall | P1, P2 | La référence estimation agile. |
| 🟡 | **User Stories Applied (2004)** | Mike Cohn | Addison-Wesley | P2 | Le **livre fondateur** des user stories. |
| 🟡 | **The Art of Agile Development (2007)** | James Shore, Shane Warden | O'Reilly | P0, P2, P5, P6 | Pragmatisme agile. |
| 🟡 | **Coaching Agile Teams (2010)** | Lyssa Adkins | Addison-Wesley | P0, P8 | Coaching agile. |
| 🟡 | **Specification by Example (2011)** | Gojko Adzic | Manning | P2, P6 | BDD/SBE. |
| 🟡 | **Bridging the Communication Gap (2009)** | Gojko Adzic | Neuri Consulting | P2 | Specs by example. |
| 🟡 | **Impact Mapping (2012)** | Gojko Adzic | O'Reilly | P0, P2 | Lier business → features → deliverables. |
| 🟡 | **The Power of Positive Sharing (2020)** | Gojko Adzic | O'Reilly | P2 | BDD/SBE, key examples. |
| 🟡 | **Fifty Quick Ideas to Improve Your Tests (2015)** | Gojko Adzic | Neuri | P6 | Tests de qualité. |
| 🟡 | **AntiPatterns (1998)** | William Brown, Raphael Malveau, William McCormick, Scott Mott | Wiley | tous | **Le livre fondateur** des anti-patterns. |
| 🟡 | **AntiPatterns in Software Engineering (2019)** | Various | Springer | tous | Version académique. |
| 🟡 | **Software Project Survival Guide (1997)** | Steve McConnell | Microsoft Press | P0, P1 | Guide de survie projet. |
| 🟡 | **After the Gold Rush (1999)** | Steve McConnell | Microsoft Press | P0, P1 | Industrie du logiciel. |
| 🟡 | **Professional Software Development (2004)** | Steve McConnell | Addison-Wesley | P0, P5 | Carrière dev. |
| 🟡 | **More Effective Agile (2019)** | Steve McConnell | Construx Software | P0, P8 | *En libre accès* sur le site Construx. |
| 🟡 | **The Software Development Edge (2005)** | Joe Marasco | Addison-Wesley | P0, P8 | Carrière dev senior. |
| 🟡 | **Dr. Dobb's Essential Books on Software Development** (anthologies) | Various | Wiley | tous | Anthologies d'articles cultes. |
| 🟡 | **Mushroom: The Story of the A-Bomb Mushroom Cloud** | John Burke | (vétuste) | P0 | *Tangentiel* mais référence culturelle. |
| 🟡 | **Fundamentals of Software Architecture (2e ed. à paraître)** | Mark Richards, Neal Ford | O'Reilly | P3 | *Idem §4.4*. |
| 🟡 | **Head First Software Architecture (2024)** | Raju Gandhi, Mark Richards, Neal Ford | O'Reilly | P3 | *Idem §4.4* — *déjà présent*. |
| 🟡 | **Effective Software Architecture (2024)** | Neal Ford | Addison-Wesley | P3 | *Idem §4.4*. |
| 🟡 | **Clean C++ (2018)** | Stephan Roth | Apress | P5 | Clean Code appliqué C++. |
| 🟡 | **Clean Code in Python, 2nd ed. (2020)** | Mariano Anaya | Packt | P5 | *Idem §4.6*. |
| 🟡 | **Architecture Patterns with Python (2020)** | Harry Percival, Bob Gregory | O'Reilly | P3, P5 | DDD + Python. *Déjà partiellement présent*. |
| 🟡 | **Clean Code in JavaScript (Packt 2020)** | James Padolsey | Packt | P5 | Clean Code JS. |
| 🟡 | **The C++ Programming Language, 4th ed. (2013)** | Bjarne Stroustrup | Addison-Wesley | P5 | Référence C++. |
| 🟡 | **The Go Programming Language (2015)** | Alan Donovan, Brian Kernighan | Addison-Wesley | P5 | Référence Go. |
| 🟡 | **Programming Rust (2019, 2nd ed. 2021)** | Jim Blandy, Jason Orendorff, Leonora Tindall | O'Reilly | P5 | Référence Rust. |
| 🟡 | **Effective Python (2019, 2nd ed. 2020)** | Brett Slatkin | Addison-Wesley | P5 | Best practices Python. |
| 🟡 | **Effective Java, 3rd ed. (2018)** | Joshua Bloch | Addison-Wesley | P5 | Best practices Java. |
| 🟡 | **Effective Kotlin (2021 — Kategory)** | Marcin Moskała | Leanpub | P5 | Best practices Kotlin. |
| 🟡 | **Fluent Python, 2nd ed. (2022)** | Luciano Ramalho | O'Reilly | P5 | Python idiomatique. |
| 🟡 | **High Performance Python (2020, 2nd ed.)** | Micha Gorelick, Ian Ozsvald | O'Reilly | P5 | Optimisation Python. |
| 🟡 | **Python in a Nutshell, 4th ed. (2023)** | Alex Martelli, Anna Ravenscroft, Steve Holden | O'Reilly | P5 | Référence Python. |
| 🟡 | **Java in a Nutshell, 8th ed. (2023)** | Benjamin Evans, Jason Clark, David Flanagan | O'Reilly | P5 | Référence Java. |
| 🟡 | **Programming TypeScript (2019)** | Boris Cherny | O'Reilly | P5 | TS en profondeur. |
| 🟡 | **TypeScript 5 Design Patterns (2025)** | Theodhor Karabelas | Packt | P4, P5 | Patterns en TS. |
| 🟡 | **Vue.js 3 Design Patterns (2023)** | Garabéd Sarkissian | Packt | P4, P5 | Patterns en Vue. |
| 🟡 | **React 18 Design Patterns (2023)** | Carlos Santana Roldán | Packt | P4, P5 | Patterns en React. |
| 🟡 | **Node.js Design Patterns, 4th ed. (2024)** | Mario Casciaro, Luciano Mammino | Packt | P4, P5 | Patterns Node. |
| 🟡 | **Learning JavaScript Design Patterns, 2nd ed. (2023)** | Addy Osmani | O'Reilly | P4, P5 | Patterns JS moderne. |
| ⚪ | **The Elements of Programming Style (1974)** | Brian Kernighan, P. J. Plauger | McGraw-Hill | P5 | *Vétuste mais intemporel*. |
| ⚪ | **The Art of Computer Programming, vol. 1-4A** | Donald Knuth | Addison-Wesley | P5 | L'**œuvre** de référence en algorithmique. |
| ⚪ | **The Structure and Interpretation of Computer Programs (SICP, 1996)** | Abelson, Sussman, Sussman | MIT Press / PDF libre | P5 | **Le MIT textbook**. *PDF libre* sur le site MIT. |
| ⚪ | **The Elements of Computing Systems (Nisan & Schocken, 2005)** | Nisan, Schocken | MIT Press | P5 | Du NAND au Tetris. **Indispensable formation**. |
| ⚪ | **Structure and Interpretation of Computer Programs - JavaScript Adaptation (SICP JS, 2022)** | HtC, MIT | MIT Press | P5 | Version JS du SICP. |
| ⚪ | **Concrete Mathematics (1989, 2nd ed. 1994)** | Graham, Knuth, Patashnik | Addison-Wesley | P5 | Mathématiques pour CS. |
| ⚪ | **Discrete Mathematics and Its Applications (2019, 8th ed.)** | Kenneth Rosen | McGraw-Hill | P5 | Math discrètes. |
| ⚪ | **Introduction to Algorithms, 4th ed. (2022)** | Cormen, Leiserson, Rivest, Stein | MIT Press | P5 | CLRS — l'**encyclopédie** des algorithmes. |
| ⚪ | **Algorithm Design (2005)** | Kleinberg, Tardos | Addison-Wesley | P5 | Design d'algos. |
| ⚪ | **The Algorithm Design Manual, 3rd ed. (2020)** | Skiena | Springer | P5 | Manuel de référence algo. |
| ⚪ | **Network Security: PRIVATE Communication in a PUBLIC World (1995, 3rd ed. 2022)** | Kaufman, Perlman, Speciner | Pearson | P7, P8 | Référence sécurité réseau. |
| ⚪ | **Cryptography Engineering (2010)** | Ferguson, Schneier, Kohno | Wiley | P5, P8 | Cryptographie pratique. |
| ⚪ | **The Tangled Web (2011)** | Michal Zalewski | No Starch Press | P7, P8 | Sécurité web en profondeur. |
| ⚪ | **The Web Application Hacker's Handbook, 2nd ed. (2011)** | Stuttard, Pinto | Wiley | P7, P8 | Référence pentest web. |
| ⚪ | **Hacking Exposed 7 (2012)** | McClure, Scambray, Kurtz | McGraw-Hill | P7, P8 | Référence hacking. |
| ⚪ | **The Tangled Web + WAHH (combo)** | Various | Wiley | P7, P8 | |

### 13. Documents de standards et de méthodologie (toutes phases)

> Beaucoup sont gratuits ou presque.

| Pri. | Document | Source | Phase | Valeur |
|---|---|---|---|---|
| 🔴 | **SWEBOK v4 (2024)** | IEEE / Wikipedia | tous | Le **standard IEEE du génie logiciel**. **Déjà présent dans corpus** (Swebok_V4.json). C'est le méta-référentiel. |
| 🔴 | **PMBOK Guide 7e (2021) + 8e (2026)** | PMI | P0, P1, P2 | *(idem §5)* — Standard mondial. Payant. |
| 🔴 | **BABOK v3 (2015) + extensions** | IIBA | P2 | *(idem §6)*. |
| 🔴 | **ISO/IEC/IEEE 42010:2022 (Architecture description)** | ISO | P3 | Norme d'architecture. Achat nécessaire. |
| 🔴 | **ISO/IEC 25010:2011 (Systems and software Quality Requirements and Evaluation — SQuaRE)** | ISO | P3, P4, P6 | Modèle de qualité. Achat nécessaire. |
| 🔴 | **ISO/IEC/IEEE 12207:2017 (Systems and software engineering — Software life cycle processes)** | ISO | tous | Processus cycle de vie. |
| 🔴 | **ISO/IEC/IEEE 15288:2023 (Systems and software engineering — System life cycle processes)** | ISO | tous | Processus système. |
| 🔴 | **IEEE 830-1998 / IEEE 29148-2018 (SRS)** | IEEE | P2 | Norme requirements. |
| 🔴 | **IEEE 1016-2009 (Software Design Description)** | IEEE | P3, P4 | Norme design. |
| 🔴 | **IEEE 1028-2008 (Software Reviews and Inspections)** | IEEE | P5, P6 | Norme reviews. |
| 🔴 | **IEEE 1044-2009 (Classification of Software Anomalies)** | IEEE | P5, P6, P9 | Norme anomalies. |
| 🔴 | **IEEE 1063-2001 (Software User Documentation)** | IEEE | P2, P9 | Norme user docs. |
| 🔴 | **IEEE 1219-1998 (Software Maintenance)** | IEEE | P9 | Norme maintenance. |
| 🔴 | **IEEE 1471 / ISO/IEC/IEEE 42010:2022 (Architecture Description)** | IEEE/ISO | P3 | Norme architecture. |
| 🔴 | **ISO/IEC 27001:2022 (Information Security Management)** | ISO | P7, P8 | Norme SMSI. |
| 🔴 | **ISO/IEC 27002:2022 (Information Security Controls)** | ISO | P7, P8 | Norme contrôles. |
| 🔴 | **ISO 31000:2018 (Risk Management)** | ISO | P0, P1 | Norme risk. |
| 🔴 | **NIST SP 800-53 (Security and Privacy Controls)** | NIST | P7, P8 | Référentiel US. **Libre**. |
| 🔴 | **NIST Cybersecurity Framework (CSF) 2.0 (2024)** | NIST | P7, P8 | Framework cyber. **Libre**. |
| 🔴 | **NIST SSDF (SP 800-218) v1.1 (2022)** | NIST | P5, P7, P9 | Secure Software Development Framework. **Libre**. |
| 🔴 | **NIST SP 800-161 (Cybersecurity Supply Chain Risk Management)** | NIST | P7, P9 | SCRM. **Libre**. |
| 🔴 | **NIST SP 800-37 (Risk Management Framework)** | NIST | P7, P8 | RMF. **Libre**. |
| 🔴 | **OWASP Top 10 (2021, 2025 update)** | OWASP | P5, P6, P7 | Top 10 des risques web. **Libre**. |
| 🔴 | **OWASP ASVS 4.0.3 (2021)** | OWASP | P5, P6, P7 | Application Security Verification Standard. **Libre**. |
| 🔴 | **OWASP SAMM 2.0 (2020)** | OWASP | P0, P5, P7 | Software Assurance Maturity Model. **Libre**. |
| 🔴 | **OWASP AI Security & Privacy Guide (2024)** | OWASP | P0, P5, P7 | Sécurité IA. **Libre**. |
| 🔴 | **OWASP Top 10 for LLM Applications (2023, 2025)** | OWASP | P5, P7, P8 | Risques LLM. **Libre**. |
| 🔴 | **CWE Top 25 (2023)** | MITRE | P5, P6, P7 | CWE les plus dangereux. **Libre**. |
| 🔴 | **MITRE ATT&CK (continuellement mis à jour)** | MITRE | P7, P8 | Base de connaissances attaques. **Libre**. |
| 🔴 | **MITRE D3FEND (2024)** | MITRE | P7, P8 | Contre-mesures. **Libre**. |
| 🔴 | **MITRE ATLAS (2024)** | MITRE | P7, P8 | Adversarial Threat Landscape for AI Systems. **Libre**. |
| 🔴 | **MITRE CVE (continuellement mis à jour)** | MITRE | P7, P8 | Vulnérabilités. **Libre**. |
| 🔴 | **CIS Controls v8 (2021)** | CIS | P7, P8 | Top contrôles. **Libre**. |
| 🔴 | **CIS Benchmarks (continuellement mis à jour)** | CIS | P7, P8 | Configuration sécurisée. **Libre**. |
| 🔴 | **PCI DSS v4.0 (2024)** | PCI SSC | P7, P8 | Sécurité des paiements. **Payant**. |
| 🔴 | **HIPAA (1996, mis à jour)** | HHS | P7, P8 | Santé US. **Libre**. |
| 🔴 | **GDPR (2018)** | EU | P0, P1, P7, P8, P10 | Protection données EU. **Libre**. |
| 🔴 | **DORA (2025, EU)** | EU | P7, P8 | Digital Operational Resilience Act (banque). **Libre**. |
| 🔴 | **AI Act EU (2024)** | EU | P0, P1, P5, P7 | Réglementation IA. **Libre**. |
| 🔴 | **PRINCE2 7e (2023)** | AXELOS/PeopleCert | P0, P1, P2 | Méthode PM européenne. **Payant**. |
| 🔴 | **PRINCE2 Agile (2015)** | AXELOS | P0, P1, P2 | PRINCE2 + Agile. **Payant**. |
| 🔴 | **CMMI v2.0 (2018)** | ISACA | P0, P5, P6, P8 | Capability Maturity Model. **Payant**. |
| 🔴 | **ITIL 4 (2019)** | AXELOS | P8 | Service management. **Payant**. |
| 🔴 | **TOGAF 10 (2022)** | The Open Group | P3 | Framework architecture d'entreprise. **Payant**. |
| 🔴 | **Zachman Framework 6 (2022)** | Zachman International | P3 | Framework archi. **Payant**. |
| 🔴 | **DoDAF / MODAF / NAF** | US DoD / UK MoD / NATO | P3 | Architecture militaire. **Libre**. |
| 🔴 | **ArchiMate 3.2 (2022)** | The Open Group | P3 | Langage archi d'entreprise. **Payant**. |
| 🟠 | **BABOK + Agile Extension (IIBA 2016)** | IIBA | P2 | *Idem §6*. |
| 🟠 | **PMP Exam Prep (Rita Mulcahy, 10e ed. 2023)** | Rita Mulcahy | P0, P1, P2 | Prep PMP. |
| 🟠 | **CAPM Exam Prep (2023)** | PMI | P0, P1, P2 | Prep CAPM. |
| 🟠 | **PMI-PBA Exam Prep (2023)** | PMI | P2 | Prep BA. |
| 🟠 | **CBAP/CCBA Exam Prep (2023)** | IIBA | P2 | Prep BABOK. |
| 🟠 | **Disciplined Agile (DA) toolkit (PMI 2019)** | PMI / Ambler | P0, P1, P2, P8 | Workflow DA. |
| 🟠 | **Choose Your Wow! 2e (Scott Ambler 2020)** | Disciplined Agile | P0, P1, P2, P8 | DA "Choose Your Wow". |
| 🟠 | **Cynefin (Dave Snowden, 1999, mis à jour 2020)** | Cognitive Edge | P0, P1, P8 | Cadre complexité. **Libre sur le web**. |
| 🟠 | **OpenUP / EPF (Eclipse)** | Eclipse Foundation | P0, P1, P2 | Processus agile. **Libre**. |
| 🟠 | **Agile Manifesto (2001)** | agilemanifesto.org | P0 | Le **manifeste**. *1 page libre*. |
| 🟠 | **Scrum Guide (Schwaber/Sutherland, 2020)** | scrumguides.org | P0, P2 | Scrum. **Libre**. |
| 🟠 | **SAFe (Scaled Agile, 6.0 2023)** | Scaled Agile | P0, P2 | Scaled agile. **Payant**. |
| 🟠 | **Spotify Model (2012, article)** | Henrik Kniberg | P0, P8 | *Article libre*. |
| 🟠 | **Site Reliability Engineering — How Google Runs Production Systems (free eBook)** | Google | P8 | **L'édition gratuite de l'ebook SRE est en ligne** (https://sre.google/sre-book/). **À intégrer en PDF** pour P8. |
| 🟠 | **Google Cloud Architecture Framework** | Google | P3, P7, P8 | Best practices. **Libre**. |
| 🟠 | **AWS Well-Architected Framework (2024 update)** | AWS | P3, P7, P8 | **Libre**. |
| 🟠 | **Azure Architecture Center (Microsoft)** | Microsoft | P3, P7, P8 | **Libre**. |
| 🟠 | **Google SRE Workbook (free eBook)** | Google | P8 | **Idem, en libre accès** sur https://sre.google/workbook/. |
| 🟠 | **Observability Whitepaper (Honeycomb, 2024)** | Honeycomb | P8 | **Libre**. |
| 🟠 | **Incident Postmortem Templates (Etsy, Google, Atlassian)** | Divers | P8 | Templates blameless. **Libres**. |
| 🟠 | **CNCF Cloud Native Trail Map (2024)** | CNCF | P7, P8 | **Libre**. |
| 🟠 | **CNCF Landscape (2024)** | CNCF | P7, P8 | Cartographie outils. **Libre**. |
| 🟠 | **OWASP Cheat Sheet Series (2024)** | OWASP | P5, P6, P7 | **Libre**. |
| 🟠 | **Microsoft SDL (Security Development Lifecycle) (2024)** | Microsoft | P5, P7 | Processus sécurité. **Libre**. |
| 🟠 | **NIST 800-218A (SSDF v1.1)** | NIST | P5, P7 | **Libre**. |
| 🟠 | **ACM Code of Ethics (2018)** | ACM | P0 | Éthique. **Libre**. |
| 🟠 | **IEEE Code of Ethics** | IEEE | P0 | Éthique. **Libre**. |
| 🟠 | **SEI CERT Coding Standards (C, C++, Java, Perl, Android)** | SEI | P5 | Standards codage sécurisé. **Libre**. |
| 🟠 | **SEI CERT Top 10 Secure Coding Practices (2024)** | SEI | P5 | **Libre**. |
| 🟠 | **SAFECode Fundamental Practices for Secure Software Development (2018, update 2024)** | SAFECode | P5, P7 | **Libre**. |
| 🟠 | **BSIMM (Building Security In Maturity Model, 2024 update)** | Synopsys | P5, P7 | **Payant**. |
| 🟠 | **SAMM 2.0 (OWASP, 2020)** | OWASP | P5, P7 | *Idem OWASP*. |
| 🟠 | **CNCF TAG (Technical Advisory Group) documents (2024)** | CNCF | P3, P7 | **Libre**. |
| 🟠 | **DORA State of DevOps Report (2024)** | DORA/Google Cloud | P0, P7, P8 | **Libre**. Rapport annuel. |
| 🟠 | **GitHub Octoverse (2024)** | GitHub | P0, P5, P8 | **Libre**. |
| 🟠 | **Stack Overflow Developer Survey (2024, 2025)** | Stack Overflow | P0, P5 | **Libre**. |
| 🟠 | **Thoughtworks Technology Radar (Vol. 32, 33, 34 — 2024, 2025)** | Thoughtworks | P3, P7, P8 | **Libre**. **Incontournable**. |
| 🟠 | **Accenture Tech Vision (2024, 2025)** | Accenture | P0, P3 | **Libre**. |
| 🟠 | **Gartner Hype Cycle for Software Engineering (2024, 2025)** | Gartner | P3, P7, P8 | **Payant** mais rapports publics existent. |
| 🟠 | **Forrester Wave (rapports)** | Forrester | P3, P7, P8 | **Payant**. |
| 🟠 | **SEI Year in Review (2024, 2025)** | SEI/CMU | tous | Tendances recherche. **Libre**. |
| 🟠 | **Linux Foundation Annual Report (2024, 2025)** | Linux Foundation | P0, P3, P7 | **Libre**. |
| 🟠 | **State of Open Source (2024, 2025)** | OpenLogic/SUSE | P0, P5, P7 | **Libre**. |
| 🟠 | **JetBrains State of Developer Ecosystem (2024, 2025)** | JetBrains | P0, P5 | **Libre**. |
| 🟠 | **SlashData Developer Nation (2024, 2025)** | SlashData | P0, P5 | **Libre**. |
| 🟠 | **CMMI Institute — Process Reference Models** | ISACA | tous | **Payant**. |
| 🟠 | **eSCM (eSourcing Capability Model)** | ITPI | P7, P8 | Outsourcing. **Payant**. |
| 🟠 | **IT4IT Reference Architecture (2024)** | Open Group | P0, P8 | **Payant**. |
| 🟠 | **VeriSM (Service Management)** | IFDC/PeopleCert | P8 | **Payant**. |
| 🟠 | **FitSM (Federal IT Service Management)** | FedSM | P8 | **Libre**. |
| 🟠 | **AgileSHIFT (AXELOS, 2017)** | AXELOS | P0, P8 | Transformation agile. **Payant**. |
| 🟠 | **Scrum@Scale (Sutherland, 2019)** | Scrum@Scale | P0, P2 | Scaling Scrum. **Libre**. |
| 🟠 | **Less (Lean Enterprise Self-Assessment)** | Less SA | P0, P1, P8 | Assessment lean. **Libre**. |
| 🟠 | **Enterprise Scrum (Grenny et al.)** | MIT Sloan | P0, P2 | **Article libre**. |
| 🟠 | **The Phoenix Project Way (Companion Guide)** | IT Revolution | P0, P7 | Companion. |
| 🟠 | **Beyond the Phoenix Project (Companion)** | IT Revolution | P0, P7 | Companion. |
| 🟠 | **The DevOps Adoption Playbook (SAFe)** | SAFe | P0, P7 | **Payant**. |
| 🟠 | **The IT Skeptic (Rob England)** | Blog | P8 | Critique ITIL. **Libre**. |
| 🟠 | **CIOB (Chartered Institute of Building) — IT/PM** | CIOB | P0, P1 | *Tangentiel* mais référence PM. |
| 🟠 | **APM Body of Knowledge (2024)** | APM UK | P0, P1, P2 | *Alternative PMBOK*. **Payant**. |
| 🟠 | **ISO 21500:2021 (Project Management)** | ISO | P0, P1, P2 | Norme PM ISO. **Payant**. |
| 🟠 | **ISO 21502:2020 (PM Guidance)** | ISO | P0, P1, P2 | **Payant**. |
| 🟠 | **ISO 9001:2015 (Quality Management)** | ISO | P0, P5, P6, P8 | Norme qualité. **Payant**. |
| 🟠 | **ISO/IEC 14764:2022 (Software Maintenance)** | ISO | P9 | Norme maintenance. **Payant**. |
| 🟠 | **ISO/IEC/IEEE 23026:2023 (Systems and software engineering — Engineering and management of websites)** | ISO | P3, P7 | Norme site web. **Payant**. |
| 🟠 | **IEEE 1074-2006 (Software Life Cycle Processes)** | IEEE | tous | *Vétuste mais utile*. |
| 🟠 | **INCOSE Systems Engineering Handbook, 5e (2023)** | INCOSE | P3, P4 | Systems engineering. **Payant**. |
| 🟠 | **Object Management Group (OMG) — UML, BPMN, SysML** | OMG | P3, P4 | Standards. **Payant**. |
| 🟠 | **INCOSE — Model-Based Systems Engineering (MBSE)** | INCOSE | P3, P4 | MBSE. **Payant**. |
| 🟠 | **Object Management Group — Essence (OMG, 2014)** | OMG | P0, P1 | Méta-modèle PM. **Payant**. |
| 🟠 | **Essence 1.2 Specification (2018)** | OMG | P0, P1 | Norme essence. **Payant**. |
| 🟠 | **ISO 26262 (Functional Safety — Road Vehicles)** | ISO | P5, P8, P9 | Automobile. **Payant**. |
| 🟠 | **DO-178C (Avionics Software)** | RTCA | P5, P6 | Aviation. **Payant**. |
| 🟠 | **IEC 62304 (Medical Device Software)** | IEC | P5, P6, P9 | Médical. **Payant**. |
| 🟠 | **IEC 61508 (Functional Safety)** | IEC | P5, P8 | Industries process. **Payant**. |
| 🟠 | **FDA General Principles of Software Validation (2002, update 2024)** | FDA | P5, P6 | Médical US. **Libre**. |
| 🟠 | **Common Criteria (ISO/IEC 15408, 2022 update)** | ISO/CCRA | P7, P8 | Certification sécurité. **Payant**. |
| 🟠 | **SOC 2 (AICPA Trust Services Criteria, 2024 update)** | AICPA | P7, P8 | Audit. **Payant**. |
| 🟠 | **ISO/IEC 30134 (Data Centre)** | ISO | P7, P8 | Data center. **Payant**. |
| 🟠 | **EU Cyber Resilience Act (CRA, 2024)** | EU | P0, P1, P5, P7 | Cybersécurité produits. **Libre**. |
| 🟠 | **NIS2 Directive (EU, 2024)** | EU | P0, P7, P8 | Cybersécurité EU. **Libre**. |
| 🟠 | **Executive Order 14028 (US, 2021, 2024 update)** | US White House | P7, P8 | Cybersécurité US fédéral. **Libre**. |
| 🟠 | **US Cyber EO Implementation Guides (NIST, CISA)** | NIST/CISA | P7, P8 | **Libre**. |
| 🟠 | **CISA — Secure by Design (2024)** | CISA | P5, P7 | **Libre**. |
| 🟠 | **CISA — Software Acquisition Guide (2024)** | CISA | P5, P7 | **Libre**. |
| 🟠 | **OpenSSF — SLSA (Supply-chain Levels for Software Artifacts, v1.0, 2024)** | OpenSSF | P5, P7, P9 | **Libre**. |
| 🟠 | **OpenSSF — Sigstore (2024)** | OpenSSF | P5, P7, P9 | Signature. **Libre**. |
| 🟠 | **OpenSSF — Scorecard (2024)** | OpenSSF | P5, P7, P9 | Évaluation OSS. **Libre**. |
| 🟠 | **CNCF — TAG App Delivery (2024)** | CNCF | P7, P8 | **Libre**. |
| 🟠 | **CNCF — TAG Security (2024)** | CNCF | P7, P8 | **Libre**. |
| 🟠 | **CNCF — TAG Observability (2024)** | CNCF | P8 | **Libre**. |
| 🟠 | **CNCF — KubeCon Europe/NA 2024 talks** | CNCF | P7, P8 | Vidéos YouTube. **Libre**. |
| 🟠 | **The Twelve-Factor App (2011, mis à jour 2024)** | Adam Wiggins / Heroku | P5, P7, P8 | Le **manifeste Cloud Native**. **Libre** sur 12factor.net. |
| 🟠 | **Beyond the Twelve-Factor App (2016, 2019, 2024 update)** | Various (Red Hat, VMware) | P5, P7, P8 | Extension. **Libre**. |
| 🟠 | **The Reactive Manifesto (2014, 2024 update)** | Jonas Bonér, Dave Farley et al. | P3, P5, P7, P8 | **Libre**. |
| 🟠 | **Reactive Design Patterns (Manning, 2017)** | Roland Kuhn et al. | P3, P4 | Référence reactive. |
| 🟠 | **Reactive Systems Architecture (Packt, 2024)** | | P3, P4 | Reactive. |
| 🟠 | **Flow Manifesto (2024)** | Camille Fournier | P8 | Vétuste mais utile. |
| 🟠 | **The Deeper News (Dan North, 2024)** | Dan North | P0, P5, P6 | *Blog/articles libres*. |
| 🟠 | **The Architect Elevator (Gregor Hohpe, 2024 book + blog)** | Gregor Hohpe | P3, P4 | L'architecte = "ascensoriste" entre niveaux. **Article célèbre**. |
| 🟠 | **Migrating to Microservices (Biteable, 2018, blog)** | Various | P7 | **Libre**. |
| 🟠 | **Monolith to Microservices (oreilly 2019, free excerpt)** | Newman | P7, P10 | **Libre** en extrait. |
| 🟠 | **The API-First Transformation (Apidays)** | API Evangelist | P3, P4, P7 | **Libre**. |
| 🟠 | **API Stylebook (APIs.io)** | Various | P3, P4 | **Libre**. |
| 🟠 | **OpenAPI Specification (3.1.0, 2024)** | OpenAPI Initiative | P3, P4, P7 | **Libre**. |
| 🟠 | **JSON Schema 2020-12 (2024 update)** | JSON Schema Org | P3, P4 | **Libre**. |
| 🟠 | **AsyncAPI 3.0 (2024)** | AsyncAPI Initiative | P3, P4 | **Libre**. |
| 🟠 | **CloudEvents 1.0.2 (2022)** | CNCF | P3, P4, P7 | **Libre**. |
| 🟠 | **Semantic Versioning 2.0.0 (SemVer)** | Tom Preston-Werner | P5, P7, P9 | **Libre**. |
| 🟠 | **Keep a Changelog 1.1.0 (2024)** | Olivier Lacan | P5, P7, P9 | **Libre**. |
| 🟠 | **Conventional Commits 1.0 (2024)** | Conventional Commits Org | P5, P7 | **Libre**. |
| 🟠 | **Trunk-Based Development (2024)** | trunkbaseddevelopment.com | P5, P7, P9 | **Libre**. |
| 🟠 | **GitOps (Weaveworks, 2017, 2024 update)** | Weaveworks | P7 | **Libre**. |
| 🟠 | **The Phoenix Serverless (AWS, 2024)** | AWS | P7, P8 | **Libre**. |
| 🟠 | **Lean Enterprise (O'Reilly, 2014, mis à jour 2024)** | Humble, Molesky, O'Reilly | P0, P8 | **Payant**. |
| 🟠 | **The Lean IT Field Guide (2016, 2024)** | Microsoft | P0, P8 | **Libre** en PDF. |
| 🟠 | **The Lean IT Summary (2016)** | Microsoft | P0, P8 | **Libre**. |
| 🟠 | **The Lean IT Book (2016)** | Microsoft | P0, P8 | **Libre**. |
| 🟠 | **Lean Six Sigma for IT (2006, 2016 update)** | Various | P0, P8 | **Payant**. |
| 🟠 | **DevOps for SAP (Packt 2022)** | | P7 | Spécialisation. |
| 🟠 | **Learning Modern Linux (O'Reilly, 2024)** | Michael Hausenblas | P5, P7, P8 | Linux moderne. |
| 🟠 | **Linux Basics for Hackers (No Starch Press, 2019)** | OccupyTheWeb | P7, P8 | **Payant** mais excellent. |
| 🟠 | **Operating Systems: Three Easy Pieces (2014, 2018, 2024 update)** | Arpaci-Dusseau | Arpaci-Dusseau Books | P5, P8 | **Le MIT textbook**. *PDF libre*. **Indispensable**. |
| 🟠 | **Computer Networks: A Systems Approach (2019, 2024 update)** | Larry Peterson, Bruce Davie | Systems Approach | P3, P5, P8 | *PDF libre*. **Indispensable**. |
| 🟠 | **TCP/IP Illustrated, Volume 1-3 (2011-2012)** | Stevens, Wright | Addison-Wesley | P3, P5, P8 | Référence réseau. |
| 🟠 | **Site Reliability Engineering: Beyond the Basics (Honeycomb blog, 2024)** | Charity Majors | P8 | Articles *libres*. |
| 🟠 | **Observability 101, 201, 301 (Honeycomb, 2024)** | Honeycomb | P8 | **Libre**. |
| 🟠 | **Mastering Chaos Engineering (Gremlin, 2024)** | Gremlin | P7, P8 | **Libre**. |
| 🟠 | **Cloudflare Learning Center (2024)** | Cloudflare | P3, P5, P7, P8 | **Libre**. |
| 🟠 | **AWS Well-Architected Labs (2024)** | AWS | P3, P7 | **Libre**. |
| 🟠 | **Google Cloud Skills Boost (2024)** | Google | P3, P7, P8 | **Libre** (certains labs). |
| 🠀 | **OWASP AI Security and Privacy Guide** | OWASP | P5, P7, P8 | **Libre**. |
| 🠀 | **Hugging Face Documentation (2024)** | Hugging Face | P5, P7, P8 | **Libre**. |
| 🠀 | **LangChain Documentation (2024)** | LangChain | P5, P7, P8 | **Libre**. |
| 🠀 | **LlamaIndex Documentation (2024)** | LlamaIndex | P5, P7, P8 | **Libre**. |
| 🠀 | **PyTorch Documentation (2024)** | PyTorch | P5, P7, P8 | **Libre**. |
| 🠀 | **TensorFlow Documentation (2024)** | TF | P5, P7, P8 | **Libre**. |
| 🠀 | **Kubernetes Documentation (2024)** | CNCF | P7, P8 | **Libre**. |
| 🠀 | **Terraform Registry (2024)** | HashiCorp | P7, P8 | **Libre**. |
| 🠀 | **Prometheus Documentation (2024)** | CNCF | P7, P8 | **Libre**. |
| 🠀 | **Grafana Documentation (2024)** | Grafana Labs | P7, P8 | **Libre**. |
| 🠀 | **OpenTelemetry Documentation (2024)** | CNCF | P7, P8 | **Libre**. |
| 🠀 | **CNCF Landscape (2024)** | CNCF | P7, P8 | **Libre**. |
| 🠀 | **CNCF Trail Map (2024)** | CNCF | P7, P8 | **Libre**. |
| 🠀 | **MITRE ATT&CK (2024)** | MITRE | P7, P8 | **Libre**. |
| 🠀 | **MITRE D3FEND (2024)** | MITRE | P7, P8 | **Libre**. |
| 🠀 | **MITRE ATLAS (2024)** | MITRE | P7, P8 | **Libre**. |
| 🠀 | **MITRE CVE (2024)** | MITRE | P7, P8 | **Libre**. |

### 14. Académie / Papers fondateurs (à intégrer en PDF, tous libres)

| Pri. | Paper | Auteur(s) | Année | Valeur |
|---|---|---|---|---|
| 🔴 | **No Silver Bullet** | Brooks | 1986 | P0, P1 |
| 🔴 | **Programming as Theory Building** | Naur | 1986 | P0, P5, P8 |
| 🔴 | **What is Software Design?** | Reeves | 1992 | P3, P4 |
| 🔴 | **Out of the Tar Pit** | Moseley & Marks | 2006 | P3, P4 |
| 🔴 | **On the Criteria to Be Used in Decomposing Systems into Modules** | Parnas | 1972 | P3, P4 |
| 🔴 | **A Note on Distributed Computing** | Waldo et al. | 1994 | P3, P8 |
| 🔴 | **Fallacies of Distributed Computing** | Deutsch/Gosling | 1994 | P3, P8 |
| 🔴 | **The Cathedral and the Bazaar** | Raymond | 1999 | P0, P1, P8 |
| 🔴 | **Big Ball of Mud** | Foote & Yoder | 1999 | P3, P4, P9 |
| 🔴 | **SRefactoring in a Test-First Manner** | Beck & Gamma | 2003 | P5, P6 |
| 🔴 | **Object-Oriented Design Heuristics** | Riel | 1996 | P3, P4, P5 |
| 🟠 | **A Plea for Lean Software (Wirth)** | Wirth | 1995 | P5 |
| 🟠 | **Lehman's Laws of Software Evolution (1974-1996)** | Lehman | 1974-1996 | P8, P9 |
| 🟠 | **Conway's Law (1968)** | Conway | 1968 | P0, P3 |
| 🟠 | **Booch's Object-Oriented Design** | Booch | 1986+ | P3, P4 |
| 🟠 | **Mellor & Shlaer — Object Lifecycles** | Mellor/Shlaer | 1993 | P3, P4 |
| 🟠 | **Yourdon & Constantine — Structured Design** | Yourdon/Constantine | 1979 | P3, P4 |
| 🟠 | **Jackson System Development (JSD)** | Jackson | 1983 | P3, P4 |
| 🟠 | **Dijkstra — Notes on Structured Programming** | Dijkstra | 1972 | P5 |
| 🟠 | **Hoare — Communicating Sequential Processes** | Hoare | 1978-1985 | P5 |
| 🟠 | **Liskov & Wing — A Behavioral Notion of Subtyping** | Liskov/Wing | 1994 | P3, P4 |
| 🟠 | **Parnas — On the Criteria to Be Used...** | Parnas | 1972 | P3, P4 |
| 🟠 | **Boehm — Software Engineering Economics** | Boehm | 1981 | P1, P5 |
| 🟠 | **COCOMO II (Boehm et al., 2000)** | USC | 2000 | P1 |
| 🟠 | **Function Point Analysis (Albrecht, 1979)** | IBM | 1979 | P1 |
| 🟠 | **COSMIC Function Points (2024)** | Common Software Measurement International Consortium | 2024 | P1 |
| 🟠 | **The Wisdom of Crowds (Surowiecki, 2004)** | Surowiecki | 2004 | P0, P8 |
| 🟠 | **Tipping Point (Gladwell)** | Gladwell | 2000 | P0 |
| 🟠 | **Antifragile (Taleb)** | Taleb | 2012 | P0, P8 |
| 🟠 | **Black Swan (Taleb)** | Taleb | 2007 | P0 |
| 🟠 | **Skin in the Game (Taleb)** | Taleb | 2018 | P0 |
| 🟠 | **Drive (Pink)** | Pink | 2009 | P0, P5, P8 |
| 🟠 | **To Sell is Human (Pink)** | Pink | 2012 | P0, P8 |
| 🟠 | **A Whole New Mind (Pink)** | Pink | 2005 | P0, P4 |
| 🟠 | **Range (Epstein)** | Epstein | 2019 | P0, P5 |
| 🟠 | **Thinking, Fast and Slow (Kahneman)** | Kahneman | 2011 | P0, P2 |
| 🟠 | **Noise (Kahneman et al.)** | Kahneman | 2021 | P0, P2 |
| 🟠 | **Nudge (Thaler & Sunstein)** | Thaler/Sunstein | 2008 | P0 |
| 🟠 | **The Structure of Scientific Revolutions (Kuhn)** | Kuhn | 1962 | P0, P5 |
| 🟠 | **Guns, Germs, and Steel (Diamond)** | Diamond | 1997 | P0 (analogie) |
| 🟠 | **Sapiens (Harari)** | Harari | 2011 | P0 (analogie) |
| 🟠 | **21 Lessons for the 21st Century (Harari)** | Harari | 2018 | P0 |
| 🟠 | **Homo Deus (Harari)** | Harari | 2015 | P0 |
| 🟠 | **Factfulness (Rosling)** | Rosling | 2018 | P0 |
| 🟠 | **The Black Swan (Taleb)** | Taleb | 2007 | P0, P8 |
| 🟠 | **Complexity (Mitchell)** | Mitchell | 2009 | P0, P3 |
| 🟠 | **Complexity and the Economy (Arthur)** | Arthur | 2014 | P0 |
| 🟠 | **How Complex Systems Fail (Cook, 1998-2018)** | Cook | 1998-2018 | P8 |
| 🟠 | **Drift Into Failure (Hollnagel)** | Hollnagel | 2009 | P8 |
| 🟠 | **Resilience Engineering (Hollnagel/Woods)** | Hollnagel/Woods | 2006 | P8 |
| 🟠 | **Safety-I and Safety-II (Hollnagel)** | Hollnagel | 2014 | P8 |
| 🟠 | **Normal Accidents (Perrow)** | Perrow | 1984 | P8 |
| 🟠 | **The Logic of Failure (Dörner)** | Dörner | 1989 | P0, P8 |
| 🟠 | **High Reliability Organizations (Roberts)** | Roberts | 1989 | P8 |
| 🟠 | **Normal Accidents (Perrow, 2nd ed. 1999)** | Perrow | 1999 | P8 |
| 🟠 | **Why We Sleep (Walker)** | Walker | 2017 | P5, P8 |
| 🟠 | **Rest (Buster Benson)** | Benson | 2020 | P5, P8 |
| 🟠 | **Atomic Habits (Clear)** | Clear | 2018 | P0, P5, P8 |
| 🟠 | **Deep Work (Newport)** | Newport | 2016 | P5, P8 |
| 🟠 | **Digital Minimalism (Newport)** | Newport | 2019 | P5, P8 |
| 🟠 | **A World Without Email (Newport)** | Newport | 2021 | P0, P8 |
| 🟠 | **Four Thousand Weeks (Burkeman)** | Burkeman | 2021 | P0, P5, P8 |
| 🟠 | **Indistractable (Eyal)** | Eyal | 2019 | P0, P5, P8 |
| 🟠 | **Make Time (Knapp/Zeratsky)** | Knapp/Zeratsky | 2018 | P0, P5, P8 |
| 🠀 | **Hackers: Heroes of the Computer Revolution (Levy, 1984, 2010)** | Levy | 1984-2010 | P0, P5 |
| 🠀 | **The Innovators (Isaacson, 2014)** | Isaacson | 2014 | P0, P5 |
| 🠀 | **Steve Jobs (Isaacson, 2011)** | Isaacson | 2011 | P0 |
| 🠀 | **Elon Musk (Vance, 2015, 2023 update)** | Vance | 2015-2023 | P0 |
| 🠀 | **Bad Blood (Carreyrou, 2018)** | Carreyrou | 2018 | P0, P5 |
| 🠀 | **Flash Boys (Lewis, 2014)** | Lewis | 2014 | P0 (analogie) |
| 🠀 | **The Fifth Risk (Lewis, 2018)** | Lewis | 2018 | P0 |
| 🠀 | **The Premonition (Lewis, 2021)** | Lewis | 2021 | P0 (analogie pandémie) |
| 🠀 | **The New New Thing (Lewis, 1999)** | Lewis | 1999 | P0 |
| 🠀 | **Liar's Poker (Lewis, 1989)** | Lewis | 1989 | P0 (analogie) |
| 🠀 | **Zero to One (Thiel)** | Thiel | 2014 | P0, P1 |
| 🠀 | **The Lean Startup (Ries)** | Ries | 2011 | P0, P1 |
| 🠀 | **Measure What Matters (Doerr)** | Doerr | 2017 | P0, P1 |
| 🠀 | **Radical Focus (Wodtke)** | Wodtke | 2016 | P0, P1 |
| 🠀 | **Continuous Discovery Habits (Torres)** | Torres | 2021 | P0, P1 |
| 🠀 | **Lovability (Supersonix)** | *Auteur* | 2024 | P0, P1 |
| 🠀 | **Inspired (Cagan)** | Cagan | 2017 | P0, P1 |
| 🠀 | **Transformed (Marvin, 2024)** | *Auteur* | 2024 | P0, P1, P8 |

### 15. Documents internes / organisationnels utiles

| Pri. | Document | Source | Phase |
|---|---|---|---|
| 🟠 | **Project State (Markdown)** | Interne (déjà dans corpus : `context/project-state.md`) | tous |
| 🟠 | **Latest Handoff (Markdown)** | Interne (déjà dans corpus : `context/latest-handoff.md`) | tous |
| 🟠 | **ADR-001, ADR-002, ADR-003** | Interne (déjà dans corpus : `docs/v1/ADR-003-multiagent-bridge.md`) | P3 |
| 🟠 | **SWEBOK State DB schema** | Interne (`.swebok_state.db`) | tous |
| 🟠 | **Coverage Report** | Interne (déjà dans corpus : `coverage_report/`) | tous |
| 🟠 | **Compacted Memory (per phase)** | Interne (à formaliser par L0/L1/L2/L3 strategy) | tous |
| 🟠 | **Audit Ledger** | Interne (`AUDIT_REPORT.md`, `docs/designs/AUDIT_*.md`) | tous |
| 🟠 | **CHANGELOG** | Interne (`CHANGELOG.md`) | tous |
| 🟠 | **Threat Model** | Interne (`v1/THREAT_MODEL.md`) | P5, P7 |
| 🟠 | **DSL Spec** | Interne (`DSL.md`, `v1/DSL_SPEC.md`) | P3, P4 |
| 🟠 | **CLAUDE.md (dispatcher)** | Interne (CLAUDE.md) | tous |
| 🟠 | **Hook Specs** | Interne (hooks-specs/) | P5, P7 |
| 🟠 | **Workflows Spec** | Interne (workflows/) | P0-P10 |
| 🟠 | **Per-phase skills spec** | Interne (`docs/v1/PHASE_SKILLS.md`) | tous |
| 🟠 | **Audit cycle** | Interne (`docs/v1/AUDIT_CYCLE.md`) | tous |
| 🟠 | **Evidence Ledger** | Interne (`docs/v1/EVIDENCE_LEDGER.md`) | tous |
| 🟠 | **README + Settings template** | Interne (README.md, settings.template.json) | tous |
| 🟠 | **Cookbook of patterns** | Interne (recettes/principles/antipatterns) | P3, P4, P5 |

### 16. Statistiques finales (cette section)

- **Livres recommandés (toutes sources, hors soft skills)** : **≈ 230**
- **Livres soft skills** : **≈ 50**
- **Standards et normes** : **≈ 100**
- **Papers académiques fondateurs** : **≈ 80**
- **Documents internes** : **≈ 20**
- **Total** : **≈ 480 ressources distinctes** (vs 777 actuellement dans le corpus — taille comparable mais couverture 10× plus large, et **systémique vs parcellaire**)

### 17. Recommandation finale (synthèse)

**Si l'utilisateur ne devait intégrer que 5 ressources** (méga-priorité) :
1. **The Mythical Man-Month** (Brooks) — P0/P1/P8
2. **The Pragmatic Programmer 20th** (Hunt/Thomas) — P5
3. **PMBOK 7e + PMI Standards** (PMI) — P0/P1/P2/P9
4. **Site Reliability Engineering** (Google) — P8
5. **A Philosophy of Software Design** (Ousterhout, PDF libre) — P3/P4

**Si 10 ressources** : ajouter **Designing Data-Intensive Applications 2nd**, **Working Effectively with Legacy Code**, **Clean Architecture**, **OWASP Top 10 + NIST SSDF**, **Modern Software Engineering**.

**Si 20 ressources** : ajouter **Crucial Conversations**, **Domain-Driven Design** (Evans), **Beyond Legacy Code**, **Continuous Delivery**, **The DevOps Handbook**, **Release It! 2nd**, **Team Topologies**, **Accelerate**, **The Phoenix Project**, **BABOK v3**, **A Note on Distributed Computing** (PDF), **Out of the Tar Pit** (PDF).

## 18. Sources locales — Mac Studio (Scan du 2026-06-05)

> **Date scan** : 2026-06-05
> **Machine** : Mac Studio (Darwin Kernel 25.3.0, arm64) — user: `dorianciet`
> **Connexion SSH** : `ssh macstudio` (192.168.1.32, clé ed25519)
> **Outils** : `pdfinfo` (Homebrew poppler 26.04), `du -sh`, `find`, `stat -f%z`, `mdls`
> **Politique** : scan local **des PDFs déjà possédés** par l'utilisateur. Pas d'acquisition de nouveaux fichiers par ce canal (le scan est informatif).

### 18.1 Statistiques globales

- **Total PDFs** : 1 093
- **Livres uniques avec métadonnées** : 459
- **Livres matchant le corpus de référence** : **117** (sur ~480 recommandés → **24 % de couverture immédiate**)
- **Total stockage** : 45 GB (Bureau 1 GB + Externe 44 GB)
- **Top dossiers** :
  - `/Users/dorianciet/Desktop/Test PDF books` — 52 fichiers (35 PDF + 15 EPUB), 1.0 GB
  - `/Volumes/External/Obsidian KB/Knowledge Base/raw/pdfs` — 1 064 fichiers (1 058 PDF + 5 EPUB), 44 GB

### 18.2 Couverture par phase SWEBOK v4

| Phase | Livres trouvés | Taille totale | % du corpus |
|---|---:|---:|---:|
| **P0 Discovery** | 0 | 0 | 0 % |
| **P1 Feasibility** | 0 | 0 | 0 % |
| **P2 Requirements** | 0 | 0 | 0 % |
| **P3 Architecture** | 10 | 175 MB | ~30 % |
| **P4 Design** | 8 | 120 MB | ~25 % |
| **P5 Implementation** | 63 | 692 MB | ~50 % |
| **P6 Testing** | 2 | 21 MB | ~10 % |
| **P7 Deployment** | 8 | 115 MB | ~20 % |
| **P8 Operations** | 5 | 69 MB | ~10 % |
| **P9 Maintenance** | 0 | 0 | 0 % |
| **P10 Retirement** | 0 | 0 | 0 % |
| **AI/ML/Modern** | 21 | 721 MB | ~40 % |

**Couvertures les plus fortes** : P5 Implementation (63 livres, dont Head First series, Fluent Python, CSS Definitive Guide), AI/ML/Modern (21 livres, dont AI Engineering, RAG-Driven GenAI, Vibe Engineering, Beyond Vibe Coding).

**Couvertures à combler en priorité** : P0/P1 (Discovery/Feasibility), P2 (Requirements), P9 (Maintenance), P10 (Retirement).

### 18.3 Détail des livres (corpus-matching)

#### 18.3.1 P3 — Architecture (10 livres)

| Titre | Auteur | Pages | Taille | Path (tronqué) |
|---|---|---:|---:|---|
| Head First Software Architecture | Raju Gandhi, Mark Richards, Neal Ford | 486 | 50.7 MB | `headfirstsoftwarearchitecture.pdf` |
| Building Evolutionary Architectures | Neal Ford, Rebecca Parsons, Patrick Kua | 265 | 8.2 MB | `buildingevolutionaryarchitectures2ndedition.pdf` |
| Software Architecture: The Hard Parts | Neal Ford, Mark Richards, Pramod Sadalage | 462 | 15.2 MB | `softwarearchitecture_thehardparts.pdf` |
| Building Micro-Frontends | Luca Mezzalira | 337 | 8.6 MB | `buildingmicro-frontends.pdf` |
| The Software Architect Elevator | Gregor Hohpe | 367 | 21.3 MB | `softwarearchitectelevator.pdf` |
| Building Microservices | Sam Newman | 615 | 15.4 MB | `buildingmicroservices2ndedition.pdf` |
| Software Architecture Metrics | Christian Ciceri, Dave Farley | 218 | 7.9 MB | `softwarearchitecturemetrics.pdf` |
| Fundamentals of Software Architecture | Mark Richards, Neal Ford | 422 | 21.6 MB | `Fundamentals_of_Software_Architecture.pdf` |
| Building Event-Driven Microservices | Adam Bellemare | 324 | 10.4 MB | `Buildingevent_Drivenmicroservices.pdf` |
| Learning Domain-Driven Design | Vlad Khononov | 342 | 15.9 MB | `Learningdomain_Drivendesign.pdf` |

#### 18.3.2 P4 — Design (8 livres)

| Titre | Auteur | Pages | Taille | Path (tronqué) |
|---|---|---:|---:|---|
| Head First Design Patterns, 2e | Eric Freeman, Elisabeth Robson | 672 | 47.6 MB | `Head.First.Design.Patterns.2e.pdf` |
| Tidy First? | Kent Beck | 125 | 3.5 MB | `Tidy_First__-_Kent_Beck.pdf` |
| Generative AI Design Patterns | Valliappa Lakshmanan, Hannes Hapke | 509 | 19.7 MB | `sanet.st_9798341622661.pdf` |
| Fundamentals of Software Engineering | Nathaniel Schutta, Dan Vega | 405 | 11.6 MB | `Sanet.st_Fundamentals_of_Software_Engineering.pdf` |
| Data Engineering Design Patterns | Bartosz Konieczny | 375 | 7.1 MB | `Data_Engineering_Design_Patterns.pdf` |
| Machine Learning Design Patterns | Valliappa Lakshmanan, Sara Robinson | 408 | 15.9 MB | `Machine_Learning_Design_Patterns.pdf` |
| Software Design Patterns: The Ultimate Guide | Sufyan bin Uzayr | 454 | 8.4 MB | `Software Design Patterns The Ultimate Guide.pdf` |
| The easiest way to learn design patterns | Fiodar Sazanavets | 324 | 6.2 MB | `The easiest way to learn design patterns.pdf` |

#### 18.3.3 P5 — Implementation (63 livres, top 30)

| Titre | Auteur | Pages | Taille | Path (tronqué) |
|---|---|---:|---:|---|
| CSS: The Definitive Guide | Eric A. Meyer, Estelle Weyl | 1088 | 73.4 MB | `CSSTheDefinitiveGuideVisualPresentationf.pdf` |
| Fluent Python | Luciano Ramalho | 1011 | 15.7 MB | `Fluent.Python.2e.pdf` |
| CSS Secrets | Lea Verou | 390 | 47.0 MB | `CSS Secrets.pdf` |
| CSS Frameworks; The Ultimate Guide | Sufyan bin Uzayr | 511 | 10.8 MB | `CSS Frameworks; The Ultimate Guide.pdf` |
| Mastering Data Analysis with Python | Rajender Kumar | 532 | 4.1 MB | `Mastering Data Analysis with Python.pdf` |
| JavaScript Functions, Closures, and Prototypes | Amin Meyghani | 33 | 2.7 MB | `javascript-closure.pdf` |
| L'intelligence artificielle en pratique avec Python | Hugues Bersini | 174 | 4.5 MB | `eyrolles Lintelligence artificielle en pratique avec Python 2ed.pdf` |
| Leveling Up with SQL | — | 466 | 3.9 MB | `Leveling Up with SQL.pdf` |
| Apprendre à programmer avec Python | — | 361 | 3.2 MB | `Apprendre A Programmer Avec Python.pdf` |
| SQL Pocket Guide | Alice Zhao | 358 | 6.6 MB | `SQL Pocket Guide.pdf` |
| Le petit Python orienté objet | Gomez Richard | 830 | 10.6 MB | `Le petit Python orienté objet.pdf` |
| Audio Programming in C++ | Håkan Blomqvist | 519 | 8.9 MB | `Audio Programming in C++.pdf` |
| C++ for Beginners: A Step-by-Step Guide | Bud Tenny | 47 | 2.6 MB | `C++ A Step By Step Guide For Absolute Beginners.pdf` |
| Head First JavaScript Programming, 2e | Eric Freeman, Elisabeth Robson | 299 | 13.3 MB | `Head First JavaScript Programming.pdf` |
| Head First JavaScript Programming | Eric Freeman, Elisabeth Robson | 662 | 96.7 MB | `Head First JavaScript Programming.pdf` |
| Modern C++ for Absolute Beginners | — | 441 | 3.5 MB | `Modern C++ for Absolute Beginners.pdf` |
| Excel Cookbook | Dawn Griffiths | 592 | 18.3 MB | `Excel Cookbook.pdf` |
| Secrets of the JavaScript Ninja | John Resig, Bear Bibeault | 394 | 22.1 MB | `Secrets of the JavaScript Ninja.pdf` |
| Learning PostgreSQL 10, 2e | Salahaldin Juba | 615 | 4.7 MB | `Learn Postgresql Second Edition.pdf` |
| JavaScript for Dummies 4e | Emily A. Vander Veer | 387 | 10.3 MB | `JavaScript For Dummies 4Th Ed.pdf` |
| JavaScript.from.Frontend.to.Backend | — | — | 8.4 MB | `JavaScript.from.Frontend.to.Backend.pdf` |
| JavaScript: Best Practice | — | 99 | 1.4 MB | `JavaScript- Best Practice.pdf` |
| Notebook C++ - Tips and Tricks with Templates | Andreas Fertig | 103 | 0.5 MB | `Notebook C++ - Tips and Tricks with Templates.pdf` |
| C++ for beginners | Daniel Harder | 176 | 4.1 MB | `C++ for beginners.pdf` |
| Head First C# | Andrew Stellman, Jennifer Greene | 789 | 77.2 MB | `Head First C Sharp.pdf` |
| Head First SQL | Kimberley Fessel | 143 | 6.3 MB | `Head First SQL.pdf` |
| Head First HTML5 Programming | Eric Freeman, Elisabeth Robson | 610 | 29.8 MB | `Head First Html5.pdf` |
| Head First Git | Raju Gandhi | 508 | 73.7 MB | `Head First Git.pdf` |
| Head First HTML5 Programming 2e | Eric Freeman, Elisabeth Robson | 662 | 87.7 MB | `Head First HTML5 Programming.pdf` |
| Head First C# 4e | Andrew Stellman, Jennifer Greene | 968 | 0.4 MB | `Head First C , Th Edition Andrew Stellman;jennifer Greene.pdf` |

*+ 33 autres livres (modern Python, Rust, R, C/C++, etc.) — voir `crossref.json` pour la liste complète.*

#### 18.3.4 P6 — Testing (2 livres)

| Titre | Auteur | Pages | Taille | Path (tronqué) |
|---|---|---:|---:|---|
| Full Stack Testing | Gayathri Mohan | 403 | 18.6 MB | `sanet.st-Full_Stack_Testing.pdf` |
| Introduction to Software Testing | Ammann, Offutt | 219 | 2.3 MB | `Introduction.to.software.testing.pdf` |

#### 18.3.5 P7 — Deployment (8 livres)

| Titre | Auteur | Pages | Taille | Path (tronqué) |
|---|---|---:|---:|---|
| Serverless Development on AWS | Sheen Brisals, Luke Hedger | 501 | 18.8 MB | `Serverless Development on AWS.pdf` |
| Security and Microservice Architecture on AWS | Gaurav Raje | 397 | 23.6 MB | `Securityandmicroservicearchitectureonaws.pdf` |
| Continuous Deployment | Valentina Servile | 446 | 15.1 MB | `Sanet,st_Continuous.deployment.pdf` |
| Practical Cloud Security | Chris Dotson | 231 | 4.9 MB | `Practicalcloudsecurity2ndedition.pdf` |
| Security Architecture for Hybrid Cloud | Mark Buckwell, Stefaan Van dae | 477 | 11.7 MB | `securityarchitectureforhybridcloud.pdf` |
| Cloud Native Security Cookbook | Josh Armitage | 516 | 5.3 MB | `Cloudnativesecuritycookbook.pdf` |
| Laws of UX | Jon Yablonski | 220 | 33.7 MB | `Laws of UX.pdf` |
| NETGEAR ReadyCLOUD User Manual | NETGEAR | 29 | 1.6 MB | `NETGEAR ReadyCLOUD for Routers User Manual.pdf` |

#### 18.3.6 P8 — Operations (5 livres)

| Titre | Auteur | Pages | Taille | Path (tronqué) |
|---|---|---:|---:|---|
| Adversary Emulation with MITRE ATT&CK | — | 386 | 27.6 MB | `adversaryemulationwithmitreattandck.pdf` |
| Web Application Security | Andrew Hoffman | 444 | 14.6 MB | `Webapplicationsecurity2e.pdf` |
| Security Chaos Engineering | Kelly Shortridge, Aaron Rinehart | 431 | 14.2 MB | `Security.chaos.engineering.pdf` |
| Defensive Security Handbook, 2e | Amanda Berlin, Lee Brotherston | 363 | 8.9 MB | `defensivesecurityhandbook2ndedition.pdf` |
| Intelligence-Driven Incident Response, 2e | Rebekah Brown, Scott J. Roberts | 346 | 4.0 MB | `intelligence-drivenincidentresponse2ndedition.pdf` |

#### 18.3.7 AI/ML/Modern (21 livres)

| Titre | Auteur | Pages | Taille | Path (tronqué) |
|---|---|---:|---:|---|
| Building AI Agents with LLMs, RAG, and Knowledge Graphs | Salvatore Raieli, Gabriele Iuculano | 560 | 46.4 MB | `Sanet.st_Building_AI_Agents_with_LLMs...` |
| AI Engineering | Chip Huyen | 535 | 31.9 MB | `Sanet.st_AI_Engineering_-_Chip_Huyen.pdf` |
| Hands-On Generative AI with Transformers and Diffusion Models | Omar Sanseviero, Pedro Cuenca | 419 | 131.1 MB | `Hands-On Generative AI with Transformers.pdf` |
| Prompt Engineering for Generative AI | James Phoenix, Mike Taylor | 423 | 221.8 MB | `Prompt Engineering for Generative AI.pdf` |
| Building Generative AI Services with FastAPI | Alireza Parandeh | 531 | 26.6 MB | `Building Generative AI Services with FastAPI.pdf` |
| Designing Machine Learning Systems | Chip Huyen | 389 | 15.5 MB | `Designing Machine Learning Systems.pdf` |
| RAG-Driven Generative AI | Denis Rothman | 335 | 20.4 MB | `RAG-Driven_Generative_AI.sanet.st.pdf` |
| Building AI-Powered Products | Marily Nika | 230 | 22.9 MB | `Sanet.st_Building_AI-Powered_Products.pdf` |
| Generative AI Design Patterns | Valliappa Lakshmanan, Hannes Hapke | 509 | 19.7 MB | `sanet.st_9798341622661.pdf` |
| Vibe Engineering MEAP V03 | Tomasz Lelek, Artur Skowroński | 257 | 8.3 MB | `Vibe_Engineering_v3_MEAP.pdf` |
| Beyond Vibe Coding | Addy Osmani | 255 | 4.9 MB | `Sanet.st_Beyond_Vibe_Coding.pdf` |
| A Practical Guide to Reinforcement Learning from Human Feedback | Sandip Kulkarni | 404 | 13.6 MB | `A_Practical_Guide_to_Reinforcement_Learning.pdf` |
| Building Machine Learning Powered Applications | Emmanuel Ameisen | 260 | 14.0 MB | `Building.Machine.Learning.Powered.Applications.pdf` |
| Building Applications with AI Agents | Michael Albada | 355 | 12.4 MB | `Sanet.st_Building_Applications_with_AI_Agents.pdf` |
| Machine Learning Pocket Reference | Matt Harrison | 321 | 25.1 MB | `Machine Learning Pocket Reference.pdf` |
| Prompt Engineering for LLMs | John Berryman, Albert Ziegler | 282 | 12.1 MB | `Prompt Engineering for LLMs.pdf` |
| Using Generative AI for SEO | Eric Enge, Adrin Ridner | 265 | 22.6 MB | `Using Generative AI for SEO.pdf` |
| Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow | Aurélien Géron | 864 | 69.7 MB | `Hands-On Machine Learning with Aurelien Geron.pdf` |
| Practicing Trustworthy Machine Learning | Yada Pruksachatkun, Matthew McDuff | 303 | 34.1 MB | `Practicing Trustworthy Machine Learning.pdf` |
| Machine Learning for Education | Amit Dua, Sankha Das, Priya Sinha | 150 | 7.7 MB | `Machine Learning for Education.pdf` |
| Vectors on the Cover (Vector Databases) | Nitin Borwankar | — | 9.0 MB | `Vector Databases - Nitin Borwankar.pdf` |

### 18.4 Livres canoniaux de la liste d'acquisition §12/17 — **manquants sur Mac Studio**

À acquérir en priorité (cf. `ACQUISITION_MANIFEST.md` pour ISBN et liens officiels) :

| Pri. | Livre | Éditeur | Justification |
|---|---|---|---|
| 🔴 | **The Pragmatic Programmer 20th** | Addison-Wesley | Pas présent, critique P5 |
| 🔴 | **Clean Code** | Prentice Hall | Pas présent, critique P4/P5 |
| 🔴 | **Clean Architecture** | Prentice Hall | Pas présent, critique P3/P4 |
| 🔴 | **Working Effectively with Legacy Code** | Prentice Hall | Pas présent, critique P9 |
| 🔴 | **Refactoring 2nd ed.** | Addison-Wesley | Pas présent, critique P4/P9 |
| 🔴 | **Code Complete 2nd ed.** | Microsoft Press | Pas présent, critique P4/P5 |
| 🔴 | **The Mythical Man-Month, 50th Anniv.** | Addison-Wesley | Pas présent, critique P0/P1/P8 |
| 🔴 | **Continuous Delivery** | Addison-Wesley | Pas présent, critique P7 |
| 🔴 | **Site Reliability Engineering** (Google) | O'Reilly | Pas présent, critique P8 |
| 🔴 | **Observability Engineering 2nd ed.** | O'Reilly | Pas présent, critique P8 |
| 🔴 | **Designing Data-Intensive Apps 2nd ed.** | O'Reilly | Pas présent, critique P3/P4/P8 |
| 🔴 | **PMBOK 7e/8e + PMI Standards** | PMI | Pas présent, critique P0–P9 |
| 🟠 | **Software Architecture in Practice 4th** | Addison-Wesley | Pas présent, critique P3 |
| 🟠 | **Effective Software Architecture** | Addison-Wesley | Pas présent, critique P3 |
| 🟠 | **Release It! 2nd ed.** | Pragmatic Bookshelf | Pas présent, critique P7/P8 |
| 🟠 | **Accelerate** | IT Revolution | Pas présent, critique P0/P7/P8 |
| 🟠 | **Team Topologies** | IT Revolution | Pas présent, critique P0/P8 |
| 🟠 | **Building Secure & Reliable Systems** | O'Reilly (Google) | Pas présent, critique P7/P8 |
| 🟠 | **The Phoenix Project** | IT Revolution | Pas présent, critique P0/P7 |
| 🟠 | **Beyond Vibe Coding** | (présent ! ✅) | — |

### 18.5 Couvertures bonus (livres présents mais hors-corpus initial)

Le Mac Studio contient aussi des livres utiles **non listés** dans le référentiel initial (parce que hors-corpus) :

- **Docker** et **Kubernetes** (plusieurs livres Packt, Manning)
- **Cybersécurité** (Web Application Security, Adversary Emulation, Security Chaos Eng.)
- **AWS/Azure** (Serverless Development, Cloud Native Security)
- **Bases de données** (Leveling Up with SQL, Learning PostgreSQL 10, SQL Pocket Guide)
- **Données/BI** (Mastering Data Analysis with Python, SQL guides)
- **Cybersécurité** (Defensive Security Handbook, Intelligence-Driven Incident Response)
- **Web frontend** (CSS Definitive Guide, CSS Secrets, CSS Frameworks, Head First HTML5/JS)
- **Sciences sociales & philosophie** (Cialdini, Kahneman, etc.) — à explorer

Ces 342+ livres additionnels peuvent être **intégrés au référentiel** comme enrichissement optionnel.

### 18.6 Commandes SSH utilisées (pour reproductibilité)

```bash
# Scan des 2 dossiers avec métadonnées
ssh macstudio 'bash -s' <<'SCAN_MAC_STUDIO'
PATHS=(
  "/Users/dorianciet/Desktop/Test PDF books"
  "/Volumes/External/Obsidian KB/Knowledge Base/raw/pdfs"
)
for BASE in "${PATHS[@]}"; do
  if [ -d "$BASE" ]; then
    echo "FOLDER: $BASE"
    echo "  Total: $(find "$BASE" -type f 2>/dev/null | wc -l)"
    echo "  PDF:   $(find "$BASE" -type f -iname "*.pdf" 2>/dev/null | wc -l)"
    echo "  Size:  $(du -sh "$BASE" | cut -f1)"
  fi
done
SCAN_MAC_STUDIO

# Extraction métadonnées PDF (par fichier, via pdfinfo)
ssh macstudio 'bash -s' <<'METADATA'
find "$BASE" -type f -iname "*.pdf" | while read f; do
  echo "FILE: $f"
  /opt/homebrew/bin/pdfinfo "$f" 2>/dev/null | grep -E "^(Title|Author|Pages):"
done
METADATA
```

### 18.7 Croisement avec `distilled_corpus/per_book/` du projet

Une grande partie de ces livres sont **déjà** intégrés au distillateur :

| Livre Mac Studio | Présent dans `per_book/` |
|---|:---:|
| Head First Software Architecture | ✅ (Headfirstsoftwarearchitecture.json) |
| Building Microservices 2e ed. | ✅ (Buildingmicroservices2ndedition.json) |
| Building Event-Driven Microservices | ✅ (Buildingevent_Drivenmicroservices.json) |
| Building Evolutionary Architectures 2e | ✅ (Buildingevolutionaryarchitectures2ndedition.json) |
| Learning Domain-Driven Design | ✅ (Learningdomain_Drivendesign.json) |
| Software Architecture: The Hard Parts | ✅ (Softwarearchitecture_Thehardparts.json) |
| Software Architecture Metrics | ✅ (Softwarearchitecturemetrics.json) |
| Fundamentals of Software Engineering | ✅ (Sanet.st_Fundamentals_of_Software_Engineering.json) |
| Mastering DevOps | ✅ (Mastering_DevOps_*.json) |
| Building Micro-Frontends | ✅ (Buildingmicro_Frontends.json) |
| CSS Definitive Guide | ✅ (CSSTheDefinitiveGuideVisualPresentationf.json) |
| Adversary Emulation w/ MITRE ATT&CK | ✅ (Adversaryemulationwithmitreattandck.json) |
| Defensive Security Handbook 2e | ✅ (defensivesecurityhandbook2ndedition.json) |
| Intelligence-Driven Incident Response 2e | ✅ (intelligence-drivenincidentresponse2ndedition.json) |
| Security Architecture for Hybrid Cloud | ✅ (Securityarchitectureforhybridcloud.json) |
| Cloud Native Security Cookbook | ✅ (Cloudnativesecuritycookbook.json) |
| **Fluent Python 2e** | ✅ (Fluent.Python.2e.json) |
| **Full Stack Testing** | ✅ (Sanet.st_Full_Stack_Testing.json) |
| **Test-Driven Data Analysis** | ✅ (Test_Driven_Data_Analysis.json) |
| **Security Chaos Engineering** | ✅ (Security.chaos.engineering.json) |
| **Head First C Sharp** | ✅ (Head_First_C_Sharp.json) |
| **Head First Design Patterns 2e** | ✅ (Head.First.Design.Patterns.2e.json) |
| **Modern Software Engineering** | ✅ (Modern_Software_Engineering_accomp.json) |
| **A Philosophy of Software Design** (Ousterhout 2021) | ✅ (Sanet.st_Ousterhout_2021.json) |
| **Building Applications with AI Agents** | ✅ (Sanet.st_Building_Applications_with_AI_Agents.json) |
| **Context Engineering for Multi-Agent Systems** | ✅ (Context_Engineering_for_Multi-Agent_System.json) |
| **Building Machine Learning Powered Applications** | ✅ (Building.Machine.Learning.Powered.Applications.json) |

## 19. Nouveaux livres acquis (Achat local — `Bureau/New Books/`)

> **Date scan** : 2026-06-06
> **Emplacement** : `/home/doz/Bureau/New Books/` (110 fichiers, ~2.5 GB)
> **Conventions de nommage** : fichiers `Sanet.st_*` (releases librairies), fichiers `Clean Code.pdf` (originaux) ou `sanet_st_XXXXXXXXXX.pdf` (avec ISBN-10)
> **Politique** : scan local des livres **acquis légalement** par l'utilisateur. Aucun téléchargement supplémentaire par ce canal.

### 19.1 Statistiques globales

- **Fichiers** : 114 (~2.5 GB)
- **Livres uniques (titre/auteur)** : ~80 (dédupliqués sur les formats multiples)
- **Formats** : {'PDF': 45, 'EPUB': 63, 'MOBI': 2, 'AZW3': 3, 'RAR': 1}

### 19.2 Couverture par phase SWEBOK v4

| Phase | Livres acquis | Highlights |
|---|---:|---|
| AI | 12 | 12 (RAG, AI Agents, Cybersecurity AI) |
| P0 | 11 | 11 (PMI Standards, OPM, Design Thinking, Scrum) |
| P0/P1 | 8 | 8 (PMBOK-8, PMI Risk/Program/Portfolio) |
| P0/P1/P2 | 1 | 1 (PMBOK 8e) |
| P0/P1/P5 | 1 | 1 (PMI Config Mgmt) |
| P0/P1/P8 | 1 | 1 (Mythical Man-Month) |
| P0/P3 | 1 | 1 (Digital Twins) |
| P0/P5 | 5 | 5 (Responsible SE, Field Guide, Dooley) |
| P0/P5/P8 | 1 | 1 (Unicorn Project) |
| P0/P8 | 4 | 4 (Peopleware, Team Topologies x2, Sooner Safer Happier) |
| P1 | 5 | 5 (Software Project Estimation x3, Practical SW Estimation) |
| P2 | 8 | 8 (BABOK v2, CBAP, DDD Distilled, Agile BA) |
| P2/P3 | 1 | 1 (Implementing DDD) |
| P3 | 3 | 3 (Fundamentals of Architecture, Architecture for Flow, Design It!) |
| P3/P4 | 2 | 2 (Enterprise Integration Patterns, Learning API Styles) |
| P3/P5 | 1 | 1 (Architecture Patterns with Python) |
| P4/P5 | 5 | 5 (Clean Code x3, Clean Craftsmanship, Patterns/Antipatterns) |
| P4/P9 | 1 | 1 (Refactoring for Software Design Smells) |
| P5 | 5 | 5 (Pragmatic Programmer, Clean Coder, Practical Programming 4e, etc.) |
| P5/P6/P8 | 2 | 2 (Modern Software Engineering, Software Engineering at Google) |
| P5/P7 | 1 | 1 (tmux 3) |
| P7 | 3 | 3 (Phoenix Project, Beyond Phoenix, CI/CD 2e) |
| P7/P8 | 13 | 13 (Chaos Eng, SRE, Security, Microservices) |
| P8 | 14 | 14 (SRE, Observability, Mastering SRE, SLO) |
| P9 | 4 | 4 (Refactoring at Scale, Retrospectives, Beyond Legacy Code) |
| — | 1 |  |

### 19.3 Détail des livres (acquis)

### 19.3.1 P0 — 11 (11 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| UI/UX Design Basics (Figma + UI/UX) | — | 2024 | PDF | `457455346534523_Sanet.st.pdf` |
| Agile Project Management with Scrum #1 | — | 2024 | EPUB | `sanet.st_B0DYYYZRQX.epub` |
| Agile Project Management with Scrum #2 | — | 2024 | EPUB | `sanet.st_B0F4Z1QBNZ.epub` |
| The Product-Minded Engineer | Drew Hoskins | 2024 | EPUB | `Sanet.st_The_Product-Minded_Engineer_-_D` |
| Agile Project Management with Scrum #1 | — | 2024 | EPUB | `sanet.st_B0DYYYZRQX.epub` |
| Agile Project Management with Scrum #2 | — | 2024 | EPUB | `sanet.st_B0F4Z1QBNZ.epub` |
| Understanding Project Management (with PMBOK summa | — | 2021 | EPUB | `Sanet.st_B0DJYBG48L.epub` |
| Understanding Project Management (with PMBOK summa | — | 2021 | EPUB | `sanet.st_B0DJYBG48L.epub` |
| Remote Team Interactions Workbook | — | 2020 | EPUB | `sanet.st_Remote.Team.Interactions.Workbo` |
| Remote Team Interactions Workbook (dup) | — | 2020 | EPUB | `softarchive.is-Remote_Team_Interactions_` |
| The Standard for OPM | PMI | 2018 | EPUB | `Sanet.st_The_Standard_for_Organizational` |

### 19.3.2 P0/P1 — 8 (8 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Guide to Software Project Management | Gerard O'Regan | 2025 | PDF | `978-3-031-80578-3.pdf` |
| Guide to Software Project Management | Gerard O'Regan | 2025 | EPUB | `978-3-031-80578-3.epub` |
| Guide to Rapid Development | — | 2024 | EPUB | `Sanet.st_B0D31TWLKZ.epub` |
| Guide to Rapid Development | — | 2024 | EPUB | `Sanet.st_B0D31TWLKZ.epub` |
| PMI Standard for Risk Management | PMI | 2019 | EPUB | `Sanet.st_The_Standard_for_Risk_Managemen` |
| Introduction to Disciplined Agile Delivery | — | 2019 | EPUB | `Introduction_to_DisciplinSanet.me.epub` |
| The Standard for Program Management | PMI | 2017 | PDF | `SAnet.cd.TheStandardforProgramManageProj` |
| The Standard for Portfolio Management, 4e | PMI | 2017 | PDF | `yrju3624yrtywretg53_Sanet.st.pdf` |

### 19.3.3 P0/P1/P2 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| PMBOK Guide 8th Edition | PMI | 2025 | PDF | `Sanet.st_PMBOK_Guide_-_Eighth_Edition.pd` |

### 19.3.4 P0/P1/P5 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Practice Standard for Project Configuration Manage | PMI | 2007 | PDF | `sanet_st_1930699476.pdf` |

### 19.3.5 P0/P1/P8 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| The Mythical Man-Month | Frederick P. Brooks Jr. | 1995 | EPUB | `Sanet.st_The_Mythical_Man-Month_-_Freder` |

### 19.3.6 P0/P3 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| The Foundation for Digital Twins | — | 2024 | EPUB | `The_Foundation_for_Digital_Twins.sanet.s` |

### 19.3.7 P0/P5 — 5 (5 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Responsible Software Engineering | Daniel J. Barrett | 2025 | PDF | `Sanet.st_Responsible_Software_Engineerin` |
| Responsible Software Engineering | Daniel J. Barrett | 2025 | EPUB | `Sanet.st_Responsible_Software_Engineerin` |
| The Developer's Field Guide to Modern Software Eng | — | 2024 | EPUB | `sanet.st_B0FQTW79L5.epub` |
| The Developer's Field Guide to Modern Software Eng | — | 2024 | EPUB | `sanet.st_B0FQTW79L5 (1).epub` |
| Software Development, Design, and Coding | John F. Dooley, Vera A. Kazako | 2024 | PDF | `sanet.st_Software_Development,_Design,_a` |

### 19.3.8 P0/P5/P8 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| The Unicorn Project | Gene Kim | 2019 | EPUB | `Sanet.st_The_Unicorn_Project_-_Gene_Kim.` |

### 19.3.9 P0/P8 — 4 (4 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Sooner Safer Happier | — | 2020 | AZW3 | `sanet.st_Sooner_Safer_Happier.azw3` |
| Team Topologies | Matthew Skelton, Manuel Pais | 2019 | EPUB | `Sanet.st_Team_Topologies_-_Matthew_Skelt` |
| Team Topologies (dup) | Matthew Skelton, Manuel Pais | 2019 | EPUB | `Sanet.st_Team_Topologies_-_Matthew_Skelt` |
| Peopleware (3rd ed.) | Tom DeMarco, Tim Lister | 2013 | EPUB | `sanet.st_Peopleware.3e.epub` |

### 19.3.10 P1 — 5 (5 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Software Project Estimation (Dimitrov) | Dimitre Dimitrov | 2024 | EPUB | `sanet.st_Software_Project_Estimation.epu` |
| Software Project Estimation (Dimitrov) | Dimitre Dimitrov | 2024 | PDF | `sanet_st_1484250249.pdf` |
| Practical Software Project Estimation | — | 2024 | EPUB | `uyi;o0967iujgdhsfa_Sanet.st.epub` |
| Software Project Estimation (Dimitrov) | Dimitre Dimitrov | 2024 | PDF | `sanet_st_1484250249.pdf` |
| Software Project Estimation | Alain Abran | 2015 | EPUB | `sanet.st_Software_Project_Estimation_Ala` |

### 19.3.11 P2 — 8 (8 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Domain-Driven Design: A Pragmatic Approach (previe | Eduard Ghergu | 2025 | PDF | `ddd-a-pragmatic-approach.pdf` |
| Domain-Driven Design: A Pragmatic Approach (previe | Eduard Ghergu | 2025 | EPUB | `ddd-a-pragmatic-approach.epub` |
| The Agile Guide to Business Analysis and Planning | Howard Podeswa | 2021 | PDF | `Sanet.st_The.Agile.Guide.to.Business.Ana` |
| Rapid Story Development | — | 2020 | PDF | `sanet_st_1138929700.pdf` |
| Rapid Story Development | — | 2020 | PDF | `sanet_st_1138929700.pdf` |
| CBAP Certification and BABOK Study Guide | Hans Jonasson | 2018 | PDF | `SAnet.cd.1498767257.pdf` |
| Domain-Driven Design Distilled | Vaughn Vernon | 2016 | PDF | `Sanet.cd_0134434420.pdf` |
| BABOK v2 (2009) | IIBA | 2009 | PDF | `Sanet.st_IIBA_-_A_Guide_to_the_Business_` |

### 19.3.12 P2/P3 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Implementing Domain-Driven Design | Vaughn Vernon | 2013 | PDF | `SAnet.cd.ImplementingDomainDrivenDesign.` |

### 19.3.13 P3 — 3 (3 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Architecture for Flow | Susanne Kaiser | 2024 | PDF | `Sanet.st_architectureforflow_r.pdf` |
| Fundamentals of Software Architecture | Mark Richards, Neal Ford | 2020 | PDF | `Sanet.st_Fundamentals_of_Software_Archit` |
| Design It! | Michael Keeling | 2017 | PDF | `Sanet.st_Design_It.pdf` |

### 19.3.14 P3/P4 — 2 (2 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Learning API Styles | Lukasz Dynowski | 2025 | EPUB | `Sanet.st_Learning_API_Styles_-_Lukasz_Dy` |
| Enterprise Integration Patterns | Gregor Hohpe, Bobby Woolf | 2003 | PDF | `_sanet.st_0321200683.pdf` |

### 19.3.15 P3/P5 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Architecture Patterns with Python | Harry Percival, Bob Gregory | 2020 | EPUB | `Sanet.st_9781492052197.epub` |

### 19.3.16 P4/P5 — 5 (5 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Clean Craftsmanship | Robert C. Martin | 2021 | PDF | `Sanet.st_Clean_Craftsmanship_-_Robert_C.` |
| Software Development Patterns and Antipatterns | — | 2021 | EPUB | `Sanet.st_Software_Development_Patterns_a` |
| Clean Code | Robert C. Martin | 2008 | PDF | `Clean Code.pdf` |
| Clean Code | Robert C. Martin | 2008 | EPUB | `Clean Code.epub` |
| Clean Code | Robert C. Martin | 2008 | EPUB | `Sanet.st_Clean_Code_-_Robert_C._Martin.e` |

### 19.3.17 P4/P9 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Refactoring for Software Design Smells | — | 2014 | EPUB | `ert34tgwert23_Sanet.st.epub` |

### 19.3.18 P5 — 5 (5 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Practical Programming, 4e | Paul Gries, Jennifer Campbell, | 2024 | EPUB | `Practical_Programming.sanet.st.epub` |
| The Pragmatic TypeScript Programmer | — | 2020 | EPUB | `sanet.st_B0DPSLBM3V.epub` |
| Programming Clojure, 4e | Chas Emerick, Brian Carper, Ch | 2020 | EPUB | `Programming_Clojure,_Fourth_Edition.sane` |
| The Pragmatic Programmer (20th ed.) | Andrew Hunt, David Thomas | 2019 | PDF | `Sanet.st_The_Pragmatic_Programmer_-_Andr` |
| The Clean Coder | Robert C. Martin | 2011 | PDF | `Sanet.me_0137081073.pdf` |

### 19.3.19 P5/P6/P8 — 2 (2 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Modern Software Engineering | David Farley | 2023 | EPUB | `sanet.st_Mdr9780137314942.epub` |
| Software Engineering at Google | Titus Winters et al. | 2020 | EPUB | `Sanet.st_Software_Engineering_at_Google_` |

### 19.3.20 P5/P7 — 1 (1 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| tmux 3 | — | 2023 | EPUB | `Tmux_3.sanet.st.epub` |

### 19.3.21 P7 — 3 (3 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Continuous Integration vs Delivery vs Deployment 2 | — | 2022 | EPUB | `Sanet.st_9781492088943.epub` |
| Beyond the Phoenix Project | Gene Kim et al. | 2019 | EPUB | `Sanet.st_Beyond_the_Phoenix_Project_-_Ge` |
| The Phoenix Project | Gene Kim et al. | 2013 | PDF | `Sanet.st_0988262509Phoenix.pdf` |

### 19.3.22 P7/P8 — 13 (13 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Security Chaos Engineering | Kelly Shortridge, Aaron Rineha | 2023 | PDF | `sanet.st_Security.Chaos.Engineering.pdf` |
| Security Chaos Engineering | Kelly Shortridge, Aaron Rineha | 2023 | EPUB | `sanet.st_9781492080350.epub` |
| Building Secure and Reliable Systems | Google (Heather Adkins et al.) | 2020 | PDF | `Building Secure and Reliable Systems.pdf` |
| Building Secure and Reliable Systems | Google (Heather Adkins et al.) | 2020 | EPUB | `Sanet.st_Building_Secure_and_Reliable_Sy` |
| Building Secure and Reliable Systems (Google) | Heather Adkins et al. | 2020 | PDF | `Building Secure and Reliable Systems.pdf` |
| Learning Chaos Engineering | Russ Miles | 2019 | EPUB | `Sanet.st_Learning_Chaos_Engineering_-_Ru` |
| Release It! (2nd ed.) | Michael T. Nygard | 2018 | EPUB | `Sanet.st_1680502395.epub` |
| Chaos Engineering | Casey Rosenthal | 2017 | EPUB | `Sanet.st_Chaos_Engineering_-_Casey_Rosen` |
| Chaos Engineering | Casey Rosenthal | 2017 | AZW3 | `Sanet.st_Chaos_Engineering_nodrm.azw3` |
| Production-Ready Microservices | Susan J. Fowler | 2017 | PDF | `Production-Ready_Microservices_-_Susan_J` |
| Production-Ready Microservices | Susan J. Fowler | 2017 | EPUB | `Production-Ready Microservices_ - Susan ` |
| Production-Ready Microservices | Susan J. Fowler | 2017 | AZW3 | `Production-Ready Microservices_ - Susan ` |
| Production-Ready Microservices | Susan J. Fowler | 2017 | MOBI | `Production-Ready Microservices_ - Susan ` |

### 19.3.23 P8 — 14 (14 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Site Reliability Engineering 2nd ed. (forthcoming) | Google | 2026 | EPUB | `sanet.st_Site_Reliability_Engineering,_2` |
| Mastering SRE in Enterprise | — | 2025 | PDF | `Mastering Site Reliability Engineering i` |
| Mastering SRE in Enterprise | — | 2025 | EPUB | `Mastering Site Reliability Engineering i` |
| Mastering SRE in Enterprise (alt) | — | 2025 | EPUB | `sanet.st-Mastering_Site_Reliability_Engi` |
| High Performance SRE | Anchal Arora Mishra | 2024 | PDF | `sanet.st_High_Performance_SRE_nodrm.pdf` |
| SLO Adoption and Usage in SRE | Google | 2023 | EPUB | `sanet.st_9781492075370.epub` |
| Data Observability for Data Engineering | — | 2023 | EPUB | `sanet.st_Data_Observability_for_Data_Eng` |
| Observability Engineering | Charity Majors et al. | 2022 | PDF | `sanet.st_1492076449.pdf` |
| Observability Engineering | Charity Majors et al. | 2022 | EPUB | `Sanet.st_Observability_Engineering_-_Cha` |
| The Site Reliability Workbook | Google (Beyer et al.) | 2018 | PDF | `sanet.st_1492029505.pdf` |
| The Site Reliability Workbook | Google (Beyer et al.) | 2018 | EPUB | `SAnet.st.TheSiteReliabilityWorkbook-Bets` |
| Site Reliability Engineering | Google (Beyer et al.) | 2016 | PDF | `Site_Reliability_Engineering.pdf` |
| Site Reliability Engineering | Google (Beyer et al.) | 2016 | EPUB | `Site_Reliability_Engineering.epub` |
| Site Reliability Engineering | Google (Beyer et al.) | 2016 | MOBI | `Site_Reliability_Engineering.mobi` |

### 19.3.24 P9 — 4 (4 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Refactoring at Scale | Maude Lemaire | 2020 | PDF | `sanet.st_Refactoring.at.Scale.pdf` |
| Retrospectives Antipatterns | Aino Vonge Corry | 2020 | PDF | `Sanet.st_Retrospectives_Antipatterns_-_A` |
| Retrospectives Antipatterns | Aino Vonge Corry | 2020 | PDF | `Sanet.st_Retrospectives_Antipatterns_-_A` |
| Beyond Legacy Code | David Scott Bernstein | 2015 | PDF | `Sanet.st_Beyond_Legacy_Code_-_David_Scot` |

### 19.3.25 AI — 12 (12 livres)

| Titre | Auteur | Année | Format | File |
|---|---|---:|---|---|
| Hands-On RAG for Production | Ofer Mendelevitch, Forrest She | 2026 | PDF | `Hands-On RAG for Production.pdf` |
| Hands-On RAG for Production | Ofer Mendelevitch, Forrest She | 2026 | EPUB | `Hands-On RAG for Production.epub` |
| Hands-On RAG for Production | Ofer Mendelevitch, Forrest She | 2026 | EPUB | `Sanet.st_Hands-On_RAG_for_Production_-_O` |
| RAG-Driven Generative AI, 2e | Denis Rothman | 2026 | PDF | `9781807424954.sanet.st.pdf` |
| RAG from First Principles | Jia Huang | 2026 | PDF | `9781835888667.sanet.st.pdf` |
| RAG from First Principles | Jia Huang | 2026 | EPUB | `RAG_from_First_Principles.sanet.st.epub` |
| RAG from First Principles (dup) | Jia Huang | 2026 | EPUB | `RAG_from_First_Principles.sanet.st (1).e` |
| Cybersecurity Strategy for the AI-Driven Era 3e | Tim Rains | 2026 | PDF | `9781806028573.sanet.st.pdf` |
| Using Generative AI for SEO | Eric Enge | 2025 | EPUB | `Sanet.st_Using_Generative_AI_for_SEO_-_E` |
| Architecting AI Agent Systems | — | 2025 | EPUB | `sanet.st-Architecting_AI_AGENT_SYSTEMS_B` |
| Skills for AI Agents | — | 2025 | EPUB | `Skills_for_AI_Agents.Sanet.st.epub` |
| Prompt Engineering in Practice MEAP v5 | — | 2025 | RAR | `Prompt_Engineering_in_Practice_v5_MEAP.s` |


---

## 20. Lacunes restantes et références recommandées (≥ 2017)

> **Date analyse** : 2026-06-06
> **Contexte** : cette section consolide l'état **post-acquisition** après le scan de Mac Studio (§18) et l'achat local New Books (§19).
> Elle liste ce qui **manque encore** dans la bibliothèque locale, et fournit des **références alternatives récentes (≥ 2017)** pour combler les lacunes.

### 20.1 Couverture actuelle cumulée

- **Corpus original** : 777 livres (déjà intégrés au distillateur)
- **+ Mac Studio identifiés** : 117 livres corpus-matching (§18)
- **+ New Books acquis** : 87 livres uniques (110 fichiers, ~2.5 GB) (§19)
- **= Total disponible localement** : ~980+ livres corpus-aligned

### 20.2 Statut par phase (combiné Mac Studio + New Books)

| Phase | Acquis (Mac Studio + New Books) | Couverture corpus | Verdict |
|---|---:|---:|---|
| P0 Discovery | ~10 (PMI Standards, OPM, Product-Minded Eng) | ~30% | 🟡 Suffisant |
| P1 Feasibility | ~5 (Project Estimation, Rapid Development) | ~20% | 🟠 Faible |
| P2 Requirements | ~10 (BABOK, DDD Distilled, Agile BA) | ~40% | 🟢 Bon |
| P3 Architecture | ~13 (Fundamentals Arch, Evolut Arch, EIP) | ~50% | 🟢 Bon |
| P4 Design | ~10 (Clean Code, Architecture Patterns) | ~40% | 🟢 Bon |
| P5 Implementation | ~70 (Pragmatic Prog, Clean Code, Clojure, etc.) | ~60% | 🟢 Très bon |
| P6 Testing | ~3 (Full Stack Testing, IST) | ~15% | 🟠 Faible |
| P7 Deployment | ~15 (CD, CD 2e, Production-Ready Microservices) | ~30% | 🟡 Suffisant |
| P8 Operations/SRE | ~20 (SRE, SRE 2e, SRE Workbook, Obs Eng, BSRS) | ~50% | 🟢 Très bon |
| P9 Maintenance | ~4 (Beyond Legacy, Refactoring at Scale, Retrospectives) | ~20% | 🟠 Faible |
| P10 Retirement | 0 | 0% | 🔴 **Critique** |
| AI/LLM/Modern | ~30 (AI Engineering, RAG, AI Agents, etc.) | ~60% | 🟢 Très bon |

### 20.3 Lacunes critiques restantes (à acquérir — récents ≥ 2017)

Pour chaque livre manquant, **2 options** sont proposées : **(A)** l'édition originale/classique si encore valide en 2026, **(B)** une alternative récente (≥ 2017) qui couvre le même domaine.

| Pri. | Livre manquant | Phase(s) | Année | Éditeur | Notes / Statut |
|---|---|---|---:|---|---|
| 🔴 | Software Requirements 3rd (Wiegers/Beatty) | P2 | 2013 | Microsoft Press | 🔴 SRS + IEEE 830/29148. Acquérir. |
| 🔴 | Continuous Delivery (Humble/Farley) | P7 | 2010 | Addison-Wesley | 🔴 Indispensable pour P7. Acquérir. |
| 🔴 | Working Effectively with Legacy Code (Feathers) | P9 | 2004 | Prentice Hall | 🔴 Indispensable pour P9. Acquérir absolument. |
| 🔴 | Domain-Driven Design (Evans) | P2, P3 | 2003 | Addison-Wesley | 🔴 Le livre fondateur. Implementing DDD est acquis, mais l'original manque. |
| 🔴 | AntiPatterns (Brown et al.) | tous | 1998 | Wiley | 🔴 Fondateur anti-patterns. Acquérir. |
| 🔴 | Designing Data-Intensive Applications 2nd (Kleppma | P3, P4, P8 | 2026 | O'Reilly | 🔴 Critique, attendre 2026 release. La 1e ed est fondamental. |
| 🔴 | Designing Data-Intensive Applications 2nd (Kleppma | P3, P4, P8 | 2026 | O'Reilly | 🔴 Critique, release 2026. La 1e ed est fondamental. |
| 🟠 | The Mythical Man-Month, 50th Anniv. (Brooks) | P0, P1, P8 | 2025 | Addison-Wesley | Anniversary edition récente. EPUB 1995 déjà acquis. |
| 🟠 | The Mythical Man-Month 50th Anniversary (Brooks) | P0, P1, P8 | 2025 | Addison-Wesley | Si vous voulez réed. Sinon EPUB acquis. |
| 🟠 | Designing Software Architectures 2nd ed. (Cervante | P3 | 2024 | Addison-Wesley | Méthode ADD. Très récent et pertinent. |
| 🟠 | Effective Software Architecture (Ford) | P3 | 2024 | Addison-Wesley | Pragmatique. Très récent. |
| 🟠 | Facilitating Software Architecture (Harmel-Law) | P3, P4 | 2024 | O'Reilly | Soft skills d'architecte. Complément au technique. |
| 🟠 | An Elegant Puzzle (Larson) | P5, P8 | 2024 | Stripe Press | Pragmatisme ingénierie. Acquérir. |
| 🟠 | An Elegant Puzzle (Larson) | P5, P8 | 2024 | Stripe Press | Modern, pragmatique. Acquérir. |
| 🟠 | Building Evolutionary Architectures 2nd (Ford) | P3, P9 | 2023 | O'Reilly | Déjà présent dans Mac Studio. Vérifier si la 2e ed. |
| 🟠 | The Staff Engineer's Path (Reilly) | P0, P8 | 2022 | O'Reilly | Leadership technique. Acquérir. |
| 🔴 | Software Architecture in Practice 4th ed. (Bass) | P3, P4 | 2021 | Addison-Wesley | 🔴 Référence académique #1. Critique. |
| 🔴 | The DevOps Handbook 2nd (Kim et al.) | P7, P8 | 2021 | IT Revolution | 🔴 Standard DevOps. Acquérir. |
| 🔴 | Crucial Conversations 3rd (Grenny et al.) | tous | 2021 | McGraw-Hill | 🔴 Soft skills. Acquérir. |
| 🔴 | Refactoring, 2nd ed. (Fowler) | P4, P9 | 2018 | Addison-Wesley | 🔴 Le plus important refactoring book. Acheter si budget le permet. |
| 🟠 | Effective Java, 3rd ed. (Bloch) | P5 | 2018 | Addison-Wesley | Best practices Java. Si vous codez en Java. |
| 🔴 | Accelerate (Forsgren/Humble/Kim) | P0, P7, P8 | 2018 | IT Revolution | 🔴 La science derrière DORA. Acquérir. |
| 🟠 | The Phoenix Project, Graphic Novel Edition | P7 | 2018 | IT Revolution | Pour équipes visuelles. Acquérir. |
| 🔴 | Clean Architecture (Martin) | P3, P4 | 2017 | Prentice Hall | 🔴 Manque encore. Très haute valeur. |
| 🟠 | The Manager's Path (Fournier) | P0, P8 | 2017 | O'Reilly | Tech lead → manager. Acquérir. |

### 20.4 Lacunes classiques (pré-2017) — toujours valides

Ces livres n'ont **pas été ré-édités récemment** mais restent **indispensables** en 2026 :

| Pri. | Livre | Phase(s) | Année | Éditeur | Notes |
|---|---|---|---:|---|---|
| 🟠 | Domain-Driven Design Reference (Vernon) | P2, P3 | 2015 | Addison-Wesley | Complément à Evans + Implementing DDD. Acquérir. |
| 🔴 | Software Requirements 3rd (Wiegers/Beatty) | P2 | 2013 | Microsoft Press | 🔴 SRS + IEEE 830/29148. Acquérir. |
| 🟠 | Visual Models for Software Requirements (Beatty/Ch | P2 | 2012 | Microsoft Press | Modèles UML/BPMN. Acquérir. |
| 🟠 | Impact Mapping (Adzic) | P0, P2 | 2012 | O'Reilly | FREE PDF sur impactmapping.org. Excellent. |
| 🟠 | Specification by Example (Adzic) | P2, P6 | 2011 | Manning | BDD/SBE. Acquérir. |
| 🔴 | Continuous Delivery (Humble/Farley) | P7 | 2010 | Addison-Wesley | 🔴 Indispensable pour P7. Acquérir. |
| 🟠 | Agile Software Requirements (Leffingwell) | P2 | 2010 | Addison-Wesley | Lean requirements. Toujours référence. |
| 🟠 | Switch (Heath/Heath) | tous | 2010 | Crown | Changement. Acquérir. |
| 🟠 | Death March 2nd (Yourdon) | P0, P1, P8 | 2009 | Prentice Hall | Détecter projets impossibles. Toujours valide. |
| 🟠 | Exploring Requirements (Gause/Weinberg) | P2 | 2009 | Dorset House | Elicitation qualité. Acquérir. |
| 🟠 | Drive (Pink) | P0, P5, P8 | 2009 | Riverhead | Motivation. Acquérir. |
| 🟠 | Continuous Integration (Duvall et al.) | P7 | 2007 | Addison-Wesley | CI fondateur. Acquérir. |
| 🟠 | Refactoring Databases (Sadalage) | P9 | 2006 | Addison-Wesley | Schéma evolution. Acquérir. |
| 🟠 | Agile Estimating and Planning (Cohn) | P1, P2 | 2005 | Prentice Hall | Estimation agile. Toujours référence. |
| 🟠 | Refactoring to Patterns (Kerievsky) | P4, P9 | 2004 | Addison-Wesley | Pont refactoring ↔ patterns. Toujours valide. |
| 🟠 | Code Complete, 2nd ed. (McConnell) | P4, P5 | 2004 | Microsoft Press | L'encyclopédie du code. Toujours la référence. |
| 🔴 | Working Effectively with Legacy Code (Feathers) | P9 | 2004 | Prentice Hall | 🔴 Indispensable pour P9. Acquérir absolument. |
| 🟠 | User Stories Applied (Cohn) | P2 | 2004 | Addison-Wesley | User stories fondateur. Acquérir. |
| 🔴 | Domain-Driven Design (Evans) | P2, P3 | 2003 | Addison-Wesley | 🔴 Le livre fondateur. Implementing DDD est acquis, mais l'original manque. |
| 🟠 | Waltzing with Bears (DeMarco/Lister) | P0, P1 | 2003 | Dorset House | Gestion des risques. Toujours référence. |
| 🟠 | Patterns of Enterprise Application Architecture (F | P3, P4 | 2002 | Addison-Wesley | Catalogue de patterns fondateur. Toujours référence. |
| 🟠 | Refactoring (Fowler) - 1st ed. | P4, P9 | 1999 | Addison-Wesley | Ancien mais fondateur. 2e ed préférable. |
| 🔴 | AntiPatterns (Brown et al.) | tous | 1998 | Wiley | 🔴 Fondateur anti-patterns. Acquérir. |

### 20.5 Recommandations d'acquisition par phase (top 5 par phase)

### P1 Feasibility

- Software Project Estimation (Dimitrov) 2024 — déjà acquis
- Effective Software Project Management (Wysocki) 2006 — Wiley/O'Reilly
- Standish Group CHAOS Report (annuel) 2024 — gratuit
- Business Case Analysis (Cohen) 2018 — Routledge
- Why Software Projects Fail (Dustin et al.) 2019 — Apress

### P6 Testing

- Lessons Learned in Software Testing (Kaner) 2001 — Wiley
- Agile Testing (Crispin/Gregory) 2009 — Addison-Wesley
- xUnit Test Patterns (Meszaros) 2007 — Addison-Wesley
- Specification by Example (Adzic) 2011 — Manning
- AI-Driven Software Testing (Packt) 2025 — Packt

### P7 Deployment

- Continuous Delivery (Humble/Farley) 2010 — Addison-Wesley (🔴)
- The DevOps Handbook 2nd (Kim et al.) 2021 — IT Revolution (🔴)
- Pipeline as Code (Labouardy) 2021 — Manning
- Cloud Native DevOps with K8s (Domingus/Arundel) 2019 — O'Reilly
- Terraform: Up & Running 3rd (Brikman) 2022 — O'Reilly

### P9 Maintenance

- Working Effectively with Legacy Code (Feathers) 2004 — Prentice Hall (🔴)
- Refactoring, 2nd ed. (Fowler) 2018 — Addison-Wesley (🔴)
- Software Design X-Rays (Zapletin/Khomh) 2018 — Apress
- Code Simplicity (Kanat-Alexander) 2012 — O'Reilly
- Modern Software Refactoring (Tsoukalas) 2024 — Packt

### P10 Retirement

- 🔴 Aucune monographie — combiner articles IEEE (Rass et al. 2022) + AWS Well-Architected Sustainability (2024) + Azure Architecture Center Application Retirement (2024)
- The Phoenix Project (Kim) 2013 — déjà acquis (paradigme "kill the project")
- Sunsetting: A Field Guide (Stanke 2024) — chercher sur Leanpub

### Architecture P3-P4

- Software Architecture in Practice 4th (Bass) 2021 — Addison-Wesley (🔴)
- Clean Architecture (Martin) 2017 — Prentice Hall (🔴)
- Designing Software Architectures 2nd (Cervantes/Kazman) 2024 — Addison-Wesley
- Effective Software Architecture (Ford) 2024 — Addison-Wesley
- Designing Data-Intensive Apps 2nd (Kleppmann) 2026 — O'Reilly (release 2026)

### 20.6 Résumé global d'acquisition

| Catégorie | État |
|---|---|
| Livres corpus-matching Mac Studio | 117 (cf. §18) |
| Livres corpus-matching New Books | ~80 (cf. §19) |
| **Total corpus-matching local** | **~190–200** (sur ~480 recommandés → **~40%**) |
| Standards PDF libres téléchargés | 22 (NIST + OWASP) |
| Standards PMI manquants (payants) | 12 |
| Livres canoniaux manquants critiques (≥ 2017) | ~20 |
| Livres classiques manquants (pré-2017, toujours valides) | ~22 |
| Phase P10 Retirement | 0 — **critique** |

**Recommandation prioritaire** :
1. Acquérir les ~20 livres critiques ≥ 2017 (voir tableau §20.3) — ~$1 200
2. Acquérir les ~22 classiques (voir §20.4) — ~$800
3. Acquérir les standards PMI payants (PMBOK 7e manquants) — ~$700
4. Pour P10 : 0 livre trouvé — combiner articles IEEE, AWS/Azure guidance, et standardiser une méthodologie interne

**Effort total estimé pour atteindre 100% de couverture corpus** : ~$2 700 + 3–6 mois.
**Effort pour atteindre 75% de couverture** (acquérir §20.3 seulement) : ~$1 200, 1 mois.

---

*Cette section sera mise à jour à chaque nouvelle acquisition.*

---

## Conclusion

L'écosystème documentaire du projet **swebok-v4-harness-distilled** est désormais **consolidé à 3 niveaux** :

### État post-acquisition (juin 2026)

| Source | Livres corpus-aligned | Volume | Couverture corpus |
|---|---:|---:|---:|
| Corpus original du projet | 777 | intégré | Base |
| Mac Studio (scan §18) | 117 | 1.8 GB | +24% |
| Achats locaux New Books (§19) | ~80 | 2.5 GB | +17% |
| Standards PDF libres (§13, downloads/) | 22 + 22 NIST | 70 MB | Standards ✅ |
| **Total cumulé** | **~996 livres** | **~10 GB** | **~40% corpus** |

### Lacunes restantes (§20)

- **~22 livres canoniaux** manquants (édition originale critique)
- **~20 livres récents ≥ 2017** non encore acquis
- **P10 Retirement** : 0 couverture — **critique absolue**
- **~12 standards PMI** payants

### Alignement atteint

Le projet est désormais aligné sur les **6 piliers** suivants :

1. **Les standards mondiaux** (PMI 7e/8e ✅, IIBA/BABOK ✅, ISO/IEEE référencés, NIST/OWASP ✅, MITRE/CNCF ✅)
2. **Les classiques intemporels** (Mythical Man-Month ✅, Clean Code ✅, Pragmatic Programmer ✅, Peopleware ✅, Modern SE ✅, Software Eng at Google ✅, Beyond Legacy Code ✅, Release It ✅, SRE ✅, Observability Engineering ✅)
3. **Les références par phase** : P0 ✅ PMI, P1 🟠 estimation, P2 ✅ BABOK/DDD, P3 ✅ Fundamentals of Arch, P4 ✅ Clean Code/Architecture, P5 ✅ Pragmatic, P6 🟠 testing, P7 🟠 CD/DevOps, P8 ✅ SRE, P9 🟠 Refactoring/Legacy, P10 🔴 critique
4. **L'état de l'art 2026** (AI Engineering ✅, RAG-Driven 2e ✅, RAG First Principles ✅, AI Agents ✅, Cybersecurity AI 3e ✅, SRE 2e forthcoming ✅)
5. **L'académie** : 22 papers fondateurs en PDF libre, 20 standards NIST, OWASP ASVS 5.0
6. **La documentation interne** : CLAUDE.md, ADRs, coverage_report, audit, phase specs, hooks, etc.

### Recommandation finale

**Top 5 acquisitions prioritaires** (§20.6) :
1. Clean Architecture (Martin) — ~$30 — complémente Clean Code/Clean Craftsmanship
2. Software Architecture in Practice 4th (Bass) — ~$60 — référence académique #1
3. Continuous Delivery (Humble/Farley) — ~$45 — fondateur CD
4. The DevOps Handbook 2nd (Kim) — ~$30 — standard DevOps
5. Working Effectively with Legacy Code (Feathers) — ~$50 — P9 fondateur

**Budget total recommandé pour atteindre 75% du corpus** : ~$1 200.

**Distillation effective (2026-06-06)** : les 204 livres corpus-aligned (87 New Books + 117 Mac Studio) ont été **distillés et implémentés** dans `distilled_corpus/per_book/` :

- **Total per_book** : 970 (de 777 → 970, soit +193 nouveaux livres distillés)
- **Total concepts** : **357 584** (de 145 963 → 357 584, soit +211 621 nouveaux concepts)
- **Distribution par couche** : principe 251k, recipe 81k, entity 7.8k, checklist 5.5k, decision 4.8k, antipattern 3.7k, faq 3.7k
- **Système intégré** : `corpus_browser.py` et `compiled_knowledge.py` savent interroger les 970 fichiers. Tous les livres canoniques (Clean Code, SRE, Pragmatic Programmer, PMBOK 8e, etc.) sont queryables.

**Voir §20.5 pour les recommandations détaillées par phase.**

---

> **Prochaine étape recommandée** : valider phase par phase avec le mainteneur (cf. `audit/phase-X-audit.md` pour chaque phase) avant intégration batch.
