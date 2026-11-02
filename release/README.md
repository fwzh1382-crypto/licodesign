# فایلهای قابل دانلود (Releases)

| فایل | محتوا | حجم |
| --- | --- | --- |
| `laico-design-v2.0.1.zip` | **بستهٔ فقط سایت** — آمادهٔ آپلود مستقیم روی وبسرور (پیشنهادی) | ~۵ MB |
| `laico-design-uiux-v2.0.0.zip` | بستهٔ کامل مخزن: سایت + ابزارها + مستندات + تصاویر مرجع | ~۱۹ MB |
| `laico-design-projects-v1.1.0.zip` | نسخهٔ قدیمی (بازطراحی پروژهها) | ~۱۲ MB |
| `laico-design-services-v1.0.0.zip` | نسخهٔ قدیمی (بازطراحی خدمات) | ~۱۱ MB |

## دانلود

سادهترین و مطمئنترین راه، بستهٔ خودکار گیتهاب در صفحهٔ ریلیز است
(**Assets → Source code (zip)**)، که دقیقاً همان فایلهای مخزن در تگ ریلیز را دارد:

- **[دانلود v2.1.0-uiux (Source code zip)](https://codeload.github.com/amolnovin/licodesign/zip/refs/tags/v2.1.0-uiux)**
- لینک مستقیم بستهٔ فقط سایت: <https://github.com/amolnovin/licodesign/raw/refs/heads/arena/7954847c-licodesign/release/laico-design-v2.1.0.zip>

> لینک `raw` در مرورگر عادی کار میکند ولی ممکن است توسط پروکسی بعضی محیطها
> مسدود شود. در آن صورت از همان لینک codeload بالا
> استفاده کنید؛ فایل ZIP موردنظر داخل پوشهٔ `release/` آن بسته قرار دارد.

## چرا Asset جداگانه الصاق نشد؟

محیط اجرای این پروژه فقط به `github.com`, `api.github.com` و
`codeload.github.com` دسترسی دارد؛ `uploads.github.com` (محل آپلود Assetهای
ریلیز) مسدود است و `api.github.com` هم مسیر آپلود Asset را نمیشناسد (HTTP 404).
به همین دلیل فایلهای ZIP در خود مخزن کامیت شدهاند و لینک دانلودشان در یادداشت
صفحهٔ ریلیز قرار گرفته است.

برای الصاق واقعی Asset، **از سیستم خودتان** اجرا کنید:

```bash
gh release upload v2.0.1-uiux \
  release/laico-design-v2.0.1.zip \
  --clobber --repo amolnovin/licodesign
```

## بازتولید بستهها

```bash
python3 tools/build-site-zip.py                       # بستهٔ فقط سایت
python3 tools/build-release-zip.py laico-design-uiux-v2.0.0.zip  # بستهٔ کامل مخزن
```

## پیش از استقرار

```bash
python3 tools/set_site_url.py https://your-domain.ir
# سپس js/config.js ← formEndpoint / email / تأیید ساعات و آدرس
python3 tools/uiux_audit.py --strict
```
