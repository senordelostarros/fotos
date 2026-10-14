import asyncio,os
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':800,'height':800})
        for n in ['herramientas','repuestos','quimicos','seguridad-higiene','mister-solucion']:
            await pg.goto('file://'+D+f'/{n}.svg'); await pg.screenshot(path=D+f'/{n}.png')
        await b.close()
asyncio.run(main())
