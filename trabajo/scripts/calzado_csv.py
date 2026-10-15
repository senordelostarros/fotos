"""CSV Jumpseller del calzado Climber / Proflex / Tempest desde la lista de precios del proveedor.
Precio tienda = lista proveedor +10% (neto). Con foto -> visible; sin foto -> deshabilitado."""
import sys, re, csv, os, openpyxl, unicodedata
XLSX = sys.argv[1]; OUT = sys.argv[2]
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
URL = 'https://senordelostarros.github.io/fotos/'
CAT = 'Seguridad e higiene,Seguridad e higiene / Ropa y Calzado de Trabajo'

ZAPATILLA = {'climber-bachelor','proflex-112-n','proflex-151-g','tempest-4031-g','tempest-4031-n','tempest-4032-g','tempest-4032-m','tempest-4033-b'}
ZAPATO = {'climber-banff','climber-thorens-3','climber-valdisere-c','climber-valdisere-v','proflex-103-c','proflex-104-c',
          'tempest-3010-nd','tempest-3020-nda','tempest-3041-bd','tempest-3041-nd','tempest-3082-cda'}
BOTA = {'climber-anton','climber-tignes-high','proflex-110-c','proflex-111-c','proflex-111-n','proflex-120-c'}

def foto(marca, nombre):
    n = nombre.strip().upper()
    if marca == 'Climber':
        k = n.lower().replace(' ', '-')
        cand = {'meribel-c': 'climber-meribel', 'haines': 'climber-haines'}.get(k, 'climber-' + k)
    elif marca == 'Proflex':
        m = re.fullmatch(r'PF(\d{3})([A-Z]+)', n.split()[0])
        cand = f'proflex-{m.group(1)}-{m.group(2).lower()}' if m else None
    else:
        m = re.fullmatch(r'TP(\d{4})([A-Z]*)', n)
        cand = None
        if m:
            base = f'tempest-{m.group(1)}'
            for f in sorted(os.listdir(REPO)):
                if f.startswith(base + '-') and f.endswith('.jpg') and f[len(base)+1:-4].startswith(m.group(2).lower() or '#'):
                    cand = f[:-4]; break
    return cand if cand and os.path.exists(os.path.join(REPO, cand + '.jpg')) else None

def tipo(key, nombre):
    if 'PFAQ' in nombre: return 'Bota de agua'
    if key in ZAPATILLA: return 'Zapatilla de seguridad'
    if key in ZAPATO: return 'Zapato de seguridad'
    if key in BOTA: return 'Bota de seguridad'
    return 'Bototo de seguridad'

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

H = ['Permalink','Name','Description','Meta Title','Meta Description','Brand','Categories','Images','Digital','Featured',
     'Status','SKU','Stock','Stock Unlimited','Stock Notification','Price']
ws = openpyxl.load_workbook(XLSX, data_only=True).active
rows = []; vistos = set()
for r in list(ws.iter_rows(values_only=True))[1:]:
    if not r or not r[1]: continue
    marca, nombre, tallas, norma, precio = r[1].strip(), str(r[2]).strip(), str(r[3]).strip(), str(r[4]).strip(), r[5]
    key = foto(marca, nombre)
    if key in vistos: key = None
    if key: vistos.add(key)
    t = tipo(key, nombre)
    modelo = nombre.title() if marca == 'Climber' else nombre
    name = f'{t} {marca} {modelo}'
    sku = slug(f'{marca}-{nombre}').upper()
    norma_t = 'norma chilena' if 'CHILENA' in norma.upper() else 'norma europea'
    desc = (f'{t} {marca} modelo {modelo}. Tallas {tallas}. Certificado bajo {norma_t}. '
            f'Indica tu talla al comprar o consúltanos por WhatsApp +56 9 4969 1686. Precio neto + IVA, emitimos factura.')
    rows.append({'Permalink': slug(name), 'Name': name, 'Description': desc, 'Meta Title': name, 'Meta Description': desc[:155],
                 'Brand': marca, 'Categories': CAT, 'Images': URL + key + '.jpg' if key else '', 'Digital': 'NO', 'Featured': 'NO',
                 'Status': 'available' if key else 'disabled', 'SKU': sku, 'Stock': '5', 'Stock Unlimited': 'NO',
                 'Stock Notification': 'YES', 'Price': str(round(precio * 1.10))})
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, H); w.writeheader(); w.writerows(rows)
print(len(rows), 'productos;', sum(1 for x in rows if x['Images']), 'con foto')
for x in rows:
    if not x['Images']: print('  sin foto:', x['Name'], x['Price'])
print('fotos sin usar:', sorted(f[:-4] for f in os.listdir(REPO) if re.match(r'(climber|proflex|tempest)-', f) and f[:-4] not in vistos))
