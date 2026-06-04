import json
from backend.models import JobOffer, Profile, AnalysisResult
from backend.config import settings
from backend.ai.base import BaseAnalyzer


class OpenAIAnalyzer(BaseAnalyzer):
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ):
        self.base_url = (base_url or settings.openai_base_url).rstrip("/")
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model or self._detect_model()
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    base_url=self.base_url,
                    api_key=self.api_key,
                )
            except ImportError:
                raise ImportError("openai no instalado. pip install openai")
        return self._client

    def _detect_model(self) -> str:
        try:
            models = self.client.models.list()
            for m in models:
                name = m.id if hasattr(m, 'id') else m
                if isinstance(name, str) and name.strip():
                    return name
            return "local-model"
        except Exception:
            return "local-model"

    async def analyze(self, offer: JobOffer, profile: Profile) -> AnalysisResult:
        prompt = self._build_prompt(offer, profile)
        response = await self._call(prompt)
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

    async def _call(self, prompt: str) -> str:
        import asyncio
        loop = asyncio.get_event_loop()

        def sync_call():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=512,
            )
            return response.choices[0].message.content or ""

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
