---
title: "[SCRAPER] Implementar scraper de Wellfound (AngelList)"
labels: ["scraper", "playwright"]
milestone: "Fase 2 - Scrapers"
---

## Descripción

Implementar scraper que extraiga ofertas de empleo desde Wellfound (anteriormente AngelList) usando Playwright.

## Criterios de aceptación

- [ ] Navegar Wellfound Jobs y buscar por keywords predefinidas
- [ ] Extraer: empresa, cargo, ubicación, salario, link
- [ ] Manejar paginación
- [ ] Rate limiting y manejo de errores
- [ ] Retornar lista de diccionarios normalizados

## Estructura esperada

```python
# backend/scrapers/wellfound.py
class WellfoundScraper:
    async def scrape(self, keywords: list[str]) -> list[dict]: ...
```

## Tiempo estimado

4 horas
