#!/usr/bin/env python3
"""Extrae las imágenes incrustadas (base64 data URI) de HTML locales.

Los exports de BuildAI / Drive pesan 59 MB y no tienen <img src>: llevan las
imágenes dentro del HTML como data:image/...;base64,. Este script las
decodifica a ficheros reales en assets/imports/<slug>/.

Solo LEE los HTML de origen. Nunca los modifica.

Uso:
  python tools/optimize-media/extract-inline-images.py --dir "G:/.../BELENTANI-WEB"
  python tools/optimize-media/extract-inline-images.py archivo.html --min-kb 8
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEST = REPO / "assets" / "imports"
REPORT = REPO / "docs" / "context-pack" / "80-inline-extraidos.json"

RE_DATAURI = re.compile(
    r"data:(image/(?:png|jpeg|jpg|webp|gif|avif|svg\+xml|bmp|x-icon|vnd\.microsoft\.icon))"
    r"\s*;\s*base64\s*,\s*([A-Za-z0-9+/=\s]{64,})", re.I)

EXT_MAP = {
    "image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
    "image/webp": ".webp", "image/gif": ".gif", "image/avif": ".avif",
    "image/svg+xml": ".svg", "image/bmp": ".bmp",
    "image/x-icon": ".ico", "image/vnd.microsoft.icon": ".ico",
}


def slug(texto: str) -> str:
    limpio = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return (limpio or "html")[:44]


def extrae(path: Path, subdir: Path, min_kb: float) -> list[dict]:
    try:
        texto = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"  ! no leído: {e}")
        return []

    hallados: list[dict] = []
    vistos: set[str] = set()
    for i, m in enumerate(RE_DATAURI.finditer(texto), start=1):
        mime, b64 = m.group(1).lower(), m.group(2)
        crudo = re.sub(r"\s+", "", b64)
        try:
            datos = base64.b64decode(crudo, validate=False)
        except (binascii.Error, ValueError):
            continue
        kb = len(datos) / 1024
        if kb < min_kb:
            continue
        h = hashlib.sha1(datos).hexdigest()
        if h in vistos:            # dedupe: muchos exports repiten los mismos blobs
            continue
        vistos.add(h)
        ext = EXT_MAP.get(mime, ".png")
        nombre = f"{slug(path.stem)}-{i:03d}-{h[:8]}{ext}"
        subdir.mkdir(parents=True, exist_ok=True)
        destino = subdir / nombre
        try:
            destino.write_bytes(datos)
        except OSError as e:
            print(f"  ! no escrito {nombre}: {e}")
            continue
        hallados.append({"archivo": str(destino), "kb": round(kb, 1),
                         "mime": mime, "sha1": h, "origen": str(path)})
    return hallados


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*", help="rutas de HTML")
    ap.add_argument("--dir", help="carpeta con HTML")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--min-kb", type=float, default=5, help="tamaño mínimo por imagen")
    ap.add_argument("--dry-run", action="store_true", help="no escribe ficheros")
    args = ap.parse_args()

    rutas = [Path(p) for p in args.archivos]
    if args.dir:
        d = Path(args.dir)
        if not d.exists():
            print(f"no existe: {d}")
            return 1
        rutas += sorted(d.glob("*.html"), key=lambda p: -p.stat().st_size)[:args.limit]
    rutas = [p for p in rutas if p.exists()]
    if not rutas:
        print("sin ficheros (usa rutas o --dir)")
        return 1

    todo: list[dict] = []
    for p in rutas:
        print(f"· {p.name[:70]} ({round(p.stat().st_size/1024)} KB)")
        if args.dry_run:
            texto = p.read_text(encoding="utf-8", errors="replace")
            n = len(RE_DATAURI.findall(texto))
            print(f"  (dry-run) candidatos: {n}")
            continue
        got = extrae(p, DEST / slug(p.stem), args.min_kb)
        print(f"  extraídas: {len(got)}")
        todo += got

    if not args.dry_run:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps({
            "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "destino": str(DEST), "total": len(todo), "imagenes": todo,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        mb = sum(x["kb"] for x in todo) / 1024
        print(f"\nTOTAL {len(todo)} imágenes · {mb:.1f} MB -> {DEST}")
        print(f"OK -> {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())