from __future__ import annotations

import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

ROOTS = (
    Path(r"C:\Users\USER\Desktop"),
    Path(r"C:\Users\USER\Documents"),
    Path(r"C:\Users\USER\Downloads"),
    Path(r"C:\Users\USER\AppData\Roaming\Claude\local-agent-mode-sessions"),
)
PROJECT = Path(r"C:\Users\USER\Desktop\belentani_Omega-live")
TERMS = ("belentani", "judas", "omega", "buildai", "buildaispace", "judas experience")
SKIP = {".git", "node_modules", "cache", "caches", "code cache", "gpucache", "service worker"}

records = []
errors = []
for base in ROOTS:
    if not base.exists():
        continue
    for current, dirs, files in os.walk(base, topdown=True):
        dirs[:] = [d for d in dirs if d.lower() not in SKIP]
        for filename in files:
            path = Path(current) / filename
            if path.suffix.lower() not in {".html", ".htm"}:
                continue
            try:
                stat = path.stat()
                name_hits = [term for term in TERMS if term in filename.lower()]
                content_hits = []
                if stat.st_size <= 60 * 1024 * 1024:
                    raw = path.read_bytes()
                    text = raw.decode("utf-8", errors="ignore").lower()
                    content_hits = [term for term in TERMS if term in text]
                if not name_hits and not content_hits:
                    continue
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                records.append({
                    "path": str(path),
                    "size_bytes": stat.st_size,
                    "name_terms": name_hits,
                    "content_terms": content_hits,
                    "sha256": digest,
                })
            except OSError as exc:
                errors.append({"path": str(path), "error": str(exc)})

records.sort(key=lambda item: item["path"].lower())
groups = defaultdict(list)
for item in records:
    groups[item["sha256"]].append(item["path"])
duplicates = {digest: paths for digest, paths in groups.items() if len(paths) > 1}
folders = Counter(str(Path(item["path"]).parent) for item in records)
payload = {
    "roots": [str(root) for root in ROOTS],
    "related_html": len(records),
    "unique_related_content": len(groups),
    "duplicate_groups": duplicates,
    "files": records,
    "errors": errors,
}
(PROJECT / "BELENTANI-HTML-INVENTORY.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
)
lines = [
    "# Inventario HTML BELENTANI / JUDAS / OMEGA",
    "",
    f"- Archivos relacionados: **{len(records)}**",
    f"- Contenidos únicos: **{len(groups)}**",
    f"- Grupos duplicados: **{len(duplicates)}**",
    f"- Errores de lectura: **{len(errors)}**",
    "",
    "## Distribución",
    "",
]
lines.extend(f"- `{folder}`: {count}" for folder, count in folders.most_common())
lines.extend(["", "## Archivos", ""])
for index, item in enumerate(records, 1):
    hits = sorted(set(item["name_terms"] + item["content_terms"]))
    lines.append(f"{index}. `{item['path']}` — {item['size_bytes']} bytes — {', '.join(hits)} — `{item['sha256'][:12]}`")
lines.extend(["", "## Duplicados exactos", ""])
for index, paths in enumerate(duplicates.values(), 1):
    lines.append(f"### Grupo {index}")
    lines.append("")
    lines.extend(f"- `{path}`" for path in paths)
    lines.append("")
(PROJECT / "BELENTANI-HTML-INVENTORY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({
    "related_html": len(records),
    "unique_related_content": len(groups),
    "duplicate_groups": len(duplicates),
    "errors": len(errors),
}, ensure_ascii=False))
