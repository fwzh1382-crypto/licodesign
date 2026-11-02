/* LAICO DESIGN — projects.html only
   Scoped filter/search logic + translations for the strings that cannot use
   the global data-i18n dictionary (native <option> labels, placeholders,
   result counters). js/main.js stays untouched. */
(function () {
  "use strict";

  var dict = {
    fa: {
      "search": "جستجو کنید",
      "all": "همه پروژه ها",
      "residential": "مسکونی",
      "commercial": "تجاری",
      "space-label": "فضا:",
      "space-all": "همه",
      "kitchen": "آشپزخانه",
      "living": "نشیمین",
      "office": "اداری",
      "hall": "سالن و بار",
      "location": "موقعیت:",
      "all-cities": "همه شهرها",
      "city-amol": "آمل",
      "city-tehran": "تهران",
      "city-mazandaran": "مازندران",
      "year": "سال:",
      "all-years": "همه سالها",
      "year-1403": "۱۴۰۳",
      "year-1404": "۱۴۰۴",
      "area": "متراژ:",
      "all-sizes": "همه ابعاد",
      "size-small": "کوچک",
      "size-medium": "متوسط",
      "size-large": "بزرگ",
      "filters": "جستجو و فیلتر پروژهها",
      "group-category": "دستهبندی پروژهها",
      "group-space": "نوع فضا",
      "results": "نتایج جستجو",
      "count": "{n} پروژه",
      "empty": "پروژهای با این فیلترها یافت نشد.",
      "view": "مشاهده پروژه"
    },
    en: {
      "search": "Search projects",
      "all": "All projects",
      "residential": "Residential",
      "commercial": "Commercial",
      "space-label": "Space:",
      "space-all": "All",
      "kitchen": "Kitchen",
      "living": "Living",
      "office": "Office",
      "hall": "Hall & bar",
      "location": "Location:",
      "all-cities": "All cities",
      "city-amol": "Amol",
      "city-firuzkuh": "Firuzkuh",
      "year": "Year:",
      "all-years": "All years",
      "year-1402": "2023",
      "year-1405": "2026",
      "area": "Area:",
      "all-sizes": "All sizes",
      "size-small": "Small",
      "size-medium": "Medium",
      "size-large": "Large",
      "filters": "Search and filter projects",
      "group-category": "Project category",
      "group-space": "Space type",
      "results": "Search results",
      "count": "{n} projects",
      "empty": "No projects match these filters.",
      "view": "View project"
    }
  };

  function lang() {
    return document.documentElement.lang === "en" ? "en" : "fa";
  }
  function t(key) {
    var pack = dict[lang()] || dict.fa;
    return pack[key] != null ? pack[key] : "";
  }

  /* ---------- translations for scoped strings ---------- */
  function applyPrj() {
    document.querySelectorAll("[data-prj-i18n]").forEach(function (el) {
      el.textContent = t(el.getAttribute("data-prj-i18n"));
    });
    document.querySelectorAll("[data-prj-i18n-placeholder]").forEach(function (el) {
      el.setAttribute("placeholder", t(el.getAttribute("data-prj-i18n-placeholder")));
    });
    document.querySelectorAll("[data-prj-i18n-aria]").forEach(function (el) {
      el.setAttribute("aria-label", t(el.getAttribute("data-prj-i18n-aria")));
    });
    updateCount();
  }

  document.querySelectorAll("[data-lang]").forEach(function (btn) {
    btn.addEventListener("click", function () { setTimeout(applyPrj, 0); });
  });
  /* main.js broadcasts language changes so this page stays in sync even when
     the switch is triggered programmatically. */
  document.addEventListener("laico:langchange", applyPrj);

  /* filter controls are toggles: expose their state to assistive tech */
  function markPressed(selector) {
    document.querySelectorAll(selector).forEach(function (b) {
      b.setAttribute("aria-pressed", b.classList.contains("is-active") ? "true" : "false");
    });
  }
  markPressed("[data-category]");
  markPressed("[data-space-filter]");
  document.querySelectorAll("[data-prj-count]").forEach(function (el) {
    el.setAttribute("role", "status");
    el.setAttribute("aria-live", "polite");
  });

  /* ---------- filtering ---------- */
  var grid = document.querySelector("[data-prj-grid]");
  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-prj-card]"));
  var empty = document.querySelector("[data-prj-empty]");
  var search = document.querySelector("[data-prj-search]");
  var tabs = Array.prototype.slice.call(document.querySelectorAll("[data-category]"));
  var pills = Array.prototype.slice.call(document.querySelectorAll("[data-space-filter]"));
  var selects = {
    city: document.querySelector("[data-prj-select='city']"),
    year: document.querySelector("[data-prj-select='year']"),
    size: document.querySelector("[data-prj-select='size']")
  };
  var state = { category: "all", space: "all", q: "" };

  function normalize(text) {
    return (text || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  function updateCount() {
    var visible = cards.filter(function (c) { return !c.hidden; }).length;
    document.querySelectorAll("[data-prj-count]").forEach(function (el) {
      el.textContent = t("count").replace("{n}", visible);
    });
  }

  function applyFilters() {
    var q = normalize(state.q);
    var city = selects.city ? selects.city.value : "all";
    var year = selects.year ? selects.year.value : "all";
    var size = selects.size ? selects.size.value : "all";
    var shown = 0;

    cards.forEach(function (card) {
      var ok = true;
      if (state.category !== "all" && card.getAttribute("data-category") !== state.category) ok = false;
      if (state.space !== "all" && card.getAttribute("data-space") !== state.space) ok = false;
      if (city !== "all" && card.getAttribute("data-city") !== city) ok = false;
      if (year !== "all" && card.getAttribute("data-year") !== year) ok = false;
      if (size !== "all" && card.getAttribute("data-size") !== size) ok = false;
      if (q && normalize(card.textContent).indexOf(q) === -1) ok = false;
      card.hidden = !ok;
      if (ok) shown++;
    });

    if (grid) grid.hidden = shown === 0;
    if (empty) empty.hidden = shown !== 0;
    updateCount();
  }

  if (search) {
    search.addEventListener("input", function () { state.q = search.value; applyFilters(); });
    search.addEventListener("keydown", function (e) {
      if (e.key === "Enter") e.preventDefault();
    });
  }
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      state.category = tab.getAttribute("data-category");
      tabs.forEach(function (b) { b.classList.toggle("is-active", b === tab); });
      markPressed("[data-category]");
      applyFilters();
    });
  });
  pills.forEach(function (pill) {
    pill.addEventListener("click", function () {
      state.space = pill.getAttribute("data-space-filter");
      pills.forEach(function (b) { b.classList.toggle("is-active", b === pill); });
      markPressed("[data-space-filter]");
      applyFilters();
    });
  });
  Object.keys(selects).forEach(function (k) {
    if (selects[k]) selects[k].addEventListener("change", applyFilters);
  });

  /* initial state (also respects the language saved by main.js) */
  applyPrj();
  applyFilters();
})();
