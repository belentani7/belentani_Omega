#!/usr/bin/env python3
"""Optimiza los assets extraídos de assets/imports/ -> assets/galaxy/.

Qué hace, en este orden:
  1. Deduplica por sha1 de CONTENIDO (la misma imagen aparece en 12 HTML).
  2. Convierte a WebP (máx. 1920 px de lado, calidad 82) con Pillow.
  3. Escribe assets/galaxy/manifest.json con dimensiones, peso y ahorro
     para que las 50 galaxias puedan elegir imagen sin adivinar.
  4. Informe legible en docs/context-pack/80-imports-optimizados.md

No borra nada de assets/imports/ (los originales son archivo).
Sin Pillow avisa y sale sin tocar ficheros.

Uso:
  python tools/optimize-media/optimize-imports.py
  python tools/optimize-media/optimize-imports.py --max-px 1600 --quality 78
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ORIGEN = REPO / "assets" / "imports"
DESTINO = REPO / "assets" / "galaxy"
OUT = REPO / "docs" / "context-pack"

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".avif"}


def sha1(ruta: Path, bloque: int = 1 << 20) -> str:
    h = hashlib.sha1()
    with ruta.open("rb") as fh:
        while True:
            trozo = fh.read(bloque)
            if not trozo:
                break
            h.update(trozo)
    return h.hexdigest()


def recolecta() -> dict[str, list[Path]]:
    """sha1 -> lista de rutas con ese contenido (duplicados agrupados)."""
    grupos: dict[str, list[Path]] = {}
    if not ORIGEN.exists():
        return grupos
    for f in sorted(ORIGEN.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in IMG_EXT:
            continue
        try:
            grupos.setdefault(sha1(f), []).append(f)
        except OSError:
            continue
    return grupos


def elegir(rutas: list[Path]) -> Path:
    """Canónico: nombre más corto y fuera de _duplicados (más legible)."""
    def clave(p: Path):
        return ("_duplicados" in p.parts, len(p.name), len(str(p)))
    return sorted(rutas, key=clave)[0]


def nombre_galaxy(canonico: Path, ext: str = ".webp") -> str:
    """slug de carpeta + nombre original, sin repetir el sufijo de carpeta."""
    carpeta = canonico.parent.name
    base = canonico.stem
    limpio = f"{carpeta}__{base}" if base.startswith(("image", "font")) else f"{carpeta}-{base}"
    return (limpio[:80] + ext)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-px", type=int, default=1920, help="lado máximo en píxeles")
    ap.add_argument("--quality", type=int, default=82, help="calidad WebP")
    ap.add_argument("--min-kb", type=float, default=0, help="ignorar menores de X KB")
    ap.add_argument("--force", action="store_true", help="reconvertir existentes")
    args = ap.parse_args()

    try:
        from PIL import Image
    except ImportError:
        print("Pillow no disponible: pip install Pillow")
        return 1

    Image.MAX_IMAGE_PIXELS = None  # los exports traen PNG enormes legítimas

    grupos = recolecta()
    if not grupos:
        print(f"nada que optimizar en {ORIGEN}")
        return 1

    DESTINO.mkdir(parents=True, exist_ok=True)
    entradas, omitidos, kb_in, kb_out = [], 0, 0.0, 0.0
    usados: set[str] = set()

    for h, rutas in grupos.items():
        canonico = elegir(rutas)
        try:
            kb_origen = canonico.stat().st_size / 1024
        except OSError:
            continue
        if kb_origen < args.min_kb:
            omitidos += 1
            continue
        salida = DESTINO / nombre_galaxy(canonico)
        if salida.name in usados:
            salida = DESTINO / f"{salida.stem}-{h[:6]}.webp"
        usados.add(salida.name)

        ancho = alto = 0
        if salida.exists() and not args.force:
            try:
                with Image.open(salida) as im:
                    ancho, alto = im.size
            except OSError:
                ancho = alto = 0
        else:
            try:
                with Image.open(canonico) as im:
                    im.load()
                    if im.mode in ("P", "LA", "RGBA"):
                        im = im.convert("RGBA")
                    elif im.mode != "RGB":
                        im = im.convert("RGB")
                    ancho, alto = im.size
                    if max(ancho, alto) > args.max_px:
                        escala = args.max_px / float(max(ancho, alto))
                        im = im.resize((max(1, int(ancho * escala)),
                                        max(1, int(alto * escala))),
                                       Image.LANCZOS)
                        ancho, alto = im.size
                    im.save(salida, "WEBP", quality=args.quality, method=6)
            except (OSError, ValueError) as e:
                print(f"  ! fallo {canonico.name}: {e}")
                continue

        try:
            kb_destino = salida.stat().st_size / 1024
        except OSError:
            continue
        kb_in += kb_origen
        kb_out += kb_destino
        entradas.append({
            "webp": str(salida.relative_to(REPO)).replace("\\", "/"),
            "origen": str(canonico),
            "copias_duplicadas": len(rutas) - 1,
            "kb_origen": round(kb_origen, 1),
            "kb_webp": round(kb_destino, 1),
            "ancho": ancho, "alto": alto,
            "sha1": h,
        })
        marca = "=" if kb_destino < kb_origen else "!"
        print(f"  {marca} {kb_origen:9.1f} -> {kb_destino:8.1f} KB  "
              f"{ancho}x{alto}  {salida.name[:52]}")

    entradas.sort(key=lambda e: -e["ancho"] * e["alto"])
    ahorro = round(kb_in - kb_out, 1)
    pct = round(100 * (1 - kb_out / kb_in), 1) if kb_in else 0
    manifiesto = {
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "max_px": args.max_px, "quality": args.quality,
        "unicos": len(entradas),
        "duplicados_colapsados": sum(e["copias_duplicadas"] for e in entradas),
        "kb_origen": round(kb_in, 1), "kb_webp": round(kb_out, 1),
        "ahorro_kb": ahorro, "ahorro_pct": pct,
        "imagenes": entradas,
    }
    (DESTINO / "manifest.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")

    OUT.mkdir(parents=True, exist_ok=True)
    lineas = ["# Imports optimizados -> assets/galaxy", "",
              f"Únicos: {len(entradas)} · duplicados colapsados: "
              f"{manifiesto['duplicados_colapsados']} · omitidos (<{args.min_kb} KB): {omitidos}",
              f"Peso: {round(kb_in/1024,1)} MB -> {round(kb_out/1024,1)} MB "
              f"(ahorro {pct}%)", "",
              "| WxH | origen KB | webp KB | fichero |", "|---|---|---|---|"]
    for e in entradas:
        lineas.append(f"| {e['ancho']}x{e['alto']} | {e['kb_origen']} | "
                      f"{e['kb_webp']} | `{e['webp']}` |")
    (OUT / "80-imports-optimizados.md").write_text("\n".join(lineas), encoding="utf-8")

    print(f"\núnicos={len(entradas)} duplicados_cortados={manifiesto['duplicados_colapsados']}")
    print(f"peso {round(kb_in/1024,1)} MB -> {round(kb_out/1024,1)} MB (ahorro {pct}%)")
    print(f"OK -> {DESTINO / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())