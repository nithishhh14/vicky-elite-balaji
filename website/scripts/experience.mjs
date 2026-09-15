// Playwright "experience" pass: drives the real interactions and captures
// screenshots + layout-shift numbers. Usage (preview on 4322):
//   node scripts/experience.mjs [baseUrl] [label]
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const BASE = process.argv[2] ?? "http://localhost:4322";
const LABEL = process.argv[3] ?? "run";
const OUT = new URL(`../qa-screens/experience-${LABEL}/`, import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
mkdirSync(OUT, { recursive: true });

const log = [];
const note = (s) => { log.push(s); console.log(s); };
const shot = (page, name) => page.screenshot({ path: join(OUT, `${name}.png`) });

async function cls(page) {
  return page.evaluate(() => (window.__cls ?? 0).toFixed(4));
}
async function newPage(context) {
  const page = await context.newPage();
  const errors = [];
  page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  page.on("pageerror", (e) => errors.push(e.message));
  await page.addInitScript(() => {
    window.__cls = 0;
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) if (!e.hadRecentInput) window.__cls += e.value;
    }).observe({ type: "layout-shift", buffered: true });
  });
  page.errors = errors;
  return page;
}
const exists = async (page, sel) => (await page.locator(sel).count()) > 0;

const browser = await chromium.launch();

// ---------- Desktop ----------
{
  const context = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const page = await newPage(context);

  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.waitForTimeout(3200);
  await shot(page, "d01-home-top");
  const hTop = await page.locator("#site-header").boundingBox();
  await page.mouse.wheel(0, 600);
  await page.waitForTimeout(900);
  await shot(page, "d02-home-scrolled");
  const hScrolled = await page.locator("#site-header").boundingBox();
  note(`home header height top=${hTop?.height} scrolled=${hScrolled?.height}`);

  // Products menu
  await page.locator("#materials-toggle").click();
  await page.waitForTimeout(700);
  await shot(page, "d03-products-menu");
  note(`products menu visible=${await page.locator("#materials-menu").isVisible()}`);
  await page.keyboard.press("Escape");
  await page.waitForTimeout(500);
  note(`products menu after Esc visible=${await page.locator("#materials-menu").isVisible()}`);

  // Material worlds hover
  await page.locator("#materials").scrollIntoViewIfNeeded();
  await page.waitForTimeout(900);
  const cards = page.locator("#materials .material-card");
  if (await cards.count()) {
    await cards.nth(1).hover();
    await page.waitForTimeout(800);
    await shot(page, "d04-worlds-hover");
  }

  // Material Match
  const mm = page.locator("#material-match");
  await mm.scrollIntoViewIfNeeded();
  await mm.locator('[data-group="surface"] button[data-value="kitchen"]').click();
  await page.waitForTimeout(1200);
  await mm.locator('[data-group="look"] button').first().click();
  await page.waitForTimeout(1200);
  await shot(page, "d05-material-match");
  note(`material match products=${await mm.locator("[data-products] li").count()}`);

  // Header search
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);
  await page.locator('#site-header [aria-label="Search the catalogue"]').click();
  await page.waitForTimeout(900);
  await shot(page, "d06-search-open");
  if (await exists(page, "#search-overlay")) {
    await page.keyboard.type("black granite");
    await page.waitForTimeout(900);
    await shot(page, "d07-search-typed");
    note(`search overlay results=${await page.locator("#search-overlay [data-search-results] li").count()}`);
    await page.keyboard.press("Escape");
    await page.waitForTimeout(500);
  } else {
    note(`search navigated to ${page.url()}`);
  }
  note(`home CLS=${await cls(page)} errors=${page.errors.length}`);

  // Product page: save + enquiry
  const p2 = await newPage(context);
  await p2.goto(BASE + "/products/granite-black-galaxy/", { waitUntil: "networkidle" });
  await p2.waitForTimeout(800);
  await p2.evaluate(() => localStorage.removeItem("eb-my-materials"));
  const save = p2.locator("[data-save]").first();
  await save.click();
  await p2.waitForTimeout(350);
  await shot(p2, "d08-save-flight");
  await p2.waitForTimeout(900);
  note(`saved pressed=${await save.getAttribute("aria-pressed")} count=${await p2.locator("#site-header [data-shortlist-count]").first().textContent()}`);
  const ask = p2.locator("[data-enquire]").first();
  if (await ask.count()) {
    await ask.click();
    await p2.waitForTimeout(800);
    await shot(p2, "d09-enquiry-drawer");
    note(`enquiry drawer open=${await p2.locator("#enquiry-drawer").isVisible()} product=${await p2.locator("#enquiry-drawer [name=product]").inputValue()}`);
    await p2.keyboard.press("Escape");
    await p2.waitForTimeout(500);
    note(`enquiry drawer after Esc=${await p2.locator("#enquiry-drawer").isVisible()}`);
  } else {
    note("no [data-enquire] triggers on product page");
  }
  note(`floating CTA label="${(await p2.locator(".enquiry-cta").innerText()).trim()}"`);
  await p2.evaluate(() => window.scrollTo(0, 400));
  await p2.waitForTimeout(700);
  note(`product CLS=${await cls(p2)} errors=${p2.errors.length}`);

  // Non-overlay page header CLS on scroll
  const p3 = await newPage(context);
  await p3.goto(BASE + "/granite/", { waitUntil: "networkidle" });
  await p3.waitForTimeout(1200);
  await shot(p3, "d10-granite-top");
  const firstY = await p3.locator("main").boundingBox();
  await p3.mouse.wheel(0, 120);
  await p3.waitForTimeout(900);
  const firstY2 = await p3.locator("main").boundingBox();
  note(`granite main shift on header change=${(firstY2.y + 120 - firstY.y).toFixed(1)}px`);
  await p3.mouse.wheel(0, 900);
  await p3.waitForTimeout(1200);
  await shot(p3, "d11-granite-scrolled");
  const fam = p3.locator("[data-family-stage]");
  if (await fam.count()) {
    await fam.scrollIntoViewIfNeeded();
    await p3.locator("[data-family-pick]").nth(2).click();
    await p3.waitForTimeout(1400);
    await shot(p3, "d12-granite-family");
    note(`granite stage name="${await fam.locator("[data-stage-name]").textContent()}" count=${await fam.locator("[data-granite-count]").textContent()} thumbs=${await fam.locator("[data-stage-thumb]").count()}`);
    await p3.locator('[data-filter-key="finish"]').first().click();
    await p3.waitForTimeout(900);
    note(`granite stage after finish name="${await fam.locator("[data-stage-name]").textContent()}" count=${await fam.locator("[data-granite-count]").textContent()}`);
  }
  note(`granite CLS=${await cls(p3)} errors=${p3.errors.length}`);

  // Custom horizontal story
  const p4 = await newPage(context);
  await p4.goto(BASE + "/custom/", { waitUntil: "networkidle" });
  const hs = p4.locator("[data-gsap-hscroll]");
  if (await hs.count()) {
    const box = await hs.boundingBox();
    await p4.evaluate((y) => window.scrollTo(0, y), box.y + 10);
    await p4.waitForTimeout(900);
    await shot(p4, "d13-custom-hscroll-start");
    await p4.mouse.wheel(0, 900);
    await p4.waitForTimeout(1400);
    await shot(p4, "d14-custom-hscroll-mid");
  }
  note(`custom errors=${p4.errors.length}`);

  // Shortlist compare tray
  const p5 = await newPage(context);
  await p5.goto(BASE + "/granite/", { waitUntil: "networkidle" });
  const saves = p5.locator(".specimen [data-save]");
  for (let i = 0; i < 3; i++) { await saves.nth(i).scrollIntoViewIfNeeded(); await saves.nth(i).click(); await p5.waitForTimeout(250); }
  await p5.goto(BASE + "/shortlist/", { waitUntil: "networkidle" });
  await p5.waitForTimeout(600);
  const boxes = p5.locator("[data-select]");
  await boxes.nth(0).check();
  await p5.waitForTimeout(500);
  await boxes.nth(1).check();
  await p5.waitForTimeout(700);
  await shot(p5, "d15-compare-tray");
  note(`tray visible=${await p5.locator("[data-compare-tray]").isVisible()} thumbs=${await p5.locator("[data-tray-thumbs] li").count()}`);
  await p5.locator("[data-tray-btn]").click();
  await p5.waitForTimeout(1200);
  note(`compare table visible=${await p5.locator("[data-compare]").isVisible()} tray hidden=${!(await p5.locator("[data-compare-tray]").isVisible())} errors=${p5.errors.length}`);

  // Gallery filter + applications hover
  const p6 = await newPage(context);
  await p6.goto(BASE + "/gallery/", { waitUntil: "networkidle" });
  await p6.locator('[data-filter="marble"]').click();
  await p6.waitForTimeout(1000);
  const visibleTiles = await p6.locator("#gallery-grid > [data-groups]:not([hidden])").count();
  note(`gallery marble tiles=${visibleTiles} gridOpacity=${await p6.locator("#gallery-grid").evaluate((g) => getComputedStyle(g).opacity)} errors=${p6.errors.length}`);
  await shot(p6, "d16-gallery-marble");

  const p7 = await newPage(context);
  await p7.goto(BASE + "/", { waitUntil: "networkidle" });
  await p7.waitForTimeout(2500);
  const app = p7.locator('a[href="/applications/#kitchen"]').first();
  await app.scrollIntoViewIfNeeded();
  await p7.waitForTimeout(900);
  await app.hover();
  await p7.waitForTimeout(900);
  await shot(p7, "d17-applications-hover");
  note(`app reveal opacity=${await app.locator(".app-reveal").evaluate((e) => getComputedStyle(e).opacity)}`);
  await context.close();
}

// ---------- Reduced motion: everything must be visible and static ----------
{
  const context = await browser.newContext({ viewport: { width: 1366, height: 900 }, reducedMotion: "reduce" });
  const page = await newPage(context);
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  const hidden = await page.evaluate(() =>
    [...document.querySelectorAll("h1, [data-hero-seq], [data-gsap-stagger] > *, [data-intro-image]")].filter((e) => getComputedStyle(e).opacity === "0").length
  );
  await shot(page, "r01-reduced-home");
  note(`reduced-motion hidden elements=${hidden} errors=${page.errors.length}`);
  await context.close();
}

// ---------- Phone ----------
{
  const context = await browser.newContext({ viewport: { width: 375, height: 812 }, hasTouch: true, isMobile: true });
  const page = await newPage(context);
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.waitForTimeout(3000);
  await shot(page, "m01-home-top");
  await page.locator("#menu-toggle").tap();
  await page.waitForTimeout(800);
  await shot(page, "m02-drawer");
  note(`phone drawer visible=${await page.locator("#site-menu").isVisible()}`);
  await page.locator("#menu-toggle").tap();
  await page.waitForTimeout(700);
  note(`phone drawer closed=${!(await page.locator("#site-menu").isVisible())}`);
  await page.evaluate(() => window.scrollTo(0, 700));
  await page.waitForTimeout(900);
  await shot(page, "m03-home-scrolled");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  note(`phone home overflow=${overflow} CLS=${await cls(page)} errors=${page.errors.length}`);

  await page.locator('#site-header [aria-label="Search the catalogue"]').tap();
  await page.waitForTimeout(700);
  await page.keyboard.type("quartz sink");
  await page.waitForTimeout(900);
  await shot(page, "m05-search");
  note(`phone search results=${await page.locator("#search-overlay [data-search-results] li").count()}`);
  await page.keyboard.press("Escape");

  const p2 = await newPage(context);
  await p2.goto(BASE + "/products/sanitary-quartz-sink-single/", { waitUntil: "networkidle" });
  const ask = p2.locator("main [data-enquire]").first();
  if (await ask.count()) {
    await ask.tap();
    await p2.waitForTimeout(900);
    await shot(p2, "m04-enquiry");
    const box = await p2.locator("#enquiry-drawer .eb-dialog-panel").boundingBox();
    note(`phone enquiry panel y=${box?.y?.toFixed(0)} h=${box?.height?.toFixed(0)}`);
  }
  note(`phone product errors=${p2.errors.length}`);

  const p3 = await newPage(context);
  await p3.goto(BASE + "/granite/", { waitUntil: "networkidle" });
  await p3.locator("[data-family-stage]").scrollIntoViewIfNeeded();
  await p3.waitForTimeout(600);
  await shot(p3, "m06-granite-stage");
  const overflow2 = await p3.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  note(`phone granite overflow=${overflow2} errors=${p3.errors.length}`);
  await context.close();
}

await browser.close();
