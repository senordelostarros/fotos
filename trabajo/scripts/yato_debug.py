import urllib.request, urllib.parse, os
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15','Accept-Language':'en'}
os.makedirs('yato/debug',exist_ok=True)
for c in ['YT-0192','YT-5088','YT-0138']:
    u='https://toya24.pl/search.php?'+urllib.parse.urlencode({'text':c})
    r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60)
    open(f'yato/debug/{c}.html','wb').write(r.read()); open(f'yato/debug/{c}.url','w').write(r.geturl())
