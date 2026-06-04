import random
from backend.scrapers.base import BaseScraper


class WellfoundScraper(BaseScraper):
    platform_for_auth = "wellfound"

    @property
    def fuente(self) -> str:
        return "wellfound"

    async def scrape_keyword(self, keyword: str) -> list[dict]:
        results: list[dict] = []
        pw, browser, context = await self.with_browser()
        page = await context.new_page()

        try:
            url = f"https://wellfound.com/role/{keyword.replace(' ', '-')}"
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(random.randint(3000, 5000))

            cards = await page.query_selector_all("a[data-test='SearchResultsItem']")
            cards = cards[:15]

            for card in cards:
                try:
                    data = await self._extract_job_data(card)
                    if data:
                        results.append(data)
                except Exception:
                    continue
        finally:
            await browser.close()
            await pw.stop()

        return results

    async def _extract_job_data(self, card) -> dict | None:
        result: dict = {
            "fuente": self.fuente,
            "link": "",
            "empresa": "",
            "cargo": "",
            "ubicacion": "",
            "descripcion": "",
        }

        title_el = await card.query_selector("div[class*='name']")
        result["cargo"] = await title_el.inner_text() if title_el else ""

        company_el = await card.query_selector("div[class*='company-name']")
        result["empresa"] = await company_el.inner_text() if company_el else ""

        meta_el = await card.query_selector("div[class*='meta']")
        result["ubicacion"] = await meta_el.inner_text() if meta_el else ""

        link = await card.get_attribute("href")
        result["link"] = f"https://wellfound.com{link}" if link else ""

        desc_el = await card.query_selector("div[class*='description']")
        result["descripcion"] = await desc_el.inner_text() if desc_el else ""

        return result
