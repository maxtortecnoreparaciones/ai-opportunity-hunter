---
title: "[TEST] Configurar pytest, coverage y CI con GitHub Actions"
labels: ["test", "ci"]
milestone: "Fase 6 - Testing"
---

## Descripción

Configurar el entorno de testing con pytest, medición de cobertura y automatización en CI con GitHub Actions.

## Criterios de aceptación

- [ ] Configurar `pytest` con `pytest-asyncio` para tests async
- [ ] Configurar `pytest-cov` para cobertura (mínimo 70%)
- [ ] Separar tests unitarios de integración con markers
- [ ] Crear `conftest.py` con fixtures globales
- [ ] Crear GitHub Actions workflow para CI
- [ ] Ejecutar tests en cada push y PR
- [ ] Reporte de cobertura en PR comments o artifact
- [ ] Linting con ruff o flake8 en CI

## Estructura esperada

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=backend --cov-report=term-missing -m "not integration"
```

## Tiempo estimado

3 horas
