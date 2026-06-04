import random
import logging
from datetime import datetime
from playwright.async_api import Page
from backend.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

# LinkedIn cambia sus selectores frecuentemente.
# Estrategias por orden de prioridad para cada campo.
JOB_CARD_SELECTORS = [
    "li[data-occludable-job-id]",           # selector clásico
    "li.jobs-search-results__job-card",     # variante 2024+
    "div.job-card-container",               # variante reciente
    "article.job-card",                     # variante article
    "[data-job-id]",                        # basado en data attr
    "li[data-job-id]",                      # otra variante
    "a.job-card-list__title",               # enlace directo en lista
]

TITLE_SELECTORS = [
    "a[data-tracking-control-name='public_jobs_jserp-result_search-card']",
    "a.job-card-list__title",
    "a[data-anonymize='job-title']",
    "a[id^='job-title-']",
    "a.base-card__full-link",
    "h3 a",
    "a.job-title",
    "h3.base-search-card__title",
]

COMPANY_SELECTORS = [
    "h4 a",
    "a[data-tracking-control-name='public_jobs_jserp-result_search-card'] span",
    "span.job-card-container__primary-description",
    "a.job-card-container__company-name",
    "h4.base-search-card__subtitle",
    "[data-anonymize='company-name']",
    ".job-card-container__primary-description",
    "span[class*='company-name']",
]

LOCATION_SELECTORS = [
    "span.job-card-container__metadata-wrapper .bulleted",
    "span.job-card-container__metadata-wrapper",
    "span.job-search-card__location",
    ".base-search-card__metadata",
    "span[class*='location']",
    "[data-anonymize='location']",
    ".job-card-container__metadata-item",
]

DESC_SELECTORS = [
    "div.show-more-less-html__markup",
    "div.job-view-layout",
    "article.jobs-description__container",
    "#job-details",
    ".jobs-description-content",
    "div[class*='description']",
    "section.job-description",
]


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

            cards = await self._find_cards(page)
            if not cards:
                logger.warning("No se encontraron tarjetas de trabajo con ningún selector")
                await page.screenshot(path=f"data/linkedin_debug_{datetime.now():%Y%m%d_%H%M%S}.png")
                return results

            logger.info(f"Encontradas {len(cards)} tarjetas")
            cards = cards[:15]

            for card in cards:
                try:
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

    async def _find_cards(self, page: Page):
        for selector in JOB_CARD_SELECTORS:
            try:
                cards = await page.query_selector_all(selector)
                if cards and len(cards) > 0:
                    logger.info(f"Selector de tarjetas funcionando: '{selector}' → {len(cards)} cards")
                    return cards
            except Exception:
                continue
        return []

    async def _first_text(self, card: Page, selectors: list[str]) -> str:
        for sel in selectors:
            try:
                el = await card.query_selector(sel)
                if el:
                    text = await el.inner_text()
                    if text and text.strip():
                        return text.strip()
            except Exception:
                continue
        return ""

    async def _first_attr(self, card: Page, selectors: list[str], attr: str = "href") -> str:
        for sel in selectors:
            try:
                el = await card.query_selector(sel)
                if el:
                    val = await el.get_attribute(attr)
                    if val and val.strip():
                        return val.strip()
            except Exception:
                continue
        return ""

    async def _extract_job_data(self, page: Page, card) -> dict | None:
        result: dict = {
            "fuente": self.fuente,
            "link": "",
            "empresa": "",
            "cargo": "",
            "ubicacion": "",
            "descripcion": "",
        }

        link_sel = TITLE_SELECTORS + ["a[href*='/jobs/view']", "a.base-card__full-link"]
        link = await self._first_attr(card, link_sel)
        result["link"] = link.split("?")[0] if link and "?" in link else link or ""
        result["cargo"] = await self._first_text(card, TITLE_SELECTORS)
        result["empresa"] = await self._first_text(card, COMPANY_SELECTORS)
        result["ubicacion"] = await self._first_text(card, LOCATION_SELECTORS)

        if not result["cargo"] and not result["link"]:
            return None

        try:
            desc = None
            for sel in DESC_SELECTORS:
                try:
                    desc = await page.wait_for_selector(sel, timeout=3000)
                    if desc:
                        break
                except Exception:
                    continue
            if desc:
                result["descripcion"] = await desc.inner_text()
        except Exception:
            pass

        return result
