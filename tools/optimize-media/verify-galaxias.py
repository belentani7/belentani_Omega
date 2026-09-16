#!/usr/bin/env python3
"""Verifica la integridad de las 50 galaxias de BELENTANI // JUDAS ERA.

Comprueba: 50 ficheros, cero placeholders sin sustituir, JSON válido,
cada página con title/hreflang/navegación/mount, y que el hub enlace a las 50.

Uso: python tools/optimize-media/verify-galaxias.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
G = REPO / "galaxias"

ESPERADOS = 50


def main() -> int:
    fallos: list[str] = []
    if not G.exists():
        print("FALLO: no existe galaxias/ — ejecuta build-galaxy-pages.py")
        return 1

    paginas = sorted(G.glob("galaxia-*.html"))
    if len(paginas) != ESPERADOS:
        fallos.append(f"hay {len(paginas)} páginas, se esperaban {ESPERADOS}")

    hub = G / "index.html"
    if not hub.exists():
        fallos.append("falta galaxias/index.html (hub)")

    # 1) placeholders sin sustituir (solo {{IDENT}}, no las llaves del CSS)
    for p in paginas + ([hub] if hub.exists() else []):
        txt = p.read_text(encoding="utf-8")
        restos = set(re.findall(r"\{\{[A-Z_]+\}\}", txt))
        if restos:
            fallos.append(f"{p.name}: placeholders sin sustituir {sorted(restos)[:6]}")

    # 2) cada página: title, hreflang x4, ndots x5, nav, mount, i18n
    for p in paginas:
        t = p.read_text(encoding="utf-8")
        n = p.name
        if "<title>" not in t:
            fallos.append(f"{n}: sin <title>")
        hl = t.count("hreflang=")
        if hl != 5:
            fallos.append(f"{n}: hreflang={hl}, se esperaban 5 (pt/es/en/ca/x-default)")
        dots = t.count('class="nstar"')
        if dots != 5:
            fallos.append(f"{n}: ndots={dots}, se esperaban 5 (las 5 Firmas)")
        if "mountGalaxia(" not in t:
            fallos.append(f"{n}: sin arranque mountGalaxia()")
        if 'id="orbit"' not in t:
            fallos.append(f"{n}: sin hero-orbit (sparks de las 10 estaciones)")
        if "omega-galaxias" in t:
            fallos.append(f"{n}: referencia CSS/JS externo no usado (debe ser inline)")
        if "lang=" in t and "pt" not in t.split("var ORDER")[-1]:
            fallos.append(f"{n}: falta orden de idiomas PT>ES>EN>CA")

    # 3) navegación circular 01<->50
    g1 = (G / "galaxia-01.html").read_text(encoding="utf-8")
    g50 = (G / "galaxia-50.html").read_text(encoding="utf-8")
    if 'href="galaxia-50.html"' not in g1:
        fallos.append("galaxia-01 no enlaza a galaxia-50 (cadena rota)")
    if 'href="galaxia-01.html"' not in g50:
        fallos.append("galaxia-50 no enlaza a galaxia-01 (cadena rota)")

    # 4) JSON
    j = G / "galaxias.json"
    datos = None
    if not j.exists():
        fallos.append("falta galaxias/galaxias.json")
    else:
        try:
            datos = json.loads(j.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fallos.append(f"galaxias.json inválido: {e}")
        else:
            if len(datos.get("paginas", [])) != ESPERADOS:
                fallos.append(f"galaxias.json: {len(datos.get('paginas', []))} páginas")
            if len(datos.get("firmas", [])) != 5:
                fallos.append("galaxias.json: no hay 5 firmas")
            if len(datos.get("estaciones", [])) != 10:
                fallos.append("galaxias.json: no hay 10 estaciones")

    # 5) hub enlaza a las 50
    if hub.exists():
        h = hub.read_text(encoding="utf-8")
        faltan = [f"{i:02d}" for i in range(1, ESPERADOS + 1)
                  if f'galaxia-{i:02d}.html' not in h]
        if faltan:
            fallos.append(f"hub sin enlaces a: {faltan}")
        tiles = h.count('class="tile"')
        if tiles != ESPERADOS:
            fallos.append(f"hub con {tiles} tiles, se esperaban {ESPERADOS}")

    # 6) core compartido
    for f in ("core/omega-galaxias.css", "core/omega-galaxias.js"):
        if not (G / f).exists():
            fallos.append(f"falta galaxias/{f}")

    if fallos:
        print(f"FALLOS ({len(fallos)}):")
        for f in fallos:
            print(" -", f)
        return 1
    print(f"OK — {len(paginas)} galaxias + hub verificadas, sin fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())