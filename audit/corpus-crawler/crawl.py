#!/usr/bin/env python3
"""
crawl.py — corpus-crawler CLI orchestrator
==========================================
Commands:
  crawl   crawl <category>   # download one or all categories from sources.yaml
  convert convert <dir>      # batch-convert all PDFs in a directory tree to MD
  list   list                # list all entries grouped by category
  validate validate          # audit all URLs in sources.yaml (HEAD request)
  index   index              # rebuild the corpus index (downloads/INDEX.jsonl)
  stats   stats              # summary of what was downloaded and converted

Run from the corpus-crawler/ directory.

Examples:
  python crawl.py list
  python crawl.py crawl --category owasp
  python crawl.py crawl --id nist-800-53r5
  python crawl.py convert downloads/standards
  python crawl.py validate
  python crawl.py index
  python crawl.py stats
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import yaml

# Make `scripts/` importable
HERE = Path(__file__).resolve().parent
SCRIPTS = HERE / "scripts"
sys.path.insert(0, str(SCRIPTS))

from fetcher import Fetcher  # noqa: E402
from pdf_to_md import convert as pdf_to_md  # noqa: E402
from html_to_md import convert as html_to_md  # noqa: E402
from txt_to_md import convert as txt_to_md  # noqa: E402

LOG = logging.getLogger("crawl")


# --------------------------------------------------------------------- helpers
def _load_config() -> dict:
    return yaml.safe_load((HERE / "config" / "sources.yaml").read_text(encoding="utf-8"))


def _iter_entries(cfg: dict, category: Optional[str] = None) -> Iterable[tuple[str, dict, dict]]:
    """Yields (entry_id, entry_dict, category_dict) pairs."""
    for cat in cfg.get("categories", []):
        if category and cat["name"] != category:
            continue
        for entry in cat.get("entries", []):
            yield entry["id"], entry, cat


def _download_path(cfg: dict, category: dict, entry: dict) -> Path:
    kind = category.get("kind", "misc")
    base = HERE / "downloads" / kind
    safe = entry["id"].replace("/", "_")
    # explicit format wins
    fmt = entry.get("format")
    if fmt == "html":
        return base / f"{safe}.html"
    if fmt == "md":
        return base / f"{safe}.md"
    if fmt == "txt":
        return base / f"{safe}.txt"
    # else: infer from the URL extension; default to .pdf
    url = entry.get("resolved_url") or entry["url"]
    lower = url.lower().split("?")[0]
    for ext in (".pdf", ".txt", ".html", ".md"):
        if lower.endswith(ext):
            return base / f"{safe}{ext}"
    return base / f"{safe}.pdf"


# --------------------------------------------------------------------- crawl
def cmd_crawl(args) -> int:
    cfg = _load_config()
    fetcher = Fetcher(HERE / "config" / "sources.yaml", HERE / "logs" / "audit.jsonl")
    try:
        n_ok = n_blocked = n_failed = n_too_big = n_skipped = 0
        for eid, entry, cat in _iter_entries(cfg, category=args.category):
            if args.id and eid != args.id:
                continue
            if entry.get("broken"):
                LOG.info("[SKIP-BROKEN] %s marked as unreachable in config", eid)
                n_skipped += 1
                continue
            url = entry.get("resolved_url") or entry["url"]
            out = _download_path(cfg, cat, entry)
            if out.exists() and not args.force:
                LOG.info("[SKIP] %s already at %s", eid, out)
                continue
            LOG.info("[FETCH] %s <- %s", eid, url)
            res = fetcher.fetch(
                url, out,
                max_size_mb_override=entry.get("max_size_mb"),
                license_hint=entry.get("license") or cat.get("license", ""),
            )
            if res.status == "OK":
                n_ok += 1
            elif res.status in ("BLOCKED", "ROBOTS_FORBIDDEN", "REJECTED"):
                n_blocked += 1
            elif res.status == "TOO_BIG":
                n_too_big += 1
            else:
                n_failed += 1
        LOG.info("DONE: ok=%d blocked=%d too_big=%d failed=%d", n_ok, n_blocked, n_too_big, n_failed)
        return 0
    finally:
        fetcher.close()


# --------------------------------------------------------------------- list
def cmd_list(args) -> int:
    cfg = _load_config()
    by_cat: dict[str, list[tuple[str, str, list[str]]]] = defaultdict(list)
    for eid, entry, cat in _iter_entries(cfg):
        by_cat[cat["name"]].append((eid, entry["title"], entry.get("phase", [])))
    for cat_name, items in by_cat.items():
        cat = next(c for c in cfg["categories"] if c["name"] == cat_name)
        print(f"\n## {cat_name}  ({cat.get('kind','?')} — {cat.get('license','?')})")
        for eid, title, phases in items:
            phase_str = ",".join(phases) if phases else "-"
            print(f"  - {eid:<45}  [{phase_str}]  {title}")
    print()
    return 0


# --------------------------------------------------------------------- convert
def cmd_convert(args) -> int:
    root = Path(args.dir).resolve()
    if not root.exists():
        LOG.error("no such directory: %s", root)
        return 2
    out_root = Path(args.out_dir).resolve() if args.out_dir else root
    pdfs = sorted(root.rglob("*.pdf"))
    htmls = sorted(root.rglob("*.html")) + sorted(root.rglob("*.htm"))
    txts = sorted(root.rglob("*.txt"))
    LOG.info("converting %d PDFs + %d HTMLs + %d TXTs under %s -> %s",
             len(pdfs), len(htmls), len(txts), root, out_root)
    n_ok = n_fail = n_image = n_skip = 0
    # Index the existing .md sidecars (PDF and HTML) to skip already-done
    already_md = {p.stem for p in out_root.rglob("*.md")}
    for pdf in pdfs:
        if pdf.stem in already_md:
            n_skip += 1
            continue
        rel = pdf.relative_to(root)
        out_sub = out_root / rel.parent
        url = (args.url_map or {}).get(pdf.name, "")
        res = pdf_to_md(pdf, out_sub, source_url=url or None, license_hint=args.license)
        if res.error:
            n_fail += 1
        elif res.is_image_only:
            n_image += 1
        else:
            n_ok += 1
    for html in htmls:
        if html.stem in already_md:
            n_skip += 1
            continue
        rel = html.relative_to(root)
        out_sub = out_root / rel.parent
        url = (args.url_map or {}).get(html.name, "")
        res = html_to_md(html, out_sub, source_url=url or None, license_hint=args.license)
        if res.error:
            n_fail += 1
        else:
            n_ok += 1
    for txt in txts:
        if txt.stem in already_md:
            n_skip += 1
            continue
        rel = txt.relative_to(root)
        out_sub = out_root / rel.parent
        url = (args.url_map or {}).get(txt.name, "")
        res = txt_to_md(txt, out_sub, source_url=url or None, license_hint=args.license)
        if res.error:
            n_fail += 1
        else:
            n_ok += 1
    LOG.info("CONVERT: ok=%d image_only=%d skipped=%d failed=%d", n_ok, n_image, n_skip, n_fail)
    return 0


# --------------------------------------------------------------------- validate
def cmd_validate(args) -> int:
    """Audit all URLs in sources.yaml with a real GET (not HEAD) — some
    hosts (rfc-editor.org notably) return 404 on HEAD with non-browser
    UAs. GETs are capped at 8 KB to stay fast."""
    import httpx
    cfg = _load_config()
    fetcher = Fetcher(HERE / "config" / "sources.yaml", HERE / "logs" / "audit.jsonl")
    whitelist = fetcher.allowed_hosts
    n_total = n_blocked = n_ok = n_warn = 0
    client = httpx.Client(
        headers={"User-Agent": cfg["policy"]["user_agent"]},
        timeout=20, follow_redirects=True,
    )
    for eid, entry, cat in _iter_entries(cfg):
        if entry.get("broken"):
            continue
        url = entry.get("resolved_url") or entry["url"]
        n_total += 1
        host = (url.split("/")[2] if "://" in url else "")
        if host not in whitelist:
            print(f"  [BLOCKED] {eid:<45} host not whitelisted: {host}")
            n_blocked += 1
            continue
        try:
            # Range request to cap at first 8KB
            r = client.get(url, headers={"Range": "bytes=0-8191"})
            code = r.status_code
            ctype = r.headers.get("content-type", "")[:30]
            if 200 <= code < 400:
                print(f"  [OK      {code}] {eid:<45} {ctype}  {url}")
                n_ok += 1
            else:
                print(f"  [HTTP {code}] {eid:<45} {url}")
                n_warn += 1
        except (httpx.HTTPError, OSError, ValueError, TypeError, AttributeError) as exc:
            print(f"  [FAIL    ] {eid:<45} {url}  ({exc})")
            n_warn += 1
    client.close()
    fetcher.close()
    print(f"\nValidated {n_total} entries: {n_ok} OK, {n_warn} warning, {n_blocked} blocked-by-whitelist")
    return 0


# --------------------------------------------------------------------- index
def cmd_index(args) -> int:
    """Rebuild downloads/INDEX.jsonl from what's on disk."""
    cfg = _load_config()
    by_id = {eid: (entry, cat) for eid, entry, cat in _iter_entries(cfg)}
    rows = []
    for path in sorted((HERE / "downloads").rglob("*")):
        if not path.is_file():
            continue
        eid = path.stem
        meta_entry, meta_cat = by_id.get(eid, (None, None))
        url = (meta_entry.get("resolved_url") or meta_entry["url"]) if meta_entry else ""
        rows.append({
            "id": eid,
            "path": str(path.relative_to(HERE)),
            "size_bytes": path.stat().st_size,
            "kind": meta_cat.get("kind", "?") if meta_cat else "?",
            "license_hint": (meta_entry.get("license") or meta_cat.get("license", ""))
                            if meta_entry else "",
            "source_url": url,
            "phase": meta_entry.get("phase", []) if meta_entry else [],
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        })
    idx_path = HERE / "index" / "INDEX.jsonl"
    idx_path.parent.mkdir(parents=True, exist_ok=True)
    with idx_path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    LOG.info("indexed %d files -> %s", len(rows), idx_path)
    return 0


# --------------------------------------------------------------------- stats
def cmd_stats(args) -> int:
    idx = HERE / "index" / "INDEX.jsonl"
    if not idx.exists():
        LOG.warning("no index yet — run `python crawl.py index` first")
        return 0
    by_kind: dict[str, int] = defaultdict(int)
    size_by_kind: dict[str, int] = defaultdict(int)
    n = 0
    for line in idx.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        by_kind[row.get("kind", "?")] += 1
        size_by_kind[row.get("kind", "?")] += row.get("size_bytes", 0)
        n += 1
    print(f"\nCorpus index: {n} files\n")
    for k, count in sorted(by_kind.items()):
        mb = size_by_kind[k] / 1024 / 1024
        print(f"  {k:<14}  {count:>4} files   {mb:>8.1f} MB")
    print()
    return 0


# --------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(prog="corpus-crawler", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    p_crawl = sub.add_parser("crawl", help="download files from sources.yaml")
    p_crawl.add_argument("--category", default=None, help="only crawl this category name")
    p_crawl.add_argument("--id", default=None, help="only crawl this single entry id")
    p_crawl.add_argument("--force", action="store_true", help="re-download even if file exists")
    p_crawl.set_defaults(func=cmd_crawl)

    p_list = sub.add_parser("list", help="list all entries")
    p_list.set_defaults(func=cmd_list)

    p_conv = sub.add_parser("convert", help="batch convert PDFs and HTMLs to Markdown")
    p_conv.add_argument("dir")
    p_conv.add_argument("--out-dir", default=None,
                        help="defaults to ./md next to the crawler")
    p_conv.add_argument("--license", default="")
    p_conv.add_argument("--url-map", default=None,
                        help="path to JSON filename->url map (default: use index/INDEX.jsonl)")
    p_conv.set_defaults(func=cmd_convert)

    p_val = sub.add_parser("validate", help="HEAD-check every URL in sources.yaml")
    p_val.set_defaults(func=cmd_validate)

    p_idx = sub.add_parser("index", help="rebuild the corpus index from disk")
    p_idx.set_defaults(func=cmd_index)

    p_stat = sub.add_parser("stats", help="print corpus stats")
    p_stat.set_defaults(func=cmd_stats)

    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if args.cmd == "convert":
        if args.url_map is None:
            # default: build the url map from the index
            idx = HERE / "index" / "INDEX.jsonl"
            if idx.exists():
                url_map = {}
                for line in idx.read_text(encoding="utf-8").splitlines():
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    fname = Path(row["path"]).name
                    url_map[fname] = row.get("source_url", "")
                args.url_map = url_map
            else:
                args.url_map = {}
        elif isinstance(args.url_map, str):
            args.url_map = json.loads(Path(args.url_map).read_text())
        # default --out-dir to ./md
        if getattr(args, "out_dir", None) is None:
            args.out_dir = HERE / "md"
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
