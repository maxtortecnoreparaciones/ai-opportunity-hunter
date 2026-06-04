---
title: "[SCRAPER] Implementar scraper de GetOnBoard"
labels: ["scraper", "playwright"]
milestone: "Fase 2 - Scrapers"
---

## Descripción

Implementar scraper que extraiga ofertas de empleo desde GetOnBoard usando Playwright.

## Criterios de aceptación

- [ ] Navegar GetOnBoard y buscar por keywords
- [ ] Extraer: empresa, cargo, ubicación, salario, link, descripción
- [ ] Manejar paginación
- [ ] Rate limiting y manejo de errores
- [ ] Retornar lista de diccionarios normalizados

## Estructura esperada

```python
# backend/scrapers/getonboard.py
class GetOnBoardScraper:
    async def scrape(self, keywords: list[str]) -> list[dict]: ...
```

## Tiempo estimado

4 horas
