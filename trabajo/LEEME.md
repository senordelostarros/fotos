# Carpeta de trabajo – El Señor de los Tarros

Herramientas y datos usados con Claude para la tienda elsenordelostarros.cl (Jumpseller).
Fotos de productos en la raíz del repo; URL pública: https://senordelostarros.github.io/fotos/<archivo>

## scripts/
- ms_proc.py: limpia una foto de producto → fondo blanco, centrado, 1000x1000 (estilo Mister Solución).
- seg.py / comp.py: método por piezas para fotos con sellos (numera piezas, se eligen a mano, compone).
- cut.py: recorta productos desde páginas de catálogos PDF quitando el fondo (rembg isnet-general-use).
- insta.py (+ insta5/insta7 de ejemplo): publicaciones Instagram 1080x1350 con marca. Rutas internas apuntan al scratchpad antiguo: ajustar LOGO a marca/logo-000.png.
- cot_cem.py: plantilla de cotización PDF (reportlab, Poppins, colores de marca).
- build.py / equip.py / render.py: tiles de banners de categorías (SVG → PNG con Playwright).
- cat_rules.py: reglas para clasificar productos en las 8 categorías.

## datos/
- productos.csv: export de la tienda (6 oct 2026).
- visibles.json: 2.172 productos visibles {p=permalink, n=nombre, s=sku, b=marca, img, c}.
- categorias-8.csv (+ arreglo): categoría asignada a cada producto.

## marca/
- logo-000.png, logo-encabezado-ancho-v2.jpg, pat.b64 (patrón de fondo).
- Colores: carbón #1D2126 · turquesa #6FC8DA · amarillo #FFC72C · rojo #E0473A. Fuente Poppins.
