// ═══════════════════════════════════════════════════════════════
// OMEGA LORE PANEL — aditivo. Inyecta lore unificado + storyEngine.
// Lee docs/LORE-UNIFICADO.md (fetch local) con fallback embebido.
// ═══════════════════════════════════════════════════════════════
(function () {
  var FALLBACK = [
    ['01', 'EL ENTRE', 'En un pliegue del universo donde el tiempo no corre, caminaba un hombre con muchos nombres.'],
    ['02', 'LA DEUDA', 'Pedro beso los pies de Judas. No por sumision. Por devocion. La deuda se volvio impagable.'],
    ['03', 'EL ROBO', 'Judas tomo la Llave Dorada. Y Pedro se puso a cantarle.'],
    ['04', 'LA VICTORIA AMARGA', 'Quedatela. La llave es metal. Lo que yo tengo, nadie me lo arrebata: mi voz.'],
    ['05', 'LA MENTIRA COMPARTIDA', 'La llave nunca fue lo valioso. LA TRAICION ES EL INPUT. LA VOZ ES EL OUTPUT.']
  ];
  function mount() {
    if (document.getElementById('omega-lore')) return;
    var anchor = document.getElementById('mythology') || document.getElementById('judas');
    if (!anchor) return;
    var sec = document.createElement('section');
    sec.id = 'omega-lore';
    sec.className = 'sec';
    sec.setAttribute('aria-labelledby', 'omega-lore-t');
    sec.innerHTML = '<h2 class="sec-title rv" id="omega-lore-t">LORE <span>UNIFICADO</span></h2>' +
      '<div class="sec-sub rv">BELENTANI ES TODO UNIFICADO // 5 FASES</div>' +
      '<div class="g4 rv" id="omegaLoreGrid" style="max-width:1200px"></div>';
    anchor.insertAdjacentElement('afterend', sec);
    var grid = sec.querySelector('#omegaLoreGrid');
    var prog = {};
    try { prog = (window.storyEngine && window.storyEngine.progress()) || JSON.parse(localStorage.getItem('omega_story') || '{}'); } catch (e) {}
    FALLBACK.forEach(function (f) {
      var done = !!prog[f[0]];
      var card = document.createElement('article');
      card.className = 'tcard supreme-glass';
      card.innerHTML = '<div class="tc-name">FASE_' + f[0] + ' · ' + f[1] + '</div>' +
        '<p class="tc-desc">' + f[2] + '</p>' +
        '<div style="font-family:var(--fm);font-size:10px;letter-spacing:2px;color:' + (done ? 'var(--gold)' : 'var(--txt-dim)') + '">' + (done ? '◉ REGISTRADA' : '○ NO LEÍDA') + '</div>';
      card.style.cursor = 'pointer';
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      ;(function (id, el) {
        function open() {
          var ch = window.storyEngine ? window.storyEngine.open(id) : null;
          el.querySelector('div:last-child').textContent = '◉ REGISTRADA';
          if (ch) alert(ch.title + '\n\n' + ch.text);
        }
        el.addEventListener('click', open);
        el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
      })(f[0], card);
      grid.appendChild(card);
    });
    if (window.observeRV) window.observeRV();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
})();
