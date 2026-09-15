// "My Materials": a no-login shortlist kept in localStorage.
// Any element with [data-save] (JSON in data-save) becomes a save toggle;
// [data-shortlist-count] shows the live count. Pages listen for
// "shortlist:change" to re-render.

export interface SavedItem {
  id: string;
  name: string;
  url: string;
  image: string;
  hall: string;
  category: string;
  brand: string;
  finish: string;
  size: string;
  applications: string[];
  thickness: string;
}

const KEY = "eb-my-materials";
const MAX = 24;

export function readShortlist(): SavedItem[] {
  try {
    const raw = localStorage.getItem(KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

function write(list: SavedItem[]) {
  try {
    localStorage.setItem(KEY, JSON.stringify(list.slice(0, MAX)));
  } catch {
    /* storage blocked (private mode): the page still works, just not saved */
  }
  document.dispatchEvent(new CustomEvent("shortlist:change", { detail: list }));
}

export const isSaved = (id: string) => readShortlist().some((i) => i.id === id);

export function toggleSaved(item: SavedItem): boolean {
  const list = readShortlist();
  const exists = list.some((i) => i.id === item.id);
  write(exists ? list.filter((i) => i.id !== item.id) : [item, ...list]);
  return !exists;
}

export function removeSaved(id: string) {
  write(readShortlist().filter((i) => i.id !== id));
}

export function replaceShortlist(items: SavedItem[]) {
  write(items);
}

let lastCount = -1;
function syncButtons() {
  const ids = new Set(readShortlist().map((i) => i.id));
  document.querySelectorAll<HTMLElement>("[data-save]").forEach((btn) => {
    const id = btn.dataset.saveId ?? "";
    const on = ids.has(id);
    btn.setAttribute("aria-pressed", String(on));
    const label = btn.querySelector("[data-save-label]");
    if (label) label.textContent = on ? (btn.dataset.savedText ?? "Saved") : (btn.dataset.saveText ?? "Save");
  });
  const count = ids.size;
  document.querySelectorAll<HTMLElement>("[data-shortlist-count]").forEach((el) => {
    el.textContent = String(count);
    el.hidden = count === 0;
    if (lastCount >= 0 && count > lastCount) {
      el.classList.remove("count-bump");
      void el.offsetWidth;
      el.classList.add("count-bump");
    }
  });
  lastCount = count;
}

const reduceMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Saved: the material's own photo travels to the My Materials bookmark in
// the header, which then acknowledges it. Small, quick, no confetti.
function flyToShortlist(btn: HTMLElement) {
  if (reduceMotion()) return;
  const target = document.querySelector<HTMLElement>("[data-shortlist-target]");
  const card = btn.parentElement?.closest("article, li, figure, .group");
  const source = card?.querySelector<HTMLImageElement>("img") ?? document.getElementById("product-main-image") as HTMLImageElement | null;
  if (!target || !source || !source.complete) return;
  const from = source.getBoundingClientRect();
  const to = target.getBoundingClientRect();
  if (!from.width || from.bottom < 0 || from.top > innerHeight) return;
  const size = Math.min(from.width, from.height, 140);
  const ghost = source.cloneNode() as HTMLImageElement;
  ghost.removeAttribute("id");
  ghost.alt = "";
  Object.assign(ghost.style, {
    position: "fixed",
    left: `${from.left + from.width / 2 - size / 2}px`,
    top: `${from.top + from.height / 2 - size / 2}px`,
    width: `${size}px`,
    height: `${size}px`,
    objectFit: "cover",
    zIndex: "70",
    pointerEvents: "none",
    boxShadow: "0 18px 40px -12px rgba(0,0,0,.5)",
    border: "1px solid rgba(163,130,47,.7)",
  });
  document.body.appendChild(ghost);
  const dx = to.left + to.width / 2 - (from.left + from.width / 2);
  const dy = to.top + to.height / 2 - (from.top + from.height / 2);
  ghost
    .animate(
      [
        { transform: "translate(0,0) scale(1)", opacity: 1 },
        { transform: `translate(${dx * 0.55}px, ${dy * 0.55 - 40}px) scale(0.55)`, opacity: 0.95, offset: 0.55 },
        { transform: `translate(${dx}px, ${dy}px) scale(0.12)`, opacity: 0.2 },
      ],
      { duration: 720, easing: "cubic-bezier(0.22, 0.61, 0.36, 1)" }
    )
    .finished.finally(() => ghost.remove());
}

let toastTimer: number | undefined;
function toast(message: string) {
  let el = document.getElementById("shortlist-toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "shortlist-toast";
    el.setAttribute("role", "status");
    el.className =
      "fixed bottom-24 left-1/2 z-50 -translate-x-1/2 border border-brass/60 bg-charcoal-deep px-5 py-3 text-xs uppercase tracking-[0.16em] text-paper shadow-lift transition-opacity duration-300";
    document.body.appendChild(el);
  }
  el.innerHTML = message;
  el.style.opacity = "1";
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    if (el) el.style.opacity = "0";
  }, 2600);
}

document.addEventListener("click", (e) => {
  const btn = (e.target as HTMLElement).closest<HTMLElement>("[data-save]");
  if (!btn) return;
  e.preventDefault();
  try {
    const item = JSON.parse(btn.dataset.save ?? "{}") as SavedItem;
    const nowSaved = toggleSaved(item);
    if (nowSaved) {
      flyToShortlist(btn);
      btn.classList.remove("just-saved");
      void btn.offsetWidth;
      btn.classList.add("just-saved");
      window.setTimeout(() => btn.classList.remove("just-saved"), 600);
    }
    toast(nowSaved ? `Saved to <a href="/shortlist/" class="underline decoration-brass underline-offset-4">My Materials</a>` : "Removed from My Materials");
  } catch {
    /* malformed data attribute: ignore */
  }
});

document.addEventListener("shortlist:change", syncButtons);
window.addEventListener("storage", (e) => {
  if (e.key === KEY) syncButtons();
});
syncButtons();
