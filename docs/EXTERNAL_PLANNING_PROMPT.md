# External planning prompt — Vicky / Elite Balaji

_Written 2026-09-11. Copy everything in the fenced block below into an
external LLM (ChatGPT, Gemini, a fresh Claude session, etc.) to get a full
architecture and build plan. Bring the result back into this project's
Claude Code session so it can be reconciled against `docs/DECISIONS.md`
before anything is built — do not implement an external plan blind._

---

```
I need you to act as a senior solo-founder technical architect and produce a
complete, step-by-step build plan for a real small business's automation
system. I am a novice at cloud infrastructure and GitHub — I can follow
precise instructions, but I don't know the vocabulary yet, so explain
deployment steps like you would to someone who has never deployed anything
before. Do not assume I know what a "repo", "environment variable," or
"DNS record" is until you've briefly defined it once.

====================================================================
BUSINESS CONTEXT (real facts — do not alter or embellish these)
====================================================================
- Business: Elite Balaji Stones & Ceramics, Karamadai, Coimbatore, Tamil
  Nadu, India. Trading since 2012.
- What they sell: granite, marble, tiles, sanitaryware, sinks, tile
  adhesive/epoxy/accessories, granite engraving/sculptures/name boards, plus
  their own laying (installation) crews and site measurement/estimation.
- Customers: wholesale/trade — contractors, builders, civil engineers, laying
  crews, and project customers, not just walk-in retail.
- Owner/contact: Vignesh Yadav A, +91 91590 56767.
- Service area: Coimbatore city and nearby hubs (Mettupalayam, Karamadai,
  Kallar, Ooty, Kotagiri, Nilgiris, Sirumugai, Annur, Periyanaickenpalayam,
  Saravanampatti, Thudiyalur, RS Puram).
- Budget: effectively ₹0 for software/hosting until proven necessary. Prefer
  free tiers (GitHub, Cloudflare, etc.) over paid SaaS. Flag anything that
  would cost money clearly, with the free alternative, rather than assuming
  it's fine to spend.

====================================================================
WHAT ALREADY EXISTS (do not redesign from scratch — extend/integrate it)
====================================================================
This is a Python-based multi-agent system called "Vicky," run locally on the
owner's Windows machine today, with these pieces already built and working:

1. **Lead-generation scraper** (`lead_agent.py`) — harvests business leads
   from Google Maps + Google Search for the service area above, normalizes
   and deduplicates them, filters to the service hubs only. LIVE and working.

2. **Shared memory layer** (`shared_memory.py`) — currently a Google Sheet
   (via `gspread`), holding: a leads sheet, a council activity log, and an
   SEO audit sheet. This is the closest thing to a "database" today — it is
   NOT a real database yet.

3. **SEO agent** — writes local-SEO audit notes into the shared sheet. LIVE.

4. **Marketing agent** — currently a stub. Intentionally blocked until the
   public website is live and reachable, so it has real brand pages to
   generate campaigns from. NOT YET BUILT OUT.

5. **Email agent** — currently a stub. Drafts only, human must approve before
   anything sends — auto-send is explicitly forbidden by project rules. Also
   blocked on the website going live. NOT YET BUILT OUT.

6. **Executive agent** (`vicky_executive.py`) — a simple keyword/regex intent
   router that dispatches commands to the above agents, plus a Gemini-backed
   general chat fallback. This is the seed of the "Vicky" personal-assistant
   layer, but today it only runs inside a local Streamlit dashboard
   (`app.py`) on one machine, one session at a time, with no memory of past
   conversations beyond the current process.

7. **Public website** ("virtual showroom") — just rebuilt as a static Astro 5
   + TypeScript + Tailwind CSS v4 site. Home page, 8 product-category pages
   ("halls": Tiles, Granite & Marbles, Kota Stone, Kadappa, Sanitaryware,
   Adhesive & Accessories, Quartz, Laying Works), About, Contact. WhatsApp-
   based enquiry flow (no backend needed for that part). Only the Tiles hall
   has real product photography so far; the rest use a placeholder design
   until real photos exist. The site builds successfully locally but is
   **not deployed anywhere yet** — no domain, no hosting connected, and while
   a local git repository exists, there is no GitHub remote yet.

Tech stack currently in use: Python 3.14, Streamlit, Google Sheets API
(gspread + google-auth), Google Gemini API (`google-generativeai`), Playwright
(for the scraper), Astro 5 + TypeScript + Tailwind CSS v4 + Node.js 24 (for
the website). No database yet. No cloud hosting yet. No mobile app yet.

====================================================================
HARD RULES (do not propose anything that violates these)
====================================================================
- Never fabricate business facts, product data, prices, certifications, or
  testimonials. Never present stock/catalogue photos as genuine Elite Balaji
  product/premises photos unless they actually are.
- Never let an agent auto-send a real email or message to a real customer
  without human approval first.
- API keys/credentials must never be hardcoded or committed to git — they
  must load from environment variables / a secrets manager, and example env
  files must only contain safe placeholder names.
- Prefer the smallest amount of new infrastructure that actually works —
  no premature scaling, no infra "because it's best practice," everything
  must be justified by an actual near-term need for a single-location small
  business.
- Marketing and Email agents must stay gated behind the website actually
  being live and reachable at a public URL — don't have them activate before
  that.

====================================================================
THE GOAL — please produce a complete architecture + step-by-step plan for:
====================================================================

**A. The three remaining specialist agents, fully speced:**
   1. Marketing Agent — what it should actually do once the website is live
      (e.g. drafting social captions/posts from real hall/product content,
      suggesting local-SEO content ideas), what data it needs, what it
      should never do (no fabricated claims, no auto-posting without
      approval unless explicitly decided otherwise).
   2. Email Agent — drafting only, human-approved sending, what triggers a
      draft (e.g. a new lead from the scraper), what it needs access to.
   3. Executive / "Vicky" agent as a true personal-assistant orchestrator —
      not just a keyword router, but something that can hold real
      multi-turn context, learn the owner's preferences over time, and
      route across the other agents intelligently.

**B. The website's remaining needs** to go from "builds locally" to
   "genuinely live and useful": hosting choice (evaluate free options,
   recommend one with reasons), domain strategy (can it launch on a free
   subdomain first and add a custom domain later without rework?), and how
   the Marketing/SEO agents should actually read from the live site once
   it's up (e.g. a content API, a shared data file, or something else —
   your call, justify it).

**C. The "Vicky as a cross-device JARVIS assistant" vision:** the owner
   wants Vicky to eventually be reachable from his own devices (phone,
   laptop, etc.) — not just one Streamlit tab on one PC — and to
   automatically keep a "brain" of his requirements/preferences that
   updates itself over time rather than requiring manual re-entry every
   session. For this, please design:
   - What "reachable across devices" should concretely be for a solo small
     business owner with a ₹0-first budget — e.g. a mobile-friendly web app/
     PWA with notifications vs. a lightweight always-on backend the owner
     talks to via WhatsApp/Telegram vs. something else. Compare options and
     recommend one, with reasons and a rough cost if it ever needs to leave
     the free tier.
   - What "auto-updating backend brain" should actually be: a real database
     (recommend one, free-tier friendly) replacing the Google Sheet for
     structured data, PLUS a preferences/context store that updates from
     the owner's actual usage over time (e.g. explicit corrections he gives
     Vicky, patterns in what he asks for). Be concrete about the data model
     and update mechanism — don't hand-wave "AI will just remember."
   - Privacy/security: this brain will hold real business + personal-
     preference data. What's the minimum sensible protection for a solo
     operator (not an enterprise) — auth for the owner's own access, secrets
     handling, backup strategy.
   - How this backend relates to the existing agents (Scraper, SEO,
     Marketing, Email, Executive) — should they all read/write through it,
     or stay mostly independent with the brain just for the Executive layer?

**D. A complete, beginner-friendly GitHub + cloud deployment walkthrough**,
   written for someone who has never done this before:
   - What GitHub actually is and why we need it (one paragraph, plain
     English).
   - Exact steps to create a GitHub account (if needed) and a new repository
     for this existing local project.
   - Exact commands to connect the existing local git repository (already
     initialized, 3 commits, branch `master`, no remote) to that new GitHub
     repository and push it, explained line by line.
   - How to deploy the Astro website from that GitHub repo to a free host
     (evaluate Cloudflare Pages vs. GitHub Pages vs. others, recommend one),
     step by step, including where environment variables/secrets go if
     needed.
   - Where and how the Python backend (agents + the future "brain") should
     actually run continuously — a free-tier cloud option appropriate for a
     small, low-traffic solo project, explained simply, with the tradeoffs
     of each option you consider (always-on server vs. serverless functions
     vs. a scheduled job) named plainly.
   - How rollback works if a deploy breaks something (in plain English).

====================================================================
OUTPUT FORMAT I WANT
====================================================================
1. A short "Architecture Overview" section — plain language, no jargon
   without a one-line definition the first time it's used.
2. A numbered, sequential list of phases (build on top of what already
   exists — don't propose throwing away the working scraper, website, or
   Google Sheet unless you explicitly justify the replacement).
3. For each phase: goal, concrete deliverables, exact tools/services to use
   (favoring free tiers, naming the paid alternative only if genuinely
   better and flagging the cost), and how to verify that phase actually
   works before moving to the next.
4. A single consolidated list, at the end, of every decision that needs my
   explicit yes/no before it's implemented (e.g. "buy a domain," "create a
   database account," "connect a GitHub remote") — do not bundle these into
   the middle of the plan where they're easy to miss.
5. Be honest about complexity and time — I am a solo, non-professional
   builder using an AI coding assistant (Claude Code) to implement this.
   Don't propose an enterprise-grade architecture for a single-location
   family business.
```

---

## What to do with the result

1. Paste the external LLM's answer back into this Claude Code session.
2. Claude will reconcile it against `docs/DECISIONS.md` and this project's
   hard rules (no fabrication, ₹0-first, phased build order, human-approved
   sends) before proposing any implementation.
3. Anything involving spending money, creating external accounts, or
   irreversible changes still needs your explicit go-ahead at that point —
   getting a plan back doesn't pre-authorize acting on it.
