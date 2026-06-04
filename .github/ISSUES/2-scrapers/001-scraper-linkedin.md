---
title: "[SCRAPER] Implementar scraper de LinkedIn"
labels: ["scraper", "playwright"]
milestone: "Fase 2 - Scrapers"
---

## Descripción

Implementar scraper que extraiga ofertas de empleo desde LinkedIn usando Playwright.

## Criterios de aceptación

- [ ] Navegar LinkedIn Jobs y buscar por keywords predefinidas
- [ ] Extraer: empresa, cargo, ubicación, link y descripción
- [ ] Manejar paginación (mínimo 3 páginas)
- [ ] Rate limiting: 2-3 segundos entre requests
- [ ] Manejar errores de conexión y timeouts
- [ ] Respetar robots.txt
- [ ] Retornar lista de diccionarios normalizados

## Estructura esperada

```python
# backend/scrapers/linkedin.py
class LinkedInScraper:
    async def scrape(self, keywords: list[str]) -> list[dict]: ...
```

## Salida esperada (MVP #1: CSV)

```csv
empresa,cargo,ubicacion,link,descripcion,fuente
MixRank,Senior Python Developer,Remote,https://...,"...",linkedin
```

## Dependencias

- Playwright instalado
- Navegador Chromium descargado

## Tiempo estimado

6 horas
