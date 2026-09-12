// Single source of truth for how the real halls group into "material
// worlds" for navigation and discovery. SiteHeader, the homepage, and the
// material-world landing pages all read this instead of each hardcoding
// their own grouping -- add a hall here once and every surface picks it up.
export const materialWorlds = [
  {
    slug: "natural-stone",
    label: "Natural Stone",
    hallIds: ["granite-marbles", "kota-stone", "kadappa"],
  },
  {
    slug: "tiles-ceramics",
    label: "Tiles & Ceramics",
    hallIds: ["tiles"],
  },
  {
    slug: "surfaces",
    label: "Surfaces",
    hallIds: ["quartz"],
  },
] as const;

// Real stock that isn't a "material" in the discovery sense (fittings,
// accessories) -- still real halls, just not part of a material world.
export const alsoStockedHallIds = ["sanitaryware", "adhesive"] as const;

export const standaloneHallIds = ["laying-works"] as const;
