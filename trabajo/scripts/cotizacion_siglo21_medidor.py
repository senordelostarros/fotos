from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
W,H=A4; C=HexColor('#1D2126'); Y=HexColor('#FFC72C'); T=HexColor('#6FC8DA'); G=HexColor('#5b646d'); L=HexColor('#e3e7eb')
out='trabajo/cotizaciones/Cotizacion_Siglo21_Medidor_Frenos_24nov2026.pdf'
c=canvas.Canvas(out,pagesize=A4); c.setTitle('Cotización Siglo 21 - Medidor de desgaste de frenos')
def cl(v): return '$'+f'{round(v):,}'.replace(',','.')
# encabezado
c.setFillColor(C); c.rect(0,H-120,W,120,fill=1,stroke=0)
logo=ImageReader('trabajo/marca/logo-encabezado-ancho-v2.jpg'); iw,ih=logo.getSize(); lh=44; c.drawImage(logo,36,H-82,width=lh*iw/ih,height=lh)
c.setFillColor(Y); c.setFont('Helvetica-Bold',22); c.drawRightString(W-36,H-58,'COTIZACIÓN')
c.setFillColor(white); c.setFont('Helvetica',10); c.drawRightString(W-36,H-76,'N° 2026-1124-01'); c.drawRightString(W-36,H-90,'Fecha: 24 de noviembre de 2026')
c.setFillColor(T); c.rect(0,H-126,W,6,fill=1,stroke=0)
# cliente
y=H-160; c.setFillColor(C); c.setFont('Helvetica-Bold',11); c.drawString(36,y,'Señores:')
c.setFont('Helvetica',10)
for i,t in enumerate(['Comercial Automotriz Siglo XXI Ltda.','RUT 78.770.630-4','Bellavista 0170','Atención: Sr. Rodrigo Arriagada']): c.drawString(36,y-15-14*i,t)
c.setFont('Helvetica-Bold',11); c.drawString(330,y,'De:'); c.setFont('Helvetica',10)
for i,t in enumerate(['El Señor de los Tarros SPA','Renato González Madrid','WhatsApp +56 9 4969 1686','elsenordelostarros.cl']): c.drawString(330,y-15-14*i,t)
# tabla
y=H-250; c.setFillColor(C); c.rect(36,y,W-72,24,fill=1,stroke=0); c.setFillColor(white); c.setFont('Helvetica-Bold',10)
cols=[(46,'Código'),(120,'Descripción'),(360,'Cant.'),(410,'P. unitario'),(495,'Total')]
for x,t in cols: c.drawString(x,y+8,t)
y-=230; c.setStrokeColor(L); c.setFillColor(HexColor('#ffffff')); c.rect(36,y,W-72,230,fill=1,stroke=1); y+=80
img=ImageReader('ms2-medidor-de-desgaste-de-frenos.jpg'); c.drawImage(img,150,y-76,width=104,height=104,mask='auto')
c.setFillColor(C); c.setFont('Helvetica-Bold',10); c.drawString(46,y+126,'MDF8H')
c.drawString(120,y+126,'Medidor de desgaste de pastillas de freno')
c.setFont('Helvetica',9); c.setFillColor(G)
for i,t in enumerate(['• 8 láminas: 2, 3, 4, 5, 6, 8, 10 y 12 mm','• Código de colores: rojo = cambiar,','   amarillo = revisar pronto, verde = OK','• Mide el espesor de la pastilla sin','   desmontar la rueda','• Láminas de aluminio con remache central']): c.drawString(120,y+108-13*i,t)
c.setFillColor(C); c.setFont('Helvetica',10); c.drawString(368,y+126,'1'); c.drawString(410,y+126,cl(18900)); c.drawString(495,y+126,cl(18900))
# totales
y-=160; neto=18900; iva=round(neto*0.19)
for i,(k,v) in enumerate([('Neto',neto),('IVA 19%',iva)]):
    c.setFont('Helvetica',10); c.setFillColor(C); c.drawString(400,y+50-16*i,k); c.drawRightString(W-46,y+50-16*i,cl(v))
c.setFillColor(Y); c.rect(390,y-4,W-426,26,fill=1,stroke=0); c.setFillColor(C); c.setFont('Helvetica-Bold',12); c.drawString(400,y+5,'TOTAL'); c.drawRightString(W-46,y+5,cl(neto+iva))
# condiciones
y-=50; c.setFont('Helvetica-Bold',11); c.drawString(36,y,'Condiciones'); c.setFont('Helvetica',9.5); c.setFillColor(G)
for i,t in enumerate(['• Precios netos en pesos chilenos; se agrega IVA 19%. Emitimos factura.','• Validez de la cotización: 15 días.','• Despacho en 24 horas. Sin costo dentro de Américo Vespucio en compras sobre $50.000 + IVA.','• Sujeto a disponibilidad de stock al momento de confirmar.']): c.drawString(36,y-16-14*i,t)
# pie
c.setFillColor(C); c.rect(0,0,W,46,fill=1,stroke=0); c.setFillColor(white); c.setFont('Helvetica-Bold',10)
c.drawCentredString(W/2,26,'El Señor de los Tarros SPA · Insumos para talleres automotrices e industria'); c.setFillColor(Y); c.setFont('Helvetica',9); c.drawCentredString(W/2,12,'WhatsApp +56 9 4969 1686 · elsenordelostarros.cl')
c.save(); print(out)
