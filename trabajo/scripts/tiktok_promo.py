"""Video TikTok/Reels 1080x1920 de la promo de octubre (sin música: el sonido se agrega en TikTok)."""
import sys, os, subprocess, math, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
insta.LOGO = R + '/trabajo/marca/logo-000.png'
from insta import recortar, patron, sombra, CARBON, TURQ, AMAR, BLANCO, FB, FM, FR, f
from PIL import Image, ImageDraw, ImageFilter
DADOS = sys.argv[1]; OUT = sys.argv[2]; TMP = sys.argv[3]
W, H, FPS = 1080, 1920, 30
os.makedirs(TMP, exist_ok=True)

logo = Image.open(insta.LOGO).convert('RGBA')
guante = recortar(R + '/ms-guante-de-nitrilo-naranjo-texturizado-alto-espesor-tallas-s-a-xl.jpg')
dados = recortar(DADOS)
fondo_t = patron((W, H)).convert('RGBA')
fondo_c = Image.new('RGBA', (W, H), CARBON + (255,))

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.7
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def fit(p, h): return p.resize((max(1, int(p.width * h / p.height)), max(1, int(h))), Image.LANCZOS)

def texto(c, txt, font, y, fill, alpha=1, dy=0, anchor='mt', x=W // 2):
    if alpha <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y + dy), txt, font=font, fill=fill + (int(255 * alpha),), anchor=anchor)
    c.alpha_composite(lay)

def pastilla(c, txt, font, y, bg, fg, alpha=1, s=1.0, pad=(34, 18)):
    if alpha <= 0 or s <= 0.01: return
    d0 = ImageDraw.Draw(c); w = d0.textlength(txt, font=font); h = font.size
    bw, bh = int(w + pad[0] * 2), int(h + pad[1] * 2 + 8)
    b = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=18, fill=bg + (255,))
    d.text((bw // 2, pad[1]), txt, font=font, fill=fg, anchor='mt')
    if s != 1: b = b.resize((max(1, int(bw * s)), max(1, int(bh * s))), Image.LANCZOS)
    if alpha < 1: b.putalpha(b.split()[3].point(lambda v: int(v * alpha)))
    c.alpha_composite(b, (W // 2 - b.width // 2, int(y + bh / 2 - b.height / 2)))

def producto(c, p, cy, h, s):
    if s <= 0.01: return
    q = fit(p, h * s); sh = sombra(q, blur=30, op=120, dy=26); pad = (sh.width - q.width) // 2
    x, y = W // 2 - q.width // 2, int(cy - q.height / 2)
    c.alpha_composite(sh, (x - pad, y - pad)); c.alpha_composite(q, (x, y))

def logo_en(c, y, w, alpha=1):
    l = logo.resize((w, int(logo.height * w / logo.width)), Image.LANCZOS)
    if alpha < 1: l.putalpha(int(255 * alpha))
    c.alpha_composite(l, (W // 2 - w // 2, y))

def franja(c):  # pie con WhatsApp en todas las escenas
    d = ImageDraw.Draw(c); d.rectangle((0, H - 150, W, H), fill=AMAR)
    d.text((W // 2, H - 75), 'Pedidos WhatsApp +56 9 4969 1686', font=f(FB, 44), fill=CARBON, anchor='mm')

ESC = [(0, 3.2), (3.2, 7.4), (7.4, 11.6), (11.6, 15.5)]
TOTAL = ESC[-1][1]

def frame(t):
    if t < ESC[0][1]:  # 1 · gancho
        c = fondo_c.copy(); u = t
        logo_en(c, 170, 760, ease(u / 0.5))
        texto(c, '¿COMPRAS PARA', f(FB, 92), 720, BLANCO, ease((u - .3) / .4), dy=40 * (1 - ease((u - .3) / .4)))
        texto(c, 'TU TALLER?', f(FB, 92), 830, BLANCO, ease((u - .5) / .4), dy=40 * (1 - ease((u - .5) / .4)))
        pastilla(c, 'ESTE MES TE REGALAMOS', f(FB, 58), 1030, AMAR, CARBON, 1, back((u - .9) / .5))
        texto(c, 'algo con tu compra', f(FM, 54), 1180, TURQ, ease((u - 1.3) / .4))
        texto(c, 'Promo de octubre 2026', f(FR, 40), 1290, (170, 178, 188), ease((u - 1.6) / .4))
    elif t < ESC[2][1]:  # 2 y 3 · regalos
        k = 0 if t < ESC[1][1] else 1; u = t - ESC[1 + k][0]
        c = fondo_t.copy()
        d = ImageDraw.Draw(c); d.rectangle((0, 0, W, 210), fill=CARBON)
        texto(c, f'REGALO {k + 1} DE 2', f(FB, 60), 70, AMAR)
        pastilla(c, 'SOBRE ' + ('$100.000' if k == 0 else '$200.000') + ' + IVA', f(FB, 74), 300, AMAR, CARBON, 1, back(u / .45))
        producto(c, guante if k == 0 else dados, 960, 820 if k == 0 else 860, back((u - .3) / .6))
        nombre = 'Caja de guantes de nitrilo naranjos' if k == 0 else 'Set de dados 1/4"'
        sub = 'Texturizados, alto espesor' if k == 0 else 'Con chicharra y extensión'
        pastilla(c, 'TE LLEVAS GRATIS', f(FB, 50), 1440, CARBON, BLANCO, ease((u - .9) / .3), 1)
        texto(c, nombre, f(FB, 56), 1560, CARBON, ease((u - 1.1) / .4), dy=30 * (1 - ease((u - 1.1) / .4)))
        texto(c, sub, f(FM, 42), 1640, CARBON, ease((u - 1.3) / .4))
        franja(c)
    else:  # 4 · cierre
        c = fondo_c.copy(); u = t - ESC[3][0]
        logo_en(c, 150, 700, ease(u / .5))
        texto(c, 'Compra en la tienda', f(FB, 70), 640, BLANCO, ease((u - .2) / .4))
        texto(c, 'o pide por WhatsApp', f(FB, 70), 730, BLANCO, ease((u - .4) / .4))
        pastilla(c, 'elsenordelostarros.cl', f(FB, 64), 900, TURQ, CARBON, 1, back((u - .7) / .5))
        pastilla(c, '+56 9 4969 1686', f(FB, 64), 1060, AMAR, CARBON, 1, back((u - 1.0) / .5))
        texto(c, 'Válido hasta el 31 de octubre', f(FM, 46), 1260, BLANCO, ease((u - 1.4) / .4))
        texto(c, 'Montos netos · Emitimos factura', f(FR, 38), 1340, (170, 178, 188), ease((u - 1.6) / .4))
        texto(c, 'Despacho Santiago $5.000', f(FR, 38), 1395, (170, 178, 188), ease((u - 1.6) / .4))
    return c

n = int(TOTAL * FPS)
for i in range(n):
    frame(i / FPS).convert('RGB').save(f'{TMP}/f{i:04d}.jpg', quality=92)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{TMP}/f%04d.jpg',
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '20', '-movflags', '+faststart',
                '-c:a', 'aac', '-b:a', '128k', OUT], check=True)
for i in (45, 160, 300, 440): frame(i / FPS).convert('RGB').resize((360, 640)).save(f'{TMP}/prev{i}.jpg')
print('ok', n, 'frames')
