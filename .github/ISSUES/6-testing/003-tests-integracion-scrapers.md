---
title: "[TEST] Tests de integración para scrapers (Playwright)"
labels: ["test", "scraper", "playwright"]
milestone: "Fase 6 - Testing"
---

## Descripción

Escribir tests de integración para los scrapers de Playwright, probando la extracción de datos contra sitios reales o mockeados.

## Criterios de aceptación

- [ ] Test: LinkedIn scraper extrae al menos 1 oferta
- [ ] Test: Wellfound scraper extrae al menos 1 oferta
- [ ] Test: GetOnBoard scraper extrae al menos 1 oferta
- [ ] Test: normalizador unifica campos correctamente
- [ ] Test: exportación CSV genera archivo válido
- [ ] Test: manejo de errores (página no disponible, timeout)
- [ ] Usar fixtures de Playwright para navegador
- [ ] Marcar tests como `integration` para separar de unitarios

## Tiempo estimado

4 horas
