# Crea productos en Jumpseller desde jumpseller/crear.json (lista). Cada uno: name, sku, barcode, brand, price, stock, description, categoria, imagen (URL), permalink opcional.
# Si ya existe un producto con ese SKU, NO lo duplica. Resultado en jumpseller/estado.txt
import os, json, base64, urllib.request, urllib.error
L, T = os.environ['JS_LOGIN'], os.environ['JS_TOKEN']
AUTH = 'Basic ' + base64.b64encode(f'{L}:{T}'.encode()).decode()
def api(p, data=None, m='GET'):
    r = urllib.request.Request('https://api.jumpseller.com/v1/' + p, method=m, headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'sdt-bot'}, data=json.dumps(data).encode() if data else None)
    try: return json.loads(urllib.request.urlopen(r, timeout=90).read())
    except urllib.error.HTTPError as e: raise Exception(f'{e.code} {e.read()[:300]}')
log = []
items = json.load(open('jumpseller/crear.json', encoding='utf-8'))
cats = {}
pg = 1
while True:
    cs = api(f'categories.json?limit=100&page={pg}')
    if not cs: break
    for c in cs: c = c.get('category', c); cats[c['name'].strip().lower()] = c['id']
    pg += 1
for it in items:
    try:
        ex = api('products/search.json?query=' + urllib.request.quote(it['sku']))
        ex = [e.get('product', e) for e in ex if (e.get('product', e).get('sku') or '') == it['sku']]
        if ex: log.append(f"YA EXISTE {it['sku']}: {ex[0]['name']} (id {ex[0]['id']}) — no se crea"); continue
        prod = {'name': it['name'], 'sku': it['sku'], 'barcode': it.get('barcode', ''), 'brand': it.get('brand', ''), 'price': it['price'],
                'stock': it.get('stock', 5), 'description': it.get('description', ''), 'status': 'available'}
        if it.get('permalink'): prod['permalink'] = it['permalink']
        cid = cats.get(it.get('categoria', '').strip().lower())
        if cid: prod['categories'] = [{'id': cid}]
        p = api('products.json', {'product': prod}, 'POST'); p = p.get('product', p)
        log.append(f"CREADO {it['sku']}: {p['name']} id {p['id']} precio {p.get('price')} permalink {p.get('permalink')} categoria {'OK' if cid else 'NO ENCONTRADA'}")
        if it.get('imagen'):
            api(f"products/{p['id']}/images.json", {'image': {'url': it['imagen']}}, 'POST'); log.append('   imagen OK')
    except Exception as e: log.append(f"ERROR {it.get('sku')}: {e}")
open('jumpseller/estado.txt', 'w').write('\n'.join(log) + '\n'); print('\n'.join(log))
