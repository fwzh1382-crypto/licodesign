#!/usr/bin/env python3
"""Build a compact, deployable ZIP containing ONLY the website.

Unlike tools/build-release-zip.py (which packages the whole repository with
docs, tools and design references), this produces the folder you can upload
straight to a web server: unzip -> index.html, css/, js/, assets/, 404.html...

    python3 tools/build-site-zip.py                       # default name
    python3 tools/build-site-zip.py laico-design-v2.0.1.zip

The archive is written to release/ and its integrity is verified.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = "laico-design-v2.1.0.zip"

TOP_FILES = [
    "404.html", "robots.txt", "sitemap.xml", "site.webmanifest",
    "README.md", "CHANGELOG.md",
]
DIRS = ["css", "js", "assets"]


def collect() -> list[tuple[Path, str]]:
    items: list[tuple[Path, str]] = []
    for page in sorted(ROOT.glob("*.html")):
        items.append((page, page.name))
    for name in TOP_FILES:
        p = ROOT / name
        if p.is_file():
            items.append((p, name))
    for d in DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                items.append((p, p.relative_to(ROOT).as_posix()))
    # unique, deterministic
    seen = set()
    out = []
    for p, rel in items:
        if rel not in seen:
            seen.add(rel)
            out.append((p, rel))
    return out


def main() -> int:
    name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    if not name.endswith(".zip"):
        name += ".zip"
    out = ROOT / "release" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    items = collect()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, rel in items:
            zf.write(path, rel)
    with zipfile.ZipFile(out) as zf:
        assert zf.testzip() is None, "corrupt ZIP"
        names = zf.namelist()
        for required in ("index.html", "404.html", "css/styles.css", "js/main.js",
                         "js/config.js", "js/i18n-content.js",
                         "assets/images/hero.webp", "robots.txt", "sitemap.xml"):
            assert required in names, f"{required} missing from ZIP"
    print(f"{out.relative_to(ROOT)}: {out.stat().st_size/1024/1024:.2f} MB, {len(items)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
