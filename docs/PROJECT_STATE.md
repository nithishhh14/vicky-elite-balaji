# Vicky / Elite Balaji — Current Project State

_Last updated: 2026-09-10, end of Phase 2 website rebuild session._

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
  sanitaryware, adhesive/accessories, quartz, or laying works — those halls
  render a `MaterialField` placeholder instead.

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

- The 7 non-tile halls intentionally show a `MaterialField` placeholder
  instead of any photograph — this is a deliberate stand-in, not a bug, and
  should be replaced hall-by-hall as real photos arrive (see
  `docs/WEBSITE_ARCHITECTURE.md` §3 for the exact steps).
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
