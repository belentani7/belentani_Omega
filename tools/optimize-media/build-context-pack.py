#!/usr/bin/env python3
"""Extract MAX context from local HTML/TXT into OMEGA lore pack (additive)."""
from pathlib import Path
import re
import html as ihtml

HOME = Path.home()
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "docs" / "context-pack"
CHAT = HOME / "Downloads" / "chat-Judas Experience.txt"
PORTAL = HOME / "Downloads" / "NOIACORE" / "belentani_portal_3k_1.html"
OMEGA30K = HOME / "Downloads" / "NOIACORE" / "belentani_omega_30k_1.html"
RUPTURA = HOME / "Downloads" / "NOIACORE" / "BELENTANI _ Ruptura y senal.html"
GUI = HOME / "Downloads" / "NOIACORE" / "Belentani_Web_GUI_1.html"

def clean(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[ \t\xa0]+", " ", ihtml.unescape(s))

def sents(t, keys):
    out = []
    for line in t.splitlines():
        s = line.strip(" -·•\t")
        if 24 <= len(s) <= 320 and any(k.lower() in s.lower() for k in keys):
            out.append(s)
    u, seen = [], set()
    for s in out:
        if s not in seen:
            seen.add(s)
            u.append(s)
    return u[:400]
KEYS = ["BELENTANI", "JUDAS", "PORTAL", "DIAMOND", "ORACLE", "ZION", "DUCK", "NOIACORE", "ENTER", "FALL", "KISS", "MEMORY", "FRAGMENT", "SYSTEM ONLINE", "ENTITY", "NEXT CHAPTER", "REVELATION"]

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    chat = CHAT.read_text(encoding="utf-8", errors="replace") if CHAT.exists() else ""
    portal = PORTAL.read_text(encoding="utf-8", errors="replace") if PORTAL.exists() else ""
    omega = OMEGA30K.read_text(encoding="utf-8", errors="replace") if OMEGA30K.exists() else ""
    base = HOME / "Downloads" / "NOIACORE"
    rupt, gui = "", ""
    for c in base.glob("BELENTANI*Ruptura*"):
        rupt = c.read_text(encoding="utf-8", errors="replace")
        break
    if GUI.exists():
        gui = GUI.read_text(encoding="utf-8", errors="replace")
    heads = re.findall(r"(?m)^(\d{2} — .{3,90})$", chat)[:40]
    (OUT / "10-master-prompt-resumen.md").write_text("# Master prompt — indice local\n\nFuente: chat-Judas Experience (" + str(len(chat.splitlines())) + " lineas)\n\n" + "".join("- " + h + "\n" for h in heads) + "\nReglas: NO landing/portfolio/cyberpunk/gamer. 90% BLACK / 10% BLOOD RED. HERO BELENTANI/JUDAS/THE EXPERIENCE + ENTER. Recorrido: PORTAL > CONSTELLATION > 5 DIAMANTES > KISS > CHOICE > REVELATION. Final: THE MISSING PIECE IS YOU.\n", encoding="utf-8")
    pt = clean(portal)
    phrases = sents(pt, KEYS)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", portal, re.I | re.S)
    h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", portal, re.I | re.S)
    f1 = OUT / "20-portal-textos.md"
    f1.write_text("# Portal 3K — textos\n\n## H1\n" + "".join("- " + re.sub(r"<[^>]+>", "", x).strip()[:160] + "\n" for x in h1[:10]) + "\n## H2\n" + "".join("- " + re.sub(r"<[^>]+>", "", x).strip()[:160] + "\n" for x in h2[:30]) + "\n## Frases\n" + "".join("- " + s + "\n" for s in phrases[:200]), encoding="utf-8")
    assets = sorted(set(re.findall(r"(?:src|href)=\"(assets/[^\"]{1,140})\"", portal + omega)))[:200]
    ext = sorted(set(re.findall(r"https?://[A-Za-z0-9_./:@?=&%#+-]{4,140}", omega)))[:40]
    (OUT / "30-assets-manifest.md").write_text("# Assets — checklist (copiar a mano a assets/imports/)\n\n" + "".join("- [ ] `" + a + "`\n" for a in assets) + "\n## Externas (referencia, NO hotlinkear)\n" + "".join("- `" + u + "`\n" for u in ext), encoding="utf-8")
    big = clean(chat + "\n" + rupt + "\n" + gui)
    lore = sents(big, KEYS)
    (OUT / "40-lore-frases.md").write_text("# Lore — frases canon\n\n" + "".join(str(i + 1) + ". " + s + "\n" for i, s in enumerate(lore[:300])), encoding="utf-8")
    (OUT / "50-gui-patterns.md").write_text("# GUI patterns\n\n- Sidebar glass overview/monorepo/agents/api_vault\n- Agents & CLI Hub OpenCode/Kilo/Mimo\n- Living Universe: bloom + cinematic shader (aberracion/grano/vineta)\n", encoding="utf-8")
    (OUT / "00-INDEX.md").write_text("# Context pack local\n\n- 10-master-prompt-resumen\n- 20-portal-textos\n- 30-assets-manifest\n- 40-lore-frases\n- 50-gui-patterns\n", encoding="utf-8")
    print("OK " + str(OUT))
    return 0

if __name__ == "__main__":
    raise SystemExit(build())

