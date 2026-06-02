#!/usr/bin/env python3
"""
SWEBOK v4 Harness - RAG Query Tool
Queries knowledge base and returns compressed3-sentence extract
Usage: python3 swebok-query.py <query> [--max-sentences N]
"""

import sys
import json
import sqlite3
from pathlib import Path
from typing import Optional, List

# Configuration
HARNESS_DIR = Path(__file__).parent.parent
DB_PATH = HARNESS_DIR / "knowledge" / "swebok.db"
DEFAULT_MAX_SENTENCES = 3

def init_db() -> None:
    """Initialize SQLite FTS5 database if it doesn't exist."""
    if DB_PATH.exists():
        return

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Create FTS5 virtual table
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS swebok_fts USING fts5(
            content,
            ka,
            phase,
            metadata
        )
    """)

    # Index knowledge files if they exist
    knowledge_dir = HARNESS_DIR / "knowledge"
    if knowledge_dir.exists():
        for md_file in knowledge_dir.rglob("*.md"):
            try:
                content = md_file.read_text()
                ka = extract_ka(md_file)
                phase = extract_phase(md_file)
                cursor.execute(
                    "INSERT INTO swebok_fts (content, ka, phase, metadata) VALUES (?, ?, ?, ?)",
                    (content, ka, phase, str(md_file))
                )
            except Exception as e:
                print(f"[WARN] Could not index {md_file}: {e}", file=sys.stderr)

    conn.commit()
    conn.close()
    print(f"[RAG] Database initialized at {DB_PATH}", file=sys.stderr)

def extract_ka(file_path: Path) -> str:
    """Extract KA from filename or path."""
    name = file_path.name
    if "KA-" in name:
        import re
        match = re.search(r'KA-(\d+)', name)
        if match:
            return match.group(1)
    return "unknown"

def extract_phase(file_path: Path) -> str:
    """Extract phase from path."""
    path_str = str(file_path)
    if "P1" in path_str or "discovery" in path_str.lower():
        return "P1"
    elif "P2" in path_str or "requirement" in path_str.lower():
        return "P2"
    elif "P3" in path_str or "architecture" in path_str.lower():
        return "P3"
    elif "P4" in path_str or "design" in path_str.lower():
        return "P4"
    elif "P5" in path_str or "construction" in path_str.lower():
        return "P5"
    elif "P6" in path_str or "testing" in path_str.lower():
        return "P6"
    elif "P7" in path_str or "deployment" in path_str.lower():
        return "P7"
    elif "P8" in path_str or "operations" in path_str.lower():
        return "P8"
    elif "P9" in path_str or "retirement" in path_str.lower():
        return "P9"
    return "all"

def query_swebok(query: str, max_sentences: int = DEFAULT_MAX_SENTENCES) -> str:
    """
    Query the SWEBOK knowledge base.
    Returns compressed3-sentence extract.
    """
    # Initialize DB if needed
    init_db()

    if not DB_PATH.exists():
        return f"[RAG] DB not found at {DB_PATH}. Run scripts/generate-kg.sh first."

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # FTS5 search
    try:
        cursor.execute("""
            SELECT content, ka, phase, metadata
            FROM swebok_fts
            WHERE swebok_fts MATCH ?
            ORDER BY rank
            LIMIT 1
        """, (query,))

        row = cursor.fetchone()
    except Exception as e:
        conn.close()
        return f"[RAG] Search error: {e}"

    conn.close()

    if not row:
        return f"[RAG] No results for: {query}"

    content, ka, phase, metadata = row

    # Extract first N sentences
    sentences = [s.strip() for s in content.split('.') if s.strip()]
    extracted = '. '.join(sentences[:max_sentences])
    if len(sentences) > max_sentences:
        extracted += '...'

    # Return compressed DSL format
    return f"[KA-{ka} | {phase}] {extracted}"

def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: swebok-query.py <query> [--max-sentences N]", file=sys.stderr)
        print("Example: swebok-query.py 'ISO 25010 maintainability metrics'", file=sys.stderr)
        sys.exit(1)

    query = ' '.join(sys.argv[1:])

    # Check for --max-sentences flag
    max_sentences = DEFAULT_MAX_SENTENCES
    if "--max-sentences" in query:
        parts = query.split("--max-sentences")
        query = parts[0].strip()
        try:
            max_sentences = int(parts[1].strip())
        except ValueError:
            pass

    result = query_swebok(query, max_sentences)
    print(result)

if __name__ == "__main__":
    main()
