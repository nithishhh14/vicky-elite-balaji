import type { APIRoute } from "astro";

// Generated from the configured site URL (astro.config.mjs / SITE_URL), so the
// sitemap line can never point at a stale domain.
export const GET: APIRoute = ({ site }) => {
  const sitemap = new URL("/sitemap-index.xml", site).toString();
  return new Response(`User-agent: *
Allow: /

Sitemap: ${sitemap}
`, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
