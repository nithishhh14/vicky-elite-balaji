# Elite Balaji — full project context

_Snapshot: 2026-09-21. Written to be pasted into another AI assistant so it can
answer questions without access to the repo. Everything below is verified, not
estimated; where a number came from a live measurement it says so._

---

## 1. The business

**Elite Balaji Stones & Ceramics** — Karamadai, Coimbatore, Tamil Nadu, India.
Trading since 2012. Granite, marble, tiles, kota stone, kadappa, quartz,
sanitaryware, adhesives, plus made-to-order stonecraft (engraving, tulsi
madams, granite furniture).

- Contact person: Vignesh Yadav A
- Address: 12-B, Gandhi Nagar, Mettupalayam Main Road, Karamadai, Coimbatore 641104
- Phone: +91 91590 56767 · Email: elitebalajistonesandceramics@gmail.com
- Service area: Coimbatore / Nilgiris (Mettupalayam, Karamadai, Ooty, Kotagiri,
  Annur, Sirumugai, Saravanampatti, Thudiyalur, RS Puram). Custom art ships
  pan-India.
- Offer that leads the site: **free on-site measurement**, no charge.

**The showroom is under renovation** — roughly one to two more months. This is
why some imagery is AI-generated: it doubles as the brief for the finished
space. Every such image is labelled on the page.

---

## 2. What exists

Two things, in one git repository:

1. **The website** — live at https://elitebalaji.com
2. **Vicky** — a multi-agent business automation system (Python/Streamlit) that
   will eventually maintain the website, do SEO and draft marketing. Partly built.

---

## 3. Website: stack and architecture

| | |
|---|---|
| Framework | **Astro 7.3.3**, TypeScript, Tailwind CSS v4 (`@theme` tokens) |
| Content | Astro content collections, Zod-validated, `.strict()` — 4 collections: `halls`, `products`, `services`, `guides` |
| Animation | **GSAP + ScrollTrigger**, all inside `gsap.matchMedia`, gated on `prefers-reduced-motion`. No Lenis (deliberate — it degrades mid-range Android scrolling) |
| Interactive bits | React islands only where needed, `client:idle` |
| Hosting | **Cloudflare Pages** (static). Domain + DNS also Cloudflare |
| Repo | GitHub `nithishhh14/vicky-elite-balaji`, private, 77 commits |
| Deploy | Push to `main` → Cloudflare builds → live in ~2–4 minutes. Branch push → private preview URL |
| CI | GitHub Actions runs the full 24-check gate on every push |

**Content scale:** 89 products · 8 halls · 14 local landing pages · 129 built
pages · 401 media files.

### Directory shape
```
website/
  src/content/{halls,products,services,guides}/*.json   ← all content is data
  src/components/*.astro        SiteHeader, QuickActions, EnquiryDrawer,
                                SearchOverlay, MaterialMatch, AmbientVideo…
  src/pages/                    index, granite, marble, custom, applications,
                                gallery, search, shortlist, [guide].astro,
                                halls/[slug], products/[id], robots.txt.ts
  src/lib/                      business.ts (verified business facts),
                                media-library.ts (51 client photos + provenance),
                                image-badge.ts, seo.ts, video-zones.ts,
                                material-worlds.ts, facets.ts, order.ts
  src/scripts/motion-gsap.ts    the whole motion system, 280 lines
  public/media/                 client/, tiles/, basins/, concepts/,
                                illustrative/, swatches/, brand/
  public/_headers               CSP + 8 more security headers
  public/_redirects             301s; documents the no-rename rule
  scripts/                      preflight.mjs, qa.mjs, experience.mjs,
                                check-content.mjs, make-swatch.mjs
```

### The provenance system (important — it shapes every decision)
`src/lib/image-badge.ts` derives a label from the image's folder, so it can
never be forgotten or faked:
- `/media/illustrative/` → **"Illustrative image"**
- `/media/swatches/` → **"Colour swatch"**
- unsplash/pexels → **"Reference photo"**
- `/media/client/` → real, credited "From our stock" / "Our work"

Hard rule: no generated or supplier photo may be presented as Elite Balaji's
own stock or work. Automated checks enforce it.

### Quality gate — `npm run preflight`, 24 checks
Content references resolve · astro check · build · page count · real domain ·
robots ↔ domain · sitemap coverage · title 10–65 chars · description 50–160 ·
canonical · OG image · H1 · lang · no placeholders · **no prices anywhere** ·
no broken internal links · no third-party scripts · security.txt · JSON-LD
parses · LocalBusiness schema · security headers served · Playwright all pages
× 3 viewports (1920/1366/375) under enforced CSP · interaction pass · no
console errors.

Currently **24/24 passing**. Nothing is pushed unless it passes.

---

## 4. Live state (verified 2026-09-21)

- `elitebalaji.com` — 200, canonical points to itself
- `www.elitebalaji.com` — 200, canonical points to apex.
  **The www→apex 301 redirect rule is still not created in Cloudflare.**
- robots.txt + sitemap (128 URLs) correct
- All 9 security headers served: CSP, HSTS, X-Content-Type-Options,
  Referrer-Policy, Permissions-Policy, COOP, CORP, X-Frame-Options, cache rules
- `/.well-known/security.txt` published
- Zero third-party scripts, zero cookies, zero analytics

### Measured performance (phone viewport, live)
| | Elite Balaji | The Tile Bros (market leader) |
|---|---|---|
| Load | **4.9 s** | 19.2 s |
| Weight | **1.5 MB** | 11.6 MB |
| Requests | **28** | 132 |
| WhatsApp links | **9** | 1 |
| Phone links | **5** | 2 |
| Real product pages | **89** | 0 |

### Known problem, unfixed
**The mobile hero shows a black screen for ~2.6 seconds.** The headline is
hidden by the GSAP entrance animation, not by loading — measured 2650 ms on a
fast connection and 1975 ms on throttled 4G (slower when the network is
faster, which proves it is the animation timeline). This is the biggest
conversion issue on the site. Fix direction: the hero text should be visible at
rest and animate *from* visible, not be revealed after a delay.

### Homepage structure
13 sections, 14 600 px tall on mobile (~17 screens). Five catalogue cards:
Granite · Marble · Tiles & Ceramics · **Bath Spaces** · Custom Stonecraft —
all now using real photographs (the category was renamed from "Bathroom" to
"Bath Spaces"; ids and URLs still say `bathroom`, so nothing broke).

---

## 5. SEO position

- 14 local landing pages, all ending `-coimbatore`, each backed by real
  products and carrying FAQPage structured data: floor-tiles, wall-tiles,
  bathroom-tiles, vitrified-tiles, large-format-tiles, marble-look-tiles,
  athangudi-tiles, parking-tiles, elevation-tiles, granite-countertops,
  wash-basins, kitchen-sinks, kota-stone, custom-printed-tiles.
- Structured data: LocalBusiness, Product, FAQPage, Breadcrumb.
- **Google Search Console: not yet verified, sitemap not yet submitted.** This
  is why the site does not appear in search yet. The domain is 3 days old.
- **Google Business Profile: verification pending** — the old listing was
  "Sri Balaji Granite" and is being renamed to Elite Balaji; the physical name
  board has not arrived, which video verification needs.
- Brand data is incomplete: only 24 of 89 products carry a `brand` field, and
  values are inconsistent ("Home Center" vs "Home Centre"). Brand *is* already
  fed into the search index, so text search by brand works; there is no brand
  filter UI, and building one now would show a list missing Jaquar and
  Parryware. Recommended order: clean the data → build brand landing pages
  (they win Google traffic) → only then a filter.

---

## 6. Vicky — the automation system

Python + Streamlit. Entry point `app.py`.

| File | Status |
|---|---|
| `app.py` | Streamlit dashboard, live. Now includes an **Operations panel**: approvals queue, daily SEO, campaigns, agent run log |
| `vicky_store.py` | Local data layer over `vicky_data/`. Stdlib only, atomic JSON writes, `SCHEMA_VERSION` on every record |
| `shared_memory.py` | Google Sheet I/O (leads, council log, SEO audits) via gspread |
| `lead_agent.py` | Real scraper — Google Maps/Search harvesting, phone-first lead ranking, Coimbatore/Nilgiris filter |
| `agents/vicky_executive.py` | Intent router + Gemini chat — live |
| `agents/scraper_agent.py` | Wraps lead_agent — live |
| `agents/seo_agent.py` | Writes to the SEO_Audits sheet — live but basic |
| `agents/marketing_agent.py` | **Stub**, intentionally blocked until the site was live |
| `agents/email_agent.py` | **Stub**, drafts only, never auto-sends |

**Not yet built:** the Website agent (the one that would edit content and open
pull requests), the SEO upgrade (Search Console API), Marketing, Email.

### The data directory
```
vicky_data/
  config/    committed — seo_targets.json (23 tracked pages),
             schedule.json (9 jobs + a never-automatic list),
             campaign_templates.json (6 skeletons + no-fabrication rules)
  state/     runtime, gitignored — approvals/, seo/daily/, campaigns/,
             logs/, leads/
  inbox/     photos/ and catalogues/ the client drops in
  outbox/    drafts waiting for a person to post
  backups/   weekly Sheet exports
```

### The intended update flow (built, not yet enforced)
```
request → Vicky edits content on a branch → 24 checks run
        → Cloudflare preview URL → owner approves → merge → live in 2 min
```
Nothing publishes itself. **Branch protection on GitHub is not yet enabled**,
so today the gate is discipline rather than a wall.

Deliberately never automatic: publishing to the live site, posting to Google
Business Profile / Instagram / WhatsApp, sending customer email, changing
business facts, publishing any price.

---

## 7. Hard rules this project runs on

1. **No fabrication.** No invented products, collections, brands, specs,
   stock counts, reviews, ratings, awards or dealership claims.
2. **No prices on the website.** Enforced by an automated check.
3. **Provenance never blurs.** Generated/supplier imagery is always labelled.
4. **The client's logo is used exactly as supplied** — never redrawn or recoloured.
5. **Secrets never committed** — `.env`, `google_creds.json`, `chrome_profile/`.
6. **Never rename a live URL** without a 301 in `public/_redirects`.
7. **Never overwrite an image in place** — `/media/*` is cached for 30 days, so
   a replacement at the same path never reaches visitors. Ship a new filename.
   (Learned the hard way; now documented.)

---

## 8. Security posture

- Static site: no server, no database, no login, no form endpoint. Nothing to
  rate-limit, nothing to inject into.
- Cloudflare free-tier DDoS protection, automatic and unmetered.
- Enforced CSP with no third-party scripts; the site sets no cookies and runs
  no analytics (Cloudflare tried to auto-inject its Web Analytics beacon and
  **the CSP blocks it** — currently an unresolved console error, and the
  decision whether to allow it is open).
- Deliberately public: `search-index.json` (43 KB) and `catalogue.json` (32 KB)
  expose the whole catalogue in two requests. This powers on-site search;
  scraping it is accepted, not preventable.
- Email appears in plain text on the contact page — normal for a local
  business, expect some spam harvesting.
- Real risk is account security, not the site: Cloudflare, GitHub and Google
  accounts all need 2FA.

---

## 9. Open items

**Blocked on the client**
- Real showroom photos once the renovation finishes (1–2 months)
- Two supplier PDFs arrived 2026-09-21 and are not yet imported: Somany
  Bathware "Export Catalogue May 2026" (228 pages, prices already removed) and
  Jaquar "Ice Blue" matt sanitaryware (7 pages)
- Two earlier PDFs were 0 bytes and need re-sending
- Supplier permission for catalogue photos; GSTIN / legal entity details

**Blocked on the owner (dashboard clicks)**
- Cloudflare: create the `www` → apex 301 Redirect Rule
- Cloudflare: decide on Web Analytics (allow via CSP, or turn it off)
- GitHub: enable branch protection requiring the `website-preflight` check
- Google: verify Search Console + submit the sitemap ← biggest SEO blocker
- Google Business Profile: claim and **rename** the existing "Sri Balaji
  Granite" listing rather than create a new one (keeps history and reviews)

**Technical, queued**
- Fix the 2.6-second mobile hero blank
- Import the two supplier catalogues
- Convert `src/lib/media-library.ts` (51 client photos, still TypeScript) into
  a content collection
- Build the Website agent, then upgrade SEO, then Marketing, then Email
- Migrate `google.generativeai` → the `google-genai` SDK
- A larger visual/motion upgrade brief exists (choreographed catalogue card
  reveals, hero → catalogue transition, unified card art direction) — planned,
  not built
- Hero video is Phase 2: `AmbientVideo` + four video zones already support
  desktop/mobile/poster/reduced-motion; every zone is `null` because no
  approved footage exists

---

## 10. Useful facts for answering questions

- Running costs today: ₹0 beyond the domain (~$10.46/yr, auto-renew on).
  Cloudflare Pages, GitHub, Google tools are all free tier.
- Rollback is one click in Cloudflare Pages → Deployments.
- The operator is a solo builder; the client is the business owner. The
  long-term plan is to migrate the whole system to the client's PC with fresh
  credentials, client-owned accounts, and the operator added as a member.
- Competitors: The Tile Bros, Lakshmi Ceramics, Kandhaas, Kurinji, plus
  Karamadai/Mettupalayam shops. Stated goal: dominate them online on truth and
  stone specialism rather than on claims.
