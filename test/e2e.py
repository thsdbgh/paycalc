import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
D = Path(__file__).resolve().parent.parent / "dist"
SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else D
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        for f in sorted(D.glob("*.html")):
            await pg.goto(f.as_uri())
            res = await pg.locator("#result").inner_text() if await pg.locator("#result").count() else "-"
            print(f"== {f.name}: {res.splitlines()[0] if res else 'EMPTY'}")
        # interaction test: 주휴 14h → 비대상, 
        await pg.goto((D / "juhyu.html").as_uri()); await pg.fill("#hours", "14")
        print("juhyu 14h:", (await pg.locator("#result").inner_text()).splitlines()[0])
        await pg.fill("#hourly", "10700"); await pg.fill("#hours", "40")
        print("juhyu 40h/10700:", (await pg.locator("#result").inner_text()).splitlines()[0], "| input shown:", await pg.input_value("#hourly"))
        await pg.goto((D / "alba.html").as_uri()); await pg.click("label:has(input[name=ded][value=ins])")
        print("alba ins:", (await pg.locator("#result").inner_text()).replace("\n"," | ")[:200])
        await pg.goto((D / "freelancer.html").as_uri()); await pg.click("label:has(input[name=mode][value=n])")
        print("freelancer n:", (await pg.locator("#result").inner_text()).splitlines()[0])
        for name in ("index", "juhyu", "unemployment"):
            await pg.goto((D / f"{name}.html").as_uri())
            await pg.screenshot(path=str(SHOTS / f"shot_{name}.png"), full_page=False)
        await pg.emulate_media(color_scheme="dark"); await pg.goto((D / "severance.html").as_uri())
        await pg.screenshot(path=str(SHOTS / "shot_dark.png"))
        sw = await pg.evaluate("document.documentElement.scrollWidth")
        print("scrollWidth", sw, "errors:", errs or "none")
        await b.close()
asyncio.run(main())
