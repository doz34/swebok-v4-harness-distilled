# Audit — Phase 5: Implementation

> Grille d'audit à compléter hors-ligne. Coche, reformule, ou écris dans les espaces libres.

## Métadonnées
- Phase : 5
- Nom : Implementation
- Équivalent SWEBOK v4 : P4 SWEBOK (Software Construction KA — Code construction, Integration, Reuse, Technical debt tracking)
- Spec existante : `specs/workflows/by-phase/phase-5-implementation.md` (v2 — validé 2026-06-07)
- Date de l'audit : 2026-06-07
- Auditeur : mainteneur (audit clos via grille offline + 4 questions AskUserQuestion vague 1)

---

## ⚠️ Findings pré-identifiés

1. **P4 SWEBOK (Estimation) absente** du modèle → comblé par `effort-report.md` (livrable formel P5, T-shirt S/M/L/XL vs temps réel passé).
2. **P5 SWEBOK (Construction) fusionnée avec P4** dans le modèle 9-phases initial → corrigé par fix structurel 2026-06-05 (modèle 10-phases, P5 = Construction seule).
3. **Phase la plus critique du projet** (là où on consomme le plus de tokens, où les erreurs coûtent le plus cher) → justifié par budget 5k/10k/15k (le plus large) et Nexus-Critic T1+T2+T3 obligatoire (3 invocations).

---

## Section 1 — Charte de la phase

### 1.1 Mission (1 phrase)
**Suggestions** :
- [x] A. *« Translate design specifications into executable software »* (spec actuelle)
- [x] B. *« Implémenter en respectant design + NFR + contrats d'interface, avec tests unitaires, couverture et SAST clean »*
- [x] C. *« Produire du code production-ready, testable, traçable jusqu'au design »*

**Mission retenue (v2 2026-06-07)** : « Consommer les DDS P4 + ADRs P3 et descendre au niveau code : organisation fichiers, naming, classes, dépendances, tests unitaires, CI/CD — pour que P6 Testing puisse tester sans ambiguïté et P7 Deployment puisse packager sans re-implémentation. »

### 1.2 Périmètre
- [x] A. Module implementation (spec)
- [x] B. Code quality (peer review + SAST)
- [x] C. Unit testing
- [x] D. Integration preparation
- [x] E. **+ Estimation effort réelle** (vs prévue) — combler P4 absent → `effort-report.md` (livrable formel, T-shirt S/M/L/XL vs heures réelles)
- [x] F. **+ Feature flags / toggles** si déploiement progressif
- [x] G. **+ Documentation inline** (docstrings, README par module)
- [x] H. **+ Adversarial validation Nexus-Critic T1+T2+T3** (3 invocations systématiques, comme P3 et P4)

### 1.3 Hors-périmètre
- [x] A. Tests d'intégration (phase-6)
- [x] B. Tests E2E (phase-6)
- [x] C. Tests d'acceptance (phase-6)
- [x] D. **+ Déploiement** (phase-7)
- [x] E. **+ Performance tuning** au-delà des NFR (phase-8)
- [ ] Autre : ____________________________________________

### 1.4 Verdict
- [x] 🟢 OK
- [ ] 🟡 À ajuster
- [ ] 🔴 À repenser

---

## Section 2 — Conditions d'entrée et de sortie

### 2.1 Trigger d'activation
- [x] A. Phase 4 design approved (spec EG-5.1)
- [x] B. Detailed design specifications complete (spec EG-5.2 — 100% modules avec DDS)
- [x] C. Module interface contracts finalized (spec EG-5.3 — md+json modules internes, +OpenAPI REST, +AsyncAPI events)
- [x] D. Design traceability matrix established (spec EG-5.4 — DTAM + DRTM 100%)
- [x] E. Matrice de conformité aux ADRs P3 validée (spec EG-5.5 — XG-4.7)
- [x] F. Dev env opérationnel (spec EG-5.6 — compilateur, linter, test runner, SAST, coverage)
- [x] G. Modules assignés (spec EG-5.7 — qui code quoi)
- [x] H. CI/CD pipeline stages defined (spec EG-5.8 — build, test, lint, SAST, coverage)

### 2.2 Critères de complétion
- [x] A. **≥95% modules complétés (XG-5.1)** — compromis mainteneur 2026-06-07 (vs ≥80% v2-renum, vs ≥99% grille initiale). Adaptatif : ≥99% compliance, ≥80% R&D.
- [x] B. Code review clean (XG-5.2) — incluant T1 casseur Nexus-Critic
- [x] C. Coverage ≥80% line / ≥70% branch (XG-5.3) — adaptatif si conformité/compliance
- [x] D. 100% interfaces DDS P4 connectées (XG-5.4)
- [x] E. ITM 100% — matrice code → DDS P4 + ADR P3 + NFR P2 (XG-5.5)
- [x] F. SAST 0 critical (XG-5.6)
- [x] G. **+ Matrice de conformité aux DDS P4 vérifiée (XG-5.7)** — équivalent XG-4.7 pour P4
- [x] H. **+ UDL 7 éléments P5-spécifiques loggés (XG-5.8)**
- [x] I. **+ Effort report signé (XG-5.9)**
- [x] J. **+ Technical debt register à jour (XG-5.10)**
- [x] K. **+ Complexité cyclomatique < seuil** (maintenabilité)
- [x] L. **+ Pas de TODO/FIXME critiques** dans le code mergé
- [x] M. **+ Documentation à jour** (API doc, README)

### 2.3 Conditions d'échec → escalade
- [x] A. Coverage < cible après 2 itérations
- [x] B. SAST critique non résolvable
- [x] C. Effort réel > 2× estimation (signaling: design sous-estimé)
- [x] D. Conflit de contrats d'interface (signaling: design incomplet)
- [ ] Autre : ____________________________________________

### 2.4 Verdict
- [x] 🟢

---

## Section 3 — Inputs

### 3.1 Depuis phases précédentes
- [x] A. Design détaillé + interface contracts
- [x] B. DTM (design traceability matrix)
- [x] C. Security architecture
- [x] D. **+ Slice pertinente du SRS** (acceptance criteria pour les modules en cours)
- [ ] Autre : ____________________________________________

### 3.2 Depuis l'utilisateur
- [x] A. Décisions sur les trade-offs techniques (ex: dette technique acceptée)
- [x] B. **+ Validation des raccourcis** (utiliser lib X au lieu de Y, etc.)
- [x] C. **+ Priorisation si effort > estimation** (quoi livrer en premier)
- [ ] Autre : ____________________________________________

### 3.3 Depuis sources externes

> **🆕 Mis à jour 2026-06-06** : couverture corpus à **100%** (██████████).**Sources externes disponibles localement (post-corpus) :****Mac Studio** (63 livres) — chemin `/Users/dorianciet/Desktop/Test PDF books` et `/Volumes/External/Obsidian KB/Knowledge Base/raw/pdfs` :- **CSS: The Definitive Guide** (Eric A. Meyer,Estelle Weyl) — 73.4 MB, 1088 pages- **Mastering Data Analysis with Python: A Comprehensive Guide to NumPy, Pandas, and Matplotlib** (Rajender Kumar) — 4.1 MB, 532 pages- **JavaScript Functions, Closures, and Prototypes** (Amin Meyghani) — 2.7 MB, 33 pages- **L'intelligence artificielle en pratique avec Python : Recherche, optimisation, apprentissage Ed. 2** (Bersini, Hugues) — 4.5 MB, 174 pages- **Leveling Up with SQL** () — 3.9 MB, 466 pages- **Fluent Python** (Luciano Ramalho) — 15.7 MB, 1011 pages- **Apprendre à programmer avec Python** (http://avaxhm.com/blogs/Proghu) — 3.2 MB, 361 pages- **SQL Pocket Guide** (Zhao, Alice;) — 6.6 MB, 358 pages- **CSS Secrets** (Lea Verou) — 47.0 MB, 390 pages- **Le petit Python orienté objet** (Gomez Richard) — 10.6 MB, 830 pages- **CSS Frameworks; The Ultimate Guide** (Sufyan bin Uzayr) — 10.8 MB, 511 pages- **Practicing Trustworthy Machine Learning** (Yada Pruksachatkun, Matthew Mc) — 34.1 MB, 303 pages- **Audio Programming in C++** (Håkan Blomqvist) — 8.9 MB, 519 pages- **C++ for Beginners: A Step-by-Step Guide on C++ Programming Language Fundamentals with Practical Explanations (2022 Crash Course for All)** (Tenny, Bud) — 2.6 MB, 47 pages- **Head First JavaScript Programming, 2nd Edition** () — 13.3 MB, 299 pages- ... et 48 autres. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §18.**New Books (achats locaux)** (5 livres) — chemin `/home/doz/Bureau/New Books/` :- **Practical Programming, 4e** (Paul Gries, Jennifer Campbell,, 2024) — formats: EPUB- **Programming Clojure, 4e** (Chas Emerick, Brian Carper, Ch, 2020) — formats: EPUB- **The Pragmatic TypeScript Programmer** (—, 2020) — formats: EPUB- **The Pragmatic Programmer (20th ed.)** (Andrew Hunt, David Thomas, 2019) — formats: PDF- **The Clean Coder** (Robert C. Martin, 2011) — formats: PDF**Standards NIST/OWASP téléchargés (open access)** (4) :- NIST SSDF 800-218 / 218A (Secure Dev)- NIST 800-190 (Container Security)- NIST 800-193 (BIOS)- NIST 800-22r1a (RNG)**Livres open-access téléchargés** (5) :- Operating Systems: 3 Easy Pieces (Arpaci-Dusseau, 6 MB)- Convex Optimization (Boyd, 7 MB)- Think X series (Python/OS/Stats/DSP, 7 MB)- Math 4 ML (Deisenroth, 18 MB)- Linear Algebra Done Right (Axler 4e, 3 MB)**Lacunes critiques restantes (à acquérir)** (3) :- Effective Java, 3rd ed. (Bloch) (2018)  -- Best practices Java. Si vous codez en Java.- An Elegant Puzzle (Larson) (2024)  -- Pragmatisme ingénierie. Acquérir.- An Elegant Puzzle (Larson) (2024)  -- Modern, pragmatique. Acquérir.
### 3.4 Verdict
- [x] 🟢

---

## Section 4 — Outputs

### 4.1 Deliverables concrets
- [x] A. `source-code/` (par module, généré depuis DDS P4) — le vrai livrable
- [x] B. `code-review-reports.md` (revue pair-à-pair + T1 casseur Nexus-Critic)
- [x] C. `unit-test-suite.md` (spec)
- [x] D. `coverage-report.md` + `coverage.json` + `coverage.html` (JSON+HTML)
- [x] E. `implementation-traceability.md` (matrice code → DDS P4 + ADR P3 + NFR P2, XG-5.7)
- [x] F. `ci-cd-pipeline.md` (spec)
- [x] G. **+ Build artifacts** (binaires, packages)
- [x] H. **`effort-report.md` (NOUVEAU v2)** — T-shirt S/M/L/XL par module vs temps réel passé, signé par mainteneur
- [x] I. **`technical-debt-register.md`** — dette introduite + rationale + plan remédiation
- [x] J. **`implementation-report.md`** — résumé 1 page (modules livrés, dette, estimations, sign-off)

### 4.2 Format de stockage
- [x] A. Code source en git
- [x] B. Specs en markdown
- [x] C. Coverage report en JSON + HTML
- [x] D. SAST report en SARIF/JSON
- [ ] Autre : ____________________________________________

### 4.3 Format de présentation à l'utilisateur
- [x] A. Status board temps réel
- [x] B. PR par module avec diff + review
- [ ] C. Daily/weekly report (selon rythme)
- [ ] Autre : ____________________________________________

### 4.4 Auditabilité
- [x] A. Oui — git log + PR + reviews = trace complète
- [x] B. Manque le lien "pourquoi cette approche vs alternative"
- [ ] Autre : ____________________________________________

### 4.5 Verdict
- [x] 🟢

---

## Section 5 — Mécanique opérationnelle

### 5.1 Agents utilisés
- [x] A. Hyperagent-Orchestrator (spec)
- [x] B. Nexus-Backend, Nexus-Frontend (spec)
- [x] C. Nexus-DevOps (spec)
- [x] D. Nexus-Security (spec)
- [x] E. speckit-qa (spec)
- [x] F. **+ T1 (Code Producer vs Code Breaker)** : un agent code, l'autre essaie de casser (mutation testing, edge cases)
- [x] G. **+ T2 (Spec-Compliance Reviewer)** : le code respecte-t-il le design ?
- [x] H. **+ T3 (Consequentialist)** : prédire les bugs en phase-5
- [x] I. **Limiter les agents actifs simultanément** (per Anthropic: éviter le "10+ subagents pour rien")
- [ ] Autre : ____________________________________________

### 5.2 Tools disponibles
- [x] A. `nexus-backend`, `nexus-frontend`, `nexus-devops`, `nexus-security` (spec)
- [x] B. `speckit-qa` (spec)
- [x] C. **+ Outils de test** (pytest, jest, etc.)
- [x] D. **+ Outils SAST** (semgrep, snyk, etc.)
- [x] E. **+ Linter** (ruff, eslint, etc.)
- [x] F. **+ Coverage tool** (coverage.py, c8, istanbul)
- [x] G. **+ Git tools** (diff, blame, log)
- [x] H. **+ Consult L0 corpus** via tool (jamais injecté en bloc)
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

**Livres canoniques disponibles localement pour cette phase** (68 livres corpus-aligned sur ~30 recommandés = **100%**) :

- **Mac Studio** : 63 livres — voir détail §3.3 ci-dessus
- **New Books** : 5 livres — voir détail §3.3 ci-dessus
- **Standards** : 4 NIST/OWASP
- **Open-access** : 5 livres (Ousterhout, OSTEP, CS229, etc.)

**Lacunes critiques (§20)** : 3 livres non encore acquis. Voir `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §20 pour les références alternatives ≥ 2017.

**Plan d'intégration** : 5 vagues (cf. §10.1 du référentiel). Effort estimé pour atteindre 75% de couverture : ~$1 200, 1 mois.


### 5.4 Pattern adversarial applicable
- [x] A. T1 critique (code prod vs code breaker)
- [x] B. T2 critique (spec-compliance)
- [x] C. T3 applicable (prédire bugs phase-5)
- [x] D. Council pour les choix structurants (ex: dette technique)
- [x] E. **+ Pair programming simulé** (producteur + reviewer)
- [ ] Autre : ____________________________________________

### 5.5 Points de décision utilisateur (B threshold)

> **Validation 2026-06-07** : 7 questions précises avec options AskUserQuestion (vs vide en v1). Format actionnable identique à P3 v2 et P4 v2. Chaque question a 2-4 options mutuellement exclusives.

**Q1 — Bibliothèque X vs Y** (vendor lock-in check, par module)
- A. **Importer une lib externe battle-tested** (ex: `authlib` pour l'auth, `pydantic` pour la validation) — lock-in faible à modéré selon la lib
- B. **Code interne from-scratch** — pas de dépendance, mais réinventer la roue
- C. **Code interne + spec stricte** — from-scratch mais avec tests + doc + revue externe (équivalent lib externe en qualité)
- D. **Pas de décision** → escalade mainteneur

**Q2 — Convention de nommage / format fichiers** (kebab-case vs snake_case vs camelCase)
- A. **kebab-case fichiers + snake_case variables + PascalCase classes** (standard Python/JS moderne)
- B. **camelCase fichiers + camelCase variables + PascalCase classes** (standard Java/TS ancien)
- C. **Adaptatif selon stack** (Python = option A, Java = option B, etc.)
- D. **Pas de décision** → escalade mainteneur

**Q3 — Réutilisation interne** (lib interne maison vs from-scratch)
- A. **Importer la lib interne maison** si elle existe (capitalisation)
- B. **From-scratch** si la lib interne n'existe pas ou ne couvre pas le besoin
- C. **Étendre la lib interne** (PR sur la lib) si le besoin est générique
- D. **Pas de décision** → escalade mainteneur

**Q4 — Style de code** (OOP strict vs fonctionnel vs hybride)
- A. **OOP strict** (classes, héritage, polymorphisme) — aligné enterprise Java/.NET
- B. **Fonctionnel** (fonctions pures, immutabilité) — aligné Haskell/Elixir
- C. **Hybride pragmatique** (OOP pour le domain, fonctionnel pour les transformations de données) — aligné Python/TS moderne
- D. **Pas de décision** → escalade mainteneur

**Q5 — Gestion d'erreur** (exceptions vs Result type vs error codes)
- A. **Exceptions typées** (raise/catch avec hiérarchie d'exceptions) — standard Python/Java
- B. **Result type** (Ok/Err explicite, pas d'exception) — aligné Rust/Go moderne
- C. **Error codes + sentinel values** — aligné C ancien, mais simple
- D. **Pas de décision** → escalade mainteneur (impacte tous les modules)

**Q6 — Logging** (structured JSON vs unstructured text)
- A. **Structured JSON** (champs typés, parsable par les outils d'observabilité) — aligné cloud-native
- B. **Unstructured text** (lisible humain, mais difficile à parser) — aligné legacy
- C. **Hybride** (JSON pour les events structurés, text pour les debug logs) — pragmatique
- D. **Pas de décision** → escalade mainteneur (impacte les logs P8)

**Q7 — Stratégie de tests** (mock-heavy vs integration-heavy vs mutation)
- A. **Mock-heavy** (mocks pour les dépendances externes, tests unitaires rapides) — aligné TDD classique
- B. **Integration-heavy** (vraies dépendances, tests plus lents mais plus réalistes) — aligné E2E moderne
- C. **Mix pragmatique** (unit + integration + quelques E2E) — pragmatique
- D. **+ Mutation testing** activé en CI/CD (vérifie que les tests détectent les régressions) — coût additionnel
- E. **Pas de décision** → escalade mainteneur

### 5.6 Verdict
- [x] 🟢

---

## Section 6 — Bornes & modes d'échec

### 6.1 Refus catégoriques (7)
- [x] A. **Pas de re-décision design** (escalade P4 si déviation DDS détectée — règle de démarcation)
- [x] B. **Pas de re-décision architecturale** (escalade P3 si décision impacte ≥2 bounded contexts)
- [x] C. Pas de feature non-spec
- [x] D. Pas de dette technique non documentée
- [x] E. Pas de SAST critique accepté
- [x] F. **+ Pas d'optimisation prématurée** (réf. YAGNI)
- [x] G. **+ Pas de dépendance non-justifiée** (vendor lock-in)
- [x] H. **+ Pas de merge sans review** (T1 casseur Nexus-Critic obligatoire)

### 6.2 Modes d'échec connus (7)
- [x] A. **Phase la plus chère en tokens** (15× multi-agent vs chat, per Anthropic F2)
- [x] B. Big bang implementation (tout en un, pas de feedback loop)
- [x] C. Sous-estimation d'effort (mitigé par effort-report.md et T-shirt S/M/L/XL)
- [x] D. Architecture erosion (le design se dégrade en codant) — mitigé par XG-5.7 matrice DDS → code
- [x] E. Test theater (coverage mais tests bidons) — mitigé par T1 casseur mutation testing
- [x] F. Security theater (SAST clean mais vulnérabilités business) — mitigé par SAST + revue sécurité Nexus-Security
- [x] G. **+ HPO bypass trop libéral** (micro-tâches qui deviennent méga-changements) — circuit breaker 3 blocks

### 6.3 Cas limites
- [x] A. Greenfield vs legacy refonte
- [x] B. Solo dev vs équipe (parallélisme)
- [x] C. Criticalité forte (formel, auditable) vs CRUD
- [x] D. Stack contraint (legacy) vs green stack
- [x] E. **+ Timebox serré** (pas de livraison partielle acceptable)
- [ ] Autre : ____________________________________________

### 6.4 Règles d'escalade
- [x] A. Effort > 2× estimation pour >30% modules → escalade P3 (design sous-estimé) ou P4 (DDS incomplet)
- [x] B. SAST critique non résolvable → décision mainteneur (accepter dette ou bloquer)
- [x] C. Conflit de contrats d'interface DDS P4 → escalade P4 (refus catégorique 1)
- [x] D. Coverage < cible après 2 itérations → escalade P4 (DDS incomplets) ou P5 (tests incomplets)
- [x] E. DDS P4 non respecté et déviation non escaladée → escalade P4 (refus catégorique 1)
- [x] F. Décision architecturale détectée en P5 (impacte ≥2 bounded contexts) → escalade P3

### 6.5 Verdict
- [x] 🟢

---

## Section 7 — Adéquation aux besoins (utilité)

### 7.1 Usage réel
P5 = phase d'implémentation, utilisée pour transformer les DDS P4 + ADRs P3 en code production-ready. Profil projet (détecté en P0 + validé en P1) adapte le déroulé :

| Profil | Effort typique P5 | % du projet total | Livrables clés |
|--------|-------------------|-------------------|-----------------|
| **Greenfield from-scratch** | 2-6 semaines | 30-40% | source-code/ + tests + CI/CD from scratch |
| **Maintenance legacy** | 1-4 semaines | 20-30% | code modifié pour matcher nouveau DDS, dette pré-existante à inventorier |
| **Projet interne** (gouvernance légère) | 1-3 semaines | 25-35% | code standard, peer review, T1 casseur optionnel (T2+T3 obligatoires) |
| **Projet externe client** | 4-12 semaines | 30-50% | code + revue externe + sign-off formel, T1+T2+T3 + revue externe |
| **Compliance-driven** (finance, santé) | 6-16 semaines | 35-60% | code security-heavy, XG-5.1 ≥99%, SAST + tests + traçabilité renforcés |
| **R&D / exploration** | 1-2 semaines | 15-25% | POC, XG-5.1 ≥80% avec justification, dette technique acceptée |

Cohérence P0 v2 + P1 v2 + P2 v2 + P3 v2 + P4 v2 : mêmes profils, mêmes patterns d'effort, validés par le mainteneur.

### 7.2 Friction observée (6 frictions attendues)
1. **F1 = Phase la plus chère en tokens** (15× multi-agent vs chat, F2 recherche 2026) — mitigation = Nexus-Critic 3 invocations fixes + compaction 60-70% + 3-5 agents max
2. **F2 = Risque de "big bang"** (tout en un, pas de feedback loop) — mitigation = intégration continue (CI/CD) + tests d'intégration par module (XG-5.4)
3. **F3 = Sous-estimation d'effort** (surtout en R&D, code imprévu) — mitigation = `effort-report.md` T-shirt S/M/L/XL vs réel + critère d'abandon 2 (>30% modules >2× réel → escalade)
4. **F4 = Architecture erosion** (le design se dégrade en codant, raccourcis) — mitigation = matrice DDS → code (XG-5.7) + refus catégorique 1 (pas de re-décision design)
5. **F5 = Test theater** (coverage mais tests bidons) — mitigation = T1 casseur mutation testing simulé + couverture adaptative (XG-5.3)
6. **F6 = Security theater** (SAST clean mais vulnérabilités business) — mitigation = Nexus-Security + revue pair-à-pair + threat model P3 appliqué

### 7.3 Pattern de contournement probable (4 contournements)
1. **C1 = "vite fait, mal fait"** : P5 livre un module qui marche mais ne respecte pas le DDS → mitigation = matrice DDS → code (XG-5.7) détecte la déviation + refus catégorique 1
2. **C2 = "feature creep"** : dev ajoute des features non-spec (gold-plating) → mitigation = refus catégorique 3 (pas de feature non-spec) + UDL 1 (pointeur DDS P4 d'origine)
3. **C3 = "coverage inflation"** : tests qui ne testent rien pour gonfler le % → mitigation = T1 casseur Nexus-Critic + review pair-à-pair
4. **C4 = "copy-paste"** : copier du code d'un autre module sans factoriser → mitigation = dette technique trackée (UDL 5 + `technical-debt-register.md`) + plan remédiation P9

Cohérence P3 v2 + P4 v2 : mêmes frictions, mêmes contournements, mêmes mitigations. Aucun contournement remonté par le mainteneur à ce stade.

### 7.4 Valeur ajoutée perçue
P5 = 100% de la valeur du produit final. Sans P5, le design P3/P4 reste abstrait, le code n'existe pas, l'utilisateur ne peut rien utiliser.

| Métrique | Valeur typique | Source |
|----------|----------------|--------|
| Effort P5 / total projet | 30-60% | SWEBOK v4 (Implementation = activity 1) |
| Lignes de code livrées | 1k-100k+ selon profil | Variable |
| Modules livrés | 5-50 selon profil | Variable |
| Coverage moyenne | 80-95% line | XG-5.3 (adaptatif) |
| Dette technique introduite | 5-15% du code | Variable |
| Taux de détection bugs P5 (vs P6) | ~70% (industry) | IBM Systems Sciences Institute |

### 7.5 Dette d'orchestration
La coordination multi-agent (3-5 Nexus en parallèle) consomme ~20% du budget P5 (vs 80% pour le code lui-même). Risques :
- **Sync failure** : si un agent bloque, les autres attendent (mitigation = tâches async par défaut, monitoring par Hyperagent, escalade rapide)
- **Context drift** : 3-5 contextes séparés peuvent diverger (mitigation = ACI strict, prompt caching si API, Consultation Envelope A1)
- **Effort reporting overhead** : T-shirt S/M/L/XL vs réel = 5-10% du temps par module (acceptable, vu la valeur de la traçabilité)

Cohérence avec P3 v2 + P4 v2 (mêmes risques d'orchestration, mêmes mitigations).

### 7.6 Verdict
- [x] 🟢

---

## Section 8 — Context Engineering (transverse)

> Référence : `00-context-engineering-strategy.md`. **Token budget proposé : 5k base / 10k soft / 15k hard** (la plus grosse phase).

### 8.1 Token budget alloué
**Confirmé 2026-06-07** : 5k base / 10k soft / 15k hard. Budget déjà aligné `pre-tool-use/token-counter.sh` (ligne 63) et `audit/00-context-engineering-strategy.md` §5.

### 8.2 Compaction checkpoint
- [ ] A. Tous les 5 tool calls (déjà en place)
- [ ] B. À 70% du soft cap (7k)
- [x] C. Les deux
- [x] D. **+ Compaction sélective** : garder les décisions et les diffs, drop les résultats d'outils intermédiaires
- [ ] Autre : ____________________________________________

### 8.3 Consultation cross-phase
- [x] A. Phase 3 design en slice (juste la partie du module en cours)
- [x] B. Phase 2 SRS en slice (acceptance criteria du module)
- [x] C. **+ Pas de re-chargement du design complet** à chaque module
- [x] D. **+ L0 corpus via tool, jamais en bloc** (227 items, mortel)
- [ ] Autre : ____________________________________________

### 8.4 Pattern adversarial concret
- [x] A. T1 : Code Producer vs Code Breaker (essaye de casser avec edge cases)
- [x] B. T2 : Spec-Compliance (le code matche le design ?)
- [x] C. T3 : Consequentialist (prédire les bugs phase-5)
- [x] D. **+ Mutation testing** simulé par l'adversaire
- [x] E. **+ Context isolation stricte** (chaque rôle a son propre slice)
- [ ] Autre : ____________________________________________

### 8.5 User Decision Ledger — quoi logger (7 éléments P5-spécifiques)

> **Validation 2026-06-07** : 7 éléments P5-spécifiques (aligné P2, P3, P4 — 7 éléments par phase).

| # | Élément | Description | Exemple |
|---|---------|-------------|---------|
| 1 | **Module code completed** | Pointeur vers `source-code/${module}/` + hash du commit | "Module billing = `source-code/billing/` commit `a3f9d2`" |
| 2 | **Library / dependency added** | Rationale + vendor lock-in check | "Ajout de `pydantic` v2 pour validation, alternative `marshmallow` écartée (perf), lock-in faible (open source)" |
| 3 | **Estimation réelle vs estimée** | T-shirt size S/M/L/XL vs heures réelles passées | "Module billing estimé M (4-8h), réel 12h (sous-estimé 50%), raison = DDS incomplet sur les cas d'erreur" |
| 4 | **Reuse vs create-from-scratch** | Décision documentée (import lib externe vs code interne vs from scratch) | "Module auth = reuse `authlib` (battle-tested) vs from scratch (réinventer la roue, risque sécurité)" |
| 5 | **Dette technique introduite** | Pointeur vers `technical-debt-register.md` avec rationale | "Module reporting = utilise `eval()` pour parser les formules dynamiques, dette TD-005 avec plan migration vers AST en P9" |
| 6 | **Rejet T1/T2 casseur** | Quand Nexus-Critic a trouvé un problème et comment c'est résolu | "T1 a trouvé injection SQL dans module X via concaténation, corrigé via parameterized queries + review" |
| 7 | **Décision "pas de décision"** | Cas où on a choisi de NE PAS trancher, et pourquoi | "Pas d'arbitrage perf vs memory pour cache LRU : escaladé P6 (P5 ne mesure pas la perf, c'est P6+P8)" |

Stockés dans `.swebok_state.db` (table `udl_p5`) et consultables via Consultation Envelope (A1) par P6 Testing.

### 8.6 Verdict
- [x] 🟢

### 8.7 Validation empirique 2026 (recherche complémentaire)

> Référence : `01-context-engineering-research-2026.md`. **Phase la plus chère en tokens (15× multi-agent vs chat)** — la discipline context engineering est critique.

#### Findings les plus pertinents pour cette phase
- **F2** : Multi-agent = 15× tokens → 3-5 subagents max, **chaque subagent = OBJECT/FORMAT/TOOLS/BOUND écrit dans le DSL**
- **F6** : Mur à 35 min → checkpoint obligatoire par module, au-delà forcer compaction/fin
- **F7** : 60% du 1er tour = retrieval → **pre-hydrate avec la slice du design (interfaces à implémenter) + acceptance criteria**, sinon on perd 60% du budget
- **F12** : BM25 > embedding sur code → sur codebase existant, `grep`/AST > embedding search naïf
- **F10** : Subagent output → filesystem → chaque Nexus-Backend/Frontend écrit dans `.swebok_state.db` avec un hash, le retour au Hyperagent = pointeur uniquement
- **F1** : 80% de la variance perf = token usage → **mesurer les tokens consommés par module**, c'est un signal de qualité

#### Anti-patterns à éviter dans cette phase
- **AP1** : Fan-out excessif sur micro-tâches — single Nexus par module sauf si read-heavy parallèle
- **AP2** : Brief vague "implement X" — le brief doit spécifier la slice du design, les tests à passer, les contraintes
- **AP3** : Transcripts complets à chaque wakeup — digest structuré via modèle cheap
- **AP5** : Compaction tardive (95%) — trigger à 60-70% du soft cap (7k)
- **AP6** : Tool result clearing absent — vider après consommation par la phase suivante
- **AP8** : "Mon modèle a 1M tokens, je peux tout charger" → rot à 50K, budget ≠ fenêtre

#### Audit des 4 failure modes Drew Breunig
- [x] **Poisoning** : un module qui contamine les autres (mauvaise abstraction propagée) ?
- [x] **Distraction** : scope creep (gold-plating non demandé) ?
- [x] **Confusion** : dette technique non documentée qui s'accumule ?
- [x] **Clash** : conflits de merge, conflits d'interfaces entre modules ?

#### Recommandation budget (mise à jour 2026)
- **Hard 15k** (multi-agent discipliné, pre-hydrate par module, compaction 60-70% = 6-7k tokens, structure pyramidale des éléments critiques)

---



---

## 🆕 MISE À JOUR POST-CORPUS (2026-06-06)

> **Note importante** : cette grille a été révisée le 2026-06-06 pour intégrer le nouveau référentiel corpus (cf. `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md`).

### Couverture effective

| Source | Livres disponibles pour cette phase |
|---|---:|
| Mac Studio (§18) | 63 |
| New Books achetés (§19) | 5 |
| Standards NIST/OWASP (§13) | 4 |
| Open-access téléchargés | 5 |
| **TOTAL corpus-aligned local** | **77** |

### Couverture recommandée (corpus)

- **Recommandé pour cette phase** : ~30 livres
- **Disponible localement** : 68 corpus-aligned
- **Couverture effective** : **100%** ██████████

### Lacunes (§20)

- **3** livres manquants critiques pour cette phase
- **P10 Retirement** : 0 livre (🔴 critique globale)
- **Standards PMI payants** : 12 (PMBOK 7e/8e, Risk, etc.)

### Verdict révisé

- Les ressources sont **suffisantes** pour la phase
- Cross-référencer `corpus-references/SWEBOK_CORPUS_BOOKS_REFERENCE.md` §17 pour le détail
- Top priorité d'acquisition pour cette phase : voir §20.3/§20.4 du référentiel


## Verdict global de la phase
- [x] 🟢 (2026-06-07, 4 décisions tranchées vague 1 + transformations implicites)

## Liste d'actions
1. **Refonte spec v2** ✅ (2026-06-07) — `specs/workflows/by-phase/phase-5-implementation.md` v2-renum → v2
2. **Mise à jour grille** ✅ (2026-06-07) — verdict 🟢, sections 5.5/7/8.5 comblées
3. **Mise à jour token counter** ✅ déjà à 5k/10k/15k (ligne 63) — pas de modification nécessaire
4. **Mise à jour stratégie** ✅ déjà à jour §5/§12.6 (P5 = 5k/10k/15k, multi justifié)
5. **Mémoire projet** ⏳ à créer — `swebok-v4-p5-spec-v2-vert-2026-06-07.md` (à faire dans cette conversation)
6. **User prompt P6 Testing** ⏳ à générer — prochaine conversation

## Notes libres
> ____________________________________________________________________________
> ____________________________________________________________________________
