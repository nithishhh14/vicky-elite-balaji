"""Command-line entry point, so the jobs in schedule.json can actually run.

    python -m agents.seo daily          yesterday's snapshot
    python -m agents.seo health         crawl + sitemap check
    python -m agents.seo weekly         opportunity analysis -> approvals
    python -m agents.seo backfill 60    build history from Search Console
    python -m agents.seo status         what the agent can currently see

Exit code is 0 when the job ran and 1 when it did not, so Task Scheduler can
tell a genuine failure from "Search Console had nothing to say today" — the
second is a successful run that found nothing, and must not page anyone.

Output is deliberately plain text on stdout: this is read from a log file at
07:31 by someone who wants to know whether it worked, not parsed.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta

from . import daily_snapshot, health_check, source_status, weekly_opportunities
from .sources import SearchConsoleSource
from .model import RunReport


def _print(report: RunReport) -> int:
    print(f"{report.job}: {report.headline()}")
    print(f"  sources: {', '.join(report.sources_used) or 'none'}")
    for f in report.findings:
        print(f"  [{f.provenance.value}/{f.severity.value}] {f.title} — {f.detail}")
    for o in report.opportunities:
        mark = "→" if o.actionable else "·"
        print(f"  {mark} [{o.confidence.value}] {o.title}")
    if report.approvals_created:
        print(f"  approvals filed: {', '.join(report.approvals_created)}")
    for e in report.errors:
        print(f"  ERROR: {e}")
    return 0 if report.ok else 1


def backfill(days: int = 60) -> int:
    """Build history from what Search Console already holds.

    Without this the agent's trend detection is useless for a month, because
    it only compares against snapshots it took itself. Google has the past
    already; there is no reason to wait for it a second time.

    Days we have are skipped, so this is safe to re-run.
    """
    gsc = SearchConsoleSource()
    ok, reason = gsc.available()
    if not ok:
        print(f"backfill: Search Console unavailable — {reason}")
        return 1

    import vicky_store as store

    # Skip only days we already hold *data* for. Search Console finalises a
    # day late, so a snapshot taken too early stores a legitimate zero that is
    # then wrong forever if "the file exists" is the skip condition. It was:
    # 2026-09-21 sat empty on disk while the API had 25 impressions for it.
    have = set()
    for f in store.SEO_DIR.glob("*.json"):
        rec = store.read_json(f, {}) or {}
        if (rec.get("totals") or {}).get("impressions", 0) > 0:
            have.add(f.stem)
    # Search Console finalises with a ~2 day lag; asking for today returns
    # nothing and would store a misleading zero.
    end = date.today() - timedelta(days=2)
    written = skipped = empty = 0
    for i in range(days):
        day = end - timedelta(days=i)
        if day.isoformat() in have:
            skipped += 1
            continue
        report = daily_snapshot(day=day, gsc=gsc)
        if not report.ok:
            print(f"  {day}: failed — {report.errors[:1]}")
            continue
        if report.queries_processed == 0 and report.pages_processed == 0:
            empty += 1
        written += 1
    print(f"backfill: {written} days written, {skipped} already present, "
          f"{empty} of the written days had no data (normal before the site ranked)")
    return 0


def status() -> int:
    for row in source_status():
        mark = "ok " if row["available"] == "yes" else "-- "
        print(f"  {mark}{row['source']}" + (f"  ({row['reason']})" if row["reason"] else ""))
    return 0


def main(argv: list[str]) -> int:
    job = (argv[1] if len(argv) > 1 else "status").lower()
    if job in ("daily", "seo-daily"):
        return _print(daily_snapshot())
    if job in ("health", "seo-health"):
        return _print(health_check())
    if job in ("weekly", "opportunities", "seo-opportunities"):
        return _print(weekly_opportunities())
    if job == "backfill":
        return backfill(int(argv[2]) if len(argv) > 2 else 60)
    if job == "status":
        return status()
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
