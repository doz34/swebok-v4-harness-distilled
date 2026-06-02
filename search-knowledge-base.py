#!/usr/bin/env python3
"""
Search Knowledge Base — SWEBOK v4 Harness
Semantic search across knowledge base.

Inputs:  query
Outputs: relevant SWEBOK sections + corpus files + skill recommendations
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import argparse
from difflib import SequenceMatcher

# Configuration paths
HARNESS_DIR = Path(__file__).parent.parent
KNOWLEDGE_DIR = HARNESS_DIR / "knowledge"
INDEX_DIR = KNOWLEDGE_DIR / "indexes"
CONFIG_DIR = HARNESS_DIR / "config"
SKILLS_DIR = HARNESS_DIR / "skills"

DEFAULT_KEYWORD_INDEX = INDEX_DIR / "keyword-index.json"
DEFAULT_KA_INDEX = INDEX_DIR / "ka-index.json"
DEFAULT_TOPIC_INDEX = INDEX_DIR / "topic-index.json"
# I11: deprecated .yaml registry paths retained as empty defaults so the
# CLI --skills-registry flag remains a no-op (no external file read).
DEFAULT_SKILLS_REGISTRY = ""
DEFAULT_INTENT_MAP = ""


@dataclass
class SearchResult:
    """A single search result."""
    file_path: str
    file_name: str
    relevance_score: float
    matched_keywords: List[str]
    ka: Optional[int]
    section_title: str
    preview: str
    result_type: str  # 'swebok', 'corpus', 'skill'


@dataclass
class SearchResponse:
    """Complete search response with results and metadata."""
    query: str
    total_results: int
    swebok_results: List[SearchResult]
    corpus_results: List[SearchResult]
    skill_recommendations: List[Dict]
    ka_coverage: Dict[int, int]
    execution_time_ms: float


class KnowledgeBaseSearcher:
    """Semantic search across the SWEBOK knowledge base."""

    def __init__(self,
                 keyword_index_path: str = str(DEFAULT_KEYWORD_INDEX),
                 ka_index_path: str = str(DEFAULT_KA_INDEX),
                 topic_index_path: str = str(DEFAULT_TOPIC_INDEX),
                 skills_registry_path: str = str(DEFAULT_SKILLS_REGISTRY),
                 intent_map_path: str = str(DEFAULT_INTENT_MAP)):
        """Initialize the knowledge base searcher."""
        self.keyword_index_path = Path(keyword_index_path)
        self.ka_index_path = Path(ka_index_path)
        self.topic_index_path = Path(topic_index_path)
        self.skills_registry_path = Path(skills_registry_path)
        self.intent_map_path = Path(intent_map_path)

        self._load_indexes()
        self._load_configs()

    def _load_indexes(self):
        """Load all index files."""
        # Keyword index
        if self.keyword_index_path.exists():
            with open(self.keyword_index_path) as f:
                data = json.load(f)
                # Handle both old format (flat dict) and new format (with keyword_index key)
                if isinstance(data, dict) and "keyword_index" in data:
                    self.keyword_index = data.get("keyword_index", {})
                    self.file_metadata = data.get("files", {})
                else:
                    # Old format: keyword -> [files] directly
                    self.keyword_index = data
                    self.file_metadata = {}
        else:
            self.keyword_index = {}
            self.file_metadata = {}

        # KA index
        if self.ka_index_path.exists():
            with open(self.ka_index_path) as f:
                self.ka_index = json.load(f)
        else:
            self.ka_index = {}

        # Topic index
        if self.topic_index_path.exists():
            with open(self.topic_index_path) as f:
                self.topic_index = json.load(f)
        else:
            self.topic_index = {}

    def _load_configs(self):
        """Load configuration for skills and intents.

        I11: hardcoded Python defaults. The .yaml configs are deprecated;
        the canonical config lives in `.swebok_state.db` via state_engine.
        Skills/intents are kept here as in-script constants for the
        knowledge-base search to remain functional without an external
        registry file.
        """
        # Skills registry: hardcoded default (no external yaml file).
        self.skills_registry = {"skills": []}

        # Intent map: hardcoded default. The script never reads
        # self.intents at search time, but we keep the attribute so any
        # future caller can introspect it.
        self.intent_map = {"intents": {}}
        self.intents = {}

    def _tokenize(self, text: str) -> set:
        """Tokenize text into normalized words."""
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        return set(w for w in words if len(w) > 2)

    def _compute_similarity(self, text1: str, text2: str) -> float:
        """Compute similarity between two texts."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _compute_keyword_score(self, query_tokens: set, file_path: str) -> Tuple[float, List[str]]:
        """Compute keyword match score for a file."""
        if file_path not in self.file_metadata:
            return 0.0, []

        metadata = self.file_metadata[file_path]
        file_keywords = set(metadata.get("keywords", []))
        matched = list(query_tokens & file_keywords)

        if not matched:
            return 0.0, []

        # Score based on match ratio
        score = len(matched) / max(len(query_tokens), 1)
        return min(score, 1.0), matched

    def _search_keyword_index(self, query: str, max_results: int = 20) -> List[SearchResult]:
        """Search using keyword index."""
        query_tokens = self._tokenize(query)
        results = []

        # Track which files have been scored
        file_scores = defaultdict(lambda: {"score": 0.0, "matched": set(), "keywords": []})

        # Check each keyword in query
        for token in query_tokens:
            # Exact match in keyword index
            if token in self.keyword_index:
                for file_path in self.keyword_index[token]:
                    file_scores[file_path]["score"] += 1.0
                    file_scores[file_path]["matched"].add(token)
                    file_scores[file_path]["keywords"].append(token)

            # Fuzzy match in keyword index
            for keyword, files in self.keyword_index.items():
                if token in keyword or keyword in token:
                    for file_path in files:
                        file_scores[file_path]["score"] += 0.5
                        file_scores[file_path]["matched"].add(keyword)
                        file_scores[file_path]["keywords"].append(keyword)

        # Convert to SearchResults
        for file_path, data in file_scores.items():
            score = data["score"]
            matched = list(data["matched"])

            # Get metadata
            metadata = self.file_metadata.get(file_path, {})
            preview = metadata.get("preview", "")[:200]

            # Determine result type
            if "swebok-sections" in file_path:
                result_type = "swebok"
            elif "corpus" in file_path:
                result_type = "corpus"
            else:
                result_type = "corpus"

            # Extract section title from filename
            filename = Path(file_path).name
            section_title = self._extract_title_from_filename(filename)

            results.append(SearchResult(
                file_path=file_path,
                file_name=filename,
                relevance_score=score,
                matched_keywords=matched[:10],
                ka=metadata.get("ka"),
                section_title=section_title,
                preview=preview,
                result_type=result_type
            ))

        # Sort by score and limit
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:max_results]

    def _search_topic_index(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search using topic index."""
        query_tokens = self._tokenize(query)
        results = []

        topic_scores = defaultdict(lambda: {"score": 0.0, "topics": []})

        def extract_files_from_topic(topic_data):
            """Recursively extract files from topic structure."""
            if isinstance(topic_data, list):
                return topic_data
            elif isinstance(topic_data, dict):
                files = []
                if "subtopics" in topic_data:
                    for subtopic_data in topic_data["subtopics"].values():
                        files.extend(extract_files_from_topic(subtopic_data))
                elif "files" in topic_data:
                    files.extend(topic_data["files"])
                return files
            return []

        for token in query_tokens:
            # Exact match
            if token in self.topic_index:
                files = extract_files_from_topic(self.topic_index[token])
                for file_path in files:
                    topic_scores[file_path]["score"] += 1.0
                    topic_scores[file_path]["topics"].append(token)

            # Fuzzy match - search through topic hierarchy
            for topic_name, topic_data in self.topic_index.items():
                if token in topic_name:
                    files = extract_files_from_topic(topic_data)
                    for file_path in files:
                        topic_scores[file_path]["score"] += 0.5
                        topic_scores[file_path]["topics"].append(topic_name)

        for file_path, data in topic_scores.items():
            filename = Path(file_path).name
            metadata = self.file_metadata.get(file_path, {})

            results.append(SearchResult(
                file_path=file_path,
                file_name=filename,
                relevance_score=data["score"],
                matched_keywords=data["topics"][:10],
                ka=metadata.get("ka") if isinstance(metadata, dict) else None,
                section_title=self._extract_title_from_filename(filename),
                preview=metadata.get("preview", "")[:200] if isinstance(metadata, dict) else "",
                result_type="swebok" if "swebok" in file_path else "corpus"
            ))

        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:max_results]

    def _extract_title_from_filename(self, filename: str) -> str:
        """Extract a readable title from filename."""
        # Remove extension
        title = Path(filename).stem
        # Replace separators with spaces
        title = re.sub(r'[-_]+', ' ', title)
        # Remove hashes
        title = re.sub(r'^[a-f0-9]{32,}\s*', '', title)
        # Capitalize
        title = ' '.join(w.capitalize() for w in title.split())
        return title or filename

    def _get_skill_recommendations(self, query: str, max_results: int = 5) -> List[Dict]:
        """Get skill recommendations based on query."""
        query_tokens = self._tokenize(query)
        skills = self.skills_registry.get("skills", [])
        recommendations = []

        for skill in skills:
            skill_id = skill.get("id", "")
            skill_name = skill.get("name", "")
            skill_desc = skill.get("description", "")
            skill_ka = skill.get("ka")
            triggers = skill.get("triggers", [])

            score = 0.0
            matched = []

            # Check triggers
            for trigger in triggers:
                trigger_tokens = self._tokenize(trigger)
                overlap = len(query_tokens & trigger_tokens)
                if overlap > 0:
                    score += overlap
                    matched.append(trigger)

            # Check description
            desc_tokens = self._tokenize(skill_desc)
            overlap = len(query_tokens & desc_tokens)
            if overlap > 0:
                score += overlap * 0.5
                matched.extend(list(query_tokens & desc_tokens)[:3])

            # Check ID/name
            name_tokens = self._tokenize(skill_id + " " + skill_name)
            overlap = len(query_tokens & name_tokens)
            if overlap > 0:
                score += overlap * 0.8

            if score > 0:
                recommendations.append({
                    "skill_id": skill_id,
                    "skill_name": skill_name,
                    "description": skill_desc[:100] + "..." if len(skill_desc) > 100 else skill_desc,
                    "ka": skill_ka,
                    "relevance_score": score,
                    "matched_criteria": matched[:5]
                })

        # Sort and limit
        recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
        return recommendations[:max_results]

    def _get_ka_coverage(self, results: List[SearchResult]) -> Dict[int, int]:
        """Calculate KA coverage from results."""
        ka_counts = defaultdict(int)
        for result in results:
            if result.ka:
                ka_counts[result.ka] += 1
        return dict(ka_counts)

    def search(self, query: str, max_results: int = 20) -> SearchResponse:
        """
        Main search function.

        Args:
            query: Search query string
            max_results: Maximum number of results per category

        Returns:
            SearchResponse with results and metadata
        """
        import time
        start_time = time.time()

        # Search keyword index
        keyword_results = self._search_keyword_index(query, max_results)

        # Search topic index
        topic_results = self._search_topic_index(query, max_results // 2)

        # Merge and deduplicate results
        all_results = keyword_results + topic_results
        seen_paths = set()
        merged_results = []
        for result in all_results:
            if result.file_path not in seen_paths:
                seen_paths.add(result.file_path)
                merged_results.append(result)

        # Separate by type
        swebok_results = [r for r in merged_results if r.result_type == "swebok"]
        corpus_results = [r for r in merged_results if r.result_type == "corpus"]

        # Get skill recommendations
        skill_recommendations = self._get_skill_recommendations(query)

        # Calculate KA coverage
        ka_coverage = self._get_ka_coverage(merged_results)

        execution_time = (time.time() - start_time) * 1000

        return SearchResponse(
            query=query,
            total_results=len(merged_results),
            swebok_results=swebok_results[:max_results],
            corpus_results=corpus_results[:max_results],
            skill_recommendations=skill_recommendations,
            ka_coverage=ka_coverage,
            execution_time_ms=execution_time
        )

    def search_by_ka(self, ka: int, max_results: int = 10) -> List[SearchResult]:
        """Search all content related to a specific Knowledge Area."""
        results = []

        if str(ka) in self.ka_index:
            for file_path in self.ka_index[str(ka)]:
                metadata = self.file_metadata.get(file_path, {})
                results.append(SearchResult(
                    file_path=file_path,
                    file_name=Path(file_path).name,
                    relevance_score=1.0,
                    matched_keywords=[],
                    ka=ka,
                    section_title=self._extract_title_from_filename(Path(file_path).name),
                    preview=metadata.get("preview", "")[:200] if metadata else "",
                    result_type="swebok" if "swebok" in file_path else "corpus"
                ))

        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:max_results]


def format_results_text(response: SearchResponse, verbose: bool = False) -> str:
    """Format search results as readable text."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"Knowledge Base Search: \"{response.query}\"")
    lines.append("=" * 70)
    lines.append(f"Found {response.total_results} results in {response.execution_time_ms:.1f}ms")
    lines.append("")

    # KA Coverage
    if response.ka_coverage:
        lines.append("Knowledge Areas Covered:")
        for ka, count in sorted(response.ka_coverage.items()):
            lines.append(f"  KA{ka}: {count} sections")
        lines.append("")

    # Skill Recommendations
    if response.skill_recommendations:
        lines.append("Recommended Skills:")
        for skill in response.skill_recommendations[:5]:
            lines.append(f"  - {skill['skill_name']} (score: {skill['relevance_score']:.1f})")
            if verbose and skill.get('matched_criteria'):
                for crit in skill['matched_criteria'][:3]:
                    lines.append(f"      matched: {crit}")
        lines.append("")

    # SWEBOK Results
    if response.swebok_results:
        lines.append("SWEBOK v4 Sections:")
        for i, result in enumerate(response.swebok_results[:10], 1):
            lines.append(f"  {i}. {result.section_title}")
            lines.append(f"     File: {result.file_name}")
            if result.ka:
                lines.append(f"     KA: {result.ka}")
            lines.append(f"     Relevance: {result.relevance_score:.2f}")
            if result.matched_keywords:
                lines.append(f"     Keywords: {', '.join(result.matched_keywords[:5])}")
            if verbose and result.preview:
                lines.append(f"     Preview: {result.preview[:100]}...")
            lines.append("")

    # Corpus Results
    if response.corpus_results:
        lines.append("Corpus Files:")
        for i, result in enumerate(response.corpus_results[:10], 1):
            lines.append(f"  {i}. {result.section_title}")
            lines.append(f"     File: {result.file_name}")
            lines.append(f"     Relevance: {result.relevance_score:.2f}")
            if result.matched_keywords:
                lines.append(f"     Keywords: {', '.join(result.matched_keywords[:5])}")
            lines.append("")

    return "\n".join(lines)


def format_results_json(response: SearchResponse) -> str:
    """Format search results as JSON."""
    def serialize_result(r: SearchResult) -> Dict:
        return {
            "file_path": r.file_path,
            "file_name": r.file_name,
            "relevance_score": r.relevance_score,
            "matched_keywords": r.matched_keywords,
            "ka": r.ka,
            "section_title": r.section_title,
            "preview": r.preview[:200] if r.preview else "",
            "result_type": r.result_type
        }

    return json.dumps({
        "query": response.query,
        "total_results": response.total_results,
        "execution_time_ms": response.execution_time_ms,
        "ka_coverage": response.ka_coverage,
        "skill_recommendations": response.skill_recommendations,
        "swebok_results": [serialize_result(r) for r in response.swebok_results],
        "corpus_results": [serialize_result(r) for r in response.corpus_results]
    }, indent=2)


def main():
    """CLI interface for knowledge base search."""
    parser = argparse.ArgumentParser(
        description="Search Knowledge Base — Semantic search across SWEBOK knowledge"
    )
    parser.add_argument("query", nargs="*", help="Search query")
    parser.add_argument("--keyword-index", default=str(DEFAULT_KEYWORD_INDEX),
                       help="Path to keyword index")
    parser.add_argument("--ka-index", default=str(DEFAULT_KA_INDEX),
                       help="Path to KA index")
    parser.add_argument("--topic-index", default=str(DEFAULT_TOPIC_INDEX),
                       help="Path to topic index")
    parser.add_argument("--skills-registry", default=str(DEFAULT_SKILLS_REGISTRY),
                       help="Path to skills registry")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--max-results", type=int, default=20,
                       help="Maximum results per category")
    parser.add_argument("--ka", type=int, help="Filter by Knowledge Area (1-15)")

    args = parser.parse_args()

    # Check if indexes exist
    if not Path(args.keyword_index).exists():
        print(f"Error: Keyword index not found at {args.keyword_index}")
        print("Run generate-keyword-index.py first to create the index.")
        return 1

    # Build searcher
    searcher = KnowledgeBaseSearcher(
        keyword_index_path=args.keyword_index,
        ka_index_path=args.ka_index,
        topic_index_path=args.topic_index,
        skills_registry_path=args.skills_registry
    )

    # Handle KA-only query
    if args.ka:
        if not (1 <= args.ka <= 15):
            print("Error: KA must be between 1 and 15")
            return 1
        results = searcher.search_by_ka(args.ka, max_results=args.max_results)
        print(f"Found {len(results)} sections for KA{args.ka}:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.section_title}")
            print(f"     {result.file_path}")
        return 0

    # Regular query
    if not args.query:
        print("Error: query required (or use --ka to browse by Knowledge Area)")
        parser.print_help()
        return 1

    query = " ".join(args.query)
    response = searcher.search(query, max_results=args.max_results)

    if args.json:
        print(format_results_json(response))
    else:
        print(format_results_text(response, verbose=args.verbose))

    return 0


if __name__ == "__main__":
    exit(main())
