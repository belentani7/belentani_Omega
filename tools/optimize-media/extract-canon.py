#!/usr/bin/env python3
"""Reutiliza los bloques canon (CSS/JS) ya escritos a mano en sesiones previas
y los inserta en el generador limpio build-galaxias.py entre marcadores
idempotentes. No inventa nada: copia texto literal ya validado.

Uso: python tools/optimize-media/extract-canon.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FUENTE = HERE / "_archive" / "build-galaxy-pages.5mains.bak.py"
DESTINO = HERE / "build-galaxias.py"

BEGIN = "# ===BEGIN EXTRACTED CANON==="
END = "# ===END EXTRACTED CANON==="

# nombre -> tipo. Se toma la PRIMERA aparición (la más reciente a mano).
BLOQUES = [
    ("CORE_CSS_A", "triple"),
    ("CORE_CSS_B", "triple"),
    ("CORE_JS", "triple"),
    ("TRAD", "dict"),
    ("UI", "dict"),
]


def extrae(texto: str, nombre: str, tipo: str) -> str | None:
    if tipo == "triple":
        m = re.search(rf'^{nombre}\s*=\s*r?"""(.*?)"""', texto, re.S | re.M)
    else:
        m = re.search(rf'^{nombre}\s*=\s*\{{.*?^\}}', texto, re.S | re.M)
    if not m:
        print(f"  ! no encontrado: {nombre}")
        return None
    if tipo == "dict":
        return m.group(0)
    return f'{nombre} = r"""' + m.group(1) + '"""'


def main() -> int:
    if not FUENTE.exists():
        print(f"falta la fuente: {FUENTE}")
        return 1
    fuente = FUENTE.read_text(encoding="utf-8", errors="replace")
    destino = DESTINO.read_text(encoding="utf-8", errors="replace")

    if BEGIN in destino:
        destino = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?",
                         "", destino, flags=re.S)

    piezas = []
    for nombre, tipo in BLOQUES:
        cuerpo = extrae(fuente, nombre, tipo)
        if cuerpo:
            piezas.append(cuerpo)
            print(f"  + {nombre} ({len(cuerpo)} car.)")
    if not piezas:
        print("nada que insertar")
        return 1

    bloque = BEGIN + "\n" + "\n\n".join(piezas) + "\n" + END + "\n"
    DESTINO.write_text(destino.rstrip("\n") + "\n\n" + bloque, encoding="utf-8")
    print(f"OK -> {DESTINO} (+{len(bloque)} car.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())