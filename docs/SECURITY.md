# Security plan — Elite Balaji website

Scope: a static Astro site (no backend, no database, no logins, no payments).
That removes most classic web risk; what remains is account security, supply
chain, content integrity and privacy hygiene.

_Last updated: 2026-09-16._

## 1. What the site holds
- **No user accounts, no payments, no server.** Every enquiry opens WhatsApp
  or the visitor's mail app on their own device.
- **Enquiry drawer / quote form:** typed values never leave the browser until
  the visitor presses send in WhatsApp or their mail app.
- **localStorage only** (`eb-my-materials`): the visitor's own shortlist, on
  their own device. No tracking, no cookies, no analytics today.
- Therefore: no personal data is stored or processed by us through the site.

## 2. Shipped protections
- **Security headers** in `website/public/_headers` (works on Cloudflare
  Pages and Netlify), verified locally with `scripts/serve-headers.mjs`:
  - `Content-Security-Policy` — self-only scripts/styles/images/connections,
    fonts from Google Fonts, the Maps iframe allowed, `frame-ancestors 'none'`
    (no clickjacking), `object-src 'none'`, `upgrade-insecure-requests`.
  - `Strict-Transport-Security` (1 year, includeSubDomains) — HTTPS only.
  - `X-Content-Type-Options: nosniff`, `Referrer-Policy:
    strict-origin-when-cross-origin`, `X-Frame-Options: DENY`,
    `Cross-Origin-Opener-Policy: same-origin`,
    `Permissions-Policy` denying geolocation, camera, mic, payment, USB.
- **External links** use `target="_blank" rel="noopener"` (no tabnabbing).
- **No inline user HTML**: values rendered into markup are escaped
  (`esc()` helpers in the shortlist, search overlay and Material Match).
- **No secrets in the repo**: `.env`, `google_creds.json` and
  `chrome_profile/` are gitignored, and the site build needs no secrets at all.

## 3. Accounts to protect (the real attack surface)
| Account | Risk if lost | Required |
|---|---|---|
| Domain registrar | Site hijack, email hijack | Strong unique password, 2FA, registrar lock, auto-renew ON |
| Hosting (Cloudflare/Netlify) | Site defacement | 2FA, no shared logins |
| GitHub (`nithishhh14/vicky-elite-balaji`) | Malicious code deployed | 2FA, private repo, branch protection on `main` |
| Google (Search Console, Business Profile) | Fake listing, redirect spam | 2FA, recovery phone/email current |
| Business WhatsApp / email | Impersonation of the client | 2FA, device PIN |

Rules: one owner account per service, no password sharing over WhatsApp,
2FA on all five, and write down recovery codes offline.

## 4. Supply chain
- Dependencies are pinned in `package-lock.json`; deploys build from the lock
  file (`npm ci`).
- Run `npm audit` before each deploy; patch anything high/critical that
  affects the build output.
- Do not add new runtime dependencies or third-party scripts (chat widgets,
  analytics pixels, "free" popups) without checking them against the CSP —
  they are the most likely way this site would ever leak visitor data.
- Astro/Tailwind/GSAP/React updates: review changelogs, rebuild, run
  `npm run qa` before deploying.

## 5. Content integrity (the client's reputation)
- Every image is labelled with what it is (`src/lib/image-badge.ts`,
  provenance labels). Never relabel a generated or supplier image as our own
  stock.
- No prices are published anywhere — supplier MRP is deliberately stripped
  from extracted catalogue images.
- No invented facts (see `CLAUDE.md` hard rules). A false claim is a bigger
  business risk than any technical vulnerability on a static site.

## 6. Monitoring and recovery
- **Backups:** the site is fully reproducible from the Git repo; push to
  GitHub is the backup. Keep the client's original photos and PDFs backed up
  separately (OneDrive already holds them).
- **Uptime:** free uptime check (e.g. UptimeRobot) on the homepage after launch.
- **Search Console:** watch the Security & Manual Actions section; it reports
  hacking or spam.
- **If the site is defaced:** re-deploy from the last good Git commit (one
  command), then rotate the hosting password and check for a compromised token.
- **If the domain expires:** the site and the Google listing both break —
  auto-renew must stay on.

## 7. Deliberately not done
- No analytics/pixels (would need a cookie banner and a privacy policy update).
- No contact form backend (nothing to breach, no spam pipeline).
- No user accounts or file uploads.
