#!/usr/bin/env python3
"""
*** EXPERIMENTAL_v2 - OPT-IN ONLY. NOT CONSUMED BY COMPILED_KNOWLEDGE.PY. ***
SWEBOK v4 Harness V2 — Hierarchical Tree
========================================

Builds a book > chapter > section > paragraph tree from chunks.
Pure Python, no LLM. Enables hierarchical search (top-down) and
summarization (bottom-up).

Usage:
    from retrieval.hierarchy import Hierarchy
    tree = Hierarchy()
    tree.build(chunks)
    # Find all chunks in "Head First Design Patterns" > "Chapter 4"
    sub = tree.find_under("Head First Design Patterns", "Factory Pattern")
"""

import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.chunker import Chunk


@dataclass
class TreeNode:
    """A node in the book/chapter/section tree."""
    name: str
    level: int  # 0=book, 1=chapter, 2=section, 3=subsection
    parent: str = ""  # path of parent
    children: List[str] = field(default_factory=list)  # child node names
    chunk_ids: Set[str] = field(default_factory=set)
    chunk_count: int = 0
    total_chars: int = 0

    @property
    def full_path(self) -> str:
        return f"{self.parent} > {self.name}" if self.parent else self.name


class Hierarchy:
    """Book > chapter > section tree over chunks."""

    def __init__(self):
        self.books: Dict[str, TreeNode] = {}
        self.chapters: Dict[str, TreeNode] = {}  # key: book > chapter
        self.sections: Dict[str, TreeNode] = {}  # key: book > chapter > section

    def _book_key(self, chunk: Chunk) -> str:
        return chunk.book

    def _chapter_key(self, chunk: Chunk) -> str:
        return f"{chunk.book} > {chunk.chapter}" if chunk.chapter else f"{chunk.book}"

    def _section_key(self, chunk: Chunk) -> str:
        if not chunk.section_path:
            return self._chapter_key(chunk)
        return f"{chunk.book} > {' > '.join(chunk.section_path)}"

    def build(self, chunks: List[Chunk]) -> None:
        """Build the tree from chunks."""
        for chunk in chunks:
            book_key = self._book_key(chunk)
            chapter_key = self._chapter_key(chunk)
            section_key = self._section_key(chunk)
            # Book
            if book_key not in self.books:
                self.books[book_key] = TreeNode(name=book_key, level=0)
            book = self.books[book_key]
            book.chunk_ids.add(chunk.id)
            book.chunk_count += 1
            book.total_chars += chunk.char_count
            # Chapter
            if chapter_key not in self.chapters:
                self.chapters[chapter_key] = TreeNode(
                    name=chunk.chapter or "(no chapter)",
                    level=1,
                    parent=book_key,
                )
                book.children.append(chapter_key)
            chapter = self.chapters[chapter_key]
            chapter.chunk_ids.add(chunk.id)
            chapter.chunk_count += 1
            chapter.total_chars += chunk.char_count
            # Section (if different from chapter)
            if section_key != chapter_key:
                if section_key not in self.sections:
                    self.sections[section_key] = TreeNode(
                        name=" > ".join(chunk.section_path[1:]) if len(chunk.section_path) > 1 else "(section)",
                        level=min(2 + len(chunk.section_path) - 2, 3),
                        parent=chapter_key,
                    )
                    chapter.children.append(section_key)
                section = self.sections[section_key]
                section.chunk_ids.add(chunk.id)
                section.chunk_count += 1
                section.total_chars += chunk.char_count

    def find_under(self, *path_parts: str) -> Set[str]:
        """Find all chunk IDs under a path. Path parts: book, chapter, section."""
        if not path_parts:
            return set()
        if len(path_parts) == 1:
            return self.books.get(path_parts[0], TreeNode("?", -1)).chunk_ids
        if len(path_parts) == 2:
            return self.chapters.get(f"{path_parts[0]} > {path_parts[1]}", TreeNode("?", -1)).chunk_ids
        return self.sections.get(f"{path_parts[0]} > {' > '.join(path_parts[1:])}", TreeNode("?", -1)).chunk_ids

    def find_books(self) -> List[str]:
        return sorted(self.books.keys())

    def find_chapters(self, book: str) -> List[str]:
        return [c for c in self.chapters.keys() if c.startswith(f"{book} > ")]

    def search_by_path_substring(self, substring: str) -> List[TreeNode]:
        """Find any node whose path contains the substring (case-insensitive)."""
        sub = substring.lower()
        results = []
        for path, node in {**self.books, **self.chapters, **self.sections}.items():
            if sub in path.lower():
                results.append(node)
        return sorted(results, key=lambda n: -n.chunk_count)

    def get_chunks_in_node(self, path: str, all_chunks: List[Chunk]) -> List[Chunk]:
        """Get all chunks under a node path, given the chunk list."""
        if path in self.books:
            ids = self.books[path].chunk_ids
        elif path in self.chapters:
            ids = self.chapters[path].chunk_ids
        elif path in self.sections:
            ids = self.sections[path].chunk_ids
        else:
            return []
        return [c for c in all_chunks if c.id in ids]

    def stats(self) -> dict:
        return {
            "n_books": len(self.books),
            "n_chapters": len(self.chapters),
            "n_sections": len(self.sections),
            "top_books_by_chunks": sorted(
                [(b.name, b.chunk_count) for b in self.books.values()],
                key=lambda x: -x[1]
            )[:10],
        }


# === CLI ===
if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Build a hierarchy from chunks JSONL")
    parser.add_argument("chunks_jsonl")
    parser.add_argument("query", nargs="?", help="Path substring to search (default: stats)")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()
    chunks = []
    with open(args.chunks_jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(Chunk(**json.loads(line)))
    h = Hierarchy()
    h.build(chunks)
    print("Stats:", json.dumps(h.stats(), indent=2)[:2000])
    if args.query:
        print(f"\nPath substring '{args.query}':")
        for node in h.search_by_path_substring(args.query)[:args.top_k]:
            print(f"  [{node.level}] {node.full_path} ({node.chunk_count} chunks, {node.total_chars} chars)")
