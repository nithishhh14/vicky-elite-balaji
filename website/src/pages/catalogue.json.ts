import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { cardData } from "../lib/similarity";

// Compact card data for every real product. Used by My Materials to rebuild
// a shared shortlist link (?ids=...) on another device.
export const GET: APIRoute = async () => {
  const halls = await getCollection("halls");
  const hallName = (id: string) => halls.find((h) => h.id === id)?.data.name ?? id;
  const items = (await getCollection("products")).map((p) => cardData(p, hallName(p.data.hallId)));
  return new Response(JSON.stringify(items), { headers: { "Content-Type": "application/json" } });
};
