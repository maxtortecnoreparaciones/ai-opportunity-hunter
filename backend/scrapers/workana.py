import random
import re
from backend.scrapers.base import BaseScraper


class WorkanaScraper(BaseScraper):
    platform_for_auth = "workana"

    @property
    def fuente(self) -> str:
        return "workana"

    async def scrape_keyword(self, keyword: str) -> list[dict]:
        results: list[dict] = []
        pw, browser, context = await self.with_browser()
        page = await context.new_page()
        page.set_default_timeout(30000)

        try:
            url = f"https://www.workana.com/jobs?language=es&q={keyword.replace(' ', '+')}"
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(random.randint(3000, 5000))

            cards = await page.query_selector_all("div.project-item")
            if not cards:
                cards = await page.query_selector_all(".js-project")

            for card in cards:
                try:
                    data = await self._extract_job_data(card)
                    if data and data.get("link"):
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
            "salario_min": None,
            "salario_max": None,
            "moneda": None,
        }

        title_el = await card.query_selector("h2.project-title a")
        if title_el:
            href = await title_el.get_attribute("href")
            result["link"] = f"https://www.workana.com{href}" if href and href.startswith("/") else href or ""
            result["cargo"] = (await title_el.inner_text()).strip()

        desc_el = await card.query_selector(".html-desc .text-expander-content span")
        if not desc_el:
            desc_el = await card.query_selector(".project-details")
        if desc_el:
            result["descripcion"] = (await desc_el.inner_text()).strip()

        author_el = await card.query_selector(".project-author .user-name span")
        if author_el:
            result["empresa"] = (await author_el.inner_text()).strip()
        if not result["empresa"]:
            author_el = await card.query_selector(".author-info button span")
            if author_el:
                result["empresa"] = (await author_el.inner_text()).strip()

        country_el = await card.query_selector(".country .country-name a")
        if country_el:
            result["ubicacion"] = (await country_el.inner_text()).strip()

        budget_el = await card.query_selector(".budget .values span")
        if budget_el:
            budget_text = (await budget_el.inner_text()).strip()
            result = self._parse_budget(budget_text, result)

        return result

    def _parse_budget(self, text: str, result: dict) -> dict:
        text_clean = text.replace(",", "").replace(".", "")
        nums = re.findall(r"\d+", text_clean)
        if len(nums) >= 2:
            result["salario_min"] = nums[0]
            result["salario_max"] = nums[1]
        elif len(nums) == 1:
            result["salario_min"] = nums[0]
        currency_match = re.search(r"(USD|EUR|CLP|MXN|COP|BRL|PEN|ARS)", text, re.IGNORECASE)
        if currency_match:
            result["moneda"] = currency_match.group(1).upper()
        return result
