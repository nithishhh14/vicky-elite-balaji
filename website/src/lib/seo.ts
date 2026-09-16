// Search-result friendly lengths: Google shows roughly 60 characters of a
// title and 155 of a description. Trim on a word boundary, never mid-word.
export function metaText(text: string, max = 150): string {
  const clean = text.replace(/\s+/g, " ").trim();
  if (clean.length <= max) return clean;
  const cut = clean.slice(0, max - 1);
  return cut.slice(0, Math.max(cut.lastIndexOf(" "), 40)).replace(/[,;:.\s]+$/, "") + "…";
}

// "Name | Elite Balaji" — the brand suffix stays short so the page's own
// words survive truncation in search results.
export function pageTitle(subject: string, max = 65): string {
  const brand = " | Elite Balaji";
  const head = subject.replace(/\s+/g, " ").trim();
  return (head.length + brand.length <= max ? head : metaText(head, max - brand.length)) + brand;
}
