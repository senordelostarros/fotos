import re,json,csv,collections,unicodedata
def norm(t): return unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
R=[ # (categoria, subcategoria, regex sobre nombre)
('Herramientas Manuales','Herramientas Aisladas 1000 V',r'aislad(o|a|os|as)\b|vde|1000 ?v'),
('Taller Automotriz','Levante',r'gata|tecle|banquillo'),
('Taller Automotriz','Lubricación y Fluidos',r'saca ?filtro|llave (de|para) filtro|filtro de aceite|llave de filtro'),
('Taller Automotriz','Neumáticos y Ruedas',r'(desmontar|valvula para|valvula de|presion de|porta|llave de) neumatic|neumatico tubular|neumaticos\b|infla|plomo|parche|vulcaniz|profundimetro|llave de rueda|llave cruz'),
('Taller Automotriz','Electricidad Automotriz',r'cinta (electrica|aislante|aisladora)|huincha aisladora|cargador (partidor|para ?baterias|de baterias)|partidor|roba corriente|cable (de|para) (bateria|partida|puente)|fusible|bornes|terminal'),
('Herramientas Eléctricas e Inalámbricas',None,r'bateria.*(litio|ion|\dah)|cargador .*\d+ ?v'),
('Abrasivos y Accesorios',None,r'escobilla|disco|lija|broca|fresa|piedra copa|sierra copa|hoja(s)? de sierra|grata|mandril|afilador'),
('Herramientas Neumáticas y Aire',None,r'neumatic[oa](?!s)'),
('Herramientas Manuales','Alicates y Tenazas',r'alicate|saca seguro|tenaza'),
('Herramientas Manuales','Llaves',r'^llave|^juego de llaves|llaves '),
('Taller Automotriz','Diagnóstico y Medición',r'probador|medidor|tester|comprobador'),
('Químicos',None,r'senfineco|spray|aerosol|lubricante|grasa |grasa$|aceite (para|de motor|hidraul|2t|4t)|silicona|sellador|adhesivo|pegamento|traba ?pernos|desengras|limpia(dor)? (de )?(contactos|frenos|carbur|inyect|motor|tapiz|vidrio|llanta)|refrigerante|anticongelante|liquido de frenos|liquido frenos|dot ?[34]|aditivo|cemento vulcanizador|pintura|shampoo|cera |abrillantador|renovador|desoxidante|wd-?40|super glue|epoxi|reinzosil|loctite|motor ?flush|anti ?humo|antichirrido'),
('Desabolladura y Pintura',None,r'desabolla|porto ?power|mordaza de tiro|lima carrocer|pistola de pintar|pistola de pintura|calderin|aplicador(es)? de masilla|masilla|taco lijador|hojalatero|ventosa|cuna (para )?desabollar|pistola selladora|pistola de secado'),
('Iluminación',None,r'linterna|lampara|foco |reflector|minilinterna|ampolleta'),
('Seguridad e Higiene','Ropa y Calzado de Trabajo',r'chaqueta|overol|pantalon|buzo|zapato|bota|calzado|chaleco|jardinera|polera|polar|traje'),
('Seguridad e Higiene','Guantes',r'guante'),
('Seguridad e Higiene','Protección Personal',r'mascara|careta|lente(s)? de seguridad|antiparra|protector (auditivo|facial)|mascarilla|respirador|casco|arnes|tapon(es)? (auditivo|de oido)|fonos'),
('Seguridad e Higiene','Limpieza e Higiene',r'pano|papel|toalla|tork|wypall|absorbente|escoba|basurero|dispensador|jabon|guaipe|huaipe'),
('Seguridad e Higiene','Señalización y Seguridad',r'candado|cono|cinta reflectante|extintor|alarma|senaliz|botiquin|cadena de seguridad'),
('Carros y Almacenaje',None,r'carro|caja (para|de) herramienta|caja metalica|caja plastica|organizador|maleta (vacia|plastica|metalica|para herramienta)|bolso|mochila|porta herramienta|estante|banco de trabajo|tablero|panel perforado|cajonera|porta notebook|alfombra de trabajo'),
('Herramientas Eléctricas e Inalámbricas',None,r'taladro|atornillador (inalambrico|electrico)|esmeril|amoladora|rotomartillo|demoledor|sierra (circular|caladora|electrica|sable)|caladora|lijadora (electrica|orbital)|pulidora|rectificador|bateria( de| li| \d)|cargador|inalambric|soldadora|cautin|pistola de calor|pistola de silicona|aspiradora|hidrolavadora|generador|\d+ ?w(att)?\b'),
('Herramientas Neumáticas y Aire',None,r'compresor (de aire|\d)|manguera|acople|enchufe rapido|cachimba|pistola (de aire|sopladora|para inflar|infladora|de impacto)|llave de impacto|chicharra neumatica|engrasadora|pulverizador|enrollador|regulador de presion|filtro de aire|lubricador|conector rapido'),
('Abrasivos y Accesorios',None,r'disco|lija|broca|escobilla|fresa|piedra (de esmeril|abrasiva)|copa|sierra copa|hoja de sierra|hojas de sierra|punta(s)? (de|para) atornillar|bit(s)?\b|cincel sds|mandril|portabrocas|afilador'),
('Taller Automotriz','Levante',r'gata|tecle|banquillo|soporte (o banquillo|para eje|de motor)|elevador|grua|pluma|camilla|plataforma rodante|mesa elevadora'),
('Taller Automotriz','Diagnóstico y Medición',r'compresimetro|vacu?ometro|multimetro|tester|probador|scanner|escaner|obd|estroboscop|manometro|medidor|calibrador|pie de metro|micrometro|torquimetro|llave de torque|llave dinamometrica|torque|feeler|lamina|estetoscopio|regla de luz|reloj comparador|nivel|flexometro|huincha (de medir|metrica)|termometro|endoscopio|densimetro|refractometro'),
('Taller Automotriz','Frenos',r'freno|caliper|sangrado|pastilla|balata'),
('Taller Automotriz','Suspensión y Dirección',r'rotula|axial|amortiguador|resorte|mcpherson|terminal de direccion|buje|suspension|direccion'),
('Taller Automotriz','Neumáticos y Ruedas',r'neumatico|rueda|llanta|valvula de neumatico|plomo|parche|vulcaniz|desmontador de neumat|infla|profundimetro|llave de rueda|llave cruz'),
('Taller Automotriz','Lubricación y Fluidos',r'embudo'),
('Taller Automotriz','Motor y Distribución',r'arbol de levas|motor|distribucion|valvula|piston|anillo|biela|culata|cigue|inyector|common rail|bujia|filtro|correa|cadena de distribucion|bruñidor|brunidor|carter|asentador|retenes|reten'),
('Taller Automotriz','Lubricación y Fluidos',r'aceite|embudo|jeringa|recogedor|aspirador de aceite|recuperador|bomba (de|para) (aceite|grasa|trasvasije)|aceitera|bidon|jarro|trasvasije|llenado|tambor'),
('Taller Automotriz','Electricidad Automotriz',r'bateria|cable (de|para) (bateria|partida|puente)|pinza (de|para) bateria|fusible|terminal|electric|arrancador|partidor|relay|rele'),
('Taller Automotriz','Extractores y Prensas',r'extractor|prensa|saca|separador|desmontador|removedor|compresor de (resorte|valvula)'),
('Fijación y Sujeción',None,r'tornillo|perno|tuerca|golilla|arandela|remach|abrazadera|amarra|seguro|chaveta|prisionero|tarugo|clavo|grapa|corchete|sujecion|prensa en c|sargento|tornillo de banco|morsa|cinta (aislante|aisladora|de embalar|teflon|doble)|huincha aisladora|teflon|o-?ring|surtido'),
('Herramientas Manuales','Dados y Chicharras',r'dado|chicharra|barrote|mango (articulado|de fuerza)|extension|junta cardan|adaptador (de|para)? ?(impacto|dado|cuadrante)|cuadrante|carraca|trinquete'),
('Herramientas Manuales','Llaves',r'llave|allen|torx|hexagonal'),
('Herramientas Manuales','Alicates y Tenazas',r'alicate|tenaza|pinza|tijera|cortafrio|cortador|napoleon|pela ?cable|cortacable|crimpa|ponchadora'),
('Herramientas Manuales','Destornilladores y Puntas',r'destornillador|atornillador|punta'),
('Herramientas Manuales','Martillos y Combos',r'martillo|combo|maceta|mazo|cincel|punzon|botador|corta ?fierro|marcador de golpe'),
('Herramientas Manuales','Corte y Medición',r'sierra|serrucho|arco|cuchillo|cuchilla|cartonero|escuadra|lima|raspador|espatula|machos|terraja'),
('Herramientas Manuales','Juegos y Maletas',r'juego|set|maleta|kit|estuche'),
]
# Prioridad: herramientas manuales específicas antes que 'motor' etc.? reordenamos al evaluar
ORDER=['Químicos','Desabolladura y Pintura','Iluminación','Seguridad e Higiene','Carros y Almacenaje','Herramientas Eléctricas e Inalámbricas','Herramientas Neumáticas y Aire','Taller Automotriz','Abrasivos y Accesorios','Fijación y Sujeción','Herramientas Manuales']
def clasificar(name,oldcat=''):
    n=norm(name)
    for c,s,rx in R:
        if re.search(rx,n): return c,s
    o=norm(oldcat)
    if 'repuesto' in o: return 'Repuestos',None
    if 'quimic' in o: return 'Químicos',None
    if 'seguridad' in o: return 'Seguridad e Higiene',None
    if 'fijacion' in o: return 'Fijación y Sujeción',None
    return 'Herramientas Manuales','Otras herramientas'
