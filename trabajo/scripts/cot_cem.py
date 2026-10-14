from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
F='/usr/share/fonts/truetype/google-fonts/'
pdfmetrics.registerFont(TTFont('PB',F+'Poppins-Bold.ttf'));pdfmetrics.registerFont(TTFont('PM',F+'Poppins-Medium.ttf'));pdfmetrics.registerFont(TTFont('PR',F+'Poppins-Regular.ttf'))
CAR=HexColor('#1D2126');TUR=HexColor('#6FC8DA');AM=HexColor('#FFC72C');GR=HexColor('#6B7480');LG=HexColor('#EEF1F4')
out='/mnt/user-data/outputs/Cotizacion_Siglo21_Multimetro_Osciloscopio_CEM_AT-9996.pdf'
W,H=letter;c=canvas.Canvas(out,pagesize=letter);M=46
def n(v):return '$'+f'{v:,.0f}'.replace(',','.')
# header
c.setFillColor(CAR);c.rect(0,H-110,W,110,fill=1,stroke=0)
lg=ImageReader('logo/logo-000.png');lw,lh=lg.getSize();w=170;c.drawImage(lg,M,H-95,w,w*lh/lw,mask='auto')
c.setFillColor(AM);c.setFont('PB',22);c.drawRightString(W-M,H-55,'COTIZACIÓN')
c.setFillColor(white);c.setFont('PR',10);c.drawRightString(W-M,H-75,'N° 2026-1013-01  ·  13 de octubre de 2026')
c.setFillColor(AM);c.rect(0,H-116,W,6,fill=1,stroke=0)
y=H-150
c.setFillColor(GR);c.setFont('PM',9);c.drawString(M,y,'CLIENTE');c.drawString(W/2+10,y,'EMITIDA POR')
c.setFillColor(CAR);c.setFont('PB',13);c.drawString(M,y-18,'Siglo 21');c.setFont('PR',9.5);c.setFillColor(GR);c.drawString(M,y-34,'Atención: Sr. Rodrigo');c.setFillColor(CAR);c.setFont('PB',13);c.drawString(W/2+10,y-18,'El Señor de los Tarros SPA')
c.setFont('PR',9.5);c.setFillColor(GR)
c.drawString(W/2+10,y-34,'WhatsApp +56 9 4969 1686');c.drawString(W/2+10,y-48,'elsenordelostarros.cl')
# product block
y=H-235
c.setFillColor(LG);c.roundRect(M,y-250,W-2*M,250,10,fill=1,stroke=0)
im=ImageReader('cot/cem.jpg');iw,ih=im.getSize();hh=220;ww=hh*iw/ih
c.drawImage(im,M+4,y-240,ww,hh)
x=M+ww+14
c.setFillColor(TUR);c.setFont('PB',9);c.drawString(x,y-24,'CEM  ·  MODELO AT-9996')
c.setFillColor(CAR);c.setFont('PB',15);c.drawString(x,y-44,'Multímetro osciloscopio automotriz')
specs=['True RMS con función osciloscopio y pantalla TFT a color','14 funciones: DCV, ACV, DCA, ACA, resistencia,','  frecuencia, ciclo de trabajo, temperatura °C/°F,','  capacitancia, continuidad y diodos','RPM (tacómetro) motores 2 a 10 cilindros con captador','Ángulo de parada (dwell) · registro de datos y tendencias','CAT IV 600 V / CAT III 1000 V · IP67 (resistente al agua)']
c.setFont('PR',9.5);yy=y-66
for s in specs:
    (s.startswith(' ') or (c.setFillColor(AM),c.circle(x+3,yy+3,2.3,fill=1,stroke=0)));c.setFillColor(CAR);c.drawString(x+12,yy,s.strip());yy-=16.5
# table
y=y-285
cols=[M,M+290,M+360,M+445];hd=['Descripción','Cant.','Precio unit.','Total']
c.setFillColor(CAR);c.rect(M,y-6,W-2*M,22,fill=1,stroke=0);c.setFillColor(white);c.setFont('PB',9.5)
c.drawString(cols[0]+8,y,hd[0]);c.drawCentredString(cols[1]+35,y,hd[1]);c.drawRightString(cols[3]-8,y,hd[2]);c.drawRightString(W-M-8,y,hd[3])
y-=26;c.setFillColor(CAR);c.setFont('PR',10)
c.drawString(cols[0]+8,y,'Multímetro osciloscopio automotriz CEM AT-9996');c.drawCentredString(cols[1]+35,y,'1');c.drawRightString(cols[3]-8,y,n(218900));c.drawRightString(W-M-8,y,n(218900))
c.setStrokeColor(HexColor('#D9DEE3'));c.line(M,y-10,W-M,y-10)
neto=218900;iva=round(neto*0.19);tot=neto+iva;y-=34
for lab,v,b in [('Neto',neto,0),('IVA 19%',iva,0)]:
    c.setFont('PR',10);c.setFillColor(GR);c.drawRightString(cols[3]-8,y,lab);c.setFillColor(CAR);c.drawRightString(W-M-8,y,n(v));y-=18
y-=8;c.setFillColor(AM);c.roundRect(cols[2]-10,y-10,W-M-cols[2]+10,28,6,fill=1,stroke=0)
c.setFillColor(CAR);c.setFont('PB',12);c.drawRightString(cols[3]-8,y,'TOTAL');c.drawRightString(W-M-8,y,n(tot))
# conditions
y-=50;c.setFont('PB',10);c.drawString(M,y,'Condiciones');c.setFont('PR',9.5);c.setFillColor(GR)
for s in ['Precios en pesos chilenos, netos más IVA.','Validez de la oferta: 10 días o hasta agotar stock.','Despacho en Santiago y factura el mismo día.','Pedidos y consultas por WhatsApp +56 9 4969 1686.']:
    y-=15;c.drawString(M,y,'·  '+s)
c.setFillColor(AM);c.rect(0,0,W,34,fill=1,stroke=0);c.setFillColor(CAR);c.setFont('PB',10)
c.drawString(M,13,'El Señor de los Tarros SPA  ·  Insumos para talleres');c.drawRightString(W-M,13,'elsenordelostarros.cl')
c.save();print(neto,iva,tot)
