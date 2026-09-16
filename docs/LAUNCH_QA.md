# Launch: final QA, deployment and Google visibility

_Last updated: 2026-09-16._

## 1. The one command
```bash
cd website && npm run preflight
```
It fails loudly and exits non-zero if anything below is wrong, so it is the
gate before every deploy:

| Check | What it catches |
|---|---|
| `astro check` | TypeScript/content-schema errors |
| production build | build breakage |
| pages built | a route that silently disappeared |
| real domain configured | the `example.in` placeholder still in `astro.config.mjs` |
| robots.txt ↔ domain | sitemap URL pointing at the wrong host |
| sitemap covers pages | pages Google would never discover |
| title 10–65 chars | titles Google truncates |
| description 50–160 chars | missing/over-long snippets |
| canonical, OG image, H1, `lang` | per-page SEO basics |
| no placeholder text | lorem/TODO/example.in leaking into content |
| **no prices published** | supplier MRP leaking from a catalogue import |
| structured data parses | broken JSON-LD (rich results) |
| security headers served | CSP/HSTS missing from `public/_headers` |
| Playwright, all pages × 2 viewports, CSP on | console errors, failed requests, broken images, horizontal overflow, unlabelled generated images |
| Playwright interaction pass | header convergence, menus, search, Material Match, save, compare, enquiry drawer, granite stage, reduced motion |

Individual pieces: `npm run qa`, `npm run qa:experience`,
`node scripts/serve-headers.mjs 4323` (serves `dist/` with production headers).

## 2. Manual pass (10 minutes, after preflight is green)
1. **Phone, real device:** home → granite → a product → save → My Materials →
   compare → enquiry drawer → WhatsApp opens with the right message.
2. **Content truth:** every image labelled correctly; no price anywhere; no
   claim the client hasn't confirmed.
3. **Contact details:** phone, WhatsApp, email, address, map pin all correct.
4. **Legal pages:** `/privacy/` and `/terms/` match what the site actually does.
5. **404:** visit a nonsense URL, confirm the styled 404 and a way back.

## 3. Deploy (static site, ~15 minutes)
Prerequisites the client/user must provide:
- **Domain** (e.g. `elitebalajistones.in`) — registered in the client's name,
  auto-renew and registrar lock ON.
- **Host account** — Cloudflare Pages (recommended: free, fast in India,
  free SSL, `_headers` supported) or Netlify.
- **Explicit go-ahead to deploy.**

Steps:
1. Set the real domain in `website/astro.config.mjs` (`site:`) and in
   `website/public/robots.txt` (Sitemap line). Re-run `npm run preflight`.
2. Push the repo to GitHub (`main`).
3. Cloudflare Pages → Create project → connect the GitHub repo:
   - Build command: `npm ci && npm run build`
   - Build output directory: `website/dist`
   - Root directory: `website`
   - Node version: 20+
4. Add the custom domain in Pages → follow the DNS instructions (CNAME, or
   nameservers if the domain is moved to Cloudflare). Wait for SSL to say
   "Active".
5. Verify on the live URL: `curl -sI https://<domain>/ | grep -i content-security`
   and run `npm run qa -- https://<domain>` (same Playwright sweep against production).
6. Tag the release: `git tag launch-YYYY-MM-DD && git push --tags`.

**Rollback:** Cloudflare Pages keeps every deployment — "Rollback to this
deployment" in the dashboard, or revert the commit and push.

## 4. Getting found on Google
Indexing is not instant: expect a few days for the first pages, 2–6 weeks for
the site to settle. Do all of this on launch day:

1. **Google Search Console** (client's Google account):
   - Add the domain property, verify by DNS TXT record.
   - Submit `https://<domain>/sitemap-index.xml`.
   - URL Inspection → "Request indexing" for: home, `/granite/`, `/marble/`,
     `/custom/`, `/halls/tiles/`, `/contact/`.
2. **Google Business Profile** — the single biggest driver for "granite shop
   near me" searches:
   - Claim/verify the Karamadai listing (address, hours, phone, WhatsApp).
   - Set the website link to the new domain.
   - Add 15–20 real photos (the client's own only), and the product categories.
   - Keep the name, address and phone **identical** to the website footer (NAP
     consistency is a ranking factor).
3. **Bing Webmaster Tools** — import from Search Console, one click.
4. **Local citations:** JustDial, IndiaMART, Sulekha, Google Maps — same NAP.
5. **After a week:** check Search Console → Pages for "Crawled – currently not
   indexed", and Performance for the first queries.

What already helps on the site: one H1 per page, unique titles/descriptions,
LocalBusiness + Product + Breadcrumb structured data, a sitemap, clean URLs,
fast static pages, alt text on every image, and city/area names in real copy.

## 5. Ongoing
- Re-run `npm run preflight` before every deploy.
- Monthly: `npm audit`, dependency updates, Search Console coverage check.
- Replace illustrative images with real photos as the client sends them
  (`docs/NEXT_SESSION.md` tracks which).
