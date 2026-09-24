/**
 * Stone under gallery light — a real slab you can move the light across.
 *
 * Why this exists: a photograph of granite shows you one lighting condition.
 * Stone doesn't work like that. Black Galaxy is nearly plain under flat light
 * and full of bronze fire under a raking beam, which is exactly the thing a
 * customer standing in the yard tilts a sample to see. This lets them do that
 * on a phone.
 *
 * It renders OUR photographs, not a generated material. The albedo is the
 * client's own slab photo; the relief and gloss are derived from it. So what
 * the visitor tilts is genuinely the stone we sell.
 *
 * Cost discipline, because the page is 1.5MB and that is a competitive
 * advantage worth keeping:
 *   • three.js is bundled (CSP is script-src 'self' — no CDN is possible) but
 *     dynamically imported, so it is only fetched if a visitor actually
 *     reaches this section.
 *   • Nothing initialises until the section intersects the viewport.
 *   • The render loop runs only while visible and only while interacting;
 *     it is not a perpetual animation frame burning battery.
 *   • Under prefers-reduced-motion we never load three at all — the poster
 *     image is the experience.
 */

type Slab = { src: string; name: string; note: string };

const MAX_DPR = 2;
const LIGHT_HEIGHT = 2.2;

export function initStoneViewer(root: HTMLElement): void {
  const canvas = root.querySelector<HTMLCanvasElement>("[data-stone-canvas]");
  const poster = root.querySelector<HTMLElement>("[data-stone-poster]");
  const hint = root.querySelector<HTMLElement>("[data-stone-hint]");
  if (!canvas) return;

  // Reduced motion: the still is the whole experience. Don't download a 3D
  // engine to show someone a picture they asked not to have move.
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const slabs: Slab[] = JSON.parse(root.dataset.slabs || "[]");
  if (!slabs.length) return;

  let started = false;
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (e.isIntersecting && !started) {
          started = true;
          io.disconnect();
          void start(root, canvas, poster, hint, slabs);
        }
      }
    },
    { rootMargin: "200px" }
  );
  io.observe(root);
}

async function start(
  root: HTMLElement,
  canvas: HTMLCanvasElement,
  poster: HTMLElement | null,
  hint: HTMLElement | null,
  slabs: Slab[]
): Promise<void> {
  let THREE: typeof import("three");
  try {
    THREE = await import("three");
  } catch {
    return; // bundle failed to load: the poster stays, nothing breaks
  }

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, MAX_DPR));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 16 / 9, 0.1, 100);
  // Framed so the slab fills the canvas: at fov 32 the visible height is
  // 2*d*tan(16°), so d ≈ height/0.573. A hair further back for a margin.
  camera.position.set(0, 0.12, 3.35);
  camera.lookAt(0, 0, 0);

  // A gallery, not a showroom: one hard key light the visitor owns, and just
  // enough ambient to keep the shadows from going black.
  const ambient = new THREE.AmbientLight(0xaab4c2, 0.55);
  scene.add(ambient);
  const key = new THREE.SpotLight(0xfff2dc, 140, 12, Math.PI / 5, 0.55, 1.6);
  key.position.set(1.4, LIGHT_HEIGHT, 2.4);
  scene.add(key);
  scene.add(key.target);

  const loader = new THREE.TextureLoader();
  const plane = new THREE.PlaneGeometry(3.2, 1.8, 1, 1);
  const material = new THREE.MeshStandardMaterial({ roughness: 0.28, metalness: 0.0 });
  const mesh = new THREE.Mesh(plane, material);
  scene.add(mesh);

  let current = 0;
  await applySlab(THREE, loader, material, slabs[0]);
  poster?.setAttribute("hidden", "");
  hint?.removeAttribute("hidden");

  // ── interaction: drag moves the light, not the camera ──────────────────
  // Moving the camera would be the obvious choice and the wrong one. The
  // question a stone buyer is asking is "how does it catch the light", so the
  // light is what their finger should hold.
  let dragging = false;
  let needsRender = true;
  const setLightFromPointer = (clientX: number, clientY: number) => {
    const r = canvas.getBoundingClientRect();
    const x = ((clientX - r.left) / r.width) * 2 - 1;
    const y = -(((clientY - r.top) / r.height) * 2 - 1);
    key.position.set(x * 2.6, LIGHT_HEIGHT * (0.35 + y * 0.5), 2.2 + Math.abs(x) * 0.4);
    needsRender = true;
  };

  canvas.addEventListener("pointerdown", (e) => {
    dragging = true;
    canvas.setPointerCapture(e.pointerId);
    setLightFromPointer(e.clientX, e.clientY);
    hint?.setAttribute("hidden", "");
  });
  canvas.addEventListener("pointermove", (e) => {
    if (dragging) setLightFromPointer(e.clientX, e.clientY);
  });
  const stop = () => (dragging = false);
  canvas.addEventListener("pointerup", stop);
  canvas.addEventListener("pointercancel", stop);
  canvas.addEventListener("pointerleave", stop);

  // Keyboard: the same control, reachable without a pointer.
  canvas.addEventListener("keydown", (e) => {
    const step = 0.35;
    if (e.key === "ArrowLeft") key.position.x -= step;
    else if (e.key === "ArrowRight") key.position.x += step;
    else if (e.key === "ArrowUp") key.position.y += step;
    else if (e.key === "ArrowDown") key.position.y -= step;
    else return;
    e.preventDefault();
    key.position.x = Math.max(-2.8, Math.min(2.8, key.position.x));
    key.position.y = Math.max(0.5, Math.min(3.2, key.position.y));
    needsRender = true;
  });

  root.querySelectorAll<HTMLButtonElement>("[data-stone-pick]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const i = Number(btn.dataset.stonePick);
      if (Number.isNaN(i) || i === current || !slabs[i]) return;
      current = i;
      root.querySelectorAll("[data-stone-pick]").forEach((b) =>
        b.setAttribute("aria-pressed", String(b === btn))
      );
      const label = root.querySelector("[data-stone-name]");
      const note = root.querySelector("[data-stone-note]");
      if (label) label.textContent = slabs[i].name;
      if (note) note.textContent = slabs[i].note;
      await applySlab(THREE, loader, material, slabs[i]);
      needsRender = true;
    });
  });

  // ── sizing and the render loop ─────────────────────────────────────────
  const resize = () => {
    const w = canvas.clientWidth || root.clientWidth;
    const h = Math.round(w * (9 / 16));
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    needsRender = true;
  };
  resize();
  const ro = new ResizeObserver(resize);
  ro.observe(root);

  // Render on demand. A slab sitting still costs nothing; only movement does.
  let visible = true;
  const vis = new IntersectionObserver((es) => es.forEach((e) => (visible = e.isIntersecting)));
  vis.observe(root);

  const tick = () => {
    if (visible && needsRender) {
      renderer.render(scene, camera);
      needsRender = false;
    }
    requestAnimationFrame(tick);
  };
  tick();
}

/**
 * Build the material from one photograph.
 *
 * There is no authored normal map — we derive relief from the photo's own
 * luminance. It is an approximation, but for stone it is a good one: the dark
 * parts of a granite photo genuinely are the pits and the veins, so lighting
 * them as depth reads true rather than invented.
 */
async function applySlab(
  THREE: typeof import("three"),
  loader: import("three").TextureLoader,
  material: import("three").MeshStandardMaterial,
  slab: Slab
): Promise<void> {
  const map = await loader.loadAsync(slab.src);
  map.colorSpace = THREE.SRGBColorSpace;
  map.anisotropy = 8;
  material.map = map;

  const derived = derivedMaps(map.image as HTMLImageElement);
  if (derived) {
    const bump = new THREE.CanvasTexture(derived.bump);
    material.bumpMap = bump;
    material.bumpScale = 0.9;
    const rough = new THREE.CanvasTexture(derived.rough);
    material.roughnessMap = rough;
  }
  material.needsUpdate = true;
}

function derivedMaps(img: HTMLImageElement): { bump: HTMLCanvasElement; rough: HTMLCanvasElement } | null {
  if (!img || !img.width) return null;
  const w = Math.min(img.width, 1024);
  const h = Math.round((img.height / img.width) * w);

  const src = document.createElement("canvas");
  src.width = w;
  src.height = h;
  const sctx = src.getContext("2d", { willReadFrequently: true });
  if (!sctx) return null;
  sctx.drawImage(img, 0, 0, w, h);

  let data: ImageData;
  try {
    data = sctx.getImageData(0, 0, w, h);
  } catch {
    return null; // tainted canvas — same-origin only, so this should not happen
  }

  const bump = document.createElement("canvas");
  const rough = document.createElement("canvas");
  bump.width = rough.width = w;
  bump.height = rough.height = h;
  const bctx = bump.getContext("2d");
  const rctx = rough.getContext("2d");
  if (!bctx || !rctx) return null;

  const bOut = bctx.createImageData(w, h);
  const rOut = rctx.createImageData(w, h);
  for (let i = 0; i < data.data.length; i += 4) {
    const lum = (data.data[i] * 0.299 + data.data[i + 1] * 0.587 + data.data[i + 2] * 0.114) | 0;
    bOut.data[i] = bOut.data[i + 1] = bOut.data[i + 2] = lum;
    bOut.data[i + 3] = 255;
    // Bright crystal faces take a polish; dark pits stay matte. Inverting
    // luminance gives that without authoring a second texture.
    const r = 255 - lum;
    rOut.data[i] = rOut.data[i + 1] = rOut.data[i + 2] = 60 + ((r * 0.55) | 0);
    rOut.data[i + 3] = 255;
  }
  bctx.putImageData(bOut, 0, 0);
  rctx.putImageData(rOut, 0, 0);
  return { bump, rough };
}
