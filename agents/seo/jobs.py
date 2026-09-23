"""The three scheduled jobs, exactly as specified in vicky_data/config/schedule.json.

Each one: gathers from whatever sources are available, records what it did,
and stops. The only thing a job can create is a *proposal*. Nothing here edits
the website, touches git, or publishes anything — that separation is what the
approvals queue is for, and there is a test asserting this module never
imports the machinery to break it.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import vicky_store as store

from .analysis import MIN_IMPRESSIONS, analyse
from .model import Confidence, Finding, Opportunity, Provenance, RunReport, Severity
from .sources import (
    SearchConsoleSource,
    SourceUnavailable,
    WebsiteCrawlSource,
    default_registry,
)

AGENT = "seo"

#: Title/description limits the website's own deploy gate enforces. Repeated
#: here so a drift finding uses the same numbers the build would fail on.
TITLE_MIN, TITLE_MAX = 10, 65
DESC_MIN, DESC_MAX = 50, 160

#: Pages sampled by the health check when Search Console has nothing to say.
HEALTH_SAMPLE = 8


def _targets() -> list[dict[str, Any]]:
    """The tracked pages, from the committed config. Never hardcoded here."""
    cfg = store.config("seo_targets", {}) or {}
    return list(cfg.get("core", [])) + list(cfg.get("landing", []))


def _site_origin() -> str:
    cfg = store.config("seo_targets", {}) or {}
    return (cfg.get("site") or "https://elitebalaji.com").rstrip("/")


def _finish(report: RunReport, detail: str = "") -> RunReport:
    report.finished = store.now()
    store.log_run(AGENT, report.job, report.ok, detail or report.headline())
    return report


# ─────────────────────────── 1. daily snapshot ───────────────────────────

def daily_snapshot(day: date | None = None, window_days: int = 1,
                   gsc: SearchConsoleSource | None = None) -> RunReport:
    """One Search Console snapshot per day, stored forever.

    Search Console keeps 16 months. We keep everything, because a trend we can
    compute ourselves is the only trend we can be sure of.
    """
    report = RunReport(job="seo-daily", started=store.now())
    gsc = gsc or SearchConsoleSource()

    ok, reason = gsc.available()
    if not ok:
        report.ok = False
        report.sources_unavailable.append(f"google_search_console ({reason})")
        report.errors.append(f"Search Console unavailable: {reason}")
        return _finish(report, reason)
    report.sources_used.append("google_search_console")

    target_day = day or (date.today() - timedelta(days=2))  # GSC lags ~2 days
    start = target_day - timedelta(days=window_days - 1)

    try:
        totals = gsc.query(start, target_day)
        queries = gsc.query(start, target_day, ["query"], row_limit=500)
        pages = gsc.query(start, target_day, ["page"], row_limit=500)
    except SourceUnavailable as exc:
        report.ok = False
        report.errors.append(str(exc))
        return _finish(report, str(exc))

    total = totals[0] if totals else {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
    tracked = {t["path"] for t in _targets()}
    origin = _site_origin()

    record = {
        "totals": {
            "clicks": total.get("clicks", 0),
            "impressions": total.get("impressions", 0),
            "ctr": round(float(total.get("ctr", 0.0)), 4),
            "position": round(float(total.get("position", 0.0)), 1),
        },
        "queries": queries[:100],
        "pages": pages[:100],
        "trackedPages": [
            p for p in pages
            if p.get("page", "").replace(origin, "") in tracked
        ],
        "window": {"start": start.isoformat(), "end": target_day.isoformat(), "days": window_days},
        "provenance": Provenance.GOOGLE_CONFIRMED.value,
        "flags": [],
    }

    # A drop is only meaningful against our own stored history.
    previous = store.latest_seo()
    if previous and previous.get("date") != target_day.isoformat():
        before = (previous.get("totals") or {}).get("impressions", 0)
        after = record["totals"]["impressions"]
        if before >= 20 and after < before * 0.6:
            record["flags"].append(
                f"Impressions fell from {before} to {after} versus {previous.get('date')}."
            )

    if not queries and not pages:
        record["flags"].append(
            "Search Console returned no rows for this window. Normal for a new property."
        )
        report.findings.append(Finding(
            code="seo.no_data", title="No Search Console rows yet",
            detail=f"No data for {start} to {target_day}. The property is new; this is expected.",
            provenance=Provenance.GOOGLE_CONFIRMED, severity=Severity.INFO,
        ))

    store.save_seo_day(target_day, record)
    report.queries_processed = len(queries)
    report.pages_processed = len(pages)
    for flag in record["flags"]:
        report.findings.append(Finding(
            code="seo.flag", title="Change worth a look", detail=flag,
            provenance=Provenance.GOOGLE_CONFIRMED, severity=Severity.WARNING,
        ))
    return _finish(report, f"{report.queries_processed} queries, {report.pages_processed} pages")


# ──────────────────────────── 2. health check ────────────────────────────

def health_check(gsc: SearchConsoleSource | None = None,
                 crawl: WebsiteCrawlSource | None = None,
                 sample: int = HEALTH_SAMPLE) -> RunReport:
    """The silent breakages: a page that 404s, a canonical pointing elsewhere,
    a title that drifted past the limit, a price that appeared.

    Findings are split by provenance — what Google told us versus what we
    observed ourselves — because the two carry different weight.
    """
    report = RunReport(job="seo-health", started=store.now())
    gsc = gsc or SearchConsoleSource()
    crawl = crawl or WebsiteCrawlSource(_site_origin())

    # ---- Google's own view: sitemap status
    ok, reason = gsc.available()
    if ok:
        report.sources_used.append("google_search_console")
        try:
            for sm in gsc.sitemaps():
                errors = int(sm.get("errors", 0) or 0)
                warnings = int(sm.get("warnings", 0) or 0)
                never_read = not sm.get("lastDownloaded")
                if errors or warnings or never_read:
                    report.findings.append(Finding(
                        code="seo.sitemap",
                        title="Sitemap needs attention",
                        detail=(f"{sm.get('path')}: {errors} errors, {warnings} warnings, "
                                f"last downloaded {sm.get('lastDownloaded', 'never')}."),
                        provenance=Provenance.GOOGLE_CONFIRMED,
                        severity=Severity.CRITICAL if errors else Severity.WARNING,
                        url=sm.get("path", ""),
                    ))
                else:
                    report.findings.append(Finding(
                        code="seo.sitemap_ok", title="Sitemap healthy",
                        detail=f"{sm.get('path')} read {sm.get('lastDownloaded')}, no errors.",
                        provenance=Provenance.GOOGLE_CONFIRMED, url=sm.get("path", ""),
                    ))
        except SourceUnavailable as exc:
            report.errors.append(str(exc))
    else:
        report.sources_unavailable.append(f"google_search_console ({reason})")

    # ---- our own view: fetch the pages and look
    ok, reason = crawl.available()
    if not ok:
        report.ok = False
        report.sources_unavailable.append(f"website_crawl ({reason})")
        report.errors.append(f"Site unreachable: {reason}")
        return _finish(report)
    report.sources_used.append("website_crawl")

    origin = _site_origin()
    targets = _targets()[:sample]
    for target in targets:
        path = target.get("path", "/")
        try:
            page = crawl.fetch(path)
        except SourceUnavailable as exc:
            report.errors.append(str(exc))
            continue
        report.pages_processed += 1
        url = f"{origin}{path}"

        if page["status"] != 200:
            report.findings.append(Finding(
                code="seo.http_status", title=f"{path} returned {page['status']}",
                detail=(f"Expected 200, got {page['status']}. This path is in the tracked list "
                        f"(vicky_data/config/seo_targets.json); either the page moved or the list is stale."),
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.CRITICAL, url=url,
            ))
            continue

        html = page["body"]
        title = crawl.title_of(html)
        desc = crawl.description_of(html)
        canonical = crawl.canonical_of(html)
        robots_meta = crawl.robots_meta_of(html)

        if not (TITLE_MIN <= len(title) <= TITLE_MAX):
            report.findings.append(Finding(
                code="seo.title_drift", title=f"{path} title is {len(title)} characters",
                detail=f"Outside the {TITLE_MIN}–{TITLE_MAX} range the deploy gate enforces: “{title}”",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.WARNING, url=url,
            ))
        if not (DESC_MIN <= len(desc) <= DESC_MAX):
            report.findings.append(Finding(
                code="seo.description_drift", title=f"{path} description is {len(desc)} characters",
                detail=f"Outside the {DESC_MIN}–{DESC_MAX} range the deploy gate enforces.",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.WARNING, url=url,
            ))
        if canonical and canonical.rstrip("/") != url.rstrip("/"):
            report.findings.append(Finding(
                code="seo.canonical_mismatch", title=f"{path} points its canonical elsewhere",
                detail=f"Canonical is {canonical}, page is {url}. Intentional for a duplicate, wrong otherwise.",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.WARNING, url=url,
            ))
        if not canonical:
            report.findings.append(Finding(
                code="seo.canonical_missing", title=f"{path} has no canonical tag",
                detail="Without one, www and apex can be indexed as separate pages.",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.WARNING, url=url,
            ))
        if "noindex" in robots_meta:
            report.findings.append(Finding(
                code="seo.noindex", title=f"{path} is set to noindex",
                detail="A page in the sitemap telling Google not to index it.",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.CRITICAL, url=url,
            ))
        # The project's own hard rule, checked on the live site rather than the build.
        if _looks_like_a_price(html):
            report.findings.append(Finding(
                code="seo.price_published", title=f"{path} appears to show a price",
                detail="Publishing prices is not allowed on this site. Verify and remove.",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.CRITICAL, url=url,
            ))

    # ---- robots.txt and sitemap reachability, observed by us
    try:
        robots = crawl.fetch("/robots.txt")
        if robots["status"] != 200:
            report.findings.append(Finding(
                code="seo.robots", title=f"robots.txt returned {robots['status']}",
                detail="Crawlers read this first.", provenance=Provenance.CRAWL_OBSERVED,
                severity=Severity.CRITICAL, url=f"{origin}/robots.txt",
            ))
        elif "Sitemap:" not in robots["body"]:
            report.findings.append(Finding(
                code="seo.robots_sitemap", title="robots.txt does not point at the sitemap",
                detail="A second route for Google to discover every page.",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.WARNING,
            ))
        sm = crawl.fetch("/sitemap-index.xml")
        if sm["status"] != 200:
            report.findings.append(Finding(
                code="seo.sitemap_fetch", title=f"sitemap-index.xml returned {sm['status']}",
                detail="We serve this ourselves; it must be reachable.",
                provenance=Provenance.CRAWL_OBSERVED, severity=Severity.CRITICAL,
            ))
    except SourceUnavailable as exc:
        report.errors.append(str(exc))

    report.ok = not any(f.severity is Severity.CRITICAL for f in report.findings)

    # Persist onto today's snapshot so the dashboard shows health beside traffic.
    today_record = store.latest_seo() or {}
    if today_record.get("date") == date.today().isoformat():
        today_record["health"] = {
            "checked": report.pages_processed,
            "critical": sum(1 for f in report.findings if f.severity is Severity.CRITICAL),
            "warnings": sum(1 for f in report.findings if f.severity is Severity.WARNING),
        }
        store.save_seo_day(today_record["date"], today_record)

    return _finish(report)


def _looks_like_a_price(html: str) -> bool:
    """Deliberately narrow: a currency marker next to digits in visible text.

    Over-flagging would train the reader to ignore this check, which is worse
    than missing one instance.
    """
    import re
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    return bool(re.search(r"(₹|Rs\.?|INR)\s?\d{2,}", body))


# ───────────────────── 3. weekly opportunity analysis ─────────────────────

def weekly_opportunities(window_days: int = 28, gsc: SearchConsoleSource | None = None,
                         create_approvals: bool = True, max_approvals: int = 5) -> RunReport:
    """Real queries in, evidence-backed proposals out — or an honest nothing.

    Proposals are filed as approvals. They are never applied: this function
    returns, and a person decides.
    """
    report = RunReport(job="seo-opportunities", started=store.now())
    gsc = gsc or SearchConsoleSource()

    ok, reason = gsc.available()
    if not ok:
        report.ok = False
        report.sources_unavailable.append(f"google_search_console ({reason})")
        report.errors.append(f"Search Console unavailable: {reason}")
        return _finish(report, reason)
    report.sources_used.append("google_search_console")

    end = date.today() - timedelta(days=2)
    start = end - timedelta(days=window_days - 1)
    try:
        query_rows = gsc.query(start, end, ["query"], row_limit=500)
        page_rows = gsc.query(start, end, ["page"], row_limit=500)
    except SourceUnavailable as exc:
        report.ok = False
        report.errors.append(str(exc))
        return _finish(report, str(exc))

    report.queries_processed = len(query_rows)
    report.pages_processed = len(page_rows)

    if not query_rows:
        report.findings.append(Finding(
            code="seo.no_queries", title="No queries in the window",
            detail=f"Search Console returned nothing for {start} to {end}. "
                   "Too early for this property — nothing to recommend.",
            provenance=Provenance.GOOGLE_CONFIRMED,
        ))
        return _finish(report, "no query data yet")

    report.opportunities = analyse(query_rows, page_rows, _targets(), window_days)

    actionable = [o for o in report.opportunities if o.actionable]
    held = [o for o in report.opportunities if not o.actionable]
    report.findings.append(Finding(
        code="seo.analysis",
        title=f"{len(actionable)} actionable, {len(held)} held back",
        detail=(f"{len(query_rows)} queries examined over {window_days} days. "
                f"Anything under {MIN_IMPRESSIONS} impressions is recorded but not recommended."),
        provenance=Provenance.INFERRED,
    ))

    if create_approvals:
        for opp in actionable[:max_approvals]:
            approval = store.create_approval(
                kind="seo",
                title=opp.title,
                summary=opp.summary_text(),
                payload=opp.to_dict(),
                requested_by="seo-agent",
            )
            report.approvals_created.append(approval["id"])

    return _finish(report)


def run_all() -> dict[str, RunReport]:
    """Every job, for a manual 'run the SEO agent' from the dashboard."""
    return {
        "daily": daily_snapshot(),
        "health": health_check(),
        "weekly": weekly_opportunities(),
    }


def source_status() -> list[dict[str, str]]:
    """What the agent can and cannot see right now — shown in the dashboard."""
    out = []
    for name, source in default_registry(origin=_site_origin()).items():
        ok, reason = source.available()
        out.append({"source": name, "available": "yes" if ok else "no", "reason": reason})
    return out
