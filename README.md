# لایکو دیزاین (LAICO DESIGN)

قالب **سایت ایستا** برای استودیو معماری داخلی و سیستم آشپزخانه لوکس؛ راست‑به‑چپ (RTL)،
دوزبانهٔ فارسی/انگلیسی و بدون هیچ وابستگی، فریمورک یا مرحلهٔ build.

این مخزن شامل کدهای استخراج‌شده از فایل `laico.zip` (دانلودشده از Google Drive)،
اطلاعات پروژه، یک اسکریپت ممیزی و **[گزارش بررسی قالب](REVIEW.md)** است.

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
| نشانه‌گذاری | HTML5، ۲۱ صفحه، `<html lang="fa" dir="rtl">` |
| استایل | CSS3 خالص: متغیرها، logical properties (`inset-inline`, `padding-inline`)، Grid/Flexbox، `clamp()`، breakpointهای 1180/800/720px، حالت چاپ و `prefers-reduced-motion` |
| رفتار | JavaScript خالص (IIFE، بدون کتابخانه): ۴۳۱ خط در `js/main.js` |
| فونت | ۸ فایل `woff2` محلی: Vazirmatn (۵ وزن) + Outfit (۳ وزن)، همراه `font-display: swap` |
| تصاویر | ۲۸ فایل JPG محلی (۱۹ تصویر قالب + ۹ تصویر پروژه/صحنه)، ۱ favicon SVG، آیکون‌های شبکه‌های اجتماعی به صورت inline SVG |
| زیرساخت | نیازی به npm/build ندارد؛ فقط یک وب سرور استاتیک |

هیچ درخواستی به CDN، فونت گوگل، آنالیتیکس یا سرویس ثالث انجام نمی‌شود.

---

## ۳. ساختار مخزن

```text
.
├── index.html                 # صفحهٔ اصلی (نمونهٔ کامل همهٔ بخش‌ها)
├── about.html                 # دربارهٔ ما
├── services.html              # خدمات
├── projects.html              # آرشیو پروژه‌ها + فیلتر
├── project-firuzkuh.html      # پروژه کوهستانی فیروزکوه (آسور)
├── project-mahd-dozak.html    # مهد کودک نقش دوزک (آمل)
├── project-club.html          # باشگاه ورزشی آمل
├── project-cafe-amol.html     # طراحی کافه آمل
├── kitchen.html, living.html, bath.html, cafe.html   # چهار مجموعه
├── studio.html, systems.html, process.html, materials.html, showroom.html
├── journal.html               # مجله/مقالات
├── contact.html               # تماس + فرم
├── privacy.html, cookies.html # صفحات حقوقی
├── css/styles.css             # تمام استایل‌ها (۱٬۷۱۵ خط)
├── js/main.js                 # دیکشنری دوزبانه + تعاملات (۴۳۱ خط)
├── assets/
│   ├── fonts/                 # ۸ فایل woff2
│   ├── images/                # ۱۹ فایل JPG
│   └── favicon.svg
├── archive/laico.zip          # آرشیو اصلی دریافتی از Drive
├── tools/audit.py             # اسکریپت ممیزی بدون وابستگی
├── REVIEW.md                  # گزارش کامل بررسی قالب
└── README.md                  # همین فایل
```

---

## ۴. صفحات (۲۱ صفحه)

| گروه | فایل‌ها |
| --- | --- |
| اصلی و منو | `index.html`, `services.html`, `projects.html`, `journal.html`, `about.html`, `contact.html` |
| مجموعه‌ها | `kitchen.html`, `living.html`, `bath.html`, `cafe.html` |
| پروژه‌ها (واقعی) | `project-firuzkuh.html`, `project-mahd-dozak.html`, `project-club.html`, `project-cafe-amol.html` |
| استودیو/سیستم | `studio.html`, `systems.html`, `process.html`, `materials.html`, `showroom.html` |
| حقوقی | `privacy.html`, `cookies.html` |

### پروژه‌های واقعی (بخش «نمونه کارها، امضای کیفیت»)

| پروژه | مکان | اطلاعات | تصویر |
| --- | --- | --- | --- |
| پروژه کوهستانی فیروزکوه | روستای آسور | زمین ۵۰۰ متر، بنا ۱۰۰ متر، کارفرما خانم قاسمی | `proj-firuzkuh.jpg` |
| مهد کودک و آموزشگاه نقش دوزک | آمل، آفتاب ۳۱ | کارفرما خانم اکبری، طراحی ۱۴۰۲ | `proj-mahd-dozak.jpg` |
| باشگاه ورزشی آمل | آمل | کارفرما خانم پرستار، ۱۴۰۵، ۱۵۵ متر | `proj-club.jpg` (+ `proj-club-2.jpg`) |
| طراحی کافه آمل | آمل | طراحی داخلی و اجرا | `proj-cafe-amol.jpg` |

عکس قهرمان صفحهٔ اصلی (`hero.jpg`) و همین تصویر با شفافیت ۱۰٪ به‌عنوان پس‌زمینهٔ
بخش شو روم استفاده می‌شود.

هر صفحه شامل `<title>` و `meta description` منحصربه‌فرد، `og:title`، `og:description`،
`theme-color`، پیش‌بارگذاری ۲ فونت و هدر/فوتر مشترک است. وضعیت منوی فعال از روی
`data-page` در `<body>` و `data-nav` روی لینک‌ها تعیین می‌شود.

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

- **طراحی سیستم:** رنگ‌ها، فونت‌ها، فاصله‌ها و ارتفاع هدر در `:root` متمرکز شده است.
- **جلوگیری از پرش زبان:** یک اسکریپت کوتاه inline در `<head>` زبان ذخیره‌شده در
  `localStorage["laico-lang"]` را قبل از رنگ‌آمیزی صفحه اعمال می‌کند.
- **`js/main.js`:** دیکشنری `fa`/`en` (هرکدام ۹۸ کلید، ۸۰ کلید در صفحات استفاده شده)،
  تغییر زبان، هدر چسبان، منوی موبایل، `aria-current`، شمارندهٔ آمار، select سفارشی،
  فیلتر پروژه‌ها و اعتبارسنجی فرم.
- **ترجمه:** متن‌ها با `data-i18n`، `data-i18n-placeholder`، `data-i18n-aria` و
  جفت‌های `<span class="lang-fa">` / `<span class="lang-en" hidden>` انجام می‌شود؛
  عنوان صفحه از `data-title-fa` / `data-title-en` خوانده می‌شود.
- **فیلتر پروژه:** دکمه‌های `data-filter` و کارت‌های `data-kind` در `projects.html`.

---

## ۷. فرم‌های تماس — نکتهٔ مهم پیش از انتشار

چهار صفحه (`index.html`، `showroom.html`، `about.html`، `contact.html`) فرم دارند.
این فرم‌ها **فقط سمت کاربر** هستند: پس از اعتبارسنجی، اطلاعات در
`localStorage["laico-requests"]` ذخیره و پیام «درخواست شما ثبت شد» نمایش داده می‌شود؛
هیچ داده‌ای به سرور ارسال نمی‌شود. `privacy.html` و `cookies.html` همین موضوع را توضیح
می‌دهند، ولی این دو صفحه در هیچجا لینک نشده‌اند. برای استفادهٔ واقعی حتماً فرم را به یک
API/سرویس ایمیل متصل کنید — جزئیات در [REVIEW.md](REVIEW.md).

---

## ۸. بررسی کیفیت

```bash
python3 tools/audit.py            # لینک‌ها، دارایی‌ها، idهای تکراری، کلیدهای i18n، هشدارها
python3 tools/audit.py --strict   # هشدارها را هم به عنوان خطا برمی‌گرداند
node --check js/main.js           # صحت نحوی جاوااسکریپت
npx html-validate "*.html"        # اعتبارسنجی HTML (ابزار خارجی، اختیاری)
```

وضعیت فعلی `tools/audit.py`: **۰ خطا، ۳ هشدار** (سه صفحهٔ یتیم، `alt` خالی روی
تصاویر تزئینی و لینک عمومی یوتیوب در فوتر). خلاصهٔ کامل یافته‌ها، اولویت‌ها و پیشنهادهای اصلاحی
در **[REVIEW.md](REVIEW.md)** آمده است.

---

## ۹. مالکیت و مجوز

منبع قالب، فایل `laico.zip` دریافتی از Google Drive است و فایل `LICENSE` یا اعلام مجوزی
همراه آن نبوده است. پیش از انتشار تجاری، مالکیت محتوا/تصاویر و مجوز فونت‌ها و طرح را
با صاحب اثر مشخص کنید.
