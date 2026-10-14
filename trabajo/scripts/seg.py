import json,os,sys,numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
sys.path.insert(0,'..'); from ms_proc import to_rgb,card_crop
SP='..'; os.makedirs('seg',exist_ok=True); os.makedirs('ann',exist_ok=True)
y=json.load(open('pend.json')); files=os.listdir(SP+'/ms/all_orig')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') else ImageFont.load_default()
idx=[]
for i,x in enumerate(y):
    fs=[f for f in files if os.path.splitext(f)[0]==x['p'][:80] or os.path.splitext(f)[0]==x['p']]
    if not fs: fs=[f for f in files if f.startswith(x['p'][:60])]
    if not fs: print('nofile',x['p']); continue
    try: im=to_rgb(Image.open(SP+'/ms/all_orig/'+fs[0]))
    except Exception as e: print('bad',fs[0]); continue
    a=np.asarray(im).astype(np.int16)
    cc=card_crop(a)
    if cc:
        x0,y0,x1,y1=cc; im=im.crop((x0+6,y0+6,x1-6,y1-6)); a=np.asarray(im).astype(np.int16)
    if max(im.size)>900:
        r=900/max(im.size); im=im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS); a=np.asarray(im).astype(np.int16)
    ink=(a.min(axis=2)<232)|((a.max(axis=2)-a.min(axis=2))>30)
    ink[:3,:]=ink[-3:,:]=False; ink[:,:3]=ink[:,-3:]=False
    m=ndimage.binary_closing(ink,structure=np.ones((3,3)))
    et,n=ndimage.label(m)
    H,W=m.shape; objs=ndimage.find_objects(et)
    comps=[]
    for k,sl in enumerate(objs,1):
        ar=(et[sl]==k).sum()
        if ar>=0.002*H*W: comps.append((ar,k,sl))
    comps.sort(reverse=True); comps=comps[:18]
    lab=np.zeros_like(et,dtype=np.uint8)
    ann=im.copy().convert('RGB'); d=ImageDraw.Draw(ann)
    for j,(ar,k,sl) in enumerate(comps,1):
        lab[et==k]=j
        y0,y1,x0,x1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
        col=['red','blue','green','magenta','orange','purple'][j%6]
        d.rectangle((x0,y0,x1,y1),outline=col,width=3)
        d.rectangle((x0,y0,x0+30,y0+26),fill=col); d.text((x0+4,y0+1),str(j),fill='white',font=font)
    im.save(f'seg/{i}.png'); np.save(f'seg/{i}.npy',lab); ann.save(f'ann/{i}.jpg',quality=85)
    idx.append(i)
json.dump(idx,open('idx.json','w'))
print(len(idx))
