# Vicky / Elite Balaji — Current Project State

_Last updated: 2026-09-12 — functional-fix pass (real catalogue routes, search, product detail pages), then a motion/3D pass (GSAP + Three.js, approved as new dependencies), then a strategic-direction update ("living digital showroom" / large-scale filterable catalogue) received and currently at the planning stage — see `docs/DECISIONS.md` for each._

## 2026-09-12 — motion system + 3D viewer + consistency fixes

- Added GSAP + ScrollTrigger (`website/src/scripts/motion-gsap.ts`, wired via
  `BaseLayout.astro`) replacing the previous vanilla-JS scroll parallax:
  hero entrance, coordinated staggered reveals (`data-gsap-stagger`, used on
  the homepage material grid, hall product/service grids, and the Custom page
  cards), and a layered "living heritage" Athangudi section (real photo +
  decorative quatrefoil pattern layer + content, each drifting at a different
  rate, `data-gsap-heritage`). Gated the same way the pre-existing reveal
  system is: CSS only pre-hides `[data-gsap-hero]`/`[data-gsap-stagger]`
  children once a synchronous inline script confirms JS is running AND the
  user allows motion (`js-motion-ready` class) — content is never stuck
  invisible if a script fails to load.
- **Real bug found and fixed during QA**: `gsap.from()` was used initially,
  which auto-detects the tween's end state from each element's *current*
  computed CSS — but the CSS pre-hide already set `opacity: 0` before GSAP
  ran, so it animated 0 → 0 and content stayed permanently invisible. Fixed
  by switching to `gsap.fromTo()` with explicit end values everywhere.
- Added `MaterialViewer3D.astro`: a lazy-loaded (dynamic `import("three")`,
  tree-shaken named imports, ~132KB gzip, only fetched on the Tiles hall
  page) rotating 3D viewer mapping the real, already-verified Athangudi
  Petal Red swatch photo onto a simple tile mesh. Drag-to-rotate, idle
  auto-spin suppressed under `prefers-reduced-motion`, falls back to the
  static `<img>` if WebGL/texture loading fails.
- Custom & Fabrication page (`custom.astro`) restyled with icon-badged
  capability cards; same 4 real services as before (Custom Photo-Printing on
  Tiles, CNC Granite Engraving, Handcrafted Inlay Slabs, Sculptures & Name
  Boards) — no new capabilities invented.
- Fixed leftover `bottle`-green Tailwind classes in `about.astro`,
  `contact.astro`, `privacy.astro`, `terms.astro`, `404.astro`,
  `halls/index.astro`, and `SiteFooter.astro` — these were missed by the
  2026-09-12 terracotta/charcoal palette migration, which only touched the
  homepage and hall detail page at the time.
- Fixed two more em-dashes that survived the earlier sitewide cleanup
  (`dc65952`) because they lived in a JS string literal (`search.astro`
  error text) and a meta-description template literal
  (`products/[id].astro`), not in template markup — the original grep only
  checked rendered text nodes.
- Verified: `astro check` (0 errors) and `astro build` (39 pages) both clean;
  browser QA at desktop (588×415) and mobile (375×812) — hero/stagger/
  heritage transforms confirmed genuinely dynamic via direct DOM/transform
  measurement (not just visual screenshot, which had known compositing
  glitches in this session's tooling — see below); CTAs click-tested; no
  console errors on home, Tiles hall, Granite & Marbles hall, or Custom.
- Committed as `d23f6ef` (consistency fixes) and `35ecc4f` (motion/3D/custom).
- **Known cost, disclosed not hidden**: GSAP+ScrollTrigger now loads on
  every page (~46KB gzip, was ~0KB with the vanilla approach it replaced).
  This was an explicit user choice (approved adding GSAP + Three.js over
  keeping the vanilla approach) after being told the tradeoff plainly.

## 2026-09-12 — strategic direction update (planning stage, not yet implemented)

The user sent a "PLAN UPDATE" message repositioning the site from a small
static catalogue toward a "living digital showroom": large/expandable
data-driven product catalogue (10 → 500+ products without redesign),
multi-axis discovery (by material/colour/look/application), product
relationships, a dedicated "can't find it? we can source it" experience,
custom fabrication as a major site section, and a luxury-stone-website-tier
visual/interaction standard. The message explicitly asks for a concise
implementation plan before any implementation, and states a master product
list will be supplied separately — **do not fabricate products/categories to
make the catalogue look bigger in the meantime.** See `docs/DECISIONS.md`
for the plan itself and what is/isn't blocked on that product list.

## Website optimization pass (2026-09-11)

Following a design/technical brief the user relayed (sourced from an
external LLM, not a documented Elite Balaji conversation), Claude made
targeted changes to the existing Astro site — no rewrite. See
`docs/DECISIONS.md` for full reasoning on each; summary:

- Palette rebalanced green-dominant (terracotta/mustard demoted to secondary
  accents). Still a working assumption, not confirmed client preference.
- `business.email` added (user-confirmed real) and surfaced in the footer,
  About, Contact, JSON-LD, and new "Request Email Quote" `mailto:` CTAs
  alongside every WhatsApp/Call CTA (the brief's "no prices, always an
  enquiry trigger" rule).
- All 7 non-Tiles halls now show verified stock photography (each image was
  opened and visually checked, not trusted from search-result order —
  several initial picks were wrong, e.g. a mountain landscape mistagged
  "granite," and were caught and replaced) with a visible "Mood photography
  — not actual stock" disclosure, plus 2 structured product cards per hall
  using only generic category/finish language and a mandatory
  "representative style, confirm with our team" disclaimer — no invented
  specific origin/provenance claims, per this project's no-fabrication rule.
- Google Maps embedded on About + Contact, deliberately as an address-only
  query rather than a business-name search, after a business-name query was
  found (by actually loading it) to resolve to unrelated nearby businesses.
- Minor real fixes: anchor-scroll landing under the sticky header on the
  homepage "Enter showroom" link, nav wrapping at in-between viewport widths.
- No dropdown nav or product-gallery tabs exist in this codebase (the relayed
  brief assumed they did) — nothing to fix there; noted to the user rather
  than fabricating features to match the brief's assumptions.

## Expanded vision (stated 2026-09-11 — planning stage only)

The user has stated a larger ambition beyond the original phased plan: Vicky
should eventually run as a JARVIS-style assistant reachable across the
client's (the business owner's) own devices, automating his requirements and
preferences, with an auto-updating shared "brain" in the backend (context/
preferences that update themselves over time rather than being manually
re-entered). This is a **stated goal, not a decision** — no architecture for
it exists yet. The user asked for a comprehensive planning prompt to run
through an external LLM before any of this is built; see
`docs/EXTERNAL_PLANNING_PROMPT.md` for the prompt itself. When the user
brings back a plan from that external session, treat it as input to review
and reconcile with `docs/DECISIONS.md`, not as something to implement blind.
Do not start building cross-device/always-on infrastructure until that
review happens.

## Project objective

Vicky is a multi-agent automation system for Elite Balaji Stones & Ceramics
(Karamadai, Coimbatore, since 2012) — a granite/marble/tile/sanitaryware
wholesale + laying business. An executive agent routes commands across a
council of specialist agents; a Streamlit dashboard is the temporary control
surface; a public static website is the "virtual showroom" that Marketing/SEO/
Email agents will eventually consume. Locked build order (`.cursorrules`):
Scraper → Website → Marketing+SEO → Executive personality → Final interface.
We are inside Phase 2 (Website).

## Current architecture

- `app.py` — Streamlit dashboard (temporary workbench), routes to
  `agents/vicky_executive.py`.
- `shared_memory.py` — Google Sheets I/O + `.cursorrules` loader. Live shared
  state layer for the agent council.
- `lead_agent.py` + `agents/scraper_agent.py` — working Google Maps/Search
  scraper. Not touched this session.
- `agents/seo_agent.py` — live, writes to `SEO_Audits` sheet.
- `agents/marketing_agent.py`, `agents/email_agent.py` — intentional stubs,
  gated on the website being live and reachable at a public URL.
- `website/` — **rebuilt this session** into an Astro 5 + TypeScript +
  Tailwind v4 static site. This is the only part of the repo that changed
  today.

## Current website stack

- Astro 5 (`astro@^5.6.1`), static output mode, no SSR.
- TypeScript (`astro check` for typechecking, strict tsconfig).
- Tailwind CSS v4 via `@tailwindcss/vite` (CSS-first `@theme` tokens, no
  separate `tailwind.config.js`).
- `@astrojs/sitemap` for `sitemap-index.xml`.
- `sharp` installed (for `astro:assets` image optimization) but not yet wired
  into every image — most images are plain `<img>` served from `public/media/`.
- No client-side JS framework (no React/Vue/Svelte). Two small `is:inline`
  scripts: mobile-menu toggle, and the contact-form WhatsApp-link builder.
- Node.js 24 LTS installed on this machine via winget (was not present
  before this session).

## Completed work (verified, not assumed)

- Deleted the old static shell (`index.html`, `css/showroom.css`,
  `halls/*.html` — 3 of which were empty files) and replaced it with the
  Astro site described above.
- Two Zod-validated content collections: `halls` (8 entries) and
  `tileProducts` (7 entries), defined in `website/src/content.config.ts`.
- Design system in `website/src/styles/global.css` (`@theme` tokens):
  terracotta/mustard/bottle-green/warm-ivory palette, derived by actually
  rendering the Athangudi-Series supplier PDF and sampling its colours —
  not guessed. Cormorant Garamond (display) + Outfit (UI) typefaces.
- Pages implemented and build-verified: `/`, `/halls/`, `/halls/[slug]/`
  (×8), `/about/`, `/contact/`, `/404`. 13 static pages total in the build
  output.
- Tiles hall has a real 7-series product grid, each entry sourced from an
  actual page image in `website/catalogue_extract/` with an honest source
  caption (brand/catalogue name) — see `website/src/content/tile-products/`.
- The other 7 halls (Granite & Marbles, Kota Stone, Kadappa, Sanitaryware,
  Adhesive & Accessories, Quartz, Laying Works) use the `MaterialField`
  component (colour + CSS texture pattern) instead of stock photography,
  since no real photos exist for them yet.
- WhatsApp-first enquiry flow: floating enquiry bar (product-aware message),
  per-hall/per-product "Ask for trade rate" links, and a `/contact/` form
  that builds a `wa.me` deep link client-side (no backend, no data leaves
  the browser).
- SEO: per-page title/description, Open Graph + Twitter meta, canonical URLs,
  `HomeAndConstructionBusiness` JSON-LD (name/address/phone/founding date/
  area served) in `website/src/components/Seo.astro`, sitemap + robots.txt.
- Mobile-first responsive nav: full nav at `lg:`, hamburger + slide-down
  panel below it (all 8 halls + About + Contact). Verified at 375/768/1280.
- Accessibility basics: skip-to-content link, `:focus-visible` rings,
  semantic landmarks, `prefers-reduced-motion` support, alt text describing
  actual image content (not keyword-stuffed).
- Fixed a real bug found during QA: `MaterialField`'s hero usage had two
  conflicting Tailwind `position` utilities on the same element (`relative`
  from the component's own base class + `absolute` passed in from the
  caller), which silently broke full-bleed rendering into a 50/50 split
  with the page background showing through. Fixed by wrapping the component
  in an external positioning `<div>` instead of passing a conflicting class.
  Documented in `docs/WEBSITE_ARCHITECTURE.md` §5 so it isn't reintroduced.
- git repository initialized for the whole project (none existed before this
  session). Two commits so far (see `git log`). No remote configured yet.
- `.env.example` created with safe variable names only.

## Current routes

| Route | Source | Notes |
|---|---|---|
| `/` | `src/pages/index.astro` | Homepage — hero, brand story, showroom index, USPs, service area, CTA |
| `/halls/` | `src/pages/halls/index.astro` | Grid of all 8 halls |
| `/halls/tiles/` | `src/pages/halls/[slug].astro` | Real product grid (7 series) |
| `/halls/granite-marbles/` | `src/pages/halls/[slug].astro` | Placeholder (`MaterialField`) |
| `/halls/kota-stone/` | `src/pages/halls/[slug].astro` | Placeholder |
| `/halls/kadappa/` | `src/pages/halls/[slug].astro` | Placeholder |
| `/halls/sanitaryware/` | `src/pages/halls/[slug].astro` | Placeholder |
| `/halls/adhesive/` | `src/pages/halls/[slug].astro` | Placeholder |
| `/halls/quartz/` | `src/pages/halls/[slug].astro` | Placeholder |
| `/halls/laying-works/` | `src/pages/halls/[slug].astro` | Placeholder |
| `/about/` | `src/pages/about.astro` | Business facts, what we supply, service area |
| `/contact/` | `src/pages/contact.astro` | Phone/address + WhatsApp-building enquiry form |
| `/404` | `src/pages/404.astro` | Not-found page |

## Current components

- `BaseLayout.astro` — HTML shell, fonts, `Seo`, `SiteHeader`/`SiteFooter`/`EnquiryBar`.
- `Seo.astro` — meta/OG/Twitter/canonical/JSON-LD.
- `SiteHeader.astro` — sticky nav, desktop (`lg:`) + mobile hamburger menu.
- `SiteFooter.astro` — address/phone/WhatsApp/service-hub list.
- `EnquiryBar.astro` — floating WhatsApp CTA, accepts a custom message.
- `MaterialField.astro` — colour/texture placeholder panel for halls without
  real photography (see the position-conflict gotcha above and in the
  architecture doc before editing this one).

## Current content/data

- `website/src/content/halls/*.json` — one file per hall: name, tagline,
  intro copy, applications, `hasRealContent` flag, `materialColor`/
  `materialTexture` for the placeholder look.
- `website/src/content/tile-products/*.json` — 7 real tile series entries,
  each traceable to a specific catalogue page image.
- `website/src/lib/business.ts` — single source of truth for phone, address,
  contact person, tagline, service hubs, partner brands, USPs. All values
  trace back to `.cursorrules` / the business card.
- Schemas for both collections: `website/src/content.config.ts`.

## Current assets

- `website/public/media/tiles/<series-slug>/*.jpg` — **real** catalogue
  images, copied from `website/catalogue_extract/` (crops chosen by hand
  after visually reviewing each source PDF page).
- `website/public/media/brand/business-card.jpg` — real business card scan.
- `website/catalogues/` — source PDF drop zone (not web-served).
- `website/catalogue_extract/` — raw page-render cache from
  `scripts/extract_catalogues.py` (the source of the images copied into
  `public/media/`). Kept as the extraction cache, not itself served.
- No real photography exists yet for granite, marble, kota stone, kadappa,
  sanitaryware, adhesive/accessories, quartz, or laying works. As of
  2026-09-11 those halls show verified, individually-checked Unsplash stock
  photography (hotlinked, not downloaded) with a visible "Mood photography —
  not actual stock" disclosure, instead of the earlier `MaterialField`
  colour/texture placeholder. `MaterialField` itself is untouched and still
  used as a fallback if a hall's `heroImage` is ever cleared.
- `website/src/content/material-products/*.json` — 15 generic product-style
  entries across the 7 non-Tiles halls, each with a mandatory disclaimer
  ("Representative style — confirm exact stock, size and finish with our
  team") and no invented specific origin/provenance claims. See
  `docs/DECISIONS.md` "Stock photography for the 7 non-Tiles halls."

## Current agents

Unchanged this session. `agents/vicky_executive.py` routes intents (scrape/
optimize/seo/marketing/email/status/chat); `marketing_agent.py` and
`email_agent.py` remain deliberate stubs that report "waiting for Phase 2
website" — they do NOT yet read anything from the new website, because the
website is not live/public yet. Wiring that read-path is future work, not
started.

## Known issues

- None currently open in the website itself — `astro check` and
  `astro build` both pass clean as of this checkpoint, and the position-
  conflict bug (see above) was found and fixed this session.
- `astro.config.mjs`'s `site` value and `public/robots.txt`'s sitemap URL
  both use a placeholder hostname (`elitebalaji.example.in`) — cosmetic
  until a real domain exists, but must be updated together when it does.

## Temporary decisions

- The 7 non-tile halls intentionally show verified stock photography plus
  generic-only product cards, clearly disclosed as mood imagery — this is a
  deliberate stand-in, not a bug, and should be replaced hall-by-hall with
  real photography and real product data as it arrives (see
  `docs/WEBSITE_ARCHITECTURE.md` §3 and `docs/DECISIONS.md` "Stock
  photography for the 7 non-Tiles halls" for the exact steps and rationale).
- The contact form has no backend — it only builds a `wa.me` link
  client-side. This was a deliberate zero-budget, zero-backend choice, not
  an oversight.
- `website/catalogue_extract/` is kept as a cache/reference rather than
  deleted, in case more images need to be pulled from those same catalogues
  later.

## Blocked items

- **Real photography** for 7 of 8 halls — needs the client (Elite Balaji) to
  supply photos or approve a shoot. Nothing on the code side is blocking this.
- **Domain + hosting** — no domain purchased, no hosting connected. Cloudflare
  Pages is recommended (free tier) in `docs/WEBSITE_ARCHITECTURE.md` §8, but
  this needs a decision + possibly a domain purchase, which requires explicit
  go-ahead before spending money.
- **GitHub remote** — none exists. Needs either `gh auth login` in this
  environment or the user creating a repo and giving the remote URL.
- **Client design/content feedback** — none has been given yet. See
  `docs/CLIENT_PREFERENCES.md` (created this session, all sections pending).
- **Google Sheets integration is currently BROKEN (regression, 2026-09-12).**
  `google_creds.json` was swapped to a new service account
  (`vicky-agent@vicky-agent-508408.iam.gserviceaccount.com`) as part of the
  planned account migration. Verified by actually attempting
  `gc.open_by_key(...)` against the live sheet: it fails with a 403 because
  the Google Sheets API is not enabled on the new Cloud project
  (`vicky-agent-508408` / project number `529561488217`). Two things must
  happen before the scraper/shared_memory Sheets integration works again:
  1. Enable the Google Sheets API (and Drive API) for project
     `vicky-agent-508408` in Google Cloud Console.
  2. Share the target spreadsheet with
     `vicky-agent@vicky-agent-508408.iam.gserviceaccount.com` as an Editor
     (exactly like sharing a Google Doc with another person) — not yet
     verified, since the API-enablement error blocked testing this.
  The previous working service account's key content was not backed up
  before the overwrite — if you need to revert, generate a fresh key for
  the old service account in Cloud Console rather than looking for the old
  `google_creds.json` here.

## Next actions

**P0 — must do first**
- Get client sign-off/feedback on the current design direction (colours,
  layout, tone) before investing further polish — see `CLIENT_PREFERENCES.md`.
- Decide whether to proceed with a domain/hosting purchase or stay on a free
  subdomain for an initial soft-launch.

**P1 — important**
- Source real photography for at least Granite & Marbles and Sanitaryware
  (the two categories most likely to convert enquiries).
- Set up the GitHub remote so history isn't only local.

**P2 — later**
- Wire `astro:assets` image optimization for the tile catalogue images
  (currently served as plain `<img>` from `public/media/`).
- Consider a filterable/searchable catalogue view once there are enough real
  products across halls to warrant it (would be the first real "island" of
  client-side interactivity).

**P3 — optional**
- Partner brand logos (currently just a text list) if the client can supply
  usable logo files.
- A projects/portfolio hall once real project photos exist.

## Do NOT redo

- Do not re-evaluate Astro vs. static HTML vs. another framework — this was
  decided with the user this session (see `docs/DECISIONS.md`).
- Do not re-ask whether the 8 extracted tile catalogues are legitimate Elite
  Balaji content — the user confirmed this explicitly this session (see
  `docs/DECISIONS.md` and the `feedback-no-fabrication` memory entry).
- Do not rebuild the design system from scratch — the Athangudi-derived
  palette in `global.css` was deliberately sampled from the real source PDF,
  not guessed, and should be extended, not replaced, absent new client
  direction in `CLIENT_PREFERENCES.md`.
- Do not re-fix the `MaterialField` position bug — it's already fixed; if a
  similar visual glitch reappears, re-read §5 of the architecture doc first.
