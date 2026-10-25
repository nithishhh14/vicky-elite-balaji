// Pixel size of an image in /public, read from its header at build time.
//
// Used where a layout lets images take their natural height (the gallery's
// masonry columns). Without width/height the browser can't reserve the
// space, so the page jumps as each image arrives. Reads only the header
// bytes of JPEG, PNG and WebP; anything else returns undefined and the
// image simply renders without the hint, as before.
import { closeSync, openSync, readSync } from "node:fs";
import { join } from "node:path";

const PUBLIC = join(process.cwd(), "public");
const cache = new Map<string, { width: number; height: number } | undefined>();

export function imageDims(src: string): { width: number; height: number } | undefined {
  if (cache.has(src)) return cache.get(src);
  let dims: { width: number; height: number } | undefined;
  try {
    const fd = openSync(join(PUBLIC, decodeURIComponent(src)), "r");
    const buf = Buffer.alloc(256 * 1024);
    const n = readSync(fd, buf, 0, buf.length, 0);
    closeSync(fd);
    dims = parse(buf.subarray(0, n));
  } catch {
    dims = undefined;
  }
  cache.set(src, dims);
  return dims;
}

function parse(b: Buffer): { width: number; height: number } | undefined {
  // PNG: IHDR is always the first chunk.
  if (b.length > 24 && b.readUInt32BE(0) === 0x89504e47) {
    return { width: b.readUInt32BE(16), height: b.readUInt32BE(20) };
  }
  // WebP: lossy (VP8 ), lossless (VP8L) or extended (VP8X).
  if (b.length > 30 && b.toString("ascii", 0, 4) === "RIFF" && b.toString("ascii", 8, 12) === "WEBP") {
    const kind = b.toString("ascii", 12, 16);
    if (kind === "VP8 ") return { width: b.readUInt16LE(26) & 0x3fff, height: b.readUInt16LE(28) & 0x3fff };
    if (kind === "VP8L") {
      const bits = b.readUInt32LE(21);
      return { width: (bits & 0x3fff) + 1, height: ((bits >> 14) & 0x3fff) + 1 };
    }
    if (kind === "VP8X") return { width: b.readUIntLE(24, 3) + 1, height: b.readUIntLE(27, 3) + 1 };
  }
  // JPEG: walk the segments to the first start-of-frame marker.
  if (b[0] === 0xff && b[1] === 0xd8) {
    let i = 2;
    while (i + 9 < b.length) {
      if (b[i] !== 0xff) { i++; continue; }
      const marker = b[i + 1];
      if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
        return { height: b.readUInt16BE(i + 5), width: b.readUInt16BE(i + 7) };
      }
      i += 2 + b.readUInt16BE(i + 2);
    }
  }
  return undefined;
}
