// Single source of truth for verified business facts.
// Every figure here must trace back to .cursorrules / the business card — never invent.

export const business = {
  name: "Elite Balaji Stones & Ceramics",
  since: 2012,
  tagline: "Complete Flooring Solution",
  subTagline: "Build Better Spaces",
  contactPerson: "Vignesh Yadav A",
  phoneDisplay: "+91 91590 56767",
  phoneTel: "+919159056767",
  phoneWa: "919159056767",
  email: "elitebalajistonesandceramics@gmail.com",
  address: "12-B, Gandhi Nagar, Mettupalayam Main Road, Karamadai, Coimbatore (Dist - 641104)",
  // The verified Google Business listing, checked 2026-10-25: Maps resolves
  // "Elite Balaji Stones and Ceramics" to 12-B, Mettupalayam Main Rd, Gandhi
  // Nagar, Karamadai 641104 at these coordinates. (Before the listing existed,
  // a name search could land on a similarly-named business, so the old embed
  // searched the address instead — which showed a wide map full of other
  // shops with no clear pin.)
  geo: { lat: 11.269576, lng: 76.9504572 },
  // Close-in map pinned on the listing itself. The listing's full address is
  // needed in the query: with only "name, Karamadai" the embed showed the
  // street but no pin (checked in the browser 2026-10-25).
  mapEmbedSrc:
    "https://www.google.com/maps?q=Elite+Balaji+Stones+and+Ceramics,+12-B,+Mettupalayam+Main+Rd,+Gandhi+Nagar,+Karamadai,+Tamil+Nadu+641104&z=17&output=embed",
  // "Directions": opens turn-by-turn straight to the showroom pin.
  mapLink: "https://www.google.com/maps/dir/?api=1&destination=11.269576,76.9504572",
  // The Google listing itself (reviews, hours, photos).
  mapListing: "https://maps.google.com/?cid=14503407691811989555",
  serviceHubs: [
    "Coimbatore",
    "Mettupalayam",
    "Karamadai",
    "Kallar",
    "Ooty",
    "Kotagiri",
    "Nilgiris",
    "Sirumugai",
    "Annur",
    "Periyanaickenpalayam",
    "Saravanampatti",
    "Thudiyalur",
    "RS Puram",
  ],
  partnerBrands: ["Kajaria", "Somany", "Johnson", "Orientbell", "Simpolo", "Varmora", "AGL", "Parryware", "Jaquar"],
  usps: [
    { title: "Faster timelines", detail: "We move fast on structural work without cutting corners on finish." },
    { title: "Zero-bubble laying", detail: "Our crews lay tile so it doesn't bubble or lift later." },
    { title: "Specialist workforce", detail: "Hands that know granite, marble, kota and sanitary installs." },
    { title: "Wholesale bundles", detail: "Buy material in bulk at factory-style rates. Ask for the trade price." },
  ],
} as const;

export function waLink(message: string): string {
  return `https://wa.me/${business.phoneWa}?text=${encodeURIComponent(message)}`;
}

export function telLink(): string {
  return `tel:${business.phoneTel}`;
}

export function productEnquiryMessage(productName: string, category?: string): string {
  const what = category ? `${productName} (${category})` : productName;
  return `Hi Elite Balaji, I would like to enquire about ${what}. Please share current availability and price.`;
}

export const defaultEnquiryMessage = `Hi Elite Balaji, I'd like trade pricing information.`;

export function emailQuoteLink(productName?: string): string {
  const subject = productName ? `Trade rate enquiry: ${productName}` : "Trade rate enquiry";
  const body = productName
    ? `Hi Elite Balaji,\n\nI'm interested in ${productName}. Please share the current trade rate and availability.\n\nThanks.`
    : `Hi Elite Balaji,\n\nI'd like trade pricing information.\n\nThanks.`;
  return `mailto:${business.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
