"""Estado WhatsApp 1080x1920: descuento especial para clientes habituales (consultar por interno)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import patron, f, FB, FM, FR, CARBON, TURQ, AMAR, BLANCO
from PIL import Image, ImageDraw
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'
insta.LOGO = R + 'trabajo/marca/logo-000.png'
W, H = 1080, 1920
c = patron((W, H)).convert('RGB'); d = ImageDraw.Draw(c)
logo = Image.open(insta.LOGO).convert('RGBA')
l = logo.resize((760, int(logo.height * 760 / logo.width)), Image.LANCZOS)
c.paste(l, ((W - l.width) // 2, 100), l)
y0 = 100 + l.height + 60
d.rounded_rectangle([70, y0, W - 70, 1700], radius=48, fill=CARBON)
d.rounded_rectangle([W // 2 - 300, y0 + 60, W // 2 + 300, y0 + 140], radius=40, fill=AMAR)
d.text((W // 2, y0 + 100), 'CLIENTES HABITUALES', font=f(FB, 44), fill=CARBON, anchor='mm')
y = y0 + 230
for t, s, col in [('Tenemos un', 72, BLANCO), ('descuento especial', 80, AMAR), ('para ti', 72, BLANCO)]:
    d.text((W // 2, y), t, font=f(FB, s), fill=col, anchor='mm'); y += s + 30
y += 30
d.line([(200, y), (W - 200, y)], fill=(60, 66, 74), width=3); y += 80
for t in ['Si nos compras seguido,', 'tu precio es mejor.']:
    d.text((W // 2, y), t, font=f(FM, 46), fill=BLANCO, anchor='mm'); y += 66
y += 50
# globo de chat simple
bw, bh = 820, 200; bx = (W - bw) // 2
d.rounded_rectangle([bx, y, bx + bw, y + bh], radius=40, fill=TURQ)
d.polygon([(bx + 120, y + bh - 2), (bx + 200, y + bh - 2), (bx + 110, y + bh + 60)], fill=TURQ)
d.text((W // 2, y + 70), 'Escríbenos por interno', font=f(FB, 56), fill=CARBON, anchor='mm')
d.text((W // 2, y + 140), 'y te contamos tu descuento', font=f(FM, 42), fill=CARBON, anchor='mm')
d.rectangle([0, 1760, W, H], fill=CARBON)
d.text((W // 2, 1815), 'WhatsApp +56 9 4969 1686', font=f(FB, 50), fill=AMAR, anchor='mm')
d.text((W // 2, 1875), 'elsenordelostarros.cl', font=f(FR, 32), fill=TURQ, anchor='mm')
out = R + 'trabajo/whatsapp/estados-imagenes/estado-clientes-habituales.jpg'
c.save(out, quality=92); print(out)
