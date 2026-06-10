# Communication Plan — openclaw-docs Retirement

> **Date** : 2026-06-09
> **But** : Documenter la communication 6-3-1 mois avant retirement

## Stakeholders identifiés

| Stakeholder | Canal | Fréquence |
|---|---|---|
| Contributeurs GitHub | GitHub Issues + email | À T-6, T-3, T-1, T-0 |
| Équipe OpenClaw | Slack #openclaw channel | À T-3, T-1, T-0 |
| Utilisateurs du site | Bannière sur le site lui-même | À T-1, T-0 |
| Search engines | robots.txt + sitemap retired | À T-0 |

## Timeline de communication

| Quand | Message | Canal |
|---|---|---|
| **T-6 mois** (2025-12-09) | "Documentation site sera archivé en juin 2026, migrer vers Notion interne" | GitHub Issue + Slack |
| **T-3 mois** (2026-03-09) | "Rappel : retirement dans 3 mois, comment migrer vos bookmarks" | GitHub Issue + Slack |
| **T-1 mois** (2026-05-09) | "Dernière chance : retirement dans 1 mois, archive sera en read-only" | GitHub Issue + Slack + bannière site |
| **T-1 semaine** (2026-06-02) | "Cette semaine : retirement lundi 2026-06-09" | Slack + bannière site |
| **T-0 (2026-06-09)** | "Site archivé, redirect vers page archived" | GitHub + banner + robots.txt |
| **T+1 semaine** (2026-06-16) | "Post-retirement review, lessons learned" | Slack + GitHub |

**Note (Demo)** : Pour ce demo project, tous les messages sont simulés en 1 jour (T-6, T-3, T-1, T-0 = même jour 2026-06-09). En production, respecter les vraies durées.

## Message type (T-1 mois)

```
Subject: openclaw-docs retirement — 1 month notice

Hi all,

This is a reminder that the openclaw-docs site will be retired on 2026-06-09.

What you need to do:
1. Update any bookmarks pointing to https://docs.openclaw.com/* to use Notion
2. If you have local clones, ensure they're up-to-date
3. After retirement, the repo will be archived (read-only) on GitHub
4. The archived content will be available at https://archive.openclaw.com/openclaw-docs-2026-06-09

Questions? Reply to this thread or ping me on Slack.

Thanks,
SWEBOK v4 P10 demo team
```

## Message type (T-0)

```
Subject: openclaw-docs retired — site archived

Hi all,

As of today (2026-06-09), the openclaw-docs site has been retired.

What changed:
- Site now redirects to /archived page
- Repo marked as "archived" on GitHub (read-only)
- All content preserved at https://archive.openclaw.com/openclaw-docs-2026-06-09
- No data loss

What's next:
- Future documentation will be in Notion (internal)
- A lessons learned post-mortem will be shared next week

Thanks for your understanding,
SWEBOK v4 P10 demo team
```
