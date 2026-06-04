"""Autenticador para Wellfound (AngelList)."""

from backend.auth.authenticator import BaseAuthenticator


class WellfoundAuthenticator(BaseAuthenticator):
    @property
    def platform(self) -> str:
        return "wellfound"

    @property
    def login_url(self) -> str:
        return "https://wellfound.com/login"
