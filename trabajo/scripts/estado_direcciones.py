"""Estado de WhatsApp 1080x1920 con la página web e Instagram del negocio."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta, qrcode
from insta import patron, f, FB, FM, FR, CARBON, TURQ, AMAR, BLANCO
from PIL import Image, ImageDraw
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'
insta.LOGO = R + 'trabajo/marca/logo-000.png'
W, H = 1080, 1920
c = patron((W, H)).convert('RGB'); d = ImageDraw.Draw(c)
logo = Image.open(insta.LOGO).convert('RGBA')
l = logo.resize((820, int(logo.height * 820 / logo.width)), Image.LANCZOS)
c.paste(l, ((W - l.width) // 2, 110), l)
# tarjeta blanca
y0 = 110 + l.height + 70
d.rounded_rectangle([70, y0, W - 70, 1760], radius=48, fill=BLANCO)
d.text((W // 2, y0 + 90), 'Visita nuestra tienda online', font=f(FB, 54), fill=CARBON, anchor='mm')
q = qrcode.QRCode(border=1, box_size=12); q.add_data('https://elsenordelostarros.cl'); q.make(fit=True)
qi = q.make_image(fill_color=(29, 33, 38), back_color='white').convert('RGB').resize((420, 420), Image.NEAREST)
c.paste(qi, ((W - 420) // 2, y0 + 160))
yy = y0 + 160 + 420 + 40
fp = f(FB, 62); t = 'elsenordelostarros.cl'; tw = d.textlength(t, font=fp)
d.rounded_rectangle([W // 2 - tw / 2 - 40, yy, W // 2 + tw / 2 + 40, yy + 110], radius=55, fill=AMAR)
d.text((W // 2, yy + 55), t, font=fp, fill=CARBON, anchor='mm')
d.text((W // 2, yy + 160), 'Escanea el código o escribe la dirección', font=f(FR, 32), fill=(90, 98, 108), anchor='mm')
yi = yy + 240
d.line([(170, yi), (W - 170, yi)], fill=(225, 229, 233), width=3)
d.text((W // 2, yi + 75), 'Síguenos en Instagram', font=f(FB, 50), fill=CARBON, anchor='mm')
fi = f(FB, 50); ti = '@el_senor_de_los_tarros_spa_'
while d.textlength(ti, font=fi) > W - 260: fi = f(FB, fi.size - 2)
d.text((W // 2, yi + 160), ti, font=fi, fill=(74, 160, 178), anchor='mm')
d.text((W // 2, yi + 235), 'Herramientas, ofertas y la bomba del día', font=f(FM, 32), fill=(90, 98, 108), anchor='mm')
d.rectangle([0, 1820, W, H], fill=CARBON)
d.text((W // 2, 1870), 'El Señor de los Tarros SPA', font=f(FB, 36), fill=AMAR, anchor='mm')
out = sys.argv[1] if len(sys.argv) > 1 else R + 'trabajo/whatsapp/estados-imagenes/estado-00-pagina-e-instagram.jpg'
c.save(out, quality=92); print(out)
