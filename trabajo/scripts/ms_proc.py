import sys,os,numpy as np
from PIL import Image
from scipy import ndimage
def to_rgb(im):
    if im.mode in('RGBA','LA','P'):
        im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
    return im.convert('RGB')
def card_crop(a):
    # plantilla turquesa: buscar la tarjeta blanca grande
    turq=(np.abs(a[...,0]-111)<35)&(np.abs(a[...,1]-200)<35)&(np.abs(a[...,2]-218)<35)
    if turq.mean()<0.25: return None
    white=a.min(axis=2)>235
    et,n=ndimage.label(white)
    if n==0: return None
    areas=ndimage.sum(white,et,range(1,n+1)); k=int(np.argmax(areas))+1
    ys,xs=np.where(et==k)
    return (xs.min(),ys.min(),xs.max()+1,ys.max()+1)
def procesar(path,out,frac=0.12,margin=0.10):
    im=to_rgb(Image.open(path))
    a=np.asarray(im).astype(np.int16)
    info=''
    cc=card_crop(a)
    if cc:
        x0,y0,x1,y1=cc; im=im.crop((x0+6,y0+6,x1-6,y1-6)); a=np.asarray(im).astype(np.int16); info='tarjeta'
    ink=a.min(axis=2)<232
    ink|=(a.max(axis=2)-a.min(axis=2))>30
    # quitar marco/borde de 3px
    ink[:3,:]=ink[-3:,:]=False; ink[:,:3]=ink[:,-3:]=False
    m=ndimage.binary_closing(ink,structure=np.ones((5,5)))
    et,n=ndimage.label(m)
    if n==0: return 'vacia'
    H,W=m.shape
    gray=a.mean(axis=2); sat=a.max(axis=2)-a.min(axis=2)
    comps=[]
    for k in range(1,n+1):
        sl=ndimage.find_objects(et==k)[0] if False else None
    objs=ndimage.find_objects(et)
    for k,sl in enumerate(objs,1):
        cm=(et[sl]==k); ar=cm.sum()
        if ar<30: continue
        bh=sl[0].stop-sl[0].start; bw=sl[1].stop-sl[1].start
        fill=ar/(bh*bw)
        if fill<0.12 and (bh>0.6*H or bw>0.6*W): continue   # marcos y líneas largas
        g=gray[sl][cm]; sa=sat[sl][cm]
        mid=(((g>60)&(g<215))|(sa>60)).mean()
        comps.append(dict(k=k,ar=ar,mid=mid,sl=sl))
    if not comps: return 'vacia'
    def textish(c):
        g=gray[c['sl']][et[c['sl']]==c['k']]
        return ((g<70)|(g>200)).mean()>0.80 and c['mid']<0.30
    cand=[c for c in comps if not textish(c)] or comps
    main=max(cand,key=lambda c:c['ar'])
    keep=[c['k'] for c in cand if c is main or (c['ar']>=main['ar']*0.22 and c['mid']>0.30)]
    km=np.isin(et,keep); km=ndimage.binary_fill_holes(km)
    m=et>0
    ys,xs=np.where(km)
    rgb=np.asarray(im).copy()
    rgb[~ndimage.binary_dilation(km,iterations=2)]=255
    o=Image.fromarray(rgb).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    S=1000; inner=int(S*(1-2*margin)); r=min(inner/o.width,inner/o.height)
    o=o.resize((max(1,int(o.width*r)),max(1,int(o.height*r))),Image.LANCZOS)
    c=Image.new('RGB',(S,S),'white'); c.paste(o,((S-o.width)//2,(S-o.height)//2))
    c.save(out,quality=90)
    dropped=1-km.sum()/max(1,m.sum())
    return f'{info} keep={len(keep)}/{n} drop={dropped:.2f} src={max(a.shape[:2])}'
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]
    for f in sorted(os.listdir(src)):
        r=procesar(os.path.join(src,f),os.path.join(dst,os.path.splitext(f)[0]+'.jpg'))
        print(f[:40],r)
