# Prueba de conexión a la API de Jumpseller (corre en GitHub Actions con los secretos). No imprime credenciales.
import os, json, base64, urllib.request
L, T = os.environ.get('JS_LOGIN',''), os.environ.get('JS_TOKEN','')
out=[]
if not L or not T: out.append('FALTAN SECRETOS: login=%s token=%s' % (bool(L), bool(T)))
else:
    auth='Basic '+base64.b64encode(f'{L}:{T}'.encode()).decode()
    def get(p):
        r=urllib.request.Request('https://api.jumpseller.com/v1/'+p,headers={'Authorization':auth,'User-Agent':'sdt-bot'})
        return json.loads(urllib.request.urlopen(r,timeout=60).read())
    try:
        s=get('store/info.json'); out.append('OK tienda: '+str(s.get('store',s).get('name')))
        c=get('products/count.json'); out.append('productos: '+str(c.get('count')))
    except Exception as e: out.append('ERROR '+str(e)[:200])
open('jumpseller/estado.txt','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
