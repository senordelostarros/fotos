"""Estados de WhatsApp 1080x1920 (fondo blanco) para los más vendidos a talleres.
Uso: python3 scripts/estados_wsp.py <carpeta_salida> [set.py con lista P]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import recortar, colocar, texto_ajustado, f, FB, FM, FR, CARBON, TURQ, AMAR, BLANCO, GRIS
from PIL import Image, ImageDraw
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/'
insta.LOGO = R + 'trabajo/marca/logo-000.png'
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
# [nombre, código, detalle, precio neto, foto]
P = [
 ['Paño mecánico Tork Heavy-Duty', 'TO70036', 'Rollo de 280 paños en caja dispensadora', 33900, 'ms-pano-mecanico-tork-heavy-duty-combi-roll-in-box-280-panos.jpg'],
 ['Guante de nitrilo naranjo texturizado', 'GP-92753', 'Alto espesor · tallas S a XL', 8900, 'ms-guante-de-nitrilo-naranjo-texturizado-alto-espesor-tallas-s-a-xl.jpg'],
 ['Guante Aquiles nylon y poliuretano', 'CV003244', 'Tallas 7 a 10 · precio por par', 1450, 'ms-guante-de-nylon-con-palma-de-poliuretano-aquiles-tallas-7-a-10.jpg'],
 ['Guantes desechables de nitrilo naranjos', '69750', 'Texturizados tipo diamante', 21989, 'ms-guantes-desechables-nitrilo-naranjos-texturizados-tipo-diamantado.jpg'],
 ['Guante de nitrilo alta resistencia', 'ESDLT-0005', 'Para el trabajo pesado del taller', 8900, 'ms-guante-nitrilo-alta-resistencia.jpg'],
 ['Guante con palma reforzada', 'ESDLT-0013', 'Más agarre y más duración', 8900, 'ms-guante-con-palma-reforzada.jpg'],
 ['Jabón mecánico YATO 2 litros', 'YT01234T', 'Saca grasa y aceite de las manos', 14289, 'ms-jabon-mecanico-2-litros.jpg'],
 ['Limpia frenos y piezas Senfineco 660 ml', '11632', 'Seca rápido y no deja residuos', 5340, 'ms-limpia-frenos-660ml.jpg'],
 ['Limpia frenos Senfineco granel 60 L', '11735', 'Para talleres de alto consumo', 179900, 'ms-limpia-frenos-60l.jpg'],
 ['Limpia contactos Senfineco 450 ml', '11602', 'Para conectores y sensores', 5560, 'ms-limpia-contacto.jpg'],
 ['Silicona RTV negra Senfineco 100 g', '11639', 'Formador de juntas', 3260, 'ms-silicona-negra-rtv.jpg'],
 ['Silicona en spray Senfineco 450 ml', '11635', 'Lubrica y protege gomas y plásticos', 4720, 'ms-silicona-spray.jpg'],
 ['Ampolleta halógena H7 Hella', 'AL-018-H7', '12 V · 55 W', 2980, 'ms-ampolleta-halogena-h7-12v-55w-hella-px26d.jpg'],
 ['Ampolleta halógena H11', 'BRMH11', '12 V · 55 W', 3890, 'ms-ampolleta-halogena-h11-12v-55w-brm-pgj19-2.jpg'],
 ['Silicona Gasket sin olor Senfineco 100 g', '11738', 'Formador de juntas sin olor', 3350, 'ms-silicona-gasket-sin-olor.jpg'],
 ['Huincha aisladora negra', '382206', '19 mm x 18 m', 1639, 'ms-huincha-aisladora-19mm-x-18m-negra.jpg'],
 ['Juego de dados hexagonales 1/2" 12 piezas YATO', 'YT12621', 'Los dados que más se usan', 51689, 'ms2-juegos-de-dados-hexagonales-std-12-12-pzas.jpg'],
 ['Juego de dados hexagonales largos 1/2" YATO', 'YT5539', 'Llegan donde el dado corto no', 51689, 'ms2-juego-de-dados-hexagonales-largos-12.jpg'],
 ['Juego de dados hexagonales 3/8" 22 piezas YATO', 'YT38561', 'Con chicharra y accesorios', 52789, 'ms-juego-de-dados-hexagonales-de-38-22-piezas.jpg'],
 ['Buzo de trabajo YATO', 'YT80196', 'Tallas M a XXL', 60489, 'ms-buzo-de-trabajo-talla-l.jpg'],
]
if len(sys.argv) > 2:  # set alternativo: archivo .py con lista P
    P = eval(open(sys.argv[2], encoding='utf-8').read())
def cl(v): return '$' + f'{round(v):,}'.replace(',', '.')
logo = Image.open(insta.LOGO).convert('RGBA')
for i, (nom, cod, det, pre, foto) in enumerate(P, 1):
    c = Image.new('RGB', (W, H), BLANCO); d = ImageDraw.Draw(c)
    # cabecera carbón con logo y franja
    d.rectangle([0, 0, W, 300], fill=CARBON)
    lw = 560; l = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    if l.height > 230: l = logo.resize((int(logo.width * 230 / logo.height), 230), Image.LANCZOS)
    c.paste(l, ((W - l.width) // 2, 35), l)
    d.rectangle([0, 300, W, 312], fill=TURQ); d.rectangle([0, 312, W, 320], fill=AMAR)
    d.text((W // 2, 385), 'LO QUE MÁS SE LLEVAN LOS TALLERES', font=f(FB, 40), fill=CARBON, anchor='mm')
    # producto
    colocar(c, recortar(R + foto), (110, 450, W - 110, 1150))
    # textos
    ft, ls = texto_ajustado(d, nom, FB, W - 140, 60, 40)
    y = 1215
    for ln in ls: d.text((W // 2, y), ln, font=ft, fill=CARBON, anchor='mm'); y += ft.size + 12
    d.text((W // 2, y + 8), det, font=f(FM, 36), fill=(90, 98, 108), anchor='mm')
    d.text((W // 2, y + 60), 'Código ' + cod, font=f(FR, 30), fill=GRIS, anchor='mm')
    # precio
    t = cl(pre) + ' + IVA'; fp = f(FB, 74); tw = d.textlength(t, font=fp)
    py = y + 115; d.rounded_rectangle([W // 2 - tw / 2 - 40, py, W // 2 + tw / 2 + 40, py + 120], radius=60, fill=AMAR)
    d.text((W // 2, py + 60), t, font=fp, fill=CARBON, anchor='mm')
    # pie
    d.rectangle([0, H - 240, W, H], fill=CARBON)
    d.text((W // 2, H - 170), 'Pídelo por WhatsApp +56 9 4969 1686', font=f(FB, 46), fill=AMAR, anchor='mm')
    d.text((W // 2, H - 105), 'Despacho gratis dentro de Vespucio sobre $50.000 + IVA', font=f(FM, 32), fill=BLANCO, anchor='mm')
    d.text((W // 2, H - 55), 'elsenordelostarros.cl', font=f(FR, 30), fill=TURQ, anchor='mm')
    c.save(os.path.join(OUT, f'estado-{i:02d}-{cod.lower()}.jpg'), quality=90)
print('ok', len(P))
