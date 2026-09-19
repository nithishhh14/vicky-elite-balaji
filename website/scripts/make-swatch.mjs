// Generates a colour swatch for a material we have no photograph of.
//
// A swatch is deliberately NOT a photo: it shows the colour family and grain
// character and nothing else, and `src/lib/image-badge.ts` labels anything
// under /media/swatches/ as "Colour swatch" on every card and product page.
// That keeps the promise in docs/WEBSITE_ARCHITECTURE.md §3 — no image is ever
// allowed to read as a picture of our actual stock.
//
// Replace a swatch with a real photo the moment one exists; the badge then
// disappears on its own because it is derived from the path.
//
//   node scripts/make-swatch.mjs <out.jpg> <baseHex> [grain] [seed]
//
// grain: "fine" (granite-like speckle) | "flat" (tile-like field, default)
import sharp from "sharp";

const [out, base, grain = "flat", seedArg = "1"] = process.argv.slice(2);
if (!out || !base) {
  console.error("usage: node scripts/make-swatch.mjs <out.jpg> <#rrggbb> [fine|flat] [seed]");
  process.exit(1);
}

const W = 1200, H = 900;
const hex = base.replace("#", "");
const br = parseInt(hex.slice(0, 2), 16), bg = parseInt(hex.slice(2, 4), 16), bb = parseInt(hex.slice(4, 6), 16);

// Deterministic PRNG so re-running produces the same swatch.
let seed = Number(seedArg) * 2654435761 % 2147483647;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;

const px = Buffer.alloc(W * H * 3);
for (let i = 0; i < W * H; i++) {
  let d;
  if (grain === "fine") {
    // Most pixels sit near the base; a small share are bright or dark mineral
    // flecks, which is what reads as granite rather than paint.
    const r = rand();
    d = r > 0.985 ? 55 + rand() * 45 : r < 0.02 ? -45 - rand() * 30 : (rand() - 0.5) * 26;
  } else {
    d = (rand() - 0.5) * 10;
  }
  const clamp = (v) => (v < 0 ? 0 : v > 255 ? 255 : v | 0);
  px[i * 3] = clamp(br + d);
  px[i * 3 + 1] = clamp(bg + d);
  px[i * 3 + 2] = clamp(bb + d * 1.1); // let blue drift a touch further
}

const full = sharp(px, { raw: { width: W, height: H, channels: 3 } });
await full.clone().jpeg({ quality: 78, mozjpeg: true }).toFile(out);

// The granite and home pages build their thumbnail path by swapping .jpg for
// -720.jpg, so every product image needs that sibling or the card 404s.
const thumb = out.replace(/\.jpg$/, "-720.jpg");
await full.clone().resize(720).jpeg({ quality: 76, mozjpeg: true }).toFile(thumb);
console.log("wrote", out, "and", thumb);
