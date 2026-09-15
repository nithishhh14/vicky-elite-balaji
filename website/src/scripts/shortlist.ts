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
  });
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
