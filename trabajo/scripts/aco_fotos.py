# Descarga fotos de productos desde acomayorista.cl (corre en GitHub Actions)
import csv, json, os, re, time, urllib.request, urllib.parse
UA={'User-Agent':'Mozilla/5.0'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
os.makedirs('aco/raw',exist_ok=True); log=[]
for r in csv.DictReader(open('trabajo/datos/jonnesway-40.csv')):
    m=(r.get('modelo_web') or r['modelo']).strip()
    q='https://acomayorista.cl/search/suggest.json?'+urllib.parse.urlencode({'q':m,'resources[type]':'product','resources[limit]':'5'})
    try:
        ps=json.loads(get(q))['resources']['results']['products']
        key=re.sub(r'[^a-z0-9]','',m.lower())
        p=next((p for p in ps if re.sub(r'[^a-z0-9]','',p['title'].lower()).endswith(key)),None) or next((p for p in ps if key in re.sub(r'[^a-z0-9]','',p['title'].lower())),None)
        if not p: log.append(f'{m}\tSIN RESULTADO'); continue
        pj=json.loads(get('https://acomayorista.cl/products/'+p['handle']+'.json'))['product']
        for i,img in enumerate(pj['images'][:4]):
            open(f'aco/raw/{m.lower()}-{i}.jpg','wb').write(get(img['src'].split('?')[0]+'?width=1600'))
        log.append(f"{m}\t{p['handle']}\t{len(pj['images'])} fotos")
    except Exception as e:
        log.append(f'{m}\tERROR {e}')
    time.sleep(1.5)
open('aco/log.txt','w').write('\n'.join(log)+'\n')
