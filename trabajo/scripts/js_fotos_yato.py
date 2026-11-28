# Reemplaza las fotos de productos YATO por las oficiales (yato/raw) vía API. LIMIT=n procesa solo n productos.
import os, re, json, time, base64, urllib.request, urllib.error
A = 'Basic ' + base64.b64encode(f"{os.environ['JS_LOGIN']}:{os.environ['JS_TOKEN']}".encode()).decode()
BASE = 'https://senordelostarros.github.io/fotos/yato/raw/'
LIMIT = int(os.environ.get('LIMIT', '0') or 0)
def api(p, data=None, m='GET', tries=5):
    for k in range(tries):
        r = urllib.request.Request('https://api.jumpseller.com/v1/' + p, method=m, headers={'Authorization': A, 'Content-Type': 'application/json', 'User-Agent': 'sdt-bot'}, data=json.dumps(data).encode() if data else None)
        try:
            b = urllib.request.urlopen(r, timeout=90).read(); time.sleep(0.25); return json.loads(b) if b.strip() else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and k < tries - 1: time.sleep(5 * (k + 1)); continue
            raise Exception(f'{e.code} {e.read()[:200]}')
norm = lambda s: re.sub(r'[^A-Z0-9]', '', (s or '').upper())
files = sorted(os.listdir('yato/raw')); ok = {}
for l in open('yato/log.txt'):
    c = l.split('\t')
    if len(c) > 2 and 'fotos' in c[2]:
        code = c[0].strip().upper().replace('YT', 'YT-').replace('YT--', 'YT-')
        imgs = [f for f in files if re.match(re.escape(code) + r'-\d\.', f)]
        if imgs: ok[norm(code)] = imgs
hecho = set(l.split('\t')[0] for l in open('jumpseller/fotos-yato-log.txt')) if os.path.exists('jumpseller/fotos-yato-log.txt') else set()
prods = {}; pg = 1
while True:
    ps = api(f'products.json?limit=100&page={pg}')
    if not ps: break
    for x in ps:
        p = x.get('product', x); prods.setdefault(norm(p.get('sku')), []).append(p)
    pg += 1
out = open('jumpseller/fotos-yato-log.txt', 'a'); n = 0
for sku, imgs in ok.items():
    for p in prods.get(sku, []):
        if str(p['id']) in hecho: continue
        if LIMIT and n >= LIMIT: break
        try:
            full = api(f'products/{p["id"]}.json'); full = full.get('product', full)
            viejas = [i.get('image', i).get('id') for i in full.get('images', [])]
            for f in imgs[:3]: api(f'products/{p["id"]}/images.json', {'image': {'url': BASE + f}}, 'POST')
            for iid in viejas: api(f'products/{p["id"]}/images/{iid}.json', None, 'DELETE')
            out.write(f'{p["id"]}\t{sku}\tOK\t{len(imgs[:3])} nuevas, {len(viejas)} borradas\t{p.get("permalink")}\n'); out.flush(); n += 1
        except Exception as e:
            out.write(f'{p["id"]}\t{sku}\tERROR\t{str(e)[:150]}\n'); out.flush()
print('procesados', n)
