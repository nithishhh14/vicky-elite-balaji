# Elite Balaji Virtual Showroom

Astro 5 + TypeScript + Tailwind CSS v4. See
[`../docs/WEBSITE_ARCHITECTURE.md`](../docs/WEBSITE_ARCHITECTURE.md) for the
full architecture, content model, and how to add hall photos or tile series.

## Develop

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # astro check + astro build -> dist/
npm run preview   # serve the production build locally
```

Requires Node.js 20+.

## Structure

- `src/content/halls/*.json`, `src/content/tile-products/*.json` — editable
  content, validated by `src/content.config.ts`.
- `src/lib/business.ts` — the one place phone/address/hub facts live.
- `public/media/` — web-servable images. `catalogues/` and `catalogue_extract/`
  at the project root are source material, not served directly.
