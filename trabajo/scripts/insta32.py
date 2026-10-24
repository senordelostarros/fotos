import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import publicacion, recortar, W, f, FB, FM, GRIS
from PIL import Image, ImageDraw
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); insta.OUT=os.path.join(B,'..','instagram')
F=os.path.join(B,'..','..')+'/'
PW,PH=W-120,650
# 32 · Bomba del día (sábado 24): inflador digital -20%
n="32-bomba-inflador-digital-yato.jpg"
publicacion(n,[(recortar(F+"ms5-inflador-manual-0-a-120-psi-con-pantalla-digital.jpg"),(60,50,PW-60,PH-40))],
  "Bomba del día · solo hoy","Inflador digital 0 a 120 psi","Danos hoy nuestra promoción de cada día  ·  YT73530","$39.591","+ IVA")
p=os.path.join(insta.OUT,n); im=Image.open(p).convert("RGB"); d=ImageDraw.Draw(im)
cx,cy,r=W-150,300,95
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(224,71,58)); d.text((cx,cy),"-20%",font=f(FB,58),fill=(255,255,255),anchor="mm")
fa=f(FM,34); t="Antes $49.489"; x=W-60; y=1170
w=d.textlength(t,font=fa); d.text((x,y),t,font=fa,fill=GRIS,anchor="ra")
d.line([(x-w,y+21),(x,y+21)],fill=GRIS,width=3)
im.save(p,quality=92)
publicacion("33-jabon-mecanico-yato-2l.jpg",[(recortar(F+"ms-jabon-mecanico-2-litros.jpg"),(120,40,PW-120,PH-40))],
  "YATO · El más pedido","Jabón mecánico 2 litros","Con partículas que sacan la grasa  ·  YT01234T","$14.289","+ IVA")
publicacion("34-panos-tork-280.jpg",[(recortar(F+"ms-pano-mecanico-tork-heavy-duty-combi-roll-in-box-280-panos.jpg"),(80,40,PW-80,PH-40))],
  "Tork · El más pedido","Paños Tork, rollo de 280","Absorben aceite y grasa sin pelusa  ·  TO70036","$33.900","+ IVA")
