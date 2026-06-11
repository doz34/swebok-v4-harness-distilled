#!/usr/bin/env python3
"""
SWEBOK v4 Harness — Batch Distillation Pipeline
================================================

Industrial-scale distillation for newly acquired books (PDF/EPUB/MD).
Converts source files to text, applies heuristic layer classification,
and generates per_book.json files compatible with the existing v1.5.2 schema.

Source format (existing v1.5.2):
{
  "book": "<title>",
  "file": "<original path>",
  "n_concepts": <int>,
  "by_layer": {"principle": <n>, "antipattern": <n>, ...},
  "concepts": [
    {"layer": "principle", "line": <int>, "content": "<text>"},
    ...
  ]
}

Heuristic layer classification:
  - "principle":    Imperative/definitional statement (length > 30, no question)
  - "recipe":       Numbered step, instruction, or procedure
  - "antipattern":  Warning / "don't" / "avoid" / "warning" / "pitfall"
  - "decision":     "if/then/else" or comparison structure
  - "entity":       Proper noun, acronym, named concept
  - "checklist":    Bulleted list item ("- " or "* ")
  - "faq":          Question + answer pair

Usage:
    python3 scripts/batch_distill.py --input <file> --title <title> --author <author> [--year YYYY]
    python3 scripts/batch_distill.py --batch <directory> [--recursive]
    python3 scripts/batch_distill.py --batch-csv <csv> --book-col 0 --path-col 1
"""

import os
import sys
import json
import re
import argparse
import subprocess
import zipfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple


# =============================================================================
# PDF / EPUB → TEXT CONVERSION
# =============================================================================

def convert_pdf_to_text(pdf_path: str) -> str:
    """Convert PDF to text using pdftotext with UTF-8."""
    try:
        result = subprocess.run(
            ['pdftotext', '-enc', 'UTF-8', '-q', pdf_path, '-'],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout
    except (subprocess.SubprocessError, OSError, FileNotFoundError) as e:
        print(f"  ⚠️ PDF extraction failed: {e}", file=sys.stderr)
        return ""


def convert_epub_to_text(epub_path: str) -> str:
    """Convert EPUB to text by extracting HTML content and stripping tags."""
    try:
        with zipfile.ZipFile(epub_path, 'r') as z:
            # Find all HTML/XHTML files
            html_files = [n for n in z.namelist() if n.endswith(('.html', '.xhtml', '.htm'))
                          and 'OEBPS' in n or 'OPS' in n or 'content' in n.lower()]
            html_files.sort()

            text_parts = []
            for hf in html_files:
                try:
                    content = z.read(hf).decode('utf-8', errors='ignore')
                    # Strip HTML tags, keep text
                    text = re.sub(r'<[^>]+>', ' ', content)
                    # Remove excess whitespace
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text:
                        text_parts.append(text)
                except (KeyError, ValueError, OSError, UnicodeDecodeError):
                    continue
            return '\n\n'.join(text_parts)
    except (zipfile.BadZipFile, OSError, ValueError, KeyError) as e:
        print(f"  ⚠️ EPUB extraction failed: {e}", file=sys.stderr)
        return ""


def convert_mobi_to_text(mobi_path: str) -> str:
    """Convert MOBI/AZW3 to text (basic extraction)."""
    # MOBI/AZW3 are proprietary. Use simple string extraction.
    # For high quality, use Calibre's ebook-convert, but basic extraction works.
    try:
        result = subprocess.run(
            ['ebook-convert', mobi_path, '-', '--txt-output-formatting=plain'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return result.stdout
    except FileNotFoundError:
        pass
    # Fallback: try to extract plain text
    try:
        with open(mobi_path, 'rb') as f:
            data = f.read()
        # Try to decode as UTF-8 with replacement
            text = data.decode('utf-8', errors='replace')
        # Extract printable ASCII / common UTF-8 chars
        printable = re.sub(r'[^\x20-\x7E\n\t]+', ' ', text)
        printable = re.sub(r'\s+', ' ', printable)
        return printable
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print(f"  ⚠️ MOBI extraction failed: {e}", file=sys.stderr)
        return ""


def convert_to_text(file_path: str) -> str:
    """Auto-detect format and convert to text."""
    lower = file_path.lower()
    if lower.endswith('.pdf'):
        return convert_pdf_to_text(file_path)
    elif lower.endswith('.epub'):
        return convert_epub_to_text(file_path)
    elif lower.endswith(('.mobi', '.azw3')):
        return convert_mobi_to_text(file_path)
    elif lower.endswith(('.md', '.txt')):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    else:
        return ""


# =============================================================================
# HEURISTIC LAYER CLASSIFICATION
# =============================================================================

# Patterns for layer detection
PATTERNS = {
    'antipattern': [
        r'\bdon\'?t\b', r'\bshouldn\'?t\b', r'\bavoid\b', r'\bnever\b',
        r'\bwarning\b', r'\bpitfall\b', r'\banti-?pattern\b',
        r'\bbad practice\b', r'\bdon\'?t do\b', r'\bdo not\b',
        r'\bcaution\b', r'\bsmell\b', r'\bnot recommended\b',
    ],
    'recipe': [
        r'^\s*\d+[\.\)]\s+',  # 1. or 1)
        r'^\s*step\s+\d+', r'^\s*Step\s+\d+',
        r'\bto\s+(do|achieve|create|implement|set up|build|configure|run|install)\b',
        r'\bclick\b.*\bthen\b', r'\bopen\b.*\band\b',
        r'^Run\b', r'^Use\b', r'^Create\b', r'^Add\b', r'^Set\b', r'^Build\b',
    ],
    'checklist': [
        r'^\s*[-*•]\s+',  # - or * or •
        r'^\s*\[\s*[xX ]?\s*\]\s+',  # [ ] or [x]
    ],
    'faq': [
        r'\?$',  # ends with question
        r'^\s*(Q|Question|FAQ)\s*[:.]',
        r'^\s*(A|Answer)\s*[:.]',
    ],
    'decision': [
        r'\bif\b.*\bthen\b', r'\bwhen\b.*\buse\b', r'\bchoose\b.*\bif\b',
        r'\beither\b.*\bor\b', r'\bfor each\b.*\buse\b',
    ],
    'entity': [
        # Capitalized phrases 2-4 words
        r'^[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){1,3}$',
        r'\b[A-Z]{2,}\b',  # Acronyms
    ],
}

# A principle is what remains after removing all the above (default)
MIN_LINE_LENGTH = 25  # minimum characters for a concept


def classify_line(line: str) -> Optional[str]:
    """Classify a single line by its primary layer. Returns layer name or None."""
    line = line.strip()
    if len(line) < MIN_LINE_LENGTH:
        return None

    # Check for antipattern (highest priority)
    for pat in PATTERNS['antipattern']:
        if re.search(pat, line, re.IGNORECASE):
            return 'antipattern'

    # Check for recipe
    for pat in PATTERNS['recipe']:
        if re.search(pat, line, re.IGNORECASE):
            return 'recipe'

    # Check for checklist
    for pat in PATTERNS['checklist']:
        if re.search(pat, line):
            return 'checklist'

    # Check for FAQ
    for pat in PATTERNS['faq']:
        if re.search(pat, line):
            return 'faq'

    # Check for decision
    for pat in PATTERNS['decision']:
        if re.search(pat, line, re.IGNORECASE):
            return 'decision'

    # Check for entity (only short lines, proper nouns)
    if len(line) < 100:
        for pat in PATTERNS['entity']:
            if re.match(pat, line):
                # Avoid classifying common English as entity
                if line.lower() not in ('the', 'a', 'an', 'and', 'or', 'but'):
                    return 'entity'

    # Default: principle (if line is substantive)
    if len(line) >= 40:
        return 'principle'

    return None


# =============================================================================
# CONCEPT EXTRACTION
# =============================================================================

def extract_concepts(text: str) -> List[Dict]:
    """Extract concepts from text. Returns list of {layer, line, content}."""
    if not text:
        return []

    lines = text.split('\n')
    concepts = []
    line_count = 0
    seen_hashes = set()  # avoid near-duplicates

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        # Skip obviously non-content lines
        if len(line) < 5:
            continue
        if line.startswith('---') or line.startswith('==='):
            continue
        if all(c in '=*#-_~' for c in line):
            continue

        # Classify
        layer = classify_line(line)
        if not layer:
            continue

        # Deduplication
        h = hash(line[:80].lower())
        if h in seen_hashes:
            continue
        seen_hashes.add(h)

        concepts.append({
            'layer': layer,
            'line': i,
            'content': line[:500]  # cap at 500 chars
        })
        line_count += 1

    return concepts


# =============================================================================
# PER_BOOK.JSON GENERATION
# =============================================================================

def slugify(s: str) -> str:
    """Generate a safe filename slug."""
    s = re.sub(r'[^\w\s-]', '', s.lower())
    s = re.sub(r'[-\s]+', '_', s).strip('-_')
    return s[:80]


def build_per_book_json(title: str, author: str, year: int, source_path: str,
                         text: str, max_concepts: int = 1500) -> Dict:
    """Build a per_book.json from extracted text."""
    concepts = extract_concepts(text)
    # Cap to prevent memory issues
    if len(concepts) > max_concepts:
        # Sample evenly across the book
        step = len(concepts) // max_concepts
        concepts = concepts[::step][:max_concepts]

    # Reassign line numbers to be sequential
    for idx, c in enumerate(concepts, 1):
        c['seq'] = idx

    # Build by_layer counts
    by_layer = {}
    for c in concepts:
        by_layer[c['layer']] = by_layer.get(c['layer'], 0) + 1

    return {
        'book': title,
        'file': source_path,
        'n_concepts': len(concepts),
        'by_layer': by_layer,
        'concepts': concepts,
        'author': author,
        'year': year,
        'distilled_at': '2026-06-06T00:00:00',
        'distiller': 'batch_distill_v1.0',
    }


# =============================================================================
# BATCH PROCESSING
# =============================================================================

def process_file(file_path: str, title: str = None, author: str = '', year: int = 0) -> Optional[Dict]:
    """Process a single file and return the per_book data (or None on failure)."""
    if not os.path.exists(file_path):
        print(f"  ❌ File not found: {file_path}")
        return None

    if title is None:
        title = Path(file_path).stem

    print(f"  📖 Processing: {Path(file_path).name} ({file_path})")
    text = convert_to_text(file_path)
    if not text:
        print(f"  ❌ No text extracted")
        return None
    print(f"     Text: {len(text):,} chars, {len(text.split(chr(10))):,} lines")

    data = build_per_book_json(title, author, year, file_path, text)
    print(f"     Concepts: {data['n_concepts']} | Layers: {data['by_layer']}")
    return data


def save_per_book(data: Dict, output_dir: str = None):
    """Save a per_book.json to the corpus directory."""
    if output_dir is None:
        output_dir = '/home/doz/swebok-v4-harness-distilled/distilled_corpus/per_book'
    slug = slugify(data['book'])
    fp = os.path.join(output_dir, f"{slug}.json")
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"     💾 Saved: {fp}")
    return fp


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Batch distillation of books for SWEBOK v4 Harness')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # Process single file
    p1 = sub.add_parser('file', help='Process a single file')
    p1.add_argument('--input', required=True, help='Input file (PDF/EPUB/MD)')
    p1.add_argument('--title', help='Book title (default: filename)')
    p1.add_argument('--author', default='', help='Author')
    p1.add_argument('--year', type=int, default=0, help='Year')

    # Process batch from directory
    p2 = sub.add_parser('dir', help='Process all books in a directory')
    p2.add_argument('--dir', required=True, help='Directory containing books')
    p2.add_argument('--recursive', action='store_true')
    p2.add_argument('--pattern', default='*.{pdf,epub,mobi,azw3,md}')
    p2.add_argument('--metadata-csv', help='CSV file with title,author,year per book')

    # Process from JSON manifest
    p3 = sub.add_parser('manifest', help='Process books from JSON manifest')
    p3.add_argument('--manifest', required=True, help='JSON manifest file with {file, title, author, year, phase}')

    args = parser.parse_args()

    if args.cmd == 'file':
        data = process_file(args.input, args.title, args.author, args.year)
        if data:
            save_per_book(data)

    elif args.cmd == 'dir':
        path = Path(args.dir)
        if not path.exists():
            print(f"❌ Directory not found: {args.dir}")
            return
        # Build pattern
        patterns = args.pattern.split(',')
        files = []
        for pat in patterns:
            if args.recursive:
                files.extend(path.rglob(pat.strip()))
            else:
                files.extend(path.glob(pat.strip()))
        files = sorted(set(files))

        # Optional metadata CSV
        metadata = {}
        if args.metadata_csv and os.path.exists(args.metadata_csv):
            import csv
            with open(args.metadata_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    fname = row.get('file', '').strip()
                    if fname:
                        metadata[fname] = {
                            'title': row.get('title', '').strip(),
                            'author': row.get('author', '').strip(),
                            'year': int(row.get('year', 0) or 0)
                        }

        print(f"📚 Found {len(files)} books to process")
        for f in files:
            fname = f.name
            meta = metadata.get(fname, {})
            data = process_file(
                str(f),
                title=meta.get('title'),
                author=meta.get('author', ''),
                year=meta.get('year', 0)
            )
            if data:
                save_per_book(data)

    elif args.cmd == 'manifest':
        with open(args.manifest, 'r') as f:
            manifest = json.load(f)
        print(f"📚 Processing {len(manifest)} books from manifest")
        for item in manifest:
            data = process_file(
                item['file'],
                title=item.get('title'),
                author=item.get('author', ''),
                year=item.get('year', 0)
            )
            if data:
                save_per_book(data)


if __name__ == '__main__':
    main()
