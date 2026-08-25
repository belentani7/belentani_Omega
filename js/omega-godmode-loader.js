/* BELENTANI OMEGA // GODMODE LOADER */
(function(){'use strict';
function css(h){var l=document.createElement('link');l.rel='stylesheet';l.href=h+'?v=20260825';document.head.appendChild(l)}
css('css/omega-godmode.css');
var scenes=['GENESIS','KISS','DEBT','MIRROR','DESCENT','CHOICE','RETURN'];
var state={scene:'GENESIS',progress:0};window.OMEGA_VISUAL=state;
var mark=document.createElement('div');mark.className='omega-chapter-mark';mark.innerHTML='<b>00</b> // GENESIS';document.body.appendChild(mark);
function setScene(i){i=Math.max(0,Math.min(scenes.length-1,i));state.scene=scenes[i];document.documentElement.dataset.omegaScene=scenes[i].toLowerCase();document.documentElement.style.setProperty('--omega-scene-scale',(1+i*.018).toFixed(3));document.documentElement.style.setProperty('--omega-accent',i===3?'#b8d8ff':i===6?'#d6b36a':'#ff003c');mark.innerHTML='<b>0'+i+'</b> // '+scenes[i]}
function scroll(){var max=Math.max(1,document.documentElement.scrollHeight-innerHeight),p=Math.max(0,Math.min(1,scrollY/max)),i=Math.min(6,Math.floor(p*7));state.progress=p;document.documentElement.style.setProperty('--omega-scroll-progress',p.toFixed(4));setScene(i)}
function pointer(e){document.documentElement.style.setProperty('--omega-pointer-x',(e.clientX/innerWidth*100).toFixed(2)+'%');document.documentElement.style.setProperty('--omega-pointer-y',(e.clientY/innerHeight*100).toFixed(2)+'%')}
addEventListener('scroll',function(){requestAnimationFrame(scroll)},{passive:true});addEventListener('pointermove',pointer,{passive:true});addEventListener('resize',scroll,{passive:true});document.addEventListener('DOMContentLoaded',function(){scroll();
 var title=document.querySelector('.hero-title,#heroTitle');if(title){title.style.maxWidth='min(11ch,95vw)';title.style.overflowWrap='anywhere'}
});
})();
