#!/usr/bin/env python3
"""Generate PWA raster icons + a social og:image for belentani.es.

Additive only: writes new files under assets/icons/ and assets/images/.
Design: obsidian black + blood red (#ff003c) diamond, matching the canon.

Usage:  python tools/optimize-media/gen-assets.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
ICONS = ROOT / "assets" / "icons"
IMAGES = ROOT / "assets" / "images"

VOID = (5, 5, 5, 255)
BLOOD = (255, 0, 60, 255)
BLOOD_SOFT = (255, 0, 60, 90)


def diamond_icon(size: int, pad_ratio: float = 0.18) -> Image.Image:
    """Square icon: black plate + glowing red diamond."""
    ss = size * 4  # supersample for smooth edges
    img = Image.new("RGBA", (ss, ss), VOID)
    glow = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx = cy = ss / 2
    r = ss * (0.5 - pad_ratio)
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    gd.polygon(pts, fill=BLOOD_SOFT)
    glow = glow.filter(ImageFilter.GaussianBlur(ss * 0.06))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)
    d.polygon(pts, outline=BLOOD, width=max(2, int(ss * 0.012)))
    inner = r * 0.42
    ip = [(cx, cy - inner), (cx + inner, cy), (cx, cy + inner), (cx - inner, cy)]
    d.polygon(ip, fill=BLOOD)
    return img.resize((size, size), Image.LANCZOS)


def og_cover(width: int = 1200, height: int = 630) -> Image.Image:
    """Crop the hero poster to 1.91:1 and lay a red/black cinematic veil."""
    src = IMAGES.parent / "media" / "judas-poster.webp"
    if src.exists():
        base = Image.open(src).convert("RGB")
        ratio = width / height
        w, h = base.size
        if w / h > ratio:
            nw = int(h * ratio)
            base = base.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / ratio)
            base = base.crop((0, 0, w, nh))
        base = base.resize((width, height), Image.LANCZOS)
    else:
        base = Image.new("RGB", (width, height), (5, 5, 5))
    veil = Image.new("RGBA", (width, height), (5, 5, 5, 0))
    vd = ImageDraw.Draw(veil)
    for x in range(width):
        a = int(150 * (1 - x / width) ** 1.5)
        vd.line([(x, 0), (x, height)], fill=(5, 5, 5, a))
    base = Image.alpha_composite(base.convert("RGBA"), veil)
    d = ImageDraw.Draw(base)
    d.rectangle([0, height - 8, width, height], fill=BLOOD)
    d.rectangle([0, 0, 8, height], fill=BLOOD)
    return base.convert("RGB")


def main() -> int:
    ICONS.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)

    for size in (192, 512):
        p = ICONS / f"icon-{size}.png"
        diamond_icon(size).save(p, "PNG", optimize=True)
        print(f"OK  {p.relative_to(ROOT)}  {size}x{size}")

    # Maskable variant: extra safe-zone padding for Android.
    p = ICONS / "icon-maskable-512.png"
    diamond_icon(512, pad_ratio=0.30).save(p, "PNG", optimize=True)
    print(f"OK  {p.relative_to(ROOT)}  512x512")

    cover = IMAGES / "og-cover.jpg"
    og_cover().save(cover, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"OK  {cover.relative_to(ROOT)}  1200x630")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
