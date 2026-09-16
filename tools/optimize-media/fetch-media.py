#!/usr/bin/env python3
"""Fetch third-party hotlinked media and republish it locally, optimized.

Removes the dependency on files.catbox.moe (privacy + availability + CLS).
Original bytes are never deleted: this only ADDS optimized copies under
assets/images/. Re-runnable (idempotent).

Usage:  python tools/optimize-media/fetch-media.py
"""
from __future__ import annotations

import io
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "images"

# remote URL -> local filename
SOURCES: dict[str, str] = {
    "https://files.catbox.moe/943t1r.png": "artist.png",
    "https://files.catbox.moe/8s1v5g.jpg": "artist-gaze.jpg",
    "https://files.catbox.moe/h0wamv.jpg": "judas.jpg",
    "https://files.catbox.moe/tf46wf.jpg": "zion-warrior.jpg",
    "https://files.catbox.moe/iobmrn.png": "zion.png",
}

MAX_W = 1400


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "belentani-media/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return resp.read()


def optimize(raw: bytes, dest_stem: str) -> tuple[str, tuple[int, int]]:
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    dest = OUT / f"{dest_stem}.webp"
    im.save(dest, "WEBP", quality=82, method=6)
    return dest.name, im.size


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ok = 0
    for url, name in SOURCES.items():
        stem = Path(name).stem
        try:
            raw = fetch(url)
            out_name, size = optimize(raw, stem)
            kb = (OUT / out_name).stat().st_size // 1024
            print(f"OK   {url}  ->  assets/images/{out_name}  {size[0]}x{size[1]}  {kb} KB")
            ok += 1
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {url}  {exc}", file=sys.stderr)
    print(f"\n{ok}/{len(SOURCES)} assets localized in {OUT}")
    return 0 if ok == len(SOURCES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
