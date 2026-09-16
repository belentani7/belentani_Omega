"""Lista el manifiesto de assets/galaxy para elegir imágenes (solo lectura)."""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAN = REPO / "assets" / "galaxy" / "manifest.json"


def main() -> int:
    orden = (sys.argv[1] if len(sys.argv) > 1 else "area")
    d = json.loads(MAN.read_text(encoding="utf-8"))
    items = d.get("imagenes") or d.get("assets") or []
    total = sum(e["kb_webp"] for e in items)
    print(f"TOTAL {d['unicos']} webp · {total / 1024:.1f} MB")
    print(f"{'KB':>8} {'ancho':>6} {'alto':>6}  archivo")
    if orden == "nombre":
        items = sorted(items, key=lambda e: e["webp"])
    for e in items:
        if orden == "pequenas" and e["kb_webp"] > 300:
            continue
        print(f"{e['kb_webp']:8.1f} {e['ancho']:>6} {e['alto']:>6}  {e['webp'][13:]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())