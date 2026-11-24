"""Genera dados-datos.js (dados sueltos clasificados) desde cotizador-datos.js.
Uso: python3 trabajo/scripts/dados_datos.py   (desde la raíz del repo)"""
import re, json
s = open('cotizador-datos.js', encoding='utf-8').read()
cat = json.loads(re.search(r'var CAT=(\[.*?\]);', s, re.S).group(1))
CUAD = {'1/4': '1/4"', '3/8': '3/8"', '1/2': '1/2"', '3/4': '3/4"', '1': '1"'}
def cuad(n):
    m = re.search(r'cuadrante\s*(?:de\s*)?(1/4|3/8|1/2|3/4|1)\s*"', n, re.I) or re.search(r'(?<![\d/])(1/4|3/8|1/2|3/4)\s*"', n) or re.search(r'(?<![\d/,.])(1)\s*"', n)
    return CUAD[m.group(1)] if m else None
def tipo(n):
    l = n.lower()
    if 'adaptador' in l and 'dado' in l and ('aumentador' in l or 'reductor' in l): return 'Adaptador'
    if 'buj' in l: return 'Bujía'
    if 'torx' in l or 'estrella' in l: return 'Torx'
    if 'multifuncional' in l: return 'Multifuncional'
    if 'allen' in l or 'imbus' in l: return 'Allen / Spline'
    if 'impacto' in l: return 'Impacto'
    if 'poligonal' in l: return 'Poligonal (12 puntas)'
    if 'hexagonal' in l or ' hex' in l: return 'Hexagonal (6 puntas)'
    return None
def medida(n, t):
    if t == 'Adaptador':
        m = re.search(r'(\d/\d|1)"?\s*F\s*-\s*(\d/\d|1)"?\s*M', n, re.I)
        return (m.group(1) + '" a ' + m.group(2) + '"') if m else None
    m = re.search(r'\b([TEMH]\d{1,3})\b', n) if t in ('Torx', 'Allen / Spline') else None
    if m: return m.group(1)
    m = re.search(r'(?<!\d)(\d{1,2}(?:[,.]\d)?)\s*mm(?!L|\))', n, re.I)
    if m: return m.group(1).replace('.', ',') + ' mm'
    r = re.sub(r'cuadrante\s*(?:de\s*)?\d/\d\s*"|(?:de\s*)?\b\d/\d"\s*(?=corto|largo|hex|x|$)', ' ', n, count=1, flags=re.I)
    m = re.search(r'(?:(\d)\s+)?(\d{1,2}/\d{1,2})\s*"', r)
    return ((m.group(1) + ' ' if m.group(1) else '') + m.group(2) + '"') if m else None
out = []
for c in cat:
    n = c[1]; l = n.lower()
    if 'dado' not in l or re.search(r'juego|jgo|juedo|set |caja|display|destornillador|llave|candado|pipa', l): continue
    t = tipo(n); q = cuad(n)
    if not t or not q: continue
    md = medida(n, t)
    if not md: continue
    largo = 1 if re.search(r'largo', l) else 0
    out.append([c[0], n, c[2], c[3], c[4], c[5], q, t, md, largo])
open('dados-datos.js', 'w', encoding='utf-8').write('var IMGPRE="https://images.jumpseller.com/store/el-senor-de-los-tarros/";\nvar DADOS=' + json.dumps(out, ensure_ascii=False) + ';\n')
from collections import Counter
print(len(out)); print(Counter((o[6], o[7]) for o in out))
