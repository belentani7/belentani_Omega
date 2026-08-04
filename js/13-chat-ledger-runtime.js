(function () {
  'use strict';

  var STORAGE_KEY = 'belentani_omega_runtime_v1';
  var FALLBACK = {
    frequencies: [432, 528, 639, 741, 852],
    temporalGate: { startHour: 3, endHour: 4, endMinute: 44 },
    identity: { prefix: 'BEL' },
    frequencyNote: 'Frecuencias usadas como lenguaje simbólico y sonoro; no son tratamiento clínico.'
  };
  var canon = FALLBACK;
  var state = readState();

  function readState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch (error) { return {}; }
  }
  function writeState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (error) { /* storage optional */ }
  }
  function text(selector, value) {
    var node = document.querySelector(selector);
    if (node) node.textContent = String(value);
  }
  function identity() {
    if (state.identity) return state.identity;
    var bytes = new Uint8Array(2);
    if (window.crypto && window.crypto.getRandomValues) window.crypto.getRandomValues(bytes);
    else { bytes[0] = Date.now() % 256; bytes[1] = Math.floor(Math.random() * 256); }
    state.identity = 'BEL-' + ((bytes[0] << 8 | bytes[1]) % 100).toString().padStart(2, '0');
    writeState();
    return state.identity;
  }
  function frequency() { return canon.frequencies.indexOf(state.frequency) >= 0 ? state.frequency : canon.frequencies[0]; }
  function updateFrequency(value) {
    state.frequency = Number(value);
    writeState();
    text('#hFreq', state.frequency);
    text('#teleFreq', state.frequency.toFixed(2));
    text('#hbF', state.frequency);
    var root = document.documentElement;
    root.dataset.frequency = String(state.frequency);
  }
  function gateOpen(now) {
    var hour = now.getHours();
    var minute = now.getMinutes();
    var afterStart = hour >= canon.temporalGate.startHour;
    var beforeEnd = hour < canon.temporalGate.endHour || (hour === canon.temporalGate.endHour && minute <= canon.temporalGate.endMinute);
    return afterStart && beforeEnd;
  }
  function updateGate() {
    var open = gateOpen(new Date());
    var status = document.getElementById('hStatus');
    if (status) status.textContent = open ? 'ENTRE OPEN' : 'OPTIMAL';
    var gate = document.getElementById('omegaGate');
    if (gate) gate.textContent = open ? 'EL ENTRE // 03:00–04:44 // OPEN' : 'EL ENTRE // 03:00–04:44 // SEALED';
  }
  function downloadState() {
    var blob = new Blob([JSON.stringify({ identity: identity(), frequency: frequency(), savedAt: new Date().toISOString() }, null, 2)], { type: 'application/json' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = identity().toLowerCase() + '-omega-state.json';
    link.click();
    setTimeout(function () { URL.revokeObjectURL(link.href); }, 0);
  }
  function mountPanel() {
    var home = document.getElementById('home');
    if (!home || document.getElementById('omegaRuntimePanel')) return;
    var panel = document.createElement('section');
    panel.id = 'omegaRuntimePanel';
    panel.className = 'omega-runtime-panel';
    panel.setAttribute('aria-labelledby', 'omega-runtime-title');
    panel.innerHTML = '<div><p class="omega-runtime-kicker">LOCAL CORE / BEL-XX</p><h2 id="omega-runtime-title">TU SEÑAL OMEGA</h2><p class="omega-runtime-copy">Identidad, frecuencia y estado temporal quedan en este navegador. No se envía nada a un servidor.</p><p id="omegaGate" class="omega-runtime-gate" aria-live="polite"></p></div><div class="omega-runtime-controls"><label for="omegaFrequency">Frecuencia simbólica<select id="omegaFrequency"></select></label><output id="omegaIdentity" aria-live="polite"></output><button type="button" id="omegaExport">Exportar estado</button></div><p class="omega-runtime-note" id="omegaFrequencyNote"></p>';
    home.insertAdjacentElement('afterend', panel);
    var select = panel.querySelector('#omegaFrequency');
    canon.frequencies.forEach(function (value) {
      var option = document.createElement('option');
      option.value = value;
      option.textContent = value + ' Hz';
      select.appendChild(option);
    });
    select.value = frequency();
    select.addEventListener('change', function () { updateFrequency(select.value); });
    panel.querySelector('#omegaExport').addEventListener('click', downloadState);
    panel.querySelector('#omegaIdentity').textContent = identity();
    panel.querySelector('#omegaFrequencyNote').textContent = canon.frequencyNote;
    updateFrequency(select.value);
    updateGate();
    setInterval(updateGate, 60000);
  }
  function mountHudControl() {
    var hud = document.querySelector('.hud-top > div');
    if (!hud || document.getElementById('omegaEntity')) return;
    var entity = document.createElement('span');
    entity.id = 'omegaEntity';
    entity.className = 'omega-entity-badge';
    entity.textContent = identity();
    entity.title = 'Identidad local de esta sesión';
    hud.insertBefore(entity, hud.firstChild);
  }
  function init() {
    document.documentElement.dataset.reducedMotion = window.OMEGA_REDUCED_MOTION ? 'true' : 'false';
    mountHudControl();
    mountPanel();
    fetch('data/omega-canon.json', { cache: 'no-store' }).then(function (response) {
      if (!response.ok) throw new Error('canon unavailable');
      return response.json();
    }).then(function (data) {
      canon = data;
      mountPanel();
      updateFrequency(frequency());
      updateGate();
    }).catch(function () { updateGate(); });
    window.OMEGA_RUNTIME = { identity: identity, frequency: frequency, exportState: downloadState };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
}());
