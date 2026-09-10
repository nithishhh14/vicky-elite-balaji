"""Scraper Agent — Google Maps + Google Search lead harvest."""
from __future__ import annotations

from typing import Any

import lead_agent as hunter
import shared_memory as mem


def run_scraper() -> dict[str, Any]:
    found, notes = hunter.run_harvest()
    phones = sum(1 for x in found if x.get("phone"))
    return {
        "agent": "scraper",
        "ok": True,
        "leads": found,
        "count": len(found),
        "phones": phones,
        "notes": notes,
        "message": f"Scraper finished: {len(found)} leads ({phones} with phone). {notes}",
    }


def optimize_leads(ws, incoming: list[dict[str, str]] | None = None) -> dict[str, Any]:
    total = mem.optimize_sheet(ws, incoming)
    return {
        "agent": "scraper",
        "ok": True,
        "total": total,
        "message": f"Lead ledger optimized — {total} clean row(s), phone-first.",
    }
