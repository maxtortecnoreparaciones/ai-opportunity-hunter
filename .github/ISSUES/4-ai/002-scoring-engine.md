---
title: "[AI] Implementar Scoring Engine para clasificar ofertas"
labels: ["ai", "scoring"]
milestone: "Fase 4 - IA"
---

## Descripción

El Scoring Engine toma el análisis de Gemini y aplica lógica adicional para clasificar y filtrar ofertas.

## Criterios de aceptación

- [ ] Combinar score de IA con reglas adicionales (e.g., experiencia mínima, ubicación)
- [ ] Aplicar umbral configurable (`SCORE_THRESHOLD`, default: 7.0)
- [ ] Clasificar ofertas en: "Excelente", "Buena", "Regular", "Descartada"
- [ ] Ordenar resultados por score descendente
- [ ] Exponer método `get_top_offers(n: int) -> list[ScoredOffer]`

## Reglas de scoring

- Score IA (Gemini): 60% del peso total
- Experiencia requerida vs perfil: 20%
- Ubicación (remoto = bonus): 10%
- Tecnologías requeridas vs perfil: 10%

## Estructura esperada

```python
# backend/ai/scoring_engine.py
class ScoringEngine:
    async def score_offer(self, offer: JobOffer, profile: Profile) -> ScoredOffer: ...
    async def get_top_offers(self, offers: list[JobOffer], profile: Profile, n: int = 5) -> list[ScoredOffer]: ...
```

## Tiempo estimado

3 horas
