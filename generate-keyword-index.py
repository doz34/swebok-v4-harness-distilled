#!/usr/bin/env python3
"""
Generate Keyword Index — SWEBOK v4 Harness
Generates keyword-index.json from corpus files (872 files).

Indexes by: keywords, topics, file references.
Outputs to: knowledge/indexes/
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Optional, Tuple
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

# Configuration
HARNESS_DIR = Path(__file__).parent.parent
CORPUS_DIR = HARNESS_DIR / "corpus"
KNOWLEDGE_DIR = HARNESS_DIR / "knowledge"
INDEX_DIR = KNOWLEDGE_DIR / "indexes"
SWEBOK_SECTIONS_DIR = KNOWLEDGE_DIR / "swebok-sections"

# Ensure index directory exists
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# Stop words to filter out
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
    'that', 'which', 'who', 'whom', 'this', 'these', 'those', 'it', 'its',
    'they', 'them', 'their', 'what', 'where', 'when', 'why', 'how',
    'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there',
    'then', 'once', 'if', 'about', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'between', 'under', 'again', 'further',
    'while', 'because', 'against', 'out', 'up', 'down', 'off', 'over',
    'under', 'again', 'further', 'any', 'our', 'we', 'us', 'i', 'me',
    'my', 'your', 'you', 'he', 'him', 'his', 'she', 'her', 'it', 'its',
    'one', 'two', 'three', 'four', 'five', 'first', 'second', 'third',
    'new', 'old', 'good', 'bad', 'high', 'low', 'big', 'small', 'large',
    'long', 'short', 'great', 'little', 'own', 'other', 'same', 'well',
    'even', 'back', 'still', 'way', 'well', 'use', 'used', 'using', 'make',
    'made', 'many', 'much', 'often', 'however', 'although', 'though',
    'since', 'while', 'whether', 'either', 'neither', 'ever', 'never',
    'always', 'usually', 'sometimes', 'often', 'rarely', 'seldom'
}

# SWEBOK-specific domain terms to boost
DOMAIN_TERMS = {
    # KA1: Requirements
    'requirement', 'elicitation', 'stakeholder', 'user-story', 'use-case',
    'acceptance-criteria', 'functional', 'non-functional', 'traceability',
    # KA2: Architecture
    'architecture', 'architectural', 'pattern', 'microservice', 'monolith',
    'layered', 'component', 'connector', 'interface', 'boundary',
    # KA3: Design
    'design', 'class', 'module', 'solid', 'cohesion', 'coupling',
    'encapsulation', 'polymorphism', 'inheritance', 'abstraction',
    # KA4: Construction
    'construction', 'coding', 'implementation', 'api', 'endpoint',
    'refactoring', 'technical-debt', 'code-smell', 'clean-code',
    # KA5: Testing
    'testing', 'unit-test', 'integration-test', 'e2e', 'test-case',
    'coverage', 'tdd', 'bdd', 'mutation-testing', 'exploratory',
    # KA6-15: Other KAs
    'maintenance', 'configuration', 'management', 'process', 'quality',
    'safety', 'security', 'system', 'foundation', 'algorithm'
}


def normalize_keyword(word: str) -> str:
    """Normalize a keyword for indexing."""
    # Lowercase
    word = word.lower()
    # Replace separators with hyphens for compound terms
    word = re.sub(r'[-\s]+', '-', word)
    # Remove remaining punctuation except hyphens
    word = re.sub(r'[^\w-]', '', word)
    return word


def is_significant_keyword(word: str, min_length: int = 3) -> bool:
    """Check if a word is a significant keyword."""
    if len(word) < min_length:
        return False
    if word in STOP_WORDS:
        return False
    if word.isdigit():
        return False
    return True


def extract_keywords_from_text(text: str, max_keywords: int = 50) -> Set[str]:
    """Extract significant keywords from text."""
    # Find hyphenated compound terms first
    compounds = re.findall(r'\b[a-z]+(?:-[a-z]+){1,4}\b', text.lower())
    keywords = set(normalize_keyword(c) for c in compounds)

    # Split into words
    words = re.findall(r'\b[a-z]+\b', text.lower())

    for word in words:
        normalized = normalize_keyword(word)
        if is_significant_keyword(normalized):
            keywords.add(normalized)

    # Boost domain terms
    for term in DOMAIN_TERMS:
        if term in keywords:
            # Add the term multiple times to boost its score
            keywords.add(term)

    return set(list(keywords)[:max_keywords])


def extract_topics_from_filename(filename: str) -> List[str]:
    """Extract topics from filename."""
    # Remove extension
    name = Path(filename).stem
    # Split on separators
    parts = re.split(r'[-_]', name)
    # Filter and normalize
    topics = []
    for part in parts:
        part = part.lower().strip()
        if len(part) > 2 and not part.isdigit():
            topics.append(part)
    return topics


def extract_ka_from_content(content: str, filename: str) -> Optional[int]:
    """Extract Knowledge Area from content or filename."""
    # Check for chapter indicators
    chapter_match = re.search(r'CHAPTER\s*(\d+)', content[:1000])
    if chapter_match:
        ka = int(chapter_match.group(1))
        if 1 <= ka <= 15:
            return ka

    # Check filename for KA indicators
    ka_patterns = [
        (r'ka[_\-]?(\d+)', lambda m: int(m.group(1))),
        (r'(?:^|_)(\d{2})(?:_|\.)', lambda m: int(m.group(1)) if 1 <= int(m.group(1)) <= 15 else None),
    ]

    for pattern, extractor in ka_patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            result = extractor(match)
            if result:
                return result

    # Infer from keywords
    content_lower = content.lower()
    ka_keywords = {
        1: ['requirement', 'stakeholder', 'elicitation'],
        2: ['architecture', 'architectural'],
        3: ['design', 'class', 'module'],
        4: ['construction', 'coding', 'api'],
        5: ['testing', 'test case'],
        6: ['maintenance'],
        7: ['configuration', 'version control'],
        8: ['management', 'project'],
        9: ['process', 'ci/cd', 'devops'],
        10: ['methodology', 'agile', 'scrum'],
        11: ['quality', 'quality assurance'],
        12: ['safety', 'hazard'],
        13: ['security', 'vulnerability'],
        14: ['system', 'embedded'],
        15: ['algorithm', 'foundation'],
    }

    scores = {}
    for ka, keywords in ka_keywords.items():
        score = sum(1 for kw in keywords if kw in content_lower)
        if score > 0:
            scores[ka] = score

    if scores:
        return max(scores, key=scores.get)

    return None


def extract_file_metadata(filepath: Path) -> Dict:
    """Extract metadata from a file."""
    try:
        content = filepath.read_text(errors='ignore')
    except (OSError, UnicodeDecodeError):
        return {}

    filename = filepath.name
    topics = extract_topics_from_filename(filename)
    ka = extract_ka_from_content(content, filename)
    keywords = extract_keywords_from_text(content)

    return {
        "filename": filename,
        "path": str(filepath),
        "ka": ka,
        "topics": topics,
        "keywords": list(keywords),
        "size": filepath.stat().st_size,
        "preview": content[:200].strip() if content else ""
    }


def process_file(filepath: Path) -> Tuple[str, Dict]:
    """Process a single file and return its indexed content."""
    metadata = extract_file_metadata(filepath)
    return str(filepath), metadata


def generate_keyword_index(files: List[Path], verbose: bool = False) -> Dict:
    """
    Generate keyword index from corpus files.

    Returns a dict mapping keywords to list of files containing them.
    """
    keyword_map = defaultdict(list)
    file_metadata = {}

    if verbose:
        print(f"Processing {len(files)} files...")

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        futures = {executor.submit(process_file, f): f for f in files}

        for i, future in enumerate(as_completed(futures)):
            filepath, metadata = future.result()
            file_metadata[filepath] = metadata

            # Add to keyword index
            for keyword in metadata.get("keywords", []):
                keyword_map[keyword].append(filepath)

            if verbose and (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(files)} files")

    # Convert to regular dict and sort
    result = {
        "keyword_index": dict(keyword_map),
        "file_count": len(files),
        "unique_keywords": len(keyword_map),
        "files": file_metadata
    }

    return result


def generate_ka_index(files: List[Path], verbose: bool = False) -> Dict:
    """Generate KA (Knowledge Area) index."""
    ka_map = defaultdict(list)

    for f in files:
        try:
            content = f.read_text(errors='ignore')[:1000]
        except (OSError, UnicodeDecodeError):
            continue

        ka = extract_ka_from_content(content, f.name)
        if ka:
            ka_map[ka].append(str(f))

    return dict(ka_map)


def generate_topic_index(files: List[Path], verbose: bool = False) -> Dict:
    """Generate topic index."""
    topic_map = defaultdict(list)

    for f in files:
        topics = extract_topics_from_filename(f.name)
        for topic in topics:
            topic_map[topic].append(str(f))

    return dict(topic_map)


def generate_corpus_file_index(base_dir: Path, extensions: List[str] = ['.md', '.txt', '.pdf']) -> List[Path]:
    """Find all corpus files to index."""
    files = []
    for ext in extensions:
        files.extend(base_dir.rglob(f'*{ext}'))
    return files


def main():
    """CLI interface for keyword index generation."""
    parser = argparse.ArgumentParser(
        description="Generate Keyword Index — Index corpus files for semantic search"
    )
    parser.add_argument("--corpus-dir", type=str, default=str(CORPUS_DIR),
                       help="Corpus directory to index")
    parser.add_argument("--output-dir", type=str, default=str(INDEX_DIR),
                       help="Output directory for indexes")
    parser.add_argument("--swebok-sections", type=str, default=str(SWEBOK_SECTIONS_DIR),
                       help="SWEBOK sections directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--rebuild", action="store_true",
                       help="Force rebuild of existing index")
    parser.add_argument("--workers", type=int, default=0,
                       help="Number of worker threads (0=auto)")

    args = parser.parse_args()

    corpus_dir = Path(args.corpus_dir)
    output_dir = Path(args.output_dir)
    swebok_dir = Path(args.swebok_sections)

    output_dir.mkdir(parents=True, exist_ok=True)

    keyword_index_path = output_dir / "keyword-index.json"
    ka_index_path = output_dir / "ka-index.json"
    topic_index_path = output_dir / "topic-index.json"

    # Check if rebuild needed
    if not args.rebuild and keyword_index_path.exists():
        existing = json.loads(keyword_index_path.read_text())
        print(f"Index already exists with {existing.get('file_count', 0)} files")
        print(f"Use --rebuild to regenerate")
        return 0

    print("=" * 60)
    print("SWEBOK v4 Harness — Keyword Index Generator")
    print("=" * 60)

    # Collect files from multiple sources
    all_files = []

    # 1. Main corpus directory
    if corpus_dir.exists():
        corpus_files = generate_corpus_file_index(corpus_dir)
        all_files.extend(corpus_files)
        print(f"Found {len(corpus_files)} files in corpus")

    # 2. SWEBOK sections
    if swebok_dir.exists():
        swebok_files = list(swebok_dir.glob("*.md"))
        all_files.extend(swebok_files)
        print(f"Found {len(swebok_files)} SWEBOK section files")

    # 3. Corpus by-phase
    by_phase_dir = corpus_dir / "by-phase"
    if by_phase_dir.exists():
        phase_files = generate_corpus_file_index(by_phase_dir)
        all_files.extend(phase_files)
        print(f"Found {len(phase_files)} by-phase files")

    # Remove duplicates based on path
    seen = set()
    unique_files = []
    for f in all_files:
        if str(f) not in seen:
            seen.add(str(f))
            unique_files.append(f)

    print(f"\nTotal unique files to index: {len(unique_files)}")

    if len(unique_files) == 0:
        print("No files found to index!")
        return 1

    # Generate keyword index
    print("\nGenerating keyword index...")
    keyword_data = generate_keyword_index(unique_files, verbose=args.verbose)

    # Save keyword index
    with open(keyword_index_path, 'w') as f:
        json.dump(keyword_data, f, indent=2)
    print(f"Saved keyword index to {keyword_index_path}")
    print(f"  - {keyword_data['unique_keywords']} unique keywords")
    print(f"  - {keyword_data['file_count']} files indexed")

    # Generate and save KA index
    print("\nGenerating KA index...")
    ka_data = generate_ka_index(unique_files, verbose=args.verbose)
    with open(ka_index_path, 'w') as f:
        json.dump(ka_data, f, indent=2)
    print(f"Saved KA index to {ka_index_path}")

    # Generate and save topic index
    print("\nGenerating topic index...")
    topic_data = generate_topic_index(unique_files, verbose=args.verbose)
    with open(topic_index_path, 'w') as f:
        json.dump(topic_data, f, indent=2)
    print(f"Saved topic index to {topic_index_path}")

    # Summary
    print("\n" + "=" * 60)
    print("Index Generation Summary")
    print("=" * 60)
    print(f"Total files indexed: {len(unique_files)}")
    print(f"Unique keywords: {keyword_data['unique_keywords']}")
    print(f"KAs covered: {len(ka_data)}")
    print(f"Topics indexed: {len(topic_data)}")
    print(f"\nOutput directory: {output_dir}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
