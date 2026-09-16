var CACHE = 'belentani-omega-v17';
var CORE = [
  './',
  './index.html',
  './manifest.json',
  './css/main.css',
  './site/css/omega-next.css',
  './site/css/omega-supreme.css',
  './js/01-boot.js',
  './js/02-scroll.js',
  './js/03-webgl.js',
  './js/04-matrix.js',
  './js/05-audio.js',
  './js/06-ai.js',
  './js/07-portal.js',
  './js/08-content.js',
  './js/09-terminal.js',
  './js/10-v13.js',
  './js/11-unified.js',
  './js/12-hero-media.js',
  './site/js/omega-next.js',
  './site/js/omega-supreme.js',
  './site/js/features/lore-panel.js',
  './site/js/features/saas-console.js',
  './site/js/core/edition-engine.js',
  './site/js/features/local-studio.js',
  './site/js/features/background-media.js',
  './docs/LORE-UNIFICADO.md',
  './ecosistema.html',
  './assets/images/og-cover.jpg',
  './assets/media/judas-poster.webp',
  './js/sw-register.js'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      // Add each asset independently: a single 404 must not abort the install.
      return Promise.all(CORE.map(function(u) {
        return cache.add(u).catch(function() {});
      }));
    }).then(function() { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.filter(function(k) { return k !== CACHE; }).map(function(k) { return caches.delete(k); }));
    }).then(function() { return self.clients.claim(); })
  );
});

// Bound every network request so a hung origin cannot stall the page.
function fetchWithTimeout(req, ms) {
  if (!self.AbortController) return fetch(req);
  var ctrl = new AbortController();
  var timer = setTimeout(function() { ctrl.abort(); }, ms);
  return fetch(req, { signal: ctrl.signal }).then(
    function(res) { clearTimeout(timer); return res; },
    function(err) { clearTimeout(timer); throw err; }
  );
}

self.addEventListener('fetch', function(e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);

  if (url.origin !== location.origin) {
    // Cross-origin (CDN/fonts): network-first. Never persist opaque responses.
    e.respondWith(
      fetchWithTimeout(req, 8000).then(function(res) {
        return res;
      }).catch(function() {
        return caches.match(req).then(function(c) {
          return c || new Response('', { status: 504, statusText: 'Offline' });
        });
      })
    );
    return;
  }

  // Same-origin: network-first, fall back to cache. Serve the SPA shell only
  // for navigations, so missing assets surface as real 404/504 instead of HTML.
  e.respondWith(
    fetchWithTimeout(req, 8000).then(function(res) {
      if (res && res.ok) {
        var copy = res.clone();
        caches.open(CACHE).then(function(c) { c.put(req, copy); });
      }
      return res;
    }).catch(function() {
      return caches.match(req).then(function(c) {
        if (c) return c;
        if (req.mode === 'navigate') return caches.match('./index.html');
        return new Response('', { status: 504, statusText: 'Offline' });
      });
    })
  );
});
