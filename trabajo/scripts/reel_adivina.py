"""Reel formato "¿Adivinas qué herramienta es?" 1080x1920, ~15 s, sin música.
Uso: python3 reel_adivina.py <clave> <salida.mp4> <carpeta_tmp>
Escenas: detalle con zoom + cuenta 3-2-1 / revelación / 3 usos / precio / cierre con pregunta.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
insta.LOGO = R + '/trabajo/marca/logo-000.png'
from insta import recortar, patron, sombra, CARBON, TURQ, AMAR, BLANCO, FB, FM, FR, f
from PIL import Image, ImageDraw, ImageFilter

ROJO = (224, 71, 58)
GRIS = (170, 178, 188)
# clave: [foto, punto de zoom (x,y en fracción), "Es un/una…", nombre, código, 3 usos, precio neto, bomba?]
DATOS = {
    'esmeril': ['ms2-esmeril-angular-de-5-125mm-1100-w-1200-rpm.jpg', (0.20, 0.60), 'Es un esmeril angular',
                'Esmeril angular 5" 1100 W YATO', 'YT82101',
                ['Corta acero e inoxidable', 'Desbasta soldaduras', 'Velocidad regulable en 6 pasos'], 115489, True],
    'grata': ['ms2-grata-copa-trenzada-100mm-para-galletero-m14.jpg', (0.50, 0.84), 'Es una grata copa',
              'Grata copa trenzada 100 mm YATO', 'YT4769',
              ['Saca óxido y pintura', 'Limpia escoria de soldadura', 'Para esmeril con hilo M14'], 26059, False],
    'sierra': ['ms-kit-de-sierra-copa-para-metal-9-piezas.jpg', (0.20, 0.32), 'Es un kit de sierra copa',
               'Sierra copa para metal 9 piezas YATO', 'YT3380',
               ['De 22 a 73 mm', 'Corta hasta 40 mm de profundidad', 'Acero inoxidable, tubos y madera'], 54439, False],
}
CLAVE, OUT, TMP = sys.argv[1], sys.argv[2], sys.argv[3]
FOTO, ZP, ES, NOM, COD, USOS, PRECIO, BOMBA = DATOS[CLAVE]
W, H, FPS = 1080, 1920, 30
os.makedirs(TMP, exist_ok=True)

logo = Image.open(insta.LOGO).convert('RGBA')
orig = Image.open(R + '/' + FOTO).convert('RGB')
prod = recortar(R + '/' + FOTO)
fondo_t = patron((W, H)).convert('RGBA')
fondo_c = Image.new('RGBA', (W, H), CARBON + (255,))
def cl(v): return '$' + f'{round(v):,}'.replace(',', '.')
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.7
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def fitbox(p, w, h):
    s = min(w / p.width, h / p.height); return p.resize((max(1, int(p.width * s)), max(1, int(p.height * s))), Image.LANCZOS)

def texto(c, txt, font, y, fill, alpha=1, dy=0, x=None, anchor='mt'):
    if alpha <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W // 2 if x is None else x, y + dy), txt, font=font, fill=fill + (int(255 * alpha),), anchor=anchor)
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

def logo_en(c, y, w, alpha=1):
    l = logo.resize((w, int(logo.height * w / logo.width)), Image.LANCZOS)
    if alpha < 1: l.putalpha(int(255 * alpha))
    c.alpha_composite(l, (W // 2 - w // 2, y))

def franja(c):
    d = ImageDraw.Draw(c); d.rectangle((0, H - 150, W, H), fill=AMAR)
    d.text((W // 2, H - 75), 'Pedidos WhatsApp +56 9 4969 1686', font=f(FB, 44), fill=CARBON, anchor='mm')

D = 760  # diámetro de la lupa
def lupa(z):
    """Recorte circular del detalle. z = tamaño del recorte en fracción del lado menor (chico = más zoom)."""
    s = min(orig.size) * z; cx, cy = orig.width * ZP[0], orig.height * ZP[1]
    x0 = max(0, min(orig.width - s, cx - s / 2)); y0 = max(0, min(orig.height - s, cy - s / 2))
    q = orig.crop((int(x0), int(y0), int(x0 + s), int(y0 + s))).resize((D, D), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (D, D), 0); ImageDraw.Draw(m).ellipse((0, 0, D - 1, D - 1), fill=255)
    q.putalpha(m)
    return q

ESC = [(0, 4.2), (4.2, 6.4), (6.4, 10.4), (10.4, 13.4), (13.4, 16.4)]
TOTAL = ESC[-1][1]

def frame(t):
    if t < ESC[0][1]:  # detalle + pregunta + cuenta regresiva
        c = fondo_c.copy(); u = t
        texto(c, '¿Adivinas qué', f(FB, 92), 170, BLANCO, ease(u / .4), dy=30 * (1 - ease(u / .4)))
        texto(c, 'herramienta es?', f(FB, 92), 280, AMAR, ease((u - .25) / .4), dy=30 * (1 - ease((u - .25) / .4)))
        z = 0.30 + 0.10 * (u / ESC[0][1])  # zoom que se abre lento
        q = lupa(z); s = back((u - .3) / .6)
        if s > .01:
            qq = q.resize((max(1, int(D * s)), max(1, int(D * s))), Image.LANCZOS)
            cy = 900
            ring = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ring)
            r = int(D * s / 2) + 14
            dr.ellipse((W // 2 - r, cy - r, W // 2 + r, cy + r), fill=TURQ + (255,))
            c.alpha_composite(ring)
            c.alpha_composite(qq, (W // 2 - qq.width // 2, cy - qq.height // 2))
        n = 3 - int((u - 1.2) // 1.0)
        if 1.2 <= u and 1 <= n <= 3:
            k = ((u - 1.2) % 1.0)
            pastilla(c, str(n), f(FB, 120), 1420, AMAR, CARBON, back(k / .35))
        texto(c, 'Escríbelo en los comentarios', f(FM, 46), 1650, GRIS, ease((u - 1.0) / .4))
    elif t < ESC[1][1]:  # revelación
        c = fondo_t.copy(); u = t - ESC[1][0]
        d = ImageDraw.Draw(c); d.rectangle((0, 0, W, 230), fill=CARBON)
        texto(c, '¡' + ES + '!', f(FB, 64 if len(ES) < 24 else 56), 80, AMAR, ease(u / .3))
        producto(c, 900, 940, 1000, back((u - .1) / .55))
        flash = max(0, 1 - u / .35)
        if flash > 0: c.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(220 * flash))))
        franja(c)
    elif t < ESC[2][1]:  # 3 usos
        c = fondo_t.copy(); u = t - ESC[2][0]
        d = ImageDraw.Draw(c); d.rectangle((0, 0, W, 230), fill=CARBON)
        texto(c, '¿Para qué sirve?', f(FB, 70), 75, BLANCO)
        producto(c, 640, 760, 680, 1)
        for i, us in enumerate(USOS):
            a = back((u - .3 - i * .7) / .45)
            if a <= .01: continue
            y = 1080 + i * 175
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            bw = int(940 * min(1, a)); x0 = W // 2 - 470
            dl.rounded_rectangle((x0, y, x0 + bw, y + 140), radius=24, fill=CARBON + (240,))
            c.alpha_composite(lay)
            if a > .6:
                dd = ImageDraw.Draw(c)
                dd.ellipse((x0 + 30, y + 35, x0 + 100, y + 105), fill=AMAR)
                dd.text((x0 + 65, y + 70), str(i + 1), font=f(FB, 46), fill=CARBON, anchor='mm')
                fs = 46 if len(us) < 28 else 40
                dd.text((x0 + 130, y + 70), us, font=f(FB, fs), fill=BLANCO, anchor='lm')
        franja(c)
    elif t < ESC[3][1]:  # precio
        c = fondo_t.copy(); u = t - ESC[3][0]
        d = ImageDraw.Draw(c); d.rectangle((0, 0, W, 230), fill=CARBON)
        texto(c, 'BOMBA DEL DÍA' if BOMBA else 'Precio de hoy', f(FB, 70), 75, AMAR if BOMBA else BLANCO)
        producto(c, 700, 860, 760, 1)
        box = Image.new('RGBA', (W, 560), CARBON + (235,)); c.alpha_composite(box, (0, 1180))
        texto(c, NOM, f(FB, 50 if len(NOM) < 32 else 44), 1220, BLANCO, ease(u / .4))
        texto(c, 'Código ' + COD, f(FM, 40), 1300, GRIS, ease((u - .2) / .4))
        y = 1380
        if BOMBA:
            a = ease((u - .4) / .4)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            fa = f(FM, 48); ta = 'Antes ' + cl(PRECIO); wa = dl.textlength(ta, font=fa)
            dl.text((W // 2, y), ta, font=fa, fill=GRIS + (int(255 * a),), anchor='mt')
            dl.line((W // 2 - wa / 2, y + 30, W // 2 + wa / 2, y + 30), fill=GRIS + (int(255 * a),), width=4)
            c.alpha_composite(lay); y += 90
        p = PRECIO * (.8 if BOMBA else 1)
        pastilla(c, cl(p) + ' + IVA', f(FB, 96), y + 40, AMAR, CARBON, back((u - .7) / .5))
        if BOMBA: texto(c, '20% menos, solo por hoy', f(FM, 44), y + 210, TURQ, ease((u - 1.1) / .4))
        franja(c)
    else:  # cierre
        c = fondo_c.copy(); u = t - ESC[4][0]
        logo_en(c, 170, 700, ease(u / .5))
        texto(c, '¿Le achuntaste?', f(FB, 84), 640, BLANCO, ease((u - .2) / .4))
        texto(c, 'Cuéntanos en los comentarios', f(FB, 58), 750, AMAR, ease((u - .4) / .4))
        pastilla(c, 'elsenordelostarros.cl', f(FB, 62), 930, TURQ, CARBON, back((u - .8) / .5))
        pastilla(c, 'WhatsApp +56 9 4969 1686', f(FB, 58), 1090, AMAR, CARBON, back((u - 1.1) / .5))
        texto(c, 'Precios netos · Emitimos factura', f(FM, 42), 1290, BLANCO, ease((u - 1.5) / .4))
        texto(c, 'Despacho gratis dentro de Vespucio', f(FR, 40), 1360, GRIS, ease((u - 1.7) / .4))
        texto(c, 'sobre $50.000 + IVA', f(FR, 40), 1412, GRIS, ease((u - 1.7) / .4))
    return c

n = int(TOTAL * FPS)
for i in range(n):
    frame(i / FPS).convert('RGB').save(f'{TMP}/f{i:04d}.jpg', quality=90)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{TMP}/f%04d.jpg',
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '21', '-movflags', '+faststart',
                '-c:a', 'aac', '-b:a', '128k', OUT], check=True)
for i in (75, 160, 260, 360, 460): frame(i / FPS).convert('RGB').resize((360, 640)).save(f'{TMP}/prev{i}.jpg')
print('ok', OUT)
