import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import publicacion, recortar, W, f, FB, FM, AMAR, GRIS
from PIL import Image, ImageDraw
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); insta.OUT=os.path.join(B,'..','instagram')
F=os.path.join(B,'..','..')+'/'
PW,PH=W-120,650
# 28 · Bomba del día (miércoles 21): chicharra -20%
n="28-bomba-chicharra-18-dados.jpg"
publicacion(n,[(recortar(F+"ms5-juego-chicharra-12-con-18-dados-19-piezas.jpg"),(50,60,PW-50,PH-40))],
  "Bomba del día · solo hoy","Chicharra 1/2\" con 18 dados","Danos hoy nuestra promoción de cada día  ·  YT38681","$61.591","+ IVA")
p=os.path.join(insta.OUT,n); im=Image.open(p).convert("RGB"); d=ImageDraw.Draw(im)
# sello -20%
cx,cy,r=W-150,300,95
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(224,71,58)); d.text((cx,cy),"-20%",font=f(FB,58),fill=(255,255,255),anchor="mm")
# precio anterior tachado
fa=f(FM,34); t="Antes $76.989"; x=W-60; y=1170
w=d.textlength(t,font=fa); d.text((x,y),t,font=fa,fill=GRIS,anchor="ra")
d.line([(x-w,y+21),(x,y+21)],fill=GRIS,width=3)
im.save(p,quality=92)
publicacion("29-remachadora-neumatica-yato.jpg",[(recortar(F+"ms5-remachadora-neumatica-1.jpg"),(80,40,PW-80,PH-40))],
  "YATO","Remachadora neumática","Fuerza 10.400 N  ·  Remaches 2,4 a 5,0 mm  ·  YT36171","$109.989","+ IVA")
publicacion("30-alicates-frenos-yato.jpg",[(recortar(F+"ms5-juego-de-alicates-para-frenos-3-piezas.jpg"),(60,40,PW-60,PH-40))],
  "YATO","Alicates para frenos, 3 piezas","Resortes y seguros de balatas  ·  YT0684","$29.139","+ IVA")
