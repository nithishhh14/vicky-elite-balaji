# START HERE

## Current objective
The website is mid-way through a large, still-active "anti-slop" redesign
and content-depth brief (material-first nav, DISCOVER→EXPLORE→FILTER
homepage, canonical product schema, real React Bits islands, growing real
catalogue depth from already-approved supplier PDFs). Deployment is
explicitly **DEFERRED — POST-DESIGN / PRE-LAUNCH**; do not deploy, buy a
domain, or set up hosting without new, explicit user permission (the user
answered "No, not yet" to a direct deployment question on 2026-09-12, and a
later brief reiterated deployment is out of scope for now).

## What was completed in the most recent session (2026-09-13)
- Expanded the Athangudi Series from 1 to all 8 real colourway variants
  found in the already-approved `catalogue_extract/Athangudi_Series_/`
  render cache (cropped with `ffmpeg`, verified against source pages).
- Extended the `products` schema with an optional multi-image `images`
  gallery and real spec fields (thickness/qty-per-box/coverage/weight);
  rendered both on the product detail page (thumbnail-swap gallery, spec
  grid), verified via browser QA on desktop + mobile.
- Closed a flagged SEO gap: added `CollectionPage` + `BreadcrumbList`
  JSON-LD to hall and material-world pages (product pages already had it).
- `astro check` + `astro build` verified clean; committed as `9d5e92c` and
  `956ac8e`. See `docs/PROJECT_STATE.md` for full detail, `docs/DECISIONS.md`
  for the schema/architecture reasoning.

## What still needs work (real, deferred-for-time, not forgotten)
- `catalogue_extract/GC_COIMBATORE/` has 10 more real, currently-unused SKU
  codes for the existing single "Adoration Ceramica" product — not yet
  mined into separate product records.
- 5 more catalogue folders never examined at all: `HOME_CENTER_-_COIMBATORE`,
  `HOME_CENTRE_..._MOROCAN_...`, `LEVERPOOL_15`, `_20_SONEX_...`,
  `12x18-wall_tiles`, `GC_TILES_COIMBATORE_LLP` — likely more real SKU depth
  sitting unused, same pattern as Athangudi.
- Real photography still missing for most non-Tiles halls (Granite &
  Marbles, Kota Stone, Kadappa, Sanitaryware, Adhesive & Accessories,
  Quartz) — they still use the `MaterialField` colour/texture placeholder.
- The broader 12-stage "lead designer" brief (design system refinement,
  motion/imagery/responsive polish, a full regression pass) is large and
  was only partially worked through this session — catalogue depth + the
  SEO gap were the concrete, verifiable, non-fabricated wins picked out of
  it. Re-read that brief in the transcript/summary if continuing it
  directly, and keep applying the same rule: real data and real fixes over
  decoration, never invent products/specs/stats.

## First thing Claude should inspect
Run `git log --oneline -15` and `git status` to confirm nothing changed
outside the last session, then read `docs/PROJECT_STATE.md` (top entry) and
`docs/DECISIONS.md` (bottom entries) for what's freshest.

## Known bugs
None open as of 2026-09-13.

## Known placeholders
- Most non-Tiles halls still use `MaterialField` instead of real photography.
- `astro.config.mjs`'s `site` and `public/robots.txt`'s sitemap URL use a
  placeholder hostname (`elitebalaji.example.in`) — domain is not decided,
  though `elitebalaji.com` was confirmed available as of 2026-09-12.

## Deployment status
Not deployed anywhere. No hosting connected, no domain purchased, no CI/CD.
**Do not deploy without new explicit permission** — see "Current objective."
The site builds cleanly to `website/dist/` locally (`astro build`).

## Git status
Local repository, branch `main`. Working tree was clean at end of the
2026-09-13 session (verify again with `git status` before assuming this
still holds) — no GitHub remote as of this writing.

---

# RESUME INSTRUCTION

When a new Claude Code session begins on this project, Claude MUST read:

1. `CLAUDE.md`
2. `docs/PROJECT_STATE.md`
3. `docs/CLIENT_PREFERENCES.md`
4. `docs/DECISIONS.md`
5. `docs/NEXT_SESSION.md` (this file)
6. `docs/WEBSITE_ARCHITECTURE.md`

before making significant changes to the website or its documentation.
