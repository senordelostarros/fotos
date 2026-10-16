import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import insta
from insta import publicacion, recortar, W
B=os.path.dirname(os.path.abspath(__file__))
insta.LOGO=os.path.join(B,'..','marca','logo-000.png'); insta.OUT=os.path.join(B,'..','instagram')
F=os.path.join(B,'..','..')+'/'
PW,PH=W-120,650
publicacion("22-linterna-lapiz-irimo.jpg",[(recortar(F+"ms-linterna-de-taller-tipo-lapiz-recargable-y-magnetica.jpg"),(60,40,PW-60,PH-40))],
  "IRIMO","Linterna de taller tipo lápiz","Recargable y magnética  ·  150 lm  ·  L-PEN-1","$9.490","+ IVA")
publicacion("23-camilla-tipo-z.jpg",[(recortar(F+"ms-camilla-de-trabajo-convertible-en-piso-tipo-z.jpg"),(50,40,PW-50,PH-40))],
  "Equipamiento de taller","Camilla convertible en piso tipo Z","Dos en uno: camilla o asiento  ·  Largo 92 cm","$71.489","+ IVA")
publicacion("24-linterna-cob-irimo.jpg",[(recortar(F+"ms-linterna-cob-inalambrica-y-plegable-l-slim-1.jpg"),(60,40,PW-60,PH-40))],
  "IRIMO","Linterna COB plegable","Hasta 400 lm regulable  ·  Inalámbrica  ·  L-SLIM-1","$53.889","+ IVA")
