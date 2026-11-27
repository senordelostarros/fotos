# Descarga fotos oficiales YATO desde toya24.pl (tienda oficial de TOYA S.A.). Corre en GitHub Actions.
# Entrada: yato/pedir.txt (un código por línea, ej. YT-06877). Salida: yato/raw/<codigo>-<n>.<ext> y yato/log.txt
import os, re, time, urllib.request, urllib.parse
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15','Accept-Language':'en'}
B='https://toya24.pl'
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
os.makedirs('yato/raw',exist_ok=True); log=[]
for cod in [l.strip() for l in open('yato/pedir.txt') if l.strip()]:
    c=cod.upper().replace('YT','YT-').replace('YT--','YT-')
    try:
        h=get(B+'/search.php?'+urllib.parse.urlencode({'text':c})).decode('utf-8','ignore')
        links=list(dict.fromkeys(re.findall(r'(?:https://toya24\.pl)?/(?:[a-z]{2}-[A-Z]{2}/)?product-[a-z]{3}-\d+-[^"\'#?\s]+\.html',h)))
        ok=None
        for L in links[:6]:
            u=L if L.startswith('http') else B+L
            p=get(u).decode('utf-8','ignore')
            if re.search(r'\b'+re.escape(c)+r'\b',p): ok=(u,p); break
        if not ok:
            # a veces la búsqueda redirige directo a la ficha
            if re.search(r'\b'+re.escape(c)+r'\b',h) and 'hpeciai' in h: ok=('search',h)
        if not ok: log.append(f'{cod}\tSIN RESULTADO\t{len(links)} links'); continue
        u,p=ok
        imgs=list(dict.fromkeys(re.findall(r'/hpeciai/[0-9a-f]{32}/[a-z]{3}_[a-z]{2}_[^"\'\s)]+?\.(?:jpg|jpeg|png|webp)',p)))
        big=[i for i in imgs if '_pl_' in i] or imgs
        n=0
        for i in big[:3]:
            ext=i.rsplit('.',1)[1]
            open(f'yato/raw/{c}-{n}.{ext}','wb').write(get(B+i)); n+=1
        log.append(f'{cod}\t{u}\t{n} fotos ({len(imgs)} encontradas)')
    except Exception as e:
        log.append(f'{cod}\tERROR {e}')
    time.sleep(1.2)
open('yato/log.txt','a').write('\n'.join(log)+'\n')
