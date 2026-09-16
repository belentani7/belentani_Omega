#!/usr/bin/env python3
"""Consolida assets/imports/: una copia canónica por contenido (SHA-1).

Los extractores pueden producir la misma imagen varias veces (mismo export
repetido, mismo asset incrustado en 20 HTML). Esta herramienta:

  1. agrupa por SHA-1 todo lo que hay en assets/imports/
  2. conserva UNA copia por hash (la de nombre más corto) y la renombra a
     <origen>-<sha8><ext>
  3. MUEVE el resto a assets/imports/_duplicados/  (no se borra nada)
  4. reescribe docs/context-pack/90-assets-canon.json con el inventario final

Uso:
  python tools/optimize-media/consolidate-imports.py --dry-run
  python tools/optimize-media/consolidate-imports.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IMPORTS = REPO / "assets" / "imports"
OUT = REPO / "docs" / "context-pack"
DUPS = IMPORTS / "_duplicados"
IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".svg", ".ico", ".bmp"}
MED = {".mp4", ".webm", ".mp3", ".wav", ".ogg"}


def sha1(p: Path) -> str:
    h = hashlib.sha1()
    with p.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not IMPORTS.exists():
        print(f"no existe {IMPORTS} (ejecuta primero decode-html-assets.py)")
        return 1

    archivos = [p for p in IMPORTS.rglob("*")
                if p.is_file() and p.suffix.lower() in (IMG | MED)
                and "_duplicados" not in p.parts]
    print(f"candidatos: {len(archivos)}")

    grupos: dict[str, list[Path]] = {}
    for i, p in enumerate(archivos, 1):
        grupos.setdefault(sha1(p), []).append(p)
        if i % 40 == 0:
            print(f"  hasheando {i}/{len(archivos)}...")

    canon: list[dict] = []
    movidos = 0
    ahorro = 0
    for h, lista in grupos.items():
        lista.sort(key=lambda p: (len(p.name), str(p)))
        principal = lista[0]
        ext = principal.suffix.lower()
        destino = IMPORTS / f"{principal.stem.split('-')[0][:40]}-{h[:8]}{ext}"
        dups = lista[1:]
        # stat() ANTES de renombrar: tras el rename la ruta antigua ya no existe.
        tamano = principal.stat().st_size
        if not args.dry_run and principal != destino and not destino.exists():
            principal.rename(destino)
        canon.append({
            "archivo": str((destino if not args.dry_run else principal)
                           .relative_to(REPO)).replace("\\", "/"),
            "sha1": h, "bytes": tamano,
            "ext": ext, "copias": len(lista),
            "duplicados": [str(d) for d in dups],
        })
        for d in dups:
            ahorro += d.stat().st_size
            movidos += 1
            if not args.dry_run:
                DUPS.mkdir(parents=True, exist_ok=True)
                objetivo = DUPS / d.name
                n = 1
                while objetivo.exists():
                    objetivo = DUPS / f"{d.stem}-{n}{d.suffix}"
                    n += 1
                shutil.move(str(d), str(objetivo))

    canon.sort(key=lambda e: -e["bytes"])
    total = sum(e["bytes"] for e in canon)
    salida = {
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "canonicos": len(canon),
        "duplicados_movidos": movidos,
        "mb_canonicos": round(total / 1048576, 2),
        "mb_ahorrados": round(ahorro / 1048576, 2),
        "items": canon,
    }
    if not args.dry_run:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "90-assets-canon.json").write_text(
            json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\ncanónicos: {len(canon)} · {salida['mb_canonicos']} MB")
    print(f"duplicados movidos: {movidos} · {salida['mb_ahorrados']} MB liberados")
    print(f"destino de duplicados: {DUPS}")
    if args.dry_run:
        print("(dry-run: no se escribió nada)")
    else:
        print(f"OK -> {OUT / '90-assets-canon.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())