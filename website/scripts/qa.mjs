// Playwright QA sweep over the built site.
// Usage: npm run build && npx astro preview --port 4322, then
//   node scripts/qa.mjs [baseUrl]
// Visits every page in dist/ at desktop and phone width and reports console
// errors, failed requests, broken images, horizontal overflow, and generated
// images shown without their "Illustrative image" label.
import { chromium } from "playwright";
import { readdirSync, statSync, mkdirSync } from "node:fs";
import { join, relative, sep } from "node:path";

const BASE = process.argv[2] ?? "http://localhost:4322";
const DIST = new URL("../dist/", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
const SHOTS = new URL("../qa-screens/", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
mkdirSync(SHOTS, { recursive: true });

function pages(dir) {
  return readdirSync(dir).flatMap((name) => {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) return pages(full);
    return name === "index.html" ? ["/" + relative(DIST, dir).split(sep).join("/")] : [];
  });
}
const routes = pages(DIST).map((r) => (r === "/" ? "/" : r.replace(/\/?$/, "/")));

const viewports = [
  // 1920 covers the 2xl breakpoint. Without it a header that only breaks on a
  // wide monitor ships unseen — which is exactly how the logo once grew into
  // the nav.
  { name: "wide", width: 1920, height: 1080 },
  { name: "desktop", width: 1366, height: 900 },
  { name: "phone", width: 375, height: 812 },
];
const screenshotRoutes = new Set(["/", "/halls/sanitaryware/", "/products/sanitary-quartz-sink-single/", "/halls/quartz/"]);

const browser = await chromium.launch();
const problems = [];
for (const vp of viewports) {
  const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, reducedMotion: "reduce" });
  for (const route of routes) {
    const page = await context.newPage();
    const issues = [];
    page.on("console", (m) => m.type() === "error" && issues.push(`console: ${m.text()}`));
    page.on("pageerror", (e) => issues.push(`pageerror: ${e.message}`));
    page.on("requestfailed", (r) => {
      if (r.url().startsWith(BASE)) issues.push(`request failed: ${r.url()}`);
    });
    page.on("response", (r) => {
      if (r.url().startsWith(BASE) && r.status() >= 400) issues.push(`HTTP ${r.status()}: ${r.url()}`);
    });
    await page.goto(BASE + route, { waitUntil: "load" });
    // Load lazy images before checking them.
    await page.evaluate(async () => {
      // Measure after the webfonts land: the fallback serif is wider, so the
      // wordmark reads as overlapping for the split second before the swap.
      await document.fonts.ready;
      document.querySelectorAll("img[loading=lazy]").forEach((i) => (i.loading = "eager"));
      await Promise.all([...document.images].map((i) => (i.complete ? null : new Promise((r) => { i.onload = i.onerror = r; }))));
    });
    const result = await page.evaluate(() => {
      const broken = [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && i.src).map((i) => i.src);
      const overflow = document.documentElement.scrollWidth - window.innerWidth;
      // A generated image on a card or product hero must carry its label
      // within the same card / image frame.
      const unlabelled = [...document.querySelectorAll('img[src*="/media/illustrative/"]')]
        .filter((img) => !img.closest("#search-results, [data-shortlist-list], #mm-results, .product-thumb, [aria-hidden=true]"))
        // Small list thumbnails (under 80px) sit beside the product name; the
        // label is on the product's own card and page.
        .filter((img) => img.getBoundingClientRect().width >= 80 || img.closest("[hidden]"))
        .filter((img) => {
          const frame = img.closest("a, article, figure, div.relative") ?? img.parentElement;
          return !/illustrative/i.test(frame?.textContent ?? "") && !/illustrative/i.test(frame?.parentElement?.textContent ?? "");
        })
        .map((img) => img.getAttribute("src"));
      // The wordmark is nowrap inside a shrinkable flex item, so when it
      // outgrows its box it silently paints over the nav instead of pushing.
      const brand = document.querySelector("header .header-brand");
      const navLink = document.querySelector("header .header-nav a");
      let headerOverlap = 0;
      if (brand && navLink) {
        // The link's box carries line-height padding well above and below the
        // glyphs; measure the text itself so a hairline grazing that padding
        // isn't reported as the logo sitting on the nav.
        const inkRect = (el) => {
          const range = document.createRange();
          range.selectNodeContents(el);
          const r = range.getBoundingClientRect();
          return r.width ? r : el.getBoundingClientRect();
        };
        const n = inkRect(navLink);
        // A real collision needs both axes: the tagline under the wordmark is
        // wider than the wordmark but sits below the nav's line, so comparing
        // right edges alone cries wolf.
        for (const el of [brand, ...brand.querySelectorAll("*")]) {
          const r = el.getBoundingClientRect();
          if (!r.width || !n.width) continue;
          const x = Math.min(r.right, n.right) - Math.max(r.left, n.left);
          const y = Math.min(r.bottom, n.bottom) - Math.max(r.top, n.top);
          if (x > 0 && y > 0) headerOverlap = Math.max(headerOverlap, Math.round(x));
        }
      }
      return { broken, overflow, unlabelled, headerOverlap };
    });
    result.broken.forEach((s) => issues.push(`broken image: ${s}`));
    if (result.overflow > 1) issues.push(`horizontal overflow: ${result.overflow}px`);
    if (result.headerOverlap > 0) issues.push(`logo overlaps the nav by ${result.headerOverlap}px`);
    result.unlabelled.forEach((s) => issues.push(`generated image without label: ${s}`));
    if (screenshotRoutes.has(route)) {
      const file = `${vp.name}${route.replace(/\//g, "_") || "_home"}.png`;
      await page.screenshot({ path: join(SHOTS, file), fullPage: false });
    }
    issues.forEach((i) => problems.push(`[${vp.name}] ${route} ${i}`));
    await page.close();
  }
  await context.close();
}
await browser.close();

console.log(`Checked ${routes.length} pages x ${viewports.length} viewports.`);
if (problems.length) {
  console.log(`${problems.length} problem(s):`);
  problems.forEach((p) => console.log("  " + p));
  process.exit(1);
}
console.log("No problems found.");
