#!/usr/bin/env python3
"""Activate the `uiux-agent-team` package in this repository.

Source: https://github.com/amolnovin/aiagent.amolnovin  ->  teams/ui-ux
The 13 source files are vendored verbatim under agents/uiux-agent-team/.
This script (re)generates the machine-readable activation artifacts:

  * .claude/agents/uiux-0X-*.md  — one subagent per team member, built from
    the `system_prompt` in agents.json (Claude Code / Cursor / Arena style)
  * agents/uiux-agent-team/ACTIVATION.json — status + integrity record
  * AGENTS.md — repo-level router so any coding agent finds the active team

It is idempotent: running it twice produces the same files.

Usage:
    python3 tools/activate_uiux_team.py           # activate / regenerate
    python3 tools/activate_uiux_team.py --check   # verify only, change nothing
    python3 tools/activate_uiux_team.py --deactivate

No third-party dependencies (standard library only).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAM = ROOT / "agents" / "uiux-agent-team"
MANIFEST = TEAM / "agents.json"
ZIP = TEAM / "_source" / "uiux-agent-team.zip"
ACTIVATE_MD = TEAM / "ACTIVATE.md"
STATUS = TEAM / "ACTIVATION.json"
SUBAGENTS = ROOT / ".claude" / "agents"
AGENTS_MD = ROOT / "AGENTS.md"
SOURCE_REPO = "https://github.com/amolnovin/aiagent.amolnovin"
EXPECTED_SHA256 = "b8013fe61ca8599cbd8fe56cdf25c6f9224af5261b61c4ebd8b879f30d0ae627"

# id -> short English slug + one-line "when to use" hint for the subagent header
HINTS = {
    "ui-01-research": "Research & benchmark analyst — use for competitor/reference-site scans and audit scoring.",
    "ui-02-ux-strategy": "UX strategist & IA — use for personas, journeys, sitemap and prioritised UX problems.",
    "ui-03-visual-design": "Visual designer & design system — use for design tokens, layouts, style guides, WCAG contrast.",
    "ui-04-motion": "Motion & interaction engineer — use for scroll-driven animation, micro-interactions, reduced-motion.",
    "ui-05-frontend-qa": "Front-end implementer & QA — use for semantic HTML/CSS/JS, responsive checks and QA reports.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("package") != "uiux-elite-team":
        raise SystemExit("Unexpected manifest: 'package' is not uiux-elite-team")
    if len(data.get("agents", [])) != 5:
        raise SystemExit("Expected exactly 5 agents in manifest")
    return data


def validate() -> list[str]:
    """Return a list of problems (empty == OK)."""
    problems: list[str] = []
    if not MANIFEST.is_file():
        return [f"missing manifest: {MANIFEST.relative_to(ROOT)}"]
    data = load_manifest()

    for agent in data["agents"]:
        for key in ("id", "name_fa", "name_en", "playbook", "system_prompt", "responsibilities"):
            if not agent.get(key):
                problems.append(f"agent {agent.get('id','?')}: missing '{key}'")
        pb = TEAM / agent.get("playbook", "")
        if not pb.is_file():
            problems.append(f"missing playbook: {pb.relative_to(ROOT)}")

    for rel in data.get("shared_knowledge", []) + [a["playbook"] for a in data["agents"]]:
        if not (TEAM / rel).is_file():
            problems.append(f"missing knowledge/playbook file: {rel}")
    for rel in ("README.md", "workflow.md", "ACTIVATE.md"):
        if not (TEAM / rel).is_file():
            problems.append(f"missing required file: agents/uiux-agent-team/{rel}")
    for name in ("index.html", "styles.css", "script.js"):
        if not (TEAM / "templates" / "starter" / name).is_file():
            problems.append(f"missing starter template: {name}")

    if not ZIP.is_file():
        problems.append("missing source ZIP")
    elif sha256(ZIP) != EXPECTED_SHA256:
        problems.append("source ZIP SHA-256 does not match upstream CHECKSUMS.sha256")
    return problems


def subagent_text(agent: dict, shared: list[str]) -> str:
    slug = agent["id"]
    hint = HINTS.get(slug, agent["name_en"])
    lines = [
        "---",
        f"name: {slug}",
        f"description: {agent['name_fa']} ({agent['name_en']}). {hint}",
        "---",
        "",
        f"# {agent['name_fa']} — {agent['name_en']}",
        "",
        agent["system_prompt"],
        "",
        "## زبان و خروجی",
        "به فارسی پاسخ بده. خروجیها را در `agents/uiux-agent-team/output/` ذخیره کن.",
        "هر تحویل باید بخش «خلاصه» (۵ خط) و «باز» (سؤال یا ریسک) داشته باشد.",
        "هیچ ادعایی بدون شاهد (لینک، فایل، اسکرینشات یا داده) ننویس.",
        "",
        "## مسئولیتها",
    ]
    lines += [f"- {item}" for item in agent["responsibilities"]]
    lines += ["", "## دانش مرجع (حتماً بخوان)", ""]
    lines.append(f"- Playbook: `agents/uiux-agent-team/{agent['playbook']}`")
    for rel in shared:
        lines.append(f"- `agents/uiux-agent-team/{rel}`")
    lines += [
        "",
        "## اصول مشترک تیم",
        "- شاهدمحور؛ کاربر اول؛ حرکت با معنا؛ دسترسپذیری WCAG 2.2 AA بهصورت پیشفرض.",
        "- ریسپانسیو mobile-first با `clamp()`/`grid`؛ پشتیبانی از `prefers-reduced-motion`.",
        "- فقط `transform` و `opacity` انیمیت شوند؛ بدون کتابخانه غیرضروری.",
        "- متنها فارسی و `dir=\"rtl\"` مگر اینکه بریف زبان دیگری بخواهد.",
    ]
    return "\n".join(lines) + "\n"


def agents_md_text(data: dict, files: list[str]) -> str:
    rows = "\n".join(
        f"| `{a['id']}` | {a['name_fa']} | `agents/uiux-agent-team/{a['playbook']}` |" for a in data["agents"]
    )
    return f"""<!-- Generated by tools/activate_uiux_team.py — edit the script, not this file. -->
# AGENTS.md — تیم فعال در این مخزن

## ✅ `uiux-agent-team` v{data['version']} — **ACTIVE**

تیم ۵ نفره فوق\u200cتخصص UI/UX از مخزن [{SOURCE_REPO}]({SOURCE_REPO}) (`teams/ui-ux`)
در این پروژه **فعال** است. پرامپت فعالسازی کامل و خودکفا:
[`agents/uiux-agent-team/ACTIVATE.md`](agents/uiux-agent-team/ACTIVATE.md).

### اعضا

| ID | نقش | Playbook |
| --- | --- | --- |
{rows}

### تریگرها (هر وقت آمدند، پروتکل تیم اجرا شود)
`/uiux` · `@uiux` · `@تیم-طراحی` · `@پژوهش` · `@بنچمارک` · `@استراتژی` ·
`@طراحی` · `@حرکت` · `@فرانت` · `@QA` · `/ممیزی` · `/audit` · `/بنچمارک` ·
و هر درخواست طراحی/تجربه کاربری/دسترسپذیری/ریسپانسیو.

### پروتکل اجرا (`workflow.md`)
1. **بریف** بگیر: حوزه، برند، مخاطب، هدف، ۱۰–۲۰ سایت مرجع.
2. ایجنت ۱ → `benchmark-matrix.md`, `site-reviews/*.md`, `opportunities.md`
3. ایجنت ۲ → `ux-problems.md`, `user-journeys.md`, `sitemap-ia.md`
4. ایجنت ۳ و ۴ (همزمان) → `design-tokens.css`, `style-guide.md`, `motion-spec.md`
5. ایجنت ۵ → `index.html`, `styles.css`, `script.js`, `qa-report.md`
6. تحویل نهایی با **گزارش QA** و چک\u200cلیست پایانی `workflow.md`.

هر تحویل = «خلاصه» ۵ خط + «باز» (سؤال/ریسک). حدس زدن ممنوع؛ تصمیم برند فقط با
تأیید کاربر. حداقل ۳ مزیت مشخص نسبت به بنچمارک برای هر طرح جدید.

### دانش مشترک
- `agents/uiux-agent-team/knowledge/trends-2026.md` (روندهای ۲۰۲۶)
- `agents/uiux-agent-team/knowledge/site-audit-checklist.md` (چک\u200cلیست ممیزی)
- `agents/uiux-agent-team/workflow.md` (جریان کار و چک\u200cلیست پایانی)
- `agents/uiux-agent-team/templates/starter/` (قالب شروع HTML/CSS/JS)

### قوانین این مخزن
- خروجیها را در `agents/uiux-agent-team/output/` بنویس؛ فایلهای سایت را بدون
  درخواست صریح کاربر تغییر نده.
- ساختار کلی قالب لایکو (هدر/فوتر/`css/styles.css`/`js/main.js`) محفوظ است.
- فایلهای تولیدشده: {', '.join('`'+f+'`' for f in files)}
- وضعیت ماشین\u200cخوانا: `agents/uiux-agent-team/ACTIVATION.json`.
- غیرفعالسازی: `python3 tools/activate_uiux_team.py --deactivate`.
"""


def activate(check_only: bool = False) -> int:
    problems = validate()
    if problems:
        print("VALIDATION FAILED:")
        for p in problems:
            print("  ✗", p)
        return 1
    data = load_manifest()
    print("VALIDATION OK: 5 agents, 13 source files, ZIP SHA-256 verified.")

    generated: list[str] = []
    subagent_paths: list[str] = []
    for agent in data["agents"]:
        rel = f".claude/agents/{agent['id']}.md"
        subagent_paths.append(rel)
        if not check_only:
            path = ROOT / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(subagent_text(agent, data["shared_knowledge"]), encoding="utf-8")
        generated.append(rel)

    status = {
        "active": True,
        "team": data["package"],
        "version": data["version"],
        "language": data["language"],
        "knowledge_date": data["knowledge_date"],
        "source_repo": SOURCE_REPO,
        "source_path": "teams/ui-ux",
        "source_zip": "agents/uiux-agent-team/_source/uiux-agent-team.zip",
        "source_zip_sha256": EXPECTED_SHA256,
        "activation_prompt": "agents/uiux-agent-team/ACTIVATE.md",
        "manifest": "agents/uiux-agent-team/agents.json",
        "agents": [{"id": a["id"], "name_fa": a["name_fa"], "playbook": a["playbook"]} for a in data["agents"]],
        "subagents": subagent_paths,
        "repo_router": "AGENTS.md",
        "output_dir": "agents/uiux-agent-team/output",
    }
    files = subagent_paths + ["agents/uiux-agent-team/ACTIVATION.json", "AGENTS.md"]
    if check_only:
        missing = [f for f in files if not (ROOT / f).is_file()]
        print("CHECK:", "OK" if not missing else "missing " + ", ".join(missing))
        return 0 if not missing else 1

    STATUS.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    AGENTS_MD.write_text(agents_md_text(data, files), encoding="utf-8")
    print("ACTIVATED:")
    for f in files:
        print("  ✓", f)
    print("Team is live. Paste ACTIVATE.md into a chat, or use a trigger like /uiux.")
    return 0


def deactivate() -> int:
    removed = []
    for path in SUBAGENTS.glob("uiux-*.md"):
        path.unlink()
        removed.append(str(path.relative_to(ROOT)))
    for path in (STATUS, AGENTS_MD):
        if path.exists():
            path.unlink()
            removed.append(str(path.relative_to(ROOT)))
    print("DEACTIVATED. Removed:", ", ".join(removed) or "(nothing)")
    print("The vendored package under agents/uiux-agent-team/ was kept.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Activate the UI/UX agent team")
    ap.add_argument("--check", action="store_true", help="verify only, change nothing")
    ap.add_argument("--deactivate", action="store_true", help="remove generated activation artifacts")
    args = ap.parse_args()
    if args.deactivate:
        return deactivate()
    return activate(check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
