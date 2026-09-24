# Elite Balaji — Client Preferences

_This file is the permanent source of truth for the client's design/content
preferences. As of 2026-09-10, the client (Elite Balaji) has not yet given a
round of feedback on the rebuilt website — every section below is marked
PENDING CLIENT INPUT until that happens. Nothing in this file is invented;
where a working assumption was made by Claude without client sign-off, it is
labeled as a **working assumption**, not a preference, and lives in
`docs/DECISIONS.md` instead._


## 2026-09-18 → 09-24: feedback relayed by the user (all implemented unless noted)
- **"Bath Spaces"**, not "Bathroom", as the category name everywhere it shows.
  URLs and ids still say `bathroom`.
- **Blue Sapphire, not Black Pearl** — the stone photographed in the yard and
  listed as Black Pearl is Blue Sapphire.
- **Real stock photos on the catalogue cards.** Generated images are only for
  what has no photo (Emerald Gold Marble). The generated images are
  aspirational: "these can be replicated even better in real life".
- **No yellow wash.** Luxury, but with colour and life — not bland, not
  sepia. Cool grade; warm accents only where real.
- **Awe.** Direction: temple and divine presence — Indian deities with Greek
  marble architecture and granite backgrounds, museum-style lighting on all
  artwork. Reference: a suspended bronze Krishna in a gallery, a Nataraja
  against raw rock, the Trevi Fountain. *(Direction agreed; not yet built.)*
- **Vilakku is an oil lamp**, never a candle. Caught by the client in the
  first generated frame.
- **Logo in the corner**, keeping all three lines of the lockup, header edge
  to edge.
- **Hero video at least 720p**, and **short** — "nobody watches a hero card
  for 20 seconds"; conversion and reducing friction matter more.
- Wants **3D elements**, **cursor interaction**, cinematic feel — "be
  deliberate with art"; a little page weight is acceptable. *(3D viewer and
  sheen built; museum lighting on the source images pending.)*
- Catalogue organisation: adhesives must not appear among tiles; Bath Spaces
  must not be one mixed list of sinks and adhesives.
- The showroom is **under renovation for 1–2 months**; generated interiors
  stand in until real photos exist, and are labelled as concepts.

## 2026-09-16 (evening): free site measurement + premium floating CTA
- **Client offer (confirmed by the user):** a **free site measurement**. Now
  bookable from the floating actions, a homepage band, the contact page
  (`/contact/#measure`), the footer, the mobile drawer and the Laying Works
  hall. The enquiry drawer has a "Book a free site measurement" intent with
  preferred day and time-of-day fields.
- **Wording used:** "We bring the tape. You keep the estimate." — free across
  Coimbatore and the surrounding region, estimate yours to keep, no
  obligation to buy. No timeline promised (nothing confirmed by the client).
- **Feedback:** the old floating WhatsApp pill "looked cheap". Replaced with a
  brass-on-charcoal pill that opens a panel of four real actions
  (measurement, WhatsApp, call, visit). The bright WhatsApp green is gone from
  the floating CTA; the glyph stays inside the panel in brass.

## 2026-09-16: statement marbles, gold header, no repeated brand in hero
- The marble range needs gold-veined statement marbles ("black gold, emerald
  gold and all"). Added Black Gold (the last Runway image) and Emerald Gold
  (a crop of the client-approved reference render). Both are labelled
  "Illustrative image" in a new "Gold-veined & dramatic" section on /marble/.
  Calacatta Gold, Nero Marquina and Botticino were added to the "varieties we
  source" list only. **Confirm with the client** which of these they actually
  stock, and get slab photos.
- The header wordmark should be engraved metallic gold like the reference.
  Implemented in CSS (`.gold-engraved`); the logo image itself is unchanged,
  only larger.
- The hero repeated "Elite Balaji" right under the header. It now opens with
  the reference's "Natural beauty / Timeless spaces" eyebrow.

## 2026-09-15 (late night): quartz sinks + fill missing images
- The client says **quartz sinks and other sinks** are missing. Three
  quartz sink products were added. The exact models, sizes, colours and
  what "other sinks" means are still to be confirmed.
- The user asked to fill the missing catalogue images with image
  generation. 15 generated images now replace the stock photos. They are
  always labelled "Illustrative image" and should be replaced with real
  photos when available.

## 2026-09-15 (night) — service area + custom tile printing
- **Service area (client-confirmed):** Coimbatore and the surrounding region
  for site visits, supply and laying. **Pan-India** for custom art products
  (engraved stonecraft, name plates, tulsi madams, custom printed tiles).
  Reflected in the footer, homepage and About page.
- **Custom tile printing** must be shown. The client has no finished-job
  photos yet, so the user asked for generated visuals "for now". Four
  Runway concept images are in `public/media/concepts/tile-printing/`,
  always captioned "Concept visual". Replace them with real job photos when
  available.

## 2026-09-15 (later) — the AI reference mockup IS the design
Client instruction, relayed by the user: "even if the AI mockups are not
looking like the actual showroom, that's what the client wants; the showroom
is under renovation now … pull the design … remake the website."
- The mockup's layout, copy, navigation and imagery are the approved design.
  The mockup is `Downloads/ChatGPT Image Sep 13, 2026, 02_11_51 PM.png`.
- AI-render imagery is acceptable for the hero, category cards and gallery
  while the showroom is renovated.
- Implemented the same day; see `docs/DECISIONS.md` and
  `docs/ART_DIRECTION.md`.

## 2026-09-15 — exact logo, Kota images, art direction
- **Logo:** the client supplied their exact emblem: a gold star seal with
  ribbons, and a handshake holding a dark-green marble tile and a white one.
  Instruction: **use it exactly, never redraw or alter it.** It is now used
  in the header as `public/media/brand/logo-emblem-240.png`. The only changes
  are crop, scale, and the outer teal backdrop made transparent. **Approved
  by the user ("the badge looks great").** A hand-drawn SVG version was
  rejected before this.
- **Kota Stone images are inaccurate.** They are generic Unsplash photos.
  The user asked for art direction first, before any new imagery; see
  `docs/ART_DIRECTION.md`.
- The user is exploring AI image and video generation for empty catalogue
  areas. Not decided yet. Any generated image must be labelled illustrative,
  per the no-fabrication rule.

## 2026-09-13 — reference image + concrete complaints
User supplied a reference screenshot (source/authorship unknown — reads as
an AI-generated or template mockup, not a photo of a real competitor site)
showing a dark charcoal/deep-green hero, gold serif wordmark ("Elite
Balaji" logotype with a handshake emblem), a 5-tile category strip
(Granite/Marble/Tiles/Bathroom/Exterior), and a trust-stat bar reading
"1000+ Products / Premium Global Brands / Expert Consultation / Pan India
Supply / Trusted by Architects & Builders." Treated as **visual/typography
direction only** — the dark+gold palette, serif logotype confidence, and
category-strip layout were used as inspiration (see `docs/DECISIONS.md`
2026-09-13 hero decision). The trust-bar statistics were explicitly **not**
copied: "1000+ Products," "Premium Global Brands," and "Trusted by
Architects & Builders" are not verified Elite Balaji facts and would violate
the project's no-fabrication rule if presented as such. Real facts (founded
2012, 8 material halls, Karamadai/Coimbatore) were used in their place —
flag to the user if the client specifically wants invented-sounding stats
anyway, since that would need an explicit, informed override of the
no-fabrication rule, not just visual styling.

Same message also reported 3 concrete issues, resolved as of commit
`26ae9d2`: (1) the homepage/Tiles hero was still a single Athangudi photo
despite the earlier "de-emphasis" pass only having touched copy, not the
actual identity image; (2) Natural Stone's "ask us to source" honest layer
existed but Quartz and Sanitaryware had no equivalent, making those halls
look sparse; (3) a "searchbar doesn't work" report that could not be
reproduced in testing (filtering, typing, and result counts all functioned)
— flagged back to the user rather than guessed at further.

## Brand personality
PENDING CLIENT INPUT

## Preferred visual style
PENDING CLIENT INPUT — a design brief was relayed by the user on 2026-09-11
(sourced from an external LLM session, not a documented conversation with
Elite Balaji itself) requesting a flat, editorial, no-3D, premium-trading-
business aesthetic. Treated as a working assumption, not confirmed client
preference — see `docs/DECISIONS.md`. The 2026-09-13 reference image (dark/
gold, serif wordmark) is a second, partially-overlapping direction — see
above.

## Colours
PENDING CLIENT INPUT — the 2026-09-11 relayed brief requested green-dominant
tones (deep emerald/moss/sage), which was implemented (see
`docs/DECISIONS.md` "Palette rebalanced green-dominant"). This is still not
confirmed as the real client's preference — it's what the user asked Claude
to implement based on a brief they brought in, not feedback attributed to
Elite Balaji directly. Flag clearly if/when the actual client reacts to it.

## Typography
PENDING CLIENT INPUT

## Hero section
PENDING CLIENT INPUT — see 2026-09-13 entry above: homepage hero rebuilt as
a photo-free dark/gold treatment specifically to stop a single product
photo (Athangudi) reading as the site's identity.

## Navigation
PENDING CLIENT INPUT

## Homepage
PENDING CLIENT INPUT

## Product halls
PENDING CLIENT INPUT

## Product cards
PENDING CLIENT INPUT

## Product photography
PENDING CLIENT INPUT — real photography for 7 of 8 halls is still an open
gap (see `docs/PROJECT_STATE.md` "Blocked items"). As of 2026-09-11, those
7 halls now show verified, clearly-labeled stock photography ("Mood
photography — not actual stock") instead of the earlier colour/texture
placeholders — see `docs/DECISIONS.md` "Stock photography for the 7
non-Tiles halls." This is a stand-in, not a client-approved final look.

## Catalogue usage
PENDING CLIENT INPUT

## Athangudi influence
PENDING CLIENT INPUT

## Animations
PENDING CLIENT INPUT

## 3D / interactive elements
PENDING CLIENT INPUT

## Mobile experience
PENDING CLIENT INPUT

## WhatsApp / enquiry experience
PENDING CLIENT INPUT

## Content/copy tone
PENDING CLIENT INPUT

## Things the client likes
PENDING CLIENT INPUT

## Things the client dislikes
PENDING CLIENT INPUT

## Explicit client corrections
PENDING CLIENT INPUT

## Approved designs
PENDING CLIENT INPUT

## Rejected designs
PENDING CLIENT INPUT

## Pending decisions
- Domain and hosting choice (see `docs/PROJECT_STATE.md` "Blocked items")
- Whether to commission a real photo shoot for the 7 halls without photography

## Client feedback log
_(Newest first. Empty until the first round of client feedback arrives.)_

## Date of last client review
None yet.

---

**Instruction for future sessions:** when the user relays client feedback,
update the relevant section(s) above with what was actually said, add an
entry to the feedback log with the date, and update "Date of last client
review." Per `CLAUDE.md`'s Client Feedback Override Rule, new feedback that
conflicts with an existing decision in `docs/DECISIONS.md` wins — record the
old decision as superseded there, don't silently delete it.
