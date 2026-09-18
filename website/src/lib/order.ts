// One ordering rule for every catalogue listing: the curated `order` first,
// then the name. Records may share an `order` (or omit it entirely) without
// the listing shuffling between builds — so adding a product never means
// hunting for a free number or renumbering its neighbours.
export function byOrder(
  a: { data: { order: number; name: string } },
  b: { data: { order: number; name: string } }
): number {
  return a.data.order - b.data.order || a.data.name.localeCompare(b.data.name);
}
