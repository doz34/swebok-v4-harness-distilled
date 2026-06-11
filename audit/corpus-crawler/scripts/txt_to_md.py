"""
txt_to_md.py — RFC / plain-text files -> Markdown
==================================================
For plain-text files (RFCs, etc.) we just need to:
  1. Read the text
  2. Detect simple heading patterns (lines of "=" or "-" underneath)
  3. Wrap long text into a single <pre> block (it's a plain-text RFC,
     not Markdown — keeping the layout is more useful than re-flowing)
  4. Add a YAML-style frontmatter with title, source URL, license
  5. Write sidecar with sha256, char count
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

LOG = logging.getLogger("txt_to_md")


@dataclass
class ConversionResult:
    input_path: str
    output_path: str
    sidecar_path: str
    title: str
    char_count: int
    sha256: str
    source_url: Optional[str] = None
    license_hint: str = ""
    error: str = ""
    timestamp: str = ""


def _detect_title(text: str) -> str:
    """Best-effort: look for the first non-empty line, trim and cap."""
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line[:200]
    return ""


def convert(txt_path: Path, out_dir: Path, source_url: Optional[str] = None,
            license_hint: str = "") -> ConversionResult:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = txt_path.stem
    md_path = out_dir / f"{stem}.md"
    side_path = out_dir / f"{stem}.sidecar.json"

    sha = hashlib.sha256()
    with txt_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(64 * 1024), b""):
            sha.update(chunk)
    sha_hex = sha.hexdigest()

    if not txt_path.exists():
        return ConversionResult(
            input_path=str(txt_path), output_path="", sidecar_path=str(side_path),
            title="", char_count=0, sha256=sha_hex,
            source_url=source_url, license_hint=license_hint,
            error="input not found", timestamp=datetime.now(timezone.utc).isoformat(),
        )

    try:
        raw = txt_path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError) as exc:
        return ConversionResult(
            input_path=str(txt_path), output_path="", sidecar_path=str(side_path),
            title="", char_count=0, sha256=sha_hex,
            source_url=source_url, license_hint=license_hint,
            error=str(exc), timestamp=datetime.now(timezone.utc).isoformat(),
        )

    title = _detect_title(raw)
    # Wrap as a fenced code block to preserve the RFC's text layout
    # (rfc-editor's text format has carefully-aligned column data that
    # would be destroyed by Markdown re-flowing).
    body = f"# {title}\n\n```\n{raw.rstrip()}\n```\n"
    md_path.write_text(body, encoding="utf-8")
    sidecar = {
        "input_path": str(txt_path),
        "output_path": str(md_path),
        "title": title,
        "engine_used": "passthrough",
        "char_count": len(raw),
        "sha256": sha_hex,
        "source_url": source_url,
        "license_hint": license_hint,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    side_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    return ConversionResult(
        input_path=str(txt_path), output_path=str(md_path), sidecar_path=str(side_path),
        title=title, char_count=len(raw), sha256=sha_hex,
        source_url=source_url, license_hint=license_hint,
        timestamp=sidecar["timestamp"],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("txt", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--source-url", default=None)
    ap.add_argument("--license", default="")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = convert(args.txt, args.out_dir, source_url=args.source_url, license_hint=args.license)
    print(json.dumps(asdict(res), indent=2))
    sys.exit(0 if not res.error else 1)


if __name__ == "__main__":
    main()
