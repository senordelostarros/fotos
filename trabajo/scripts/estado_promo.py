"""Estado WhatsApp 1080x1920 de promoción. Uso: estado_promo.py foto titulo detalle1 detalle2 precio salida"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import recortar, colocar, texto_ajustado, f, FB, FM, FR, CARBON, TURQ, AMAR, BLANCO, GRIS
from PIL import Image, ImageDraw
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'
insta.LOGO = R + 'trabajo/marca/logo-000.png'
foto, tit, d1, d2, precio, out = sys.argv[1:7]
W, H = 1080, 1920
c = Image.new('RGB', (W, H), BLANCO); d = ImageDraw.Draw(c)
d.rectangle([0, 0, W, 300], fill=CARBON)
logo = Image.open(insta.LOGO).convert('RGBA'); l = logo.resize((int(logo.width * 230 / logo.height), 230), Image.LANCZOS)
c.paste(l, ((W - l.width) // 2, 35), l)
d.rectangle([0, 300, W, 312], fill=TURQ); d.rectangle([0, 312, W, 320], fill=AMAR)
d.rounded_rectangle([W // 2 - 230, 370, W // 2 + 230, 450], radius=40, fill=(224, 71, 58))
d.text((W // 2, 410), 'PROMOCIÓN', font=f(FB, 48), fill=BLANCO, anchor='mm')
colocar(c, recortar(R + foto), (90, 500, W - 90, 1080))
ft, ls = texto_ajustado(d, tit, FB, W - 140, 66, 44); y = 1150
for ln in ls: d.text((W // 2, y), ln, font=ft, fill=CARBON, anchor='mm'); y += ft.size + 12
d.text((W // 2, y + 10), d1, font=f(FM, 40), fill=(90, 98, 108), anchor='mm')
d.text((W // 2, y + 62), d2, font=f(FM, 40), fill=(90, 98, 108), anchor='mm')
t = precio + ' + IVA'; fp = f(FB, 86); tw = d.textlength(t, font=fp); py = y + 120
d.rounded_rectangle([W // 2 - tw / 2 - 45, py, W // 2 + tw / 2 + 45, py + 140], radius=70, fill=AMAR)
d.text((W // 2, py + 70), t, font=fp, fill=CARBON, anchor='mm')
d.rectangle([0, H - 240, W, H], fill=CARBON)
d.text((W // 2, H - 170), 'Pídelo por WhatsApp +56 9 4969 1686', font=f(FB, 46), fill=AMAR, anchor='mm')
d.text((W // 2, H - 105), 'Despacho gratis dentro de Vespucio sobre $50.000 + IVA', font=f(FM, 32), fill=BLANCO, anchor='mm')
d.text((W // 2, H - 55), 'elsenordelostarros.cl', font=f(FR, 30), fill=TURQ, anchor='mm')
c.save(out, quality=92); print(out)
