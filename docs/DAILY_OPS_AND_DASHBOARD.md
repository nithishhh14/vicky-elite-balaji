# Daily operations, the data directory, and the admin dashboard

_Written 2026-09-18. This is the answer to: how does SEO get maintained every
day, how do marketing campaigns get updated, what does the combined admin
screen look like, where does Vicky keep its data, and is it futureproof._

Read `docs/OPERATIONS_PLAN.md` first — it covers hosting, accounts, roles and
the migration to the client's PC. This document is the layer above it: the
daily rhythm and the data that rhythm runs on.

---

## 1. Hosting: Cloudflare Pages. Not Vercel, and Supabase isn't a host.

| Option | What it actually is | Verdict |
|---|---|---|
| **Cloudflare Pages** | Static site hosting + CDN, in the same account as the domain | **Use this.** DNS, SSL, redirects and hosting in one place; free; a preview URL per pull request; one-click rollback |
| Vercel | Also static/SSR hosting | Works, but adds a second account and splits DNS from hosting for zero gain on a static site |
| **Supabase** | Postgres database + auth + file storage — a **backend**, not a website host | Not a choice here. There is nothing to put in it today: the site is static and stores no visitor data |

The site is 129 pre-built HTML pages. No server, no database, no login. That is
deliberate — it is why it is fast, cheap, hard to break and hard to hack.

Supabase becomes relevant only if we add something that must remember things
between visits — see §7.

---

## 2. The data directory: `vicky_data/`

One folder holds everything Vicky knows that isn't code. Backing up Vicky =
copying this folder.

```
vicky_data/
├── config/          ← committed to git. The rules.
│   ├── seo_targets.json         23 pages we track, and the search intent of each
│   ├── schedule.json            every automatic job, and the list of things that are never automatic
│   └── campaign_templates.json  post skeletons + the no-fabrication rules
├── state/           ← runtime. Gitignored.
│   ├── approvals/   apr-<date>-<id>.json  — one file per thing waiting for a human yes
│   ├── seo/daily/   <date>.json           — one snapshot a day, forever
│   ├── campaigns/   cmp-<date>-<id>.json  — one file per post
│   ├── logs/        runs-<year>-<month>.jsonl — append-only record of every agent run
│   └── leads/       lead exports (personal data — treat like the Sheet)
├── inbox/           ← what the client sends us
│   ├── photos/      real showroom photos waiting to replace illustrative images
│   └── catalogues/  supplier PDFs waiting for extraction (prices stripped)
├── outbox/drafts/   ← generated posts waiting for a person to publish
└── backups/         ← weekly Google Sheet exports
```

`vicky_store.py` is the only way anything reads or writes this folder. Plain
JSON, standard library only, atomic writes. It works today, with no agents
built and nothing installed.

**Why files and not a database:** one operator, one PC, a few hundred records a
year. Files are readable in Notepad, diffable in git, backed up by copy-paste,
and need no service running. Every record carries `schemaVersion`, so §7's
migration is a script, not a rewrite.

**What stays out of it:** secrets (`.env`, `google_creds.json`), the leads
Sheet itself (it is the shared memory and lives in the cloud), and the website
content (that belongs in git, where it gets reviewed).

---

## 3. Daily SEO maintenance

Two automatic jobs, both read-only, both writing one file a day.

**07:30 — `seo-daily`.** Pull yesterday's Google Search Console rows for the 23
tracked pages and save a snapshot:

```json
{
  "date": "2026-10-04",
  "totals":  { "clicks": 41, "impressions": 1830, "ctr": 2.2, "position": 18.4 },
  "pages":   [ { "path": "/granite-countertops-coimbatore/", "clicks": 6, "impressions": 210, "position": 12.1 } ],
  "queries": [ { "q": "granite countertop coimbatore", "clicks": 3, "impressions": 88, "position": 9.4 } ],
  "flags":   [ "'kota stone coimbatore' fell from position 8 to 19" ]
}
```

**07:40 — `seo-health`.** Fetch the live sitemap and a sample of pages, and
check the things that silently break a site: a page returning 404 or 500, a
canonical pointing at the wrong domain, a title or description that drifted out
of its limit, a page that dropped out of the sitemap, and — our own hard rule —
any price that appeared on a page.

**Weekly — `seo-opportunities`.** Group the week's real queries. Where people
searched for something we stock but have no page for, propose a landing page.
The proposal quotes the actual queries and impressions as evidence, lands in the
approvals queue, and becomes a page only after a person approves it.

What the SEO agent may never do: invent keyword volumes, claim rankings it
didn't measure, publish a page by itself, or touch business facts. A suggestion
carries its evidence or it doesn't leave the machine.

Trends come from our own stored history, which is why the daily snapshot matters
from day one — Search Console keeps 16 months, and we keep everything.

---

## 4. Marketing campaign updates

**Friday 10:00 — `campaign-weekly`.** The Marketing agent drafts next week's
posts from `campaign_templates.json`. Each template has a `needs` list, and
every item must be filled from something real: a product file in the repo, a
photo already in `public/media`, or an offer the owner confirmed in writing. A
template with an unfilled placeholder stays a draft and cannot reach the queue.

Channels: Google Business Profile (the highest-value one for a local showroom),
WhatsApp broadcast, Instagram, and the website itself when a campaign needs a
page behind it.

**Daily 09:00 — `campaign-post-reminder`.** Lists what's approved and due today,
with the text and the photo ready to copy.

A campaign moves `draft → awaiting_approval → scheduled → posted`. **Vicky never
posts to a public account.** It writes the post; a person sends it. That stays
true even after the Google Business Profile API is connected — the API only
removes the copy-paste, not the approval.

Standing content rules, enforced in the template file: no prices, no discounts,
no stock counts, no review quotes, no ratings, no dealership claims, and no
photo presented as Elite Balaji's own unless it is.

---

## 5. The combined admin dashboard

The Vicky dashboard is the admin screen — there is no separate admin site to
build, secure and log into. `app.py` now carries an **Operations** panel above
the lead ledger:

```
┌─ Operations ────────────────────────────────────────────────┐
│  Waiting for you   Campaign drafts   SEO last pulled   Inbox │
│        3                  2            2026-10-04 +12%    5  │
├─────────────────────────────────────────────────────────────┤
│ [ Approvals ] [ SEO ] [ Campaigns ] [ Agent runs ]           │
│                                                              │
│  Add 3 wood-look tiles                                       │
│  Three products from the supplier PDF, prices stripped.      │
│  website · asked 2026-10-04 09:12                            │
│  → Open the preview                                          │
│  [ Approve ]  [ Reject ]                                     │
└──────────────────────────────────────────────────────────────┘
```

- **Approvals** — every change any agent wants to make, in one queue, with the
  Cloudflare preview link. Approve or reject, with a note back to Vicky.
- **SEO** — the last 30 daily snapshots as a table, plus the day's flags.
- **Campaigns** — drafts and scheduled posts, with the text ready to copy.
- **Agent runs** — what ran, when, and whether it worked.

It reads `vicky_data/` through `vicky_store`, so it works right now and simply
shows empty sections until the agents start writing. Approving something writes
a local decision; publishing still happens through GitHub and Cloudflare, which
keep the real history and the rollback button.

It is reachable from a phone on the same network (`streamlit run app.py`), which
is enough for approvals. If the client later wants to approve from anywhere with
the PC off, that is the point at which §7 applies — not before.

---

## 6. Who writes what

| File/folder | Written by | Read by |
|---|---|---|
| `config/*.json` | A person, in git | Every agent |
| `state/approvals/` | Any agent (create) · the owner in the dashboard (decide) | Dashboard, Executive |
| `state/seo/daily/` | SEO agent | Dashboard, SEO agent (trends), Marketing (what to push) |
| `state/campaigns/` | Marketing agent | Dashboard, Executive |
| `state/logs/` | Every agent | Dashboard |
| `inbox/` | The client / you, by dropping files in | Website agent |
| `outbox/drafts/` | Marketing, Email | A person, to send |
| `backups/` | The weekly backup job | A person, if something is lost |

---

## 7. Is it futureproof?

**Already permanent.** The website's content is schema-validated data, not
markup; the checks run in CI; the site is static; every record here carries
`schemaVersion`; and `vicky_store` is the single door to the data, so changing
what sits behind that door touches one file.

**The one thing that would force a change** is a second person needing access
when the PC is off. Everything here assumes one operator at one machine. Watch
for three signals:

1. The client wants to approve changes from their phone, anywhere, with the PC
   switched off.
2. More than one person needs the same queue at the same time.
3. The website starts needing to store something from a visitor — a booked
   measurement slot, a shortlist that survives the browser, a quote.

**Then, and only then,** Supabase (or any Postgres) earns its place. The
migration is small by design:

- `state/` becomes four tables — `approvals`, `seo_daily`, `campaigns`,
  `run_log` — whose columns are the JSON keys already in use.
- Rewrite the ten functions in `vicky_store.py`; nothing else changes.
- The dashboard keeps working, because it only calls `vicky_store`.
- A one-off script loads the existing JSON files in, because `schemaVersion`
  says exactly what shape they are.
- The website would then gain one small form endpoint — and that is the moment
  to revisit hosting, since a database means secrets, rate limits and a privacy
  notice that a static site doesn't need.

Until one of those three signals appears, a database would cost a paid service,
a second set of credentials to rotate and a new outage surface, in exchange for
nothing the client can see.

---

## 8. What's built now, and what comes next

**Built today:** `vicky_data/` with its config seeded, `vicky_store.py`, and the
Operations panel in the dashboard.

**Next, in this order** (unchanged from `docs/OPERATIONS_PLAN.md` §4):

1. **Website agent** — reads `inbox/`, opens pull requests, files approvals.
   Everything else eventually becomes a website change, so it goes first.
2. **SEO agent upgrade** — connect Search Console (read-only), then the jobs
   `seo-daily`, `seo-health`, `seo-opportunities`.
3. **Marketing agent** — the weekly draft job. Unblocks once the site is live.
4. **Email agent** — drafts only, as it always was.
5. **Executive** — routes "add this product", "what's ranking", "post the
   offer", and surfaces the approvals queue in chat.

A scheduler is deliberately not built yet: `schedule.json` is the specification,
and until the agents exist there is nothing to schedule. When they do, Windows
Task Scheduler running one `python -m vicky_jobs <job-id>` per row is enough —
no new service, and it survives a reboot.
