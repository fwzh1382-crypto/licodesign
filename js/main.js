/* LAICO DESIGN — interactions, language, forms, accessibility
 *
 * Rewritten as part of the full UI/UX remediation. Behaviour that used to be
 * spread over 21 copied pages now lives here, driven by js/config.js and
 * js/i18n-content.js. Everything degrades gracefully without JavaScript.
 */
(function () {
  "use strict";

  var CFG = window.LAICO_CONFIG || {};
  var T9N = window.LAICO_T9N || {};
  var RETENTION_MS = (CFG.requestRetentionDays || 30) * 24 * 60 * 60 * 1000;
  var STORE_KEY = "laico-requests";

  /* ------------------------------------------------------------------ *
   * 1. UI dictionary — every string that JavaScript injects or changes.
   *    fa and en MUST have identical keys (checked by tools/uiux_audit.py).
   * ------------------------------------------------------------------ */
  var dict = {
    fa: {
      "skip": "رد شدن از منو",
      "nav-home": "صفحه اصلی", "nav-services": "خدمات", "nav-projects": "پروژه‌ها",
      "nav-journal": "مجله", "nav-about": "درباره ما", "nav-contact": "تماس با ما",
      "cta": "درخواست مشاوره", "menu": "منو", "close": "بستن",
      "hero-kicker": "معماری داخلی • سیستم آشپزخانه لوکس",
      "hero-1": "از ایده تا اجرا با لایکو", "hero-2": "دیزاین",
      "hero-lede": "لایکو دیزاین؛ طراحی و اجرای آشپزخانه، پذیرایی و اتاق، حمام و فضاهای کافه-رستوران با زبان مینیمال و متریال صادق.",
      "col-eye": "۰۱ — مجموعه‌ها", "col-title": "چهار فضا، یک استاندارد ساخت",
      "col-all": "همه مجموعه‌ها", "col-kitchen": "آشپزخانه", "col-living": "پذیرایی و اتاق",
      "col-bath": "حمام", "col-cafe": "کافه و رستوران",
      "prj-eye": "۰۲ — پروژه‌های منتخب", "prj-title": "نمونه کارها، امضای کیفیت",
      "prj-all": "آرشیو کامل", "tag-kitchen": "آشپزخانه", "tag-interior": "معماری داخلی",
      "tag-cafe": "کافه و رستوران", "tag-bath": "حمام",
      "p-firuzkuh": "پروژه کوهستانی فیروزکوه", "p-dozak": "مهد کودک نقش دوزک",
      "p-club": "باشگاه ورزشی آمل", "p-cafe-amol": "طراحی کافه آمل",
      "m-firuzkuh": "آسور • ۱۰۰ متر بنا", "m-dozak": "آمل، آفتاب ۳۱ • ۱۴۰۲",
      "m-club": "۱۵۵ مترمربع • ۱۴۰۵", "m-cafe-amol": "آمل • طراحی داخلی",
      "tag-mountain": "کوهستانی", "tag-edu": "فضای آموزشی", "tag-sport": "باشگاه ورزشی",
      "phone-v": "۰۹۱۲ ۰۸۹ ۸۹۳۸",
      "hero-1": "لایکودیزاین،", "hero-2": "فراتر از طراحی",
      "why-eye": "۰۳ — استودیو",
      "why-quote": "چرا لایکو دیزاین؟ چون از اولین اسکچ تا آخرین پیچ نصب، یک تیم و یک استاندارد پشت کار شماست؛ متریال صادق، اجرای دقیق و تعهدی که سال‌ها بعد از تحویل هم همراه شما میماند.",
      "st-projects": "پروژه اجراشده", "st-years": "سال تجربه", "st-brands": "برند اروپایی",
      "sys-eye": "۰۴ — سیستم‌ها و متریال", "sys-title": "بدون دستگیره، بدون درز اضافی",
      "sys-body": "سیستم‌های آشپزخانه، کمد و پذیرایی لایکو بر پایه پروفیل‌های آلومینیومی، روکش‌های لاک مات و صفحات سنگ طبیعی طراحی میشوند؛ با تلورانس اجرایی زیر یک میلیمتر.",
      "spec-finish": "روکش", "spec-finish-v": "لاک مات، چوب راش، گرس porcelain",
      "spec-hw": "سختافزار", "spec-hw-v": "لولای آرامبند، ریل فول بلوم",
      "spec-w": "ضمانت", "spec-w-v": "۱۰ سال ساخت، ۲ سال خدمات",
      "sh-eye": "۰۵ — شو روم", "sh-title": "متریال و کیفیت را لمس کنید",
      "sh-body": "بازدید از شو روم با هماهنگی قبلی؛ همراه با مشاوره فنی و انتخاب پالت متریال.",
      "addr": "آدرس", "addr-v": "آمل، دریای ۲۰", "hours": "ساعات",
      "hours-v": "شنبه تا پنجشنبه، ۱۰ تا ۱۹", "phone": "تماس",
      "form-eye": "۰۶ — شروع پروژه", "form-1": "چطور میتوانیم", "form-2": "همکاری کنیم؟",
      "form-body": "فرم را پر کنید؛ تیم طراحی ظرف ۴۸ ساعت کاری برای جلسه اول با شما تماس میگیرد.",
      "f-name": "نام و نام خانوادگی", "f-phone": "شماره تماس", "f-type": "نوع پروژه",
      "f-note": "توضیح کوتاه", "f-note-ph": "متراژ، شهر، بازه زمانی",
      "about-ph-note": "متن پیام را بنویسید..", "f-send": "ارسال درخواست",
      "f-ok-title": "درخواست شما ثبت شد.",
      "f-ok-body": "تیم طراحی ظرف ۴۸ ساعت کاری برای جلسه اول با شما تماس میگیرد.",
      "err-name": "نام را بنویسید.", "err-phone": "شماره موبایل معتبر وارد کنید.",
      "err-note": "چند خط درباره فضا بنویسید.",
      "opt-kitchen": "آشپزخانه", "opt-living": "پذیرایی و اتاق", "opt-bath": "حمام",
      "opt-cafe": "کافه و رستوران", "opt-wardrobe": "کمد و سیستم", "opt-full": "بازسازی کامل",
      "foot-about": "مجموعه تخصصی معماری داخلی و سیستم لوکس آشپزخانه.",
      "foot-col": "مجموعهها", "foot-studio": "استودیو", "foot-contact": "تماس",
      "foot-about-us": "درباره ما", "foot-process": "فرآیند کار", "foot-journal": "ژورنال",
      "foot-collab": "همکاری", "foot-material": "متریال", "foot-ig": "اینستاگرام",
      "foot-wa": "واتساپ", "copy": "© ۱۴۰۵ لایکو دیزاین — تمام حقوق محفوظ است",
      "privacy": "حریم خصوصی", "cookies": "کوکیها", "filter-all": "همه",
      "next": "پروژه بعد", "book": "رزرو بازدید", "read": "ادامه",
      /* --- new keys: form lifecycle / status / navigation --- */
      "f-demo-title": "درخواست شما آماده است.",
      "f-demo-body": "این قالب به سرور متصل نیست، بنابراین چیزی بهصورت خودکار ارسال نشد. متن درخواست آماده است؛ آن را از یکی از راههای زیر به دست ما برسانید.",
      "f-send-wa": "ارسال در واتساپ", "f-send-mail": "ارسال با ایمیل",
      "f-call": "تماس تلفنی", "f-copy": "کپی متن درخواست", "f-copied": "کپی شد",
      "f-copy-fail": "کپی نشد؛ متن را دستی انتخاب کنید.",
      "f-edit": "ویرایش درخواست", "f-clear": "حذف اطلاعات ذخیرهشده",
      "f-cleared": "اطلاعات محلی حذف شد.", "f-sending": "در حال ارسال…",
      "f-error": "ارسال انجام نشد. دوباره تلاش کنید یا از واتساپ استفاده کنید.",
      "f-subject": "درخواست مشاوره — لایکو دیزاین",
      "f-consent-err": "لطفاً رضایت خود را اعلام کنید.",
      "f-consent-label": "با قوانین حریم خصوصی موافقم.",
      "f-privacy-note": "این قالب نمایشی است؛ درخواست فقط در مرورگر شما ذخیره میشود.",
      "st-invalid": "لطفاً خطاهای فرم را اصلاح کنید.",
      "st-sending": "در حال ارسال درخواست…",
      "st-ok": "درخواست ارسال شد.",
      "st-demo": "پیشنمایش: درخواست فقط در همین مرورگر ذخیره شد.",
      "st-cleared": "اطلاعات محلی حذف شد.",
      "clear-data": "پاک کردن دادههای محلی",
      "filter-status": "{n} مورد نمایش داده شد.",
      "bc-label": "مسیر صفحه",
      "external": "لینک خارجی",
      "lang-label": "زبان"
    },
    en: {
      "skip": "Skip to content",
      "nav-home": "Home", "nav-services": "Services", "nav-projects": "Projects",
      "nav-journal": "Journal", "nav-about": "About", "nav-contact": "Contact",
      "cta": "Book a consultation", "menu": "Menu", "close": "Close",
      "hero-kicker": "Interior architecture • Luxury kitchen system",
      "hero-1": "From the idea to the last screw,", "hero-2": "with Laico Design",
      "hero-lede": "Laico Design plans and builds kitchens, living rooms, baths, and café spaces in a minimal language, with honest materials.",
      "col-eye": "01 — Collections", "col-title": "Four rooms, one standard of making",
      "col-all": "All collections", "col-kitchen": "Kitchen", "col-living": "Living",
      "col-bath": "Bath", "col-cafe": "Café & restaurant",
      "prj-eye": "02 — Selected work", "prj-title": "Projects, signed by quality",
      "prj-all": "Full archive", "tag-kitchen": "Kitchen", "tag-interior": "Interior",
      "tag-cafe": "Café", "tag-bath": "Bath",
      "p-firuzkuh": "Firuzkuh Mountain House", "p-dozak": "Naghsh Dozak Kindergarten",
      "p-club": "Amol Fitness Club", "p-cafe-amol": "Café Amol",
      "m-firuzkuh": "Asur • 100 m² built", "m-dozak": "Amol, Aftab 31 • 2023",
      "m-club": "155 m² • 2026", "m-cafe-amol": "Amol • Interior",
      "tag-mountain": "Mountain", "tag-edu": "Learning space", "tag-sport": "Fitness club",
      "phone-v": "+98 912 089 8938",
      "hero-1": "Laico Design,", "hero-2": "beyond design",
      "why-eye": "03 — Studio",
      "why-quote": "Why Laico? Because one team and one standard stay with the work, from the first sketch to the last screw. Honest materials, precise installation, and a commitment that remains years after handover.",
      "st-projects": "Completed projects", "st-years": "Years of practice", "st-brands": "European brands",
      "sys-eye": "04 — Systems & materials", "sys-title": "No handles. No extra joints.",
      "sys-body": "Laico kitchen, wardrobe, and living systems are built on aluminium profiles, matte lacquer, and natural stone, with an installation tolerance under one millimetre.",
      "spec-finish": "Finish", "spec-finish-v": "Matte lacquer, beech, gres porcelain",
      "spec-hw": "Hardware", "spec-hw-v": "Soft-close hinge, Blum full-extension runner",
      "spec-w": "Warranty", "spec-w-v": "10 years on making, 2 years of service",
      "sh-eye": "05 — Showroom", "sh-title": "Touch the material.",
      "sh-body": "Showroom visits are by appointment, with a technical consultation and a material palette.",
      "addr": "Address", "addr-v": "Amol, Darya 20", "hours": "Hours",
      "hours-v": "Saturday to Thursday, 10–19", "phone": "Phone",
      "form-eye": "06 — Start a project", "form-1": "How should we", "form-2": "work together?",
      "form-body": "Send the form. The design team will call within 48 working hours to set the first meeting.",
      "f-name": "Full name", "f-phone": "Phone", "f-type": "Project type",
      "f-note": "A short note", "f-note-ph": "Area, city, timeline",
      "about-ph-note": "Write your message..", "f-send": "Send request",
      "f-ok-title": "Your request is in.",
      "f-ok-body": "The design team will call within 48 working hours to arrange the first meeting.",
      "err-name": "Please enter your name.", "err-phone": "Enter a valid mobile number.",
      "err-note": "Tell us a little about the space.",
      "opt-kitchen": "Kitchen", "opt-living": "Living", "opt-bath": "Bath",
      "opt-cafe": "Café & restaurant", "opt-wardrobe": "Wardrobe system", "opt-full": "Full renovation",
      "foot-about": "A studio for interior architecture and luxury kitchen systems.",
      "foot-col": "Collections", "foot-studio": "Studio", "foot-contact": "Contact",
      "foot-about-us": "About", "foot-process": "Process", "foot-journal": "Journal",
      "foot-collab": "Collaborate", "foot-material": "Materials", "foot-ig": "Instagram",
      "foot-wa": "WhatsApp", "copy": "© 2026 Laico Design — All rights reserved",
      "privacy": "Privacy", "cookies": "Cookies", "filter-all": "All",
      "next": "Next project", "book": "Book a visit", "read": "Read",
      "f-demo-title": "Your request is ready.",
      "f-demo-body": "This template has no server connection, so nothing was sent automatically. Your request text is ready — send it to us using one of the options below.",
      "f-send-wa": "Send via WhatsApp", "f-send-mail": "Send by e-mail",
      "f-call": "Call us", "f-copy": "Copy request text", "f-copied": "Copied",
      "f-copy-fail": "Could not copy; select the text manually.",
      "f-edit": "Edit request", "f-clear": "Delete saved data",
      "f-cleared": "Local data deleted.", "f-sending": "Sending…",
      "f-error": "Sending failed. Please try again or use WhatsApp.",
      "f-subject": "Consultation request — Laico Design",
      "f-consent-err": "Please confirm to continue.",
      "f-consent-label": "I agree to the privacy policy.",
      "f-privacy-note": "This is a demo template; the request is stored in your browser only.",
      "st-invalid": "Please correct the errors in the form.",
      "st-sending": "Sending your request…",
      "st-ok": "Your request was sent.",
      "st-demo": "Preview: the request was saved in this browser only.",
      "st-cleared": "Local data deleted.",
      "clear-data": "Clear local data",
      "filter-status": "{n} items shown.",
      "bc-label": "Breadcrumb",
      "external": "external link",
      "lang-label": "Language"
    }
  };

  /* ------------------------------------------------------------------ */
  function lang() { return document.documentElement.lang === "en" ? "en" : "fa"; }
  function t(key) {
    var pack = dict[lang()] || dict.fa;
    return pack[key] != null ? pack[key] : (dict.fa[key] || "");
  }
  function reducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }
  function announce(form, key) {
    var region = form.parentNode && form.parentNode.querySelector("[data-form-status]");
    if (!region) region = form.querySelector("[data-form-status]");
    if (region) region.textContent = t(key);
  }

  /* ------------------------------------------------------------------ *
   * 2. Content translation (fa -> en) for static markup.
   *    Text-node based, so no HTML markup is ever destroyed. Originals are
   *    kept in WeakMaps and restored when switching back to Persian.
   *    Strings owned by data-i18n / data-prj-i18n / .lang-fa / .lang-en
   *    are skipped — those already have their own translation path.
   * ------------------------------------------------------------------ */
  var SKIP = "[data-i18n], [data-i18n-placeholder], [data-i18n-aria], " +
             "[data-prj-i18n], [data-prj-i18n-placeholder], [data-prj-i18n-aria], " +
             ".lang-fa, .lang-en, [data-no-i18n], script, style, svg, noscript, template";
  var textOriginals = new WeakMap();
  var attrOriginals = new WeakMap();
  var TRANS_ATTRS = ["placeholder", "aria-label", "alt", "title"];

  function skipped(node) {
    var el = node.nodeType === 3 ? node.parentElement : node;
    while (el && el.nodeType === 1 && el !== document.body.parentNode) {
      if (el.matches && el.matches(SKIP)) return true;
      el = el.parentElement;
    }
    return false;
  }

  function applyContent(language) {
    if (!T9N || !Object.keys(T9N).length) return;
    var toEn = language === "en";

    var walker = document.createTreeWalker(document.body, window.NodeFilter.SHOW_TEXT, null, false);
    var node;
    while ((node = walker.nextNode())) {
      if (!node.nodeValue || !node.nodeValue.trim() || skipped(node)) continue;
      if (!textOriginals.has(node)) textOriginals.set(node, node.nodeValue);
      var original = textOriginals.get(node);
      var key = original.trim();
      if (toEn && Object.prototype.hasOwnProperty.call(T9N, key)) {
        node.nodeValue = original.replace(key, T9N[key]);
      } else {
        node.nodeValue = original;
      }
    }

    var all = document.querySelectorAll("*");
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (skipped(el)) continue;
      if (!attrOriginals.has(el)) attrOriginals.set(el, {});
      var store = attrOriginals.get(el);
      TRANS_ATTRS.forEach(function (attr) {
        if (!el.hasAttribute(attr)) return;
        if (!Object.prototype.hasOwnProperty.call(store, attr)) store[attr] = el.getAttribute(attr);
        var val = store[attr] || "";
        if (toEn && Object.prototype.hasOwnProperty.call(T9N, val.trim())) {
          el.setAttribute(attr, val.replace(val.trim(), T9N[val.trim()]));
        } else {
          el.setAttribute(attr, val);
        }
      });
    }

    /* Meta descriptions / OG titles / OG locale */
    document.querySelectorAll('meta[name="description"], meta[property="og:description"], meta[property="og:title"]').forEach(function (meta) {
      if (!meta.hasAttribute("content")) return;
      if (!attrOriginals.has(meta)) attrOriginals.set(meta, {});
      var st = attrOriginals.get(meta);
      if (!Object.prototype.hasOwnProperty.call(st, "content")) st.content = meta.getAttribute("content");
      var v = st.content || "";
      meta.setAttribute("content", toEn && T9N[v.trim()] != null ? T9N[v.trim()] : v);
    });
    var loc = document.querySelector('meta[property="og:locale"]');
    if (loc) loc.setAttribute("content", toEn ? "en_US" : "fa_IR");
  }

  /* ------------------------------------------------------------------ *
   * 3. Language switch
   * ------------------------------------------------------------------ */
  var header = document.querySelector("[data-header]");
  var burger = document.querySelector("[data-burger]");

  function updateBurgerLabel() {
    if (!burger || !header) return;
    burger.setAttribute("aria-label", t(header.classList.contains("is-open") ? "close" : "menu"));
  }

  function apply(language) {
    document.documentElement.lang = language;
    document.documentElement.dir = language === "en" ? "ltr" : "rtl";
    try { localStorage.setItem("laico-lang", language); } catch (e) {}

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (dict[language] && dict[language][key] != null) el.textContent = dict[language][key];
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-placeholder");
      if (dict[language] && dict[language][key] != null) el.setAttribute("placeholder", dict[language][key]);
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-aria");
      if (dict[language] && dict[language][key] != null) el.setAttribute("aria-label", dict[language][key]);
    });
    document.querySelectorAll("[data-lang]").forEach(function (btn) {
      var on = btn.getAttribute("data-lang") === language;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    var en = language === "en";
    document.querySelectorAll(".lang-fa").forEach(function (el) { el.hidden = en; });
    document.querySelectorAll(".lang-en").forEach(function (el) { el.hidden = !en; });
    document.title = en
      ? (document.body.getAttribute("data-title-en") || "Laico Design")
      : (document.body.getAttribute("data-title-fa") || "لایکو دیزاین");
    var langGroup = document.querySelector(".lang[role=group]");
    if (langGroup) langGroup.setAttribute("aria-label", t("lang-label"));
    updateBurgerLabel();
    applyContent(language);
    try { document.dispatchEvent(new CustomEvent("laico:langchange", { detail: { lang: language } })); } catch (e) {}
  }

  document.querySelectorAll("[data-lang]").forEach(function (btn) {
    btn.addEventListener("click", function () { apply(btn.getAttribute("data-lang")); });
  });

  /* ------------------------------------------------------------------ *
   * 4. Header + mobile menu (scroll lock, focus trap, resize recovery)
   * ------------------------------------------------------------------ */
  function onScroll() { if (header) header.classList.toggle("is-scrolled", window.scrollY > 12); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  var lastFocused = null;
  function focusables() {
    if (!header) return [];
    return Array.prototype.slice.call(
      header.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])')
    ).filter(function (el) { return el.offsetParent !== null || el === document.activeElement; });
  }
  function setMenu(open) {
    if (!header) return;
    if (open) lastFocused = document.activeElement;
    header.classList.toggle("is-open", open);
    document.body.style.overflow = open ? "hidden" : "";
    if (burger) burger.setAttribute("aria-expanded", open ? "true" : "false");
    updateBurgerLabel();
    var panel = document.getElementById("nav-panel");
    if (panel) {
      if (open) panel.setAttribute("aria-hidden", "false");
      else panel.removeAttribute("aria-hidden");
    }
    if (!open && lastFocused && document.contains(lastFocused)) {
      try { lastFocused.focus(); } catch (e) {}
    }
  }
  if (burger) burger.addEventListener("click", function () {
    setMenu(!header.classList.contains("is-open"));
  });
  document.querySelectorAll(".nav-panel a").forEach(function (a) {
    a.addEventListener("click", function () { setMenu(false); });
  });
  document.addEventListener("keydown", function (e) {
    if (!header || !header.classList.contains("is-open")) return;
    if (e.key === "Escape") { setMenu(false); return; }
    if (e.key !== "Tab") return;
    var items = focusables();
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  document.addEventListener("click", function (e) {
    if (header && header.classList.contains("is-open") && !header.contains(e.target)) setMenu(false);
  });
  if (window.matchMedia) {
    var mq = window.matchMedia("(min-width: 1181px)");
    var onBreak = function () { if (mq.matches) setMenu(false); };
    if (mq.addEventListener) mq.addEventListener("change", onBreak);
    else if (mq.addListener) mq.addListener(onBreak);
  }
  window.addEventListener("resize", function () {
    if (window.innerWidth > 1180 && header && header.classList.contains("is-open")) setMenu(false);
  }, { passive: true });

  /* ------------------------------------------------------------------ *
   * 5. Active navigation — subpages highlight their parent section
   * ------------------------------------------------------------------ */
  var active = document.body.getAttribute("data-active-nav") || document.body.getAttribute("data-page");
  if (active) {
    document.querySelectorAll("[data-nav]").forEach(function (a) {
      var on = a.getAttribute("data-nav") === active;
      a.classList.toggle("is-active", on);
      if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
  }

  /* ------------------------------------------------------------------ *
   * 6. Animated counters — respect reduced motion
   * ------------------------------------------------------------------ */
  var counted = false;
  function runCounts() {
    if (counted) return;
    var nodes = document.querySelectorAll("[data-count]");
    if (!nodes.length) return;
    if (reducedMotion()) {
      nodes.forEach(function (el) { el.textContent = (el.getAttribute("data-prefix") || "") + el.getAttribute("data-count"); });
      counted = true;
      return;
    }
    var rect = nodes[0].getBoundingClientRect();
    if (rect.top > window.innerHeight * 0.92) return;
    counted = true;
    nodes.forEach(function (el) {
      var target = parseInt(el.getAttribute("data-count"), 10) || 0;
      var prefix = el.getAttribute("data-prefix") || "";
      var start = performance.now();
      function frame(now) {
        var p = Math.min(1, (now - start) / 900);
        el.textContent = prefix + Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    });
  }
  window.addEventListener("scroll", runCounts, { passive: true });
  runCounts();

  /* ------------------------------------------------------------------ *
   * 7. Legacy project filters (index / older pages)
   * ------------------------------------------------------------------ */
  document.querySelectorAll("[data-filter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var key = btn.getAttribute("data-filter");
      var shown = 0;
      document.querySelectorAll("[data-filter]").forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      document.querySelectorAll("[data-kind]").forEach(function (card) {
        var show = key === "all" || card.getAttribute("data-kind") === key;
        card.classList.toggle("is-hidden", !show);
        if (show) shown++;
      });
      var live = document.querySelector("[data-filter-status]");
      if (live) live.textContent = t("filter-status").replace("{n}", shown);
    });
  });

  /* ------------------------------------------------------------------ *
   * 8. Forms — validation, honest demo mode, optional real endpoint
   * ------------------------------------------------------------------ */
  function normalizePhone(raw) {
    var value = (raw || "").trim();
    var digits = value.replace(/\D/g, "");
    if (!digits) return null;
    if (/^\+/.test(value)) return digits.length >= 8 && digits.length <= 15 ? "+" + digits : null;
    if (digits.indexOf("0098") === 0) digits = digits.slice(4);
    else if (digits.indexOf("98") === 0 && digits.length >= 12) digits = digits.slice(2);
    if (digits.charAt(0) === "0") digits = digits.slice(1);
    if (/^9\d{9}$/.test(digits)) return "+98" + digits;
    if (digits.length >= 8 && digits.length <= 15) return "+" + digits;
    return null;
  }

  function requestText(payload) {
    var lines = [t("f-subject"), "",
      t("f-name") + ": " + payload.name,
      t("f-phone") + ": " + payload.phone];
    if (payload.typeLabel) lines.push(t("f-type") + ": " + payload.typeLabel);
    lines.push(t("f-note") + ": " + payload.note);
    return lines.join("\n");
  }

  function storeRequest(payload) {
    try {
      var all = JSON.parse(localStorage.getItem(STORE_KEY) || "[]");
      if (!Array.isArray(all)) all = [];
      var cutoff = Date.now() - RETENTION_MS;
      all = all.filter(function (r) { return r && r.at && Date.parse(r.at) > cutoff; });
      all.push(payload);
      localStorage.setItem(STORE_KEY, JSON.stringify(all));
    } catch (e) {}
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function copyText(text, btn, done) {
    function ok() { btn.textContent = t("f-copied"); setTimeout(done, 1800); }
    function fail() { btn.textContent = t("f-copy-fail"); setTimeout(done, 2600); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(ok, fail);
      return;
    }
    var ta = el("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy") ? ok() : fail(); } catch (e) { fail(); }
    document.body.removeChild(ta);
  }

  function buildActions(done, form, payload, sentToServer) {
    var old = done.querySelector("[data-form-actions]");
    if (old) old.parentNode.removeChild(old);
    var box = el("div", "form-actions");
    box.setAttribute("data-form-actions", "");
    var text = requestText(payload);

    if (!sentToServer) {
      var wa = el("a", "btn-action btn-action-primary", t("f-send-wa"));
      wa.href = "https://wa.me/" + (CFG.whatsapp || "989120898938") + "?text=" + encodeURIComponent(text);
      wa.target = "_blank"; wa.rel = "noopener noreferrer";
      box.appendChild(wa);

      if (CFG.email) {
        var mail = el("a", "btn-action", t("f-send-mail"));
        mail.href = "mailto:" + CFG.email + "?subject=" + encodeURIComponent(t("f-subject")) + "&body=" + encodeURIComponent(text);
        box.appendChild(mail);
      }
      var call = el("a", "btn-action", t("f-call"));
      call.href = "tel:" + (CFG.phoneIntl || "+989120898938");
      box.appendChild(call);

      var copy = el("button", "btn-action", t("f-copy"));
      copy.type = "button";
      copy.addEventListener("click", function () {
        copyText(text, copy, function () { copy.textContent = t("f-copy"); });
      });
      box.appendChild(copy);
    }

    var edit = el("button", "btn-action btn-action-quiet", t("f-edit"));
    edit.type = "button";
    edit.addEventListener("click", function () {
      form.hidden = false;
      done.hidden = true;
      var first = form.querySelector("input[name=name]");
      if (first) first.focus();
      announce(form, sentToServer ? "st-ok" : "st-demo");
    });
    box.appendChild(edit);

    var clear = el("button", "btn-action btn-action-quiet", t("f-clear"));
    clear.type = "button";
    clear.addEventListener("click", function () {
      try { localStorage.removeItem(STORE_KEY); } catch (e) {}
      clear.textContent = t("f-cleared");
      announce(form, "st-cleared");
      setTimeout(function () { clear.textContent = t("f-clear"); }, 2600);
    });
    box.appendChild(clear);

    done.appendChild(box);
  }

  document.querySelectorAll("[data-clear-data]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      try { localStorage.removeItem(STORE_KEY); localStorage.removeItem("laico-lang"); } catch (e) {}
      btn.textContent = t("f-cleared");
      setTimeout(function () { btn.textContent = t("clear-data"); }, 2600);
    });
  });

  document.querySelectorAll("[data-form]").forEach(function (form, formIndex) {
    /* Wire accessible labels <-> controls <-> error messages. */
    form.querySelectorAll("[data-field]").forEach(function (field, i) {
      var control = field.querySelector("input:not([type=hidden]), textarea, select");
      var err = field.querySelector(".field-error");
      if (!control) return;
      if (!control.id) control.id = "laico-f" + formIndex + "-" + i;
      if (err) {
        if (!err.id) err.id = control.id + "-error";
        control.setAttribute("aria-describedby", err.id);
        err.setAttribute("role", "alert");
      }
      var label = field.querySelector("label.field-label");
      if (label && !label.getAttribute("for")) label.setAttribute("for", control.id);
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var hp = form.querySelector('[name="website"]');
      if (hp && hp.value) return; /* honeypot: silently drop bots */

      var ok = true;
      function setError(name, key) {
        var field = form.querySelector('[data-field="' + name + '"]');
        if (!field) return;
        var err = field.querySelector(".field-error");
        var control = field.querySelector("input:not([type=hidden]), textarea, select");
        if (key) {
          field.classList.add("is-invalid");
          if (err) err.textContent = t(key);
          if (control) control.setAttribute("aria-invalid", "true");
          ok = false;
        } else {
          field.classList.remove("is-invalid");
          if (err) err.textContent = "";
          if (control) control.removeAttribute("aria-invalid");
        }
      }

      var name = (form.querySelector('[name="name"]') || {}).value || "";
      var phoneRaw = (form.querySelector('[name="phone"]') || {}).value || "";
      var note = (form.querySelector('[name="note"]') || {}).value || "";
      var phone = normalizePhone(phoneRaw);
      var consent = form.querySelector('[name="consent"]');

      setError("name", name.trim().length < 2 ? "err-name" : "");
      setError("phone", phone ? "" : "err-phone");
      setError("note", note.trim().length < 4 ? "err-note" : "");
      if (consent) setError("consent", consent.checked ? "" : "f-consent-err");

      if (!ok) {
        announce(form, "st-invalid");
        var bad = form.querySelector(".is-invalid input, .is-invalid textarea, .is-invalid select");
        if (bad) bad.focus();
        return;
      }

      var typeControl = form.querySelector('[name="type"]');
      var typeLabel = "";
      if (typeControl && typeControl.tagName === "SELECT") {
        typeLabel = typeControl.options[typeControl.selectedIndex]
          ? typeControl.options[typeControl.selectedIndex].text : typeControl.value;
      } else if (typeControl) {
        typeLabel = typeControl.value;
      }

      var payload = {
        name: name.trim(), phone: phone, type: typeControl ? typeControl.value : "",
        typeLabel: typeLabel, note: note.trim(), at: new Date().toISOString(),
        page: window.location.pathname.split("/").pop()
      };
      storeRequest(payload);

      var btn = form.querySelector('[type="submit"]');
      var originalLabel = btn ? btn.innerHTML : "";
      var endpoint = form.getAttribute("data-endpoint") || CFG.formEndpoint || "";
      var done = form.parentElement.querySelector("[data-success]");

      function finish(sent) {
        if (btn) { btn.innerHTML = originalLabel; btn.disabled = false; }
        form.hidden = true;
        if (done) {
          done.hidden = false;
          var h = done.querySelector("h3"), p = done.querySelector("p");
          if (h) h.textContent = t(sent ? "f-ok-title" : "f-demo-title");
          if (p) p.textContent = t(sent ? "f-ok-body" : "f-demo-body");
          buildActions(done, form, payload, sent);
        }
        announce(form, sent ? "st-ok" : "st-demo");
      }

      if (!endpoint) { finish(false); return; }

      if (btn) { btn.disabled = true; btn.textContent = t("f-sending"); }
      announce(form, "st-sending");
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        finish(true);
      }).catch(function () {
        if (btn) { btn.innerHTML = originalLabel; btn.disabled = false; }
        announce(form, "f-error");
        var status = form.parentNode.querySelector("[data-form-status]");
        if (status) status.classList.add("is-error");
      });
    });
  });

  /* ------------------------------------------------------------------ *
   * 9. Boot: apply the saved language once the DOM is complete
   * ------------------------------------------------------------------ */
  var saved = "fa";
  try { saved = localStorage.getItem("laico-lang") || document.documentElement.lang || "fa"; } catch (e) {}
  if (saved !== "fa" && saved !== "en") saved = "fa";
  apply(saved);
})();
