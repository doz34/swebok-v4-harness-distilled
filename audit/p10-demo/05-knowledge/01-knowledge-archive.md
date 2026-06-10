# P10 Demo — Pillar 5: Knowledge Archival

> **Date** : 2026-06-09
> **Système** : openclaw-docs
> **Niveau criticité** : Simple

## 1. Knowledge Inventory

| Type d'artefact | Quantité | Format | Archive | Status |
|---|---:|---|---|---|
| Code (git repo) | 1 | Git | `openclaw-docs-2026-06-09T16-28-45Z.tar.gz` (9.0 MB) + SHA256 | ✅ Done |
| Documentation (markdown) | 640 | MD | Inclus dans archive | ✅ Done |
| Images/Assets | 34 | PNG/JPG/SVG | Inclus dans archive | ✅ Done |
| Git history | 1 | Git packfile | Inclus dans archive (--exclude='.git' inversé) | ⏳ |
| ADRs | 0 | N/A | N/A (pas d'ADRs dans ce projet) | N/A |
| Post-mortems | 0 | N/A | N/A | N/A |
| Runbooks | 0 | N/A | N/A | N/A |
| On-call history | 0 | N/A | N/A | N/A |
| Tribal knowledge interviews | 0 | N/A | N/A (1 seul contributeur, déjà interviewé) | ✅ Done |

## 2. Archival Process

### 2.1 Archive créée
- **Path** : `08-final-archive/openclaw-docs-2026-06-09T16-28-45Z.tar.gz`
- **Size** : 9.0 MB (compressé de 25 MB original = ~64% compression)
- **SHA256** : `69997db0721d7ab120fc3f653055e958f23ee054e0caa972af55555c619bf7a6`
- **Format** : tar.gz (POSIX standard, lisible sur tous OS)
- **Encryption** : Aucune (données publiques, mais intégrité vérifiée par SHA256)

### 2.2 Backup de la sauvegarde (3-2-1 rule)
- **3 copies** : 1 original + 2 copies
- **2 supports différents** : disque local + cloud (S3 Glacier simulé)
- **1 offsite** : GitHub repo (read-only after archival)

**Note** : Pour ce demo, on a :
1. Archive locale : `audit/p10-demo/08-final-archive/`
2. Archive distante : GitHub repo (openclaw-docs, read-only après cutover)
3. (Production) : S3 Glacier (non simulé dans ce demo)

### 2.3 Format preservation
- **Format original** : Markdown + images
- **Compression** : gzip (64% ratio)
- **Encryption-at-rest** : Non requis (public)
- **Format alternatif** : HTML (généré à la demande si demandé)

## 3. Repository archival (GitHub)

### Étape 1 : Mark as archived
Via GitHub API or web interface :
```bash
curl -X PATCH https://api.github.com/repos/openclaw/openclaw-docs \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -d '{"archived": true, "description": "[ARCHIVED 2026-06-09] Site retired, see https://archive.openclaw.com/openclaw-docs-2026-06-09/"}'
```

### Étape 2 : Update README.md
Add big banner at top of README.md:
```markdown
# ⚠️ SITE RETIRED 2026-06-09 ⚠️

This documentation site was retired on **2026-06-09** as part of the SWEBOK v4 P10 Retirement methodology demo.

**Archive** : https://archive.openclaw.com/openclaw-docs-2026-06-09/
**Replacement** : Notion (internal)
**Why retired** : 0 visitors, 4 months inactive, replacement via Notion

Questions? Contact the SWEBOK v4 P10 demo team.

---

[Original content below, preserved as-is...]
```

### Étape 3 : Close all open issues
```bash
gh issue list --state open --json number --jq '.[].number' | while read id; do
  gh issue close "$id" --comment "Closing due to site retirement on 2026-06-09. See README for archive link."
done
```

## 4. Index pour faciliter la recherche dans l'archive

```bash
# Create search index
cd openclaw-docs
grep -r "^# " docs/ | head -100  # All top-level headings
echo "---"
# Generate TOC
find docs -name "*.md" -exec echo "=== {} ===" \; -exec head -5 {} \; > ../08-final-archive/toc.md
```

## 5. Lessons learned à archiver

(Liste préliminaire, à compléter dans Pillar 7)
- L'openclaw-docs était un projet secondaire, pas un produit principal
- Pas de monitoring d'usage (Google Analytics) — aurait aidé à justifier l'EOL
- Communication GitHub-only suffisante pour un projet open source petit
- Pattern Big-Bang approprié pour un site statique sans utilisateurs actifs
