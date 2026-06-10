"""
manifest_grab.py — download only the OFFICIAL free chapters listed in
audit/corpus-references/ACQUISITION_MANIFEST.md
==========================================================
This script reads the manifest, finds rows with a "Free chapter" or
"Sample" link, and uses the Fetcher to download ONLY that chapter
(typically a 10–30 page PDF). It never tries to fetch the full book.

Important policy:
  - We only download content that the publisher has explicitly made
    free. We never scrape around paywalls, never login as anyone,
    never use a borrowed copy.
  - If the manifest row has no free chapter, we skip it silently.
  - Every download is recorded in the audit log.
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from typing import Iterable, Optional

import yaml

HERE = Path(__file__).resolve().parent.parent
LOG = logging.getLogger("manifest_grab")

sys.path.insert(0, str(HERE / "scripts"))
from fetcher import Fetcher  # noqa: E402


@dataclass
class ChapterDownload:
    manifest_row: str
    title: str
    author: str
    isbn: str
    source_url: str
    saved_to: str
    status: str
    note: str = ""
    timestamp: str = ""


# Match a markdown table row: | ... | ... | ... |
# The manifest columns are: Pri | Livre | Auteur | Éditeur | ISBN-13 | Prix | Lien | Free chapter | Alt bib | Niveau
# Capture groups we care about: 1=Livre, 2=Auteur, 4=ISBN, 7=Free chapter
_ROW_RE = re.compile(
    r"\|\s*([^|]+?)\s*\|"  # pri
    r"\s*\*\*([^*]+)\*\*\s*\|"  # title (bold)
    r"\s*([^|]+?)\s*\|"  # author
    r"\s*([^|]+?)\s*\|"  # editor
    r"\s*(\d{13})\s*\|"  # ISBN-13
    r"\s*([^|]+?)\s*\|"  # price
    r"\s*([^|]+?)\s*\|"  # shop link
    r"\s*\[([^\]]+)\]\(([^)]+)\)\s*\|"  # free chapter
    r"([^|\n]*)"  # alt bib
)

_FALLBACK_RE = re.compile(
    r"\|\s*([^|]+?)\s*\|"  # pri
    r"\s*\*\*([^*]+)\*\*\s*\|"  # title
    r"\s*([^|]+?)\s*\|"  # author
    r"\s*([^|]+?)\s*\|"  # editor
    r"\s*(\d{13})\s*\|"  # ISBN
)


def parse_manifest(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line or line.count("|") < 6:
            continue
        # Find a markdown link inside the line
        link_re = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
        links = link_re.findall(line)
        if not links:
            continue
        title_match = re.search(r"\*\*([^*]+)\*\*", line)
        title = title_match.group(1).strip() if title_match else "?"
        isbn_match = re.search(r"(\d{13})", line)
        isbn = isbn_match.group(1) if isbn_match else ""
        # We look specifically for a "free chapter"-style link
        free_link = None
        for label, url in links:
            ll = label.lower()
            if "chapter" in ll or "sample" in ll or "excerpt" in ll or "free" in ll or ll.endswith(".pdf"):
                free_link = (label, url)
                break
        if not free_link:
            continue
        rows.append({"title": title, "isbn": isbn, "label": free_link[0], "url": free_link[1]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(HERE.parent / "corpus-references" / "ACQUISITION_MANIFEST.md"))
    ap.add_argument("--out", default=str(HERE / "downloads" / "manifest-chapters"))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    cfg = yaml.safe_load((HERE / "config" / "sources.yaml").read_text(encoding="utf-8"))
    fetcher = Fetcher(HERE / "config" / "sources.yaml", HERE / "logs" / "audit.jsonl")
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        LOG.error("manifest not found: %s", manifest_path)
        return 2

    rows = parse_manifest(manifest_path)
    LOG.info("found %d free-chapter links in manifest", len(rows))
    if args.limit:
        rows = rows[: args.limit]

    results: list[ChapterDownload] = []
    for r in rows:
        safe = re.sub(r"[^a-z0-9-]+", "-", r["title"].lower())[:50].strip("-")
        out_path = out_dir / f"{r['isbn']}-{safe}.pdf"
        if out_path.exists():
            results.append(ChapterDownload(manifest_row=r["title"], title=r["title"],
                                            author="", isbn=r["isbn"],
                                            source_url=r["url"], saved_to=str(out_path),
                                            status="SKIPPED", note="already on disk",
                                            timestamp=datetime.now(timezone.utc).isoformat()))
            continue
        if args.dry_run:
            results.append(ChapterDownload(manifest_row=r["title"], title=r["title"],
                                            author="", isbn=r["isbn"],
                                            source_url=r["url"], saved_to=str(out_path),
                                            status="DRYRUN", timestamp=datetime.now(timezone.utc).isoformat()))
            continue
        LOG.info("[FETCH] %s <- %s", r["title"], r["url"])
        res = fetcher.fetch(r["url"], out_path, license_hint="publisher free distribution")
        results.append(ChapterDownload(
            manifest_row=r["title"], title=r["title"], author="", isbn=r["isbn"],
            source_url=r["url"], saved_to=str(out_path),
            status=res.status, note=res.reason,
            timestamp=datetime.now(timezone.utc).isoformat(),
        ))
        if res.status != "OK":
            out_path.unlink(missing_ok=True)

    log_path = HERE / "logs" / "manifest-grab.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")

    summary = {}
    for r in results:
        summary[r.status] = summary.get(r.status, 0) + 1
    LOG.info("DONE: %s", summary)
    fetcher.close()
    return 0


if __name__ == "__main__":
    main()
