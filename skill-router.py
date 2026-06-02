#!/usr/bin/env python3
"""
Skill Router — SWEBOK v4 Harness
Routes intents to skills based on intent-map.yaml semantic routing.

Inputs:  user prompt, context
Outputs: skill activation + agent assignment
Uses:    KB index integration, hyperagent parallel creation
"""

import os
import json
# I13 (L1 cleanup): PyYAML removed. Skill/agent registries are not
# maintained as separate files - the canonical routing table lives in
# the .swebok_state.db (via state_engine) and the intent-map dispatch
# table is now a JSON file (config/intent-map.json).
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from collections import defaultdict
from threading import Lock
import argparse

# Configuration paths
HARNESS_DIR = Path(__file__).parent.parent
CONFIG_DIR = HARNESS_DIR / "config"
KNOWLEDGE_DIR = HARNESS_DIR / "knowledge"
INDEX_DIR = KNOWLEDGE_DIR / "indexes"

# Default paths
# I13: dispatch table now JSON. skills/agents registries are deprecated -
# they were never populated and the script now hardcodes empty defaults.
DEFAULT_INTENT_MAP = CONFIG_DIR / "intent-map.json"
DEFAULT_SKILLS_REGISTRY = ""  # deprecated - no external file
DEFAULT_AGENTS_REGISTRY = ""  # deprecated - no external file
DEFAULT_KA_INDEX = INDEX_DIR / "ka-index.json"
DEFAULT_KEYWORD_INDEX = INDEX_DIR / "keyword-index.json"


@dataclass
class RoutingResult:
    """Result of skill routing operation."""
    intent: str
    confidence: float
    primary_skill: str
    secondary_skills: List[str]
    agents: List[str]
    hooks: List[str]
    kb_tags: List[str]
    phase: str
    parallel_candidates: List[str]
    fallback_chain: List[Dict]
    routing_method: str  # 'semantic', 'pattern', 'kb', 'fallback'


@dataclass
class SkillActivation:
    """Skill activation details."""
    skill_id: str
    skill_name: str
    skill_path: str
    status: str
    description: str
    ka: Optional[int]
    category: str


@dataclass
class AgentAssignment:
    """Agent assignment details."""
    agent_id: str
    agent_name: str
    agent_type: str
    ka: Optional[str]
    capabilities: List[str]


class SkillRouter:
    """Routes user intents to appropriate skills and agents using semantic routing."""

    def __init__(self,
                 intent_map_path: str = str(DEFAULT_INTENT_MAP),
                 skills_registry_path: str = str(DEFAULT_SKILLS_REGISTRY),
                 agents_registry_path: str = str(DEFAULT_AGENTS_REGISTRY),
                 ka_index_path: str = str(DEFAULT_KA_INDEX),
                 keyword_index_path: str = str(DEFAULT_KEYWORD_INDEX)):
        """Initialize the skill router with configuration files."""
        self.intent_map_path = Path(intent_map_path)
        self.skills_registry_path = Path(skills_registry_path)
        self.agents_registry_path = Path(agents_registry_path)
        self.ka_index_path = Path(ka_index_path)
        self.keyword_index_path = Path(keyword_index_path)

        self.intent_map = self._load_json(self.intent_map_path)
        # I13: skills/agents registries are deprecated. They were never
        # populated and the script keeps empty defaults. We honour the
        # constructor argument but no external file is read.
        self.skills_registry = {"skills": []}
        self.agents_registry = {"agents": []}

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

        self.routing_config = self.intent_map.get("routing", {})
        self.intents = self.intent_map.get("intents", {})
        self.hyperagent_config = self.routing_config.get("hyperagent", {})

        self.similarity_threshold = self.routing_config.get("similarity_threshold", 0.72)
        self.max_parallel_agents = self.hyperagent_config.get("max_parallel_agents", 4)
        self.parallel_threshold = self.hyperagent_config.get("parallel_threshold", 0.85)

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
        """Load JSON configuration file (I13: replaces _load_yaml)."""
        if not path.exists():
            print(f"Warning: {path} not found")
            return {}
        with open(path) as f:
            return json.load(f)

    def _compute_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts using SequenceMatcher."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _pattern_match(self, prompt: str, patterns: List[str]) -> Tuple[float, List[str]]:
        """Match prompt against patterns, returning confidence and matched patterns."""
        prompt_lower = prompt.lower()
        matched = []
        for pattern in patterns:
            if pattern.lower() in prompt_lower:
                matched.append(pattern)
        if not matched:
            return 0.0, []
        # Confidence based on proportion of patterns matched
        confidence = min(len(matched) / max(len(patterns) * 0.3, 1), 1.0)
        return confidence, matched

    def _semantic_match(self, prompt: str, aliases: List[str]) -> float:
        """Match prompt against semantic aliases."""
        if not aliases:
            return 0.0
        prompt_lower = prompt.lower()
        best_score = 0.0
        for alias in aliases:
            # Word overlap scoring
            prompt_words = set(prompt_lower.split())
            alias_words = set(alias.lower().split())
            if alias_words:
                overlap = len(prompt_words & alias_words) / len(alias_words)
                best_score = max(best_score, overlap)
            # Sequence similarity
            sim = self._compute_similarity(prompt, alias)
            best_score = max(best_score, sim)
        return best_score

    def _kb_relevance_score(self, prompt: str, kb_tags: List[str]) -> float:
        """Calculate KB relevance score based on keyword index."""
        # Trigger lazy load of keyword_index when KB scoring is needed
        if not kb_tags:
            return 0.0
        # Access keyword_index via property to trigger lazy loading
        kbidx = self.keyword_index
        if not kbidx:
            return 0.0
        self._record_access("kb_scoring")
        prompt_lower = prompt.lower()
        prompt_words = set(prompt_lower.split())
        score = 0.0
        for tag in kb_tags:
            tag_lower = tag.lower()
            if tag_lower in kbidx:
                # Higher score if tag keywords appear in prompt
                tag_keywords = set(kbidx.keys())
                overlap = len(prompt_words & tag_keywords)
                score += min(overlap / len(kb_tags), 1.0) * 0.5
            # Check direct tag match
            if tag_lower in prompt_lower:
                score += 0.3
        return min(score, 1.0)

    def _context_weighted_score(self,
                               semantic_score: float,
                               pattern_score: float,
                               kb_score: float,
                               context: Dict,
                               intent_config: Dict) -> float:
        """Compute weighted score combining all signals with context."""
        weights = intent_config.get("weights", {
            "semantic": 0.45,
            "pattern": 0.25,
            "context": 0.20,
            "kb_relevance": 0.10
        })

        # Context contribution (simplified - could be enhanced with actual context analysis)
        context_score = 0.5  # Default neutral context

        total_weight = sum(weights.values())
        weighted_score = (
            (weights.get("semantic", 0) * semantic_score +
             weights.get("pattern", 0) * pattern_score +
             weights.get("context", 0) * context_score +
             weights.get("kb_relevance", 0) * kb_score) / total_weight
        )
        return weighted_score

    def _detect_phase(self, intent: str) -> str:
        """Infer SDLC phase from intent."""
        phase_map = {
            "requirement": "PHASE_0_1",
            "architecture": "PHASE_2_3",
            "design": "PHASE_2_3",
            "construction": "PHASE_4_5",
            "code": "PHASE_4_5",
            "implementation": "PHASE_4_5",
            "testing": "PHASE_4_5",
            "test": "PHASE_4_5",
            "deployment": "PHASE_6_7",
            "devops": "PHASE_6_7",
            "maintenance": "PHASE_6_7",
            "security": "PHASE_6_7",
            "project": "PHASE_0_1",
            "process": "PHASE_0_1",
            "quality": "PHASE_4_5",
        }
        for key, phase in phase_map.items():
            if key in intent.lower():
                return phase
        return "PHASE_0_1"  # Default to discovery/requirements

    def route(self, prompt: str, context: Optional[Dict] = None) -> RoutingResult:
        """
        Main routing function - determines best skill/agent match for prompt.

        Args:
            prompt: User's raw prompt/input
            context: Optional context dict with conversation history, etc.

        Returns:
            RoutingResult with matched intent, skills, agents, and routing details
        """
        context = context or {}
        prompt_lower = prompt.lower()

        best_intent = None
        best_score = 0.0
        best_method = "fallback"
        best_details = {}

        # Iterate through all intents and score them
        for intent_name, intent_config in self.intents.items():
            patterns = intent_config.get("patterns", [])
            aliases = intent_config.get("semantic_aliases", [])
            kb_tags = intent_config.get("kb_tags", [])

            # Calculate individual scores
            pattern_score, matched_patterns = self._pattern_match(prompt, patterns)
            semantic_score = self._semantic_match(prompt, aliases)
            kb_score = self._kb_relevance_score(prompt, kb_tags)

            # Weighted combined score
            combined_score = self._context_weighted_score(
                semantic_score, pattern_score, kb_score, context, intent_config
            )

            # Boost for priority
            priority = intent_config.get("priority", 50) / 100.0
            final_score = combined_score * 0.7 + priority * 0.3

            if final_score > best_score:
                best_score = final_score
                best_intent = intent_name
                best_method = self._determine_routing_method(
                    semantic_score, pattern_score, kb_score
                )
                best_details = {
                    "pattern_score": pattern_score,
                    "semantic_score": semantic_score,
                    "kb_score": kb_score,
                    "matched_patterns": matched_patterns,
                    "priority": intent_config.get("priority", 50)
                }

        # If no good match, use fallback
        if best_score < self.similarity_threshold:
            fallback = self.intent_map.get("fallback", {})
            return RoutingResult(
                intent=fallback.get("skill", "general-assistance"),
                confidence=best_score,
                primary_skill=fallback.get("skill", "general-assistance"),
                secondary_skills=[],
                agents=[fallback.get("agent", "generalist")],
                hooks=fallback.get("hooks", []),
                kb_tags=[],
                phase="PHASE_0_1",
                parallel_candidates=[],
                fallback_chain=fallback.get("chain", []),
                routing_method="fallback"
            )

        # Build full result for matched intent
        intent_config = self.intents[best_intent]
        return RoutingResult(
            intent=best_intent,
            confidence=best_score,
            primary_skill=intent_config.get("skills", {}).get("primary", ""),
            secondary_skills=intent_config.get("skills", {}).get("secondary", []),
            agents=intent_config.get("agents", []),
            hooks=intent_config.get("hooks", []),
            kb_tags=intent_config.get("kb_tags", []),
            phase=self._detect_phase(best_intent),
            parallel_candidates=intent_config.get("parallel_candidates", []),
            fallback_chain=intent_config.get("fallback_chain", []),
            routing_method=best_method
        )

    def _determine_routing_method(self, semantic: float, pattern: float, kb: float) -> str:
        """Determine which routing signal contributed most."""
        if pattern >= semantic and pattern >= kb:
            return "pattern"
        elif semantic >= pattern and semantic >= kb:
            return "semantic"
        elif kb > 0:
            return "kb"
        return "combined"

    def get_skill_activation(self, skill_id: str) -> Optional[SkillActivation]:
        """Get full skill details from registry."""
        skills = self.skills_registry.get("skills", [])
        for skill in skills:
            if skill.get("id") == skill_id:
                return SkillActivation(
                    skill_id=skill.get("id"),
                    skill_name=skill.get("name"),
                    skill_path=skill.get("path"),
                    status=skill.get("status"),
                    description=skill.get("description"),
                    ka=skill.get("ka"),
                    category=skill.get("category")
                )
        return None

    def get_agent_assignment(self, agent_id: str) -> Optional[AgentAssignment]:
        """Get full agent details from registry."""
        agents = self.agents_registry.get("agents", [])
        for agent in agents:
            if agent.get("id") == agent_id:
                return AgentAssignment(
                    agent_id=agent.get("id"),
                    agent_name=agent.get("name"),
                    agent_type=agent.get("type"),
                    ka=agent.get("ka"),
                    capabilities=agent.get("capabilities", [])
                )
        return None

    def should_parallelize(self, result: RoutingResult) -> bool:
        """Determine if hyperagent parallel execution is warranted."""
        return (
            result.confidence >= self.parallel_threshold and
            len(result.parallel_candidates) > 0
        )

    def get_parallel_agents(self, result: RoutingResult) -> List[str]:
        """Get list of agents for parallel execution."""
        if not self.should_parallelize(result):
            return result.agents[:1]  # Return single agent
        return result.agents + result.parallel_candidates[:self.max_parallel_agents - 1]

    def route_with_full_context(self,
                               prompt: str,
                               context: Optional[Dict] = None) -> Dict:
        """
        Full routing with skill activations and agent assignments.

        Returns a complete dict suitable for hyperagent orchestration.
        """
        routing = self.route(prompt, context)

        # Resolve skill activations
        primary_skill = self.get_skill_activation(routing.primary_skill)
        secondary_skills = [
            self.get_skill_activation(sid) for sid in routing.secondary_skills
            if self.get_skill_activation(sid)
        ]

        # Resolve agent assignments
        primary_agent = self.get_agent_assignment(routing.agents[0]) if routing.agents else None
        parallel_agents = [
            self.get_agent_assignment(aid) for aid in self.get_parallel_agents(routing)
            if self.get_agent_assignment(aid)
        ]

        return {
            "routing": {
                "intent": routing.intent,
                "confidence": routing.confidence,
                "phase": routing.phase,
                "routing_method": routing.routing_method,
                "kb_tags": routing.kb_tags
            },
            "skills": {
                "primary": primary_skill.__dict__ if primary_skill else None,
                "secondary": [s.__dict__ for s in secondary_skills],
                "parallel": self.should_parallelize(routing)
            },
            "agents": {
                "primary": primary_agent.__dict__ if primary_agent else None,
                "parallel_candidates": [a.__dict__ for a in parallel_agents],
                "parallel_execution": len(parallel_agents) > 1
            },
            "hooks": routing.hooks,
            "fallback_chain": routing.fallback_chain,
            "details": {
                "should_parallelize": self.should_parallelize(routing),
                "max_parallel": self.max_parallel_agents
            }
        }


def main():
    """CLI interface for skill router."""
    parser = argparse.ArgumentParser(
        description="Skill Router — Route intents to skills based on semantic routing"
    )
    parser.add_argument("prompt", nargs="*", help="User prompt to route")
    parser.add_argument("-c", "--context", help="Path to context JSON file")
    parser.add_argument("-f", "--full", action="store_true",
                       help="Output full routing context with skill/agent details")
    parser.add_argument("--intent-map", default=str(DEFAULT_INTENT_MAP),
                       help="Path to intent-map.json (I13: was intent-map.yaml)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.prompt:
        print("Error: prompt required")
        parser.print_help()
        return 1

    prompt = " ".join(args.prompt)
    context = {}
    if args.context:
        with open(args.context) as f:
            context = json.load(f)

    router = SkillRouter(intent_map_path=args.intent_map)

    if args.full:
        result = router.route_with_full_context(prompt, context)
    else:
        routing = router.route(prompt, context)
        result = {
            "intent": routing.intent,
            "confidence": routing.confidence,
            "primary_skill": routing.primary_skill,
            "agents": routing.agents,
            "phase": routing.phase,
            "routing_method": routing.routing_method,
            "should_parallelize": router.should_parallelize(routing)
        }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Intent: {result.get('intent')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Primary Skill: {result.get('primary_skill', 'N/A')}")
        print(f"Agents: {', '.join(result.get('agents', result.get('routing', {}).get('agents', [])))}")
        print(f"Phase: {result.get('phase', 'N/A')}")
        print(f"Routing Method: {result.get('routing_method', 'N/A')}")
        if result.get('should_parallelize'):
            print(f"Parallel Execution: YES")
        if args.full:
            print("\n--- Full Routing Context ---")
            print(json.dumps(result, indent=2, default=str))

    return 0


if __name__ == "__main__":
    exit(main())
