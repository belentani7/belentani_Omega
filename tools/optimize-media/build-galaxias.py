#!/usr/bin/env python3
"""Generador ÚNICO de las 50 galaxias unificadas de BELENTANI // JUDAS ERA.

Fuente de verdad del universo (todo elemento tiene función, nada decorativo):

  5 Firmas (LORE-UNIFICADO §6) x 10 Estaciones = 50 páginas.
  ┌ topnav ndots ....... las 5 Firmas; cambiar de firma = cambiar de mundo
  ├ Ojo de Judas ....... el planeta; late a la frecuencia de la estación
  ├ anillo / ring-b .... la Llave Dorada robada (victoria amarga)
  ├ hero-orbit sparks .. las 10 estaciones; la activa brilla en oro
  ├ mirror (espejo) .... línea canon de (firma x estación), cambia de idioma
  ├ hbar waveC ......... el Canto (LA VOZ ES EL OUTPUT) + navegación
  ├ sense slider ....... NEON / MATRIX / VENOM / VOID / ASCENDED
  └ .relic ............. reliquia: asset real extraído de tus exports de Drive

Idiomas en orden fijo del ecosistema: PT > ES > EN > CA.

Escribe SOLO bajo galaxias/. No toca index.html, css/, js/, assets/ ni el
sw.js del sitio. Idempotente: se puede relanzar cuantas veces haga falta.

Uso:
  python tools/optimize-media/build-galaxias.py
  python tools/optimize-media/build-galaxias.py --no-relic   # sin assets
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "galaxias"
CORE = OUT / "core"
IMPORTS = REPO / "assets" / "imports"

# ── Canon: las 5 firmas (LORE-UNIFICADO §6) ──────────────────────────────
FIRMAS = [
    ("pedro", "PEDRO.SIG", "LA ROCA", "#FFD700", "permanencia",
     "Porque estás aquí. Porque me acompañas."),
    ("marcos", "MARCOS.SIG", "EL CRONISTA", "#00FFFF", "memoria",
     "El Cronista registró lo que el Ángel cantaba."),
    ("santos", "SANTOS.SIG", "LA ANTENA", "#B026FF", "canal",
     "Cuatro voces. Un solo hombre. Un solo canal."),
    ("belentani", "BELENTANI.SIG", "NÚCLEO", "#FF003C", "integración",
     "LA TRAICIÓN ES EL INPUT. LA VOZ ES EL OUTPUT."),
    ("human", "HUMAN.SIG", "INTERFAZ", "#F5F5F5", "puente tangible",
     "La pieza que falta es el testigo."),
]

# ── Canon: las 10 estaciones (entre → constelación) ──────────────────────
# (slug, nombre, beat_s, frase_es)
ESTACIONES = [
    ("entre", "EL ENTRE", 3.2, "La historia no se repite. Se confronta."),
    ("deuda", "LA DEUDA", 2.8, "La deuda se volvió impagable: devoción sin devolución."),
    ("robo", "EL ROBO", 2.4, "Judas tomó la Llave Dorada de noche, con vergüenza más que maldad."),
    ("canto", "EL CANTO", 2.0, "Pedro se sentó y se puso a cantarle."),
    ("victoria", "LA VICTORIA AMARGA", 1.8,
     "Quédatela. La llave es metal. Lo que yo tengo nadie me lo arrebata: mi voz."),
    ("mentira", "LA MENTIRA COMPARTIDA", 1.6,
     "La llave nunca fue lo valioso. Era una mentira compartida."),
    ("umbral", "EL UMBRAL", 1.4,
     "Deja que te roben lo que no importa para revelar lo que sí."),
    ("senal", "LA SEÑAL", 1.2, "Fragmentos visuales + sonido + texto."),
    ("portal", "EL PORTAL", 1.0,
     "El portal no es una página. THE PORTAL TO BECOMING SOMEONE ELSE."),
    ("constelacion", "LA CONSTELACIÓN", 0.9, "THE NEXT CHAPTER IS YOURS."),
]

SENTIDOS = ["neon", "matrix", "venom", "void", "ascended"]
IDIOMAS = ["pt", "es", "en", "ca"]

FUENTES = ("https://fonts.googleapis.com/css2?"
           "family=Chakra+Petch:wght@300;400;600;700&"
           "family=JetBrains+Mono:wght@400;700&"
           "family=Orbitron:wght@600;900&display=swap")


def pagina_id(f: int, e: int) -> int:
    """f 0..4 (firma), e 0..9 (estación) -> 1..50."""
    return (f * 10 + e) + 1


def vecinos(n: int) -> tuple[str, str]:
    """Anterior/siguiente circular: las 50 galaxias son un anillo."""
    return (f"galaxia-{50 if n == 1 else n - 1:02d}.html",
            f"galaxia-{1 if n == 50 else n + 1:02d}.html")

# ===BEGIN EXTRACTED CANON===
CORE_CSS_A = r"""/* ══════════════════════════════════════════════════════════════════════
   BELENTANI // GALAXIAS — núcleo compartido de las 50 páginas.
   Canon: negro obsidiana #050505, rojo sangre #ff003c, oro #ffd700.
   Cada elemento tiene función: ver docs/GALAXIAS-UNIVERSO.md
   ══════════════════════════════════════════════════════════════════════ */
:root{
  --void:#050505; --blood:#ff003c; --gold:#ffd700; --cyan:#00ffff;
  --purple:#b026ff; --white:#f5f5f5; --green:#00ff41;
  --txt:#fff; --txt-dim:rgba(255,255,255,.72); --txt-ghost:rgba(255,255,255,.5);
  --sig:#ff003c;            /* firma de la página */
  --beat:2.4s;              /* latido del Ojo de Judas */
  --glass:rgba(12,2,6,.62);
  --fu:'Chakra Petch',system-ui,-apple-system,sans-serif;
  --fm:'JetBrains Mono',ui-monospace,SFMono-Regular,monospace;
  --fd:'Orbitron','Chakra Petch',sans-serif;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%}
body{background:var(--void);color:var(--txt);font-family:var(--fu);overflow:hidden;
  -webkit-font-smoothing:antialiased;overscroll-behavior:none}
body.sense-matrix{--blood:#00ff41}
body.sense-venom{--blood:#b026ff}
body.sense-void{--txt-dim:rgba(255,255,255,.55);--txt-ghost:rgba(255,255,255,.35)}
body.sense-ascended{--blood:#ffd700}
#stars{position:fixed;inset:0;z-index:0;display:block}
.skip{position:absolute;left:-9999px;top:0;background:var(--blood);color:#000;padding:10px 16px;
  font:700 12px/1 var(--fm);z-index:99}
.skip:focus{left:12px;top:12px}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px}

/* ── TOPNAV ndots: las 5 Firmas (§6). Cambiar firma = cambiar de mundo. ── */
.topnav{position:fixed;top:0;left:0;right:0;z-index:40;display:flex;align-items:center;gap:14px;
  padding:10px 18px;background:linear-gradient(180deg,rgba(5,5,5,.94),rgba(5,5,5,.5));
  backdrop-filter:blur(22px) saturate(160%);-webkit-backdrop-filter:blur(22px) saturate(160%);
  border-bottom:1px solid rgba(255,255,255,.08)}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit;cursor:pointer}
.brand-eye{width:14px;height:14px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#fff,var(--sig) 60%,#0a0003);
  box-shadow:0 0 12px var(--sig);animation:pulso 2.2s ease-in-out infinite}
@keyframes pulso{0%,100%{transform:scale(1);opacity:.9}50%{transform:scale(1.18);opacity:1}}
.brand b{font:900 13px/1 var(--fd);letter-spacing:3px}
.brand small{font:400 9px/1 var(--fm);letter-spacing:2px;color:var(--txt-ghost);display:block;margin-top:4px}
.ndots{display:flex;align-items:center;gap:9px;margin-left:auto;list-style:none}
.nstar{width:12px;height:12px;border-radius:50%;border:1px solid var(--sig);background:transparent;
  cursor:pointer;padding:0;transition:transform .25s,box-shadow .25s,background .25s}
.nstar:hover{transform:scale(1.35);box-shadow:0 0 12px var(--sig)}
.nstar[aria-current="true"]{background:var(--sig);box-shadow:0 0 16px var(--sig)}
.sig-badge{font:700 9px/1 var(--fm);letter-spacing:2px;color:var(--sig);border:1px solid var(--sig);
  border-radius:999px;padding:5px 9px;white-space:nowrap}

/* ── Ojo de Judas: late a la frecuencia de la estación. ── */
.stage{position:fixed;inset:0;z-index:1;display:grid;place-items:center;padding:96px 18px 140px}
.eye-wrap{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:min(62vmin,430px);aspect-ratio:1;display:grid;place-items:center}
.eye{position:absolute;inset:0;border-radius:50%;overflow:hidden;
  background:var(--foto,none) center/cover no-repeat,
    radial-gradient(circle at 34% 28%,rgba(255,255,255,.42),transparent 42%),
    radial-gradient(circle at 66% 74%,rgba(0,0,0,.88),transparent 62%),
    radial-gradient(circle at 50% 50%,var(--sig),#0a0003 74%);
  box-shadow:0 0 70px var(--sig),inset -20px -24px 70px rgba(0,0,0,.9);
  animation:latido var(--beat) ease-in-out infinite}
/* Luz + tinte rojo sobre la textura real del planeta (--foto): el reflejo es el canon. */
.eye::after{content:'';position:absolute;inset:0;border-radius:50%;pointer-events:none;
  background:radial-gradient(circle at 30% 24%,rgba(255,255,255,.5),transparent 36%),
    radial-gradient(circle at 52% 52%,transparent 44%,rgba(0,0,0,.82) 96%),
    radial-gradient(circle at 50% 50%,rgba(255,0,60,.3),transparent 74%)}
@keyframes latido{0%,100%{transform:scale(1)}50%{transform:scale(1.075)}}
.skin{position:absolute;inset:0;border-radius:50%;opacity:.42;mix-blend-mode:overlay;
  background:repeating-linear-gradient(115deg,rgba(255,255,255,.14) 0 2px,transparent 2px 9px);
  animation:deriva 90s linear infinite}
@keyframes deriva{to{background-position:600px 300px}}
.ring{position:absolute;width:158%;height:158%;border-radius:50%;
  border:2px solid rgba(255,215,0,.75);box-shadow:0 0 26px rgba(255,215,0,.45);
  animation:anillo 46s linear infinite}
.ring-b{width:186%;height:186%;border-style:dashed;border-color:rgba(255,0,60,.55);
  box-shadow:0 0 34px rgba(255,0,60,.3);animation-duration:72s;animation-direction:reverse}
@keyframes anillo{0%{transform:rotateX(74deg) rotateZ(0)}100%{transform:rotateX(74deg) rotateZ(360deg)}}
/* sparks = las 10 estaciones; la activa brilla (el oro de la Llave) */
.orbit{position:absolute;inset:-22%;animation:orbita 54s linear infinite;pointer-events:none}
@keyframes orbita{to{transform:rotate(360deg)}}
.spark{position:absolute;left:50%;top:50%;width:7px;height:7px;margin:-3.5px;border-radius:50%;
  background:var(--txt-ghost);transform:rotate(var(--a)) translate(var(--r))}
.spark.on{background:var(--gold);box-shadow:0 0 14px var(--gold),0 0 34px rgba(255,215,0,.6);
  animation:pulso 1.6s ease-in-out infinite}
"""

CORE_CSS_B = r"""
/* Ojo y espejo comparten la misma celda: el cristal se apoya en el planeta. */
.stage>*{grid-area:1/1}

/* ── ESPEJO: línea canon de (firma x estación) ── */
.mirror{position:relative;z-index:5;width:min(760px,92vw);padding:22px 24px;border-radius:18px;
  background:var(--glass);backdrop-filter:blur(26px) saturate(170%);
  -webkit-backdrop-filter:blur(26px) saturate(170%);
  border:1px solid rgba(255,255,255,.14);
  box-shadow:0 1px 0 rgba(255,255,255,.22) inset,0 30px 90px rgba(0,0,0,.78),0 0 60px rgba(255,0,60,.16)}
.mirror::after{content:'';position:absolute;inset:0;border-radius:inherit;padding:1px;
  background:linear-gradient(160deg,rgba(255,255,255,.55),rgba(255,255,255,.05) 34%,transparent 58%,var(--sig));
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.kicker{font:400 10px/1 var(--fm);letter-spacing:5px;color:var(--sig);margin-bottom:12px}
.title{font:900 clamp(30px,7.4vw,74px)/1 var(--fd);letter-spacing:.05em;
  text-shadow:0 0 26px rgba(255,0,60,.75),0 0 90px rgba(255,0,60,.35)}
.title em{font-style:normal;color:var(--sig)}
.espejo{font:300 clamp(14px,2.2vw,18px)/1.75 var(--fu);color:var(--txt-dim);margin:14px 0 6px}
.firma{font:400 11px/1.7 var(--fm);letter-spacing:1px;color:var(--txt-ghost)}
.firma b{color:var(--sig)}
.vec{margin:14px 0 0;padding-left:18px;font:300 13px/1.9 var(--fu);color:var(--txt-ghost)}
.vec li::marker{color:var(--gold)}
.progress{margin-top:16px;height:3px;border-radius:2px;background:rgba(255,255,255,.1);overflow:hidden}
.progress i{display:block;height:100%;width:calc(var(--hechas,0) * 10%);background:var(--gold);
  box-shadow:0 0 12px var(--gold);transition:width .5s}

/* ── HBAR waveC: el Canto (LA VOZ ES EL OUTPUT). Navegación + sentido. ── */
.hbar{position:fixed;left:0;right:0;bottom:0;z-index:40;
  padding:8px 16px calc(8px + env(safe-area-inset-bottom,0px));
  background:linear-gradient(0deg,rgba(5,5,5,.97),rgba(5,5,5,.6));
  backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);
  border-top:1px solid rgba(255,255,255,.08)}
.waveC{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.wave{flex:1 1 180px;min-width:120px;height:26px;overflow:visible}
.wave path{fill:none;stroke:var(--sig);stroke-width:1.6;stroke-linecap:round;
  filter:drop-shadow(0 0 6px var(--sig));animation:canto 4.6s ease-in-out infinite}
@keyframes canto{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.hn{font:700 10px/1 var(--fm);letter-spacing:2px;color:var(--txt-dim);text-decoration:none;
  border:1px solid rgba(255,255,255,.18);background:transparent;border-radius:8px;padding:9px 13px;
  cursor:pointer;transition:border-color .25s,color .25s,background .25s;white-space:nowrap}
.hn:hover{border-color:var(--sig);color:#fff;background:rgba(255,0,60,.12)}
.hn.core{border-color:var(--sig);color:var(--sig)}
.sense{display:flex;align-items:center;gap:8px}
.sense label{font:400 9px/1 var(--fm);letter-spacing:2px;color:var(--txt-ghost)}
.sense input[type=range]{width:104px;accent-color:var(--sig);cursor:pointer}
.sense output{font:700 9px/1 var(--fm);color:var(--sig);min-width:62px}

.langs{display:flex;gap:6px;align-items:center}
.langs .hn{padding:8px 9px;letter-spacing:1px}
.langs .hn[aria-current="true"]{border-color:var(--gold);color:var(--gold);background:rgba(255,215,0,.1)}

/* ── Accesibilidad y responsive ─ */
@media (max-width:680px){
  .brand small{display:none}
  .sig-badge{display:none}
  .stage{padding:84px 14px 176px}
  .mirror{padding:18px}
  .title{letter-spacing:.02em}
}
@media (prefers-reduced-motion:reduce){
  .eye,.ring,.ring-b,.orbit,.wave path,.spark.on,.brand-eye,.skin{animation:none !important}
}
"""

CORE_JS = r"""/* ══════════════════════════════════════════════════════════════════════
   BELENTANI // GALAXIAS — runtime compartido de las 50 páginas.
   Sin dependencias externas. Nunca bloquea la página. Respeta
   prefers-reduced-motion y no interpola datos no confiables en HTML.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var REDUCED = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SENSES = ['neon', 'matrix', 'venom', 'void', 'ascended'];

  /* Campo de estrellas: rojo sangre cada 7 estrellas (la firma del universo). */
  function starfield(canvas) {
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    var S = [], w = 0, h = 0, dpr = 1, t = 0;
    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.width = Math.floor(innerWidth * dpr);
      h = canvas.height = Math.floor(innerHeight * dpr);
      canvas.style.width = innerWidth + 'px';
      canvas.style.height = innerHeight + 'px';
    }
    resize();
    addEventListener('resize', resize, { passive: true });
    var N = innerWidth < 700 ? 130 : 240;
    for (var i = 0; i < N; i++) {
      S.push({
        x: Math.random(), y: Math.random(),
        r: (Math.random() * 1.6 + 0.4) * dpr,
        s: (Math.random() * 0.5 + 0.12) * dpr,
        red: i % 7 === 0
      });
    }
    function paint() {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < S.length; i++) {
        var p = S[i];
        var tw = 0.35 + 0.65 * Math.abs(Math.sin(t / 90 + i));
        ctx.fillStyle = p.red ? 'rgba(255,0,60,' + tw + ')'
                              : 'rgba(255,255,255,' + (tw * 0.68) + ')';
        ctx.beginPath();
        ctx.arc(p.x * w, p.y * h, p.r, 0, 6.2832);
        ctx.fill();
      }
    }
    if (REDUCED) { t = 40; paint(); return; }
    (function frame() {
      t += 1;
      for (var i = 0; i < S.length; i++) {
        S[i].y -= S[i].s / 900;
        if (S[i].y < 0) S[i].y = 1;
      }
      paint();
      requestAnimationFrame(frame);
    })();
  }

  /* Sparks del hero-orbit = las 10 estaciones; la activa brilla en oro.
     El radio se mide en px porque translate(%) es relativo al propio punto. */
  function buildSparks(orbit, estaciones, activa) {
    var frag = document.createDocumentFragment();
    var dots = [];
    for (var i = 0; i < estaciones.length; i++) {
      var s = document.createElement('span');
      s.className = 'spark' + (i === activa ? ' on' : '');
      s.style.setProperty('--a', (i * 36) + 'deg');
      s.title = estaciones[i][1];
      s.setAttribute('aria-hidden', 'true');
      frag.appendChild(s);
      dots.push(s);
    }
    orbit.appendChild(frag);
    function medida() {
      var lado = orbit.getBoundingClientRect().width;
      if (!lado) return;
      for (var k = 0; k < dots.length; k++) {
        dots[k].style.setProperty('--r',
          (lado * (0.30 + (k % 3) * 0.035)).toFixed(1) + 'px');
      }
    }
    medida();
    addEventListener('resize', medida, { passive: true });
  }

  /* Memoria: omega_story guarda las estaciones recorridas (§9 canon). */
  function story(id) {
    try {
      var raw = localStorage.getItem('omega_story');
      var list = Array.isArray(JSON.parse(raw)) ? JSON.parse(raw) : [];
      if (list.indexOf(id) === -1) list.push(id);
      if (list.length > 50) list = list.slice(-50);
      localStorage.setItem('omega_story', JSON.stringify(list));
      return list.length;
    } catch (e) { return 0; }
  }

  function mountGalaxia(cfg) {
    var body = document.body;
    var st = document.getElementById('stars');
    if (st) starfield(st);
    var orbit = document.getElementById('orbit');
    var EST = (window.GALAXIA_I18N && window.GALAXIA_I18N.estaciones) || cfg.estaciones || [];
    if (orbit) buildSparks(orbit, EST, cfg.estacion);
    body.style.setProperty('--beat', cfg.beat + 's');
    document.documentElement.style.setProperty('--hechas', String(story(cfg.id)));

    /* Sentido: 5 paradas = 5 firmas (rojo/verde/púrpura/void/oro). */
    var slider = document.getElementById('sense');
    var out = document.getElementById('sense-out');
    function apply(i, persist) {
      i = Math.max(0, Math.min(SENSES.length - 1, i | 0));
      for (var k = 0; k < SENSES.length; k++) body.classList.remove('sense-' + SENSES[k]);
      body.classList.add('sense-' + SENSES[i]);
      if (slider) slider.value = String(i);
      if (out) out.textContent = SENSES[i].toUpperCase();
      if (persist) { try { localStorage.setItem('omega_sense', String(i)); } catch (e) {} }
    }
    var saved = 0;
    try { saved = parseInt(localStorage.getItem('omega_sense'), 10) || 0; } catch (e) {}
    apply(saved, false);
    if (slider) slider.addEventListener('input', function () { apply(this.value, true); });

    /* i18n: orden fijo PT > ES > EN > CA (regla global del ecosistema).
       No se crean ficheros por idioma: ?lang=xx + hreflang alternates. */
    var LANGS = ['pt', 'es', 'en', 'ca'];
    function langCode() {
      var q = '';
      try { q = new URLSearchParams(location.search).get('lang') || ''; } catch (e) {}
      q = q.toLowerCase();
      if (LANGS.indexOf(q) !== -1) return q;
      var nav = (navigator.language || 'es').slice(0, 2).toLowerCase();
      return LANGS.indexOf(nav) !== -1 ? nav : 'es';
    }
    function applyLang(code) {
      document.documentElement.lang = code;
      if (cfg.espejo && cfg.espejo[code]) {
        var esp = document.getElementById('espejo');
        if (esp) esp.textContent = cfg.espejo[code];
      }
      var dict = (cfg.ui && cfg.ui[code]) || null;
      if (dict) {
        var nodos = document.querySelectorAll('[data-i18n]');
        for (var i = 0; i < nodos.length; i++) {
          var clave = nodos[i].getAttribute('data-i18n');
          if (dict[clave]) nodos[i].textContent = dict[clave];
        }
      }
      try { localStorage.setItem('omega_lang', code); } catch (e) {}
    }
    var qlang = '';
    try { qlang = new URLSearchParams(location.search).get('lang') || ''; } catch (e) {}
    var prefs = '';
    try { prefs = localStorage.getItem('omega_lang') || ''; } catch (e) {}
    applyLang(LANGS.indexOf(qlang.toLowerCase()) !== -1 ? qlang.toLowerCase()
              : (LANGS.indexOf(prefs) !== -1 ? prefs : langCode()));

    /* Teclado: ← anterior · → siguiente · ESC hub · 1-5 sentido. */
    addEventListener('keydown', function (ev) {
      if (ev.target && /INPUT|TEXTAREA|SELECT/.test(ev.target.tagName)) return;
      if (ev.key === 'ArrowLeft' && cfg.prev) location.href = cfg.prev;
      else if (ev.key === 'ArrowRight' && cfg.next) location.href = cfg.next;
      else if (ev.key === 'Escape') location.href = 'index.html';
      else if (ev.key >= '1' && ev.key <= '5') apply(parseInt(ev.key, 10) - 1, true);
    });

    /* El Ojo late más rápido al acercar el cursor: feedback, no decoración. */
    if (!REDUCED) {
      var eye = document.querySelector('.eye');
      if (eye) eye.addEventListener('pointermove', function () {
        body.style.setProperty('--beat', (cfg.beat * 0.55).toFixed(2) + 's');
      });
      if (eye) eye.addEventListener('pointerleave', function () {
        body.style.setProperty('--beat', cfg.beat + 's');
      });
    }
    /* Idioma: orden fijo PT > ES > EN > CA (regla del ecosistema). */
    var I18N = window.GALAXIA_I18N || { order: ['pt', 'es', 'en', 'ca'], ui: {}, trad: {} };
    var lang = 'es';
    try {
      var q = new URLSearchParams(location.search).get('lang');
      if (q && I18N.order.indexOf(q) !== -1) lang = q;
    } catch (e2) { lang = 'es'; }
    function applyLang(code) {
      if (I18N.order.indexOf(code) === -1) code = 'es';
      document.documentElement.lang = code;
      var tr = (I18N.trad && I18N.trad[cfg.slug]) || {};
      var espejo = document.getElementById('espejo');
      if (espejo && tr[code]) espejo.textContent = tr[code];
      var ui = (I18N.ui && I18N.ui[code]) || {};
      var map = { 'l-skip': 'skip', 'l-prev': 'prev', 'l-core': 'core',
                  'l-next': 'next', 'l-sense': 'sense', 'l-sig': 'firma' };
      for (var id in map) {
        var el = document.getElementById(id);
        if (el && ui[map[id]]) el.textContent = ui[map[id]];
      }
      var chips = document.querySelectorAll('.langs .hn');
      for (var i = 0; i < chips.length; i++) {
        if (chips[i].getAttribute('hreflang') === code) chips[i].setAttribute('aria-current', 'true');
        else chips[i].removeAttribute('aria-current');
      }
    }
    applyLang(lang);

    window.GALAXIA = { id: cfg.id, firma: cfg.firma, estacion: cfg.estacion,
                       slug: cfg.slug, lang: lang, reduced: REDUCED };
  }

  window.mountGalaxia = mountGalaxia;
  window.omegaStarfield = starfield;
})();
"""

TRAD = {
    "entre": {
        "pt": "A história não se repete. Confronta-se.",
        "en": "History does not repeat. It confronts.",
        "ca": "La història no es repeteix. Es confronta.",
    },
    "deuda": {
        "pt": "A dívida tornou-se impagável: devoção sem retorno.",
        "en": "The debt became unpayable: devotion given without return.",
        "ca": "El deute es va tornar impagable: devoció sense retorn.",
    },
    "robo": {
        "pt": "Judas tomou a Chave Dourada de noite, com vergonha mais do que maldade.",
        "en": "Judas took the Golden Key by night, out of shame more than malice.",
        "ca": "Judas va prendre la Clau Daurada de nit, per vergonya més que per maldat.",
    },
    "canto": {
        "pt": "Pedro sentou-se e começou a cantar-lhe.",
        "en": "Pedro sat down and began to sing to him.",
        "ca": "Pedro es va asseure i es va posar a cantar-li.",
    },
    "victoria": {
        "pt": "Fica com ela. A chave é metal. O que eu tenho ninguém me tira: a minha voz.",
        "en": "Keep it. The key is metal. What I have no one can take from me: my voice.",
        "ca": "Queda-te-la. La clau és metall. El que jo tinc ningú no m'ho arrabassa: la meva veu.",
    },
    "mentira": {
        "pt": "A chave nunca foi o valioso. Era uma mentira partilhada.",
        "en": "The key was never the valuable thing. It was a shared lie.",
        "ca": "La clau mai no va ser el valuós. Era una mentida compartida.",
    },
    "umbral": {
        "pt": "Deixa que te roubem o que não importa para revelar o que importa.",
        "en": "Let them take what does not matter so that what does is revealed.",
        "ca": "Deixa que et robin el que no importa per revelar el que sí.",
    },
    "senal": {
        "pt": "Fragmentos visuais + som + texto.",
        "en": "Visual fragments + sound + text.",
        "ca": "Fragments visuals + so + text.",
    },
    "portal": {
        "pt": "O portal não é uma página. THE PORTAL TO BECOMING SOMEONE ELSE.",
        "en": "The portal is not a page. THE PORTAL TO BECOMING SOMEONE ELSE.",
        "ca": "El portal no és una pàgina. THE PORTAL TO BECOMING SOMEONE ELSE.",
    },
    "constelacion": {
        "pt": "THE NEXT CHAPTER IS YOURS.",
        "en": "THE NEXT CHAPTER IS YOURS.",
        "ca": "THE NEXT CHAPTER IS YOURS.",
    },
}

UI = {
    "pt": {"skip": "Ir para o núcleo", "prev": "ANTERIOR", "core": "NÚCLEO",
           "next": "SEGUINTE", "sense": "SENTIDO", "hub": "OMEGA",
           "firma": "ASSINATURA", "nav": "Navegação do Canto",
           "progreso": "Estações gravadas"},
    "es": {"skip": "Ir al núcleo", "prev": "ANTERIOR", "core": "NÚCLEO",
           "next": "SIGUIENTE", "sense": "SENTIDO", "hub": "OMEGA",
           "firma": "FIRMA", "nav": "Navegación del Canto",
           "progreso": "Estaciones grabadas"},
    "en": {"skip": "Skip to the core", "prev": "PREVIOUS", "core": "CORE",
           "next": "NEXT", "sense": "SENSE", "hub": "OMEGA",
           "firma": "SIGNATURE", "nav": "Song navigation",
           "progreso": "Recorded stations"},
    "ca": {"skip": "Ves al nucli", "prev": "ANTERIOR", "core": "NUCLI",
           "next": "SEGÜENT", "sense": "SENTIT", "hub": "OMEGA",
           "firma": "SIGNATURA", "nav": "Navegació del Cant",
           "progreso": "Estacions enregistrades"},
}
# ===END EXTRACTED CANON===

CORE_CSS = CORE_CSS_A + CORE_CSS_B

# ── CSS exclusivo del hub (mapa de las 50 galaxias) ──────────────────────
HUB_CSS = r"""
/* ══ HUB: el mapa. Se sirve dentro de galaxia.css para cachear un solo CSS. ══ */
body.hub-body{overflow:auto}
.hub{position:relative;z-index:2;max-width:1180px;margin:0 auto;padding:104px 18px 190px}
.hub .hero{text-align:center;margin-bottom:34px}
.hub .hero h1{font:900 clamp(38px,9vw,96px)/1 var(--fd);letter-spacing:.06em;
  text-shadow:0 0 30px rgba(255,0,60,.7),0 0 110px rgba(255,0,60,.35);
  animation:neonpulse 3.8s ease-in-out infinite}
@keyframes neonpulse{0%,100%{opacity:.88}50%{opacity:1}}
.hub .hero p{max-width:64ch;margin:14px auto 0;color:var(--txt-dim);
  font:300 15px/1.8 var(--fu)}
.hub .hero .eq{font:700 11px/1 var(--fm);letter-spacing:4px;color:var(--blood);
  margin-top:14px;letter-spacing:4px}
.rowlab{display:flex;align-items:baseline;gap:12px;margin:26px 0 10px;
  border-left:2px solid var(--fg,var(--blood));padding-left:12px}
.rowlab b{font:900 13px/1 var(--fd);letter-spacing:3px;color:var(--fg,var(--blood))}
.rowlab span{font:400 10px/1 var(--fm);letter-spacing:2px;color:var(--txt-ghost)}
.matrix{display:grid;gap:9px;grid-template-columns:repeat(auto-fill,minmax(122px,1fr))}
.cell{position:relative;display:flex;flex-direction:column;gap:5px;padding:13px 12px;
  border-radius:12px;text-decoration:none;color:inherit;
  background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.12);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  transition:transform .22s,border-color .22s,box-shadow .22s,background .22s}
.cell b{font:900 19px/1 var(--fd);color:var(--fg,var(--blood));
  text-shadow:0 0 16px var(--fg,var(--blood))}
.cell i{font:400 9.5px/1.35 var(--fm);letter-spacing:1.1px;color:var(--txt-dim);
  font-style:normal;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cell:hover{transform:translateY(-3px);border-color:var(--fg,var(--blood));
  background:rgba(255,255,255,.06);box-shadow:0 14px 40px rgba(0,0,0,.6),
  0 0 26px color-mix(in srgb,var(--fg,var(--blood)) 45%,transparent)}
.cell.done::after{content:'◉';position:absolute;top:8px;right:9px;font-size:10px;
  color:var(--gold);text-shadow:0 0 10px var(--gold)}
.legend{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(238px,1fr));
  margin:44px 0 0}
.legend>div{padding:16px 18px;border-radius:14px;background:var(--glass);
  border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(18px);
  -webkit-backdrop-filter:blur(18px)}
.legend h3{font:700 10.5px/1 var(--fm);letter-spacing:2.4px;color:var(--blood);
  margin-bottom:9px}
.legend p{font:300 13px/1.72 var(--fu);color:var(--txt-dim)}
.legend b{color:#fff}
.legend code{font:400 11px/1 var(--fm);color:var(--gold)}
.reliquias{margin:48px 0 0}
.reliquias h2{font:900 15px/1 var(--fd);letter-spacing:3px;margin-bottom:6px}
.reliquias p{font:300 13px/1.7 var(--fu);color:var(--txt-ghost);margin-bottom:16px}
.rgrid{display:grid;gap:9px;grid-template-columns:repeat(auto-fill,minmax(104px,1fr))}
.rgrid figure{margin:0;border-radius:11px;overflow:hidden;
  border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);
  transition:transform .22s,border-color .22s}
.rgrid figure:hover{transform:translateY(-3px) scale(1.02);border-color:var(--blood)}
.rgrid img{display:block;width:100%;height:auto;aspect-ratio:1;object-fit:cover}
.rgrid figcaption{font:400 8.5px/1.3 var(--fm);color:var(--txt-ghost);padding:6px 7px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.langs{display:flex;gap:7px;align-items:center}
.lchip{font:700 9.5px/1 var(--fm);letter-spacing:1.6px;color:var(--txt-dim);
  text-decoration:none;border:1px solid rgba(255,255,255,.2);border-radius:999px;
  padding:6px 10px;cursor:pointer;background:transparent}
.lchip[aria-current="true"]{border-color:var(--blood);color:var(--blood)}
.count{font:700 10px/1 var(--fm);letter-spacing:2px;color:var(--gold)}
@media (max-width:680px){
  .hub{padding:92px 14px 200px}
  .matrix{grid-template-columns:repeat(auto-fill,minmax(96px,1fr))}
}
"""
