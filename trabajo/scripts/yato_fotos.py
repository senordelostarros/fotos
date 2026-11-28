# Descarga fotos oficiales YATO desde toya24.pl (tienda oficial de TOYA S.A.). Corre en GitHub Actions.
# Entrada: yato/pedir.txt (un código por línea, ej. YT-06877). Salida: yato/raw/<codigo>-<n>.<ext> y yato/log.txt
import os, re, time, urllib.request, urllib.parse
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15','Accept-Language':'en'}
B='https://toya24.pl'
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
import shutil; shutil.rmtree('yato/raw',ignore_errors=True); os.makedirs('yato/raw',exist_ok=True); log=[]
open('yato/log.txt','w').write('')
for cod in [l.strip() for l in open('yato/pedir.txt') if l.strip()]:
    c=cod.upper().replace('YT','YT-').replace('YT--','YT-')
    try:
        r=urllib.request.urlopen(urllib.request.Request(B+'/search.php?'+urllib.parse.urlencode({'text':c}),headers=UA),timeout=60)
        u=r.geturl(); p=r.read().decode('utf-8','ignore')
        if '/products/' not in u and '/product-' not in u:
            log.append(f'{cod}\tLISTA (varios resultados, no se usa)\t{u}'); time.sleep(1.2); continue
        if not re.search(r'(?<![A-Z0-9-])'+re.escape(c)+r'(?![0-9])',p):
            log.append(f'{cod}\tDUDOSO ficha sin el código\t{u}'); time.sleep(1.2); continue
        imgs=list(dict.fromkeys(re.findall(r'/hpeciai/[0-9a-f]{32}/[a-z]{3}_pl_[^"\'\s)]+?\.(?:jpg|jpeg|png|webp)',p)))
        def num(i):
            m=re.search(r'_(\d+)\.[a-z]+$',i); return int(m.group(1)) if m else 0
        imgs.sort(key=num)
        n=0; urls=[]
        for i in imgs[:3]:
            ext=i.rsplit('.',1)[1]
            open(f'yato/raw/{c}-{n}.{ext}','wb').write(get(B+i)); n+=1; urls.append(i)
        log.append(f'{cod}\t{u}\t{n} fotos\t'+' '.join(urls))
    except Exception as e:
        log.append(f'{cod}\tERROR {e}')
    time.sleep(1.2)
open('yato/log.txt','a').write('\n'.join(log)+'\n')
