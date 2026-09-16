// Final pre-deploy check. One command, exits non-zero if anything fails:
//   npm run preflight
//
// 1. typecheck + build
// 2. serves dist/ with the production security headers
// 3. Playwright: every page x 2 viewports, then the interaction pass
// 4. content/SEO checks over the built HTML (below)
import { spawn, spawnSync } from "node:child_process";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
const DIST = join(ROOT, "dist");
const PORT = 4399;
const results = [];
const ok = (name, pass, detail = "") => {
  results.push({ name, pass, detail });
  console.log(`${pass ? "PASS" : "FAIL"}  ${name}${detail ? " — " + detail : ""}`);
};
const run = (cmd, args, label) => {
  const r = spawnSync(cmd, args, { cwd: ROOT, shell: true, encoding: "utf8" });
  const out = (r.stdout ?? "") + (r.stderr ?? "");
  ok(label, r.status === 0, out.trim().split("\n").slice(-1)[0]);
  return out;
};

// 1 — typecheck + build
run("npx", ["astro", "check"], "astro check (0 type errors)");
run("npx", ["astro", "build"], "production build");

// 4 — content and SEO checks over dist/
const htmlFiles = (function walk(dir) {
  return readdirSync(dir).flatMap((n) => {
    const full = join(dir, n);
    return statSync(full).isDirectory() ? walk(full) : n.endsWith(".html") ? [full] : [];
  });
})(DIST);
const pageUrl = (f) => "/" + relative(DIST, f).split(sep).join("/").replace(/index\.html$/, "").replace(/\.html$/, "/");
const site = readFileSync(join(ROOT, "astro.config.mjs"), "utf8").match(/site:\s*"([^"]+)"/)?.[1] ?? "";

ok("pages built", htmlFiles.length > 50, `${htmlFiles.length} pages`);
ok("real domain configured (no placeholder)", !!site && !/example\./.test(site), site || "site missing");

const robots = readFileSync(join(DIST, "robots.txt"), "utf8");
ok("robots.txt sitemap matches the site domain", site ? robots.includes(new URL("/sitemap-index.xml", site).toString()) : false, robots.split("\n").at(-1));

let sitemapUrls = 0;
try {
  const index = readFileSync(join(DIST, "sitemap-index.xml"), "utf8");
  for (const m of index.matchAll(/<loc>([^<]+)<\/loc>/g)) {
    const file = join(DIST, new URL(m[1]).pathname);
    sitemapUrls += [...readFileSync(file, "utf8").matchAll(/<loc>/g)].length;
  }
} catch {}
ok("sitemap lists every page", sitemapUrls >= htmlFiles.length - 2, `${sitemapUrls} urls / ${htmlFiles.length} pages`);

const decode = (s) => s.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n))).replace(/&amp;/g, "&").replace(/&apos;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&nbsp;/g, " ").replace(/&hellip;/g, "…");
const problems = { title: [], desc: [], canonical: [], og: [], h1: [], placeholder: [], price: [], lang: [] };
const PRICE = /\bM\.?R\.?P\.?\b|₹|\bRs\.?\s?\d|\bINR\s?\d/i;
const PLACEHOLDER = /lorem ipsum|example\.(in|com)|TODO|FIXME|\bTBD\b|xxx-xxx/i;
for (const f of htmlFiles) {
  const html = readFileSync(f, "utf8");
  const u = pageUrl(f);
  const text = html.replace(/<script[\s\S]*?<\/script>/g, " ").replace(/<[^>]+>/g, " ");
  const title = decode(html.match(/<title>([^<]*)<\/title>/)?.[1] ?? "");
  const desc = decode(html.match(/<meta name="description" content="([^"]*)"/)?.[1] ?? "");
  if (title.length < 10 || title.length > 65) problems.title.push(`${u} (${title.length})`);
  if (desc.length < 50 || desc.length > 160) problems.desc.push(`${u} (${desc.length})`);
  if (!html.includes('rel="canonical"')) problems.canonical.push(u);
  if (!html.includes('property="og:image"')) problems.og.push(u);
  if (!/<h1[\s>]/.test(html)) problems.h1.push(u);
  if (!/<html lang="/.test(html)) problems.lang.push(u);
  if (PLACEHOLDER.test(text)) problems.placeholder.push(u);
  if (PRICE.test(text)) problems.price.push(u);
}
const show = (list) => list.slice(0, 5).join(", ") + (list.length > 5 ? ` +${list.length - 5}` : "");
ok("every page has a title (10-65 chars)", !problems.title.length, show(problems.title));
ok("every page has a meta description (50-160 chars)", !problems.desc.length, show(problems.desc));
ok("every page has a canonical URL", !problems.canonical.length, show(problems.canonical));
ok("every page has an OG image", !problems.og.length, show(problems.og));
ok("every page has an H1", !problems.h1.length, show(problems.h1));
ok("every page declares a language", !problems.lang.length, show(problems.lang));
ok("no placeholder text or example domain in content", !problems.placeholder.length, show(problems.placeholder));
ok("no prices published", !problems.price.length, show(problems.price));

const home = readFileSync(join(DIST, "index.html"), "utf8");
let ld = [];
for (const m of home.matchAll(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)) {
  try { ld.push(JSON.parse(m[1])); } catch { ld.push(null); }
}
ok("homepage structured data parses", ld.length > 0 && ld.every(Boolean), `${ld.length} blocks`);
ok("local business schema present", ld.some((b) => b && /Business|LocalBusiness|Store/.test(b["@type"] ?? "")), "");

// 2 + 3 — serve with production headers, then the browser passes
const server = spawn("node", ["scripts/serve-headers.mjs", String(PORT)], { cwd: ROOT, shell: true, stdio: "ignore" });
await new Promise((r) => setTimeout(r, 2500));
try {
  const res = await fetch(`http://127.0.0.1:${PORT}/`);
  const csp = res.headers.get("content-security-policy") ?? "";
  ok("security headers served", csp.includes("default-src 'self'") && !!res.headers.get("strict-transport-security"), csp.slice(0, 40) + "…");
  const qa = run("node", ["scripts/qa.mjs", `http://127.0.0.1:${PORT}`], "playwright: all pages, 2 viewports, CSP on");
  const exp = run("node", ["scripts/experience.mjs", `http://127.0.0.1:${PORT}`, "preflight"], "playwright: interaction pass");
  const errs = [...exp.matchAll(/errors=(\d+)/g)].reduce((n, m) => n + Number(m[1]), 0);
  ok("no console errors during interactions", errs === 0, `${errs} errors`);
  void qa;
} finally {
  server.kill();
}

const failed = results.filter((r) => !r.pass);
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
if (failed.length) {
  console.log("Blocking:\n" + failed.map((f) => "  - " + f.name).join("\n"));
  process.exit(1);
}
console.log("Ready to deploy.");
