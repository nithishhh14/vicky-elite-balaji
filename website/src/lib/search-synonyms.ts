// Query understanding for /search/. Pure functions, no network, no AI.
//
// 1. Multi-word phrases are collapsed to one canonical token first
//    ("anti skid" -> "anti-skid", "wall hung" -> "wall-hung").
// 2. Each remaining term expands to alternatives; an item matches a term if
//    ANY alternative appears in its text. Every term must match (AND).
//
// Tamil / Tanglish: add entries to TERM_SYNONYMS below as the business
// confirms the words customers actually type (e.g. "tharai" = floor). The
// structure needs no code change.

const PHRASES: [RegExp, string][] = [
  [/\banti[\s-]?skid\b/g, "anti-skid"],
  [/\bwall[\s-]?hung\b/g, "wall-hung"],
  [/\bwall[\s-]?mounted\b/g, "wall-hung"],
  [/\btable[\s-]?top\b/g, "countertop"],
  [/\bcounter[\s-]?top\b/g, "countertop"],
  [/\bkitchen slab\b/g, "countertop"],
  [/\blarge[\s-]?format\b/g, "large-format"],
  [/\bsingle[\s-]?piece\b/g, "one-piece"],
  [/\bone[\s-]?piece\b/g, "one-piece"],
  [/\bhealth faucet\b/g, "health-faucet"],
  [/\bmarble[\s-]?look\b/g, "marble"],
  [/\bstone[\s-]?look\b/g, "stone"],
  // Sizes: feet/inch shorthand -> millimetres. Order matters (longest first).
  [/\b(2\s?x\s?4|24\s?x\s?48)\b/g, "600x1200"],
  [/\b(4\s?x\s?2)\b/g, "600x1200"],
  [/\b(2\s?x\s?2|24\s?x\s?24)\b/g, "600x600"],
  [/\b(1\s?x\s?2|12\s?x\s?24)\b/g, "300x600"],
  [/\b(1\s?x\s?1|12\s?x\s?12)\b/g, "300x300"],
  [/\b(12\s?x\s?18)\b/g, "300x450"],
  [/\b(8\s?x\s?4|4\s?x\s?8)\b/g, "1200x2400"],
  [/\b(2\s?x\s?1\.?5|800\s?x\s?800)\b/g, "800x800"],
  [/(\d{3,4})\s?(?:x|\*|×|by)\s?(\d{3,4})\s?(?:mm)?/g, "$1x$2"],
];

const TERM_SYNONYMS: Record<string, string[]> = {
  tile: ["tile", "vitrified", "ceramic", "gvt", "pgvt", "porcelain"],
  tiles: ["tile", "vitrified", "ceramic", "gvt", "pgvt", "porcelain"],
  vitrified: ["vitrified", "gvt", "pgvt", "tile"],
  granite: ["granite"],
  marble: ["marble", "statuario", "carrara", "calacatta", "veined"],
  quartz: ["quartz", "engineered"],
  kota: ["kota"],
  kadappa: ["kadappa", "cuddapah"],
  toilet: ["wc", "ewc", "closet", "toilet"],
  commode: ["wc", "ewc", "closet", "toilet"],
  wc: ["wc", "ewc", "closet", "toilet"],
  basin: ["basin", "wash basin", "sink"],
  washbasin: ["basin", "wash basin"],
  sink: ["sink", "basin"],
  tap: ["tap", "faucet", "mixer", "fitting"],
  faucet: ["faucet", "tap", "mixer", "fitting"],
  bathroom: ["bathroom", "washroom", "bath", "toilet", "sanitary"],
  bath: ["bathroom", "washroom", "bath", "sanitary"],
  toilets: ["bathroom", "washroom", "toilet"],
  kitchen: ["kitchen", "countertop", "counter", "platform"],
  countertop: ["countertop", "counter", "worktop", "platform", "vanity"],
  floor: ["floor", "flooring"],
  flooring: ["floor", "flooring"],
  wall: ["wall", "cladding", "backsplash"],
  outdoor: ["outdoor", "exterior", "pathway", "driveway", "courtyard", "parking", "veranda"],
  exterior: ["outdoor", "exterior", "pathway", "driveway", "courtyard", "elevation", "facade"],
  elevation: ["elevation", "facade", "exterior", "cladding"],
  parking: ["parking", "driveway"],
  stairs: ["stair", "step"],
  staircase: ["stair", "step"],
  villa: ["floor", "flooring", "living"],
  living: ["living", "floor", "flooring"],
  "anti-skid": ["anti-skid", "anti skid", "matt", "outdoor", "parking"],
  matte: ["matt", "matte"],
  matt: ["matt", "matte"],
  glossy: ["gloss", "glossy", "polished"],
  shiny: ["gloss", "glossy", "polished"],
  black: ["black"],
  white: ["white"],
  grey: ["grey", "gray"],
  gray: ["grey", "gray"],
  gold: ["gold", "brown", "beige", "galaxy"],
  engraved: ["engrav", "cnc", "carv", "name board", "sculpture"],
  engraving: ["engrav", "cnc", "carv", "name board", "sculpture"],
  nameplate: ["name board", "engrav"],
  "wall-hung": ["wall-hung", "wall hung", "wall-mounted", "wall mounted"],
  "large-format": ["large format", "large-format", "1200", "1600", "2400", "slab"],
  // Tamil / Tanglish: seeded conservatively; extend as confirmed.
  tharai: ["floor", "flooring"],
  kal: ["stone", "granite", "kota", "kadappa"],
};

const STOPWORDS = new Set(["for", "the", "a", "an", "and", "in", "of", "with", "my", "to", "type", "design", "designs", "best", "near", "me"]);

export function expandQuery(raw: string): string[][] {
  let q = raw.toLowerCase().trim();
  for (const [re, rep] of PHRASES) q = q.replace(re, rep);
  return q
    .split(/\s+/)
    .map((t) => t.replace(/[^\p{L}\p{N}x.-]/gu, ""))
    .filter((t) => t && !STOPWORDS.has(t))
    .map((t) => {
      const base = TERM_SYNONYMS[t] ?? TERM_SYNONYMS[t.replace(/s$/, "")];
      const alts = new Set<string>([t, ...(base ?? [])]);
      // "600x1200" should also match "600 x 1200" and "600 × 1200" in data.
      const size = t.match(/^(\d{3,4})x(\d{3,4})$/);
      if (size) {
        alts.add(`${size[1]} x ${size[2]}`);
        alts.add(`${size[1]}×${size[2]}`);
        alts.add(`${size[1]} × ${size[2]}`);
      }
      return [...alts];
    });
}

export function matchesQuery(haystack: string, groups: string[][]): boolean {
  const h = haystack.toLowerCase();
  return groups.every((alts) => alts.some((a) => h.includes(a)));
}
