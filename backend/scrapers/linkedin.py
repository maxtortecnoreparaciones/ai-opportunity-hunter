import random
import logging
from datetime import datetime
from playwright.async_api import Page
from backend.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

JOB_CARD = "div.job-search-card"
TITLE = "h3.base-search-card__title"
LINK = "a.base-card__full-link"
COMPANY = "h4.base-search-card__subtitle"
LOCATION = "div.base-search-card__metadata"
DESC = "div.show-more-less-html__markup"


class LinkedInScraper(BaseScraper):
    platform_for_auth = "linkedin"

    @property
    def fuente(self) -> str:
        return "linkedin"

    async def scrape_keyword(self, keyword: str) -> list[dict]:
        results: list[dict] = []
        pw, browser, context = await self.with_browser()
        page = await context.new_page()
        page.set_default_timeout(30000)

        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            logger.info(f"Navegando a: {url}")
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(random.randint(3000, 5000))

            await self._close_modal(page)

            cards = await page.query_selector_all(JOB_CARD)
            if not cards:
                logger.warning("No se encontraron tarjetas de trabajo")
                fname = f"data/linkedin_debug_{datetime.now():%Y%m%d_%H%M%S}.png"
                await page.screenshot(path=fname)
                logger.info(f"Screenshot guardado: {fname}")
                return results

            logger.info(f"Encontradas {len(cards)} tarjetas")
            cards = cards[:15]

            for card in cards:
                try:
                    await page.evaluate("(el) => el.scrollIntoView({block: 'center'})", card)
                    await page.wait_for_timeout(500)
                    await card.click()
                    await page.wait_for_timeout(random.randint(1500, 2500))
                    data = await self._extract_job_data(page, card)
                    if data and data.get("link"):
                        results.append(data)
                except Exception as e:
                    logger.debug(f"Error extrayendo tarjeta: {e}")
                    continue
        finally:
            await browser.close()
            await pw.stop()

        return results

    async def _close_modal(self, page: Page):
        """Cierra el modal de login/registro que LinkedIn muestra a usuarios no autenticados."""
        try:
            close_btn = await page.query_selector(
                "button[aria-label='Dismiss'], "
                "button.modal__dismiss, "
                "button[data-control-name='auth_modal_dismiss'], "
                ".modal__overlay ~ button, "
                "button[action='dismiss']"
            )
            if close_btn:
                await close_btn.click()
                await page.wait_for_timeout(1000)
                logger.info("Modal de LinkedIn cerrado")
        except Exception:
            pass

        # Cerrar por ESC si el modal sigue presente
        try:
            modal = await page.query_selector(".modal__overlay--visible")
            if modal:
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(1000)
        except Exception:
            pass

    async def _extract_job_data(self, page: Page, card) -> dict | None:
        result: dict = {
            "fuente": self.fuente,
            "link": "",
            "empresa": "",
            "cargo": "",
            "ubicacion": "",
            "descripcion": "",
        }

        link_el = await card.query_selector(LINK)
        if link_el:
            link = await link_el.get_attribute("href")
            result["link"] = link.split("?")[0] if link and "?" in link else link or ""

        title_el = await card.query_selector(TITLE)
        if title_el:
            result["cargo"] = (await title_el.inner_text()).strip()

        company_el = await card.query_selector(COMPANY)
        if company_el:
            text = (await company_el.inner_text()).strip()
            result["empresa"] = text.split("\n")[0].strip()

        loc_el = await card.query_selector(LOCATION)
        if loc_el:
            text = (await loc_el.inner_text()).strip()
            parts = text.split("\n")
            result["ubicacion"] = parts[0].strip()

        if not result["cargo"] and not result["link"]:
            return None

        try:
            desc_el = await page.wait_for_selector(DESC, timeout=3000)
            if desc_el:
                result["descripcion"] = (await desc_el.inner_text()).strip()
        except Exception:
            pass

        return result
