"""Command-line entry point, so the jobs in schedule.json can actually run.

    python -m agents.seo daily          latest snapshot + repair the last 10 days
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
import time
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


#: Errors that mean "the network wasn't up yet", not "something is wrong".
#: The scheduled runs fire as the laptop wakes, often before Wi-Fi connects.
TRANSIENT = ("TransportError", "TimeoutError", "timed out", "Unable to find the server",
             "ConnectionError", "ConnectionResetError", "10060", "getaddrinfo")
RETRIES = 3
RETRY_WAIT = 120  # seconds; long enough for a waking laptop to join Wi-Fi

#: How far back the daily job re-checks. Search Console revises recent days
#: for a while, and a day fetched too early stores a zero that is wrong.
HEAL_DAYS = 10
#: The most recent days are re-fetched even when they hold data, because
#: Google is still adding to them.
SETTLING_DAYS = 3


def _transient(report: RunReport) -> bool:
    return not report.ok and any(t in e for e in report.errors for t in TRANSIENT)


def _with_retry(job, sleep=time.sleep):
    """Run a job; if it failed only because the network was down, wait and retry."""
    report = job()
    for attempt in range(2, RETRIES + 1):
        if not _transient(report):
            break
        print(f"  network not ready ({report.errors[0][:80]}); retry {attempt}/{RETRIES} "
              f"in {RETRY_WAIT}s")
        sleep(RETRY_WAIT)
        report = job()
    return report


def _resync(gsc: SearchConsoleSource, days: int, settling: int = 0) -> tuple[int, int, int, int]:
    """Fetch every day in the window that is missing, empty, or still settling.

    Returns (written, skipped, empty, failed).
    """
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
    written = skipped = empty = failed = 0
    for i in range(days):
        day = end - timedelta(days=i)
        if day.isoformat() in have and i >= settling:
            skipped += 1
            continue
        report = daily_snapshot(day=day, gsc=gsc, compare=False)
        if not report.ok:
            print(f"  {day}: failed — {report.errors[:1]}")
            failed += 1
            continue
        if report.queries_processed == 0 and report.pages_processed == 0:
            empty += 1
        written += 1
    return written, skipped, empty, failed


def daily() -> int:
    """Yesterday-but-one's snapshot, then repair the last ten days.

    The repair is what makes a missed morning harmless: if the laptop was
    asleep, offline, or the window got closed, the next run that succeeds
    fills the gap from Google instead of leaving a hole in the history.
    """
    report = _with_retry(daily_snapshot)
    code = _print(report)
    if not report.ok:
        return code
    gsc = SearchConsoleSource()
    written, skipped, empty, failed = _resync(gsc, HEAL_DAYS, SETTLING_DAYS)
    print(f"  history: {written} days refreshed, {skipped} already complete"
          + (f", {empty} still empty" if empty else "")
          + (f", {failed} failed" if failed else ""))
    return 1 if failed else 0


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
    written, skipped, empty, failed = _resync(gsc, days)
    print(f"backfill: {written} days written, {skipped} already present, "
          f"{empty} of the written days had no data (normal before the site ranked)"
          + (f", {failed} failed" if failed else ""))
    return 1 if failed else 0


def status() -> int:
    for row in source_status():
        mark = "ok " if row["available"] == "yes" else "-- "
        print(f"  {mark}{row['source']}" + (f"  ({row['reason']})" if row["reason"] else ""))
    return 0


def main(argv: list[str]) -> int:
    # Redirected to schedule.log, Windows hands Python a cp1252 stdout, and
    # the first "→" or "—" raised UnicodeEncodeError after the work was done.
    # That is why the weekly job had never once finished.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    job = (argv[1] if len(argv) > 1 else "status").lower()
    if job in ("daily", "seo-daily"):
        return daily()
    if job in ("health", "seo-health"):
        return _print(_with_retry(health_check))
    if job in ("weekly", "opportunities", "seo-opportunities"):
        return _print(_with_retry(weekly_opportunities))
    if job == "backfill":
        return backfill(int(argv[2]) if len(argv) > 2 else 60)
    if job == "status":
        return status()
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
