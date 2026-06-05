from .base import BaseScraper

__all__ = ["BaseScraper"]


def _import_scrapers():
    from .linkedin import LinkedInScraper
    from .wellfound import WellfoundScraper
    from .getonboard import GetOnBoardScraper
    from .workana import WorkanaScraper
    from .computrabajo import ComputrabajoScraper
    from .normalizer import JobNormalizer
    return LinkedInScraper, WellfoundScraper, GetOnBoardScraper, WorkanaScraper, ComputrabajoScraper, JobNormalizer


LinkedInScraper, WellfoundScraper, GetOnBoardScraper, WorkanaScraper, ComputrabajoScraper, JobNormalizer = _import_scrapers()
