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
**Current status:** Implemented in `website/src/styles/global.css`. This is
a **working assumption pending client review** — see
`docs/CLIENT_PREFERENCES.md` "Colours" / "Athangudi influence," both marked
PENDING CLIENT INPUT. If the client pushes back, update `CLIENT_PREFERENCES.md`
first, then this entry (mark superseded, don't delete), then implement.

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
