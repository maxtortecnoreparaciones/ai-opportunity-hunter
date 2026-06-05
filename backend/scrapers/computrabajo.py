import re
from backend.scrapers.base import BaseScraper


class ComputrabajoScraper(BaseScraper):
    platform_for_auth = "computrabajo"

    @property
    def fuente(self) -> str:
        return "computrabajo"

    async def _make_context(self):
        from playwright.async_api import async_playwright
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="es-CO",
        )
        return pw, browser, context

    async def scrape_keyword(self, keyword: str) -> list[dict]:
        results: list[dict] = []
        pw, browser, context = await self._make_context()
        page = await context.new_page()
        page.set_default_timeout(30000)

        try:
            kw = keyword.replace(" ", "-").lower()
            url = f"https://co.computrabajo.com/trabajo-de-{kw}"
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            cards = await page.query_selector_all("article.box_offer")
            if not cards:
                return results

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

        data = await card.evaluate("""
            (el) => {
                const get = (sel) => {
                    const e = el.querySelector(sel);
                    return e ? e.textContent.trim() : "";
                };
                const getAttr = (sel, attr) => {
                    const e = el.querySelector(sel);
                    return e ? (e.getAttribute(attr) || "") : "";
                };

                const link = getAttr("h2 a.js-o-link", "href") || "";
                const fullLink = link.startsWith("/")
                    ? "https://co.computrabajo.com" + link.split("#")[0]
                    : link.split("#")[0];

                const paragraphs = el.querySelectorAll("p.fs16.fc_base.mt5");
                let ubicacion = "";
                for (const p of paragraphs) {
                    if (!p.classList.contains("dFlex")) {
                        const sp = p.querySelector("span.mr10");
                        if (sp) ubicacion = sp.textContent.trim();
                        break;
                    }
                }

                const salaryEl = el.querySelector(".icon.i_salary");
                let salario = "";
                if (salaryEl && salaryEl.parentElement) {
                    salario = salaryEl.parentElement.textContent.trim();
                }

                return {
                    cargo: get("h2 a.js-o-link"),
                    link: fullLink,
                    empresa: getAttr("a[offer-grid-article-company-url]", "href")
                        .split("/").pop() || get("a[offer-grid-article-company-url]"),
                    empresaNombre: get("a[offer-grid-article-company-url]"),
                    ubicacion: ubicacion,
                    salario_text: salario,
                };
            }
        """)

        if data:
            result["cargo"] = data.get("cargo", "")
            result["link"] = data.get("link", "")
            result["empresa"] = data.get("empresaNombre", "")
            result["ubicacion"] = data.get("ubicacion", "")
            salary_text = data.get("salario_text", "")
            if salary_text:
                result = self._parse_salary(salary_text, result)

        return result

    def _parse_salary(self, text: str, result: dict) -> dict:
        match = re.search(r"\d[\d.]*", text)
        if match:
            clean = match.group().replace(".", "")
            result["salario_min"] = clean
            result["moneda"] = "COP"
        return result
