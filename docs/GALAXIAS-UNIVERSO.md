# BELENTANI // 50 GALAXIAS — el universo navegable

> Generado por `tools/optimize-media/build-galaxy-pages.py`. Aditivo y
> reversible: no modifica `index.html`, `css/` ni `js/` existentes.

## Modelo

   5 Firmas (LORE-UNIFICADO §6) x 10 Estaciones = 50 galaxias

| # | Firma | Virtud | Color |
|---|---|---|---|
| 1 | PEDRO.SIG | permanencia | #FFD700 |
| 2 | MARCOS.SIG | memoria | #00FFFF |
| 3 | SANTOS.SIG | canal | #B026FF |
| 4 | BELENTANI.SIG | integracion | #FF003C |
| 5 | HUMAN.SIG | puente tangible | #F5F5F5 |

Estaciones: EL ENTRE, LA DEUDA, EL ROBO, EL CANTO, LA VICTORIA AMARGA,
LA MENTIRA COMPARTIDA, EL UMBRAL, LA SENAL, EL PORTAL, LA CONSTELACION.

`galaxia-NN.html` con `NN = firma*10 + estacion`. Fila = firma, columna =
estacion. Cada pagina es la MISMA estacion vista desde otra firma: el mundo
cambia de color y de lectura, la orbita no cambia.

## Cada elemento tiene funcion

| Elemento | Que es en el universo |
|---|---|
| topnav ndots | las 5 Firmas (cambiar firma = cambiar de mundo) |
| Ojo de Judas (planeta) | late a la frecuencia de la estacion (3.2 s -> 0.9 s) |
| anillos | la Llave Dorada robada (oro 46 s, rojo punteado 72 s inverso) |
| hero-orbit sparks | las 10 estaciones; la activa brilla en oro |
| hbar waveC | el Canto (LA VOZ ES EL OUTPUT): navegacion |
| espejo | linea canon de (firma x estacion) |
| slider sentido | NEON / MATRIX / VENOM / VOID / ASCENDED |

## Memoria e idioma

- `localStorage omega_story` guarda las estaciones recorridas (barra de progreso).
- `localStorage omega_sense` guarda la parada de sentido.
- `localStorage omega_lang` guarda el idioma.
- i18n en orden fijo **PT > ES > EN > CA** con `?lang=` + `hreflang` alternates.
- Teclado: izquierda anterior, derecha siguiente, ESC nucleo, 1-5 sentido.

## Accesibilidad

`skip-link`, `aria-current`, `aria-label`, foco visible, `prefers-reduced-motion`
detiene todas las animaciones, y sin JS la pagina sigue siendo legible (HTML
estatico + CSS).

## Regenerar

    python tools/optimize-media/build-galaxy-pages.py

## Ver

    python -m http.server 8099
    http://localhost:8099/galaxias/
