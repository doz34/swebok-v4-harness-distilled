#!/usr/bin/env python3
"""
Knowledge Base Indexer — SWEBOK v4 Harness
Génère des index structurés des 742 sections SWEBOK par KA, topic, et keyword.
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

SECTIONS_DIR = Path("knowledge/swebok-sections")
OUTPUT_DIR = Path("knowledge/indexes")
OUTPUT_DIR.mkdir(exist_ok=True)

CHAPTER_KA_MAP = {
    "01": {"ka": 1, "name": "Software Requirements"},
    "02": {"ka": 2, "name": "Software Architecture"},
    "03": {"ka": 3, "name": "Software Design"},
    "04": {"ka": 4, "name": "Software Construction"},
    "05": {"ka": 5, "name": "Software Testing"},
    "06": {"ka": 6, "name": "Software Maintenance"},
    "07": {"ka": 7, "name": "Software Configuration Management"},
    "08": {"ka": 8, "name": "Software Engineering Management"},
    "09": {"ka": 9, "name": "Software Engineering Process"},
    "10": {"ka": 10, "name": "Software Engineering Models and Methods"},
    "11": {"ka": 11, "name": "Software Quality"},
    "12": {"ka": 12, "name": "Software Safety"},
    "13": {"ka": 13, "name": "Security Engineering"},
    "14": {"ka": 14, "name": "Systems Engineering"},
    "15": {"ka": 15, "name": "Computing Foundations"},
    "16": {"ka": 16, "name": "Mathematical Foundations"},
    "17": {"ka": 17, "name": "Engineering Foundations"},
}

def extract_keywords(text: str) -> List[str]:
    patterns = [
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:pattern|technique|method|approach|process)\b',
        r'\b(?:API|REST|GraphQL|SQL|NoSQL|Cache|Queue)\b',
        r'\b(?:microservices|monolith|serverless|container)\b',
    ]
    keywords = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        keywords.extend(matches)
    return list(set(keywords))[:30]

def classify_section(filename: str, content: str) -> Dict:
    chapter_match = re.search(r'CHAPTER\s*(\d+)', content[:1000])
    if chapter_match:
        chapter = chapter_match.group(1).zfill(2)
        if chapter in CHAPTER_KA_MAP:
            return {"ka": CHAPTER_KA_MAP[chapter]["ka"], "ka_name": CHAPTER_KA_MAP[chapter]["name"]}
    content_lower = content.lower()
    ka_scores = defaultdict(int)
    ka_keywords = {
        1: ["requirement", "stakeholder", "elicitation"],
        2: ["architecture", "component", "pattern"],
        3: ["design", "class", "module"],
        4: ["construction", "coding", "api"],
        5: ["testing", "test case", "coverage"],
    }
    for ka, kws in ka_keywords.items():
        for kw in kws:
            if kw in content_lower:
                ka_scores[ka] += 1
    if ka_scores:
        best_ka = max(ka_scores.items(), key=lambda x: x[1])[0]
        return {"ka": best_ka, "ka_name": CHAPTER_KA_MAP.get(str(best_ka).zfill(2), {}).get("name", "Unknown")}
    return {"ka": 0, "ka_name": "Unclassified"}

def main():
    print("Indexing SWEBOK v4 sections...")
    sections = []
    for f in SECTIONS_DIR.glob("*.md"):
        content = f.read_text(errors='ignore')
        cls = classify_section(f.name, content)
        sections.append({
            "filename": f.name,
            "ka": cls["ka"],
            "ka_name": cls["ka_name"],
            "size": f.stat().st_size,
            "preview": content[:200].strip(),
            "keywords": extract_keywords(content)
        })
    ka_index = defaultdict(lambda: {"sections": []})
    for s in sections:
        if s["ka"] > 0:
            ka_index[s["ka"]]["ka"] = s["ka"]
            ka_index[s["ka"]]["name"] = s["ka_name"]
            ka_index[s["ka"]]["sections"].append(s["filename"])
    with open(OUTPUT_DIR / "ka-index.json", "w") as f:
        json.dump(dict(ka_index), f, indent=2)
    summary = {"total": len(sections), "by_ka": {str(k): len(v["sections"]) for k, v in ka_index.items()}}
    with open(OUTPUT_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Indexed {len(sections)} sections")
    print(f"KA distribution: {summary['by_ka']}")

if __name__ == "__main__":
    main()
