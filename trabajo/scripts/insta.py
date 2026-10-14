#!/usr/bin/env python3
"""Publicaciones de Instagram 1080x1350 con la línea gráfica de El Señor de los Tarros.

Estructura: logo arriba, panel turquesa con patrón y el producto grande,
bloque carbón con nombre, código y precio, pie amarillo con WhatsApp.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from scipy import ndimage

SP = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(SP, "logo", "logo-000.png")
OUT = "/mnt/user-data/outputs/instagram"

W, H = 1080, 1350
CARBON = (29, 33, 38)
TURQ = (111, 200, 218)
TURQ_HONDO = (74, 160, 178)
AMAR = (255, 199, 44)
BLANCO = (255, 255, 255)
GRIS = (170, 178, 188)

FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
FR = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
f = lambda p, s: ImageFont.truetype(p, s)


def recortar(path, umbral=238):
    """Producto con fondo blanco transparente (solo el blanco unido al borde)."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    claro = a.max(axis=2) > umbral
    et, n = ndimage.label(claro)
    borde = set(et[0, :]) | set(et[-1, :]) | set(et[:, 0]) | set(et[:, -1])
    borde.discard(0)
    fondo = np.isin(et, list(borde))
    obj = ~fondo
    # quedarse con la pieza principal y lo que esté pegado a ella
    et2, n2 = ndimage.label(ndimage.binary_closing(obj, structure=np.ones((9, 9))))
    if n2 > 1:
        areas = ndimage.sum(obj, et2, range(1, n2 + 1))
        keep = [i + 1 for i, ar in enumerate(areas) if ar >= areas.max() * 0.08]
        obj = obj & np.isin(et2, keep)
    alfa = Image.fromarray((obj * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.7))
    rgba = im.convert("RGBA"); rgba.putalpha(alfa)
    bb = alfa.point(lambda v: 255 if v > 40 else 0).getbbox()
    return rgba.crop(bb) if bb else rgba


def patron(size):
    """Turquesa con el patrón de herramientas del logo, espejado para que no se noten costuras."""
    w, h = size
    logo = Image.open(LOGO).convert("RGB")
    lw, lh = logo.size
    t = logo.crop((int(lw * 0.62) + 4, 4, lw - 4, int(lh * 0.32)))
    t = t.resize((520, int(t.height * 520 / t.width)), Image.LANCZOS)
    tw, th = t.size
    b = Image.new("RGB", (tw * 2, th * 2))
    b.paste(t, (0, 0)); b.paste(t.transpose(Image.FLIP_LEFT_RIGHT), (tw, 0))
    b.paste(t.transpose(Image.FLIP_TOP_BOTTOM), (0, th)); b.paste(t.transpose(Image.ROTATE_180), (tw, th))
    cap = Image.new("RGB", (w + b.width, h + b.height))
    for y in range(0, cap.height, b.height):
        for x in range(0, cap.width, b.width):
            cap.paste(b, (x, y))
    base = Image.new("RGB", (w, h), TURQ)
    return Image.blend(base, cap.crop((0, 0, w, h)), 0.45)


def sombra(p, blur=26, op=110, dy=22):
    pad = blur * 3
    s = Image.new("RGBA", (p.width + pad * 2, p.height + pad * 2), (0, 0, 0, 0))
    sil = Image.new("RGBA", p.size, (0, 0, 0, 255))
    sil.putalpha(p.split()[3].point(lambda a: int(a * op / 255)))
    s.paste(sil, (pad, pad + dy), sil)
    return s.filter(ImageFilter.GaussianBlur(blur))


def colocar(lienzo, prod, caja, centro=None):
    """Escala el producto para que quepa en la caja (x0,y0,x1,y1) y lo pega con sombra."""
    x0, y0, x1, y1 = caja
    r = min((x1 - x0) / prod.width, (y1 - y0) / prod.height)
    p = prod.resize((int(prod.width * r), int(prod.height * r)), Image.LANCZOS)
    cx = centro[0] if centro else (x0 + x1) // 2
    cy = centro[1] if centro else (y0 + y1) // 2
    sh = sombra(p)
    lienzo.paste(sh, (cx - sh.width // 2, cy - sh.height // 2), sh)
    lienzo.paste(p, (cx - p.width // 2, cy - p.height // 2), p)


def texto_ajustado(d, txt, fuente, ancho_max, tam, tam_min=34):
    """Reduce el tamaño hasta que el texto cabe en hasta 2 líneas."""
    while tam >= tam_min:
        ft = f(fuente, tam)
        palabras, lineas, actual = txt.split(), [], ""
        for p in palabras:
            prueba = (actual + " " + p).strip()
            if d.textlength(prueba, font=ft) <= ancho_max:
                actual = prueba
            else:
                lineas.append(actual); actual = p
        lineas.append(actual)
        if len(lineas) <= 2:
            return ft, lineas
        tam -= 4
    return f(fuente, tam_min), lineas


def publicacion(nombre_archivo, productos, etiqueta, titulo, detalle, precio, sufijo):
    img = Image.new("RGB", (W, H), CARBON)
    d = ImageDraw.Draw(img)

    # cabecera: logo
    logo = Image.open(LOGO).convert("RGB")
    lw = 300
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    img.paste(logo, (60, 52))
    d.text((W - 60, 78), etiqueta.upper(), font=f(FB, 26), fill=AMAR, anchor="ra")
    d.text((W - 60, 114), "Insumos para talleres", font=f(FR, 24), fill=GRIS, anchor="ra")

    # panel turquesa con el producto
    py0, py1 = 230, 880
    panel = patron((W - 120, py1 - py0))
    m = Image.new("L", panel.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, panel.width - 1, panel.height - 1], 28, fill=255)
    img.paste(panel, (60, py0), m)
    for prod, caja in productos:
        x0, y0, x1, y1 = caja
        colocar(img, prod, (60 + x0, py0 + y0, 60 + x1, py0 + y1))

    # texto
    ft, lineas = texto_ajustado(d, titulo, FB, W - 120, 62)
    y = 920
    for ln in lineas:
        d.text((60, y), ln, font=ft, fill=BLANCO)
        y += int(ft.size * 1.18)
    d.text((60, y + 6), detalle, font=f(FM, 28), fill=GRIS)

    # precio
    yp = 1138
    if precio:
        fp = f(FB, 74)
        d.text((60, yp), precio, font=fp, fill=AMAR)
        wpr = d.textlength(precio, font=fp)
        d.text((60 + wpr + 16, yp + 34), sufijo, font=f(FM, 30), fill=GRIS)
    else:
        d.text((60, yp + 10), sufijo, font=f(FB, 46), fill=AMAR)

    # pie
    d.rectangle([0, H - 96, W, H], fill=AMAR)
    d.text((60, H - 48), "Pedidos por WhatsApp  +56 9 4969 1686", font=f(FB, 32), fill=CARBON, anchor="lm")
    d.text((W - 60, H - 48), "elsenordelostarros.cl", font=f(FM, 26), fill=CARBON, anchor="rm")

    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, nombre_archivo), quality=92, optimize=True)
    print("listo", nombre_archivo)


if __name__ == "__main__":
    L = os.path.join(SP, "fotos_limpias")
    S = os.path.join(SP, "senf")
    PW, PH = W - 120, 650

    publicacion("01-gata-caiman-3t.jpg",
                [(recortar(os.path.join(L, "YT17211.jpg")), (70, 50, PW - 70, PH - 40))],
                "YATO", "Gata caimán 3 toneladas",
                "Hidráulica  ·  YT-17211  ·  Levante 130 a 465 mm", "$263.989", "+ IVA")

    publicacion("02-juego-dados-1-2.jpg",
                [(recortar(os.path.join(L, "YT12651.jpg")), (60, 70, PW - 60, PH - 60))],
                "YATO", 'Juego de dados 1/2"',
                "23 piezas  ·  Caja metálica  ·  YT-12651", "$120.989", "+ IVA")

    publicacion("03-motorflush-senfineco.jpg",
                [(recortar(os.path.join(S, "pr-030.png")), (PW // 2 - 220, 30, PW // 2 + 220, PH - 30))],
                "Senfineco · Alemania", "MotorFlush Senfineco",
                "Pre-lavado de motor  ·  Se aplica antes del cambio de aceite", "$4.990", "+ IVA")
