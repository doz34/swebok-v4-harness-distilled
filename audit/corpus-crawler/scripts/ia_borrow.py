"""
ia_borrow.py — Internet Archive controlled lending (manual)
============================================================
Internet Archive's lending library works by:
  1. Logging in with email + password (or a session cookie).
  2. Borrowing a book identifier (creates a 14-day loan on the user's
     account, single-seat at a time).
  3. Downloading the loan PDF (typically encrypted with a per-user key
     that IA's reader decrypts in-browser; programmatic download is
     rate-limited and may require the borrow API).

This script does NOT do the borrow API dance automatically. It:

  - Reads config/sources.yaml -> script_only_sources -> candidates.
  - For each ISBN, opens the borrowable URL in a format the user
    can paste into a browser (or queue for the controlled-lending
    CLI provided by IA).
  - Emits a list of "borrowed" file paths it would expect to be
    present, and verifies the ones the user has already pulled down
    to downloads/ia-borrow/.

The point: keep an auditable, dry-run-friendly record of WHAT we
plan to borrow, so we never silently exceed IA's loan quota or
end up with files we can't explain. If you have a paid IA account
and want full automation, swap in `archive_ia_borrow` from a vetted
Python client; we deliberately don't ship one here.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

HERE = Path(__file__).resolve().parent.parent
LOG = logging.getLogger("ia_borrow")


@dataclass
class BorrowPlan:
    isbn: str
    title: str
    author: str
    borrow_url: str
    expected_pdf: str
    status: str          # QUEUED | PRESENT | MISSING
    note: str = ""


def _build_borrow_url(isbn: str) -> str:
    return f"https://archive.org/details/isbn_{isbn}"


def plan(cfg: dict) -> list[BorrowPlan]:
    out_dir = HERE / "downloads" / "ia-borrow"
    out_dir.mkdir(parents=True, exist_ok=True)
    plans: list[BorrowPlan] = []
    for src in cfg.get("script_only_sources", []):
        if src.get("name") != "internet-archive-borrow":
            continue
        for c in src.get("candidates", []):
            isbn = c["isbn"]
            safe = f"{isbn}-{c['title'].lower().replace(' ', '-').replace(',', '')[:40]}.pdf"
            expected = out_dir / safe
            borrow_url = _build_borrow_url(isbn)
            if expected.exists():
                plans.append(BorrowPlan(isbn=isbn, title=c["title"], author=c["author"],
                                        borrow_url=borrow_url, expected_pdf=str(expected),
                                        status="PRESENT"))
            else:
                plans.append(BorrowPlan(isbn=isbn, title=c["title"], author=c["author"],
                                        borrow_url=borrow_url, expected_pdf=str(expected),
                                        status="QUEUED",
                                        note="Open the borrow URL in a browser, click Borrow, "
                                             "then save the PDF to expected_pdf."))
    return plans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true", help="emit the borrow plan as JSON")
    ap.add_argument("--print", action="store_true", help="print a human-readable checklist")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    cfg = yaml.safe_load((HERE / "config" / "sources.yaml").read_text(encoding="utf-8"))
    plans = plan(cfg)
    if args.print or not args.plan:
        print(f"\nInternet Archive borrow plan — {len(plans)} candidates\n")
        for p in plans:
            mark = "[x]" if p.status == "PRESENT" else "[ ]"
            print(f"  {mark} {p.isbn}  {p.title}  —  {p.author}")
            print(f"        borrow: {p.borrow_url}")
            print(f"        save to: {p.expected_pdf}")
            if p.note:
                print(f"        note: {p.note}")
        print()
    if args.plan:
        out = HERE / "index" / "ia-borrow-plan.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as fh:
            for p in plans:
                fh.write(json.dumps(asdict(p), ensure_ascii=False) + "\n")
        LOG.info("wrote %d plans -> %s", len(plans), out)


if __name__ == "__main__":
    main()
