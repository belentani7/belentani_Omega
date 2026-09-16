def extract_inline(html: str, dest_dir: Path, threshold_kb=24, force=False):
    """Decodifica data URIs de imagen/sonido/video a dest_dir/<slug>-<i>.<ext>.

    Solo escribe si el fichero no existe o el contenido SHA256 difiere.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", html.stem)[:40]
    out = []
    for i, m in enumerate(RE_DATA.findall(html), 1):
        mime, b64 = m.group(1).split(";base64,")[0], m.group(2)
        cr = re.sub(r"\s+", "", b64)
        try:
            data = base64.b64decode(cr + "=" * (-len(cr) % 4))
        except Exception:
            continue
        if len(data) < 1024 * threshold_kb:
            continue
        ext = m.group(1).split("/")[1].split(";")[0]
        name = slug + f"-{i:03d}" + (".bin" if ext in ("mp3", "wav", "ogg", "m4a", "epub") else f".{ext}")
        dest_name = dest_dir / name
        hash = hashlib.sha256(data).hexdigest()[:20]
        action = "skip"
        if force or not dest_name.exists():
            with open(dest_name, "wb") as fh:
                fh.write(data)
            action = "extract"
        elif dest_name.stat().st_size != len(data) or hash != hashlib.sha256(dest_name.read_bytes()).hexdigest()[:20]:
            action = "replace"
            with open(dest_name, "wb") as fh:
                fh.write(data)
        else:
            action = "ok"
        out.append({
            "name": dest_name.name, "action": action, "mime": mime,
            "size_bytes": len(data), "hash20": hash, "ext": ext,
        })
    return out


def extract_all(paths: list, out_dir: Path, threshold_kb=24, force=False):
    INLINE = ("", force, threshold_kb)  # dummy placeholder (not used)
    return []  # We'll hoist extraction out of extract_inline and only do inline zip
import json, re, hashlib, base64
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
DIFERENCES = True  # extraer inline inline assets only if different from existing