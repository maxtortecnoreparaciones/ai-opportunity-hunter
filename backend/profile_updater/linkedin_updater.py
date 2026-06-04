from playwright.async_api import Page
from backend.auth.session import SessionStorage
from backend.profile_updater.updater import BaseProfileUpdater, ProfileData


class LinkedInProfileUpdater(BaseProfileUpdater):
    PROFILE_URL = "https://www.linkedin.com/in/johan-poveda-788760263"
    EDIT_URL = "https://www.linkedin.com/in/johan-poveda-788760263/edit"

    def __init__(self):
        self.session = SessionStorage("linkedin")
        self.cookies = None

    async def with_browser(self):
        from playwright.async_api import async_playwright
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=False, channel="chrome")
        context = await browser.new_context()
        if self.cookies:
            await context.add_cookies(self.cookies)
        return pw, browser, context

    async def login(self) -> bool:
        stored = self.session.load()
        if not stored:
            print("[LinkedInUpdater] No hay sesion guardada")
            return False
        self.cookies = stored.get("cookies", [])
        if not self.cookies:
            print("[LinkedInUpdater] No hay cookies en la sesion")
            return False
        return True

    async def update_profile(self, data: ProfileData) -> bool:
        ok = await self.login()
        if not ok:
            return False

        pw, browser, context = await self.with_browser()
        page = await context.new_page()

        try:
            await page.goto(self.EDIT_URL, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)

            captcha_ok = await self._handle_captcha(page)
            if not captcha_ok:
                print("[LinkedInUpdater] CAPTCHA detectado, abortando")
                return False

            if data.headline:
                await self._update_field(page, "input[name='headline']", data.headline)
            if data.about:
                await self._update_field(page, "textarea[name='about']", data.about)
            if data.skills:
                for skill in data.skills:
                    await self._add_skill(page, skill)
                    await page.wait_for_timeout(1000)

            await self._save(page)
            print("[LinkedInUpdater] Perfil actualizado correctamente")
            return True
        finally:
            await browser.close()
            await pw.stop()

    async def _update_field(self, page: Page, selector: str, value: str):
        try:
            el = await page.wait_for_selector(selector, timeout=5000)
            if el:
                await el.fill("")
                await el.fill(value)
                print(f"[LinkedInUpdater] Campo actualizado: {selector}")
        except Exception:
            print(f"[LinkedInUpdater] No se pudo actualizar: {selector}")

    async def _add_skill(self, page: Page, skill: str):
        try:
            input_el = await page.wait_for_selector(
                "input[placeholder*='skill']",
                timeout=3000,
            )
            if input_el:
                await input_el.fill(skill)
                await page.keyboard.press("Enter")
        except Exception:
            pass

    async def _save(self, page: Page):
        try:
            btn = await page.query_selector("button[data-control-name='save']")
            if btn:
                await btn.click()
        except Exception:
            pass
