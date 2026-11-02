#!/usr/bin/env python3
"""Generate WebP mirrors of every JPG and record real pixel dimensions.

Part of the UI/UX remediation (performance + cumulative layout shift).
Idempotent: an existing WebP is only rewritten when the JPG is newer.

    python3 tools/gen_webp.py

Outputs:
  assets/images/<name>.webp          for every .jpg
  tools/image-dimensions.json        {"assets/images/x.jpg": [w, h], ...}
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images"
OUT = ROOT / "tools" / "image-dimensions.json"


def main() -> None:
    dims: dict[str, list[int]] = {}
    saved = 0
    for jpg in sorted(IMG_DIR.glob("*.jpg")):
        rel = jpg.relative_to(ROOT).as_posix()
        with Image.open(jpg) as im:
            dims[rel] = [im.width, im.height]
            webp = jpg.with_suffix(".webp")
            if webp.exists() and webp.stat().st_mtime >= jpg.stat().st_mtime:
                continue
            rgb = im.convert("RGB")
            rgb.save(webp, "WEBP", quality=82, method=6)
            saved += im.width * 0  # keep Pillow reference explicit
    OUT.write_text(json.dumps(dims, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    jpg_bytes = sum(p.stat().st_size for p in IMG_DIR.glob("*.jpg"))
    webp_bytes = sum(p.stat().st_size for p in IMG_DIR.glob("*.webp"))
    print(f"images: {len(dims)}  JPG {jpg_bytes/1024:.0f} KiB  WebP {webp_bytes/1024:.0f} KiB "
          f"({100 - 100*webp_bytes/max(jpg_bytes,1):.0f}% smaller)")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
