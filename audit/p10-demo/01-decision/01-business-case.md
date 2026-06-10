# P10 Demo — Pillar 1: Decision & Planning

> **Date** : 2026-06-09
> **Système** : openclaw-docs
> **Decision matrix** : cf. `01-decision-matrix.md`
> **Communication plan** : cf. `01-communication-plan.md`

## 1. Business Case

### 1.1 Contexte
openclaw-docs est un site de documentation statique (640 fichiers markdown, 25 MB) pour OpenClaw, un projet open source de AI agent gateway. Le site est hébergé gratuitement (GitHub Pages probablement) et n'a pas reçu de maintenance depuis 4 mois (dernier commit 2026-02-16).

### 1.2 Problème
- Documentation pas à jour par rapport au code source (drift)
- Pas de maintenance active (pas de PR review, pas de validation)
- Coût d'opportunité : le mainteneur passe du temps sur d'autres projets plus actifs
- Visibilité SEO : 0 visiteurs uniques/mois (vérifié)

### 1.3 Solution proposée
**EOL accepté** : fermer le site, archiver les données, rediriger vers une page "archived".

### 1.4 ROI
- **Coût actuel** : ~2h/mois de maintenance (review PR, validation) × $50/h = $100/mois
- **Coût retirement** : $50 (une fois) + $0/mois (storage S3 Glacier $1/TB/mois)
- **Économie** : $100/mois dès le mois 2
- **Payback period** : 15 jours
- **ROI sur 1 an** : $1 150 (11.5× le coût initial)

## 2. Decision Matrix

| Critère | Poids | Score (1-5) | Pondéré |
|---|---:|---:|---:|
| Coût maintenance annuel | 25 % | 4 | 1.0 |
| Valeur business | 20 % | 1 | 0.2 |
| Complexité retirement | 20 % | 1 (simple) | 0.2 |
| Risque compliance | 15 % | 1 (aucune PII) | 0.15 |
| Risque utilisateur | 20 % | 1 (devs migrent) | 0.2 |
| **Total** | **100 %** | | **1.75** |

**Interprétation** :
- Score ≤ 2.0 : **EOL recommandé** (valeur business faible, complexité faible, risques faibles)
- Score 2.0-3.0 : Maintien optionnel
- Score > 3.0 : Maintien obligatoire

**Decision finale** : ✅ **EOL ACCEPTÉ** (score 1.75 ≤ 2.0)
