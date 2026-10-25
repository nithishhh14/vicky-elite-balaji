"""Marketing Agent — not built yet; next in the build order (docs/OPERATIONS_PLAN.md)."""
from __future__ import annotations

from typing import Any


def run_marketing(brief: str = "") -> dict[str, Any]:
    return {
        "agent": "marketing",
        "ok": False,
        "blocked": True,
        "message": (
            "Marketing Agent isn't built yet. It is next in the build order; the website "
            "is live, so nothing blocks it. When built it will draft Google Business posts, "
            "Instagram captions and WhatsApp broadcasts for approval, never posting on its own."
        ),
    }
