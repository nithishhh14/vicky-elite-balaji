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
      { name: "Kashmir White" },
      { name: "River White", note: "Tamil Nadu-quarried" },
      { name: "Imperial Red", note: "Tamil Nadu-quarried" },
      { name: "Classic Grey" },
      { name: "Viscount White" },
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
      { name: "Banswara White" },
      { name: "Katni" },
      { name: "Ambaji White" },
      { name: "Crema Marfil" },
      { name: "Emperador" },
      { name: "Calacatta Gold" },
      { name: "Nero Marquina" },
      { name: "Botticino" },
      { name: "Italian marble (various)" },
    ],
  },
  {
    slug: "limestone",
    label: "Limestone",
    blurb: "Kota and Kadappa limestone, our most-stocked natural stone for flooring and platforms.",
    varieties: [
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
    blurb: "Engineered quartz surfaces for counters and heavy-use worktops, sourced on request beyond our confirmed colours.",
    varieties: [
      { name: "Pure White" },
      { name: "Calacatta-look" },
      { name: "Carrara-look" },
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
    blurb: "Single and double-bowl sinks in quartz composite, stainless steel or granite composite.",
    varieties: [
      { name: "Quartz sink, single bowl" },
      { name: "Quartz sink, double bowl" },
      { name: "Quartz sink with drainboard" },
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

// Tile types customers search for (industry vocabulary, general explanations
// only). `match` finds real catalogue products of that type; types with no
// match are presented as "ask us to source", never as stocked.
export interface TileType {
  name: string;
  also?: string;
  what: string;
  bestFor: string;
  query: string;
  match: RegExp;
}

export const tileTypes: TileType[] = [
  { name: "Large format", also: "600×1200, 800×1600, slabs", what: "Big tiles with few joints for a seamless, spacious look.", bestFor: "Living rooms, halls, feature walls", query: "600x1200", match: /1200|1600|2400|large format/i },
  { name: "GVT", also: "Glazed vitrified", what: "Vitrified body with a printed glaze, so it can look like marble, stone or wood.", bestFor: "Floors across the home", query: "gvt", match: /\bgvt\b|glazed vitrified/i },
  { name: "PGVT", also: "Polished glazed vitrified", what: "GVT with a high-gloss polished surface, for mirror-like floors.", bestFor: "Living and dining floors", query: "pgvt", match: /\bpgvt\b|polished glazed/i },
  { name: "Double charge", what: "Two layers of pigment pressed into the tile, so the design wears well in busy areas.", bestFor: "Commercial and high-traffic floors", query: "double charge", match: /double charge/i },
  { name: "Ceramic wall tiles", also: "Digital wall", what: "Lighter glazed tiles printed with patterns, for walls rather than floors.", bestFor: "Bathroom and kitchen walls", query: "wall tiles", match: /wall tile|12x18|300 ?x ?450|5213/i },
  { name: "Heritage & patterned", also: "Athangudi, Moroccan", what: "Handmade or patterned tiles that bring colour and craft to a floor.", bestFor: "Verandas, pooja rooms, accent floors", query: "athangudi", match: /athangudi|moroccan|pattern/i },
  { name: "Parking & anti-skid", also: "Outdoor, heavy duty", what: "Textured, thicker tiles with grip for wet and vehicle areas.", bestFor: "Car parking, driveways, portico, wash areas", query: "parking", match: /parking|anti.?skid|heavy duty/i },
  { name: "Elevation tiles", also: "Exterior cladding", what: "Weather-resistant tiles for front walls and building facades.", bestFor: "Front elevation, compound walls", query: "elevation", match: /elevation/i },
  { name: "Wood-look", what: "Plank-shaped tiles with wood grain, without the upkeep of timber.", bestFor: "Bedrooms, balconies, decks", query: "wood", match: /wood/i },
];

export const tileSizes = [
  "300 x 300mm", "300 x 600mm", "600 x 600mm", "600 x 1200mm",
  "800 x 800mm", "800 x 1600mm", "1200 x 2400mm",
];

export const tileFinishes = [
  "Polished", "Glossy", "Matt", "Satin", "Honed", "Structured", "Lappato", "Anti-skid",
];
