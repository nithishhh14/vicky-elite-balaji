import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { byOrder } from "../lib/order";

// Static structural export of the 8 showroom halls, for any future tooling
// (Marketing/SEO agents, etc.) that needs to read the site's own content
// model without scraping HTML. No live query engine — this is a static
// build artifact, same as sitemap.xml, since the site has no backend.
export const GET: APIRoute = async () => {
  const halls = (await getCollection("halls")).sort(byOrder);

  const payload = {
    business: "Elite Balaji Stones & Ceramics",
    generatedAt: new Date().toISOString(),
    halls: halls.map((hall) => ({
      id: hall.id,
      path: `/halls/${hall.id}/`,
      name: hall.data.name,
      order: hall.data.order,
      tagline: hall.data.tagline,
      intro: hall.data.intro,
      applications: hall.data.applications,
      hasRealPhotography: hall.data.hasRealContent,
      enquiryNote: hall.data.enquiryNote,
    })),
  };

  return new Response(JSON.stringify(payload, null, 2), {
    headers: { "Content-Type": "application/json" },
  });
};
