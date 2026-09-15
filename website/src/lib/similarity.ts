// "Find similar": related materials grouped by WHY they are related, computed
// only from real catalogue fields (via lib/facets). Makes a small catalogue
// explorable without inventing anything.
import type { CollectionEntry } from "astro:content";
import { deriveColours, deriveCharacterTags, deriveApplicationTags } from "./facets";

type Product = CollectionEntry<"products">;

export interface Profile {
  colours: Set<string>;
  looks: Set<string>;
  applications: Set<string>;
  family: string;
  size: string;
  brand: string;
}

// Material family: the thing a customer would call it, not the hall id.
export function materialFamily(p: Product): string {
  const text = `${p.data.name} ${p.data.category ?? ""}`.toLowerCase();
  if (text.includes("granite")) return "granite";
  if (text.includes("marble")) return "marble";
  if (text.includes("quartz")) return "quartz";
  if (text.includes("kota")) return "kota";
  if (text.includes("kadappa")) return "kadappa";
  if (p.data.hallId === "sanitaryware") return "sanitaryware";
  if (p.data.hallId === "adhesive") return "adhesive";
  if (p.data.hallId === "laying-works") return "service";
  return p.data.kind === "tile" ? "tile" : p.data.hallId;
}

const normSize = (s?: string) => (s ?? "").toLowerCase().replace(/\s|mm/g, "").replace("×", "x");

export function profile(p: Product): Profile {
  return {
    colours: new Set(deriveColours(p.data.name, p.data.finish, p.data.imageAlt)),
    looks: new Set([
      ...deriveCharacterTags(p.data.name, p.data.finish, p.data.imageAlt),
      ...(/(marble|statuario|carrara|veined)/i.test(`${p.data.name} ${p.data.imageAlt}`) ? ["marble-look"] : []),
    ]),
    applications: new Set(deriveApplicationTags(p.data.applications)),
    family: materialFamily(p),
    size: normSize(p.data.size),
    brand: p.data.brand ?? "",
  };
}

const overlap = (a: Set<string>, b: Set<string>) => [...a].filter((x) => b.has(x)).length;

export interface SimilarGroup {
  key: string;
  title: string;
  reason: string;
  items: Product[];
}

export function similarGroups(product: Product, all: Product[], perGroup = 4): SimilarGroup[] {
  const me = profile(product);
  const others = all.filter((p) => p.id !== product.id).map((p) => ({ p, pr: profile(p) }));
  const used = new Set<string>();
  const pick = (scored: { p: Product; s: number }[]) => {
    const out: Product[] = [];
    for (const { p, s } of scored.sort((a, b) => b.s - a.s)) {
      if (s <= 0 || used.has(p.id)) continue;
      out.push(p);
      used.add(p.id);
      if (out.length === perGroup) break;
    }
    return out;
  };

  const groups: SimilarGroup[] = [
    {
      key: "material",
      title: `More ${me.family === "tile" ? "tiles" : me.family}`,
      reason: "Same material family",
      items: pick(others.filter((o) => o.pr.family === me.family).map((o) => ({ p: o.p, s: 1 + overlap(o.pr.colours, me.colours) + overlap(o.pr.looks, me.looks) }))),
    },
    {
      key: "look",
      title: "Similar look",
      reason: [...me.looks].slice(0, 2).join(" · ") || "Similar character",
      items: pick(others.map((o) => ({ p: o.p, s: overlap(o.pr.looks, me.looks) * 2 + overlap(o.pr.colours, me.colours) }))),
    },
    {
      key: "colour",
      title: "Similar colour",
      reason: [...me.colours].join(" · ") || "Similar tones",
      items: pick(others.map((o) => ({ p: o.p, s: overlap(o.pr.colours, me.colours) * 2 }))),
    },
    {
      key: "use",
      title: me.size ? "Same size or use" : "Suits the same spaces",
      reason: me.size ? `${product.data.size} · ${[...me.applications].slice(0, 2).join(" · ")}` : [...me.applications].slice(0, 3).join(" · "),
      items: pick(others.map((o) => ({ p: o.p, s: (me.size && o.pr.size === me.size ? 3 : 0) + overlap(o.pr.applications, me.applications) }))),
    },
  ];
  return groups.filter((g) => g.items.length > 0);
}

// Serializable card data for client-side features (shortlist, compare).
export function cardData(p: Product, hallName: string) {
  return {
    id: p.id,
    name: p.data.name,
    url: `/products/${p.id}/`,
    image: p.data.image,
    hall: hallName,
    category: p.data.category ?? "",
    brand: p.data.brand ?? "",
    finish: p.data.finish,
    size: p.data.size ?? "",
    applications: p.data.applications,
    thickness: p.data.thickness ?? "",
  };
}
