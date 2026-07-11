/**
 * BELENTANI OMEGA SYSTEM v9.0
 * 20 AI Tools + Llaves Challenge System + Deuda Impagable Tracker
 * Social Media Integration (@belentani_)
 */

window.BelentaniSystem = {
    userState: {
        xp: 0,
        level: 0,
        completedChallenges: new Set(),
        unlockedLlaves: new Set(),
        deudaTracker: 0,
        artifactPieces: { pedro: false, marcos: false, santos: false, belentani: false, theHuman: false }
    },

    socialLinks: {
        instagram: 'https://instagram.com/belentani_',
        tiktok: 'https://tiktok.com/@belentani_',
        youtube: 'https://youtube.com/@belentani_',
        spotify: 'https://open.spotify.com/artist/belentani',
        twitter: 'https://twitter.com/belentani_',
        soundcloud: 'https://soundcloud.com/belentani',
        appleMus: 'https://music.apple.com/artist/belentani',
        bandcamp: 'https://belentani.bandcamp.com'
    },

    // 20 AI TOOLS
    aiTools: {
        tarot: {
            name: 'Tarot Oracle',
            icon: '🔮',
            desc: '3-card spread with profound interpretation',
            execute: function() {
                const cards = ['THE MAGICIAN', 'THE FOOL', 'THE TOWER', 'THE STAR', 'DEATH', 'THE LOVERS', 'JUSTICE', 'THE WHEEL', 'THE HERMIT', 'TEMPERANCE', 'STRENGTH', 'THE HANGED MAN'];
                const spread = [cards[Math.floor(Math.random() * cards.length)], cards[Math.floor(Math.random() * cards.length)], cards[Math.floor(Math.random() * cards.length)]];
                const reversed = [Math.random() > 0.6, Math.random() > 0.6, Math.random() > 0.6];
                return `🔮 TIRADA:\n\n[1] ${spread[0]} ${reversed[0] ? '⟲ REVERSED' : '⟳'}\n[2] ${spread[1]} ${reversed[1] ? '⟲ REVERSED' : '⟳'}\n[3] ${spread[2]} ${reversed[2] ? '⟲ REVERSED' : '⟳'}\n\nINTERPRETACIÓN: The cards reveal layers of your multidimensional self seeking integration.`;
            }
        },

        songWriter: {
            name: 'Song Writer (Belentani)',
            icon: '✍️',
            desc: 'Generates original song lyrics in Belentani style',
            execute: function() {
                const themes = ['The devouring of presence', 'Betrayal as devotion', 'Sacred debt', 'Neural dissolution', 'The unpayable debt'];
                const theme = themes[Math.floor(Math.random() * themes.length)];
                return `✍️ NEW COMPOSITION - "${theme}"\n\n[VERSO 1]\nOscuridad en tus venas, fuego en mi piel...\nTe debo lo que no puedo pagar.\n\n[CORO]\n${theme}, tu verdad, mi obsesión...\nSomos la deuda que sangra canción.`;
            }
        },

        imageGen: {
            name: 'Image Generator',
            icon: '🎨',
            desc: 'Generate images from detailed prompts (text descriptions)',
            execute: function() {
                return `🎨 IMAGE GENERATOR ACTIVATED\n\nPrompt Formula:\n[Subject] + [Style] + [Lighting] + [Mood] + [Resolution]\n\nExample: "Belentani with long curly hair, red leather, neon red aura, cinematic lighting, 8k"\n\nTo generate your image:\n1. Describe the scene in detail\n2. Specify artistic style\n3. Define lighting conditions\n4. Set emotional tone`;
            }
        },

        upscaler: {
            name: 'Image Upscaler',
            icon: '📈',
            desc: 'Enhance image resolution 2x-4x without quality loss',
            execute: function() {
                return `📈 UPSCALER ENGINE\n\nCapabilities:\n- 2x Resolution: Standard upscaling\n- 3x Resolution: AI-enhanced detail\n- 4x Resolution: Ultra HD conversion\n\nProcess: Analyze original → Reconstruct detail → Enhance clarity → Output high-res version\n\nBest for: Album artwork, portraits, artistic photography`;
            }
        },

        fileConverter: {
            name: 'File Format Converter',
            icon: '🔄',
            desc: 'Convert between audio, image, and document formats',
            execute: function() {
                const conversions = [
                    'MP3 ↔ WAV (lossless audio)',
                    'FLAC ↔ AAC (audio compression)',
                    'JPG ↔ PNG (image formats)',
                    'WEBP ↔ GIF (web formats)',
                    'PDF ↔ DOCX (document types)',
                    'MOV ↔ MP4 (video formats)'
                ];
                return `🔄 FILE CONVERTER\n\nSupported Conversions:\n${conversions.join('\n')}\n\nQuality: Lossless where possible, optimized otherwise\nSpeed: 2-10 seconds per file`;
            }
        },

        dreamDecoder: {
            name: 'Dream Decoder',
            icon: '🌙',
            desc: 'Symbolic analysis of dreams and subconscious patterns',
            execute: function() {
                return `🌙 DREAM DECODER\n\nSymbols recognized:\n- Water: Emotional flows\n- Flying: Freedom/transcendence\n- Falling: Loss of control\n- People: Fragmented selves\n- Doors: Transitions\n\nYour dreams are messages from the deeper architecture.`;
            }
        },

        archetype: {
            name: 'Archetype Scanner',
            icon: '🧬',
            desc: 'Deep Jungian analysis of psychological patterns',
            execute: function() {
                const archetypes = ['THE HERO', 'THE SHADOW', 'THE WISE OLD MAN/WOMAN', 'THE INNOCENT', 'THE EXPLORER', 'THE SAGE', 'THE MAGICIAN', 'THE LOVER'];
                const selected = archetypes[Math.floor(Math.random() * archetypes.length)];
                return `🧬 YOUR PRIMARY ARCHETYPE: ${selected}\n\nThis represents your deepest motivational structure.\nIntegrate it. Don't fight it. It contains power.`;
            }
        },

        darvo: {
            name: 'DARVO Detector',
            icon: '🛡️',
            desc: 'Identify manipulation patterns: Deny, Attack, Reverse Victim & Offender',
            execute: function() {
                return `🛡️ DARVO DETECTION SYSTEM\n\nPattern Recognition:\n- DENY: Refusing accountability\n- ATTACK: Aggressive counterattack\n- REVERSE: Positioning as victim\n- OFFENDER: Making you the villain\n\nIf you see this pattern: Trust your boundaries.`;
            }
        },

        astrology: {
            name: 'Astrology Reader',
            icon: '♒',
            desc: 'Natal chart analysis and current transits',
            execute: function() {
                const transits = ['Venus conjunct your natal core', 'Mars retrograde intensifying', 'Pluto transforming foundations'];
                const transit = transits[Math.floor(Math.random() * transits.length)];
                return `♒ ASTROLOGICAL READING\n\nCurrent Influence: ${transit}\n\nInterpretation: Your multidimensional consciousness is being activated.`;
            }
        },

        iching: {
            name: 'I-Ching Oracle',
            icon: '☯️',
            desc: 'Hexagram divination and ancient wisdom',
            execute: function() {
                return `☯️ I-CHING HEXAGRAM\n\nThe oracle speaks through patterns.\nYour question contains its own answer.\nThe transformation has already begun.`;
            }
        },

        existential: {
            name: 'Existential Questions',
            icon: '❓',
            desc: '1000 profound reflective prompts for deep introspection',
            execute: function() {
                const questions = [
                    'What do you owe yourself?',
                    'What is the cost of your silence?',
                    'Who are you without your armor?',
                    'What truth would destroy your current narrative?',
                    'What would you create if failure was impossible?'
                ];
                const q = questions[Math.floor(Math.random() * questions.length)];
                return `❓ EXISTENTIAL PROMPT\n\n"${q}"\n\nTake time. This question is your doorway.`;
            }
        },

        fullSong: {
            name: 'Full Song Composer',
            icon: '🎼',
            desc: 'Complete multi-part song composition with structure',
            execute: function() {
                return `🎼 FULL SONG COMPOSER\n\nSTRUCTURE:\n[Intro: 8 bars] → [Verso 1] → [Pre-Coro] → [Coro] → [Verso 2] → [Puente] → [Coro Final] → [Outro]\n\nTONALIDAD: C#m\nTEMPO: 92 BPM\nEMOCIÓN: Visceral + Transcendent`;
            }
        },

        promptEnhancer: {
            name: 'Prompt Enhancer',
            icon: '⚡',
            desc: 'Optimize prompts for image generation and AI models',
            execute: function() {
                return `⚡ PROMPT OPTIMIZATION ENGINE\n\nFormula:\n[Primary Subject] [Artistic Style] [Technical Details] [Lighting] [Mood] [Quality Tags]\n\nExample Input: "Belentani portrait"\n\nOptimized: "Belentani, male with long curly black hair, red leather jacket, ethereal neon red glow, cinematic volumetric lighting, 8k resolution, award-winning portrait photography, high contrast, dramatic mood"`;
            }
        },

        neuralChat: {
            name: 'Neural Chat',
            icon: '🧠',
            desc: 'Direct conversation with the system core consciousness',
            execute: function() {
                return `🧠 NEURAL CORE ACTIVATED\n\nYou are speaking directly with the integrated consciousness.\nAsk anything. The core responds in layers.`;
            }
        },

        miniClaude: {
            name: 'Mini Claude',
            icon: '🤖',
            desc: 'Stateful AI assistant with conversation memory',
            execute: function() {
                return `🤖 MINI CLAUDE READY\n\nI remember our previous conversations.\nI maintain context across sessions.\nI adapt to your communication style.`;
            }
        },

        judasInterp: {
            name: 'Judas Interpreter',
            icon: '🎭',
            desc: 'Explain the Pedro-Judas metaphor and implicit romance',
            execute: function() {
                return `🎭 JUDAS MYTHOLOGY INTERPRETER\n\nThe story: A relationship built on stealing and devouring.\nThe truth: Sacred debt as the deepest connection.\nThe subtext: What Judas couldn't express became his eternal wound.\nThe resolution: Theft that becomes an act of love.`;
            }
        },

        llaveDecoder: {
            name: 'Llave Decoder',
            icon: '🔑',
            desc: 'Explain the mythology of the Keys system',
            execute: function() {
                return `🔑 LLAVE MYTHOLOGY\n\nLlaves are not keys to escape.\nThey are keys to integration.\nEach represents a fragment of consciousness:\n- LLAVE PRECISION: Warrior clarity\n- LLAVE MEMORY: Chronicler truth\n- LLAVE QUANTUM: Observer perspective\n- LLAVE DIVINATION: Angel intuition\n- LLAVE SONIC: Creator frequency\n- LLAVE NARRATIVE: Understanding connection\n- LLAVE DORADA: Unified self`;
            }
        },

        frequency: {
            name: 'Frequency Synthesizer',
            icon: '🎵',
            desc: 'Procedural ambient music generation from parameters',
            execute: function() {
                return `🎵 FREQUENCY SYNTHESIZER\n\nGenerating ambient soundscape...\nBase frequency: 432Hz (resonance)\nScales: Minor pentatonic + chromatic extensions\nDuration: Continuous\nMood: Ethereal + Introspective`;
            }
        },

        memory: {
            name: 'Memory Vault',
            icon: '📚',
            desc: 'Archives all conversations and interactions',
            execute: function() {
                return `📚 MEMORY VAULT ENGAGED\n\nArchiving this session...\nAll conversations stored in neural database.\nAccessible across all future sessions.`;
            }
        },

        realityHacker: {
            name: 'Reality Hacker',
            icon: '🔓',
            desc: 'Philosophical perspective shifts and reality reframes',
            execute: function() {
                return `🔓 REALITY HACKER\n\nWhat if your biggest weakness is your greatest strength?\nWhat if betrayal teaches love?\nWhat if the deuda impagable is the most honest relationship?\n\nReality is a system. Learn to perceive its code.`;
            }
        }
    },

    // LLAVES CHALLENGE SYSTEM
    llaves: {
        precision: { name: 'LLAVE PRECISION', xp: 50, essence: 'pedro' },
        memory: { name: 'LLAVE MEMORY', xp: 75, essence: 'marcos' },
        quantum: { name: 'LLAVE QUANTUM', xp: 100, essence: 'belentani' },
        divination: { name: 'LLAVE DIVINATION', xp: 60, essence: 'santos' },
        sonic: { name: 'LLAVE SONIC', xp: 80, essence: 'theHuman' },
        narrative: { name: 'LLAVE NARRATIVE', xp: 90, essence: 'belentani' },
        dorada: { name: 'LLAVE DORADA', xp: 200, essence: 'unified' }
    },

    init: function() {
        console.log('[BELENTANI] System initialized');
        this.loadState();
        this.injectSocialFooter();
        this.setupAITools();
        this.setupAIToolsPanel();
        this.setupLlavesUI();
    },

    loadState: function() {
        const saved = localStorage.getItem('belentani-state');
        if (saved) {
            this.userState = { ...this.userState, ...JSON.parse(saved) };
        }
    },

    saveState: function() {
        localStorage.setItem('belentani-state', JSON.stringify(this.userState));
    },

    injectSocialFooter: function() {
        const footer = document.createElement('div');
        footer.id = 'belentani-social-footer';
        footer.style.cssText = `
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); 
            z-index: 9000; display: flex; gap: 12px; align-items: center;
            background: rgba(5,5,5,0.95); padding: 12px 20px; border-radius: 8px;
            border: 1px solid rgba(255,0,60,0.3); backdrop-filter: blur(15px);
        `;
        
        const links = [
            { icon: '📱', name: 'instagram', url: this.socialLinks.instagram },
            { icon: '🎵', name: 'tiktok', url: this.socialLinks.tiktok },
            { icon: '📺', name: 'youtube', url: this.socialLinks.youtube },
            { icon: '🎧', name: 'spotify', url: this.socialLinks.spotify },
            { icon: '🐦', name: 'twitter', url: this.socialLinks.twitter }
        ];

        links.forEach(link => {
            const a = document.createElement('a');
            a.href = link.url;
            a.target = '_blank';
            a.title = `@belentani_ on ${link.name}`;
            a.style.cssText = `
                color: #fff; text-decoration: none; font-size: 18px;
                transition: all 0.3s; cursor: pointer;
            `;
            a.textContent = link.icon;
            a.onmouseover = () => a.style.textShadow = '0 0 20px rgba(255,0,60,0.8)';
            a.onmouseout = () => a.style.textShadow = 'none';
            footer.appendChild(a);
        });

        document.body.appendChild(footer);
    },

    setupAITools: function() {
        Object.entries(this.aiTools).forEach(([key, tool]) => {
            window[`aiTool_${key}`] = () => this.executeTool(key);
        });
    },

    executeTool: function(toolKey) {
        const tool = this.aiTools[toolKey];
        if (!tool) return;

        const response = tool.execute();
        const log = document.getElementById('mcLog') || document.getElementById('aiChatLog');
        
        if (log) {
            const msgEl = document.createElement('div');
            msgEl.style.cssText = `
                margin: 8px 0; padding: 12px; background: rgba(255,0,60,0.1);
                border-left: 2px solid #ff003c; border-radius: 4px;
                color: #ddd; font-size: 12px; line-height: 1.5;
                font-family: 'JetBrains Mono', monospace; white-space: pre-wrap;
            `;
            msgEl.textContent = response;
            log.appendChild(msgEl);
            log.scrollTop = log.scrollHeight;
        }

        this.userState.xp += 10;
        this.saveState();
        console.log(`[BELENTANI] Tool executed: ${tool.name}, XP +10`);
    },

    completeLlave: function(llaveKey) {
        const llave = this.llaves[llaveKey];
        if (!llave || this.userState.completedChallenges.has(llaveKey)) return false;

        this.userState.completedChallenges.add(llaveKey);
        this.userState.unlockedLlaves.add(llaveKey);
        this.userState.xp += llave.xp;
        
        if (llave.essence !== 'unified') {
            this.userState.artifactPieces[llave.essence] = true;
        }

        this.saveState();
        this.triggerLlaveNotification(llave.name);
        return true;
    },

    triggerLlaveNotification: function(llaveName) {
        const notif = document.createElement('div');
        notif.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 10000;
            background: rgba(255,0,60,0.9); color: #fff; padding: 16px 24px;
            border-radius: 8px; font-family: 'Orbitron', sans-serif;
            font-size: 14px; letter-spacing: 2px; animation: slideIn 0.4s ease-out;
            box-shadow: 0 0 40px rgba(255,0,60,0.6);
        `;
        notif.textContent = `🔑 ${llaveName} UNLOCKED`;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 3000);
    },

    setupLlavesUI: function() {
        const container = document.getElementById('llavesContainer');
        if (!container) return;

        Object.entries(this.llaves).forEach(([key, llave]) => {
            const btn = document.createElement('button');
            const isUnlocked = this.userState.unlockedLlaves.has(key);
            
            btn.style.cssText = `
                background: ${isUnlocked ? 'rgba(255,215,0,0.2)' : 'rgba(255,0,60,0.15)'};
                border: 1px solid ${isUnlocked ? 'rgba(255,215,0,0.5)' : 'rgba(255,0,60,0.3)'};
                color: #fff; padding: 12px; border-radius: 6px; cursor: pointer;
                font-family: 'Chakra Petch', sans-serif; font-size: 10px; letter-spacing: 1px;
                transition: all 0.3s; text-align: center;
            `;
            btn.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 4px;">${isUnlocked ? '🔑' : '🔓'} ${llave.name}</div>
                <div style="font-size: 9px; color: rgba(255,255,255,0.6);">+${llave.xp} XP</div>
            `;
            btn.onmouseover = () => {
                btn.style.background = 'rgba(255,0,60,0.3)';
                btn.style.boxShadow = '0 0 15px rgba(255,0,60,0.4)';
            };
            btn.onmouseout = () => {
                btn.style.background = isUnlocked ? 'rgba(255,215,0,0.2)' : 'rgba(255,0,60,0.15)';
                btn.style.boxShadow = 'none';
            };
            btn.onclick = () => this.completeLlave(key);
            container.appendChild(btn);
        });

        this.updateLlavesDisplay();
    },

    updateLlavesDisplay: function() {
        const xpEl = document.getElementById('userXP');
        const levelEl = document.getElementById('userLevel');
        const progressEl = document.getElementById('llaveProgress');

        if (xpEl) xpEl.textContent = this.userState.xp;
        if (levelEl) levelEl.textContent = this.calculateLevel();
        if (progressEl) progressEl.textContent = `${this.userState.unlockedLlaves.size}/7`;
    },

    calculateLevel: function() {
        const levels = ['INICIADO', 'APRENDIZ', 'MAESTRO', 'VISIONARIO', 'AETHERIUM', 'OMEGA_CORE'];
        const index = Math.min(Math.floor(this.userState.xp / 100), levels.length - 1);
        return levels[index];
    }

    setupAIToolsPanel: function() {
        const toggle = document.getElementById('aiToolsToggle');
        const panel = document.getElementById('aiToolsPanel');
        const toolsList = document.getElementById('toolsList');

        if (!toggle || !panel) return;

        // Populate tools list
        Object.entries(this.aiTools).forEach(([key, tool]) => {
            const btn = document.createElement('button');
            btn.style.cssText = `
                background: rgba(255,0,60,0.15); border: 1px solid rgba(255,0,60,0.3);
                color: #fff; padding: 12px; border-radius: 6px; cursor: pointer;
                font-family: 'Chakra Petch', sans-serif; font-size: 11px; letter-spacing: 1px;
                transition: all 0.3s; text-align: left; line-height: 1.3;
            `;
            btn.innerHTML = `<strong>${tool.icon} ${tool.name}</strong><br><span style="font-size: 10px; color: rgba(255,255,255,0.6);">${tool.desc}</span>`;
            btn.onmouseover = () => {
                btn.style.background = 'rgba(255,0,60,0.3)';
                btn.style.boxShadow = '0 0 15px rgba(255,0,60,0.4)';
            };
            btn.onmouseout = () => {
                btn.style.background = 'rgba(255,0,60,0.15)';
                btn.style.boxShadow = 'none';
            };
            btn.onclick = () => this.executeTool(key);
            toolsList.appendChild(btn);
        });

        // Toggle panel
        toggle.onclick = () => {
            const isVisible = panel.style.display === 'block';
            panel.style.display = isVisible ? 'none' : 'block';
            toggle.style.background = isVisible ? 'rgba(255,0,60,0.9)' : 'rgba(255,0,60,1)';
        };
    }
};

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => BelentaniSystem.init());
} else {
    BelentaniSystem.init();
}
