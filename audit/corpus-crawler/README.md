# corpus-crawler

Crawler légal pour élargir le corpus de `swebok-v4-harness-distilled/`.

## Politique

1. **Whitelist explicite des hôtes** — tout URL qui n'est pas listé dans
   `config/sources.yaml::allowed_hosts` est rejeté, même si le serveur
   répond 200.
2. **Respect de `robots.txt`** — pour chaque hôte, on parse
   `https://<host>/robots.txt` et on demande via notre User-Agent
   identifié. Si l'UA est interdit sur un chemin, on télécharge pas.
3. **User-Agent identifié** — `swebok-corpus-crawler/1.0 (research, ...)`.
4. **Rate limiting** — `min_delay_seconds` (1.5s) entre requêtes vers
   le même hôte, max 2 requêtes concurrentes par hôte.
5. **Cap de taille** — 80 MB par fichier par défaut, override par entrée.
6. **Cap de format** — content-type strict : un `.pdf` doit renvoyer
   `application/pdf`, un `.html` doit renvoyer `text/html`, un `.txt`
   doit renvoyer `text/plain` ou `application/octet-stream`. Les
   redirects malhonnêtes (ex: `owasp.org/...pdf` → page login GitHub)
   sont détectés et rejetés.
7. **Politique de license** — on ne télécharge que du contenu explicitement
   public-domain, CC, ou officiellement free-distribué par l'auteur/éditeur.
   Pas de scraping de "PDF download" louches, pas de Libgen, pas de Sci-Hub,
   pas de torrents, pas de .onion.

## Sources couvertes (par catégorie)

| Catégorie | Type | Sources notables |
|---|---|---|
| `nist-standards` | standards | NIST 800-53, CSF 2.0, AI RMF, SSDF, ZTA, RMF, Incident Handling |
| `owasp` | standards | ASVS 5.0, Top 10, Mobile Top 10, SAMM, Cheat Sheets, WSTG |
| `ietf-rfcs` | standards | HTTP, JSON, GeoJSON, Problem Details, QUIC, OAuth, JWT, TLS 1.2/1.3, URN |
| `w3c-recs` | standards | HTML, JSON-LD, SPARQL, OWL, RDF, XPath, XSLT, XML |
| `omg-specs` | standards | UML, BPMN 2.0 |
| `itu` | standards | X.509 |
| `gov-publications` | standards | ENISA, CSA, ISO 27001/27002/42010/12207 |
| `open-books` | books | Stanford CS190, SRE Google, 12-factor, Fowler articles, Laws of UX |
| `open-textbooks` | books | SICP, OSTEP, Sutton & Barto, Jurafsky, Boyd, Murphy, Downey, Sedgewick, Goodfellow, D2L |
| `pragprog-landing` | book-landing | Pragmatic Programmer 20th, Release It! 2e (offices pages) |
| `founder-papers` | papers | Parnas 1972, Brooks 1986, Naur 1985, Moseley & Marks 2006, Chen 1976 |
| `cncf-specs` | standards | OCI image/runtime, CNCF glossary, Argo, Flux, Kubernetes |

En plus :
- **Internet Archive borrow** : `scripts/ia_borrow.py` génère un plan de
  prêt pour ~15 classiques payants (Clean Code, DDD, Refactoring 2e,
  Pragmatic Programmer 20th, Mythical Man-Month, etc.). L'utilisateur
  ouvre le lien dans un navigateur, emprunte, et place le PDF dans
  `downloads/ia-borrow/`.
- **Manifest free chapters** : `scripts/manifest_grab.py` lit
  `ACQUISITION_MANIFEST.md` et télécharge uniquement les chapitres
  gratuits officiels (jamais le livre complet).

## Utilisation

### Lister toutes les sources
```
python3 crawl.py list
```

### Valider toutes les URLs (GET + Range 8KB, ne télécharge pas)
```
python3 crawl.py validate
```

### Prober des URLs candidates avant de les ajouter au config
```
python3 scripts/probe_urls.py scripts/probe-candidates.txt
python3 scripts/probe_urls.py scripts/probe-candidates.txt --also-working-only
```

### Télécharger une catégorie
```
python3 crawl.py crawl --category owasp
python3 crawl.py crawl --category nist-standards
python3 crawl.py crawl --category open-textbooks
python3 crawl.py crawl --category ietf-rfcs
```

### Télécharger une entrée unique
```
python3 crawl.py crawl --id nist-800-53r5
```

### Convertir tout en Markdown
```
python3 crawl.py index
python3 crawl.py convert downloads
# -> écrit dans md/ à côté du crawler
```

### Convertir vers un autre endroit
```
python3 crawl.py convert downloads --out-dir /tmp/corpus-md
```

### Index + stats
```
python3 crawl.py index
python3 crawl.py stats
```

### Manifest grab (chapitres gratuits officiels)
```
python3 scripts/manifest_grab.py --dry-run --limit 5
python3 scripts/manifest_grab.py --limit 10
```

### IA borrow (plan de prêt)
```
python3 scripts/ia_borrow.py --print
python3 scripts/ia_borrow.py --plan
```

## Arborescence

```
corpus-crawler/
├── README.md                       (ce fichier)
├── crawl.py                        (CLI principal)
├── config/
│   └── sources.yaml                (manifest des sources whitelistées)
├── scripts/
│   ├── fetcher.py                  (HTTP fetcher avec robots/rate-limit)
│   ├── pdf_to_md.py                (PDF → Markdown)
│   ├── html_to_md.py               (HTML → Markdown)
│   ├── txt_to_md.py                (TXT → Markdown — passthrough RFC)
│   ├── ia_borrow.py                (plan de prêt Internet Archive)
│   ├── manifest_grab.py            (télécharge chapitres gratuits du manifest)
│   ├── probe_urls.py               (URL discovery helper)
│   └── probe-candidates.txt        (liste d'URLs à tester)
├── downloads/
│   ├── books/                      (PDFs / HTML de livres open-access)
│   ├── standards/                  (PDFs / HTML / TXT de standards)
│   ├── papers/                     (papers fondateurs)
│   ├── manifest-chapters/          (chapitres gratuits éditeurs)
│   ├── book-landing/               (landing pages éditeurs)
│   └── ia-borrow/                  (PDFs empruntés via IA — user-side)
├── index/
│   ├── INDEX.jsonl                 (catalogue machine-readable)
│   └── ia-borrow-plan.jsonl        (plan de prêt IA)
├── logs/
│   ├── audit.jsonl                 (toutes les requêtes)
│   └── manifest-grab.jsonl         (résultats manifest grab)
├── md/                             (output par défaut du convert)
└── logs/URL_TODO.md                (URLs cassées à re-résoudre)
```

## Notes

- Le projet **n'inclut pas** et **n'automatise pas** l'acquisition
  d'œuvres sous copyright au-delà des contenus explicitement
  gratuits (chapitres publiés par les éditeurs, open-access,
  domaine public). Pour les livres intégralement sous copyright,
  le `ACQUISITION_MANIFEST.md` du projet liste les liens
  d'achat officiels (O'Reilly, Pearson, Amazon, etc.) et les
  options d'emprunt bibliothèque.
- Aucun `magnet:`, aucun `tor://`, aucun `.onion` n'est jamais
  résolu par ce crawler. Les hôtes non-whitelistés sont rejetés
  en amont par `fetcher.is_host_whitelisted()`.
- La conversion PDF→MD utilise `pdfplumber` puis `pymupdf` en
  fallback. Les PDF scannés (image-only) ne sont pas OCR-és ici ;
  un sidecar JSON enregistre le fait pour traitement ultérieur
  par `ocrmypdf` si tu veux.
- La conversion HTML→MD utilise `BeautifulSoup` avec un parser
  lxml. Les balises `<script>`, `<style>`, `<nav>`, etc. sont
  droppées, et les classes bruyantes (navbar, footer, ads, etc.)
  sont filtrées par tokens. Pour les sites JS-heavy (datatracker),
  on préfère rfc-editor.org pour le texte brut.
- Le validateur utilise GET avec `Range: bytes=0-8191` plutôt que
  HEAD car certains hôtes (rfc-editor.org, owasp.org) bloquent HEAD
  pour les UA non-browser. Le Range header garde la requête rapide.

## Dépendances

Toutes déjà installées dans l'environnement (cf. `pip3 list`) :
- `httpx` 0.28
- `PyYAML`
- `pdfplumber` 0.11
- `pdfminer.six` 20251230
- `PyMuPDF` (fitz) 1.27
- `beautifulsoup4` 4.14
- `lxml` (inferred)

Rien à installer de plus.
