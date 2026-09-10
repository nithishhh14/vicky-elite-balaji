# Vicky — Work Plan

Locked build order (from `.cursor/rules/vicky-council.mdc`): ship working
agents + shared memory first, then the website, then marketing/SEO, then
executive personality, then the final interface. Do not skip ahead.

## Phase 1 — Scraper & shared memory: LIVE
- `lead_agent.py` harvests from Google Maps + Search, `shared_memory.py`
  cleans/dedupes into the shared Google Sheet.
- Status: working. Not blocking anything else.

## Phase 2 — Website: IN PROGRESS
What exists: `index.html`, 8 hall pages (tiles, granite-marbles,
sanitaryware, quartz, kadappa, kota-stone, adhesive, laying-works),
`catalogue_extract/` with 91 images already pulled from source PDFs.

Next steps, in order:
1. Confirm every hall page actually pulls its images from
   `catalogue_extract/` (some may still be placeholder/Unsplash stock —
   audit `index.html`'s hero image, which is currently a stock Unsplash
   photo, not a real product shot).
2. Wire `website/catalogues/DROP_HERE.md` workflow — decide if
   `_extract_catalogues.py` needs to run again for any new PDFs before
   go-live.
3. Pick hosting (Netlify/Vercel/GitHub Pages are all fine for a static
   site with no backend needs yet) and get a real domain or subdomain live.
4. Once live and reachable at a public URL, Marketing and Email agents
   unblock automatically (they're gated on this, not on code).

## Phase 3 — Marketing + SEO: BLOCKED on Phase 2
- `seo_agent.py` is already functional (writes to `SEO_Audits` sheet) —
  it just has less to work with until the site exists.
- `marketing_agent.py` is a stub by design — do not build it out until
  the site is live, per the locked build order.

## Phase 4 — Executive personality: NOT STARTED
- `vicky_executive.py`'s default chat path works but has no distinct
  personality/voice defined yet beyond the system prompt in
  `handle_command()`.

## Phase 5 — Final interactive interface: NOT STARTED
- Today's Streamlit dashboard (`app.py`) is explicitly a temporary
  workbench, not the final UI, per the locked plan.

## Standing technical debt (not phase-blocking, do when convenient)
- `archive/elite_balaji_scraper.py` — confirm it's safe to delete outright
  once you're sure nothing references it (nothing does as of this review).
- Google Sheet ID and Gemini model name are hardcoded in `shared_memory.py`
  — fine for now, worth moving to `.env` if this ever needs to run against
  more than one sheet/client.
