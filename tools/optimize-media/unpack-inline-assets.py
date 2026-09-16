#!/usr/bin/env python3
"""Desempaqueta los assets embebidos (data URI base64) de los HTML exportados.

Los exports de BuildAI / BELENTANI-WEB son HTML de 26–59 MB con las imágenes
incrustadas en base64. Este script las extrae a assets/imports/ con nombre
derivado del sha1 (deduplicado) y deja un manifiesto JSON.

Solo LEE los HTML indicados. Escribe ÚNICAMENTE dentro de assets/imports/.
Nunca modifica ni borra los ficheros de origen.

Uso:
  python tools/optimize-media/unpack-inline-assets.py FILE.html ...
  python tools/optimize-media/unpack-inline-assets.py --dir RUTA --limit 8
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
DEST = REPO / "assets" / "imports"
OUT = REPO / "docs" / "context-pack"

RE_DATA = re.compile(
    r"data:(?P<mime>[a-z0-9.+-]+/[a-z0-9.+-]+);base64,(?P<payload>[A-Za-z0-9+/=\s]{64,})",
    re.I)

EXT_MIME = {
    "image/webp": ".webp", "image/png": ".png", "image/jpeg": ".jpg",
    "image/jpg": ".jpg", "image/gif": ".gif", "image/svg+xml": ".svg",
    "image/avif": ".avif", "image/bmp": ".bmp", "image/x-icon": ".ico",
    "video/mp4": ".mp4", "video/webm": ".webm", "audio/mpeg": ".mp3",
    "audio/wav": ".wav", "font/woff2": ".woff2", "font/woff": ".woff",
    "application/font-woff2": ".woff2",
}


def nombres(texto: str, pos: int) -> dict:
    """Pistas de nombre/alt cerca de la posición del data URI."""
    ventana = texto[max(0, pos - 400):pos + 200]
    pistas = {}
    alt = re.findall(r'\balt\s*=\s*["\']([^"\']{2,60})["\']', ventana, re.I)
    if alt:
        pistas["alt"] = alt[-1]
    cls = re.findall(r'\bclass\s*=\s*["\']([^"\']{2,60})["\']', ventana, re.I)
    if cls:
        pistas["class"] = cls[-1]
    return pistas


def extrae(path: Path, dest: Path) -> dict:
    try:
        texto = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"archivo": str(path), "error": str(e), "extraidos": []}

    hallados = {}
    total_bytes = 0
    for m in RE_DATA.finditer(texto):
        mime = m.group("mime").lower()
        payload = re.sub(r"\s+", "", m.group("payload"))
        if len(payload) < 256:
            continue
        try:
            crudo = base64.b64decode(payload, validate=False)
        except Exception:
            continue
        if len(crudo) < 1024:
            continue
        sha = hashlib.sha1(crudo).hexdigest()[:12]
        ext = EXT_MIME.get(mime, ".bin")
        if sha not in hallados:
            hallados[sha] = {"sha": sha, "mime": mime, "ext": ext, "crudo": crudo,
                             "bytes": len(crudo), "pistas": nombres(texto, m.start())}
            total_bytes += len(crudo)

    escritos = []
    dest.mkdir(parents=True, exist_ok=True)
    for sha, meta in hallados.items():
        base = f"{path.stem[:40].replace(' ', '-')}-{sha}"
        base = re.sub(r"[^A-Za-z0-9._-]", "", base)
        destino = dest / (base + meta["ext"])
        try:
            if not destino.exists():
                destino.write_bytes(meta["crudo"])
            escritos.append({"archivo": str(destino), "kb": round(meta["bytes"] / 1024, 1),
                             "mime": meta["mime"], "pistas": meta["pistas"]})
        except OSError as e:
            escritos.append({"error": str(e), "sha": sha})

    return {"archivo": str(path), "kb_origen": round(path.stat().st_size / 1024, 1),
            "inline_encontrados": len(hallados), "bytes_inline": total_bytes,
            "extraidos": escritos}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="*")
    ap.add_argument("--dir", help="carpeta con HTML")
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument("--min-kb", type=float, default=200)
    args = ap.parse_args()

    rutas = [Path(p) for p in args.archivos]
    if args.dir:
        d = Path(args.dir)
        if not d.exists():
            print(f"no existe: {d}")
            return 1
        rutas += sorted(d.glob("*.html"), key=lambda p: -p.stat().st_size)[:args.limit]
    rutas = [p for p in rutas if p.exists() and p.stat().st_size / 1024 >= args.min_kb]
    if not rutas:
        print("sin ficheros (usa rutas o --dir)")
        return 1

    informes = []
    for p in rutas:
        inf = extrae(p, DEST)
        informes.append(inf)
        print(f"{inf.get('kb_origen', 0):>9} KB origen · "
              f"inline={inf.get('inline_encontrados', 0):<4} · "
              f"extraídos={len(inf.get('extraidos', [])):<4} {p.name[:56]}")

    salida = {"generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "destino": str(DEST), "informes": informes}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "80-inline-extraidos.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(len(i.get("extraidos", [])) for i in informes)
    print(f"\nextraídos={total} -> {DEST}")
    print(f"OK -> {OUT / '80-inline-extraidos.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())