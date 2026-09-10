# Elite Balaji Virtual Showroom — Brief & Suggestions

## Business card analysis (design framework)

| Element | Card | Website use |
|---|---|---|
| Surface | Emerald/teal marble + gold veins | Full-site atmosphere / heroes |
| Brand type | Silver 3D serif “ELITE BALAJI” | Entrance + hall titles |
| Sub-line | Gold “STONES & CERAMICS” | Under brand everywhere |
| Taglines | COMPLETE FLOORING SOLUTION / BUILD BETTER SPACES | Hero + footer |
| Since | 2012 | Entrance corner / about |
| Contact | Vignesh Yadav A · 9159056767 | Contact hall + floating enquire |
| Halls | 8 gold-icon categories | Primary nav / showroom floors |
| Partners | Kajaria → Jaquar strip | Trusted brands bar on entrance |

**Update (client lock):** the **look of the site** follows **Athangudi catalogue designs** (patterned Chettinad tile craft). The business card still supplies **name, logo, 8 halls, partners, contact**. Do not use JARVIS cyan / black-gold sci-fi on the public showroom.

## Pricing — recommendation

For a wholesale + laying business selling to contractors, a public MRP list usually **hurts** more than it helps (undercutting, stale rates, awkward negotiations).

**Suggested framing (use until you decide otherwise):**

1. **Catalogue / halls** — photos, finish names, sizes, use-cases — **no rupee amounts**.
2. Every product CTA: **“Ask for trade rate”** → WhatsApp/call with product name pre-filled.
3. Laying Works hall: **“Laying with Materials — site measure & estimate”** (aligns with your USP).
4. Optional later (if client insists on numbers): private trade PDF, or “from ₹X/sq.ft” bands **only for a few hero SKUs**, marked “indicative · confirm before order”.

When the catalogue arrives: we map pages/SKUs into halls; prices stay enquiry-gated unless they mark specific rates to show.

## Separate rules file?

**Yes.** Created:

- `.cursor/rules/elite-balaji-virtual-showroom.mdc` — applies when editing `website/**`
- Root `.cursorrules` — still owns business facts, agents, scraper, geo

Keeps showroom design preferences out of the agent-council file.

## Drop catalogues here (chat upload often fails)

Put files on disk, then say in chat that they are in place:

`C:\Users\gardo\Vicky\website\catalogues\`

See `website/catalogues/DROP_HERE.md`.

- Athangudi PDFs → `catalogues/athangudi/pdfs/`  **(theme + tile list)**
- Other PDFs → `catalogues/other-catalogues/pdfs/`
- Real photos → `catalogues/product-photos/<hall>/`

## Foundations created

```
website/
  index.html
  css/showroom.css
  halls/
  catalogues/          ← DROP PDFs AND PHOTOS HERE
  assets/business-card.jpg
  SHOWROOM_BRIEF.md
```

## Cost (default = free)

| Piece | Cost |
|---|---|
| Site code (HTML/CSS), Google Fonts | Free |
| Unsplash / Pexels hall mood images | Free (license-friendly atmosphere) |
| Hosting options (Netlify / GitHub Pages / Cloudflare) | Free tiers exist |
| Custom domain (elitebalaji.in etc.) | Paid (usually ₹500–1500/yr) — ask before buying |
| Pro photo shoot / paid stock packs | Paid — only if client wants |

## Images — what to upload vs what I can fill

**Ideal (for real products):** catalogue PDFs + any phone photos of slabs/tiles in *their* yard/showroom. Individual images per SKU are best **after** we know real names from the PDF — not required as a dump of random files first.

**What I can do with few PDFs:**
1. Extract product names / series from the PDFs into the 8 halls  
2. Keep beautiful free **mood** photos as placeholders, clearly marked *not stock*  
3. Swap moods → real images as you send more photos  

**What I will not do:** invent a fake full catalogue or pass random internet product shots off as Elite Balaji stock (looks premium, risks client trust).

## Next (after catalogue upload)

1. Split catalogue into the 8 halls  
2. Replace mood cards with real Elite Balaji SKUs / photos  
3. Keep WhatsApp enquire links  
4. Partner logo strip (export from card or brand packs)  
5. Launch URL → shared memory for Marketing Agent  
