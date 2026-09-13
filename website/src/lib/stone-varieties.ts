// Reference vocabulary of commonly-traded stone/tile variety names, used
// ONLY as an honest "ask us to source / confirm availability" layer on
// category pages -- never rendered as confirmed in-stock products. Real
// confirmed stock lives exclusively in the `products` content collection.
//
// Ordering within each category is deliberately demand-weighted from real
// market research (Indian/Tamil Nadu granite, marble and tile demand,
// 2026), not alphabetical -- see docs/DECISIONS.md for sources. Tamil
// Nadu-quarried varieties are flagged where research confirms it; this is
// general market fact, not a specific sourcing claim about Elite Balaji.
export interface VarietyRef {
  name: string;
  note?: string;
}

export interface StoneCategory {
  slug: string;
  label: string;
  blurb: string;
  varieties: VarietyRef[];
}

export const stoneCategories: StoneCategory[] = [
  {
    slug: "granite",
    label: "Granite",
    blurb: "Indian and imported granite for counters, flooring, cladding and staircases.",
    varieties: [
      { name: "Black Galaxy" },
      { name: "Absolute Black" },
      { name: "Kashmir White", note: "Tamil Nadu-quarried" },
      { name: "Tan Brown" },
      { name: "River White", note: "Tamil Nadu-quarried" },
      { name: "Imperial Red", note: "Tamil Nadu-quarried" },
      { name: "Steel Grey" },
      { name: "Colonial White" },
      { name: "Alaska White" },
      { name: "P White" },
      { name: "Ivory White" },
      { name: "Vizag Blue" },
      { name: "Coffee Brown" },
      { name: "Kashmir Gold" },
    ],
  },
  {
    slug: "marble",
    label: "Marble",
    blurb: "Indian and imported marble for flooring, feature walls and counters.",
    varieties: [
      { name: "Makrana White" },
      { name: "Statuario-look" },
      { name: "Carrara-look" },
      { name: "Fantasy Brown" },
      { name: "Banswara White" },
      { name: "Katni" },
      { name: "Ambaji White" },
      { name: "Crema Marfil" },
      { name: "Emperador" },
      { name: "Italian marble (various)" },
    ],
  },
  {
    slug: "limestone",
    label: "Limestone",
    blurb: "Kota and Kadappa limestone, our most-stocked natural stone for flooring and platforms.",
    varieties: [
      { name: "Kota Blue" },
      { name: "Kota Brown" },
      { name: "Tandur Limestone" },
      { name: "Black Limestone" },
    ],
  },
  {
    slug: "quartzite",
    label: "Quartzite",
    blurb: "Dense, durable natural stone with a crystalline look, sourced on request.",
    varieties: [
      { name: "Taj Mahal Quartzite" },
      { name: "Super White Quartzite" },
      { name: "White Quartzite" },
      { name: "Grey Quartzite" },
      { name: "Patagonia Quartzite" },
    ],
  },
  {
    slug: "onyx",
    label: "Onyx",
    blurb: "Translucent decorative stone, often backlit, sourced on request.",
    varieties: [
      { name: "White Onyx" },
      { name: "Green Onyx" },
      { name: "Honey Onyx" },
      { name: "Backlit Onyx panels" },
    ],
  },
  {
    slug: "travertine",
    label: "Travertine",
    blurb: "Warm-toned natural stone for flooring and cladding, sourced on request.",
    varieties: [
      { name: "Classic Travertine" },
      { name: "Silver Travertine" },
      { name: "Noce Travertine" },
      { name: "Beige Travertine" },
    ],
  },
  {
    slug: "sandstone",
    label: "Sandstone",
    blurb: "Rajasthan sandstone for exteriors, paving and cladding, sourced on request.",
    varieties: [
      { name: "Dholpur Sandstone" },
      { name: "Jaisalmer Sandstone" },
      { name: "Agra Red Sandstone" },
      { name: "Mint Sandstone" },
    ],
  },
  {
    slug: "slate",
    label: "Slate",
    blurb: "Natural slate for feature walls and flooring, sourced on request.",
    varieties: [
      { name: "Black Slate" },
      { name: "Grey Slate" },
      { name: "Multicolour Slate" },
    ],
  },
];

// Same honest "ask us to source" pattern as stoneCategories above, applied
// to Quartz and Sanitaryware -- added 2026-09-13 after client feedback that
// large parts of the earlier supplied product list weren't reflected
// anywhere on the site outside Natural Stone. Generic industry colour/
// category vocabulary only, never a specific brand-stock claim.
export const quartzCategories: StoneCategory[] = [
  {
    slug: "quartz",
    label: "Engineered Quartz",
    blurb: "Engineered quartz surfaces for counters and heavy-use worktops, sourced on request beyond our 2 confirmed colours.",
    varieties: [
      { name: "Pure White" },
      { name: "Calacatta-look" },
      { name: "Carrara-look" },
      { name: "Concrete Grey" },
      { name: "Black Pearl" },
      { name: "Beige Sahara" },
      { name: "Snow White" },
    ],
  },
];

export const sanitarywareCategories: StoneCategory[] = [
  {
    slug: "wash-basins",
    label: "Wash Basins",
    blurb: "Counter-top, wall-mounted and pedestal basins across standard Indian sanitaryware brands.",
    varieties: [
      { name: "Counter-top basin" },
      { name: "Wall-mounted basin" },
      { name: "Pedestal basin" },
      { name: "Semi-recessed basin" },
    ],
  },
  {
    slug: "wc-flush",
    label: "Water Closets & Flush Tanks",
    blurb: "One-piece and wall-hung EWC with matching flush tanks.",
    varieties: [
      { name: "One-piece EWC" },
      { name: "Wall-hung EWC" },
      { name: "Two-piece flush tank set" },
      { name: "Concealed cistern" },
    ],
  },
  {
    slug: "kitchen-sinks",
    label: "Kitchen Sinks",
    blurb: "Single and double-bowl sinks in stainless steel or granite composite.",
    varieties: [
      { name: "Single-bowl stainless steel" },
      { name: "Double-bowl stainless steel" },
      { name: "Granite composite sink" },
    ],
  },
  {
    slug: "faucets-fittings",
    label: "Faucets & Bath Fittings",
    blurb: "Taps, mixers, health faucets and shower fittings.",
    varieties: [
      { name: "Single-lever basin mixer" },
      { name: "Wall mixer" },
      { name: "Health faucet" },
      { name: "Overhead shower" },
    ],
  },
];

export const tileSizes = [
  "300 x 300mm", "300 x 600mm", "600 x 600mm", "600 x 1200mm",
  "800 x 800mm", "800 x 1600mm", "1200 x 2400mm",
];

export const tileFinishes = [
  "Polished", "Glossy", "Matt", "Satin", "Honed", "Structured", "Lappato", "Anti-skid",
];
