from dataclasses import dataclass, field
from backend.models import JobOffer, Profile, AnalysisResult


@dataclass
class ScoredOffer:
    offer: JobOffer
    analysis: AnalysisResult
    score_final: float
    clasificacion: str = "Regular"


class ScoringEngine:
    def __init__(self, threshold: float = 7.0):
        self.threshold = threshold

    def score(self, offer: JobOffer, profile: Profile, analysis: AnalysisResult) -> ScoredOffer:
        score_ia = analysis.score
        score_perfil = self._calc_profile_match(offer, profile)
        score_final = score_ia * 0.6 + score_perfil * 0.4
        score_final = round(min(max(score_final, 0), 10), 1)

        clasificacion = self._classify(score_final)
        return ScoredOffer(offer=offer, analysis=analysis, score_final=score_final, clasificacion=clasificacion)

    def _calc_profile_match(self, offer: JobOffer, profile: Profile) -> float:
        tec_perfil = set(t.strip().lower() for t in profile.tecnologias.split(","))
        tec_oferta = set(t.strip().lower() for t in offer.descripcion.split())
        comunes = tec_perfil & tec_oferta
        if not tec_oferta:
            return 5.0
        return min(10.0, (len(comunes) / max(len(tec_perfil), 1)) * 10)

    def _classify(self, score: float) -> str:
        if score >= 9.0:
            return "Excelente"
        if score >= 7.5:
            return "Buena"
        if score >= 5.0:
            return "Regular"
        return "Descartada"

    def filter_best(self, scored: list[ScoredOffer]) -> list[ScoredOffer]:
        return [s for s in scored if s.score_final >= self.threshold]

    def top_n(self, scored: list[ScoredOffer], n: int = 5) -> list[ScoredOffer]:
        sorted_list = sorted(scored, key=lambda x: x.score_final, reverse=True)
        return sorted_list[:n]
