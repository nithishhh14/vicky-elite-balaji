"""Client-ready scrape: wipe Sheet1, harvest, write phone-first ledger."""
from __future__ import annotations

import sys
import shared_memory as mem
from agents import scraper_agent

# Windows consoles often can't print checkmarks
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    print("Vicky Scraper Agent - live harvest for Elite Balaji")
    book = mem.open_sheet()
    ws = mem.worksheet(book, "Sheet1", mem.LEAD_HEADERS)
    ws.clear()
    ws.update(values=[mem.LEAD_HEADERS], range_name="A1:G1")
    print("Sheet1 cleared to headers.")

    result = scraper_agent.run_scraper()
    print(result.get("notes") or result.get("message"))
    leads = result.get("leads") or []
    print(f"Captured {len(leads)} | phones {result.get('phones')}")
    for row in leads[:30]:
        print(
            f"  - {row.get('name')} | {row.get('phone') or '-'} | "
            f"{row.get('city')} | {row.get('source')}"
        )

    opt = scraper_agent.optimize_leads(ws, leads)
    print(opt.get("message"))

    rows = ws.get_all_values()
    phone_n = sum(1 for r in rows[1:] if len(r) > 1 and str(r[1]).strip())
    print(f"SHEET READY -> {len(rows)-1} rows | {phone_n} with phone")
    print("Preview:")
    for r in rows[:20]:
        padded = (r + [""] * 7)[:6]
        print(" | ".join(str(x) for x in padded))
    mem.log_council(book, "scraper", "client_harvest", opt.get("message", ""))


if __name__ == "__main__":
    main()
