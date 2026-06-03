#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Knowledge Graph Extractor
================================================

Builds a navigable graph from chunks WITHOUT requiring an LLM.
Heuristics:
- Entities: capitalized noun phrases, technical terms
- Relations: co-occurrence in the same chunk
- Claims: sentence patterns (subject predicate object)
- Communities: simple connected-component analysis

This is a LIGHTER version of GraphRAG. For the full GraphRAG with
LLM-based claim extraction, swap in a claim_extractor using a Provider.

Usage:
    from retrieval.graph import KnowledgeGraph
    kg = KnowledgeGraph()
    kg.build(chunks)
    neighbors = kg.neighbors("SOLID")
    path = kg.shortest_path("architecture", "testing")
"""

import math
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.chunker import Chunk

# Common technical terms that should be recognized as entities even in lowercase
# (heuristics: these are common in software engineering literature)
_TECH_VOCAB = set("""
api rest graphql grpc sql nosql postgres mysql mongodb redis sqlite
python javascript typescript rust go java kotlin swift ruby php
react vue angular svelte solid html css dom
docker kubernetes k8s helm terraform ansible chef puppet
aws gcp azure vercel netlify heroku cloudflare
git github gitlab bitbucket
junit pytest mocha jest cypress playwright
tdd bdd ddd ci cd devops
http https tcp udp dns ssh tls ssl oauth jwt saml
mvc mvvm mvp hexagonal layered event cqrs saga
orm jdbc jpa hibernate sqlalchemy
kafka rabbitmq nats zeromq pulsar
tdd bdd
""".split())

# Sentence patterns that look like claims
_CLAIM_PATTERNS = [
    re.compile(r"\b([A-Z][A-Za-z0-9_\-]{2,}(?:\s+[A-Z][A-Za-z0-9_\-]+){0,3})\s+(is|are|means|refers to|denotes|equals|provides|enables|requires|uses|supports|contains|extends|implements|inherits|overrides|delegates to|depends on|builds on|contrasts with|differs from)\s+([a-z][^.!?\n]{3,80})", re.MULTILINE),
    re.compile(r"\b([A-Z][A-Za-z0-9_\-]{2,})\s+(is|are)\s+(a|an|the)?\s*([a-z][a-z\s\-]{2,40})", re.MULTILINE),
]


@dataclass
class Entity:
    """A node in the knowledge graph."""
    name: str
    type: str  # "PERSON", "CONCEPT", "TECH", "PATTERN", "TOOL", "BOOK"
    chunk_ids: Set[str] = field(default_factory=set)
    frequency: int = 0  # how many chunks mention this entity

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Entity) and self.name == other.name


@dataclass
class Relation:
    """An edge in the knowledge graph."""
    source: str
    target: str
    relation_type: str  # "co-occurs", "is-a", "uses", "depends-on", etc.
    weight: float = 1.0
    evidence_count: int = 1  # how many chunks support this

    def __hash__(self):
        return hash((self.source, self.target, self.relation_type))


@dataclass
class Claim:
    """An extracted claim (subject predicate object)."""
    subject: str
    predicate: str
    object: str
    chunk_id: str
    confidence: float = 0.5


class KnowledgeGraph:
    """Lightweight knowledge graph from chunks. No LLM required."""

    # Stopword-ish words to filter from entity candidates
    ENTITY_STOPWORDS = set("""
    the a an and or but if else for on at to from by with as is are was were be been being
    this that these those it its their there here what when where why how
    chapter section page figure table example note warning tip
    see also references bibliography index appendix
    you your we our they them their
    one two three four five six seven eight nine ten first second third
    """.split())

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self.claims: List[Claim] = []
        # Index: chunk_id -> set of entity names
        self.chunk_entities: Dict[str, Set[str]] = defaultdict(set)
        # Adjacency for fast traversal
        self.adjacency: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        # Claim text cache for display
        self._chunk_text_cache: Dict[str, str] = {}

    def build(self, chunks: List[Chunk]) -> None:
        """Build the graph from chunks."""
        # Phase 1: extract entities per chunk
        for chunk in chunks:
            self._chunk_text_cache[chunk.id] = chunk.text
            entities = self._extract_entities(chunk.text)
            for entity_name, entity_type in entities:
                if entity_name not in self.entities:
                    self.entities[entity_name] = Entity(name=entity_name, type=entity_type)
                self.entities[entity_name].chunk_ids.add(chunk.id)
                self.entities[entity_name].frequency += 1
                self.chunk_entities[chunk.id].add(entity_name)
            # Phase 2: extract claims
            for claim in self._extract_claims(chunk.text, chunk.id):
                self.claims.append(claim)
        # Phase 3: build co-occurrence relations
        for chunk_id, entities in self.chunk_entities.items():
            entities_list = list(entities)
            for i in range(len(entities_list)):
                for j in range(i + 1, len(entities_list)):
                    src, tgt = entities_list[i], entities_list[j]
                    self.adjacency[src][tgt] += 1.0
                    self.adjacency[tgt][src] += 1.0
        # Phase 4: normalize adjacency and create Relation objects
        for src, targets in self.adjacency.items():
            for tgt, weight in targets.items():
                if weight >= 1.0:  # only meaningful co-occurrences
                    self.relations.append(Relation(
                        source=src, target=tgt,
                        relation_type="co-occurs",
                        weight=math.log(1 + weight),
                        evidence_count=int(weight),
                    ))

    def _extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """Extract entities from text. Returns (name, type) tuples."""
        entities = []
        # 1. Capitalized noun phrases (1-4 words, all capitalized)
        for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b", text):
            phrase = m.group(1).strip()
            if not self._is_stopword_phrase(phrase):
                # Infer type from context
                entity_type = "CONCEPT"
                if self._looks_like_book(phrase):
                    entity_type = "BOOK"
                elif self._looks_like_pattern(phrase):
                    entity_type = "PATTERN"
                entities.append((phrase, entity_type))
        # 2. Technical vocab (case-insensitive, but normalize)
        text_lower = text.lower()
        for term in _TECH_VOCAB:
            # Word boundary match
            pattern = r"\b" + re.escape(term) + r"\b"
            if re.search(pattern, text_lower):
                # Normalize to canonical form
                canonical = self._canonical_tech(term)
                entities.append((canonical, "TECH"))
        # Deduplicate
        seen = set()
        unique = []
        for name, t in entities:
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append((name, t))
        return unique

    def _is_stopword_phrase(self, phrase: str) -> bool:
        words = phrase.lower().split()
        if not words:
            return True
        if words[0] in self.ENTITY_STOPWORDS:
            return True
        if len(words) == 1 and len(words[0]) <= 3:
            return True
        return False

    def _looks_like_book(self, phrase: str) -> bool:
        indicators = ["Design Patterns", "Clean Code", "Clean Architecture", "Refactoring",
                      "Pragmatic", "Code Complete", "Head First", "Mythical Man-Month",
                      "Modern Software", "Tidy First", "Working Effectively"]
        return any(ind in phrase for ind in indicators)

    def _looks_like_pattern(self, phrase: str) -> bool:
        patterns = ["Pattern", "Architecture", "Strategy", "Factory", "Observer",
                    "Singleton", "Builder", "Adapter", "Decorator"]
        return any(p in phrase for p in patterns)

    def _canonical_tech(self, term: str) -> str:
        """Normalize tech terms to canonical case (e.g., 'sql' -> 'SQL')."""
        upper_terms = {"sql", "api", "rest", "graphql", "grpc", "http", "https", "tcp", "udp",
                       "dns", "ssh", "tls", "ssl", "oauth", "jwt", "saml", "css", "html",
                       "dom", "orm", "mvc", "mvvm", "mvp", "ddd", "tdd", "bdd", "ci", "cd",
                       "aws", "gcp", "k8s", "orm"}
        if term in upper_terms:
            return term.upper()
        # Title-case for multi-word
        return " ".join(w.capitalize() for w in term.split())

    def _extract_claims(self, text: str, chunk_id: str) -> List[Claim]:
        """Extract claims using pattern matching."""
        claims = []
        for pattern in _CLAIM_PATTERNS:
            for m in pattern.finditer(text):
                subj = m.group(1).strip() if m.group(1) else ""
                pred = m.group(2).strip() if m.group(2) else ""
                obj = m.group(3).strip() if m.group(3) else ""
                if not subj or not pred:
                    continue
                if len(subj) > 50 or len(obj) > 100:
                    continue
                if subj.lower() in self.ENTITY_STOPWORDS:
                    continue
                claims.append(Claim(
                    subject=subj, predicate=pred, object=obj,
                    chunk_id=chunk_id, confidence=0.6,
                ))
        return claims

    def neighbors(self, entity_name: str, top_k: int = 10) -> List[Relation]:
        """Get top-k neighbors of an entity, ranked by edge weight."""
        name = entity_name.lower()
        if name not in self.adjacency:
            # Try case-insensitive
            for n in self.adjacency:
                if n.lower() == name:
                    name = n
                    break
        if name not in self.adjacency:
            return []
        nbrs = [(tgt, w) for tgt, w in self.adjacency[name].items()]
        nbrs.sort(key=lambda x: -x[1])
        return [Relation(source=name, target=t, relation_type="co-occurs", weight=w, evidence_count=int(w))
                for t, w in nbrs[:top_k]]

    def shortest_path(self, source: str, target: str, max_depth: int = 4) -> List[str]:
        """BFS shortest path between two entities."""
        source, target = source.lower(), target.lower()
        # Normalize names
        for n in self.adjacency:
            if n.lower() == source:
                source = n
            if n.lower() == target:
                target = n
        if source == target:
            return [source]
        if source not in self.adjacency or target not in self.adjacency:
            return []
        # BFS
        visited = {source}
        queue = [(source, [source])]
        while queue:
            node, path = queue.pop(0)
            if len(path) > max_depth:
                continue
            for nbr in self.adjacency[node]:
                if nbr == target:
                    return path + [nbr]
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, path + [nbr]))
        return []

    def find_community(self, entity_name: str, max_size: int = 20) -> Set[str]:
        """Return the connected component containing this entity (a 'community')."""
        name = entity_name.lower()
        for n in self.adjacency:
            if n.lower() == name:
                name = n
                break
        if name not in self.adjacency:
            return set()
        community = {name}
        frontier = [name]
        while frontier and len(community) < max_size:
            current = frontier.pop()
            for nbr in self.adjacency[current]:
                if nbr not in community:
                    community.add(nbr)
                    frontier.append(nbr)
                    if len(community) >= max_size:
                        break
        return community

    def stats(self) -> dict:
        return {
            "n_entities": len(self.entities),
            "n_relations": len(self.relations),
            "n_claims": len(self.claims),
            "top_entities": sorted(
                [(e.name, e.frequency) for e in self.entities.values()],
                key=lambda x: -x[1]
            )[:10],
        }


# === CLI ===
if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Build a knowledge graph from a chunks JSONL file")
    parser.add_argument("chunks_jsonl", help="JSONL chunks file (from chunker.py)")
    parser.add_argument("query", nargs="?", help="Entity to inspect (default: print stats)")
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()
    chunks = []
    with open(args.chunks_jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(Chunk(**json.loads(line)))
    kg = KnowledgeGraph()
    kg.build(chunks)
    print("Stats:", json.dumps(kg.stats(), indent=2)[:2000])
    if args.query:
        print(f"\nNeighbors of '{args.query}':")
        for r in kg.neighbors(args.query, top_k=args.top_k):
            print(f"  {r.source} -> {r.target} (weight={r.weight:.2f}, evidence={r.evidence_count})")
        print(f"\nCommunity of '{args.query}':")
        for e in sorted(kg.find_community(args.query)):
            print(f"  - {e}")
