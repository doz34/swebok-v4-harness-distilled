# P10 Demo — Pillar 3: User Migration

> **Date** : 2026-06-09
> **Système** : openclaw-docs
> **Niveau criticité** : Simple (n°1)

## 1. User Inventory

| Catégorie | Count | Action |
|---|---:|---|
| **Contributeurs GitHub** (commits) | 1+ | Notification GitHub Issue |
| **Stars** (project popularity) | 0 (repo public, peu connu) | Pas de notification directe |
| **Forks** | 0 | Pas de notification directe |
| **Site visitors** (analytics) | 0 (vérifié Google Analytics hypothétique) | Notification via bannière site |
| **Équipe interne OpenClaw** | 2-3 devs | Notification Slack |

**Total users à notifier** : **~5** (3 contributeurs + 2-3 équipe)

## 2. Communication Timeline (Demo simulation)

| T | Action | Format |
|---|---|---|
| T-6 mois | "Site will be retired 2026-06-09" | GitHub Issue |
| T-3 mois | "Reminder: retirement in 3 months" | GitHub Issue + Slack |
| T-1 mois | "Last chance: retirement in 1 month" | GitHub + Slack + bannière site |
| T-1 semaine | "This week: retirement Monday" | Slack + bannière site |
| T-0 | "Site retired, see archived version" | GitHub + bannière + robots.txt |
| T+1 semaine | "Lessons learned" | Slack + GitHub |

**Démo** : Pour ce demo, tous les messages sont simulés (envoyés le 2026-06-09).

## 3. Migration Path

**Pas de replacement system** → EOL accepté

**Options offertes aux users** :
1. **Local clone** : `git clone https://github.com/openclaw/openclaw-docs.git`
2. **Archive permanente** : `https://archive.openclaw.com/openclaw-docs-2026-06-09/`
3. **GitHub read-only** : `https://github.com/openclaw/openclaw-docs` (repo archived, read-only)
4. **Migration OpenClaw** : Internal Notion (si user interne)

## 4. Training Plan

N/A (pas de replacement system).

## 5. Cutover

| Étape | Action | Status |
|---|---|---|
| T-1h | Banner site "Site will be retired at 17:00 UTC" | ⏳ |
| T-0 | Update CNAME → archive.openclaw.com | ⏳ |
| T+0 | Update robots.txt → noindex, nofollow | ⏳ |
| T+0 | GitHub repo marked as "archived" | ⏳ |
| T+1h | Verify all redirects work | ⏳ |
| T+1d | Support hotline still active (1 semaine) | ⏳ |

## 6. Post-Retirement User Support

- **1 semaine** : Slack channel dédié + email support
- **2-4 semaines** : FAQ publique
- **1+ an** : Archive accessible (mais pas updated)
