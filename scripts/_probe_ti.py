import asyncio
import json
from playwright.async_api import async_playwright

EXTRACT = r"""
() => {
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const out = [];
  const cards = Array.from(document.querySelectorAll('div, section, article, li')).filter(el => {
    const t = clean(el.innerText);
    return t.includes('View Mobile Number') || t.includes('Contact Supplier') || t.includes('Business Type');
  });
  const seen = new Set();
  for (const card of cards.slice(0, 80)) {
    const text = clean(card.innerText);
    if (text.length < 40 || text.length > 1200) continue;
    const key = text.slice(0, 100);
    if (seen.has(key)) continue;
    seen.add(key);
    const link = card.querySelector('a[href*="/products/"], a[href*="company"], a[href*="seller"]');
    out.push({ text: text.slice(0, 400), href: link ? link.href : location.href });
  }
  return out.slice(0, 20);
}
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=False, args=["--disable-blink-features=AutomationControlled"])
        ctx = await b.new_context(permissions=["geolocation"], geolocation={"latitude": 11.0168, "longitude": 76.9558}, locale="en-IN")
        page = await ctx.new_page()
        await page.goto("https://www.tradeindia.com/coimbatore/civil-contractor-city-228082.html", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)
        data = await page.evaluate(EXTRACT)
        print(json.dumps(data[:8], ensure_ascii=False, indent=2))
        await b.close()

asyncio.run(main())
