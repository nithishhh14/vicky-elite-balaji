// Facet derivation: colour / character / application tags are computed
// from fields that are already real and verified (name, finish, imageAlt,
// applications) -- never invented, never entered by hand per-product. This
// is what lets the catalogue stay honestly "empty" for a facet nothing
// supports, and means every future real product is automatically
// filterable the moment its JSON file is added, with no extra tagging step.

const COLOUR_KEYWORDS: Record<string, string[]> = {
  white: ["white"],
  black: ["black"],
  grey: ["grey", "gray"],
  beige: ["beige"],
  brown: ["brown"],
  red: ["red"],
  mustard: ["mustard"],
  green: ["green"],
};

const CHARACTER_KEYWORDS: Record<string, string[]> = {
  polished: ["polish"],
  honed: ["honed"],
  matte: ["matt", "matte"],
  glossy: ["glossy", "gloss"],
  textured: ["textured", "texture", "cleft"],
  patterned: ["pattern", "motif", "floral"],
  veined: ["vein"],
  "large-format": ["large format", "large-format"],
  handcrafted: ["handcraft", "hand-inlaid", "handmade"],
};

const APPLICATION_TAG_KEYWORDS: Record<string, string[]> = {
  kitchen: ["kitchen"],
  bathroom: ["bathroom", "washroom", "powder room"],
  flooring: ["floor"],
  walls: ["wall", "cladding", "backsplash"],
  countertop: ["counter", "worktop"],
  staircase: ["stair", "step"],
  exterior: ["veranda", "courtyard", "driveway", "pathway", "outdoor", "exterior", "godown"],
  commercial: ["commercial", "lobby", "retail"],
};

function deriveFromKeywordMap(text: string, map: Record<string, string[]>): string[] {
  const lower = text.toLowerCase();
  return Object.entries(map)
    .filter(([, keywords]) => keywords.some((k) => lower.includes(k)))
    .map(([tag]) => tag);
}

export function deriveColours(...fields: (string | undefined)[]): string[] {
  return deriveFromKeywordMap(fields.filter(Boolean).join(" "), COLOUR_KEYWORDS);
}

export function deriveCharacterTags(...fields: (string | undefined)[]): string[] {
  return deriveFromKeywordMap(fields.filter(Boolean).join(" "), CHARACTER_KEYWORDS);
}

export function deriveApplicationTags(applications: string[]): string[] {
  return deriveFromKeywordMap(applications.join(" "), APPLICATION_TAG_KEYWORDS);
}
