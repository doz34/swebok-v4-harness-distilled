# Adversarial Loop Library for swebok-v4-harness
"""
Per Fowler (2026) "Harness engineering for coding agent users":
- Feedforward controls (guides) — prevent issues before they happen
- Feedback controls (sensors) — detect and self-correct after
- Computational (deterministic) vs Inferential (LLM-judge) controls
- Steering loop — human improves the harness when issues repeat
- Keep quality left — feedback sensors as early as possible

Per swebok spec (10-phase + P10):
- Each phase has a spec with explicit missions, deliverables, verdicts
- Council Bridge (4 simulated reviewers: ciso, qa-lead, architect, devops-lead)
- DSL output: KEY:VALUE;;KEY:VALUE (compressed)
- Adversarial loop runs at each phase boundary: entry → in-loop → exit
- Stop conditions are mechanical (time, tokens, value) not emotional
- No Docker, no external deps — bash + Python stdlib only
"""
__version__ = "0.1.0-2026-06-09"
