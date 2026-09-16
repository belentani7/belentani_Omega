// ═══════════════════════════════════════════════════════════════
// OMEGA SAAS CONSOLE — aditivo. Miles de líneas en espíritu, cero peso:
// consola unificada que ejecuta los 300 tools locales (CORE_AI_300),
// Beat Forge, Vision Forge, Tarot y Dream Decoder desde un solo dock.
// Sin API keys. Todo local-first.
// ═══════════════════════════════════════════════════════════════
(function () {
  function mount() {
    if (document.getElementById('omega-saas')) return;
    var studio = document.getElementById('studio');
    if (!studio) return;
    var sec = document.createElement('section');
    sec.id = 'omega-saas';
    sec.className = 'sec';
    sec.setAttribute('aria-labelledby', 'omega-saas-t');
    sec.innerHTML =
      '<h2 class="sec-title rv" id="omega-saas-t">LABORATORIO <span>SAAS</span></h2>' +
      '<div class="sec-sub rv">300 HERRAMIENTAS LOCALES // SIN API KEY</div>' +
      '<div class="tcard supreme-glass rv" style="max-width:1100px;width:100%">' +
      '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px">' +
      '<input id="saasIn" placeholder="pide: beat oscuro 96bpm / tarot / sueño con agua / prompt vision..." aria-label="Consola SaaS" style="flex:1;min-width:220px;background:transparent;border:1px solid var(--blood);color:#fff;padding:14px;font-family:var(--fm);font-size:12px;outline:none">' +
      '<button class="tc-btn" id="saasGo">EJECUTAR</button>' +
      '<button class="tc-btn" id="saasBeat">BEAT</button>' +
      '<button class="tc-btn" id="saasTarot">TAROT</button>' +
      '<button class="tc-btn" id="saasDream">DREAM</button>' +
      '</div>' +
      '<div id="saasOut" aria-live="polite" style="min-height:180px;max-height:320px;overflow-y:auto;background:rgba(0,0,0,.55);border:1px solid var(--glass-border);padding:14px;font-family:var(--fm);font-size:12px;line-height:1.9;white-space:pre-wrap">&gt; CONSOLA LISTA. 300 módulos + contexto máximo local (master prompt 7684 líneas + portal 3K + lore 300).</div>' +
      '<div style="font-family:var(--fm);font-size:10px;color:var(--txt-dim);margin-top:10px">[ LOCAL ] audio Tone.js + tarot + sueños + 300 tools. [ EXTERNO ] solo Vision Forge usa pollinations.ai.</div>' +
      '</div>';
    studio.insertAdjacentElement('afterend', sec);
    var inp = sec.querySelector('#saasIn'), out = sec.querySelector('#saasOut');
    function say(t) { out.textContent = t; out.scrollTop = 0; }
    function run() {
      var q = (inp.value || '').trim();
      if (!q) { say('> PROMPT VACIO.'); return; }
      var low = q.toLowerCase();
      try {
        // MAX CONTEXTO: comandos lore/oracle/portal/diamante responden con canon local
        if (/^(lore|oracle|oraculo|portal|diamante|diamonds|revelaci|fall|kiss|next chapter)/.test(low) || /missing piece|cinco diamantes|five diamonds|the fall|the kiss/.test(low)) {
          say(runLore(low, q));
          return;
        }
        if (/beat|bpm|ritmo/.test(low)) {
          if (typeof beatPlay === 'function') beatPlay();
          say('> BEAT FORGE // 96 BPM Am DARK\n> Bajo: A1 A1 C2 C2 F1 F1 G1 G1\n> Kick + hats activos en Tone.js local.');
          return;
        }
        if (/tarot|oraculo|carta/.test(low)) {
          if (typeof drawTarot === 'function' && document.getElementById('tarotResult')) { drawTarot(); say('> TAROT revelado en AI LAB (tarotResult).'); return; }
          say('> ORACULO LOCAL\n> PASADO: EL ENTRE\n> PRESENTE: LA DEUDA\n> FUTURO: LA MENTIRA COMPARTIDA');
          return;
        }
        if (/sueño|sueno|dream|agua|fuego|volar|caer/.test(low)) {
          var hit = null;
          if (typeof dreamSymbols !== 'undefined') {
            Object.keys(dreamSymbols).forEach(function (k) { if (!hit && low.indexOf(k) !== -1) hit = k; });
            say(hit ? '> DREAM DECODER // ' + hit.toUpperCase() + '\n' + dreamSymbols[hit] : '> DREAM DECODER\n> Símbolos: agua, fuego, volar, caer, llave, rojo, judas.');
          } else say('> DREAM DECODER no cargado (06-ai.js).');
          return;
        }
        if (/tool|modulo|herramienta|[0-9]/.test(low)) {
          var m = low.match(/[0-9]{1,3}/);
          if (m && typeof window.executeAITool300 === 'function') { say(window.executeAITool300(m[0], q)); return; }
        }
        if (typeof window.executeAITool300 === 'function' && window.CORE_AI_300_REGISTRY) {
          var pool = window.CORE_AI_300_REGISTRY.filter(function (t) {
            return (t.title + ' ' + t.cat).toLowerCase().indexOf(low.split(' ')[0]) !== -1;
          });
          var pick = pool[0] || window.CORE_AI_300_REGISTRY[Math.floor(Math.random() * window.CORE_AI_300_REGISTRY.length)];
          say(window.executeAITool300(pick.id, q));
          return;
        }
        say('> CORE_AI local: escribe "beat", "tarot", "sueño con agua" o "tool 42".');
      } catch (e) { say('> ERROR LOCAL: ' + e.message); }
    }
    function runLore(low, q) {
      if (/diamante|diamond|cinco|five/.test(low)) return '> THE FIVE DIAMONDS\n> I THE HUMAN (○ Memoria) — Who were you before the world named you? > MEMORY FRAGMENT\n> II THE ARTIST (✦ Creación) — CREATION IS AN ACT OF DEFIANCE > CREATION FRAGMENT\n> III THE SINNER (◈ Deseo) — qué deseas de verdad > DESIRE FRAGMENT\n> IV THE SAINT († Perdón) — verdad/culpa/perdón/autoengaño > FORGIVENESS FRAGMENT\n> V THE WARRIOR (△ Voluntad) — el enemigo es doubt > WILL FRAGMENT\n> Final: FIVE FRAGMENTS RECOVERED → ONE FRAGMENT IS MISSING → THE MISSING PIECE IS YOU.';
      if (/portal/.test(low)) return '> THE PORTAL\n> BELENTANI PORTAL / ACTIVE — ABRIR EL UMBRAL.\n> El portal no es una página: es la entrada al universo secreto.\n> Secuencia: ORIGEN > CUERPO > SEÑAL > PORTAL > OMEGA > JUDAS.';
      if (/kiss/.test(low)) return '> THE KISS\n> THE ONE WHO KISSED THE END. EVERY KISS IS A BETRAYAL AND A PROMISE.\n> La traición es el input. La voz es el output.';
      if (/fall/.test(low)) return '> THE FALL\n> THE FALL WAS NOT THE END. IT WAS THE PORTAL.\n> WHO ARE YOU AFTER THE FALL? EVERY FALL CREATES A DIFFERENT VERSION OF THE SELF.';
      if (/next chapter|revelaci|revelation/.test(low)) return '> REVELATION\n> HUMAN / ARTIST / SINNER / SAINT / WARRIOR se fusionan → BELENTANI → JUDAS → THE NEXT CHAPTER IS YOURS. ENTER AGAIN.';
      return '> LORE UNIFICADO (canon local)\n> BELENTANI = universo. JUDAS = era/experiencia dentro.\n> EL ENTRE > LA DEUDA > EL ROBO > LA VICTORIA AMARGA > LA MENTIRA COMPARTIDA.\n> "No he visitado una web. He entrado en una obra."';
    }
    sec.querySelector('#saasGo').addEventListener('click', run);
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') run(); });
    sec.querySelector('#saasBeat').addEventListener('click', function () { inp.value = 'beat oscuro 96bpm'; run(); });
    sec.querySelector('#saasTarot').addEventListener('click', function () { inp.value = 'tarot'; run(); });
    sec.querySelector('#saasDream').addEventListener('click', function () { inp.value = 'sueño con agua'; run(); });
    if (window.observeRV) window.observeRV();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
})();
