from .base import BaseScraper

__all__ = ["BaseScraper"]


def _import_scrapers():
    from .linkedin import LinkedInScraper
    from .wellfound import WellfoundScraper
    from .getonboard import GetOnBoardScraper
    from .normalizer import JobNormalizer
    return LinkedInScraper, WellfoundScraper, GetOnBoardScraper, JobNormalizer


LinkedInScraper, WellfoundScraper, GetOnBoardScraper, JobNormalizer = _import_scrapers()
