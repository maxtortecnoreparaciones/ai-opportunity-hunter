---
title: "[SCRAPER] MVP #1: Exportar datos de scrapers a CSV"
labels: ["scraper", "mvp"]
milestone: "Fase 2 - Scrapers"
---

## Descripción

Implementar el pipeline mínimo del MVP #1: los scrapers recolectan ofertas y las guardan en un archivo CSV. Sin IA, sin Telegram, sin PostgreSQL.

## Criterios de aceptación

- [ ] Ejecutar todos los scrapers secuencialmente
- [ ] Normalizar datos al esquema unificado
- [ ] Guardar resultados en `data/ofertas_<fecha>.csv`
- [ ] Mostrar resumen en consola: "Se encontraron X ofertas de Y portales"
- [ ] Manejar errores para que un scraper fallido no detenga los demás

## Estructura esperada

```python
# backend/scrapers/main.py
async def run_pipeline(keywords: list[str], output: str = "data/ofertas.csv"):
    scrapers = [LinkedInScraper(), WellfoundScraper(), GetOnBoardScraper()]
    # ejecutar, normalizar, exportar a CSV
```

## Uso esperado

```bash
python -m backend.scrapers.main --keywords "python developer,backend engineer" --output data/ofertas.csv
```

## Tiempo estimado

3 horas
