#!/usr/bin/env python3
"""
SWEBOK v4 Harness - Knowledge Graph Generator
Fast indexing using Python directly
Usage: python3 generate-kg.py [--rebuild] [--lite]
"""

import sys
import sqlite3
import os
from pathlib import Path

HARNESS_DIR = Path(__file__).parent.parent
DB_DIR = HARNESS_DIR / "knowledge"
DB_PATH = DB_DIR / "swebok.db"
LITE = "--lite" in sys.argv
REBUILD = "--rebuild" in sys.argv

def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("DROP TABLE IF EXISTS swebok_fts")
    conn.execute("""
        CREATE VIRTUAL TABLE swebok_fts USING fts5(
            content,
            ka,
            phase,
            metadata
        )
    """)
    conn.commit()
    conn.close()

def extract_ka(content, filename):
    import re
    # Try filename first
    match = re.search(r'KA-(\d+)', filename)
    if match:
        return f"KA-{match.group(1)}"
    # Try content
    match = re.search(r'KA-(\d+)', content[:1000])
    if match:
        return f"KA-{match.group(1)}"
    return "all"

def extract_phase(content):
    import re
    match = re.search(r'Phase (\d)', content[:1000])
    if match:
        return f"P{match.group(1)}"
    return "all"

def index_file(conn, filepath, source):
    try:
        content = filepath.read_text(errors='ignore')
        ka = extract_ka(content, filepath.name)
        phase = extract_phase(content)
        metadata = f"{source}:{filepath.name}"

        conn.execute("INSERT INTO swebok_fts (content, ka, phase, metadata) VALUES (?, ?, ?, ?)",
                    (content, ka, phase, metadata))
    except Exception as e:
        print(f"[WARN] Failed to index {filepath}: {e}")

def main():
    print("[KG] SWEBOK v4 Harness - Knowledge Graph Generator")

    if REBUILD and DB_PATH.exists():
        print("[KG] Rebuilding database...")
        DB_PATH.unlink()

    init_db()
    conn = sqlite3.connect(str(DB_PATH))
    total = 0

    # knowledge/swebok-sections
    print("[KG] Indexing knowledge/swebok-sections...")
    count = 0
    for f in (HARNESS_DIR / "knowledge" / "swebok-sections").glob("*.md"):
        index_file(conn, f, "swebok-sections")
        count += 1
    print(f"[KG] Indexed {count} files from swebok-sections")
    total += count

    # corpus/by-phase
    print("[KG] Indexing corpus/by-phase...")
    count = 0
    for f in (HARNESS_DIR / "corpus" / "by-phase").glob("*.md"):
        index_file(conn, f, "corpus")
        count += 1
    print(f"[KG] Indexed {count} files from corpus/by-phase")
    total += count

    # research (always)
    print("[KG] Indexing research/...")
    count = 0
    for f in (HARNESS_DIR / "research").glob("*.md"):
        index_file(conn, f, "research")
        count += 1
    print(f"[KG] Indexed {count} files from research/")
    total += count

    # corpus/pdfs (skip if lite)
    if LITE:
        print("[KG] Skipping corpus/pdfs/ (lite mode)")
    else:
        print("[KG] Indexing corpus/pdfs/...")
        count = 0
        for f in (HARNESS_DIR / "corpus" / "pdfs").glob("*.md"):
            index_file(conn, f, "pdfs")
            count += 1
        print(f"[KG] Indexed {count} files from corpus/pdfs/")
        total += count

    # other knowledge files
    print("[KG] Indexing other knowledge files...")
    count = 0
    for ext in ["*.md", "*.txt"]:
        for f in (HARNESS_DIR / "knowledge").glob(ext):
            if f.name == "swebok.db":
                continue
            index_file(conn, f, "knowledge")
            count += 1
    print(f"[KG] Indexed {count} other files")
    total += count

    conn.commit()
    conn.close()

    print(f"\n[KG] Knowledge graph ready at {DB_PATH}")
    cursor = sqlite3.connect(str(DB_PATH)).execute("SELECT COUNT(*) FROM swebok_fts")
    print(f"[KG] Total entries: {cursor.fetchone()[0]}")

if __name__ == "__main__":
    main()