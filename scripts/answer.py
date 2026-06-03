#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — End-to-End Answer Generator
==================================================

L0 (compiled) + L1 (retrieval) + LLM provider → final answer.
The LLM sees a working dossier; the answer cites [N] for each claim.

Usage:
    python3 scripts/answer.py "How do I design a REST API?"
    python3 scripts/answer.py --provider openai "Compare TDD vs BDD"
    python3 scripts/answer.py --dossier-only --provider anthropic "..."
"""

import argparse
import json
import os
import sys
from pathlib import Path

HARNESS_DIR = Path(__file__).parent.parent

sys.path.insert(0, str(HARNESS_DIR / "scripts"))

from retrieval.providers import create as create_provider  # noqa: E402
from query import Router  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="V2 End-to-end answer generator (L0 + L1 + LLM)")
    parser.add_argument("query", help="Question to answer")
    parser.add_argument("--provider", default=None, help="LLM provider (default: env SWEBOK_PROVIDER or 'deterministic')")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--dossier-only", action="store_true", help="Just print the dossier, don't call the LLM")
    args = parser.parse_args()
    # Build the dossier
    router = Router()
    dossier = router.dossier(args.query, top_k=args.top_k)
    print(f"# Dossier for: {args.query}\n")
    print(f"Stats: {dossier.stats()}\n")
    if args.dossier_only:
        print(dossier.to_prompt(max_tokens=10000))
        return 0
    # Call the LLM
    try:
        provider = create_provider(args.provider)
    except (ImportError, EnvironmentError) as e:
        print(f"[{args.provider or 'deterministic'}] not available: {e}", file=sys.stderr)
        print("Falling back to deterministic (no LLM call)", file=sys.stderr)
        provider = create_provider("deterministic")
    print(f"Provider: {provider.name}\n")
    response = provider.answer_with_dossier(dossier, args.query)
    print("# Answer\n")
    print(response)
    return 0


if __name__ == "__main__":
    sys.exit(main())
