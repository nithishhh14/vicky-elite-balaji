// What a product image actually is, when it is not Elite Balaji's own or a
// supplier's catalogue photo. Every card and product page shows this badge so
// generated or stock imagery is never read as our stock.
export function imageBadge(src: string): string | null {
  if (src.startsWith("/media/illustrative/")) return "Illustrative image";
  if (src.startsWith("/media/swatches/")) return "Colour swatch";
  if (/unsplash|pexels/.test(src)) return "Reference photo";
  return null;
}
