"""Mixins para que los scrapers usen sesiones autenticadas.

Proporciona un context manager que crea un contexto de Playwright
con la sesión guardada (si existe) para cada plataforma.
"""

from playwright.async_api import async_playwright
from backend.auth import SessionStorage


class AuthenticatedScraperMixin:
    """Mixin para scrapers que necesitan sesión autenticada.

    Se usa en lugar de crear el context manualmente.
    Llama a `with_browser()` para obtener un page autenticado.
    """

    platform_for_auth: str = ""

    async def with_browser(self):
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=True)

        storage = SessionStorage(self.platform_for_auth or self.fuente)
        state = storage.load()

        if state:
            context = await browser.new_context(storage_state=state)
        else:
            context = await browser.new_context()

        return pw, browser, context
