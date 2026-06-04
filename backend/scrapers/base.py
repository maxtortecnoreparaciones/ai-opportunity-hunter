from abc import ABC, abstractmethod
from backend.models import JobOffer
from backend.auth.scraper_mixin import AuthenticatedScraperMixin


class BaseScraper(ABC, AuthenticatedScraperMixin):
    @property
    @abstractmethod
    def fuente(self) -> str: ...

    @abstractmethod
    async def scrape_keyword(self, keyword: str) -> list[dict]: ...

    async def scrape(self, keywords: list[str]) -> list[JobOffer]:
        raw_offers = []
        for kw in keywords:
            try:
                results = await self.scrape_keyword(kw)
                raw_offers.extend(results)
            except Exception as e:
                print(f"[{self.fuente}] Error scraping '{kw}': {e}")
        return [JobOffer(**o) for o in raw_offers]
