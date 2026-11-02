# لایکو دیزاین (LAICO DESIGN)

قالب **سایت ایستا** برای استودیو معماری داخلی و سیستم آشپزخانه لوکس؛ راست‑به‑چپ (RTL)،
دوزبانهٔ فارسی/انگلیسی و بدون هیچ وابستگی، فریمورک یا مرحلهٔ build.

این مخزن شامل کدهای استخراج‌شده از فایل `laico.zip` (دانلودشده از Google Drive)،
اطلاعات پروژه، ابزارهای ممیزی، **[گزارش بررسی قالب](REVIEW.md)** و
**[گزارش کامل بررسی و رفع مشکلات UI/UX](UIUX-REPORT.md)** است.

> **بهروزرسانی ۲۰۲۶‑۱۰‑۲۷:** ممیزی کامل UI/UX روی **همهٔ ۲۲ صفحه** انجام و
> همهٔ مشکلات قابل رفع برطرف شد (کنتراست WCAG AA، دوزبانگی کامل، فرم صادقانه،
> breadcrumb، ۴۰۴، سئو، WebP، دسترسپذیری). نتیجه: **۱۰۰/۱۰۰** در
> `tools/uiux_audit.py`. جزئیات در [بخش ۱۳](#۱۳-ممیزی-و-رفع-کامل-مشکلات-uiux) و
> [UIUX-REPORT.md](UIUX-REPORT.md).

---

## ۱. منبع فایل

| مورد | مقدار |
| --- | --- |
| نام فایل در Google Drive | `laico.zip` |
| شناسهٔ فایل در Drive | `1nyH_kNjPT3GbL2ZNzPB3SgnHKtaNyJi2` |
| تاریخ آخرین تغییر در Drive | 2026‑10‑21 |
| تاریخ دانلود | 2026‑10‑26 |
| حجم | 2,689,105 بایت (حدود ۲٫۶ مگابایت) |
| MD5 | `56768ba15707745489fbc68e99ca9b23` |
| محتوای آرشیو | ۵۷ ورودی (۵۱ فایل + ۶ پوشه) در پوشهٔ `laico/` |
| نسخهٔ اصلی آرشیو در این مخزن | [`archive/laico.zip`](archive/laico.zip) |

فایل‌های داخل پوشهٔ `laico/` بدون تغییر در ریشهٔ مخزن قرار گرفته‌اند تا سایت مستقیماً
از root سرو شود (مناسب GitHub Pages). آرشیو اصلی برای راستی‌آزمایی نگه داشته شده است.

---

## ۲. پشتهٔ فنی

| لایه | تکنولوژی |
| --- | --- |
| نشانهگذاری | HTML5، ۲۲ صفحه (۲۱ + `404.html`)، `<html lang="fa" dir="rtl">`، canonical + OG + JSON‑LD |
| استایل | CSS3 خالص: متغیرها، logical properties، Grid/Flexbox، `clamp()`، breakpointهای 1180/800/720، حالت چاپ، `prefers-reduced-motion`، لایهٔ «UI/UX REMEDIATION» در انتهای `styles.css` |
| رفتار | JavaScript خالص (IIFE، بدون کتابخانه): `js/config.js` (منبع واحد تنظیمات)، `js/main.js` (تعاملات + فرم + ترجمه)، `js/projects.js` (فیلترها)، `js/i18n-content.js` (نقشهٔ ۳۸۸ رشتهای FA→EN) |
| فونت | ۸ فایل `woff2` محلی: Vazirmatn (۵ وزن) + Outfit (۳ وزن)، همراه `font-display: swap` |
| تصاویر | ۲۷ فایل JPG + ۲۷ نسخهٔ WebP (‎−۶۰٪ حجم)، `<picture>` با fallback، ابعاد و `loading` صریح |
| زیرساخت | نیازی به npm/build ندارد؛ فقط یک وب سرور استاتیک + `robots.txt`, `sitemap.xml`, `site.webmanifest` |

هیچ درخواستی به CDN، فونت گوگل، آنالیتیکس یا سرویس ثالث انجام نمی‌شود.

---

## ۳. ساختار مخزن

```text
.
├── index.html                 # صفحهٔ اصلی (نمونهٔ کامل همهٔ بخش‌ها)
├── about.html                 # دربارهٔ ما
├── services.html              # خدمات
├── projects.html              # آرشیو پروژه‌ها + فیلتر
├── project-{aftab,haraz,acajou,darya}.html
├── kitchen.html, living.html, bath.html, cafe.html   # چهار مجموعه
├── studio.html, systems.html, process.html, materials.html, showroom.html
├── journal.html               # مجله/مقالات
├── contact.html               # تماس + فرم
├── privacy.html, cookies.html # صفحات حقوقی
├── 404.html                   # صفحهٔ خطای اختصاصی
├── css/styles.css             # استایل پایه + لایهٔ رفعهای UI/UX
├── css/services.css, css/projects.css  # استایل اختصاصی دو صفحهٔ بازطراحیشده
├── js/config.js               # منبع واحد: دامنه، تماس، endpoint فرم
├── js/main.js                 # تعاملات، فرم، منو، ترجمه
├── js/projects.js             # فیلتر و جستجوی پروژهها
├── js/i18n-content.js         # تولیدشده از tools/translations.json
├── assets/
│   ├── fonts/                 # ۸ فایل woff2
│   ├── images/                # ۲۷ JPG + ۲۷ WebP
│   └── favicon.svg
├── robots.txt, sitemap.xml, site.webmanifest
├── archive/laico.zip          # آرشیو اصلی دریافتی از Drive
├── tools/                     # audit, i18n_scan, build_i18n, uiux_fix,
│                              # gen_webp, uiux_audit, set_site_url, ...
├── REVIEW.md                  # گزارش بررسی اولیه (همهٔ بندها رفع شدهاند)
├── UIUX-REPORT.md             # گزارش کامل بررسی و رفع UI/UX
└── README.md                  # همین فایل
```

---

## ۴. صفحات (۲۲ صفحه)

| گروه | فایل‌ها |
| --- | --- |
| اصلی و منو | `index.html`, `services.html`, `projects.html`, `journal.html`, `about.html`, `contact.html` |
| مجموعه‌ها | `kitchen.html`, `living.html`, `bath.html`, `cafe.html` |
| پروژه‌های نمونه | `project-aftab.html`, `project-haraz.html`, `project-acajou.html`, `project-darya.html` |
| استودیو/سیستم | `studio.html`, `systems.html`, `process.html`, `materials.html`, `showroom.html` |
| حقوقی | `privacy.html`, `cookies.html` |
| خطا | `404.html` |

هر صفحه شامل `<title>` و `meta description` منحصربهفرد، `canonical`،
`og:title/description/image/url`، `twitter:card`، `theme-color`، پیشبارگذاری ۲ فونت،
هدر/فوتر مشترک، breadcrumb (بهجز صفحهٔ اصلی و ۴۰۴) و لینکهای فوتر به همهٔ صفحات است.
وضعیت منوی فعال از روی `data-active-nav` (و `data-page` برای استایل صفحات حقوقی)
در `<body>` تعیین میشود.

---

## ۵. اجرای محلی

```bash
python3 -m http.server 8000 --bind 0.0.0.0
# سپس: http://localhost:8000
```

یا با هر سرور استاتیک دیگر (nginx، `npx serve`، Live Server در VS Code). چون تمام مسیرها
نسبی هستند، سایت از یک زیرپوشه هم کار می‌کند.

**GitHub Pages:** تنظیمات مخزن → Pages → Deploy from a branch → شاخه و پوشهٔ `/` (root).

> نیازی به `npm install` نیست. تنها ابزار سمت سرور Python 3 برای `tools/audit.py`
> و Node.js برای `node --check` (اختیاری) است.

---

## ۶. معماری کد

- **طراحی سیستم:** رنگها، فونتها، فاصلهها و ارتفاع هدر در `:root` متمرکز شده است؛
  انتهای `css/styles.css` یک «لایهٔ رفعهای UI/UX» دارد (hidden، فوکوس، breadcrumb،
  اجزای فرم، ۴۰۴، کنتراست) تا سیستم طراحی اصلی دستنخورده بماند.
- **منبع واحد تنظیمات:** `js/config.js` شامل دامنه، تلفن، واتساپ، ایمیل، آدرس،
  ساعات کاری، `formEndpoint` و مدت نگهداری دادههاست. برای تغییر دامنه:
  `python3 tools/set_site_url.py https://your-domain.ir`.
- **`js/main.js`:** دیکشنری `fa`/`en` (۱۲۵ کلید)، تغییر زبان، هدر چسبان، منوی
  موبایل (focus trap + رفع قفل اسکرول)، `aria-current`، شمارندهها، فرمها،
  ترجمهٔ گرههای متنی و فیلترها.
- **ترجمهٔ کامل:** علاوه بر `data-i18n*` و جفتهای `lang-fa`/`lang-en`، نقشهٔ
  `tools/translations.json` (۳۸۸ رشته) توسط `tools/build_i18n.py` به
  `js/i18n-content.js` تبدیل میشود و `main.js` متنها، `alt`، `placeholder`،
  `aria-label`، `meta` و `og:locale` را ترجمه میکند — بدون تخریب markup.
- **تصاویر:** `tools/gen_webp.py` نسخههای WebP و ابعاد واقعی را میسازد؛
  `tools/uiux_fix.py` تگها را به `<picture>` + `width/height` + `loading` تبدیل میکند.
- **فیلتر پروژه:** `js/projects.js` (جستجو، دستهبندی، فضا، شهر/سال/متراژ) با
  `aria-pressed` و شمارندهٔ `aria-live`.

## ۷. فرمهای تماس — نکتهٔ مهم پیش از انتشار

شش صفحه (`index`, `showroom`, `about`, `contact`, `services`, `projects`) فرم دارند.
قالب **هیچ بکاندی ندارد**، بنابراین رفتار صادقانهای پیادهسازی شده است:

1. اعتبارسنجی سمت کاربر (نام، شمارهٔ موبایل ایران، توضیح، تیک رضایت، honeypot).
2. ذخیرهٔ محلی در `localStorage["laico-requests"]` با **انقضای ۳۰ روزه**.
3. پیام «درخواست شما آماده است» (ادعای ثبت دروغین وجود ندارد) بههمراه دکمههای
   **ارسال در واتساپ** (متن آماده)، تماس تلفنی، کپی متن، ویرایش درخواست و
   حذف اطلاعات ذخیرهشده. در صورت تنظیم `email`، دکمهٔ ایمیل هم اضافه میشود.
4. اگر `LAICO_CONFIG.formEndpoint` تنظیم شود، همان فرم با `fetch` به سرور
   ارسال میشود (حالت بارگذاری، خطا، تلاش مجدد و پیام موفقیت واقعی).

همهٔ مراحل با `role="status"` / `role="alert"` اعلام میشوند. `privacy.html` و
`cookies.html` دقیقاً همین رفتار را توضیح میدهند و از فوتر لینک شدهاند.
برای استقرار واقعی، حداقل `formEndpoint` (یا ایمیل) را در `js/config.js` پر کنید.

## ۸. بررسی کیفیت

```bash
python3 tools/audit.py --strict       # لینکها، داراییها، id تکراری، i18n، یتیمها
python3 tools/build_i18n.py --check  # پوشش ۱۰۰٪ ترجمهٔ EN
python3 tools/uiux_audit.py --strict # ۴۷ چک وزندار UI/UX/A11Y/SEO/کنتراست
node --check js/main.js && node --check js/projects.js
npx html-validate "*.html"           # اعتبارسنجی HTML (ابزار خارجی، اختیاری)
python3 -m http.server 8000 --bind 0.0.0.0
```

وضعیت فعلی: **`audit.py` → ۰ خطا / ۰ هشدار**،
**`uiux_audit.py` → ۴۷/۴۷ چک (۱۰۰/۱۰۰)**،
**`html-validate` → ۰ خطا**، تستهای jsdom **۲۵۱/۲۵۱** و رندر Chromium
**۵۴۵/۵۴۵ + ۲۴۲/۲۴۲** (همهٔ صفحات، ۳۲۰…۱۴۴۰px، حالت FA و EN).
گزارش کامل در **[UIUX-REPORT.md](UIUX-REPORT.md)**؛ اسکرینشاتها در
[`reference/uiux/`](reference/uiux/).

## ۹. مالکیت و مجوز

منبع قالب، فایل `laico.zip` دریافتی از Google Drive است و فایل `LICENSE` یا اعلام مجوزی
همراه آن نبوده است. پیش از انتشار تجاری، مالکیت محتوا/تصاویر و مجوز فونت‌ها و طرح را
با صاحب اثر مشخص کنید.


---

## ۱۰. بازطراحی صفحهٔ خدمات (`services.html`)

صفحهٔ خدمات بر اساس تصاویر مرجع پیوستشده ([`reference/`](reference/)) بازسازی شد،
بدون تغییر در ساختار کلی قالب: هدر، فوتر، `css/styles.css`، `js/main.js` و سایر
صفحات دستنخورده باقی ماندند.

**تغییرات:**

| مورد | توضیح |
| --- | --- |
| تصویر هیرو | `assets/images/services-hero.jpg` — برش تمیز از `خدمات.png` / `image-1.png` بدون متن جاسازیشده |
| ۵ بخش خدمات | ردیفهای دوسوتونی یکدرمیان (عکس راست/چپ) با شمارهٔ ۱ تا ۵، عنوان، توضیح و دکمهٔ «مشاهده پروژه ها» — بر اساس `image-2..6.png` |
| نوار «چرا لایکودیزاین؟» | زمینهٔ سرمهای `#020c3b` + تصویر `services-why.jpg` — بر اساس `image-7.png` |
| فرم مشاوره | پنل سرمهای سمت راست + فیلدهای خاکستری سمت چپ — بر اساس `image-8.png`؛ همچنان به هندلر `js/main.js` متصل است |
| تصاویر جدید | ۷ فایل JPG در `assets/images/services-*.jpg` (قابل بازتولید با `tools/extract-service-images.py`) |
| استایل | فقط [`css/services.css`](css/services.css) — فایل اختصاصی همان صفحه |
| ریسپانسیو | دسکتاپ (دو ستون) → ≤1000px تکستون با عکس در بالا → ≤640px تایپوگرافی و فاصلههای موبایل |
| دوزبانگی | تمام متنهای جدید به صورت جفت `lang-fa` / `lang-en` هستند؛ سوییچ EN در این صفحه کامل کار میکند |
| دسترسپذیری | ۱ عدد `<h1>`، `alt` توصیفی و `width`/`height` برای همهٔ تصاویر جدید، `<label>` واقعی برای فیلدها، قانون `[hidden]` صریح برای فرم و پیام موفقیت |

**تأیید شده با مرورگر headless:** عرضهای ۳۲۰، ۳۶۰، ۳۹۰، ۷۶۸، ۱۰۲۴، ۱۴۴۰ و ۱۹۲۰ پیکسل،
بدون سرریز افقی (`scrollWidth == clientWidth`) در هیچکدام. پیشنمایشها:
[`reference/preview-desktop.jpg`](reference/preview-desktop.jpg)،
[`reference/preview-tablet.jpg`](reference/preview-tablet.jpg)،
[`reference/preview-mobile.jpg`](reference/preview-mobile.jpg).

### انتشار (Release)

[صفحهٔ ریلیز `v1.0.0-services`](https://github.com/amolnovin/licodesign/releases/tag/v1.0.0-services)
شامل لینک دانلود فایل ZIP است:

- [`laico-design-services-v1.0.0.zip`](release/laico-design-services-v1.0.0.zip) —
  بستهٔ تمیز و قابل استقرار (همچنین از صفحهٔ ریلیز قابل دانلود است).
- بستهٔ خودکار `Source code (zip)` گیتهاب نیز همان قالب بهروزرسانیشده را دارد.
- ساخت مجدد ZIP: `python3 tools/build-release-zip.py laico-design-services-v1.0.0.zip`.

> نکته: همانند تصاویر مرجع، بخش ۴ (کافه و رستوران) از تصویر سالن ورزشی و بخش ۵
> (آشپزخانه و فضای مسکونی) از تصویر مجتمع تفریحی استفاده میکند؛ در صورت تمایل میتوان
> این دو JPG را با عکسهای واقعی جایگزین کرد.


---

## ۱۱. بازطراحی صفحهٔ پروژهها (`projects.html`)

صفحهٔ پروژهها بر اساس تصاویر مرجع پیوستشده ([`reference/projects/`](reference/projects/))
بازسازی شد. همانند مرحلهٔ قبل، ساختار کلی قالب دستنخورده ماند: هدر، فوتر،
`css/styles.css` و `js/main.js` تغییری نکردند.

**تغییرات:**

| مورد | توضیح |
| --- | --- |
| هیرو (`image-1`) | نوار سرمهای `#020c3b` با عنوان «همه پروژهها، یک استاندارد ساخت»، توضیح و شمارندهٔ ‎+۱۰۰ |
| فیلترها (`image-2`) | جستجو، سه تب دستهبندی (همه/مسکونی/تجاری)، ۵ دکمهٔ فضا و سه select بومی (موقعیت/سال/متراژ) — **همه فعال و قابل استفاده** |
| نتایج (`image-3`) | جدول ۳×۲ کارت پروژه با اورلی تیره، دکمهٔ «مشاهده پروژه»، عنوان و متراژ؛ شمارندهٔ نتایج و پیام حالت خالی |
| نوار و فرم (`image-4`, `image-5`) | دقیقاً همان مؤلفههای صفحهٔ خدمات — از `css/services.css` و `services-why.jpg` استفاده مجدد شده است |
| تصویر جدید | `assets/images/projects-card.jpg` — عکس تمیز مجتمع تجاری شب (`tools/extract-project-images.py`) |
| فایلهای اختصاصی | [`css/projects.css`](css/projects.css) + [`js/projects.js`](js/projects.js) — فقط همین صفحه آنها را بارگذاری میکند |
| ریسپانسیو | دسکتاپ ۳ ستون → ≤1000px دو ستون / فیلترها پشت سر هم → ≤640px تکستون، دکمهها و selectها تمامعرض |
| دوزبانگی | تمام متنها FA/EN (شامل optionها، placeholder و شمارنده)؛ سوییچ زبان بدون متن فارسی باقیمانده |
| دسترسپذیری | ۱ عدد `<h1>`، `alt` و ابعاد برای همهٔ تصاویر، `<select>` بومی، `<label>` واقعی، قانون `[hidden]` صریح |

**منطق فیلتر (`js/projects.js`):** جستجو بر اساس عنوان، فیلتر دستهبندی و فضا بهصورت
دکمهای، و فیلتر شهر/سال/متراژ از روی `data-*` کارتها. شمارندهٔ نتایج و پیام
«پروژهای یافت نشد» بهصورت زنده بهروزرسانی میشود.

**تأیید شده با مرورگر headless:** عرضهای ۳۲۰، ۳۶۰، ۳۹۰، ۷۶۸، ۱۰۲۴ و ۱۴۴۰ پیکسل —
بدون سرریز افقی؛ `html-validate` و `tools/audit.py` روی صفحه **۰ خطا**. پیشنمایشها:
[`reference/projects/preview-desktop.jpg`](reference/projects/preview-desktop.jpg)،
[`reference/projects/preview-tablet.jpg`](reference/projects/preview-tablet.jpg)،
[`reference/projects/preview-mobile.jpg`](reference/projects/preview-mobile.jpg).

### انتشار (Release)

[صفحهٔ ریلیز `v1.1.0-projects`](https://github.com/amolnovin/licodesign/releases/tag/v1.1.0-projects)
شامل لینک دانلود [`laico-design-projects-v1.1.0.zip`](release/laico-design-projects-v1.1.0.zip)
است؛ بستهٔ خودکار `Source code (zip)` گیتهاب نیز همان قالب کامل (هر دو صفحهٔ
بازطراحیشده) را دارد. ساخت مجدد: `python3 tools/build-release-zip.py`.

> نکته: در `image-3.png` هر ۶ کارت یک عکس نمونه دارند. در پیادهسازی نهایی همان
> عکس تمیز برای کارت «مجتمع تجاری آفتاب» و عکسهای واقعی پروژههای موجود قالب
> برای ۵ کارت دیگر استفاده شده تا آرشیو قابل استفاده باشد.


---

## ۱۲. فعالسازی تیم ایجنت UI/UX (`uiux-agent-team`)

تیم ۵ نفرهٔ UI/UX از مخزن
[`amolnovin/aiagent.amolnovin`](https://github.com/amolnovin/aiagent.amolnovin)
(مسیر `teams/ui-ux`) در این مخزن **فعال** شد. بستهٔ اصلی بدون تغییر و با هش
تأییدشده در [`agents/uiux-agent-team/`](agents/uiux-agent-team/) قرار دارد
(جزئیات: [`SOURCE.md`](agents/uiux-agent-team/SOURCE.md)).

### چه چیزی فعال شد

| مورد | مسیر |
| --- | --- |
| ۱۳ فایل اصلی بسته (playbook، دانش، قالب starter) | `agents/uiux-agent-team/` |
| پرامپت فعالسازی خودکفا (کپی در چت جدید) | [`ACTIVATE.md`](agents/uiux-agent-team/ACTIVATE.md) |
| روتدر سطح مخزن — هر ایجنت کدنویسی آن را میخواند | [`AGENTS.md`](AGENTS.md) |
| ۵ سابایجنت آمادهٔ Claude Code / Cursor / Arena | `.claude/agents/ui-0X-*.md` |
| وضعیت ماشینخوانا (`active: true`) | `agents/uiux-agent-team/ACTIVATION.json` |
| اسکریپت فعالسازی/بررسی/غیرفعالسازی (بدون وابستگی) | [`tools/activate_uiux_team.py`](tools/activate_uiux_team.py) |
| نخستین خروجی واقعی تیم (ممیزی سایت، ۷۲/۱۰۰) | [`output/first-audit.md`](agents/uiux-agent-team/output/first-audit.md) |

### اعضا

`ui-01-research` پژوهش و بنچمارک · `ui-02-ux-strategy` استراتژی UX و IA ·
`ui-03-visual-design` طراحی بصری و سیستم طراحی · `ui-04-motion` حرکت و تعامل ·
`ui-05-frontend-qa` پیادهسازی فرانتاند و QA.

### نحوهٔ استفاده

- در همین مخزن بنویسید **`/uiux`**، **`@تیم-طراحی`**، `/ممیزی`، `/UX`،
  `/طراحی`، `/حرکت` یا `/QA` — `AGENTS.md` درخواست را به ایجنت درست مسیریابی میکند.
- یا محتوای [`ACTIVATE.md`](agents/uiux-agent-team/ACTIVATE.md) را در هر چت
  جدید (Arena/ChatGPT/Claude/Gemini/Cursor) پیست کنید تا کل تیم بالا بیاید.
- خط تولید: بریف → ایجنت ۱ → ۲ → (۳ و ۴ همزمان) → ۵ → `qa-report.md`.
  خروجیها در `agents/uiux-agent-team/output/` ذخیره میشوند.

### مدیریت وضعیت

```bash
python3 tools/activate_uiux_team.py --check       # بررسی یکپارچگی و فایلهای تولیدشده
python3 tools/activate_uiux_team.py               # فعالسازی/بازتولید (idempotent)
python3 tools/activate_uiux_team.py --deactivate  # حذف فایلهای تولیدشده (بستهٔ اصلی میماند)
```

---

## ۱۳. ممیزی و رفع کامل مشکلات UI/UX

در پاسخ به درخواست «بررسی کامل از نگاه متخصص UI و UX و رفع همهٔ مشکلات»،
تیم `uiux-agent-team` روی **کل قالب** اجرا شد (گزارش کامل:
[`UIUX-REPORT.md`](UIUX-REPORT.md)، خلاصهٔ تیم:
[`agents/uiux-agent-team/output/uiux-full-audit.md`](agents/uiux-agent-team/output/uiux-full-audit.md)).

### چه چیزی رفع شد

| حوزه | رفع |
| --- | --- |
| 🎨 UI / کنتراست | ۱۳ جفت رنگ اصلاح شدند؛ همهٔ متنها ≥ ۴٫۵:۱ (WCAG 2.2 AA) |
| 🎨 UI / حالتها | فوکوس ۳px سراسری، خوانایی هدر روی عکس، رفع نوار سفید skip link، `scroll-padding-top` |
| 🎨 UI / تصاویر | ۲۷ WebP (‎−۶۰٪)، `<picture>`, ابعاد واقعی ۶۱/۶۱، `loading`/`fetchpriority` |
| 🧭 UX / فرمها | پیام صادقانه + ارسال واقعی از طریق واتساپ/تلفن/ایمیل + `formEndpoint` قابل تنظیم + رضایت + honeypot + انقضای ۳۰ روز |
| 🧭 UX / IA | breadcrumb در ۲۰ صفحه، لینک ۵ صفحهٔ یتیم، `data-active-nav`، ۴۰۴ واقعی |
| 🧭 UX / منو | رفع قفل اسکرول در resize، focus trap، `aria-label` پویا |
| 🧭 UX / محتوا | تلفن/ساعات/آدرس/شبکههای اجتماعی یکسان شدند (`js/config.js`) |
| 🌐 دوزبانگی | ۳۸۸ رشتهٔ FA→EN؛ بعد از EN **۰ حرف فارسی** در ۲۲/۲۲ صفحه |
| ♿ دسترسپذیری | ۲۲/۲۲ صفحه یک `h1`؛ `alt` + ابعاد + `<label for>` بومی + `aria-live` |
| 🔍 SEO | canonical، OG، twitter card، sitemap، robots، 404، JSON‑LD، web manifest |
| 🧹 کد | ۰ استایل درونخطی، ۰ `&` خام، ۰ `tel:` با فاصله، ۰ خطای `html-validate` |

### ابزارهای جدید (همه بدون وابستگی، جز موارد مشخصشده)

| فایل | کار |
| --- | --- |
| `tools/uiux_fix.py` | اعمال idempotent تمام تغییرات HTML روی ۲۲ صفحه (نشانگر `data-uiux="2.0"`) |
| `tools/gen_webp.py` | ساخت WebP + `tools/image-dimensions.json` (نیازمند Pillow) |
| `tools/i18n_scan.py` | اسکنر DOM برای رشتههای قابلترجمه |
| `tools/build_i18n.py` | ساخت `js/i18n-content.js` + جلوگیری از ترجمهٔ ناقص |
| `tools/translations.json` | منبع ۳۸۸ رشتهٔ FA→EN |
| `tools/uiux_audit.py` | ممیزی وزندار ۴۷ چکی (امتیاز ۱۰۰/۱۰۰) |
| `tools/set_site_url.py` | تغییر دامنه در تمام فایلها با یک دستور |
| `js/config.js` | منبع واحد تنظیمات کسبوکار |

ترتیب اجرا در صورت بازتولید:

```bash
python3 tools/gen_webp.py
python3 tools/uiux_fix.py
python3 tools/build_i18n.py
python3 tools/set_site_url.py https://your-domain.ir   # اختیاری
python3 tools/uiux_audit.py --strict
```

### پیش از انتشار (تصمیمهای باقیمانده)

1. `python3 tools/set_site_url.py https://your-domain.ir` — دامنهٔ پیشفرض
   `https://laicodesign.ir` را عوض کنید (در canonical/OG/sitemap/robots/config).
2. `js/config.js` → `formEndpoint` (و در صورت تمایل `email`) را پر کنید.
3. ساعات و آدرس نهایی را با صاحب برند تأیید کنید.
4. در وبسرور: معرفی `404.html` بهعنوان ErrorDocument، هدرهای کش برای فونت/تصاویر،
   CSP / `Referrer-Policy` / `X-Content-Type-Options` و فشردهسازی.
5. (اختیاری) فهرست ۱۰–۲۰ سایت رقیب را بدهید تا ایجنت ۱ بنچمارک خارجی را تکمیل کند.

اسکرینشاتهای تأیید: [`reference/uiux/`](reference/uiux/).

### 📦 انتشار نسخهٔ نهایی (Release)

| نسخه | لینک |
| --- | --- |
| **v2.1.0-uiux** (Latest) | [صفحهٔ ریلیز](https://github.com/amolnovin/licodesign/releases/tag/v2.1.0-uiux) · [Source code (zip)](https://codeload.github.com/amolnovin/licodesign/zip/refs/tags/v2.1.0-uiux) |
| v2.0.1-uiux | [صفحهٔ ریلیز](https://github.com/amolnovin/licodesign/releases/tag/v2.0.1-uiux) |
| v2.0.0-uiux | [صفحهٔ ریلیز](https://github.com/amolnovin/licodesign/releases/tag/v2.0.0-uiux) |

- [`release/laico-design-v2.1.0.zip`](release/laico-design-v2.1.0.zip) — **بستهٔ فقط سایت**
  (۴٫۲۶ مگابایت، ۹۷ فایل): ۲۲ صفحهٔ HTML، CSS، JS، فونتها، JPG+WebP،
  `404.html`, `robots.txt`, `sitemap.xml`, `site.webmanifest`.
  استخراجشده و بررسی شد: **۰ ارجاع محلی شکسته** — مستقیماً آپلود کنید.
  بازتولید: `python3 tools/build-site-zip.py`.
- [`release/laico-design-uiux-v2.0.0.zip`](release/laico-design-uiux-v2.0.0.zip) —
  بستهٔ کامل مخزن (سایت + ابزارها + مستندات + تصاویر مرجع).
- راهنمای دانلود و دلیل عدم الصاق Asset: [`release/README.md`](release/README.md).
- تاریخچهٔ نسخهها: [`CHANGELOG.md`](CHANGELOG.md).

> محیط اجرا به `uploads.github.com` دسترسی ندارد، بنابراین ZIPها داخل مخزن
> کامیت شدهاند و لینک دانلودشان در صفحهٔ ریلیز قرار گرفته است (در صفحهٔ ریلیز،
> گزینهٔ خودکار **Assets → Source code (zip)** همان بستهٔ کامل است).
> برای الصاق واقعی Asset از سیستم خود بزنید:
> `gh release upload v2.1.0-uiux release/laico-design-v2.1.0.zip --clobber --repo amolnovin/licodesign`.
