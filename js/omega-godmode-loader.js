/* BELENTANI OMEGA // GODMODE LOADER */
(function(){'use strict';
function css(h){var l=document.createElement('link');l.rel='stylesheet';l.href=h+'?v=20260825';document.head.appendChild(l)}
css('css/omega-godmode.css');
var scenes=['GENESIS','KISS','DEBT','MIRROR','DESCENT','CHOICE','RETURN'];
var state={scene:'GENESIS',progress:0,overflow:0};window.OMEGA_VISUAL=state;
var mark=document.createElement('div');mark.className='omega-chapter-mark';mark.innerHTML='<b>00</b> // GENESIS';document.body.appendChild(mark);
var light=document.createElement('div');light.setAttribute('aria-hidden','true');light.style.cssText='position:fixed;inset:-25%;pointer-events:none;z-index:2;opacity:.45;mix-blend-mode:screen;background:radial-gradient(circle at 50% 50%,rgba(255,0,60,.09),transparent 28%,transparent 68%);transition:background 1.4s,transform 1.2s;will-change:transform';document.body.appendChild(light);
function setScene(i){i=Math.max(0,Math.min(scenes.length-1,i));state.scene=scenes[i];document.documentElement.dataset.omegaScene=scenes[i].toLowerCase();document.documentElement.style.setProperty('--omega-scene-scale',(1+i*.018).toFixed(3));var a=i===3?'#b8d8ff':i===6?'#d6b36a':i===4?'#263a70':'#ff003c';document.documentElement.style.setProperty('--omega-accent',a);light.style.background='radial-gradient(circle at 50% 50%,'+a+'1a,transparent 30%,transparent 70%)';light.style.transform='rotate('+(i*18)+'deg) scale('+(1+i*.015)+')';mark.innerHTML='<b>0'+i+'</b> // '+scenes[i]}
function scroll(){var max=Math.max(1,document.documentElement.scrollHeight-innerHeight),p=Math.max(0,Math.min(1,scrollY/max)),i=Math.min(6,Math.floor(p*7));state.progress=p;document.documentElement.style.setProperty('--omega-scroll-progress',p.toFixed(4));setScene(i)}
function pointer(e){document.documentElement.style.setProperty('--omega-pointer-x',(e.clientX/innerWidth*100).toFixed(2)+'%');document.documentElement.style.setProperty('--omega-pointer-y',(e.clientY/innerHeight*100).toFixed(2)+'%')}
function audit(){var vw=document.documentElement.clientWidth+1,c=0;document.querySelectorAll('body *').forEach(function(el){if(el===light||el===mark)return;var r=el.getBoundingClientRect();if(r.width>vw*1.01||r.right>vw+1||r.left<-1)c++});state.overflow=c;document.body.dataset.omegaOverflow=c?'true':'false';window.OMEGA_OVERFLOW_COUNT=c}
addEventListener('scroll',function(){requestAnimationFrame(scroll)},{passive:true});addEventListener('pointermove',pointer,{passive:true});addEventListener('resize',function(){scroll();audit()},{passive:true});document.addEventListener('DOMContentLoaded',function(){scroll();audit();setTimeout(audit,1000);var title=document.querySelector('.hero-title,#heroTitle');if(title){title.style.maxWidth='min(11ch,95vw)';title.style.overflowWrap='anywhere'}});
})();
