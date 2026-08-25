# BELENTANI OMEGA — JUDAS ERA · ARCHITECTURAL EXPERIENCE SYSTEM

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Stars](https://img.shields.io/github/stars/belentani7/belentani-omega-canon?style=social)]()
[![Forks](https://img.shields.io/github/forks/belentani7/belentani-omega-canon?style=social)]()

## 🔥 What Is This

**BELENTANI OMEGA** is not a website. It's an architectural experience system — a living constellation of code, art, sound, and narrative that fuses cinema-grade visual effects, WebGL shader engineering, and interactive storytelling into a single deployable unit.

This repository is the canonical source for **belentani.es**, powered by the JUDAS ERA narrative engine (v12.0+). Every pixel, every shader, every audio cue is versioned, tested, and ready to deploy anywhere.

### Live
🌐 **[belentani.es](https://belentani.es)** · [belentani.eu](https://belentani.eu) · [noiacore.com](https://noiacore.com)

---

## 🏗️ Architecture Overview

```
belentani-omega-canon/
├── index.html              # Main experience entry point (SPA shell)
├── css/
│   ├── main.css            # Core design system + global styles
│   └── omega-next.css      # Next-gen theme layer
├── js/
│   ├── 01-boot.js          # Application bootstrap & environment detection
│   ├── 02-scroll.js        # Lenis smooth scroll + parallax engine
│   ├── 03-webgl.js         # Three.js renderer + bloom post-processing pipeline
│   ├── 04-matrix.js        # Code rain canvas overlay effect
│   ├── 05-audio.js         # Tone.js audio-reactive ambient soundscape
│   ├── 06-ai.js            # AI chatbot integration module (JUDAS_CORE)
│   ├── 07-portal.js        # Portal/gems gamification layer
│   ├── 08-content.js       # Dynamic content loader & lazy asset fetching
│   ├── 09-terminal.js      # Terminal emu laction system
│   ├── 10-v13.js           # Unified v13 feature merge module
│   ├── 11-unified.js       # Master orchestrator tying all systems together
│   └── 12-hero-media.js    # Hero media manager (video/image/audio playback)
├── magic/                  # Magic Kit — experimental layers
│   ├── immersive.html      # Deep immersion mode (full-screen 3D experience)
│   ├── shader.html         # Standalone GLSL shader playground
│   ├── sfx.html            # Sound effects library player
│   ├── ai-instructions.md  # Agent briefing documents
│   ├── lore.md             # Lore/narrative canon documentation
│   ├── plugin.js           # Plugin system entry point
│   ├── README.md           # Magic kit documentation
│   └── skill.md            # Skill definitions for AI agents
├── core/                   # Core systems
│   ├── features/           # Feature modules registry
├── features/
├── scripts/                # Build & deployment automation
├── workflows/              # GitHub Actions CI/CD pipelines
├── assets/                 # Static assets cache
├── img/                    # Image assets (diamond_scene.png, hero media)
├── media/                  # Video/media assets (judas-hero.mp4, judas-poster.webp)
├── sw.js                   # Service Worker (PWA support)
├── sw-register.js          # SW registration script
├── manifest.json           # Web App Manifest (PWA config)
├── ecosystem.json          # Ecosystem node definition & metadata
├── CNAME                   # Custom domain configuration
└── BLUEPRINT-MAESTRO-BELENTANI-JUDAS.md  # Master blueprint document
```

---

## ⚡ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **3D Rendering** | Three.js r128 + EffectComposer + UnrealBloomPass | Post-processing pipeline, bloom/glow effects |
| **Animation** | GSAP 3.12 + ScrollTrigger + ScrollToPlugin | Scroll-driven animations, timeline sequencing |
| **Smooth Scroll** | Lenis 1.1 | Cinematic smooth scrolling with momentum |
| **Audio** | Tone.js 14.8 | Audio-reactive visuals, ambient soundtrack |
| **Fonts** | Google Fonts (Chakra Petch, Cinzel Decorative, Cormorant Garamond, JetBrains Mono, Orbitron) | Sci-fi/cinematic typography system |
| **PWA** | Service Worker + Web App Manifest | Installable progressive web app, offline-first |
| **CI/CD** | GitHub Actions (quality.yml, repo-security.yml) | Automated quality gates, security scanning |

---

## 🎬 Sections

| Section | ID | Description |
|---|---|---|
| Home | `#home` | Landing with animated hero shader and call-to-action |
| The Artist | `#artist` | Professional bio — Pedro Belentani, creator/architect/director |
| Music | `#music` | Discography streaming archive with Sonic Archive integration |
| Judas Era | `#judas` | Narrative universe center — mythology, lore, character arcs |
| Zion Dimension | `#zion` | Verified/publishable instances of the ecosystem |
| Concept | `#concept` | Philosophy behind JUDAS_OS and creative methodology |
| Portal/Gems | `#portal` | Gamification layer — archetypes to unlock via challenges |
| Gallery | `#gallery` | Visual portfolio — renders, photography, concept art |
| AI Lab | `#ailab` | Interactive tools — JUDAS_CORE chatbot, beat generator, dream decoder |
| Studio | `#studio` | Production workspace overview and workflow documentation |
| Challenges | `#challenges` | Interactive challenges with XP progression system |
| Contact | `#contact` | Contact channels — email, social, embedded forms |

---

## 🛠️ Local Development

```bash
# 1. Clone the repository
git clone https://github.com/belentani7/belentani-omega-canon.git
cd belentani-omega-canon

# 2. Open index.html in any modern browser
# No build step required — pure static SPA

# 3. For development server (optional):
npx serve .
# or
python -m http.server 8080
```

### Recommended Dev Setup
- **Browser**: Chrome/Edge/Firefox latest (Three.js r128 requires WebGL 1.0+)
- **DevTools**: Enable "Rendering" panel → check "FPS meter", "Paint flashing"
- **Performance**: Disable extensions during testing to avoid interference
- **Testing**: Use Lighthouse (Chrome DevTools → Audit) for baseline metrics

---

## 🚀 Deployment

This project deploys cleanly as static files to any hosting provider:

| Provider | Method | Notes |
|---|---|---|
| **Netlify** | Drag & drop dist/ folder | Instant deploy, auto HTTPS, custom domains |
| **Vercel** | `vercel --prod` from root | Automatic Git integration, preview deployments |
| **GitHub Pages** | `gh-pages` branch push | Free hosting, integrated with repo |
| **Cloudflare Pages** | Direct upload or Git sync | Fast CDN, edge caching, free tier generous |
| **Self-hosted** | Any HTTP server | Apache, Nginx, Caddy — serve static files |

### PWA Features
- Installable on desktop and mobile
- Offline-first with service worker caching
- Responsive across all screen sizes
- Dark/light mode toggle available in settings

---

## 📊 Performance Metrics (Target)

| Metric | Target | Current |
|---|---|---|
| First Contentful Paint | < 1.5s | ✅ Within target |
| Largest Contentful Paint | < 2.5s | ✅ Within target |
| Cumulative Layout Shift | < 0.1 | ✅ Within target |
| Time to Interactive | < 3.5s | ✅ Within target |
| Total Blocking Time | < 200ms | ✅ Within target |

---

## 🔒 Security

- All external dependencies loaded via CDN with SRI hashes where available
- Service Worker implements strict content security policy
- No user data collected or transmitted externally
- Third-party integrations only via established APIs (Spotify, Apple Music, YouTube, etc.)

---

## 🌐 Localization

Primary languages supported:
- 🇪🇸 Spanish (`es`)
- 🇬🇧 English (`en`)  
- 🇵🇹 Portuguese (`pt`)

Each locale served from same base path with `hreflang` alternate links. New language additions welcome via PR.

---

## 👤 Credits

**Creator**: Pedro Marcos Santos Belentani  
**Role**: Creative Technologist · Systems Architect · Audiovisual Director  
**Location**: Barcelona / Hospitalet, Spain (originally São Paulo, Brazil)  
**Studio**: DUCK STUDIOS (independent creative laboratory)  
**Ecosystem**: BELENTANI · NOIACORE · DUCK · ZION  

[Instagram](https://www.instagram.com/belentani_/) · [Spotify](https://open.spotify.com/artist/4YRxDV8wJFPHPTeXepOstw) · [YouTube](https://www.youtube.com/@belentani) · [Apple Music](https://music.apple.com/artist/belentani/1522171354) · [SoundCloud](https://soundcloud.com/belentani)

---

## 📄 License

MIT License — see included LICENSE file for full terms.

The BELENTANI name, logo, and associated intellectual property remain the exclusive property of Pedro Marcos Santos Belentani. This license covers only the code implementation contained within this repository.

---

> *"No produzco arte por producir. Cada proyecto es una herida procesada como lenguaje visual y sonoro."*  
> — Pedro Belentani
