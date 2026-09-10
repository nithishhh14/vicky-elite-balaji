"""Scraper Agent engine — Google Maps + Google Search + public IG cards + buyer signals.

Hard rules: Coimbatore hubs only · never invent phones · no Instagram login · phone-first ledger.
"""
from __future__ import annotations

import asyncio
import re
import threading
from typing import Any
from urllib.parse import quote_plus, unquote

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

GEO = {"latitude": 11.0168, "longitude": 76.9558}

ALLOWED_CITY_HINTS = (
    "coimbatore", "ooty", "kotagiri", "nilgiri", "kallar", "mettupalayam", "karamadai",
    "sirumugai", "annur", "velingaadu", "periyanaickenpalayam", "kovilpalayam",
    "saravanampatti", "thudiyalur", "koundampalayam", "rs puram", "ramanathapuram",
    "gandhipuram", "peelamedu", "saibaba colony", "race course", "singanallur",
    "ganapathy", "vadavalli", "town hall",
)
REJECT_CITY_HINTS = (
    "noida", "delhi", "chandigarh", "hyderabad", "gurgaon", "baraut", "ghaziabad",
    "chennai", "bengaluru", "bangalore", "mumbai", "pune", "tirupur", "kumbakonam",
    "kanchipuram", "maduravoyal", "secunderabad", "jeedimetla", "kukatpally",
    "erode", "malappuram", "thrissur", "kozhikode", "calicut", "manjeri",
    "salem", "mysore", "mysuru", "madurai", "ernakulam", "mandya", "trichy",
    "cochin", "kochi", "vizag", "jaipur",
)

TRADE_WORDS = (
    "civil", "contractor", "builder", "construction", "engineer", "architect",
    "mason", "tile laying", "infra", "structural", "interior", "promoter",
    "realty", "housing", "flooring contractor", "marble contractor", "epoxy",
    "developer",
)
# Retail / showroom peers of Elite Balaji — NOT email targets
RETAIL_SHOWROOM_HINTS = (
    "tile store", "tiles store", "granite supplier", "marble supplier",
    "granite dealer", "tile dealer", "showroom", "sanitaryware", "sanitary ware",
    "bathroom fittings", "building materials store", "construction material wholesaler",
    "material wholesaler", "tiles & stones", "tiles and stones", "granites",
    "stone supplier", "ceramic shop", "ceramics shop", "hardware shop",
)
JUNK_WORDS = (
    "electronics", "mobile shop", "computer", "cartridge", "printer", "xerox",
    "copier", "laptop", "phone accessories", "furniture store", "saree",
    "restaurant", "hotel", "salon", "clinic", "hospital", "pharmacy",
    "contact list", "pdf", "scribd", "slideshare", "quora", "reddit",
    "yellow pages", "ancient india", "hackathon", "job vacancy",
) + RETAIL_SHOWROOM_HINTS

MAP_QUERIES = (
    "civil contractors Coimbatore",
    "building contractors Coimbatore",
    "home builders Coimbatore",
    "tile laying contractors Coimbatore",
    "civil contractors Karamadai",
    "builders Mettupalayam",
    "construction company Saravanampatti",
    # Nilgiris — priority hubs for easy customers
    "civil contractors Ooty",
    "building contractors Ooty",
    "builders Kotagiri",
    "civil contractors Nilgiris",
    "home builders Ooty Nilgiris",
)

SEARCH_QUERIES = (
    "civil contractors Coimbatore phone number",
    "building contractors Coimbatore contact",
    "tile laying contractors Coimbatore phone",
    "civil contractors Ooty phone number",
    "builders Kotagiri contact number",
    "civil contractor Nilgiris phone",
)

IG_QUERIES = (
    'site:instagram.com "civil contractor" Coimbatore',
    'site:instagram.com builder Coimbatore construction',
    'site:instagram.com builder Ooty OR Kotagiri',
)

BUYER_QUERIES = (
    "need tiles contractor Coimbatore",
    "looking for granite flooring Coimbatore",
    "civil contractor required Karamadai",
    "builder needed Ooty",
)

# Justdial retired as primary: category noise (electronics etc.). Maps+Search cover phones better.
# Do not re-enable without iron contractor-only filters.

KILL_JS = """
() => {
  const kill = (el) => { try { el.remove(); } catch (e) {} };
  ['.modal','.popup','[role="dialog"]','[aria-modal="true"]',
   '[class*="cookie"]','[class*="consent"]','form[action*="consent"]'
  ].forEach(sel => document.querySelectorAll(sel).forEach(kill));
  document.body.style.overflow = 'auto';
}
"""

MAPS_FEED_JS = """
() => {
  const out = [];
  const seen = new Set();
  const links = Array.from(document.querySelectorAll('a[href*="/maps/place/"]'));
  for (const a of links) {
    let href = a.href || '';
    if (!href.includes('/maps/place/')) continue;
    href = href.split('&')[0];
    const key = href.split('?')[0];
    if (seen.has(key)) continue;
    seen.add(key);
    let name = (a.getAttribute('aria-label') || '').split('\\n')[0].trim();
    if (!name) name = (a.innerText || '').split('\\n')[0].trim();
    if (!name || name.length < 2) continue;
    if (/^(sponsored|ad|results|directions)$/i.test(name)) continue;
    out.push({ name, href });
    if (out.length >= 16) break;
  }
  return out;
}
"""

MAPS_DETAIL_JS = """
() => {
  const clean = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const name = clean(document.querySelector('h1')?.innerText || '');
  let phone = '';

  const phoneNodes = Array.from(document.querySelectorAll(
    'button[data-item-id^="phone:"], a[data-item-id^="phone:"], button[aria-label*="Phone"], a[href^="tel:"]'
  ));
  for (const el of phoneNodes) {
    const id = el.getAttribute('data-item-id') || '';
    const href = el.getAttribute('href') || '';
    const aria = el.getAttribute('aria-label') || '';
    const blob = id + ' ' + href + ' ' + aria + ' ' + (el.innerText || '');
    const m = blob.match(/(?:\\+?91[\\s\\-:]*)?[6-9]\\d{9}/);
    if (m) { phone = m[0]; break; }
    if (id.startsWith('phone:tel:')) { phone = id.replace(/^phone:tel:/i, ''); break; }
  }
  if (!phone) {
    const body = document.body?.innerText || '';
    const m = body.match(/(?:\\+?91[\\s-]*)?[6-9]\\d{9}/);
    if (m) phone = m[0];
  }

  let address = '';
  const addrBtn = document.querySelector('button[data-item-id="address"]');
  if (addrBtn) {
    address = clean((addrBtn.getAttribute('aria-label') || '').replace(/^Address:?\\s*/i, '') || addrBtn.innerText || '');
  }
  if (!address) {
    const copy = document.querySelector('button[data-tooltip*="address" i], button[aria-label*="Address"]');
    if (copy) address = clean((copy.getAttribute('aria-label') || '').replace(/^Address:?\\s*/i, ''));
  }

  let website = '';
  const web = document.querySelector('a[data-item-id="authority"]');
  if (web && web.href) website = web.href;

  let category = '';
  const cat = document.querySelector('button[jsaction*="category"], button[jsaction*="pane.rating.category"]');
  if (cat) category = clean(cat.innerText || '');

  return {
    name,
    phone,
    address,
    website,
    mapsUrl: location.href.split('&')[0],
    category,
  };
}
"""

SEARCH_EXTRACT_JS = """
() => {
  const clean = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const phones = (s) => {
    const m = (s || '').match(/(?:\\+?91[\\s-]*)?[6-9]\\d{9}/g);
    return m ? Array.from(new Set(m.map(x => x.replace(/\\D/g,'').slice(-10)))) : [];
  };
  const out = [];
  const seen = new Set();

  document.querySelectorAll('[data-local-attribute], .VkpGBb, .rllt__details, .cXedhc, .QRY5ie, .uMdZh').forEach((card) => {
    const text = clean(card.innerText || '');
    if (text.length < 10) return;
    const nameEl = card.querySelector('a, .OSrXXb, .qBF1Pd, .dbg0pd');
    const name = clean(nameEl ? nameEl.textContent : text.split('\\n')[0]);
    if (!name || seen.has(name.toLowerCase())) return;
    const href = (nameEl && nameEl.href) ? nameEl.href : location.href;
    seen.add(name.toLowerCase());
    out.push({ name, phone: phones(text)[0] || '', details: text.slice(0, 240), href, kind: 'local' });
  });

  document.querySelectorAll('div.g, .MjjYud, div[data-sokoban-container]').forEach((block) => {
    const h3 = block.querySelector('h3');
    if (!h3) return;
    const a = h3.closest('a') || block.querySelector('a[href^="http"]');
    if (!a) return;
    const name = clean(h3.innerText || '');
    const href = a.href || '';
    const snip = clean((block.querySelector('.VwiC3b, .IsZvec') || {}).innerText || block.innerText || '');
    if (!name || name.length < 3 || seen.has(name.toLowerCase())) return;
    const blob = (name + ' ' + snip + ' ' + href).toLowerCase();
    if (!/(coimbatore|karamadai|mettupalayam|saravanampatti|thudiyalur|ooty|kotagiri|nilgiri|rs\\s*puram|instagram\\.com)/i.test(blob)) return;
    seen.add(name.toLowerCase());
    out.push({ name: name.slice(0, 90), phone: phones(snip + ' ' + name)[0] || '', details: snip.slice(0, 240), href, kind: 'organic' });
  });

  return out.slice(0, 35);
}
"""


def clean(v: Any) -> str:
    if v is None:
        return ""
    t = re.sub(r"\s+", " ", str(v).replace("\xa0", " ").replace("\u200b", "")).strip()
    if t.lower() in {"null", "none", "undefined", "n/a", "na", "-", "empty"}:
        return ""
    return t


def phone_digits(phone: str) -> str:
    d = "".join(ch for ch in (phone or "") if ch.isdigit())
    if len(d) >= 12 and d.startswith("91"):
        d = d[-10:]
    return d[-10:] if len(d) >= 10 else ""


def local_ok(blob: str) -> bool:
    low = (blob or "").lower()
    if any(bad in low for bad in REJECT_CITY_HINTS):
        return False
    return any(good in low for good in ALLOWED_CITY_HINTS)


def trade_ok(blob: str) -> bool:
    low = (blob or "").lower()
    if any(j in low for j in JUNK_WORDS):
        return False
    return any(w in low for w in TRADE_WORDS)


def is_retail_showroom(name: str, category: str = "", details: str = "") -> bool:
    """True for tile/granite shops & showrooms — not contractor email targets."""
    blob = f"{name} {category} {details}".lower()
    if any(h in blob for h in RETAIL_SHOWROOM_HINTS):
        # Keep if clearly a laying/contractor business despite stone words
        if re.search(r"\b(laying|contractor|builders?|construction|civil\s+engineer)\b", blob):
            if not re.search(r"\b(store|supplier|showroom|dealer|wholesaler)\b", blob):
                return False
            # "Tile contractor" ok; "Tile store" not
            if re.search(r"\b(tile|marble|granite)\s+contractor\b", blob) or "laying" in blob:
                return False
        return True
    # Name like "X Granites" / "Y Tiles & Stones" without contractor language
    if re.search(r"\b(granites?|tiles?\s*&\s*stones|tiles?\s+and\s+stones)\b", name, re.I):
        if not re.search(r"\b(contractor|laying|builder|construction|engineer)\b", blob):
            return True
    return False


def is_outreach_target(name: str, category: str = "", details: str = "") -> bool:
    """Client rule: email contractors/engineers/builders — not peer showrooms."""
    if is_retail_showroom(name, category, details):
        return False
    blob = f"{name} {category} {details}".lower()
    return bool(
        re.search(
            r"\b(contractor|builders?|construction|civil|engineer|architect|laying|"
            r"promoter|developer|infra|housing|mason|structural|interior)\b",
            blob,
        )
    )


def is_clean_company_name(name: str) -> bool:
    n = clean(name)
    if not n or len(n) < 3 or len(n) > 100:
        return False
    low = n.lower()
    if any(j in low for j in ("http://", "https://", "www.", "google maps", "directions")):
        return False
    if low.startswith(("results", "sponsored", "nearby", "search", "need a", "looking for", "want", "required")):
        return False
    if n.count("|") >= 1 or " pdf" in low:
        return False
    if any(x in low for x in ("contact list", "companies list", "contractors list", "top 10", "best 10")):
        return False
    return True


def hub_from_text(blob: str) -> str:
    low = (blob or "").lower()
    for hub in (
        "Karamadai", "Mettupalayam", "Saravanampatti", "Thudiyalur", "Koundampalayam",
        "RS Puram", "Ooty", "Kotagiri", "Nilgiris", "Kallar", "Sirumugai", "Annur",
        "Periyanaickenpalayam", "Kovilpalayam", "Ramanathapuram", "Gandhipuram",
        "Peelamedu", "Singanallur", "Ganapathy", "Vadavalli", "Coimbatore",
    ):
        if hub.lower().replace(" ", "") in low.replace(" ", "") or hub.lower() in low:
            return hub
    return "Coimbatore"


def unwrap_google_url(href: str) -> str:
    h = clean(href)
    if not h:
        return ""
    if "/url?" in h and "q=" in h:
        m = re.search(r"[?&]q=([^&]+)", h)
        if m:
            return unquote(m.group(1))
    if "google.com/goto" in h:
        return ""
    return h


def normalize_lead(raw: dict[str, str], *, require_phone: bool = False) -> dict[str, str] | None:
    name = clean(raw.get("name"))
    phone = phone_digits(clean(raw.get("phone")))
    source = clean(raw.get("source")) or "Unknown"
    website = unwrap_google_url(clean(raw.get("website")) or clean(raw.get("mapsUrl")) or "")
    details = clean(raw.get("details") or raw.get("address") or "")
    category = clean(raw.get("category") or "")
    city = clean(raw.get("city")) or hub_from_text(f"{details} {raw.get('address','')} {website} {name}")
    blob = f"{name} {city} {details} {category} {website}"

    if not name or not is_clean_company_name(name):
        return None
    if not website:
        return None
    if require_phone and not phone:
        return None
    if not local_ok(blob) and source != "Instagram":
        # Instagram SERP often has hub only in query; allow if query/details mention hub
        if not local_ok(blob + " coimbatore"):
            return None
    if source == "Instagram":
        if "instagram.com" not in website.lower():
            return None
        if not local_ok(blob + " " + clean(raw.get("query", "")) + " coimbatore"):
            return None
    elif not local_ok(blob):
        return None

    if source in {"Google Maps", "Google Search", "Instagram"} and not (
        trade_ok(blob)
        or any(w in name.lower() for w in ("builder", "construct", "civil", "infra", "homes", "housing", "tile", "granite", "marble"))
        or source == "Instagram" and trade_ok(blob + " " + clean(raw.get("query", "")))
    ):
        if source != "Buyer Signal":
            return None

    if category and any(j in category.lower() for j in JUNK_WORDS):
        return None
    if not is_outreach_target(name, category, details):
        return None

    if source == "Google Search":
        site_l = website.lower()
        if any(x in site_l for x in ("scribd.com", "quora.com", "reddit.com", "facebook.com/login", "/url?")):
            return None
        if re.match(
            r"^(tiles?|civil|building|home)?\s*(flooring\s+)?(contractors?|builders?|engineers?)\b.*\bin\b",
            name,
            re.I,
        ):
            return None

    if source == "Buyer Signal":
        details = ("Buyer/demand signal · " + details).strip(" ·")

    detail_bits = [x for x in (category, details) if x]
    safe_name = re.sub(r"[^\w\s&.'\-()/]", "", name).strip() or name
    return {
        "name": safe_name[:90],
        "phone": phone,
        "city": city if city else "Coimbatore",
        "source": source,
        "website": website[:500],
        "details": " · ".join(detail_bits)[:260],
    }


async def overlays(page: Page) -> None:
    try:
        await page.evaluate(KILL_JS)
    except Exception:
        pass
    try:
        await page.keyboard.press("Escape")
    except Exception:
        pass


async def dismiss_google(page: Page) -> None:
    await overlays(page)
    for label in ("Accept all", "I agree", "Accept", "Reject all", "Stay signed out", "Not now"):
        try:
            btn = page.get_by_role("button", name=re.compile(label, re.I))
            if await btn.count():
                await btn.first.click(timeout=1200)
                await page.wait_for_timeout(400)
        except Exception:
            pass


async def open_browser():
    pw = await async_playwright().start()
    try:
        browser = await pw.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"],
        )
    except Exception:
        browser = await pw.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
    context = await browser.new_context(
        permissions=["geolocation"],
        geolocation=GEO,
        locale="en-IN",
        timezone_id="Asia/Kolkata",
        viewport={"width": 1440, "height": 960},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
    )
    try:
        await context.set_geolocation(GEO)
        for origin in ("https://www.google.com", "https://maps.google.com", "https://www.google.co.in"):
            await context.grant_permissions(["geolocation"], origin=origin)
    except Exception:
        pass
    return pw, browser, context


async def scroll_maps_feed(page: Page, times: int = 5) -> None:
    for _ in range(times):
        try:
            await page.evaluate(
                """() => {
                  const feed = document.querySelector('div[role="feed"]');
                  if (feed) feed.scrollBy(0, 1100);
                  else window.scrollBy(0, 1100);
                }"""
            )
        except Exception:
            await page.mouse.wheel(0, 1100)
        await page.wait_for_timeout(850)


async def reveal_maps_phone(page: Page) -> None:
    try:
        btn = page.locator('button[data-item-id^="phone:"], button[aria-label*="Phone"]').first
        if await btn.count():
            await btn.click(timeout=2000)
            await page.wait_for_timeout(900)
    except Exception:
        pass


async def scrape_maps_query(page: Page, query: str, max_places: int = 8) -> list[dict[str, str]]:
    # Bias map center: Nilgiris queries → Ooty; else Coimbatore
    qlow = query.lower()
    if any(x in qlow for x in ("ooty", "kotagiri", "nilgiri")):
        lat, lng, zoom = 11.4102, 76.6950, 12
    else:
        lat, lng, zoom = GEO["latitude"], GEO["longitude"], 13
    url = (
        "https://www.google.com/maps/search/"
        + quote_plus(query)
        + f"/@{lat},{lng},{zoom}z?hl=en"
    )
    await page.goto(url, wait_until="domcontentloaded", timeout=75000)
    await page.wait_for_timeout(4000)
    await dismiss_google(page)
    await scroll_maps_feed(page, 5)
    cards = await page.evaluate(MAPS_FEED_JS) or []
    leads: list[dict[str, str]] = []
    seen: set[str] = set()

    for card in cards[:max_places]:
        href = clean(card.get("href"))
        if not href or href in seen:
            continue
        seen.add(href)
        try:
            await page.goto(href, wait_until="domcontentloaded", timeout=50000)
            await page.wait_for_timeout(2600)
            await dismiss_google(page)
            await reveal_maps_phone(page)
            detail = await page.evaluate(MAPS_DETAIL_JS) or {}
            if not clean(detail.get("name")):
                detail["name"] = clean(card.get("name"))
            maps_url = clean(detail.get("mapsUrl")) or href
            biz_web = clean(detail.get("website"))
            addr = clean(detail.get("address")) or f"Google Maps listing · {query}"
            details = addr
            if biz_web and "google." not in biz_web.lower():
                details = f"{addr} · Site: {biz_web}"
            raw = {
                "name": detail.get("name"),
                "phone": detail.get("phone"),
                "address": addr,
                "details": details,
                "category": detail.get("category"),
                "website": maps_url,
                "mapsUrl": maps_url,
                "source": "Google Maps",
                "city": hub_from_text(f"{addr} {detail.get('name','')} {query}"),
            }
            # Client-grade: prefer phone; still keep Maps rows with solid address if phone locked
            parsed = normalize_lead(raw, require_phone=False)
            if parsed and (parsed.get("phone") or len(parsed.get("details") or "") > 20):
                leads.append(parsed)
        except Exception:
            continue
    return leads


async def scrape_google_search(page: Page, query: str, source: str = "Google Search") -> list[dict[str, str]]:
    url = f"https://www.google.com/search?q={quote_plus(query)}&hl=en&gl=in&pws=0&num=15"
    await page.goto(url, wait_until="domcontentloaded", timeout=65000)
    await page.wait_for_timeout(3000)
    await dismiss_google(page)
    for _ in range(2):
        await page.mouse.wheel(0, 1400)
        await page.wait_for_timeout(500)
    raw_items = await page.evaluate(SEARCH_EXTRACT_JS) or []
    leads: list[dict[str, str]] = []
    for item in raw_items:
        href = unwrap_google_url(clean(item.get("href"))) or url
        item_source = source
        if "instagram.com" in href.lower():
            item_source = "Instagram"
        raw = {
            "name": item.get("name"),
            "phone": item.get("phone"),
            "details": item.get("details"),
            "website": href,
            "source": item_source,
            "city": hub_from_text(f"{item.get('details','')} {item.get('name','')} {query}"),
            "query": query,
        }
        require_phone = item_source == "Google Search"
        if item_source == "Instagram":
            require_phone = False
            # Keep IG handle/title as name; details from SERP snippet
            if not raw.get("details"):
                raw["details"] = f"Public Instagram profile card · {query}"
        if source == "Buyer Signal":
            raw["source"] = "Buyer Signal"
            require_phone = False
        parsed = normalize_lead(raw, require_phone=require_phone)
        if parsed:
            leads.append(parsed)
    return leads


def dedupe_leads(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_phone: dict[str, dict[str, str]] = {}
    by_name: dict[str, dict[str, str]] = {}

    def better(a: dict[str, str], b: dict[str, str]) -> dict[str, str]:
        if phone_digits(b.get("phone") or "") and not phone_digits(a.get("phone") or ""):
            return b
        if len(b.get("details") or "") > len(a.get("details") or ""):
            merged = dict(a)
            merged["details"] = b["details"]
            if b.get("website") and "/maps/" in (b.get("website") or ""):
                merged["website"] = b["website"]
            if phone_digits(b.get("phone") or ""):
                merged["phone"] = phone_digits(b.get("phone") or "")
            return merged
        return a

    for row in rows:
        phone = phone_digits(row.get("phone") or "")
        name = clean(row.get("name")).lower()
        if not name:
            continue
        if phone:
            by_phone[phone] = better(by_phone[phone], row) if phone in by_phone else row
        else:
            if any(clean(v.get("name")).lower() == name for v in by_phone.values()):
                continue
            by_name[name] = better(by_name[name], row) if name in by_name else row

    phone_rows = sorted(by_phone.values(), key=lambda r: clean(r.get("name")).lower())
    # Keep limited no-phone Maps/IG only
    name_rows = [
        r for r in by_name.values()
        if r.get("source") in {"Google Maps", "Instagram", "Buyer Signal"}
    ]
    name_rows = sorted(name_rows, key=lambda r: clean(r.get("name")).lower())
    return phone_rows + name_rows


async def harvest(
    max_map_queries: int = 10,
    max_search_queries: int = 5,
    max_ig_queries: int = 2,
    max_buyer_queries: int = 2,
) -> tuple[list[dict[str, str]], str]:
    pw = None
    browser: Browser | None = None
    context: BrowserContext | None = None
    bag: list[dict[str, str]] = []
    notes: list[str] = []
    try:
        pw, browser, context = await open_browser()
        page = await context.new_page()

        for q in MAP_QUERIES[:max_map_queries]:
            try:
                got = await scrape_maps_query(page, q, max_places=8)
                bag.extend(got)
                notes.append(f"Maps[{q.split()[0]}…]:{len(got)}/{sum(1 for x in got if x.get('phone'))}ph")
            except Exception as exc:
                notes.append(f"Maps fail:{exc}")

        for q in SEARCH_QUERIES[:max_search_queries]:
            try:
                got = await scrape_google_search(page, q, source="Google Search")
                bag.extend(got)
                notes.append(f"Search:{len(got)}/{sum(1 for x in got if x.get('phone'))}ph")
            except Exception as exc:
                notes.append(f"Search fail:{exc}")

        for q in IG_QUERIES[:max_ig_queries]:
            try:
                got = await scrape_google_search(page, q, source="Google Search")
                ig = [x for x in got if x.get("source") == "Instagram"]
                bag.extend(ig)
                notes.append(f"IG-cards:{len(ig)}")
            except Exception as exc:
                notes.append(f"IG fail:{exc}")

        for q in BUYER_QUERIES[:max_buyer_queries]:
            try:
                got = await scrape_google_search(page, q, source="Buyer Signal")
                bag.extend(got)
                notes.append(f"Buyer:{len(got)}")
            except Exception as exc:
                notes.append(f"Buyer fail:{exc}")
    finally:
        if context is not None:
            await context.close()
        if browser is not None:
            await browser.close()
        if pw is not None:
            await pw.stop()

    final = dedupe_leads(bag)
    # Client demo bar: at least keep all with phone; cap weak no-phone
    with_phone = [r for r in final if r.get("phone")]
    without = [r for r in final if not r.get("phone")][:8]
    final = with_phone + without
    notes.append(f"TOTAL:{len(final)} phones:{len(with_phone)}")
    return final, " | ".join(notes)


def run_harvest() -> tuple[list[dict[str, str]], str]:
    holder: dict[str, Any] = {"leads": [], "notes": "", "error": None}

    def worker() -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            leads, notes = loop.run_until_complete(harvest())
            holder["leads"] = leads
            holder["notes"] = notes
        except Exception as exc:
            holder["error"] = exc
        finally:
            loop.close()

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    thread.join()
    if holder["error"] is not None:
        raise holder["error"]
    return list(holder["leads"] or []), str(holder["notes"] or "")
