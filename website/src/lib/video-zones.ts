// Cinematic video zones. Every zone is empty on purpose: no approved footage
// exists yet, and stock or generated "installation footage" is not used
// (docs/DECISIONS.md). When the client supplies a real, approved clip, drop
// the files into public/media/video/ and fill in the zone. The pages already
// render <AmbientVideo> for a filled zone, so no other code changes are needed.
//
// Recommended encodes: 1920px H.264 MP4 (+ optional WebM), 6–12 s loop,
// no audio track, under ~4 MB; a lighter 720px MP4 as mobileSrc if the clip
// should play on phones at all (otherwise phones show the poster).
export interface VideoZone {
  src: string;
  webm?: string;
  mobileSrc?: string;
  poster: string;
  label: string; // provenance caption, e.g. "Our Karamadai yard, 2026"
}

export const videoZones: Record<"hero" | "granite" | "custom" | "showroom", VideoZone | null> = {
  hero: null,
  granite: null,
  custom: null,
  showroom: null,
};
