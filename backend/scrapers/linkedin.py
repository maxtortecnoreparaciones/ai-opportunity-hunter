import random
from playwright.async_api import Page
from backend.scrapers.base import BaseScraper


class LinkedInScraper(BaseScraper):
    platform_for_auth = "linkedin"

    @property
    def fuente(self) -> str:
        return "linkedin"

    async def scrape_keyword(self, keyword: str) -> list[dict]:
        results: list[dict] = []
        pw, browser, context = await self.with_browser()
        page = await context.new_page()

        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(random.randint(3000, 5000))

            cards = await page.query_selector_all("li[data-occludable-job-id]")
            cards = cards[:15]

            for card in cards:
                try:
                    await card.click()
                    await page.wait_for_timeout(random.randint(1500, 2500))
                    data = await self._extract_job_data(page, card)
                    if data and data.get("link"):
                        results.append(data)
                except Exception:
                    continue
        finally:
            await browser.close()
            await pw.stop()

        return results

    async def _extract_job_data(self, page: Page, card) -> dict | None:
        result: dict = {
            "fuente": self.fuente,
            "link": "",
            "empresa": "",
            "cargo": "",
            "ubicacion": "",
            "descripcion": "",
        }

        title_el = await card.query_selector(
            "a[data-tracking-control-name='public_jobs_jserp-result_search-card']"
        )
        if title_el:
            result["cargo"] = await title_el.inner_text()
            link = await title_el.get_attribute("href")
            result["link"] = link.split("?")[0] if link and "?" in link else link or ""

        empresa_el = await card.query_selector("h4 a")
        result["empresa"] = await empresa_el.inner_text() if empresa_el else ""

        ubic_el = await card.query_selector(
            "span.job-card-container__metadata-wrapper .bulleted"
        )
        result["ubicacion"] = await ubic_el.inner_text() if ubic_el else ""

        try:
            desc_el = await page.wait_for_selector(
                "div.show-more-less-html__markup", timeout=3000
            )
            result["descripcion"] = await desc_el.inner_text() if desc_el else ""
        except Exception:
            result["descripcion"] = ""

        return result
