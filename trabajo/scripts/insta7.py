import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from insta import publicacion, recortar, W
PW,PH=W-120,650; A=os.path.dirname(os.path.abspath(__file__))+'/yato469/out4/'
publicacion("19-llave-torque-yato.jpg",[(recortar(A+"413.jpg"),(30,40,PW-30,PH-40))],
  "YATO  ·  15% DCTO","Llave de torque 1/2\"","Con puntas intercambiables  ·  YT-0767","$345.941","+ IVA")
publicacion("20-bateria-18v-yato.jpg",[(recortar(A+"69.jpg"),(PW//2-260,40,PW//2+260,PH-40))],
  "YATO  ·  15% DCTO","Batería Li-Ion 18 V 2,0 Ah","Compatible con toda la línea YATO 18 V  ·  YT-82842","$42.066","+ IVA")
publicacion("21-destornillador-flexible-yato.jpg",[(recortar(A+"434.jpg"),(40,40,PW-40,PH-40))],
  "YATO  ·  15% DCTO","Destornillador flexible","Con dados y puntas, llega donde otros no  ·  YT-2780","$14.951","+ IVA")
