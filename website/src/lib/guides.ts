import { getCollection, type CollectionEntry } from "astro:content";

// Landing-page data now lives in src/content/guides/*.json (one file per
// page, schema-validated). This module only loads and orders it, and turns
// the stored pattern into a RegExp at build time.
export type Guide = CollectionEntry<"guides">;

export async function loadGuides(): Promise<Guide[]> {
  const guides = await getCollection("guides");
  return guides.sort((a, b) => a.data.h1.localeCompare(b.data.h1));
}

export function guideMatcher(guide: Guide): RegExp {
  return new RegExp(guide.data.match.pattern, guide.data.match.flags);
}
