# منبع و یکپارچگی بسته

| مورد | مقدار |
| --- | --- |
| مخزن مبدأ | https://github.com/amolnovin/aiagent.amolnovin |
| مسیر در مخزن مبدأ | `teams/ui-ux` (نسخهٔ استخراجشده) |
| آرشیو اصلی | `archives/uiux-agent-team.zip` (کپی شده در `_source/`) |
| نام بسته | `uiux-elite-team` v1.0.0 — زبان `fa` — دانش تا `2026-10` |
| SHA‑256 آرشیو | `b8013fe61ca8599cbd8fe56cdf25c6f9224af5261b61c4ebd8b879f30d0ae627` |
| تأیید هش | `sha256sum -c CHECKSUMS.sha256` در مخزن مبدأ → `uiux-agent-team.zip: OK` |
| تعداد فایل | ۱۳ فایل (۵ playbook + ۲ knowledge + ۳ قالب starter + README + agents.json + workflow) |
| مقایسه | تکتک فایلهای استخراجشده با محتوای ZIP برابر بودند (۰ اختلاف) |

فایلهای این پوشه **بدون تغییر** از مخزن مبدأ کپی شدهاند. فایلهای اضافهشده
در این مخزن (خروجی فعالسازی) عبارتاند از:
`ACTIVATE.md`، `SOURCE.md`، `ACTIVATION.json`، `_source/` و `output/`.

راستیآزمایی مجدد:

```bash
sha256sum agents/uiux-agent-team/_source/uiux-agent-team.zip
python3 tools/activate_uiux_team.py --check
```
