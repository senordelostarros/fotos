"""Promo 3 x $13.900 IVA incl. · Grata circular 100 mm YATO YT-4757 (WhatsApp Business: estado 1080x1920 y cuadrado 1080x1080)."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import recortar, sombra, f, FB, FM, FR, CARBON, TURQ, AMAR, BLANCO, GRIS
from PIL import Image, ImageDraw
B=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(B,'..','..')+'/'
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); OUT=os.path.join(B,'..','whatsapp')+'/'
ROJO=(224,71,58)
g=recortar(R+'ms-grata-circular-100mm-con-vastago.jpg')
logo=Image.open(insta.LOGO).convert('RGBA')
def fit(p,w): return p.resize((int(w),int(p.height*w/p.width)),Image.LANCZOS)
def pegar(c,p,cx,cy):
    s=sombra(p,blur=24,op=90,dy=18); pad=(s.width-p.width)//2
    x,y=int(cx-p.width/2),int(cy-p.height/2); c.alpha_composite(s,(x-pad,y-pad)); c.alpha_composite(p,(x,y))
def tres(c,cx,cy,w):
    for dx,dy,k in [(-w*.42,-w*.10,.78),(w*.42,-w*.10,.78),(0,w*.08,1)]:
        pegar(c,fit(g,w*k),cx+dx,cy+dy)
def chip(d,cx,y,t,font,bg,fg,padx=34,pady=16):
    w=d.textlength(t,font=font); h=font.size
    d.rounded_rectangle([cx-w/2-padx,y,cx+w/2+padx,y+h+pady*2+6],radius=(h+pady*2)//2,fill=bg)
    d.text((cx,y+pady),t,font=font,fill=fg,anchor='mt')
def pieza(W,H,nombre,cuad):
    c=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(c)
    l=fit(logo,300 if not cuad else 250); c.alpha_composite(l,(60,50))
    d.text((W-60,80),'PROMO ESPECIAL',font=f(FB,34),fill=ROJO,anchor='ra')
    d.text((W-60,124),'Solo por pack de 3',font=f(FR,28),fill=GRIS,anchor='ra')
    if not cuad:
        d.rounded_rectangle([60,260,W-60,1060],radius=32,fill=(243,245,246))
        tres(c,W/2,660,560)
        d=ImageDraw.Draw(c)
        d.text((60,1110),'Grata circular 100 mm',font=f(FB,66),fill=CARBON)
        d.text((60,1195),'con vástago · YATO',font=f(FB,66),fill=CARBON)
        d.text((60,1290),'Alambre latonado · vástago 6 mm · 4.500 rpm · YT-4757',font=f(FM,30),fill=GRIS)
        d.rounded_rectangle([60,1370,W-60,1640],radius=28,fill=CARBON)
        d.text((W/2,1395),'LLÉVATE 3 POR',font=f(FB,40),fill=TURQ,anchor='mt')
        d.text((W/2,1450),'$13.900',font=f(FB,130),fill=AMAR,anchor='mt')
        d.text((W/2,1595),'IVA incluido · unidad $5.269 IVA incl.',font=f(FM,30),fill=BLANCO,anchor='mt')
        d.rectangle([0,H-200,W,H],fill=AMAR)
        d.text((W/2,H-140),'Pídelas por WhatsApp',font=f(FB,46),fill=CARBON,anchor='mt')
        d.text((W/2,H-80),'+56 9 4969 1686 · elsenordelostarros.cl',font=f(FM,34),fill=CARBON,anchor='mt')
    else:
        d.rounded_rectangle([60,200,W-60,640],radius=28,fill=(243,245,246))
        tres(c,W/2,425,360)
        d=ImageDraw.Draw(c)
        d.text((60,670),'Grata circular 100 mm con vástago YATO',font=f(FB,40),fill=CARBON)
        d.text((60,725),'Alambre latonado · vástago 6 mm · YT-4757',font=f(FM,28),fill=GRIS)
        d.rounded_rectangle([60,785,W-60,975],radius=24,fill=CARBON)
        d.text((110,880),'3 x',font=f(FB,64),fill=TURQ,anchor='lm')
        d.text((230,880),'$13.900',font=f(FB,104),fill=AMAR,anchor='lm')
        d.text((W-110,860),'IVA',font=f(FB,32),fill=BLANCO,anchor='rm')
        d.text((W-110,900),'incluido',font=f(FM,28),fill=BLANCO,anchor='rm')
        d.rectangle([0,H-80,W,H],fill=AMAR)
        d.text((W/2,H-40),'WhatsApp +56 9 4969 1686',font=f(FB,36),fill=CARBON,anchor='mm')
    c.convert('RGB').save(OUT+nombre,quality=92); print('listo',nombre)
pieza(1080,1920,'promo-grata-yt4757-estado.jpg',False)
pieza(1080,1080,'promo-grata-yt4757-cuadrado.jpg',True)
