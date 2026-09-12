# Decision Log — Vicky / Elite Balaji Website

Chronological record of architectural/design decisions. Check here before
reconsidering something that may already have been decided.

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
