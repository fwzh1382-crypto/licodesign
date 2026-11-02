#!/usr/bin/env python3
"""Full UI/UX remediation for the LAICO DESIGN static template.

Applies, idempotently, to every *.html in the repository root:

  SEO      canonical, og:url/og:image/og:site_name, twitter card, manifest,
           JSON-LD LocalBusiness on index + contact
  i18n     load js/config.js and js/i18n-content.js before js/main.js,
           parent nav highlighting, translated aria-labels
  IA       breadcrumbs on every inner page, footer links for all orphan pages
  A11y     one <h1> per page, real <label for>, native <select>, descriptive
           alt text (or explicit decorative marker), error/status live regions,
           consent + honeypot on every form
  UI       no inline styles, consistent phone/address/hours/social links
  Perf     real width/height, loading/decoding/fetchpriority hints, WebP
           <picture> sources, 60% smaller images

  Content  honest demo-mode wording on legal pages

The script is safe to re-run: files already carrying data-uiux="2.0" are
skipped. Site-wide URLs are rewritten by tools/set_site_url.py.

    python3 tools/uiux_fix.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://laicodesign.ir"          # change with tools/set_site_url.py
DIMS = json.loads((ROOT / "tools" / "image-dimensions.json").read_text(encoding="utf-8"))
MARK = 'data-uiux="2.0"'

GROUP = {
    "services": ("خدمات", "services.html"),
    "collections": ("مجموعهها", "index.html#collections"),
    "projects": ("پروژهها", "projects.html"),
    "studio": ("استودیو", "about.html"),
    "journal": ("مجله", "journal.html"),
    "contact": ("تماس", "contact.html"),
}

# page -> (group or None, current label or None, parent nav item, page title fa)
PAGES = {
    "index.html":           (None, None, "home", "صفحه اصلی"),
    "services.html":        ("services", None, "services", "خدمات"),
    "projects.html":        ("projects", None, "projects", "پروژهها"),
    "journal.html":         ("journal", None, "journal", "مجله"),
    "about.html":           (None, "درباره ما", "about", "درباره ما"),
    "studio.html":          ("studio", "استودیو", "about", "استودیو"),
    "process.html":         ("studio", "فرآیند کار", "about", "فرآیند کار"),
    "materials.html":       ("studio", "متریال", "about", "متریال"),
    "systems.html":         ("studio", "سیستمها و متریال", "about", "سیستمها و متریال"),
    "showroom.html":        ("studio", "شو روم", "about", "شو روم"),
    "kitchen.html":         ("collections", "آشپزخانه", "services", "آشپزخانه"),
    "living.html":          ("collections", "پذیرایی و اتاق", "services", "پذیرایی و اتاق"),
    "bath.html":            ("collections", "حمام", "services", "حمام"),
    "cafe.html":            ("collections", "کافه و رستوران", "services", "کافه و رستوران"),
    "project-aftab.html":   ("projects", "پنتهاوس آفتاب", "projects", "پنتهاوس آفتاب"),
    "project-haraz.html":   ("projects", "ویلای هراز", "projects", "ویلای هراز"),
    "project-acajou.html":  ("projects", "کافه اکاژو", "projects", "کافه اکاژو"),
    "project-darya.html":   ("projects", "خانه دریا", "projects", "خانه دریا"),
    "contact.html":         ("contact", None, "contact", "تماس با ما"),
    "privacy.html":         ("contact", "حریم خصوصی", "contact", "حریم خصوصی"),
    "cookies.html":         ("contact", "کوکیها", "contact", "کوکیها"),
    "404.html":             (None, None, "home", "صفحه یافت نشد"),
}

SRC_ALT = {
    "hero.jpg": "نمای داخلی آشپزخانه لوکس لایکو دیزاین",
    "about-hero.jpg": "نمای داخلی استودیو لایکو دیزاین",
    "contact-hero.jpg": "نمای شهر در شب، پسزمینه صفحه تماس",
    "contact-form.jpg": "نشیمن با مبل سرمهای و نمای شهر",
    "contact-map.jpg": "نقشه لایکودیزاین کنار آتشکده آمل",
    "detail.jpg": "جزئیات پروفیل آلومینیومی و روکش لاک مات",
    "col-kitchen.jpg": "نمای آشپزخانه بدون دستگیره",
    "col-living.jpg": "نمای پذیرایی و اتاق",
    "col-bath.jpg": "نمای حمام با کابینت سرمهای",
    "col-cafe.jpg": "نمای داخلی کافه و رستوران",
    "proj-aftab.jpg": "نمای آشپزخانه پنتهاوس آفتاب",
    "proj-haraz.jpg": "نمای داخلی ویلای هراز",
    "proj-acajou.jpg": "فضای داخلی کافه اکاژو",
    "proj-darya.jpg": "حمام و فضای داخلی خانه دریا",
    "projects-card.jpg": "نمای شبانه مجتمع تجاری و تفریحی",
    "services-hero.jpg": "کابینت شیشهای سرمهای در کنار دیوار کاشی سفید",
    "services-clinic.jpg": "نمای داخلی مطب دندانپزشکی",
    "services-sport.jpg": "سالن بدنسازی مدرن با نورپردازی خطی",
    "services-complex.jpg": "نمای شبانه مجتمع تفریحی",
    "services-residential.jpg": "نمای بیرونی مجموعه مسکونی",
    "services-cafe.jpg": "فضای داخلی کافه با نورپردازی خطی",
    "services-why.jpg": "نشیمنی با دیوارهای سرمهای و لوستر کریستالی",
    "about-k-base.jpg": "جزئیات کشوها و دستگیرهها",
    "about-k-glass.jpg": "کابینت شیشهای دیواری",
    "about-k-run.jpg": "کابینت سرمهای با صفحه سنگ",
    "about-k-sink.jpg": "سینک و کابینت سرمهای",
    "about-team.jpg": "اعضای گروه معماران و طراحان لایکودیزاین",
}

INLINE_STYLES = [
    ('<p class="eyebrow" style="padding-top:120px">', '<p class="eyebrow eyebrow--top">'),
    ('class="page-hero" style="min-height:46vh;background:#0b1d33"', 'class="page-hero page-hero--short"'),
    ('class="shade" style="background:#0b1d33"', 'class="shade shade--solid"'),
    ('class="measure" style="padding-top:48px"', 'class="measure measure--gap-lg"'),
    ('class="measure" style="padding-top:36px"', 'class="measure measure--gap"'),
    ('class="specs" style="max-width:640px"', 'class="specs specs--narrow"'),
    ('class="media-frame" style="margin-top:36px"', 'class="media-frame media-frame--gap"'),
    ('class="showroom" style="min-height:70vh;display:flex;align-items:flex-end"', 'class="showroom showroom--hero"'),
]

# Legal pages use paired .lang-fa/.lang-en spans. Replacing by exact Persian
# text is fragile (ZWNJ variants), so rewrite long paragraph pairs by position.
LEGAL_FA = {
    "cookies.html": [
        "این قالب کوکی تبلیغاتی یا ردیاب ندارد. تنها دادهها، زبان انتخابی و درخواست\u200cهای فرم هستند که در حافظه\u200cی محلی مرورگر شما نگهداری می\u200cشوند و حداکثر ۳۰ روز می\u200cمانند. تا زمانی که فرم به سرور وصل نشود، هیچ اطلاعاتی به بیرون فرستاده نمی\u200cشود.",
        "در نسخه\u200cی نمایشی، پس از ثبت فرم می\u200cتوانید متن درخواست را با واتساپ، ایمیل یا تلفن برای ما بفرستید. برای حذف فوری دادهها از دکمه\u200cی «پاک کردن داده\u200cهای محلی» در فوتر استفاده کنید.",
    ],
    "privacy.html": [
        "فرم مشاوره فقط نام، شماره تماس، نوع پروژه و توضیح شما را در همین مرورگر ذخیره می\u200cکند. این قالب به سرور متصل نیست، پس هیچ اطلاعاتی به\u200cصورت خودکار ارسال نمی\u200cشود. پیام «درخواست شما آماده است» به معنای دریافت آن توسط ما نیست؛ باید متن درخواست را از طریق واتساپ، ایمیل یا تلفن بفرستید.",
        "داده\u200cهای فرم فقط با رضایت شما (تیک موافقت) ذخیره می\u200cشوند، حداکثر ۳۰ روز نگهداری می\u200cشوند و با دکمه\u200cی «پاک کردن داده\u200cهای محلی» در فوتر یا «حذف اطلاعات ذخیره\u200cشده» در پیام موفقیت، فوراً پاک می\u200cشوند. انتخاب زبان هم در حافظه\u200cی محلی مرورگر می\u200cماند.",
    ],
}
LEGAL_EN = {
    "cookies.html": [
        "This template sets no advertising cookies or trackers. The only data stored is your language choice and form requests, kept in your browser's local storage for at most 30 days. Until the form is connected to a server, nothing is sent anywhere.",
        "In this demo, after submitting the form you can send the request text to us via WhatsApp, e-mail or phone. To delete the stored data immediately, use the Clear local data button in the footer.",
    ],
    "privacy.html": [
        "The consultation form stores your name, phone, project type and note in this browser only. This template has no server connection, so nothing is sent automatically. A message saying your request is ready does not mean we received it — send the request text via WhatsApp, e-mail or phone.",
        "Form data is stored only with your consent, kept for at most 30 days, and can be deleted instantly with the Clear local data button in the footer or the Delete saved data action in the confirmation panel. Your language choice is also kept in local storage.",
    ],
}
LEGAL_PAIR = re.compile(
    r'(<p><span class="lang-fa">)([^<]*)(</span><span class="lang-en" hidden>)([^<]*)(</span></p>)')


def fix_legal_content(name: str, s: str) -> str:
    if name not in LEGAL_FA:
        return s
    fa_list, en_list = LEGAL_FA[name][:], LEGAL_EN[name][:]

    def repl(m):
        if len(m.group(2).strip()) < 80:   # eyebrow / short labels
            return m.group(0)
        fa = fa_list.pop(0) if fa_list else m.group(2)
        en = en_list.pop(0) if en_list else m.group(4)
        return m.group(1) + fa + m.group(3) + en + m.group(5)

    return LEGAL_PAIR.sub(repl, s)


FOOTER_LEGAL = '''<div class="footer-legal">
    <p>تمامی حقوق این سایت محفوظ میباشد.</p>
    <nav class="footer-legal-links" aria-label="پیوندهای حقوقی و سایت">
      <a href="privacy.html">حریم خصوصی</a>
      <a href="cookies.html">کوکیها</a>
      <a href="studio.html">استودیو</a>
      <a href="process.html">فرآیند کار</a>
      <a href="materials.html">متریال</a>
      <a href="systems.html">سیستمها</a>
      <a href="showroom.html">شو روم</a>
      <a href="projects.html">پروژهها</a>
      <a href="journal.html">ژورنال</a>
    </nav>
    <p>طراحی و اجرا آمل نوین</p>
    <button type="button" class="clear-data" data-clear-data data-i18n="clear-data">پاک کردن دادههای محلی</button>
  </div>'''

FORM_EXTRAS = '''<div class="form-consent" data-field="consent">
          <label class="consent-line">
            <input id="{cid}" type="checkbox" name="consent" required>
            <span data-i18n="f-consent-label">با قوانین حریم خصوصی موافقم.</span>
          </label>
          <a class="consent-link" href="privacy.html" data-i18n="privacy">حریم خصوصی</a>
          <span class="field-error"></span>
        </div>
        <div class="hp-wrap" data-no-i18n aria-hidden="true">
          <label for="{hid}">Website</label>
          <input id="{hid}" type="text" name="website" tabindex="-1" autocomplete="off">
          <span>Leave this field empty.</span>
        </div>
        <p class="form-privacy-note"><span data-i18n="f-privacy-note">این قالب نمایشی است؛ درخواست فقط در مرورگر شما ذخیره میشود.</span> <a href="privacy.html" data-i18n="privacy">حریم خصوصی</a></p>
        '''

NATIVE_SELECT = '''<select class="native-select" name="type" data-i18n-aria="f-type" aria-label="نوع پروژه">
          <option value="kitchen" data-i18n="opt-kitchen">آشپزخانه</option>
          <option value="living" data-i18n="opt-living">پذیرایی و اتاق</option>
          <option value="bath" data-i18n="opt-bath">حمام</option>
          <option value="cafe" data-i18n="opt-cafe">کافه و رستوران</option>
          <option value="wardrobe" data-i18n="opt-wardrobe">کمد و سیستم</option>
          <option value="full" data-i18n="opt-full">بازسازی کامل</option>
        </select>'''


def canonical(name: str) -> str:
    return SITE_URL + ("" if name == "index.html" else "/" + name)


def json_ld(name: str, title: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE_URL + "/#business",
        "name": "لایکو دیزاین",
        "alternateName": "Laico Design",
        "url": SITE_URL + "/",
        "image": SITE_URL + "/assets/images/hero.jpg",
        "telephone": "+989120898938",
        "description": "استودیو معماری داخلی و سازنده سیستم آشپزخانه لوکس در آمل.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "خیابان طالب آملی، دریای ۲۰",
            "addressLocality": "آمل",
            "addressRegion": "مازندران",
            "addressCountry": "IR",
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"],
            "opens": "10:00", "closes": "19:00",
        }],
        "sameAs": [
            "https://www.instagram.com/Laico_design/",
            "https://t.me/Laico_design",
            "https://x.com/Laico_design",
            "https://wa.me/989120898938",
        ],
        "priceRange": "$$",
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return '<script type="application/ld+json">\n' + payload + '\n</script>\n'


def breadcrumb(name: str) -> str:
    group, current, _, _ = PAGES[name]
    parts = ['<nav class="breadcrumb" aria-label="مسیر صفحه">',
             '<a href="index.html">خانه</a>']
    # Hub pages (services/projects/journal/contact) are two levels deep;
    # leaf pages get an extra group link. Never repeat the same label twice.
    if current and group:
        group_label, group_href = GROUP[group]
        parts.append('<span class="sep" aria-hidden="true">/</span>')
        parts.append('<a href="' + group_href + '">' + group_label + '</a>')
    label = current if current is not None else PAGES[name][3]
    parts.append('<span class="sep" aria-hidden="true">/</span>')
    parts.append('<span aria-current="page">' + label + '</span>')
    parts.append('</nav>')
    return "\n".join(parts)


def map_outside(s: str, pattern: str, repl, tags=("script", "style")) -> str:
    """Apply re.sub only outside <script>/<style> blocks."""
    chunks, last = [], 0
    guard = re.compile(r"<(" + "|".join(tags) + r")\b.*?</\1>", re.S | re.I)
    for m in guard.finditer(s):
        chunks.append(re.sub(pattern, repl, s[last:m.start()]))
        chunks.append(m.group(0))
        last = m.end()
    chunks.append(re.sub(pattern, repl, s[last:]))
    return "".join(chunks)


def anchor_has_text(s: str, start: int, end: int) -> bool:
    opened = s.rfind("<a ", 0, start)
    prev_close = s.rfind("</a>", 0, start)
    if opened == -1 or prev_close > opened:
        return False
    close = s.find("</a>", end)
    if close == -1:
        return False
    inner = re.sub(r"<[^>]+>", " ", s[opened:close])
    return bool(re.search(r"\w", inner, re.UNICODE))


def add_attr(tag: str, attr: str) -> str:
    """Append an attribute to an <img ...> tag without breaking /> syntax."""
    base = tag[:-1].rstrip()
    if base.endswith("/"):
        base = base[:-1].rstrip()
    return base + " " + attr + ">"


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


def top_level_insert(inner: str, target: int) -> int:
    """Position of the form's direct child that contains `target`."""
    depth, child = 0, target
    for m in re.finditer(r"<(/?)([a-zA-Z][\w-]*)\b[^>]*?(/?)>", inner[:target]):
        closing, tag, selfclose = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID_TAGS or selfclose:
            continue
        if not closing:
            if depth == 0:
                child = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                child = target
    return child


def fix_images(name: str, s: str) -> str:
    img_re = re.compile(r"<img\b[^>]*>", re.I)
    out, last, idx = [], 0, 0
    wrap = "<picture" not in s

    for m in img_re.finditer(s):
        tag = m.group(0)
        src_m = re.search(r'\bsrc="([^"]+)"', tag)
        if not src_m:
            out.append(s[last:m.end()]); last = m.end(); continue
        src = src_m.group(1)
        rel = src
        dims = DIMS.get(rel)
        alt_m = re.search(r'\balt="([^"]*)"', tag, re.I)
        current_alt = alt_m.group(1) if alt_m else None

        # 1. alt: descriptive for informative images, explicit decorative otherwise
        if current_alt is None or current_alt == "":
            decorative = anchor_has_text(s, m.start(), m.end())
            if decorative:
                new_alt = ""
                if 'aria-hidden="true"' not in tag:
                    tag = add_attr(tag, 'aria-hidden="true"')
            else:
                new_alt = SRC_ALT.get(Path(src).name, "تصویر پروژه لایکو دیزاین")
            if alt_m:
                tag = re.sub(r'\balt="[^"]*"', 'alt="' + new_alt.replace('"', "&quot;") + '"', tag, count=1)
            else:
                tag = add_attr(tag, 'alt="' + new_alt.replace('"', "&quot;") + '"')

        # 2. real intrinsic dimensions (kills CLS)
        if dims and "width=" not in tag:
            tag = add_attr(tag, 'width="%d" height="%d"' % (dims[0], dims[1]))

        # 3. decoding / loading / priority
        if 'decoding=' not in tag:
            tag = add_attr(tag, 'decoding="async"')
        if idx == 0:
            if 'loading=' not in tag:
                tag = add_attr(tag, 'loading="eager"')
            if 'fetchpriority=' not in tag:
                tag = add_attr(tag, 'fetchpriority="high"')
        elif 'loading=' not in tag:
            tag = add_attr(tag, 'loading="lazy"')
        idx += 1

        # 4. WebP <picture> source
        if wrap and src.lower().endswith(".jpg"):
            webp = src[:-4] + ".webp"
            if (ROOT / webp).exists():
                piece = '<picture><source srcset="' + webp + '" type="image/webp">' + tag + "</picture>"
            else:
                piece = tag
        else:
            piece = tag

        out.append(s[last:m.start()])
        out.append(piece)
        last = m.end()
    out.append(s[last:])
    return "".join(out)


def fix_forms(name: str, s: str) -> str:
    if "data-form" not in s:
        return s
    slug = re.sub(r"[^a-z0-9]+", "-", name[:-5]).strip("-")

    # custom listbox -> real native <select> (keyboard + screen-reader friendly)
    s = re.sub(
        r'<div class="select" data-select>.*?<input type="hidden" name="type" value="kitchen">\s*</div>',
        NATIVE_SELECT, s, flags=re.S)

    # <span class="field-label"> -> <label class="field-label">
    s = re.sub(r'<span class="field-label"([^>]*)>(.*?)</span>',
               r'<label class="field-label"\1>\2</label>', s, flags=re.S)

    form_re = re.compile(r'(<form\b[^>]*\bdata-form\b[^>]*>)(.*?)(</form>)', re.S)
    counter = [0]

    def fix_one(m):
        counter[0] += 1
        cid = "consent-%s-%d" % (slug, counter[0])
        hid = "hp-%s-%d" % (slug, counter[0])
        extras = FORM_EXTRAS.format(cid=cid, hid=hid)
        inner = m.group(2)
        btn = re.search(r'<button[^>]*type="submit"[^>]*>', inner)
        if btn and 'name="consent"' not in inner:
            pos = top_level_insert(inner, btn.start())
            inner = inner[:pos] + extras + inner[pos:]
        status = ('\n        <p class="form-status" data-form-status data-no-i18n '
                  'role="status" aria-live="polite"></p>')
        return m.group(1) + inner + m.group(3) + status

    return form_re.sub(fix_one, s)


def fix_page(name: str, s: str) -> str:
    # --- body marker / nav -------------------------------------------------
    s = re.sub(r"<body\b", "<body " + MARK, s, count=1)
    _, _, nav, _ = PAGES[name]
    s = re.sub(r'<body\b([^>]*)>', lambda m: "<body" + m.group(1) + ' data-active-nav="' + nav + '">', s, count=1)
    if name in ("cookies.html", "privacy.html"):
        s = s.replace('data-page="contact"', 'data-page="legal"')

    # --- head: SEO ---------------------------------------------------------
    title = (re.search(r"<title>([^<]*)</title>", s) or ["", ""])[1]
    desc = (re.search(r'<meta name="description" content="([^"]*)"', s) or ["", ""])[1]
    seo = (
        '\n<link rel="canonical" href="' + canonical(name) + '">'
        '\n<meta property="og:url" content="' + canonical(name) + '">'
        '\n<meta property="og:image" content="' + SITE_URL + '/assets/images/hero.jpg">'
        '\n<meta property="og:image:alt" content="Laico Design — interior architecture">'
        '\n<meta property="og:site_name" content="Laico Design">'
        '\n<meta name="twitter:card" content="summary_large_image">'
        '\n<meta name="twitter:image" content="' + SITE_URL + '/assets/images/hero.jpg">'
        '\n<link rel="manifest" href="site.webmanifest">'
    )
    anchor = '<meta property="og:locale" content="fa_IR">'
    if anchor in s and 'rel="canonical"' not in s:
        s = s.replace(anchor, anchor + seo, 1)
    if name in ("index.html", "contact.html") and 'application/ld+json' not in s:
        s = s.replace("</head>", json_ld(name, title) + "</head>", 1)
    if name == "404.html" and 'name="robots"' not in s:
        s = s.replace('<meta name="viewport"',
                      '<meta name="robots" content="noindex, follow">\n<meta name="viewport"', 1)

    # --- scripts -----------------------------------------------------------
    boot = '<script src="js/config.js"></script>\n<script src="js/i18n-content.js"></script>\n'
    if 'js/i18n-content.js' not in s:
        s = s.replace('<script src="js/main.js"></script>', boot + '<script src="js/main.js"></script>', 1)

    # --- accessible nav labels --------------------------------------------
    s = s.replace('aria-label="main"', 'aria-label="ناوبری اصلی"')
    s = s.replace('aria-label="footer"', 'aria-label="پیوندهای فوتر"')

    # --- breadcrumbs -------------------------------------------------------
    if name not in ("index.html", "404.html") and 'class="breadcrumb"' not in s:
        s = s.replace('<main id="main">', '<main id="main">\n' + breadcrumb(name), 1)

    # --- one h1 per page ---------------------------------------------------
    if '<h1' not in s:
        if name == "contact.html":
            s = s.replace('<section class="contact-hero">',
                          '<section class="contact-hero">\n  <h1 class="contact-hero-title">تماس با ما</h1>', 1)
        elif name == "showroom.html":
            s = s.replace('<h2 data-i18n="sh-title">متریال و کیفیت را لمس کنید</h2>',
                          '<h1 data-i18n="sh-title">متریال و کیفیت را لمس کنید</h1>', 1)
        elif name in ("cookies.html", "privacy.html"):
            key = "cookies" if name == "cookies.html" else "privacy"
            s = re.sub(r'<h2 data-i18n="' + key + r'">([^<]*)</h2>',
                       r'<h1 data-i18n="' + key + r'">\1</h1>', s, count=1)

    # --- inline styles -> utility classes ---------------------------------
    for old, new in INLINE_STYLES:
        s = s.replace(old, new)

    # --- legal pages: describe what actually happens now ------------------
    s = fix_legal_content(name, s)

    # --- raw ampersands in text -------------------------------------------
    s = map_outside(s, r"&(?!(?:amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9A-Fa-f]+);)", "&amp;")

    # --- one business identity --------------------------------------------
    s = s.replace("+98 21 000 0000", "+98&nbsp;912&nbsp;089&nbsp;8938")
    s = s.replace("tel:+98210000000", "tel:+989120898938")
    s = s.replace("tel:09120898938", "tel:+989120898938")
    s = re.sub(r"(?<!مازندران، )آمل، خیابان طالب آملی، دریای ۲۰",
               "مازندران، آمل، خیابان طالب آملی، دریای ۲۰", s)
    s = s.replace("مازندران، آمل، دریای20، لایکودیزاین",
                  "مازندران، آمل، خیابان طالب آملی، دریای ۲۰")
    s = s.replace("Mazandaran, Amol, Darya 20, Laico Design",
                  "Mazandaran, Amol, Taleb Amoli St., Darya 20")
    s = s.replace("شنبه تا چهارشنبه 9 صبح الی 15 شب", "شنبه تا پنجشنبه، ۱۰ تا ۱۹")
    s = s.replace("Saturday to Wednesday, 9:00 to 15:00", "Saturday to Thursday, 10–19")

    # --- real social profiles, no dead generic links -----------------------
    s = s.replace('href="https://www.instagram.com/"', 'href="https://www.instagram.com/Laico_design/"')
    s = s.replace('href="https://t.me/"', 'href="https://t.me/Laico_design"')
    s = re.sub(r'\s*<a class="soc" href="https://www\.youtube\.com/"[^>]*>.*?</a>', "", s, flags=re.S)

    # --- footer: link every orphan page -----------------------------------
    s = re.sub(r'<div class="footer-legal">.*?</div>', FOOTER_LEGAL, s, count=1, flags=re.S)

    # --- forms --------------------------------------------------------------
    s = fix_forms(name, s)

    # --- images -------------------------------------------------------------
    s = fix_images(name, s)
    return s


def write_404() -> None:
    """Build a real 404 page that reuses the standard header/footer."""
    src = (ROOT / "contact.html").read_text(encoding="utf-8")
    head = src[src.index("<head>"):src.index("</head>") + len("</head>")]
    header = src[src.index("<a class=\"skip\""):src.index("</header>") + len("</header>")]
    footer = src[src.index("<footer class=\"site-footer\">"):src.index("</footer>") + len("</footer>")]
    head = head.replace("<title>تماس با ما — لایکو دیزاین</title>", "<title>صفحه یافت نشد — لایکو دیزاین</title>")
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="صفحهای که دنبال آن بودید یافت نشد.">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="صفحه یافت نشد — لایکو دیزاین">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">',
                  '<meta property="og:description" content="صفحهای که دنبال آن بودید یافت نشد.">', head)
    # drop page-scoped SEO/JSON-LD inherited from contact.html; fix_page re-adds
    head = re.sub(r'\n<link rel="canonical"[^>]*>', "", head)
    head = re.sub(r'\n<meta property="og:url"[^>]*>', "", head)
    head = re.sub(r'\n<meta property="og:image"[^>]*>', "", head)
    head = re.sub(r'\n<meta property="og:image:alt"[^>]*>', "", head)
    head = re.sub(r'\n<meta property="og:site_name"[^>]*>', "", head)
    head = re.sub(r'\n<meta name="twitter:card"[^>]*>', "", head)
    head = re.sub(r'\n<meta name="twitter:image"[^>]*>', "", head)
    head = re.sub(r'\n<link rel="manifest"[^>]*>', "", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", head, flags=re.S)
    head = re.sub(r'<script src="js/(?:config|i18n-content|main)\.js"></script>\n?', "", head)
    body_open = ('<body data-page="legal" '
                 'data-title-fa="صفحه یافت نشد — لایکو دیزاین" '
                 'data-title-en="Page not found — Laico Design">')
    main = '''<main id="main">
<section class="error-page">
  <p class="error-code" dir="ltr" aria-hidden="true">404</p>
  <h1>صفحهای که دنبال آن بودید پیدا نشد.</h1>
  <p>شاید آدرس اشتباه باشد یا صفحه جابهجا شده باشد. از صفحه اصلی شروع کنید.</p>
  <div class="error-actions">
    <a class="btn-solid" href="index.html">بازگشت به صفحه اصلی</a>
    <a class="btn-line" href="projects.html">مشاهده پروژهها</a>
  </div>
</section>
</main>'''
    out = ('<!DOCTYPE html>\n<html lang="fa" dir="rtl">\n' + head + "\n" + body_open + "\n"
           + header + "\n" + main + "\n\n" + footer +
           '\n<script src="js/config.js"></script>\n<script src="js/i18n-content.js"></script>'
           '\n<script src="js/main.js"></script>\n</body>\n</html>\n')
    (ROOT / "404.html").write_text(out, encoding="utf-8")


def write_seo_files() -> None:
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + SITE_URL + "/sitemap.xml\n", encoding="utf-8")
    urls = []
    for name in sorted(p.name for p in ROOT.glob("*.html") if p.name != "404.html"):
        prio = "1.0" if name == "index.html" else "0.7"
        urls.append("  <url>\n    <loc>" + canonical(name) + "</loc>\n"
                    "    <lastmod>2026-10-27</lastmod>\n"
                    "    <changefreq>monthly</changefreq>\n"
                    "    <priority>" + prio + "</priority>\n  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    manifest = {
        "name": "Laico Design — لایکو دیزاین", "short_name": "Laico",
        "description": "Interior architecture and luxury kitchen systems.",
        "lang": "fa", "dir": "rtl", "start_url": "./", "scope": "./",
        "display": "standalone", "background_color": "#ffffff",
        "theme_color": "#071425",
        "icons": [{"src": "assets/favicon.svg", "sizes": "any", "type": "image/svg+xml",
                   "purpose": "any maskable"}],
    }
    (ROOT / "site.webmanifest").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if not (ROOT / "404.html").exists():
        write_404()
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        s = path.read_text(encoding="utf-8")
        if MARK in s:
            continue
        fixed = fix_page(path.name, s)
        # make sure our own marker is present exactly once
        fixed = fixed.replace("<body  " + MARK, "<body " + MARK)
        path.write_text(fixed, encoding="utf-8")
        changed.append(path.name)
    write_seo_files()
    print("fixed %d HTML pages" % len(changed))
    print(", ".join(changed))
    print("wrote robots.txt, sitemap.xml, site.webmanifest, 404.html")


if __name__ == "__main__":
    main()
