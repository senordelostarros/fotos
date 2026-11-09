"""Reel promo de la tarde 1080x1920 ~16 s · Hidrolavadora inalámbrica Redbo HL20BL $79.900 + IVA."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
insta.LOGO = R + '/trabajo/marca/logo-000.png'
from insta import recortar, patron, sombra, CARBON, TURQ, AMAR, BLANCO, FB, FM, FR, f
from PIL import Image, ImageDraw
OUT, TMP = sys.argv[1], sys.argv[2]; os.makedirs(TMP, exist_ok=True)
ROJO = (224, 71, 58); GR = (170, 178, 188)
W, H, FPS = 1080, 1920, 30
logo = Image.open(insta.LOGO).convert('RGBA')
g = recortar(R + '/ms2-hidrolavadora-inalambrica-20v-redbo-hl20bl.jpg')
from recorte_todo import recortar_todo
kit = recortar_todo(R + '/ms-hidrolavadora-inalambrica-20v-redbo-hl20bl.jpg')
fondo_t = patron((W, H)).convert('RGBA'); fondo_c = Image.new('RGBA', (W, H), CARBON + (255,))
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.7; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def fitbox(p, w, h):
    s = min(w / p.width, h / p.height); return p.resize((max(1, int(p.width * s)), max(1, int(p.height * s))), Image.LANCZOS)
def texto(c, txt, font, y, fill, a=1, dy=0):
    if a <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((W // 2, y + dy), txt, font=font, fill=fill + (int(255 * a),), anchor='mt'); c.alpha_composite(lay)
def pastilla(c, txt, font, y, bg, fg, s=1.0, pad=(36, 18)):
    if s <= .01: return
    w = ImageDraw.Draw(c).textlength(txt, font=font); h = font.size
    bw, bh = int(w + pad[0] * 2), int(h + pad[1] * 2 + 8)
    b = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=18, fill=bg + (255,)); d.text((bw // 2, pad[1]), txt, font=font, fill=fg, anchor='mt')
    if s != 1: b = b.resize((max(1, int(bw * s)), max(1, int(bh * s))), Image.LANCZOS)
    c.alpha_composite(b, (W // 2 - b.width // 2, int(y + bh / 2 - b.height / 2)))
def pieza(c, p, cx, cy, w, h, s, rot=0):
    if s <= .01: return
    q = fitbox(p, w * s, h * s)
    if rot: q = q.rotate(rot, resample=Image.BICUBIC, expand=True)
    sh = sombra(q, blur=26, op=110, dy=22); pad = (sh.width - q.width) // 2
    x, y = int(cx - q.width / 2), int(cy - q.height / 2); c.alpha_composite(sh, (x - pad, y - pad)); c.alpha_composite(q, (x, y))
def logo_en(c, y, w, a=1):
    l = logo.resize((w, int(logo.height * w / logo.width)), Image.LANCZOS)
    if a < 1: l.putalpha(Image.eval(l.getchannel('A'), lambda v: int(v * a)))
    c.alpha_composite(l, (W // 2 - w // 2, y))
def franja(c):
    d = ImageDraw.Draw(c); d.rectangle((0, H - 150, W, H), fill=AMAR)
    d.text((W // 2, H - 75), 'Pedidos WhatsApp +56 9 4969 1686', font=f(FB, 44), fill=CARBON, anchor='mm')
ESC = [0, 3.0, 7.5, 11.5, 16.0]
def frame(t):
    if t < ESC[1]:  # gancho
        c = fondo_c.copy(); u = t
        logo_en(c, 170, 600, ease(u / .5))
        texto(c, '¿Lavas el auto', f(FB, 88), 760, BLANCO, ease((u - .25) / .4), 40 * (1 - ease((u - .25) / .4)))
        texto(c, 'con balde y esponja?', f(FB, 80), 870, AMAR, ease((u - .5) / .4), 40 * (1 - ease((u - .5) / .4)))
        pastilla(c, 'PROMO DE LA TARDE', f(FB, 58), 1100, ROJO, BLANCO, back((u - 1.0) / .5))
        texto(c, 'Agua a presión, sin enchufe', f(FM, 50), 1250, TURQ, ease((u - 1.4) / .4))
    elif t < ESC[2]:  # producto
        c = fondo_t.copy(); u = t - ESC[1]
        ImageDraw.Draw(c).rectangle((0, 0, W, 200), fill=CARBON)
        texto(c, 'HIDROLAVADORA INALÁMBRICA', f(FB, 54), 70, AMAR)
        pieza(c, g, W // 2, 720, 940, 760, back((u - .1) / .6), rot=-6 * (1 - ease(u / 1.2)))
        if u > 1.0:
            a = ease((u - 1.0) / .4); c.alpha_composite(Image.new('RGBA', (W, 470), CARBON + (int(235 * a),)), (0, 1260))
        texto(c, 'Redbo HL20BL · batería 20 V 4,0 Ah', f(FB, 48), 1300, BLANCO, ease((u - 1.1) / .4))
        texto(c, 'Motor brushless · 9 a 35 bar', f(FM, 44), 1385, BLANCO, ease((u - 1.4) / .4))
        texto(c, '4,09 L/min · agua de balde o llave', f(FM, 44), 1450, GR, ease((u - 1.7) / .4))
        pastilla(c, 'Autos · motos · pisos · maquinaria', f(FB, 40), 1545, TURQ, CARBON, back((u - 2.0) / .5))
        franja(c)
    elif t < ESC[3]:  # kit completo + precio
        c = fondo_t.copy(); u = t - ESC[2]
        ImageDraw.Draw(c).rectangle((0, 0, W, 200), fill=CARBON)
        texto(c, 'KIT COMPLETO', f(FB, 64), 62, AMAR)
        pieza(c, kit, W // 2, 690, 900, 860, back((u - .1) / .6))
        if u > 1.0:
            a = ease((u - 1.0) / .4); c.alpha_composite(Image.new('RGBA', (W, 560), CARBON + (int(240 * a),)), (0, 1180))
        texto(c, 'Con batería, cargador, espumadora y estuche', f(FM, 40), 1225, TURQ, ease((u - 1.1) / .4))
        pastilla(c, '$79.900', f(FB, 150), 1330, AMAR, CARBON, back((u - 1.4) / .5), pad=(50, 16))
        texto(c, '+ IVA · emitimos factura', f(FM, 46), 1560, BLANCO, ease((u - 1.9) / .4))
        franja(c)
    else:  # cierre
        c = fondo_c.copy(); u = t - ESC[3]
        logo_en(c, 170, 700, ease(u / .5))
        texto(c, 'Pídela esta tarde', f(FB, 80), 650, BLANCO, ease((u - .2) / .4))
        texto(c, 'y llega mañana', f(FB, 80), 750, AMAR, ease((u - .4) / .4))
        pastilla(c, 'WhatsApp +56 9 4969 1686', f(FB, 58), 930, AMAR, CARBON, back((u - .8) / .5))
        pastilla(c, 'elsenordelostarros.cl', f(FB, 58), 1090, TURQ, CARBON, back((u - 1.1) / .5))
        texto(c, 'Despacho en 24 horas', f(FM, 42), 1290, BLANCO, ease((u - 1.5) / .4))
        texto(c, 'Gratis dentro de Vespucio', f(FR, 40), 1360, GR, ease((u - 1.7) / .4))
        texto(c, 'sobre $50.000 + IVA', f(FR, 40), 1412, GR, ease((u - 1.7) / .4))
    return c
n = int(ESC[-1] * FPS)
for i in range(n): frame(i / FPS).convert('RGB').save(f'{TMP}/f{i:04d}.jpg', quality=90)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{TMP}/f%04d.jpg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '22', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', OUT], check=True)
for i in (60, 200, 320, 420): frame(i / FPS).convert('RGB').resize((360, 640)).save(f'{TMP}/prev{i}.jpg')
print('ok')
