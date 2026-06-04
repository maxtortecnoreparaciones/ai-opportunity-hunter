from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from playwright.async_api import Page
from backend.auth.session import SessionManager
from backend.captcha.detector import CaptchaDetector
from backend.captcha.handler import CaptchaHandler


@dataclass
class ProfileData:
    headline: Optional[str] = None
    about: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[list[str]] = None


class BaseProfileUpdater(ABC):
    def __init__(self, session_manager: SessionManager):
        self.session = session_manager
        self.captcha_detector = CaptchaDetector()
        self.captcha_handler = CaptchaHandler()

    @abstractmethod
    async def update_profile(self, data: ProfileData) -> bool: ...

    async def _handle_captcha(self, page: Page) -> bool:
        detected = await self.captcha_detector.detect(page)
        if detected:
            print(f"[{self.__class__.__name__}] CAPTCHA detectado: {detected}")
            return await self.captcha_handler.handle(page, detected)
        return True

    @abstractmethod
    async def login(self, page: Page) -> bool: ...
