from abc import ABC, abstractmethod
from backend.models import JobOffer, Profile, AnalysisResult


class BaseAnalyzer(ABC):
    @abstractmethod
    async def analyze(self, offer: JobOffer, profile: Profile) -> AnalysisResult:
        ...
