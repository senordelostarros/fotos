import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import publicacion, recortar, W
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); insta.OUT=os.path.join(B,'..','instagram')
S=os.path.join(B,'..','fuentes')+'/'
PW,PH=W-120,650
publicacion("31-jonnesway-torx-32-piezas.jpg",
  [(recortar(S+"jonnesway-torx-32-maleta.jpg"),(30,30,PW//2+40,PH-30)),
   (recortar(S+"jonnesway-torx-32-piezas.jpg"),(PW//2+60,50,PW-30,PH-50))],
  "Jonnesway · Nuevo","Juego dados torx macho y hembra, 32 pzas",
  "Cromo vanadio y molibdeno  ·  Maleta metálica","$39.000","+ IVA")
