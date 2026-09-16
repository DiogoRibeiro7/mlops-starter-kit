"""Search utilities for starter tuning workflows."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


def grid_search(
    candidates: Iterable[dict[str, Any]],
    score: Callable[[dict[str, Any]], float],
) -> dict[str, Any]:
    """Return the candidate with the highest score."""
    best_candidate: dict[str, Any] | None = None
    best_score: float | None = None
    for candidate in candidates:
        value = score(candidate)
        if best_score is None or value > best_score:
            best_score = value
            best_candidate = dict(candidate)
    if best_candidate is None:
        raise ValueError("at least one candidate is required")
    best_candidate["score"] = best_score
    return best_candidate
