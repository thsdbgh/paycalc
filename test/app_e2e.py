# 사장님 앱 E2E: 로컬 wrangler dev(8787) 대상
import asyncio, sys, time
from playwright.async_api import async_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8787"
SHOT = sys.argv[2] if len(sys.argv) > 2 else "."
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        email = f"e2e{int(time.time())}@example.com"
        await pg.goto(BASE + "/app/#signup")
        await pg.fill("#em", email); await pg.fill("#pw", "testpass123"); await pg.check("#agree")
        await pg.click("#authf button[type=submit]"); await pg.wait_for_selector("#ef")
        print("signup → staff form OK")
        await pg.goto(BASE + "/app/#settings"); await pg.wait_for_selector("#bf")
        await pg.fill("#b-name", "하늘카페"); await pg.fill("#b-ceo", "홍길동"); await pg.click("#bf button[type=submit]"); await pg.wait_for_timeout(600)
        await pg.goto(BASE + "/app/#staff"); await pg.wait_for_selector("#ef")
        await pg.fill("#f-name", "김하늘"); await pg.fill("#f-birth", "2001-03-14"); await pg.fill("#f-hourly", "10500"); await pg.fill("#f-weekly", "20")
        await pg.select_option("#f-ded", "33"); await pg.click("#ef button[type=submit]"); await pg.wait_for_timeout(800)
        await pg.fill("#f-name", "이준호"); await pg.fill("#f-hourly", "10320"); await pg.fill("#f-weekly", "40"); await pg.select_option("#f-ded", "ins")
        await pg.click("#ef button[type=submit]"); await pg.wait_for_timeout(800)
        upsell = await pg.locator(".upsell").count()
        print("2 employees added, limit card shown:", upsell > 0)
        # 김하늘 2026-10: 월~목 10:00-15:30 휴게 30
        await pg.goto(BASE + "/app/#home"); await pg.wait_for_selector(".emp-card")
        href = await pg.locator(".emp-card").first.get_attribute("href")
        await pg.goto(BASE + "/app/" + href)
        await pg.wait_for_selector("#days")
        # 월 이동: 현재월 → 2026-10
        for _ in range(12):
            t = await pg.locator(".monthbar b").inner_text()
            if t.startswith("2026년 10월"): break
            await pg.click("[data-mv='-1']" if t > "2026년 10월" else "[data-mv='1']"); await pg.wait_for_selector("#days")
        await pg.click(".pattern summary")
        for i in ["4"]: await pg.uncheck(f".pattern .wd input[value='{i}']", force=True)
        await pg.fill("#pst", "10:00"); await pg.fill("#pen", "15:30"); await pg.fill("#pbr", "30")
        await pg.click("#pfill"); await pg.click("#save"); await pg.wait_for_timeout(1200)
        print("sum:", (await pg.locator("#sum").inner_text()).replace("\n", " "))
        await pg.click("#slipbtn"); await pg.wait_for_selector(".slip")
        slip = (await pg.locator(".slip").inner_text()).replace("\n", " | ")
        print("slip:", slip[:400])
        await pg.locator(".slip").screenshot(path=f"{SHOT}/app_slip.png")
        link = await pg.input_value("#lnk"); print("share link:", link[:60] + "…")
        p2 = await (await b.new_context(viewport={"width": 390, "height": 844})).new_page()
        await p2.goto(link); await p2.wait_for_selector(".slip")
        print("employee view:", (await p2.locator(".slip .pay").inner_text()).replace("\n", " "))
        await pg.goto(BASE + "/app/#home"); await pg.wait_for_selector(".emp-card")
        await pg.screenshot(path=f"{SHOT}/app_home.png")
        print("home width:", await pg.evaluate("document.documentElement.scrollWidth"))
        await pg.goto(BASE + "/app/" + href); await pg.wait_for_selector("#days")
        await pg.screenshot(path=f"{SHOT}/app_emp.png")
        print("emp width:", await pg.evaluate("document.documentElement.scrollWidth"), "errors:", errs or "none")
        await b.close()
asyncio.run(main())
