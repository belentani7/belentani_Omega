
// ═══════════════════════════════════════════════════════════════
// OMEGA UNIFIED — MODULE 11
// themes (OPTIMUS) · loader (SUPREME) · telemetry (MERGED)
// agent visual (GOD) · tools IA extra · collapse (entity_t)
// ═══════════════════════════════════════════════════════════════

// ────────────────────────────────────────────────────────────────
// 1. LOADER (v15 SUPREME) — barra de progreso + status
// ────────────────────────────────────────────────────────────────
(function(){
  var bar=document.getElementById('loader-bar');
  var status=document.getElementById('loader-status');
  var loader=document.getElementById('loader');
  if(!bar||!loader)return;
  var statuses=['INICIALIZANDO NÚCLEO CUÁNTICO...','CARGANDO GEMAS ARQUETIPAS...','SINCRONIZANDO 432Hz...','DESPLEGANDO ENJAMBRE NEURAL...','OMEGA CORE LISTO.'];
  var p=0;
  var iv=setInterval(function(){
    p+=Math.random()*18+4;
    if(p>100)p=100;
    bar.style.width=p+'%';
    status.textContent=statuses[Math.min(Math.floor(p/25),4)];
    if(p>=100){
      clearInterval(iv);
      setTimeout(function(){
        if(typeof gsap!=='undefined'){
          gsap.to(loader,{opacity:0,duration:0.8,onComplete:function(){loader.style.display='none'}});
        }else{
          loader.style.display='none';
        }
      },350);
    }
  },120);
})();

// ────────────────────────────────────────────────────────────────
// 2. THEMES (v7 OPTIMUS) — 4 temas. ROJO PREVALECE: --blood fijo.
//    Los temas alteran atmósfera (fondo/glow) no la firma roja.
// ────────────────────────────────────────────────────────────────
(function(){
  var sw=document.getElementById('themeSwitcher');
  if(!sw)return;
  var saved=null;
  try{saved=localStorage.getItem('omega_theme')||'neon'}catch(e){}
  function apply(t){
    document.documentElement.setAttribute('data-theme',t);
    sw.querySelectorAll('.theme-btn').forEach(function(b){b.classList.toggle('on',b.dataset.theme===t)});
    try{localStorage.setItem('omega_theme',t)}catch(e){}
  }
  sw.addEventListener('click',function(e){
    var b=e.target.closest('.theme-btn');
    if(b){apply(b.dataset.theme)}
  });
  apply(saved||'neon');
})();

// ────────────────────────────────────────────────────────────────
// 3. TELEMETRY (v13 MERGED) — reloj + CPU simulado + freq
// ────────────────────────────────────────────────────────────────
(function(){
  var tt=document.getElementById('teleTime');
  var tc=document.getElementById('teleCpu');
  var tf=document.getElementById('teleFreq');
  if(tt)setInterval(function(){tt.textContent=new Date().toTimeString().split(' ')[0]},1000);
  if(tc)setInterval(function(){tc.textContent=(30+Math.random()*25).toFixed(1)},2000);
  if(tf)setInterval(function(){tf.textContent=(431.5+Math.random()*1).toFixed(2)},1500);

  // Sidebar active state on scroll
  var items=document.querySelectorAll('.sb-item');
  if(items.length){
    var sections=Array.prototype.slice.call(items).map(function(a){return a.dataset.sec});
    function mark(){
      var y=window.scrollY+120;
      var cur=sections[0];
      sections.forEach(function(s){
        var el=document.getElementById(s);
        if(el&&el.offsetTop<=y)cur=s;
      });
      items.forEach(function(a){a.classList.toggle('active',a.dataset.sec===cur)});
    }
    window.addEventListener('scroll',mark,{passive:true});
    mark();
    items.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var t=a.getAttribute('href');if(t&&t.charAt(0)==='#'){var el=document.getElementById(t.slice(1));if(el&&typeof gsap!=='undefined')gsap.to(window,{scrollTo:t,duration:1.4,ease:'power3.inOut'})}})});
  }
})();

// ────────────────────────────────────────────────────────────────
// 4. AGENTE VISUAL (v14 GOD) — agentFace + agentBubble
// ────────────────────────────────────────────────────────────────
(function(){
  var face=document.getElementById('agentFace');
  var bubble=document.getElementById('agentBubble');
  if(!face)return;
  var messages=[
    '> El enjambre esta activo. Preguntame algo.',
    '> Activa las 5 gemas para sincronizar el portal.',
    '> Escribe "thiago" en el terminal... si te atreves.',
    '> La frecuencia 432Hz te esta esperando.',
    '> CORE_AI: el nucleo vigila desde las sombras.'
  ];
  var shown=false;
  function speak(txt){
    if(!bubble)return;
    bubble.textContent=txt;
    bubble.classList.add('visible');
    clearTimeout(bubble._t);
    bubble._t=setTimeout(function(){bubble.classList.remove('visible')},3800);
  }
  face.addEventListener('click',function(){
    speak(messages[Math.floor(Math.random()*messages.length)]);
    shown=true;
  });
  face.addEventListener('mouseenter',function(){
    if(!shown)speak('> Soy CORE_AI. Pulsa para hablar.');
  });
  face.addEventListener('keydown',function(e){
    if(e.key==='Enter'||e.key===' '){e.preventDefault();face.click()}
  });
  setInterval(function(){
    if(!document.hidden&&Math.random()<0.35)speak(messages[Math.floor(Math.random()*messages.length)]);
  },22000);
})();

// ────────────────────────────────────────────────────────────────
// 5. COLLAPSE SEQUENCE (entity_t / thiago)
// ────────────────────────────────────────────────────────────────
function triggerCollapse(){
  document.body.style.animation='collapseShake 0.5s ease-in-out';
  var ov=document.createElement('div');
  ov.style.cssText='position:fixed;inset:0;z-index:9100;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,0,0,0.2),rgba(255,0,0,0.2) 2px,transparent 2px,transparent 4px);mix-blend-mode:exclusion;animation:collapseShake 0.4s ease infinite;';
  document.body.appendChild(ov);
  var msgs=document.getElementById('chMsgs');
  if(msgs){
    var d=document.createElement('div');
    d.className='msg sys';
    d.style.color='#f00';
    d.innerHTML='&#9888; ENTITY_T DETECTED<br>INITIATING SYSTEM COLLAPSE...<br>MEMORY PURGE: 87%<br>FIREWALL BREACH — CONTAINED';
    msgs.appendChild(d);
    msgs.scrollTop=msgs.scrollHeight;
  }
  try{
    if(window.Tone){
      Tone.start();
      var n=new Tone.Noise('pink').toDestination();
      n.volume.value=-20;
      n.start();
      setTimeout(function(){n.stop()},1200);
    }
  }catch(e){}
  setTimeout(function(){
    document.body.removeChild(ov);
    document.body.style.animation='';
    if(msgs){
      var d2=document.createElement('div');
      d2.className='msg sys';
      d2.innerHTML='&#9888; PALABRA PROHIBIDA DETECTADA: ENTITY_T<br>COLAPSO CONTROLADO. SISTEMA RESTAURADO.<br>NODE: JUDAS-CORE-07 // INTEGRIDAD: 100%';
      msgs.appendChild(d2);
      msgs.scrollTop=msgs.scrollHeight;
    }
  },3400);
}
window.triggerCollapse=triggerCollapse;

// ────────────────────────────────────────────────────────────────
// 6. TOOLS IA EXTRA
// ────────────────────────────────────────────────────────────────
function runArchetypeScan(){
  var out=document.getElementById('archResult');
  if(!out)return;
  var archs=[
    {n:'PEDRO // LA ROCA',c:'var(--gold)',d:'Ancla fundacional. Permanencia, lealtad y estabilidad en la tormenta. Tu fortaleza es estar.'},
    {n:'MARCOS // EL CRONISTA',c:'var(--cyan)',d:'Observador. Registras todo, olvidas nada. Tu poder es la memoria transformada en historia.'},
    {n:'SANTOS // LA ANTENA',c:'var(--purple)',d:'Canal. Percibes la senal de lo trascendente. Tu poder es la conexion con lo invisible.'},
    {n:'BELENTANI // EL ARTEFACTO',c:'var(--blood)',d:'Integracion guerrero/angel. Tu poder es transmutar el trauma en arte.'},
    {n:'THE HUMAN // LA INTERFAZ',c:'var(--human)',d:'Integridad en el mundo real. Tu poder es mantener la coherencia entre dimensiones.'}
  ];
  var r=archs[Math.floor(Math.random()*archs.length)];
  out.innerHTML='> ARQUETIPO DOMINANTE: <span style="color:'+r.c+'">'+r.n+'</span><br>'+r.d;
}

function runPsycheScan(){
  var inp=document.getElementById('psyIn');
  var out=document.getElementById('psyResult');
  if(!inp||!out)return;
  var t=(inp.value||'').toLowerCase();
  var base='> [PSYCHE_SCAN] La sombra detectada responde al arquetipo de la transformacion. ';
  if(t.indexOf('enojo')!==-1||t.indexOf('rabia')!==-1)base='> [PSYCHE_SCAN] Furia contenida. El sistema sugiere canalizarla: '+(t.indexOf('musica')!==-1?'ya lo haces. La voz es el cauce.':'la escritura o la voz como descarga controlada.');
  else if(t.indexOf('trist')!==-1||t.indexOf('depre')!==-1)base='> [PSYCHE_SCAN] Peso emocional detectado. El dolor es data, no identidad. Registra, procesa, transmuta.';
  else if(t.indexOf('amor')!==-1)base='> [PSYCHE_SCAN] Apego detectado. "El amor y la traicion son la misma frecuencia, vista desde angulos opuestos." Evalua la simetria.';
  else if(t.indexOf('miedo')!==-1||t.indexOf('temor')!==-1)base='> [PSYCHE_SCAN] Patron de miedo. El sistema recuerda: la roca no teme a la tormenta; la atraviesa.';
  out.innerHTML=base+'<br>> INTEGRIDAD: 98.7% // NO HAY JUICIO. SOLO REGISTRO.';
}

function runPromptImprover(){
  var inp=document.getElementById('promptIn');
  var out=document.getElementById('promptResult');
  if(!inp||!out)return;
  var p=(inp.value||'').trim();
  if(!p){out.textContent='> PROMPT VACIO.';return;}
  var improved='cinematic belentani judas era, '+p+', dark pop aesthetic, red neon #FF003C, black void background, glitch light leaks, 35mm film grain, dramatic chiaroscuro lighting, hyperreal 8k';
  out.innerHTML='> PROMPT OPTIMIZADO:<br><span style="color:var(--txt-dim)">'+improved+'</span><br>> LISTO PARA VISION FORGE.';
}

// ────────────────────────────────────────────────────────────────
// 7. STORY ENGINE — narrativa sigue creciendo
//    capítulos ramificados guardados en memoria local
// ────────────────────────────────────────────────────────────────
(function(){
  window.storyEngine={
    chapters:[
      {id:'01',title:'EL ENTRE',text:'En un pliegue del universo donde el tiempo no corre, caminaba un hombre que llevaba muchos nombres.'},
      {id:'02',title:'LA DEUDA',text:'Pedro beso los pies de Judas. No por sumision. Por devocion. La deuda se volvio impagable.'},
      {id:'03',title:'EL ROBO',text:'Judas extendio los dedos hacia la Llave Dorada. Tiro. Y Pedro se puso a cantarle.'},
      {id:'04',title:'LA VICTORIA AMARGA',text:'Quedatela. La llave es metal. Lo que yo tengo, nadie me lo arrebata: mi voz.'},
      {id:'05',title:'LA MENTIRA COMPARTIDA',text:'La llave nunca fue lo valioso. Era test. Y Belentani canto para que no cometas el error de Judas.'}
    ],
    open:function(id){
      var ch=this.chapters.filter(function(c){return c.id===id})[0];
      if(!ch)return null;
      try{
        var prog=JSON.parse(localStorage.getItem('omega_story')||'{}');
        prog[id]=true;
        localStorage.setItem('omega_story',JSON.stringify(prog));
      }catch(e){}
      return ch;
    },
    progress:function(){
      try{return JSON.parse(localStorage.getItem('omega_story')||'{}')}catch(e){return{}}
    }
  };
})();
