# Oferta flash: espera hasta INICIO, pone precio flash y stock limitado; en FIN restaura precio y stock originales.
# Config en jumpseller/flash.json: {"permalink","precio_flash","stock_flash","inicio":"YYYY-MM-DDTHH:MM","fin":"..."} (hora Chile, UTC-3)
import os, json, time, base64, datetime, urllib.request
L, T = os.environ['JS_LOGIN'], os.environ['JS_TOKEN']
AUTH = 'Basic ' + base64.b64encode(f'{L}:{T}'.encode()).decode()
def api(p, data=None, m='GET'):
    r = urllib.request.Request('https://api.jumpseller.com/v1/' + p, method=m, headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'sdt-bot'}, data=json.dumps(data).encode() if data else None)
    return json.loads(urllib.request.urlopen(r, timeout=60).read())
CL = datetime.timezone(datetime.timedelta(hours=-3))
cfg = json.load(open('jumpseller/flash.json'))
ini = datetime.datetime.fromisoformat(cfg['inicio']).replace(tzinfo=CL); fin = datetime.datetime.fromisoformat(cfg['fin']).replace(tzinfo=CL)
def log(s):
    print(datetime.datetime.now(CL).strftime('%H:%M:%S'), s, flush=True)
p = None; pg = 1
while not p:
    ps = api(f'products.json?limit=100&page={pg}')
    if not ps: break
    p = next((x.get('product', x) for x in ps if x.get('product', x).get('permalink') == cfg['permalink']), None); pg += 1
if not p: log('NO ENCONTRADO'); raise SystemExit(1)
orig = {'price': p['price'], 'stock': p.get('stock')}
log(f'{p["name"]} id {p["id"]} original {orig}')
while datetime.datetime.now(CL) < ini: time.sleep(20)
r = api(f'products/{p["id"]}.json', {'product': {'price': cfg['precio_flash'], 'stock': cfg['stock_flash']}}, 'PUT'); r = r.get('product', r)
log(f'FLASH ON precio {r.get("price")} stock {r.get("stock")}')
while datetime.datetime.now(CL) < fin: time.sleep(20)
cur = api(f'products/{p["id"]}.json'); cur = cur.get('product', cur)
vendidos = cfg['stock_flash'] - (cur.get('stock') or 0)
nuevo_stock = max((orig['stock'] or 0) - max(vendidos, 0), 0)
r = api(f'products/{p["id"]}.json', {'product': {'price': orig['price'], 'stock': nuevo_stock}}, 'PUT'); r = r.get('product', r)
log(f'FLASH OFF vendidos {vendidos} · precio {r.get("price")} stock {r.get("stock")}')
