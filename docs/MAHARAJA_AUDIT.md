# Project Maharaja — Phase 1 Audit (2026-09-15)

Checkpoint before this audit: commit `9de6d79`.

## 1. Repository state
- **Stack:** Astro 5, TypeScript, Tailwind v4, GSAP. Static, 61 pages, `astro check` clean.
- **Data:** 8 halls, **38 products**, 4 services; the "source on request"
  lists are in `src/lib/stone-varieties.ts`.
- **Product image sources:**

  | Hall | Real local images | Unsplash stock |
  |---|---|---|
  | Tiles | 14 (supplier catalogues) | 0 |
  | Granite & Marbles | 0 | **7** |
  | Kota | 0 | **4** (client-flagged inaccurate) |
  | Quartz | 0 | 4 |
  | Kadappa | 0 | 2 |
  | Sanitaryware | 1 | 2 |
  | Adhesive | 0 | 2 |
  | Laying Works | 0 | 2 |

  **24 of 38 products use stock photos.** The 7 "granite" products (Absolute
  Black, Tan Brown, Kashmir White, Classic Grey, and so on) show Unsplash
  images while real granite photos sat unused.
- **Homepage imagery:** from the AI mockup (`public/media/reference/`), per
  the 2026-09-15 client override.

## 2. Client-supplied assets found (NOT yet in the site)

Source: `C:\Users\gardo\Downloads\` (WhatsApp exports, 9 and 11 Sept),
51 unique images after de-duplication. Contact sheets are in the session
scratchpad.

| # | Content | Group |
|---|---|---|
| 1 | AI showroom poster (teal) | Concept render |
| 2–5 | Phone screenshots (Google Sheets leads, service-account share) | **EXCLUDE: private/admin** |
| 6 | Business card | Brand (already in repo) |
| 7–11 | Mozzato "Endless" tile catalogue pages (sizes, finish, room scenes) | Tile catalogue |
| 12, 13, 15 | Black granite with gold/copper flecks: slab stack + close-ups | Granite |
| 14 | Blue/black granite with iridescent crystals, close-up | Granite |
| 16 | Brown/black granite slab | Granite |
| 17 | Red-brown flecked slab stack, **labelled "kondagattu"** | Granite |
| 18 | Polished jet-black slabs in a warehouse | Granite |
| 19 | Black kitchen with white-veined black island (**"STYLE STONE" watermark**) | Application |
| 20 | Dark blue-grey granite slabs outdoors | Granite |
| 21 | Black slab with white wave veins | Granite |
| 22 | Black slab, **labelled "Absolute Black leathered finish"** | Granite |
| 23 | Grey speckled slab outdoors | Granite |
| 24 | Leathered black countertop close-up | Granite finish |
| 25 | Dark granite entrance staircase | Application |
| 26 | White marble-look kitchen island (US-style home) | Application |
| 27, 28 | White marble/quartz slabs | Marble/Quartz |
| 29 | Stone vessel basins on a "JACOF" display (Spanish signage) | Bath |
| 30 | WCs + wall-hung basins display | Sanitaryware |
| 31 | Somany Bathware showroom display | Sanitaryware |
| 32 | White marble counter with undermount sink | Kitchen |
| 33 | Black undermount sink on granite | Kitchen |
| 34–36 | Designer vessel basins on shelving | Bath |
| 37 | CNC/waterjet cutting a motif | Custom stonecraft |
| 38 | Engraved rose motif on black granite | Custom stonecraft |
| 39 | House name plate (**contains private customer names**) | Custom (private) |
| 40 | Hand finishing a carved granite piece | Custom stonecraft |
| 41 | "Welcome" engraved black granite sign | Custom stonecraft |
| 42, 45 | Granite benches | Custom furniture |
| 43, 44 | Granite dining table; outdoor table + stools | Custom furniture |
| 46 | Black granite tulsi madam with engraved deity panels | Custom / devotional |
| 47 | Red granite tulsi madam | Custom / devotional |
| 48, 49 | Grey/black granite tulsi madam / pooja units | Custom / devotional |
| 50 | White marble tulsi madam | Custom / devotional |
| 51 | White-grey wavy granite bench | Custom furniture |

Other unused client material, in `OneDrive\Documents\whatsapp vicky pdfs\`:
- `SEF 333 (002).pdf`, `SEF 666 (003).pdf`, `SEF 666 plus.pdf`: tile adhesive technical sheets
- `Somany EZY Grout_Shade Card.pdf`: real grout shade card
- 2 videos, one of which is a third-party tile-fixing ad ("#tvc"), **not** client work.

Tile catalogues already in the repo but only partly mined: GC_COIMBATORE,
GC_TILES_COIMBATORE_LLP, HOME_CENTER, LEVERPOOL_15, SONEX, 12x18-wall_tiles.

## 3. Provenance flags (blocking, need client confirmation)
Several photos look like **the client's own stock/work**: yard slab stacks
on wooden bearers, a local site, a "kondagattu" hand label, engravings,
tulsi madams. Others look like **internet reference images** the client
forwarded:
- #19 has a third-party watermark
- #26 is a US-style kitchen
- #29 has Spanish JACOF display signage
- #31 is a Somany-branded showroom
- #37 and #40 look like stock workshop shots

Presenting the second group as "Elite Balaji work" would be a false claim.

## 4. Claims audit
| Claim on site | Source | Status |
|---|---|---|
| Since 2012 | `.cursorrules`, business card | Verified |
| Address, phone, email, contact | business card / user | Verified |
| 9 partner brands | `.cursorrules` / card logos | Verified (not "authorised dealer") |
| Service hubs (13) | `.cursorrules` | Verified |
| Supply/transport anywhere in India | commit `8881174` (client confirmed) | Verified; phrase separately from local service |
| Granite engraving, sculptures, name boards | `.cursorrules` | Verified capability |
| "Premium Partner Brands / Expert Consultation / Trusted by Contractors & Builders" | derived | Soft; reword truthfully |
| Granite product names on 7 products | earlier session, generic | **Unverified names + stock images** |

## 5. Tooling notes
- Playwright MCP is **not** available in this session. QA will use the
  in-app browser (same checks: console, overflow, links, interactions).
- There is no text-to-image API. Adobe upload was blocked by the permission
  classifier.
