from .base import BaseScraper

__all__ = ["BaseScraper"]


def _import_scrapers():
    from .linkedin import LinkedInScraper
    from .wellfound import WellfoundScraper
    from .getonboard import GetOnBoardScraper
    from .workana import WorkanaScraper
    from .normalizer import JobNormalizer
    return LinkedInScraper, WellfoundScraper, GetOnBoardScraper, WorkanaScraper, JobNormalizer


LinkedInScraper, WellfoundScraper, GetOnBoardScraper, WorkanaScraper, JobNormalizer = _import_scrapers()
