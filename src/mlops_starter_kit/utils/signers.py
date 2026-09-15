"""Model signature helpers."""

from __future__ import annotations

from typing import Any


def model_signature(
    features: Any, predictions: list[object] | None = None
) -> dict[str, object]:
    """Return a compact schema signature for dataframe-like inputs."""
    signature: dict[str, object] = {
        "inputs": list(getattr(features, "columns", [])),
        "rows": len(features),
    }
    if predictions is not None:
        signature["outputs"] = {"rows": len(predictions), "type": "prediction"}
    return signature
