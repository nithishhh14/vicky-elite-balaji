"""Nilgiris pass + drop retail showrooms from Sheet1."""
from __future__ import annotations

import asyncio
import sys

import lead_agent as hunter
import shared_memory as mem
from agents import scraper_agent

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


async def nilgiris_only() -> list[dict[str, str]]:
    pw = browser = context = None
    bag: list[dict[str, str]] = []
    try:
        pw, browser, context = await hunter.open_browser()
        page = await context.new_page()
        queries = [q for q in hunter.MAP_QUERIES if any(x in q.lower() for x in ("ooty", "kotagiri", "nilgiri"))]
        searches = [q for q in hunter.SEARCH_QUERIES if any(x in q.lower() for x in ("ooty", "kotagiri", "nilgiri"))]
        for q in queries:
            got = await hunter.scrape_maps_query(page, q, max_places=8)
            bag.extend(got)
            print(f"Maps {q}: {len(got)} ({sum(1 for x in got if x.get('phone'))} phones)")
        for q in searches:
            got = await hunter.scrape_google_search(page, q)
            bag.extend(got)
            print(f"Search {q}: {len(got)}")
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()
    return hunter.dedupe_leads(bag)


def main() -> None:
    print("1) Strip retail showrooms/shops from current sheet…")
    book = mem.open_sheet()
    ws = mem.worksheet(book, "Sheet1", mem.LEAD_HEADERS)
    before = len(ws.get_all_values()) - 1
    cleaned_n = mem.optimize_sheet(ws)
    print(f"   {before} -> {cleaned_n} contractor/engineer rows")

    print("2) Nilgiris / Ooty / Kotagiri harvest…")
    fresh = asyncio.run(nilgiris_only())
    print(f"   Nilgiris captured: {len(fresh)} ({sum(1 for x in fresh if x.get('phone'))} phones)")
    for row in fresh[:15]:
        print(f"   - {row.get('name')} | {row.get('phone') or '-'} | {row.get('city')}")

    total = mem.optimize_sheet(ws, fresh)
    rows = ws.get_all_values()
    phone_n = sum(1 for r in rows[1:] if len(r) > 1 and str(r[1]).strip())
    nilg = sum(
        1
        for r in rows[1:]
        if any(x in " ".join(r).lower() for x in ("ooty", "kotagiri", "nilgiri", "coonoor"))
    )
    print(f"SHEET READY -> {total} leads | {phone_n} phones | {nilg} Nilgiris-tagged")
    mem.log_council(book, "scraper", "nilgiris_plus_filter", f"total={total} phones={phone_n} nilg={nilg}")


if __name__ == "__main__":
    main()
