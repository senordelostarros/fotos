"""Reels/TikTok 1080x1920 (~13 s, sin música) de la bomba del día.
Uso: python3 reel_bomba.py <n> <salida.mp4> <carpeta_tmp>   (n = índice en REELS)
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
insta.LOGO = R + '/trabajo/marca/logo-000.png'
from insta import recortar, patron, sombra, CARBON, TURQ, AMAR, BLANCO, FB, FM, FR, f
from PIL import Image, ImageDraw

ROJO = (224, 71, 58)
# [día, gancho línea 1, gancho línea 2, nombre, detalle, precio normal neto, foto(permalink)]
REELS = [
    ['DOMINGO', '¿Aprietas las ruedas', 'a ojo?', 'Llave de torque 1/2" YATO', '60 a 330 Nm · con clic de aviso', 186989, 'llave-de-torque-12-60-a-330-nm'],
    ['LUNES', '¿No sale', 'ni a combos?', 'Juego de extractores 16 piezas YATO', 'Poleas, rodamientos y engranajes', 184789, 'juego-de-extractores-16-piezas'],
    ['MARTES', 'Tres bombeadas', 'y arriba', 'Gata caimán hidráulica 3 t YATO', 'Para el taller, robusta y segura', 263989, 'gata-caiman-hidraulica-3-toneladas'],
    ['MIÉRCOLES', 'El juego que no puede', 'faltar en tu carro', 'Chicharra 1/2" con 18 dados YATO', 'Dados de 8 a 32 mm · 72 dientes', 76989, 'juego-chicharra-12-con-18-dados-19-piezas'],
    ['JUEVES', 'Saca emblemas', 'sin rayar la pintura', 'Pistola de calor 2000 W YATO', 'Hasta 550 °C · con accesorios', 49489, 'pistola-de-aire-caliente-2000-w'],
    ['VIERNES', '23 piezas para', 'todo el taller', 'Juego de dados 1/2" 23 piezas YATO', 'En caja metálica', 120989, 'juego-de-dados-12-23-piezas-caja-metalica'],
    ['SÁBADO', 'Presión exacta', 'en cada neumático', 'Inflador digital 0 a 120 psi YATO', 'Con pantalla digital', 49489, 'inflador-manual-0-a-120-psi-con-pantalla-digital'],
]
N = int(sys.argv[1]); OUT = sys.argv[2]; TMP = sys.argv[3]
DIA, G1, G2, NOM, DET, PRECIO, PERMA = REELS[N]
W, H, FPS = 1080, 1920, 30
os.makedirs(TMP, exist_ok=True)

logo = Image.open(insta.LOGO).convert('RGBA')
prod = recortar(R + '/ms5-' + PERMA + '.jpg')
fondo_t = patron((W, H)).convert('RGBA')
fondo_c = Image.new('RGBA', (W, H), CARBON + (255,))
def cl(v): return '$' + f'{round(v):,}'.replace(',', '.')

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.7
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def fit(p, h): return p.resize((max(1, int(p.width * h / p.height)), max(1, int(h))), Image.LANCZOS)
def fitbox(p, w, h):
    s = min(w / p.width, h / p.height); return p.resize((max(1, int(p.width * s)), max(1, int(p.height * s))), Image.LANCZOS)

def texto(c, txt, font, y, fill, alpha=1, dy=0):
    if alpha <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W // 2, y + dy), txt, font=font, fill=fill + (int(255 * alpha),), anchor='mt')
    c.alpha_composite(lay)

def pastilla(c, txt, font, y, bg, fg, s=1.0, pad=(36, 18)):
    if s <= 0.01: return
    d0 = ImageDraw.Draw(c); w = d0.textlength(txt, font=font); h = font.size
    bw, bh = int(w + pad[0] * 2), int(h + pad[1] * 2 + 8)
    b = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=18, fill=bg + (255,))
    d.text((bw // 2, pad[1]), txt, font=font, fill=fg, anchor='mt')
    if s != 1: b = b.resize((max(1, int(bw * s)), max(1, int(bh * s))), Image.LANCZOS)
    c.alpha_composite(b, (W // 2 - b.width // 2, int(y + bh / 2 - b.height / 2)))

def producto(c, cy, w, h, s):
    if s <= 0.01: return
    q = fitbox(prod, w * s, h * s); sh = sombra(q, blur=30, op=120, dy=26); pad = (sh.width - q.width) // 2
    x, y = W // 2 - q.width // 2, int(cy - q.height / 2)
    c.alpha_composite(sh, (x - pad, y - pad)); c.alpha_composite(q, (x, y))

def sello(c, cx, cy, s):
    if s <= 0.01: return
    r = int(120 * s); d = ImageDraw.Draw(c)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ROJO)
    if s > .5: d.text((cx, cy), '-20%', font=f(FB, int(78 * s)), fill=BLANCO, anchor='mm')

def logo_en(c, y, w, alpha=1):
    l = logo.resize((w, int(logo.height * w / logo.width)), Image.LANCZOS)
    if alpha < 1: l.putalpha(int(255 * alpha))
    c.alpha_composite(l, (W // 2 - w // 2, y))

def franja(c):
    d = ImageDraw.Draw(c); d.rectangle((0, H - 150, W, H), fill=AMAR)
    d.text((W // 2, H - 75), 'Pedidos WhatsApp +56 9 4969 1686', font=f(FB, 44), fill=CARBON, anchor='mm')

ESC = [(0, 2.8), (2.8, 7.6), (7.6, 13.0)]
TOTAL = ESC[-1][1]

def frame(t):
    if t < ESC[0][1]:  # gancho
        c = fondo_c.copy(); u = t
        logo_en(c, 180, 620, ease(u / .5))
        texto(c, G1, f(FB, 88), 760, BLANCO, ease((u - .25) / .4), dy=40 * (1 - ease((u - .25) / .4)))
        texto(c, G2, f(FB, 88), 870, AMAR, ease((u - .5) / .4), dy=40 * (1 - ease((u - .5) / .4)))
        pastilla(c, 'BOMBA DEL ' + DIA, f(FB, 54), 1100, ROJO, BLANCO, back((u - 1.0) / .5))
        texto(c, '20% menos, solo por hoy', f(FM, 50), 1250, TURQ, ease((u - 1.4) / .4))
    elif t < ESC[1][1]:  # producto + precio
        c = fondo_t.copy(); u = t - ESC[1][0]
        d = ImageDraw.Draw(c); d.rectangle((0, 0, W, 200), fill=CARBON)
        texto(c, 'BOMBA DEL ' + DIA, f(FB, 58), 66, AMAR)
        producto(c, 760, 900, 820, back((u - .1) / .6))
        sello(c, W - 190, 330, back((u - .7) / .4))
        d = ImageDraw.Draw(c)
        if u > 1.0:
            a = ease((u - 1.0) / .4)
            box = Image.new('RGBA', (W, 520), CARBON + (int(235 * a),)); c.alpha_composite(box, (0, 1250))
        texto(c, NOM, f(FB, 52 if len(NOM) < 32 else 46), 1290, BLANCO, ease((u - 1.1) / .4))
        texto(c, DET, f(FM, 40), 1370, (170, 178, 188), ease((u - 1.3) / .4))
        if u > 1.6:
            a = ease((u - 1.6) / .4)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            fa = f(FM, 48); ta = 'Antes ' + cl(PRECIO); wa = dl.textlength(ta, font=fa)
            dl.text((W // 2, 1460), ta, font=fa, fill=(170, 178, 188, int(255 * a)), anchor='mt')
            dl.line((W // 2 - wa / 2, 1490, W // 2 + wa / 2, 1490), fill=(170, 178, 188, int(255 * a)), width=4)
            c.alpha_composite(lay)
        pastilla(c, cl(PRECIO * .8) + ' + IVA', f(FB, 96), 1555, AMAR, CARBON, back((u - 2.0) / .5))
        franja(c)
    else:  # cierre
        c = fondo_c.copy(); u = t - ESC[2][0]
        logo_en(c, 170, 700, ease(u / .5))
        texto(c, 'Bomba del día', f(FB, 76), 650, BLANCO, ease((u - .2) / .4))
        texto(c, 'en el link del perfil', f(FB, 76), 745, AMAR, ease((u - .4) / .4))
        pastilla(c, 'elsenordelostarros.cl', f(FB, 62), 930, TURQ, CARBON, back((u - .8) / .5))
        pastilla(c, 'WhatsApp +56 9 4969 1686', f(FB, 58), 1090, AMAR, CARBON, back((u - 1.1) / .5))
        texto(c, 'Precios netos · Emitimos factura', f(FM, 42), 1290, BLANCO, ease((u - 1.5) / .4))
        texto(c, 'Despacho gratis dentro de Vespucio', f(FR, 40), 1360, (170, 178, 188), ease((u - 1.7) / .4))
        texto(c, 'sobre $50.000 + IVA', f(FR, 40), 1412, (170, 178, 188), ease((u - 1.7) / .4))
    return c

n = int(TOTAL * FPS)
for i in range(n):
    frame(i / FPS).convert('RGB').save(f'{TMP}/f{i:04d}.jpg', quality=90)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{TMP}/f%04d.jpg',
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '21', '-movflags', '+faststart',
                '-c:a', 'aac', '-b:a', '128k', OUT], check=True)
for i in (60, 190, 330): frame(i / FPS).convert('RGB').resize((360, 640)).save(f'{TMP}/prev{i}.jpg')
print('ok', OUT)
