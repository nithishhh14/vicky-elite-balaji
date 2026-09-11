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
  // Address-only query, deliberately without the business name: a name-based
  // Maps search can resolve to an unrelated, similarly-named business near
  // Karamadai. An address-only pin is slightly less precise but never wrong.
  mapEmbedSrc:
    "https://www.google.com/maps?q=12-B+Gandhi+Nagar,+Mettupalayam+Main+Road,+Karamadai,+Coimbatore+641104&output=embed",
  mapLink:
    "https://www.google.com/maps/search/?api=1&query=12-B+Gandhi+Nagar+Mettupalayam+Main+Road+Karamadai+Coimbatore+641104",
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
    { title: "Faster timelines", detail: "Structural project speed without cutting finish quality." },
    { title: "Zero-bubble laying", detail: "Precision tile laying technique with experienced crews." },
    { title: "Specialist workforce", detail: "Hands that know granite, marble, kota and sanitary installs." },
    { title: "Wholesale bundles", detail: "Factory-style material bundles — trade rates on enquiry." },
  ],
} as const;

export function waLink(message: string): string {
  return `https://wa.me/${business.phoneWa}?text=${encodeURIComponent(message)}`;
}

export function telLink(): string {
  return `tel:${business.phoneTel}`;
}

export function productEnquiryMessage(productName: string): string {
  return `Hi Elite Balaji, I'm interested in ${productName}. Please share the current trade rate and availability.`;
}

export const defaultEnquiryMessage = `Hi Elite Balaji, I'd like trade pricing information.`;

export function emailQuoteLink(productName?: string): string {
  const subject = productName ? `Trade rate enquiry — ${productName}` : "Trade rate enquiry";
  const body = productName
    ? `Hi Elite Balaji,\n\nI'm interested in ${productName}. Please share the current trade rate and availability.\n\nThanks.`
    : `Hi Elite Balaji,\n\nI'd like trade pricing information.\n\nThanks.`;
  return `mailto:${business.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
