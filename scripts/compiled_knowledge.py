#!/usr/bin/env python3
"""
SWEBOK v4 Harness — Compiled Knowledge Engine
==============================================

The deterministic, self-contained alternative to RAG.

Given a query, returns structured answers from the compiled knowledge base
(872 books distilled into 7 layers: principles, antipatterns, ontologies,
decision trees, recipes, comparisons, checklists, risks).

NO LLM. NO embeddings. NO vector search. NO network. NO hallucination.

Usage:
    python3 scripts/compiled-knowledge.py "should I use SQL or NoSQL?"
    python3 scripts/compiled-knowledge.py --phase P3 "design patterns"
    python3 scripts/compiled-knowledge.py --checklist P5
    python3 scripts/compiled-knowledge.py --recipe api-design
    python3 scripts/compiled-knowledge.py --antipattern god-class
    python3 scripts/compiled-knowledge.py --principle KISS
    python3 scripts/compiled-knowledge.py --decision-tree choose-database
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configuration
HARNESS_DIR = Path(__file__).parent.parent
DISTILLED_DIR = HARNESS_DIR / "distilled"


def load_json(path: Path) -> Dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


class CompiledKnowledge:
    """
    The compiled knowledge engine. Loads all distilled files once,
    answers questions deterministically.
    """

    def __init__(self, distilled_dir: Path = DISTILLED_DIR):
        self.distilled_dir = distilled_dir
        self.principles = self._load_principles()
        self.antipatterns = self._load_antipatterns()
        self.ontologies = self._load_ontologies()
        self.decision_trees = self._load_decision_trees()
        self.recipes = self._load_recipes()
        self.comparisons = self._load_comparisons()
        self.citations = self._load_citations()
        # Build indexes for fast lookup
        self.principle_by_id = {p["id"]: p for p in self.principles}
        self.antipattern_by_id = {a["id"]: a for a in self.antipatterns}
        self.decision_tree_by_id = {t["id"]: t for t in self.decision_trees}
        self.recipe_by_id = {
            r["file"].stem: r for r in self.recipes if "file" in r
        }

    def _load_principles(self) -> List[Dict]:
        data = load_json(self.distilled_dir / "principles.json")
        return data.get("principles", [])

    def _load_antipatterns(self) -> List[Dict]:
        data = load_json(self.distilled_dir / "antipatterns.json")
        return data.get("antipatterns", [])

    def _load_ontologies(self) -> Dict[str, Dict]:
        result = {}
        ont_dir = self.distilled_dir / "ontologies"
        if ont_dir.exists():
            for f in ont_dir.glob("*.json"):
                result[f.stem] = load_json(f)
        return result

    def _load_decision_trees(self) -> List[Dict]:
        result = []
        dt_dir = self.distilled_dir / "decision-trees"
        if dt_dir.exists():
            for f in dt_dir.glob("*.json"):
                data = load_json(f)
                if "decision_tree" in data:
                    data["id"] = data["decision_tree"].get("id", f.stem)
                    result.append(data)
        return result

    def _load_recipes(self) -> List[Dict]:
        result = []
        r_dir = self.distilled_dir / "recipes"
        if r_dir.exists():
            for f in r_dir.glob("*.md"):
                result.append({"file": f, "name": f.stem, "content": f.read_text()})
        return result

    def _load_comparisons(self) -> List[Dict]:
        result = []
        c_dir = self.distilled_dir / "comparisons"
        if c_dir.exists():
            for f in c_dir.glob("*.json"):
                result.append(load_json(f))
        return result

    def _load_citations(self) -> Dict:
        return load_json(self.distilled_dir / "citations" / "by-domain.json")

    def query(self, question: str, top_k: int = 5) -> List[Dict]:
        """
        Answer a question by matching against the compiled knowledge base.
        Returns top-k most relevant results across all knowledge types.
        """
        q = question.lower().strip()
        results = []
        # Principles
        for p in self.principles:
            score = self._score(p, q, ["id", "name", "synthesis", "category", "domains", "phases", "applies_when", "violations_signal"])
            if score > 0:
                results.append({"type": "principle", "data": p, "score": score})
        # Antipatterns
        for a in self.antipatterns:
            score = self._score(a, q, ["id", "name", "symptom", "cause", "fix", "domain", "languages", "phases"])
            if score > 0:
                results.append({"type": "antipattern", "data": a, "score": score})
        # Recipes
        for r in self.recipes:
            score = self._score({"name": r["name"], "content": r["content"]}, q, ["name", "content"])
            if score > 0:
                results.append({"type": "recipe", "data": {"name": r["name"], "snippet": r["content"][:500]}, "score": score})
        # Comparisons
        for c in self.comparisons:
            score = self._score(c, q, ["name", "description", "domain"])
            if score > 0:
                results.append({"type": "comparison", "data": c, "score": score})
        # Decision trees
        for t in self.decision_trees:
            score = self._score(t, q, ["id", "description", "domain"])
            if score > 0:
                results.append({"type": "decision_tree", "data": t, "score": score})
        # Sort by score, return top_k
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]

    def _score(self, item: Dict, query: str, fields: List[str]) -> float:
        """Score an item against a query. Higher is better. 0 means no match."""
        score = 0.0
        for field in fields:
            value = item.get(field)
            if value is None:
                continue
            if isinstance(value, str):
                if query in value.lower():
                    score += 2.0
                else:
                    for word in query.split():
                        if len(word) > 2 and word in value.lower():
                            score += 0.5
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, str) and any(w in v.lower() for w in query.split() if len(w) > 2):
                        score += 0.8
        # Boost for ID matches
        if "id" in item and isinstance(item["id"], str) and query in item["id"].lower():
            score += 5.0
        return score

    def get_principle(self, principle_id: str) -> Optional[Dict]:
        return self.principle_by_id.get(principle_id.upper().replace("-", "_"))

    def get_antipattern(self, antipattern_id: str) -> Optional[Dict]:
        return self.antipattern_by_id.get(antipattern_id.upper().replace("-", "_"))

    def get_decision_tree(self, tree_id: str) -> Optional[Dict]:
        return self.decision_tree_by_id.get(tree_id.replace("-", "_"))

    def get_recipe(self, recipe_name: str) -> Optional[Dict]:
        return self.recipe_by_id.get(recipe_name)

    def get_phase_checklist(self, phase: str) -> Optional[str]:
        """Returns markdown checklist for a phase (P1-P9)."""
        checklist_file = self.distilled_dir / "checklists" / "all-phases.md"
        if not checklist_file.exists():
            return None
        content = checklist_file.read_text()
        # Extract the section for the requested phase
        phase_norm = phase.upper()
        marker = f"## {phase_norm} —"
        if marker not in content:
            return f"No checklist for {phase}. Available: P1-P9."
        start = content.index(marker)
        # Find the next phase or end
        end = len(content)
        for next_phase in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"]:
            next_marker = f"## {next_phase} —"
            if next_marker == marker:
                continue
            if next_marker in content[start + 1:]:
                end = start + 1 + content[start + 1:].index(next_marker)
                break
        return content[start:end].strip()

    def get_risks(self, category: str = "all") -> str:
        """Returns the risk catalog (security, performance, etc.)."""
        risks_file = self.distilled_dir / "risks" / "all-risks.md"
        if not risks_file.exists():
            return "Risk catalog not found."
        return risks_file.read_text()

    def stats(self) -> Dict:
        """Statistics about the compiled knowledge base."""
        return {
            "principles": len(self.principles),
            "antipatterns": len(self.antipatterns),
            "ontologies": len(self.ontologies),
            "decision_trees": len(self.decision_trees),
            "recipes": len(self.recipes),
            "comparisons": len(self.comparisons),
            "domains_in_citations": len(self.citations.get("domains", {})),
            "total_distilled_size_kb": sum(
                f.stat().st_size for f in self.distilled_dir.rglob("*") if f.is_file()
            ) // 1024,
        }


def format_result(result: Dict) -> str:
    """Format a search result for terminal output."""
    t = result["type"]
    d = result["data"]
    score = result["score"]
    out = [f"[{t.upper()}] (score={score:.1f})"]
    if t == "principle":
        out.append(f"  ID: {d.get('id', '?')}")
        out.append(f"  Name: {d.get('name', '?')}")
        out.append(f"  Category: {d.get('category', '?')}")
        out.append(f"  Citation density: {d.get('citation_density', '?')}")
        out.append(f"  Books endorsing: {d.get('books_endorsing', '?')}")
        out.append(f"  Phases: {', '.join(d.get('phases', []))}")
        out.append(f"  Synthesis: {d.get('synthesis', '?')}")
    elif t == "antipattern":
        out.append(f"  ID: {d.get('id', '?')}")
        out.append(f"  Name: {d.get('name', '?')}")
        out.append(f"  Domain: {d.get('domain', '?')}")
        out.append(f"  Severity: {d.get('severity', '?')}")
        out.append(f"  Symptom: {d.get('symptom', '?')}")
        out.append(f"  Fix: {d.get('fix', '?')}")
    elif t == "recipe":
        out.append(f"  Name: {d.get('name', '?')}")
        out.append(f"  Snippet: {d.get('snippet', '?')[:200]}...")
    elif t == "comparison":
        out.append(f"  Name: {d.get('name', '?')}")
        out.append(f"  Domain: {d.get('domain', '?')}")
        out.append(f"  Description: {d.get('description', '?')}")
    elif t == "decision_tree":
        out.append(f"  ID: {d.get('id', '?')}")
        out.append(f"  Description: {d.get('description', '?')}")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Compiled Knowledge Engine — deterministic alternative to RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", nargs="?", help="Question to answer")
    parser.add_argument("--principle", help="Get a specific principle by ID (e.g. KISS, YAGNI)")
    parser.add_argument("--antipattern", help="Get a specific antipattern by ID (e.g. GOD_CLASS)")
    parser.add_argument("--recipe", help="Get a recipe by name (e.g. api-design, authentication)")
    parser.add_argument("--decision-tree", help="Get a decision tree by ID (e.g. choose-database)")
    parser.add_argument("--checklist", help="Get a phase checklist (P1-P9)")
    parser.add_argument("--risks", action="store_true", help="Get the full risk catalog")
    parser.add_argument("--stats", action="store_true", help="Show knowledge base statistics")
    parser.add_argument("--phase", help="Filter by phase (P1-P9)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default 5)")
    args = parser.parse_args()
    ck = CompiledKnowledge()
    if args.stats:
        print(json.dumps(ck.stats(), indent=2))
        return 0
    if args.principle:
        p = ck.get_principle(args.principle)
        if p:
            print(json.dumps(p, indent=2))
        else:
            print(f"Principle not found: {args.principle}", file=sys.stderr)
            print(f"Available: {', '.join(sorted(ck.principle_by_id.keys()))}", file=sys.stderr)
            return 1
    elif args.antipattern:
        a = ck.get_antipattern(args.antipattern)
        if a:
            print(json.dumps(a, indent=2))
        else:
            print(f"Antipattern not found: {args.antipattern}", file=sys.stderr)
            return 1
    elif args.recipe:
        r = ck.get_recipe(args.recipe)
        if r:
            print(r["content"])
        else:
            print(f"Recipe not found: {args.recipe}", file=sys.stderr)
            return 1
    elif args.decision_tree:
        t = ck.get_decision_tree(args.decision_tree)
        if t:
            print(json.dumps(t, indent=2))
        else:
            print(f"Decision tree not found: {args.decision_tree}", file=sys.stderr)
            return 1
    elif args.checklist:
        c = ck.get_phase_checklist(args.checklist)
        if c:
            print(c)
        else:
            return 1
    elif args.risks:
        print(ck.get_risks())
    elif args.query:
        results = ck.query(args.query, top_k=args.top_k)
        if not results:
            print(f"No results for: {args.query}")
            print("Try: --principle KISS, --antipattern GOD_CLASS, --recipe api-design, --checklist P5")
            return 1
        for r in results:
            print(format_result(r))
            print()
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
