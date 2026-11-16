"""Genera cotizador-datos.js (catálogo para cotizador.html).
Uso: python3 cotizador_datos.py <exportacion_jumpseller.csv> [ajuste1.csv ...]
- La exportación (Productos → Exportar) manda: nombre, precio, foto, categoría, estado.
- Ajustes: CSV con Permalink y Price (y Name, SKU, Images para productos nuevos aún no exportados).
- Si un producto no tiene foto en Jumpseller, usa la foto propia ms-*.jpg del repositorio si existe."""
import csv, json, re, sys, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PRE = 'https://images.jumpseller.com/store/el-senor-de-los-tarros/'
BASE = sys.argv[1] if len(sys.argv) > 1 else R + '/trabajo/datos/productos-2026-11-16.csv'
rows = {}
for r in csv.DictReader(open(BASE)):
    if r['Permalink'] not in rows: rows[r['Permalink']] = r
for a in sys.argv[2:]:
    for r in csv.DictReader(open(a)):
        p = r['Permalink']
        if p in rows:
            if r.get('Price'): rows[p]['Price'] = r['Price']
        elif r.get('Name'):
            rows[p] = {'Permalink': p, 'Name': r['Name'], 'SKU': r.get('SKU', ''), 'Price': r.get('Price', '0'),
                       'Images': r.get('Images', ''), 'Status': 'available', 'Brand': r.get('Brand', ''),
                       'Categories': r.get('Categories', '')}

def cat(s):
    cs = [c.strip() for c in re.split(r',(?=[A-ZÁÉÍÓÚ])', s or '') if c.strip()]
    sub = [c for c in cs if ' / ' in c]
    return sub[0] if sub else (cs[0] + ' / Otros' if cs else '')

FAMILIAS = {'Herramientas manuales', 'Herramientas eléctricas y neumáticas', 'Insumos de taller', 'Desabolladura y Pintura',
            'Diagnóstico y herramienta especial', 'Equipamiento de taller', 'Seguridad e higiene'}
cats = {p: cat(r.get('Categories')) for p, r in rows.items()}
cats = {p: c if c.split(' / ')[0] in FAMILIAS else '' for p, c in cats.items()}
CATS = sorted(set(c for c in cats.values() if c))
CI = {c: i for i, c in enumerate(CATS)}
out = []
for p, r in rows.items():
    if r.get('Status') != 'available': continue
    try: pr = round(float(r['Price'] or 0))
    except ValueError: pr = 0
    img = (r.get('Images') or '').split(',')[0].strip()
    img = img[len(PRE):] if img.startswith(PRE) else img
    if not img:
        for pre in ('ms2-', 'ms-', 'ms5-', 'ms6-'):
            if os.path.exists(f'{R}/{pre}{p}.jpg'):
                img = f'{pre}{p}.jpg'; break
    sku = (r.get('SKU') or '').strip()
    if sku.endswith('.0') and sku[:-2].isdigit(): sku = sku[:-2]
    out.append([sku, r['Name'].strip(), pr, p, img, (r.get('Brand') or '').strip(), CI.get(cats.get(p, ''), -1)])
js = 'var CAT=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\nvar CATS=' + json.dumps(CATS, ensure_ascii=False) + ';\nvar IMGPRE=' + json.dumps(PRE) + ';\n'
open(R + '/cotizador-datos.js', 'w').write(js)
print(len(out), 'productos', len(js) // 1024, 'KB', sum(1 for x in out if not x[4]), 'sin foto', sum(1 for x in out if x[6] < 0), 'sin categoría')
