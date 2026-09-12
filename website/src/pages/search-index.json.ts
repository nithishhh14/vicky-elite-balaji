import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { deriveColours, deriveCharacterTags, deriveApplicationTags } from "../lib/facets";

// Build-time search index over the real product dataset only — no invented
// entries. Consumed client-side by /search/. Facet fields (colours,
// character, applicationTags) are derived from the same real fields shown
// on the product page itself, not entered separately — see src/lib/facets.ts.
export const GET: APIRoute = async () => {
  const halls = await getCollection("halls");
  const hallName = (id: string) => halls.find((h) => h.id === id)?.data.name ?? id;

  const tileProducts = (await getCollection("tileProducts")).map((p) => {
    const name = `${p.data.series}${p.data.code ? ` ${p.data.code}` : ""}`;
    return {
      id: p.id,
      url: `/products/${p.id}/`,
      name,
      hall: hallName("tiles"),
      category: p.data.brand,
      finish: p.data.finish,
      size: p.data.size,
      applications: p.data.applications,
      image: p.data.image,
      colours: deriveColours(name, p.data.finish, p.data.imageAlt),
      character: deriveCharacterTags(name, p.data.finish, p.data.imageAlt),
      applicationTags: deriveApplicationTags(p.data.applications),
    };
  });

  const materialProducts = (await getCollection("materialProducts")).map((p) => ({
    id: p.id,
    url: `/products/${p.id}/`,
    name: p.data.name,
    hall: hallName(p.data.hallId),
    category: p.data.category,
    finish: p.data.finish,
    size: "",
    applications: p.data.applications,
    image: p.data.image,
    colours: deriveColours(p.data.name, p.data.finish, p.data.imageAlt),
    character: deriveCharacterTags(p.data.name, p.data.finish, p.data.imageAlt),
    applicationTags: deriveApplicationTags(p.data.applications),
  }));

  const hallEntries = halls.map((h) => ({
    id: h.id,
    url: `/halls/${h.id}/`,
    name: h.data.name,
    hall: h.data.name,
    category: "Hall",
    finish: "",
    size: "",
    applications: h.data.applications,
    image: h.data.heroImage || "",
    colours: [] as string[],
    character: [] as string[],
    applicationTags: deriveApplicationTags(h.data.applications),
  }));

  const items = [...tileProducts, ...materialProducts, ...hallEntries];
  return new Response(JSON.stringify(items), { headers: { "Content-Type": "application/json" } });
};
