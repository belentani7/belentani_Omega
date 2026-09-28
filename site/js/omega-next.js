/* ═══════════════════════════════════════════════════════════════════════
   BELENTANI // OMEGA-NEXT — THICK REAL GLASS (runtime)
   Progressive enhancement: upgrades existing .glass surfaces into thick,
   refractive, pulsing neon-red glass. No-op without JS. Local-first.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var REDUCED = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Inline SVG refraction filter (feTurbulence → feDisplacementMap).
        Used by `backdrop-filter: url(#omega-refraction)` in omega-next.css. */
  function injectRefraction() {
    if (document.getElementById('omega-refraction-svg')) return;
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('id', 'omega-refraction-svg');
    svg.setAttribute('width', '0');
    svg.setAttribute('height', '0');
    svg.setAttribute('aria-hidden', 'true');
    svg.style.cssText = 'position:absolute;width:0;height:0;pointer-events:none';
    svg.innerHTML =
      '<filter id="omega-refraction" x="-20%" y="-20%" width="140%" height="140%">' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.006 0.012" numOctaves="2" seed="7" result="noise"/>' +
      '<feGaussianBlur in="noise" stdDeviation="3" result="soft"/>' +
      '<feDisplacementMap in="SourceGraphic" in2="soft" scale="18" xChannelSelector="R" yChannelSelector="G"/>' +
      '</filter>';
    document.body.appendChild(svg);
  }

  /* 2. Upgrade every existing .glass surface. */
  function upgradeSurfaces() {
    var nodes = document.querySelectorAll('.glass, .hud-panel, .tcard');
    nodes.forEach(function (el) {
      el.classList.add('glass-thick');
      if (!REDUCED) {
        el.classList.add('refract');
        if (!el.querySelector(':scope > .sheen-band')) {
          var band = document.createElement('span');
          band.className = 'sheen-band';
          band.setAttribute('aria-hidden', 'true');
          el.appendChild(band);
        }
      }
    });
  }

  /* 3. Pointer-tracked specular highlight (--mx / --my per surface). */
  function trackPointer() {
    if (REDUCED) return;
    var active = null;
    document.addEventListener('pointermove', function (e) {
      var el = e.target && e.target.closest ? e.target.closest('.glass-thick') : null;
      if (el) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
        el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
        if (active && active !== el) active.classList.remove('lit');
        el.classList.add('lit');
        active = el;
      } else if (active) {
        active.classList.remove('lit');
        active = null;
      }
    }, { passive: true });
  }

  /* 4. Orchestrate the pulse: a slow global "heartbeat" that intensifies the
        neon ring on the primary hero surface. */
  function pulse() {
    if (REDUCED) return;
    var hero = document.querySelector('#home .glass-thick, #home .glass-c, #home .hero-c');
    if (hero) hero.classList.add('glass-pulse');
  }

  function init() {
    try {
      injectRefraction();
      upgradeSurfaces();
      trackPointer();
      pulse();
    } catch (err) {
      /* Never block the page on a decorative layer. */
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }

  window.OMEGA_GLASS = { version: '1.0', reduced: REDUCED };
})();
