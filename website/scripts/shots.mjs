// Quick visual captures: node scripts/shots.mjs [baseUrl]
import { chromium } from "playwright";
const BASE = process.argv[2] ?? "http://localhost:4322";
const browser = await chromium.launch();
const run = async (name, vp, path, fn) => {
  const page = await browser.newPage({ viewport: vp, ...(vp.width < 500 ? { isMobile: true, hasTouch: true } : {}) });
  await page.goto(BASE + path, { waitUntil: "networkidle" });
  await page.waitForTimeout(4600);
  if (fn) await fn(page);
  await page.screenshot({ path: `qa-screens/${name}.png` });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  console.log(name, "overflow", overflow);
  await page.close();
};
await run("hdr-desktop-top", { width: 1366, height: 900 }, "/");
await run("hdr-desktop-scrolled", { width: 1366, height: 900 }, "/", async (p) => { await p.mouse.wheel(0, 700); await p.waitForTimeout(1000); });
await run("hdr-phone-top", { width: 375, height: 812 }, "/");
await run("hdr-1280-top", { width: 1280, height: 800 }, "/granite/");
await run("marble-statement", { width: 1366, height: 900 }, "/marble/", async (p) => { await p.locator("#statement").scrollIntoViewIfNeeded(); await p.waitForTimeout(1500); });
await browser.close();
