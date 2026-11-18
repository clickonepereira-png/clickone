# Guía para continuar las ediciones en otra sesión de Claude

> **Cómo usarla en un repositorio NUEVO:**
> 1. Crea el repositorio nuevo en GitHub y abre una sesión de Claude Code con él.
> 2. Adjunta este archivo en el primer mensaje, o súbelo a la raíz del repositorio nuevo.
> 3. Escribe: *"Lee GUIA-EDICION-CLAUDE.md y sigue esas reglas. Trabaja en este repositorio."*
> 4. Adjunta el video.
>
> **Sobre los recursos (sonidos, logos, overlays, señales):** están en el repositorio anterior, `clickonepereira-png/clickone`. Tienes dos opciones:
> - **(a) Recomendada:** pídele al nuevo Claude *"agrega el repositorio clickonepereira-png/clickone solo para copiar recursos"*. Así puede copiar a su repositorio lo que necesite: sonidos, logo de COCOA, overlays o un proyecto parecido como plantilla.
> - **(b)** Vuelve a enviarle los recursos (zips de sonidos, logos) cuando los necesite.
>
> Las rutas `videos/...` de esta guía se refieren al repositorio anterior. En el nuevo, Claude debe crear su propia carpeta por video, con la misma estructura.

## 1. Cómo trabajamos

- El usuario edita en **CapCut** y habla en español. Claude edita los videos con **HyperFrames** (`npx hyperframes@0.8.101`), renderiza y entrega los archivos.
- Cada video tiene su carpeta en `videos/<proyecto>/`, con `index.html`, `assets/` (footage, sfx, fuentes, imágenes) y `renders/`.
- Se trabaja en la rama que indique la sesión del repositorio nuevo. Hay que hacer commit y push al terminar.
- Para arrancar un proyecto nuevo, corre `npx hyperframes@0.8.101 init <nombre>`, o copia la estructura de un proyecto del repositorio anterior.
- El render "completo" pesa mucho: se agrega a `.gitignore` y no se sube. GitHub no acepta archivos de más de 100 MB.

### Entregables de cada video
1. **Video para compartir:** MP4 de menos de 30 MB, con libx264 a dos pasadas y audio AAC a 160k.
2. **Una capa de croma:** CRF 10, con efectos de sonido y **solo gráficos**.
   - Por defecto el fondo es **verde #00b140**.
   - En los videos donde los aciertos llevan cosas verdes, el fondo es **azul #0047bb**.
   - **Nunca** se incluye a la persona recortada en la capa. El usuario quita el fondo a mano en CapCut.
   - No hay que enviar una capa de sonido aparte.
3. Los archivos se envían con `SendUserFile`, con un resumen corto en español.

## 2. Reglas generales (el usuario las ha pedido varias veces)

- **Nunca poner nada encima de los rostros:** ni textos, ni logos, ni gráficos. Hay que detectar las caras y ubicar los textos en la franja libre de cada toma.
- **No sobrecargar.** Pocos efectos y bien puestos. Nada de stickers ni etiquetas de quién habla.
- **Subtítulos fieles:** escuchar por tramos cortos. La transcripción automática se equivoca, por ejemplo "ya me refiero a todo" en vez de "llámese…", o "cubría" en vez de "cubre".
- **Censurar groserías** con un pitido.
- **Difuminar las placas** de carros y motos, con un parche pequeño que siga la placa. No debe quedar un recuadro grande ni durar todo el video.
- **Los bordes de color a los lados** (verde, rojo o amarillo) se ven mal al aplicar el croma. No usarlos.
- **Legibilidad:** en tomas claras, oscurecer el fondo detrás del texto y dar a las letras una sombra fuerte.

## 3. Estilo por cliente

### Profe Milton (tránsito, humor)
- Paleta: tinta #0b1428, amarillo #ffd400 (**solo para acentos**) y naranja #ff7a2f. Fuente Montserrat.
- Subtítulos con jerarquía de "cápsula": una línea pequeña arriba, la **palabra clave grande** abajo y, si hace falta, una cola pequeña. Las animaciones van variadas: pop, flip, slide, bounce y letra a letra.
- El amarillo va solo en los remates o datos clave.
- Pocos efectos de sonido (boing, scratch, dun-dun, ding, sello, caja registradora). Zooms en las reacciones.
- Motion graphics sencillos en **escenas de fondo blanco** a pantalla completa. Ejemplos: sigla SOAT, íconos de peatón/conductor, contador de "18 meses", sello "VIGENTE".
- Cuando dice "contáctenos", el número es **301 930 7974**. Si el video termina justo ahí, congelar el último cuadro unos 2,5 s.
- **Concurso de señales:** solo la **imagen** de la señal, sin el nombre. Sonidos de acierto, error y "más o menos", sin bordes de color.
  - La flecha doblada en ángulo es una **curva pronunciada**, no un "giro".

### Cornabis (seguridad social)
- Fuente Montserrat. Azul marino oficial #17304d más azules. **Nada de amarillo.** Usar el logo oficial (familia CORNABIS T.I.A. con el lema "Unidos Construyendo Bienestar Social").
- Motion graphics solo en **escenas de fondo blanco** a pantalla completa, sin recortar a la persona.
- Reencuadrar los planos mal encuadrados.
- Tapar las tomas malas con escenas blancas.
- Variar los sonidos del pack del cliente: error en lo negativo, clics en las palabras clave y whooshes en las transiciones.
- El formato "cápsula" debe ser distinto de los demás: escenas azul marino, barra de progreso y la misma jerarquía de subtítulos.

### COCOA (bienestar)
- Dorado del logo (#c9a75c a #f3dc9a) con Playfair en itálica y Poppins. Logo en `videos/cocoa-testimonio/assets/img/cocoa-logo.png`.
- **Formato tráiler:** apertura en negro con el logo, tarjetas de impacto con golpe grave, destello y zoom, palabras sobre los golpes de la música y cierre "CONSCIENCIA · COHERENCIA · ACCIÓN".

### Otros
- **Casa de lujo:** tipografía tipo New Roman (Tinos) con gráficos premium.
- **Viajando por el Eje:** dorado de lujo. El link www.viajandoporeleje.co se escribe letra por letra.
- **MoviGym:** amarillo solo en acentos y resaltado del recorrido con tracking anclado a la calle. Las flechas de giro van rectas en pantalla.

## 4. Recetas técnicas

- **Preparar el footage:** `ffmpeg -i in.mp4 -c:v libx264 -crf 14 -r 30 -g 30 -keyint_min 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart assets/footage.mp4`
- **Revisar:** `npx hyperframes@0.8.101 lint` y `snapshot --at t1,t2,... --no-end -o carpeta`. Hay que **mirar las capturas** antes de renderizar.
  - El error `video_nested_in_timed_element` es inofensivo porque `#stage` empieza en 0.
- **Render:** `render . -q high --fps 30 -o renders/X-completo.mp4`. Para la capa:
  1. Crea `_green/` con enlaces a `assets` y copia de los json.
  2. Genera la página: `sed -e 's/data-mode="full"/data-mode="green"/' -e '/id="voice"/d' index.html > _green/index.html`
  3. Renderiza con `--crf 10`.
- Lanza los renders con `run_in_background` del harness y espera con `until grep -q SHARE salida`. Nada de `nohup`.
  - Para detener procesos usa su PID. `pkill -f` mata la propia terminal.
- **Transcribir:** Whisper local (`npm i --ignore-scripts sts-whisper-small @huggingface/transformers`), con ventanas de unos 4–7 s.
  - El scratchpad se borra seguido, así que hay que reinstalarlo.
- **Rostros:** `pip install opencv-python-headless==4.10.0.84`, porque la 5.x no trae `CascadeClassifier`. Con los cascades Haar se sacan las cajas de las caras y se elige la franja vertical libre. **Siempre verificar a ojo**, porque falla en tomas oscuras.
- **Placas:** se detectan con una máscara amarilla y se confirman en recortes. El blur es una copia del video con `filter: blur()` y `clip-path` animado:
  - usa `opacity` y no `visibility`;
  - pon una copia en espejo para que el blur no se aclare en el borde.
- **Trampas de GSAP:**
  - un `fromTo` aplica su valor inicial desde t=0; en elementos con varias animaciones usa `set` + `to`;
  - no animes `letterSpacing`;
  - revisa que la plantilla no tenga clases viejas con el mismo nombre (pasó con `.stamp`).

## 5. Proyectos hechos (en el repositorio anterior `clickonepereira-png/clickone`, carpeta `videos/`)

casa-lujo, cocoa-testimonio, cocoa-congreso, boda-diana-german, cornabis-pension, cornabis-arl, cornabis-pago, cornabis-eps, cornabis-regimenes, milton-transito, milton-tecnomecanica, milton-alcoholemia, milton-soat, milton-senales, viajando-eje, movigym.

Todos usan la misma estructura. Para un video nuevo de un cliente, lo más rápido es copiar el proyecto más parecido y cambiar el guion, los tiempos, los efectos y las escenas.

## 6. Biblioteca de recursos (en el repositorio anterior; copiar al nuevo según se necesite)

- **Sonidos del cliente** (whoosh, click, error/falla, correct, cash, digits, riser, typing…): en `videos/cornabis-regimenes/assets/sfx` y `videos/movigym/assets/sfx`.
- **Sonidos graciosos:** en `videos/milton-transito/assets/sfx`.
- **Overlays:** quemado de película en `milton-transito/assets/fx` y transiciones de Cornabis en `cornabis-regimenes/assets/fx`.
- **Señales de tránsito recortadas:** en `videos/milton-senales/assets/signs`.
- **Si falta un recurso,** pedírselo al usuario; él lo descarga y lo envía.
