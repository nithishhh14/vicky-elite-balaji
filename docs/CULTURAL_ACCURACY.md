# Cultural accuracy checklist for generated imagery

_Written 2026-09-24, after a generated pooja-room frame put **candles** on a
kuthuvilakku. The client caught it in about a second._

## Why this document exists

The image models we use — FLUX, SDXL, LTX — are trained overwhelmingly on
Western imagery. Ask for "brass lamp with a flame" and the model reaches for a
candlestick, because that is what it has mostly seen. It does not know it is
wrong, and it renders the mistake beautifully, at high resolution, in perfect
light. A convincing image of the wrong thing is harder to catch than an
obviously bad one.

This matters more than colour grading or composition ever will. A bland frame
is forgettable. **A wrong frame is disqualifying** — a Tamil family in Karamadai
looks at a candle on a vilakku and knows immediately that nobody who
understands their home was involved. That is a worse outcome than publishing
nothing.

It is the same principle as the image-provenance rule in
`docs/WEBSITE_ARCHITECTURE.md` §3: the credibility of everything rests on not
being caught in a small lie. This is the cultural half of that rule.

---

## The rule

**Every generated frame containing a culturally specific object is checked
against this list before it ships. No exceptions, including when the frame
looks stunning.** Looking stunning is how these errors survive review.

Anything on this list that cannot be verified goes to the client. Vignesh will
spot in one second what we would argue about for ten minutes.

---

## 1. Kuthuvilakku / நிலைவிளக்கு (the standing oil lamp)

**What it is:** a turned brass stand with a wide, shallow oil bowl at the top.
Cotton wicks lie *in* the oil, resting at the bowl's rim. The flames sit at the
rim — small, flat, slightly leaning. Often a finial above the bowl.

| Check | Right | Wrong |
|---|---|---|
| Light source | Oil in an open bowl, cotton wick at the rim | **A candle or taper** |
| Flame position | At the rim of the bowl, low and flat | On top of a stick, tall and teardrop |
| Any wax | Never | Any wax at all |
| Bowl | Wide, shallow, open | Narrow cup, enclosed holder |

> **This is the error that prompted this document.** Both candidates in the
> first hero batch had candlesticks. Check it first, every time.

**Prompt language that works:**
```
traditional South Indian brass kuthuvilakku oil lamp: tall turned brass stand,
wide shallow oil bowl at the top, cotton wicks lying in the oil at the bowl's
rim, small flat flames at the rim
```
**Do NOT write the forbidden word in the prompt.** Diffusion models do not
process negation: "no candles" contains the token *candles*, and frequently
produces them. Proven here on 2026-09-24 — an otherwise identical pair of
prompts ending "no candles, no tapers, no wax" gave one frame with pillar
candles and one without. The negation did nothing; the seed decided.

Two reliable approaches instead:
1. **Describe only the correct object**, in physical detail, and never name
   the wrong one. The oil bowl and the wick at the rim are what to specify.
2. **Use a Space that exposes a real negative-prompt field** (FLUX schnell's
   `/infer` does not — its parameters are prompt, seed, width, height, steps).
   Then `candle, taper, wax` belongs there, never in the positive prompt.

If neither works after two attempts, compose the lamp out of focus or out of
frame. A correct room with no lamp beats a wrong lamp.

Related lamps, if they appear: the **agal vilakku** is a small flat clay or
brass dish on the floor, not a stand. A **hanging vilakku** hangs by chains.
Neither is a candle either.

---

## 2. Ganesha / Vinayagar murti

The model does not know iconography; it makes a plausible elephant figure.

- **Arms:** usually four. Count them. Two or six needs a reason.
- **Objects held:** commonly modak, ankusha (goad), pasha (noose), and one
  hand in abhaya (palm out, blessing). Random empty hands read as wrong.
- **Trunk:** curves to one side; a straight-down or forward trunk is unusual.
- **Mooshika:** the mouse vahana normally sits at the base, often facing the
  murti. Its absence is safe; a random animal is not.
- **Proportions:** AI limbs go wrong constantly. Zoom in on every arm.

**If the murti is rendered indistinctly or from behind, the risk drops to
almost nothing.** When unsure, compose so the murti is softly out of focus or
partially turned — a real photographic choice, not a dodge.

---

## 3. Floor, threshold and doorway

- **Kolam:** rice-flour pattern at the threshold, white on the floor, drawn
  freehand and symmetrical. Not a painted tile pattern, not a rangoli of
  coloured powder unless a festival is intended.
- **Thoranam:** fresh mango leaves strung above the doorway, leaves pointing
  down. Not a garland of flowers, not tinsel.

Absent is fine. Wrong is not.

---

## 4. Flowers and garlands

- Marigold, jasmine, rose are the usual ones. Jasmine is strung in tight
  strands; marigold in loose round heads.
- Garlands on a murti hang from the shoulders or neck, not draped over the
  head like a wreath.
- Loose petals scattered on the plinth read correctly. A Western floral
  arrangement in a vase does not belong in a pooja space.

---

## 5. Athangudi tiles

A real, specific product — handmade in Athangudi, Chettinad, not a generic
"Moroccan" tile.

- Patterns are geometric or floral, laid as a repeating field.
- The palette is muted: teal, ochre, terracotta, off-white, dark green. Not
  neon, not high-gloss.
- Surface is matte to satin, slightly uneven — handmade, not machine-perfect.

Calling these "Moroccan tiles" in copy is its own error. They are Chettinad.

---

## 6. General "is this actually India" checks

- Switch plates, sockets and fittings should not be American.
- Window and door proportions, grilles, and the quality of daylight should read
  South Indian, not Scandinavian.
- Furniture scale: low, solid teak rather than tall European pieces.

---

## How to use this in practice

1. Generate the frame.
2. Zoom in on every culturally specific object. Do not judge from the thumbnail
   — the thumbnail is where these errors hide.
3. Work down this list for anything present in the frame.
4. Anything uncertain → the client, before it ships.
5. If a detail is wrong and the prompt cannot fix it, **change the composition
   so the object is not the subject** rather than shipping it wrong.

A frame that fails this check does not get published, however good it looks.

---

## Adding to this list

When the client corrects something, it gets written here the same day, with
what was wrong and the prompt language that fixed it. The list is only useful
if it grows from real mistakes rather than from what we imagined might go
wrong.

| Date | Caught by | Error | Fix |
|---|---|---|---|
| 2026-09-24 | Client | Candles on a kuthuvilakku in both hero candidates | Describe the oil bowl and wick precisely; never name the wrong object |
| 2026-09-24 | Self-check | Writing "no candles" in the positive prompt still produced candles in 1 of 2 frames | Negation does not work in diffusion prompts — see §1 |
