#!/usr/bin/env python3
"""Compute SRI (sha384) hashes for the CDN assets used by belentani.es.

Usage:  python tools/optimize-media/sri.py
Outputs a JSON map {url: "sha384-..."} to stdout and tools/optimize-media/sri.json.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

URLS = [
    "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollToPlugin.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/CopyShader.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/ShaderPass.js",
    "https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js",
    "https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js",
]


def sri(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "belentani-sri/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (pinned https)
        data = resp.read()
    digest = hashlib.sha384(data).digest()
    return "sha384-" + base64.b64encode(digest).decode("ascii")


def main() -> int:
    out: dict[str, str] = {}
    for url in URLS:
        try:
            out[url] = sri(url)
            print(f"{out[url]}  {url}")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR  {url}  {exc}", file=sys.stderr)
    dest = Path(__file__).with_name("sri.json")
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {dest}")
    return 0 if len(out) == len(URLS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
