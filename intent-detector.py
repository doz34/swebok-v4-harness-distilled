#!/usr/bin/env python3
"""
Intent Detector — SWEBOK v4 Harness
Detects intent from user prompt using pattern matching + semantic analysis + KB relevance scoring.

Inputs:  raw prompt
Outputs: intent type + confidence + phase + KB references
"""

import os
import re
import json
import subprocess
# I12 (L1 cleanup): PyYAML removed. The intent-map dispatch table is now
# stored as JSON in config/intent-map.json (replaces the legacy .yaml).
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from threading import Lock
import argparse

# Configuration paths
HARNESS_DIR = Path(__file__).parent.parent
CONFIG_DIR = HARNESS_DIR / "config"
KNOWLEDGE_DIR = HARNESS_DIR / "knowledge"
INDEX_DIR = KNOWLEDGE_DIR / "indexes"

# I12: dispatch table now read as JSON (no PyYAML import).
DEFAULT_INTENT_MAP = CONFIG_DIR / "intent-map.json"
DEFAULT_KA_INDEX = INDEX_DIR / "ka-index.json"
DEFAULT_KEYWORD_INDEX = INDEX_DIR / "keyword-index.json"


@dataclass
class IntentDetection:
    """Result of intent detection."""
    intent_type: str
    confidence: float
    phase: str
    ka: Optional[int]
    kb_references: List[str]
    matched_patterns: List[str]
    semantic_aliases_matched: List[str]
    kb_tags_found: List[str]
    detection_method: str  # 'exact', 'fuzzy', 'semantic', 'kb', 'combined'


@dataclass
class PhaseInfo:
    """SDLC Phase information."""
    id: str
    name: str
    ka_range: str


# SDLC Phase definitions
PHASES = {
    "PHASE_0_1": PhaseInfo("PHASE_0_1", "Discovery & Requirements", "KA1"),
    "PHASE_2_3": PhaseInfo("PHASE_2_3", "Architecture & Design", "KA2-KA3"),
    "PHASE_4_5": PhaseInfo("PHASE_4_5", "Implementation & Testing", "KA4-KA5"),
    "PHASE_6_7": PhaseInfo("PHASE_6_7", "Deployment & Operations", "KA6-KA7"),
    "PHASE_8_9": PhaseInfo("PHASE_8_9", "ML & Maintenance", "KA8-KA9"),
}


class IntentDetector:
    """Detects user intent from prompts using multi-signal analysis."""

    def __init__(self,
                 intent_map_path: str = str(DEFAULT_INTENT_MAP),
                 ka_index_path: str = str(DEFAULT_KA_INDEX),
                 keyword_index_path: str = str(DEFAULT_KEYWORD_INDEX)):
        """Initialize the intent detector."""
        self.intent_map_path = Path(intent_map_path)
        self.ka_index_path = Path(ka_index_path)
        self.keyword_index_path = Path(keyword_index_path)

        self.intent_map = self._load_json(self.intent_map_path)

        # Lazy load ka-index on startup (small file, needed for routing)
        self._ka_index = None
        self._ka_index_loaded = False
        self._ka_index_path = Path(ka_index_path)

        # Lazy load keyword-index only when search/query requires it
        self._keyword_index = None
        self._keyword_index_loaded = False
        self._keyword_index_path = Path(keyword_index_path)

        # Access pattern tracking for pre-loading optimization
        self._access_patterns = defaultdict(int)
        self._access_lock = Lock()

        self.intents = self.intent_map.get("intents", {})
        self.routing_config = self.intent_map.get("routing", {})
        self.similarity_threshold = self.routing_config.get("similarity_threshold", 0.72)

        # Build keyword to intent mapping for fast KB lookups
        self._build_keyword_intent_map()

    @property
    def ka_index(self):
        """Lazy load ka-index on first access."""
        if not self._ka_index_loaded:
            self._ka_index = self._load_json(self._ka_index_path) if self._ka_index_path.exists() else {}
            self._ka_index_loaded = True
            if self._ka_index:
                self._record_access("ka_index")
        return self._ka_index

    @property
    def keyword_index(self):
        """Lazy load keyword-index only when search/query requires it."""
        if not self._keyword_index_loaded:
            self._keyword_index = self._load_json(self._keyword_index_path) if self._keyword_index_path.exists() else {}
            self._keyword_index_loaded = True
            if self._keyword_index:
                self._record_access("keyword_index")
        return self._keyword_index

    def _record_access(self, index_name: str):
        """Record access pattern for pre-loading optimization."""
        with self._access_lock:
            self._access_patterns[index_name] += 1

    def get_access_stats(self) -> Dict:
        """Get access pattern statistics."""
        with self._access_lock:
            return dict(self._access_patterns)

    def preload_keyword_index(self):
        """Explicitly preload keyword-index when needed."""
        if not self._keyword_index_loaded:
            _ = self.keyword_index  # Trigger lazy load

    def _ensure_ka_index_loaded(self):
        """Ensure ka-index is loaded (for internal use)."""
        if not self._ka_index_loaded:
            self._ka_index = self._load_json(self._ka_index_path) if self._ka_index_path.exists() else {}
            self._ka_index_loaded = True

    def _load_json(self, path: Path) -> Dict:
        """Load JSON configuration (I12: replaces _load_yaml)."""
        if not path.exists():
            print(f"Warning: {path} not found")
            return {}
        with open(path) as f:
            return json.load(f)

    def _build_keyword_intent_map(self):
        """Build reverse index from keywords to intents."""
        self.keyword_to_intents = defaultdict(list)
        for intent_name, intent_config in self.intents.items():
            kb_tags = intent_config.get("kb_tags", [])
            for tag in kb_tags:
                self.keyword_to_intents[tag.lower()].append(intent_name)
            patterns = intent_config.get("patterns", [])
            for pattern in patterns:
                words = pattern.lower().split()
                for word in words:
                    if len(word) > 3:
                        self.keyword_to_intents[word].append(intent_name)

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        # Remove punctuation, lowercase
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # Normalize whitespace
        text = ' '.join(text.split())
        return text

    def _tokenize(self, text: str) -> set:
        """Tokenize text into words."""
        normalized = self._normalize_text(text)
        return set(normalized.split())

    def _exact_pattern_match(self, prompt: str, patterns: List[str]) -> Tuple[float, List[str]]:
        """Perform exact pattern matching."""
        prompt_lower = prompt.lower()
        matched = []
        for pattern in patterns:
            if pattern.lower() in prompt_lower:
                matched.append(pattern)
        if not matched:
            return 0.0, []
        # Score based on number and quality of matches
        score = min(len(matched) / max(len(patterns) * 0.2, 1), 1.0)
        return score, matched

    def _fuzzy_match(self, prompt: str, patterns: List[str], threshold: float = 0.6) -> Tuple[float, List[str]]:
        """Fuzzy pattern matching using token overlap."""
        prompt_tokens = self._tokenize(prompt)
        matched = []
        best_score = 0.0

        for pattern in patterns:
            pattern_tokens = set(pattern.lower().split())
            if pattern_tokens:
                overlap = len(prompt_tokens & pattern_tokens) / len(pattern_tokens)
                if overlap >= threshold:
                    matched.append(pattern)
                    best_score = max(best_score, overlap)

        return best_score, matched

    def _semantic_analysis(self, prompt: str, aliases: List[str]) -> Tuple[float, List[str]]:
        """Analyze semantic meaning using alias matching."""
        prompt_tokens = self._tokenize(prompt)
        matched = []
        scores = []

        for alias in aliases:
            alias_tokens = self._tokenize(alias)
            if alias_tokens:
                # Jaccard similarity
                intersection = len(prompt_tokens & alias_tokens)
                union = len(prompt_tokens | alias_tokens)
                jaccard = intersection / union if union > 0 else 0

                # Containment score
                containment = intersection / len(alias_tokens) if alias_tokens else 0

                score = max(jaccard, containment)
                if score > 0.3:
                    matched.append(alias)
                    scores.append(score)

        if not scores:
            return 0.0, []
        return max(scores), matched

    def _kb_relevance_scoring(self, prompt: str) -> Tuple[float, List[str], List[str]]:
        """
        Score prompt relevance using KB index.
        Returns: (score, matched_tags, referenced_files)
        """
        # Access keyword_index via property to trigger lazy loading
        kbidx = self.keyword_index
        if not kbidx:
            return 0.0, [], []
        self._record_access("kb_scoring")

        prompt_tokens = self._tokenize(prompt)
        tag_scores = defaultdict(float)
        file_scores = defaultdict(float)

        for token in prompt_tokens:
            if token in kbidx:
                files = kbidx[token]
                for f in files:
                    file_scores[f] += 1.0 / len(files)

        # Find matching KB tags
        matched_tags = []
        for intent_name, intent_config in self.intents.items():
            kb_tags = intent_config.get("kb_tags", [])
            for tag in kb_tags:
                tag_tokens = self._tokenize(tag)
                if tag_tokens & prompt_tokens:
                    matched_tags.append(tag)
                    tag_scores[intent_name] += 1

        # Score based on tag matches
        intent_scores = []
        for intent_name, score in tag_scores.items():
            kb_tags = self.intents[intent_name].get("kb_tags", [])
            if kb_tags:
                normalized = score / len(kb_tags)
                intent_scores.append((intent_name, min(normalized, 1.0)))

        if intent_scores:
            best_intent, best_score = max(intent_scores, key=lambda x: x[1])
            # Get referenced files
            referenced_files = list(set(filepath for filepath in file_scores))
            return best_score, matched_tags, referenced_files[:5]

        return 0.0, matched_tags, []

    def _infer_phase(self, prompt: str, intent_type: str) -> str:
        """Infer SDLC phase from intent and prompt content."""
        # Phase keywords
        phase_indicators = {
            "PHASE_0_1": ["requirement", "discovery", "stakeholder", "needs", "gather",
                         "elicitation", "scope", "plan", "project", "process"],
            "PHASE_2_3": ["architecture", "design", "pattern", "component", "module",
                         "structure", "high-level", "system design"],
            "PHASE_4_5": ["implement", "code", "build", "develop", "test", "coding",
                         "construction", "write", "function", "feature"],
            "PHASE_6_7": ["deploy", "release", "operation", "maintenance", "monitor",
                         "infrastructure", "devops", "ci/cd", "pipeline"],
            "PHASE_8_9": ["ml", "machine learning", "model", "training", "retire",
                         "deprecate", "archive", "optimize"]
        }

        prompt_lower = prompt.lower()
        scores = {}

        for phase, keywords in phase_indicators.items():
            score = sum(1 for kw in keywords if kw in prompt_lower)
            scores[phase] = score

        # Also use intent type hints
        intent_lower = intent_type.lower()
        if any(x in intent_lower for x in ["requirement", "stakeholder", "elicitation"]):
            scores["PHASE_0_1"] = scores.get("PHASE_0_1", 0) + 2
        elif any(x in intent_lower for x in ["architecture", "design"]):
            scores["PHASE_2_3"] = scores.get("PHASE_2_3", 0) + 2
        elif any(x in intent_lower for x in ["construction", "code", "implementation"]):
            scores["PHASE_4_5"] = scores.get("PHASE_4_5", 0) + 2
        elif any(x in intent_lower for x in ["testing", "test"]):
            scores["PHASE_4_5"] = scores.get("PHASE_4_5", 0) + 2
        elif any(x in intent_lower for x in ["deployment", "devops", "maintenance"]):
            scores["PHASE_6_7"] = scores.get("PHASE_6_7", 0) + 2

        if scores:
            return max(scores, key=scores.get)
        return "PHASE_0_1"  # Default

    def _infer_ka(self, prompt: str, intent_type: str, kb_tags: List[str]) -> Optional[int]:
        """Infer Knowledge Area from intent and KB tags."""
        # KA mapping from KB tags
        ka_patterns = {
            1: ["KA1", "requirements", "elicitation", "stakeholder"],
            2: ["KA2", "architecture", "architectural"],
            3: ["KA3", "design", "SOLID", "pattern"],
            4: ["KA4", "construction", "coding", "api"],
            5: ["KA5", "testing", "test", "coverage"],
            6: ["KA6", "maintenance"],
            7: ["KA7", "configuration", "version", "git"],
            8: ["KA8", "management", "project", "planning"],
            9: ["KA9", "process", "CI/CD", "devops"],
            10: ["KA10", "methodology", "agile", "scrum"],
            11: ["KA11", "quality", "QA", "review"],
            12: ["KA12", "safety"],
            13: ["KA13", "security", "vulnerability"],
            14: ["KA14", "systems", "embedded"],
            15: ["KA15", "foundation", "algorithm", "ML"],
        }

        for tag in kb_tags:
            for ka, patterns in ka_patterns.items():
                if any(p.lower() in tag.lower() for p in patterns):
                    return ka

        # Infer from intent name
        intent_lower = intent_type.lower()
        ka_keywords = {
            1: ["requirement", "stakeholder"],
            2: ["architecture", "architect"],
            3: ["design", "design"],
            4: ["construction", "code", "implement"],
            5: ["test", "testing"],
            6: ["maintenance"],
            7: ["config", "version"],
            8: ["project", "management"],
            9: ["process", "devops", "pipeline"],
            10: ["methodology", "agile", "scrum"],
            11: ["quality", "review", "code-review"],
            12: ["safety"],
            13: ["security"],
            14: ["system"],
            15: ["ml", "machine", "algorithm"],
        }

        for ka, keywords in ka_keywords.items():
            if any(kw in intent_lower for kw in keywords):
                return ka

        return None

    def detect(self, prompt: str) -> IntentDetection:
        """
        Main detection function - analyze prompt and detect intent.

        Args:
            prompt: Raw user prompt

        Returns:
            IntentDetection with intent type, confidence, phase, and KB references
        """
        # Collect scores for each intent
        intent_scores = {}

        for intent_name, intent_config in self.intents.items():
            patterns = intent_config.get("patterns", [])
            aliases = intent_config.get("semantic_aliases", [])
            kb_tags = intent_config.get("kb_tags", [])
            priority = intent_config.get("priority", 50) / 100.0

            # Calculate scores from each signal
            exact_score, exact_matches = self._exact_pattern_match(prompt, patterns)
            fuzzy_score, fuzzy_matches = self._fuzzy_match(prompt, patterns)
            semantic_score, semantic_matches = self._semantic_analysis(prompt, aliases)

            pattern_score = max(exact_score, fuzzy_score)
            matched_patterns = exact_matches + [m for m in fuzzy_matches if m not in exact_matches]

            # Weighted combination
            weights = intent_config.get("weights", {
                "semantic": 0.45,
                "pattern": 0.25,
                "context": 0.20,
                "kb_relevance": 0.10
            })

            combined_score = (
                weights.get("semantic", 0.3) * semantic_score +
                weights.get("pattern", 0.3) * pattern_score +
                weights.get("kb_relevance", 0.1) * 0.5 +  # Simplified KB score
                0.2 * priority  # Priority boost
            )

            intent_scores[intent_name] = {
                "score": combined_score,
                "exact_score": exact_score,
                "pattern_score": pattern_score,
                "semantic_score": semantic_score,
                "matched_patterns": matched_patterns,
                "semantic_aliases_matched": semantic_matches
            }

        # Find best matching intent
        if not intent_scores:
            return IntentDetection(
                intent_type="unknown",
                confidence=0.0,
                phase="PHASE_0_1",
                ka=None,
                kb_references=[],
                matched_patterns=[],
                semantic_aliases_matched=[],
                kb_tags_found=[],
                detection_method="none"
            )

        best_intent = max(intent_scores.items(), key=lambda x: x[1]["score"])
        intent_name = best_intent[0]
        scores = best_intent[1]
        confidence = scores["score"]

        # Get KB relevance
        kb_score, kb_tags_found, kb_references = self._kb_relevance_scoring(prompt)

        # Determine detection method
        if scores["exact_score"] > 0.5:
            method = "exact"
        elif scores["semantic_score"] > scores["pattern_score"]:
            method = "semantic"
        elif kb_score > 0.3:
            method = "kb"
        elif scores["pattern_score"] > 0.3:
            method = "fuzzy"
        else:
            method = "combined"

        # Get full intent config
        intent_config = self.intents[intent_name]

        return IntentDetection(
            intent_type=intent_name,
            confidence=min(confidence + kb_score * 0.1, 1.0),
            phase=self._infer_phase(prompt, intent_name),
            ka=self._infer_ka(prompt, intent_name, kb_tags_found),
            kb_references=kb_references,
            matched_patterns=scores["matched_patterns"],
            semantic_aliases_matched=scores["semantic_aliases_matched"],
            kb_tags_found=kb_tags_found,
            detection_method=method
        )

    def detect_batch(self, prompts: List[str]) -> List[IntentDetection]:
        """Detect intents for multiple prompts."""
        return [self.detect(p) for p in prompts]

    def get_detection_summary(self, detection: IntentDetection) -> Dict:
        """Get a summary dict of the detection result."""
        return {
            "intent": detection.intent_type,
            "confidence": f"{detection.confidence:.1%}",
            "phase": detection.phase,
            "ka": detection.ka,
            "method": detection.detection_method,
            "patterns": detection.matched_patterns[:5],
            "kb_tags": detection.kb_tags_found[:5]
        }


def main():
    """CLI interface for intent detector."""
    parser = argparse.ArgumentParser(
        description="Intent Detector — Detect intent from user prompt"
    )
    parser.add_argument("prompt", nargs="*", help="User prompt to analyze")
    parser.add_argument("--intent-map", default=str(DEFAULT_INTENT_MAP),
                       help="Path to intent-map.json (I12: was intent-map.yaml)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if not args.prompt:
        print("Error: prompt required")
        parser.print_help()
        return 1

    prompt = " ".join(args.prompt)

    detector = IntentDetector(intent_map_path=args.intent_map)
    detection = detector.detect(prompt)

    if args.json:
        result = {
            "intent_type": detection.intent_type,
            "confidence": detection.confidence,
            "phase": detection.phase,
            "ka": detection.ka,
            "kb_references": detection.kb_references,
            "matched_patterns": detection.matched_patterns,
            "semantic_aliases_matched": detection.semantic_aliases_matched,
            "kb_tags_found": detection.kb_tags_found,
            "detection_method": detection.detection_method
        }
        print(json.dumps(result, indent=2))

        # LAW 1 (HOT_PATH): wire intent -> state_engine so downstream
        # `hot_path_decision` returns LITE/FULL based on this detection.
        # Best-effort: a missing/broken state DB must not break the CLI.
        try:
            _state_engine = HARNESS_DIR / "scripts" / "lib" / "state_engine.py"
            subprocess.run(
                ["python3", str(_state_engine), "set_intent",
                 detection.intent_type, str(detection.confidence)],
                check=False, capture_output=True, timeout=10
            )
        except Exception:
            pass
    else:
        print(f"Intent Type: {detection.intent_type}")
        print(f"Confidence: {detection.confidence:.1%}")
        print(f"Phase: {detection.phase}")
        if detection.ka:
            print(f"Knowledge Area: KA{detection.ka}")
        print(f"Detection Method: {detection.detection_method}")

        if args.verbose:
            if detection.matched_patterns:
                print(f"\nMatched Patterns ({len(detection.matched_patterns)}):")
                for p in detection.matched_patterns[:5]:
                    print(f"  - {p}")
            if detection.semantic_aliases_matched:
                print(f"\nSemantic Aliases Matched:")
                for a in detection.semantic_aliases_matched[:5]:
                    print(f"  - {a}")
            if detection.kb_tags_found:
                print(f"\nKB Tags Found:")
                for t in detection.kb_tags_found[:5]:
                    print(f"  - {t}")
            if detection.kb_references:
                print(f"\nKB References:")
                for r in detection.kb_references[:5]:
                    print(f"  - {r}")

    return 0


if __name__ == "__main__":
    exit(main())
