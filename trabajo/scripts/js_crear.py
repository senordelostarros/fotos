# Crea productos en Jumpseller vía API desde jumpseller/crear.json (lista). No crea si el SKU ya existe.
import os, json, base64, urllib.request, urllib.error
L, T = os.environ['JS_LOGIN'], os.environ['JS_TOKEN']
AUTH = 'Basic ' + base64.b64encode(f'{L}:{T}'.encode()).decode()
def api(p, data=None, m='GET'):
    r = urllib.request.Request('https://api.jumpseller.com/v1/' + p, method=m, headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'sdt-bot'}, data=json.dumps(data).encode() if data else None)
    try: return json.loads(urllib.request.urlopen(r, timeout=60).read())
    except urllib.error.HTTPError as e: raise Exception(f'{e.code} {e.read()[:300]}')
log = []
cats = []; pg = 1
while True:
    cs = api(f'categories.json?limit=100&page={pg}')
    if not cs: break
    cats += [c.get('category', c) for c in cs]; pg += 1
for it in json.load(open('jumpseller/crear.json')):
    try:
        ex = api('products/search.json?query=' + urllib.request.quote(it['sku']))
        if any((x.get('product', x).get('sku') or '') == it['sku'] for x in ex):
            log.append(f'YA EXISTE sku {it["sku"]}, no se crea'); continue
        cat = [c for c in cats if c.get('name', '').strip().lower() == it.get('categoria', '').lower()]
        prod = {'name': it['nombre'], 'price': it['precio'], 'sku': it['sku'], 'stock': it.get('stock', 10), 'status': 'available',
                'description': it.get('descripcion', ''), 'brand': it.get('marca', ''), 'permalink': it.get('permalink')}
        if it.get('barcode'): prod['barcode'] = it['barcode']
        if cat: prod['categories'] = [{'id': cat[0]['id']}]
        p = api('products.json', {'product': prod}, 'POST'); p = p.get('product', p)
        log.append(f'CREADO {p.get("name")} id {p["id"]} precio {p.get("price")} permalink {p.get("permalink")} categoria {cat[0]["name"] if cat else "(ninguna)"}')
        for u in it.get('imagenes', []):
            api(f'products/{p["id"]}/images.json', {'image': {'url': u}}, 'POST'); log.append('   foto OK')
    except Exception as e: log.append(f'ERROR {it.get("sku")}: {e}')
old = open('jumpseller/crear-log.txt').read() if os.path.exists('jumpseller/crear-log.txt') else ''
open('jumpseller/crear-log.txt', 'w').write('\n'.join(log) + '\n\n' + old); print('\n'.join(log))
