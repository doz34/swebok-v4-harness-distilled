# P10 Demo Project — openclaw-docs Retirement

> **Date** : 2026-06-09
> **But** : Valider empiriquement la méthodologie P10 Retirement (cf. `audit/corpus-references/p10-retirement-resources/`) sur un cas réel
> **Cible** : `/home/doz/openclaw-docs/` — site de documentation OpenClaw (multi-channel AI agent gateway)
> **Pattern cible** : Big-Bang (simple, pas d'utilisateurs actifs à migrer, EOL accepté)

## 1. Contexte du système cible

| Attribut | Valeur |
|---|---|
| **Nom** | openclaw-docs |
| **Type** | Documentation site (markdown statique) |
| **Taille** | 25 MB |
| **Fichiers** | 640 markdown + assets |
| **Tech stack** | Markdown statique (servi par GitHub Pages ou similaire) |
| **URL publique** | (CNAME présent, à vérifier) |
| **Git remote** | https://github.com/开源claw/openclaw.git |
| **Date dernier commit** | 2026-02-16 (4 mois sans maintenance) |
| **Statut projet parent** | OpenClaw (multi-channel AI agent gateway) |

## 2. Pourquoi retirement ?

**Critères de decision** :
- ✅ **Coût maintenance annuel** : ~0 (hosting gratuit GitHub Pages) mais temps de维护 > 0
- ✅ **Valeur business** : faible (640 docs d'un projet actif mais peu consulté)
- ✅ **Complexité retirement** : faible (1-2/10) — site statique, pas de DB, pas d'users actifs
- ✅ **Risque compliance** : faible (pas de PII, pas de contrats)
- ✅ **Risque utilisateur** : faible (utilisateurs = développeurs du projet, qui migrent vers autre doc)

**Decision** : **OUI — EOL accepté**. Le site sera archivé mais le repo git reste accessible en read-only.

## 3. Pattern choisi : **Big-Bang** (niveau Simple)

| Critère | Valeur |
|---|---|
| Niveau criticité | **Simple** (cf. §41.5 du corpus reference) |
| Pattern | Big-Bang (1 fenêtre, 4-8 heures) |
| Durée | **3-5 jours** (1 préparation + 1 exécution + 1 vérification) |
| Budget | 1k/2k/3k tokens |
| Compliance | RGPD (pas de PII) |
| Replacement | Aucun (EOL accepté, alternative = openclaw.com/wiki futur) |

## 4. 7 piliers — Plan d'exécution

| Pillar | Démarrage | Fin | Status |
|---|---|---|---|
| 1. Decision & Planning | 2026-06-09 18h30 | 2026-06-09 18h45 | ⏳ |
| 2. Data Retention & Archival | 2026-06-09 18h45 | 2026-06-09 19h00 | ⏳ |
| 3. User Migration | 2026-06-09 19h00 | 2026-06-09 19h15 | ⏳ |
| 4. Dependency Map & Shutdown | 2026-06-09 19h15 | 2026-06-09 19h30 | ⏳ |
| 5. Knowledge Archival | 2026-06-09 19h30 | 2026-06-09 19h45 | ⏳ |
| 6. Compliance & Legal Sign-off | 2026-06-09 19h45 | 2026-06-09 20h00 | ⏳ |
| 7. Post-Retirement Review | 2026-06-09 20h00 | 2026-06-09 20h15 | ⏳ |

## 5. Livrables attendus

Pour chaque pilier, on génère un document dans le sous-dossier correspondant :
- `01-decision/` : business case, decision matrix, communication plan
- `02-data/` : data inventory, archival status
- `03-users/` : user inventory, communication
- `04-dependencies/` : dependency map, cascade plan
- `05-knowledge/` : code archive, docs archive, knowledge artifacts
- `06-compliance/` : RGPD checklist, sign-off
- `07-closure/` : lessons learned, closure memo
- `08-final-archive/` : final tarball, immutable signature

## 6. Critères de succès (cf. §41.5)

- [ ] Closure memo signé
- [ ] Site redirige vers 410 Gone ou page "archived"
- [ ] Repo git marqué "archived" sur GitHub
- [ ] Données archivées en S3 Glacier (ou local tar.gz)
- [ ] Knowledge artifacts (code, docs, ADRs) préservés
- [ ] Cost monitoring : hosting = $0
- [ ] Aucune erreur post-retirement
- [ ] Lessons learned documentées

## 7. Conclusion attendue

Ce demo project valide la méthodologie P10 sur un cas réel. Si succès, la méthodologie est validée empiriquement et peut être réutilisée pour des retirements plus complexes (RGPD, Critique, etc.).
