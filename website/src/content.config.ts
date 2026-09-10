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

const tileProducts = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/tile-products" }),
  schema: z.object({
    brand: z.string(),
    series: z.string(),
    code: z.string().optional(),
    size: z.string(),
    finish: z.string(),
    order: z.number(),
    applications: z.array(z.string()),
    image: z.string(),
    imageAlt: z.string(),
    sourceCatalogue: z.string(),
    note: z.string().optional(),
  }),
});

export const collections = { halls, tileProducts };
