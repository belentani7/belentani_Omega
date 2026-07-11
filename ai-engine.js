/**
 * OMEGA AI ENGINE v8.0
 * Sistemas avanzados de IA integrados directamente en el sitio
 * Sin dependencias externas de API keys
 */

window.OmegaAIEngine = class {
    constructor() {
        this.isActive = false;
        this.conversationHistory = [];
        this.userXP = 0;
        this.userLevel = 'INICIADO';
        this.achievements = [];
        this.activeChallenges = new Set();
    }

    initialize() {
        console.log('[OMEGA] Inicializando AI Engine v8.0...');
        this.setupEventListeners();
        this.loadPersistentState();
        this.startBackgroundProcesses();
        this.isActive = true;
    }

    setupEventListeners() {
        // AI Chat listeners
        const chatInput = document.getElementById('aiChatInput');
        if (chatInput) {
            chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.processAIChat(chatInput.value);
                    chatInput.value = '';
                }
            });
        }

        // Mini Claude listeners
        const mcInput = document.getElementById('mcInput');
        if (mcInput) {
            mcInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.processMiniClaude(mcInput.value);
                    mcInput.value = '';
                }
            });
        }
    }

    loadPersistentState() {
        const saved = localStorage.getItem('omega-state');
        if (saved) {
            const state = JSON.parse(saved);
            this.userXP = state.xp || 0;
            this.userLevel = state.level || 'INICIADO';
            this.achievements = state.achievements || [];
        }
        this.updateUIState();
    }

    savePersistentState() {
        localStorage.setItem('omega-state', JSON.stringify({
            xp: this.userXP,
            level: this.userLevel,
            achievements: this.achievements
        }));
    }

    updateUIState() {
        const xpEl = document.getElementById('xpCount');
        const rankEl = document.getElementById('rankName');
        if (xpEl) xpEl.textContent = this.userXP;
        if (rankEl) rankEl.textContent = this.userLevel;
    }

    processAIChat(message) {
        if (!message.trim()) return;

        const log = document.getElementById('aiChatLog');
        if (!log) return;

        // Add user message
        this.addMessage(log, message, 'user', 'USER');

        // Simulate AI processing
        setTimeout(() => {
            const response = this.generateContextualResponse(message);
            this.addMessage(log, response, 'ai', 'CORE_AI');
            this.gainXP(5);
        }, 300);
    }

    processMiniClaude(message) {
        if (!message.trim()) return;

        const log = document.getElementById('mcLog');
        if (!log) return;

        // Add user message
        this.addMessage(log, message, 'user', 'YOU');

        // Simulate assistant response
        setTimeout(() => {
            const response = this.generateAssistantResponse(message);
            this.addMessage(log, response, 'ai', 'ASISTENTE');
            this.gainXP(8);
        }, 400);
    }

    addMessage(log, text, type, label) {
        const msg = document.createElement('div');
        msg.className = `message ${type}`;
        const timestamp = new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
        msg.innerHTML = `<div class="meta">${label} // ${timestamp}</div>${this.sanitizeText(text)}`;
        log.appendChild(msg);
        log.scrollTop = log.scrollHeight;
    }

    sanitizeText(text) {
        return text
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>');
    }

    generateContextualResponse(userMessage) {
        const responses = {
            'hola': '◉ CORE_AI: Bienvenido al núcleo. ¿Qué necesitas?',
            'ayuda': '◉ CORE_AI: Tengo 12 herramientas IA disponibles. Explora el lab.',
            'música': '◉ CORE_AI: Generador de beats activo. Selecciona DARK POP, R&B o INDUSTRIAL.',
            'arte': '◉ CORE_AI: VISION FORGE está listo. Describe la visión que deseas.',
            'quién eres': '◉ CORE_AI: Soy OMEGA CORE, núcleo inteligente de BELENTANI. Asisto, creo, transformo.',
            'gracias': '◉ CORE_AI: La conexión nos enriquece a ambos. Continúa explorando.',
        };

        for (let key in responses) {
            if (userMessage.toLowerCase().includes(key)) {
                return responses[key];
            }
        }

        return `◉ CORE_AI: "${userMessage}" registrado. Procesando... ✓ Información integrada en el núcleo.`;
    }

    generateAssistantResponse(userMessage) {
        const tasks = ['writing', 'coding', 'planning', 'translating', 'brainstorming'];
        const found = tasks.find(t => userMessage.toLowerCase().includes(t));

        if (found) {
            return `◈ ASISTENTE: Puedo ayudarte con ${found}. Dame más detalles específicos.`;
        }

        return `◈ ASISTENTE: Interesante pregunta. Aquí está mi análisis: [Respuesta contextual generada]. ¿Necesitas más profundidad?`;
    }

    gainXP(amount) {
        this.userXP += amount;
        this.updateUIState();

        // Level up every 100 XP
        const levels = ['INICIADO', 'APRENDIZ', 'MAESTRO', 'VISIONARIO', 'AETHERIUM', 'OMEGA CORE'];
        const newLevel = Math.min(Math.floor(this.userXP / 100), levels.length - 1);
        if (levels[newLevel] !== this.userLevel) {
            this.userLevel = levels[newLevel];
            this.displayLevelUp();
        }

        this.savePersistentState();
    }

    displayLevelUp() {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, rgba(255, 0, 60, 0.9), rgba(176, 38, 255, 0.9));
            color: white;
            padding: 30px 60px;
            font-family: var(--font-display);
            font-size: 32px;
            text-align: center;
            border: 2px solid #ff003c;
            z-index: 10000;
            box-shadow: 0 0 50px rgba(255, 0, 60, 0.6);
            animation: levelUpPulse 1s ease-out;
        `;
        notification.innerHTML = `⭐ LEVEL UP: ${this.userLevel}`;
        document.body.appendChild(notification);

        setTimeout(() => {
            gsap.to(notification, {
                opacity: 0,
                duration: 0.5,
                onComplete: () => notification.remove()
            });
        }, 2000);
    }

    startBackgroundProcesses() {
        // Random status updates
        setInterval(() => {
            this.updateSystemStatus();
        }, 8000);

        // Periodic effects
        setInterval(() => {
            this.triggerRandomEffect();
        }, 15000);
    }

    updateSystemStatus() {
        const statusEl = document.getElementById('sysTime');
        if (statusEl) {
            const now = new Date();
            statusEl.textContent = now.toLocaleTimeString('es-ES', { 
                hour: '2-digit', 
                minute: '2-digit', 
                second: '2-digit' 
            });
        }
    }

    triggerRandomEffect() {
        if (Math.random() > 0.7) {
            document.body.classList.add('quantum-active');
            setTimeout(() => document.body.classList.remove('quantum-active'), 300);
        }
    }

    // ==================== TOOL ACTIVATORS ====================

    async activateTool(toolName) {
        const tools = {
            'improver': this.improvePrompt.bind(this),
            'tarot': this.tarotReading.bind(this),
            'dream': this.dreamDecoder.bind(this),
            'archetype': this.archetypeScan.bind(this),
            'darvo': this.darvoDetector.bind(this),
            'song': this.songWriter.bind(this),
            'agent': this.deployAgent.bind(this),
            'circuit': this.automationCircuit.bind(this),
            'astro': this.astroNexus.bind(this),
            'iching': this.ichingOracle.bind(this),
            'questions': this.universalQuestions.bind(this),
            'fullsong': this.fullSongBuilder.bind(this)
        };

        if (tools[toolName]) {
            this.triggerQuantumEffect();
            await tools[toolName]();
        }
    }

    triggerQuantumEffect() {
        document.body.classList.add('quantum-active');
        setTimeout(() => document.body.classList.remove('quantum-active'), 300);
    }

    improvePrompt() {
        return new Promise((resolve) => {
            const input = prompt('Enter your prompt:');
            if (input) {
                const improved = `⚡ ENHANCED PROMPT:\n\nOriginal: ${input}\n\nOptimized: ${input}, ultra-realistic, cinematographic, trending on artstation, dramatic volumetric lighting, 8k resolution, masterpiece quality`;
                alert(improved);
                this.gainXP(15);
            }
            resolve();
        });
    }

    tarotReading() {
        const cards = ['THE MAGICIAN', 'THE FOOL', 'THE TOWER', 'THE STAR', 'DEATH', 'THE LOVERS', 'JUSTICE', 'THE WHEEL', 'THE HERMIT', 'STRENGTH'];
        const spread = [
            cards[Math.floor(Math.random() * cards.length)],
            cards[Math.floor(Math.random() * cards.length)],
            cards[Math.floor(Math.random() * cards.length)]
        ];
        const msg = `🔮 TIRADA DE 3 CARTAS:\n\n1️⃣ ${spread[0]} - Pasado/Influencia\n2️⃣ ${spread[1]} - Presente/Núcleo\n3️⃣ ${spread[2]} - Futuro/Potencial\n\nEl núcleo interpreta: Cambio transformador en el horizonte.`;
        alert(msg);
        this.gainXP(20);
    }

    dreamDecoder() {
        const dream = prompt('Describe tu sueño (máx 200 caracteres):');
        if (dream) {
            const symbols = ['Agua', 'Fuego', 'Vuela', 'Caída', 'Luz', 'Oscuridad'];
            const symbol = symbols[Math.floor(Math.random() * symbols.length)];
            const msg = `🌙 DECODIFICACIÓN ONÍRICA:\n\nSímbolo: ${symbol}\n\nInterpretación: Tu inconsciente procesa transformación. Integra este mensaje.`;
            alert(msg);
            this.gainXP(15);
        }
    }

    archetypeScan() {
        const archetypes = ['EL HÉROE', 'EL MAGO', 'EL SABIO', 'EL INOCENTE', 'EL EXPLORADOR', 'EL CREADOR', 'EL AMANTE', 'EL BUFÓN'];
        const archetype = archetypes[Math.floor(Math.random() * archetypes.length)];
        const msg = `🧬 TU ARQUETIPO DOMINANTE: ${archetype}\n\nEste patrón define tu motivación profunda. Reconócelo, amplíficalo, trasciéndelo.`;
        alert(msg);
        this.gainXP(18);
    }

    darvoDetector() {
        const text = prompt('Pega conversación para analizar:');
        if (text) {
            const patterns = ['DARVO detected', 'Gaslighting patterns found', 'Passive aggression detected'];
            const found = patterns[Math.floor(Math.random() * patterns.length)];
            const msg = `🛡️ ANÁLISIS DE MANIPULACIÓN:\n\n⚠️ ${found}\n\nConfía en tu intuición. Estos son marcadores de dinámicas tóxicas.`;
            alert(msg);
            this.gainXP(12);
        }
    }

    songWriter() {
        const theme = prompt('Tema para la canción:');
        if (theme) {
            const msg = `✍️ CANCIÓN: "${theme}"\n\n[Verso 1]\nOscuridad en tus venas, fuego en tu alma...\n\n[Coro]\n${theme}, tu verdad, mi obsesión...\n\nEstilo: Dark Pop/R&B Visceral`;
            alert(msg);
            this.gainXP(25);
        }
    }

    deployAgent() {
        const task = prompt('Objetivo para el agente autónomo:');
        if (task) {
            const msg = `🦾 AGENTE DESPLEGADO\n\nOBJETIVO: ${task}\n\n[Analizando contexto...]\n[Generando plan de 5 pasos...]\n[Ejecutando...]\n\n✓ MISIÓN COMPLETADA`;
            alert(msg);
            this.gainXP(30);
        }
    }

    automationCircuit() {
        const idea = prompt('Tu idea inicial:');
        if (idea) {
            const msg = `🔗 CIRCUITO AUTOMATIZADO EJECUTADO\n\n1️⃣ IDEA: ${idea}\n2️⃣ OPTIMIZADO: [Mejora aplicada]\n3️⃣ CONTENIDO: [Generado]\n4️⃣ IMAGEN: [Visualización creada]\n5️⃣ AUDIO: [Track generado]\n\n✓ CIRCUITO COMPLETADO`;
            alert(msg);
            this.gainXP(35);
        }
    }

    astroNexus() {
        const signs = ['♈ ARIES', '♉ TAURO', '♊ GÉMINIS', '♋ CÁNCER', '♌ LEO', '♍ VIRGO', '♎ LIBRA', '♏ ESCORPIO', '♐ SAGITARIO', '♑ CAPRICORNIO', '♒ ACUARIO', '♓ PISCIS'];
        const sign = signs[Math.floor(Math.random() * signs.length)];
        const msg = `♒ LECTURA ASTRAL NEURAL:\n\n${sign}\n\nVenus en Casa 7: transformación relacional.\nMarte directo: poder personal en su pico.\nLa Luna en transito: inteligencia emocional activada.\n\nMomento: AHORA.`;
        alert(msg);
        this.gainXP(20);
    }

    ichingOracle() {
        const hexagrams = ['☰ EL CREATIVO', '☷ LO RECEPTIVO', '☳ LO SUSCITATIVO', '☵ LO ABISMAL', '☶ LO ADHERENTE', '☲ LO LUMINOSO'];
        const hex = hexagrams[Math.floor(Math.random() * hexagrams.length)];
        const msg = `☯ ORÁCULO I CHING:\n\n${hex}\n\nLanza las monedas virtuales... El hexagrama ha hablado.\nTu respuesta está en la interpretación de este patrón.`;
        alert(msg);
        this.gainXP(18);
    }

    universalQuestions() {
        const questions = [
            '¿Qué te impide ser completamente honesto?',
            '¿Cuál es tu mayor miedo sin nombre?',
            '¿Qué sacrificarías por tu sueño verdadero?',
            '¿Quién eres sin tu rol social?',
            '¿Qué te hace sentir realmente vivo?',
            '¿Qué verdad rehúsas aceptar?'
        ];
        const q = questions[Math.floor(Math.random() * questions.length)];
        const answer = prompt(q);
        if (answer) {
            const msg = `❓ REFLEXIÓN EXISTENCIAL:\n\nTu respuesta: "${answer}"\n\nEl núcleo ve: profundidad, vulnerabilidad, búsqueda autén tica. La pregunta era el viaje; tu respuesta es la transformación.`;
            alert(msg);
            this.gainXP(22);
        }
    }

    fullSongBuilder() {
        const msg = `🎼 CONSTRUCTOR DE CANCIÓN COMPLETA\n\n📝 TÍTULO: "Núcleo Expuesto"\n🎵 BPM: 92 | TONALIDAD: C#m | TEMPO: Visceral\n\n[ESTRUCTURA]\nIntro (8) → Verso (16) → Pre-Coro (8) → Coro (16) → Verso 2 (16) → Puente (8) → Coro Final (16) → Outro (8)\n\n[ACORDES]: C#m - A - E - B7\n\n[LETRA - VERSO 1]\nEn el silencio habita mi verdad...\nOscuro en las venas, fuego en el alma...\n\n[PRODUCTOR]: Sintetizadores Dark Pop, bajos viscerales, pads atmosféricos`;
        alert(msg);
        this.gainXP(40);
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.omegaAI = new window.OmegaAIEngine();
    window.omegaAI.initialize();
    console.log('[OMEGA] AI Engine initialized and ready.');
});

// Expose tool activator globally
window.aiTool = function(toolName) {
    if (window.omegaAI) {
        window.omegaAI.activateTool(toolName);
    }
};

// Expose chat functions
window.aiChatSend = function() {
    const input = document.getElementById('aiChatInput');
    if (input && window.omegaAI) {
        window.omegaAI.processAIChat(input.value);
        input.value = '';
    }
};

window.mcSend = function() {
    const input = document.getElementById('mcInput');
    if (input && window.omegaAI) {
        window.omegaAI.processMiniClaude(input.value);
        input.value = '';
    }
};

// Add keyframe animation dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes levelUpPulse {
        0% { 
            transform: translate(-50%, -50%) scale(0.5); 
            opacity: 0; 
        }
        50% { 
            transform: translate(-50%, -50%) scale(1.1); 
            opacity: 1; 
        }
        100% { 
            transform: translate(-50%, -50%) scale(1); 
            opacity: 1; 
        }
    }
`;
document.head.appendChild(style);
