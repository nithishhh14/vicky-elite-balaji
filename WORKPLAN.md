# Vicky — Work Plan

Locked build order (from `.cursor/rules/vicky-council.mdc`): ship working
agents + shared memory first, then the website, then marketing/SEO, then
executive personality, then the final interface. Do not skip ahead.


## CURRENT POSITION (2026-09-24) — paused, user on another project
- Website: **live** at elitebalaji.com. Next: www→apex redirect, fix the 2.6 s
  mobile hero blank, museum-direction hero (still → audit → animate).
- SEO agent: **built and scheduled** (execution unverified — check first).
- Marketing agent: **unblocked** (the site is live) — next agent to build.
- Email agent: still waits on Marketing.
- Website agent (PRs + approvals): designed in OPERATIONS_PLAN, not built.
- Full handoff: `docs/NEXT_SESSION.md` → "Paused 2026-09-24".

## PENDING CLIENT/PLANNING — expanded cross-device vision (2026-09-11)
User wants Vicky to eventually run as a JARVIS-style assistant across their
own devices with an auto-updating preference/context "brain" in the backend.
A planning prompt was written (`docs/EXTERNAL_PLANNING_PROMPT.md`) for the
user to run through an external LLM. Nothing here is architected or started —
do not build cross-device/always-on infrastructure until the user brings back
a reviewed plan. See `docs/PROJECT_STATE.md` "Expanded vision" section.

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

**Status 2026-09-16:** design, catalogue and interaction layers are
feature-complete for launch (89 pages, Playwright QA passing). What remains:
- **Client input:** confirm which marbles and sinks are stocked; real photos
  to replace illustrative images.
- **Launch:** domain, hosting, deploy permission, GitHub push.

Marketing and Email agents stay blocked until the site is live. The dated
handoff is in `docs/NEXT_SESSION.md`.

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
