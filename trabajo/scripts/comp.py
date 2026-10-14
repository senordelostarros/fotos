import numpy as np,os,sys
from PIL import Image
from scipy import ndimage
SZ={}
os.makedirs('out',exist_ok=True)
def compose(i,ids):
    im=np.asarray(Image.open(f'seg/{i}.png').convert('RGB')).copy(); lab=np.load(f'seg/{i}.npy')
    km=np.isin(lab,ids); km=ndimage.binary_fill_holes(ndimage.binary_closing(km,np.ones((5,5))))
    km=ndimage.binary_dilation(km,iterations=2)
    im[~km]=255
    ys,xs=np.where(km); o=Image.fromarray(im).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); SZ[i]=max(o.size)
    S=1000; inner=800; r=min(inner/o.width,inner/o.height)
    o=o.resize((max(1,int(o.width*r)),max(1,int(o.height*r))),Image.LANCZOS)
    c=Image.new('RGB',(S,S),'white'); c.paste(o,((S-o.width)//2,(S-o.height)//2)); c.save(f'out/{i}.jpg',quality=90)
ONLY=set(map(int,__import__("os").environ.get("ONLY","").split(","))) if __import__("os").environ.get("ONLY") else None
for l in open('dec.txt'):
    a,b=l.split()
    if b!="S" and (ONLY is None or int(a) in ONLY): compose(int(a),[int(t) for t in b.split(',')])
import json; json.dump(SZ,open('sz.json','w'))
