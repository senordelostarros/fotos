"""Carrusel Instagram 1080x1350: cómo usar elsenordelostarros.cl"""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import *
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=LOGO=os.path.join(B,'..','marca','logo-000.png')
OUT=os.path.join(B,'..','instagram','web'); os.makedirs(OUT,exist_ok=True)
F=os.path.join(B,'..','..')+'/'

def base(n,total=5):
    img=Image.new('RGB',(W,H),CARBON); d=ImageDraw.Draw(img)
    logo=Image.open(LOGO).convert('RGB'); lw=260
    logo=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS); img.paste(logo,(60,52))
    d.text((W-60,92),f'{n}/{total}',font=f(FB,30),fill=GRIS,anchor='rm')
    d.rectangle([0,H-96,W,H],fill=AMAR)
    d.text((60,H-48),'elsenordelostarros.cl',font=f(FB,32),fill=CARBON,anchor='lm')
    d.text((W-60,H-48),'WhatsApp +56 9 4969 1686',font=f(FM,26),fill=CARBON,anchor='rm')
    return img,d

def panel(img,y0,y1):
    p=patron((W-120,y1-y0)); m=Image.new('L',p.size,0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,p.width-1,p.height-1],28,fill=255); img.paste(p,(60,y0),m)

def titulo(d,y,lineas,tam=64,color=BLANCO,acento=None):
    for ln in lineas:
        c=AMAR if acento and ln in acento else color
        d.text((60,y),ln,font=f(FB,tam),fill=c); y+=int(tam*1.2)
    return y

def parrafo(d,y,txt,tam=32,color=GRIS,ancho=W-120):
    ft=f(FR,tam); act=''
    for p in txt.split():
        pr=(act+' '+p).strip()
        if d.textlength(pr,font=ft)<=ancho: act=pr
        else: d.text((60,y),act,font=ft,fill=color); y+=int(tam*1.45); act=p
    d.text((60,y),act,font=ft,fill=color); return y+int(tam*1.45)

def chip(d,x,y,txt,tam=30,bg=TURQ,fg=CARBON):
    ft=f(FB,tam); w=d.textlength(txt,font=ft)
    d.rounded_rectangle([x,y,x+w+44,y+tam+30],radius=(tam+30)//2,fill=bg)
    d.text((x+22,y+(tam+30)//2),txt,font=ft,fill=fg,anchor='lm'); return x+w+44

def productos(img,y0,y1,fotos):
    n=len(fotos); cw=(W-120)//n
    for i,fn in enumerate(fotos):
        colocar(img,recortar(F+fn),(60+i*cw+20,y0+30,60+(i+1)*cw-20,y1-30))

# 1 portada
img,d=base(1)
panel(img,200,760)
productos(img,200,760,['ms-guante-de-nitrilo-naranjo-texturizado-alto-espesor-tallas-s-a-xl.jpg','ms5-juego-chicharra-12-con-18-dados-19-piezas.jpg','ms-caja-dados-14-18-piezas-4-14mm.jpg'])
y=titulo(d,810,['Tu taller,','ahora también','en la web'],70,acento=['en la web'])
parrafo(d,y+10,'Te contamos cómo usar nuestra página. Desliza para ver más',34)
img.save(f'{OUT}/web-1-portada.jpg',quality=92)

# 2 categorías
img,d=base(2)
y=titulo(d,210,['Encuentra todo','por categoría'],66,acento=['por categoría'])
y=parrafo(d,y+10,'En el menú "Productos" o en el buscador de arriba:',32)
cats=['Herramientas manuales','Eléctricas y neumáticas','Insumos de taller','Desabolladura y pintura','Diagnóstico','Equipamiento de taller','Seguridad e higiene','Promociones']
y+=20
for c in cats:
    d.rounded_rectangle([60,y,W-60,y+78],radius=18,fill=(42,47,54))
    d.rectangle([60,y,72,y+78],fill=AMAR)
    d.text((100,y+39),c,font=f(FB,34),fill=BLANCO,anchor='lm'); y+=94
img.save(f'{OUT}/web-2-categorias.jpg',quality=92)

# 3 cómo comprar
img,d=base(3)
y=titulo(d,210,['Comprar es','muy simple'],66,acento=['muy simple'])
pasos=[('1','Elige tu producto','y agrégalo al carro'),('2','Ingresa tus datos','y la dirección de despacho'),('3','Paga con tarjeta o transferencia','y recibe tu factura')]
y+=40
for n,t,s in pasos:
    d.ellipse([60,y,160,y+100],fill=AMAR); d.text((110,y+50),n,font=f(FB,54),fill=CARBON,anchor='mm')
    d.text((190,y+8),t,font=f(FB,40),fill=BLANCO); d.text((190,y+60),s,font=f(FR,30),fill=GRIS); y+=170
y+=10
d.rounded_rectangle([60,y,W-60,y+190],radius=24,fill=TURQ)
d.text((100,y+38),'¿Prefieres WhatsApp?',font=f(FB,40),fill=CARBON)
d.text((100,y+100),'Toca el botón verde de WhatsApp,',font=f(FM,30),fill=CARBON)
d.text((100,y+140),'está en toda la página.',font=f(FM,30),fill=CARBON)
img.save(f'{OUT}/web-3-como-comprar.jpg',quality=92)

# 4 condiciones
img,d=base(4)
y=titulo(d,210,['Lo que','tienes que saber'],66,acento=['tienes que saber'])
items=[('Precios netos','El IVA se suma en el carro'),('Emitimos factura','Para tu empresa o taller'),('Despacho Santiago $5.000','Regiones: envío por pagar al recibir'),('Atención directa','Te responde una persona, no un robot')]
y+=40
for t,s in items:
    d.rounded_rectangle([60,y,W-60,y+150],radius=22,fill=(42,47,54))
    d.ellipse([96,y+50,146,y+100],fill=AMAR); d.line([(108,y+76),(118,y+86),(135,y+64)],fill=CARBON,width=6,joint='curve')
    d.text((176,y+30),t,font=f(FB,40),fill=BLANCO); d.text((176,y+86),s,font=f(FR,30),fill=GRIS); y+=172
img.save(f'{OUT}/web-4-condiciones.jpg',quality=92)

# 5 cierre
img,d=base(5)
panel(img,200,700)
productos(img,200,700,['ms5-prensa-para-caliper-de-freno-0-a-65-mm.jpg','ms5-pistola-de-aire-caliente-2000-w.jpg'])
y=titulo(d,750,['Promo de octubre:','tu compra trae regalo'],56,acento=['tu compra trae regalo'])
y=parrafo(d,y+6,'Sobre $100.000 neto: caja de guantes naranjos. Sobre $200.000 neto: set de dados 1/4". Hasta el 31 de octubre.',31)
chip(d,60,y+24,'Entra a elsenordelostarros.cl',34,bg=AMAR)
img.save(f'{OUT}/web-5-promo.jpg',quality=92)
print('ok')
