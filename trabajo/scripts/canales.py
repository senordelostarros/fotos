"""Infográfico con todos los canales de comunicación del negocio.
Uso: python3 canales.py <carpeta_salida>  -> canales-historia.jpg (1080x1920) y canales-post.jpg (1080x1350)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import patron, f, FB, FM, FR, CARBON, TURQ, AMAR, BLANCO
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'
insta.LOGO = R + 'trabajo/marca/logo-000.png'
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)
GRIS = (90, 98, 108)
EF = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)

CANALES = [  # emoji, color del círculo, título, dato, detalle
    ('💬', (37, 211, 102), 'WhatsApp pedidos', '+56 9 4969 1686', 'Cotizaciones y pedidos al tiro'),
    ('🌐', TURQ, 'Tienda online', 'elsenordelostarros.cl', 'Compra 24/7 · pago con Webpay'),
    ('📸', (225, 48, 108), 'Instagram', '@el_senor_de_los_tarros_spa_', 'Bomba del día y novedades'),
    ('🎵', (20, 20, 20), 'TikTok', '@el.sr.de.los.tarros', 'Reels "¿Adivinas qué herramienta es?"'),
    ('📍', (234, 67, 53), 'Tienda física', 'Irarrázaval 1372, Ñuñoa', 'Búscanos en Google Maps'),
    ('🔩', AMAR, 'Dados sueltos y cotizador', 'En la página web', 'Arma tu lista y cotízala por WhatsApp'),
]

def emoji(ch, size):
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((80, 80), ch, font=EF, embedded_color=True, anchor='mm')
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)

def fit(d, txt, font_path, size, maxw):
    fo = f(font_path, size)
    while d.textlength(txt, font=fo) > maxw and size > 20:
        size -= 2; fo = f(font_path, size)
    return fo

def armar(W, H, compacto):
    c = patron((W, H)).convert('RGBA'); d = ImageDraw.Draw(c)
    logo = Image.open(insta.LOGO).convert('RGBA')
    lw = 560 if compacto else 720
    l = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    top = 50 if compacto else 90
    c.alpha_composite(l, ((W - l.width) // 2, top))
    y = top + l.height + (24 if compacto else 46)
    # título
    d.rounded_rectangle([60, y, W - 60, y + (110 if compacto else 140)], radius=30, fill=CARBON)
    d.text((W // 2, y + (55 if compacto else 70)), 'Todos nuestros canales', font=f(FB, 58 if compacto else 68), fill=AMAR, anchor='mm')
    y += (130 if compacto else 175)
    # tarjetas
    fh = (H - y - (110 if compacto else 150)) // len(CANALES)
    for em, col, tit, dato, det in CANALES:
        hh = fh - 16
        d.rounded_rectangle([60, y, W - 60, y + hh], radius=26, fill=BLANCO)
        r = int(hh * 0.36); cx, cy = 60 + 30 + r, y + hh // 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        e = emoji(em, int(r * 1.15)); c.alpha_composite(e, (cx - e.width // 2, cy - e.height // 2))
        x = cx + r + 30; maxw = W - 60 - 30 - x
        k = 1 if not compacto else .82
        d.text((x, cy - hh * .30), tit, font=fit(d, tit, FM, int(34 * k), maxw), fill=GRIS, anchor='lm')
        d.text((x, cy + 2), dato, font=fit(d, dato, FB, int(50 * k), maxw), fill=CARBON, anchor='lm')
        d.text((x, cy + hh * .30), det, font=fit(d, det, FR, int(31 * k), maxw), fill=(74, 160, 178), anchor='lm')
        y += fh
    # pie
    fy = H - (90 if compacto else 120)
    d.rectangle([0, fy, W, H], fill=AMAR)
    d.text((W // 2, fy + (30 if compacto else 40)), 'Precios netos · Emitimos factura', font=f(FB, 36 if compacto else 42), fill=CARBON, anchor='mm')
    d.text((W // 2, fy + (66 if compacto else 88)), 'Despacho gratis dentro de Vespucio sobre $50.000 + IVA', font=f(FM, 26 if compacto else 31), fill=CARBON, anchor='mm')
    return c.convert('RGB')

armar(1080, 1920, False).save(OUT + '/canales-historia.jpg', quality=92)
armar(1080, 1350, True).save(OUT + '/canales-post.jpg', quality=92)
print('ok')
