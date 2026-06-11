"""
probe_urls.py — interactive URL discovery helper
=================================================
Given a list of candidate URLs (file or stdin), probe each one with a
real GET (not HEAD, since some hosts — notably rfc-editor.org — block
HEAD for non-browser UAs) and report:
  - status code
  - content type
  - content length
  - the final URL after redirects
  - a sha256 of the first 4 KB (useful for dedup)
Saves a JSONL of working URLs to logs/working-urls.jsonl.

Use this BEFORE editing sources.yaml — it's much faster to fix URLs
based on a verified list than to iterate over a config full of stale
entries.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

LOG = logging.getLogger("probe_urls")
HERE = Path(__file__).resolve().parent.parent

UA = "swebok-corpus-crawler/1.0 (research, non-commercial)"


def probe_one(client: httpx.Client, url: str, follow: bool = True) -> dict:
    out = {"url": url, "timestamp": datetime.now(timezone.utc).isoformat()}
    try:
        # Use GET with stream so we can read first 4 KB without downloading full
        r = client.get(url, follow_redirects=follow, timeout=30)
        out["http_code"] = r.status_code
        out["final_url"] = str(r.url)
        out["content_type"] = r.headers.get("content-type", "")
        out["content_length"] = int(r.headers.get("content-length") or 0)
        body = r.content[: 4 * 1024]
        out["first_4kb_sha256"] = hashlib.sha256(body).hexdigest()
        out["working"] = 200 <= r.status_code < 400
    except (httpx.HTTPError, OSError, ValueError, TypeError, AttributeError) as exc:  # noqa: BLE001
        out["http_code"] = 0
        out["error"] = str(exc)
        out["working"] = False
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="file with one URL per line, or '-' for stdin")
    ap.add_argument("--out", default=str(HERE / "logs" / "working-urls.jsonl"))
    ap.add_argument("--also-working-only", action="store_true",
                    help="only print working URLs to stdout")
    args = ap.parse_args()
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")

    if args.input == "-":
        urls = [l.strip() for l in sys.stdin if l.strip()]
    else:
        urls = [l.strip() for l in Path(args.input).read_text(encoding="utf-8").splitlines()
                if l.strip() and not l.startswith("#")]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with httpx.Client(headers={"User-Agent": UA}, timeout=30) as client:
        with out_path.open("a", encoding="utf-8") as fh:
            for url in urls:
                res = probe_one(client, url)
                fh.write(json.dumps(res, ensure_ascii=False) + "\n")
                if args.also_working_only and res.get("working"):
                    print(res["final_url"] or url)
                else:
                    mark = "OK " if res.get("working") else "BAD"
                    code = res.get("http_code", "?")
                    ct = res.get("content_type", "")[:40]
                    print(f"  [{mark}] {code}  {url}  ({ct})")


if __name__ == "__main__":
    main()
