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
# bombas nuevas por fecha: foto, titulo, sku, precio, slug, texto, hashtags, permalink
BOMBA={
 'Domingo 1 nov':('ms5-juego-de-dados-cortos-y-largos-14-23-piezas.jpg','Dados 1/4" largos y cortos 23','YT14451',43989,'dados-14-23-piezas','juego de dados 1/4" cortos y largos de 4 a 13 mm, con accesorios de encastre, para el trabajo fino del motor','#Dados #Chicharra','juego-de-dados-cortos-y-largos-14-23-piezas'),
 'Lunes 2 nov':('ms5-juego-extractor-universal-de-2-y-3-brazos.jpg','Extractor universal 12 pzas','YT25105',197989,'extractor-universal','juego extractor universal interior y exterior de 2 o 3 brazos, 12 piezas con brazos de 100, 200 y 250 mm','#Extractores #Rodamientos','juego-de-extractor-universal-interior-y-exterior'),
 'Martes 3 nov':('ms5-gata-caiman-hidraulica-2-toneladas.jpg','Gata caimán hidráulica 2 t','YT1720',160589,'gata-caiman-2t','gata caimán de 2 toneladas con mango giratorio, de 89 a 359 mm de altura, para vehículo liviano','#GataHidraulica #Gata','gata-caiman-2-ton-1'),
 'Miércoles 4 nov':('ms5-juego-de-dados-para-tapones-de-carter.jpg','Dados para tapones de cárter','YT0600',75339,'dados-carter','juego de 12 dados para tapones de cárter, con las medidas más usadas en vehículo liviano','#CambioDeAceite #Lubricentro','juego-de-dados-para-tapones-de-carter'),
 'Jueves 5 nov':('ms5-juego-para-sensores-de-oxigeno-e-inyeccion-diesel.jpg','Dados sensores de oxígeno','YT1751',65989,'sensores-oxigeno','juego de 7 piezas para sensores de oxígeno e inyección diésel, medidas 27 y 28 mm','#SensorDeOxigeno #Diesel','juego-para-sensores-de-oxigeno-e-inyeccion-diesel'),
 'Viernes 6 nov':('ms5-juego-de-extractores-de-rotulas-de-direccion-1.jpg','Extractores de rótulas 5 pzas','YT0616',50589,'extractores-rotulas','juego de 5 extractores de rótulas de dirección, con extractor de pasador de bola y de varilla','#Rotulas #Direccion #Suspension','juego-de-extractores-de-rotulas-de-direccion'),
 'Sábado 7 nov':('ms5-juego-de-dados-torx-de-impacto-12.jpg','Dados torx de impacto 1/2"','YT1065',60489,'dados-torx-impacto','juego de 8 dados torx de impacto de T30 a T80, acero CrMo con dureza HRC 54','#DadosDeImpacto #Torx','juego-de-dados-torx-de-impacto-12'),
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
  ('ms6-bomba-de-vacio-con-purgador-de-frenos-22-piezas.jpg','YATO · Frenos','Purgador de frenos 22 pzas','22 piezas · purga y diagnóstico','YT0674',87989,'purgador-frenos','🛑 Purga los frenos tú solo, sin ayudante. También sirve para diagnosticar vacío. 22 piezas en maleta.','#Frenos #PurgaDeFrenos #Taller'),
  ('ms5-juego-para-caliper-de-freno-35-piezas.jpg','YATO · Frenos','Juego para caliper 35 piezas','Para cambio de pastillas','YT06822',109989,'caliper-35','🛑 Retrocede los pistones del caliper para cambiar pastillas sin dañarlo. 35 piezas para distintos modelos.','#Frenos #Caliper #Pastillas')]),
 ('sab','Sábado 7 nov',[
  ('ms5-pistola-engrasadora-neumatica-400-cc.jpg','YATO · Lubricación','Engrasadora neumática','400 cc · acople rápido de aire','YT07055',41789,'engrasadora-neumatica','🛢️ Engrasa rótulas y crucetas con aire comprimido, sin cansarte la mano. Depósito de 400 cc.','#Lubricacion #Engrase #Maquinaria'),
  ('ms5-recuperador-de-aceite-65-litros-con-embudo.jpg','YATO · Lubricación','Recuperador de aceite 65 L','Embudo de 5 L · aspiración','YT07191',302489,'recuperador-aceite-65l','♻️ Cambio de aceite limpio: recibe con el embudo de 5 litros o aspira hasta el fondo. Capacidad total 70 litros.','#CambioDeAceite #Lubricentro #Taller')]),
]
TAGS='#ElSeñorDeLosTarros #Yato #Taller #Mecanica #Santiago'
num=37; textos=[]
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
open(os.path.join(insta.OUT,'textos-37-59-semana-31oct-7nov.txt'),'w').write('\n'.join(textos))
print('ok',num-1)
