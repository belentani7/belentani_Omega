from __future__ import annotations

import hashlib
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


SEARCH_ROOT = Path(r"C:\Users\USER")
OUTPUT_JSON = Path(__file__).resolve().parents[1] / "BELENTANI-HTML-INVENTORY.json"
OUTPUT_MD = Path(__file__).resolve().parents[1] / "BELENTANI-HTML-INVENTORY.md"
TERMS = ("belentani", "judas", "omega", "buildai", "buildaispace", "judas experience")
SKIP_PARTS = {
    ".git",
    "node_modules",
    "cache",
    "caches",
    "code cache",
    "gpucache",
    "service worker",
    "temporary internet files",
}
MAX_READ_BYTES = 60 * 1024 * 1024


def should_skip(path: Path) -> bool:
    return any(part.lower() in SKIP_PARTS for part in path.parts)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_searchable_text(path: Path, size: int) -> str:
    if size > MAX_READ_BYTES:
        return ""
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-16", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding).lower()
        except UnicodeDecodeError:
            continue
    return ""


def main() -> None:
    records: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []

    for current_root, directories, files in os.walk(SEARCH_ROOT, topdown=True):
        root_path = Path(current_root)
        directories[:] = [name for name in directories if not should_skip(root_path / name)]
        for name in files:
            path = root_path / name
            if path.suffix.lower() not in {".html", ".htm"}:
                continue
            try:
                stat = path.stat()
                lowered_name = name.lower()
                name_terms = sorted(term for term in TERMS if term in lowered_name)
                content = read_searchable_text(path, stat.st_size)
                content_terms = sorted(term for term in TERMS if term in content)
                related = bool(name_terms or content_terms)
                records.append(
                    {
                        "path": str(path),
                        "name": name,
                        "size_bytes": stat.st_size,
                        "modified_utc": datetime.fromtimestamp(
                            stat.st_mtime, tz=timezone.utc
                        ).isoformat(),
                        "name_terms": name_terms,
                        "content_terms": content_terms,
                        "related": related,
                        "sha256": file_hash(path),
                    }
                )
            except (OSError, PermissionError) as exc:
                errors.append({"path": str(path), "error": str(exc)})

    records.sort(key=lambda item: (not bool(item["related"]), str(item["path"]).lower()))
    related = [item for item in records if item["related"]]
    hashes: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in related:
        hashes[str(item["sha256"])].append(item)
    duplicate_groups = [group for group in hashes.values() if len(group) > 1]
    duplicate_groups.sort(key=lambda group: (-len(group), str(group[0]["path"]).lower()))

    payload = {
        "generated_utc": datetime.now(tz=timezone.utc).isoformat(),
        "search_root": str(SEARCH_ROOT),
        "terms": list(TERMS),
        "total_html": len(records),
        "related_html": len(related),
        "unique_related_content": len(hashes),
        "duplicate_groups": [
            {
                "sha256": str(group[0]["sha256"]),
                "size_bytes": int(group[0]["size_bytes"]),
                "paths": [str(item["path"]) for item in group],
            }
            for group in duplicate_groups
        ],
        "related_files": related,
        "scan_errors": errors,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    parent_counts = Counter(str(Path(str(item["path"])).parent) for item in related)
    lines = [
        "# Inventario de HTML de BELENTANI / JUDAS / OMEGA",
        "",
        f"- HTML totales encontrados en el perfil: **{len(records)}**",
        f"- HTML relacionados por nombre o contenido: **{len(related)}**",
        f"- Contenidos únicos por SHA-256: **{len(hashes)}**",
        f"- Grupos de duplicados exactos: **{len(duplicate_groups)}**",
        f"- Errores de lectura: **{len(errors)}**",
        "",
        "## Distribución por carpeta",
        "",
    ]
    for folder, count in parent_counts.most_common():
        lines.append(f"- `{folder}`: {count}")
    lines.extend(["", "## Archivos relacionados", ""])
    for index, item in enumerate(related, start=1):
        terms = sorted(set(item["name_terms"]) | set(item["content_terms"]))
        lines.append(
            f"{index}. `{item['path']}` — {item['size_bytes']} bytes — "
            f"términos: {', '.join(terms)} — SHA-256 `{str(item['sha256'])[:12]}`"
        )
    lines.extend(["", "## Duplicados exactos", ""])
    if duplicate_groups:
        for index, group in enumerate(duplicate_groups, start=1):
            lines.append(f"### Grupo {index}: {len(group)} copias")
            lines.append("")
            for item in group:
                lines.append(f"- `{item['path']}`")
            lines.append("")
    else:
        lines.append("No se encontraron duplicados exactos.")
    if errors:
        lines.extend(["", "## Errores de lectura", ""])
        for error in errors:
            lines.append(f"- `{error['path']}`: {error['error']}")
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "total_html": len(records),
        "related_html": len(related),
        "unique_related_content": len(hashes),
        "duplicate_groups": len(duplicate_groups),
        "scan_errors": len(errors),
        "report": str(OUTPUT_MD),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
