# TOMORROW — START HERE

## Current objective
Phase 2 (the Elite Balaji public website) is functionally rebuilt on Astro.
The immediate objective now is **client feedback and content completion**,
not further architecture work.

## What was completed today (2026-09-10)
- Full rebuild of `website/` from static HTML to Astro 5 + TypeScript +
  Tailwind v4 (see `docs/PROJECT_STATE.md` for the complete, verified list).
- Real product content for the Tiles hall (7 series, sourced from genuine
  supplier catalogues, user-confirmed).
- `MaterialField` placeholder for the 7 halls without real photography.
- WhatsApp enquiry flow, SEO foundation, responsive nav, a11y basics.
- Found and fixed a real layout bug (`MaterialField` position conflict).
- `astro check` + `astro build` both verified clean at end of session.
- git initialized for the whole project; two commits made; no remote yet.
- This handoff system itself (`docs/PROJECT_STATE.md`,
  `docs/CLIENT_PREFERENCES.md`, `docs/DECISIONS.md`, this file).

## What still needs work
- Real photography for 6-7 halls (see `docs/PROJECT_STATE.md` "Blocked items").
- Domain + hosting decision, then actual deployment.
- GitHub remote setup.
- A first round of client feedback on design direction — nothing has been
  reviewed by the client yet, so treat the current design as a draft, not
  a locked decision, until `docs/CLIENT_PREFERENCES.md` says otherwise.

## First thing Claude should inspect
Run `git log --oneline` and `git status` to confirm nothing changed outside
this session, then read the six files listed in the Resume Instruction below.

## First task to execute
Depends entirely on what the user says at the start of the next session.
Do not assume — ask, or read `docs/CLIENT_PREFERENCES.md` if the user says
"I have client feedback" before touching any code.

## Client information I need to provide
(For the user, not Claude — things Claude cannot get on its own:)
- Real photos or a photo shoot plan for Granite & Marbles, Kota Stone,
  Kadappa, Sanitaryware, Adhesive & Accessories, Quartz.
- Any explicit design feedback (colours, layout, tone) from Elite Balaji.
- A domain name decision (buy one, or launch on a free subdomain first).
- Confirmation of whether/when to create a GitHub remote.

## Design decisions waiting for client feedback
Every section of `docs/CLIENT_PREFERENCES.md` is currently PENDING CLIENT
INPUT. The Athangudi-derived colour palette and the `MaterialField` placeholder
approach are working assumptions (see `docs/DECISIONS.md`), not confirmed
client preferences.

## Known bugs
None open. The `MaterialField` position-conflict bug found during this
session's QA was fixed and verified (see `docs/PROJECT_STATE.md`
"Known issues" and `docs/WEBSITE_ARCHITECTURE.md` §5).

## Known placeholders
- 7 of 8 halls use `MaterialField` colour/texture panels instead of real
  photography (Tiles is the only hall with real product images).
- `astro.config.mjs`'s `site` and `public/robots.txt`'s sitemap URL use a
  placeholder hostname (`elitebalaji.example.in`).

## Assets still required
- Real photographs: granite/marble slabs, kota stone, kadappa stone,
  sanitaryware/sinks in stock, adhesive/accessory packaging or application
  shots, quartz surfaces, laying-works in progress.
- Optional: partner brand logo files (currently a plain text list in the footer).

## Deployment status
Not deployed anywhere. No hosting connected, no domain purchased, no CI/CD.
The site builds successfully to `website/dist/` locally.

## Git status
- Local repository only, branch `master`, 2 commits, no remote.
- Working tree was clean at end of session (verify again with `git status`
  before assuming this still holds).

## Important files to read first
See the Resume Instruction below — it's the authoritative list.

---

# RESUME INSTRUCTION

When a new Claude Code session begins on this project, Claude MUST read:

1. `CLAUDE.md`
2. `docs/PROJECT_STATE.md`
3. `docs/CLIENT_PREFERENCES.md`
4. `docs/DECISIONS.md`
5. `docs/NEXT_SESSION.md` (this file)
6. `docs/WEBSITE_ARCHITECTURE.md`

before making significant changes to the website or its documentation.
