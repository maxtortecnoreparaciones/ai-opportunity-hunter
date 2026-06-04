import random
import re
from backend.scrapers.base import BaseScraper


class GetOnBoardScraper(BaseScraper):
    platform_for_auth = "getonboard"

    @property
    def fuente(self) -> str:
        return "getonboard"

    async def scrape_keyword(self, keyword: str) -> list[dict]:
        results: list[dict] = []
        pw, browser, context = await self.with_browser()
        page = await context.new_page()

        try:
            url = f"https://www.getonbrd.com/jobs?q={keyword.replace(' ', '+')}"
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(random.randint(3000, 5000))

            cards = await page.query_selector_all("a.results-item")
            cards = cards[:20]

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

        link = await card.get_attribute("href")
        result["link"] = (
            f"https://www.getonbrd.com{link}" if link and link.startswith("/") else link or ""
        )

        title_el = await card.query_selector("h4.results-list-title strong")
        if title_el:
            result["cargo"] = (await title_el.inner_text()).strip()

        company_el = await card.query_selector(".results-list-info .size0 strong")
        if not company_el:
            company_el = await card.query_selector(
                ".results-list-info strong:not(.pr-3)"
            )
        if company_el:
            result["empresa"] = (await company_el.inner_text()).strip()

        location_el = await card.query_selector("span.location")
        if location_el:
            result["ubicacion"] = (await location_el.inner_text()).strip()

        salary_el = await card.query_selector(".icon-money-bill + span")
        if not salary_el:
            salary_parent = await card.query_selector(
                ".gb-results-list__badges div:last-child span"
            )
            if salary_parent:
                salary_el = salary_parent
        if salary_el:
            salary_text = (await salary_el.inner_text()).strip()
            result = self._parse_salary(salary_text, result)

        return result

    def _parse_salary(self, text: str, result: dict) -> dict:
        text_clean = text.replace(",", "").replace(".", "")
        parts = text_clean.split()
        nums = [p for p in parts if p.isdigit()]
        if len(nums) >= 2:
            result["salario_min"] = nums[0]
            result["salario_max"] = nums[1]
        elif len(nums) == 1:
            result["salario_min"] = nums[0]
        currency_match = re.search(
            r"(USD|EUR|CLP|MXN|COP|BRL|PEN)", text, re.IGNORECASE
        )
        if currency_match:
            result["moneda"] = currency_match.group(1).upper()
        return result
