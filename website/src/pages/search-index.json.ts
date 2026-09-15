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

  const products = (await getCollection("products")).map((p) => ({
    id: p.id,
    url: `/products/${p.id}/`,
    name: p.data.name,
    hall: hallName(p.data.hallId),
    category: p.data.brand ?? p.data.category ?? "",
    finish: p.data.finish,
    size: p.data.size ?? "",
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

  // Real made-to-order capabilities (services collection) and the two
  // editorial category pages, so "engraved stone" or "name plate" finds them.
  const serviceEntries = (await getCollection("services")).map((s) => ({
    id: `service-${s.id}`,
    url: "/custom/",
    name: s.data.name,
    hall: "Custom Stonecraft",
    category: "Made to order",
    finish: "",
    size: "",
    applications: [s.data.description],
    image: "/media/client/stonecraft/engraved-rose-granite-720.jpg",
    colours: [] as string[],
    character: ["handcrafted"],
    applicationTags: deriveApplicationTags([s.data.description]),
  }));

  const pageEntries = [
    {
      id: "page-custom-stonecraft",
      url: "/custom/",
      name: "Custom Stonecraft",
      hall: "Custom Stonecraft",
      category: "Our work",
      finish: "Engraved, polished",
      size: "",
      applications: ["Engraved name plates and welcome signs", "Tulsi madams and pooja units", "Granite dining tables, outdoor table sets and garden benches", "Temple and decorative stone work", "CNC engraving"],
      image: "/media/client/stonecraft/tulsi-madam-engraved-black-720.jpg",
      colours: ["black", "grey", "red", "white"],
      character: ["handcrafted"],
      applicationTags: ["exterior"],
    },
    {
      id: "page-granite",
      url: "/granite/",
      name: "Granite slabs",
      hall: "Granite & Marbles",
      category: "Natural granite slab",
      finish: "Polished, leathered, honed, flamed",
      size: "",
      applications: ["Kitchen countertops", "Islands", "Staircases", "Flooring", "Wall cladding", "Vanity tops", "Window sills", "Commercial surfaces"],
      image: "/media/client/granite/black-galaxy-slabs-720.jpg",
      colours: ["black", "brown", "grey"],
      character: ["polished"],
      applicationTags: ["kitchen", "countertop", "staircase", "flooring", "walls", "commercial"],
    },
  ];

  const items = [...products, ...hallEntries, ...serviceEntries, ...pageEntries];
  return new Response(JSON.stringify(items), { headers: { "Content-Type": "application/json" } });
};
