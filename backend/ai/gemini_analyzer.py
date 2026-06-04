import json
from backend.models import JobOffer, Profile, AnalysisResult
from backend.config import settings
from backend.ai.base import BaseAnalyzer


class QuotaExceededError(Exception):
    pass


class GeminiAnalyzer(BaseAnalyzer):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except ImportError:
                raise ImportError("google.genai no instalado. pip install google-genai")
        return self._client

    async def analyze(self, offer: JobOffer, profile: Profile) -> AnalysisResult:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no configurada")

        prompt = self._build_prompt(offer, profile)
        response = await self._call_gemini(prompt)
        return self._parse_response(response)

    def _build_prompt(self, offer: JobOffer, profile: Profile) -> str:
        return f"""Eres un reclutador experto evaluando compatibilidad laboral.

Perfil del candidato:
- Tecnologías: {profile.tecnologias}
- Experiencia: {profile.experiencia_anos} años
- Inglés: {profile.nivel_ingles}
- Seniority: {profile.seniority}

Oferta:
Cargo: {offer.cargo}
Empresa: {offer.empresa}
Descripción: {offer.descripcion[:2000]}

Responde SOLO en JSON sin markdown:
{{"score": 8.5, "fortalezas": ["Python", "Docker"], "debilidades": ["Kubernetes"], "recomendacion": "Buena opción, pero necesitará capacitación en K8s"}}"""

    async def _call_gemini(self, prompt: str) -> str:
        import asyncio
        loop = asyncio.get_event_loop()

        def sync_call():
            try:
                return self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                ).text
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    raise QuotaExceededError(
                        "Cuota diaria de Gemini agotada. Espera a que se resetee o usa otra API key."
                    ) from e
                raise

        return await loop.run_in_executor(None, sync_call)

    def _parse_response(self, text: str) -> AnalysisResult:
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1])

        data = json.loads(text)
        return AnalysisResult(
            score=float(data.get("score", 0)),
            fortalezas=data.get("fortalezas", []),
            debilidades=data.get("debilidades", []),
            recomendacion=data.get("recomendacion", ""),
        )
