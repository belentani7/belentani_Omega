#!/usr/bin/env python3
"""DECODIFICA los data-URI base64 incrustados en tus HTML a assets reales.

Los exports grandes de BuildAI / Drive / OMEGA CORE meten las imágenes dentro
del propio HTML en base64 (data:image/png;base64,...). Este script las saca a
ficheros .png/.jpg/.webp/.svg reales, deduplicadas por SHA-1, dentro de:

    assets/imports/<origen>/

Y escribe un índice JSON+MD para poder cablearlas después al héroe, la
galería, el manifest y el service worker.

Solo LEE los HTML. Solo ESCRIBE en assets/imports/ y docs/context-pack/.
Nunca sobrescribe un asset ya extraído (dedup por hash).

Uso:
  python tools/optimize-media/decode-html-assets.py FILE1.html [FILE2.html ...]
  python tools/optimize-media/decode-html-assets.py --dir "G:/.../BELENTANI-WEB" --limit 8
  python tools/optimize-media/decode-html-assets.py --dir ... --min-bytes 8192
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
OUT = REPO / "docs" / "context-pack"

# data:image/png;base64,AAAA...
RE_DATA = re.compile(r"data:(?P<mime>[a-z0-9.+-]+/[a-z0-9.+-]+);base64,(?P<b64>[A-Za-z0-9+/=\s]{64,})", re.I)

MIME_EXT = {
    "image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
    "image/webp": ".webp", "image/gif": ".gif", "image/avif": ".avif",
    "image/svg+xml": ".svg", "image/bmp": ".bmp", "image/x-icon": ".ico",
    "image/vnd.microsoft.icon": ".ico",
    "video/mp4": ".mp4", "video/webm": ".webm", "audio/mpeg": ".mp3",
    "audio/wav": ".wav", "audio/ogg": ".ogg", "audio/webm": ".weba",
    "font/woff2": ".woff2", "font/woff": ".woff", "font/ttf": ".ttf",
    "application/font-woff": ".woff", "application/pdf": ".pdf",
}
IMG_MIMES = {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif",
             "image/avif", "image/svg+xml", "video/mp4", "video/webm"}
# Firmas para descartar basura decodificada (sprites 1x1, píxeles de tracking).
MIN_DEFAULT = 2048


def slug(nombre: str) -> str:
    limpio = re.sub(r"[^A-Za-z0-9._-]+", "-", nombre).strip("-")
    return (limpio[:48] or "origen").lower()


def extrae(path: Path, origen: str, min_bytes: int, vistos: dict[str, dict]) -> list[dict]:
    """Decodifica los data-URI de un HTML.

    `vistos` es GLOBAL a toda la ejecución y va indexado por SHA-1: así el mismo
    asset incrustado en 20 exports distintos se escribe UNA sola vez. Sin esto,
    4 copias del mismo HTML producían 4 copias de cada imagen (150 MB -> 600 MB).
    """
    try:
        texto = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"  ! {path.name}: {e}")
        return []

    salida: list[dict] = []
    for m in RE_DATA.finditer(texto):
        mime = m.group("mime").lower()
        if mime not in IMG_MIMES:
            continue
        ext = MIME_EXT.get(mime)
        if not ext:
            continue
        crudo = re.sub(r"\s+", "", m.group("b64"))
        try:
            datos = base64.b64decode(crudo, validate=False)
        except Exception:
            continue
        if len(datos) < min_bytes:
            continue
        h = hashlib.sha1(datos).hexdigest()
        ya = vistos.get(h)
        if ya:
            ya["fuentes"].append(str(path))
            continue
        destino = DESTINO / f"{origen}-{h[:8]}{ext}"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(datos)
        item = {
            "origen": origen, "mime": mime, "sha1": h, "bytes": len(datos),
            "archivo": str(destino.relative_to(REPO)).replace("\\", "/"),
            "fuente_html": str(path), "fuentes": [str(path)],
        }
        vistos[h] = item
        salida.append(item)
    return salida


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*")
    ap.add_argument("--dir", help="carpeta con HTML")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--min-kb", type=float, default=200, help="ignorar HTML menores")
    ap.add_argument("--min-bytes", type=int, default=MIN_DEFAULT,
                    help="tamaño mínimo del asset decodificado")
    args = ap.parse_args()

    rutas = [Path(p) for p in args.archivos]
    if args.dir:
        d = Path(args.dir)
        if not d.exists():
            print(f"no existe: {d}")
            return 1
        hijos = sorted(d.glob("*.html"), key=lambda p: -p.stat().st_size)
        rutas += [p for p in hijos if p.stat().st_size / 1024 >= args.min_kb][:args.limit]
    rutas = [p for p in rutas if p.exists()]
    if not rutas:
        print("sin ficheros (usa rutas o --dir)")
        return 1

    todo: list[dict] = []
    vistos: dict[str, dict] = {}
    for p in rutas:
        origen = slug(p.stem)[:40]
        print(f"-> {p.name[:64]}  ({round(p.stat().st_size/1024)} KB)")
        encontrados = extrae(p, origen, args.min_bytes, vistos)
        todo += encontrados
        print(f"   {len(encontrados)} nuevos (únicos acumulados: {len(vistos)})")

    OUT.mkdir(parents=True, exist_ok=True)
    total_bytes = sum(e["bytes"] for e in todo)
    salida = {
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "html_analizados": len(rutas),
        "assets": len(todo),
        "mb_extraidos": round(total_bytes / 1048576, 2),
        "items": todo,
    }
    (OUT / "80-assets-extraidos.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    lineas = ["# Assets extraídos de data-URI (tus HTML)", "",
              f"HTML analizados: {len(rutas)} · assets: {len(todo)} · "
              f"{salida['mb_extraidos']} MB", "",
              "| KB | archivo | origen |", "|---|---|---|"]
    for e in sorted(todo, key=lambda x: -x["bytes"])[:80]:
        lineas.append(f"| {round(e['bytes']/1024, 1)} | `{e['archivo']}` | `{e['origen']}` |")
    (OUT / "80-assets-extraidos.md").write_text("\n".join(lineas), encoding="utf-8")

    print(f"\n{len(todo)} assets · {salida['mb_extraidos']} MB -> assets/imports/")
    print(f"OK -> {OUT / '80-assets-extraidos.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())