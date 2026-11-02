#!/usr/bin/env python3
"""Dependency-free scanner for translatable strings in the LAICO HTML files.

Used by tools/build_i18n.py to prove that the fa->en content map is complete.
It walks the DOM with html.parser (not regex) so nested markup, entities and
attributes are handled the same way a browser sees them.

A string is "owned" (and therefore skipped) when it sits inside an element that
already has its own translation mechanism:
  [data-i18n], [data-i18n-placeholder], [data-i18n-aria],
  [data-prj-i18n*], .lang-fa, .lang-en, [data-no-i18n],
  <script>, <style>, <svg>, <noscript>, <template>
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

FA = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")
SKIP_ATTRS = {
    "data-i18n", "data-i18n-placeholder", "data-i18n-aria",
    "data-prj-i18n", "data-prj-i18n-placeholder", "data-prj-i18n-aria",
    "data-no-i18n",
}
SKIP_TAGS = {"script", "style", "svg", "noscript", "template"}
TRANS_ATTRS = ("placeholder", "aria-label", "alt", "title")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Scanner(HTMLParser):
    def __init__(self, path: str):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack: list[tuple[str, dict, bool]] = []
        self.found: dict[str, dict] = {}

    def _add(self, value: str, kind: str) -> None:
        value = (value or "").strip()
        if not value or not FA.search(value):
            return
        entry = self.found.setdefault(value, {"kinds": set(), "pages": set()})
        entry["kinds"].add(kind)
        entry["pages"].add(self.path)

    @staticmethod
    def _is_skipped(tag: str, attrs: dict) -> bool:
        if tag in SKIP_TAGS:
            return True
        if any(a in attrs for a in SKIP_ATTRS):
            return True
        classes = set((attrs.get("class") or "").split())
        return bool(classes & {"lang-fa", "lang-en"})

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        parent_skip = self.stack[-1][2] if self.stack else False
        skip = parent_skip or self._is_skipped(tag, a)
        if not skip:
            for name in TRANS_ATTRS:
                if name in a:
                    self._add(a[name], "attr:" + name)
            if tag == "meta":
                key = a.get("name") or a.get("property")
                if key in {"description", "og:description", "og:title", "og:site_name"}:
                    self._add(a.get("content", ""), "meta:" + key)
        if tag not in VOID:
            self.stack.append((tag, a, skip))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.stack and self.stack[-1][2]:
            return
        self._add(data, "text")


def scan_file(path: Path) -> dict[str, dict]:
    s = Scanner(path.name)
    s.feed(path.read_text(encoding="utf-8"))
    s.close()
    return s.found


def scan_all(root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(root.glob("*.html")):
        for value, meta in scan_file(p).items():
            entry = out.setdefault(value, {"kinds": set(), "pages": set()})
            entry["kinds"] |= meta["kinds"]
            entry["pages"] |= meta["pages"]
    return out
