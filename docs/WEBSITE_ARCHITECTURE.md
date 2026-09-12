# Website Architecture — Elite Balaji Virtual Showroom

Status: catalogue-discovery + agent-ready data architecture shipped
(2026-09-12). This document is the technical reference for `website/`;
business/design rules live in `.cursorrules` and
`.cursor/rules/elite-balaji-virtual-showroom.mdc`.

The website is Phase 1 of a larger planned system (website → marketing
agents → Vicky executive/orchestrator). It is **not** built with any agent
API or backend — that's explicitly out of scope until those phases exist —
but the content layer is deliberately structured as plain, schema-validated
JSON files so a future agent can read/write business facts through this same
data layer instead of editing page components. See §3.

## 1. Current state

`website/` is an **Astro 5 + TypeScript + Tailwind CSS v4** static site.

```
website/
  src/
    content.config.ts       # Zod schemas: halls, products, services
    content/
      halls/*.json           # 8 hall entries (name, intro, applications, colour...)
      products/*.json        # Canonical product records, kind: "tile" | "material" (see §3)
      services/*.json        # Bespoke/custom-fabrication capabilities (see §3)
    components/              # SiteHeader, SiteFooter, EnquiryBar, Seo, MaterialField
    layouts/BaseLayout.astro
    lib/
      business.ts             # Single source of truth for phone/address/USPs/hubs
      material-worlds.ts       # Single source of truth for hall -> "material world" grouping
      facets.ts                 # Derives colour/character/application tags from real fields
    scripts/motion-gsap.ts    # GSAP + ScrollTrigger motion (hero, stagger reveals, heritage parallax)
    pages/
      index.astro              about.astro    contact.astro    404.astro    custom.astro
      search.astro              search-index.json.ts     (faceted catalogue discovery)
      halls/index.astro         halls/[slug].astro
      materials/[world].astro   (Natural Stone / Tiles & Ceramics / Surfaces landing pages)
      products/[id].astro
    styles/global.css         # Tailwind v4 @theme tokens (material-led charcoal/ivory/terracotta palette)
  public/
    media/                    # Web-servable images (catalogue crops, business card)
    favicon.svg  robots.txt
  catalogues/                 # Source PDFs + drop zone (NOT web-served)
  catalogue_extract/          # Raw page-render cache from scripts/extract_catalogues.py
```

Build tooling: Node 24 LTS + npm. `astro check` (typecheck) and `astro build`
both run clean. No test framework yet — content is data-driven JSON validated
by Zod at build time, which is the main correctness net for now.

## 2. Why Astro

This is a content-heavy, mostly-static showroom where SEO and load performance
matter more than interactivity. Astro ships zero JS by default and only
hydrates islands that need it (none currently — the mobile menu and contact
form use plain inline `<script>`, not a framework island). Tailwind v4 (via
`@tailwindcss/vite`) gives a design-token system without a separate config
file. If a future page genuinely needs a client-side widget (e.g. a filterable
catalogue), add a scoped island rather than converting the whole site to a SPA.

## 3. Content model

Three Astro content collections (`src/content.config.ts`), loaded from JSON so
non-developers — or a future agent — can eventually edit them without
touching component code:

- **`halls`** — one entry per showroom hall. Fields include `hasRealContent`
  (bool) which the hall template uses to decide whether to render a real photo
  or a `MaterialField` (see §5), and `materialColor`/`materialTexture` for the
  placeholder look.
- **`products`** — the canonical product record. **One shape for every real
  product across every hall** (`kind: "tile" | "material"`), so one record
  powers the catalogue card, the search/filter index, the product detail
  page, related-product ranking, and Product structured data — instead of
  the two differently-shaped collections (`tileProducts`/`materialProducts`)
  this replaced on 2026-09-12, which forced every consumer to branch on
  which shape it was looking at. Fields: `kind`, `hallId`, `name`, `brand?`,
  `series?`, `code?`, `category?`, `size?`, `finish`, `order`, `applications`,
  `image`, `imageAlt`, `sourceCatalogue?`, `note?`. Colour/look/application
  facet tags are **not stored here** — they're derived at build time from
  `name`/`finish`/`imageAlt`/`applications` by `src/lib/facets.ts`, so any
  new product automatically becomes filterable with zero extra tagging.
- **`services`** — bespoke/custom-fabrication capabilities (CNC engraving,
  tile printing, inlay, sculptures). Fields: `hallId`, `name`, `category`
  (a stable slug like `"tile-printing"` — used for icon lookup, not the
  display name, so a rename doesn't silently lose its icon), `description`,
  `capabilities?` (an array left empty until the client verifies specific
  sub-capabilities — do not populate this speculatively), `order`.

**Important finding from the Phase 2 audit (still true):** the 7 tile-shaped
catalogue extracts in `catalogue_extract/` are the only real product
photography that exists. There is currently no real photography for Granite
& Marbles, Kota Stone, Kadappa, Sanitaryware, Adhesive & Accessories, or
Quartz — those `products` entries use verified-checked stock photography
with an honest "Mood photography, not actual stock" disclosure (see the
`hasRealContent` flag on the corresponding hall).

### Adding a new real product
Drop a JSON file in `src/content/products/` matching the schema above
(`kind: "tile"` for a catalogue tile series, `"material"` for anything else),
add the image to `public/media/<hall>/<slug>/` (or reference verified stock),
and reference it — the hall page, `/search/`, the material-world landing
page, and the product detail page all pick it up automatically via
`getCollection("products")`. Never write a spec you can't see in the source
catalogue image or that the client hasn't confirmed.

### Adding a new custom-fabrication service
Drop a JSON file in `src/content/services/` with a real, described
capability — it appears automatically on `/custom/`, the homepage's Custom
section, and its parent hall page. Never invent a capability, technology,
material, or specification that hasn't been confirmed by the client.

### Adding real photos to a placeholder hall
1. Put photos under `website/catalogues/product-photos/<hall>/` (existing drop
   zone) or directly copy a web-ready crop into `public/media/<hall>/`.
2. In `src/content/halls/<hall>.json`, set `hasRealContent: true` and fill in
   `heroImage`/`heroAlt`.
3. No template change needed — `[slug].astro` already branches on `hasRealContent`.

## 4. Design system

Tokens live in `src/styles/global.css` under `@theme`. Palette was derived by
rendering the actual Athangudi-Series PDF (`scripts/extract_catalogues.py` /
ad hoc PyMuPDF render) and sampling its colours: terracotta red, mustard gold,
bottle green, warm ivory ground, muted brass accent — deliberately **not** the
black-marble/neon-gold JARVIS aesthetic the internal Vicky UI will use later
(see `.cursor/rules/elite-balaji-virtual-showroom.mdc`). Typography pairs a
serif display face (Cormorant Garamond) with a geometric sans (Outfit),
echoing the Athangudi wordmark's script + tracked-caps pairing.

Layout avoids the "heading → 3 cards → heading → 3 cards" pattern: the
homepage showroom index uses an alternating editorial list for the three
featured halls and a plain text-link row for the rest; hall pages are a single
hero + two-column intro, not a wall of cards.

## 5. `MaterialField` — the placeholder-photo component

For halls without real photography, `src/components/MaterialField.astro`
renders a full-bleed colour field (the material's real-world colour) with a
subtle CSS pattern (diagonal lines for stone, grid for ceramic, dot noise for
cement, sheen for porcelain) instead of a stock photo standing in for a real
product. This was a deliberate call during the Phase 2 build: the brief
explicitly prohibits "stock images pretending to be client work," and generic
Unsplash mood shots for specific materials (granite, kadappa, etc.) risked
exactly that. `MaterialField` is honest about what it is — texture and colour
identity, with copy that says photography is pending — and it is replaced by
real photos hall-by-hall as they arrive (§3).

**Gotcha (already hit once, keep this in mind when editing the component):**
`MaterialField`'s root element hardcodes `position: relative`. If a caller
also passes `absolute` in its own `class` prop, both utilities land on the
same element and Tailwind's cascade order decides which `position` wins —
in practice `relative` won, which silently turned the panel into an in-flow
flex item instead of a full-bleed background (a ~50/50 split with the page
background showing through). Fix pattern: wrap the component in an external
`<div class="absolute inset-0 ...">` instead of passing a conflicting position
utility straight into `class`. See `src/pages/halls/[slug].astro` hero section
for the correct pattern.

## 6. SEO

- Per-page `<title>`/meta description via `BaseLayout` props.
- `src/components/Seo.astro` emits canonical URL, Open Graph, Twitter card,
  and a `HomeAndConstructionBusiness` JSON-LD block built from
  `src/lib/business.ts` (name, address, phone, founding date, area served).
- Product pages additionally emit `Product` and `BreadcrumbList` JSON-LD
  (`src/pages/products/[id].astro`). The `Product` block deliberately has no
  `offers`/price — this site never publishes prices, and Offer markup
  without a real price is exactly the incomplete structured data Google
  flags in Search Console, so it's omitted rather than faked.
- `@astrojs/sitemap` generates `sitemap-index.xml` at build time.
- `public/robots.txt` points at it. **TODO:** the sitemap/robots hostname is
  a placeholder (`elitebalaji.example.in`) until a real domain is chosen —
  update `astro.config.mjs` `site` and `public/robots.txt` together.
- Local SEO: service hubs list from `.cursorrules` `STRICT_TARGET_LOCATIONS`
  appears naturally in the homepage service-area section, the footer, and
  `areaServed` in the JSON-LD — not stuffed into hidden text anywhere.

## 7. Performance & accessibility

- No client JS framework; the only inline scripts are the mobile-menu toggle
  and the contact form's WhatsApp-link builder (both `is:inline`, a few lines).
- Images are plain `<img>` with explicit `loading="lazy"` below the fold and
  `fetchpriority="high"` on the LCP hero image. `sharp` is installed for
  `astro:assets` if/when local image optimization is needed for a future
  gallery; not yet wired into every image since the catalogue photos are
  served as-is from `public/media/`.
- `prefers-reduced-motion` is respected globally in `global.css`.
- Skip-to-content link, visible focus rings (`:focus-visible`), semantic
  landmarks (`header`/`main`/`footer`/`nav`), and alt text on every real photo
  describing what's actually in it (not the product name as a keyword-stuff).

## 8. Deployment (not yet done — needs a decision, not a build change)

Recommended: **Cloudflare Pages**, connected to a GitHub repo, build command
`npm run build` with base directory `website/`, output `website/dist`. Free
tier covers this comfortably (static site, no functions needed yet). GitHub
Pages is an equally free fallback if Cloudflare isn't wanted.

Blocking items before this can happen (see `WORKPLAN.md`):
1. A GitHub remote — none exists yet, only a local repo initialized during
   this rebuild.
2. A real domain, or acceptance of a free subdomain (`*.pages.dev` /
   `*.github.io`) for launch.

## 9. Known gaps / next steps

- Granite & Marbles, Kota Stone, Kadappa, Sanitaryware, Adhesive & Accessories,
  Quartz: no real photography yet — `MaterialField` placeholders in place.
- No automated tests. Given the site is static content + Zod-validated data,
  the highest-value next test is a link checker over `dist/` before each
  deploy, not a JS unit-test suite.
- Domain/hosting decision (§8) is still open.
