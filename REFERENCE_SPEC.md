# Reference Spec — Elite Balaji Homepage Hero Mockup

Source: one static reference image supplied by the client (a dark-emerald-marble
hero mockup with a gold crest logo). No reference video was usable — see
`VISUAL_AUDIT.md` §0 for why. Every line below is what's actually visible in
that one image; nothing here is invented. Where the image doesn't show enough
to determine a behavior (hover states, scroll behavior, responsive rules), it's
marked UNDETERMINED rather than guessed.

## 1. Global art direction
- Palette: near-black/deep-emerald ground, warm gold/brass accent, ivory/cream
  body copy on dark, charcoal-black secondary panels.
- Typography: a connected gold-gradient serif/script for the wordmark; a plain
  geometric sans in wide letter-spacing for nav, labels and eyebrows; a serif
  for the big hero headline ("STONES & CERAMICS").
- Material identity: real (or real-looking) marble/stone photography does the
  emotional work; UI chrome stays minimal and gets out of the way.

## 2. Header
- Single row: logo left, primary nav center-right, search icon + hamburger far
  right. A second, smaller row directly under the main nav holds 3 more links
  separated by "|". Header sits directly on the hero photo with no separate
  background bar (transparent over image).
- UNDETERMINED — PRESERVE THE REFERENCE'S VISUAL INTENT: whether the header
  changes on scroll (no scroll state is visible in a static image).

## 3. Navigation
- Primary: HOME (active/underlined in gold), ABOUT, PRODUCTS (has a dropdown
  affordance), APPLICATIONS, GALLERY, RESOURCES, CONTACT.
- Secondary row: NATURAL STONES | PREMIUM SURFACES | TIMELESS SPACES.
- UNDETERMINED: dropdown contents, mobile nav pattern, menu-open animation —
  not visible in a static image.

## 4. Logo
- A circular gold emblem (compass/star rosette + a handshake motif + ribbon
  flourishes) to the left of a 3-line wordmark lockup: script wordmark, small-
  caps subtitle ("Stones & Ceramics"), tiny tracked tagline ("Build Better
  Spaces") below that.

## 5. Hero
- Full-bleed photo: dark emerald marble slab (left) blending into a lit
  hallway/reception interior (right), track lighting, a marble reception
  counter with backlit engraved lettering ("Spaces That Inspire").
- Text block sits in the left third over the marble slab, where contrast is
  highest.

## 6. Hero typography
- Eyebrow (2 lines, plain caps, wide tracking): "Natural Beauty / Timeless
  Spaces".
- Display headline, 2 lines: "Stones &" (gold gradient) / "Ceramics" (ivory).
- Subhead, one line, regular weight serif-ish: "Premium Surfaces for a Better
  Tomorrow."
- CTA pill, outlined, gold text: "Explore Collection →".

## 7. Hero image composition
- Asymmetric split: ~40% dark textured marble slab, ~60% lit interior photo,
  blended rather than hard-cut.
- A secondary text panel sits on the right edge of the photo, right-aligned,
  small type: a mission line + the "Build Better Spaces" tagline repeated.

## 8. CTA
- Outlined pill, 1px gold border, gold uppercase text, generous horizontal
  padding, arrow glyph suffix. No fill until (assumed, UNDETERMINED) hover.

## 9. Micro-interactions
UNDETERMINED — PRESERVE THE REFERENCE'S VISUAL INTENT. A static image can't
show hover/focus states. The category-strip arrow badges are visible in a
neutral (non-hover) state at ~40% opacity in the image, implying they brighten
on interaction, but the exact transition is not observable.

## 10. Scroll behavior
UNDETERMINED. No parallax, sticky, or reveal timing is inferable from a still.

## 11. Product/category navigation
- Directly under the hero: 3 small icon+label items (diamond/"Premium
  Quality", cube/"Wide Range", shield/"Trusted Partner"), plus a thin
  progress bar and "01 02 03" — reads as a hero image carousel indicator.
- Below the hero: a full-width strip of 5 equal photographic cards (Granite,
  Marble, Tiles & Ceramics, Bathroom Solutions, Exterior Solutions), each with
  a label bottom-left and a circular arrow-button bottom-right.

## 12. Image sections
- The 5-card strip is the only other imagery visible in this single-viewport
  reference. Each card: full-bleed photo, dark gradient at the bottom third
  for label legibility, label in a serif italic.

## 13. Text sections
Not visible beyond the hero and stat bar — the reference image is a single
above-the-fold viewport, not a full page.

## 14. Statistics / trust section
- A bottom bar, 5 items in a single row separated by vertical rules: "1000+
  Products", "Premium Global Brands", "Expert Consultation", "Pan India
  Supply", "Trusted by Architects & Builders" — plus a filled gold "Get a
  Quote →" button at the far right.
- **Fabrication flag**: these 5 stats are marketing copy, not verifiable Elite
  Balaji facts. Per the client's own no-fabrication rule (`CLAUDE.md`,
  `docs/DECISIONS.md`), the *position and visual weight* of this bar is worth
  reproducing; the specific numbers are not — see `VISUAL_AUDIT.md` P0-1.

## 15. Gallery / 16. Footer / 17. Mobile / 18. Menu / 19. Transitions
UNDETERMINED — none of these are visible in a single above-the-fold hero
screenshot. Nothing to spec without inventing it.

## 20. Responsive behavior
UNDETERMINED for the same reason.
