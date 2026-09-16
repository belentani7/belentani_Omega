#!/usr/bin/env python3
"""Summarize big local HTML exports: title, h1/h2, img count, urls."""
from pathlib import Path
import re
import sys

FILES = [
    r"C:\Users\USER\Downloads\NOIACORE\Judas Experience ｜ BuildAI (7_26_2026 5：12：55 AM).html",
    r"C:\Users\USER\Downloads\NOIACORE\belentani_omega_30k_1.html",
    r"C:\Users\USER\Downloads\NOIACORE\belentani_portal_3k_1.html",
    r"C:\Users\USER\Downloads\NOIACORE\BELENTANI _ Ruptura y señal (8_7_2026 12：41：43 PM).html",
    r"C:\Users\USER\Downloads\NOIACORE\Belentani_Web_GUI_1.html",
]

def summ(path: str) -> None:
    p = Path(path)
    print("=" * 78)
    print(p.name, round(p.stat().st_size / 1024), "KB")
    t = p.read_text(encoding="utf-8", errors="replace")[:300000]
    titles = re.findall(r"<title[^>]*>(.*?)</title>", t, re.I | re.S)[:1]
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.I | re.S)[:3]
    h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", t, re.I | re.S)[:8]
    imgs = re.findall(r"<img", t, re.I)
    srcs = re.findall(r"src=\"([^\"]{0,160})\"", t, re.I)[:12]
    urls = sorted(set(re.findall(r"https?://[A-Za-z0-9_./:@?=&%#+-]{4,120}", t)))[:15]
    keys = re.findall(r"JUDAS|BELENTANI|DIAMOND|PORTAL|ORACLE|ZION|DUCK|NOIACORE", t)[:6]
    strip = lambda s: re.sub(r"<[^>]+>", "", s).strip()[:110]
    print("TITLE:", [strip(x) for x in titles])
    print("H1:", [strip(x) for x in h1])
    print("H2:", [strip(x) for x in h2])
    print("IMG tags:", len(imgs))
    print("SRC sample:", srcs)
    print("URL sample:", urls)
    print("KEYS:", keys)

if __name__ == "__main__":
    targets = sys.argv[1:] or FILES
    for f in targets:
        try:
            summ(f)
        except OSError as e:
            print("MISS", f, e)
