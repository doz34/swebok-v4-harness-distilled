#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Contextual Chunker
===========================================

Splits text/markdown files into logical chunks with rich metadata.
Pure Python, no LLM, no external deps.

Each chunk carries:
- id: stable hash
- file: source path
- book: derived from file (e.g., "Head First Design Patterns")
- chapter: heading context (e.g., "## The Strategy Pattern")
- section_path: full path of headings (e.g., ["Book", "Part 1", "Chapter 2"])
- start_line, end_line: line numbers in source
- start_char, end_char: character offsets
- text: the actual chunk content
- char_count, word_count, token_estimate: stats
- chunk_type: "markdown_section" | "code_block" | "paragraph" | "table"

Usage:
    from retrieval.chunker import chunk_file, chunk_directory
    chunks = chunk_file(Path("book.md"))
    all_chunks = chunk_directory(Path("corpus/"))
"""

import hashlib
import re
import sys
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterator

# Allow standalone import of security helpers
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.security import safe_read_text, MAX_FILE_BYTES, is_within_allowed  # noqa: E402


@dataclass
class Chunk:
    """A logical unit of text with full provenance."""
    id: str
    file: str
    book: str
    chapter: str
    section_path: list
    start_line: int
    end_line: int
    start_char: int
    end_char: int
    text: str
    chunk_type: str
    char_count: int
    word_count: int
    token_estimate: int

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def context_header(self) -> str:
        """One-line context for this chunk (for LLM prompt or display)."""
        path = " > ".join(self.section_path) if self.section_path else self.chapter
        return f"[{self.book}] {path} (L{self.start_line}-{self.end_line})"


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
_CODE_BLOCK_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
_TABLE_RE = re.compile(r"^\|.+\|\s*\n\|[\s\-:|]+\|", re.MULTILINE)


def _book_from_path(path: Path) -> str:
    """Derive a clean book name from the file path."""
    # Remove extension
    name = path.stem
    # Common cleanup patterns
    name = re.sub(r"^\d+_?", "", name)  # leading numeric
    name = re.sub(r"_\d+_?", " ", name)  # embedded numeric
    name = re.sub(r"[\(\[]\d{10,}[\)\]]", "", name)  # ISBN
    name = name.replace("_", " ").replace("-", " ").strip()
    # Title-case but preserve common acronyms
    parts = []
    for w in name.split():
        if w.upper() in ("SQL", "API", "REST", "HTTP", "CSS", "HTML", "JSON", "XML", "AI", "ML", "UI", "UX", "OOP", "MVC", "MVP", "CLI", "K8S", "AWS", "GCP", "CI", "CD", "JS", "TS", "GO", "CRDT", "OLAP", "OLTP"):
            parts.append(w.upper())
        else:
            parts.append(w.capitalize())
    return " ".join(parts) if parts else path.stem


def _token_estimate(text: str) -> int:
    """Rough token estimate (~4 chars per token for English)."""
    return max(1, len(text) // 4)


def _make_id(file: str, start_line: int, end_line: int, text: str) -> str:
    """Stable chunk ID based on file path, lines, and content hash."""
    h = hashlib.sha256(f"{file}:{start_line}:{end_line}".encode()).hexdigest()[:12]
    return f"c_{h}"


def _split_markdown_sections(text: str) -> Iterator[tuple]:
    """
    Split markdown into (start_line, end_line, section_path, section_text, chunk_type).
    A section is delimited by a heading of any level.
    """
    lines = text.split("\n")
    # Build list of heading positions
    headings = []  # (line_idx, level, title)
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    if not headings:
        # No headings: treat as one big paragraph chunk
        yield (0, len(lines) - 1, [], text, "paragraph")
        return
    # Yield preamble (before first heading)
    if headings[0][0] > 0:
        preamble = "\n".join(lines[: headings[0][0]])
        if preamble.strip():
            yield (0, headings[0][0] - 1, [], preamble, "paragraph")
    # Yield each section
    for i, (line_idx, level, title) in enumerate(headings):
        # Section ends at next heading of same or higher level, or end of file
        end_idx = len(lines)
        for j in range(i + 1, len(headings)):
            if headings[j][1] <= level:
                end_idx = headings[j][0]
                break
        # Build section path: all parent headings up to this one
        path = []
        for k in range(i, -1, -1):
            h_line, h_level, h_title = headings[k]
            if h_level <= level and (not path or path[-1][1] < h_level):
                path.append((h_title, h_level))
                if h_level == 1:
                    break
        path.reverse()
        section_path = [t for t, _ in path]
        section_text = "\n".join(lines[line_idx:end_idx])
        yield (line_idx, end_idx - 1, section_path, section_text, "markdown_section")


def _split_into_paragraphs(text: str, base_line: int = 0) -> Iterator[tuple]:
    """Split text into paragraphs (separated by blank lines)."""
    lines = text.split("\n")
    para_start = None
    para_lines = []
    for i, line in enumerate(lines):
        if line.strip():
            if para_start is None:
                para_start = i
            para_lines.append(line)
        else:
            if para_lines:
                yield (base_line + para_start, base_line + i - 1, "\n".join(para_lines))
                para_lines = []
                para_start = None
    if para_lines:
        yield (base_line + para_start, base_line + len(lines) - 1, "\n".join(para_lines))


def _split_oversized(text: str, max_chars: int = 1500, base_line: int = 0) -> Iterator[tuple]:
    """
    If a chunk exceeds max_chars, split it further.
    Tries to split at sentence boundaries; falls back to hard cut.
    """
    if len(text) <= max_chars:
        yield (base_line, base_line + text.count("\n"), text)
        return
    # Split by sentences (period, exclamation, question mark followed by space)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    current = ""
    current_start_line = base_line
    current_line_count = 0
    for sent in sentences:
        if len(current) + len(sent) > max_chars and current:
            yield (current_start_line, current_start_line + current.count("\n"), current)
            current = sent
            current_start_line = current_line_count
        else:
            current = current + " " + sent if current else sent
        current_line_count = current_start_line + current.count("\n")
    if current:
        yield (current_start_line, current_start_line + current.count("\n"), current)


def chunk_file(path: Path, max_chars: int = 1500, allow_symlinks: bool = False, allowed_roots: set = None) -> Iterator[Chunk]:
    """
    Chunk a single file into logical units with full metadata.
    Yields Chunk objects.

    SECURITY (NEW-02 fix): if allowed_roots is set, files outside any
    allowed root are rejected. Defaults: rejects symlinks, enforces
    max file size.
    """
    if not path.exists():
        return
    if path.is_symlink() and not allow_symlinks:
        # Reject symlinks by default (symlink attacks)
        return
    # Path allowlist check (NEW-02 fix)
    if allowed_roots is not None:
        if not is_within_allowed(path, allowed_roots):
            return
    try:
        text = safe_read_text(path, max_bytes=MAX_FILE_BYTES)
    except (FileNotFoundError, ValueError, OSError):
        return
    book = _book_from_path(path)
    char_offset = 0
    if path.suffix.lower() in (".md", ".markdown"):
        # Markdown: split by sections, then by paragraphs/sentences
        for start_line, end_line, section_path, section_text, chunk_type in _split_markdown_sections(text):
            # If section is too big, split it
            if len(section_text) > max_chars:
                for sub_start, sub_end, sub_text in _split_oversized(section_text, max_chars, start_line):
                    yield _make_chunk(
                        file=str(path), book=book, section_path=section_path,
                        start_line=sub_start, end_line=sub_end,
                        text=sub_text, chunk_type=chunk_type,
                        start_char=char_offset,
                    )
                    char_offset += len(sub_text)
            else:
                yield _make_chunk(
                    file=str(path), book=book, section_path=section_path,
                    start_line=start_line, end_line=end_line,
                    text=section_text, chunk_type=chunk_type,
                    start_char=char_offset,
                )
                char_offset += len(section_text)
    else:
        # Plain text: split by paragraphs
        for start_line, end_line, para_text in _split_into_paragraphs(text):
            if len(para_text) > max_chars:
                for sub_start, sub_end, sub_text in _split_oversized(para_text, max_chars, start_line):
                    yield _make_chunk(
                        file=str(path), book=book, section_path=[],
                        start_line=sub_start, end_line=sub_end,
                        text=sub_text, chunk_type="paragraph",
                        start_char=char_offset,
                    )
                    char_offset += len(sub_text)
            else:
                yield _make_chunk(
                    file=str(path), book=book, section_path=[],
                    start_line=start_line, end_line=end_line,
                    text=para_text, chunk_type="paragraph",
                    start_char=char_offset,
                )
                char_offset += len(para_text)


def _make_chunk(
    file: str, book: str, section_path: list,
    start_line: int, end_line: int, text: str, chunk_type: str,
    start_char: int,
) -> Chunk:
    chapter = section_path[0] if section_path else ""
    char_count = len(text)
    word_count = len(text.split())
    return Chunk(
        id=_make_id(file, start_line, end_line, text),
        file=file, book=book, chapter=chapter, section_path=section_path,
        start_line=start_line + 1, end_line=end_line + 1,  # 1-indexed
        start_char=start_char, end_char=start_char + char_count,
        text=text, chunk_type=chunk_type,
        char_count=char_count, word_count=word_count,
        token_estimate=_token_estimate(text),
    )


def chunk_directory(
    directory: Path,
    extensions: tuple = (".md", ".markdown", ".txt"),
    max_chars: int = 1500,
    allow_symlinks: bool = False,
    enforce_root: bool = True,
) -> Iterator[Chunk]:
    """
    Chunk all files in a directory recursively.
    Yields Chunk objects across all files.

    SECURITY (NEW-02 fix): by default enforces that all files are
    under the directory (the call-site root). Symlinks are rejected.
    """
    if not directory.exists():
        return
    # Set the allowlist to the directory (NEW-02 fix)
    allowed_roots = {directory.resolve()} if enforce_root else None
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions:
            yield from chunk_file(
                path, max_chars=max_chars, allow_symlinks=allow_symlinks,
                allowed_roots=allowed_roots,
            )


def chunks_to_jsonl(chunks: Iterator[Chunk], output_path: Path) -> int:
    """Write chunks to a JSONL file (one chunk per line). Returns count."""
    import json
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(output_path, "w") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")
            count += 1
    return count


# === CLI for standalone use ===
if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Chunk a directory of text/markdown files")
    parser.add_argument("directory", help="Directory to chunk recursively")
    parser.add_argument("--output", "-o", help="Output JSONL file (default: stdout)")
    parser.add_argument("--max-chars", type=int, default=1500, help="Max chars per chunk (default 1500)")
    parser.add_argument("--limit", type=int, default=10, help="Number of chunks to show (default 10)")
    args = parser.parse_args()
    chunks = chunk_directory(Path(args.directory), max_chars=args.max_chars)
    if args.output:
        n = chunks_to_jsonl(chunks, Path(args.output))
        print(f"Wrote {n} chunks to {args.output}")
    else:
        for i, chunk in enumerate(chunks):
            print(f"\n--- Chunk {i+1} ---")
            print(f"  ID: {chunk.id}")
            print(f"  Book: {chunk.book}")
            print(f"  Section: {' > '.join(chunk.section_path)}")
            print(f"  Lines: {chunk.start_line}-{chunk.end_line}")
            print(f"  Type: {chunk.chunk_type} | {chunk.char_count} chars | ~{chunk.token_estimate} tokens")
            print(f"  Text: {chunk.text[:200]}{'...' if len(chunk.text) > 200 else ''}")
            if i + 1 >= args.limit:
                print(f"\n(limited to {args.limit} chunks)")
                break
