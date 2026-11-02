import puppeteer from "puppeteer-core";
import { readdirSync } from "node:fs";
import path from "node:path";

const ROOT = path.resolve("..");
const BASE = process.env.QA_BASE_URL || "http://127.0.0.1:8765/";
const pages = readdirSync(ROOT).filter(f => f.endsWith(".html")).sort();
const widths = [320, 768, 1440];
const FA = /[\u0600-\u06FF]/;
let pass = 0, fail = 0;
const ok = (n, c, extra = "") => { c ? pass++ : (fail++, console.log("  FAIL", n, extra)); };

const browser = await puppeteer.launch({
  executablePath: process.env.CHROMIUM_PATH || "/tmp/laico-chrome/chromium", headless: true,
  args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
         "--disable-gpu", "--hide-scrollbars"],
  defaultViewport: { width: 1440, height: 900 },
});

for (const page of pages) {
  const p = await browser.newPage();
  const errs = [];
  p.on("pageerror", e => errs.push(e.message));
  for (const width of widths) {
    await p.setViewport({ width, height: 900 });
    await p.goto(BASE + page, { waitUntil: "load" });
    await p.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 100));
    const d = await p.evaluate(() => ({
      over: document.documentElement.scrollWidth - window.innerWidth,
      broken: [...document.querySelectorAll("img")].filter(i => i.complete && i.naturalWidth === 0).length,
    }));
    ok(`${page} @${width} overflow`, d.over <= 1, String(d.over));
    ok(`${page} @${width} broken imgs`, d.broken === 0, String(d.broken));
  }
  // English mode on every page
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto(BASE + page, { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready);
  await p.click('[data-lang="en"]');
  await new Promise(r => setTimeout(r, 120));
  const en = await p.evaluate(() => ({
    dir: document.documentElement.dir,
    fa: (document.body.innerText.match(/[\u0600-\u06FF]/g) || []).length,
    over: document.documentElement.scrollWidth - window.innerWidth,
    title: document.title,
  }));
  ok(`${page} EN dir`, en.dir === "ltr");
  ok(`${page} EN zero Persian visible text`, en.fa === 0, `${en.fa} chars`);
  ok(`${page} EN no overflow`, en.over <= 1, String(en.over));
  ok(`${page} EN title`, /[A-Za-z]/.test(en.title) && !FA.test(en.title), en.title);
  ok(`${page} no JS errors`, errs.length === 0, errs.join(" | "));
  await p.close();
}
await browser.close();
console.log(`all-pages: ${pass} passed, ${fail} failed (${pages.length} pages × ${widths.length} widths + EN)`);
process.exit(fail ? 1 : 0);
