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

import math
def bici(c, cx, cy, sc, col, a=1):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); k = col + (int(255 * a),); w = max(3, int(9 * sc))
    r = 95 * sc; A = (cx - 160 * sc, cy); B = (cx + 160 * sc, cy)
    for p in (A, B): d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), outline=k, width=w)
    pd = (cx - 10 * sc, cy); st = (cx - 55 * sc, cy - 150 * sc); hd = (cx + 105 * sc, cy - 145 * sc)
    for p, q in ((A, pd), (A, st), (pd, st), (st, hd), (pd, hd), (hd, B)): d.line((p, q), fill=k, width=w)
    d.line(((st[0] - 40 * sc, st[1] - 18 * sc), (st[0] + 30 * sc, st[1] - 18 * sc)), fill=k, width=w + 4)
    d.line((hd, (hd[0] - 10 * sc, hd[1] - 45 * sc)), fill=k, width=w); d.line(((hd[0] - 10 * sc, hd[1] - 45 * sc), (hd[0] + 45 * sc, hd[1] - 50 * sc)), fill=k, width=w)
    d.ellipse((pd[0] - 22 * sc, pd[1] - 22 * sc, pd[0] + 22 * sc, pd[1] + 22 * sc), outline=k, width=w)
    c.alpha_composite(lay)
def moto(c, cx, cy, sc, col, a=1):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); k = col + (int(255 * a),); w = max(3, int(9 * sc))
    P = lambda x, y: (cx + x * sc, cy + y * sc)
    r = 88 * sc
    for (x, y) in ((-175, 0), (185, 0)):
        X, Y = P(x, y); d.ellipse((X - r, Y - r, X + r, Y + r), outline=k, width=w + 8)
        d.ellipse((X - 20 * sc, Y - 20 * sc, X + 20 * sc, Y + 20 * sc), fill=k)
    d.line((P(185, 0), P(105, -175)), fill=k, width=w + 6)              # horquilla
    d.line((P(-175, 0), P(-20, -40)), fill=k, width=w + 6)              # basculante
    d.polygon([P(-40, -95), P(70, -110), P(105, -150), P(40, -165), P(-30, -140)], fill=k)   # estanque
    d.polygon([P(-230, -125), P(-40, -125), P(-40, -100), P(-200, -100)], fill=k)          # asiento
    d.polygon([P(-250, -115), P(-150, -95), P(-170, -85), P(-260, -100)], fill=k)          # tapabarro trasero
    d.rounded_rectangle((P(-40, -90)[0], P(-40, -90)[1], P(40, -15)[0], P(40, -15)[1]), radius=int(14 * sc), fill=k)  # motor
    d.line((P(-20, -25), P(-150, -60)), fill=k, width=w)                 # escape
    d.line((P(80, -190), P(150, -205)), fill=k, width=w + 4)            # manubrio
    d.line((P(105, -175), P(95, -195)), fill=k, width=w + 2)
    d.ellipse((P(120, -165)[0] - 16 * sc, P(120, -165)[1] - 16 * sc, P(120, -165)[0] + 16 * sc, P(120, -165)[1] + 16 * sc), fill=k)  # foco
    c.alpha_composite(lay)
def gotas(c, y0, u):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(26):
        ph = (u * 1.6 + i * 0.0385) % 1; x = -20 + ph * 520; y = y0 + ((i * 37) % 90 - 45) + ph * 40
        al = int(255 * min(1, (1 - ph) * 1.6)); rr = 7 + (i % 3) * 3; d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(111, 200, 218, al))
    c.alpha_composite(lay)
ESC = [0, 3.0, 7.0, 10.5, 14.5, 18.5]
def frame(t):
    if t < ESC[1]:  # gancho
        c = fondo_c.copy(); u = t
        logo_en(c, 170, 600, ease(u / .5))
        texto(c, '¿Bici o moto', f(FB, 88), 760, BLANCO, ease((u - .25) / .4), 40 * (1 - ease((u - .25) / .4)))
        texto(c, 'llena de barro?', f(FB, 88), 870, AMAR, ease((u - .5) / .4), 40 * (1 - ease((u - .5) / .4)))
        pastilla(c, 'PROMO DE LA TARDE', f(FB, 58), 1100, ROJO, BLANCO, back((u - 1.0) / .5))
        texto(c, 'Agua a presión, sin enchufe', f(FM, 50), 1250, TURQ, ease((u - 1.4) / .4))
    elif t < ESC[2]:  # ideal para bicicletas y motos
        c = fondo_c.copy(); u = t - ESC[1]
        texto(c, 'IDEAL PARA', f(FB, 64), 150, TURQ, ease(u / .4))
        texto(c, 'BICICLETAS', f(FB, 110), 240, AMAR, ease((u - .15) / .4), 30 * (1 - ease((u - .15) / .4)))
        bici(c, W // 2, 700, 1.25 * back((u - .3) / .6) if u > .3 else 0.01, BLANCO, ease((u - .3) / .4))
        texto(c, 'Y MOTOS', f(FB, 110), 920, AMAR, ease((u - 1.2) / .4), 30 * (1 - ease((u - 1.2) / .4)))
        moto(c, W // 2 + 20, 1400, 1.15 * back((u - 1.4) / .6) if u > 1.4 else 0.01, BLANCO, ease((u - 1.4) / .4))
        if u > 2.0: gotas(c, 640, u); gotas(c, 1300, u + .3)
        texto(c, 'Barro y grasa fuera, sin enchufe', f(FM, 48), 1640, TURQ, ease((u - 2.4) / .4))
    elif t < ESC[3]:  # producto
        c = fondo_t.copy(); u = t - ESC[2]
        ImageDraw.Draw(c).rectangle((0, 0, W, 200), fill=CARBON)
        texto(c, 'HIDROLAVADORA INALÁMBRICA', f(FB, 54), 70, AMAR)
        pieza(c, g, W // 2, 720, 940, 760, back((u - .1) / .6), rot=-6 * (1 - ease(u / 1.2)))
        if u > 1.0:
            a = ease((u - 1.0) / .4); c.alpha_composite(Image.new('RGBA', (W, 470), CARBON + (int(235 * a),)), (0, 1260))
        texto(c, 'Redbo HL20BL · batería 20 V 4,0 Ah', f(FB, 48), 1300, BLANCO, ease((u - 1.1) / .4))
        texto(c, 'Motor brushless · 9 a 35 bar', f(FM, 44), 1385, BLANCO, ease((u - 1.4) / .4))
        texto(c, '4,09 L/min · agua de balde o llave', f(FM, 44), 1450, GR, ease((u - 1.7) / .4))
        pastilla(c, 'Bicicletas · motos · autos · pisos', f(FB, 40), 1545, TURQ, CARBON, back((u - 2.0) / .5))
        franja(c)
    elif t < ESC[4]:  # kit completo + precio
        c = fondo_t.copy(); u = t - ESC[3]
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
        c = fondo_c.copy(); u = t - ESC[4]
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
for i in (60, 175, 270, 380, 500): frame(i / FPS).convert('RGB').resize((360, 640)).save(f'{TMP}/prev{i}.jpg')
print('ok')
