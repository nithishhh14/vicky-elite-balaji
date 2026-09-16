// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

import react from "@astrojs/react";

export default defineConfig({
  // One place to set the live domain. Set SITE_URL in the host's build
  // environment (Cloudflare Pages ▸ Settings ▸ Environment variables), or
  // replace the fallback below once the real domain is registered.
  // robots.txt and the sitemap are both generated from this value.
  site: process.env.SITE_URL ?? "https://elitebalaji.example.in",
  integrations: [sitemap(), react()],
  vite: {
    plugins: [tailwindcss()],
  },
});