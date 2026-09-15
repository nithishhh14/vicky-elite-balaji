# Art Direction & UX Orchestration — Elite Balaji Stones & Ceramics

_Rewritten 2026-09-15 after client direction: **the client's AI reference
mockup IS the design.** The real Karamadai showroom is under renovation, and
the client wants the mockup's look and imagery on the live site. This file is
the single brief for how the site looks, what imagery may go where, and how
the experience flows. See `docs/DECISIONS.md` (2026-09-15) for the override
record and `REFERENCE_SPEC.md` for the element-by-element read of the mockup._

Reference source: `Downloads/ChatGPT Image Sep 13, 2026, 02_11_51 PM.png`
(1536×1024), supplied by the client.

---

## Part A — Art direction

### A1. Direction in one line
**A luxury architectural materials house.** Dark emerald marble and warm
gold carry the brand. Lit stone interiors do the emotional work, and the UI
chrome stays thin, tracked and quiet.

### A2. Colour system (tokens in `website/src/styles/global.css`)

| Role | Token | Hex | Use |
|---|---|---|---|
| Night ground | `charcoal-deep` | `#0a0907` | Hero, header, dark bands |
| Dark panel | `charcoal` | `#14120f` | Secondary dark sections |
| Emerald marble | `bottle-dark` / `bottle` | `#142823` / `#1f3d33` | Marble zone behind hero type (with `.marble-veins`) |
| Gold | `brass` → `mustard-dark` | `#a3822f` → `#9c6f1f` | Headline gradient first line, rules, borders, CTA fills |
| Gold highlight | (inline) | `#f3d9a4` | Top stop of the "STONES &" gradient only |
| Ivory ground | `paper` / `card` | `#f6efe1` / `#fbf6ec` | Category strip + trust bar, light content bands |
| Body on light | `ink` / `ink-soft` | `#211f1c` / `#55493c` | Text on ivory |

Rules:
- Gold is an accent: rules, borders, one gradient word and CTAs. Never
  large gold fills behind body text.
- Dark → ivory is the page's rhythm. The hero is dark, the strip/trust bar
  ivory, then alternate.
- Terracotta stays on existing catalogue pages (links/labels on ivory), not
  in the hero system.

### A3. Typography
- **Display:** Cormorant Garamond 500, **UPPERCASE**, tight leading (0.92–0.95).
  Hero headline `clamp(2.75rem, 13vw, 7.5rem)`, and page heroes 5xl–6xl.
- **UI / labels:** Outfit, uppercase, wide tracking. Nav 0.14em,
  eyebrows 0.45em, micro-labels 0.22–0.25em.
- **Wordmark:** Cormorant italic with a gold gradient, beside the client's
  exact emblem.
- Sentence-case body copy only in paragraphs. Everything navigational is
  uppercase and tracked.

### A4. Brand mark
- Use only `public/media/brand/logo-emblem-240.png` (header) and
  `logo-emblem.png` (full resolution). **Never redraw, recolour or simplify
  it** (client instruction). Minimum rendered height is 48px.

### A5. Imagery policy (client-approved)

| Imagery type | Allowed where | Label |
|---|---|---|
| **Reference mockup renders** (`/media/reference/`) | Homepage hero, category strip, page-hero bands, gallery "Showroom" set | Small caption: "Illustrative showroom render · our Karamadai showroom is being renovated" (hero); gallery footnote |
| **Real supplier catalogue photos** (`/media/tiles/`) | Product cards and detail pages | Brand credit as already shown |
| **Stock/mood photos** (hall heroes, Unsplash) | Hall pages until replaced | Existing "mood photography" note |
| **Generated application concepts** (`/media/concepts/`, Runway 2026-09-15) | Room/application sections, homepage applications, Bathroom world card | "Application concept" caption, always |
| **Future AI video** (needs a paid plan) | Hero, granite, stonecraft loops via `AmbientVideo.astro` | "Illustrative" caption |

**Hard line kept:** a product's *detail-page swatch* (the thing a buyer
orders from) should be a real photo of that product. Renders set the mood,
and product records show the product.

### A6. Image slots & specs

| Slot | Shot | Aspect | Min source | Current asset |
|---|---|---|---|---|
| Home hero | Lit stone interior, dark marble at left edge | fills 68% width, desktop | 1600px wide | `reference/hero-interior.jpg` (1630×1136, 2× upscale) |
| Category card | Material/scene, darkening to the bottom third | 16:10 | 560px | `reference/card-*.jpg` (562×348) |
| Page hero band | Same interior, 60% opacity behind marble gradient | fills right 55% | 1600px | `reference/hero-interior.jpg` |
| Product swatch | Flat top-down material face | 1:1 or 4:3 | 800px | per product JSON |
| Gallery | Any of the above, natural aspect | masonry | 600px | all of the above |

**Known limitation:** the reference renders come from a 1536px mockup, so
they're soft on retina screens. The category cards' bottom thirds were
rebuilt with a blurred, darkened fill where the mockup's labels were
baked in. When a generation API is available, regenerate these at 2–4K
from the §A8 prompts.

### A7. Material truth sheets (for any future generated or photographed stone)

**Kota stone (client flagged the current Kota images as inaccurate).**
Fine-grained Rajasthan limestone with **no marble veining**. Colours are
Kota Blue/Green (muted blue-grey to grey-green, never bright blue) and Kota
Brown (earthy tan-brown). Finishes: natural/rough, honed, polished (deepens
the colour), leather. It's laid as rectangular slabs (1×1, 1×2, 2×2 ft;
20–40 mm) with thin visible joints. Typical settings: Tamil Nadu homes,
verandas, temple courtyards, factory and office floors.
**Reject:** veins, slate layering or mica, orange tones, saturated blue,
seamless large slabs, Western flagstone patios.

**Kadappa:** black to dark grey limestone. Polished is glossy black, natural
is matte charcoal. Used for kitchen platforms, borders and steps.

**Named granite varieties** (Absolute Black, Tan Brown, Kashmir White…) have
recognisable patterns. Use real photos or supplier images for product
records.

### A8. Generation prompts (for when an image/video API is connected)

Base template:
```
Photorealistic architectural interior render, luxury stone & ceramics
showroom, [scene], dark emerald marble with gold veining, warm backlit
cove lighting, track spots, polished stone floor reflections, cinematic
low-key exposure, colour palette charcoal #0a0907 / emerald #142823 /
gold #a3822f / ivory #f6efe1, no text, no logos, no people.
```
Scenes to produce:
1. Hero, wide 21:9: reception counter in marble, lit corridor of slab
   displays (matches the current hero).
2. Hero slides 2 and 3 for a real carousel: slab gallery wall; tile display
   bay.
3. Category cards, 16:10, dark lower third: granite macro; marble macro;
   stacked glossy tiles; stone bathroom with vessel basin; marble-clad
   entrance with planting.
4. Kota hall hero, 16:9: polished Kota Blue slab floor in a Tamil Nadu
   veranda (apply §A7).
5. Video loop, 6–8s, 1080p: slow dolly along the lit slab corridor. Use it
   as a muted hero background with the still render as the poster.

---

## Part B — UX orchestration

### B1. Information architecture (matches the mockup's nav)

```
HOME ─ ABOUT ─ PRODUCTS▾ ─ APPLICATIONS ─ GALLERY ─ RESOURCES ─ CONTACT   [search] [menu]
          sub-strip: NATURAL STONES | PREMIUM SURFACES | TIMELESS SPACES
```
- **PRODUCTS▾:** the 3 material worlds → 8 halls, plus Laying Works, Custom
  and the full catalogue.
- **APPLICATIONS** (`/applications/`): the catalogue regrouped by space.
  Derived from product data, so new products appear automatically.
- **GALLERY** (`/gallery/`): every image, filterable by hall, with renders
  first.
- **RESOURCES** (`/resources/`): how quoting works, sizes and finishes,
  varieties we source, and services.
- **Menu drawer** (every width): the full hall list. On mobile it is the
  primary nav.
- Search icon → `/search/` (faceted catalogue).

### B2. The core journey
`Hero (mood)` → `Category card (intent)` → `World/hall or search results
(choice)` → `Product (detail)` → **WhatsApp enquiry (conversion)**

Every level offers a way to enquire:
- **Floating WhatsApp bar:** on every page.
- **Hero:** Explore Collection scrolls to the strip.
- **Trust bar:** Get a Quote.
- **Product pages:** WhatsApp / Call / Email.
- **Applications and Resources:** closing CTAs.

### B3. Page choreography

**Home**
1. Hero at 100svh (≥760px on desktop). The header floats transparent.
   Order: eyebrow → headline → subhead → CTA → 3 feature marks.
2. Ivory band: 5 category cards, then the trust bar with Get a Quote, sitting
   right after the hero as in the mockup.
3. Engraved-gold tagline → catalogue filter → custom work → Athangudi
   mention → why us → brands → service area → final CTA.

**Inner pages:** a `PageHero` band (marble + render) introduces the page,
then sticky in-page anchors (Applications, Resources), content, and a
closing CTA.

### B4. Motion system (GSAP, `src/scripts/motion-gsap.ts`)

| Pattern | Trigger | Spec |
|---|---|---|
| Hero entrance | load, `[data-gsap-hero]` children | y 24→0, opacity 0→1, 0.85s, stagger 0.1, power2.out |
| Section stagger | scroll into view, `[data-gsap-stagger]` | 0.6s, stagger 0.07 |
| Reveal | IntersectionObserver `.reveal` | fade/rise once |
| Magnetic CTA | hover (React Bits `Magnet`) | hero CTA only |
| Card hover | CSS | image scale 1.05 over 700ms; arrow ring fills gold |
| Header state | scroll > 40px or menu open | transparent → charcoal/95 + blur |

Rules: no motion on content that isn't visible, and everything respects
`prefers-reduced-motion` (content is never pre-hidden without JS plus motion
permission). Nothing loops or autoplays except a future muted hero video.

### B5. Interaction states
- Links and nav: ivory/85 → brass on hover. The active page gets brass text
  plus a 1px underline.
- Outline CTA (hero): gold border, fills brass with dark text on hover.
- Solid CTA (Get a Quote): brass → mustard gradient, brightens on hover.
- Focus: visible ring (global `:focus-visible`). Every interactive element is
  keyboard-reachable, and Esc closes menus.

### B6. Responsive rules
- **≥1280 (xl):** full nav, right-side hero panel, 5-up cards.
- **1024–1279:** menu drawer replaces the inline nav; the sub-strip stays.
- **640–1023:** 2-up cards, with the 5th spanning both columns.
- **<640:** 1-up cards, stats 2-up, the headline scales with the viewport.
  No horizontal scroll at 375px (verified 2026-09-15 across 19 page types).

### B7. Performance & accessibility budgets
- Hero image ≤ 350KB (`hero-interior.jpg` is 307KB), `fetchpriority=high`.
  Everything below the fold is `loading=lazy`.
- Only 1 React island on home (Magnet).
- One `h1` per page, alt text on content images, decorative images `aria-hidden`.

### B8. Open items
1. **Real domain** (`astro.config.mjs` `site` + `public/robots.txt`), which
   blocks launch.
2. **Real product count:** if the client confirms "1000+", restore it to the
   trust bar.
3. **Image/video API** to regenerate renders at high resolution and build
   the 3-slide hero carousel (§A8).
4. **Replace the Kota images** per §A7.
5. **Favicon** from the client emblem.
