import asyncio
import json
import re
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=False, args=["--disable-blink-features=AutomationControlled"])
        ctx = await b.new_context(permissions=["geolocation"], geolocation={"latitude": 11.0168, "longitude": 76.9558}, locale="en-IN")
        page = await ctx.new_page()
        await page.goto("https://www.tradeindia.com/coimbatore/civil-contractor-city-228082.html", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(4000)
        btns = page.get_by_text("View Mobile Number")
        n = await btns.count()
        print("view_mobile_buttons", n)
        if n:
            await btns.nth(0).click(timeout=5000)
            await page.wait_for_timeout(2500)
            body = await page.locator("body").inner_text()
            phones = re.findall(r"(?:\+?91[\s-]*)?[6-9]\d{9}", body)
            print("phones_after_click", phones[:10])
        # parse sellers with city
        html = await page.content()
        Path = __import__("pathlib").Path
        Path("_ti_snip.html").write_text(html[:50000], encoding="utf-8")
        data = await page.evaluate(r"""
() => {
  const clean = s => (s||'').replace(/\s+/g,' ').trim();
  const out=[];
  document.querySelectorAll('a').forEach(a => {
    const t=clean(a.innerText);
    const href=a.href||'';
    if (/products\//.test(href) && t.length>8 && t.length<120) out.push({product:t, href});
  });
  return out.slice(0,15);
}
""")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        await b.close()

asyncio.run(main())
