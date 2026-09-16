#!/usr/bin/env python3
"""Extrae los assets base64 INLINE de HTML locales a assets/imports/.

Los exports de BuildAI / BELENTANI-WEB del Drive guardan las imágenes como
data URIs dentro del propio HTML (por eso pesan 59 MB con 0 referencias
externas). Este script las decodifica a ficheros reales.

Solo LEE el HTML origen. Escribe en assets/imports/<slug>/.
Nunca sobreescribe: si existe, salta (usa --force para reemplazar).

Uso:
  python tools/optimize-media/extract-inline-assets.py FILE.html
  python tools/optimize-media/extract-inline-assets.py --dir "G:/.../BELENTANI-WEB" --limit 5
  python tools/optimize-media/extract-inline-assets.py FILE.html --min-kb 24 --force
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT_ROOT = REPO / "assets" / "imports"

# data:image/png;base64,XXXX  — se corta en comilla, paréntesis o espacio.
RE_DATA = re.compile(
    r"data:(image|video|audio|font)/([a-z0-9.+-]+);base64,([A-Za-z0-9+/=\s]{64,})",
    re.I)

EXT_OK = {
    "image": {"png", "jpeg", "jpg", "webp", "gif", "avif", "svg+xml", "bmp", "x-icon"},
    "video": {"mp4", "webm", "quicktime", "ogg"},
    "audio": {"mpeg", "mp3", "wav", "ogg", "webm", "mp4", "aac"},
    "font": {"woff", "woff2", "ttf", "otf"},
}
# Firma binaria -> extensión real (por si el MIME miente).
MAGIC = [
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpg"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"RIFF", "webp"),          # RIFF....WEBP
    (b"\x00\x00\x00\x18ftyp", "mp4"),
    (b"\x00\x00\x00\x1cftyp", "mp4"),
    (b"\x00\x00\x00 ftyp", "mp4"),
    (b"ID3", "mp3"),
    (b"wOFF", "woff"),
    (b"wOF2", "woff2"),
    (b"\x1aE\xdf\xa3", "webm"),
]


def ext_real(blob: bytes, declarada: str) -> str:
    for firma, ext in MAGIC:
        if blob.startswith(firma):
            if ext == "webp" and blob[8:12] != b"WEBP":
                continue
            return ext
    if blob.lstrip()[:5].lower() in (b"<?xml", b"<svg "):
        return "svg"
    return "png" if declarada in ("jpg", "jpeg") else declarada.replace("svg+xml", "svg")


def slug(nombre: str) -> str:
    s = re.sub(r"[^\w.-]+", "-", nombre, flags=re.UNICODE).strip("-").lower()
    return (s or "html")[:60]


def extrae(path: Path, min_kb: float, force: bool) -> dict:
    texto = path.read_text(encoding="utf-8", errors="replace")
    destino = OUT_ROOT / slug(path.stem)
    destino.mkdir(parents=True, exist_ok=True)
    escritos, saltados, kb_total = [], 0, 0.0
    vistos = set()

    for tipo, sub, payload in RE_DATA.findall(texto):
        if sub.lower() not in EXT_OK[tipo.lower()]:
            continue
        limpio = re.sub(r"\s+", "", payload)
        try:
            blob = base64.b64decode(limpio, validate=False)
        except (ValueError, TypeError):
            continue
        if len(blob) < min_kb * 1024:
            continue
        ext = ext_real(blob, sub.lower())
        if len(blob) < 4096 and tipo == "font":
            continue
        h = hash(blob)
        if h in vistos:
            continue
        vistos.add(h)
        nombre = f"{tipo}-{len(escritos) + 1:03d}.{ext}"
        f = destino / nombre
        if f.exists() and not force:
            saltados += 1
            continue
        f.write_bytes(blob)
        kb = round(len(blob) / 1024, 1)
        kb_total += kb
        escritos.append({"fichero": str(f), "kb": kb, "mime": f"{tipo}/{sub}"})

    return {
        "origen": str(path), "destino": str(destino), "extraidos": len(escritos),
        "saltados": saltados, "kb_total": round(kb_total, 1), "ficheros": escritos,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*", help="rutas de HTML")
    ap.add_argument("--dir", help="carpeta con HTML")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--min-kb", type=float, default=20, help="tamaño mínimo por asset")
    ap.add_argument("--force", action="store_true", help="sobreescribir existentes")
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

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    resultados = []
    for p in rutas:
        r = extrae(p, args.min_kb, args.force)
        resultados.append(r)
        print(f"{p.name[:56]:<56} extraidos={r['extraidos']:<4} "
              f"saltados={r['saltados']:<4} {r['kb_total']} KB")
        for f in r["ficheros"][:6]:
            print(f"      {f['kb']:>9} KB  {Path(f['fichero']).name}  ({f['mime']})")

    total = sum(r["extraidos"] for r in resultados)
    kb = round(sum(r["kb_total"] for r in resultados), 1)
    salida = {"generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "html_origen": len(rutas), "assets_extraidos": total,
              "kb_total": kb, "resultados": resultados}
    indice = OUT_ROOT / "_index.json"
    previo = []
    if indice.exists():
        try:
            previo = json.loads(indice.read_text(encoding="utf-8")).get("lotes", [])
        except (ValueError, OSError):
            previo = []
    salida["lotes"] = previo + [salida.copy()]
    indice.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nTOTAL extraídos={total}  {kb} KB")
    print(f"OK -> {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())