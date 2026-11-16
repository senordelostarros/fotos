"""Genera cotizador-datos.js (catálogo para cotizador.html) desde trabajo/datos/productos.csv
+ ajustes posteriores (CSV de precios importados). Uso: python3 cotizador_datos.py [ajuste1.csv ajuste2.csv ...]
Cada ajuste: CSV con Permalink y Price (y opcionalmente Name, SKU, Images para productos nuevos)."""
import csv, json, re, sys, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PRE = 'https://images.jumpseller.com/store/el-senor-de-los-tarros/'
rows = {r['Permalink']: r for r in csv.DictReader(open(R + '/trabajo/datos/productos.csv'))}
for a in sys.argv[1:]:
    for r in csv.DictReader(open(a)):
        p = r['Permalink']
        if p in rows:
            if r.get('Price'): rows[p]['Price'] = r['Price']
        elif r.get('Name'):
            rows[p] = {'Permalink': p, 'Name': r['Name'], 'SKU': r.get('SKU', ''), 'Price': r.get('Price', '0'),
                       'Images': r.get('Images', ''), 'Status': 'available', 'Brand': r.get('Brand', '')}
out = []
for p, r in rows.items():
    if r.get('Status') != 'available': continue
    try: pr = round(float(r['Price'] or 0))
    except ValueError: pr = 0
    img = (r.get('Images') or '').split(',')[0].strip()
    img = img[len(PRE):] if img.startswith(PRE) else img
    out.append([r['SKU'].strip(), r['Name'].strip(), pr, p, img, (r.get('Brand') or '').strip()])
js = 'var CAT=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\nvar IMGPRE=' + json.dumps(PRE) + ';\n'
open(R + '/cotizador-datos.js', 'w').write(js)
print(len(out), 'productos', len(js) // 1024, 'KB')
