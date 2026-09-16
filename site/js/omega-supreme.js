/* ═══════════════════════════════════════════════════════════════════════
   BELENTANI // OMEGA-SUPREME runtime — aditivo, local-first.
   1) HERO céntrico: centra .hero-c y activa parpadeo neón del nombre.
   2) GLASS MAX: añade .supreme-glass + beam a .glass/.tcard/.hero-c.
   3) Respeta prefers-reduced-motion. Nunca bloquea la página.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function hero() {
    var h = document.querySelector('#home .hero-c');
    if (!h) return;
    h.classList.add('supreme-hero');
    if (!REDUCED) {
      var title = h.querySelector('.hero-title');
      if (title) title.classList.add('supreme-flicker');
      if (!h.querySelector(':scope > .supreme-beam')) {
        var b = document.createElement('span');
        b.className = 'supreme-beam';
        b.setAttribute('aria-hidden', 'true');
        h.insertBefore(b, h.firstChild);
      }
      h.classList.add('supreme-pulse');
    }
  }

  function glass() {
    var nodes = document.querySelectorAll('.glass, .hud-panel, .tcard, .manifesto-shell, .mythology-shell, .core-shell');
    nodes.forEach(function (el) {
      if (el.classList.contains('supreme-glass')) return;
      el.classList.add('supreme-glass');
    });
  }

  function clean() {
    // Activa limpieza: quita barra lateral flotante, botón girando y
    // convierte la albóndiga en planeta real. Todo reversible.
    try {
      document.body.classList.add('clean-on');
      localStorage.setItem('omega_clean', '1');
      var prism = document.querySelector('#home .glass-prism, .core-media .glass-prism');
      if (prism && !document.querySelector('.planet-real')) {
        var p = document.createElement('div');
        p.className = 'planet-real';
        p.setAttribute('role', 'img');
        p.setAttribute('aria-label', 'Planeta rojo con anillos, núcleo de Judas Era');
        prism.insertAdjacentElement('afterend', p);
      }
    } catch (e) {}
  }

  function init() {
    try { hero(); glass(); clean(); } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
  window.OMEGA_SUPREME = { version: '1.0', reduced: REDUCED };
})();
