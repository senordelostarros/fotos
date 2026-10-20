import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import publicacion, recortar, W
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); insta.OUT=os.path.join(B,'..','instagram')
F=os.path.join(B,'..','..')+'/'
PW,PH=W-120,650
publicacion("25-chicharra-18-dados-yato.jpg",[(recortar(F+"ms5-juego-chicharra-12-con-18-dados-19-piezas.jpg"),(50,40,PW-50,PH-40))],
  "YATO","Chicharra 1/2\" con 18 dados","Dados de 8 a 32 mm  ·  Chicharra 72 dientes  ·  YT38681","$76.989","+ IVA")
publicacion("26-prensa-caliper-yato.jpg",[(recortar(F+"ms5-prensa-para-caliper-de-freno-0-a-65-mm.jpg"),(80,40,PW-80,PH-40))],
  "YATO","Prensa para caliper de freno","Apertura 0 a 65 mm  ·  Cambio de pastillas  ·  YT0610","$21.439","+ IVA")
publicacion("27-pistola-aire-caliente-yato.jpg",[(recortar(F+"ms5-pistola-de-aire-caliente-2000-w.jpg"),(60,40,PW-60,PH-40))],
  "YATO","Pistola de calor 2000 W","Hasta 550 °C  ·  500 l/min  ·  Con accesorios  ·  YT82291","$49.489","+ IVA")
