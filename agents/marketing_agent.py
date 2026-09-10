"""Marketing Agent — deferred until public website exists."""
from __future__ import annotations

from typing import Any


def run_marketing(brief: str = "") -> dict[str, Any]:
    return {
        "agent": "marketing",
        "ok": False,
        "blocked": True,
        "message": (
            "Marketing Agent is waiting for Phase 2 — the Elite Balaji public website. "
            "After the site ships, I will write campaigns from shared lead memory + brand pages. "
            "No pitches are stored on the lead ledger."
        ),
    }
