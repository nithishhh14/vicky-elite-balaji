// Content integrity: the checks the build itself cannot make.
// Astro's schema validates each record's shape; this validates the links
// *between* records and the files on disk, so an edit (by a person or by
// Vicky) can never publish a dangling reference or a missing photo.
//   node scripts/check-content.mjs
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
const C = (p) => join(ROOT, "src", "content", p);
const PUBLIC = join(ROOT, "public");

const problems = [];
const fail = (where, msg) => problems.push(`${where}: ${msg}`);
const load = (dir) =>
  Object.fromEntries(
    readdirSync(C(dir))
      .filter((f) => f.endsWith(".json"))
      .map((f) => [f.replace(/\.json$/, ""), JSON.parse(readFileSync(join(C(dir), f), "utf8"))])
  );

const halls = load("halls");
const products = load("products");
const guides = load("guides");
const fileExists = (src) => src.startsWith("http") || existsSync(join(PUBLIC, decodeURIComponent(src)));

// ── products ────────────────────────────────────────────────────────────
for (const [id, p] of Object.entries(products)) {
  if (!halls[p.hallId]) fail(id, `hallId "${p.hallId}" is not a hall`);
  for (const src of [p.image, ...(p.images ?? []).map((i) => i.src)]) {
    if (!fileExists(src)) fail(id, `image file missing: ${src}`);
  }
  // /granite/ and the home page's specimen rail build a card's thumbnail by
  // swapping .jpg for -720.jpg. Both select the same set, so a product in it
  // whose image has no -720 sibling renders a broken card — something the
  // schema cannot see, because the path is never written down.
  const onGraniteRails = p.hallId === "granite-marbles" && /granite|sandstone/i.test(p.category ?? "");
  if (onGraniteRails && p.image.endsWith(".jpg")) {
    const thumb = p.image.replace(/\.jpg$/, "-720.jpg");
    if (!fileExists(thumb)) fail(id, `thumbnail missing: ${thumb} (/granite/ and the home rail derive it from image)`);
  }
  // Concept/reference art is scene illustration, never a product photo.
  if (/\/media\/(concepts|reference)\//.test(p.image)) fail(id, `product image points at concept art: ${p.image}`);
  if (!p.imageAlt?.trim()) fail(id, "imageAlt is empty");
  for (const img of p.images ?? []) if (!img.alt?.trim()) fail(id, `gallery image without alt: ${img.src}`);
}

// ── halls ───────────────────────────────────────────────────────────────
for (const [id, h] of Object.entries(halls)) {
  if (h.heroImage && !fileExists(h.heroImage)) fail(id, `heroImage missing: ${h.heroImage}`);
  if (!Object.values(products).some((p) => p.hallId === id)) fail(id, "hall has no products");
}

// ── landing pages ───────────────────────────────────────────────────────
for (const [slug, g] of Object.entries(guides)) {
  if (!slug.endsWith("-coimbatore")) fail(slug, "guide slug must end in -coimbatore");
  try { new RegExp(g.match.pattern, g.match.flags ?? "i"); }
  catch (e) { fail(slug, `match.pattern is not a valid regular expression: ${e.message}`); }
  for (const h of g.match.halls ?? []) if (!halls[h]) fail(slug, `match.halls references unknown hall "${h}"`);
  for (const r of g.related) if (!guides[r]) fail(slug, `related page "${r}" does not exist`);
  if (g.related.includes(slug)) fail(slug, "related links to itself");
}

// ── media library (still a TS module) ───────────────────────────────────
const media = readFileSync(join(ROOT, "src", "lib", "media-library.ts"), "utf8");
for (const m of media.matchAll(/"productId":\s*"([^"]+)"/g)) {
  if (!products[m[1]]) fail("media-library.ts", `productId "${m[1]}" does not exist`);
}
for (const m of media.matchAll(/"(?:src|thumb)":\s*"([^"]+)"/g)) {
  if (!fileExists(m[1])) fail("media-library.ts", `image file missing: ${m[1]}`);
}

console.log(
  `content: ${Object.keys(products).length} products, ${Object.keys(halls).length} halls, ${Object.keys(guides).length} landing pages`
);
if (problems.length) {
  console.log(`\n${problems.length} problem(s):`);
  problems.forEach((p) => console.log("  - " + p));
  process.exit(1);
}
console.log("all references resolve and every image file exists.");
