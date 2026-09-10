# Vicky — Work Plan

Locked build order (from `.cursor/rules/vicky-council.mdc`): ship working
agents + shared memory first, then the website, then marketing/SEO, then
executive personality, then the final interface. Do not skip ahead.

## Phase 1 — Scraper & shared memory: LIVE
- `lead_agent.py` harvests from Google Maps + Search, `shared_memory.py`
  cleans/dedupes into the shared Google Sheet.
- Status: working. Not blocking anything else.

## Phase 2 — Website: IN PROGRESS (rebuilt on Astro)
Rebuilt from the original static HTML/CSS shell (which had 3 of 8 hall pages
as empty files, and a dark-marble theme explicitly marked temporary) into an
Astro 5 + TypeScript + Tailwind v4 site with content collections. See
`docs/WEBSITE_ARCHITECTURE.md` for the full picture. Build (`npm run build`)
and typecheck (`astro check`) both pass; browser-QA'd at desktop/tablet/mobile.

What exists now: homepage, `/halls/` index, all 8 hall pages (Tiles has a real
7-series product grid sourced from `catalogue_extract/`; the other 7 use the
`MaterialField` colour/texture placeholder pending real photos), `/about/`,
`/contact/` (WhatsApp-prefilled enquiry form, no backend), sitemap + robots.txt,
JSON-LD local business schema.

Next steps, in order:
1. Get real photography for Granite & Marbles, Kota Stone, Kadappa,
   Sanitaryware, Adhesive & Accessories, Quartz — the biggest remaining gap.
   `docs/WEBSITE_ARCHITECTURE.md` §3 explains how to wire a photo in once it
   exists (flip `hasRealContent` in that hall's JSON).
2. Pick a domain and hosting (Cloudflare Pages recommended, free tier) —
   `astro.config.mjs`'s `site` and `public/robots.txt` still have a
   placeholder hostname (`elitebalaji.example.in`) that needs replacing
   together, in the same change, once a real domain is chosen.
3. Create the GitHub remote (none exists yet — repo was `git init`'d locally
   during the rebuild) and connect it for Cloudflare Pages' git-based deploy.
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
