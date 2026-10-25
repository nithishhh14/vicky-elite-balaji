// Structural audit of every built page, in a real browser.
// Usage: npm run build && npx astro preview --port 4322, then
//   node scripts/audit.mjs [baseUrl]
//
// qa.mjs asks "does it render and behave". This asks "is the markup right":
// things a visitor feels without being able to name them (a link a screen
// reader announces as "link", a #anchor that goes nowhere, an image that
// shoves the page as it loads) and things that should never reach a page
// (template leaks like "undefined" or "[object Object]").
import { chromium } from "playwright";
import { readdirSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";

const BASE = process.argv[2] ?? "http://localhost:4322";
const DIST = new URL("../dist/", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");

function pages(dir) {
  return readdirSync(dir).flatMap((name) => {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) return pages(full);
    return name === "index.html" ? ["/" + relative(DIST, dir).split(sep).join("/")] : [];
  });
}
const routes = pages(DIST).map((r) => (r === "/" ? "/" : r.replace(/\/?$/, "/")));

const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1366, height: 900 }, reducedMotion: "reduce" });
const problems = new Map(); // message -> [routes]
const note = (route, msg) => {
  if (!problems.has(msg)) problems.set(msg, []);
  problems.get(msg).push(route);
};

for (const route of routes) {
  const page = await context.newPage();
  await page.goto(BASE + route, { waitUntil: "networkidle" });
  const found = await page.evaluate(() => {
    const out = [];
    const visible = (el) => {
      const s = getComputedStyle(el);
      return s.display !== "none" && s.visibility !== "hidden" && !el.closest("[hidden], [aria-hidden=true]");
    };
    const name = (el) =>
      (el.getAttribute("aria-label") || el.getAttribute("aria-labelledby") && "x" || el.getAttribute("title") ||
        el.textContent || [...el.querySelectorAll("img[alt]")].map((i) => i.alt).join(" ") || "").trim();

    // Duplicate ids break label/aria wiring and in-page links.
    const ids = {};
    document.querySelectorAll("[id]").forEach((el) => (ids[el.id] = (ids[el.id] || 0) + 1));
    Object.entries(ids).filter(([, n]) => n > 1).forEach(([id]) => out.push(`duplicate id "${id}"`));

    // Images: alt present (empty is fine for decoration), size reserved.
    document.querySelectorAll("img").forEach((img) => {
      if (!img.hasAttribute("alt")) out.push(`img without alt: ${img.getAttribute("src")}`);
      const reserved = img.hasAttribute("width") && img.hasAttribute("height");
      const boxed = getComputedStyle(img).position === "absolute" || /object-cover|object-contain|h-full|aspect-/.test(img.className) || img.closest("[class*='aspect-']");
      if (!reserved && !boxed && visible(img) && img.getBoundingClientRect().height > 40)
        out.push(`img may shift layout (no width/height): ${img.getAttribute("src")}`);
    });

    // Links and buttons need a name.
    document.querySelectorAll("a[href], button").forEach((el) => {
      if (!visible(el)) return;
      if (!name(el)) out.push(`${el.tagName.toLowerCase()} without accessible name: ${el.outerHTML.slice(0, 90)}`);
    });

    // In-page anchors must land somewhere.
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      const id = decodeURIComponent(a.getAttribute("href").slice(1));
      if (id && !document.getElementById(id)) out.push(`anchor to missing #${id}`);
    });

    // tel: and wa.me must carry a real number.
    document.querySelectorAll('a[href^="tel:"]').forEach((a) => {
      if (!/^tel:\+?\d{10,13}$/.test(a.getAttribute("href"))) out.push(`odd tel link: ${a.getAttribute("href")}`);
    });
    document.querySelectorAll('a[href*="wa.me/"]').forEach((a) => {
      if (!/wa\.me\/\d{11,13}(\?|$)/.test(a.getAttribute("href"))) out.push(`odd WhatsApp link: ${a.getAttribute("href").slice(0, 60)}`);
    });

    // Exactly one h1; headings don't skip down more than one level.
    const hs = [...document.querySelectorAll("main h1, main h2, main h3, main h4")].filter(visible);
    const h1s = [...document.querySelectorAll("h1")].length;
    if (h1s !== 1) out.push(`${h1s} h1 elements`);
    let prev = 1;
    for (const h of hs) {
      const lvl = Number(h.tagName[1]);
      if (lvl > prev + 1) { out.push(`heading jumps h${prev} -> h${lvl}: "${h.textContent.trim().slice(0, 40)}"`); break; }
      prev = lvl;
    }

    // Template leaks in visible text.
    const text = document.body.innerText;
    for (const leak of ["undefined", "[object Object]", "NaN", "null ", "TODO", "lorem", "{{", "}}"]) {
      if (text.includes(leak)) out.push(`visible text contains "${leak}"`);
    }

    // Structured data must parse.
    document.querySelectorAll('script[type="application/ld+json"]').forEach((s) => {
      try { JSON.parse(s.textContent); } catch { out.push("invalid JSON-LD block"); }
    });

    // Every external link opened in a new tab should not leak the opener.
    document.querySelectorAll('a[target="_blank"]').forEach((a) => {
      if (!/noopener|noreferrer/.test(a.getAttribute("rel") || "")) out.push(`target=_blank without noopener: ${a.getAttribute("href")?.slice(0, 50)}`);
    });
    return out;
  });
  found.forEach((m) => note(route, m));
  await page.close();
}
await browser.close();

if (!problems.size) {
  console.log(`Audit: ${routes.length} pages, no problems found.`);
} else {
  console.log(`Audit: ${routes.length} pages, ${problems.size} distinct problems`);
  for (const [msg, rs] of [...problems].sort((a, b) => b[1].length - a[1].length)) {
    console.log(`  ${String(rs.length).padStart(3)} page(s)  ${msg}   e.g. ${rs.slice(0, 2).join(" ")}`);
  }
  process.exitCode = 1;
}
