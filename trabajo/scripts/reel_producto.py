"""Reels 1080x1920 (~13 s, sin música) de productos (precio normal, sin descuento).
Uso: python3 reel_producto.py <n> <salida.mp4> <carpeta_tmp>
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
insta.LOGO = R + '/trabajo/marca/logo-000.png'
from insta import recortar, patron, sombra, CARBON, TURQ, AMAR, BLANCO, FB, FM, FR, f
from PIL import Image, ImageDraw

ROJO = (224, 71, 58)
# [etiqueta, gancho 1, gancho 2, nombre, detalle, precio neto, foto]
REELS = [
    ['EQUIPAMIENTO', 'Firme como', 'tiene que ser', 'Tornillo de banco 5" YATO', 'Giratorio 360° · con yunque · 12 kN', 148489, 'ms5-tornillo-de-banco-5-125-mm.jpg'],
    ['HERRAMIENTA MANUAL', 'Aprieta fuerte,', 'suelta al tiro', 'Prensa rápida reforzada 300 mm', 'Mayor fuerza de apriete', 24849, 'ms5-prensa-rapida-reforzada-300-mm.jpg'],
    ['LEVANTE', '¿Camión pesado?', 'Arriba sin esfuerzo', 'Gata botella 20 toneladas YATO', 'Altura de 242 a 452 mm', 97889, 'ms5-gata-botella-20-toneladas-2.jpg'],
    ['VULCANIZACIÓN', 'Neumático difícil,', 'llanta intacta', 'Barras desmontaneumáticos YATO', 'Juego de 3 barras de acero forjado', 115489, 'ms5-juego-de-barras-desmontadoras-de-neumaticos.jpg'],
    ['HERRAMIENTA MANUAL', 'Aprieta sin sacar', 'la llave del perno', 'Llaves con chicharra 12 pzas YATO', '8 a 19 mm · 72 dientes', 109989, 'ms5-juego-de-llaves-punta-corona-con-chicharra.jpg'],
    ['IMPACTO', 'Hechos para', 'la pistola de impacto', 'Dados de impacto largos 1/2" YATO', '10 a 24 mm · cromo-molibdeno', 49489, 'ms5-juego-de-dados-de-impacto-largos-12.jpg'],
    ['TAPICERÍA', 'Paneles fuera', 'sin quebrar clips', 'Extractores de tapicería 19 pzas', 'Clips, paneles, radio y tablero', 43989, 'ms5-juego-de-19-extractores-de-tapiceria-y-molduras.jpg'],
    ['HERRAMIENTA MANUAL', 'Remaches grandes', 'con menos fuerza', 'Remachadora tipo fuelle YATO', 'Remaches de 2,4 a 6,4 mm', 41239, 'ms5-remachadora-tipo-fuelle-extensible.jpg'],
    ['FRENOS', 'Purga los frenos', 'sin ayudante', 'Purgador de frenos 22 pzas YATO', 'Bomba de vacío · purga y diagnóstico', 87989, 'ms5-bomba-de-vacio-con-purgador-de-frenos-22-piezas.jpg'],
    ['FRENOS', '¿Cambio de pastillas?', 'El pistón vuelve fácil', 'Juego para caliper 35 piezas YATO', 'Compresión de pistones de caliper', 109989, 'ms5-juego-para-caliper-de-freno-35-piezas.jpg'],
    ['LUBRICACIÓN', 'Engrasa con aire,', 'no con la mano', 'Engrasadora neumática 400 cc YATO', 'Acople rápido de aire comprimido', 41789, 'ms5-pistola-engrasadora-neumatica-400-cc.jpg'],
    ['LUBRICACIÓN', 'Cambio de aceite', 'sin derrames', 'Recuperador de aceite 65 L YATO', 'Embudo de 5 L · aspiración', 302489, 'ms5-recuperador-de-aceite-65-litros-con-embudo.jpg'],
]
N = int(sys.argv[1]); OUT = sys.argv[2]; TMP = sys.argv[3]
ETQ, G1, G2, NOM, DET, PRECIO, FOTO = REELS[N]
W, H, FPS = 1080, 1920, 30
os.makedirs(TMP, exist_ok=True)

logo = Image.open(insta.LOGO).convert('RGBA')
prod = recortar(R + '/' + FOTO)
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
        pastilla(c, 'YATO · ' + ETQ, f(FB, 50), 1100, TURQ, CARBON, back((u - 1.0) / .5))
        texto(c, 'Lo que usan los talleres', f(FM, 50), 1250, AMAR, ease((u - 1.4) / .4))
    elif t < ESC[1][1]:  # producto + precio
        c = fondo_t.copy(); u = t - ESC[1][0]
        d = ImageDraw.Draw(c); d.rectangle((0, 0, W, 200), fill=CARBON)
        texto(c, 'EL SEÑOR DE LOS TARROS', f(FB, 54), 70, AMAR)
        producto(c, 760, 900, 820, back((u - .1) / .6))
        d = ImageDraw.Draw(c)
        if u > 1.0:
            a = ease((u - 1.0) / .4)
            box = Image.new('RGBA', (W, 520), CARBON + (int(235 * a),)); c.alpha_composite(box, (0, 1250))
        texto(c, NOM, f(FB, 52 if len(NOM) < 32 else 46), 1290, BLANCO, ease((u - 1.1) / .4))
        texto(c, DET, f(FM, 40), 1370, (170, 178, 188), ease((u - 1.3) / .4))
        pastilla(c, cl(PRECIO) + ' + IVA', f(FB, 96), 1500, AMAR, CARBON, back((u - 2.0) / .5))
        franja(c)
    else:  # cierre
        c = fondo_c.copy(); u = t - ESC[2][0]
        logo_en(c, 170, 700, ease(u / .5))
        texto(c, 'Pídelo hoy', f(FB, 76), 650, BLANCO, ease((u - .2) / .4))
        texto(c, 'por WhatsApp o en la web', f(FB, 70), 745, AMAR, ease((u - .4) / .4))
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
