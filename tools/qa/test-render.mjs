import puppeteer from "puppeteer-core";
import { mkdirSync } from "node:fs";
import path from "node:path";

const EXE = process.env.CHROMIUM_PATH || "/tmp/laico-chrome/chromium";
const BASE = process.env.QA_BASE_URL || "http://127.0.0.1:8765/";
const OUT = path.resolve("../reference/uiux");
mkdirSync(OUT, { recursive: true });

const widths = [320, 360, 390, 768, 1024, 1440];
const pages = ["index.html", "services.html", "projects.html", "contact.html",
               "about.html", "showroom.html", "journal.html", "cookies.html",
               "project-aftab.html", "404.html"];
const shotPages = ["index.html", "services.html", "projects.html", "contact.html", "404.html"];
const shotWidths = { 320: "mobile", 768: "tablet", 1440: "desktop" };

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { c ? (pass++, console.log("  PASS", n)) : (fail++, console.log("  FAIL", n, extra)); };

const args = ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
              "--disable-gpu", "--font-render-hinting=none", "--hide-scrollbars"];

async function withPage(fn) {
  const browser = await puppeteer.launch({ executablePath: EXE, headless: true, args,
    defaultViewport: { width: 1440, height: 900 } });
  try { return await fn(browser); } finally { await browser.close(); }
}

for (const page of pages) {
  console.log("\n=== " + page + " ===");
  await withPage(async browser => {
    for (const width of widths) {
      let p;
      try {
        p = await browser.newPage();
        await p.setViewport({ width, height: 900, deviceScaleFactor: 1 });
        const errs = [], bad = [];
        p.on("pageerror", e => errs.push(e.message));
        p.on("requestfailed", r => bad.push(r.url() + " " + (r.failure()?.errorText || "")));
        await p.goto(BASE + page, { waitUntil: "load", timeout: 30000 });
        await p.evaluate(() => document.fonts.ready);
        await new Promise(r => setTimeout(r, 120));
        const data = await p.evaluate(() => {
          const de = document.documentElement;
          const imgs = [...document.querySelectorAll("img")];
          const hero = document.querySelector("main img");
          const success = document.querySelector("[data-success]");
          const form = document.querySelector("[data-form]");
          const bc = document.querySelector(".breadcrumb");
          const skip = document.querySelector(".skip");
          return {
            scrollWidth: de.scrollWidth, innerWidth: window.innerWidth,
            imgCount: imgs.length,
            brokenImgs: imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute("src")),
            webpUsed: imgs.filter(i => /\.webp$/i.test(i.currentSrc)).length,
            heroOK: !hero || (hero.getBoundingClientRect().width > 0 && hero.getBoundingClientRect().height > 0),
            successHidden: !success || getComputedStyle(success).display === "none",
            formVisible: !form || getComputedStyle(form).display !== "none",
            bcVisible: !bc || bc.getBoundingClientRect().height > 10,
            skipBottom: skip ? skip.getBoundingClientRect().bottom : -999,
          };
        });
        ok(`${width}px no horizontal overflow`, data.scrollWidth <= width + 1,
           `scrollWidth=${data.scrollWidth} vs ${width}`);
        ok(`${width}px no broken images`, data.brokenImgs.length === 0, data.brokenImgs.join(","));
        ok(`${width}px WebP actually used`, data.imgCount === 0 || data.webpUsed > 0,
           `${data.webpUsed}/${data.imgCount}`);
        ok(`${width}px hero image has layout`, data.heroOK);
        ok(`${width}px [hidden] success panel is hidden`, data.successHidden);
        ok(`${width}px form visible`, data.formVisible);
        ok(`${width}px breadcrumb rendered`, data.bcVisible);
        ok(`${width}px skip link fully offscreen`, data.skipBottom <= 0, `bottom=${data.skipBottom}`);
        ok(`${width}px no page errors / failed requests`, errs.length === 0 && bad.length === 0,
           [...errs, ...bad].slice(0, 3).join(" | "));
        if (shotWidths[width] && shotPages.includes(page)) {
          await p.screenshot({ path: path.join(OUT, `${page.replace(".html", "")}-${shotWidths[width]}.png`) });
        }
      } finally {
        if (p && !p.isClosed()) await p.close().catch(() => {});
      }
    }
  });
}

// EN rendering smoke test
console.log("\n=== EN visual smoke ===");
await withPage(async browser => {
  const p = await browser.newPage();
  await p.setViewport({ width: 1280, height: 800 });
  await p.goto(BASE + "services.html", { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready);
  await p.click('[data-lang="en"]');
  await new Promise(r => setTimeout(r, 200));
  const en = await p.evaluate(() => ({
    dir: document.documentElement.dir,
    breadcrumb: document.querySelector(".breadcrumb")?.innerText,
    footer: document.querySelector(".footer-legal")?.innerText,
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    faChars: (document.body.innerText.match(/[\u0600-\u06FF]/g) || []).length,
  }));
  ok("EN dir=ltr", en.dir === "ltr");
  ok("EN breadcrumb translated", /Home|Services/.test(en.breadcrumb || ""), en.breadcrumb);
  ok("EN footer legal translated", /rights|Privacy|Cookies/i.test(en.footer || ""), en.footer);
  ok("EN no horizontal overflow", en.overflow <= 1, String(en.overflow));
  ok("EN no Persian left in visible text", en.faChars === 0, String(en.faChars));
  await p.screenshot({ path: path.join(OUT, "services-en-desktop.png") });
  await p.close();
});

console.log(`\n================\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
