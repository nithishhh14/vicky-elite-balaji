# Vicky — Work Plan

Locked build order (from `.cursor/rules/vicky-council.mdc`): ship working
agents + shared memory first, then the website, then marketing/SEO, then
executive personality, then the final interface. Do not skip ahead.

## Phase 1 — Scraper & shared memory: LIVE
- `lead_agent.py` harvests from Google Maps + Search, `shared_memory.py`
  cleans/dedupes into the shared Google Sheet.
- Status: working. Not blocking anything else.

## Phase 2 — Website: IN PROGRESS (rebuilt on Astro, 2026-09-10)
Rebuilt from the original static HTML/CSS shell (which had 3 of 8 hall pages
as empty files, and a dark-marble theme explicitly marked temporary) into an
Astro 5 + TypeScript + Tailwind v4 site with content collections. See
`docs/WEBSITE_ARCHITECTURE.md` for the full picture, and
`docs/PROJECT_STATE.md` for the verified, detailed current-state snapshot.
Build (`npm run build`) and typecheck (`astro check`) both pass; browser-QA'd
at desktop/tablet/mobile.

**DONE:** homepage; `/halls/` index; all 8 hall pages (Tiles has a real
7-series product grid sourced from `catalogue_extract/`; the other 7 use the
`MaterialField` colour/texture placeholder); `/about/`; `/contact/`
(WhatsApp-prefilled enquiry form, no backend); sitemap + robots.txt; JSON-LD
local business schema; git repo initialized (no remote yet).

**PENDING CLIENT:** any design/content feedback at all — see
`docs/CLIENT_PREFERENCES.md` (every section currently marked "PENDING CLIENT
INPUT"). Treat the current visual design as a draft until reviewed.

**BLOCKED:**
- Real photography for Granite & Marbles, Kota Stone, Kadappa, Sanitaryware,
  Adhesive & Accessories, Quartz — needs the client to supply photos or
  approve a shoot. `docs/WEBSITE_ARCHITECTURE.md` §3 explains how to wire a
  photo in once it exists (flip `hasRealContent` in that hall's JSON).
- Domain + hosting — needs a decision (Cloudflare Pages recommended, free
  tier) and possibly a paid domain purchase, which needs explicit go-ahead.
  `astro.config.mjs`'s `site` and `public/robots.txt` still have a
  placeholder hostname (`elitebalaji.example.in`) that needs replacing
  together, in the same change, once a real domain is chosen.
- GitHub remote — none exists yet (repo was `git init`'d locally only).

**NEXT:**
1. Client review round → update `docs/CLIENT_PREFERENCES.md` with real feedback.
2. Real photography sourcing (see Blocked, above).
3. Domain/hosting decision, then create the GitHub remote and connect
   Cloudflare Pages' git-based deploy.
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
