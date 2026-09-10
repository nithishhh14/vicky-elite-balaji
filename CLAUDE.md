# Vicky — Elite Balaji Stones & Ceramics automation

Multi-agent business system for Elite Balaji Stones & Ceramics (Karamadai,
Coimbatore, since 2012). Executive agent routes commands across a council of
specialist agents; a Streamlit dashboard is the control surface; a static
website is the public virtual showroom.

## Architecture (what's actually wired together)

- `app.py` — Streamlit dashboard, entry point. Loads env, configures Gemini,
  routes voice/text through `agents/vicky_executive.py`.
- `shared_memory.py` — the shared state layer: Google Sheet I/O (leads,
  council log, SEO audits), lead cleaning/dedup rules, `.cursorrules` loader.
  This is the closest thing to "shared memory" right now — it's a live
  Google Sheet, not a database.
- `lead_agent.py` — the real scraper (Google Maps + Search harvesting,
  lead normalization, filtering). This is what `agents/scraper_agent.py`
  actually calls.
- `agents/` — one file per council member:
  - `vicky_executive.py` — intent router + default chat via Gemini
  - `scraper_agent.py` — wraps `lead_agent.run_harvest()`
  - `seo_agent.py` — live, writes to `SEO_Audits` sheet
  - `marketing_agent.py` — **stub**, blocked until website ships
  - `email_agent.py` — **stub**, blocked until Marketing is live; drafts only,
    never auto-sends
- `website/` — the virtual showroom: **Astro 5 + TypeScript + Tailwind CSS v4**
  (rebuilt from the original static HTML/CSS shell). Content-driven via two
  content collections (`halls`, `tileProducts`) instead of hand-written markup
  per page. See `docs/WEBSITE_ARCHITECTURE.md` for the full architecture,
  content model, and how to add hall photos or tile series. Requires Node.js
  (installed via winget during the rebuild) — `cd website && npm run dev`.

## Do NOT use

- `archive/elite_balaji_scraper.py` — superseded by `lead_agent.py`. Dead
  code, kept for reference only. Do not wire it back in without a reason.
- `archive/showroom_memory.json` — orphaned data file, only the old scraper
  above ever read it.

## Hard rules

- Never hardcode API keys or credentials in source. `GEMINI_API_KEY` comes
  from `.env` only — `shared_memory.configure_gemini()` raises if it's
  missing, on purpose. Don't add a fallback literal back in.
- `.env` and `google_creds.json` are gitignored. Keep it that way — never
  suggest committing them, even "temporarily."
- `chrome_profile/` is runtime-only browser session data (regenerated on
  run). Never commit it, never zip it into a deliverable.
- Marketing and Email agents stay blocked until the website is actually
  live and reachable — that gate is intentional, not a bug.
- Never present a supplier's catalogue photo, or any photo, as an Elite
  Balaji product shot unless it genuinely is one — see the "Real product
  data rule" in `docs/WEBSITE_ARCHITECTURE.md` §3. Only the Tiles hall
  currently has verified real catalogue content; the other seven halls use
  the `MaterialField` colour/texture placeholder, not stock photography,
  until real photos exist.

## Conventions

- Leads are phone-first: `shared_memory.optimize_sheet()` prefers rows with
  a phone number, then Google Maps/Instagram with a website, then Buyer
  Signal leads. JustDial and OLX are deliberately filtered out as noisy
  sources.
- Coimbatore / Nilgiris hubs only — anything outside that region gets
  filtered by `lead_agent.local_ok()`.
- One-off debug/probe scripts live in `scripts/`, not the project root.

See `WORKPLAN.md` for current phase and next steps.
