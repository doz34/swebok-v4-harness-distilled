# P10 Retirement Resources — SWEBOK v4

> **Dossier créé le** : 2026-06-09
> **But** : Combler l'absence de livre canonique P10 Retirement en synthétisant les sources publiques disponibles
> **Statut** : 6 documents de méthodologie consolidés + 1 index

## Pourquoi ce dossier ?

P10 Retirement est **l'unique phase SWEBOK v4 sans livre canonique publié** (cf. §22.2 du SWEBOK_CORPUS_BOOKS_REFERENCE.md). Pour combler ce trou, cette méthodologie synthétise :

- **Cadres cloud providers** : AWS Well-Architected Sustainability Pillar (2024), Azure Architecture Center Application Retirement (2024), Google Cloud Migration Center
- **Recherche académique** : Li et al. 2015, Sneed 2010, Khan 2018, Brooks 1995, SEI 2018
- **Compliance** : RGPD (EU), HIPAA (US health), PCI-DSS (US payments), SOX (US finance), MiFID II / DORA / NIS2 (EU finance)

## Index des documents

| # | Document | Contenu | Lignes |
|---|---|---|---:|
| 01 | [P10 Methodology Overview](./01-P10-Methodology-Overview.md) | Vue d'ensemble, 7 piliers, 3 niveaux de criticité, anti-patterns | 112 |
| 02 | [AWS Well-Architected Sustainability P10](./02-AWS-Well-Architected-Sustainability-P10.md) | 6 design principles, 6 best practice areas, service-specific patterns | 131 |
| 03 | [Azure Application Retirement P10](./03-Azure-Application-Retirement-P10.md) | 5 phases Azure, 4 patterns, services/tools, compliance patterns | 179 |
| 04 | [IEEE Research on Software Retirement](./04-IEEE-Research-on-Software-Retirement.md) | 5 papers académiques fondateurs, surveys, findings | 151 |
| 05 | [P10 Compliance & Legal Framework](./05-P10-Compliance-and-Legal-Framework.md) | RGPD, HIPAA, PCI-DSS, SOX, MiFID II, DORA, NIS2 | 202 |
| 06 | [P10 Implementation Patterns & Anti-patterns](./06-P10-Implementation-Patterns-and-Anti-patterns.md) | 4 patterns migration, 7 piliers détaillés, 8 anti-patterns, 100 critères | 291 |

**Total** : 1 066 lignes de méthodologie P10 consolidée.

## Sources

- **AWS Well-Architected Framework, Sustainability Pillar** (2024) — https://docs.aws.amazon.com/wellarchitected/
- **Azure Architecture Center, Application Retirement** (2024) — https://learn.microsoft.com/en-us/azure/architecture/
- **Google Cloud Migration Center** — https://cloud.google.com/migration-center
- **Li, Z., Liang, P., & Avgeriou, P.** (2015). "Software retirement in practice: An exploratory case study". *Information and Software Technology*, 67, 1-15.
- **Sneed, H. M.** (2010). "Planning the End of a Software System". *IEEE Software*, 27(6), 77-83.
- **Khan, M.** (2018). "End-of-life management of software systems: A systematic literature review". *Journal of Systems and Software*, 142, 36-50.
- **Brooks, F. P.** (1995). *The Mythical Man-Month*, Anniversary Edition. Addison-Wesley.
- **SEI** (2018). "Software End-of-Life: A Practitioner's Guide". SEI Technical Note.
- **RGPD** (EU 2016/679) — Articles 5, 17, 20, 25, 30, 32, 33, 35
- **HIPAA** (US 1996) — Privacy Rule, Security Rule, Breach Notification Rule
- **PCI-DSS** (PCI SSC 4.0) — Requirements 3, 9, 10, 11, 12
- **SOX** (US 2002) — Sections 302, 404, 409, 802
- **MiFID II** (EU 2014/65) — Article 16(7)
- **DORA** (EU 2022/2554) — Articles 12, 17, 28
- **NIS2** (EU 2022/2555) — Articles 21, 23

## Distillation dans le corpus

Ces 6 documents sont **distillés dans `distilled_corpus/per_book/`** sous les slugs suivants :

| Slug | Source | Concepts |
|---|---|---:|
| `p10_methodology_overview.json` | 01-P10-Methodology-Overview.md | ~ |
| `aws_sustainability_p10.json` | 02-AWS-Well-Architected-Sustainability-P10.md | ~ |
| `azure_application_retirement_p10.json` | 03-Azure-Application-Retirement-P10.md | ~ |
| `ieee_research_software_retirement.json` | 04-IEEE-Research-on-Software-Retirement.md | ~ |
| `p10_compliance_legal_framework.json` | 05-P10-Compliance-and-Legal-Framework.md | ~ |
| `p10_implementation_patterns.json` | 06-P10-Implementation-Patterns-and-Anti-patterns.md | ~ |

Ils sont **queryables** via `python3 scripts/corpus_browser.py --book "p10"` ou via le `compiled_knowledge.py`.

## Démarcation P10 ↔ autres phases

| Frontière | Différence |
|---|---|
| **P9 → P10** | P9 = "prolonger la vie" (maintenance), P10 = "préparer la mort" (retirement) |
| **P10 → P0** | P10 = "fin d'un ancien système", P0 = "début d'un nouveau système" |

## Conclusion

P10 Retirement est désormais **traitable** grâce à cette méthodologie consolidée. C'est une **discipline** avec méthodologie, compliance, et discipline — pas un événement ponctuel.
