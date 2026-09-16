// Serve dist/ with the production headers from public/_headers, so the
// Content-Security-Policy can be verified locally before deploying.
//   node scripts/serve-headers.mjs [port]
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { join, extname } from "node:path";

const PORT = Number(process.argv[2] ?? 4323);
const DIST = new URL("../dist/", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
const HEADERS_FILE = new URL("../public/_headers", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");

const rules = [];
for (const line of (await readFile(HEADERS_FILE, "utf8")).split(/\r?\n/)) {
  if (!line.trim() || line.trim().startsWith("#")) continue;
  if (!line.startsWith(" ")) rules.push({ pattern: line.trim(), headers: [] });
  else if (rules.length) {
    const i = line.indexOf(":");
    rules.at(-1).headers.push([line.slice(0, i).trim(), line.slice(i + 1).trim()]);
  }
}
const matches = (pattern, path) =>
  pattern.endsWith("/*") ? path.startsWith(pattern.slice(0, -1)) : pattern.startsWith("/*.") ? path.endsWith(pattern.slice(2)) : pattern === path;

const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".webp": "image/webp", ".xml": "application/xml", ".txt": "text/plain", ".woff2": "font/woff2", ".mp4": "video/mp4" };

createServer(async (req, res) => {
  const path = decodeURIComponent(new URL(req.url, "http://x").pathname);
  const candidates = [join(DIST, path), join(DIST, path, "index.html"), join(DIST, path + ".html"), join(DIST, "404.html")];
  for (const [i, file] of candidates.entries()) {
    try {
      if (!(await stat(file)).isFile()) continue;
      const body = await readFile(file);
      for (const rule of rules) if (matches(rule.pattern, path)) for (const [k, v] of rule.headers) res.setHeader(k, v);
      res.writeHead(i === 3 ? 404 : 200, { "Content-Type": TYPES[extname(file)] ?? "application/octet-stream" });
      return res.end(body);
    } catch {}
  }
  res.writeHead(404).end("not found");
}).listen(PORT, () => console.log(`dist served with production headers on http://localhost:${PORT}`));
