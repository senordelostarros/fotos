import pymupdf,sys,numpy as np
from PIL import Image
from rembg import remove,new_session
from scipy import ndimage
S=new_session('isnet-general-use')
def cut(pdf,page,box,out,TH=0.15):
    d=pymupdf.open(pdf); p=d[page]; W,H=p.rect.width,p.rect.height
    x0,y0,x1,y1=box
    pix=p.get_pixmap(dpi=220,clip=pymupdf.Rect(x0*W,y0*H,x1*W,y1*H))
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    o=remove(im,session=S); a=np.asarray(o)[...,3]
    m=a>40; et,n=ndimage.label(ndimage.binary_dilation(m,iterations=4))
    if n:
        sz=ndimage.sum(m,et,range(1,n+1)); keep=[i+1 for i,s in enumerate(sz) if s>=sz.max()*TH]
        km=np.isin(et,keep)&m
        arr=np.asarray(o).copy(); arr[...,3]=np.where(km,arr[...,3],0); o=Image.fromarray(arr)
    bg=Image.new('RGBA',o.size,(255,255,255,255)); bg.alpha_composite(o)
    ys,xs=np.where(np.asarray(o)[...,3]>40)
    c=bg.convert('RGB').crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    r=min(800/c.width,800/c.height); c=c.resize((int(c.width*r),int(c.height*r)),Image.LANCZOS)
    f=Image.new('RGB',(1000,1000),'white'); f.paste(c,((1000-c.width)//2,(1000-c.height)//2)); f.save(out,quality=92)
