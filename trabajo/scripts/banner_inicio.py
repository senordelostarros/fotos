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

# Fondo genérico para la bomba del día (el producto se pone encima con HTML)
escritorio('banner-bomba-escritorio.jpg',[],x_top=900,x_bot=770)
celular('banner-bomba-celular.jpg',[],alto=812)

# Mix de la tienda para el slide "Tu compra trae regalo"
LL='ms-juego-de-llaves-punta-corona-8-32-mm-17-piezas.jpg'; AM='ms-amarra-plastica-negra.jpg'; JB='ms-jabon-mecanico-2-litros.jpg'
HU='ms-huincha-aisladora-19mm-x-18m-negra.jpg'; H7='ms-ampolleta-halogena-h7-12v-55w-hella-px26d.jpg'; TK='ms-pano-mecanico-tork-heavy-duty-combi-roll-in-box-280-panos.jpg'
DH='ms2-juegos-de-dados-hexagonales-std-12-12-pzas.jpg'
escritorio('banner-mix-escritorio.jpg',[
  (LL,330,880,60),(DH,190,1200,90),(TK,300,1470,40),
  (MF,250,800,520),(INY,330,900,470),(FR,360,1030,450),
  (JB,250,1180,560),(HU,170,1340,600),(H7,220,1490,570),(GN,260,1300,300),(AM,230,1050,250)],x_top=640,x_bot=510)
celular('banner-mix-celular.jpg',[
  (LL,200,125,25),(DH,120,330,40),(TK,190,560,15),(GN,170,780,30),
  (MF,140,150,250),(INY,190,270,220),(FR,210,380,205),(JB,150,500,260),(HU,100,640,300),(H7,140,800,265)],alto=430)
