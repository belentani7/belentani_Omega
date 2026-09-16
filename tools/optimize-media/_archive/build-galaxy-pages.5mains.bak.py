#!/usr/bin/env python3
"""Genera las 50 galaxias unificadas de BELENTANI // JUDAS ERA.

Modelo del universo (todo elemento tiene función, nada decorativo):
  5 Firmas (LORE-UNIFICADO §6) x 10 Estaciones = 50 páginas.

  topnav ndots ....... las 5 Firmas; cambiar de firma = cambiar de mundo
  Ojo de Judas ....... el planeta; gira y late a la frecuencia de la estación
  anillo ............. la Llave Dorada robada (victoria amarga)
  hero-orbit sparks .. las 10 estaciones; la activa brilla
  hbar waveC ......... el Canto (LA VOZ ES EL OUTPUT); navegación
  espejo ............. línea canon de (firma x estación)
  slider sentido ..... NEON / MATRIX / VENOM / VOID

Aditivo y reversible: sólo escribe en galaxias/. No toca index.html,
css/, js/ ni ningún asset existente.
"""
from __future__ import annotations

import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "galaxias"
CORE = OUT / "core"

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

# ── Canon: las 10 estaciones del portal (§9 + recorrido) ─────────────────
# (slug, nombre, beat_s, frase canon, sentido)
ESTACIONES = [
    ("entre", "EL ENTRE", 3.2, "La historia no se repite. Se confronta.", 1),
    ("deuda", "LA DEUDA", 2.8, "La deuda se volvió impagable: devoción sin devolución.", 2),
    ("robo", "EL ROBO", 2.4, "Judas tomó la Llave Dorada de noche, con vergüenza más que maldad.", 3),
    ("canto", "EL CANTO", 2.0, "Pedro se sentó y se puso a cantarle.", 4),
    ("victoria", "LA VICTORIA AMARGA", 1.8, "Quédatela. La llave es metal. Lo que yo tengo nadie me lo arrebata: mi voz.", 5),
    ("mentira", "LA MENTIRA COMPARTIDA", 1.6, "La llave nunca fue lo valioso. Era una mentira compartida.", 5),
    ("umbral", "EL UMBRAL", 1.4, "Deja que te roben lo que no importa para revelar lo que sí.", 4),
    ("senal", "LA SEÑAL", 1.2, "Fragmentos visuales + sonido + texto.", 3),
    ("portal", "EL PORTAL", 1.0, "El portal no es una página. THE PORTAL TO BECOMING SOMEONE ELSE.", 2),
    ("constelacion", "LA CONSTELACIÓN", 0.9, "THE NEXT CHAPTER IS YOURS.", 1),
]

# Sentido: 1 NEON (rojo firma) · 2 MATRIX · 3 VENOM · 4 VOID · 5 ASCENDED
SENTIDOS = {
    1: ("neon", "#ff003c"),
    2: ("matrix", "#00ff41"),
    3: ("venom", "#b026ff"),
    4: ("void", "#8899aa"),
    5: ("ascended", "#ffd700"),
}

FUENTES = ("https://fonts.googleapis.com/css2?"
           "family=Chakra+Petch:wght@300;400;600;700&"
           "family=JetBrains+Mono:wght@400;700&"
           "family=Orbitron:wght@600;900&display=swap")


def pagina_id(f: int, e: int) -> str:
    """f 0..4 (firma), e 0..9 (estación) -> 1..50."""
    return f"{(f * 10 + e) + 1:02d}"


def vecinos(n: int):
    previo = 50 if n == 1 else n - 1
    siguiente = 1 if n == 50 else n + 1
    return f"galaxia-{previo:02d}.html", f"galaxia-{siguiente:02d}.html"


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

CORE_CSS = CORE_CSS_A + CORE_CSS_B

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

# ── i18n: orden fijo PT > ES > EN > CA (regla global del ecosistema). ────
# Los nombres de estación son canon y NO se traducen; se traduce el espejo
# y las etiquetas de interfaz.
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
IDIOMAS = ["pt", "es", "en", "ca"]

SPARKS_WAVE = ("M0 13 C 14 2, 26 24, 40 13 S 66 2, 80 13 S 106 24, 120 13 "
               "S 146 2, 160 13 S 186 24, 200 13")


def slugify(txt: str) -> str:
    """Lowercase ASCII slug para uso en clases/kicker (nunca en HTML crudo)."""
    limpio = txt.lower().replace(".", "")
    return re.sub(r"[^a-z0-9]+", "-", limpio).strip("-")


def html_pagina(f: int, e: int) -> str:
    """Genera el HTML completo de una galaxia (firma f, estación e)."""
    folio = pagina_id(f, e)
    fslug, fsig, fnombre, fcolor, fvalor, ffrase = FIRMAS[f]
    eslug, enombre, ebeat, efrase, sentido = ESTACIONES[e]
    sentido_slug, _ = SENTIDOS[sentido]
    prev, nxt = vecinos(int(folio))
    ui = UI["pt"]
    # hreflang: 4 idiomas en orden PT > ES > EN > CA + x-default
    alt = "\n".join(
        f'  <link rel="alternate" hreflang="{lg}" href="galaxia-{folio}.html?lang={lg}">'
        for lg in IDIOMAS)
    alt += f'\n  <link rel="alternate" hreflang="x-default" href="galaxia-{folio}.html">'

    # El espejo: PT visible (primera posición), ES/EN/CA en el mismo bloque.
    espejos = [f'<span data-lang="pt" lang="pt">{efrase}</span>']
    for lg in ("es", "en", "ca"):
        espejos.append(f'<span data-lang="{lg}" lang="{lg}" hidden>{TRAD[eslug][lg]}</span>')

    ndots = "\n".join(
        '      <li><a class="nstar" href="galaxia-{n}" data-firma="{s}" '
        'style="--sig:{c}" title="{sig} · {nom}" '
        'aria-label="{sig} · {nom}"{cur}></a></li>'.format(
            n=f"{i * 10 + e + 1:02d}", s=fs2[0], c=fs2[3], sig=fs2[1],
            nom=fs2[2], cur=' aria-current="true"' if i == f else "")
        for i, fs2 in enumerate(FIRMAS))

    return f"""<!DOCTYPE html>
<html lang="pt" data-galaxia="{folio}" data-firma="{fslug}" data-estacion="{eslug}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>BELENTANI // {enombre} — {fnombre} · GALAXIA {folio}/50</title>
<meta name="description" content="{efrase} — {fnombre} ({fsig}), {fvalor}. Galaxia {folio} de 50 del universo BELENTANI // JUDAS ERA.">
<meta name="theme-color" content="{fcolor}">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="galaxia-{folio}.html">
{alt}
<meta property="og:type" content="website">
<meta property="og:title" content="BELENTANI // {enombre} — {fnombre}">
<meta property="og:description" content="{efrase}">
<meta property="og:image" content="../assets/images/og-cover.jpg">
<meta property="og:locale" content="pt_BR">
<meta property="og:locale:alternate" content="es_ES">
<meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/icons/icon-192.png">
<link rel="manifest" href="../manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FUENTES}">
<link rel="stylesheet" href="core/core.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CreativeWork","name":"{enombre} — {fnombre}","isPartOf":{{"@type":"CreativeWorkSeries","name":"BELENTANI // JUDAS ERA — GALAXIAS","position":{int(folio)}}},"inLanguage":["pt","es","en","ca"],"creator":{{"@type":"MusicArtist","name":"Belentani"}}}}</script>
</head>
<body>
<a class="skip" href="#espejo">{ui['skip']}</a>
<canvas id="stars" aria-hidden="true"></canvas>

<header class="topnav">
  <a class="brand" href="index.html" title="{ui['hub']}">
    <span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>GALAXIA {folio}/50 · {fsig}</small></span>
  </a>
  <span class="sig-badge">{ui['firma']} · {fnombre} · {fvalor}</span>
  <nav aria-label="{ui['firma']}">
    <ul class="ndots">
{ndots}
    </ul>
  </nav>
</header>

<main class="stage">
  <div class="eye-wrap">
    <span class="ring" aria-hidden="true"></span>
    <span class="ring ring-b" aria-hidden="true"></span>
    <span class="eye" aria-hidden="true"></span>
    <span class="skin" aria-hidden="true"></span>
    <span class="orbit" id="orbit" aria-hidden="true"></span>
  </div>
</main>

<section class="mirror" id="espejo" style="position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);margin:0">
  <p class="kicker">{ui['firma']} {slugify(fsig)} / ESTACIÓN {e + 1:02d} — {enombre}</p>
  <h1 class="title">{enombre.split(' ')[0]} <em>{' '.join(enombre.split(' ')[1:])}</em></h1>
  <p class="espejo">{"".join(espejos)}</p>
  <p class="firma">{fsig} <b>{fnombre}</b> · {fvalor} — <q>{ffrase}</q></p>
  <div class="progress" role="presentation"><i></i></div>
  <p class="firma" style="margin-top:10px">
    <button class="hn" type="button" data-lang-btn="pt">PT</button>
    <button class="hn" type="button" data-lang-btn="es">ES</button>
    <button class="hn" type="button" data-lang-btn="en">EN</button>
    <button class="hn" type="button" data-lang-btn="ca">CA</button>
  </p>
</section>

<footer class="hbar">
  <div class="waveC">
    <a class="hn" href="{prev}">← {ui['prev']}</a>
    <svg class="wave" viewBox="0 0 200 26" preserveAspectRatio="none" aria-hidden="true">
      <path d="{SPARKS_WAVE}"></path>
    </svg>
    <a class="hn core" href="index.html">{ui['hub']}</a>
    <a class="hn" href="{nxt}">{ui['next']} →</a>
    <span class="sense">
      <label for="sense">{ui['sense']}</label>
      <input id="sense" type="range" min="0" max="4" step="1" value="0" aria-describedby="sense-out">
      <output id="sense-out">NEON</output>
    </span>
  </div>
</footer>

<script src="core/core.js" defer></script>
<script>
window.addEventListener('DOMContentLoaded', function () {{
  mountGalaxia({{
    id: '{folio}', firma: '{fslug}', estacion: {e}, beat: {ebeat},
    prev: '{prev}', next: '{nxt}',
    estaciones: {json.dumps([[s, n] for s, n, *_ in ESTACIONES], ensure_ascii=False)}
  }});
}});
</script>
</body>
</html>
"""


def fecha() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def emit_core() -> list[dict]:
    """Escribe core/galaxia.css + core/galaxia.js + core/galaxias.json."""
    CORE.mkdir(parents=True, exist_ok=True)
    (CORE / "galaxia.css").write_text(CORE_CSS, encoding="utf-8")
    (CORE / "galaxia.js").write_text(CORE_JS, encoding="utf-8")
    paginas = []
    for fi, firma in enumerate(FIRMAS):
        for ei, est in enumerate(ESTACIONES):
            n = fi * 10 + ei + 1
            paginas.append({
                "n": n, "archivo": f"galaxia-{n:02d}.html",
                "firma_id": firma[0], "firma": firma[1], "rol": firma[2],
                "color_firma": firma[3],
                "estacion_id": est[0], "estacion": est[1], "beat": est[2],
                "sentido": est[4],
            })
    (CORE / "galaxias.json").write_text(json.dumps({
        "generado": fecha(), "total": len(paginas), "idiomas": IDIOMAS,
        "sentidos": [{"i": k, "nombre": v[0], "color": v[1]}
                     for k, v in sorted(SENTIDOS.items())],
        "paginas": paginas,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"core -> {CORE.name}/galaxia.css + galaxia.js + galaxias.json "
          f"({len(paginas)} páginas)")
    return paginas


def carga_imagenes() -> list[dict]:
    """Imágenes reales ya optimizadas en assets/galaxy/manifest.json."""
    ruta = REPO / "assets" / "galaxy" / "manifest.json"
    if not ruta.exists():
        return []
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return []
    return [e for e in datos.get("imagenes", []) if e.get("ancho", 0) > 0]


def html_pagina(n_f: int, n_e: int, imagenes: list[dict]) -> str:
    """Construye una de las 50 páginas desde el canon."""
    fid, fnombre, ftitulo, fcolor, fsentido, ffrase = FIRMAS[n_f]
    eslug, enombre, ebeat, efrase, esentido = ESTACIONES[n_e]
    numero = pagina_id(n_f, n_e)
    previo, siguiente = vecinos(int(numero))
    sentido_nombre, _ = SENTIDOS[esentido]

    img = imagenes[(n_f * 10 + n_e) % len(imagenes)] if imagenes else None
    img_ruta = f"../{img['webp']}" if img else ""
    img_w = img["ancho"] if img else 1920
    img_h = img["alto"] if img else 1080

    ndots = []
    for i, (_, _, otitulo, ocolor, _, _) in enumerate(FIRMAS):
        actual = "true" if i == n_f else "false"
        ndots.append(
            f'<li><a class="nstar" href="galaxia-{pagina_id(i, n_e)}.html" '
            f'style="--sig:{ocolor}" aria-current="{actual}" '
            f'title="{otitulo}" aria-label="{otitulo}"></a></li>')
    ndots = "\n      ".join(ndots)

    i18n = {"pt": {}, "es": {}, "en": {}, "ca": {}}
    for est in ESTACIONES:
        i18n["es"][est[0]] = est[3]
        for idi in ("pt", "en", "ca"):
            i18n[idi][est[0]] = TRAD.get(est[0], {}).get(idi, est[3])
    i18n["ui"] = {i: UI[i] for i in IDIOMAS}
    og_img = img_ruta or "../assets/images/og-cover.jpg"

    head = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{fnombre} · {enombre} — BELENTANI // {numero}/50</title>
<meta name="description" content="{efrase} — {ftitulo} ({fnombre}), estación {numero} de 50 del universo BELENTANI // JUDAS ERA.">
<meta name="theme-color" content="{fcolor}">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="galaxia-{numero}.html">
<link rel="alternate" hreflang="pt" href="galaxia-{numero}.html?lang=pt">
<link rel="alternate" hreflang="es" href="galaxia-{numero}.html?lang=es">
<link rel="alternate" hreflang="en" href="galaxia-{numero}.html?lang=en">
<link rel="alternate" hreflang="ca" href="galaxia-{numero}.html?lang=ca">
<link rel="alternate" hreflang="x-default" href="galaxia-{numero}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{fnombre} · {enombre} — BELENTANI // JUDAS ERA">
<meta property="og:description" content="{efrase}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FUENTES}">
<link rel="stylesheet" href="core/galaxias.css">
</head>
<body class="sense-{sentido_nombre}" data-numero="{numero}">
<a class="skip" href="#nucleo" data-i18n="skip">Ir al núcleo</a>
<canvas id="stars" aria-hidden="true"></canvas>

<header class="topnav">
  <a class="brand" href="index.html" title="Mapa de las 50">
    <span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>{numero} / 50 · JUDAS ERA</small></span>
  </a>
  <span class="sig-badge" data-i18n="firma">{UI['es']['firma']}: {fnombre}</span>
  <ul class="ndots" aria-label="Las cinco firmas">
      {ndots}
  </ul>
</header>
"""

    cuerpo = f"""
<main class="stage">
  <div class="eye-wrap">
    <div class="ring" aria-hidden="true"></div>
    <div class="ring ring-b" aria-hidden="true"></div>
    <img class="eye" src="{img_ruta}" width="{img_w}" height="{img_h}"
         alt="{enombre} — {ftitulo}" decoding="async" fetchpriority="high"
         onerror="this.style.opacity='.16'">
    <div class="skin" aria-hidden="true"></div>
    <div class="orbit" id="orbit" aria-hidden="true"></div>
  </div>
</main>

<section class="mirror" id="nucleo">
  <p class="kicker">{fnombre} — ESTACIÓN {numero} DE 50</p>
  <h1 class="title"><em>{enombre}</em></h1>
  <p class="espejo" id="espejo" data-i18n="espejo">{efrase}</p>
  <p class="firma">
    <b>{fnombre}</b> [{ftitulo}] · sentido {sentido_nombre.upper()} ·
    beat {ebeat}s · firma <b style="color:{fcolor}">{fcolor}</b><br>
    {ffrase}
  </p>
  <div class="progress" role="progressbar" aria-label="Estaciones registradas"
       aria-valuemin="0" aria-valuemax="10"><i></i></div>
  <noscript><p class="firma">Sin JavaScript el contenido y la navegación siguen
  funcionando; sólo faltan el latido del Ojo y el campo de estrellas.</p></noscript>
</section>

<footer class="hbar">
  <nav class="waveC" aria-label="Navegación de estaciones">
    <a class="hn" href="{previo}">&#9664; <span data-i18n="prev">{UI['es']['prev']}</span></a>
    <svg class="wave" viewBox="0 0 240 26" aria-hidden="true">
      <path d="M0 13 Q 15 3 30 13 T 60 13 T 90 13 T 120 13 T 150 13 T 180 13 T 210 13 T 240 13"/>
    </svg>
    <a class="hn core" href="index.html" data-i18n="core">{UI['es']['core']}</a>
    <a class="hn" href="{siguiente}"><span data-i18n="next">{UI['es']['next']}</span> &#9654;</a>
    <span class="sense">
      <label for="sense" data-i18n="sense">{UI['es']['sense']}</label>
      <input id="sense" type="range" min="0" max="4" step="1"
             value="{list(SENTIDOS).index(esentido)}"
             aria-label="Sentido: NEON, MATRIX, VENOM, VOID, ASCENDED">
      <output id="sense-out" for="sense">{sentido_nombre.upper()}</output>
    </span>
  </nav>
</footer>

<script type="application/json" id="i18n">{json.dumps(i18n, ensure_ascii=False)}</script>
<script>window.__EST__={json.dumps([[e[0], e[1]] for e in ESTACIONES], ensure_ascii=False)};
window.__ESTACION__={n_e};</script>
<script src="core/galaxias.js" defer></script>
</body>
</html>
"""
    return head + cuerpo


def esc(t: str) -> str:
    """Escape HTML: nunca interpolamos texto sin escapar en el documento."""
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


def pagina_html(num: int, fi: int, ei: int) -> str:
    """Construye una galaxia: firma fi x estación ei -> galaxia-NN.html."""
    f_slug, f_id, f_nom, f_col, f_virt, f_frase = FIRMAS[fi]
    e_slug, e_nom, beat, e_frase, sentido_n = ESTACIONES[ei]
    s_slug, s_col = SENTIDOS[sentido_n]
    prev, nxt = vecinos(num)
    gid = pagina_id(fi, ei)
    firmas_links = []
    for i, (fs, fid, fn, fc, fv, ff) in enumerate(FIRMAS):
        n2 = (i * 10 + ei) + 1
        cur = "true" if i == fi else "false"
        firmas_links.append(
            f'<li><a class="nstar" href="galaxia-{n2:02d}.html" '
            f'style="--sig:{fc}" aria-current="{cur}" '
            f'title="{esc(fn)} — {esc(fv)}"><span class="vh">{esc(fn)}</span></a></li>')
    firmas_ndots = "\n      ".join(firmas_links)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GALAXIA {gid} · {esc(e_nom)} — {esc(f_nom)} | BELENTANI</title>
<meta name="description" content="{esc(f_nom)} · {esc(e_nom)}. {esc(e_frase)}">
<meta name="theme-color" content="{f_col}">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="https://belentani.es/galaxias/galaxia-{num:02d}.html">
<link rel="alternate" hreflang="pt" href="galaxia-{num:02d}.html?lang=pt">
<link rel="alternate" hreflang="es" href="galaxia-{num:02d}.html?lang=es">
<link rel="alternate" hreflang="en" href="galaxia-{num:02d}.html?lang=en">
<link rel="alternate" hreflang="ca" href="galaxia-{num:02d}.html?lang=ca">
<link rel="alternate" hreflang="x-default" href="galaxia-{num:02d}.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FUENTES}" rel="stylesheet">
<link rel="stylesheet" href="core/galaxia.css">
<style>:root{{--sig:{f_col};--beat:{beat}s}}
body{{--sig:{f_col}}}
@keyframes neonpulse{{0%,100%{{opacity:.86;text-shadow:0 0 18px {f_col},0 0 60px rgba(255,0,60,.4)}}
  50%{{opacity:1;text-shadow:0 0 34px {f_col},0 0 110px rgba(255,0,60,.65)}}}}
.title{{animation:neonpulse 3.8s ease-in-out infinite}}
.vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
</style>
</head>
<body class="sense-{s_slug}">
<a class="skip" href="#nucleo" data-i18n="skip">Ir al núcleo</a>
<canvas id="stars" aria-hidden="true"></canvas>

<header class="topnav">
  <a class="brand" href="../index.html" aria-label="BELENTANI — inicio">
    <span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>GALAXIA {gid} / 50 · {esc(e_nom)}</small></span>
  </a>
  <span class="sig-badge" style="--sig:{f_col}">{esc(f_id)} · {esc(f_virt.upper())}</span>
  <nav aria-label="Las cinco firmas"><ul class="ndots">
      {firmas_ndots}
  </ul></nav>
</header>

<main class="stage" id="nucleo">
  <div class="eye-wrap">
    <div class="ring ring-b" aria-hidden="true"></div>
    <div class="ring" aria-hidden="true"></div>
    <div class="orbit" id="orbit" aria-hidden="true"></div>
    <div class="eye" role="img" aria-label="{esc(e_nom)} — Ojo de Judas"><div class="skin" aria-hidden="true"></div></div>
  </div>
  <section class="mirror" aria-labelledby="t">
    <p class="kicker">GALAXIA {gid} / 50 · {esc(f_nom)} · ESTACIÓN {ei + 1} / 10</p>
    <h1 class="title" id="t">{esc(e_nom)}</h1>
    <p class="espejo" id="espejo">{esc(e_frase)}</p>
    <p class="firma"><b>{esc(f_id)}</b> [{esc(f_nom)}] · {esc(f_virt)}<br>{esc(f_frase)}</p>
    <div class="progress" role="img" aria-label="Progreso del recorrido">
      <i></i>
    </div>
  </section>
</main>

<footer class="hbar">
  <nav class="waveC" aria-label="El Canto">
    <a class="hn" href="galaxia-{int(prev.split('-')[1][:2]):02d}.html" data-i18n="prev">ANTERIOR</a>
    <a class="hn core" href="index.html" data-i18n="core">NÚCLEO</a>
    <a class="hn" href="galaxia-{int(nxt.split('-')[1][:2]):02d}.html" data-i18n="next">SIGUIENTE</a>
    <svg class="wave" viewBox="0 0 200 26" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 13 Q12 0 25 13 T50 13 T75 13 T100 13 T125 13 T150 13 T175 13 T200 13"/>
    </svg>
    <span class="sense">
      <label for="sense" data-i18n="sense">SENTIDO</label>
      <input id="sense" type="range" min="0" max="4" step="1" value="{sentido_n - 1}">
      <output id="sense-out" for="sense">{s_slug.upper()}</output>
    </span>
  </nav>
</footer>

<script src="core/galaxia.js"></script>
<script>
mountGalaxia({{
  id:"{gid}", firma:"{esc(f_id)}", estacion:{ei},
  beat:{beat},
  prev:"galaxia-{int(prev.split('-')[1][:2]):02d}.html",
  next:"galaxia-{int(nxt.split('-')[1][:2]):02d}.html",
  espejo:{{
    es:{e_frase!r},
    pt:{TRAD[e_slug]['pt']!r},
    en:{TRAD[e_slug]['en']!r},
    ca:{TRAD[e_slug]['ca']!r}
  }},
  ui:{{
    pt:{{skip:"Ir para o núcleo",prev:"ANTERIOR",core:"NÚCLEO",next:"SEGUINTE",sense:"SENTIDO"}},
    es:{{skip:"Ir al núcleo",prev:"ANTERIOR",core:"NÚCLEO",next:"SIGUIENTE",sense:"SENTIDO"}},
    en:{{skip:"Skip to the core",prev:"PREVIOUS",core:"CORE",next:"NEXT",sense:"SENSE"}},
    ca:{{skip:"Ves al nucli",prev:"ANTERIOR",core:"NUCLI",next:"SEGÜENT",sense:"SENTIT"}}
  }},
  estaciones:{[[e[0], e[1]] for e in ESTACIONES]!r}
}});
</script>
</body>
</html>
"""


HUB_CSS = r"""
.hub{position:relative;z-index:5;max-width:1180px;margin:0 auto;padding:104px 20px 132px}
.hero{text-align:center;margin-bottom:26px}
.hero h1{font:900 clamp(38px,10vw,104px)/1 var(--fd);letter-spacing:.08em;
  animation:neonpulse 3.8s ease-in-out infinite}
.hero p{font:300 clamp(13px,1.8vw,17px)/1.7 var(--fu);color:var(--txt-dim);
  max-width:60ch;margin:14px auto 0}
.eq{font:700 11px/1 var(--fm);letter-spacing:3px;color:var(--gold);margin-top:12px}
.langbar{display:flex;justify-content:center;gap:8px;margin:18px 0 30px;flex-wrap:wrap}
.langbar a{font:700 10px/1 var(--fm);letter-spacing:2px;text-decoration:none;color:var(--txt-dim);
  border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:8px 13px}
.langbar a[aria-current="true"],.langbar a:hover{border-color:var(--sig);color:var(--sig)}
.matrix{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:7px}
.cell{display:block;text-decoration:none;color:inherit;padding:9px 7px;border-radius:10px;
  background:var(--glass);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  border:1px solid rgba(255,255,255,.12);transition:transform .22s,border-color .22s,box-shadow .22s}
.cell:hover{transform:translateY(-3px);border-color:var(--fg);box-shadow:0 0 22px rgba(255,0,60,.3)}
.cell b{display:block;font:900 12px/1 var(--fd);color:var(--fg)}
.cell i{display:block;font:400 8px/1.3 var(--fm);font-style:normal;color:var(--txt-ghost);
  margin-top:4px;letter-spacing:.5px}
.rowlab{display:flex;align-items:center;gap:10px;margin:22px 0 8px}
.rowlab b{font:700 11px/1 var(--fm);letter-spacing:2px;color:var(--fg)}
.rowlab span{font:400 10px/1 var(--fm);color:var(--txt-ghost)}
.legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:34px}
.legend div{padding:14px 16px;border-radius:12px;background:var(--glass);
  border:1px solid rgba(255,255,255,.1)}
.legend h3{font:700 11px/1 var(--fm);letter-spacing:2px;color:var(--sig);margin-bottom:7px}
.legend p{font:300 12px/1.6 var(--fu);color:var(--txt-dim)}
@media (max-width:900px){.matrix{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media (max-width:560px){.matrix{grid-template-columns:repeat(3,minmax(0,1fr))}}
"""

HUB_CSS2 = """
@keyframes neonpulse{0%,100%{opacity:.86;text-shadow:0 0 18px #ff003c,0 0 60px rgba(255,0,60,.4)}
  50%{opacity:1;text-shadow:0 0 34px #ff003c,0 0 110px rgba(255,0,60,.65)}}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
"""


def hub_bloques() -> str:
    """Filas (las 5 firmas) x columnas (las 10 estaciones) = 50 celdas."""
    bloques = []
    for fi, (f_slug, f_id, f_nom, f_col, f_virt, f_frase) in enumerate(FIRMAS):
        celdas = []
        for ei, (e_slug, e_nom, beat, e_frase, sn) in enumerate(ESTACIONES):
            num = (fi * 10 + ei) + 1
            celdas.append(
                f'<a class="cell" style="--fg:{f_col}" href="galaxia-{num:02d}.html" '
                f'title="{esc(f_id)} · {esc(e_nom)}"><b>{num:02d}</b>'
                f'<i>{esc(e_nom[:14])}</i></a>')
        bloques.append(
            f'<div class="rowlab"><b style="--fg:{f_col}">{esc(f_id)}</b>'
            f'<span>[{esc(f_nom)}] · {esc(f_virt)}</span></div>'
            f'<div class="matrix">{"".join(celdas)}</div>')
    return "\n  ".join(bloques)


HUB_PART1 = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BELENTANI // 50 GALAXIAS — 5 Firmas x 10 Estaciones</title>
<meta name="description" content="Mapa del universo BELENTANI: cinco firmas por diez estaciones. El Ojo de Judas, la Llave Dorada, el Canto y el espejo.">
<meta name="theme-color" content="#ff003c">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="https://belentani.es/galaxias/">
<link rel="alternate" hreflang="pt" href="index.html?lang=pt">
<link rel="alternate" hreflang="es" href="index.html?lang=es">
<link rel="alternate" hreflang="en" href="index.html?lang=en">
<link rel="alternate" hreflang="ca" href="index.html?lang=ca">
<link rel="alternate" hreflang="x-default" href="index.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="__FUENTES__" rel="stylesheet">
<link rel="stylesheet" href="core/galaxia.css">
<style>__HUBSTYLE__</style>
</head>
<body>
<a class="skip" href="#mapa" data-i18n="skip">Ir al mapa</a>
<canvas id="stars" aria-hidden="true"></canvas>

<header class="topnav">
  <a class="brand" href="../index.html" aria-label="BELENTANI - inicio">
    <span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>NUCLEO - 50 GALAXIAS</small></span>
  </a>
  <span class="sig-badge">5 FIRMAS x 10 ESTACIONES</span>
  <nav aria-label="Idioma"><ul class="ndots" style="margin:0">__LANG__</ul></nav>
</header>

<main class="hub" id="mapa">
  <div class="hero">
    <h1>BELENTANI</h1>
    <p>El universo no se navega. Se recorre. Cinco firmas, diez estaciones,
       cincuenta galaxias: cada una es una version distinta de la misma
       identidad despues de la caida.</p>
    <p class="eq">5 x 10 = 50 - PT &gt; ES &gt; EN &gt; CA</p>
  </div>
__BLOQUES__
"""

HUB_PART2 = """
  <section class="legend" aria-label="Que es cada elemento">
    <div><h3>EL OJO DE JUDAS</h3><p>El planeta del centro. No gira por
      decorar: <b>late</b> a la frecuencia de la estacion (3.2 s en EL ENTRE,
      0.9 s en LA CONSTELACION). Cuanto mas avanzas, mas rapido late.</p></div>
    <div><h3>LA LLAVE DORADA</h3><p>Los dos anillos: uno dorado y uno rojo
      punteado. Lo que Judas se llevo y lo que Pedro dejo que le robaran.
      Giran a 46 s y 72 s en sentidos opuestos.</p></div>
    <div><h3>LAS DIEZ ESTACIONES</h3><p>Los diez puntos de la orbita. La
      estacion en la que estas brilla en oro; las demas esperan su turno.</p></div>
    <div><h3>EL CANTO</h3><p>La onda del pie. LA VOZ ES EL OUTPUT: une
      anterior, nucleo y siguiente. Nunca se detiene.</p></div>
    <div><h3>EL ESPEJO</h3><p>La linea de cristal. Refleja la lectura canonica
      de (firma x estacion) y cambia de idioma sin cambiar de pagina.</p></div>
    <div><h3>EL SENTIDO</h3><p>Cinco paradas: NEON (rojo), MATRIX (verde),
      VENOM (purpura), VOID, ASCENDED (oro). El mismo mundo, mirado distinto.</p></div>
    <div><h3>LAS CINCO FIRMAS</h3><p>Los puntos de arriba a la derecha.
      PEDRO roca, MARCOS cronista, SANTOS antena, BELENTANI nucleo, HUMAN
      interfaz. Cambiar de firma es cambiar de mundo sin cambiar de estacion.</p></div>
    <div><h3>TECLADO</h3><p>Izq anterior - Der siguiente - ESC nucleo - 1 a 5
      sentido. El progreso se guarda en <code>localStorage omega_story</code>.</p></div>
  </section>
</main>

<footer class="hbar">
  <nav class="waveC" aria-label="El Canto">
    <a class="hn core" href="../index.html">OMEGA</a>
    <a class="hn" href="galaxia-01.html">EMPEZAR - EL ENTRE</a>
    <svg class="wave" viewBox="0 0 200 26" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 13 Q12 0 25 13 T50 13 T75 13 T100 13 T125 13 T150 13 T175 13 T200 13"/>
    </svg>
    <span class="sense">
      <label for="sense" data-i18n="sense">SENTIDO</label>
      <input id="sense" type="range" min="0" max="4" step="1" value="0">
      <output id="sense-out" for="sense">NEON</output>
    </span>
  </nav>
</footer>

<script src="core/galaxia.js"></script>
<script>
mountGalaxia({
  id:"00", firma:"BELENTANI // 50 GALAXIAS", estacion:0, beat:3.2,
  prev:null, next:"galaxia-01.html",
  espejo:{es:"El universo no se navega. Se recorre.",
    pt:"O universo nao se navega. Percorre-se.",
    en:"The universe is not browsed. It is walked.",
    ca:"L'univers no es navega. Es recorre."},
  ui:{pt:{skip:"Ir para o mapa",sense:"SENTIDO"},es:{skip:"Ir al mapa",sense:"SENTIDO"},
    en:{skip:"Skip to the map",sense:"SENSE"},ca:{skip:"Ves al mapa",sense:"SENTIT"}},
  estaciones:__ESTACIONES__
});
</script>
</body>
</html>
"""


def hub_html() -> str:
    """Ensambla el núcleo: mapa de 50 celdas + leyenda + El Canto."""
    lang = "".join(
        '<a class="nstar" style="--sig:#ff003c" href="index.html?lang=%s"%s'
        ' title="%s"><span class="vh">%s</span></a>'
        % (c, ' aria-current="true"' if c == "es" else "", c.upper(), c.upper())
        for c in IDIOMAS)
    return (HUB_PART1
            .replace("__FUENTES__", FUENTES)
            .replace("__HUBSTYLE__", HUB_CSS + HUB_CSS2)
            .replace("__LANG__", lang)
            .replace("__BLOQUES__", hub_bloques())
            + HUB_PART2.replace("__ESTACIONES__",
                                repr([[e[0], e[1]] for e in ESTACIONES])))


DOC = """# BELENTANI // 50 GALAXIAS — el universo navegable

> Generado por `tools/optimize-media/build-galaxy-pages.py`. Aditivo y
> reversible: no modifica `index.html`, `css/` ni `js/` existentes.

## Modelo

   5 Firmas (LORE-UNIFICADO §6) x 10 Estaciones = 50 galaxias

| # | Firma | Virtud | Color |
|---|---|---|---|
| 1 | PEDRO.SIG | permanencia | #FFD700 |
| 2 | MARCOS.SIG | memoria | #00FFFF |
| 3 | SANTOS.SIG | canal | #B026FF |
| 4 | BELENTANI.SIG | integracion | #FF003C |
| 5 | HUMAN.SIG | puente tangible | #F5F5F5 |

Estaciones: EL ENTRE, LA DEUDA, EL ROBO, EL CANTO, LA VICTORIA AMARGA,
LA MENTIRA COMPARTIDA, EL UMBRAL, LA SENAL, EL PORTAL, LA CONSTELACION.

`galaxia-NN.html` con `NN = firma*10 + estacion`. Fila = firma, columna =
estacion. Cada pagina es la MISMA estacion vista desde otra firma: el mundo
cambia de color y de lectura, la orbita no cambia.

## Cada elemento tiene funcion

| Elemento | Que es en el universo |
|---|---|
| topnav ndots | las 5 Firmas (cambiar firma = cambiar de mundo) |
| Ojo de Judas (planeta) | late a la frecuencia de la estacion (3.2 s -> 0.9 s) |
| anillos | la Llave Dorada robada (oro 46 s, rojo punteado 72 s inverso) |
| hero-orbit sparks | las 10 estaciones; la activa brilla en oro |
| hbar waveC | el Canto (LA VOZ ES EL OUTPUT): navegacion |
| espejo | linea canon de (firma x estacion) |
| slider sentido | NEON / MATRIX / VENOM / VOID / ASCENDED |

## Memoria e idioma

- `localStorage omega_story` guarda las estaciones recorridas (barra de progreso).
- `localStorage omega_sense` guarda la parada de sentido.
- `localStorage omega_lang` guarda el idioma.
- i18n en orden fijo **PT > ES > EN > CA** con `?lang=` + `hreflang` alternates.
- Teclado: izquierda anterior, derecha siguiente, ESC nucleo, 1-5 sentido.

## Accesibilidad

`skip-link`, `aria-current`, `aria-label`, foco visible, `prefers-reduced-motion`
detiene todas las animaciones, y sin JS la pagina sigue siendo legible (HTML
estatico + CSS).

## Regenerar

    python tools/optimize-media/build-galaxy-pages.py

## Ver

    python -m http.server 8099
    http://localhost:8099/galaxias/
"""


def main() -> int:
    CORE.mkdir(parents=True, exist_ok=True)
    (CORE / "galaxia.css").write_text(CORE_CSS, encoding="utf-8")
    (CORE / "galaxia.js").write_text(CORE_JS, encoding="utf-8")

    escritas = []
    for fi in range(len(FIRMAS)):
        for ei in range(len(ESTACIONES)):
            num = (fi * 10 + ei) + 1
            p = OUT / f"galaxia-{num:02d}.html"
            p.write_text(pagina_html(num, fi, ei), encoding="utf-8")
            escritas.append(p.name)

    (OUT / "index.html").write_text(hub_html(), encoding="utf-8")
    docs = REPO / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "GALAXIAS-UNIVERSO.md").write_text(DOC, encoding="utf-8")

    kb_css = len(CORE_CSS.encode()) / 1024
    kb_js = len(CORE_JS.encode()) / 1024
    print(f"core/galaxia.css {kb_css:.1f} KB · core/galaxia.js {kb_js:.1f} KB")
    print(f"escritas {len(escritas)} paginas + index.html (hub) + docs/GALAXIAS-UNIVERSO.md")
    print(f"DESTINO -> {OUT}")
    print("ABRIR -> http://localhost:8099/galaxias/")
    return 0


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())

# ─ Constructor de páginas ───────────────────────────────────────────────
def h1_de(nombre: str) -> str:
    """Reparte el nombre de estación en blanco + neón para el <h1>."""
    partes = nombre.split(" ", 1)
    if len(partes) == 2:
        return f"{partes[0]} <em>{partes[1]}</em>"
    return f"<em>{nombre}</em>"


def cabecera(n: int, f_index: int, e_index: int, firma: tuple,
             estacion: tuple, ndots: str) -> str:
    firma_key, firma_nombre, firma_titulo, firma_color, firma_cat, _ = firma
    est_slug, est_nombre, _, _, sentido = estacion
    sentido_nombre, _ = SENTIDOS[sentido]
    hreflang = "\n".join(
        f'  <link rel="alternate" hreflang="{i}" href="galaxia-{n:02d}.html?lang={i}">'
        for i in IDIOMAS)
    hreflang += (f'\n  <link rel="alternate" hreflang="x-default" '
                 f'href="galaxia-{n:02d}.html?lang=es">')
    desc = (f"{firma_nombre} [{firma_titulo}] × {est_nombre} — "
            f"galaxia {n:02d} de 50 del universo BELENTANI // JUDAS ERA.")
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <title>BELENTANI // GALAXIA {n:02d} — {firma_nombre} × {est_nombre}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="{firma_color}">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="galaxia-{n:02d}.html">
{hreflang}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FUENTES}">
  <link rel="stylesheet" href="core/galaxia.css">
</head>
<body class="sense-{sentido_nombre}" data-galaxia="{n:02d}" style="--sig:{firma_color}">
  <a class="skip" href="#nucleo">{UI['es']['skip']}</a>
  <canvas id="stars" aria-hidden="true"></canvas>

  <header class="topnav">
    <a class="brand" href="index.html">
      <span class="brand-eye" aria-hidden="true"></span>
      <span><b>BELENTANI</b><small>JUDAS ERA · OMEGA · GALAXIAS</small></span>
    </a>
    <ul class="ndots" aria-label="Las 5 Firmas">
{ndots}
    </ul>
    <span class="sig-badge">{firma_nombre} · {firma_titulo}</span>
  </header>
"""


def cuerpo(n: int, firma: tuple, estacion: tuple, frase_es: str,
           datos_js: str, previo: str, siguiente: str, sentido: int) -> str:
    _, firma_nombre, firma_titulo, _, firma_cat, firma_frase = firma
    est_slug, est_nombre, _, _, _ = estacion
    return f"""
  <main class="stage" id="nucleo">
    <div class="eye-wrap">
      <span class="ring" aria-hidden="true"></span>
      <span class="ring ring-b" aria-hidden="true"></span>
      <div class="eye" role="img" aria-label="Ojo de Judas, latiendo a la frecuencia de {est_nombre}">
        <span class="skin" aria-hidden="true"></span>
      </div>
      <div class="orbit" id="orbit" aria-hidden="true"></div>
    </div>

    <section class="mirror">
      <p class="kicker">GALAXIA {n:02d} / 50 · {firma_nombre} × {est_nombre}</p>
      <h1 class="title">{h1_de(est_nombre)}</h1>
      <p class="espejo" id="espejo">{frase_es}</p>
      <p class="firma">{firma_nombre} [{firma_titulo}] · <b>{firma_cat}</b> · {firma_frase}</p>
      <div class="progress" role="img" aria-label="Progreso de omega_story"><i></i></div>
    </section>
  </main>

  <footer class="hbar">
    <div class="waveC">
      <a class="hn" href="{previo}" title="Galaxia anterior (tecla izquierda)">&#8592; {UI['es']['prev']}</a>
      <a class="hn core" href="index.html" title="Núcleo de galaxias (ESC)">{UI['es']['core']}</a>
      <a class="hn" href="{siguiente}" title="Galaxia siguiente (tecla derecha)">{UI['es']['next']} &#8594;</a>
      <svg class="wave" viewBox="0 0 240 26" aria-hidden="true" preserveAspectRatio="none">
        <path d="M0 13 Q 30 {2 + sentido * 3} 60 13 T 120 13 T 180 13 T 240 13"/>
      </svg>
      <div class="sense">
        <label for="sense">{UI['es']['sense']}</label>
        <input id="sense" type="range" min="0" max="4" step="1" value="{sentido - 1}">
        <output id="sense-out">NEON</output>
      </div>
      <div class="sense" role="group" aria-label="Idioma">
        <button class="hn" type="button" data-lang="pt">PT</button>
        <button class="hn" type="button" data-lang="es">ES</button>
        <button class="hn" type="button" data-lang="en">EN</button>
        <button class="hn" type="button" data-lang="ca">CA</button>
      </div>
    </div>
  </footer>
"""


def pie(datos_js: str) -> str:
    """Arranque: monta la galaxia y aplica el idioma PT > ES > EN > CA."""
    return f"""
  <script src="core/galaxia.js"></script>
  <script>
    (function () {{
      var d = window.GALAXIA_DATA;
      if (window.mountGalaxia) window.mountGalaxia(d);

      /* Los tres anclas del hbar van siempre en orden: prev, core, next. */
      var nav = document.querySelectorAll('.waveC > a.hn');
      var elegido = null;
      try {{ elegido = localStorage.getItem('omega_lang'); }} catch (e) {{}}
      var desdeUrl = new URLSearchParams(location.search).get('lang');

      function pinta(idi) {{
        if (!d.espejos[idi]) idi = 'es';
        var espejo = document.getElementById('espejo');
        if (espejo) espejo.textContent = d.espejos[idi];
        document.documentElement.lang = idi;
        var u = d.ui[idi] || d.ui.es;
        var skip = document.querySelector('.skip');
        if (skip) skip.textContent = u.skip;
        if (nav.length === 3) {{
          nav[0].textContent = '\\u2190 ' + u.prev;
          nav[1].textContent = u.core;
          nav[2].textContent = u.next + ' \\u2192';
        }}
        var lbl = document.querySelector('label[for=sense]');
        if (lbl) lbl.textContent = u.sense;
        try {{ localStorage.setItem('omega_lang', idi); }} catch (e) {{}}
      }}

      Array.prototype.forEach.call(
        document.querySelectorAll('[data-lang]'),
        function (b) {{
          b.addEventListener('click', function () {{ pinta(this.getAttribute('data-lang')); }});
        }});
      pinta(desdeUrl || elegido || 'es');
    }})();
  </script>
</body>
</html>
"""


def build_html(n: int, f_index: int, e_index: int) -> str:
    firma = FIRMAS[f_index]
    estacion = ESTACIONES[e_index]
    est_slug, est_nombre, beat, frase_es, sentido = estacion
    previo, siguiente = vecinos(n)

    ndots = "\n".join(
        f'      <li><button class="nstar" type="button" '
        f'aria-current="{"true" if i == f_index else "false"}" '
        f'aria-label="{f[1]} {f[2]}" style="--sig:{f[3]}" '
        f'onclick="location.href=\'galaxia-{(i * 10 + e_index) + 1:02d}.html\'"></button></li>'
        for i, f in enumerate(FIRMAS))

    trad = TRAD[est_slug]
    payload = {
        "id": f"{n:02d}",
        "firma": f_index,
        "estacion": e_index,
        "beat": beat,
        "prev": previo,
        "next": siguiente,
        "espejos": {idi: trad.get(idi, frase_es) for idi in IDIOMAS},
        "ui": UI,
    }
    datos_js = json.dumps(payload, ensure_ascii=False)

    return (cabecera(n, f_index, e_index, firma, estacion, ndots)
            + cuerpo(n, firma, estacion, frase_es, datos_js, previo, siguiente, sentido)
            + pie(datos_js))


def build_hub() -> str:
    """Núcleo de galaxias: mapa de las 50 + las 5 Firmas."""
    bloques = []
    for f_index, firma in enumerate(FIRMAS):
        fk, fname, ftit, fcol, fcat, ffrase = firma
        filas = []
        for e_index, est in enumerate(ESTACIONES):
            n = f_index * 10 + e_index + 1
            filas.append(
                f'        <a class="cell" href="galaxia-{n:02d}.html" '
                f'style="--sig:{fcol}"><b>{n:02d}</b><span>{est[1]}</span>'
                f'<small>{est[2]}s</small></a>')
        bloques.append(f"""      <section class="firma-bloque" style="--sig:{fcol}">
        <h2><span class="brand-eye" aria-hidden="true"></span>{fname} <em>{ftit}</em></h2>
        <p class="firma-frase">{ffrase}</p>
        <div class="grid">
{chr(10).join(filas)}
        </div>
      </section>""")
    total = len(FIRMAS) * len(ESTACIONES)
    return (HUB_HEAD.format(total=total).replace("__FUENTES__", FUENTES)
            + chr(10).join(bloques) + HUB_TAIL)


HUB_HEAD = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <title>BELENTANI // GALAXIAS — las {total} galaxias del universo Judas Era</title>
  <meta name="description" content="Mapa completo de las {total} galaxias de BELENTANI // JUDAS ERA: 5 Firmas x 10 Estaciones. Cada elemento tiene funcion en el universo.">
  <meta name="theme-color" content="#ff003c">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="index.html">
  <link rel="alternate" hreflang="pt" href="index.html?lang=pt">
  <link rel="alternate" hreflang="es" href="index.html?lang=es">
  <link rel="alternate" hreflang="en" href="index.html?lang=en">
  <link rel="alternate" hreflang="ca" href="index.html?lang=ca">
  <link rel="alternate" hreflang="x-default" href="index.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="__FUENTES__">
  <link rel="stylesheet" href="core/galaxia.css">
  <link rel="stylesheet" href="core/hub.css">
</head>
<body class="hub-body">
  <a class="skip" href="#nucleo">Ir al nucleo</a>
  <canvas id="stars" aria-hidden="true"></canvas>

  <header class="topnav">
    <a class="brand" href="../index.html">
      <span class="brand-eye" aria-hidden="true"></span>
      <span><b>BELENTANI</b><small>JUDAS ERA - OMEGA - GALAXIAS</small></span>
    </a>
    <span class="sig-badge">{total} GALAXIAS - 5 FIRMAS x 10 ESTACIONES</span>
  </header>

  <main class="hub" id="nucleo">
    <h1 class="title">LAS <em>{total}</em> GALAXIAS</h1>
    <p class="espejo">Cinco firmas. Diez estaciones. Un solo hombre.
      Elige una firma para recorrer su mundo; las estaciones se repiten porque la
      historia no se repite: se confronta.</p>
    <p class="firma">Navegacion: flechas entre galaxias - ESC al nucleo - teclas 1-5 sentido.
      El progreso se guarda en <b>omega_story</b>.</p>
"""

HUB_TAIL = """
  </main>

  <script src="core/galaxia.js"></script>
  <script>
    (function () {
      var s = document.createElement('div');
      s.id = 'orbit';
      s.hidden = true;
      document.body.appendChild(s);
      if (window.mountGalaxia) window.mountGalaxia({ id: '00', firma: 0, estacion: 0, beat: 2.4 });
      s.remove();
      var idi = new URLSearchParams(location.search).get('lang');
      try { idi = idi || localStorage.getItem('omega_lang'); } catch (e) {}
      document.documentElement.lang = idi || 'es';
    })();
  </script>
</body>
</html>
"""

HUB_CSS = r"""/* Hub de galaxias: rejilla del mapa. Mismo canon, misma vara de medir. */
.hub-body{overflow:auto}
.hub{position:relative;z-index:5;max-width:1180px;margin:0 auto;padding:96px 20px 64px}
.firma-bloque{margin-top:38px;padding:20px 22px;border-radius:16px;
  background:var(--glass);backdrop-filter:blur(24px) saturate(160%);
  -webkit-backdrop-filter:blur(24px) saturate(160%);
  border:1px solid rgba(255,255,255,.13);
  box-shadow:0 1px 0 rgba(255,255,255,.18) inset,0 24px 70px rgba(0,0,0,.7);
  border-left:3px solid var(--sig)}
.firma-bloque h2{font:900 clamp(16px,2.6vw,24px)/1 var(--fd);letter-spacing:.06em;
  display:flex;align-items:center;gap:10px}
.firma-bloque h2 em{font-style:normal;color:var(--sig)}
.firma-frase{font:300 13px/1.6 var(--fu);color:var(--txt-dim);margin:8px 0 14px}
.grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(158px,1fr))}
.cell{display:flex;flex-direction:column;gap:6px;padding:13px 14px;border-radius:12px;
  text-decoration:none;color:var(--txt);background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.1);cursor:pointer;
  transition:transform .22s,border-color .22s,box-shadow .22s,background .22s}
.cell:hover{transform:translateY(-3px);border-color:var(--sig);
  box-shadow:0 0 26px rgba(255,0,60,.28);background:rgba(255,0,60,.09)}
.cell b{font:900 15px/1 var(--fd);color:var(--sig);letter-spacing:.08em}
.cell span{font:600 11px/1.35 var(--fu);letter-spacing:.04em}
.cell small{font:400 9px/1 var(--fm);color:var(--txt-ghost)}
@media (max-width:680px){.hub{padding:84px 14px 48px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(132px,1fr))}}
@media (prefers-reduced-motion:reduce){.cell{transition:none}}
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    CORE.mkdir(parents=True, exist_ok=True)
    (CORE / "galaxia.css").write_text(CORE_CSS, encoding="utf-8")
    (CORE / "galaxia.js").write_text(CORE_JS, encoding="utf-8")
    (CORE / "hub.css").write_text(HUB_CSS, encoding="utf-8")

    manifiesto = {"generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                  "firmas": [f[0] for f in FIRMAS],
                  "estaciones": [e[0] for e in ESTACIONES],
                  "idiomas": IDIOMAS, "paginas": []}

    n = 0
    for f_index in range(len(FIRMAS)):
        for e_index in range(len(ESTACIONES)):
            n += 1
            html = build_html(n, f_index, e_index)
            (OUT / f"galaxia-{n:02d}.html").write_text(html, encoding="utf-8")
            manifiesto["paginas"].append({
                "numero": n,
                "fichero": f"galaxia-{n:02d}.html",
                "firma": FIRMAS[f_index][0],
                "estacion": ESTACIONES[e_index][0],
                "sentido": SENTIDOS[ESTACIONES[e_index][4]][0],
            })

    (OUT / "index.html").write_text(build_hub(), encoding="utf-8")
    (OUT / "_manifest.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"galaxias generadas: {n} + hub")
    print(f"OK -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Nombres EN de las estaciones: el canon ES no se traduce, pero el hub
# muestra la lectura inglesa para que el universo sea legible fuera.
EN_EST = {
    "entre": "THE BETWEEN",
    "deuda": "THE DEBT",
    "robo": "THE THEFT",
    "canto": "THE SONG",
    "victoria": "THE BITTER VICTORY",
    "mentira": "THE SHARED LIE",
    "umbral": "THE THRESHOLD",
    "senal": "THE SIGNAL",
    "portal": "THE PORTAL",
    "constelacion": "THE CONSTELLATION",
}

CORE_CSS_C = r"""
/* El nombre parpadeante céntrico: el latido de la firma sobre el cristal. */
.title{animation:neonFlick 7s infinite}
@keyframes neonFlick{
  0%,17%,19.5%,49%,51.5%,100%{opacity:1}
  18.2%,50.4%{opacity:.52}
}
/* El Ojo de Judas queda centrado detrás del cristal del espejo. */
.eye-wrap{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
@media (prefers-reduced-motion:reduce){.title{animation:none}}
"""

CORE_CSS = CORE_CSS_A + CORE_CSS_B + CORE_CSS_C

HUB_CSS = r"""
/* ── HUB: las 50 galaxias (5 firmas x 10 estaciones) ── */
.hub{position:relative;z-index:5;width:min(1180px,94vw);margin:0 auto;padding:92px 0 132px}
.eyebrow{font:400 10px/1 var(--fm);letter-spacing:6px;color:var(--sig)}
.hub h1{font:900 clamp(34px,8vw,86px)/.98 var(--fd);letter-spacing:.04em;margin:10px 0 6px;
  text-shadow:0 0 30px rgba(255,0,60,.7),0 0 100px rgba(255,0,60,.3)}
.hub h1 em{font-style:normal;color:var(--sig)}
.hub p.lead{font:300 15px/1.8 var(--fu);color:var(--txt-dim);max-width:66ch;margin-bottom:22px}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 26px}
.fbtn{font:700 10px/1 var(--fm);letter-spacing:2px;color:var(--txt-dim);cursor:pointer;
  border:1px solid rgba(255,255,255,.18);background:transparent;border-radius:999px;padding:9px 14px;
  transition:border-color .25s,color .25s,background .25s}
.fbtn:hover{border-color:var(--sig);color:#fff}
.fbtn[aria-pressed="true"]{border-color:var(--sig);color:var(--sig);background:rgba(255,0,60,.12)}
.tiles{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(232px,1fr))}
.tile{position:relative;display:flex;flex-direction:column;gap:8px;padding:15px 16px;border-radius:15px;
  text-decoration:none;color:inherit;border:1px solid rgba(255,255,255,.12);
  background:var(--glass);backdrop-filter:blur(20px) saturate(160%);
  -webkit-backdrop-filter:blur(20px) saturate(160%);
  box-shadow:0 1px 0 rgba(255,255,255,.16) inset,0 18px 44px rgba(0,0,0,.6);
  transition:transform .28s,border-color .28s,box-shadow .28s}
.tile:hover,.tile:focus-visible{transform:translateY(-3px);border-color:var(--tile-color,var(--sig));
  box-shadow:0 1px 0 rgba(255,255,255,.22) inset,0 26px 60px rgba(0,0,0,.72),0 0 40px var(--tile-color,var(--sig))}
.tile .num{font:900 26px/1 var(--fd);letter-spacing:.04em;color:var(--tile-color,var(--sig))}
.tile .nom{font:700 12px/1.35 var(--fu);letter-spacing:.06em}
.tile .sig{font:400 9px/1 var(--fm);letter-spacing:1.6px;color:var(--txt-ghost)}
.tile .dot{position:absolute;right:13px;top:13px;width:9px;height:9px;border-radius:50%;
  background:var(--tile-color,var(--sig));box-shadow:0 0 12px var(--tile-color,var(--sig))}
.tile[hidden]{display:none}
@media (max-width:680px){.hub{padding:84px 0 168px}.tiles{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}
"""

# ── Plantilla de página. Se usa {{CLAVE}} porque el CSS/JS tiene llaves. ──
PAGE_TPL = """<!DOCTYPE html>
<html lang="{{LANG}}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<meta name="theme-color" content="{{THEME}}">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{{CANON}}">
<link rel="manifest" href="../manifest.json">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23ff003c'/><text x='50' y='70' font-size='58' text-anchor='middle' fill='%23050505' font-family='Arial'>B</text></svg>">
<link rel="alternate" hreflang="pt" href="{{CANON}}?lang=pt">
<link rel="alternate" hreflang="es" href="{{CANON}}?lang=es">
<link rel="alternate" hreflang="en" href="{{CANON}}?lang=en">
<link rel="alternate" hreflang="ca" href="{{CANON}}?lang=ca">
<link rel="alternate" hreflang="x-default" href="{{CANON}}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{{TITLE}}">
<meta property="og:description" content="{{DESC}}">
<meta property="og:site_name" content="BELENTANI // JUDAS ERA">
<meta property="og:image" content="https://belentani.es/assets/images/og-cover.jpg">
<meta property="og:url" content="{{CANON}}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{{LD}}</script>
<style>{{CSS}}</style>
</head>
<body class="sense-{{SENSE}}">
<a class="skip" href="#nucleo">{{T_SKIP}}</a>
<canvas id="stars" aria-hidden="true"></canvas>

<header class="topnav">
  <a class="brand" href="index.html" aria-label="BELENTANI hub">
    <span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>GALAXIAS · {{N}}/50</small></span>
  </a>
  <ul class="ndots" role="list" aria-label="{{T_FIRMA}}">
    {{NDOTS}}
  </ul>
  <span class="sig-badge">{{FIRMA}} · {{ESTACION}}</span>
</header>

<main class="stage" id="nucleo">
  <div class="eye-wrap" aria-hidden="true">
    <span class="eye"></span>
    <span class="skin"></span>
    <span class="ring"></span>
    <span class="ring ring-b"></span>
    <span class="orbit" id="orbit"></span>
  </div>
  <article class="mirror">
    <p class="kicker">GALAXIA {{N}} / 50 · {{FIRMA_FUNC}}</p>
    <h1 class="title">BELENTANI <em>{{ESTACION}}</em></h1>
    <p class="espejo" id="espejo">{{ESPEJO}}</p>
    <p class="firma"><b>{{FIRMA}}</b> [{{FIRMA_TITULO}}] — {{FIRMA_FRASE}}</p>
    <div class="progress" role="progressbar" aria-label="{{T_PROGRESO}}" aria-valuemin="0" aria-valuemax="50">
      <i></i>
    </div>
  </article>
</main>

<nav class="hbar" aria-label="{{T_NAV}}">
  <div class="waveC">
    <a class="hn" href="{{PREV}}">← {{T_PREV}}</a>
    <svg class="wave" viewBox="0 0 800 26" preserveAspectRatio="none" aria-hidden="true">
      <path d="{{WAVE}}"/>
    </svg>
    <a class="hn core" href="index.html">◆ {{T_CORE}}</a>
    <a class="hn" href="{{NEXT}}">{{T_NEXT}} →</a>
    <span class="sense">
      <label for="sense">{{T_SENSE}}</label>
      <input id="sense" type="range" min="0" max="4" step="1" value="{{SENSE_I}}">
      <output id="sense-out" for="sense">{{SENSE}}</output>
    </span>
  </div>
</nav>

<script>{{JS}}</script>
<script>
(function(){
  var T = {{TRAD}};
  var U = {{UILABEL}};
  var ORDER = ["pt","es","en","ca"];
  function pick(){
    var q = (location.search.match(/[?&]lang=(pt|es|en|ca)/) || [])[1];
    if (q) return q;
    var n = (navigator.language || "es").slice(0,2).toLowerCase();
    return ORDER.indexOf(n) === -1 ? "es" : n;
  }
  function paint(l){
    var t = T[l] || T.es, u = U[l] || U.es;
    document.documentElement.lang = l;
    document.getElementById("espejo").textContent = t;
    var el;
    el = document.querySelector(".skip"); if (el) el.textContent = u.skip;
    el = document.querySelector(".hn"); if (el) el.textContent = "← " + u.prev;
    el = document.querySelector(".hn.core"); if (el) el.textContent = "◆ " + u.core;
    var links = document.querySelectorAll(".hn");
    if (links.length > 2) links[2].textContent = u.next + " →";
    el = document.querySelector(".sense label"); if (el) el.textContent = u.sense;
    el = document.querySelector(".hbar"); if (el) el.setAttribute("aria-label", u.nav);
    el = document.querySelector(".progress"); if (el) el.setAttribute("aria-label", u.progreso);
    el = document.querySelector(".ndots"); if (el) el.setAttribute("aria-label", u.firma);
  }
  paint(pick());
  window.GALAXIA_LANG = pick();
})();
</script>
</body>
</html>
"""


def onda(seed: int) -> str:
    """Path SVG del Canto: cada estación canta en una frecuencia distinta."""
    pts = []
    for x in range(0, 801, 40):
        y = 13 + math.sin((x + seed * 53) / 58.0) * 8.5 + math.sin(x / 21.0 + seed) * 2.6
        pts.append(f"{x},{y:.1f}")
    return "M" + " L".join(pts)


def build_page(fi: int, ei: int) -> str:
    slug_f, firma_nom, firma_titulo, firma_color, firma_func, firma_frase = FIRMAS[fi]
    slug_e, est_nom, beat, frase, sentido = ESTACIONES[ei]
    n = fi * 10 + ei + 1
    prev, nxt = vecinos(n)
    sense_nom, sense_color = SENTIDOS[sentido]

    # Los 5 ndots: misma estación, otra firma. Cambiar firma = otro mundo.
    ndots = []
    for k in range(5):
        dest = f"galaxia-{(k * 10 + ei) + 1:02d}.html"
        activo = "true" if k == fi else "false"
        ndots.append(
            f'<li><a class="nstar" href="{dest}" aria-current="{activo}" '
            f'style="border-color:{FIRMAS[k][3]};'
            + (f'background:{FIRMAS[k][3]};box-shadow:0 0 16px {FIRMAS[k][3]}' if k == fi else '')
            + f'" title="{FIRMAS[k][1]} — {FIRMAS[k][2]}" aria-label="{FIRMAS[k][1]}"></a></li>'
        )

    lang_es = UI["es"]
    canon = f"https://belentani.es/galaxias/galaxia-{n:02d}.html"
    title = f"BELENTANI // {firma_nom} · {est_nom} — GALAXIA {n:02d}/50"
    desc = f"{frase} — {firma_nom} [{firma_titulo}], estación {est_nom} " \
           f"({EN_EST[slug_e]}) del universo BELENTANI // JUDAS ERA."
    ld = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": f"{firma_nom} · {est_nom}",
        "alternateName": EN_EST[slug_e],
        "description": desc,
        "inLanguage": IDIOMAS,
        "url": canon,
        "isPartOf": {
            "@type": "CreativeWorkSeries",
            "name": "BELENTANI // GALAXIAS",
            "numberOfItems": 50,
        },
        "creator": {"@type": "MusicArtist", "name": "Belentani",
                    "url": "https://belentani.es/"},
        "position": n,
    }
    trad = {"es": frase}
    trad.update({k: v for k, v in TRAD[slug_e].items()})

    repl = {
        "{{LANG}}": "es",
        "{{TITLE}}": title,
        "{{DESC}}": desc,
        "{{THEME}}": sense_color,
        "{{CANON}}": canon,
        "{{LD}}": json.dumps(ld, ensure_ascii=False),
        "{{CSS}}": CORE_CSS,
        "{{JS}}": CORE_JS,
        "{{SENSE}}": sense_nom,
        "{{SENSE_I}}": str(sentido - 1),
        "{{N}}": f"{n:02d}",
        "{{NDOTS}}": "".join(ndots),
        "{{FIRMA}}": firma_nom,
        "{{FIRMA_TITULO}}": firma_titulo,
        "{{FIRMA_FUNC}}": firma_func.upper(),
        "{{FIRMA_FRASE}}": firma_frase,
        "{{ESTACION}}": est_nom,
        "{{ESPEJO}}": frase,
        "{{PREV}}": prev,
        "{{NEXT}}": nxt,
        "{{WAVE}}": onda(ei + 1),
        "{{T_SKIP}}": lang_es["skip"],
        "{{T_PREV}}": lang_es["prev"],
        "{{T_CORE}}": lang_es["core"],
        "{{T_NEXT}}": lang_es["next"],
        "{{T_SENSE}}": lang_es["sense"],
        "{{T_NAV}}": lang_es["nav"],
        "{{T_PROGRESO}}": lang_es["progreso"],
        "{{T_FIRMA}}": lang_es["firma"],
        "{{TRAD}}": json.dumps(trad, ensure_ascii=False),
        "{{UILABEL}}": json.dumps(UI, ensure_ascii=False),
    }
    html = PAGE_TPL
    for k, v in repl.items():
        html = html.replace(k, v)
    cfg = json.dumps({
        "id": f"galaxia-{n:02d}",
        "firma": slug_f,
        "estacion": ei,
        "beat": beat,
        "prev": prev,
        "next": nxt,
        "estaciones": [[e[0], e[1]] for e in ESTACIONES],
    }, ensure_ascii=False)
    html = html.replace("</body>", f"<script>mountGalaxia({cfg});</script>\n</body>")
    return html


HUB_TPL = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>BELENTANI // GALAXIAS — 50 mundos (5 Firmas x 10 Estaciones)</title>
<meta name="description" content="Las 50 galaxias del universo BELENTANI // JUDAS ERA: 5 Firmas (PEDRO, MARCOS, SANTOS, BELENTANI, HUMAN) por 10 Estaciones (EL ENTRE, LA DEUDA, EL ROBO...).">
<meta name="theme-color" content="#ff003c">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="https://belentani.es/galaxias/index.html">
<link rel="manifest" href="../manifest.json">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23ff003c'/><text x='50' y='70' font-size='58' text-anchor='middle' fill='%23050505' font-family='Arial'>B</text></svg>">
<link rel="alternate" hreflang="pt" href="https://belentani.es/galaxias/?lang=pt">
<link rel="alternate" hreflang="es" href="https://belentani.es/galaxias/?lang=es">
<link rel="alternate" hreflang="en" href="https://belentani.es/galaxias/?lang=en">
<link rel="alternate" hreflang="ca" href="https://belentani.es/galaxias/?lang=ca">
<link rel="alternate" hreflang="x-default" href="https://belentani.es/galaxias/">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:title" content="BELENTANI // GALAXIAS — 50 mundos">
<meta property="og:description" content="5 Firmas x 10 Estaciones = 50 galaxias. El universo Belentani, navegable.">
<meta property="og:image" content="https://belentani.es/assets/images/og-cover.jpg">
<script type="application/ld+json">{{LD}}</script>
<style>{{CSS}}</style>
</head>
<body class="sense-neon">
<a class="skip" href="#hub">Ir al hub</a>
<canvas id="stars" aria-hidden="true"></canvas>

<header class="topnav">
  <a class="brand" href="../index.html" aria-label="BELENTANI núcleo">
    <span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>GALAXIAS · HUB</small></span>
  </a>
  <span class="sig-badge">5 FIRMAS × 10 ESTACIONES = 50</span>
</header>

<main class="hub" id="hub">
  <p class="eyebrow">UNIVERSO NAVEGABLE</p>
  <h1>50 <em>GALAXIAS</em></h1>
  <p class="lead">Cinco firmas —PEDRO.SIG, MARCOS.SIG, SANTOS.SIG, BELENTANI.SIG, HUMAN.SIG—
  cruzadas con diez estaciones del relato: EL ENTRE, LA DEUDA, EL ROBO, EL CANTO,
  LA VICTORIA AMARGA, LA MENTIRA COMPARTIDA, EL UMBRAL, LA SEÑAL, EL PORTAL y LA
  CONSTELACIÓN. Cada página es un mundo: el mismo Ojo de Judas, distinta firma,
  distinta frecuencia.</p>
  <div class="filters" role="group" aria-label="Filtrar por firma">
    <button class="fbtn" type="button" data-firma="all" aria-pressed="true">TODAS · 50</button>
    {{FILTROS}}
  </div>
  <section class="tiles" id="tiles" aria-label="Las 50 galaxias">
    {{TILES}}
  </section>
</main>

<nav class="hbar" aria-label="Salida del universo">
  <div class="waveC">
    <a class="hn" href="../index.html">← NÚCLEO OMEGA</a>
    <svg class="wave" viewBox="0 0 800 26" preserveAspectRatio="none" aria-hidden="true">
      <path d="{{WAVE}}"/>
    </svg>
    <a class="hn" href="../ecosistema.html">ECOSISTEMA</a>
    <a class="hn core" href="galaxia-01.html">◆ GALAXIA 01</a>
  </div>
</nav>

<script>{{JS}}</script>
<script>
(function(){
  omegaStarfield(document.getElementById('stars'));
  var btns = document.querySelectorAll('.fbtn');
  var tiles = document.querySelectorAll('.tile');
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', function(){
      var want = this.getAttribute('data-firma');
      for (var j = 0; j < btns.length; j++) btns[j].setAttribute('aria-pressed', String(btns[j] === this));
      for (var k = 0; k < tiles.length; k++) {
        var t = tiles[k];
        var show = want === 'all' || t.getAttribute('data-firma') === want;
        if (show) t.removeAttribute('hidden'); else t.setAttribute('hidden', 'hidden');
      }
    });
  }
})();
</script>
</body>
</html>
"""


def build_hub() -> str:
    filtros, tiles = [], []
    for slug, nom, _titulo, color, _func, _frase in FIRMAS:
        filtros.append(
            f'<button class="fbtn" type="button" data-firma="{slug}" aria-pressed="false" '
            f'style="border-color:{color};color:{color}">{nom} · 10</button>')
    for fi in range(5):
        slug_f, firma_nom, _ft, firma_color, _fn, _fr = FIRMAS[fi]
        for ei in range(10):
            slug_e, est_nom, _beat, _frase, _sent = ESTACIONES[ei]
            n = fi * 10 + ei + 1
            tiles.append(
                f'<a class="tile" href="galaxia-{n:02d}.html" data-firma="{slug_f}" '
                f'style="--tile-color:{firma_color}">'
                f'<span class="dot" aria-hidden="true"></span>'
                f'<span class="num">{n:02d}</span>'
                f'<span class="nom">{est_nom}</span>'
                f'<span class="sig">{firma_nom} · {EN_EST[slug_e]}</span></a>')

    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "BELENTANI // GALAXIAS",
        "description": "50 galaxias: 5 Firmas por 10 Estaciones del universo Belentani.",
        "url": "https://belentani.es/galaxias/",
        "inLanguage": IDIOMAS,
        "isPartOf": {"@type": "WebSite", "name": "BELENTANI // JUDAS ERA",
                     "url": "https://belentani.es/"},
        "hasPart": [
            {"@type": "CreativeWork",
             "name": f"{FIRMAS[f][1]} · {ESTACIONES[e][1]}",
             "url": f"https://belentani.es/galaxias/galaxia-{f * 10 + e + 1:02d}.html"}
            for f in range(5) for e in range(10)
        ],
        "numberOfItems": 50,
    }
    html = HUB_TPL
    for k, v in {
        "{{CSS}}": CORE_CSS + HUB_CSS,
        "{{JS}}": CORE_JS,
        "{{LD}}": json.dumps(ld, ensure_ascii=False),
        "{{FILTROS}}": "".join(filtros),
        "{{TILES}}": "".join(tiles),
        "{{WAVE}}": onda(0),
    }.items():
        html = html.replace(k, v)
    return html


def write_all() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    CORE.mkdir(parents=True, exist_ok=True)
    (CORE / "omega-galaxias.css").write_text(CORE_CSS + HUB_CSS, encoding="utf-8")
    (CORE / "omega-galaxias.js").write_text(CORE_JS, encoding="utf-8")

    escritos = 0
    for fi in range(5):
        for ei in range(10):
            n = fi * 10 + ei + 1
            (OUT / f"galaxia-{n:02d}.html").write_text(build_page(fi, ei), encoding="utf-8")
            escritos += 1
    (OUT / "index.html").write_text(build_hub(), encoding="utf-8")

    indice = {
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "modelo": "5 firmas x 10 estaciones",
        "total": escritos,
        "firmas": [
            {"slug": s, "sig": nom, "titulo": tit, "color": c, "funcion": fn}
            for s, nom, tit, c, fn, _ in FIRMAS
        ],
        "estaciones": [
            {"slug": s, "nombre": n, "en": EN_EST[s], "beat_s": b, "sentido": sd}
            for s, n, b, _f, sd in ESTACIONES
        ],
        "paginas": [
            {"n": f * 10 + e + 1,
             "id": f"galaxia-{f * 10 + e + 1:02d}",
             "firma": FIRMAS[f][1],
             "estacion": ESTACIONES[e][1],
             "en": EN_EST[ESTACIONES[e][0]],
             "beat_s": ESTACIONES[e][2],
             "archivo": f"galaxias/galaxia-{f * 10 + e + 1:02d}.html"}
            for f in range(5) for e in range(10)
        ],
    }
    (OUT / "galaxias.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2), encoding="utf-8")
    return indice


def main() -> int:
    indice = write_all()
    print(f"OK -> {indice['total']} galaxias + hub en {OUT}")
    print(f"OK -> {OUT / 'galaxias.json'}")
    print(f"OK -> {CORE / 'omega-galaxias.css'} / .js")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# ─ Vectores: 3 estímulos por estación (regla anti-emoji del canon). ─────
# Guiones con la energía del lore, siempre los mismos por estación, para
# que las 5 firmas se lean como 5 miradas al mismo instante.
VECTORES = {
    "entre": ["Abre el pecho y respira una vez.",
              "Di tu nombre real, sin apellido.",
              "No te defendas: concéntrate."],
    "deuda": ["Baja la cabeza ante el que te acompaña.",
              "Paga sin contar lo que pusiste.",
              "Deja que te vean entregado."],
    "robo": ["Toma lo que no te pertenece, de noche.",
             "Guarda la vergüenza antes que el metal.",
             "No mires atrás al salir."],
    "canto": ["Siéntate. Después del robo, canta.",
              "Alarga la nota hasta que duela.",
              "Canta para el que te robó."],
    "victoria": ["Sostén la llave y no la defiendas.",
                 "Nombra lo que nadie te puede quitar.",
                 "Deja que la victoria te sepa amarga."],
    "mentira": ["Mira el metal y admite que mentiste.",
                "Suelta lo que nunca valió.",
                "Guarda el pacto, no el objeto."],
    "umbral": ["Deja la puerta abierta al que te robó.",
               "Cruza sin pedir permiso.",
               "Elige el cuerpo que vas a habitar."],
    "senal": ["Ajusta la antena hasta oír el ruido.",
              "Fragmenta la señal y vuelve a unirla.",
              "Sigue el pulso rojo sobre el negro."],
    "portal": ["Empuja el aire: se abre.",
               "No vuelvas por donde entraste.",
               "Conviértete en otro aquí."],
    "constelacion": ["Levanta la vista hacia las cinco luces.",
                     "Marca tu lugar entre las firmas.",
                     "Escribe el capítulo que falta."],
}

# ─ Plantilla de página ────────────────────────────────────────────────
ICONO = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
         "<rect width='100' height='100' rx='22' fill='%23FF003C'/>"
         "<text x='50' y='72' font-size='60' text-anchor='middle' fill='%23070707'"
         " font-family='Arial' font-weight='bold'>B</text></svg>")

WAVE = "M0 13 C 10 2,18 24,28 13 S 46 2,56 13 S 74 24,84 13 S 108 4,120 13"


def build_html(n, f, e, lang="es"):
    """HTML de la galaxia n (1..50) para la firma f y la estación e."""
    fid, sig, rol, color, funcion, lema = FIRMAS[f]
    slug, nom, beat, frase, sentido = ESTACIONES[e]
    sentido_nombre = SENTIDOS[sentido][0]
    prev, nxt = vecinos(n)
    trozos = nom.split(" ", 1)
    a, b = trozos[0], (trozos[1] if len(trozos) > 1 else "")
    titulo = f"{a} <em>{b}</em>" if b else f"<em>{a}</em>"
    trad = TRAD.get(slug, {})
    espejo = trad.get(lang) or frase
    desc = espejo.replace('"', "&quot;")

    lang_links = "".join(
        f'<link rel="alternate" hreflang="{c}" href="galaxia-{n:02d}.html?lang={c}">\n'
        for c in IDIOMAS)
    chips = "".join(
        '<a class="hn%s" href="galaxia-%02d.html?lang=%s" hreflang="%s">%s</a>'
        % (" core" if c == lang else "", n, c, c, c.upper()) for c in IDIOMAS)
    dots = "".join(
        '<li><a class="nstar" href="../index.html#%s" style="--sig:%s" title="%s [%s]" '
        'aria-label="%s %s"%s></a></li>'
        % (F[0], F[3], F[1], F[2], F[1], F[2], ' aria-current="true"' if i == f else "")
        for i, F in enumerate(FIRMAS))
    vectores = "".join(f"<li>{v}</li>" for v in VECTORES[slug])
    cfg = json.dumps({"id": "%02d" % n, "n": n, "firma": fid, "estacion": e,
                      "slug": slug, "beat": beat},
                     ensure_ascii=False, separators=(",", ":"))
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "CreativeWork",
        "name": f"GALAXIA {n:02d} · {nom} · {sig}",
        "isPartOf": {"@type": "CreativeWorkSeries", "name": "BELENTANI // JUDAS ERA"},
        "inLanguage": IDIOMAS, "genre": "digital experience",
        "creator": {"@type": "MusicArtist", "name": "Belentani"},
        "abstract": espejo,
    }, ensure_ascii=False, separators=(",", ":"))

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-galaxia="{n:02d}" data-firma="{fid}" data-estacion="{e}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>GALAXIA {n:02d} · {nom} · {sig} — BELENTANI // JUDAS ERA</title>
<meta name="description" content="{desc}">
<meta name="author" content="Belentani">
<meta name="theme-color" content="#050505">
<link rel="canonical" href="https://belentani.es/galaxias/galaxia-{n:02d}.html">
{lang_links}<link rel="alternate" hreflang="x-default" href="galaxia-{n:02d}.html">
<link rel="icon" href="{ICONO}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FUENTES}">
<link rel="stylesheet" href="core/galaxia-core.css">
<meta property="og:type" content="website">
<meta property="og:title" content="GALAXIA {n:02d} · {nom} · {sig}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://belentani.es/galaxias/galaxia-{n:02d}.html">
<meta property="og:image" content="../assets/images/og-cover.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ld}</script>
</head>
<body class="sense-neon">
<a class="skip" id="l-skip" href="#mirror">Ir al núcleo</a>
<canvas id="stars" aria-hidden="true"></canvas>

<header class="topnav">
  <a class="brand" href="../index.html">
    <span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>JUDAS ERA // GALAXIA {n:02d}</small></span>
  </a>
  <span class="sig-badge">{sig} [{rol}]</span>
  <ul class="ndots" aria-label="Las 5 Firmas">{dots}</ul>
</header>

<main class="stage" id="main">
  <div class="eye-wrap">
    <div class="orbit" id="orbit" aria-hidden="true"></div>
    <div class="ring" aria-hidden="true"></div>
    <div class="ring ring-b" aria-hidden="true"></div>
    <div class="eye" role="img" aria-label="Ojo de Judas: planeta de la firma {sig}"><span class="skin"></span></div>
  </div>
  <section class="mirror" id="mirror" aria-labelledby="t">
    <p class="kicker">GALAXIA {n:02d} // ESTACIÓN {e + 1:02d} // {sentido_nombre.upper()}</p>
    <h1 class="title" id="t">{titulo}</h1>
    <p class="espejo" id="espejo">{espejo}</p>
    <p class="firma"><span id="l-sig">FIRMA</span> <b>{sig}</b> · {rol} · {funcion}</p>
    <ul class="vec">{vectores}</ul>
    <div class="progress" role="img" aria-label="Estaciones recorridas"><i></i></div>
  </section>
</main>

<footer class="hbar">
  <div class="waveC">
    <a class="hn" href="{prev}" rel="prev"><span aria-hidden="true">← </span><span id="l-prev">ANTERIOR</span></a>
    <a class="hn core" href="../index.html" id="l-core">NÚCLEO</a>
    <a class="hn" href="{nxt}" rel="next"><span id="l-next">SIGUIENTE</span><span aria-hidden="true"> →</span></a>
    <svg class="wave" viewBox="0 0 120 26" aria-hidden="true"><path d="{WAVE}"/></svg>
    <div class="sense">
      <label for="sense" id="l-sense">SENTIDO</label>
      <input id="sense" type="range" min="0" max="4" step="1" value="0">
      <output id="sense-out" for="sense">NEON</output>
    </div>
    <div class="langs" role="group" aria-label="Idioma">{chips}</div>
  </div>
</footer>

<script src="core/galaxia-i18n.js" defer></script>
<script src="core/galaxia-core.js" defer></script>
<script defer>if(window.mountGalaxia){{mountGalaxia({cfg});}}else{{document.body.classList.add('no-js');}}</script>
</body>
"</html>
"""

# ─ i18n compartido: un solo fichero cacheado para las 50 páginas. ─────
I18N_JS = ("/* BELENTANI // GALAXIAS — i18n. Orden fijo PT > ES > EN > CA. */\n"
           "window.GALAXIA_I18N = "
           + json.dumps({"order": IDIOMAS, "ui": UI, "trad": TRAD,
                         "estaciones": ESTACIONES},
                        ensure_ascii=False, separators=(",", ":"))
           + ";\n")


def build_hub():
    """Portada del cúmulo: las 50 galaxias ordenadas por firma."""
    cols = []
    for f, F in enumerate(FIRMAS):
        links = []
        for e, E in enumerate(ESTACIONES):
            nn = f * 10 + e + 1
            links.append('<li><a href="galaxia-%02d.html"><b>%02d</b> %s</a></li>'
                         % (nn, e + 1, E[1]))
        cols.append(
            '<article class="col" style="--sig:%s"><h2>%s</h2>'
            '<p class="rol">%s · %s</p><p class="lema">“%s”</p><ul>%s</ul></article>'
            % (F[3], F[1], F[2], F[4], F[5], "".join(links)))
    sentido = " ".join('<span style="--sig:%s" class="st">%s</span>' % (c, nm.upper())
                       for nm, c in SENTIDOS.values())
    dots_hub = "".join('<li><a class="nstar" href="#%s" style="--sig:%s" title="%s" '
                       'aria-label="%s"></a></li>' % (F[0], F[3], F[1], F[1]) for F in FIRMAS)
    chips_hub = "".join('<a class="hn" href="?lang=%s" hreflang="%s">%s</a>'
                        % (c, c, c.upper()) for c in IDIOMAS)
    return f"""<!DOCTYPE html>
<html lang="es" data-galaxia="hub">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>CÚMULO BELENTANI — 50 GALAXIAS // JUDAS ERA</title>
<meta name="description" content="Cincuenta galaxias unificadas: 5 Firmas por 10 Estaciones del canon BELENTANI // JUDAS ERA.">
<meta name="theme-color" content="#050505">
<link rel="canonical" href="https://belentani.es/galaxias/">
<link rel="alternate" hreflang="pt" href="?lang=pt">
<link rel="alternate" hreflang="es" href="?lang=es">
<link rel="alternate" hreflang="en" href="?lang=en">
<link rel="alternate" hreflang="ca" href="?lang=ca">
<link rel="alternate" hreflang="x-default" href="./">
<link rel="icon" href="{ICONO}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FUENTES}">
<link rel="stylesheet" href="core/galaxia-core.css">
<style>
body{{overflow:auto}}
.hub{{position:relative;z-index:5;max-width:1240px;margin:0 auto;padding:112px 20px 132px}}
.lead{{font:300 clamp(14px,2vw,18px)/1.8 var(--fu);color:var(--txt-dim);max-width:62ch;margin:14px 0 26px}}
.grid{{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}}
.col{{border-radius:16px;padding:18px;background:var(--glass);border:1px solid rgba(255,255,255,.13);
  backdrop-filter:blur(24px) saturate(160%);-webkit-backdrop-filter:blur(24px) saturate(160%);
  box-shadow:0 24px 70px rgba(0,0,0,.7),0 0 50px color-mix(in srgb,var(--sig) 22%,transparent)}}
.col h2{{font:900 19px/1 var(--fd);letter-spacing:.06em;color:var(--sig)}}
.col .rol{{font:400 10px/1.7 var(--fm);letter-spacing:2px;color:var(--txt-ghost);margin:8px 0 6px}}
.col .lema{{font:300 12px/1.7 var(--fu);color:var(--txt-dim);margin-bottom:12px}}
.col ul{{list-style:none;display:grid;gap:5px}}
.col a{{display:flex;gap:9px;align-items:baseline;text-decoration:none;color:var(--txt-dim);
  font:400 12px/1.5 var(--fu);padding:5px 7px;border-radius:7px;transition:background .2s,color .2s}}
.col a:hover{{background:rgba(255,255,255,.07);color:#fff}}
.col a b{{font:700 10px/1 var(--fm);color:var(--sig);min-width:18px}}
.st{{border:1px solid var(--sig);color:var(--sig);border-radius:999px;padding:4px 8px;font:700 9px/1 var(--fm)}}
</style>
</head>
<body class="sense-neon">
<a class="skip" href="#cumulo">Ir al cúmulo</a>
<canvas id="stars" aria-hidden="true"></canvas>
<header class="topnav">
  <a class="brand" href="../index.html"><span class="brand-eye" aria-hidden="true"></span>
    <span><b>BELENTANI</b><small>CÚMULO // 50 GALAXIAS</small></span></a>
  <ul class="ndots" aria-label="Las 5 Firmas">{dots_hub}</ul>
</header>
<main class="hub" id="cumulo">
  <p class="kicker">JUDAS ERA // CINCUENTA GALAXIAS</p>
  <h1 class="title">EL CÚMULO <em>BELENTANI</em></h1>
  <p class="lead">Cinco firmas. Diez estaciones. La misma historia contada desde cinco cuerpos.
  Cada galaxia es un instante del canon; el espejo repite la línea, el sentido cambia la luz.</p>
  <p class="firma">SENTIDO {sentido}</p>
  <div class="grid">{"".join(cols)}</div>
</main>
<footer class="hbar"><div class="waveC">
  <a class="hn core" href="../index.html">OMEGA</a>
  <svg class="wave" viewBox="0 0 120 26" aria-hidden="true"><path d="{WAVE}"/></svg>
  <div class="langs" role="group" aria-label="Idioma">{chips_hub}</div>
</div></footer>
<script src="core/galaxia-i18n.js" defer></script>
<script src="core/galaxia-core.js" defer></script>
<script defer>if(window.mountGalaxia){{mountGalaxia({{"id":"hub","n":0,"firma":"belentani","estacion":0,"slug":"entre","beat":2.6}});}}</script>
</body>
</html>
"""


def main():
    """Escribe 50 galaxias + hub + núcleo compartido. Sólo dentro de galaxias/."""
    OUT.mkdir(parents=True, exist_ok=True)
    CORE.mkdir(parents=True, exist_ok=True)
    (CORE / "galaxia-core.css").write_text(CORE_CSS, encoding="utf-8")
    (CORE / "galaxia-core.js").write_text(CORE_JS, encoding="utf-8")
    (CORE / "galaxia-i18n.js").write_text(I18N_JS, encoding="utf-8")
    n = 0
    for f in range(len(FIRMAS)):
        for e in range(len(ESTACIONES)):
            n += 1
            (OUT / f"galaxia-{n:02d}.html").write_text(build_html(n, f, e), encoding="utf-8")
    (OUT / "index.html").write_text(build_hub(), encoding="utf-8")
    (OUT / "GALAXIAS.json").write_text(json.dumps({
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "modelo": "5 firmas x 10 estaciones",
        "total": n,
        "firmas": [F[1] for F in FIRMAS],
        "estaciones": [E[0] for E in ESTACIONES],
        "idiomas": IDIOMAS,
        "paginas": [f"galaxia-{i:02d}.html" for i in range(1, n + 1)],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK {n} galaxias + hub + 3 ficheros core -> {OUT}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
