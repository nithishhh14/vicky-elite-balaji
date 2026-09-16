# Legal & licences — Elite Balaji website

_Last updated: 2026-09-16. Not legal advice: this is a working checklist of
what the site uses, what it needs permission for, and what is still open._

## 1. Software licences (all fine for commercial use, no fees)
| Component | Licence | Obligation |
|---|---|---|
| Astro, React, Tailwind CSS, Vite, TypeScript | MIT | Keep the licence text in `node_modules`; nothing to display |
| GSAP + ScrollTrigger | GreenSock standard "no-charge" licence | Free for this use. **Verify current terms** at gsap.com/licensing before launch and keep a dated screenshot |
| Cormorant Garamond, Outfit (Google Fonts) | SIL Open Font Licence | Free commercially. Optional: self-host to avoid a third-party request |
| Playwright, Pillow, PyMuPDF | Apache-2.0 / MIT-CMU / AGPL-3.0 | Build/QA tools only, never shipped to visitors. PyMuPDF's AGPL applies to distributed software — we only ran it locally to crop images |

No paid plugin, template or theme is used.

## 2. Imagery — the part that needs written permission
| Source | Where used | Status |
|---|---|---|
| Client's own photos (granite, marble, stonecraft) | Throughout | ✅ Client-owned |
| Supplier catalogues: Mozzato tiles, Somany adhesives, Golden & Marble wash basins | Tile and basin products, gallery | ⚠️ **Get the supplier's/distributor's written OK** (a WhatsApp message is enough) to publish their catalogue photos on a dealer website. Usual practice allows it; get it in writing anyway |
| AI-generated illustrative images (Runway) | Quartz, Kadappa, sinks, basins, laying, statement marbles, tile-printing concepts | ⚠️ Confirm Runway's terms for the plan the images were generated on allow commercial use, and keep that in writing. All are labelled "Illustrative image" on the site |
| Client's reference mockup render (hero, showroom concept, Emerald Gold crop) | Homepage, marble page | ⚠️ Generated for the client via ChatGPT; the client supplied it and approved its use. Labelled "Illustrative showroom concept" |
| Old stock photos (Unsplash/Pexels) | **None left** — the last one (adhesive hall hero) was replaced on 2026-09-16 | ✅ |

**Rule going forward:** a photo goes live only if it is the client's own, a
supplier's with permission, or clearly labelled as illustrative.

## 3. Brand names and trademarks
- Kajaria, Somany, Johnson, Orientbell, Simpolo, Varmora, AGL, Parryware,
  Jaquar, Mozzato are named as brands stocked/worked with — nominative use,
  which is normally fine. Do **not** use their logos, and do not imply an
  exclusive dealership or authorised-distributor status unless the client
  holds one in writing.
- The Elite Balaji emblem is the client's mark. Consider a trademark search /
  registration (Class 19 stone & tiles, Class 35 retail) — optional, client's call.

## 4. Business/legal pages on the site
- `/privacy/` and `/terms/` exist and are linked in the footer. They must
  match reality — update them whenever data handling changes.
- Indian consumer-protection e-commerce rules mainly bite on sites that sell
  online. This site takes no orders and no payments, so the heavy obligations
  don't apply — but the following must be visible, and are: legal business
  name, full address, phone and email.
- **Add when the client confirms them:** GSTIN and the exact registered
  entity name (proprietorship/firm) in the footer or Terms. Do not invent them.
- No cookie banner is needed today: no cookies, no analytics, no trackers.
  Adding Google Analytics later would change that.

## 5. Claims to keep honest (legal as much as ethical)
- No prices anywhere; all rates are quoted privately. This also keeps the site
  clear of price-display/advertising disputes.
- No "1000+ products", "authorised dealer", "certified", "best in Coimbatore",
  guarantees or warranties, and no customer reviews until real ones exist.
  Misleading-advertisement rules (CCPA 2019) apply to website claims.
- Material naming: granite varieties identified visually carry a
  "confirm availability" note; the Marble basin range says "confirm the
  material" because the catalogue name may describe a finish.

## 6. Domain and identity
- Register the domain in the **client's** name/email (not a developer's), with
  registrar lock and auto-renew.
- Use a business email on the client's domain later if desired; the Gmail
  address is fine for launch.

## 7. Open items before/at launch
1. Supplier permission (written) for catalogue photos — Mozzato, Somany, basins.
2. Runway commercial-use confirmation for the illustrative images.
3. GSTIN + registered entity name for the footer/Terms, if the client wants them shown.
4. GSAP licence page screenshot for the file.
5. Confirm the client is happy that brand names are listed without logos.
