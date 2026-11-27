"""Estado/historia Black Friday 1080x1920. Uso: estado_blackfriday.py foto nombre precio_normal salida [etiqueta]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import recortar, colocar, texto_ajustado, f, FB, FM, FR, AMAR, BLANCO
from PIL import Image, ImageDraw
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'
foto, nom, normal, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
etq = sys.argv[5] if len(sys.argv) > 5 else 'BLACK FRIDAY'
final = int(sys.argv[6]) if len(sys.argv) > 6 else round(normal * 0.8)
sub = sys.argv[7] if len(sys.argv) > 7 else 'Bomba de hoy · 20% menos'
pct = round((1 - final / normal) * 100)
cl = lambda v: '$' + f'{round(v):,}'.replace(',', '.')
W, H = 1080, 1920
c = Image.new('RGB', (W, H), (11, 11, 11)); d = ImageDraw.Draw(c)
for k in range(-H, W, 70): d.polygon([(k, H), (k + 35, H), (k + 35 + H, 0), (k + H, 0)], fill=(20, 20, 20))
logo = Image.open(R + 'trabajo/marca/logo-000.png').convert('RGBA'); l = logo.resize((int(logo.width * 190 / logo.height), 190), Image.LANCZOS)
c.paste(l, ((W - l.width) // 2, 60), l)
fe = f(FB, 128)
while d.textlength(etq, font=fe) > W - 120: fe = f(FB, fe.size - 6)
d.text((W // 2, 360), etq, font=fe, fill=AMAR, anchor='mm')
d.text((W // 2, 460), sub, font=f(FM, 46), fill=BLANCO, anchor='mm')
d.rounded_rectangle([110, 540, W - 110, 1220], radius=40, fill=BLANCO)
colocar(c, recortar(R + foto), (150, 580, W - 150, 1180))
d.ellipse([W - 250, 490, W - 80, 660], fill=AMAR); d.text((W - 165, 575), f'-{pct}%', font=f(FB, 52), fill=(0, 0, 0), anchor='mm')
ft, ls = texto_ajustado(d, nom, FB, W - 140, 60, 40); y = 1290
for ln in ls: d.text((W // 2, y), ln, font=ft, fill=BLANCO, anchor='mm'); y += ft.size + 12
a = 'Antes ' + cl(normal); fa = f(FM, 44); aw = d.textlength(a, font=fa)
d.text((W // 2, y + 30), a, font=fa, fill=(150, 156, 162), anchor='mm'); d.line([(W // 2 - aw / 2, y + 32), (W // 2 + aw / 2, y + 32)], fill=(150, 156, 162), width=4)
t = cl(final) + ' + IVA'; fp = f(FB, 96); tw = d.textlength(t, font=fp); py = y + 90
d.rounded_rectangle([W // 2 - tw / 2 - 50, py, W // 2 + tw / 2 + 50, py + 150], radius=75, fill=AMAR)
d.text((W // 2, py + 75), t, font=fp, fill=(0, 0, 0), anchor='mm')
d.text((W // 2, H - 170), (sys.argv[8] if len(sys.argv) > 8 else 'Solo hoy o hasta agotar stock'), font=f(FM, 40), fill=BLANCO, anchor='mm')
d.text((W // 2, H - 100), 'WhatsApp +56 9 4969 1686 · elsenordelostarros.cl', font=f(FB, 38), fill=AMAR, anchor='mm')
c.save(out, quality=92); print(out)
