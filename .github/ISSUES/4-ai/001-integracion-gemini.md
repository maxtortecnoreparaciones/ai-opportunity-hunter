---
title: "[AI] Integrar Gemini API para análisis de compatibilidad"
labels: ["ai", "gemini"]
milestone: "Fase 4 - IA"
---

## Descripción

Integrar la API de Google Gemini para analizar la compatibilidad entre una oferta de empleo y el perfil del usuario.

## Criterios de aceptación

- [ ] Configurar cliente Gemini con API key desde variable de entorno
- [ ] Construir prompt estructurado con: perfil del usuario + descripción de la oferta
- [ ] Parsear respuesta JSON: score (0-10), fortalezas, debilidades, recomendación
- [ ] Manejar errores de API (timeouts, rate limits, tokens)
- [ ] Cache de análisis para evitar re-procesar ofertas ya analizadas

## Ejemplo de prompt

```
Eres un reclutador experto evaluando compatibilidad laboral.

Perfil del candidato:
- Tecnologías: Python, FastAPI, PostgreSQL, Docker, AWS
- Experiencia: 5 años
- Inglés: Avanzado

Oferta:
{cargo} en {empresa}
Descripción: {descripcion}

Responde SOLO en JSON:
{"score": 8.5, "fortalezas": [...], "debilidades": [...], "recomendacion": "..."}
```

## Estructura esperada

```python
# backend/ai/gemini_analyzer.py
class GeminiAnalyzer:
    async def analyze(self, offer: JobOffer, profile: Profile) -> AnalysisResult: ...
```

## Tiempo estimado

4 horas
