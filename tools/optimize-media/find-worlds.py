#!/usr/bin/env python3
"""Busca material de planetas/galaxias/universo en el índice de disco.

Lee docs/context-pack/60-drive-index.json (lo genera scan-drive.py) y filtra
por palabras clave del universo Belentani. Solo lee y reporta rutas.

Uso:
  python tools/optimize-media/find-worlds.py                # resumen
  python tools/optimize-media/find-worlds.py --ext .html    # solo HTML
  python tools/optimize-media/find-worlds.py --top 40       # más resultados
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INDEX = REPO / "docs" / "context-pack" / "60-drive-index.json"

# Palabras clave del universo: mundo/cosmos + motor gráfico + lore.
KEYS = [
    "planet", "galax", "star", "cosmos", "univers", "nebula", "orbit",
    "solar", "world", "space", "astro", "lunar", "saturn", "jupiter",
    "immersive", "cinematic", "three", "webgl", "shader", "render", "bloom",
    "belentani", "judas", "omega", "noia", "zion", "prisma", "hermes",
    "portal", "nexus", "duck", "vault", "matrix", "neon",
]
PAT = re.compile("|".join(KEYS), re.I)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ext", default=None, help="filtrar por extensión, ej .html")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--all", action="store_true", help="listar todo lo encontrado")
    args = ap.parse_args()

    if not INDEX.exists():
        print("FALTA el índice: python tools/optimize-media/scan-drive.py")
        return 1
    data = json.loads(INDEX.read_text(encoding="utf-8"))

    total = 0
    resumen: dict[str, int] = {}
    for label, block in data.get("roots", {}).items():
        hits = []
        for e in block.get("files", []):
            if args.ext and e["ext"] != args.ext:
                continue
            if PAT.search(e["path"]):
                hits.append(e)
        hits.sort(key=lambda e: -e["kb"])
        total += len(hits)
        for h in hits:
            resumen[h["ext"]] = resumen.get(h["ext"], 0) + 1
        print(f"\n=== {label}: {len(hits)} coincidencias ({block.get('total', 0)} indexados) ===")
        show = hits if args.all else hits[:args.top]
        for h in show:
            print(f"  {h['kb']:>9} KB  {h['ext']:<6} {h['path']}")
        if not args.all and len(hits) > args.top:
            print(f"  ... +{len(hits) - args.top} más (usa --all)")

    print(f"\nTOTAL coincidencias: {total}")
    print("Por extensión: " + ", ".join(
        f"{k}×{v}" for k, v in sorted(resumen.items(), key=lambda kv: -kv[1])))
    return 0


if __name__ == "__main__":
    sys.exit(main())