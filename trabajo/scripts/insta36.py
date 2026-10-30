import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import publicacion, recortar, W, H, f, FB, FM, GRIS, CARBON, AMAR, BLANCO, TURQ
from PIL import Image, ImageDraw
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); insta.OUT=os.path.join(B,'..','instagram')
F=os.path.join(B,'..','..')+'/'
PW,PH=W-120,650
# 36 · Bomba del viernes 30: dados 1/2" 23 piezas -20%
n="36-bomba-dados-23-piezas.jpg"
publicacion(n,[(recortar(F+"ms5-juego-de-dados-12-23-piezas-caja-metalica.jpg"),(60,60,PW-60,PH-40))],
  "Bomba del día · solo hoy","Juego de dados 1/2\" 23 piezas","Danos hoy nuestra promoción de cada día  ·  YT12651","$96.791","+ IVA")
p=os.path.join(insta.OUT,n); im=Image.open(p).convert("RGB"); d=ImageDraw.Draw(im)
cx,cy,r=W-150,300,95
d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(224,71,58)); d.text((cx,cy),"-20%",font=f(FB,58),fill=(255,255,255),anchor="mm")
fa=f(FM,34); t="Antes $120.989"; x=W-60; y=1142
w=d.textlength(t,font=fa); d.text((x,y),t,font=fa,fill=GRIS,anchor="ra")
d.line([(x-w,y+21),(x,y+21)],fill=GRIS,width=3)
im.save(p,quality=92)

# Historia 1080x1920 con espacio para el sticker de enlace
SH=1920; s=Image.new("RGB",(W,SH),(255,255,255)); post=Image.open(p).convert("RGB")
s.paste(post,(0,120))
ds=ImageDraw.Draw(s)
ds.rectangle([0,0,W,120],fill=CARBON); ds.text((W//2,60),"BOMBA DEL VIERNES · SOLO HOY",font=f(FB,46),fill=AMAR,anchor="mm")
ds.rectangle([0,1470,W,SH],fill=CARBON)
ds.text((W//2,1560),"Toca el enlace para comprar",font=f(FB,52),fill=BLANCO,anchor="mm")
ds.rounded_rectangle([290,1640,790,1760],radius=60,outline=AMAR,width=5)
ds.text((W//2,1700),"(pon aquí el enlace)",font=f(FM,34),fill=GRIS,anchor="mm")
s.save(os.path.join(insta.OUT,"36-historia-bomba-dados-23-piezas.jpg"),quality=92)
print('ok')
