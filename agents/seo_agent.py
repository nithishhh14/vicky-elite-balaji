"""SEO Agent — evidence-driven monitoring and recommendation.

The real work lives in the `agents.seo` package; this module is the face the
rest of Vicky already knows. `run_seo()` keeps the signature the executive
router has always called, so nothing upstream had to change — but it now
answers from measured Search Console data instead of from a language model's
impression of what a keyword might be worth.

What this agent cannot do, by construction: edit the website, touch git, or
publish anything. Its only output channel for a change is
`vicky_store.create_approval`, and a person decides from there.
"""
from __future__ import annotations

from typing import Any

import shared_memory as mem
import vicky_store as store

from agents.seo import (
    daily_snapshot,
    health_check,
    run_all,
    source_status,
    weekly_opportunities,
)
from agents.seo.analysis import MIN_IMPRESSIONS, has_local_intent, match_page
from agents.seo.jobs import _targets
from agents.seo.sources import SearchConsoleSource

__all__ = [
    "run_seo", "run_daily", "run_health", "run_weekly", "run_all",
    "source_status", "status_line",
]


def run_daily(**kw) -> dict[str, Any]:
    return _wrap(daily_snapshot(**kw))


def run_health(**kw) -> dict[str, Any]:
    return _wrap(health_check(**kw))


def run_weekly(**kw) -> dict[str, Any]:
    return _wrap(weekly_opportunities(**kw))


def status_line() -> str:
    """One sentence on what the agent can currently see."""
    rows = source_status()
    live = [r["source"] for r in rows if r["available"] == "yes"]
    missing = [f"{r['source']} ({r['reason']})" for r in rows if r["available"] == "no"]
    parts = [f"Live sources: {', '.join(live) or 'none'}."]
    if missing:
        parts.append("Not connected: " + "; ".join(missing) + ".")
    return " ".join(parts)


def run_seo(keyword: str) -> dict[str, Any]:
    """Answer a keyword question from real data, or say we have none.

    Kept for the executive's `seo <keyword>` intent. Where the old version
    asked Gemini to imagine demand, this reports what Search Console actually
    recorded for queries containing the term — and says so plainly when the
    answer is "nothing yet", which for a young property is the honest one.
    """
    term = mem.clean(keyword)
    if not term:
        return {"agent": "seo", "ok": False, "message": "Give SEO a keyword first."}

    gsc = SearchConsoleSource()
    ok, reason = gsc.available()
    if not ok:
        store.log_run("seo", f"lookup {term}", False, reason)
        return {
            "agent": "seo", "ok": False,
            "message": f"Search Console is not reachable, so I have no data for “{term}”. {reason}",
        }

    from datetime import date, timedelta
    end = date.today() - timedelta(days=2)
    start = end - timedelta(days=27)
    try:
        rows = gsc.query(start, end, ["query"], row_limit=500)
    except Exception as exc:  # surfaced, never silently emptied
        store.log_run("seo", f"lookup {term}", False, str(exc)[:200])
        return {"agent": "seo", "ok": False, "message": f"Search Console query failed: {exc}"}

    needle = term.lower()
    hits = [r for r in rows if needle in r.get("query", "").lower()]
    store.log_run("seo", f"lookup {term}", True, f"{len(hits)} matching queries")

    if not hits:
        msg = (
            f"No Search Console impressions for anything containing “{term}” in the last 28 days.\n"
            f"That is a measurement, not an opinion — the property is new and most queries "
            f"have not appeared yet. I will not invent demand figures for it."
        )
        return {"agent": "seo", "ok": True, "analysis": msg, "message": msg}

    hits.sort(key=lambda r: r["impressions"], reverse=True)
    targets = _targets()
    lines = [f"Search Console, last 28 days, queries containing “{term}”:", ""]
    for row in hits[:10]:
        page, score = match_page(row["query"], targets)
        local = has_local_intent(row["query"])
        lines.append(
            f"· “{row['query']}” — {row['impressions']} impressions, {row['clicks']} clicks, "
            f"position {row['position']:.1f}"
            + (f", page: {page}" if score >= 0.5 else ", no page targets this")
            + (f" [{local}]" if local else "")
        )
    total_impr = sum(r["impressions"] for r in hits)
    lines += ["", f"{len(hits)} queries, {total_impr} impressions in total."]
    if total_impr < MIN_IMPRESSIONS:
        lines.append(
            f"Below the {MIN_IMPRESSIONS}-impression threshold, so I am not recommending "
            "an action on it yet."
        )
    text = "\n".join(lines)

    # Mirror to the Sheet the council already reads, best-effort.
    try:
        book = mem.open_sheet()
        ws = mem.worksheet(book, "SEO_Audits", mem.SEO_HEADERS)
        ws.append_row([mem.stamp(), term, text], value_input_option="USER_ENTERED")
        mem.log_council(book, "seo", "lookup", f"keyword={term}, {len(hits)} queries")
    except Exception as exc:
        return {"agent": "seo", "ok": True, "analysis": text, "message": text, "warn": str(exc)[:200]}
    return {"agent": "seo", "ok": True, "analysis": text, "message": text}


def _wrap(report) -> dict[str, Any]:
    return {
        "agent": "seo",
        "ok": report.ok,
        "job": report.job,
        "message": f"{report.job}: {report.headline()}",
        "report": report.to_dict(),
    }
