"""Fondos del banner del inicio (banner.html). Escritorio 1600x900, celular 900x820."""
import sys,os
B=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(B,'..','..')+'/'
sys.path.insert(0,B)
import insta
insta.LOGO=os.path.join(B,'..','marca','logo-000.png')
from insta import recortar, patron, sombra, CARBON, AMAR
from PIL import Image, ImageDraw

def fit(p,h): return p.resize((int(p.width*h/p.height),h),Image.LANCZOS)
def pegar(c,p,cx,top):
    x=cx-p.width//2; s=sombra(p); pad=(s.width-p.width)//2
    c.alpha_composite(s,(x-pad,top-pad)); c.alpha_composite(p,(x,top))

def escritorio(nombre,prods,x_top=600,x_bot=470):
    W,H=1600,900
    c=Image.new("RGBA",(W,H),CARBON+(255,)); pt=patron((W,H)).convert("RGBA")
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon([(x_top,0),(W,0),(W,H),(x_bot,H)],fill=255)
    c.paste(pt,(0,0),m); ImageDraw.Draw(c).line([(x_top,0),(x_bot,H)],fill=AMAR,width=9)
    for f,h,cx,top in prods: pegar(c,fit(recortar(R+f),h),cx,top)
    c.convert("RGB").save(R+nombre,quality=86)

def celular(nombre,prods,alto=430):
    W,H=900,820
    c=Image.new("RGBA",(W,H),CARBON+(255,)); c.paste(patron((W,alto)).convert("RGBA"),(0,0))
    ImageDraw.Draw(c).rectangle([0,alto-4,W,alto+5],fill=AMAR)
    for f,h,cx,top in prods: pegar(c,fit(recortar(R+f),h),cx,top)
    c.convert("RGB").save(R+nombre,quality=86)

MF='ms-motor-flush-motorbike-10min.jpg'; INY='ms-limpia-inyector-gasolina.jpg'; FR='ms-limpia-frenos-660ml.jpg'
GN='ms-guante-de-nitrilo-naranjo-texturizado-alto-espesor-tallas-s-a-xl.jpg'; DA='ms2-juegos-de-dados-hexagonales-std-12-12-pzas.jpg'
GA='ms-guante-de-nylon-con-palma-de-poliuretano-aquiles-tallas-7-a-10.jpg'

# Senfineco: zona oscura grande a la izquierda (texto + guía), latas a la derecha
escritorio('banner-senfineco-escritorio.jpg',[(INY,560,1130,190),(MF,470,1330,300),(FR,600,1500,170)],x_top=1000,x_bot=870)
celular('banner-senfineco-celular.jpg',[(INY,330,300,60),(MF,280,470,120),(FR,350,640,45)],alto=430)
# Despacho y factura
escritorio('banner-despacho-escritorio.jpg',[(GA,330,740,270),(DA,200,1110,420),(GN,360,1460,240)])
celular('banner-despacho-celular.jpg',[(GA,230,150,110),(DA,150,450,190),(GN,250,750,80)],alto=430)
print('ok')
