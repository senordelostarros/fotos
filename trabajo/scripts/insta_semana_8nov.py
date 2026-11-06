"""Posts Instagram 60-80: dom 8 a sáb 14 nov (bomba del día + 2 productos por día) e historias de cada bomba."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import publicacion, recortar, W, f, FB, FM, GRIS, CARBON, AMAR, BLANCO
from PIL import Image, ImageDraw
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); insta.OUT=os.path.join(B,'..','instagram')
F=os.path.join(B,'..','..')+'/'
PW,PH=W-120,650
def cl(v): return '$'+f'{round(v):,}'.replace(',','.')
from semana_8nov_datos import BOMBAS as BB, PRODS as PP
BOMBA={b[1]:(b[2],b[3],b[4],b[5],b[6],b[7],b[8],b[9]) for b in BB}
DN={'sab':'SÁBADO','dom':'DOMINGO','lun':'LUNES','mar':'MARTES','mie':'MIÉRCOLES','jue':'JUEVES','vie':'VIERNES'}
DIAS=[(b[0],b[1],[p[:9] for p in PP[i]]) for i,b in enumerate(BB)]
TAGS='#ElSeñorDeLosTarros #Yato #Taller #Mecanica #Santiago'
num=60; textos=[]
for dia,fecha,prods in DIAS:
  if fecha not in BOMBA: textos.append(f"══════ {fecha.upper()} ══════\n\n(Bomba de hoy: inflador digital, ya salió en post. Hoy sube solo el Reel y la historia de la bomba.)\n")
  else:
    foto,tit,sku,precio,slug,txt,tg,perma=BOMBA[fecha]; pb=precio*0.8
    n=f"{num}-bomba-{slug}.jpg"
    publicacion(n,[(recortar(F+foto),(60,50,PW-60,PH-40))],"Bomba del día · solo hoy",tit,f"Danos hoy nuestra promoción de cada día  ·  {sku}",cl(pb),"+ IVA")
    p=os.path.join(insta.OUT,n); im=Image.open(p).convert("RGB"); d=ImageDraw.Draw(im)
    cx,cy,r=W-150,300,95; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(224,71,58)); d.text((cx,cy),"-20%",font=f(FB,58),fill=(255,255,255),anchor="mm")
    fa=f(FM,34); t="Antes "+cl(precio); x=W-60; y=1142; w=d.textlength(t,font=fa); d.text((x,y),t,font=fa,fill=GRIS,anchor="ra"); d.line([(x-w,y+21),(x,y+21)],fill=GRIS,width=3)
    im.save(p,quality=92)
    s=Image.new("RGB",(W,1920),(255,255,255)); s.paste(im,(0,120)); ds=ImageDraw.Draw(s)
    ds.rectangle([0,0,W,120],fill=CARBON); ds.text((W//2,60),f"BOMBA DEL {DN[dia]} · SOLO HOY",font=f(FB,46),fill=AMAR,anchor="mm")
    ds.rectangle([0,1470,W,1920],fill=CARBON); ds.text((W//2,1560),"Toca el enlace para comprar",font=f(FB,52),fill=BLANCO,anchor="mm")
    ds.rounded_rectangle([290,1640,790,1760],radius=60,outline=AMAR,width=5); ds.text((W//2,1700),"(pon aquí el enlace)",font=f(FM,34),fill=GRIS,anchor="mm")
    s.save(os.path.join(insta.OUT,f"{num}-historia-bomba-{slug}.jpg"),quality=92)
    textos.append(f"══════ {fecha.upper()} ══════\n\n{num} · Bomba del día: {tit} YATO\n🔥 Danos hoy nuestra promoción de cada día: {txt}. 20% más barato solo por hoy.\n💲 {cl(pb)} + IVA (antes {cl(precio)}) · Código {sku}\n📲 Pedidos por WhatsApp +56 9 4969 1686 · elsenordelostarros.cl\n#ElSeñorDeLosTarros #BombaDelDia #Yato {tg} #Taller #Mecanica #Santiago\n🔗 Enlace historia: https://www.elsenordelostarros.cl/{perma}\n")
    num+=1
  for foto,et,tit,det,sku,precio,slug,txt,tg in prods:
    publicacion(f"{num}-{slug}.jpg",[(recortar(F+foto),(60,50,PW-60,PH-40))],et,tit,f"{det}  ·  {sku}",cl(precio),"+ IVA")
    textos.append(f"{num} · {tit} YATO\n{txt}\n💲 {cl(precio)} + IVA · Código {sku}\n📲 Pedidos por WhatsApp +56 9 4969 1686 · elsenordelostarros.cl\n#ElSeñorDeLosTarros #Yato {tg} #Taller #Mecanica #Santiago\n")
    num+=1
open(os.path.join(insta.OUT,'textos-60-80-semana-8-14nov.txt'),'w').write('\n'.join(textos))
print('ok',num-1)
