# Content editing contract

_The rules any editor — a person or the Website agent — follows to change the
site safely. Written 2026-09-18, when the landing pages moved from code to
data and the integrity checker was added._

## 1. What may be edited, and by whom

| Path | Contains | Who |
|---|---|---|
| `website/src/content/products/*.json` | one file per product | Agent or person |
| `website/src/content/guides/*.json` | one file per local landing page | Agent or person |
| `website/src/content/halls/*.json` | the 8 showroom halls | Person (rare) |
| `website/src/content/services/*.json` | made-to-order capabilities | Person (rare) |
| `website/public/media/**` | photos | Agent or person |
| `website/src/lib/media-library.ts` | client photos + provenance (still TypeScript) | Person, until it becomes a collection |
| `website/src/lib/business.ts` | phone, address, brands, USPs — **business facts** | **Owner approval only** |
| `src/components`, `src/pages`, `src/styles`, `src/scripts` | design and code | Developer |

Every change, whoever makes it: branch → pull request → `npm run preflight`
passes → Cloudflare preview → owner approves → merge.

## 2. Recipes

### Add a product
1. Create `website/src/content/products/<id>.json`. The filename becomes the
   URL (`/products/<id>/`), so pick it once and keep it.
2. Required: `kind` (`tile` or `material`), `hallId` (an existing hall),
   `name`, `finish`, `applications[]`, `image`, `imageAlt`.
   Optional: `brand`, `series`, `code`, `category`, `size`, `images[]`,
   `sourceCatalogue`, `note`, `thickness`, `qtyPerBox`, `coverageArea`,
   `weight`, `order`.
3. `order` may be left out — listings fall back to the name, and two products
   may share a number. No renumbering of neighbours, ever.
4. Put the photo under `public/media/…` first. Generated or stand-in imagery
   goes in `public/media/illustrative/` so it is labelled automatically.
5. `npm run check:content` → then `npm run preflight`.

Unknown or misspelled fields now **fail the build** (the schemas are strict),
so a typo can't silently disappear.

### Add a local landing page
1. Create `website/src/content/guides/<something>-coimbatore.json`
   (the filename is the URL and must end in `-coimbatore`).
2. Fields: `h1`, `title` (≤65 chars), `description` (50–160), `eyebrow`,
   `intro[]`, `match`, `choose[]`, `faq[]`, `related[]`, `enquiry`.
3. `match` selects the real products for the page:
   `{ "pattern": "wood|plank", "flags": "i", "halls": ["tiles"] }`.
   `halls` and `kind` are optional filters.
4. `related` must list slugs that exist. The checker enforces it.
5. If nothing matches yet, the page still builds and honestly says we source
   it on request.

### Replace an illustrative image with a real photo
1. Add the real file under `public/media/client/…` (or the supplier folder),
   **under a new filename**. Never overwrite an image in place: `/media/*` is
   served with `max-age=2592000`, so Cloudflare keeps handing visitors the old
   picture for thirty days even after the deploy succeeds. A new path is a new
   cache entry and shows up immediately.
2. Point the product's `image`/`images[]` at it and update `imageAlt`.
3. Delete the old file from `public/media/illustrative/` if nothing else uses it.
4. The "Illustrative image" badge disappears on its own — it is derived from
   the path (`src/lib/image-badge.ts`), never typed by hand.

### Rename or remove a page
Don't rename a live slug. If it is unavoidable, add a 301 line to
`website/public/_redirects` in the same change, so the old address keeps
working for Google and for any link the client has shared.

## 3. What the checks enforce

`npm run check:content` (also inside `npm run preflight`, and in CI):
- every `hallId` exists;
- every product/gallery/hall image file exists on disk;
- no product uses concept or reference art as its photo;
- every image has alt text;
- every hall has at least one product;
- landing-page slugs end in `-coimbatore`, their `match.pattern` compiles,
  `match.halls` are real halls, and `related` points at real pages;
- `media-library.ts` product references and image paths resolve.

`npm run preflight` adds: strict schema validation, the build, SEO limits,
sitemap/robots consistency, **no prices anywhere**, no broken internal links,
no third-party scripts, security headers, and the two Playwright passes.

## 4. Still to convert

`src/lib/media-library.ts` (51 client photos with provenance) is the last
content that lives in TypeScript. It is planned to become a `media`
collection so photo updates are data too — a good first task to run through
the new branch → preview → approval flow rather than a pre-launch change.
