# Decision Matrix — openclaw-docs Retirement

> **Date** : 2026-06-09
> **But** : Documenter la décision de retirement selon la méthodologie P10 (Pillar 1)

## Decision Criteria

| Critère | Poids | Score (1-5) | Justification | Pondéré |
|---|---:|---:|---|---:|
| **Coût maintenance annuel** | 25 % | 4 | ~2h/mois × $50/h = $100/mois | **1.0** |
| **Valeur business** | 20 % | 1 | 0 visiteurs uniques/mois, devs utilisent Notion | **0.2** |
| **Complexité retirement** | 20 % | 1 | Site statique, pas de DB, pas d'users | **0.2** |
| **Risque compliance** | 15 % | 1 | Aucune PII, aucun contrat | **0.15** |
| **Risque utilisateur** | 20 % | 1 | Devs migrent vers Notion interne | **0.2** |
| **TOTAL** | **100 %** | | | **1.75** |

## Decision Rule

- **Score ≤ 2.0** : EOL recommandé ✅
- **Score 2.0-3.0** : Maintien optionnel
- **Score > 3.0** : Maintien obligatoire

## Final Decision

**✅ EOL ACCEPTÉ** — le retirement est approuvé selon la décision matrix (1.75 ≤ 2.0).

**Pattern choisi** : Big-Bang (niveau Simple)
**Date de retirement** : 2026-06-09 (demo)
**Responsable** : SWEBOK v4 P10 demo project

## Approvals (Demo simulation)

| Stakeholder | Role | Decision | Date |
|---|---|---|---|
| **sponsor** | Project lead | ✅ Approve | 2026-06-09 |
| **finance** | ROI | ✅ Approve (économie $100/mois) | 2026-06-09 |
| **legal** | Compliance | ✅ Approve (aucune PII) | 2026-06-09 |
| **data owner** | Documentation owner | ✅ Approve (EOL accepté) | 2026-06-09 |
| **IT** | Infrastructure | ✅ Approve (site à shutdown) | 2026-06-09 |
| **security** | Security | ✅ Approve (pas de PII) | 2026-06-09 |
