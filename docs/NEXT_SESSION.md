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

## Latest (2026-09-15, afternoon) — site rebuilt from the client's AI mockup
- **Client direction:** the AI reference mockup IS the design (the showroom
  is under renovation). See the `docs/DECISIONS.md` top entry.
- **Homepage:** hero, category strip and trust bar rebuilt to the mockup,
  with its imagery in `public/media/reference/`.
- **Header:** mockup nav (Home, About, Products▾, Applications, Gallery,
  Resources, Contact), sub-strip, a menu drawer at every width, and a
  transparent overlay on the homepage.
- **New pages:** `/applications/`, `/gallery/`, `/resources/` (built only from
  existing data), plus a `PageHero` component.
- **Favicon:** `favicon-48.png` and `apple-touch-icon.png`, from the client
  emblem.
- **Bugs fixed:** the 6px phone header overflow (header call button
  removed) and the phone hero headline clipping.
- **Docs:** `docs/ART_DIRECTION.md` rewritten as the full art direction +
  UX orchestration brief.
- **Verified:**
  - `astro check` 0 errors, build 61 pages.
  - Static crawl: 0 broken links or images.
  - All 19 page types have no overflow at 375px, and there are no console
    errors.
  - Menu, dropdown, header scroll state, gallery filter and search deep
    links all work.
- **Launch blockers still open:**
  1. Real domain for `astro.config.mjs` `site` and `public/robots.txt`.
     Every canonical URL currently says `elitebalaji.example.in`.
  2. Hosting decision and permission to deploy.
- **Not done:**
  - High-resolution regeneration of the renders. Adobe upload was blocked
    by the permission classifier, and no text-to-image API exists yet.
  - A 3-slide hero carousel.
  - Kota image replacement.
  - Confirming a real product count for the "1000+" stat.

## Earlier on 2026-09-15
- Finished `VISUAL_AUDIT_V2.md` phase 2: steps 4–9 (#6, #11, #12, #13, #14,
  #15), all in `website/src/pages/index.astro`. The status section at the
  bottom of that file has the details.
- Build, typecheck and browser QA (desktop + mobile) are clean.
- Items still held from that audit: #3 nav structure, CTA wording, carousel
  dots.
- **Header badge replaced with the client's exact logo:**
  `public/media/brand/logo-emblem-240.png`, with the full-size cutout at
  `logo-emblem.png`. The user approved it. Never redraw or alter it; see
  `docs/CLIENT_PREFERENCES.md`.
- **Kota Stone images are flagged as inaccurate** (generic Unsplash). Art
  direction has started in `docs/ART_DIRECTION.md`, with the Kota sheet done
  and other materials "to complete".
- **Next:**
  1. The user reviews the Kota sheet.
  2. The user picks an image/video generation API. Recommended: Google
     Imagen + Veo, reusing the Gemini key. It may need billing.
  3. Then build a review-first generation script.

  Any generated image must be labelled illustrative.
- **Still open from the user:** do "empty catalogues" mean the text-only
  "sourced on request" lists in `src/lib/stone-varieties.ts`? Also, which
  option: client photos, supplier catalogues, stock, or swatches?
- All of the above was committed at the user's request ("save it").

## Earlier session (2026-09-13)
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
