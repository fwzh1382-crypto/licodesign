#!/usr/bin/env python3
"""Set the production origin in one command.

Canonical tags, Open Graph URLs, JSON-LD, sitemap.xml, robots.txt and
js/config.js all share one absolute origin. Before deploying, run:

    python3 tools/set_site_url.py https://your-real-domain.example

The old origin is discovered from js/config.js, so the command is repeatable.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "js" / "config.js"
FILES = (list(ROOT.glob("*.html")) + [CONFIG, ROOT / "robots.txt",
                                     ROOT / "sitemap.xml", ROOT / "tools" / "uiux_fix.py"])


def current() -> str:
    m = re.search(r'siteUrl:\s*"([^"]+)"', CONFIG.read_text(encoding="utf-8"))
    if not m:
        raise SystemExit("could not find siteUrl in js/config.js")
    return m.group(1).rstrip("/")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 tools/set_site_url.py https://your-domain.example")
        return 2
    new = sys.argv[1].rstrip("/")
    if not re.match(r"^https?://[^\s/]+$", new):
        print("error: expected an origin like https://example.com (no path, no slash)")
        return 2
    old = current()
    if old == new:
        print("already set to " + new)
        return 0
    n = 0
    for path in FILES:
        s = path.read_text(encoding="utf-8")
        if old not in s:
            continue
        path.write_text(s.replace(old, new), encoding="utf-8")
        n += 1
    print(f"replaced {old} -> {new} in {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
