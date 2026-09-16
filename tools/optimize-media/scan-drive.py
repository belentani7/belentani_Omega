#!/usr/bin/env python3
"""Indexa G: (Google Drive) + repos locales buscando material Belentani/Judas/Omega.

Solo LEE. Escribe un indice JSON en docs/context-pack/60-drive-index.json
y un resumen legible en docs/context-pack/60-drive-index.md

Uso:
  python tools/optimize-media/scan-drive.py            # escaneo por defecto
  python tools/optimize-media/scan-drive.py --quick    # solo carpetas clave
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "docs" / "context-pack"

KEY_RE = re.compile(r"belentani|judas|omega|noia|zion|duck|prisma|secure", re.I)
WEB_EXT = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".md", ".txt",
           ".svg", ".webp", ".png", ".jpg", ".jpeg", ".mp4", ".webm", ".wav", ".mp3"}
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "venv", ".venv",
             "__pycache__", ".cache", "$RECYCLE.BIN", ".Encrypted",
             "System Volume Information", "10_QUARANTINE_REVERSIBLE"}

# Carpetas de Drive con más probabilidad de contener material del universo.
DRIVE_ROOTS = [
    "NOIACORE", "noiacore_art_lab", "nexus_data_v2", "nexus_data_040",
    "INTELIGENCIA", "todo_mi_drive", "_CONTENIDO", "_ARCHIVOS",
    "belentani_office_pack_2027", "saved_from_chrome", "manos_abiertas_ai",
    "rh_fiscal_ultra_web", "bigfiles_no_borrar",
]

LOCAL_ROOTS = [
    Path.home() / "belentani-repos-master",
    Path.home() / ".tmp-duck-check",
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "Desktop",
    REPO,
]


def walk(root: Path, max_files: int, depth_limit: int = 6):
    """Recorre root podando ruido ANTES de descender.

    No usa Path.rglob porque rglob entra en node_modules/ antes de filtrar y
    revienta con junctions/symlinks rotos (WinError 3). Aquí se poda con
    os.scandir y cada directorio va aislado en su propio try/except.
    """
    import os

    stack = [(str(root), 0)]
    count = 0
    while stack:
        cur, depth = stack.pop()
        if depth > depth_limit:
            continue
        try:
            with os.scandir(cur) as it:
                entries = list(it)
        except (OSError, PermissionError):
            continue
        for e in entries:
            name = e.name
            if name in SKIP_DIRS:
                continue
            try:
                if e.is_dir(follow_symlinks=False):
                    stack.append((e.path, depth + 1))
                elif e.is_file(follow_symlinks=False):
                    yield Path(e.path)
                    count += 1
                    if count >= max_files:
                        return
            except OSError:
                continue


def scan(roots, label, max_files):
    found = {"files": [], "by_ext": {}, "by_dir": {}, "total": 0}
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for f in walk(root, max_files):
            if f.suffix.lower() not in WEB_EXT:
                continue
            try:
                size = f.stat().st_size
            except OSError:
                continue
            if size < 2048:
                continue
            entry = {
                "path": str(f),
                "kb": round(size / 1024, 1),
                "ext": f.suffix.lower(),
                "key": bool(KEY_RE.search(str(f))),
            }
            found["files"].append(entry)
            found["by_ext"][entry["ext"]] = found["by_ext"].get(entry["ext"], 0) + 1
            parent = str(f.parent)
            found["by_dir"][parent] = found["by_dir"].get(parent, 0) + 1
    found["total"] = len(found["files"])
    found["files"].sort(key=lambda e: -e["kb"])
    found["label"] = label
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="solo carpetas clave")
    ap.add_argument("--max", type=int, default=40000, help="máx ficheros por raíz")
    args = ap.parse_args()

    drive_root = None
    for letter in ("G:/", "H:/", "F:/"):
        cand = Path(letter)
        if cand.exists():
            drive_root = cand
            break

    result = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "drive_root": str(drive_root) if drive_root else None,
        "roots": {},
    }

    if drive_root:
        base = drive_root / ("Mi unidad" if (drive_root / "Mi unidad").exists() else ".")
        picked = DRIVE_ROOTS if not args.quick else DRIVE_ROOTS[:5]
        drive_roots = [base / d for d in picked] if (base != drive_root) else picked
        result["roots"]["drive"] = scan(drive_roots, "drive", args.max)
    else:
        result["roots"]["drive"] = {"total": 0, "files": [], "by_ext": {}, "by_dir": {},
                                    "label": "drive", "note": "sin unidad montada"}

    result["roots"]["local"] = scan(LOCAL_ROOTS, "local", args.max)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "60-drive-index.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Índice Drive + local (Belentani / Judas / Omega)", "",
             f"Generado: `{result['generated']}`  ",
             f"Unidad: `{result['drive_root']}`", ""]
    for label, data in result["roots"].items():
        lines += [f"## {label} — {data.get('total', 0)} ficheros", ""]
        if data.get("note"):
            lines.append(f"> {data['note']}")
        top = data.get("files", [])[:40]
        if top:
            lines += ["| KB | ext | ruta |", "|---|---|---|"]
            for e in top:
                lines.append(f"| {e['kb']} | `{e['ext']}` | `{e['path']}` |")
        lines.append("")
        ext = data.get("by_ext", {})
        if ext:
            tot = ", ".join(f"`{k}`×{v}" for k, v in sorted(ext.items(), key=lambda kv: -kv[1]))
            lines += [f"Por extensión: {tot}", ""]
    (OUT_DIR / "60-drive-index.md").write_text("\n".join(lines), encoding="utf-8")

    for label, data in result["roots"].items():
        print(f"{label}: {data.get('total', 0)} ficheros indexados")
    print(f"OK -> {OUT_DIR / '60-drive-index.json'}")
    print(f"OK -> {OUT_DIR / '60-drive-index.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
