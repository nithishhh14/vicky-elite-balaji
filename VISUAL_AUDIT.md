# Visual Audit — Current Site vs. Reference Spec

Compared against `REFERENCE_SPEC.md`. Current site inspected live at
`localhost:4321` (desktop 1400px + mobile 375px) as of this audit, not
assumed from code alone.

## §0 — Input material note (read first)

The "reference video" supplied is not usable as an interaction/navigation
specification. It's a generic Instagram design-tips reel (@dylanjcreates,
"Why does your vibecoded app look SO UGLY") that cuts between unrelated clips
— the React Bits component-library site, a generic AI app-builder screen, and
an unrelated concept project ("Aurora Systems"). No stone/marble business
site appears in it, and no single site is scrolled/navigated long enough to
extract real menu/scroll/transition behavior. An `INTERACTION_SPEC.md`
derived from it would be invented, not observed — so it wasn't written. Motion
work below follows the reference *image's* visible intent (restrained,
purposeful) plus the project's existing GSAP conventions, not a fabricated
video-derived spec.

---

## P0 — Fundamentally wrong

**None currently open.** The one P0-grade risk — copying the reference's
stat-bar numbers ("1000+ Products", "Trusted by Architects & Builders") as if
they were real Elite Balaji facts — was caught and avoided from the start
(see `docs/DECISIONS.md`, 2026-09-13 hero decision). Current stat bars use
real, checkable figures instead (founding year, hall count, partner-brand
count, service-hub count).

---

## P1 — Major visual mismatch

### ELEMENT: Primary navigation structure
- REFERENCE: HOME / ABOUT / PRODUCTS / APPLICATIONS / GALLERY / RESOURCES /
  CONTACT, plus a secondary row (NATURAL STONES | PREMIUM SURFACES | TIMELESS
  SPACES).
- CURRENT: MATERIALS (dropdown) / LAYING WORKS / CUSTOM / ABOUT. No secondary
  row.
- PROBLEM: Structurally different information architecture, not just a
  styling gap.
- SEVERITY: P1 — deliberately not fixed yet, not overlooked. APPLICATIONS,
  GALLERY and RESOURCES don't exist as real pages. Adding nav links to pages
  with no real content would recreate the "empty site" complaint from
  earlier in this project. PRODUCTS could reasonably replace/rename
  MATERIALS today; APPLICATIONS/GALLERY/RESOURCES need real content first.
- RECOMMENDED FIX: build the 3 missing pages from real, already-existing data
  (Applications: aggregate every hall's real `applications` field into one
  browsable page; Gallery: a real photo grid pulled from the `products`
  collection's own images; Resources: consolidate the already-built honest
  "sourced on request" reference layers — stone varieties, tile sizes/
  finishes — into one page). Then restructure nav. Not done this pass —
  flagging for explicit go-ahead before building 3 new pages.

---

## P2 — Noticeable mismatch

### ELEMENT: Hero carousel indicator
- REFERENCE: a thin progress bar + "01 02 03" under the trust-icon row,
  implying a multi-slide hero.
- CURRENT: none.
- PROBLEM: n/a — this isn't a gap, it's an intentional exclusion.
- SEVERITY: P2, resolved as "won't fix as decorative-only." The site has one
  hero photo. Non-functional carousel dots implying multiple slides that
  don't exist would be exactly the kind of decoration-without-function this
  project's anti-fabrication/anti-slop rules exist to prevent. If/when a
  second real hero photo exists, a real 2-state carousel becomes worth
  building — not before.

### ELEMENT: Hero eyebrow copy tone
- REFERENCE: aspirational marketing copy ("Natural Beauty / Timeless
  Spaces").
- CURRENT: a factual line ("Since 2012 · Karamadai, Coimbatore").
- PROBLEM: different register — reference leads with feeling, current site
  leads with a verifiable fact.
- SEVERITY: P2 — a deliberate, defensible choice (real fact over mood copy),
  not an oversight. Not changing without direction, since the alternative is
  inventing a mood-line that isn't tied to anything real.

---

## P3 — Polish / detail

### ELEMENT: Logo lockup
- REFERENCE: ornate circular badge (compass-star + handshake + ribbon
  flourishes) + 3-line wordmark.
- CURRENT: simplified compass-star badge (no ribbons; handshake motif
  relocated to the "Why Elite Balaji" section where it's large enough to
  read) + 3-line wordmark lockup (wordmark / Stones & Ceramics / Build
  Better Spaces).
- PROBLEM: less ornate than the reference at header scale.
- SEVERITY: P3 — a deliberate simplification, not a miss. The reference's
  full badge has fine detail that's illegible at a 36px header size; cramming
  it in would look muddy, not premium. Current split (simple mark in header,
  full motif large in-page) preserves legibility over literal fidelity.
- RECOMMENDED FIX: none proposed unless the client specifically wants the
  full ornate badge at header size regardless of legibility.

### ELEMENT: Category strip photography
- REFERENCE: Uses the reference's own stock photography.
- CURRENT: Uses this project's real/licensed photography (5 real halls: 3
  material worlds + Sanitaryware + Laying Works).
- PROBLEM: none — this is correct by design. The reference's actual images
  aren't licensed to this project and shouldn't be reused; the layout/hover
  pattern was reproduced, the content was not.
- SEVERITY: P3, informational only.

---

## Summary

| Priority | Open | Resolved / intentional |
|---|---|---|
| P0 | 0 | 1 (stat fabrication avoided from the start) |
| P1 | 1 (nav restructure — blocked on 3 missing pages) | — |
| P2 | 0 | 2 (carousel dots excluded; eyebrow copy kept factual) |
| P3 | 0 | 2 (logo simplified for legibility; imagery kept real) |

The one open, actionable item is the nav restructure, and it's gated on
building 3 real pages first, not on visual work. Everything else the
reference image actually shows (logo lockup, hero composition, hero
typography, right-side text panel, 5-card category strip with hover arrows,
post-strip stat/CTA bar, engraved-gold marble motif) is implemented and
browser-verified as of the last few commits.
