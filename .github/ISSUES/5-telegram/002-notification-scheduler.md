---
title: "[TELEGRAM] Implementar scheduler de notificaciones periódicas"
labels: ["telegram", "scheduler"]
milestone: "Fase 5 - Telegram"
---

## Descripción

Implementar un scheduler que ejecute el pipeline completo de búsqueda, análisis y notificación en intervalos regulares.

## Criterios de aceptación

- [ ] Ejecutar pipeline completo: scrape → analyze → notify
- [ ] Configurar intervalo vía variable de entorno (default: cada 6 horas)
- [ ] Enviar resumen diario con top 5 ofertas
- [ ] Evitar notificar ofertas ya enviadas
- [ ] Logging de cada ejecución del scheduler
- [ ] Manejar solapamiento (no ejecutar si ya está corriendo)

## Opciones de scheduler

- **APScheduler** para ejecución en proceso
- **Cron** + script Python para despliegue simple
- **GitHub Actions** como alternativa serverless

## Tiempo estimado

2 horas
