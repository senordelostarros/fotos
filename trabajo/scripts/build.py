import os
D=os.path.dirname(os.path.abspath(__file__))
PAT=open(D+'/pat.b64').read()
C='#1D2126'; T='#6FC8DA'; Y='#FFC72C'; W='#FFFFFF'; G='#AAB2BC'; R='#E0473A'
S='stroke="%s" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'%C
def base(icons):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="800" height="800" viewBox="0 0 800 800">
<rect width="800" height="800" fill="{C}"/>
<image href="data:image/png;base64,{PAT}" width="800" height="800" opacity="0.13"/>
<ellipse cx="400" cy="900" rx="520" ry="330" fill="{T}"/>
<rect x="0" y="784" width="800" height="16" fill="{Y}"/>
<g transform="translate(0,0)">{icons}</g></svg>'''
rep=f'''
<!-- bateria -->
<g transform="translate(120,600)"><rect x="0" y="30" width="230" height="160" rx="12" fill="{C}" stroke="{W}" stroke-width="6"/><rect x="0" y="30" width="230" height="40" rx="12" fill="{Y}" {S}/><rect x="30" y="8" width="34" height="24" rx="4" fill="{G}" {S}/><rect x="166" y="8" width="34" height="24" rx="4" fill="{G}" {S}/><path d="M80 120 h30 M95 105 v30 M140 120 h30" stroke="{W}" stroke-width="8" stroke-linecap="round"/></g>
<!-- plumilla -->
<g transform="translate(560,760) rotate(-8) scale(0.6)"><rect x="0" y="0" width="330" height="22" rx="8" fill="{C}"/><rect x="10" y="22" width="310" height="12" rx="4" fill="{G}" {S}/><rect x="140" y="-30" width="40" height="34" rx="6" fill="{Y}" {S}/></g>
<!-- ampolleta H7 -->
<g transform="translate(400,540) scale(0.92)">
<rect x="45" y="0" width="70" height="140" rx="35" fill="#EAF7FA" {S}/>
<rect x="68" y="30" width="24" height="70" rx="6" fill="{Y}" opacity="0.9"/>
<rect x="25" y="138" width="110" height="26" rx="6" fill="{G}" {S}/>
<rect x="45" y="164" width="70" height="56" rx="8" fill="{C}" stroke="{W}" stroke-width="4"/>
<rect x="60" y="220" width="10" height="34" fill="{G}"/><rect x="90" y="220" width="10" height="34" fill="{G}"/></g>'''
qui=f'''
<!-- tarro grande -->
<g transform="translate(150,560)"><rect x="0" y="20" width="170" height="200" rx="14" fill="{C}" stroke="{W}" stroke-width="6"/><rect x="0" y="80" width="170" height="70" fill="{Y}"/><ellipse cx="85" cy="20" rx="85" ry="18" fill="{G}" {S}/><rect x="130" y="-8" width="26" height="22" rx="4" fill="{G}" {S}/></g>
<!-- spray -->
<g transform="translate(360,520)"><rect x="0" y="60" width="100" height="200" rx="22" fill="{Y}" {S}/><rect x="0" y="150" width="100" height="70" fill="{C}"/><rect x="25" y="18" width="50" height="46" rx="10" fill="{W}" {S}/><rect x="40" y="0" width="40" height="22" rx="6" fill="{R}" {S}/></g>
<!-- botella -->
<g transform="translate(505,555) scale(0.92)"><path d="M55 0 h40 v40 l30 40 v170 a14 14 0 0 1 -14 14 h-72 a14 14 0 0 1 -14 -14 v-170 l30 -40 z" fill="{W}" {S}/><rect x="25" y="120" width="100" height="70" fill="{R}"/><rect x="45" y="140" width="60" height="8" fill="{W}"/><rect x="45" y="160" width="40" height="8" fill="{W}"/><rect x="52" y="-14" width="46" height="20" rx="5" fill="{Y}" {S}/></g>'''
seg=f'''
<!-- rollo papel -->
<g transform="translate(130,560)"><rect x="0" y="20" width="190" height="200" rx="12" fill="{W}" {S}/><ellipse cx="95" cy="20" rx="95" ry="26" fill="#EEF3F5" {S}/><ellipse cx="95" cy="20" rx="30" ry="9" fill="{G}" {S}/><rect x="0" y="120" width="190" height="34" fill="{T}" opacity="0.7"/></g>
<!-- guante -->
<g transform="translate(375,545) scale(0.8)"><path d="M40 300 v-130 l-30 -40 a20 20 0 0 1 32 -24 l18 22 v-110 a20 20 0 0 1 40 0 v90 v-110 a20 20 0 0 1 40 0 v110 v-95 a20 20 0 0 1 40 0 v100 v-70 a20 20 0 0 1 40 0 v160 q0 60 -40 97 v0 z" fill="#4FA8D8" {S}/><rect x="40" y="270" width="155" height="40" rx="8" fill="{Y}" {S}/></g>
<!-- lentes -->
<g transform="translate(560,640)"><path d="M0 20 q0 -22 22 -22 h60 q22 0 22 22 v24 q0 30 -30 30 h-44 q-30 0 -30 -30z" fill="#BFE8F1" {S}/><path d="M120 20 q0 -22 22 -22 h60 q22 0 22 22 v24 q0 30 -30 30 h-44 q-30 0 -30 -30z" fill="#BFE8F1" {S}/><path d="M104 22 q8 -10 16 0" fill="none" {S}/></g>'''
mis=f'''
<!-- caja herramientas -->
<g transform="translate(220,580) scale(0.92)"><path d="M140 40 v-36 h120 v36" fill="none" stroke="{C}" stroke-width="16" stroke-linejoin="round"/><rect x="0" y="40" width="400" height="190" rx="18" fill="{Y}" {S}/><rect x="0" y="100" width="400" height="22" fill="{C}"/><rect x="170" y="88" width="60" height="46" rx="8" fill="{G}" {S}/></g>
<!-- llave -->
<g transform="translate(120,640) rotate(-30) scale(0.85)"><rect x="0" y="0" width="210" height="34" rx="12" fill="{G}" {S}/><path d="M200 -22 a48 48 0 1 1 0 78 l0 -22 h28 v-34 h-28 z" fill="{G}" {S}/></g>
<!-- check -->
<g transform="translate(590,540) scale(0.85)"><circle cx="60" cy="60" r="62" fill="{T}" stroke="{W}" stroke-width="8"/><path d="M30 62 l22 22 l40 -46" fill="none" stroke="{C}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></g>'''
her=f'''
<!-- destornillador -->
<g transform="translate(70,700) rotate(-35) scale(0.9)"><rect x="0" y="0" width="120" height="44" rx="18" fill="{Y}" {S}/><rect x="0" y="12" width="120" height="8" fill="{C}"/><rect x="118" y="14" width="150" height="16" fill="{G}" {S}/><path d="M266 12 l22 10 l-22 10z" fill="{G}" {S}/></g>
<!-- chicharra -->
<g transform="translate(250,680) rotate(-12) scale(0.85)"><rect x="60" y="20" width="230" height="40" rx="16" fill="{G}" {S}/><rect x="190" y="18" width="100" height="44" rx="16" fill="{C}"/><circle cx="50" cy="40" r="50" fill="{G}" {S}/><circle cx="50" cy="40" r="18" fill="{C}"/></g>
<!-- dados -->
<g transform="translate(560,640)"><rect x="0" y="40" width="70" height="100" rx="10" fill="{G}" {S}/><rect x="14" y="40" width="42" height="18" fill="{C}"/><rect x="90" y="10" width="90" height="130" rx="12" fill="{T}" {S}/><rect x="108" y="10" width="54" height="22" fill="{C}"/></g>'''
for n,ic in [('herramientas',her),('repuestos',rep),('quimicos',qui),('seguridad-higiene',seg),('mister-solucion',mis)]:
    open(f'{D}/{n}.svg','w').write(base(ic))
print('ok')
