# Art Direction — Elite Balaji Stones & Ceramics

_Started 2026-09-15, after client feedback that the Kota Stone images are
inaccurate. This is the brief every image (photographed, stock, or AI-generated)
must pass before it goes on the site. Material facts below are general,
publicly known stone-industry facts, not claims about Elite Balaji's own
stock._

## 1. Why the current images fail

The Kota hall uses generic Unsplash photos (hall hero, `kota-grey`,
`kota-brown`, `kota-blue`, `kota-beige`; the beige product reuses the hall
hero). They were picked for mood, not for material accuracy. A buyer who
knows Kota stone sees immediately that they aren't Kota. **Rule going
forward: accuracy over mood.** An image that looks premium but shows the
wrong stone is worse than no image.

## 2. Global rules (all materials)

1. **Material truth first.** Colour, grain, veining, surface finish, slab
   size and thickness must match the real material (see §4 sheets).
2. **Honest labelling.**
   - Real Elite Balaji photos: no label needed.
   - Supplier catalogue: credit the brand.
   - Stock: "Reference image".
   - AI-generated: **"Illustrative image — actual stone varies by batch"**.

   Never present a generated or stock image as Elite Balaji stock.
3. **One shot type per slot.** Don't mix a macro swatch and a room scene in the same card grid (see §3).
4. **Natural colour.** No teal/orange grading, and no oversaturation or HDR
   look on the stone itself. The site's charcoal/gold palette lives in the UI,
   not in the stone.
5. **Indian context.** Settings should be plausible for Coimbatore and Tamil
   Nadu: homes, verandas, temples, offices, factory floors, kitchen platforms.
   No Scandinavian lofts or US suburban kitchens.
6. **No invented details.** No fake logos, text, watermarks, people's faces,
   or branded packaging in generated images.

## 3. Shot types (the site's image slots)

| Slot | Shot type | Framing | Aspect |
|---|---|---|---|
| Product card / swatch | **Macro swatch** | Flat, top-down, one slab face filling the frame, even diffuse light | 1:1 |
| Product detail gallery #2 | **Laid surface** | 30–45° floor-level view of the material installed, showing joints/pattern | 4:3 |
| Product detail gallery #3 | **Slab/edge** | Stack or single slab showing thickness and edge finish | 4:3 |
| Hall hero | **Application scene** | Wide, real-use space, material dominant (≥50% of frame) | 16:9 |
| Category strip card | **Application scene, tight** | Material clearly readable at card size | 2:3 |

Lighting: soft daylight, and warm late-afternoon light is allowed for
heroes. Swatches use neutral 5000–5500K diffuse light with no hard shadows,
so the colour stays true.

## 4. Material truth sheets

### 4.1 Kota Stone (priority — client-flagged)

- **What it is:** a fine-grained limestone from the Kota region of
  Rajasthan. Dense, non-porous-looking, very uniform.
- **Grain:** very fine and even. It has **no dramatic veining**. At most you
  see faint tonal clouding or thin natural layer lines. If a render shows
  marble-like veins, it's wrong.
- **Colours:**
  - **Kota Blue / Green:** the classic look, a muted blue-grey to grey-green.
    Not saturated blue.
  - **Kota Brown:** earthy brown to tan, sometimes with slight grey clouding.
  - Beige and grey variations exist within those ranges.
- **Finishes:**
  - **Natural / rough:** matte, slightly uneven cleft texture.
  - **Machine-cut / honed:** flat and matte.
  - **Polished / mirror:** soft sheen, and colour deepens noticeably when
    polished.
  - **Leather:** subtle tactile texture.
- **Format:** rectangular slabs or tiles, commonly 1×1, 1×2, 2×2 ft and
  similar, roughly 20–40 mm thick, laid in a grid or running bond with
  **thin, visible joints**.
- **Typical settings:**
  - Traditional and modern Tamil Nadu homes: polished living-room floors,
    verandas, staircases.
  - Temple and courtyard floors.
  - Industrial, factory and warehouse floors.
  - Offices, balconies and parking areas.
- **Common mistakes to reject:**
  - Marble veins.
  - Slate-like layering or shiny mica.
  - Terracotta or orange tones on "brown".
  - Bright blue.
  - Large-format seamless slabs (Kota reads as a jointed slab floor).
  - Rustic Western flagstone patios.

### 4.2 Kadappa (Cuddapah) — to complete
Black/dark grey limestone, fine-grained, typically used for kitchen platforms,
borders, steps. Polished = deep glossy black; natural = matte charcoal.

### 4.3 Granite & Marbles — to complete
Per-variety sheets needed, since each named variety (Absolute Black, Tan
Brown, Kashmir White, etc.) has a specific, recognisable pattern.
**Named granite varieties should not be AI-generated at all:** buyers
recognise them and a generated look-alike will be wrong. Use real
photos or supplier images.

### 4.4 Quartz, Sanitaryware, Adhesive — to complete

## 5. What AI generation is and isn't suitable for

| Suitable (labelled illustrative) | Not suitable, use real photos |
|---|---|
| Application/room scenes for hall heroes | Named varieties (Black Galaxy, Kashmir White, Makrana…) |
| Generic material textures (Kota Blue, Kadappa black) | Specific branded tiles (Kajaria, Somany… SKUs) |
| Laying-process illustrations | Anything shown as "our stock" |
| Short hero background videos (slow pan across a floor) | Product detail swatches that buyers order from |

## 6. Prompt template (for generated application scenes)

```
[Shot type] of [material + colour + finish], [format + joint description],
installed in [Indian setting], [lighting], photorealistic architectural
photography, natural true-to-material colour, no text, no logos, no people.
Material rules: [paste the "grain" and "common mistakes" lines from §4].
```

Example (Kota hall hero):
```
Wide architectural photograph of a polished Kota Blue limestone floor,
2x2 ft slabs laid in a grid with thin visible joints, in a traditional
Tamil Nadu home veranda with wooden pillars, soft late-afternoon daylight,
photorealistic, natural true-to-material muted blue-grey colour, fine
uniform grain with no veining, no text, no logos, no people.
```

Every generated image gets a human accuracy check against §4 before use, and
the illustrative label from §2.
