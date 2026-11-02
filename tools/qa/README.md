# اختیاری — تستهای مرورگری (QA)

این سه اسکریپت همان تستهایی هستند که گزارش `UIUX-REPORT.md` بر اساس آنها
تأیید شده است. برای اجرای محلی به Node.js 20+ و بستههای زیر نیاز دارند
(نصب در پوشهٔ `.qa/` که توسط Git نادیده گرفته میشود):

```bash
mkdir -p .qa && cd .qa
npm init -y
npm install jsdom@26 html-validate@9 puppeteer-core@24 @sparticuz/chromium
cd ..
# یک سرور استاتیک در پورت ۸۷۶۵ اجرا کنید (در ترمینال جداگانه):
python3 -m http.server 8765 --bind 127.0.0.1
# سپس:
node tools/qa/test-behavior.mjs     # ۲۵۱ تست رفتاری (jsdom)
node tools/qa/test-all-pages.mjs    # ۲۴۲ چک روی ۲۲ صفحه × ۳ عرض + EN
node tools/qa/test-render.mjs       # ۵۴۵ چک رندر + اسکرینشاتها
```

برای `test-render.mjs` و `test-all-pages.mjs` یک باینری Chromium لازم است.
مسیر آن را با `CHROMIUM_PATH` و آدرس سرور را با `QA_BASE_URL` مشخص کنید:

```bash
CHROMIUM_PATH=/path/to/chromium QA_BASE_URL=http://127.0.0.1:8765/ \
  node tools/qa/test-render.mjs
```

اسکریپت `test-render.mjs` پیشنمایشها را در `reference/uiux/` مینویسد.
تستهای بدون وابستگی (`tools/audit.py`, `tools/uiux_audit.py`,
`tools/build_i18n.py`) برای استفادهٔ روزمره کافیاند.
