import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const halls = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/halls" }),
  schema: z.object({
    name: z.string(),
    order: z.number(),
    tagline: z.string(),
    intro: z.string(),
    heroImage: z.string(),
    heroAlt: z.string(),
    hasRealContent: z.boolean(),
    materialColor: z.string(),
    materialTexture: z.enum(["stone", "ceramic", "cement", "porcelain"]),
    applications: z.array(z.string()),
    enquiryNote: z.string(),
  }),
});

// Canonical product record. One shape for every real product across every
// hall (tile or material), so one record powers the catalogue card, search/
// filters, the product detail page, related-product ranking, structured
// data, and any future marketing/agent consumer -- instead of maintaining
// two differently-shaped collections that had to be branched on everywhere
// they were used.
const products = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/products" }),
  schema: z.object({
    kind: z.enum(["tile", "material"]),
    hallId: z.string(),
    name: z.string(),
    brand: z.string().optional(),
    series: z.string().optional(),
    code: z.string().optional(),
    category: z.string().optional(),
    size: z.string().optional(),
    finish: z.string(),
    order: z.number(),
    applications: z.array(z.string()),
    image: z.string(),
    imageAlt: z.string(),
    sourceCatalogue: z.string().optional(),
    note: z.string().optional(),
  }),
});

// Bespoke/made-to-order capabilities (CNC engraving, tile printing, inlay,
// sculptures...). Previously an inline array on each hall's JSON, which
// forced every consumer to flatMap across all halls just to find them. A
// dedicated collection makes each capability directly addressable and
// leaves room for real, verified sub-capabilities later without another
// data migration -- see "capabilities" below, left empty until confirmed.
const services = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/services" }),
  schema: z.object({
    hallId: z.string(),
    name: z.string(),
    category: z.string(),
    description: z.string(),
    capabilities: z.array(z.string()).optional(),
    order: z.number(),
  }),
});

export const collections = { halls, products, services };
