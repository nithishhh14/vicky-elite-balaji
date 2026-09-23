"""Turning Search Console rows into opportunities — or refusing to.

Every rule here starts from rows Google returned and stops the moment the
evidence runs out. There is no keyword ideation step, because a keyword we
invented has no impressions behind it and would enter the queue looking
exactly like one that does.

When a pattern is visible but too thin to act on, the rule still emits an
Opportunity — with `Confidence.INSUFFICIENT_EVIDENCE` and the reason. Saying
"three impressions is not a trend yet" is more useful than silence, and far
more useful than a confident guess.
"""
from __future__ import annotations

import re
from typing import Any, Iterable

from .model import Confidence, Evidence, Opportunity, Provenance

#: Below this, a query is noise rather than demand. Deliberately conservative:
#: a brand-new property produces single-impression rows for queries it will
#: never rank for, and acting on those would fill the queue with nonsense.
MIN_IMPRESSIONS = 10

#: Positions worth chasing. Above 3 we are already winning; past 20 the gap is
#: usually content that does not exist rather than a tweak.
STRIKING_MIN, STRIKING_MAX = 4.0, 20.0

#: Modelled click-through by position. INFERRED, never presented as Google's.
#: Used only to ask "is this unusually low for where it sits", never to
#: forecast traffic.
EXPECTED_CTR = {
    1: 0.28, 2: 0.15, 3: 0.11, 4: 0.08, 5: 0.06,
    6: 0.05, 7: 0.04, 8: 0.033, 9: 0.028, 10: 0.025,
}
DEEP_CTR = 0.01  # anything past 10

#: The real service area. A query naming one of these has local intent we can
#: actually serve; anywhere else is not an opportunity, it is a wrong turn.
SERVICE_AREA = [
    "coimbatore", "karamadai", "mettupalayam", "kovai", "annur", "sirumugai",
    "periyanaickenpalayam", "saravanampatti", "thudiyalur", "rs puram",
    "ooty", "kotagiri", "nilgiris", "kallar",
]

#: Words that mean someone is shopping, not reading.
COMMERCIAL_INTENT = [
    "price", "cost", "rate", "buy", "shop", "showroom", "dealer", "supplier",
    "near me", "best", "wholesale",
]


def expected_ctr_at(position: float) -> float:
    """Modelled, not measured. Callers must label it inferred."""
    return EXPECTED_CTR.get(int(round(position)), DEEP_CTR) if position <= 10 else DEEP_CTR


def normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", (text or "").lower()).strip()


def tokens(text: str) -> set[str]:
    return {t for t in normalise(text).split() if len(t) > 2}


def has_local_intent(query: str) -> str:
    q = normalise(query)
    for place in SERVICE_AREA:
        if place in q:
            return place
    return ""


def has_commercial_intent(query: str) -> str:
    q = normalise(query)
    for word in COMMERCIAL_INTENT:
        if word in q:
            return word
    return ""


def match_page(query: str, pages: Iterable[dict[str, Any]]) -> tuple[str, float]:
    """Best existing page for a query, by token overlap with its path/intent.

    Returns ("", 0.0) when nothing we publish addresses the query — which is
    the signal that a page may be missing, not that the matcher is weak.
    """
    q = tokens(query)
    if not q:
        return "", 0.0
    best, best_score = "", 0.0
    for page in pages:
        haystack = tokens(page.get("path", "")) | tokens(page.get("intent", ""))
        for watch in page.get("watch", []):
            haystack |= tokens(watch)
        if not haystack:
            continue
        score = len(q & haystack) / len(q)
        if score > best_score:
            best, best_score = page.get("path", ""), score
    return best, round(best_score, 2)


def _evidence(row: dict[str, Any], window_days: int, matching: str = "",
              expected: float | None = None) -> Evidence:
    return Evidence(
        query=row.get("query", ""),
        page=row.get("page", ""),
        impressions=int(row.get("impressions", 0)),
        clicks=int(row.get("clicks", 0)),
        ctr=float(row.get("ctr", 0.0)),
        position=float(row.get("position", 0.0)),
        matching_page=matching,
        expected_ctr=expected,
        window_days=window_days,
        source=Provenance.GOOGLE_CONFIRMED,
    )


def _thin(row: dict[str, Any], window_days: int, code: str, title: str, reason: str,
          matching: str = "") -> Opportunity:
    """The honest non-recommendation: a pattern seen, deliberately not acted on."""
    return Opportunity(
        code=code,
        title=title,
        what_to_change="Nothing yet — recorded so it can be re-checked as data accumulates.",
        why=reason,
        evidence=_evidence(row, window_days, matching),
        confidence=Confidence.INSUFFICIENT_EVIDENCE,
        limitations=f"Fewer than {MIN_IMPRESSIONS} impressions in {window_days} days.",
        seo_purpose="",
        risks="",
    )


# ────────────────────────────────── rules ──────────────────────────────────

def missing_page_opportunities(query_rows: list[dict[str, Any]], tracked_pages: list[dict[str, Any]],
                               window_days: int) -> list[Opportunity]:
    """Queries earning impressions that no page of ours actually targets."""
    out = []
    for row in query_rows:
        query = row.get("query", "")
        if not query:
            continue
        matching, score = match_page(query, tracked_pages)
        if score >= 0.5:
            continue  # we already have a page for this
        local = has_local_intent(query)
        if not local:
            continue  # outside the service area is not an opportunity
        impressions = int(row.get("impressions", 0))
        if impressions < MIN_IMPRESSIONS:
            out.append(_thin(row, window_days, "seo.missing_page",
                             f"No page targets “{query}”",
                             f"Real impressions for a {local} query we have no page for, "
                             "but too few to justify a page yet.", matching))
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", normalise(query)).strip("-")
        out.append(Opportunity(
            code="seo.missing_page",
            title=f"Landing page for “{query}”",
            what_to_change=(
                f"Add website/src/content/guides/{slug}.json following the recipe in "
                "docs/CONTENT_EDITING.md §2, matched to products we actually stock."
            ),
            why=(f"“{query}” earned {impressions} impressions in {window_days} days at average "
                 f"position {row.get('position', 0):.1f}, and no existing page targets it "
                 f"(closest: {matching or 'none'})."),
            evidence=_evidence(row, window_days, matching),
            affected_file=f"website/src/content/guides/{slug}.json",
            seo_purpose=f"Give a {local} query with demonstrated demand a page written for it.",
            risks=("A new page too close to an existing one can split ranking signals. "
                   "Check it does not cannibalise " + (matching or "an existing landing page") + "."),
            confidence=Confidence.MEDIUM if impressions < MIN_IMPRESSIONS * 3 else Confidence.HIGH,
            limitations="Impressions show demand, not conversion. No keyword-volume source is connected.",
        ))
    return out


def striking_distance_opportunities(query_rows: list[dict[str, Any]], tracked_pages: list[dict[str, Any]],
                                    window_days: int) -> list[Opportunity]:
    """Queries sitting just off the first page, where small gains pay."""
    out = []
    for row in query_rows:
        pos = float(row.get("position", 0.0))
        if not (STRIKING_MIN <= pos <= STRIKING_MAX):
            continue
        impressions = int(row.get("impressions", 0))
        query = row.get("query", "")
        matching, score = match_page(query, tracked_pages)
        if impressions < MIN_IMPRESSIONS:
            out.append(_thin(row, window_days, "seo.striking_distance",
                             f"“{query}” is at position {pos:.0f}",
                             "Within reach of page one, but on too few impressions to act on.",
                             matching))
            continue
        out.append(Opportunity(
            code="seo.striking_distance",
            title=f"“{query}” sits at position {pos:.1f}",
            what_to_change=(f"Strengthen {matching or 'the closest page'}: answer this query "
                            "explicitly in the H1, intro and FAQ rather than in passing."),
            why=(f"{impressions} impressions at position {pos:.1f} over {window_days} days. "
                 "Moving from the second page to the first is where the clicks appear."),
            evidence=_evidence(row, window_days, matching),
            affected_url=matching,
            affected_file=f"website/src/content/guides{matching}.json" if matching.startswith("/") else "",
            seo_purpose="Convert existing impressions into clicks by improving an existing page.",
            risks="Over-optimising for one query can weaken a page for the others it already ranks for.",
            confidence=Confidence.MEDIUM if score >= 0.4 else Confidence.LOW,
            limitations="Position is an average across the window; it may hide a wide spread.",
        ))
    return out


def low_ctr_opportunities(query_rows: list[dict[str, Any]], window_days: int) -> list[Opportunity]:
    """Rankings that are not earning the clicks their position should."""
    out = []
    for row in query_rows:
        impressions = int(row.get("impressions", 0))
        pos = float(row.get("position", 0.0))
        ctr = float(row.get("ctr", 0.0))
        query = row.get("query", "")
        if pos > 10 or impressions == 0:
            continue
        expected = expected_ctr_at(pos)
        if ctr >= expected * 0.6:
            continue  # within the normal band for this position
        if impressions < MIN_IMPRESSIONS:
            out.append(_thin(row, window_days, "seo.low_ctr",
                             f"“{query}” may be under-clicked",
                             "Click-through looks low for the position, on too little data to be sure."))
            continue
        out.append(Opportunity(
            code="seo.low_ctr",
            title=f"“{query}” ranks {pos:.1f} but earns {ctr * 100:.1f}% CTR",
            what_to_change="Rewrite the page's title and meta description so they answer this query directly.",
            why=(f"{impressions} impressions at position {pos:.1f} produced {row.get('clicks', 0)} clicks. "
                 f"A page at that position typically sees around {expected * 100:.0f}%."),
            evidence=_evidence(row, window_days, expected=expected),
            seo_purpose="Earn more clicks from rankings already held — no new ranking needed.",
            risks="Titles must stay within the 10–65 character limit the deploy gate enforces.",
            confidence=Confidence.MEDIUM,
            limitations=("The expected-CTR figure is a modelled heuristic, not Google data. "
                         "Branded and local results legitimately vary from it."),
        ))
    return out


def page_opportunities(page_rows: list[dict[str, Any]], window_days: int) -> list[Opportunity]:
    """Pages collecting impressions without converting them into visits."""
    out = []
    for row in page_rows:
        impressions = int(row.get("impressions", 0))
        clicks = int(row.get("clicks", 0))
        page = row.get("page", "")
        if impressions < MIN_IMPRESSIONS or clicks > 0:
            continue
        out.append(Opportunity(
            code="seo.page_no_clicks",
            title=f"{page} — {impressions} impressions, no clicks",
            what_to_change="Review this page's title, description and intro against what it actually ranks for.",
            why=f"Google showed it {impressions} times in {window_days} days and nobody clicked.",
            evidence=_evidence(row, window_days),
            affected_url=page,
            seo_purpose="Find the mismatch between what the page promises in search and what it is about.",
            risks="None from investigating; any edit still goes through approval and the deploy gate.",
            confidence=Confidence.MEDIUM,
            limitations="Average position for the page is not shown per query here.",
        ))
    return out


def deduplicate(opportunities: list[Opportunity]) -> list[Opportunity]:
    """One opportunity per (code, query-or-url), keeping the best-evidenced.

    Rules overlap on purpose — a query can be both in striking distance and
    under-clicked. The queue should show the strongest version once, not the
    same finding three times wearing different hats.
    """
    best: dict[tuple[str, str], Opportunity] = {}
    order = {Confidence.HIGH: 3, Confidence.MEDIUM: 2, Confidence.LOW: 1,
             Confidence.INSUFFICIENT_EVIDENCE: 0}
    for opp in opportunities:
        key = (opp.code, opp.evidence.query or opp.affected_url or opp.evidence.page)
        current = best.get(key)
        if current is None:
            best[key] = opp
            continue
        if (order[opp.confidence], opp.evidence.impressions) > (order[current.confidence], current.evidence.impressions):
            best[key] = opp
    return sorted(
        best.values(),
        key=lambda o: (order[o.confidence], o.evidence.impressions),
        reverse=True,
    )


def analyse(query_rows: list[dict[str, Any]], page_rows: list[dict[str, Any]],
            tracked_pages: list[dict[str, Any]], window_days: int) -> list[Opportunity]:
    """Every rule, deduplicated. The only entry point jobs should use."""
    found: list[Opportunity] = []
    found += missing_page_opportunities(query_rows, tracked_pages, window_days)
    found += striking_distance_opportunities(query_rows, tracked_pages, window_days)
    found += low_ctr_opportunities(query_rows, window_days)
    found += page_opportunities(page_rows, window_days)
    return deduplicate(found)
