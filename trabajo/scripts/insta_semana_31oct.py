"""Posts Instagram 37-60: sáb 31 oct a sáb 7 nov (bomba del día + 2 productos por día) e historias de cada bomba."""
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
# bombas: dia, foto, titulo, sku, precio normal, slug corto, texto
BOMBA={
 'sab':('ms5-inflador-manual-0-a-120-psi-con-pantalla-digital.jpg','Inflador digital 0 a 120 psi','YT73530',49489,'inflador-digital','inflador de pie con manómetro digital, para dejar cada neumático en su presión exacta','#Neumaticos #Inflador','inflador-manual-0-a-120-psi-con-pantalla-digital'),
 'dom':('ms5-llave-de-torque-12-60-a-330-nm.jpg','Llave de torque 1/2" 330 Nm','YT07415',186989,'llave-torque','llave de torque con clic de aviso, para apretar ruedas y culatas al torque exacto','#LlaveDeTorque #Torque','llave-de-torque-12-60-a-330-nm'),
 'lun':('ms5-juego-de-extractores-16-piezas.jpg','Extractores 16 piezas','YT25391',184789,'extractores-16','juego de extractores interior y exterior con martillo deslizante, para poleas, rodamientos y engranajes','#Extractores #Rodamientos','juego-de-extractores-16-piezas'),
 'mar':('ms5-gata-caiman-hidraulica-3-toneladas.jpg','Gata caimán hidráulica 3 t','YT17211',263989,'gata-caiman','gata caimán de 3 toneladas: tres bombeadas y arriba','#GataHidraulica #Gata','gata-caiman-hidraulica-3-toneladas'),
 'mie':('ms5-juego-chicharra-12-con-18-dados-19-piezas.jpg','Chicharra 1/2" con 18 dados','YT38681',76989,'chicharra-18-dados','chicharra de 72 dientes con 18 dados de 8 a 32 mm, el juego que no puede faltar','#Dados #Chicharra','juego-chicharra-12-con-18-dados-19-piezas'),
 'jue':('ms5-pistola-de-aire-caliente-2000-w.jpg','Pistola de calor 2000 W','YT82291',49489,'pistola-calor','pistola de calor de 2000 W hasta 550 °C, para sacar emblemas, adhesivos y retráctil','#PistolaDeCalor #Desabolladura','pistola-de-aire-caliente-2000-w'),
 'vie':('ms5-juego-de-dados-12-23-piezas-caja-metalica.jpg','Juego de dados 1/2" 23 piezas','YT12651',120989,'dados-23-piezas','juego de dados 1/2" de 23 piezas en caja metálica, con chicharra, extensiones y barrote','#Dados #Chicharra','juego-de-dados-12-23-piezas-caja-metalica'),
}
DN={'sab':'SÁBADO','dom':'DOMINGO','lun':'LUNES','mar':'MARTES','mie':'MIÉRCOLES','jue':'JUEVES','vie':'VIERNES'}
# productos: foto, etiqueta, titulo, detalle corto, sku, precio, slug, texto, hashtags
DIAS=[
 ('sab','Sábado 31 oct',[
  ('ms2-juego-para-extraer-rodamientos-delanteros-23-piezas.jpg','YATO · Taller mecánico','Extractor de masa 23 pzas','23 piezas · sin prensa','YT2541',175890,'extractor-rodamientos-masa','🔧 Saca y mete el rodamiento de masa con tornillo y campanas, sin prensa hidráulica. 23 piezas para los rodamientos delanteros más comunes.','#Rodamientos #Extractores #Suspension'),
  ('ms5-prensa-hidraulica-20-toneladas.jpg','YATO · Equipamiento','Prensa hidráulica 20 t','Para rodamientos, bujes y pasadores','YT55581',544500,'prensa-hidraulica-20t','💪 La prensa para el taller: rodamientos de masa, bujes, silentblocks y pasadores sin golpes. 20 toneladas, rango de trabajo de 0 a 695 mm.','#PrensaHidraulica #Rodamientos #Bujes')]),
 ('dom','Domingo 1 nov',[
  ('ms5-probador-de-bateria-y-alternador-12-v-1.jpg','YATO · Electricidad','Probador batería y alternador','12 V · diagnóstico rápido','YT83101',16489,'probador-bateria','🔋 Diagnóstico rápido: sabes al tiro si el problema es la batería o el alternador. Para sistemas de 12 V.','#Bateria #Alternador #ElectricidadAutomotriz'),
  ('ms5-cargador-partidor-compacto-9000-mah.jpg','YATO · Electricidad','Cargador partidor 9000 mAh','Pico de 600 A · 12 V','YT83081',137489,'partidor-9000','⚡ Parte el auto sin cables ni otro vehículo. Compacto, 9000 mAh y pico de 600 A. Funciona de -20 a 60 °C.','#Partidor #Bateria #Auxilio')]),
 ('lun','Lunes 2 nov',[
  ('ms5-tornillo-de-banco-5-125-mm.jpg','YATO · Equipamiento','Tornillo de banco 5" (125 mm)','Giratorio 360° · con yunque','YT6502',148489,'tornillo-banco-5','🛠️ El tornillo de banco que aguanta todo el trabajo del taller: mordazas de 125 mm, giratorio 360°, con yunque y 12 kN de fuerza.','#TornilloDeBanco #Taller #Maestranza'),
  ('ms5-prensa-rapida-reforzada-300-mm.jpg','YATO · Herramienta manual','Prensa rápida reforzada 300','Mayor fuerza de apriete','YT64291',24849,'prensa-rapida-300','✋ Prensa rápida reforzada de 300 mm, con mayor fuerza de apriete para trabajo pesado: soldar, pegar y cortar.','#PrensaRapida #Carpinteria #Soldadura')]),
 ('mar','Martes 3 nov',[
  ('ms5-gata-botella-20-toneladas-2.jpg','YATO · Levante','Gata botella 20 toneladas','Para camión y maquinaria','YT17007',97889,'gata-botella-20t','🚛 Levanta camiones y maquinaria sin esfuerzo. 20 toneladas, altura de 242 a 452 mm.','#GataBotella #Camiones #Maquinaria'),
  ('ms5-juego-de-barras-desmontadoras-de-neumaticos.jpg','YATO · Vulcanización','Barras desmontaneumáticos','Juego de 3 barras','YT55477',115489,'barras-neumaticos','🛞 Juego de barras de acero forjado para desmontar y montar neumáticos sin dañar la llanta.','#Vulcanizacion #Neumaticos #Gomeria')]),
 ('mie','Miércoles 4 nov',[
  ('ms5-juego-de-llaves-punta-corona-con-chicharra.jpg','YATO · Herramienta manual','Llaves con chicharra 12 pzas','12 piezas · 8 a 19 mm','YT02069',109989,'llaves-chicharra','⚙️ Llaves con chicharra de 72 dientes: aprietas y sueltas sin sacar la llave del perno. 12 medidas de 8 a 19 mm.','#Llaves #Chicharra #HerramientaManual'),
  ('ms5-juego-de-dados-de-impacto-largos-12.jpg','YATO · Impacto','Dados de impacto largos 1/2"','10 a 24 mm · cromo-molibdeno','YT1054',49489,'dados-impacto-largos','🔩 Dados largos de impacto en cromo-molibdeno, para la pistola neumática o eléctrica. Medidas de 10 a 24 mm.','#DadosDeImpacto #Dados #LlaveDeImpacto')]),
 ('jue','Jueves 5 nov',[
  ('ms5-juego-de-19-extractores-de-tapiceria-y-molduras.jpg','YATO · Desabolladura y tapicería','Extractores tapicería 19 pzas','Clips, paneles, radio y tablero','YT08442',43989,'extractores-tapiceria','🚗 Saca clips, paneles y molduras sin quebrarlos ni rayar. 19 piezas de plástico reforzado.','#Tapiceria #Desabolladura #Accesorios'),
  ('ms5-remachadora-tipo-fuelle-extensible.jpg','YATO · Herramienta manual','Remachadora tipo fuelle','Extensible · remaches hasta 6,4 mm','YT36060',41239,'remachadora-fuelle','🔨 Remachadora tipo fuelle: más fuerza con menos esfuerzo, para remaches grandes en carrocería y estructuras.','#Remachadora #Remaches #Carroceria')]),
 ('vie','Viernes 6 nov',[
  ('ms5-bomba-de-vacio-con-purgador-de-frenos-22-piezas.jpg','YATO · Frenos','Purgador de frenos 22 pzas','22 piezas · purga y diagnóstico','YT0674',87989,'purgador-frenos','🛑 Purga los frenos tú solo, sin ayudante. También sirve para diagnosticar vacío. 22 piezas en maleta.','#Frenos #PurgaDeFrenos #Taller'),
  ('ms5-juego-para-caliper-de-freno-35-piezas.jpg','YATO · Frenos','Juego para caliper 35 piezas','Para cambio de pastillas','YT06822',109989,'caliper-35','🛑 Retrocede los pistones del caliper para cambiar pastillas sin dañarlo. 35 piezas para distintos modelos.','#Frenos #Caliper #Pastillas')]),
 ('sab','Sábado 7 nov',[
  ('ms5-pistola-engrasadora-neumatica-400-cc.jpg','YATO · Lubricación','Engrasadora neumática','400 cc · acople rápido de aire','YT07055',41789,'engrasadora-neumatica','🛢️ Engrasa rótulas y crucetas con aire comprimido, sin cansarte la mano. Depósito de 400 cc.','#Lubricacion #Engrase #Maquinaria'),
  ('ms5-recuperador-de-aceite-65-litros-con-embudo.jpg','YATO · Lubricación','Recuperador de aceite 65 L','Embudo de 5 L · aspiración','YT07191',302489,'recuperador-aceite-65l','♻️ Cambio de aceite limpio: recibe con el embudo de 5 litros o aspira hasta el fondo. Capacidad total 70 litros.','#CambioDeAceite #Lubricentro #Taller')]),
]
TAGS='#ElSeñorDeLosTarros #Yato #Taller #Mecanica #Santiago'
num=37; textos=[]
for dia,fecha,prods in DIAS:
    foto,tit,sku,precio,slug,txt,tg,perma=BOMBA[dia]; pb=precio*0.8
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
open(os.path.join(insta.OUT,'textos-37-60-semana-31oct-7nov.txt'),'w').write('\n'.join(textos))
print('ok',num-1)
