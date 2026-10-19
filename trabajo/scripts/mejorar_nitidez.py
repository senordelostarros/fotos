import sys,torch,numpy as np,spandrel
from PIL import Image,ImageFilter
torch.set_num_threads(4)
M=spandrel.ModelLoader().load_from_file('/tmp/models/RealESRGAN_x4plus.pth').eval()
def mejorar(src,dst,div=4):
    im=Image.open(src).convert('RGB'); a=np.array(im)
    m=(a<240).any(2); ys,xs=np.where(m)
    y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    crop=im.crop((max(0,x0-12),max(0,y0-12),min(im.width,x1+12),min(im.height,y1+12)))
    small=crop.resize((max(8,crop.width//div),max(8,crop.height//div)),Image.LANCZOS)
    t=torch.from_numpy(np.array(small)).permute(2,0,1).float().div(255).unsqueeze(0)
    with torch.no_grad(): o=M(t).clamp(0,1)[0].permute(1,2,0).numpy()
    up=Image.fromarray((o*255).round().astype('uint8'))
    b=np.array(up); w=(b>235).all(2); b[w]=255; up=Image.fromarray(b)
    s=860/max(up.size); up=up.resize((int(up.width*s),int(up.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(1000,1000),'white'); c.paste(up,((1000-up.width)//2,(1000-up.height)//2))
    c.save(dst,quality=93)
if __name__=='__main__':
    for i in range(1,len(sys.argv),2): mejorar(sys.argv[i],sys.argv[i+1])
