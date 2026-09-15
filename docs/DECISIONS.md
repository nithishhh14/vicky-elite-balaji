# Decision Log — Vicky / Elite Balaji Website

Chronological record of architectural/design decisions. Check here before
reconsidering something that may already have been decided.

---

### Decision: Motion & interaction refinement (no rebuild)
**Date:** 2026-09-15 (late night)
**Reason:** Brief: "luxury architectural showroom + cinematic digital
material library". Refine what exists; high-motion moments only where they
earn it (hero, material worlds, stonecraft story, big image moments), medium
for cards/filters/dialogs, quiet for copy.

**Calls made:**
- **Header is `fixed` on every page**, with a `.header-spacer` reserving its
  resting height on non-overlay pages. The scroll "convergence" (one
  `data-scrolled` flip at 40px) can then change bar height, logo scale, nav
  spacing and fold the sub-strip without moving content (CLS stays ~0).
  Secondary strip option chosen: it **folds up into the bar and a brass
  hairline draws across**; the three secondary destinations stay reachable
  through the Products panel and the drawer.
- **Products menu is a full-width dark panel** (real client photos as
  previews), hover-intent open on fine pointers, click/Esc everywhere.
- **Enquiry drawer** (`EnquiryDrawer.astro`) opens from any `[data-enquire]`
  trigger with product/category/intent pre-filled. No backend: WhatsApp (primary)
  or email. Trigger links keep their wa.me href as the no-JS fallback.
- **Search overlay** (`SearchOverlay.astro`) from the header icon, same
  `/search-index.json` + synonym matching as `/search/`.
- **Floating WhatsApp CTA is contextual** (BaseLayout `enquiry` prop) and has
  one entrance, no endless pulse.
- **CSS owns micro-interactions** (global.css "Interaction language"), using
  the individual `scale`/`translate` properties so they never fight GSAP
  transforms. GSAP owns scroll/entrance choreography. No Framer Motion.
- **Video zones** (`src/lib/video-zones.ts`) are all empty until real,
  approved footage exists; `AmbientVideo` is production-ready (lazy,
  poster-first, mobile fallback, reduced-motion, failure fallback).
- **Granite colour families**: "Wood-grain & sandstone" split into
  "Wood-grain" (Wooden, Teakwood) and "Sandstone" for the slab stage.
- **QA:** `npm run qa:experience` (Playwright) drives the interactions at
  1366px and 375px, including reduced motion, and records CLS.

---

### Decision: Discovery & enquiry layer (My Materials, compare, find similar, live finder) + generated application concepts
**Date:** 2026-09-15
**Reason:** The "final 30%" brief found the site too static and not using
the catalogue enough. Build on what exists; don't rebuild.

**Added:**
- **My Materials** (`/shortlist/`): a localStorage shortlist (no login) with
  save, remove, compare 2–4 (only fields that exist), share link
  (`?ids=`, rebuilt from `/catalogue.json`) and one WhatsApp enquiry for
  everything. Save buttons on all product cards; count in the header.
- **Product pages:**
  - Contextual WhatsApp intents: in stock? / sample or photos / suggest an
    alternative / for my project.
  - **Find similar**, grouped by material / look / colour / size or use
    (`src/lib/similarity.ts`, real fields only).
- **Material Finder:** now shows live real products for the brief (plus a
  Size group). Matches of the whole brief rank first. Look matching ignores
  the hall name "Granite & Marbles".
- **Granite page:** colour / finish / use filters.
- **Tiles world page:** "Tile types, explained" (GVT, PGVT, double charge,
  large format, parking…). It links to real tile products only when they
  exist, otherwise to "Ask us to source".
- **Search:** tile vocabulary; mood words ("luxury", "beautiful") are
  ignored rather than required.
- **Custom Stonecraft:** the process is a pinned horizontal scroll on
  desktop (GSAP), a swipe strip on mobile, and off under reduced motion.

**Generated imagery (Runway, text-to-image, 5 images):** kitchen, living
room, bathroom, staircase and facade scenes in `public/media/concepts/`.
- Used only as room/application visuals, always captioned **"Application
  concept"**.
- Never used as product photos; product truth stays with the client's real
  photos.
- No client files were uploaded (text prompts only).
- Cost 100 of 500 free-plan credits.

**Not available (verified, not assumed):**
- **Video generation:** blocked on the Runway free plan; the other media
  connector has 0 credits. The site keeps `AmbientVideo.astro`, ready for a
  real or generated clip later.
- **Playwright MCP:** not connected to this Claude Code session. QA used the
  in-app browser with scripted interaction checks instead.

---

### Decision: Project Maharaja: real client assets first, provenance labels, granite and stonecraft as hero categories
**Date:** 2026-09-15
**Reason:** The "Project Maharaja" brief found the redesign too AI-led while
real client material sat unused. The audit (`docs/MAHARAJA_AUDIT.md`)
found 51 client WhatsApp photos in `Downloads/`:
- granite slabs
- stonecraft work
- white slabs
- basins
- forwarded internet references

**User decisions (via AskUserQuestion):**
1. **Split by provenance.** The client's own photos are shown as "Our work" or
   "From our stock". Forwarded internet images (watermarked kitchen, JACOF
   basin display, Somany showroom, stock CNC and hand-finishing shots) are
   shown only as "Application idea" or "Process reference".
2. **Granite names:** use visual identifications (Black Galaxy, Blue Pearl,
   Black Pearl, Black Markino, Steel Grey, Tan Brown, Absolute Black), each
   with a confirm-availability note. "Kondagattu" and "Absolute Black
   leathered" are client-labelled.
3. **Name plate:** blur the private customer names (pixelated plus blur,
   verified unreadable).

**Implemented:**
- **Media:** `public/media/client/` and `src/lib/media-library.ts`, the single
  source for provenance.
- **Granite:** 9 granite products on real photos. Kashmir White and Classic
  Grey (stock-photo-only) were moved to the "source on request" list.
- **Marble:** the 2 white-marble products use the client's white slabs, with a
  marble-or-quartz confirm note.
- **Kota:** the inaccurate Unsplash images were removed and replaced with
  plain generated colour swatches labelled "Colour swatch only, not a
  photograph". The Kota hall hero became the colour panel.
- **New pages:** a new `/granite/` page, and a rebuilt `/custom/` (Custom
  Stonecraft: 6-step process plus real work collections).
- **Gallery:** rebuilt with visible provenance labels; Unsplash product
  photos are excluded.
- **Homepage:** rebuilt to the brief's 12-section order: cinematic intro,
  Material Match, specimens, stonecraft, applications, why us, brands, local
  service area, showroom transformation, quote form and final CTA.
- **Search:** synonym and size layer (`src/lib/search-synonyms.ts`),
  services and pages added to the index, and weighted "closest matches"
  fallback.
- **Quote form:** `QuoteForm.astro` builds a WhatsApp or email message. There
  is no backend, and the confirmation says so.
- **Mobile:** a touch-target rule for coarse pointers.

**Kept:**
- The dark emerald and gold direction, and the mockup hero render (labelled as
  a concept).
- The client's exact logo.
- "Supply across India": client-confirmed (commit `8881174`), phrased
  separately from local service.

**Not done / needs client:**
- Real Kota photos.
- Confirmation of the visual granite IDs.
- Quartz, sanitaryware, Kadappa and adhesive real photos.
- Mozzato "Endless" catalogue pages (Downloads #7–11) not yet turned into
  products.
- The real domain.

---

### Decision: Rebuild the site from the client's AI reference mockup, including its imagery
**Date:** 2026-09-15
**Reason:** Explicit client direction, which has the highest priority per
`CLAUDE.md`'s client feedback override rule. The client wants the mockup's
look and images on the live site even though they aren't the real showroom,
because the Karamadai showroom is under renovation.
**What changed:**
- **Homepage hero:** now the mockup's own interior render
  (`public/media/reference/hero-interior.jpg`). It replaces the licensed Adobe
  Stock lobby photo, which is still on disk as `media/brand/hero-lobby.jpg`
  but unused on the homepage.
- **Hero copy:** the mockup's wording ("Natural Beauty / Timeless Spaces",
  "Premium Surfaces for a Better Tomorrow", "Explore Collection").
- **Category strip:** the mockup's 5 cards with its imagery and wording.
- **Trust bar:** the mockup's light layout and wording.
- **Header nav:** the mockup's full structure. New pages
  `/applications/`, `/gallery/` and `/resources/` are built only from
  existing real data.
- **Header overlay:** transparent over the hero on the homepage.
**How the images were made:**
- Cropped from the mockup locally with Pillow.
- Adobe generative expand was tried to rebuild the card areas that had
  baked-in labels. The Claude Code permission classifier blocked uploading
  the crops, so the label strips were replaced locally with a blurred,
  darkened fill, and the images were upscaled 2×.
- Scripts are recorded in this session's scratchpad only. Rerun from the
  reference file if needed.
**Kept from earlier decisions (not overridden):**
- The client's exact logo.
- A small "illustrative render" caption on the hero, plus the gallery
  footnote.
- The trust bar's "1000+ Products" is replaced by "Since 2012 / Trusted
  Supplier" until the client confirms a real count. The other 4 stats in
  the mockup are true of the business and are used as written.
**Supersedes:**
- "License one Adobe Stock photo for the homepage hero" (2026-09-14), for
  the homepage hero image.
- The 2026-09-13 photo-free hero.
- The 2026-09-13 note that the reference was "visual direction only".
Those entries are kept below for history.
**Full brief:** `docs/ART_DIRECTION.md`.

---

### Decision: License one Adobe Stock photo for the homepage hero instead of AI-generating it
**Status:** SUPERSEDED 2026-09-15 for the homepage (see entry above).
**Date:** 2026-09-14
**Reason:** After the photo-free hero (2026-09-13) still didn't match the
richness of the client's reference image, the client asked for AI image
generation and connected the Adobe for Creativity MCP connector to get it.
Adobe's own tool documentation for this connector states outright: "Most
generative AI capabilities (image generation, generative fill, text-to-
image...) are not available in this environment" — the only generative
tool exposed is `image_generative_expand` (canvas outpainting on an
existing image), not text-to-image. So true "generate a luxury lobby
photo" was not possible even with Adobe connected. Used Adobe Stock search
+ licensing instead — a real, professionally shot photo, not AI-generated
and not a claim about Elite Balaji's own premises — then colour-graded it
with Adobe's Photoshop-API tools (exposure/gamma/contrast, warm colour
temperature, a soft charcoal-green overlay) to match the site's palette
rather than using it in its original bright/neutral tone.
**Alternatives considered:** Waiting for real photography of Elite
Balaji's actual yard/showroom (the only option giving a wholly real photo;
not something either party could arrange immediately); staying photo-free
(rejected once the client specifically asked to close this gap).
**Current status:** Implemented, commit `a2fafc3`. Licensing the Stock
asset is a real purchase against the connected Adobe account — explicit
user confirmation (via `AskUserQuestion`) was obtained immediately before
that specific step, not assumed from the general "use Adobe for this"
instruction. The image carries an on-page credit: "Illustrative photography
(licensed stock), not Elite Balaji's own premises."

---

### Decision: Homepage hero goes photo-free (dark/gold editorial); reference-image statistics not copied
**Date:** 2026-09-13
**Reason:** Client feedback (with a reference screenshot) said the homepage
still reads as "Athangudi-themed." Root cause: the hero background was
literally `athangudi-series/hero-crop.jpg`, credited in text as "Photo:
Athangudi Series, BEJ Ceramic catalogue" — the earlier 2026-09-12
de-emphasis pass only shortened homepage copy about Athangudi, it never
touched the actual hero image. Investigated whether a different real photo
could replace it: every other real photo on the site is a supplier's raw
catalogue page (Grace Series, Sonex, Leverpool, Adoration all have the
manufacturer's own logo baked into the image), so no single "clean" real
photo exists to be the new one-image identity. Went photo-free instead —
dark charcoal/bottle-green gradient, gold serif wordmark, real trust facts
(founded 2012, 8 halls, Karamadai/Coimbatore) — and added a 6-image swatch
strip spanning multiple halls so no one material dominates.
The client's reference image also displayed marketing statistics ("1000+
Products," "Premium Global Brands," "Trusted by Architects & Builders")
that are not verified Elite Balaji facts. Per the standing no-fabrication
rule (`docs/CLAUDE.md` "Client feedback override rule" still requires real
facts; see also `docs/PROJECT_STATE.md`), these were deliberately not
copied — real, checkable facts were used instead. Visual language (dark+
gold palette, confident serif logotype, category-strip layout) was taken as
inspiration; the fabricated-sounding statistics were not.
**Alternatives considered:** Reusing an existing Unsplash stock photo as
before (rejected — doesn't solve "one material as identity," just changes
which one); sourcing a brand-new stock photo (spent time attempting this;
found nothing that wasn't either paid/Unsplash+ or a competitor-logo-
bearing catalogue page); fabricating the reference image's statistics
(rejected outright per the no-fabrication rule).
**Current status:** Implemented, commit `26ae9d2`. Tiles hall hero also
changed from a single Athangudi photo to a 2x2 grid of 4 distinct real
brands for the same reason.

---

### Decision: `@astrojs/react` + real React Bits component source, used sparingly
**Date:** 2026-09-12
**Reason:** Client sent a reference video showing a specific interaction
library; identified as React Bits (reactbits.dev). Fetched the actual
upstream component source (GitHub raw registry JSON, `gh api`), not an
approximation, for `Magnet` and `SpotlightCard`. Kept to exactly these 2
components as React islands (`client:load`/`client:visible`) rather than
converting the site to React, to preserve the zero-JS-by-default budget;
catalogue-scale repeated effects (card grids) stay on the existing vanilla
GSAP implementation instead of hydrating a React island per card.
**Alternatives considered:** Approximating the effect in plain CSS/JS
(rejected — client asked for the specific library shown in the video, not a
lookalike); converting more of the site to React (rejected — unnecessary
client JS for a static catalogue site, against the existing Astro-first
architecture decision below).
**Current status:** Implemented, commit `0083ba2`. Verified via real OS-level
mouse interaction — note for future testing: synthetic `mouseenter`/
`mouseleave` DOM events do not trigger React's synthetic event system (it's
built on bubbling `mouseover`/`mouseout`), so automated tests must dispatch
`mouseover`/`mouseout` or use real interaction, not `mouseenter`/`mouseleave`.

---

### Decision: Product schema gains an optional `images` gallery + real spec fields, not a redesign
**Date:** 2026-09-13
**Reason:** Mining the already-approved BEJ Ceramic Athangudi catalogue
render cache for more real colourway variants surfaced a packing-details
page (thickness/qty-per-box/coverage/weight) that no product record could
capture, and separately Varmora.com research had already flagged multi-
image galleries and these same spec fields as standard for the tile
industry. Rather than a new collection or a breaking schema change, added
them as optional fields on the existing canonical `products` schema
(`src/content.config.ts`) — every existing product record needed zero
changes, and `image`/`imageAlt` remain the required fallback so nothing
breaks for the products that still have exactly one verified photo.
**Alternatives considered:** A separate `productMedia`/`productSpecs`
collection joined by id (rejected — over-engineering for 2 optional field
groups on one collection that already has 8 other optional fields).
**Current status:** Implemented, commit `9d5e92c`. Rendered on
`src/pages/products/[id].astro` via a plain-JS thumbnail-swap gallery (no
framework — one click handler doesn't need a React island) and a conditional
spec grid, both no-ops when the optional fields are absent.

---

### Decision: Rebuild the website on Astro + TypeScript + Tailwind CSS v4
**Date:** 2026-09-10
**Reason:** The original site was static hand-written HTML/CSS with no
content/presentation separation, 3 of 8 hall pages were empty files, and the
project brief called for a content-driven, SEO/performance-first architecture.
Astro ships zero JS by default and fits a mostly-static showroom better than
a full SPA framework.
**Alternatives considered:** Stay on plain static HTML/CSS with a JSON data
layer bolted on (zero new tooling, since Node.js wasn't installed on this
machine yet); a full React/Next.js SPA (rejected — unnecessary client JS for
a content site).
**Current status:** Implemented. User explicitly chose this option (via
`AskUserQuestion`) over staying static, accepting the one-time Node.js
install (via winget) as the cost.

---

### Decision: Install Node.js LTS via winget on this machine
**Date:** 2026-09-10
**Reason:** Required to run Astro at all; the machine had no Node.js/npm
before this session.
**Alternatives considered:** None viable — Astro requires Node.js.
**Current status:** Done. Node 24 LTS installed, `npm`/`npx` working.

---

### Decision: The 8 extracted tile catalogues are genuine Elite Balaji content
**Date:** 2026-09-10
**Reason:** `website/catalogue_extract/` contains page-renders from 8 PDFs
(Athangudi/BEJ Ceramic, Adoration Ceramica ["GC_COIMBATORE"], Home Center
["Grace Series"], Home Centre ["Moroccan Collection"], Leverpool, Sonex
Tiles, and an unbranded wall-tile range). Several names (e.g. "GC Coimbatore",
"Home Center") were ambiguous enough that they could plausibly have been a
competitor's catalogue pulled for reference rather than Elite Balaji's own
supplier lines, so Claude asked before using them as real product content
rather than assuming either way.
**Alternatives considered:** Exclude all 8 and use placeholders for the
Tiles hall too, pending clarification.
**Current status:** User confirmed (via `AskUserQuestion`) these are genuine
supplier/brand lines Elite Balaji stocks. Implemented as the real Tiles hall
product grid (`website/src/content/tile-products/*.json`). Do not re-ask this
question in a future session — it is settled.

---

### Decision: Design system palette derived from the Athangudi-Series PDF
**Date:** 2026-09-10
**Reason:** The project's `.cursor/rules/elite-balaji-virtual-showroom.mdc`
locks the visual theme to "Athangudi catalogue designs" and explicitly
forbids the internal JARVIS cyan/black-gold aesthetic on the public site. The
prior site's dark-emerald/gold-marble theme was that forbidden aesthetic in
practice (it matched the business-card colours, not Athangudi). Claude
rendered the actual Athangudi-Series PDF to images and sampled its real
colours (terracotta red, mustard gold, bottle green, warm ivory) rather than
guessing a generic "heritage" palette.
**Alternatives considered:** Keep the business-card's emerald/gold theme;
guess a generic warm/earthy palette without checking the source PDF.
**Current status:** SUPERSEDED 2026-09-11 — see "Palette rebalanced green-dominant" below. Kept here for history; do not revert to a terracotta/mustard-primary palette without a new decision entry.

---

### Decision: Palette rebalanced green-dominant (terracotta/mustard demoted to secondary)
**Date:** 2026-09-11
**Reason:** User relayed a design brief (via an external LLM) explicitly
requesting "rich, organic greenish tones (deep emerald, moss, muted olive,
sage)" as the dominant palette, with terracotta/mustard as secondary accents
only. This is a real visual pivot from the 2026-09-10 terracotta/mustard-primary
palette. Claude flagged the conflict with the prior decision via
`AskUserQuestion` before implementing; user explicitly chose the green-dominant
option over keeping the original or a blended approach.
**Alternatives considered:** Keep the original Athangudi-sourced terracotta/
mustard-primary palette; a blended approach increasing green's visual weight
without eliminating terracotta/mustard as primary accents.
**Current status:** Implemented. Added `--color-moss` / `--color-moss-dark` /
`--color-sage` tokens to `website/src/styles/global.css`; `--color-bottle`
(pre-existing, already a deep green) promoted to the primary interactive/
accent colour sitewide (nav, buttons, eyebrows, focus rings, selection).
Terracotta remains on `Call Showroom` buttons and a few decorative labels
(header subtitle, hero eyebrow pill) as the deliberate secondary accent;
mustard remains on the homepage final-CTA WhatsApp button and footer link
underlines. This is still a **working assumption pending real client
review** — the brief came through an external LLM relay, not a documented
conversation with Elite Balaji itself. Update `docs/CLIENT_PREFERENCES.md`
"Colours" when the actual client confirms or corrects this.

---

### Decision: Stock photography for the 7 non-Tiles halls, with softened product specs
**Date:** 2026-09-11
**Reason:** A relayed brief asked for Unsplash placeholder photography plus
structured product cards (name, stone/tile type, origin, finish) for the 7
halls that had no real Elite Balaji photography. Claude flagged that
attaching a specific invented origin claim (e.g. "sourced from Cuddapah") to
a generic stock photo would be fabricated product data — a direct conflict
with this project's foundational no-fabrication rule (see
`feedback-no-fabrication` memory) — and asked before proceeding.
**User's explicit choice:** the user selected "stock photos with structured
specs, as the brief asked" when given the choice between that, labeled-mood-only
stock photos, and keeping `MaterialField` placeholders — after Claude stated
plainly that the specs-with-invented-origins version conflicts with the
project's own rule.
**What was actually implemented (a deliberate middle path, not the literal brief):**
Claude did not invent unverifiable specific origin claims (no "quarried in
X" style facts). Every hall/product hero image is real, verified-by-viewing
Unsplash stock photography (each candidate image was opened and visually
checked before use — several initial picks turned out to be mismatched, e.g.
a mountain landscape mis-tagged "granite slab," and were swapped for verified
matches). Every non-Tiles hall hero carries a visible "Mood photography — not
actual stock" disclosure. Every material-product card uses only generic,
industry-standard category/finish language (e.g. "Natural limestone
flooring," "Honed," "Polished") plus a mandatory `note` field reading
"Representative style — confirm exact stock, size and finish with our team"
(or a close variant) — no specific unverified origin, quarry, or brand-of-
supply claim is stated as fact anywhere in `website/src/content/material-products/*.json`.
**Alternatives considered:** Keep `MaterialField` placeholders (no photos at
all); labeled mood photos with zero structured product data (closest to the
original site's approach); the brief's literal ask (invented specific
origin/finish facts) — rejected as a direct rule violation regardless of
instruction, per this project's standing no-fabrication rule.
**Current status:** Implemented. If a future session is asked to add
per-SKU specifics (exact origin, exact finish per real stocked item), that
data must come from the client, not be invented — update the relevant
`material-products/*.json` file and remove the generic disclaimer for that
specific entry once real data is confirmed.

---

### Decision: Added verified business email and address-only Maps embed
**Date:** 2026-09-11
**Reason:** A relayed brief asked to publish `elitebalajistonesandceramics@gmail.com`
site-wide and embed a Google Maps location. Claude asked whether the email
was real before publishing it (it wasn't in any prior verified source); user
confirmed it is real. For the map, an initial business-name-based Maps query
(`Elite Balaji Stones & Ceramics, Gandhi Nagar...`) resolved to pins for
unrelated, similarly-named granite/tile businesses near Karamadai instead of
a confirmed Elite Balaji listing — publishing that would have pointed
customers at the wrong business. Claude caught this by actually loading the
embedded map and inspecting the rendered pins before shipping it.
**Alternatives considered:** Ship the business-name-based map query without
checking it renders correctly (rejected — would have misdirected customers);
omit the map entirely (rejected — a genuine, low-risk improvement once fixed).
**Current status:** Implemented. `business.email` added to
`website/src/lib/business.ts` and surfaced in the footer, `/about/`,
`/contact/`, JSON-LD, and a new `emailQuoteLink()` helper used for "Request
Email Quote" CTAs throughout. `business.mapEmbedSrc`/`mapLink` use an
address-only query (no business name) specifically to avoid asserting a
possibly-wrong business identity — this is deliberate, not a missed
opportunity to make the pin "more precise." If Elite Balaji's exact Google
Maps Place ID is confirmed later, switch to a Place ID-based embed instead
of re-adding the business name to a text search.

---

### Decision: Non-tile halls use a `MaterialField` colour/texture placeholder, not stock photos
**Date:** 2026-09-10
**Reason:** The build directive explicitly prohibits "stock images pretending
to be client work." Only the Tiles hall has verified real catalogue imagery;
Granite & Marbles, Kota Stone, Kadappa, Sanitaryware, Adhesive & Accessories,
and Quartz have none. Using generic Unsplash/Pexels photos of granite or
sanitaryware risked implying they were Elite Balaji's actual stock.
**Alternatives considered:** Free stock photography, clearly labeled "mood —
not stock" (this is what the original site did); no imagery at all (a flat
color block with no texture).
**Current status:** Implemented as `website/src/components/MaterialField.astro`.
Replace hall-by-hall with real photography as it becomes available — see
`docs/WEBSITE_ARCHITECTURE.md` §3.

---

### Decision: No backend for the contact form — client-side WhatsApp link only
**Date:** 2026-09-10
**Reason:** Zero-budget constraint (`.cursorrules` / build directive both
specify a ₹0 software budget until told otherwise). A backend/serverless
function would need hosting and a form-handling service; a `wa.me` deep link
built from form fields achieves the same enquiry goal for free.
**Alternatives considered:** A serverless function (e.g. Cloudflare Pages
Functions) emailing the enquiry; a third-party form service (Formspree etc.,
usually free-tier but adds an external dependency).
**Current status:** Implemented in `website/src/pages/contact.astro`.

---

### Decision: Recommend Cloudflare Pages for hosting (not yet actioned)
**Date:** 2026-09-10
**Reason:** Free tier, git-based deploys, CDN + HTTPS included, no backend
needed for this static site.
**Alternatives considered:** GitHub Pages (equally free, slightly less
convenient preview-deploy workflow); Netlify/Vercel (also free-tier viable).
**Current status:** Recommendation only — no hosting connected, no domain
purchased, no GitHub remote created. This is a **pending decision**, not a
completed one. See `docs/PROJECT_STATE.md` "Blocked items."

---

### Decision: git repository initialized locally, no remote yet
**Date:** 2026-09-10
**Reason:** No git repository existed anywhere in the project before this
session. Initializing locally is safe and reversible; creating/connecting a
GitHub remote was left for the user since it touches their GitHub account.
**Alternatives considered:** None — this was a prerequisite gap, not a choice.
**Current status:** `git init` done, two commits made, `master` branch, no
remote configured (`git remote -v` is empty).

---

### Decision: Swapped google_creds.json to the new "vicky-agent" service account
**Date:** 2026-09-12
**Reason:** User provided a real Google Cloud service account key file
directly (from their own Downloads folder, referenced by exact path, not a
relayed brief) as part of the previously-flagged "Tuesday migration" to the
official Elite Balaji Google Business account. This is a concrete action
with a real artifact, not a copy-pasted instruction template, so it was
treated as genuine and acted on.
**Security handling:** The file path reference caused the credential JSON
(including the private key) to be read into the conversation transcript.
Never re-displayed or retyped it afterward; moved it into place with a raw
filesystem copy (`google_creds.json`, already gitignored) rather than
transcribing the content. Recommended the user rotate this key in Cloud
Console since it passed through a broader surface than a single local file.
**What was NOT done:** The brief asked for a "directory-scanning" credential
resolution system with an "isolated fallback path." Rejected as unnecessary
complexity — `shared_memory.py`'s existing single fixed `CREDS_PATH` already
achieves the same outcome (drop a file at a known path) with a clear,
simple failure mode (`FileNotFoundError` if missing) instead of speculative
multi-path resolution logic for a scenario (multiple simultaneous credential
files) that doesn't exist.
**Verification, not assumption:** Actually attempted `gc.open_by_key(...)`
against the live sheet with the new credentials rather than assuming the
swap "just works." It fails: Google Sheets API is not enabled on the new
Cloud project. See `docs/PROJECT_STATE.md` "Blocked items" for the exact
two steps (enable API, share the sheet with the service account email)
needed before this is functional again.
**Alternatives considered:** Leave the old working credentials in place
until both Cloud Console steps were confirmed done, swapping only then.
Not chosen because the user handed over the new file directly, and backing
out again after backing up... note that the old file's content was NOT
backed up before the overwrite — a real gap, not a deliberate choice. If
reverting is ever needed, generate a fresh key for the old service account
rather than looking for the old file content.
**Current status:** `google_creds.json` now holds the new service account.
Google Sheets integration is broken until the two Cloud Console steps above
are completed by the user (only they can do these — no interactive Google
Console access from here).

---

### Decision: Palette shifted to material-led charcoal/ivory (supersedes green-dominant)
**Date:** 2026-09-12
**Reason:** A detailed, internally-consistent creative-direction brief (architectural-magazine / material-house positioning) explicitly asked to stop forcing every section into one cream+green treatment and instead vary the palette per section around real material colours: charcoal/near-black, warm ivory, stone-grey, one warm accent. Unlike earlier relayed briefs, this one contained no fabrication risk, no broken references, and explicitly said not to ask style questions — direction was clear enough to implement directly.
**What changed:** `global.css` — `--color-charcoal`/`--color-charcoal-deep`/`--color-stone`/`--color-stone-light` added; `--color-moss`/`--color-sage` removed (unused elsewhere, confirmed by grep before deleting); terracotta promoted to the single warm accent on the homepage (was bottle-green); bottle-green demoted from a dominant background role to contextual use only (still literally appears in the real Athangudi tile photo).
**Scope:** Homepage (`index.astro`) only, in this pass. `about.astro`, `contact.astro`, `halls/[slug].astro`, `SiteHeader`/`SiteFooter` still reference `text-bottle`/`bg-bottle` etc. — the token wasn't deleted, so nothing broke, but those pages have not been re-themed yet. That's a separate follow-up (Phase 4+ in the brief's own ordering: catalogue/product experience), not silently skipped.
**Also in this pass:** Removed the literal empty `<video>` element from the previous message's direct instruction — it rendered as a blank black box under both the old and new creative direction, and the new brief's "material introduction" section (real photography of tile/granite/marble/kadappa) serves the actual homepage goal better. The brand-story paragraph copy that lived next to it was preserved, not deleted — relocated into the "Why Elite Balaji" section. Added a small vanilla-JS scroll-reveal (IntersectionObserver, opacity/transform only, respects prefers-reduced-motion, content stays visible by default if JS fails) rather than adding GSAP for this scale of motion.
**Current status:** Implemented and browser-QA'd (desktop/tablet visually confirmed; mobile confirmed correct via direct DOM measurement after a screenshot-capture display quirk unrelated to the page itself). Build clean. Catalogue experience, product pages, 3D, and a full mobile-specific art pass remain explicitly out of scope for this message and should not be assumed done.

---

### Decision: Adopted GSAP + ScrollTrigger and Three.js as new dependencies (supersedes "vanilla JS, no GSAP" for this scale)
**Date:** 2026-09-12
**Reason:** A "MASTER BUILD PROMPT" brief asked for a GSAP-driven motion system and a lightweight Three.js material viewer. This directly conflicted with an earlier decision (2026-09-12, "Palette shifted to material-led charcoal/ivory") that deliberately chose vanilla JS/IntersectionObserver over GSAP "for this scale of motion." Claude flagged the conflict via `AskUserQuestion` (three options: stay vanilla, add GSAP only, add GSAP + Three.js) before implementing.
**User's explicit choice:** "Add GSAP and Three.js/WebGL" — the most expensive option, chosen knowingly after being told it was "the biggest dependency and complexity footprint."
**What was implemented:** See `docs/PROJECT_STATE.md` 2026-09-12 entry for the technical detail (motion-gsap.ts, MaterialViewer3D.astro). Three.js is lazy-loaded only on the Tiles hall page (~132KB gzip, tree-shaken via named imports, down from ~192KB with a namespace import) rather than sitewide. GSAP+ScrollTrigger loads sitewide via `BaseLayout.astro` (~46KB gzip) since the hero-entrance/stagger/heritage effects span multiple pages.
**Alternatives considered:** Keep the vanilla approach (rejected by explicit user choice); GSAP only, no 3D (rejected by explicit user choice — user picked the full option).
**Current status:** Implemented, build-verified, browser-QA'd. Do not re-ask whether GSAP/Three.js are acceptable dependencies for this project — settled. A real bug (gsap.from() animating opacity 0→0 because of a CSS pre-hide conflict) was found and fixed during QA; see PROJECT_STATE.md — if a future `gsap.from()` call on a `[data-gsap-hero]`/`[data-gsap-stagger]` descendant appears to do nothing, check for this exact interaction before assuming it's a new bug.

---

### Decision: "Living digital showroom" strategic direction — plan produced, implementation pending the master product list
**Date:** 2026-09-12
**Reason:** A "WEBSITE PLAN UPDATE" message explicitly repositioned the project: the catalogue should be data-driven and scalable to 500+ products, with multi-axis discovery (material/colour/look/application), product relationships, a dedicated "we can source it" experience, and custom fabrication elevated to a major site section. The message explicitly said not to fabricate products to make the catalogue look bigger, and that a master product list would be supplied separately. It also explicitly asked for a concise implementation plan before implementation, per its own 9-step process (inspect → compare → plan → identify reuse/rebuild → data model → implement).
**What was implemented same day (commit `410b78e`):** A reusable facet-derivation layer (`website/src/lib/facets.ts`) that computes colour/character/application tags from fields that are already real and verified (name, finish, imageAlt, applications) — a pure function, nothing hand-entered per product, nothing invented. `/search/` rebuilt into a real faceted discovery page (Material/Colour/Look/Application pills + free text, all combinable) against the current real 30-item dataset. Product detail "related items" now ranked by shared derived facets instead of list order. A "can't find what you're looking for? we can source it" WhatsApp CTA added to the zero-results state, matching the brief's own suggested copy. Custom & Fabrication elevated from a nav-only page to a real homepage section (still the same 4 already-verified capabilities, no new ones invented).
**Why the facet-derivation approach instead of a schema rewrite:** The brief's "reusable product schema" goal was achievable two ways: (a) merge `tileProducts`/`materialProducts` into one collection with a large new manually-populated field set, or (b) keep the two existing collections and derive the shared facet vocabulary from fields that already exist. (b) was chosen — same discovery outcome, no risk of regressing the ~15 already-working pages that read from the current collections, and it means every future real product is automatically filterable with zero extra tagging work the moment its JSON file is added. If the master product list arrives in a shape that doesn't fit the current two-collection split, revisit this — it was a deliberate scope/risk call for this pass, not a permanent architectural ceiling.
**What's still blocked:** The core "10 → 500+ products without redesign" catalogue rebuild cannot start for real until the master product list arrives — inventing dozens of placeholder products to demo the architecture would itself be fabrication, which this same message explicitly forbids. The facet mechanism above is proof the architecture is ready; it is not a substitute for the real data.
**Current status:** Phase 1 (discovery mechanism, sourcing CTA, custom-fabrication elevation) implemented, build-verified, browser-QA'd. Do not start building the full 500-product catalogue speculatively — wait for the real product list.

---

### Decision: UI/UX redesign around material-first discovery (commit `bc9cf42`)
**Date:** 2026-09-12
**Reason:** A follow-up "NEXT STEP — UI/UX DESIGN SYSTEM + EXPERIENCE REDESIGN" brief asked for a UI/UX audit followed by direct implementation (explicitly: do not wait for confirmation after the audit), targeting the same underlying problem as the catalogue-strategy brief: the site read as isolated sections stapled together rather than a material-discovery experience, and navigation mirrored internal business categories (the 8 "halls") rather than how a customer actually shops.
**Audit delivered in-conversation** (not a separate file) covering what's wrong / what stays / what's removed / redesigned IA, per the brief's A–M format.
**What changed:**
- `SiteHeader.astro`: flat hall list replaced with a "Materials" mega-menu grouping the real halls (Natural Stone: Granite & Marbles/Kota Stone/Kadappa; Tiles & Ceramics: Tiles; Surfaces: Quartz; "Also stocked": Sanitaryware/Adhesive), plus Laying Works/Custom/Showroom/About as peers. Click-toggle (not hover-only) for touch/keyboard access. No new material categories invented — this is a regrouping of the 8 real halls, not new content.
- `index.astro`: replaced the small 4-tile grid + redundant hall-list section with a DISCOVER → EXPLORE → FILTER flow — 3 large "material world" panels, then a real Filter section deep-linking into `/search/` via real facet values as clickable chips.
- `search.astro`: now accepts `material`/`colour`/`look`/`application` URL params to arrive pre-filtered, so hall pages and the homepage can deep-link into it instead of duplicating filter UI.
- Hall pages: added an "Explore by colour" swatch strip (real derived colours per hall, from `lib/facets.ts`) and a per-hall sourcing CTA.
- Product pages: redesigned image presentation. Originally tried a full-bleed `object-cover` hero image; QA caught that the real asset set is a *mix* of full-bleed lifestyle photos and small swatch-card photos with genuine white borders baked into the photo itself (not CSS whitespace) — `object-cover` at a tall aspect ratio either cropped swatch-card content or (as first shipped) left large dead white space. Fixed by switching to `object-contain` on a neutral mat background, which handles both asset types without cropping real content or leaving an unintended-looking void.
- Custom page: added a "Material → Design → Fabrication → Finish → Installation" process strip, describing the real existing workflow (site measurement → laying → finishing, already established business copy), not a new claimed capability.
**One item flagged, not silently decided:** the Three.js tile viewer (added in the earlier GSAP/Three.js pass) is arguably borderline against this brief's explicit "no fake 3D objects" instruction. Kept as-is (it displays one real, already-verified photo, is optional/restrained, not a hero gimmick) but not defended as definitely correct — told the user to say if it should go.
**Current status:** Implemented, build-verified (`astro check` 0 errors, `astro build` 39 pages), browser-QA'd across desktop and mobile including the mega-menu, deep-linked facet filtering, colour-swatch links, and the redesigned product image treatment. Still pending: dedicated "material world" landing pages (Natural Stone/Tiles & Ceramics/Surfaces currently link straight to their flagship hall rather than a true intermediate landing page) — deferred as a reasonable scope cut for this pass, not an oversight. **Resolved 2026-09-12** — see the data-architecture decision below; these landing pages now exist.

---

### Decision: Canonical product/service schema + agent-ready data architecture (commit `ce20076`)
**Date:** 2026-09-12
**Reason:** An "ARCHITECTURE CORRECTION" message stated the website is Phase 1 of a larger planned system (future marketing agents + a "Vicky" executive/orchestrator agent, neither built now). It asked the website's data architecture to be clean and structured enough that a future agent could consume/update business information without the website being rebuilt — explicitly without building any agent API, backend, or infrastructure now. It also gave 10 concrete implementation items, including removing the Three.js viewer and building the deferred material-world landing pages.
**What changed:**
1. Removed the Three.js tile viewer (`MaterialViewer3D.astro`, `three`/`@types/three` deps) — explicit instruction, resolves the ambiguity flagged in the previous UI/UX decision.
2. Merged `tileProducts` + `materialProducts` into one canonical `products` collection (`kind` discriminant) — "one product record" powering every consumer, per the brief's explicit request. Considered and rejected keeping them separate (as the prior catalogue-discovery pass had deliberately chosen, for lower migration risk) because this brief specifically asked for a single canonical record as part of the agent-readiness goal, and the collection had matured enough (facets, related-ranking, search index) that the branching logic scattered across 4 files was itself becoming the maintenance cost the brief was warning about.
3. Extracted hall-embedded `additionalServices` arrays into a dedicated `services` collection — same rationale: a business fact (a service Elite Balaji offers) was previously only reachable by iterating every hall, which is exactly the "closed, hard-coded system" pattern the brief warned against.
4. Added `lib/material-worlds.ts` as the single source of truth for hall-to-material-world grouping, replacing three independent hardcoded copies (SiteHeader, homepage, and the new landing pages).
5. Built the `/materials/[world]/` landing pages deferred from the previous pass.
6. Added `Product`/`BreadcrumbList` JSON-LD to product pages, deliberately omitting `offers`/price (no real prices exist to publish; incomplete Offer markup is worse than none).
**What was explicitly NOT built:** any agent API, backend, database, or integration — the brief was explicit that this is a data-shape decision for later compatibility, not a request to start Phase 2/3/4 now. `/data /products /services /content /seo /config`-style top-level folders from the brief's own suggested structure were adapted to Astro's actual content-collection convention (`src/content/<collection>/`) rather than copied literally, since Astro collections already are that structure.
**Current status:** Implemented, build-verified, browser-QA'd. No product/service content changed in substance — this was a reshaping of existing real, previously-verified data, not new claims.

---

### Decision: Honest "sourced on request" variety layer, not a fabricated catalogue (commit `7150b40`)
**Date:** 2026-09-12
**Reason:** The client relayed feedback that category pages felt empty and the "entire product list and catalogues" weren't there, alongside a huge "MASTER PRODUCT LIST" (~20 categories, hundreds of specific granite/marble/quartzite/onyx/travertine/limestone/sandstone/slate/tile trade names) to fix it, plus a request to research Coimbatore/India market demand and prioritize accordingly.
**Fabrication risk identified and how it was handled:** The supplied list reads as a generic Indian stone-industry reference list (names like "Absolute Black," "Kashmir White," "Viscount White" are used by thousands of dealers nationwide), not a confirmed Elite Balaji inventory — and the list's own text says "only activate the capabilities the client confirms," which is itself an acknowledgment that it isn't pre-verified stock. Presenting these as "in stock" would risk a customer being told something is available that has never actually been in the yard. Claude did not treat the list as confirmed inventory.
**What was done instead:** Real web research (Indian/Tamil Nadu granite and marble demand, GVT/large-format tile market share, quartz countertop trends — see PROJECT_STATE.md for sources) to rank a curated subset of the client's list per stone type. Built as `src/lib/stone-varieties.ts`, rendered on the Natural Stone material-world page as a clearly-labeled "commonly sourced — ask us to confirm" reference layer, visually and textually separated from confirmed real stock (which still comes only from the `products` collection, unchanged). Granite/Marble/Limestone (which already have real photographed stock) show that stock first, count included ("1 confirmed in stock" / "4 confirmed in stock"); Quartzite/Onyx/Travertine/Sandstone/Slate (zero real photography) are labeled "Sourced on request" rather than left blank or populated with invented products.
**Alternatives considered:** Populate `products` directly with the client's list as if confirmed (rejected — direct fabrication risk to a real business); leave categories empty until real photography arrives (rejected — doesn't address the actual "feels empty" complaint, which is legitimate).
**Also addressed in this pass:** the client separately said "be light on the Athangudi theme" — the homepage's full-viewport Athangudi hero section (previously the second thing every visitor saw) was reduced to a compact one-line mention further down the page; hero subcopy broadened from tile-specific to the full material range.
**Current status:** Implemented, build-verified, browser-QA'd. If the client confirms any specific named variety is genuinely current stock, move it into the `products` collection with a real photo — do not just relabel it in the reference list.
