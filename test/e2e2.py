import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
D = Path(__file__).resolve().parent.parent / "dist"; S = Path(sys.argv[1])
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        first = lambda t: t.splitlines()[0] if t else "EMPTY"
        for f in sorted(D.glob("*.html")):
            await pg.goto(f.as_uri())
            if await pg.locator("#result").count():
                t = await pg.locator("#result").inner_text()
                if not t.strip() or "확인해 주세요" in t: print("!! bad result", f.name, t[:80])
        print("all pages loaded")
        await pg.goto((D/"salary.html").as_uri()); print("salary 4000:", first(await pg.locator("#result").inner_text()))
        await pg.select_option("#family", "4"); await pg.select_option("#kids", "2"); print("4인 자녀2:", first(await pg.locator("#result").inner_text()))
        await pg.click("label:has(input[name=mode][value=n])"); await pg.fill("#amt", "3000000"); print("역산 300만:", first(await pg.locator("#result").inner_text()))
        await pg.goto((D/"labor-cost.html").as_uri()); print("인건비 250:", first(await pg.locator("#result").inner_text()))
        await pg.click("label:has(input[name=mode][value=h])"); await pg.fill("#pay", "10320"); await pg.fill("#hours", "12")
        print("인건비 알바12h:", (await pg.locator("#result").inner_text()).replace("\n"," | ")[:220])
        await pg.goto((D/"payslip.html").as_uri()); await pg.fill("#biz", "테스트상회")
        await pg.goto((D/"payslip.html").as_uri()); print("명세서 기억:", await pg.input_value("#biz"))
        print("명세서:", (await pg.locator("#slip").inner_text()).replace("\n"," | ")[:300])
        await pg.locator("#slip").screenshot(path=str(S/"shot_slip.png"))
        await pg.emulate_media(media="print"); await pg.screenshot(path=str(S/"shot_print.png")); await pg.emulate_media(media="screen")
        await pg.goto((D/"salary-4000.html").as_uri()); await pg.screenshot(path=str(S/"shot_s4000.png"), full_page=True)
        await pg.goto((D/"salary-table.html").as_uri())
        print("scrollWidth", await pg.evaluate("document.documentElement.scrollWidth"), "errors:", errs or "none")
        await b.close()
asyncio.run(main())
