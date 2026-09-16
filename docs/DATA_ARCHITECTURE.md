# Data architecture — Vicky / Elite Balaji

_Last updated: 2026-09-16. A map of every place data lives, how it flows, and
who owns it. Numbers are counted from the repo on that date._

## 1. The two halves of the system

```
   CLIENT + SUPPLIER SOURCES                    OUTPUTS
   -------------------------                    -------
   WhatsApp photos, catalogue PDFs  --+
   Client instructions (via user)     +--> WEBSITE  (static, public)
   Supplier data sheets             --+         Astro content collections
                                                -> 114 pages on a static host

   Google Maps / Search listings  ------> AGENTS   (internal, private)
                                                lead_agent + shared_memory
                                                -> Google Sheet (leads, logs)
```

They share nothing at runtime today. The website is a build-time artefact; the
agents are a Python/Streamlit tool. The only planned join is Phase 3: the
Marketing/SEO agents reading the live site, which stays blocked until launch.

## 2. Website data model (source of truth: the repo)

### Content collections — `website/src/content/` (Zod-validated in `src/content.config.ts`)

| Collection | Count | Shape | Notes |
|---|---|---|---|
| `products` | **89** | kind, hallId, name, brand?, series?, code?, category?, size?, finish, order, applications[], image, imageAlt, images[]?, sourceCatalogue?, note?, thickness?, qtyPerBox?, coverageArea?, weight? | One canonical shape for tiles and materials alike |
| `halls` | **8** | name, order, tagline, intro, heroImage, heroAlt, hasRealContent, materialColor, materialTexture, applications[], enquiryNote | The eight showroom halls |
| `services` | **4** | hallId, name, category, description, capabilities[]?, order | Made-to-order capabilities |

Products by hall: Sanitaryware 31 · Granite & Marbles 21 · Tiles 21 · Quartz 4 ·
Kota 4 · Adhesive 4 · Kadappa 2 · Laying works 2. Product images in total: 324.

### Derived data (computed at build, never hand-maintained)

| File | Produces |
|---|---|
| `lib/facets.ts` | colour, character and application tags derived from real product fields |
| `lib/similarity.ts` | "Find similar" groups (material / look / colour / use) and `cardData()` |
| `lib/search-synonyms.ts` | query expansion (Tanglish, trade words, sizes) and stopwords |
| `lib/material-worlds.ts` | hall to material-world grouping used by nav, menus and world pages |
| `lib/stone-varieties.ts` | "varieties we can source" vocabularies (not stock claims) |
| `lib/image-badge.ts` | "Illustrative image" / "Reference photo" / "Colour swatch" labels |
| `lib/media-library.ts` | 40+ client photographs with provenance (`work` / `stock` / `supply` / `idea`) |
| `lib/business.ts` | the single source of verified business facts (address, phone, brands, USPs) |
| `lib/video-zones.ts` | the four cinematic video slots, all empty until real footage exists |
| `lib/seo.ts` | title and description length discipline |

### Generated endpoints (fetched by the browser)

- `/search-index.json` — every product, hall, service and key page plus facets
  (powers search, the search overlay and Material Match)
- `/catalogue.json` — card data for rebuilding a shared shortlist from `?ids=`
- `/halls.json` — hall summary
- `/robots.txt` — generated from the configured site URL
- `/sitemap-index.xml` + `/sitemap-0.xml` — 114 URLs

### Client-side state (never leaves the device)

| Store | Key | Holds |
|---|---|---|
| localStorage | `eb-my-materials` | the visitor's shortlist (max 24 cards) |
| URL | `/shortlist/?ids=...` | a shared shortlist, rebuilt from `/catalogue.json` |
| DOM events | `shortlist:change` | keeps the header count, buttons and lists in sync |

No cookies, no analytics, no backend, no accounts. Enquiries compose a WhatsApp
or email message on the visitor's own device.

## 3. Media pipeline — `website/public/media/` (390 files, 32 MB)

| Folder | Files | What it is | Provenance shown |
|---|---|---|---|
| `basins/` | 192 | Golden and Marble wash basin catalogues, extracted from supplier PDFs (prices cropped out) | "Supplier catalogue" |
| `client/` | 102 | The client's own photos: granite, marble, stonecraft, forwarded ideas | "Our work" / "From our stock" / "Application idea" |
| `tiles/` | 38 | Mozzato and other tile catalogue imagery | "Supplier catalogue" |
| `concepts/` | 18 | AI application concepts and custom tile printing | "Application concept" / "Concept visual" |
| `illustrative/` | 17 | AI product stand-ins (quartz, kadappa, sinks, basins, laying, statement marbles) | "Illustrative image" |
| `adhesive/` | 9 | Somany data-sheet imagery | "Supplier catalogue" |
| `reference/` | 6 | The client-approved AI mockup renders | "Illustrative render" |
| `brand/`, `swatches/` | 8 | Logo (the exact client file) and Kota colour swatches | "Colour swatch" |

Primary product images today: **68 real or supplier photos, 17 illustrative,
4 colour swatches, 0 stock photos.**

**The provenance rule is enforced in code**, not by memory: `image-badge.ts`
labels anything under `/media/illustrative/` or `/media/swatches/`, and
`npm run preflight` fails if an unlabelled generated image appears on a page.

Extraction tooling (run locally, never shipped): PyMuPDF and Pillow scripts
that crop supplier PDFs, strip price badges, and write both the images and the
product JSON.

## 4. Quality gates — `website/scripts/`

| Script | Run by | Checks |
|---|---|---|
| `qa.mjs` | `npm run qa` | every built page × 2 viewports: console errors, failed requests, broken images, overflow, unlabelled generated images |
| `experience.mjs` | `npm run qa:experience` | drives header convergence, menus, search, Material Match, save, compare, enquiry drawer, granite stage, reduced motion; records CLS |
| `serve-headers.mjs` | manual / preflight | serves `dist/` with the production security headers so the CSP is verified before deploy |
| `shots.mjs` | manual | fixed screenshots for visual review |
| `preflight.mjs` | `npm run preflight` | all of the above plus SEO, sitemap, robots, price-leak and structured-data checks. **20 checks — the gate before deploy** |

## 5. Agent side (Phase 1, live but separate)

| Component | Data it owns |
|---|---|
| `lead_agent.py` | harvests leads from Google Maps and Search, normalises, filters to Coimbatore/Nilgiris |
| `shared_memory.py` | the shared state layer: Google Sheet I/O (Leads, Council log, SEO_Audits), dedupe rules, `.cursorrules` loader |
| `agents/vicky_executive.py` | intent router and Gemini chat |
| `agents/scraper_agent.py`, `agents/seo_agent.py` | live wrappers |
| `agents/marketing_agent.py`, `agents/email_agent.py` | stubs, intentionally blocked until the site is live |
| `app.py` | Streamlit dashboard (the control surface) |

Storage: a live **Google Sheet**, not a database. Credentials live in `.env`
and `google_creds.json`, both gitignored and never committed.

## 6. Documentation as data — `docs/`

`PROJECT_STATE.md` (what is built) · `DECISIONS.md` (architecture decisions,
superseded ones kept) · `CLIENT_PREFERENCES.md` (client feedback, dated) ·
`NEXT_SESSION.md` (handoff) · `WEBSITE_ARCHITECTURE.md` · `ART_DIRECTION.md` ·
`COMPETITOR_ANALYSIS.md` · `MAHARAJA_AUDIT.md` · `SECURITY.md` ·
`LEGAL_LICENCES.md` · `LAUNCH_QA.md` · this file.

Rule from `CLAUDE.md`: a new session reads these before changing anything and
updates them before finishing. They are the project's memory.

## 7. Where data enters, and the rules on the way in

1. **Client WhatsApp photos** land in `media/client/` with a provenance tag;
   never relabelled.
2. **Supplier PDFs** go through the extraction script into `media/` plus
   product JSON; **prices are always stripped**.
3. **Client instructions** (relayed by the user) are recorded in
   `CLIENT_PREFERENCES.md`, then implemented.
4. **AI-generated images** go to `media/illustrative/` or `media/concepts/`,
   always labelled, and are replaced as real photos arrive.
5. **Nothing else.** No scraped competitor imagery, no stock photos (the last
   one was removed on 2026-09-16), and no invented specs, prices, reviews or
   certifications.
