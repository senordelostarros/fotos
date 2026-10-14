import sys
sys.path.insert(0,'/home/claude/fotos/trabajo/scripts')
import insta
insta.LOGO='/home/claude/fotos/trabajo/marca/logo-000.png'
from insta import recortar, patron, sombra, CARBON, AMAR, BLANCO, FB, FM, f
from PIL import Image, ImageDraw
D='/tmp/claude-0/-home-claude/cf9891fc-37a1-54db-a6fb-00cc4d3410f2/scratchpad/promo/'
g=recortar('/home/claude/fotos/ms-guante-de-nitrilo-naranjo-texturizado-alto-espesor-tallas-s-a-xl.jpg')
d=recortar(D+'dados.png')

def fit(p,h):
    return p.resize((int(p.width*h/p.height),h),Image.LANCZOS)

def pegar(c,p,cx,top):
    x=cx-p.width//2
    s=sombra(p); pad=(s.width-p.width)//2
    c.alpha_composite(s,(x-pad,top-pad)); c.alpha_composite(p,(x,top))

def badge(dr,cx,y,monto,regalo,fs1,fs2):
    t1=f"SOBRE {monto} + IVA"; F1=f(FB,fs1); w1=dr.textlength(t1,font=F1)
    ph,pv=int(fs1*.8),int(fs1*.45)
    dr.rounded_rectangle((cx-w1/2-ph,y,cx+w1/2+ph,y+fs1+pv*2+6),radius=12,fill=AMAR)
    dr.text((cx,y+pv),t1,font=F1,fill=CARBON,anchor="mt")
    y2=y+fs1+pv*2+16; F2=f(FM,fs2); t2="Regalo: "+regalo; w2=dr.textlength(t2,font=F2)
    dr.rounded_rectangle((cx-w2/2-20,y2,cx+w2/2+20,y2+fs2+22),radius=10,fill=CARBON)
    dr.text((cx,y2+9),t2,font=F2,fill=BLANCO,anchor="mt")

# Escritorio 1600x900 (zona segura al centro para cualquier ancho de pantalla)
W,H=1600,900
c=Image.new("RGBA",(W,H),CARBON+(255,))
pt=patron((W,H)).convert("RGBA")
m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon([(600,0),(W,0),(W,H),(470,H)],fill=255)
c.paste(pt,(0,0),m)
dr=ImageDraw.Draw(c); dr.line([(600,0),(470,H)],fill=AMAR,width=9)
pegar(c,fit(g,400),860,330); pegar(c,fit(d,430),1255,315)
badge(dr,860,150,"$100.000","caja de guantes naranjos",28,22)
badge(dr,1255,150,"$200.000","set de dados 1/4\"",28,22)
c.convert("RGB").save('/home/claude/fotos/promo-octubre-escritorio.jpg',quality=88)

# Celular 900x820
W,H=900,820
c=Image.new("RGBA",(W,H),CARBON+(255,))
pt=patron((W,500)).convert("RGBA"); c.paste(pt,(0,0))
dr=ImageDraw.Draw(c); dr.rectangle((0,496,W,506),fill=AMAR)
pegar(c,fit(g,280),240,190); pegar(c,fit(d,300),660,180)
badge(dr,240,30,"$100.000","guantes naranjos",26,20)
badge(dr,660,30,"$200.000","set dados 1/4\"",26,20)
c.convert("RGB").save('/home/claude/fotos/promo-octubre-celular.jpg',quality=88)
