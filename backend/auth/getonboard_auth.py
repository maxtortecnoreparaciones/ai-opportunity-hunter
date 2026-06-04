"""Autenticador para GetOnBoard."""

from playwright.async_api import Page
from backend.auth.authenticator import BaseAuthenticator


class GetOnBoardAuthenticator(BaseAuthenticator):
    @property
    def platform(self) -> str:
        return "getonboard"

    @property
    def login_url(self) -> str:
        return "https://www.getonbrd.com/webpros/login"

    async def _on_page_ready(self, page: Page) -> None:
        await page.wait_for_selector(
            "a[href*='google_oauth2'], a[href*='auth/linkedin'], a[href*='auth/github'], #magic-link",
            timeout=15000,
        )
