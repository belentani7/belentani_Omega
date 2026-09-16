#!/usr/bin/env python3
"""Extrae el inventario de ASSETS referenciados dentro de ficheros HTML locales.

Para cada HTML: cuenta y lista imágenes, srcset, poster, vídeo/audio, url() de
CSS, CSS/JS externos y data URIs (base64 INLINE: aquí viven las imágenes de los
exports grandes de BuildAI/Drive).

Solo LEE los HTML y escribe un informe JSON+MD. No descarga, no modifica los
ficheros originales, no escribe en las carpetas escaneadas.

Uso:
  python tools/optimize-media/mine-html-assets.py FILE1.html FILE2.html
  python tools/optimize-media/mine-html-assets.py --dir "G:/.../01-HTML-LOCAL" --limit 30
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "docs" / "context-pack"

RE_IMG = re.compile(r"<img\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
RE_SRCSET = re.compile(r"\bsrcset\s*=\s*[\"']([^\"']+)[\"']", re.I)
RE_SRC = re.compile(r"<(?:source|video|audio|track)\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
RE_POSTER = re.compile(r"\bposter\s*=\s*[\"']([^\"']+)[\"']", re.I)
RE_LINK = re.compile(r"<link\b[^>]*?\bhref\s*=\s*[\"']([^\"']+)[\"'][^>]*>", re.I)
RE_CSSURL = re.compile(r"url\(\s*[\"']?([^\"')]+)[\"']?\s*\)", re.I)
RE_SCRIPT = re.compile(r"<script\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
RE_DATAURI = re.compile(r"data:([a-z0-9.+-]+/[a-z0-9.+-]+);base64,", re.I)

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".svg", ".bmp", ".ico")
MED_EXT = (".mp4", ".webm", ".ogv", ".mov", ".mp3", ".wav", ".ogg", ".m4a", ".flac")
FONT_EXT = (".woff2", ".woff", ".ttf", ".otf", ".eot")


def clasifica(url: str) -> str:
    limpio = url.split("?")[0].split("#")[0].lower()
    if limpio.endswith(IMG_EXT):
        return "imagen"
    if limpio.endswith(MED_EXT):
        return "media"
    if limpio.endswith(FONT_EXT):
        return "fuente"
    if limpio.endswith(".css"):
        return "css"
    if limpio.endswith(".js"):
        return "js"
    return "otro"


def es_externo(url: str) -> bool:
    return url.startswith(("http://", "https://", "//"))


def analiza(path: Path) -> dict:
    info: dict = {"archivo": str(path), "kb": round(path.stat().st_size / 1024, 1),
                  "imagenes": [], "media": [], "fuentes": [], "css": [], "js": [], "otro": [],
                  "data_uris": {}, "referencias_locales": [], "externos": []}
    try:
        texto = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        info["error"] = str(e)
        return info

    urls: list[str] = []
    urls += RE_IMG.findall(texto)
    urls += RE_SRC.findall(texto)
    urls += RE_POSTER.findall(texto)
    urls += RE_LINK.findall(texto)
    urls += RE_CSSURL.findall(texto)
    urls += RE_SCRIPT.findall(texto)
    for ss in RE_SRCSET.findall(texto):
        for parte in ss.split(","):
            u = parte.strip().split(" ")[0]
            if u:
                urls.append(u)

    vistos = set()
    for u in urls:
        if not u or u in vistos or u.startswith(("#", "data:", "javascript:", "mailto:")):
            continue
        vistos.add(u)
        cat = clasifica(u)
        if es_externo(u):
            info["externos"].append({"tipo": cat, "url": u})
        else:
            info["referencias_locales"].append({"tipo": cat, "ruta": u})
        if cat == "imagen":
            info["imagenes"].append(u)
        elif cat == "media":
            info["media"].append(u)
        elif cat == "fuente":
            info["fuentes"].append(u)
        else:
            info.setdefault(cat, []).append(u)

    for tipo in RE_DATAURI.findall(texto):
        info["data_uris"][tipo] = info["data_uris"].get(tipo, 0) + 1

    info["total_refs"] = len(info["referencias_locales"]) + len(info["externos"])
    info["total_data_uris"] = sum(info["data_uris"].values())
    return info
import json, re, hashlib, base64
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
DIFERENCES = True  # extraer inline inline assets only if different from existing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*", help="rutas de HTML")
    ap.add_argument("--dir", help="carpeta con HTML")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--min-kb", type=float, default=0, help="ignorar HTML menores")
    args = ap.parse_args()

    rutas = [Path(p) for p in args.archivos]
    if args.dir:
        d = Path(args.dir)
        if not d.exists():
            print(f"no existe: {d}")
            return 1
        hijos = sorted(d.glob("*.html"), key=lambda p: -p.stat().st_size)
        rutas += hijos[:args.limit]
    rutas = [p for p in rutas if p.exists() and p.stat().st_size / 1024 >= args.min_kb]
    if not rutas:
        print("sin ficheros que analizar (usa rutas o --dir)")
        return 1

    informes = []
    for p in rutas:
        inf = analiza(p)
        informes.append(inf)
        print(f"{inf['kb']:>9} KB  refs={inf.get('total_refs', 0):<5} "
              f"inline={inf.get('total_data_uris', 0):<5} {p.name[:64]}")

    tot_combined = {
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "html_origen": len(informes),
        "totales": {
            "imagenes_refs": tot_img,
            "media_refs": tot_media,
            "data_uris_inline": sum(i.get("total_data_uris", 0) for i in informes),
        },
        "hosts_externos": dict(sorted(ext.items(), key=lambda kv: -kv[1])),
        "informes": informes,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "70-assets-html.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    lineas = ["# Assets extraídos de HTML locales", "",
              f"Analizados: {len(informes)} · imágenes ref: {tot_img} · "
              f"media ref: {tot_media} · data URIs inline: {tot_inline}", "",
              "## Hosts externos", "", "| refs | host |", "|---|---|"]
    for h, c in list(salida["hosts_externos"].items())[:25]:
        lineas.append(f"| {c} | `{h}` |")
    lineas += ["", "## Ficheros", "", "| KB | refs | inline | fichero |", "|---|---|---|---|"]
    for i in informes:
        lineas.append(f"| {i['kb']} | {i.get('total_refs', 0)} | "
                      f"{i.get('total_data_uris', 0)} | `{i['archivo']}` |")
    (OUT / "70-assets-html.md").write_text("\n".join(lineas), encoding="utf-8")

    print(f"\nimágenes={tot_img} media={tot_media} inline={tot_inline}")
    print(f"OK -> {OUT / '70-assets-html.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())