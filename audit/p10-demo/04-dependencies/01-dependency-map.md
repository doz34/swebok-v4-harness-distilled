# P10 Demo — Pillar 4: Dependency Map & Shutdown Plan

> **Date** : 2026-06-09
> **Système** : openclaw-docs
> **Niveau criticité** : Simple

## 1. Dependency Inventory

### 1.1 Incoming dependencies (who depends on this system)
| Source | Type | Action |
|---|---|---|
| `/home/doz/src/openclaw/` | Parent project (OpenClaw main repo) | Notify maintainer |
| `/home/doz/OPENCLAW_BUG_REPORT.md` | Local bug report | Migrate to Notion |
| `/home/doz/openclaw_help.txt` | Local help file | Migrate to Notion |
| Search engines (Google, Bing) | SEO | robots.txt + sitemap removal |
| 3rd party docs aggregators | SEO | Notify aggregators (if list known) |

### 1.2 Outgoing dependencies (what this system depends on)
| Target | Type | Action |
|---|---|---|
| GitHub (repo) | Hosting | Continue, repo read-only after retirement |
| GitHub Pages | Hosting (CNAME: docs.openclaw.ai) | Switch to archive.openclaw.com or 410 Gone |
| External links (http://127.0.0.1:11434, etc.) | Reference URLs in docs | Archive as-is, no impact |
| Internal OpenClaw repo (openclaw-ansible, etc.) | Cross-references | Add redirect note in archive |

### 1.3 CNAME Discovery
- **CNAME value** : `docs.openclaw.ai`
- **Hosted on** : GitHub Pages (assumed)

## 2. Cascade Shutdown Plan

### Etape 1 (T-0, 17:00 UTC) — Site cutover
1. **DNS** : Update CNAME from `docs.openclaw.ai` → `archive.openclaw.com` (or 410 Gone page)
2. **HTTPS** : Update SSL cert
3. **robots.txt** : Add `Disallow: /` and `noindex, nofollow`
4. **sitemap.xml** : Add `<lastmod>` and remove from search engines
5. **Site content** : Replace docs with single "archived" page (200 OK + clear notice)

### Etape 2 (T-0 + 1h) — Repo archival
1. **GitHub** : Mark repo as "archived" (read-only) via Settings
2. **GitHub API** : `PUT /repos/openclaw/openclaw-docs` with `archived: true`
3. **Issues/PRs** : Close all open issues with "site retired" message
4. **README.md** : Add big banner "SITE RETIRED 2026-06-09"

### Etape 3 (T-0 + 1d) — Infrastructure cleanup
1. **GitHub Pages** : Settings → Pages → disable
2. **Custom domain** : Remove `docs.openclaw.ai` from GitHub Pages settings
3. **DNS** : Remove CNAME record from DNS provider (if external)

### Etape 4 (T-1 semaine) — Post-monitoring
- Monitor site for 1 week
- Verify all redirects work
- Verify no broken links from external sites
- Verify GitHub archive status

## 3. Cutover Script (simule)

```bash
#!/bin/bash
# OpenClaw Docs Retirement Cutover — T-0
set -e

TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
ARCHIVE_NAME="openclaw-docs-${TIMESTAMP}.tar.gz"
ARCHIVE_DIR="08-final-archive"

echo "=== P10 Retirement: openclaw-docs ==="
echo "Timestamp: ${TIMESTAMP}"
echo ""

# Step 1: Create archive
echo "[1/5] Creating archive..."
tar --exclude='.git' -czf "${ARCHIVE_DIR}/${ARCHIVE_NAME}" openclaw-docs
sha256sum "${ARCHIVE_DIR}/${ARCHIVE_NAME}" > "${ARCHIVE_DIR}/${ARCHIVE_NAME}.sha256"

# Step 2: Mark GitHub repo as archived (via API)
echo "[2/5] Marking GitHub repo as archived..."
# curl -X PATCH https://api.github.com/repos/openclaw/openclaw-docs \
#   -H "Authorization: token ${GITHUB_TOKEN}" \
#   -d '{"archived": true}'

# Step 3: Update robots.txt
echo "[3/5] Updating robots.txt..."
cat > openclaw-docs/robots.txt <<EOF
User-agent: *
Disallow: /
# Site retired 2026-06-09
# Archive: https://archive.openclaw.com/openclaw-docs-2026-06-09/
EOF

# Step 4: Create archived page
echo "[4/5] Creating archived page..."
cat > openclaw-docs/docs/index.md <<EOF
---
summary: "Site archived on 2026-06-09"
title: "openclaw-docs (archived)"
---

# openclaw-docs — ARCHIVED

This documentation site was retired on **2026-06-09** as part of the SWEBOK v4 P10 Retirement methodology demo.
EOF

# Step 5: Verify
echo "[5/5] Verifying archive..."
tar -tzf "${ARCHIVE_DIR}/${ARCHIVE_NAME}" | wc -l
sha256sum -c "${ARCHIVE_DIR}/${ARCHIVE_NAME}.sha256"

echo ""
echo "=== Retirement COMPLETE ==="
```

## 4. Rollback Plan

If something goes wrong in the cutover:

| Scenario | Action | ETA |
|---|---|---|
| DNS doesn't propagate | Restore original CNAME | 24h (DNS TTL) |
| Archive missing files | Re-create from current openclaw-docs | 1h |
| Users can't access archive | Check S3 Glacier bucket, restore | 1h |
| GitHub API fails | Re-try or manual web interface | 1h |

**Maximum rollback time** : 24h (worst case: DNS issue)
