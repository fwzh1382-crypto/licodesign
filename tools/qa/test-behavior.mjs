import { JSDOM, VirtualConsole } from "jsdom";
import { readFileSync } from "node:fs";
import path from "node:path";

const ROOT = path.resolve("..");
const FA = /[\u0600-\u06FF]/;
let pass = 0, fail = 0;
const ok = (name, cond, extra = "") => {
  if (cond) { pass++; console.log("  PASS", name); }
  else { fail++; console.log("  FAIL", name, extra); }
};

function visiblePersian(doc) {
  let n = 0;
  const walker = doc.createTreeWalker(doc.body, doc.defaultView.NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    let el = node.parentElement, hidden = false;
    while (el && el !== doc.body) {
      if (el.hasAttribute("hidden")) { hidden = true; break; }
      el = el.parentElement;
    }
    if (hidden) continue;
    n += (node.nodeValue.match(FA) || []).length;
  }
  return n;
}

async function load(file) {
  const vc = new VirtualConsole();
  const errors = [];
  vc.on("jsdomError", e => errors.push(e.message));
  vc.on("error", e => errors.push(String(e)));
  const dom = await JSDOM.fromURL((process.env.QA_BASE_URL || "http://127.0.0.1:8765/") + file, {
    runScripts: "dangerously", resources: "usable", pretendToBeVisual: true,
    virtualConsole: vc,
  });
  await new Promise(res => dom.window.addEventListener("load", res, { once: true }));
  await new Promise(r => setTimeout(r, 60));
  return { dom, doc: dom.window.document, win: dom.window, errors };
}

function fillAndSubmit(doc, form, values) {
  for (const [name, value] of Object.entries(values)) {
    const el = form.querySelector(`[name="${name}"]`);
    if (el) el.value = value;
  }
  const consent = form.querySelector('[name="consent"]');
  if (consent) consent.checked = true;
  form.dispatchEvent(new doc.defaultView.Event("submit", { bubbles: true, cancelable: true }));
}

const pages = ["index.html", "contact.html", "services.html", "projects.html",
               "showroom.html", "about.html", "cookies.html", "privacy.html",
               "journal.html", "404.html", "project-aftab.html"];

for (const page of pages) {
  console.log("\n=== " + page + " ===");
  const { doc, win, dom, errors } = await load(page);
  ok("no JS errors", errors.length === 0, errors.join(" | "));
  ok("starts in fa/rtl", doc.documentElement.lang === "fa" && doc.documentElement.dir === "rtl");
  ok("config + content map loaded", !!win.LAICO_CONFIG && Object.keys(win.LAICO_T9N || {}).length > 300);
  ok("exactly one h1", doc.querySelectorAll("h1").length === 1);
  ok("breadcrumb or home/404", !!doc.querySelector(".breadcrumb") || ["index.html", "404.html"].includes(page));
  ok("footer legal links", !!doc.querySelector('a[href="privacy.html"]') && !!doc.querySelector('a[href="cookies.html"]'));
  ok("clear-data control", !!doc.querySelector("[data-clear-data]"));
  ok("canonical present", !!doc.querySelector('link[rel="canonical"]'));

  // language switch
  const faCount = visiblePersian(doc);
  doc.querySelector('[data-lang="en"]').click();
  const enCount = visiblePersian(doc);
  ok("EN: html lang/dir", doc.documentElement.lang === "en" && doc.documentElement.dir === "ltr");
  ok("EN: translated content (" + faCount + " -> " + enCount + " FA chars)",
     enCount < faCount * 0.12 + 12, `left=${enCount}`);
  ok("EN: document title switched", /Laico|–|-|Kitchen|Contact|About|Projects|Journal|Cookies|Privacy|Services|Studio|Process|Materials|Systems|Showroom|Living|Bath|Café|Penthouse|Villa|House|Page not found/.test(doc.title), doc.title);
  ok("EN: og:locale", doc.querySelector('meta[property="og:locale"]').content === "en_US");
  doc.querySelector('[data-lang="fa"]').click();
  ok("FA: restored", doc.documentElement.lang === "fa" && visiblePersian(doc) === faCount);

  // burger menu
  const burger = doc.querySelector("[data-burger]");
  burger.click();
  ok("menu opens + aria-label changes", burger.getAttribute("aria-expanded") === "true" &&
     burger.getAttribute("aria-label") === "بستن" && win.document.body.style.overflow === "hidden");
  doc.dispatchEvent(new win.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  ok("Escape closes menu + unlocks scroll", burger.getAttribute("aria-expanded") === "false" &&
     win.document.body.style.overflow === "");

  // forms
  const form = doc.querySelector("[data-form]");
  if (form) {
    ok("native select (no custom listbox)", !form.querySelector("[data-select]") ||
       !!form.querySelector("select.native-select"));
    ok("consent + honeypot + status", !!form.querySelector('[name="consent"]') &&
       !!form.querySelector('[name="website"]') && !!doc.querySelector("[data-form-status]"));
    ok("accessible labels", [...form.querySelectorAll("[data-field]")].every(f => {
      const c = f.querySelector("input:not([type=hidden]), textarea, select");
      return !c || !!c.id;
    }));

    const done = doc.querySelector("[data-success]");
    ok("success panel hidden before submit", done.hidden === true);
    fillAndSubmit(doc, form, { name: "A", phone: "12", note: "x" });
    ok("invalid submit blocked", form.hidden === false && !!form.querySelector(".is-invalid"));
    fillAndSubmit(doc, form, { name: "Ali Rezaei", phone: "09120898938", note: "Kitchen, 120 m2, Amol" });
    ok("form hides on success", form.hidden === true);
    ok("success panel shows", done.hidden === false);
    ok("honest demo wording", /آماده است|متصل نیست/.test(done.textContent), done.textContent.slice(0, 90));
    const wa = done.querySelector('a[href^="https://wa.me/"]');
    ok("WhatsApp deep link with payload", !!wa && decodeURIComponent(wa.href).includes("Ali Rezaei"), wa?.href.slice(0, 120));
    ok("call fallback", !!done.querySelector('a[href^="tel:"]'));
    ok("edit + clear actions", [...done.querySelectorAll("button")].some(b => /ویرایش/.test(b.textContent)) &&
       [...done.querySelectorAll("button")].some(b => /حذف/.test(b.textContent)));
    const stored = JSON.parse(win.localStorage.getItem("laico-requests") || "[]");
    ok("payload normalised to +98912...", stored.length > 0 && stored.at(-1).phone === "+989120898938",
       JSON.stringify(stored.at(-1)));
    ok("aria-live status set", (doc.querySelector("[data-form-status]").textContent || "").length > 0);
    [...done.querySelectorAll("button")].find(b => /ویرایش/.test(b.textContent))?.click();
    ok("edit restores form", form.hidden === false && done.hidden === true);
  }

  if (page === "projects.html") {
    const cards = doc.querySelectorAll("[data-prj-card]");
    const before = [...cards].filter(c => !c.hidden).length;
    doc.querySelector('[data-category="commercial"]')?.click();
    const after = [...cards].filter(c => !c.hidden).length;
    ok("project filters change results (" + before + " -> " + after + ")", after !== before);
    ok("filter tabs expose aria-pressed",
       doc.querySelector('[data-category="commercial"]').getAttribute("aria-pressed") === "true");
  }
  dom.window.close();
}

console.log(`\n================\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
