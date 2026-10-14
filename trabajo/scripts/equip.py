import os,asyncio
D=os.path.dirname(os.path.abspath(__file__))
PAT=open(D+'/pat.b64').read()
C='#1D2126'; T='#6FC8DA'; Y='#FFC72C'; W='#FFFFFF'; G='#AAB2BC'; R='#E0473A'
S='stroke="%s" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'%C
ic=f'''
<!-- carro de taller -->
<g transform="translate(110,500)">
<rect x="0" y="0" width="230" height="40" rx="8" fill="{G}" {S}/>
<rect x="10" y="40" width="210" height="190" rx="10" fill="{R}" {S}/>
<rect x="28" y="58" width="174" height="38" rx="6" fill="{R}" {S}/><rect x="85" y="72" width="60" height="10" rx="4" fill="{G}"/>
<rect x="28" y="106" width="174" height="38" rx="6" fill="{R}" {S}/><rect x="85" y="120" width="60" height="10" rx="4" fill="{G}"/>
<rect x="28" y="154" width="174" height="58" rx="6" fill="{R}" {S}/><rect x="85" y="176" width="60" height="10" rx="4" fill="{G}"/>
<circle cx="45" cy="250" r="20" fill="{C}" stroke="{W}" stroke-width="5"/><circle cx="185" cy="250" r="20" fill="{C}" stroke="{W}" stroke-width="5"/></g>
<!-- gata hidraulica -->
<g transform="translate(360,640)">
<rect x="0" y="70" width="230" height="44" rx="12" fill="{Y}" {S}/>
<path d="M150 72 L70 0" stroke="{C}" stroke-width="30" stroke-linecap="round"/><path d="M150 72 L70 0" stroke="{Y}" stroke-width="16" stroke-linecap="round"/>
<rect x="40" y="-22" width="62" height="18" rx="6" fill="{G}" {S}/>
<path d="M210 80 L270 -10" stroke="{G}" stroke-width="14" stroke-linecap="round"/><path d="M210 80 L270 -10" stroke="{C}" stroke-width="4" stroke-linecap="round" opacity="0.4"/>
<circle cx="30" cy="124" r="16" fill="{C}" stroke="{W}" stroke-width="5"/><circle cx="200" cy="124" r="16" fill="{C}" stroke="{W}" stroke-width="5"/></g>
<!-- lampara de trabajo -->
<g transform="translate(650,520) rotate(10) scale(0.9)">
<rect x="20" y="0" width="70" height="170" rx="20" fill="{C}" stroke="{W}" stroke-width="6"/>
<rect x="34" y="16" width="42" height="120" rx="10" fill="#FFF3C4"/>
<rect x="34" y="16" width="42" height="120" rx="10" fill="{Y}" opacity="0.55"/>
<rect x="30" y="168" width="50" height="60" rx="10" fill="{T}" {S}/>
<path d="M55 0 v-30 q0 -20 20 -20" fill="none" stroke="{G}" stroke-width="8" stroke-linecap="round"/></g>'''
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
<rect width="800" height="800" fill="{C}"/>
<image href="data:image/png;base64,{PAT}" width="800" height="800" opacity="0.13"/>
<ellipse cx="400" cy="900" rx="520" ry="330" fill="{T}"/>
<rect x="0" y="784" width="800" height="16" fill="{Y}"/>{ic}</svg>'''
open(D+'/equipamiento.svg','w').write(svg)
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':800,'height':800})
        await pg.goto('file://'+D+'/equipamiento.svg'); await pg.screenshot(path=D+'/equipamiento.png'); await b.close()
asyncio.run(main())
