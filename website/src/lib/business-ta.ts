// Tamil versions of the verified facts in business.ts — translations only.
// If a fact changes there, change it here too; nothing in this file may say
// something the English file doesn't.
import { business } from "./business";

export const businessTa = {
  name: "எலைட் பாலாஜி ஸ்டோன்ஸ் & செராமிக்ஸ்",
  address: "12-B, காந்தி நகர், மேட்டுப்பாளையம் மெயின் ரோடு, காரமடை, கோயம்புத்தூர் மாவட்டம் – 641104",
  sinceLine: `${business.since} முதல் காரமடையில்`,
  // Same order as business.serviceHubs.
  serviceHubs: [
    "கோயம்புத்தூர்",
    "மேட்டுப்பாளையம்",
    "காரமடை",
    "கல்லார்",
    "ஊட்டி",
    "கோத்தகிரி",
    "நீலகிரி",
    "சிறுமுகை",
    "அன்னூர்",
    "பெரியநாயக்கன்பாளையம்",
    "சரவணம்பட்டி",
    "துடியலூர்",
    "ஆர்.எஸ்.புரம்",
  ],
  usps: [
    { title: "விரைவான வேலை", detail: "ஃபினிஷில் சமரசம் இல்லாமல் கட்டுமான வேலைகளை வேகமாக முடிக்கிறோம்." },
    { title: "குமிழ் இல்லாத பதிப்பு", detail: "பின்னாளில் குமிழ் வராமலும் எழும்பாமலும் எங்கள் பணியாளர்கள் டைல் பதிக்கிறார்கள்." },
    { title: "அனுபவமுள்ள பணியாளர்கள்", detail: "கிரானைட், மார்பிள், கோட்டா மற்றும் சானிட்டரி பொருத்துதலில் கைதேர்ந்தவர்கள்." },
    { title: "மொத்த விலை", detail: "மொத்தமாக வாங்கினால் ஃபேக்டரி அளவிலான விலையில் மெட்டீரியல். டிரேடு விலையைக் கேளுங்கள்." },
  ],
} as const;

if (businessTa.serviceHubs.length !== business.serviceHubs.length) {
  throw new Error("business-ta.ts serviceHubs is out of step with business.ts");
}

export function productEnquiryMessageTa(productName: string): string {
  return `வணக்கம் எலைட் பாலாஜி, ${productName} பற்றி தெரிந்துகொள்ள விரும்புகிறேன். தற்போதைய இருப்பும் விலையும் சொல்லுங்கள்.`;
}

// Tamil labels for imageBadge() in image-badge.ts.
export const imageBadgeTa: Record<string, string> = {
  "Illustrative image": "மாதிரிப் படம்",
  "Colour swatch": "நிற மாதிரி",
  "Reference photo": "குறிப்புப் புகைப்படம்",
};
