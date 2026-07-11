# 🚀 BELENTANI OMEGA CORE v8.0 - GUÍA DE INSTALACIÓN

## ⚡ QUICK START

### Opción 1: Directamente en navegador (RECOMENDADO)

1. Abre el archivo `index.html` en tu navegador
2. ¡Listo! El sitio carga automáticamente

```bash
# En tu máquina local:
python3 -m http.server 3000
# Luego abre: http://localhost:3000
```

### Opción 2: Desplegar en Vercel

```bash
# Si tienes git + Vercel CLI:
vercel
```

### Opción 3: Servir con Node.js

```bash
npm install -g http-server
http-server
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
belentani_Omega/
├── index.html              # HTML principal (190 KB)
├── styles-enhanced.css     # Estilos avanzados (6.5 KB)
├── ai-engine.js            # Motor IA (16 KB)
├── css/
│   ├── living-glass.css    # Estilos originales
│   └── creative-os.css     # Estilos creativos
├── IMPROVEMENTS.md         # Documentación técnica
├── SUMMARY.md              # Resumen ejecutivo
└── INSTALL.md              # Este archivo
```

---

## ✅ REQUISITOS

- ✓ Navegador moderno (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- ✓ Conexión a internet (para cargar CDNs)
- ✓ JavaScript habilitado
- ✓ WebGL habilitado (para efectos 3D)

### Librerías Cargadas desde CDN

```html
<!-- Animation -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/PixiPlugin.min.js"></script>

<!-- 3D Graphics -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<!-- Three.js plugins... -->

<!-- Audio -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>

<!-- ML -->
<script src="https://cdn.jsdelivr.net/npm/ml5@0.12.0/dist/ml5.min.js"></script>
```

---

## 🎮 PRIMERA VEZ: QUÉ ESPERAR

### 1. Boot Screen (3 segundos)
```
> JUDAS_OS v8.0 OMEGA
> Mounting /dev/aetherium...
> Checking reality buffers... OK
> Loading hyperreal shaders...
> Calibrating galactic core geometry...
> Aetheric frequencies stabilized.
> WELCOME. AGENT.
```

### 2. Transición a Hero Title
- Zoom 3D + blur + rotación
- Glow pulsante
- Entrada de elementos

### 3. Secciones Principales
- Desplázate para explorar
- Hover effects en todos los cards
- IA responsiva en el chat

---

## 🎯 FUNCIONES PRINCIPALES

### 🧠 AI Lab - 15 Herramientas
Desplázate hasta la sección "AI LAB":

1. **NEURAL CHAT**: Chatea con el núcleo
   - Escribe → Enter
   - Obtén respuestas contextuales

2. **MINI CLAUDE**: Asistente con memoria
   - Pregunta lo que quieras
   - Historial guardado

3. **VISION FORGE**: Generador de prompts
   - Describe visiones
   - Obtén prompts optimizados

4. **TAROT ORACLE**: Tirada de cartas
   - Click "CONSULTAR"
   - 3 cartas + interpretación

5. **Más herramientas**: Dream Decoder, Archetype Scan, DARVO Detector, etc.

### 🎮 Desafíos
Sección "DESAFÍOS":

- 5 tipos de desafío
- Gana XP con cada uno
- Sube de nivel
- Desbloquea logros

### 🎨 Efectos Visuales
En toda la página:

- Partículas que siguen mouse
- Ondas de click
- Glitch effects
- Hologramas parpadeantes
- Distorsión cuántica aleatoria

---

## 🔧 PERSONALIZACIÓN

### Cambiar Colores
Edita las variables CSS en `index.html`:

```css
:root {
    --bg-void: #050505;              /* Background */
    --red-blood: #ff003c;            /* Color primario */
    --cyan-aether: #00ffff;          /* Color secundario */
    --gold-sacred: #ffd700;          /* Terciario */
    --purple-void: #b026ff;          /* Cuaternario */
}
```

### Cambiar Efectos
Modifica `styles-enhanced.css`:

```css
/* Ajusta duración de animaciones */
--pulse-duration: 3s;

/* Ajusta intensidad de glitch */
--glitch-intensity: 0.8;

/* Ajusta tamaño de partículas */
--particle-size: 60px;
```

### Modificar IA
Edita `ai-engine.js`:

```javascript
// Personaliza respuestas
generateContextualResponse(userMessage) {
    const responses = {
        'hola': 'Tu respuesta personalizada',
        // ... agregar más
    };
}
```

---

## 🐛 TROUBLESHOOTING

### "Efectos no se ven"
- [ ] Verifica que WebGL esté habilitado
- [ ] Recarga la página (Ctrl+F5)
- [ ] Prueba en otro navegador

### "No funcionan los efectos de scroll"
- [ ] Asegúrate de que ScrollTrigger de GSAP está cargado
- [ ] Intenta desactivar extensiones del navegador

### "IA no responde"
- [ ] Abre la consola (F12) para ver errores
- [ ] Verifica que JavaScript esté habilitado
- [ ] El motor de IA funciona localmente (no necesita API)

### "Bajo rendimiento"
- [ ] Reduce cantidad de partículas en `ai-engine.js`
- [ ] Desactiva algunos efectos en `styles-enhanced.css`
- [ ] Usa navegador en modo performance

---

## 📊 MONITOREO DE PERFORMANCE

Abre Developer Tools (F12):

```javascript
// Ver FPS
console.log(performance.now())

// Checar memoria
console.log(performance.memory)

// Listar listeners activos
getEventListeners(document)
```

---

## 🚀 DEPLOYMENT

### Vercel (Recomendado)

```bash
# Conecta tu repositorio
vercel

# O si tienes Vercel CLI:
vercel --prod
```

**URL automática:** `tu-proyecto.vercel.app`

### GitHub Pages

```bash
# Sube a GitHub
git push origin main

# Activa en Settings → Pages
# Selecciona rama main

# URL: tu-usuario.github.io/belentani_Omega
```

### Netlify

```bash
# Sube a GitHub y conecta Netlify
# O usa:
npm install -g netlify-cli
netlify deploy --prod
```

### Servidor propio

```bash
# Copia archivos a servidor
scp -r ./* usuario@servidor:/var/www/html/

# Configura nginx o Apache
# Listo!
```

---

## 🔐 SEGURIDAD

✅ **Totalmente seguro**
- No hay backend
- No hay base de datos
- No hay API keys expuestas
- No hay cookies tracking

Datos guardados:
- LocalStorage (cliente)
- Nunca se envía al servidor

---

## 📱 COMPATIBILIDAD

| Navegador | Desktop | Mobile |
|-----------|---------|--------|
| Chrome    | ✅ 90+  | ✅ 90+ |
| Firefox   | ✅ 88+  | ✅ 88+ |
| Safari    | ✅ 14+  | ✅ 14+ |
| Edge      | ✅ 90+  | ✅ 90+ |
| Opera     | ✅ 76+  | ✅ 76+ |

---

## 💡 CONSEJOS

1. **Full Screen**: Presiona F11 para inmersión total
2. **Dark Mode**: Ya viene activado (óptimo para ojos)
3. **Audio**: Los sonidos mejoran con Tone.js + altavoces
4. **Mouse**: El cursor interactivo es parte del diseño
5. **Desafíos**: Vuelve regularmente para sumar XP

---

## 🎓 APRENDIZAJE

### Inspiración en código

Abre DevTools (F12) y explora:

```javascript
// Ver objeto IA
window.omegaAI

// Activar herramienta
window.aiTool('improver')

// Ganar XP manualmente
window.omegaAI.gainXP(50)
```

### Modificar comportamiento

```javascript
// En consola:
window.omegaAI.userXP = 1000  // Ganar XP rápido
window.omegaAI.updateUIState() // Actualizar UI

// Cambiar nivel
window.omegaAI.userLevel = 'OMEGA CORE'
```

---

## 📞 SOPORTE

Si algo no funciona:

1. Verifica que tienes la última versión
2. Borra caché (Ctrl+Shift+Delete)
3. Abre en navegador diferente
4. Mira la consola de errores (F12)
5. Lee IMPROVEMENTS.md para más detalles

---

## 🎉 ¡LISTO!

Tu sitio **BELENTANI OMEGA CORE v8.0** está completamente funcional.

Explora todas las secciones, prueba herramientas IA, completa desafíos y ¡sube de nivel!

**¿Preguntas?** Lee los archivos de documentación:
- `IMPROVEMENTS.md` - Detalles técnicos
- `SUMMARY.md` - Resumen de mejoras
- Este archivo - Instalación y uso

---

**Versión:** 8.0
**Fecha:** Julio 2026
**Estado:** LISTO PARA PRODUCCIÓN ✅

**Disfruta de OMEGA CORE.**
