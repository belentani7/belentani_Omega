#!/usr/bin/env python3
"""Decodifica los ASSETS embebidos en base64 dentro de los HTML grandes.

Los exports de BuildAI / Drive / NOACORE guardan las imágenes como data URIs
(`data:image/webp;base64,...`). Este script los extrae a ficheros reales para
que puedan optimizarse y servirse desde el repo.

Solo LEE los HTML origen. Escribe SIEMPRE dentro del repo, en
assets/imports/<origen>/ — nunca toca las carpetas escaneadas.

Uso:
  python tools/optimize-media/extract-base64-assets.py --dir "G:/.../BELENTANI-WEB" --limit 10
  python tools/optimize-media/extract-base64-assets.py FILE.html --min-kb 4
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DESTINO = REPO / "assets" / "imports"
INFORME = REPO / "docs" / "context-pack" / "80-assets-extraidos.json"

EXT_POR_MIME = {
    "image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp",
    "image/gif": ".gif", "image/avif": ".avif", "image/svg+xml": ".svg",
    "image/bmp": ".bmp", "image/x-icon": ".ico", "image/vnd.microsoft.icon": ".ico",
    "video/mp4": ".mp4", "video/webm": ".webm", "audio/mpeg": ".mp3",
    "audio/wav": ".wav", "audio/webm": ".webm", "audio/mp4": ".m4a",
    "font/woff2": ".woff2", "font/woff": ".woff", "font/ttf": ".ttf",
    "application/font-woff": ".woff", "application/font-woff2": ".woff2",
}
# Solo extraemos binarios con valor visual/sonoro; se ignoran fuentes para no
# inflar el repo con licencias dudosas.
MIMES = tuple(k for k in EXT_POR_MIME if k.startswith(("image/", "video/", "audio/")))

RE_DATA = re.compile(
    r"data:(" + "|".join(re.escape(m) for m in MIMES) + r");base64,([A-Za-z0-9+/=\s]{64,})",
    re.I)


def slug(texto: str, maximo: int = 40) -> str:
    limpio = re.sub(r"[^A-Za-z0-9]+", "-", texto).strip("-").lower()
    return (limpio or "origen")[:maximo]


def extrae(html: Path, destino: Path, min_kb: float) -> dict:
    res = {"origen": str(html), "kb_html": round(html.stat().st_size / 1024, 1),
           "extraidos": [], "duplicados": 0, "descartados_pequenos": 0, "errores": 0}
    try:
        texto = html.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        res["error"] = str(e)
        return res

    vistos: set[str] = set()
    indice = 0
    for mime, payload in RE_DATA.findall(texto):
        mime = mime.lower()
        try:
            datos = base64.b64decode(re.sub(r"\s+", "", payload), validate=False)
        except Exception:
            res["errores"] += 1
            continue
        if len(datos) / 1024 < min_kb:
            res["descartados_pequenos"] += 1
            continue
        huella = hashlib.sha256(datos).hexdigest()[:16]
        if huella in vistos:
            res["duplicados"] += 1
            continue
        vistos.add(huella)
        indice += 1
        ext = EXT_POR_MIME.get(mime, ".bin")
        nombre = f"{indice:02d}-{huella}{ext}"
        destino.mkdir(parents=True, exist_ok=True)
        (destino / nombre).write_bytes(datos)
        res["extraidos"].append({"archivo": nombre, "mime": mime,
                                 "kb": round(len(datos) / 1024, 1)})
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*")
    ap.add_argument("--dir", help="carpeta con HTML grandes")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--min-kb", type=float, default=4.0,
                    help="ignorar assets menores de X KB (iconos diminutos)")
    ap.add_argument("--solo-listar", action="store_true",
                    help="no escribe ficheros, solo informa")
    args = ap.parse_args()

    rutas = [Path(p) for p in args.archivos]
    if args.dir:
        d = Path(args.dir)
        if not d.exists():
            print(f"no existe: {d}")
            return 1
        hijos = sorted(d.glob("*.html"), key=lambda p: -p.stat().st_size)
        rutas += hijos[:args.limit]
    rutas = [p for p in rutas if p.exists()]
    if not rutas:
        print("sin ficheros (usa rutas o --dir)")
        return 1

    informes = []
    for p in rutas:
        carpeta = DESTINO / slug(p.stem)
        if args.solo_listar:
            carpeta = REPO / "__dryrun__"
        inf = extrae(p, carpeta, args.min_kb)
        informes.append(inf)
        kb = sum(e["kb"] for e in inf["extraidos"])
        print(f"{inf['kb_html']:>9} KB -> {len(inf['extraidos'])} assets "
              f"({kb:.0f} KB) dup={inf['duplicados']} "
              f"peq={inf['descartados_pequenos']} err={inf['errores']}  {p.name[:52]}")

    total = sum(len(i["extraidos"]) for i in informes)
    total_kb = sum(e["kb"] for i in informes for e in i["extraidos"])
    out = {"generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "ficheros_origen": len(informes), "assets_extraidos": total,
           "kb_extraidos": round(total_kb, 1), "informes": informes}
    INFORME.parent.mkdir(parents=True, exist_ok=True)
    INFORME.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nTOTAL: {total} assets · {total_kb:.0f} KB")
    print(f"OK -> {INFORME}")
    if not args.solo_listar:
        print(f"DESTINO -> {DESTINO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())