# Visual Audit V2 — Objective Reproduction Accuracy vs. Reference Image

Method: live site inspected at 1024px width (desktop) via direct browser
screenshot, compared against the reference image frame by frame. This audit
judges reproduction accuracy only — "does this match the reference" — not
whether the current implementation is good on its own terms. A cleaner or
more restrained choice that changes the reference's composition still counts
as a mismatch below.

The previous audit (`VISUAL_AUDIT.md`) was too charitable. It treated
"the element exists somewhere on the page" as a match. This pass measures
scale, proportion, hierarchy and density against the reference, and several
things previously marked resolved are not.

---

### 1. HEADER
- REFERENCE: Two-row header, transparent/dark, sits directly on the hero
  photo with no background separation. Row 1 ~100px tall. Row 2 is a thin
  secondary-link strip.
- CURRENT: Single-row header, opaque cream/ivory background, sits above the
  hero as a separate light bar. No secondary row.
- MATCH LEVEL: 20%
- WHAT IS DIFFERENT: Background colour is inverted (light vs. dark/
  transparent), row count is wrong (1 vs. 2), the header reads as a
  separate UI bar rather than part of the hero composition.
- EXACT CHANGE REQUIRED: Make the header transparent over the hero (dark
  text/gold accents on transparent, transitioning to the existing cream bar
  only once scrolled past the hero — or, if a single treatment is preferred,
  make the always-dark header the permanent state sitewide, not just on the
  hero). Add the secondary link row.

### 2. LOGO SCALE + PLACEMENT
- REFERENCE: Large badge (~60-70px) + 3-line wordmark stack, a substantial
  visual anchor, generous clearance from the header edges.
- CURRENT: 38px badge, ~20px wordmark, the whole lockup reads as a small
  corner detail, not an anchor.
- MATCH LEVEL: 30%
- WHAT IS DIFFERENT: Current logo is roughly half the reference's visual
  weight and doesn't command the header the way the reference's does.
- EXACT CHANGE REQUIRED: Scale the badge to ~56-64px and the wordmark
  proportionally larger; increase header height to accommodate it.

### 3. NAVIGATION
- REFERENCE: HOME / ABOUT / PRODUCTS / APPLICATIONS / GALLERY / RESOURCES /
  CONTACT + secondary row.
- CURRENT: MATERIALS (dropdown) / LAYING WORKS / CUSTOM / ABOUT.
- MATCH LEVEL: 10%
- WHAT IS DIFFERENT: Different item count, different labels, no secondary
  row, different visual scale/tracking.
- EXACT CHANGE REQUIRED: Held per your instruction — no new pages/nav
  destinations this pass. Flagging the number honestly rather than hiding
  it behind "intentionally deferred."

### 4. HERO HEIGHT
- REFERENCE: Hero photo + text occupies roughly two-thirds of the full
  viewport on its own, as a single uninterrupted visual block.
- CURRENT: The hero `<section>` is 92vh tall, but that space is subdivided
  into three stacked pieces — headline block, a dark facts bar, and a
  6-image swatch strip — so the actual photo+headline "hero moment" is
  compressed to roughly the top half of that.
- MATCH LEVEL: 40%
- WHAT IS DIFFERENT: The reference's hero is one uninterrupted statement.
  The current hero is three stacked bands inside one tall section, which
  reads as denser and less confident, even though the outer section height
  is similar.
- EXACT CHANGE REQUIRED: Let the photo+headline occupy the hero's full
  height on its own; move the facts bar and swatch strip out of the hero
  section into their own subsequent section(s), the way the reference
  treats its category strip as a clearly separate block below the hero.

### 5. HERO IMAGE COMPOSITION
- REFERENCE: Asymmetric two-zone photo — a dark textured marble slab
  occupying the left ~40%, blending into a lit interior on the right ~60%,
  with a visible seam between the two.
- CURRENT: One uniform photo (the licensed reception-lobby image) with a
  single dark gradient overlay across the whole frame. No two-zone split.
- MATCH LEVEL: 35%
- WHAT IS DIFFERENT: The reference's composition is doing real work — it
  puts a dark, high-contrast zone exactly where the text sits, and a bright
  "showroom" zone on the other side. The current single-photo-plus-overlay
  approach doesn't reproduce that structure.
- EXACT CHANGE REQUIRED: Either (a) composite the existing licensed photo
  against a dark marble-texture panel on the left third (CSS/gradient, not
  a new photo) so the text sits on a genuinely darker, higher-contrast
  zone, or (b) explicitly accept this as a deliberate deviation and say so
  — but right now it's an unflagged mismatch, not a decision.

### 6. HERO TEXT POSITION
- REFERENCE: Left-aligned block, positioned in the lower-middle two-thirds
  of the hero's height, sitting over the dark marble zone.
- CURRENT: Left-aligned, vertically centred via flexbox across the whole
  hero-text row.
- MATCH LEVEL: 55%
- WHAT IS DIFFERENT: Horizontal alignment matches; vertical placement is
  more centred than the reference's lower-weighted placement.
- EXACT CHANGE REQUIRED: Shift the text block toward the lower half of the
  hero rather than dead-centre.

### 7. HERO TYPOGRAPHY
- REFERENCE: 2-line small caps eyebrow ("Natural Beauty / Timeless
  Spaces") → massive 2-line display headline where the *category* words
  ("Stones &" / "Ceramics") are the huge hero statement, gold-gradient on
  the first line → one-line subhead.
- CURRENT: 1-line factual eyebrow ("Since 2012 · Karamadai, Coimbatore") →
  the *brand name* ("Elite Balaji") is the huge headline, in plain ivory,
  no gradient → "Stones & Ceramics" demoted to a small caps line below it.
- MATCH LEVEL: 35%
- WHAT IS DIFFERENT: This is a hierarchy inversion, not a styling gap. The
  reference makes the category/value-proposition the dominant hero
  statement and treats the brand name as a secondary/logo-level element.
  The current hero makes the brand name dominant and the category
  secondary. Type scale is also noticeably smaller throughout.
- EXACT CHANGE REQUIRED: Restructure the headline so the largest text on
  the page is the category statement, gold-gradient on part of it, with
  "Elite Balaji" living at logo scale (header) rather than repeated at
  hero scale. Increase overall type scale.

### 8. CTA
- REFERENCE: Outlined gold pill, "Explore Collection →".
- CURRENT: Outlined gold pill, "Explore Materials", same visual treatment.
- MATCH LEVEL: 75%
- WHAT IS DIFFERENT: Wording only (a legitimate real-content adaptation);
  size and treatment are close.
- EXACT CHANGE REQUIRED: None required; optional minor size increase to
  match the larger surrounding type if #7 is corrected.

### 9. RIGHT-SIDE INFORMATION PANEL
- REFERENCE: Plain right-aligned stacked text, no border/rule, modest
  size, sits quietly in the frame.
- CURRENT: Same general position and content intent, but has a left
  vertical border rule the reference doesn't have, and reads slightly
  heavier.
- MATCH LEVEL: 55%
- WHAT IS DIFFERENT: An added border element not present in the reference.
- EXACT CHANGE REQUIRED: Remove the left border; rely on spacing alone to
  separate it from the hero photo, matching the reference's quieter
  treatment.

### 10. FEATURE INDICATORS
- REFERENCE: 3 larger line-art icons (~32px) each with a 2-line stacked
  label (bold word / thin word), generously spaced, plus a carousel
  progress bar + "01 02 03" beneath them.
- CURRENT: 3 smaller icons (~20px), single-line labels, no carousel
  indicator.
- MATCH LEVEL: 40%
- WHAT IS DIFFERENT: Icon scale, label structure (1-line vs. 2-line
  stacked), and the carousel indicator are all different. The carousel
  omission is a deliberate, defensible call (there's only one hero photo,
  so dots implying multiple slides would be non-functional decoration) —
  everything else here is an unflagged gap, not a decision.
- EXACT CHANGE REQUIRED: Enlarge icons to ~30-32px; restructure labels to
  2-line stacked to match the reference's typographic rhythm. Leave the
  carousel indicator out unless a real multi-photo hero is built.

### 11. CATEGORY STRIP
- REFERENCE: Cards are tall — roughly 40% of the total viewport height —
  with a 2-line label (bold category name + small caps descriptor
  underneath, e.g. "Granite" / "Natural Strength").
- CURRENT: Cards are `aspect-[3/4]`, noticeably shorter in proportion to
  the reference, single-line label only, no descriptor line.
- MATCH LEVEL: 50%
- WHAT IS DIFFERENT: Card height-to-width ratio is shorter than the
  reference, and the secondary descriptor line is missing entirely.
- EXACT CHANGE REQUIRED: Increase card aspect ratio (taller), add a second,
  smaller descriptor line under each category label (real copy — e.g. a
  short real phrase per hall, not invented marketing).

### 12. STAT / TRUST BAR
- REFERENCE: One single bar, 5 stats + 1 CTA button, evenly spaced with
  vertical divider rules, appears exactly once.
- CURRENT: Split into two separate bars with two different visual
  treatments — a dark facts-row inside the hero, and a separate light
  stat/CTA bar after the category strip.
- MATCH LEVEL: 45%
- WHAT IS DIFFERENT: The reference consolidates this into one clear
  statement; the current site dilutes the same idea across two different
  locations and styles.
- EXACT CHANGE REQUIRED: Consolidate into a single stat/CTA bar (matching
  #4's fix — once the hero stops absorbing the facts row, there's a
  natural single place for this to live), with vertical divider rules
  between items to match the reference's rhythm.

### 13. OVERALL SPACING
- REFERENCE: Generous, editorial whitespace; each element has visible
  breathing room.
- CURRENT: Noticeably more compact — smaller type, tighter padding between
  stacked elements in the hero especially.
- MATCH LEVEL: 40%
- WHAT IS DIFFERENT: Current density is closer to a typical SaaS/business
  site than an editorial luxury layout.
- EXACT CHANGE REQUIRED: Increase padding/margins throughout the hero and
  category strip; reduce the number of stacked elements competing for
  space in the hero (see #4).

### 14. COLOUR BALANCE
- REFERENCE: Dark palette but reads warm overall — the lit interior photo
  bleeds warm light across a large share of the frame.
- CURRENT: Reads cooler/darker overall — the licensed photo sits at 80%
  opacity under a heavy dark gradient, muting the warmth the colour-grading
  pass added.
- MATCH LEVEL: 55%
- WHAT IS DIFFERENT: Overlay is heavier than the reference's, crushing
  photo warmth.
- EXACT CHANGE REQUIRED: Lighten the gradient overlay somewhat, or increase
  photo opacity, so more of the graded warm tone reads through.

### 15. VISUAL DENSITY
- REFERENCE: Sparse, confident — few large elements per screen, high
  negative-space ratio.
- CURRENT: Denser — trust icons, facts bar, swatch strip, and a disclosure
  caption are all stacked inside one hero section.
- MATCH LEVEL: 35%
- WHAT IS DIFFERENT: Direct consequence of #4 and #13 — elements were
  added incrementally over several passes without removing anything,
  compounding density the reference doesn't have.
- EXACT CHANGE REQUIRED: Same fix as #4 — decompose the hero into fewer
  elements per section.

### 16. PREMIUM / EDITORIAL FEEL
- REFERENCE: Reads as a luxury architectural/materials brand.
- CURRENT: Reads as a competent dark-mode business site — correct palette,
  wrong density and hierarchy to earn the "editorial" feel.
- MATCH LEVEL: 40%
- WHAT IS DIFFERENT: This is the compounding effect of #1, #2, #4, #7,
  #13 and #15 together, not a separate issue on its own.
- EXACT CHANGE REQUIRED: Resolved as a consequence of fixing the items
  above, not a separate task.

---

## A. TOP 10 VISUAL MISMATCHES (ranked by impact)

1. Hero headline hierarchy inverted — brand name dominant instead of
   category statement (#7)
2. Header background/structure wrong — opaque light bar instead of
   transparent-over-hero, two-row (#1)
3. Hero section overloaded — 3 stacked bands compress what should be one
   uninterrupted hero moment (#4)
4. Visual density/spacing far tighter than reference throughout (#13, #15)
5. Logo scale roughly half the reference's visual weight (#2)
6. Stat/trust content split across two bars instead of one (#12)
7. Category strip cards too short, missing descriptor line (#11)
8. Hero image is one flat photo+overlay, not the reference's two-zone
   marble/interior composition (#5)
9. Feature-indicator icons/labels smaller and structured differently (#10)
10. Colour balance reads cooler/darker than reference due to overlay
    weight (#14)

## B. P0/P1/P2/P3 CLASSIFICATION

**P0 — fundamentally wrong, reproduces a different composition:**
- Hero headline hierarchy (#7)
- Header background/structure (#1)
- Hero section decomposition (#4)

**P1 — major visual mismatch:**
- Visual density/spacing (#13/#15)
- Logo scale (#2)
- Stat bar consolidation (#12)
- Hero image two-zone composition (#5)

**P2 — noticeable mismatch:**
- Category strip proportions + descriptor line (#11)
- Feature indicator scale/structure (#10)
- Colour balance/overlay weight (#14)

**P3 — polish/detail:**
- Right-side panel border removal (#9)
- Hero text vertical position (#6)

**Not a mismatch — deliberate, held per your instruction:**
- Navigation labels/structure (#3) — blocked on pages you told me not to
  build yet
- CTA wording (#8) — real-content adaptation, not a gap
- Carousel dots — would be non-functional without a second hero photo

## C. EXACT IMPLEMENTATION ORDER

1. Decompose the hero section: photo+headline alone fills its own full-
   height block; move facts/stats out (fixes #4, contributes to #13/#15)
2. Fix headline hierarchy and type scale (fixes #7 — the single highest-
   impact item)
3. Rebuild the header: transparent-over-hero, two-row, larger logo (fixes
   #1, #2)
4. Consolidate the stat/trust content into one bar with dividers, placed
   where the hero decomposition in step 1 now leaves room (fixes #12)
5. Rework the category strip: taller cards, add descriptor line (fixes
   #11)
6. Rebuild feature indicators at correct scale/structure (fixes #10)
7. Adjust hero image overlay weight for warmth (fixes #14)
8. Composite a two-zone hero image treatment, or explicitly confirm this
   deviation is acceptable (fixes #5, lowest priority since it's the most
   implementation-heavy for one line item)
9. Polish pass: right-panel border removal, hero text vertical position
   (fixes #6, #9)

Waiting for your approval before touching any code.

---

## IMPLEMENTATION STATUS (2026-09-15)

- **Phase 1 (commit `f778785`)**: steps 1, 2, 3, 6, 8 and the #9 half of
  step 9, i.e. #1, #2, #4, #5, #7, #9, #10.
- **Phase 2 (2026-09-15)**: the remaining steps.
  - #12: both stat bars merged into one dark bar (5 real facts + Get a Quote
    CTA, vertical dividers at `lg:`), placed directly under the category
    strip.
  - #11: cards made taller (`aspect-[2/3]` at `lg:`), with a descriptor line
    added under each label. The descriptor reuses the flagship hall's
    existing tagline, not new copy.
  - #14: photo opacity raised from 80% to 95%, bottom overlay lightened
    (`via /50` to `/20`).
  - #6: hero text is bottom-weighted (`items-end`). The hero height is now
    viewport minus header, not `min-h-screen`, which had pushed the feature
    row below the fold.
  - #13/#15: more padding in the category section. The 6-image swatch strip
    and the quatrefoil divider between the hero and the category strip were
    removed, because they repeated the strip's own hall photos.
- **Still deliberately held**: #3 navigation, #8 CTA wording and the
  carousel dots, as listed above.
