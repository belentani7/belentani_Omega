"use client";

import Image from "next/image";
import dynamic from "next/dynamic";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { ArrowDown, ArrowUpRight, KeyRound, Menu, Send, Sparkles, Volume2, X } from "lucide-react";
import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { assistants, tools } from "@/lib/judas-context";

const LivingPlanet = dynamic(() => import("./living-planet").then((m) => m.LivingPlanet), { ssr: false });

const chapters = [
  ["FASE 01", "El Hombre Integrado", "No existe un cuándo. No existe un dónde. Existe un entre: un pliegue del universo donde el tiempo no corre, se respira. Allí caminaba un hombre con muchos nombres: Pedro, Marcos, Santos, Belentani. Cuatro procesos en paralelo. Una sola voz.", "La huella no miente. Cada surco es una decisión."],
  ["FASE 02", "La Deuda Impagable", "Se conocieron en un camino ausente de todos los mapas. Judas caminaba con la prisa de quien huye de algo que todavía lleva dentro. Pedro le besó los pies, no por sumisión, sino por devoción. Judas recibió un espejo que no podía soportar.", "Tu presencia, aunque a veces duela, es un regalo."],
  ["FASE 03", "El Robo y el Canto", "Judas esperó la noche y extendió las manos hacia la Llave Dorada. Cuando tiró de ella, cuatro voces emergieron: el Ángel cantó, el Guerrero se irguió, el Analítico observó y el Cronista registró. Pedro no lanzó una maldición. Se sentó y cantó.", "No cantaba contra él. Cantaba para él."],
  ["FASE 04", "La Victoria Amarga", "Judas volvió con la llave. Lo reconocieron y lo recordaron. Su victoria, sin embargo, sabía a metal. Nunca pudo olvidar al hombre arrodillado que cantó después del robo. Intentó destruir a quien lo había visto por completo.", "Victorioso. Y destrozado."],
  ["FASE 05", "La Mentira Compartida", "La llave nunca fue lo valioso. Pedro permitió que Judas robara un símbolo para que descubriera lo irremplazable: la voz integrada, la capacidad de transformar el dolor y cantar al traidor sin convertirse en él.", "La traición es el input. La voz es el output."],
] as const;

const archetypes = [
  ["01", "PEDRO", "La Roca", "El ancla fundacional. La raíz que atraviesa dimensiones sin moverse."],
  ["02", "MARCOS", "El Cronista", "Observa, registra y escribe la historia mientras los demás la viven."],
  ["03", "SANTOS", "La Antena", "Recibe la señal de lo trascendente y la traduce al cuerpo."],
  ["04", "BELENTANI", "El Artefacto", "Integra el poder del guerrero con la voz del ángel."],
  ["05", "THE HUMAN", "La Interfaz", "Mantiene conciencia, integridad y humanidad en el mundo real."],
] as const;

const music = [
  ["01", "MON AMOUR", "Deseo / distancia", "R&B alternativo"],
  ["02", "THERAPIST", "Intimidad / defensa", "Dark pop"],
  ["03", "APAGA A LUZ", "Sombra / cuerpo", "Electronic soul"],
  ["04", "LENTO", "Tensión / entrega", "Industrial R&B"],
] as const;

function Nav() {
  const [open, setOpen] = useState(false);
  const links = [["artist", "The Artist"], ["music", "Music"], ["judas", "Judas"], ["portal", "Portal"], ["gallery", "Archive"], ["studio", "Studio"]];
  return <header className="nav"><a className="brand" href="#home">BELENTANI</a><nav className="navlinks" aria-label="Principal">{links.map(([id,label]) => <a key={id} href={`#${id}`}>{label}</a>)}</nav><a className="nav-cta" href="#studio">Entrar al OS</a><button className="ghost mobile-menu" onClick={() => setOpen(!open)} aria-expanded={open} aria-label="Abrir navegación">{open ? <X /> : <Menu />}</button>{open && <nav className="mobile-panel" aria-label="Móvil">{links.map(([id,label]) => <a key={id} href={`#${id}`} onClick={() => setOpen(false)}>{label}</a>)}</nav>}</header>;
}

function AudioSigil() {
  const play = () => {
    const AudioContextClass = window.AudioContext || (window as typeof window & { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ctx = new AudioContextClass();
    [216, 270, 324, 432].forEach((frequency, index) => {
      const oscillator = ctx.createOscillator(); const gain = ctx.createGain();
      oscillator.type = index % 2 ? "triangle" : "sine"; oscillator.frequency.value = frequency;
      gain.gain.setValueAtTime(0, ctx.currentTime + index * .12); gain.gain.linearRampToValueAtTime(.08, ctx.currentTime + index * .12 + .05); gain.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + 2.4 + index * .12);
      oscillator.connect(gain).connect(ctx.destination); oscillator.start(ctx.currentTime + index * .12); oscillator.stop(ctx.currentTime + 2.7 + index * .12);
    });
  };
  return <button className="secondary" onClick={play}><Volume2 data-icon="inline-start" /> Escuchar señal 432</button>;
}

function Studio() {
  const [mode, setMode] = useState("CORE");
  const transport = useMemo(() => new DefaultChatTransport({ api: "/api/chat", body: { mode } }), [mode]);
  const { messages, sendMessage, status, stop, error } = useChat({ transport });
  const [input, setInput] = useState("");
  const list = useRef<HTMLDivElement>(null);
  useEffect(() => { list.current?.scrollTo({ top: list.current.scrollHeight, behavior: "smooth" }); }, [messages, status]);
  const submit = (event: FormEvent) => { event.preventDefault(); if (!input.trim() || status !== "ready") return; sendMessage({ text: input }); setInput(""); };
  const launchTool = (name: string, description: string) => { setInput(`Activa la herramienta «${name}». Necesito: ${description}. Empieza haciéndome las preguntas mínimas necesarias.`); document.querySelector<HTMLTextAreaElement>("#judas-prompt")?.focus(); };
  return <section className="section" id="studio"><div className="section-head reveal"><div><div className="eyebrow">Creative operating system</div><h2>La caja mágica.</h2></div><p>Asistentes especializados comparten el contexto JUDAS ERA. Todo ocurre aquí, sin romper la experiencia ni exponer el motor que hay detrás.</p></div><div className="assistant-row reveal" aria-label="Seleccionar asistente">{assistants.map(([code,name,description]) => <button key={code} className="assistant glass" data-active={mode === code} onClick={() => setMode(code)}><code>{code}</code><b>{name}</b><span>{description}</span></button>)}</div><div className="chat glass reveal"><div className="chat-top"><b>NEURAL CORE // {mode}</b><span className="status">{status === "streaming" ? "SINTETIZANDO" : "ONLINE"}</span></div><div className="messages" ref={list} aria-live="polite">{messages.length === 0 && <div className="message">Soy el núcleo creativo de BELENTANI. Puedo ayudarte a convertir una herida en canción, una idea en sistema o un símbolo en lenguaje visual. ¿Qué quieres construir?</div>}{messages.map((message) => <div className="message" data-role={message.role} key={message.id}>{message.parts.map((part, index) => part.type === "text" ? <span key={index}>{part.text}</span> : null)}</div>)}{error && <div className="message">La transmisión se interrumpió. Inténtalo de nuevo sin compartir información sensible.</div>}</div><form className="composer" onSubmit={submit}><label className="sr-only" htmlFor="judas-prompt">Mensaje para el núcleo</label><textarea id="judas-prompt" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing && e.keyCode !== 229) { e.preventDefault(); e.currentTarget.form?.requestSubmit(); } }} placeholder="Describe una canción, imagen, app, sueño o decisión…" /><button type={status === "streaming" ? "button" : "submit"} onClick={status === "streaming" ? stop : undefined} className="primary" aria-label={status === "streaming" ? "Detener" : "Enviar"}>{status === "streaming" ? <X /> : <Send />}</button></form></div><div className="studio-grid reveal">{tools.map(([name,category,description]) => <button key={name} className="tool glass" onClick={() => launchTool(name, description)}><small>{category}</small><strong>{name}</strong><span>{description}</span></button>)}</div></section>;
}

function Contact() {
  const [note,setNote] = useState("");
  const submit = async (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); setNote("ENCRIPTANDO TRANSMISIÓN…"); const form = new FormData(event.currentTarget); const response = await fetch("/api/contact", { method:"POST", headers:{"content-type":"application/json"}, body:JSON.stringify(Object.fromEntries(form)) }); const data = await response.json(); setNote(response.ok ? "TRANSMISIÓN RECIBIDA // EL NÚCLEO RESPONDERÁ" : data.error); if(response.ok) event.currentTarget.reset(); };
  return <section className="section" id="contact"><div className="contact glass reveal"><div><div className="eyebrow">Direct transmission</div><h3>Construyamos la siguiente anomalía.</h3><p>Colaboraciones musicales, identidad, actuaciones, tecnología creativa y proyectos que necesiten una voz propia.</p></div><form className="form" onSubmit={submit}><div className="field"><label htmlFor="name">IDENTIFICADOR</label><input id="name" name="name" required minLength={2} autoComplete="name" /></div><div className="field"><label htmlFor="email">VECTOR DE RETORNO</label><input id="email" name="email" type="email" required autoComplete="email" /></div><div className="field"><label htmlFor="subject">CLASIFICACIÓN</label><input id="subject" name="subject" required placeholder="Colaboración / Booking / Visual" /></div><div className="field"><label htmlFor="message">CARGA ENCRIPTADA</label><textarea id="message" name="message" rows={5} required minLength={20} /></div><div className="honeypot"><label htmlFor="website">Website</label><input id="website" name="website" tabIndex={-1} autoComplete="off" /></div><button className="primary" type="submit">Ejecutar transmisión <ArrowUpRight data-icon="inline-end" /></button><div className="form-note" role="status">{note}</div></form></div></section>;
}

export function JudasExperience() {
  const [unlocked,setUnlocked] = useState(false);
  useEffect(() => {
    let cleanup = () => {};
    void import("gsap").then(({ gsap }) => import("gsap/ScrollTrigger").then(({ ScrollTrigger }) => {
      gsap.registerPlugin(ScrollTrigger);
      const context = gsap.context(() => {
        gsap.utils.toArray<HTMLElement>(".reveal").forEach((element) => gsap.to(element,{ opacity:1,y:0,duration:1.05,ease:"power3.out",scrollTrigger:{trigger:element,start:"top 86%",once:true} }));
        gsap.utils.toArray<HTMLElement>(".chapter").forEach((element) => gsap.fromTo(element,{clipPath:"inset(12% 0 12% 0)"},{clipPath:"inset(0% 0 0% 0)",scrollTrigger:{trigger:element,start:"top 82%",end:"top 40%",scrub:1}}));
      }); cleanup = () => context.revert();
    })); return () => cleanup();
  }, []);
  return <div className="shell"><a className="sr-only" href="#main">Saltar al contenido</a><LivingPlanet /><div className="veil" /><div className="content"><Nav /><main id="main"><section className="section hero" id="home"><div className="eyebrow reveal">Creative OS // Judas Era</div><h1 className="reveal">JUDAS<em>Experience IV</em></h1><p className="lead reveal">Una ópera digital sobre traición, devoción y la voz que permanece cuando todos los símbolos han sido robados.</p><div className="actions reveal"><a className="primary" href="#judas">Iniciar la crónica <ArrowDown data-icon="inline-end" /></a><AudioSigil /></div><div className="scroll-mark">DESCIENDE AL NÚCLEO</div></section>
<section className="section" id="artist"><div className="section-head reveal"><div><div className="eyebrow">Archive // The architect</div><h2>Pedro antes del artefacto.</h2></div><p>Nacido en São Paulo, forjado en Barcelona. BELENTANI transforma vulnerabilidad radical en R&B alternativo, dark pop y electrónica industrial.</p></div><div className="artist-grid"><article className="story glass reveal"><span className="index">RECORD_01 // ORIGIN</span><h3>El observador no reacciona. Registra.</h3><p>La música comenzó como disciplina vocal y terminó convirtiéndose en arquitectura de supervivencia. Melodías de soul, estructuras rítmicas cautivadoras y una presencia que convierte la intimidad en espacio escénico.</p><p>Cuando la realidad exterior dejó de sostener el espíritu, Pedro convirtió su santuario interior en un estudio. El dolor pasó a ser material. La voz, proceso. BELENTANI, resultado.</p></article><figure className="portrait glass reveal"><figcaption className="portrait-caption">ARCHIVE // JUDAS ERA // THE WITNESS</figcaption></figure></div><div className="archetypes">{archetypes.map(([i,name,title,desc]) => <article className="archetype glass reveal" key={name}><small>{i} // {title}</small><b>{name}</b><p>{desc}</p></article>)}</div></section>
<section className="section" id="music"><div className="section-head reveal"><div><div className="eyebrow">Sonic archive</div><h2>La voz como arma y refugio.</h2></div><p>Cada registro habita una tensión distinta. Este archivo no inventa enlaces: prepara un sistema verificable para conectar los lanzamientos oficiales cuando estén confirmados.</p></div><div className="music-grid">{music.map(([i,title,motif,genre]) => <article className="tool glass reveal" key={title}><small>RECORD_{i}</small><strong>{title}</strong><span>{motif}<br />{genre}</span></article>)}</div></section>
<section className="section" id="judas"><div className="section-head reveal"><div><div className="eyebrow">System halt // Protocol suspended</div><h2>La Crónica de la Llave Dorada.</h2></div><p>Judas asumió su rol con precisión algorítmica. Recuperaremos la llave. O cambiaremos la cerradura.</p></div><div className="chronicle">{chapters.map(([phase,title,text,quote]) => <article className="chapter glass" key={phase}><div className="chapter-index">{phase}</div><div><h3>{title}</h3><p>{text}</p><p className="quote">“{quote}”</p></div></article>)}</div><div className="key-stage glass reveal"><div className="eyebrow">Access artifact</div><div className="key" aria-hidden="true">⌘</div><h3>La llave no abre una puerta. Abre una conversación.</h3><button className="primary" onClick={() => {setUnlocked(true); document.querySelector("#portal")?.scrollIntoView({behavior:"smooth"});}}><KeyRound data-icon="inline-start" /> Recuperar llave dorada</button></div></section>
<section className="section" id="portal"><div className="section-head reveal"><div><div className="eyebrow">Sector 12 // Integration</div><h2>{unlocked ? "El núcleo reconoce tu voz." : "Cinco fragmentos esperan."}</h2></div><p>{unlocked ? "Acceso concedido. Los diamantes ya no son objetos aislados: forman una memoria común conectada al Studio." : "Completa la crónica y recupera la llave para sincronizar el núcleo."}</p></div><div className="diamonds reveal" data-unlocked={unlocked}>{["ROCA","CRONISTA","ANTENA","ARTEFACTO","INTERFAZ"].map((name,index)=><button key={name} className="diamond glass" disabled={!unlocked} onClick={() => document.querySelector("#studio")?.scrollIntoView({behavior:"smooth"})}><i style={{"--i":index} as React.CSSProperties} /><span>0{index+1} // {name}</span></button>)}</div></section>
<section className="section" id="gallery"><div className="section-head reveal"><div><div className="eyebrow">Visual archive</div><h2>Data recovered from the collapse.</h2></div><p>Fragmentos editoriales de la era. El archivo se reordena con el movimiento; cada imagen es evidencia y construcción simultáneamente.</p></div><div className="gallery reveal">{["VENOM / SERPENT PACT","GAZE / THE WITNESS","WARRIOR & ANGEL","ZION / SYSTEM HALT"].map((title)=><figure className="art glass" key={title}><span>{title}</span></figure>)}</div></section>
<Studio /><Contact /></main><footer className="footer"><span>BELENTANI // JUDAS ERA © 2026</span><span>LA TRAICIÓN ES EL INPUT. LA VOZ ES EL OUTPUT.</span></footer></div></div>;
}
