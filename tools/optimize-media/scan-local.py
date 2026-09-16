#!/usr/bin/env python3
"""Scan Desktop/Documents/Downloads for html/txt/json/md chat exports."""
from pathlib import Path
import json

HOME = Path.home()
ROOTS = [HOME / "Desktop", HOME / "Documents", HOME / "Downloads"]
EXTS = {".html", ".txt", ".json", ".md"}
SKIP = {"node_modules", ".git", "__pycache__", "AppData"}
KW = ("chat", "conversation", "conversacion", "claude", "gpt", "gemini",
      "base44", "buildai", "belentani", "judas", "omega", "lore",
      "export", "backup", "drive", "transcript")

def scan():
    hits = []
    for root in ROOTS:
        if not root.exists():
            print(f"MISS {root}")
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if any(s in p.parts for s in SKIP):
                continue
            if p.suffix.lower() not in EXTS:
                continue
            try:
                sz = p.stat().st_size
            except OSError:
                continue
            if sz > 15_000_000:
                continue
            name_hit = any(k in p.name.lower() for k in KW)
            hits.append((sz, str(p), name_hit))
    hits.sort(reverse=True)
    print(f"TOTAL candidates: {len(hits)}")
    print("=== TOP 60 by size ===")
    for sz, p, nh in hits[:60]:
        print(f"{sz//1024}KB  {'[KW]' if nh else ''}  {p}")
    print("=== KEYWORD matches (any size) ===")
    kwh = [(s, p) for s, p, nh in hits if nh]
    for sz, p in kwh[:60]:
        print(f"{sz//1024}KB  {p}")
    if not kwh:
        print("(none)")
    # Google Drive check
    for c in ["Google Drive", "Mi unidad", "My Drive"]:
        g = HOME / c
        print(f"Drive {g}: {'OK' if g.exists() else 'NO'}")
    for g in [Path("G:/Mi unidad"), Path("G:/My Drive"), Path("G:/")]:
        print(f"Drive {g}: {'OK' if g.exists() else 'NO'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(scan())
