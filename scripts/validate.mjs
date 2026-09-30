#!/usr/bin/env node
/**
 * Validador de estructura del repositorio Belentani Omega.
 *
 * Comprueba que el sitio es coherente consigo mismo antes de publicarse:
 * presencia de los archivos base, que el HTML enlaza lo que dice enlazar,
 * y que no se cuelan credenciales en el repositorio.
 *
 * Sale con codigo 0 si todo esta bien, 1 si encuentra fallos.
 * Uso: node scripts/validate.mjs
 */
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const fallos = [];
const avisos = [];
let comprobaciones = 0;

function comprobar(descripcion, condicion, esAviso = false) {
  comprobaciones++;
  if (condicion) return true;
  (esAviso ? avisos : fallos).push(descripcion);
  return false;
}

function leer(relativo) {
  const p = resolve(RAIZ, relativo);
  return existsSync(p) ? readFileSync(p, 'utf8') : null;
}

// 1. Archivos base del sitio
for (const archivo of ['index.html', 'README.md', 'LICENSE', 'CNAME']) {
  comprobar('Falta el archivo base: ' + archivo, existsSync(resolve(RAIZ, archivo)));
}

// 2. El CNAME debe apuntar al dominio real
const cname = leer('CNAME');
if (cname) {
  comprobar('CNAME no apunta a belentani.es', cname.trim() === 'belentani.es');
}

// 3. El HTML debe cerrar sus etiquetas
const html = leer('index.html');
if (html) {
  comprobar('index.html sin </html>', html.includes('</html>'));
  comprobar('index.html sin </body>', html.includes('</body>'));
  comprobar('index.html sin <title>', /<title[^>]*>/.test(html));
  comprobar('index.html sin meta description', /<meta[^>]+name=["']description["']/i.test(html));

  // 4. Los scripts locales referenciados deben existir
  const referencias = [...html.matchAll(/<script[^>]+src=["']([^"']+)["']/gi)]
    .map((m) => m[1])
    .filter((src) => !/^(https?:)?\/\//.test(src) && !src.startsWith('data:'));

  for (const src of referencias) {
    const limpio = src.split('?')[0].split('#')[0];
    comprobar('El HTML referencia un script que no existe: ' + limpio,
      existsSync(resolve(RAIZ, limpio)), true);
  }

  // 5. Las hojas de estilo locales referenciadas deben existir
  const estilos = [...html.matchAll(/<link[^>]+href=["']([^"']+\.css)["']/gi)].map((m) => m[1]);
  for (const href of estilos) {
    const limpio = href.split('?')[0];
    if (/^(https?:)?\/\//.test(limpio)) continue;
    comprobar('El HTML referencia un CSS que no existe: ' + limpio,
      existsSync(resolve(RAIZ, limpio)), true);
  }

  // 6. Accesibilidad minima
  comprobar('index.html sin atributo lang', /<html[^>]+lang=/i.test(html));
  comprobar('index.html sin viewport', /<meta[^>]+name=["']viewport["']/i.test(html), true);
}

// 7. Sin credenciales versionadas
const patronesPeligrosos = [
  ['clave de OpenAI', /sk-[A-Za-z0-9]{20,}/],
  ['token de GitHub', /gh[pousr]_[A-Za-z0-9]{30,}/],
  ['clave de AWS', /AKIA[0-9A-Z]{16}/],
  ['clave privada', /-----BEGIN [A-Z ]*PRIVATE KEY-----/],
];
for (const [nombre, patron] of patronesPeligrosos) {
  if (!html) break;
  comprobar('Posible ' + nombre + ' en index.html', !patron.test(html));
}

// 8. El motor de universo, si esta referenciado, debe existir
if (html && html.includes('belentani-universe.js')) {
  comprobar('El motor de universo esta referenciado pero no existe',
    existsSync(resolve(RAIZ, 'js/belentani-universe.js')));
}

// Informe
console.log('Validacion de Belentani Omega');
console.log('Comprobaciones: ' + comprobaciones);
console.log('Fallos: ' + fallos.length + ' | Avisos: ' + avisos.length);

for (const a of avisos) console.log('  aviso: ' + a);
for (const f of fallos) console.log('  FALLO: ' + f);

if (fallos.length > 0) {
  console.log('Validacion FALLIDA');
  process.exit(1);
}
console.log('Validacion OK');
