# Bomba del día automática vía API de Jumpseller. Lee FECHAS de banner.html.
# Hoy: precio = normal*0.8 (y stock 5 si estaba en 0). Ayer: vuelve al precio normal.
# DRY=1 solo muestra lo que haría. Resultado en jumpseller/bomba-log.txt
import os, re, json, base64, urllib.request, datetime
L, T = os.environ['JS_LOGIN'], os.environ['JS_TOKEN']
DRY = os.environ.get('DRY') == '1'
AUTH = 'Basic ' + base64.b64encode(f'{L}:{T}'.encode()).decode()
def api(p, data=None, m='GET'):
    r = urllib.request.Request('https://api.jumpseller.com/v1/' + p, method=m, headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'sdt-bot'},
                               data=json.dumps(data).encode() if data else None)
    return json.loads(urllib.request.urlopen(r, timeout=60).read())
b = open('banner.html', encoding='utf-8').read()
F = {d: (n, pl, int(pr)) for d, n, pl, pr in re.findall(r"'(\d{4}-\d\d-\d\d)':\[\"(.*?)\",'(.*?)',(\d+),", b)}
hoy = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).date()
ayer = hoy - datetime.timedelta(days=1)
H, A = F.get(str(hoy)), F.get(str(ayer))
log = [f'{datetime.datetime.utcnow():%Y-%m-%d %H:%M} UTC · hoy {hoy} · {"PRUEBA (no cambia nada)" if DRY else "REAL"}']
want = {}
if A: want[A[1]] = ('vuelve a precio normal', A[2], False)
if H: want[H[1]] = ('BOMBA -20%', round(H[2] * 0.8), True)
if not want: log.append('sin bomba para hoy ni ayer')
found = {}
page = 1
while want and len(found) < len(want):
    ps = api(f'products.json?limit=100&page={page}')
    if not ps: break
    for x in ps:
        p = x.get('product', x)
        if p.get('permalink') in want: found[p['permalink']] = p
    page += 1
for pl, (que, precio, es_hoy) in want.items():
    p = found.get(pl)
    if not p: log.append(f'NO ENCONTRADO {pl}'); continue
    upd = {'price': precio}
    if es_hoy and not p.get('stock_unlimited') and (p.get('stock') or 0) <= 0: upd['stock'] = 5
    log.append(f'{que}: {p.get("name")} (id {p["id"]}) precio {p.get("price")} -> {precio}' + (f', stock {p.get("stock")} -> 5' if 'stock' in upd else ''))
    if not DRY:
        r = api(f'products/{p["id"]}.json', {'product': upd}, 'PUT'); r = r.get('product', r)
        log.append(f'   OK ahora precio {r.get("price")} stock {r.get("stock")}')
os.makedirs('jumpseller', exist_ok=True)
old = open('jumpseller/bomba-log.txt').read() if os.path.exists('jumpseller/bomba-log.txt') else ''
open('jumpseller/bomba-log.txt', 'w').write('\n'.join(log) + '\n\n' + old[:20000]); print('\n'.join(log))
