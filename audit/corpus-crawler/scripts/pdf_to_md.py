"""
pdf_to_md.py
============
Convert PDF -> clean Markdown, suitable for ingestion by the
swebok-v4-harness-distilled RAG/distillation pipeline.

Strategy:
  1. Try pdfplumber first (best text quality on academic papers
     and standards; preserves line layout well).
  2. Fall back to pymupdf (fitz) for scanned/encoded PDFs that
     pdfplumber cannot parse cleanly.
  3. If the PDF is a scanned image (zero extractable text), do NOT
     OCR here — record that fact in the output sidecar and let a
     separate OCR pipeline (e.g. ocrmypdf) handle it later. We don't
     silently pipe pages through Tesseract, both because the output
     is poor quality and because large OCR jobs are out of scope.

Output:
  <stem>.md            — extracted text, cleaned to Markdown-like form
  <stem>.sidecar.json  — metadata: page count, char count, image-only flag,
                          hash, source URL, license hint
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOG = logging.getLogger("pdf_to_md")


@dataclass
class ConversionResult:
    input_path: str
    output_path: str
    sidecar_path: str
    page_count: int
    char_count: int
    is_image_only: bool
    engine_used: str          # "pdfplumber" | "pymupdf" | "skipped"
    sha256: str
    source_url: Optional[str] = None
    license_hint: str = ""
    error: str = ""
    timestamp: str = ""


# --------------------------------------------------------------------- text clean
_MULTI_NL = re.compile(r"\n{3,}")
_MULTI_SP = re.compile(r"[ \t]{2,}")
_PAGE_NUM = re.compile(r"^\s*\d+\s*$")


def _clean_page_text(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        s = line.rstrip()
        if not s:
            lines.append("")
            continue
        if _PAGE_NUM.match(s):
            continue
        # collapse multiple spaces/tabs
        s = _MULTI_SP.sub(" ", s)
        lines.append(s)
    # join and collapse >2 blank lines
    out = "\n".join(lines)
    out = _MULTI_NL.sub("\n\n", out)
    return out.strip()


# --------------------------------------------------------------------- engines
def _convert_pdfplumber(pdf_path: Path) -> tuple[str, int, bool]:
    import pdfplumber
    pieces = []
    page_count = 0
    char_count = 0
    with pdfplumber.open(str(pdf_path)) as pdf:
        page_count = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            txt = page.extract_text() or ""
            if i > 0:
                pieces.append(f"\n\n<!-- page {i+1} -->\n\n")
            pieces.append(_clean_page_text(txt))
            char_count += len(txt)
    full = "".join(pieces)
    # Heuristic: image-only if the entire document yielded < 50 chars/page
    is_image_only = (page_count > 0 and (char_count / page_count) < 50)
    return full, page_count, is_image_only


def _convert_pymupdf(pdf_path: Path) -> tuple[str, int, bool]:
    import fitz  # type: ignore
    pieces = []
    page_count = 0
    char_count = 0
    doc = fitz.open(str(pdf_path))
    try:
        page_count = doc.page_count
        for i, page in enumerate(doc):
            txt = page.get_text("text") or ""
            if i > 0:
                pieces.append(f"\n\n<!-- page {i+1} -->\n\n")
            pieces.append(_clean_page_text(txt))
            char_count += len(txt)
    finally:
        doc.close()
    full = "".join(pieces)
    is_image_only = (page_count > 0 and (char_count / page_count) < 50)
    return full, page_count, is_image_only


# --------------------------------------------------------------------- main
def convert(
    pdf_path: Path,
    out_dir: Path,
    source_url: Optional[str] = None,
    license_hint: str = "",
) -> ConversionResult:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = pdf_path.stem
    md_path = out_dir / f"{stem}.md"
    side_path = out_dir / f"{stem}.sidecar.json"

    sha = hashlib.sha256()
    with pdf_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(64 * 1024), b""):
            sha.update(chunk)
    sha_hex = sha.hexdigest()

    if not pdf_path.exists():
        return ConversionResult(
            input_path=str(pdf_path), output_path="", sidecar_path=str(side_path),
            page_count=0, char_count=0, is_image_only=False, engine_used="skipped",
            sha256=sha_hex, source_url=source_url, license_hint=license_hint,
            error="input file not found", timestamp=datetime.now(timezone.utc).isoformat(),
        )

    # Try pdfplumber first.
    engine = "pdfplumber"
    try:
        text, pages, image_only = _convert_pdfplumber(pdf_path)
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, ImportError) as exc:
        LOG.warning("pdfplumber failed on %s: %s — falling back to pymupdf", pdf_path, exc)
        try:
            text, pages, image_only = _convert_pymupdf(pdf_path)
            engine = "pymupdf"
        except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, ImportError) as exc2:
            LOG.error("pymupdf also failed on %s: %s", pdf_path, exc2)
            side_path.write_text(json.dumps({
                "error": str(exc2), "engine_attempted": "pymupdf",
                "source_url": source_url, "license_hint": license_hint,
                "sha256": sha_hex, "timestamp": datetime.now(timezone.utc).isoformat(),
            }, indent=2))
            return ConversionResult(
                input_path=str(pdf_path), output_path="", sidecar_path=str(side_path),
                page_count=0, char_count=0, is_image_only=False, engine_used="skipped",
                sha256=sha_hex, source_url=source_url, license_hint=license_hint,
                error=str(exc2), timestamp=datetime.now(timezone.utc).isoformat(),
            )

    md_path.write_text(text, encoding="utf-8")
    sidecar = {
        "input_path": str(pdf_path),
        "output_path": str(md_path),
        "engine_used": engine,
        "page_count": pages,
        "char_count": len(text),
        "is_image_only": image_only,
        "sha256": sha_hex,
        "source_url": source_url,
        "license_hint": license_hint,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "image_only_note": (
            "PDF appears to be scanned images; run `ocrmypdf <input> <out_pdf>` "
            "and reconvert. This pipeline does not OCR by default."
        ) if image_only else "",
    }
    side_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    return ConversionResult(
        input_path=str(pdf_path), output_path=str(md_path), sidecar_path=str(side_path),
        page_count=pages, char_count=len(text), is_image_only=image_only, engine_used=engine,
        sha256=sha_hex, source_url=source_url, license_hint=license_hint,
        timestamp=sidecar["timestamp"],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--source-url", default=None)
    ap.add_argument("--license", default="")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = convert(args.pdf, args.out_dir, source_url=args.source_url, license_hint=args.license)
    print(json.dumps(asdict(res), indent=2))
    sys.exit(0 if not res.error else 1)


if __name__ == "__main__":
    main()
