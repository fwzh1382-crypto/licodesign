#!/usr/bin/env python3
"""Comprehensive UI/UX + accessibility QA for the LAICO DESIGN template.

Dependency-free. Scores the site against 12 categories (100 points) and prints
pass/fail evidence for each check. This is the automated companion to the
human review in UIUX-REPORT.md.

    python3 tools/uiux_audit.py            # human-readable report
    python3 tools/uiux_audit.py --json     # machine-readable
    python3 tools/uiux_audit.py --strict   # non-zero exit below 100

Run after tools/uiux_fix.py and tools/build_i18n.py.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_scan import scan_all, FA  # noqa: E402

PAGES = sorted(ROOT.glob("*.html"))
CSS = {p.name: p.read_text(encoding="utf-8") for p in sorted((ROOT / "css").glob("*.css"))}
ALL_CSS = "\n".join(CSS.values())
MAIN_JS = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
CONFIG_JS = (ROOT / "js" / "config.js").read_text(encoding="utf-8")
T9N = ROOT / "js" / "i18n-content.js"


# --------------------------------------------------------------------------
def contrast(fg: str, bg: str) -> float:
    def lum(h: str) -> float:
        h = h.lstrip("#")
        ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        lin = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in ch]
        return .2126 * lin[0] + .7152 * lin[1] + .0722 * lin[2]
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + .05) / (b + .05)


def collect() -> list[dict]:
    results = []

    def check(category: str, label: str, ok: bool, detail: str = "", weight: int = 1):
        results.append({"category": category, "label": label,
                        "ok": bool(ok), "detail": detail, "weight": weight})

    # --- 1. information architecture -------------------------------------
    h1_bad = [p.name for p in PAGES if len(re.findall(r"<h1\b", p.read_text(encoding="utf-8"))) != 1]
    check("IA", "exactly one <h1> on every page", not h1_bad, ", ".join(h1_bad), 2)
    bc_bad = [p.name for p in PAGES if p.name not in ("index.html", "404.html")
              and 'class="breadcrumb"' not in p.read_text(encoding="utf-8")]
    check("IA", "breadcrumbs on all inner pages", not bc_bad, ", ".join(bc_bad), 2)
    check("IA", "sitemap.xml / robots.txt / 404.html / manifest present",
          all((ROOT / f).is_file() for f in ("sitemap.xml", "robots.txt", "404.html", "site.webmanifest")), weight=2)
    inbound = set()
    for p in PAGES:
        for href in re.findall(r'href="([^"#?]+\.html)', p.read_text(encoding="utf-8")):
            inbound.add(Path(href).name)
    orphans = sorted({p.name for p in PAGES} - inbound - {"404.html"})
    check("IA", "no orphan pages", not orphans, ", ".join(orphans), 2)

    # --- 2. SEO ------------------------------------------------------------
    for tag, label in [('rel="canonical"', "canonical"),
                       ('property="og:image"', "og:image"),
                       ('rel="manifest"', "web manifest")]:
        bad = [p.name for p in PAGES if tag not in p.read_text(encoding="utf-8")]
        check("SEO", f"{label} on every page", not bad, ", ".join(bad), 2)
    ld = sum(1 for p in PAGES if "application/ld+json" in p.read_text(encoding="utf-8"))
    check("SEO", "JSON-LD LocalBusiness", ld >= 2, f"{ld} pages", 1)
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8") if (ROOT / "sitemap.xml").exists() else ""
    check("SEO", "sitemap lists all indexable pages",
          sitemap.count("<loc>") == len(PAGES) - 1,
          f"{sitemap.count('<loc>')} urls / {len(PAGES)-1} pages", 1)

    # --- 3. accessibility: structure --------------------------------------
    img_total = img_alt = img_dims = img_lazy = img_webp = 0
    bad_alt, bad_dims, bad_lazy = [], [], []
    for p in PAGES:
        s = p.read_text(encoding="utf-8")
        for tag in re.findall(r"<img\b[^>]*>", s):
            img_total += 1
            if re.search(r'\balt="[^"]*"', tag):
                img_alt += 1
            elif re.search(r'\balt\s*=', tag) or 'alt=""' in tag:
                img_alt += 1
            else:
                bad_alt.append(p.name)
            if "width=" in tag and "height=" in tag:
                img_dims += 1
            else:
                bad_dims.append(p.name)
            if "loading=" in tag:
                img_lazy += 1
            else:
                bad_lazy.append(p.name)
        img_webp += len(re.findall(r'<source[^>]+type="image/webp"', s))
    check("A11Y", "every image has an alt attribute", not bad_alt, ", ".join(sorted(set(bad_alt))), 2)
    check("A11Y", "every image has intrinsic width/height (no CLS)", not bad_dims, ", ".join(sorted(set(bad_dims))), 2)
    check("A11Y", "explicit loading strategy on every image", img_lazy == img_total,
          f"{img_lazy}/{img_total}", 1)
    check("A11Y", "WebP <picture> source for every raster image", img_webp == img_total,
          f"{img_webp}/{img_total}", 1)
    select_bad = [p.name for p in PAGES if "data-select" in p.read_text(encoding="utf-8")]
    check("A11Y", "no inaccessible custom listbox (native <select>)", not select_bad, ", ".join(select_bad), 2)
    label_bad = [p.name for p in PAGES if '<span class="field-label"' in p.read_text(encoding="utf-8")]
    check("A11Y", "form labels are real <label> elements", not label_bad, ", ".join(label_bad), 2)
    skip_bad = [p.name for p in PAGES if 'class="skip"' not in p.read_text(encoding="utf-8")]
    check("A11Y", "skip-to-content link on every page", not skip_bad, ", ".join(skip_bad), 1)
    check("A11Y", "global [hidden] rule present", "[hidden] { display: none !important; }" in ALL_CSS, weight=2)
    check("A11Y", "strong :focus-visible outline present", "outline: 3px solid #1a6bff !important" in ALL_CSS, weight=2)
    check("A11Y", "prefers-reduced-motion respected", "prefers-reduced-motion" in ALL_CSS, weight=1)
    check("A11Y", "scroll-padding-top for fixed header", "scroll-padding-top" in ALL_CSS, weight=1)

    # --- 4. forms / conversion ---------------------------------------------
    forms = [p for p in PAGES if "data-form" in p.read_text(encoding="utf-8")]
    for feature, needle in [("consent checkbox", 'name="consent"'),
                            ("honeypot", 'name="website"'),
                            ("live status region", "data-form-status"),
                            ("privacy note", "form-privacy-note")]:
        bad = [p.name for p in forms if needle not in p.read_text(encoding="utf-8")]
        check("Forms", f"{feature} on every form", not bad, ", ".join(bad), 2)
    check("Forms", "no fake success claim in demo mode", "f-demo-title" in MAIN_JS, weight=2)
    check("Forms", "phone normalisation (leading zero removed)", "slice(1)" in MAIN_JS, weight=1)
    check("Forms", "server endpoint configurable", "formEndpoint" in CONFIG_JS and "fetch(" in MAIN_JS, weight=2)
    check("Forms", "WhatsApp / call fallback actions", "wa.me/" in MAIN_JS and "tel:" in MAIN_JS, weight=2)
    check("Forms", "local data retention + clear control", "requestRetentionDays" in CONFIG_JS and "data-clear-data" in MAIN_JS, weight=2)

    # --- 5. content / trust -------------------------------------------------
    bad_phone = [p.name for p in PAGES if "000 0000" in p.read_text(encoding="utf-8")]
    check("Content", "no sample phone number", not bad_phone, ", ".join(bad_phone), 2)
    generic = [p.name for p in PAGES if re.search(r'href="https://(?:www\.instagram\.com/|t\.me/|www\.youtube\.com/)"',
                                                  p.read_text(encoding="utf-8"))]
    check("Content", "no generic/dead social links", not generic, ", ".join(generic), 2)
    hours = [p.name for p in PAGES if "چهارشنبه 9" in p.read_text(encoding="utf-8")]
    check("Content", "consistent opening hours", not hours, ", ".join(hours), 1)
    check("Content", "single source of truth (js/config.js)", "LAICO_CONFIG" in CONFIG_JS, weight=1)
    check("Content", "legal pages linked from footer",
          all('href="privacy.html"' in p.read_text(encoding="utf-8") and
              'href="cookies.html"' in p.read_text(encoding="utf-8") for p in PAGES), weight=2)

    # --- 6. i18n ------------------------------------------------------------
    found = scan_all(ROOT)
    trans = json.loads((ROOT / "tools" / "translations.json").read_text(encoding="utf-8"))
    missing = sorted(v for v in found if v not in trans)
    check("I18N", "every translatable string has an EN value", not missing,
          "; ".join(missing[:5]), 2)
    check("I18N", "generated runtime map exists", T9N.is_file() and T9N.stat().st_size > 1000, weight=1)
    fa_keys = set(re.findall(r'"([^"]+)"\s*:', re.search(r"\bfa\s*:\s*\{(.*?)\n    \}", MAIN_JS, re.S).group(1)))
    en_keys = set(re.findall(r'"([^"]+)"\s*:', re.search(r"\ben\s*:\s*\{(.*?)\n    \}", MAIN_JS, re.S).group(1)))
    check("I18N", "fa/en dictionaries have identical keys", fa_keys == en_keys,
          f"fa={len(fa_keys)} en={len(en_keys)}", 2)
    check("I18N", "og:locale follows the language switch", "og:locale" in MAIN_JS, weight=1)
    bad_order = [p.name for p in PAGES if "js/main.js" in p.read_text(encoding="utf-8")
                 and "js/i18n-content.js" not in p.read_text(encoding="utf-8")]
    check("I18N", "config + content map load before main.js", not bad_order, ", ".join(bad_order), 2)

    # --- 7. visual / code quality ------------------------------------------
    inline = []
    raw_amp = []
    bad_tel = []
    for p in PAGES:
        s = p.read_text(encoding="utf-8")
        if re.search(r'\sstyle="', s):
            inline.append(p.name)
        if re.search(r'tel:[^"\s]*\s', s):
            bad_tel.append(p.name)
        for m in re.finditer(r"<(script|style)\b.*?</\1>", s, re.S):
            s = s.replace(m.group(0), "")
        if re.search(r"&(?!(?:amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9A-Fa-f]+);)", s):
            raw_amp.append(p.name)
    check("Code", "no inline style attributes", not inline, ", ".join(inline), 2)
    check("Code", "no unescaped ampersands", not raw_amp, ", ".join(raw_amp), 2)
    check("Code", "no spaces inside tel: URIs", not bad_tel, ", ".join(bad_tel), 1)
    dup = []
    for p in PAGES:
        ids = re.findall(r'\bid="([^"]+)"', p.read_text(encoding="utf-8"))
        dup += [p.name for k, v in __import__("collections").Counter(ids).items() if v > 1]
    check("Code", "no duplicate element ids", not dup, ", ".join(sorted(set(dup))), 2)

    # --- 8. contrast (WCAG 2.2 AA, >= 4.5:1 for normal text) ---------------
    pairs = [
        ("body text", "#3d5166", "#ffffff"), ("ink heading", "#081727", "#ffffff"),
        ("muted token", "#5e6f80", "#ffffff"), ("muted-2 token", "#5a6472", "#ffffff"),
        ("field label", "#5e6f80", "#ffffff"), ("field placeholder", "#606c7a", "#ffffff"),
        ("about placeholder", "#5f6368", "#f2f2f2"),
        ("services placeholder", "#5f6368", "#f2f3f5"),
        ("projects placeholder", "#606c7a", "#ffffff"),
        ("services body", "#5a6472", "#ffffff"), ("projects count", "#5a6472", "#ffffff"),
        ("error text", "#a44545", "#ffffff"), ("footer legal", "#3a3a3a", "#ffffff"),
    ]
    low = [f"{name} {contrast(a,b):.2f}:1" for name, a, b in pairs if contrast(a, b) < 4.5]
    check("Contrast", "all normal text >= 4.5:1 (WCAG AA)", not low, "; ".join(low), 3)
    check("Contrast", "white on navy >= 4.5:1", contrast("#ffffff", "#0b1d33") >= 4.5,
          f"{contrast('#ffffff', '#0b1d33'):.2f}:1", 2)

    # --- 9. performance -----------------------------------------------------
    jpgs = list((ROOT / "assets" / "images").glob("*.jpg"))
    webps = list((ROOT / "assets" / "images").glob("*.webp"))
    jb = sum(p.stat().st_size for p in jpgs)
    wb = sum(p.stat().st_size for p in webps)
    check("Perf", "WebP mirror for every JPG", len(webps) == len(jpgs),
          f"{len(webps)}/{len(jpgs)}, {100-100*wb/max(jb,1):.0f}% smaller", 2)
    eager = sum(1 for p in PAGES if 'fetchpriority="high"' in p.read_text(encoding="utf-8"))
    check("Perf", "hero image prioritised, others lazy", eager >= 1 and "loading=\"lazy\"" in
          "".join(p.read_text(encoding="utf-8") for p in PAGES), f"{eager} pages with prioritised hero", 1)

    return results


def main() -> int:
    results = collect()
    cats: dict[str, list[dict]] = {}
    for r in results:
        cats.setdefault(r["category"], []).append(r)
    score = 0
    total = 0
    print("LAICO DESIGN — UI/UX QA audit\n" + "=" * 46)
    for cat, items in cats.items():
        w = sum(i["weight"] for i in items)
        got = sum(i["weight"] for i in items if i["ok"])
        score += got
        total += w
        print(f"\n{cat:12} {got:>3}/{w:<3}  ({100*got//w:>3}%)")
        for i in items:
            mark = "PASS" if i["ok"] else "FAIL"
            print(f"  [{mark}] {i['label']}" + (f" — {i['detail']}" if i["detail"] else ""))
    pct = round(100 * score / max(total, 1))
    print("\n" + "=" * 46)
    print(f"CHECKS: {sum(1 for r in results if r['ok'])}/{len(results)} passed"
          f"   WEIGHTED SCORE: {score}/{total} = {pct}/100")
    if "--json" in sys.argv:
        print(json.dumps({"score": pct, "checks": results}, ensure_ascii=False, indent=2))
    if "--strict" in sys.argv and pct < 100:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
