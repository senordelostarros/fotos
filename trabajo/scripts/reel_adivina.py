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
    'cable': ['ms-cable-usb-c-a-usb-b-impresora-escaner.jpg', (0.72, 0.80), 'Es un cable USB-C a USB-B',
              'Cable USB-C a USB-B', 'USBC-USBB',
              ['Impresoras y escáneres', 'A notebook o celular USB-C', 'Malla trenzada resistente'], 15900, False],
    'impacto': ['ms2-llave-de-impacto-inalambrica-18-v-350nm-cuadrante-de-12.jpg', (0.72, 0.20), 'Es una llave de impacto inalámbrica',
                'Llave de impacto inalámbrica 18 V YATO', 'YT8277925',
                ['350 Nm de apriete, 500 Nm para soltar', 'Sin carbones, cuadrante de 1/2"', '2 baterías 2 Ah, cargador y bolso'], 164989, True],
    'dados-largos': ['ms2-juego-de-dados-de-impacto-largos-de-12-1.jpg', (0.30, 0.58), 'Son dados de impacto largos',
                     'Dados de impacto largos 1/2" YATO', 'YT1055',
                     ['15 dados de 10 a 32 mm', 'Largo 78 mm: llegan más hondo', 'En caja metálica'], 76989, False],
    'dados-allen': ['ms2-juego-de-dados-allen-de-impacto-12.jpg', (0.40, 0.25), 'Son dados Allen de impacto',
                    'Dados Allen de impacto 1/2" YATO', 'YT1066',
                    ['8 piezas de 6 a 19 mm', 'Acero CrMo, dureza HRC 54', 'Para llave de impacto'], 60489, False],
    'partidor': ['ms-dispositivo-de-arranque-banco-de-energia-12000mah-con-pantalla-lcd.jpg', (0.50, 0.40), 'Es un partidor de baterías',
                 'Partidor y banco de energía YATO', 'YT83082',
                 ['300 A, peak de 500 A', 'Bencina y diésel, 12 V', 'Carga el celular por USB'], 142989, True],
    'densimetro': ['ms-densimetro-para-baterias.jpg', (0.50, 0.50), 'Es un densímetro de baterías',
                   'Densímetro para baterías', 'VI2504',
                   ['Revisa el electrolito', 'Te dice si la batería está cargada', 'Para baterías de plomo-ácido'], 8250, False],
    'cargador4': ['ms3-cargador-de-baterias-4-en-1.jpg', (0.50, 0.50), 'Es un cargador de baterías 4 en 1',
                  'Cargador de baterías 4 en 1 YATO', 'YT83033',
                  ['Carga baterías de 6 y 12 V', 'Prueba alternador y arranque', 'Protección contra sobrecarga'], 82489, False],
    'ext2': ['ms2-extractor-de-rodamientos-de-2-brazos-de-8-180-mm.jpg', (0.50, 0.30), 'Es un extractor de rodamientos',
             'Extractor de rodamientos 2 brazos 8" YATO', 'YT2518',
             ['Fuerza máxima 5 toneladas', 'Brazos de 8" (180 mm)', 'Saca rodamientos y engranajes'], 52789, True],
    'ext3': ['ms3-extractor-de-rodamientos-de-3-brazos-de-6-150-mm.jpg', (0.50, 0.30), 'Es un extractor de 3 brazos',
             'Extractor de rodamientos 3 brazos 6" YATO', 'YT2513',
             ['Para diámetros de 80 a 300 mm', '3 brazos: agarre parejo', 'Eje central de 19 mm'], 52789, False],
    'polea': ['ms3-extractor-de-polea-40-165-mm.jpg', (0.50, 0.35), 'Es un extractor de poleas',
              'Extractor de polea 40-165 mm YATO', 'YT25480',
              ['Rango de 40 a 165 mm', 'Para poleas y engranajes', 'Saca poleas pegadas'], 34639, False],
    'sm-gata': ['smart-gata-botella-3-ton.jpg', (0.45, 0.30), 'Es una gata de botella',
                'Gata hidráulica de botella 3 ton Smart', '6107803',
                ['Levanta hasta 3 toneladas', 'Hidráulica tipo botella', 'Compacta para el taller'], 28915, False],
    'sm-dados': ['smart-juego-dados-1-2-17-piezas.jpg', (0.42, 0.62), 'Es un juego de dados 1/2"',
                 'Juego de dados 1/2" 17 piezas Smart', '6104510',
                 ['13 dados de 8 a 27 mm', 'Chicharra y dado de bujías 21 mm', 'Barrote corredizo y extensiones'], 56947, False],
    'sm-llaves': ['smart-juego-llaves-punta-corona-8-piezas.jpg', (0.30, 0.25), 'Es un juego de llaves punta corona',
                  'Juego llaves punta corona 8 pzas Smart', '6106655',
                  ['8 llaves de 8 a 19 mm', 'Punta y corona', 'Con soporte para colgar'], 15440, False],
    'fo-bujias': ['ms-comprobador-de-bujias-en-linea.jpg', (0.50, 0.50), 'Es un comprobador de bujías',
                  'Comprobador de bujías en línea Force', '88409',
                  ['Ve si la bujía da chispa', 'Va entre la bujía y el cable', 'Con el motor funcionando'], 18150, False],
    'fo-patin': ['ms-medidor-de-espesor-de-patin-de-freno.jpg', (0.50, 0.50), 'Es un medidor de pastillas de freno',
                 'Medidor de espesor de patín de freno Force', '6399485',
                 ['Mide el desgaste de las pastillas', 'Sin desmontar la rueda', 'Revisión en segundos'], 15138, False],
    'fo-seguros': ['ms-alicate-para-seguros-plano-9.jpg', (0.50, 0.30), 'Es un alicate para seguros',
                   'Alicate para seguros plano 9" Force', '6399555',
                   ['Para anillos seeger', 'Monta y desmonta seguros', 'Largo de 9 pulgadas'], 54937, False],
    'pinza': ['ms2-pinza-amperimetrica-digital.jpg', (0.50, 0.22), 'Es una pinza amperimétrica',
              'Pinza amperimétrica digital YATO', 'YT73093',
              ['Mide corriente sin cortar cables', 'Detecta voltaje sin contacto', 'Mide temperatura y capacitancia'], 98989, True],
    'fo-copas': ['force/force-3178.jpg', (0.50, 0.40), 'Es un juego de copas para filtros',
                 'Juego de copas para filtros 31 piezas Force', '6399615',
                 ['Saca filtros de aceite apretados', '31 copas para distintas marcas', 'Se usa con chicharra o barrote'], 195187, False],
    'fo-fuga': ['force/force-2870.jpg', (0.40, 0.62), 'Es un tester de fuga de cilindros',
                'Tester de fuga de cilindros Force', '6399120',
                ['Mide la fuga de cada cilindro', 'Ubica fallas en válvulas o anillos', 'Escala en PSI, BAR y %'], 195782, False],
    'caliper': ['ms-juego-universal-prensa-para-caliper-manual-12pzas.jpg', (0.47, 0.64), 'Es una prensa para caliper',
                'Prensa para caliper 12 piezas YATO', 'YT0611',
                ['Retrae el pistón del caliper', 'Para el cambio de pastillas', 'Adaptadores para varias marcas'], 47289, True],
    'jw-impacto': ['jonnesway/aco-jai-1114k.jpg', (0.52, 0.62), 'Es una llave de impacto neumática',
                   'Kit llave de impacto 1/2" Jonnesway', 'JAI-1114K',
                   ['880 Nm de trabajo, 1350 Nm máximo', '9.500 rpm, cuadrante de 1/2"', 'Incluye dados en maleta'], 292320, False],
    'jw-dados94': ['jonnesway/aco-s04h52494s.jpg', (0.36, 0.66), 'Es un juego de dados de 94 piezas',
                   'Juego de dados 1/4" y 1/2" 94 piezas Jonnesway', 'S04H52494S',
                   ['Dados de 1/4" y de 1/2"', 'Chicharras, extensiones y puntas', 'Todo en una maleta'], 210000, False],
    'jw-pernos': ['jonnesway/aco-ag010104.jpg', (0.50, 0.62), 'Es un extractor de pernos',
                  'Extractor de pernos 8 piezas Jonnesway', 'AG010104',
                  ['Saca pernos cortados o rodados', 'Rosca inversa: entra y afloja', '8 medidas en caja plástica'], 51700, True],
    'jw-filtros': ['jonnesway/aco-ai050049.jpg', (0.72, 0.42), 'Es una llave saca filtros de cadena',
                   'Llave saca filtros de cadena Jonnesway', 'AI050049',
                   ['Para filtros de 30 a 160 mm', 'La cadena agarra y no resbala', 'Mango de 220 mm'], 21740, False],
    'jw-seguros': ['jonnesway/aco-ag010002sp.jpg', (0.50, 0.40), 'Es un juego de alicates para seguros',
                   'Alicates para seguros 4 piezas Jonnesway', 'AG010002SP',
                   ['Para seguros seeger', 'Interior y exterior', 'Puntas rectas y curvas'], 70800, False],
    'fundas280': ['ms-cubre-asientos-desechables-rollo-250.jpg', (0.40, 0.50), 'Es un rollo de fundas cubre asiento',
                  'Rollo de 250 fundas cubre asiento', '0920207',
                  ['250 fundas plásticas por rollo', 'Plástico de 18 micras', 'Cuida el tapiz del cliente'], 49900, False],
    'williams': ['ms-refrigerante-williams-rojo-50-50-galon.jpg', (0.40, 0.70), 'Es refrigerante rojo 50/50',
                 'Refrigerante rojo Williams 50/50, 1 galón', '>Precio por galón llevando 6',
                 ['Premezclado 50/50: no lleva agua', 'Listo para usar', 'Galón de 3,785 litros'], 4900, False],
    'torque210': ['ms-llave-de-torque-cuadrante-12-dual-nm-y-ftlb-20-100-nm-y-15-75-lbpie.jpg', (0.10, 0.50), 'Es una llave de torque',
                  'Llave de torque 1/2" dual 20-100 Nm YATO', 'YT07413',
                  ['Aprieta al torque exacto', 'Escala en Nm y en lb·pie', 'Cuadrante de 1/2"'], 131989, True],
    'jw-maleta78': ['jonnesway/aco-c-ha78s.jpg', (0.45, 0.45), 'Es una maleta de 78 herramientas',
                    'Maleta de herramientas 78 piezas Jonnesway', 'C-HA78S',
                    ['Llaves, dados y chicharra', 'Alicates y destornilladores', 'Todo en un bolso de lona'], 789000, False],
    'jw-compresimetro': ['jonnesway/aco-ai020052.jpg', (0.45, 0.40), 'Es un compresímetro',
                         'Compresímetro bencinero Jonnesway', 'AI020052',
                         ['Mide la compresión del motor', 'Manómetro de 80 mm', 'Adaptadores M14 y M18'], 198450, False],
    'linterna': ['ms-linterna-de-taller-tipo-lapiz-recargable-y-magnetica.jpg', (0.40, 0.50), 'Es una linterna lápiz',
                 'Linterna lápiz recargable y magnética IRIMO', 'L-PEN-1',
                 ['Luz LED de 150 lm', 'Imán para dejarla pegada', 'Recargable con cable'], 9490, True],
    'medidor-frenos': ['ms2-medidor-de-desgaste-de-frenos.jpg', (0.80, 0.50), 'Es un medidor de pastillas',
                       'Medidor de desgaste de pastillas de freno', 'MDF8H',
                       ['Mide pastillas sin desarmar', '8 láminas de 2 a 12 mm', 'Rojo cambiar, verde OK'], 10890, False],
    'probador': ['ms-probador-de-corriente-6-24v.jpg', (0.72, 0.78), 'Es un probador de corriente',
                 'Probador de corriente 6-24 V Hella', 'AL018003798001',
                 ['Detecta si llega corriente', 'Encuentra cortocircuitos', 'Sirve de 6 a 24 V'], 9889, False],
    'jabon': ['ms-jabon-mecanico-2-litros.jpg', (0.50, 0.12), 'Es jabón mecánico',
              'Jabón mecánico 2 litros YATO', 'YT01234T',
              ['Saca grasa y aceite de las manos', 'Con partículas que friccionan', 'Bidón de 2 litros'], 14289, True],
    'aceitera': ['ms-aceitera-manual-con-aplicador-flexible-500cc.jpg', (0.42, 0.22), 'Es una aceitera',
                 'Aceitera con aplicador flexible YATO 500 cc', 'YT06914',
                 ['Lubrica donde no llegas', 'Pitón flexible', 'Capacidad 500 cc'], 10659, False],
    'orings': ['ms-display-surtido-de-o-ring-en-mm.jpg', (0.45, 0.45), 'Es un surtido de O-rings',
               'Surtido de O-rings en mm YATO', 'YT06877',
               ['Todas las medidas en una caja', 'Para sellos de aceite y agua', 'Ordenados por compartimiento'], 9339, False],
    'estetoscopio': ['ms-estetoscopio-para-detectar-ruido-de-motores.jpg', (0.50, 0.50), 'Es un estetoscopio mecánico',
                     'Estetoscopio para ruidos de motor', '6104580',
                     ['Escucha ruidos internos del motor', 'Ubica rodamientos y válvulas', 'Diagnóstico sin desarmar'], 10890, True],
    'llave-rueda': ['ms-llave-de-rueda-tipo-cruz-17-19-21-mm-y-cuadrante-de-12-para-automovil.jpg', (0.20, 0.22), 'Es una llave de rueda cruz',
                    'Llave de rueda cruz 17-19-21 mm', 'ASRZ149171921',
                    ['Tres medidas: 17, 19 y 21 mm', 'Cuadrante de 1/2"', 'Más fuerza para soltar tuercas'], 14289, False],
    'sopletear': ['ms-pistola-de-sopletear-corta.jpg', (0.18, 0.22), 'Es una pistola de sopletear',
                  'Pistola de sopletear corta', 'DG10B1',
                  ['Limpia piezas con aire', 'Gatillo de control', 'Para compresor'], 10450, False],
}
CARD = {'fundas280': 'card-fundas-250.png'}
PREG = {'jabon': ('¿Adivinas qué', 'producto es?'), 'orings': ('¿Adivinas qué', 'producto es?'), 'cable': ('¿Sabes qué', 'cable es este?'), 'williams': ('¿Adivinas qué', 'producto es?'), 'fundas280': ('¿Adivinas qué', 'producto es?')}
CLAVE, OUT, TMP = sys.argv[1], sys.argv[2], sys.argv[3]
FOTO, ZP, ES, NOM, COD, USOS, PRECIO, BOMBA = DATOS[CLAVE]
W, H, FPS = 1080, 1920, 30
os.makedirs(TMP, exist_ok=True)

logo = Image.open(insta.LOGO).convert('RGBA')
orig = Image.open(R + '/' + FOTO).convert('RGB')
prod = Image.open(R + '/trabajo/marca/' + CARD[CLAVE]).convert('RGBA') if CLAVE in CARD else recortar(R + '/' + FOTO)
fondo_t = patron((W, H)).convert('RGBA')
fondo_c = Image.new('RGBA', (W, H), CARBON + (255,))
# Temas de fondo (variable de entorno TEMA): clasico | panel | plano | peligro
TEMA = os.environ.get('TEMA', 'clasico')
def _panel(base, hoyo, borde):
    im = Image.new('RGB', (W, H), base); d = ImageDraw.Draw(im)
    for y in range(30, H, 64):
        for x in range(30 + (32 if (y // 64) % 2 else 0), W, 64):
            d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=hoyo); d.arc((x - 10, y - 10, x + 10, y + 10), 200, 360, fill=borde, width=2)
    return im.convert('RGBA')
def _plano(base, fina, gruesa):
    im = Image.new('RGB', (W, H), base); d = ImageDraw.Draw(im)
    for k in range(0, max(W, H), 30):
        col = gruesa if k % 150 == 0 else fina; w_ = 2 if k % 150 == 0 else 1
        d.line((k, 0, k, H), fill=col, width=w_); d.line((0, k, W, k), fill=col, width=w_)
    return im.convert('RGBA')
def _peligro(base):
    im = Image.new('RGB', (W, H), base); d = ImageDraw.Draw(im)
    for y0, y1 in ((0, 46), (H - 196, H - 150)):
        d.rectangle((0, y0, W, y1), fill=AMAR)
        for x in range(-100, W + 100, 80): d.polygon([(x, y1), (x + 40, y1), (x + 86, y0), (x + 46, y0)], fill=CARBON)
    return im.convert('RGBA')
if TEMA == 'panel':
    fondo_t = _panel((214, 196, 164), (96, 80, 60), (238, 226, 204)); fondo_c = _panel((34, 38, 44), (14, 16, 19), (58, 64, 72))
elif TEMA == 'plano':
    fondo_t = _plano((30, 86, 140), (52, 110, 166), (96, 150, 200)); fondo_c = _plano((16, 46, 78), (28, 64, 100), (52, 96, 140))
elif TEMA == 'peligro':
    fondo_t = _peligro((236, 238, 240)); fondo_c = _peligro(CARBON)
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
        P1, P2 = PREG.get(CLAVE, ('¿Adivinas qué', 'herramienta es?'))
        texto(c, P1, f(FB, 92), 170, BLANCO, ease(u / .4), dy=30 * (1 - ease(u / .4)))
        texto(c, P2, f(FB, 92), 280, AMAR, ease((u - .25) / .4), dy=30 * (1 - ease((u - .25) / .4)))
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
        texto(c, COD[1:] if COD.startswith('>') else 'Código ' + COD, f(FM, 40), 1300, GRIS, ease((u - .2) / .4))
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
        texto(c, 'Despacho gratis en Santiago', f(FR, 40), 1360, GRIS, ease((u - 1.7) / .4))
        texto(c, 'sobre $30.000 + IVA · Regiones por Blue Express', f(FR, 36), 1412, GRIS, ease((u - 1.7) / .4))
    return c

n = int(TOTAL * FPS)
if os.environ.get('PREVIEW'):
    for i in (75, 160, 260, 360, 460): frame(i / FPS).convert('RGB').resize((360, 640)).save(f'{TMP}/prev{i}.jpg')
    sys.exit(0)
for i in range(n):
    frame(i / FPS).convert('RGB').save(f'{TMP}/f{i:04d}.jpg', quality=90)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{TMP}/f%04d.jpg',
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '21', '-movflags', '+faststart',
                '-c:a', 'aac', '-b:a', '128k', OUT], check=True)
for i in (75, 160, 260, 360, 460): frame(i / FPS).convert('RGB').resize((360, 640)).save(f'{TMP}/prev{i}.jpg')
print('ok', OUT)
