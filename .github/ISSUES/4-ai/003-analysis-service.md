---
title: "[AI] Crear AnalysisService para orquestar análisis"
labels: ["ai", "service"]
milestone: "Fase 4 - IA"
---

## Descripción

Crear el servicio que orquesta el flujo completo de análisis: tomar ofertas nuevas, analizar con Gemini, calcular score y guardar resultados.

## Criterios de aceptación

- [ ] `process_new_offers()`: analiza ofertas no procesadas
- [ ] `analyze_offer(offer_id, profile_id)`: analiza una oferta específica
- [ ] `get_top_opportunities(n=5)`: retorna las mejores oportunidades
- [ ] Integrar con repositories para guardar análisis
- [ ] Evitar re-análisis de ofertas ya procesadas
- [ ] Logging de cada paso del proceso

## Flujo

```
1. Obtener ofertas no analizadas desde JobOfferRepository
2. Para cada oferta:
   a. Llamar GeminiAnalyzer
   b. Llamar ScoringEngine
   c. Guardar Analysis en DB via AnalysisRepository
3. Retornar scored offers list
```

## Tiempo estimado

3 horas
