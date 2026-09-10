"""Email Agent — drafts only after website + marketing; human approve before send."""
from __future__ import annotations

from typing import Any


def run_email(brief: str = "") -> dict[str, Any]:
    return {
        "agent": "email",
        "ok": False,
        "blocked": True,
        "message": (
            "Email Agent is queued after Marketing. Drafts only — never auto-send. "
            "It will read shared lead phones from Sheet1 and brand voice from the website."
        ),
    }
