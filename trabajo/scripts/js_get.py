import os, json, base64, urllib.request
A='Basic '+base64.b64encode(f"{os.environ['JS_LOGIN']}:{os.environ['JS_TOKEN']}".encode()).decode()
for pid in open('jumpseller/get.txt').read().split():
    r=urllib.request.Request(f'https://api.jumpseller.com/v1/products/{pid}.json',headers={'Authorization':A,'User-Agent':'sdt-bot'})
    d=json.loads(urllib.request.urlopen(r,timeout=60).read()); p=d.get('product',d)
    for k in ('description','images'): p.pop(k,None)
    open(f'jumpseller/get-{pid}.json','w').write(json.dumps(p,indent=1,ensure_ascii=False))
