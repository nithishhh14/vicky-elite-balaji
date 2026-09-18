# Operations plan — how Elite Balaji's website and Vicky run from here

_Written 2026-09-17, after the domain `www.elitebalaji.com` was bought on
Cloudflare. This is the single answer to: where does everything live, how do
updates happen, what does Vicky do, is an admin needed, and how does this move
to the client's PC._

---

## 1. The whole picture

```
 Client / you ──"Vicky, add the new wood-look tiles"──► VICKY (dashboard on a PC)
                                                          │  Executive routes the request
                                                          ▼
                                     Website agent edits content files on a NEW BRANCH
                                     (product JSON, photos, landing pages — never prices)
                                                          │  opens a pull request
                                                          ▼
                              GitHub ── runs `npm run preflight` (23 checks, Playwright)
                                                          │  pass
                                                          ▼
                     Cloudflare Pages builds a PREVIEW link (e.g. abc123.elitebalaji.pages.dev)
                                                          │
                                   OWNER looks at the preview, taps Approve
                                                          │  merge to main
                                                          ▼
                     Cloudflare Pages publishes to www.elitebalaji.com (~2 minutes)
```

Nothing reaches the live site without passing the checks **and** a human
approval. Vicky does the work; a person says yes.

---

## 2. Where everything lives (and what needs what)

| What | Lives in | Owned by (target) | Needs a PC running? |
|---|---|---|---|
| **Website code, content, photos** (89 products, 390 media files, all pages) | **GitHub** private repo | Client's GitHub account/organisation | No |
| **The live website** | **Cloudflare Pages** (global CDN) | Client's Cloudflare account (domain already there) | **No** — runs 24×7 in the cloud |
| **Domain + DNS** `elitebalaji.com` | Cloudflare Registrar | Client | No |
| **Enquiries from visitors** | The client's **WhatsApp / phone / email** (the site stores nothing) | Client | No |
| **Leads, Council log, SEO audits** | **Google Sheet** (shared memory) | Client's Google account | No (the Sheet is in the cloud) |
| **Vicky dashboard + agents** (Streamlit, Python) | A **PC** (yours now, the client's later) | Client | **Yes, while in use** |
| **Secrets** (`.env` Gemini key, `google_creds.json`, GitHub token, Cloudflare token) | Only on the PC running Vicky, never in Git | Client | — |
| **Original client photos and supplier PDFs** | OneDrive `whatsapp vicky pdfs` | Client (move to client's cloud drive) | No |
| **Search visibility** | Google Search Console + Google Business Profile | Client's Google account | No |

**The key point:** the website does **not** live on anyone's PC. The PC only
matters for running Vicky. If the PC is off, the site stays up.

---

## 3. How the website gets updated

### Today (until the Website agent exists)
1. Change content in `website/src/content/…` or `website/public/media/…`
   (done via Claude Code, as we have been).
2. `cd website && npm run preflight` → must say **Ready to deploy**.
3. Commit and push to `main` → Cloudflare Pages rebuilds and publishes.

### What kinds of change there are
| Change | Where | Risk | Approval |
|---|---|---|---|
| Add/edit a product, size, finish | `src/content/products/*.json` | Low | Owner |
| New landing page | `src/content/guides/*.json` | Low | Owner |
| Replace an illustrative image with a real photo | `public/media/…` + the product JSON | Low | Owner |
| Import a supplier catalogue PDF | extraction script → media + product JSON (**prices stripped**) | Medium | Owner + check photos |
| Business facts (phone, address, offers) | `src/lib/business.ts` | **High** (legal/claims) | Owner only |
| Design / layout / code | `src/components`, `src/pages` | Higher | Developer review |

### Soon: through Vicky (the Website agent)
- The editable surface and the recipes are fixed in `docs/CONTENT_EDITING.md`;
  `npm run check:content` enforces them.
- Vicky gets a **GitHub token limited to this one repository** (contents +
  pull requests only; no settings, no deleting, no pushing to `main`).
- It works on a branch, opens a pull request with a plain-English summary and
  the Cloudflare preview link, and posts it to the dashboard for approval.
- `main` is **branch-protected**: the `website-preflight` GitHub Action must
  pass before anything can merge (the workflow is already in
  `.github/workflows/website-preflight.yml`).

---

## 4. The agents still to build, in order

| Order | Agent | Does | Touches | Guardrails |
|---|---|---|---|---|
| 1 | **Website agent** (new) | Add/edit products, swap in real photos, import catalogue PDFs, add landing pages | GitHub (branch + PR) | Never edits `business.ts` facts or prices; every change is a PR; preflight must pass |
| 2 | **SEO agent** (upgrade the stub) | Pull Google Search Console data (queries, clicks, pages not indexed), flag drops, suggest new landing pages from real search queries, monthly report to the Sheet | Search Console API (read-only), Sheet | Suggestions only; page creation goes through the Website agent |
| 3 | **Marketing agent** | Draft Google Business Profile posts, WhatsApp broadcast text, Instagram captions for offers (e.g. free site measurement, new basin range) | Sheet (drafts) | Drafts only; a person posts. GBP API needs Google's approval first |
| 4 | **Email agent** | Draft replies/quotes from enquiries | Sheet | Drafts only, never auto-sends (existing rule) |
| 5 | **Executive (Vicky)** | Understands "update the website / add this product / what's ranking / post the offer" and routes to the right agent; shows approvals in one queue | All of the above | Nothing irreversible without an approval |

Technical notes for when building starts:
- The agents use `google.generativeai`, which Google has deprecated in favour
  of the `google-genai` SDK. Migrate while building the new agents.
- The **approval queue** is now `vicky_data/state/approvals/`, read and decided
  in the dashboard's Operations panel — see `docs/DAILY_OPS_AND_DASHBOARD.md`.
- Order matters: the Website agent first, because the other agents' outputs
  (new pages, offers) all end up as website changes.

---

## 5. Is an admin required?

**Yes — a person, not a separate admin website.**

| Role | Who | Can |
|---|---|---|
| **Owner** | The client (Elite Balaji) | Owns every account and bill; approves changes; final say on offers, facts and photos |
| **Operator** | You now; later a trained staff member | Runs Vicky, reviews pull requests, fixes failed checks, rotates keys |
| **Vicky** | Software | Prepares changes and drafts; **cannot publish on its own** |

- **No separate CMS/admin panel is needed now.** The Vicky dashboard *is* the
  admin screen — its Operations panel holds the approvals queue, the daily SEO
  numbers, the campaign drafts and the agent run log — and GitHub + Cloudflare keep a full history with one-click
  rollback.
- **Optional later:** if the client wants to edit text and photos in a browser
  without Vicky, add a Git-based CMS (e.g. Sveltia or Decap CMS) on top of the
  same repo. Same files, same checks, no database.
- **Accounts must belong to the client** (GitHub, Cloudflare, Google), with
  you added as a member. That way nothing breaks if people change.

---

## 6. Moving to the client's PC

### What moves and what doesn't
- **Does not move** (already in the cloud): the live site, the domain, the
  Google Sheet, Search Console, the GitHub repo.
- **Moves**: the Vicky dashboard/agents install, their secrets, and the
  original photos/PDFs.

### Client PC requirements
Windows 10/11, 8 GB RAM or more, always-on internet. Install: **Git**,
**Node.js 22 LTS**, **Python 3.12+**, and optionally VS Code.

### Procedure
1. **Accounts first (client-owned):**
   - GitHub: create the client's account or organisation → transfer the repo
     `vicky-elite-balaji` to it → add yourself as a collaborator.
   - Cloudflare: already the client's (domain bought there) → add yourself as a member.
   - Google: move ownership of the leads Sheet to the client's Google account;
     verify Search Console and Business Profile under the client's account.
2. **Fresh secrets on the client PC — never copy the old ones over WhatsApp or USB:**
   - Create a **new** Gemini API key in the client's Google account.
   - Create a **new** Google service account, download its JSON as
     `google_creds.json`, and share the Sheet with that service account's email.
   - Create a fine-grained GitHub token for the Website agent (one repo only).
   - Delete/disable the old keys on your side afterwards.
3. **Install:** `git clone` the repo → `pip install -r requirements.txt` →
   `cd website && npm ci` → create `.env` with the new keys.
4. **Verify:** open the dashboard (`streamlit run app.py`), run a status
   command, then `cd website && npm run preflight` → **Ready to deploy**.
5. **Move the originals:** copy `whatsapp vicky pdfs` and client photos to the
   client's own cloud drive (Google Drive/OneDrive), not only to the PC disk.
6. **Hand over:** a one-page login list kept by the owner (not in the repo),
   2FA on every account, and a 15-minute walkthrough of "approve a change" and
   "roll back a deploy".

---

## 7. Launch procedure (domain is ready)

| # | Step | Who |
|---|---|---|
| 1 | Push the repo to GitHub (`main`) — **needs your go-ahead** | You / me |
| 2 | Cloudflare → Workers & Pages → Create → Pages → Connect to Git → pick the repo | You (client's account) |
| 3 | Build settings: root `website`, build `npm ci && npm run build`, output `dist`, env `SITE_URL=https://www.elitebalaji.com` | You |
| 4 | Custom domains: add `www.elitebalaji.com`, then add a **Redirect Rule** `elitebalaji.com/*` → `https://www.elitebalaji.com/$1` (301) | You |
| 5 | SSL/TLS: Full (strict); "Always Use HTTPS" on | You |
| 6 | GitHub → Settings → Branches → protect `main`, require the `website-preflight` check | You |
| 7 | Verify live: open the site on a phone; `npm run qa -- https://www.elitebalaji.com` | Me |
| 8 | Google Search Console (Domain property, DNS verify in Cloudflare) → submit `https://www.elitebalaji.com/sitemap-index.xml` | You (client's Google) |
| 9 | Google Business Profile → website link = `https://www.elitebalaji.com` | Client |
| 10 | Bing Webmaster Tools → import from Search Console | You |

Rollback at any time: Cloudflare Pages → Deployments → "Rollback to this deployment".

---

## 8. Running costs (free tiers cover this site)

| Service | Cost |
|---|---|
| Cloudflare Pages hosting | Free tier (static site, unlimited requests; build count is capped monthly) |
| Domain `elitebalaji.com` | Yearly renewal at Cloudflare Registrar — keep auto-renew ON |
| GitHub private repo + Actions | Free tier (monthly Actions minutes are enough for this repo) |
| Google Sheets / Search Console / Business Profile | Free |
| Gemini API (for Vicky) | Free tier or pay-per-use, depending on volume |
| Image generation | Only if a paid plan is chosen; real photos preferred |

---

## 9. Security routine
- Before every deploy: `npm run preflight` (CI enforces it once `main` is protected).
- Monthly: `npm audit`; update Astro/dependencies; re-run preflight.
- Yearly: renew `/.well-known/security.txt` expiry; rotate API keys; check
  domain auto-renew.
- On any suspected compromise: roll back the Cloudflare deployment, revoke the
  GitHub token, rotate Cloudflare/Google passwords (see `docs/SECURITY.md`).
