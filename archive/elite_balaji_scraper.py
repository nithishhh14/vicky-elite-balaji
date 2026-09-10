from __future__ import annotations

import asyncio
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import gspread
from playwright.async_api import BrowserContext, Page, async_playwright

BASE_DIR = Path(__file__).resolve().parent
MEMORY_PATH = BASE_DIR / "showroom_memory.json"
CHROME_PROFILE_DIR = BASE_DIR / "chrome_profile"
CREDS_PATH = BASE_DIR / "google_creds.json"
SHEET_ID = "10-5n2epVeVhn9_ecRGd9xHpvmHkJ5qdwlGoHdMumwKg"
JUSTDIAL_URL = "https://www.justdial.com/Coimbatore/Civil-Engineers/nct-10109455"
OLX_URL = "https://www.olx.in/coimbatore_g4059255/q-construction-services"
GEO = {"latitude": 11.0168, "longitude": 76.9558, "accuracy": 80}
BLOCK = ("noida", "delhi", "chandigarh", "hyderabad", "gurgaon")
OFFICE = "+91 91590 56767"
PITCH = (
    "Hi {name}, noticed your construction profiles in the region. "
    "Elite Balaji Stones and Ceramics has been trusted since 2012. "
    "We specialize in end-to-end 'Laying with Materials' bundles, using our "
    "highly experienced workforce and a unique zero-bubble precision tile laying technique. "
    f"For wholesale factory bundles and square-foot estimates, contact Karamadai Main Road at {OFFICE}."
)
KILL_JS = """
() => {
  const kill = (el) => { try { el.remove(); } catch (e) {} };
  ['[class*="login"]','[id*="login"]','[class*="modal"]','[id*="modal"]',
   '[class*="popup"]','[id*="popup"]','[class*="overlay"]','[id*="overlay"]',
   '[class*="backdrop"]','[role="dialog"]','[class*="otp"]','iframe[src*="login"]'
  ].forEach(sel => document.querySelectorAll(sel).forEach(kill));
  document.querySelectorAll('body > div').forEach((el) => {
    const s = window.getComputedStyle(el);
    const z = parseInt(s.zIndex || '0', 10);
    if ((s.position === 'fixed' || s.position === 'absolute') && z >= 1000 && el.offsetHeight > window.innerHeight * 0.4) {
      el.style.setProperty('display','none','important');
    }
  });
  document.body.style.overflow = 'auto';
  return true;
}
"""


def clean(v: Any) -> str:
    if v is None:
        return ""
    t = re.sub(r"\s+", " ", str(v).replace("\xa0", " ")).strip()
    return "" if t.lower() in {"null", "none", "undefined", "n/a", "na", "-", "wishlist", "search not found"} else t


def blocked(title: str) -> bool:
    low = title.lower()
    return any(w in low for w in BLOCK)


def pitch_for(name: str) -> str:
    n = clean(name) or "there"
    return PITCH.format(name=n)


def load_memory() -> dict[str, Any]:
    if not MEMORY_PATH.exists():
        return {"business_profile": {}, "leads_database": []}
    with MEMORY_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data.get("leads_database"), list):
        data["leads_database"] = []
    return data


def save_memory(memory: dict[str, Any]) -> None:
    tmp = MEMORY_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(MEMORY_PATH)


def append_local(leads: list[dict[str, Any]]) -> None:
    memory = load_memory()
    db = memory["leads_database"]
    seen = {
        (clean(r.get("business_name")).lower(), clean(r.get("phone_number")))
        for r in db if isinstance(r, dict)
    }
    for lead in leads:
        name = clean(lead.get("business_name"))
        phone = clean(lead.get("phone_number"))
        if not name or blocked(name) or blocked(clean(lead.get("listing_title"))):
            continue
        key = (name.lower(), phone)
        if key in seen:
            continue
        rec = {
            "business_name": name,
            "phone_number": phone,
            "source": clean(lead.get("source")),
            "search_query": clean(lead.get("search_query")),
            "listing_title": clean(lead.get("listing_title")),
            "whatsapp_pitch": pitch_for(name),
            "email_copy": clean(lead.get("email_copy")),
            "sourced_at": datetime.now(timezone.utc).isoformat(),
            "sourced_by": "Vicky",
        }
        if not rec["listing_title"]:
            rec.pop("listing_title", None)
        db.append(rec)
        seen.add(key)
    save_memory(memory)


def open_sheet():
    if not CREDS_PATH.exists():
        print("[Vicky] google_creds.json missing")
        return None
    try:
        gc = gspread.service_account(filename=str(CREDS_PATH))
        sh = gc.open_by_key(SHEET_ID)
    except Exception as exc:
        print("[Vicky] Sheet API blocked:", exc)
        print("[Vicky] Enable Sheets API: https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=442759047674")
        print("[Vicky] Enable Drive API: https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=442759047674")
        print("[Vicky] Share Editor: vicky-bot@elite-balaji-automation.iam.gserviceaccount.com")
        return None
    try:
        ws = sh.worksheet("Sheet1")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="Sheet1", rows=1000, cols=10)
    headers = ["business_name", "phone_number", "source", "listing_title", "whatsapp_pitch", "email_copy", "sourced_at"]
    vals = ws.get_all_values()
    if not vals:
        ws.append_row(headers)
    elif [h.lower() for h in vals[0]] != headers:
        if not any(vals[0]):
            ws.update("A1:G1", [headers])
    return ws


def append_sheet(ws, leads: list[dict[str, Any]]) -> int:
    existing = set()
    for row in ws.get_all_records():
        p = clean(row.get("phone_number") or row.get("Phone") or "")
        n = clean(row.get("business_name") or row.get("Name") or "").lower()
        if p:
            existing.add(p)
        existing.add(n + "|" + p)
    added = 0
    for lead in leads:
        name = clean(lead.get("business_name"))
        phone = clean(lead.get("phone_number"))
        title = clean(lead.get("listing_title"))
        if not name or blocked(name) or blocked(title):
            continue
        if phone and phone in existing:
            continue
        if (name.lower() + "|" + phone) in existing:
            continue
        ws.append_row(
            [
                name,
                phone,
                clean(lead.get("source")),
                title,
                pitch_for(name),
                clean(lead.get("email_copy")),
                datetime.now(timezone.utc).isoformat(),
            ],
            value_input_option="USER_ENTERED",
        )
        existing.add(phone)
        existing.add(name.lower() + "|" + phone)
        added += 1
    return added


async def overlays(page: Page) -> None:
    try:
        await page.evaluate(KILL_JS)
    except Exception:
        pass
    try:
        await page.keyboard.press("Escape")
    except Exception:
        pass


async def scroll(page: Page, n: int = 3) -> None:
    for _ in range(n):
        await page.mouse.wheel(0, 1400)
        await page.wait_for_timeout(1100)
        await overlays(page)


async def open_ctx(pw) -> BrowserContext:
    CHROME_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    kwargs = {
        "user_data_dir": str(CHROME_PROFILE_DIR.resolve()),
        "headless": False,
        "viewport": {"width": 1366, "height": 900},
        "permissions": ["geolocation"],
        "geolocation": GEO,
        "locale": "en-IN",
        "timezone_id": "Asia/Kolkata",
        "args": ["--disable-blink-features=AutomationControlled", "--no-first-run"],
    }
    try:
        ctx = await pw.chromium.launch_persistent_context(channel="chrome", **kwargs)
    except Exception:
        ctx = await pw.chromium.launch_persistent_context(**kwargs)
    try:
        await ctx.grant_permissions(["geolocation"], origin="https://www.justdial.com")
        await ctx.grant_permissions(["geolocation"], origin="https://www.olx.in")
        await ctx.set_geolocation(GEO)
    except Exception:
        pass
    ctx.set_default_timeout(45000)
    ctx.set_default_navigation_timeout(60000)
    return ctx


async def scrape_jd(page: Page) -> list[dict[str, str]]:
    print("[Vicky] Justdial")
    await page.goto(JUSTDIAL_URL, wait_until="domcontentloaded")
    await page.wait_for_timeout(2200)
    await overlays(page)
    await page.evaluate(KILL_JS)
    await scroll(page)
    raw = await page.evaluate(
        """
() => {
  const clean = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const phones = (s) => {
    const m = (s || '').match(/(?:\\+?91[\\s-]*)?[6-9]\\d{9}/g);
    return m ? Array.from(m, x => x.trim()) : [];
  };
  const out = []; const seen = new Set();
  let cards = [];
  ['section.resultbox','.resultbox','[class*="resultbox"]','[class*="store-details"]'].forEach(sel => {
    const f = Array.from(document.querySelectorAll(sel));
    if (f.length > cards.length) cards = f;
  });
  for (const card of cards) {
    const el = card.querySelector('h2 a, h2, h3 a, h3, a[title], [class*="resultbox_title"] a');
    const name = el ? (el.getAttribute('title') || el.textContent) : '';
    const body = clean(card.innerText || '');
    const tel = card.querySelector('a[href^="tel:"], [class*="callcontent"], [class*="phone"]');
    let phone = '';
    if (tel) {
      const href = tel.getAttribute('href') || '';
      phone = href.startsWith('tel:') ? href.replace(/^tel:/i,'') : clean(tel.textContent);
    }
    if (!phone) { const p = phones(body); if (p.length) phone = p[0]; }
    const n = clean(name);
    if (!n || seen.has(n.toLowerCase())) continue;
    seen.add(n.toLowerCase());
    out.push({business_name:n, phone_number:clean(phone), listing_title:n});
    if (out.length >= 8) break;
  }
  return out;
}
"""
    )
    leads = []
    for row in raw or []:
        name = clean(row.get("business_name"))
        title = clean(row.get("listing_title")) or name
        if not name or blocked(name) or blocked(title):
            continue
        leads.append(
            {
                "business_name": name,
                "phone_number": clean(row.get("phone_number")),
                "listing_title": title,
                "source": "justdial",
                "search_query": "Civil Engineers Coimbatore",
            }
        )
    print(f"[Vicky] JD {len(leads)}")
    return leads[:5]


async def scrape_olx(page: Page) -> list[dict[str, str]]:
    print("[Vicky] OLX")
    try:
        await page.context.set_geolocation(GEO)
        await page.context.grant_permissions(["geolocation"], origin="https://www.olx.in")
    except Exception:
        pass

    async def acc(d):
        try:
            await d.accept()
        except Exception:
            pass

    page.on("dialog", acc)
    await page.goto(OLX_URL, wait_until="domcontentloaded")
    await page.wait_for_timeout(2800)
    await overlays(page)
    for sel in ('[data-aut-id="itemTitle"]', '[data-aut-id="itemBox"]'):
        try:
            await page.wait_for_selector(sel, timeout=8000)
            break
        except Exception:
            continue
    await scroll(page)
    titles = []
    loc = page.locator('[data-aut-id="itemTitle"]')
    try:
        n = await loc.count()
        for i in range(min(n, 24)):
            try:
                t = clean(await loc.nth(i).inner_text(timeout=700))
            except Exception:
                continue
            if t and len(t) >= 8 and t.lower() not in {"login", "sell", "chat", "olx", "home", "cars"}:
                if t not in titles:
                    titles.append(t)
    except Exception:
        pass
    if len(titles) < 3:
        extra = await page.evaluate(
            """
() => {
  const clean = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const out = []; const seen = new Set();
  document.querySelectorAll('[data-aut-id="itemTitle"], [data-aut-id="itemBox"] a').forEach(n => {
    const t = clean(n.textContent);
    if (!t || t.length < 8 || t.length > 120) return;
    if (seen.has(t.toLowerCase())) return;
    seen.add(t.toLowerCase()); out.push(t);
  });
  return out.slice(0,12);
}
"""
        )
        for t in extra or []:
            t = clean(t)
            if t and t not in titles:
                titles.append(t)
    leads = []
    for title in titles:
        if blocked(title):
            continue
        name = title.split("|")[0].split("-")[0].strip()[:60]
        if not name:
            continue
        leads.append(
            {
                "business_name": name,
                "phone_number": "",
                "listing_title": title,
                "source": "olx",
                "search_query": "Construction services Coimbatore",
            }
        )
        if len(leads) >= 5:
            break
    print(f"[Vicky] OLX {len(leads)}")
    return leads


async def run() -> int:
    all_leads: list[dict[str, Any]] = []
    async with async_playwright() as pw:
        ctx = await open_ctx(pw)
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        try:
            try:
                all_leads.extend(await scrape_jd(page))
            except Exception as e:
                print(f"[Vicky] JD fail {e}")
            try:
                olx = await ctx.new_page()
                all_leads.extend(await scrape_olx(olx))
                await olx.close()
            except Exception as e:
                print(f"[Vicky] OLX fail {e}")
        finally:
            await ctx.close()
    filtered = [
        L
        for L in all_leads
        if clean(L.get("business_name"))
        and not blocked(clean(L.get("business_name")))
        and not blocked(clean(L.get("listing_title")))
    ]
    if not filtered:
        print("[Vicky] no leads")
        return 1
    append_local(filtered)
    try:
        ws = open_sheet()
        if ws is not None:
            n = append_sheet(ws, filtered)
            print(f"[Vicky] sheet +{n}")
    except Exception as e:
        print(f"[Vicky] sheet fail {e}")
    print("[Vicky] done")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(run()))
    except KeyboardInterrupt:
        raise SystemExit(130)
