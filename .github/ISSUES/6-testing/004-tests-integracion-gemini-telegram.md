---
title: "[TEST] Tests de integración para Gemini y Telegram"
labels: ["test", "ai", "telegram"]
milestone: "Fase 6 - Testing"
---

## Descripción

Escribir tests de integración para los módulos de Gemini API y Telegram Bot.

## Criterios de aceptación

### Gemini
- [ ] Test: API key válida responde correctamente
- [ ] Test: prompt genera respuesta JSON parseable
- [ ] Test: manejo de error con API key inválida
- [ ] Test: timeout en API lenta

### Telegram
- [ ] Test: envío de mensaje a chat válido
- [ ] Test: formato del mensaje es correcto
- [ ] Test: manejo de error con token inválido
- [ ] Test: envío fallido no detiene el pipeline

### General
- [ ] Tests marcados como `integration` y `slow`
- [ ] Saltar tests de integración si faltan API keys
- [ ] Mock de servicios externos para tests unitarios

## Tiempo estimado

3 horas
