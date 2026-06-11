"""Compatibility helper for sibling state_engine modules.

Sibling modules (state_engine_audit, state_engine_counters, state_engine_logging,
state_engine_prune, state_engine_recovery, state_engine_export) historically each
defined their own private ``_se()`` lazy accessor — an identical 14-line
boilerplate that returns the ``state_engine`` module without triggering a
circular import at module-load time.

This module consolidates that pattern into a single ``get_se()`` factory
(plus the underscored ``_se`` alias for backward compatibility with the
existing call sites). All 6 sibling modules import from here, eliminating
6× duplication and ensuring any future change (e.g. error message, fallback
strategy) lands in one place.

Why a lazy accessor?
    state_engine.py re-exports the sibling modules' public symbols. If the
    siblings imported state_engine at module-load time, and state_engine
    re-imports them, Python's import system handles that with a partial
    module object — but it surfaces a chicken-and-egg problem when one
    sibling's module body calls ``state_engine.foo()``. Lazy access defers
    the lookup until the call site runs, by which time state_engine is
    fully loaded.
"""

from __future__ import annotations

import sys
from types import ModuleType


def get_se() -> ModuleType:
    """Return the ``state_engine`` module without triggering a circular import.

    The lookup order is:
      1. ``sys.modules['state_engine']`` — already loaded; the normal case
         when imported through state_engine.py (which re-exports sibling symbols).
      2. ``__import__('state_engine')`` — fallback for direct invocation
         (e.g. ``python3 -m state_engine_counters``).
      3. ``ImportError`` with an actionable message — never a silent
         ``None`` or a wrong module.
    """
    mod = sys.modules.get("state_engine")
    if mod is not None:
        return mod
    try:
        return __import__("state_engine")
    except ImportError as exc:
        raise ImportError(
            "state_engine module not found. This sibling module must be "
            "imported through state_engine.py (which re-exports our symbols), "
            "not directly."
        ) from exc


# Underscore-prefixed alias preserving the original 6× boilerplate's
# call-site shape: ``from state_engine_compat import _se`` then
# ``state_engine = _se()``.
_se = get_se


__all__ = ["get_se", "_se"]
