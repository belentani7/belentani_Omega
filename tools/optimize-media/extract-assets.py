#!/usr/bin/env python3
"""Extract same-origin <img>/<video>/<audio> asset URLs from a page.

Honest scope: only extracts what the HTML already references (same-origin
local assets). It CANNOT clone Base44/BuildAI apps (JS-rendered, auth,
private). Manual path: open each site, right-click media > Save, drop
files into assets/imports/, then run this inventory to wire them up.

Usage:
  python tools/optimize-media/extract-assets.py https://tu-sitio/ --out assets/imports
  python tools/optimize-media/extract-assets.py --inventory
"""
from __future__ import annotations
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[2]
IMPORTS = ROOT / "assets" / "imports"
IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)
SRC_RE = re.compile(r'<source[^>]+src=["\']([^"\']+)["\']', re.I)
VID_RE = re.compile(r'<video[^>]+src=["\']([^"\']+)["\']', re.I)

def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "belentani-extract/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
        return r.read().decode("utf-8", "replace")

def extract(page_url: str) -> list[str]:
    html = fetch(page_url)
    found: list[str] = []
    for rx in (IMG_RE, SRC_RE, VID_RE):
        found += rx.findall(html)
    # absolutize + keep same-origin only
    host = urlparse(page_url).netloc
    out: list[str] = []
    for u in found:
        if u.startswith("data:"):
            continue
        absu = urljoin(page_url, u)
        if urlparse(absu).netloc == host:
            out.append(absu)
    return sorted(set(out))

def inventory() -> int:
    for base in (ROOT / "assets", ROOT / "img"):
        print(f"# {base.relative_to(ROOT)}")
        for p in sorted(base.rglob("*")):
            if p.is_file():
                print(f"  {p.relative_to(ROOT)}  {p.stat().st_size//1024} KB")
    return 0

def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--inventory":
        return inventory()
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    page = sys.argv[1]
    urls = extract(page)
    print(f"{len(urls)} same-origin assets in {page}:")
    for u in urls:
        print(" ", u)
    print("\nManual step: save each file (right-click > Save) into assets/imports/,")
    print("then re-run with --inventory. Only YOUR OWN media. Respect licenses.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
