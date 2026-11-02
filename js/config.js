/* LAICO DESIGN — single source of truth for business/site settings.
 *
 * The template is static and has no backend. Everything the site needs to know
 * about the business lives here so it can be changed in ONE place instead of
 * 21 copied headers/footers. `tools/uiux_fix.py` also reads these values when
 * rewriting contact details into the HTML.
 *
 * BEFORE DEPLOYING: change `siteUrl` to your real domain and run
 *   python3 tools/set_site_url.py https://your-domain.example
 * then fill in `email` / `formEndpoint` if you have them.
 */
(function (global) {
  "use strict";

  global.LAICO_CONFIG = {
    /* Canonical production origin — no trailing slash. Used by canonical tags,
       sitemap.xml, robots.txt, Open Graph and JSON-LD. */
    siteUrl: "https://laicodesign.ir",

    name: "Laico Design",
    nameFa: "لایکو دیزاین",

    /* One phone number everywhere (was three conflicting values). */
    phoneDisplay: "09120898938",
    phoneIntl: "+989120898938",
    whatsapp: "989120898938",

    /* Empty on purpose: no invented e-mail address. Set it to enable the
       "send by e-mail" action in the consultation form. */
    email: "",

    addressFa: "مازندران، آمل، دریای ۲۰، لایکودیزاین",
    addressEn: "Mazandaran, Amol, Darya 20, Laico Design",
    hoursFa: "شنبه تا پنجشنبه، ۱۰ تا ۱۹",
    hoursEn: "Saturday to Thursday, 10–19",

    /* Set to a real POST endpoint (Formspree, Getform, your own API, ...) to
       switch the form from honest demo mode to real server submission.
       The endpoint must accept JSON: {name, phone, type, note, at}. */
    formEndpoint: "",

    /* Personal data kept in localStorage is dropped after this many days. */
    requestRetentionDays: 30
  };
})(window);
