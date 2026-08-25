
// Service Worker registration — PWA offline cache
if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('sw.js').catch(function(err) {
      console.warn('SW registration failed:', err);
    });
  });
}

// OMEGA GODMODE — additive bootstrap. Core site remains untouched.
(function(){
  var s=document.createElement('script');
  s.src='js/omega-godmode-loader.js?v=20260825';
  s.defer=true;
  document.head.appendChild(s);
})();
