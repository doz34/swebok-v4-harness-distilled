"""
html_to_md.py
==============
Convert HTML pages to clean Markdown, suitable for ingestion by the
swebok-v4-harness-distilled RAG/distillation pipeline.

Strategy:
  1. Use BeautifulSoup with lxml backend to parse.
  2. Drop <script>, <style>, <nav>, <header>, <footer>, <aside>, <noscript>,
     and any element with a class containing "nav", "footer", "header",
     "cookie", "banner", "sidebar", "menu", "ads", "promo".
  3. Pick the largest plausible <article>, <main>, or <body> as the
     main content area.
  4. Convert the rest to Markdown by hand-rolling: headings, paragraphs,
     lists, links, pre/code blocks, simple tables. We don't use a full
     HTML-to-MD library because they all fail in their own unique ways
     on standards bodies' CSS, and we want a deterministic output.
  5. Strip excessive whitespace, then write to <stem>.md.
  6. Write a sidecar JSON with the SHA256 of the input, output size,
     title, and a count of <h1>..<h6> elements.

This is intentionally a "good enough" converter. It produces Markdown
that the distillation pipeline can chunk and embed without choking on
JavaScript, nav menus, or cookie banners.
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

from bs4 import BeautifulSoup, NavigableString, Tag

LOG = logging.getLogger("html_to_md")

# tags we drop entirely (content-free)
_DROP_TAGS = {"script", "style", "noscript", "iframe", "svg", "form", "button"}

# classes/ids to drop (nav, ads, etc.). Matched on whole tokens to
# avoid catching e.g. "navbar-offset" or "position-relative".
_NOISE_TOKENS = {
    "nav", "menu", "footer", "header", "sidebar", "banner", "cookie",
    "promo", "ad", "ads", "breadcrumb", "skip", "widget", "popup",
    "modal", "toolbar", "navbar", "navigation", "advert", "adsbox",
}


def _token_match(value: str) -> bool:
    """Return True if any whitespace- or hyphen-separated token of
    `value` is in the noise set, OR matches a noise word as a whole
    word (e.g. 'nav' in 'nav-bar' or 'navigation' is fine; we want
    exact token matches to avoid false positives)."""
    if not value:
        return False
    tokens = set()
    for part in value.split():
        for sub in part.split("-"):
            if sub:
                tokens.add(sub.lower())
    return bool(tokens & _NOISE_TOKENS)


def _clean(soup: BeautifulSoup) -> BeautifulSoup:
    # Drop entire tag families first
    for tag in list(soup.find_all(_DROP_TAGS)):
        try:
            tag.decompose()
        except Exception:
            pass
    # Then walk remaining tags and drop noisy ones by class/id/aria
    for tag in list(soup.find_all(True)):
        try:
            attrs = tag.attrs
            if attrs is None:
                continue
            class_vals = list(attrs.get("class") or [])
            if not isinstance(class_vals, list):
                class_vals = [str(class_vals)]
            id_val = attrs.get("id") or ""
            haystack = " ".join(str(c) for c in class_vals) + " " + str(id_val)
            if _token_match(haystack):
                tag.decompose()
                continue
            if attrs.get("aria-hidden") == "true":
                tag.decompose()
                continue
            style = attrs.get("style") or ""
            if isinstance(style, str) and style.lower().startswith("display:none"):
                tag.decompose()
        except (AttributeError, TypeError):
            try:
                tag.decompose()
            except Exception:
                pass
    return soup


def _pick_main(soup: BeautifulSoup) -> Tag:
    """Pick the largest plausible content area. Heuristics, in order:
    1. The first <article> with > 400 chars
    2. The first <main> with > 400 chars
    3. The largest <pre> block (datatracker.ietf.org wraps the RFC
       body in a single <pre>)
    4. The first <[role=main]> with > 400 chars
    5. <body>"""
    for sel in ("article", "main", "[role=main]"):
        m = soup.select_one(sel)
        if m and len(m.get_text(strip=True)) > 400:
            return m
    # Largest <pre> — datatracker-style content
    pres = soup.find_all("pre")
    if pres:
        big = max(pres, key=lambda p: len(p.get_text()), default=None)
        if big and len(big.get_text(strip=True)) > 1000:
            return big.parent or big
    return soup.body or soup


# --------------------------------------------------------------------- inline
def _inline(node: Tag) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        if name in ("strong", "b"):
            parts.append(f"**{_inline(child).strip()}**")
        elif name in ("em", "i"):
            parts.append(f"*{_inline(child).strip()}*")
        elif name == "code":
            txt = child.get_text()
            parts.append(f"`{txt}`")
        elif name == "a":
            href = child.get("href", "")
            text = _inline(child).strip() or href
            if href and not href.startswith("#") and not href.startswith("javascript:"):
                parts.append(f"[{text}]({href})")
            else:
                parts.append(text)
        elif name == "br":
            parts.append("\n")
        else:
            parts.append(_inline(child))
    s = "".join(parts)
    return re.sub(r"\s+", " ", s).strip()


# --------------------------------------------------------------------- blocks
def _render(node: Tag, depth: int = 0) -> str:
    out: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            t = str(child).strip()
            if t:
                out.append(t)
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        if name in _DROP_TAGS or name in ("article", "main", "section", "div"):
            out.append(_render(child, depth))
            continue
        if re.match(r"h[1-6]$", name):
            level = int(name[1])
            text = _inline(child).strip()
            if text:
                out.append("")
                out.append("#" * level + " " + text)
            continue
        if name == "p":
            text = _inline(child).strip()
            if text:
                out.append("")
                out.append(text)
            continue
        if name == "pre":
            code_node = child.find("code")
            text = (code_node or child).get_text()
            lang = ""
            if code_node:
                cls = code_node.attrs.get("class") or []
                for c in cls:
                    if isinstance(c, str) and c.startswith("language-"):
                        lang = c[len("language-"):]
                        break
            # If the <pre> is enormous and contains no language-*
            # class, treat it as plain text (datatracker.ietf.org
            # style) — wrap in a fenced code block with no language.
            if not lang and len(text) > 5000:
                out.append("")
                out.append("```")
                out.append(text.rstrip())
                out.append("```")
                continue
            out.append("")
            out.append(f"```{lang}")
            out.append(text.rstrip())
            out.append("```")
            continue
        if name == "ul":
            out.append("")
            for li in child.find_all("li", recursive=False):
                out.append("- " + _inline(li).strip())
            continue
        if name == "ol":
            out.append("")
            for i, li in enumerate(child.find_all("li", recursive=False), 1):
                out.append(f"{i}. " + _inline(li).strip())
            continue
        if name == "table":
            out.append(_render_table(child))
            continue
        if name == "blockquote":
            inner = _render(child, depth + 1)
            out.append("")
            for line in inner.splitlines():
                if line.strip():
                    out.append("> " + line)
            continue
        if name == "hr":
            out.append("")
            out.append("---")
            continue
        # fallback: recurse
        out.append(_render(child, depth))
    return "\n".join(out)


def _render_table(table: Tag) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells: list[str] = []
        for cell in tr.find_all(["th", "td"]):
            cells.append(_inline(cell).strip().replace("|", "\\|").replace("\n", " "))
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    # align columns on max width
    flat: list[str] = [c for r in rows for c in r]
    width = max((len(c) for c in flat), default=1)
    width = min(width, 80)
    out: list[str] = []
    for i, row in enumerate(rows):
        out.append("| " + " | ".join(c[:width].ljust(width) for c in row) + " |")
        if i == 0:
            out.append("| " + " | ".join("-" * width for _ in row) + " |")
    return "\n".join(out)


# --------------------------------------------------------------------- public
@dataclass
class ConversionResult:
    input_path: str
    output_path: str
    sidecar_path: str
    title: str
    char_count: int
    heading_count: int
    sha256: str
    source_url: Optional[str] = None
    license_hint: str = ""
    error: str = ""
    timestamp: str = ""


def convert(html_path: Path, out_dir: Path, source_url: Optional[str] = None,
            license_hint: str = "") -> ConversionResult:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = html_path.stem
    md_path = out_dir / f"{stem}.md"
    side_path = out_dir / f"{stem}.sidecar.json"

    sha = hashlib.sha256()
    with html_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(64 * 1024), b""):
            sha.update(chunk)
    sha_hex = sha.hexdigest()

    if not html_path.exists():
        return ConversionResult(
            input_path=str(html_path), output_path="", sidecar_path=str(side_path),
            title="", char_count=0, heading_count=0, sha256=sha_hex,
            source_url=source_url, license_hint=license_hint,
            error="input not found", timestamp=datetime.now(timezone.utc).isoformat(),
        )

    try:
        raw = html_path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return ConversionResult(
            input_path=str(html_path), output_path="", sidecar_path=str(side_path),
            title="", char_count=0, heading_count=0, sha256=sha_hex,
            source_url=source_url, license_hint=license_hint,
            error=str(exc), timestamp=datetime.now(timezone.utc).isoformat(),
        )

    soup = BeautifulSoup(raw, "lxml")
    soup = _clean(soup)
    main = _pick_main(soup)

    title_node = soup.find("title")
    title = (title_node.get_text().strip() if title_node else "")[:200]

    body = _render(main)
    # collapse >2 blank lines
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    md_path.write_text(body, encoding="utf-8")
    heading_count = sum(1 for _ in re.finditer(r"^#{1,6}\s", body, re.MULTILINE))
    sidecar = {
        "input_path": str(html_path),
        "output_path": str(md_path),
        "title": title,
        "engine_used": "bs4-handrolled",
        "char_count": len(body),
        "heading_count": heading_count,
        "sha256": sha_hex,
        "source_url": source_url,
        "license_hint": license_hint,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    side_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    return ConversionResult(
        input_path=str(html_path), output_path=str(md_path), sidecar_path=str(side_path),
        title=title, char_count=len(body), heading_count=heading_count,
        sha256=sha_hex, source_url=source_url, license_hint=license_hint,
        timestamp=sidecar["timestamp"],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--source-url", default=None)
    ap.add_argument("--license", default="")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    res = convert(args.html, args.out_dir, source_url=args.source_url, license_hint=args.license)
    print(json.dumps(asdict(res), indent=2))
    sys.exit(0 if not res.error else 1)


if __name__ == "__main__":
    main()
